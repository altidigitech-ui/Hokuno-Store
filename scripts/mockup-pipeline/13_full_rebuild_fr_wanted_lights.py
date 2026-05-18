"""Fix 13 — Full rebuild from scratch of the 15 FR Wanted LIGHT mockups.

For each target product:
  1. Fetch product from Printify
  2. Dump ALL images metadata (camera_label, variant_ids, position, is_default,
     is_selected_for_publishing) for inspection
  3. Use pick_light_color to find Natural / Cream / Sport Grey / Ash / Sand
     variant (in that priority)
  4. Find the back-2 mockup (camera_label=back-2 or angle id 102006) for that
     specific colored variant
  5. Download raw → save to output/debug-fr-fix/{handle}-1-RAW.png
  6. rembg detourage → save to output/debug-fr-fix/{handle}-2-DETOURED.png
  7. Composite on bg-wanted.png → save to BOTH
     output/debug-fr-fix/{handle}-3-FINAL.webp
     shopify-theme/assets/mockup-{handle}.webp
  8. Write a per-product debug JSON with all metadata

After all 15 are done, regenerate character-map.json so fr.image_handle for
each character points to the FR light handle.

Run:
    python scripts/mockup-pipeline/13_full_rebuild_fr_wanted_lights.py
"""
from __future__ import annotations

import datetime
import json
import re
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import config  # noqa: E402
import printify_client  # noqa: E402
import mockup_selector  # noqa: E402
import detourage  # noqa: E402
import compositing  # noqa: E402


DEBUG_DIR = config.REPO_ROOT / "output" / "debug-fr-fix"


TARGETS: list[tuple[str, str]] = [
    ("bartolomiou-kouma", "t-shirt-bartolomiou-kouma-wanted-18-46"),
    ("iwankoff",          "t-shirt-iwankoff-wanted-19-46"),
    ("harllong",          "t-shirt-harllong-wanted-20-46"),
    ("momonosucke",       "t-shirt-momonosucke-wanted-21-46"),
    ("eustash-cap-kid",   "t-shirt-eustash-cap-kid-wanted-22-46"),
    ("boha-ancock",       "t-shirt-boha-ancock-wanted-23-46"),
    ("iamato",            "t-shirt-iamato-wanted-24-46"),
    ("kobi",              "t-shirt-kobi-wanted-25-46"),
    ("portgas-di-ase",    "t-shirt-portgas-di-ase-wanted-26-46"),
    ("crocockdile",       "t-shirt-crocockdile-wanted-27-46"),
    ("dracule-miok",      "t-shirt-dracule-miok-wanted-28-46"),
    ("sabot",             "t-shirt-sabot-wanted-29-46"),
    ("trafalgar-di-low",  "t-shirt-trafalgar-di-low-wanted-30-46"),
    ("monki-di-dragone",  "t-shirt-monki-di-dragone-wanted-31-46"),
    ("gayko-mauria",      "t-shirt-gayko-mauria-wanted-32-46"),
]


def normalize_handle(raw: str | None) -> str | None:
    if not raw:
        return None
    h = raw.rstrip("/").split("/products/")[-1]
    return h.split("?", 1)[0].split("#", 1)[0] or None


def describe_image(img: dict) -> dict:
    src = img.get("src", "")
    cam = mockup_selector._url_camera_label(src)
    m = re.search(r"/mockup/[a-z0-9]+/([0-9]+)/([0-9]+)/", src)
    return {
        "variant_id_in_url": m.group(1) if m else None,
        "angle_id_in_url":   m.group(2) if m else None,
        "camera_label":      cam or None,
        "position":          img.get("position"),
        "is_default":        img.get("is_default"),
        "is_selected_for_publishing": img.get("is_selected_for_publishing"),
        "variant_ids":       img.get("variant_ids") or [],
        "src":               src,
    }


def find_color_axis(product: dict) -> tuple[int | None, dict]:
    """Return (color_option_index, {variant_id: color_name})."""
    options = product.get("options") or []
    for idx, opt in enumerate(options):
        if (opt.get("type") or "").lower() == "color":
            val_id_to_name = {
                v["id"]: (v.get("title") or "")
                for v in opt.get("values") or []
            }
            return idx, val_id_to_name
    return None, {}


def variant_color_map(product: dict) -> dict[int, str]:
    """{variant_id: color_name} for every variant of the product."""
    color_idx, val_id_to_name = find_color_axis(product)
    if color_idx is None:
        return {}
    out: dict[int, str] = {}
    for v in product.get("variants", []):
        opt_vals = v.get("options") or []
        if color_idx < len(opt_vals):
            out[v["id"]] = val_id_to_name.get(opt_vals[color_idx], "")
    return out


def rebuild_one(product: dict, handle: str) -> dict:
    pid = product["id"]
    title = product.get("title", "")
    bg_path = config.BG_BY_COLLECTION["WANTED"]

    log: dict = {
        "product_id": pid,
        "title": title,
        "handle": handle,
        "blueprint_id": product.get("blueprint_id"),
        "all_images": [describe_image(i) for i in product.get("images", [])],
        "color_picked": None,
        "color_variant_ids": None,
        "chosen_image": None,
        "raw_bytes": None,
        "raw_path": None,
        "detoured_path": None,
        "final_paths": [],
        "error": None,
    }

    # Variant color map for enriching the log
    v_color = variant_color_map(product)
    for img in log["all_images"]:
        img["variant_colors"] = sorted({
            v_color.get(vid, "?") for vid in img.get("variant_ids") or []
        }) or None

    # 1. Pick the Natural / Cream / Sport Grey / etc. variant
    color_name, color_variant_ids = mockup_selector.pick_light_color(product)
    log["color_picked"] = color_name
    log["color_variant_ids"] = color_variant_ids

    if not color_variant_ids:
        log["error"] = "pick_light_color returned no neutral color — aborting"
        return log

    # 2. Pick the back-2 mockup restricted to those variant IDs
    try:
        img_meta = mockup_selector.pick_source_mockup_tshirt(
            product, color_variant_ids=color_variant_ids
        )
    except Exception as e:  # noqa: BLE001
        log["error"] = f"pick_source_mockup_tshirt failed: {e}"
        return log

    log["chosen_image"] = describe_image(img_meta)
    log["chosen_image"]["variant_colors"] = sorted({
        v_color.get(vid, "?") for vid in img_meta.get("variant_ids") or []
    }) or None

    # Sanity check: chosen image must intersect color_variant_ids
    wanted_vids = set(color_variant_ids)
    if not wanted_vids.intersection(img_meta.get("variant_ids") or []):
        log["error"] = (
            f"chosen image does NOT belong to picked color variants! "
            f"image vids={img_meta.get('variant_ids')} wanted={color_variant_ids}"
        )
        return log

    # 3. Download raw mockup
    DEBUG_DIR.mkdir(parents=True, exist_ok=True)
    src_url = img_meta["src"]
    try:
        raw_bytes = printify_client.download_image(src_url)
    except Exception as e:  # noqa: BLE001
        log["error"] = f"download failed: {e}"
        return log
    log["raw_bytes"] = len(raw_bytes)

    raw_path = DEBUG_DIR / f"{handle}-1-RAW.png"
    raw_path.write_bytes(raw_bytes)
    log["raw_path"] = str(raw_path.relative_to(config.REPO_ROOT))
    # Mirror the raw to the pipeline RAW_DIR too (for parity with the existing pipeline)
    (config.RAW_DIR / f"{pid}.png").write_bytes(raw_bytes)

    # 4. rembg detourage → PNG to debug dir
    try:
        det = detourage.detoure(raw_bytes)
    except Exception as e:  # noqa: BLE001
        log["error"] = f"detourage failed: {e}"
        return log
    det_path = DEBUG_DIR / f"{handle}-2-DETOURED.png"
    det.save(det_path, "PNG")
    log["detoured_path"] = str(det_path.relative_to(config.REPO_ROOT))
    (config.DETOURED_DIR / f"{pid}.png").write_bytes(det_path.read_bytes())

    # 5. Composite on bg-wanted → BOTH debug dir and shopify-theme/assets/
    asset_path = config.SHOPIFY_ASSETS_DIR / f"mockup-{handle}.webp"

    # Delete the existing asset first so we can prove the file is freshly written
    if asset_path.exists():
        asset_path.unlink()

    compositing.compose(det, bg_path, "tshirt", asset_path)

    final_debug = DEBUG_DIR / f"{handle}-3-FINAL.webp"
    final_debug.write_bytes(asset_path.read_bytes())

    log["final_paths"] = [
        str(asset_path.relative_to(config.REPO_ROOT)),
        str(final_debug.relative_to(config.REPO_ROOT)),
    ]
    return log


def run() -> int:
    config.ensure_dirs()
    config.require_printify_token()
    DEBUG_DIR.mkdir(parents=True, exist_ok=True)

    print("→ Fetching all Printify products…")
    products = printify_client.list_all_products()
    print(f"  {len(products)} products fetched")

    by_handle: dict[str, dict] = {}
    for p in products:
        h = normalize_handle((p.get("external") or {}).get("handle"))
        if h:
            by_handle[h] = p

    started = datetime.datetime.now()
    all_logs: list[dict] = []
    missing = []

    print("\n" + "=" * 78)
    print(f"REBUILDING {len(TARGETS)} FR LIGHT WANTED MOCKUPS")
    print("=" * 78)

    for i, (slug, handle) in enumerate(TARGETS, 1):
        print(f"\n[{i:>2}/{len(TARGETS)}] {handle}")
        p = by_handle.get(handle)
        if not p:
            print(f"  ✗ NOT FOUND on Printify")
            missing.append(handle)
            continue

        log = rebuild_one(p, handle)
        # Compact one-line summary
        ci = log.get("chosen_image") or {}
        col = log.get("color_picked") or "-"
        cam = ci.get("camera_label") or ci.get("position") or "?"
        ang = ci.get("angle_id_in_url") or "?"
        vcols = ",".join(ci.get("variant_colors") or [])
        err = log.get("error")
        tag = "ERROR" if err else "OK"
        print(f"  pid          : {log['product_id']}")
        print(f"  color_picked : {col}")
        print(f"  chosen cam   : {cam}  angle={ang}  variant_colors=[{vcols}]")
        print(f"  raw          : {log.get('raw_bytes')} bytes → {log.get('raw_path')}")
        print(f"  detoured     : {log.get('detoured_path')}")
        print(f"  final paths  : {log.get('final_paths')}")
        print(f"  status       : {tag}" + (f" — {err}" if err else ""))

        (config.LOG_DIR / f"fix13-{log['product_id']}.json").write_text(
            json.dumps(log, indent=2, ensure_ascii=False)
        )
        all_logs.append(log)
        time.sleep(config.PRINTIFY_DELAY_S)

    elapsed = (datetime.datetime.now() - started).total_seconds()
    ok = [l for l in all_logs if not l.get("error")]
    err = [l for l in all_logs if l.get("error")]

    print("\n" + "=" * 78)
    print(f"DONE — {len(ok)} OK, {len(err)} errors, {len(missing)} missing")
    print(f"Time: {int(elapsed//60)}m{int(elapsed%60)}s")
    print(f"Debug dir: {DEBUG_DIR.relative_to(config.REPO_ROOT)}")
    print("=" * 78)

    if err:
        print("\n--- ERRORS ---")
        for l in err:
            print(f"  {l['handle']}: {l['error']}")
    if missing:
        print("\n--- MISSING ---")
        for h in missing:
            print(f"  {h}")

    return 0 if not err and not missing else 1


if __name__ == "__main__":
    sys.exit(run())
