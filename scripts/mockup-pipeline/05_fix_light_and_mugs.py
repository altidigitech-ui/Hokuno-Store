"""Regenerate mockups for LIGHT products (bg replacement) and ALL mugs (new angle).

Bug 1 (light products) — rembg eats the white cotton t-shirt along with the white BG.
                        Fix: bg-replacement (compose_light) instead of detourage.

Bug 2 (mugs) — Printify 'front' default hides the design behind the handle.
              Fix: pick a design-visible angle by mockup template ID.

Targets:
    - Light products: title NOT containing NOIR / DARK / BLACK  → compose_light
    - All mugs (whether light or dark):
        - light mug → compose_light + new angle
        - dark mug  → rembg + new angle
    - Skip everything else (dark t-shirts already perfect — user explicit).

A preview grid is generated (4 light tees + 4 mugs) for visual validation.
NO push is done — the script stops before pushing so the user can validate.

Run from the repo root:
    python scripts/mockup-pipeline/05_fix_light_and_mugs.py
    python scripts/mockup-pipeline/05_fix_light_and_mugs.py --dry-run   # plan only
    python scripts/mockup-pipeline/05_fix_light_and_mugs.py --preview-only
"""
from __future__ import annotations

import datetime
import json
import re
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from PIL import Image, ImageDraw, ImageFont  # noqa: E402

import config  # noqa: E402
import printify_client  # noqa: E402
import collection_detector  # noqa: E402
import mockup_selector  # noqa: E402
import detourage  # noqa: E402
import compositing  # noqa: E402


PRODUCT_CARD = config.SHOPIFY_SNIPPETS_DIR / "product-card.liquid"
PRODUCT_TEMPLATE = config.SHOPIFY_THEME_DIR / "templates" / "product.liquid"

LIST_START = "{%- comment -%}HOKUNO-MOCKUP-LIST:START (auto-géré){%- endcomment -%}"
LIST_END = "{%- comment -%}HOKUNO-MOCKUP-LIST:END{%- endcomment -%}"
LIST_RE = re.compile(
    re.escape(LIST_START) + r"[\s\S]*?" + re.escape(LIST_END),
    re.MULTILINE,
)


def normalize_handle(raw: str | None) -> str | None:
    if not raw:
        return None
    h = raw.rstrip("/").split("/products/")[-1]
    return h.split("?", 1)[0].split("#", 1)[0] or None


def is_target(product: dict) -> tuple[bool, str]:
    """Return (is_target, reason)."""
    ptype = mockup_selector.detect_product_type(product)
    if ptype == "mug":
        return True, "mug"
    if mockup_selector.is_light_product(product):
        return True, "light"
    return False, "dark-non-mug (skip)"


def regenerate(product: dict) -> dict:
    pid = product["id"]
    title = product.get("title", "")
    ptype = mockup_selector.detect_product_type(product)
    collection = collection_detector.detect_collection(product)
    is_light = mockup_selector.is_light_product(product)
    handle = normalize_handle((product.get("external") or {}).get("handle"))

    log = {
        "product_id": pid,
        "title": title,
        "collection": collection,
        "type": ptype,
        "handle": handle,
        "is_light": is_light,
        "strategy": None,
        "mockup_position_used": None,
        "mockup_angle_id": None,
        "asset": None,
        "duration_s": None,
        "error": None,
    }

    t0 = time.time()

    if not handle:
        log["error"] = "external.handle missing"
        return log

    bg_path = config.BG_BY_COLLECTION.get(collection)
    if not bg_path or not bg_path.exists():
        log["error"] = f"bg missing for collection {collection!r}"
        return log

    try:
        img_meta = mockup_selector.pick_source_mockup(product, ptype)
    except Exception as e:  # noqa: BLE001
        log["error"] = f"mockup pick failed: {e}"
        return log

    src_url = img_meta.get("src", "")
    log["mockup_position_used"] = img_meta.get("position")
    # Best-effort extract angle id from URL (.../variant/angle/...)
    m = re.search(r"/mockup/[a-z0-9]+/[0-9]+/([0-9]+)/", src_url)
    if m:
        log["mockup_angle_id"] = m.group(1)

    try:
        raw_bytes = printify_client.download_image(src_url)
        raw_path = config.RAW_DIR / f"{pid}.png"
        raw_path.write_bytes(raw_bytes)

        dst = config.SHOPIFY_ASSETS_DIR / f"mockup-{handle}.webp"
        if is_light:
            log["strategy"] = "compose_light (bg replacement)"
            compositing.compose_light(raw_bytes, bg_path, dst)
        else:
            log["strategy"] = "rembg + compose"
            det = detourage.detoure(raw_bytes)
            det_path = config.DETOURED_DIR / f"{pid}.png"
            det.save(det_path, "PNG")
            compositing.compose(det, bg_path, ptype, dst)

        # Mirror in 03-final/ for traceability
        (config.FINAL_DIR / f"{pid}.webp").write_bytes(dst.read_bytes())

        log["asset"] = str(dst.relative_to(config.REPO_ROOT))
        log["duration_s"] = round(time.time() - t0, 2)
        return log
    except Exception as e:  # noqa: BLE001
        log["error"] = f"{type(e).__name__}: {e}"
        log["duration_s"] = round(time.time() - t0, 2)
        return log


def build_preview(picks: list[Path], labels: list[str], output: Path):
    if not picks:
        return
    cell = 600
    cols = 4
    rows = max(1, (len(picks) + cols - 1) // cols)
    grid = Image.new("RGB", (cols * cell, rows * (cell + 40)), "white")
    try:
        font = ImageFont.truetype(
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 16
        )
    except OSError:
        font = ImageFont.load_default()
    for i, (p, lbl) in enumerate(zip(picks, labels)):
        img = Image.open(p).convert("RGB").resize((cell, cell), Image.LANCZOS)
        r, c = divmod(i, cols)
        grid.paste(img, (c * cell, r * (cell + 40) + 40))
        ImageDraw.Draw(grid).text(
            (c * cell + 10, r * (cell + 40) + 10),
            lbl[:80],
            fill="black",
            font=font,
        )
    grid.save(output, "PNG")


def existing_handles(path: Path) -> list[str]:
    if not path.exists():
        return []
    m = LIST_RE.search(path.read_text())
    if not m:
        return []
    return re.findall(r'append:\s*"([^",]+),"', m.group(0))


def write_handles(path: Path, indent: str, handles: list[str]) -> None:
    src = path.read_text()
    m = LIST_RE.search(src)
    if not m:
        raise RuntimeError(f"{path}: HOKUNO-MOCKUP-LIST markers missing")
    lines = [f"{indent}{LIST_START}", f'{indent}{{%- assign mockup_handles = "" -%}}']
    for h in handles:
        lines.append(
            f'{indent}{{%- assign mockup_handles = mockup_handles | append: "{h}," -%}}'
        )
    lines.append(f"{indent}{LIST_END}")
    path.write_text(LIST_RE.sub("\n".join(lines), src, count=1))


def sync_theme_list() -> int:
    """Make sure both Liquid files list every asset currently on disk."""
    handles_in_assets = sorted(
        p.stem.removeprefix("mockup-")
        for p in config.SHOPIFY_ASSETS_DIR.glob("mockup-*.webp")
    )
    current = existing_handles(PRODUCT_CARD)
    seen = set(current)
    merged = current + [h for h in handles_in_assets if h not in seen]
    write_handles(PRODUCT_CARD, indent="    ", handles=merged)
    write_handles(PRODUCT_TEMPLATE, indent="      ", handles=merged)
    return len(merged)


def run() -> int:
    dry_run = "--dry-run" in sys.argv
    preview_only = "--preview-only" in sys.argv

    config.ensure_dirs()
    config.require_printify_token()

    print("→ Fetching all Printify products…")
    products = printify_client.list_all_products()
    print(f"  {len(products)} products fetched")

    targets = []
    for p in products:
        ok, _ = is_target(p)
        if ok:
            targets.append(p)

    # Stats
    n_mug = sum(1 for p in targets if mockup_selector.detect_product_type(p) == "mug")
    n_light_nonmug = sum(
        1
        for p in targets
        if mockup_selector.detect_product_type(p) != "mug"
        and mockup_selector.is_light_product(p)
    )
    print(f"\n=== Cible : {len(targets)} produits ===")
    print(f"  - Mugs (all blueprints)            : {n_mug}")
    print(f"  - Light products (non-mug)         : {n_light_nonmug}")
    print(f"  - Total                            : {len(targets)}")
    print(f"  - SKIP (dark non-mug, déjà parfaits): {len(products) - len(targets)}")

    if dry_run:
        print("\n(dry-run) Nothing to regenerate. Exit.")
        return 0

    if preview_only:
        # Just rebuild preview from current assets
        _make_preview_from_current(targets)
        return 0

    started = datetime.datetime.now()
    logs: list[dict] = []
    for i, p in enumerate(targets, 1):
        log = regenerate(p)
        tag = "ERROR" if log["error"] else "OK"
        col = log.get("collection", "?")
        title = (log.get("title") or "")[:50]
        dur = log.get("duration_s")
        dur_s = f"{dur:>5.2f}s" if dur is not None else "  -   "
        light_tag = "LIGHT" if log["is_light"] else "DARK "
        strat = log["strategy"] or "?"
        print(
            f"  [{i:>3}/{len(targets)}] {dur_s} [{col:<14}] {light_tag} "
            f"{log['type']:<9} {log['product_id']}  {title:<52}  → {tag}"
            + (f": {log['error']}" if log["error"] else "")
        )
        # Persist log immediately
        (config.LOG_DIR / f"fix05-{log['product_id']}.json").write_text(
            json.dumps(log, indent=2, ensure_ascii=False)
        )
        logs.append(log)
        time.sleep(config.PRINTIFY_DELAY_S)

    # Theme list sync (idempotent, no new handles if assets already on disk)
    n_total = sync_theme_list()

    # Preview grid: 4 light non-mug + 4 mugs (mix dark/light)
    _make_preview(logs)

    elapsed = (datetime.datetime.now() - started).total_seconds()
    successes = [l for l in logs if not l["error"]]
    errors = [l for l in logs if l["error"]]
    summary = config.LOG_DIR / "_SUMMARY_FIX05.md"
    summary.write_text(
        "\n".join([
            f"# Fix 05 — light + mugs — {datetime.datetime.now().isoformat(timespec='seconds')}",
            "",
            f"- Cibles traitées : **{len(logs)}**",
            f"- Succès : **{len(successes)}**",
            f"- Erreurs : **{len(errors)}**",
            f"- Durée : {int(elapsed//60)}m{int(elapsed%60)}s",
            f"- Handles dans liste theme : **{n_total}**",
            "",
            "## Répartition stratégie",
            "",
            f"- compose_light (bg replacement) : {sum(1 for l in logs if l.get('strategy','').startswith('compose_light'))}",
            f"- rembg + compose                : {sum(1 for l in logs if l.get('strategy','').startswith('rembg'))}",
            "",
            "## Erreurs",
            "",
            *(
                ["(aucune)"]
                if not errors
                else [f"- `{l['product_id']}` {l['title']} → {l['error']}" for l in errors]
            ),
        ])
    )

    print("\n" + "=" * 70)
    print("🛑 FIX 05 TERMINÉ — assets régénérés, theme NON pushé")
    print("=" * 70)
    print(f"Durée    : {int(elapsed//60)}m{int(elapsed%60)}s")
    print(f"OK / Err : {len(successes)} / {len(errors)}")
    print(f"Récap    : {summary.relative_to(config.REPO_ROOT)}")
    print(f"Preview  : output/mockup-pipeline/logs/_PREVIEW_fix05.png")
    print("\nValide la preview, puis pousse le thème :")
    print(
        f"  cd shopify-theme && shopify theme push "
        f"--store={config.SHOPIFY_STORE} --theme=198885507415 "
        f"--allow-live --nodelete"
    )
    print("=" * 70)
    return 0


def _make_preview(logs: list[dict]):
    """Pick 4 light non-mug + 4 mugs, build a 4x2 preview."""
    light_nonmug = [
        l for l in logs
        if l["is_light"] and l["type"] != "mug" and l.get("asset") and not l["error"]
    ]
    mugs = [
        l for l in logs
        if l["type"] == "mug" and l.get("asset") and not l["error"]
    ]
    # Try to get a mix of dark and light mugs
    mugs_light = [m for m in mugs if m["is_light"]][:2]
    mugs_dark = [m for m in mugs if not m["is_light"]][:2]
    picked = (light_nonmug[:4] + mugs_light + mugs_dark)[:8]
    paths = [config.REPO_ROOT / l["asset"] for l in picked]
    labels = [
        f"[{l['collection']}] {('LIGHT' if l['is_light'] else 'DARK')} {l['type']} {l['title'][:30]}"
        for l in picked
    ]
    out = config.LOG_DIR / "_PREVIEW_fix05.png"
    build_preview(paths, labels, out)
    print(f"Preview written: {out.relative_to(config.REPO_ROOT)}")


def _make_preview_from_current(targets: list[dict]):
    """For --preview-only: re-build the preview grid from existing assets."""
    samples = []
    labels = []
    for p in targets:
        h = normalize_handle((p.get("external") or {}).get("handle"))
        if not h:
            continue
        asset = config.SHOPIFY_ASSETS_DIR / f"mockup-{h}.webp"
        if not asset.exists():
            continue
        ptype = mockup_selector.detect_product_type(p)
        light = mockup_selector.is_light_product(p)
        samples.append(asset)
        labels.append(f"[{collection_detector.detect_collection(p)}] {'LIGHT' if light else 'DARK'} {ptype} {p['title'][:30]}")
        if len(samples) >= 8:
            break
    out = config.LOG_DIR / "_PREVIEW_fix05.png"
    build_preview(samples, labels, out)
    print(f"Preview written: {out.relative_to(config.REPO_ROOT)}")


if __name__ == "__main__":
    sys.exit(run())
