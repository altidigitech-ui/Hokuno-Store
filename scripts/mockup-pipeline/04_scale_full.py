"""Scale the mockup pipeline to all remaining Printify products.

Workflow per product:
    1. Detect collection + product type
    2. Pick the source mockup (back for tshirts, front for mug/case/cap)
    3. Download → rembg detourage → composite on collection bg
    4. Save as shopify-theme/assets/mockup-{handle}.webp

At the end:
    - Update inline handle list in BOTH product-card.liquid and templates/product.liquid
    - Write output/mockup-pipeline/logs/_SUMMARY.md
    - 🛑 STOP — DO NOT push the theme. Display the push command for the user.

Run from the repo root:
    python scripts/mockup-pipeline/04_scale_full.py
    python scripts/mockup-pipeline/04_scale_full.py --retry-failed-only
    python scripts/mockup-pipeline/04_scale_full.py --force   # re-process even if asset exists
"""
from __future__ import annotations

import datetime
import json
import re
import sys
import time
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

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


# ----------------------------------------------------------- helpers ----

def normalize_handle(raw: str | None) -> str | None:
    if not raw:
        return None
    h = raw.rstrip("/").split("/products/")[-1]
    h = h.split("?", 1)[0].split("#", 1)[0]
    return h or None


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
        raise RuntimeError(
            f"{path}: HOKUNO-MOCKUP-LIST markers missing — initial patch must run first."
        )
    lines = [f"{indent}{LIST_START}", f'{indent}{{%- assign mockup_handles = "" -%}}']
    for h in handles:
        lines.append(
            f'{indent}{{%- assign mockup_handles = mockup_handles | append: "{h}," -%}}'
        )
    lines.append(f"{indent}{LIST_END}")
    new_block = "\n".join(lines)
    path.write_text(LIST_RE.sub(new_block, src, count=1))


def update_theme_list(handles_in_assets: list[str]) -> tuple[int, int]:
    """Merge POC + scale handles into both Liquid files; preserve order."""
    current = existing_handles(PRODUCT_CARD)
    seen = set(current)
    added: list[str] = []
    for h in handles_in_assets:
        if h and h not in seen:
            seen.add(h)
            added.append(h)
    merged = current + added
    write_handles(PRODUCT_CARD, indent="    ", handles=merged)
    write_handles(PRODUCT_TEMPLATE, indent="      ", handles=merged)
    return len(merged), len(added)


# ----------------------------------------------------------- pipeline ----

def already_processed_handles() -> set[str]:
    """Handles already present as theme assets (skip them unless --force)."""
    out = set()
    for p in config.SHOPIFY_ASSETS_DIR.glob("mockup-*.webp"):
        out.add(p.stem.removeprefix("mockup-"))
    return out


def already_logged_ids(force: bool, retry_failed: bool) -> set[str]:
    """Product IDs we should skip (already logged success)."""
    if force or retry_failed:
        return set()
    skip: set[str] = set()
    # POC log
    poc = config.LOG_DIR / "poc_results.json"
    if poc.exists():
        for r in json.loads(poc.read_text()):
            if not r.get("error"):
                skip.add(r["product_id"])
    # Per-product logs from previous scale runs
    for f in config.LOG_DIR.glob("product-*.json"):
        try:
            r = json.loads(f.read_text())
        except Exception:
            continue
        if not r.get("error"):
            skip.add(r["product_id"])
    return skip


def previously_failed_ids() -> set[str]:
    failed = set()
    for f in config.LOG_DIR.glob("product-*.json"):
        try:
            r = json.loads(f.read_text())
        except Exception:
            continue
        if r.get("error"):
            failed.add(r["product_id"])
    return failed


def process_one(product: dict, force: bool) -> dict:
    """Returns a log dict for the product."""
    pid = product["id"]
    title = product.get("title", "")
    t0 = time.time()

    collection = collection_detector.detect_collection(product)
    ptype = mockup_selector.detect_product_type(product)
    handle = normalize_handle((product.get("external") or {}).get("handle"))

    base = {
        "product_id": pid,
        "title": title,
        "collection": collection,
        "type": ptype,
        "handle": handle,
        "shopify_external_id": (product.get("external") or {}).get("id"),
        "mockup_position_used": None,
        "asset": None,
        "duration_s": None,
        "skipped": False,
        "error": None,
    }

    if not handle:
        base["error"] = "external.handle missing (product not published to Shopify)"
        return base

    bg_path = config.BG_BY_COLLECTION.get(collection)
    if not bg_path or not bg_path.exists():
        base["error"] = f"bg missing for collection {collection!r}"
        return base

    dst = config.SHOPIFY_ASSETS_DIR / f"mockup-{handle}.webp"
    if dst.exists() and not force:
        base["asset"] = str(dst.relative_to(config.REPO_ROOT))
        base["skipped"] = True
        base["duration_s"] = round(time.time() - t0, 2)
        return base

    try:
        img_meta = mockup_selector.pick_source_mockup(product, ptype)
        pos = img_meta.get("position") or "(none)"
        src_url = img_meta.get("src")
        base["mockup_position_used"] = pos

        raw_bytes = printify_client.download_image(src_url)
        # Save raw for debug (cheap, helps re-run without re-downloading)
        raw_path = config.RAW_DIR / f"{pid}.png"
        raw_path.write_bytes(raw_bytes)

        det = detourage.detoure(raw_bytes)
        det_path = config.DETOURED_DIR / f"{pid}.png"
        det.save(det_path, "PNG")

        compositing.compose(det, bg_path, ptype, dst)
        # Also keep a per-id final copy for traceability
        final_copy = config.FINAL_DIR / f"{pid}.webp"
        final_copy.write_bytes(dst.read_bytes())

        base["asset"] = str(dst.relative_to(config.REPO_ROOT))
        base["duration_s"] = round(time.time() - t0, 2)
        return base
    except Exception as e:  # noqa: BLE001
        base["error"] = f"{type(e).__name__}: {e}"
        base["duration_s"] = round(time.time() - t0, 2)
        return base


def run() -> int:
    force = "--force" in sys.argv
    retry_failed = "--retry-failed-only" in sys.argv

    config.ensure_dirs()
    config.require_printify_token()
    config.SHOPIFY_ASSETS_DIR.mkdir(parents=True, exist_ok=True)

    print("→ Fetching all Printify products…")
    products = printify_client.list_all_products()
    total = len(products)
    print(f"  {total} products fetched")

    skip_ids = already_logged_ids(force, retry_failed)
    if retry_failed:
        failed = previously_failed_ids()
        print(f"  retry-failed-only mode: {len(failed)} previously-failed product(s)")
        products = [p for p in products if p["id"] in failed]
    else:
        products = [p for p in products if p["id"] not in skip_ids]

    queue_n = len(products)
    print(f"  → {queue_n} products to process (skipping {total - queue_n} already done)\n")

    if not queue_n:
        print("Nothing to do.")
        # Still refresh the theme handle list in case asset_dir has more than the snippet
        return finalize(force=force)

    started_at = datetime.datetime.now()
    successes: list[dict] = []
    skipped: list[dict] = []
    errors: list[dict] = []

    for i, product in enumerate(products, 1):
        log = process_one(product, force=force)

        if log["error"]:
            tag = "ERROR"
            errors.append(log)
        elif log["skipped"]:
            tag = "SKIP (asset exists)"
            skipped.append(log)
        else:
            tag = "OK"
            successes.append(log)

        col = log.get("collection", "?")
        title = (log.get("title") or "")[:50]
        dur = log.get("duration_s")
        dur_s = f"{dur:>5}s" if dur is not None else "  -   "
        print(
            f"  [{i:>3}/{queue_n}] {dur_s} [{col:<14}] {log['product_id']}  "
            f"{title:<52}  → {tag}"
            + (f": {log['error']}" if log["error"] else "")
        )

        # Persist log per product immediately (resumable)
        (config.LOG_DIR / f"product-{log['product_id']}.json").write_text(
            json.dumps(log, indent=2, ensure_ascii=False)
        )

        time.sleep(config.PRINTIFY_DELAY_S)

    return finalize(force=force, started_at=started_at)


def finalize(force: bool, started_at: datetime.datetime | None = None) -> int:
    # Collect every successful asset on disk (POC + scale)
    asset_handles = sorted(
        p.stem.removeprefix("mockup-")
        for p in config.SHOPIFY_ASSETS_DIR.glob("mockup-*.webp")
    )
    n_total, n_added = update_theme_list(asset_handles)

    # Aggregate all logs for summary
    all_logs: list[dict] = []
    poc = config.LOG_DIR / "poc_results.json"
    if poc.exists():
        all_logs.extend(json.loads(poc.read_text()))
    for f in sorted(config.LOG_DIR.glob("product-*.json")):
        try:
            all_logs.append(json.loads(f.read_text()))
        except Exception:
            continue

    successes = [r for r in all_logs if not r.get("error") and not r.get("skipped")]
    skipped = [r for r in all_logs if r.get("skipped") and not r.get("error")]
    errors = [r for r in all_logs if r.get("error")]

    by_collection: dict[str, dict[str, int]] = defaultdict(lambda: {"ok": 0, "err": 0})
    for r in all_logs:
        col = r.get("collection", "?")
        if r.get("error"):
            by_collection[col]["err"] += 1
        elif not r.get("skipped"):
            by_collection[col]["ok"] += 1

    summary_lines = [
        f"# Récap pipeline mockup — {datetime.datetime.now().isoformat(timespec='seconds')}",
        "",
        f"- Total entries logged: **{len(all_logs)}**",
        f"- Succès (asset généré): **{len(successes)}**",
        f"- Skipped (asset déjà présent): **{len(skipped)}**",
        f"- Erreurs: **{len(errors)}**",
        f"- Handles dans liste theme (product-card + product.liquid): **{n_total}**"
        f"  (+{n_added} ajoutés ce run)",
        "",
        "## Stats par collection",
        "",
        "| Collection | OK | Erreurs |",
        "|---|---:|---:|",
    ]
    for col in ("WANTED", "DIRECTION", "MYTHOLOGIE", "DESIGN HOKUNO"):
        s = by_collection.get(col, {"ok": 0, "err": 0})
        summary_lines.append(f"| {col} | {s['ok']} | {s['err']} |")

    if errors:
        summary_lines += ["", "## Erreurs détaillées", ""]
        summary_lines.append("| Product ID | Title | Collection | Erreur |")
        summary_lines.append("|---|---|---|---|")
        for r in errors:
            t = (r.get("title") or "")[:60].replace("|", "\\|")
            err = (r.get("error") or "")[:120].replace("|", "\\|")
            summary_lines.append(
                f"| {r.get('product_id','?')} | {t} | {r.get('collection','?')} | {err} |"
            )

    summary_path = config.LOG_DIR / "_SUMMARY.md"
    summary_path.write_text("\n".join(summary_lines))

    if started_at:
        elapsed = (datetime.datetime.now() - started_at).total_seconds()
        elapsed_str = f"{int(elapsed // 60)}m{int(elapsed % 60)}s"
    else:
        elapsed_str = "n/a"

    print("\n" + "=" * 70)
    print("🛑 PHASE 4 TERMINÉE — assets + liste mise à jour, theme NON pushé")
    print("=" * 70)
    print(f"Durée run    : {elapsed_str}")
    print(f"Total handles: {n_total} (+{n_added} ce run)")
    print(f"OK / Skip / Err : {len(successes)} / {len(skipped)} / {len(errors)}")
    print(f"\nRécap complet : {summary_path.relative_to(config.REPO_ROOT)}")
    print(f"Liste theme   : {PRODUCT_CARD.relative_to(config.REPO_ROOT)}")
    print(f"              {PRODUCT_TEMPLATE.relative_to(config.REPO_ROOT)}")
    print("\nProchaine étape (push live UNIQUEMENT après validation user) :")
    print(
        f"  cd shopify-theme && shopify theme push "
        f"--store={config.SHOPIFY_STORE} --theme=198885507415 "
        f"--allow-live --nodelete"
    )
    print("=" * 70)
    return 0


if __name__ == "__main__":
    sys.exit(run())
