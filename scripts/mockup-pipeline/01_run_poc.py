"""POC — generate 1 custom mockup per collection (4 total) + a 2x2 preview grid.

Run from the repo root:
    python scripts/mockup-pipeline/01_run_poc.py
"""
from __future__ import annotations

import json
import sys
import time
from pathlib import Path

# Flat imports inside scripts/mockup-pipeline (dash in dir name → no package)
sys.path.insert(0, str(Path(__file__).resolve().parent))

from PIL import Image, ImageDraw, ImageFont  # noqa: E402

import config  # noqa: E402
import printify_client  # noqa: E402
import collection_detector  # noqa: E402
import mockup_selector  # noqa: E402
import detourage  # noqa: E402
import compositing  # noqa: E402


COLLECTIONS = ["WANTED", "DIRECTION", "MYTHOLOGIE", "DESIGN HOKUNO"]


def pick_cobayes(products: list[dict]) -> dict[str, dict]:
    """One product per collection, preferring a t-shirt when available."""
    by_collection: dict[str, list[dict]] = {c: [] for c in COLLECTIONS}
    for p in products:
        c = collection_detector.detect_collection(p)
        by_collection.setdefault(c, []).append(p)

    chosen: dict[str, dict] = {}
    for c in COLLECTIONS:
        pool = by_collection.get(c, [])
        if not pool:
            continue
        tshirts = [p for p in pool if mockup_selector.detect_product_type(p) == "tshirt"]
        chosen[c] = (tshirts or pool)[0]
    return chosen


def _label(img: Image.Image, text: str) -> Image.Image:
    canvas = Image.new("RGB", (img.width, img.height + 60), "white")
    canvas.paste(img, (0, 60))
    draw = ImageDraw.Draw(canvas)
    try:
        font = ImageFont.truetype(
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 22
        )
    except OSError:
        font = ImageFont.load_default()
    draw.text((20, 18), text[:80], fill="black", font=font)
    return canvas


def build_preview(final_paths: list[tuple[str, Path]]) -> Path:
    if not final_paths:
        raise RuntimeError("No mockups produced — nothing to preview")

    cell = 750
    cols = 2
    rows = (len(final_paths) + cols - 1) // cols
    grid = Image.new("RGB", (cell * cols, (cell + 60) * rows), "white")

    for i, (label, path) in enumerate(final_paths):
        img = Image.open(path).convert("RGB").resize((cell, cell), Image.LANCZOS)
        labeled = _label(img, label)
        r, c = divmod(i, cols)
        grid.paste(labeled, (c * cell, r * (cell + 60)))

    out = config.FINAL_DIR / "_PREVIEW_grid.png"
    grid.save(out, "PNG")
    return out


def run() -> int:
    config.ensure_dirs()
    config.require_printify_token()

    print("→ Listing Printify products…")
    products = printify_client.list_all_products()
    print(f"  {len(products)} products fetched")

    chosen = pick_cobayes(products)
    if len(chosen) < len(COLLECTIONS):
        missing = [c for c in COLLECTIONS if c not in chosen]
        print(f"⚠  No cobaye for collection(s): {missing}")

    print("\n=== Cobayes sélectionnés ===")
    for c in COLLECTIONS:
        p = chosen.get(c)
        if p:
            ptype = mockup_selector.detect_product_type(p)
            print(f"  [{c:<14}] {p['id']}  {p.get('title','')[:60]}  (type={ptype})")
        else:
            print(f"  [{c:<14}] (aucun produit)")
    print("\n🛑 STOP intermédiaire — confirme la sélection avant de continuer ?")
    print("   (Ctrl+C pour annuler. Pour avancer en non-interactif : flag --yes)\n")
    if "--yes" not in sys.argv:
        try:
            input("Appuie sur Entrée pour continuer… ")
        except EOFError:
            pass

    results = []
    final_for_preview: list[tuple[str, Path]] = []

    for c in COLLECTIONS:
        product = chosen.get(c)
        if not product:
            continue
        pid = product["id"]
        title = product.get("title", "")
        ptype = mockup_selector.detect_product_type(product)
        bg_path = config.BG_BY_COLLECTION[c]

        t0 = time.time()
        print(f"\n[{c}] {pid}  {title[:60]}")
        print(f"  ├─ Type: {ptype}")

        try:
            img_meta = mockup_selector.pick_source_mockup(product, ptype)
            pos = img_meta.get("position") or "(no position)"
            src_url = img_meta.get("src")
            print(f"  ├─ Mockup source: {pos}")

            raw_bytes = printify_client.download_image(src_url)
            raw_path = config.RAW_DIR / f"{pid}.png"
            raw_path.write_bytes(raw_bytes)

            detoured = detourage.detoure(raw_bytes)
            det_path = config.DETOURED_DIR / f"{pid}.png"
            detoured.save(det_path, "PNG")
            print(f"  ├─ Détourage: OK ({detoured.width}x{detoured.height})")

            final_path = config.FINAL_DIR / f"{pid}.webp"
            compositing.compose(detoured, bg_path, ptype, final_path)
            size_kb = final_path.stat().st_size // 1024
            print(
                f"  ├─ Compositing: OK → "
                f"{final_path.relative_to(config.REPO_ROOT)} ({size_kb} KB)"
            )

            final_for_preview.append((f"[{c}] {title[:50]}", final_path))
            results.append({
                "product_id": pid,
                "title": title,
                "collection": c,
                "type": ptype,
                "mockup_position_used": pos,
                "handle": (product.get("external") or {}).get("handle"),
                "shopify_external_id": (product.get("external") or {}).get("id"),
                "raw": str(raw_path.relative_to(config.REPO_ROOT)),
                "detoured": str(det_path.relative_to(config.REPO_ROOT)),
                "final": str(final_path.relative_to(config.REPO_ROOT)),
                "duration_s": round(time.time() - t0, 2),
                "error": None,
            })
            print(f"  └─ Durée: {results[-1]['duration_s']}s")
        except Exception as e:
            print(f"  └─ ERROR: {e}")
            results.append({
                "product_id": pid,
                "collection": c,
                "title": title,
                "error": str(e),
            })

    log_path = config.LOG_DIR / "poc_results.json"
    log_path.write_text(json.dumps(results, indent=2, ensure_ascii=False))

    preview_path = build_preview(final_for_preview)

    print("\n" + "=" * 70)
    print("🛑 PHASE 2 TERMINÉE — POC sur 4 produits")
    print("=" * 70)
    print("Ouvre cette image et regarde le rendu :")
    print(f"  → {preview_path}")
    print("\nDétail par produit :")
    for r in results:
        if r.get("error"):
            print(f"  [{r['collection']:<14}] {r['product_id']}  ERROR: {r['error']}")
        else:
            print(
                f"  [{r['collection']:<14}] {r['product_id']}  "
                f"{r['title'][:50]} → {r['final']}"
            )
    print(f"\nLog JSON : {log_path.relative_to(config.REPO_ROOT)}")
    print("=" * 70)
    return 0


if __name__ == "__main__":
    sys.exit(run())
