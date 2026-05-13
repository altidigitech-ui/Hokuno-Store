"""Copy the 4 POC WebP files into shopify-theme/assets/ as mockup-{handle}.webp.

No Shopify Admin API call — assets ship with the theme.

Run from the repo root:
    python scripts/mockup-pipeline/02_upload_poc.py
"""
from __future__ import annotations

import json
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import config  # noqa: E402


def normalize_handle(raw: str | None) -> str | None:
    """Printify's external.handle is often a full URL — return only the slug."""
    if not raw:
        return None
    h = raw.rstrip("/").split("/products/")[-1]
    h = h.split("?", 1)[0].split("#", 1)[0]
    return h or None


def run() -> int:
    config.ensure_dirs()

    poc_log = config.LOG_DIR / "poc_results.json"
    if not poc_log.exists():
        print(f"❌ Missing {poc_log}. Run 01_run_poc.py first.")
        return 1

    results = json.loads(poc_log.read_text())
    config.SHOPIFY_ASSETS_DIR.mkdir(parents=True, exist_ok=True)

    copied: list[dict] = []
    skipped: list[dict] = []

    for r in results:
        pid = r.get("product_id")
        title = r.get("title", "")
        collection = r.get("collection", "?")

        if r.get("error"):
            skipped.append({**r, "reason": f"POC error: {r['error']}"})
            print(f"  [{collection}] {pid} — SKIP (POC error)")
            continue

        handle = normalize_handle(r.get("handle"))
        if not handle:
            skipped.append({**r, "reason": "external.handle missing on Printify product"})
            print(f"  [{collection}] {pid} — SKIP (no Printify external.handle)")
            continue

        final_rel = r.get("final")
        if not final_rel:
            skipped.append({**r, "reason": "no final WEBP recorded"})
            print(f"  [{collection}] {pid} — SKIP (no final path)")
            continue

        src = config.REPO_ROOT / final_rel
        if not src.exists():
            skipped.append({**r, "reason": f"missing file: {src}"})
            print(f"  [{collection}] {pid} — SKIP (file not found: {src})")
            continue

        dst = config.SHOPIFY_ASSETS_DIR / f"mockup-{handle}.webp"
        shutil.copy2(src, dst)
        size_kb = dst.stat().st_size // 1024
        copied.append({
            "product_id": pid,
            "title": title,
            "collection": collection,
            "handle": handle,
            "asset": f"shopify-theme/assets/mockup-{handle}.webp",
            "size_kb": size_kb,
        })
        print(f"  [{collection}] {pid} {title[:50]}")
        print(f"    → {dst.relative_to(config.REPO_ROOT)} ({size_kb} KB)")

    log = {"copied": copied, "skipped": skipped}
    log_path = config.LOG_DIR / "upload_poc_results.json"
    log_path.write_text(json.dumps(log, indent=2, ensure_ascii=False))

    print("\n" + "=" * 70)
    print(f"02 — Upload POC : {len(copied)} copiés, {len(skipped)} skip")
    print("=" * 70)
    print(f"Log : {log_path.relative_to(config.REPO_ROOT)}")
    if skipped:
        print("\nSkippés :")
        for s in skipped:
            print(f"  [{s.get('collection','?')}] {s.get('product_id')} — {s.get('reason')}")
    print("\nNext step :")
    print("  python scripts/mockup-pipeline/03_patch_theme.py")
    print("=" * 70)
    return 0 if copied else 2


if __name__ == "__main__":
    sys.exit(run())
