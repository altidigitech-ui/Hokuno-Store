"""Fix 12 — Re-regenerate the 15 FR Wanted LIGHT t-shirts whose mockups in
commit 5f7e624 came out as bare wanted posters (white t-shirt + rembg killed
the garment, leaving only the brown poster on bg-wanted).

Re-uses the regenerate() pipeline from 07_fix_cream_and_back2 — i.e.:
  - pick_light_color → Natural variant
  - pick_source_mockup_tshirt → back-2 (camera_label=back-2, angle 102006)
  - rembg detourage → compose on bg-wanted.png

Scope: only the 15 light FR tees. Dark variants from the same commit were
verified OK and are skipped.

Usage:
    python scripts/mockup-pipeline/12_refix_fr_wanted_lights.py
    python scripts/mockup-pipeline/12_refix_fr_wanted_lights.py --dry-run
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

import importlib.util  # noqa: E402
_spec = importlib.util.spec_from_file_location(
    "fix07",
    Path(__file__).resolve().parent / "07_fix_cream_and_back2.py",
)
fix07 = importlib.util.module_from_spec(_spec)  # type: ignore[arg-type]
_spec.loader.exec_module(fix07)  # type: ignore[union-attr]


TARGET_HANDLES = {
    "t-shirt-bartolomiou-kouma-wanted-18-46",
    "t-shirt-boha-ancock-wanted-23-46",
    "t-shirt-crocockdile-wanted-27-46",
    "t-shirt-dracule-miok-wanted-28-46",
    "t-shirt-eustash-cap-kid-wanted-22-46",
    "t-shirt-gayko-mauria-wanted-32-46",
    "t-shirt-harllong-wanted-20-46",
    "t-shirt-iamato-wanted-24-46",
    "t-shirt-iwankoff-wanted-19-46",
    "t-shirt-kobi-wanted-25-46",
    "t-shirt-momonosucke-wanted-21-46",
    "t-shirt-monki-di-dragone-wanted-31-46",
    "t-shirt-portgas-di-ase-wanted-26-46",
    "t-shirt-sabot-wanted-29-46",
    "t-shirt-trafalgar-di-low-wanted-30-46",
}


def run() -> int:
    dry_run = "--dry-run" in sys.argv

    config.ensure_dirs()
    config.require_printify_token()

    print("→ Fetching all Printify products…")
    products = printify_client.list_all_products()
    print(f"  {len(products)} products fetched")

    targets: list[dict] = []
    for p in products:
        handle = fix07.normalize_handle((p.get("external") or {}).get("handle"))
        if handle in TARGET_HANDLES:
            targets.append(p)

    missing = TARGET_HANDLES - {
        fix07.normalize_handle((p.get("external") or {}).get("handle"))
        for p in targets
    }
    if missing:
        print(f"\n⚠️  {len(missing)} target handle(s) not found on Printify:")
        for h in sorted(missing):
            print(f"   - {h}")

    print(f"\n=== Targets: {len(targets)} / {len(TARGET_HANDLES)} ===")
    for p in targets:
        h = fix07.normalize_handle((p.get("external") or {}).get("handle"))
        print(f"  - {p['id']}  {h}")

    if dry_run:
        print("\n(dry-run) Nothing regenerated. Exit.")
        return 0

    started = datetime.datetime.now()
    logs: list[dict] = []
    for i, p in enumerate(targets, 1):
        log = fix07.regenerate(p)
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
            f"  [{i:>2}/{len(targets)}] {dur_s} [{col:<8}] {light_tag} "
            f"{log['type']:<7} cam={cam:<8} col={color:<10} {strat_short:<16}  "
            f"{title:<48}  → {tag}"
            + (f": {log['error']}" if log["error"] else "")
        )
        (config.LOG_DIR / f"fix12-{log['product_id']}.json").write_text(
            json.dumps(log, indent=2, ensure_ascii=False)
        )
        logs.append(log)
        time.sleep(config.PRINTIFY_DELAY_S)

    elapsed = (datetime.datetime.now() - started).total_seconds()
    successes = [l for l in logs if not l["error"]]
    errors = [l for l in logs if l["error"]]

    print("\n" + "=" * 70)
    print("🛑 FIX 12 TERMINÉ — assets régénérés, theme NON pushé")
    print("=" * 70)
    print(f"Durée    : {int(elapsed//60)}m{int(elapsed%60)}s")
    print(f"OK / Err : {len(successes)} / {len(errors)}")
    if errors:
        for l in errors:
            print(f"  ERROR  {l['product_id']}  {l['title']}  → {l['error']}")
    print("=" * 70)
    return 0


if __name__ == "__main__":
    sys.exit(run())
