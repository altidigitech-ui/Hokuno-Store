"""Fix 07 — light products switch to Natural-variant + rembg, all tees use back-2.

What changed since fix05:
- Light t-shirts with a Natural (or other neutral) color enabled now use that
  variant's mockup and standard rembg detourage. The cotton has enough contrast
  with Printify's white BG that rembg keeps the garment intact (the bg-replace
  hack is no longer needed).
- All t-shirts (light *and* dark) prefer the wrinkled "back-2" lifestyle angle
  (camera_label=back-2, angle id 102006) over the flat "back" angle (92571).
- Light products with no neutral color enabled (White-only tees, BP 478 mugs,
  etc.) keep the bg-replacement compose_light strategy.

Scope (regenerated this run):
- All light products (any type) — picker decides cream vs compose_light per product
- All dark t-shirts — new back-2 priority

Skipped (already good):
- Dark mugs, dark phonecases, dark accessories — rembg + compose was working

Run from the repo root:
    python scripts/mockup-pipeline/07_fix_cream_and_back2.py
    python scripts/mockup-pipeline/07_fix_cream_and_back2.py --dry-run
    python scripts/mockup-pipeline/07_fix_cream_and_back2.py --preview-only
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
    """Targets for this fix: every light product, plus every dark t-shirt."""
    is_dark = mockup_selector.is_dark_product(product)
    ptype = mockup_selector.detect_product_type(product)
    if not is_dark:
        return True, f"light/{ptype}"
    if ptype == "tshirt":
        return True, "dark/tshirt-back2"
    return False, f"dark/{ptype}-skip"


def regenerate(product: dict) -> dict:
    pid = product["id"]
    title = product.get("title", "")
    ptype = mockup_selector.detect_product_type(product)
    collection = collection_detector.detect_collection(product)
    is_light = mockup_selector.is_light_product(product)
    handle = normalize_handle((product.get("external") or {}).get("handle"))

    log: dict = {
        "product_id": pid,
        "title": title,
        "collection": collection,
        "type": ptype,
        "handle": handle,
        "is_light": is_light,
        "strategy": None,
        "color_picked": None,
        "mockup_position_used": None,
        "mockup_camera_label": None,
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

    # Light path: try to pick a cream / non-white variant for rembg
    color_variant_ids: list[int] | None = None
    if is_light:
        color_name, color_variant_ids = mockup_selector.pick_light_color(product)
        log["color_picked"] = color_name
    color_variant_ids = color_variant_ids or None

    try:
        img_meta = mockup_selector.pick_source_mockup(
            product, ptype, color_variant_ids=color_variant_ids
        )
    except Exception as e:  # noqa: BLE001
        log["error"] = f"mockup pick failed: {e}"
        log["duration_s"] = round(time.time() - t0, 2)
        return log

    src_url = img_meta.get("src", "")
    log["mockup_position_used"] = img_meta.get("position")
    log["mockup_camera_label"] = mockup_selector._url_camera_label(src_url) or None
    m = re.search(r"/mockup/[a-z0-9]+/[0-9]+/([0-9]+)/", src_url)
    if m:
        log["mockup_angle_id"] = m.group(1)

    try:
        raw_bytes = printify_client.download_image(src_url)
        (config.RAW_DIR / f"{pid}.png").write_bytes(raw_bytes)

        dst = config.SHOPIFY_ASSETS_DIR / f"mockup-{handle}.webp"

        # Light WITH a picked non-white color → rembg works on the colored garment.
        # Light WITHOUT picked color (White-only tee, BP 478 mug, etc.) → bg replace.
        # Dark → rembg as before.
        if is_light and not color_variant_ids:
            log["strategy"] = "compose_light (bg replacement, no neutral color)"
            compositing.compose_light(raw_bytes, bg_path, dst)
        else:
            log["strategy"] = (
                "rembg + compose (cream variant)"
                if is_light else "rembg + compose (dark)"
            )
            det = detourage.detoure(raw_bytes)
            det.save(config.DETOURED_DIR / f"{pid}.png", "PNG")
            compositing.compose(det, bg_path, ptype, dst)

        (config.FINAL_DIR / f"{pid}.webp").write_bytes(dst.read_bytes())

        log["asset"] = str(dst.relative_to(config.REPO_ROOT))
        log["duration_s"] = round(time.time() - t0, 2)
        return log
    except Exception as e:  # noqa: BLE001
        log["error"] = f"{type(e).__name__}: {e}"
        log["duration_s"] = round(time.time() - t0, 2)
        return log


# ─── Theme list sync ────────────────────────────────────────────────────────

def existing_handles(path: Path) -> list[str]:
    if not path.exists():
        return []
    m = LIST_RE.search(path.read_text())
    return re.findall(r'append:\s*"([^",]+),"', m.group(0)) if m else []


def write_handles(path: Path, indent: str, handles: list[str]) -> None:
    src = path.read_text()
    if not LIST_RE.search(src):
        raise RuntimeError(f"{path}: HOKUNO-MOCKUP-LIST markers missing")
    lines = [f"{indent}{LIST_START}", f'{indent}{{%- assign mockup_handles = "" -%}}']
    for h in handles:
        lines.append(
            f'{indent}{{%- assign mockup_handles = mockup_handles | append: "{h}," -%}}'
        )
    lines.append(f"{indent}{LIST_END}")
    path.write_text(LIST_RE.sub("\n".join(lines), src, count=1))


def sync_theme_list() -> int:
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


# ─── Preview grid ───────────────────────────────────────────────────────────

def build_preview(picks: list[Path], labels: list[str], output: Path):
    if not picks:
        return
    cell = 600
    cols = 5
    rows = max(1, (len(picks) + cols - 1) // cols)
    grid = Image.new("RGB", (cols * cell, rows * (cell + 40)), "white")
    try:
        font = ImageFont.truetype(
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 16
        )
    except OSError:
        font = ImageFont.load_default()
    for i, (p, lbl) in enumerate(zip(picks, labels)):
        try:
            img = Image.open(p).convert("RGB").resize((cell, cell), Image.LANCZOS)
        except Exception:
            continue
        r, c = divmod(i, cols)
        grid.paste(img, (c * cell, r * (cell + 40) + 40))
        ImageDraw.Draw(grid).text(
            (c * cell + 10, r * (cell + 40) + 10),
            lbl[:90],
            fill="black",
            font=font,
        )
    grid.save(output, "PNG")


def _make_preview(logs: list[dict]):
    """Build a 5×3 preview: 5 light tees + 5 mugs + 5 dark tees."""
    light_tees = [
        l for l in logs
        if l["is_light"] and l["type"] == "tshirt" and l.get("asset") and not l["error"]
    ]
    mugs = [
        l for l in logs
        if l["type"] == "mug" and l.get("asset") and not l["error"]
    ]
    dark_tees = [
        l for l in logs
        if not l["is_light"] and l["type"] == "tshirt" and l.get("asset") and not l["error"]
    ]

    # Spread across collections for variety
    def diversified(items: list[dict], n: int) -> list[dict]:
        seen_colls: dict[str, int] = {}
        out: list[dict] = []
        for it in items:
            c = it.get("collection")
            if seen_colls.get(c, 0) >= 2:
                continue
            seen_colls[c] = seen_colls.get(c, 0) + 1
            out.append(it)
            if len(out) >= n:
                break
        if len(out) < n:
            for it in items:
                if it not in out:
                    out.append(it)
                if len(out) >= n:
                    break
        return out

    picked = diversified(light_tees, 5) + diversified(mugs, 5) + diversified(dark_tees, 5)
    paths = [config.REPO_ROOT / l["asset"] for l in picked]
    labels = []
    for l in picked:
        bucket = "LIGHT-TEE" if (l["is_light"] and l["type"] == "tshirt") else (
            "MUG" if l["type"] == "mug" else "DARK-TEE"
        )
        col = l.get("color_picked") or l.get("strategy", "").split(" ")[0]
        labels.append(f"[{l['collection']}] {bucket} {col} — {l['title'][:35]}")

    out = config.LOG_DIR / "_PREVIEW_fix07.png"
    build_preview(paths, labels, out)
    print(f"Preview written: {out.relative_to(config.REPO_ROOT)}")


def _make_preview_from_logs():
    """For --preview-only: rebuild from existing fix07-*.json logs."""
    logs: list[dict] = []
    for f in config.LOG_DIR.glob("fix07-*.json"):
        try:
            logs.append(json.loads(f.read_text()))
        except Exception:
            continue
    _make_preview(logs)


# ─── Main ───────────────────────────────────────────────────────────────────

def run() -> int:
    dry_run = "--dry-run" in sys.argv
    preview_only = "--preview-only" in sys.argv

    config.ensure_dirs()
    config.require_printify_token()

    if preview_only:
        _make_preview_from_logs()
        return 0

    print("→ Fetching all Printify products…")
    products = printify_client.list_all_products()
    print(f"  {len(products)} products fetched")

    targets: list[dict] = []
    skips = 0
    for p in products:
        ok, _ = is_target(p)
        if ok:
            targets.append(p)
        else:
            skips += 1

    n_light_tee = sum(
        1 for p in targets
        if mockup_selector.is_light_product(p)
        and mockup_selector.detect_product_type(p) == "tshirt"
    )
    n_light_mug = sum(
        1 for p in targets
        if mockup_selector.is_light_product(p)
        and mockup_selector.detect_product_type(p) == "mug"
    )
    n_light_other = sum(
        1 for p in targets
        if mockup_selector.is_light_product(p)
        and mockup_selector.detect_product_type(p) not in ("tshirt", "mug")
    )
    n_dark_tee = sum(
        1 for p in targets if not mockup_selector.is_light_product(p)
    )
    print(f"\n=== Targets : {len(targets)} ===")
    print(f"  Light t-shirts          : {n_light_tee}")
    print(f"  Light mugs              : {n_light_mug}")
    print(f"  Light other (cap/case/…): {n_light_other}")
    print(f"  Dark t-shirts (back-2)  : {n_dark_tee}")
    print(f"  SKIP (dark non-tee)     : {skips}")

    if dry_run:
        print("\n(dry-run) Nothing regenerated. Exit.")
        return 0

    started = datetime.datetime.now()
    logs: list[dict] = []
    for i, p in enumerate(targets, 1):
        log = regenerate(p)
        tag = "ERROR" if log["error"] else "OK"
        col = log.get("collection", "?")
        title = (log.get("title") or "")[:46]
        dur = log.get("duration_s")
        dur_s = f"{dur:>5.2f}s" if dur is not None else "  -   "
        light_tag = "LIGHT" if log["is_light"] else "DARK "
        strat_short = (log["strategy"] or "?")[:14]
        cam = log.get("mockup_camera_label") or log.get("mockup_position_used") or "?"
        color = log.get("color_picked") or "-"
        print(
            f"  [{i:>3}/{len(targets)}] {dur_s} [{col:<14}] {light_tag} "
            f"{log['type']:<9} cam={cam:<8} col={color:<10} {strat_short:<14}  "
            f"{title:<48}  → {tag}"
            + (f": {log['error']}" if log["error"] else "")
        )
        (config.LOG_DIR / f"fix07-{log['product_id']}.json").write_text(
            json.dumps(log, indent=2, ensure_ascii=False)
        )
        logs.append(log)
        time.sleep(config.PRINTIFY_DELAY_S)

    n_total = sync_theme_list()
    _make_preview(logs)

    elapsed = (datetime.datetime.now() - started).total_seconds()
    successes = [l for l in logs if not l["error"]]
    errors = [l for l in logs if l["error"]]

    by_strat = {}
    for l in successes:
        by_strat[l["strategy"]] = by_strat.get(l["strategy"], 0) + 1

    summary = config.LOG_DIR / "_SUMMARY_FIX07.md"
    summary.write_text("\n".join([
        f"# Fix 07 — cream variant + back-2 — {datetime.datetime.now().isoformat(timespec='seconds')}",
        "",
        f"- Cibles : **{len(logs)}**",
        f"- Succès : **{len(successes)}**",
        f"- Erreurs : **{len(errors)}**",
        f"- Durée : {int(elapsed//60)}m{int(elapsed%60)}s",
        f"- Handles dans liste theme : **{n_total}**",
        "",
        "## Répartition par stratégie",
        "",
        *(f"- {strat:<48} {n}" for strat, n in sorted(by_strat.items(), key=lambda x: -x[1])),
        "",
        "## Erreurs",
        "",
        *(
            ["(aucune)"]
            if not errors
            else [f"- `{l['product_id']}` {l['title']} → {l['error']}" for l in errors]
        ),
    ]))

    print("\n" + "=" * 70)
    print("🛑 FIX 07 TERMINÉ — assets régénérés, theme NON pushé")
    print("=" * 70)
    print(f"Durée    : {int(elapsed//60)}m{int(elapsed%60)}s")
    print(f"OK / Err : {len(successes)} / {len(errors)}")
    print(f"Récap    : {summary.relative_to(config.REPO_ROOT)}")
    print(f"Preview  : output/mockup-pipeline/logs/_PREVIEW_fix07.png")
    print("\nValide la preview avant tout push.")
    print("=" * 70)
    return 0


if __name__ == "__main__":
    sys.exit(run())
