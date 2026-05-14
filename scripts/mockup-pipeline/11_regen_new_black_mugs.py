"""Generate custom mockups for the 56 black mugs created by step 10.

Strategy:
  - Refetch each new Printify product (mockup images may need a few seconds
    after creation to appear in the API response).
  - Pick the right-side mug angle that shows the design clearly (BP 479
    angles 6407 / 101583 — same as the existing direction dark mugs).
  - rembg detourage works well on a black mug against Printify's white BG
    (high contrast). Composite onto the collection bg.

Outputs:
  shopify-theme/assets/mockup-{handle}.webp   for each new black mug.

Run:
    python scripts/mockup-pipeline/11_regen_new_black_mugs.py
    python scripts/mockup-pipeline/11_regen_new_black_mugs.py --retry-pending  # retry any products whose Printify mockup wasn't ready before
"""
from __future__ import annotations

import datetime
import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import config  # noqa: E402
import printify_client  # noqa: E402
import collection_detector  # noqa: E402
import mockup_selector  # noqa: E402
import detourage  # noqa: E402
import compositing  # noqa: E402


CREATED_LOG = config.LOG_DIR / "fix10-created.json"


def normalize_handle(raw: str | None) -> str | None:
    if not raw:
        return None
    h = raw.rstrip("/").split("/products/")[-1]
    return h.split("?", 1)[0].split("#", 1)[0] or None


def process_one(product: dict) -> dict:
    pid = product["id"]
    title = product.get("title", "")
    collection = collection_detector.detect_collection(product)
    handle = normalize_handle((product.get("external") or {}).get("handle"))
    log = {
        "product_id": pid, "title": title, "collection": collection,
        "handle": handle, "asset": None, "duration_s": None, "error": None,
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
        img_meta = mockup_selector.pick_source_mockup_mug(product)
        src_url = img_meta.get("src", "")
        raw_bytes = printify_client.download_image(src_url)
        (config.RAW_DIR / f"{pid}.png").write_bytes(raw_bytes)

        det = detourage.detoure(raw_bytes)
        det.save(config.DETOURED_DIR / f"{pid}.png", "PNG")

        dst = config.SHOPIFY_ASSETS_DIR / f"mockup-{handle}.webp"
        compositing.compose(det, bg_path, "mug", dst)
        (config.FINAL_DIR / f"{pid}.webp").write_bytes(dst.read_bytes())
        log["asset"] = str(dst.relative_to(config.REPO_ROOT))
        log["duration_s"] = round(time.time() - t0, 2)
    except Exception as e:  # noqa: BLE001
        log["error"] = f"{type(e).__name__}: {e}"
        log["duration_s"] = round(time.time() - t0, 2)
    return log


def run() -> int:
    retry_pending = "--retry-pending" in sys.argv
    config.ensure_dirs()
    config.require_printify_token()

    if not CREATED_LOG.exists():
        print(f"ERROR: {CREATED_LOG} missing — run step 10 first.")
        return 1
    created = json.loads(CREATED_LOG.read_text())
    target_ids = {info["product_id"]: slug for slug, info in created.items()}

    print(f"→ {len(target_ids)} new black mugs to mockup")

    # Fetch full Printify catalog and wait until ALL targets have:
    #   - at least one published mockup image
    #   - external.handle assigned by Shopify
    print("→ Fetching Printify catalog (waiting for Shopify to publish handles)…")
    products_by_id: dict = {}
    max_wait_sec = 360  # up to 6 min — Shopify publish queue can be slow
    started = time.time()
    while True:
        all_products = printify_client.list_all_products()
        products_by_id = {p["id"]: p for p in all_products if p["id"] in target_ids}
        ready = []
        not_published = 0
        no_image = 0
        for p in products_by_id.values():
            has_handle = bool((p.get("external") or {}).get("handle"))
            has_img = any(i.get("is_selected_for_publishing") for i in (p.get("images") or []))
            if has_handle and has_img:
                ready.append(p)
            elif not has_handle:
                not_published += 1
            elif not has_img:
                no_image += 1
        elapsed = int(time.time() - started)
        print(f"  ready: {len(ready)}/{len(target_ids)}  "
              f"(no_handle={not_published}, no_image={no_image}, elapsed={elapsed}s)")
        if len(ready) >= len(target_ids):
            break
        if elapsed >= max_wait_sec:
            print(f"  Timeout — proceeding with {len(ready)} ready products. Re-run --retry-pending later for the rest.")
            break
        time.sleep(20)

    # Process only products that have BOTH a published mockup image and a Shopify handle.
    queue = [
        p for p in products_by_id.values()
        if (p.get("external") or {}).get("handle")
           and any(i.get("is_selected_for_publishing") for i in (p.get("images") or []))
    ]
    skipped = len(products_by_id) - len(queue)
    if skipped:
        print(f"  skipped {skipped} not-yet-ready products (rerun --retry-pending later)")
    start_run = datetime.datetime.now()
    logs: list[dict] = []
    for i, p in enumerate(queue, 1):
        log = process_one(p)
        tag = "ERROR" if log["error"] else "OK"
        col = log.get("collection", "?")
        title = (log.get("title") or "")[:46]
        dur = log.get("duration_s") or 0
        print(f"  [{i:>3}/{len(queue)}] {dur:>5.2f}s [{col:<14}] {log['product_id']}  {title:<48}  → {tag}"
              + (f": {log['error']}" if log["error"] else ""))
        (config.LOG_DIR / f"fix11-{log['product_id']}.json").write_text(
            json.dumps(log, indent=2, ensure_ascii=False)
        )
        logs.append(log)
        time.sleep(config.PRINTIFY_DELAY_S)

    elapsed = (datetime.datetime.now() - start_run).total_seconds()
    successes = [l for l in logs if not l["error"]]
    errors = [l for l in logs if l["error"]]
    print("\n" + "=" * 70)
    print(f"BLACK MUG MOCKUPS — {len(successes)}/{len(queue)} OK, {len(errors)} errors  ({int(elapsed//60)}m{int(elapsed%60)}s)")
    print("=" * 70)
    if errors:
        for e in errors[:10]:
            print(f"  {e['product_id']}  →  {e['error']}")
    return 0 if not errors else 2


if __name__ == "__main__":
    sys.exit(run())
