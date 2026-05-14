"""Re-render every light/white mug with compose_light(fill_enclosed_holes=True).

Bug: the inner hole of the mug handle stayed white because it's an enclosed
region (not connected to the image borders) — the old `compose_light` only
replaced border-connected near-white pixels.

Fix: the new `fill_enclosed_holes` mode identifies the subject (largest
non-border near-white region = mug body) and replaces *every* other near-white
pixel with the collection bg, including the enclosed handle hole.

Targets:
    - ptype == "mug" AND title does NOT contain NOIR/DARK/BLACK/NOIRE
    - All Wanted/Direction/Mythologie light mugs (BP 478 etc.)

Dark mugs (BP 479) keep their rembg+compose pipeline — the black handle hole
detours cleanly because of high contrast with Printify's white BG.

Run from the repo root:
    python scripts/mockup-pipeline/09_fix_light_mug_handle.py --preview-only
    python scripts/mockup-pipeline/09_fix_light_mug_handle.py --dry-run
    python scripts/mockup-pipeline/09_fix_light_mug_handle.py
"""
from __future__ import annotations

import datetime
import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from PIL import Image, ImageDraw, ImageFont  # noqa: E402

import config  # noqa: E402
import printify_client  # noqa: E402
import collection_detector  # noqa: E402
import mockup_selector  # noqa: E402
import compositing  # noqa: E402


def normalize_handle(raw: str | None) -> str | None:
    if not raw:
        return None
    h = raw.rstrip("/").split("/products/")[-1]
    return h.split("?", 1)[0].split("#", 1)[0] or None


def is_target(product: dict) -> bool:
    if mockup_selector.detect_product_type(product) != "mug":
        return False
    return mockup_selector.is_light_product(product)


def regenerate(product: dict) -> dict:
    pid = product["id"]
    title = product.get("title", "")
    collection = collection_detector.detect_collection(product)
    handle = normalize_handle((product.get("external") or {}).get("handle"))

    log = {
        "product_id": pid,
        "title": title,
        "collection": collection,
        "handle": handle,
        "asset": None,
        "duration_s": None,
        "error": None,
    }
    if not handle:
        log["error"] = "external.handle missing"
        return log
    bg_path = config.BG_BY_COLLECTION.get(collection)
    if not bg_path or not bg_path.exists():
        log["error"] = f"bg missing for collection {collection!r}"
        return log

    t0 = time.time()
    try:
        img_meta = mockup_selector.pick_source_mockup(product, "mug")
        src_url = img_meta.get("src", "")
        raw_bytes = printify_client.download_image(src_url)
        (config.RAW_DIR / f"{pid}.png").write_bytes(raw_bytes)

        dst = config.SHOPIFY_ASSETS_DIR / f"mockup-{handle}.webp"
        compositing.compose_light(
            raw_bytes, bg_path, dst, replace_all_near_white=True
        )
        (config.FINAL_DIR / f"{pid}.webp").write_bytes(dst.read_bytes())
        log["asset"] = str(dst.relative_to(config.REPO_ROOT))
        log["duration_s"] = round(time.time() - t0, 2)
    except Exception as e:  # noqa: BLE001
        log["error"] = f"{type(e).__name__}: {e}"
        log["duration_s"] = round(time.time() - t0, 2)
    return log


def build_preview(picks: list[Path], labels: list[str], output: Path):
    if not picks:
        return
    cell = 600
    cols = min(len(picks), 4)
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
            lbl[:90], fill="black", font=font,
        )
    grid.save(output, "PNG")


def _preview_samples(products: list[dict], n_per_col: int = 2) -> list[dict]:
    """Pick 1-2 samples per collection (Wanted, Direction, Mythologie)."""
    by_col: dict[str, list[dict]] = {}
    for p in products:
        col = collection_detector.detect_collection(p)
        by_col.setdefault(col, []).append(p)
    out = []
    for col in ("WANTED", "MYTHOLOGIE", "DIRECTION"):
        out.extend(by_col.get(col, [])[:n_per_col])
    return out


def run() -> int:
    dry = "--dry-run" in sys.argv
    preview_only = "--preview-only" in sys.argv

    config.ensure_dirs()
    config.require_printify_token()

    print("→ Fetching all Printify products…")
    products = printify_client.list_all_products()
    targets = [p for p in products if is_target(p)]
    print(f"  {len(products)} total / {len(targets)} light mugs")

    by_col = {}
    for p in targets:
        c = collection_detector.detect_collection(p)
        by_col[c] = by_col.get(c, 0) + 1
    print("  Per collection:")
    for col, n in sorted(by_col.items()):
        print(f"    {col:<14} {n}")

    if dry:
        print("\n(dry-run) Nothing regenerated.")
        return 0

    queue = _preview_samples(targets) if preview_only else targets
    if preview_only:
        print(f"\n(preview-only) Regenerating {len(queue)} samples…")
    else:
        print(f"\nRegenerating {len(queue)} mugs…")

    started = datetime.datetime.now()
    logs: list[dict] = []
    for i, p in enumerate(queue, 1):
        log = regenerate(p)
        tag = "ERROR" if log["error"] else "OK"
        col = log.get("collection", "?")
        title = (log.get("title") or "")[:50]
        dur = log.get("duration_s")
        dur_s = f"{dur:>5.2f}s" if dur is not None else "  -   "
        print(
            f"  [{i:>3}/{len(queue)}] {dur_s} [{col:<14}] "
            f"{log['product_id']}  {title:<52}  → {tag}"
            + (f": {log['error']}" if log["error"] else "")
        )
        (config.LOG_DIR / f"fix09-{log['product_id']}.json").write_text(
            json.dumps(log, indent=2, ensure_ascii=False)
        )
        logs.append(log)
        time.sleep(config.PRINTIFY_DELAY_S)

    elapsed = (datetime.datetime.now() - started).total_seconds()
    successes = [l for l in logs if not l["error"]]
    errors = [l for l in logs if l["error"]]

    # Build preview grid from successful assets
    picks = [config.REPO_ROOT / l["asset"] for l in successes if l.get("asset")]
    labels = [
        f"[{l['collection']}] {l['title'][:35]}"
        for l in successes if l.get("asset")
    ]
    out = config.LOG_DIR / ("_PREVIEW_fix09_sample.png" if preview_only else "_PREVIEW_fix09.png")
    if picks:
        build_preview(picks[:8], labels[:8], out)
        print(f"\nPreview written: {out.relative_to(config.REPO_ROOT)}")

    if not preview_only:
        summary = config.LOG_DIR / "_SUMMARY_FIX09.md"
        summary.write_text("\n".join([
            f"# Fix 09 — light mug handle hole — {datetime.datetime.now().isoformat(timespec='seconds')}",
            "",
            f"- Cibles : **{len(logs)}**",
            f"- Succès : **{len(successes)}**",
            f"- Erreurs : **{len(errors)}**",
            f"- Durée : {int(elapsed//60)}m{int(elapsed%60)}s",
            "",
            "## Stratégie",
            "",
            "compose_light(fill_enclosed_holes=True) sur tous les mugs light.",
            "Le 'subject' = plus grande région near-white non-bordée (le corps du mug).",
            "Toutes les autres régions near-white (BG + intérieur de l'anse) sont remplacées par le bg de collection.",
            "",
            "## Erreurs",
            "",
            *(["(aucune)"] if not errors else [f"- {l['product_id']} {l['title']} → {l['error']}" for l in errors]),
        ]))
        print(f"Récap : {summary.relative_to(config.REPO_ROOT)}")

    print(f"\nOK / Err : {len(successes)} / {len(errors)}  ({int(elapsed//60)}m{int(elapsed%60)}s)")
    return 0


if __name__ == "__main__":
    sys.exit(run())
