"""Retarget the light t-shirts where fix05 picked a non-back angle.

Background: 15 light Wanted t-shirts had no position='back' label (legacy mockup
set with every image tagged 'other'). The first pass picked angle 102005 (front)
or 92570 (front) by falling through to is_default. The selector now also matches
known back template angle IDs (92571, 102006). This script re-runs ONLY those
mis-targeted products.

Run from the repo root:
    python scripts/mockup-pipeline/06_retry_light_tshirts.py
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
import compositing  # noqa: E402

# Same back-angle IDs as the selector — anything else is a wrong pick.
BACK_ANGLES = set(mockup_selector.TSHIRT_BACK_ANGLE_IDS)


def affected_ids() -> list[str]:
    out: list[str] = []
    for f in Path(config.LOG_DIR).glob("fix05-*.json"):
        try:
            log = json.loads(f.read_text())
        except Exception:
            continue
        if log.get("type") != "tshirt" or not log.get("is_light"):
            continue
        if log.get("mockup_position_used") == "back":
            continue
        angle = log.get("mockup_angle_id")
        if angle in BACK_ANGLES:
            continue
        out.append(log["product_id"])
    return out


def regenerate(product: dict) -> dict:
    pid = product["id"]
    title = product.get("title", "")
    handle = (product.get("external") or {}).get("handle", "")
    handle = handle.rstrip("/").split("/products/")[-1].split("?")[0].split("#")[0]
    collection = collection_detector.detect_collection(product)
    bg = config.BG_BY_COLLECTION.get(collection)

    log = {
        "product_id": pid, "title": title, "collection": collection,
        "type": "tshirt", "is_light": True, "handle": handle,
        "strategy": "compose_light (retry)", "mockup_position_used": None,
        "mockup_angle_id": None, "asset": None, "error": None, "duration_s": None,
    }
    if not handle:
        log["error"] = "no handle"
        return log
    if not bg or not bg.exists():
        log["error"] = f"bg missing for {collection!r}"
        return log

    t0 = time.time()
    try:
        img_meta = mockup_selector.pick_source_mockup(product, "tshirt")
        log["mockup_position_used"] = img_meta.get("position")
        src = img_meta.get("src", "")
        log["mockup_angle_id"] = src.split("/")[-2] if "/" in src else None

        raw = printify_client.download_image(src)
        (config.RAW_DIR / f"{pid}.png").write_bytes(raw)

        dst = config.SHOPIFY_ASSETS_DIR / f"mockup-{handle}.webp"
        compositing.compose_light(raw, bg, dst)
        (config.FINAL_DIR / f"{pid}.webp").write_bytes(dst.read_bytes())
        log["asset"] = str(dst.relative_to(config.REPO_ROOT))
        log["duration_s"] = round(time.time() - t0, 2)
    except Exception as e:  # noqa: BLE001
        log["error"] = f"{type(e).__name__}: {e}"
        log["duration_s"] = round(time.time() - t0, 2)
    return log


def run() -> int:
    config.ensure_dirs()
    config.require_printify_token()

    targets = affected_ids()
    print(f"=== {len(targets)} light t-shirts à reprendre (non-back angle) ===")
    if not targets:
        print("Nothing to do.")
        return 0

    # Fetch full product payloads
    print("→ Fetching Printify catalog…")
    all_products = printify_client.list_all_products()
    by_id = {p["id"]: p for p in all_products}
    queue = [by_id[t] for t in targets if t in by_id]
    print(f"  {len(queue)}/{len(targets)} products resolved\n")

    started = datetime.datetime.now()
    results: list[dict] = []
    for i, p in enumerate(queue, 1):
        log = regenerate(p)
        tag = "ERROR" if log["error"] else "OK"
        print(
            f"  [{i:>3}/{len(queue)}] {log.get('duration_s',0):>5.2f}s [{log['collection']:<14}] "
            f"{log['product_id']}  {log['title'][:50]:<52}  "
            f"angle={log['mockup_angle_id']}  pos={log['mockup_position_used']!r}  → {tag}"
            + (f": {log['error']}" if log["error"] else "")
        )
        # Update the fix05 log for this product so future tools see corrected state
        (config.LOG_DIR / f"fix05-{log['product_id']}.json").write_text(
            json.dumps(log, indent=2, ensure_ascii=False)
        )
        results.append(log)
        time.sleep(config.PRINTIFY_DELAY_S)

    elapsed = (datetime.datetime.now() - started).total_seconds()
    ok = [r for r in results if not r["error"]]
    err = [r for r in results if r["error"]]
    print("\n" + "=" * 70)
    print(f"06 — light tshirt retry : {len(ok)} OK, {len(err)} erreurs  ({int(elapsed)}s)")
    print("=" * 70)
    print("Re-génère la preview pour valider :")
    print("  python scripts/mockup-pipeline/05_fix_light_and_mugs.py --preview-only")
    return 0 if not err else 2


if __name__ == "__main__":
    sys.exit(run())
