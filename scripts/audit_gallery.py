#!/usr/bin/env python3
"""Audit BP6 t-shirt gallery state across three sources:

  1. Printify: camera_label presence + is_selected_for_publishing for
     {front-2, back-2, folded} per product.
  2. Shopify storefront /products/{handle}.json: total image count and
     image src list (to verify what is actually published).
  3. snippets/printify-keep-positions.liquid: the whitelist positions
     currently shipped in the theme for each handle.

Emits:
  - output/audit-gallery.md       (Markdown table for humans)
  - output/audit-gallery.json     (machine-readable, used by fix scripts)

Categorisation (Status column):
  OK    — front-2, back-2, folded all present & selected on Printify,
          Shopify has them, and snippet (or mod-4 fallback) yields the
          expected 3 visible thumbs.
  A     — folded camera_label not present at all on Printify (must be
          re-enabled in the Printify dashboard).
  A-sel — folded present on Printify but NOT selected for publishing
          (toggle "Use as preview" in dashboard, or republish).
  B     — Printify has 3 selected cameras but Shopify is missing some
          (republish needed).
  C     — Snippet whitelist entry exists but positions don't match
          what Shopify is currently serving (regen snippet).
  D     — No snippet entry & mod-4 fallback would drop required images
          (add to whitelist).
  NOSHO — Product not published on Shopify (no handle / 404).
"""

from __future__ import annotations
import json
import os
import re
import sys
import time
from pathlib import Path

import requests

REPO_ROOT = Path(__file__).resolve().parents[1]
SHOPIFY_STORE = os.environ.get("SHOPIFY_STORE", "s6btxa-q0.myshopify.com")
SHOP_ID = "22774508"
KEEP_LABELS = {"front-2", "back-2", "folded"}
SNIPPET_PATH = REPO_ROOT / "shopify-theme" / "snippets" / "printify-keep-positions.liquid"
OUT_MD = REPO_ROOT / "output" / "audit-gallery.md"
OUT_JSON = REPO_ROOT / "output" / "audit-gallery.json"


def fetch_all_printify_products(token: str) -> list[dict]:
    headers = {"Authorization": f"Bearer {token}", "User-Agent": "Hokuno-audit/1.0"}
    out = []
    for page in range(1, 30):
        r = requests.get(
            f"https://api.printify.com/v1/shops/{SHOP_ID}/products.json",
            headers=headers,
            params={"page": page, "limit": 50},
            timeout=30,
        )
        r.raise_for_status()
        data = r.json()
        out.extend(data["data"])
        if page >= data.get("last_page", page):
            break
        time.sleep(0.3)
    return out


def camera_label(img: dict) -> str:
    src = img.get("src", "")
    if "?" not in src:
        return ""
    return src.split("?")[-1].replace("camera_label=", "")


def handle_from_product(p: dict) -> str | None:
    ext = p.get("external") or {}
    h = ext.get("handle", "")
    if not h:
        return None
    if "/products/" in h:
        return h.split("/products/")[-1]
    return h


def shopify_order(images: list[dict]) -> list[int]:
    indexed = list(enumerate(images))
    indexed.sort(key=lambda x: (0 if x[1].get("is_default") else 1, x[0]))
    return [i for i, _ in indexed]


def expected_keep_positions(images: list[dict]) -> list[int]:
    """1-indexed Shopify positions where camera_label is in KEEP_LABELS AND
    the image is selected for publishing."""
    order = shopify_order(images)
    out = []
    for shopify_idx, printify_idx in enumerate(order):
        img = images[printify_idx]
        if not img.get("is_selected_for_publishing"):
            continue
        if camera_label(img) in KEEP_LABELS:
            out.append(shopify_idx + 1)
    return out


def mod4_filter_predicted(total: int) -> set[int]:
    if total < 4 or total % 4 != 0:
        return set()
    n = total // 4
    out = set()
    for i in range(total):
        if i < n:
            continue
        rel = i - n
        if rel % 3 == 0:
            continue
        out.add(i + 1)
    return out


SNIPPET_LINE_RE = re.compile(
    r"^\s*\{%-\s*when\s+'([^']+)'\s*-%\}([0-9,]*)\{%-\s*comment\s*-%\}"
)


def parse_snippet(path: Path) -> dict[str, list[int]]:
    if not path.exists():
        return {}
    out: dict[str, list[int]] = {}
    for line in path.read_text().splitlines():
        m = SNIPPET_LINE_RE.match(line)
        if not m:
            continue
        handle = m.group(1)
        csv = m.group(2).strip()
        positions = [int(x) for x in csv.split(",") if x] if csv else []
        out[handle] = positions
    return out


BROWSER_UA = (
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
)


def fetch_all_shopify_products() -> dict[str, dict]:
    """Bulk-fetch every Shopify product via the public /products.json feed
    paginated 250 at a time. Returns a {handle: product} map.

    Per-handle endpoint hits a Cloudflare 403 after ~120 requests; the bulk
    feed doesn't, and returns the same image list.
    """
    out: dict[str, dict] = {}
    for page in range(1, 20):
        url = f"https://{SHOPIFY_STORE}/products.json"
        r = requests.get(
            url,
            params={"limit": 250, "page": page},
            headers={"User-Agent": BROWSER_UA},
            timeout=30,
        )
        r.raise_for_status()
        products = r.json().get("products", [])
        if not products:
            break
        for p in products:
            handle = p.get("handle")
            if handle:
                out[handle] = p
        if len(products) < 250:
            break
        time.sleep(0.3)
    return out


def audit():
    token = os.environ.get("PRINTIFY_API_TOKEN") or os.environ.get("PRINTIFY_TOKEN")
    if not token:
        print("ERROR: PRINTIFY_API_TOKEN env var required", file=sys.stderr)
        sys.exit(1)

    print(f"[1/4] Fetching Printify products…")
    products = fetch_all_printify_products(token)
    print(f"      {len(products)} products fetched")

    print(f"[2/4] Parsing snippet…")
    snippet_map = parse_snippet(SNIPPET_PATH)
    print(f"      {len(snippet_map)} snippet entries")

    print(f"[2b/4] Fetching all Shopify products in bulk…")
    shopify_by_handle = fetch_all_shopify_products()
    print(f"      {len(shopify_by_handle)} Shopify products fetched")

    bp6 = [p for p in products if p.get("blueprint_id") == 6]
    bp6_tshirts = [p for p in bp6 if "t-shirt " in p["title"].lower()]
    print(f"[3/4] BP6 t-shirts: {len(bp6_tshirts)}")

    rows = []
    print(f"[4/4] Auditing each (Printify cameras + Shopify total)…")
    for i, p in enumerate(bp6_tshirts, 1):
        title = p["title"]
        handle = handle_from_product(p)
        images = p.get("images", [])

        # Printify-side camera_label presence
        cams = {}
        for label in KEEP_LABELS:
            present = any(camera_label(img) == label for img in images)
            selected = any(
                camera_label(img) == label and img.get("is_selected_for_publishing")
                for img in images
            )
            cams[label] = {"present": present, "selected": selected}

        expected_positions = expected_keep_positions(images)

        # Shopify-side
        shopify_imgs = None
        shopify_total = None
        shopify_404 = False
        if handle and handle in shopify_by_handle:
            sp = shopify_by_handle[handle]
            shopify_imgs = sp.get("images", [])
            shopify_total = len(shopify_imgs)
        else:
            shopify_404 = True

        snippet_positions = snippet_map.get(handle or "", None)

        # Categorise
        f2_ok = cams["front-2"]["present"] and cams["front-2"]["selected"]
        b2_ok = cams["back-2"]["present"] and cams["back-2"]["selected"]
        folded_ok = cams["folded"]["present"] and cams["folded"]["selected"]

        if shopify_404:
            status = "NOSHO"
        elif not cams["folded"]["present"]:
            status = "A"
        elif not cams["folded"]["selected"]:
            status = "A-sel"
        elif not (f2_ok and b2_ok):
            # folded is fine but f2 or b2 is missing — different fix
            status = "F2B2"
        else:
            # All 3 cameras selected on Printify. Compare expected positions to
            # what the theme would actually render.
            mod4_set = mod4_filter_predicted(shopify_total or 0)
            uppercase_tshirt = "T-SHIRT " in title

            if snippet_positions is not None:
                # Snippet branch wins. Compare.
                if set(snippet_positions) == set(expected_positions):
                    # But still verify Shopify has enough images for these positions
                    if max(snippet_positions or [0]) <= (shopify_total or 0):
                        status = "OK"
                    else:
                        status = "B"
                else:
                    status = "C"
            else:
                # No snippet entry → falls through to mod-4 / render-all
                if uppercase_tshirt and set(expected_positions) == mod4_set and mod4_set:
                    status = "OK"
                else:
                    # mod-4 would drop required positions (or render all if 4N
                    # rule fails). Compare what mod-4/all would render.
                    rendered = (
                        mod4_set
                        if (uppercase_tshirt and (shopify_total or 0) % 4 == 0 and (shopify_total or 0) >= 4)
                        else set(range(1, (shopify_total or 0) + 1))
                    )
                    if set(expected_positions).issubset(rendered) and rendered.issubset(set(expected_positions)):
                        status = "OK"
                    else:
                        status = "D"

        rows.append({
            "handle": handle or "",
            "title": title,
            "printify_id": p["id"],
            "cams": cams,
            "expected_positions": expected_positions,
            "snippet_positions": snippet_positions,
            "shopify_total": shopify_total,
            "shopify_404": shopify_404,
            "status": status,
        })

        if i % 25 == 0 or i == len(bp6_tshirts):
            print(f"      {i}/{len(bp6_tshirts)}")

    # Summary counts
    from collections import Counter
    status_counts = Counter(r["status"] for r in rows)

    # Write JSON
    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps(rows, indent=2, ensure_ascii=False))

    # Write Markdown
    md = []
    md.append("# Audit galerie t-shirts BP6\n")
    md.append(f"- Total t-shirts BP6 inspectés : **{len(rows)}**")
    md.append(f"- Snippet entries actuelles : **{len(snippet_map)}**")
    md.append("")
    md.append("## Récap par statut\n")
    md.append("| Statut | Count | Description |")
    md.append("|---|---|---|")
    legend = {
        "OK": "Tout est cohérent (front-2 + back-2 + folded visibles)",
        "A": "**folded absent** du produit Printify (camera_label introuvable) → ré-activer via dashboard",
        "A-sel": "folded présent sur Printify mais **pas sélectionné pour publication** → toggle dashboard / republier",
        "F2B2": "folded OK mais **front-2 ou back-2 manquant/non sélectionné** sur Printify",
        "B": "Printify OK mais **Shopify n'a pas les images** (republier)",
        "C": "Snippet positions **incorrectes** vs ce que Shopify expose (régénérer snippet)",
        "D": "**Pas d'entrée snippet** et la règle mod-4 masque des images requises",
        "NOSHO": "Produit pas publié sur Shopify (404 sur le handle)",
    }
    for s in ["OK", "A", "A-sel", "F2B2", "B", "C", "D", "NOSHO"]:
        md.append(f"| `{s}` | {status_counts.get(s, 0)} | {legend[s]} |")
    md.append("")

    md.append("## Détail\n")
    md.append("| Handle | f2 P | b2 P | fold P | f2 sel | b2 sel | fold sel | Sho imgs | Snippet | Expected | Status |")
    md.append("|---|---|---|---|---|---|---|---|---|---|---|")
    def tick(b):
        return "✅" if b else "❌"
    for r in rows:
        c = r["cams"]
        snip = (
            "—"
            if r["snippet_positions"] is None
            else (",".join(str(x) for x in r["snippet_positions"]) or "∅")
        )
        exp = ",".join(str(x) for x in r["expected_positions"]) or "∅"
        sho = "—" if r["shopify_total"] is None else str(r["shopify_total"])
        md.append(
            f"| `{r['handle'] or r['printify_id']}` | "
            f"{tick(c['front-2']['present'])} | {tick(c['back-2']['present'])} | {tick(c['folded']['present'])} | "
            f"{tick(c['front-2']['selected'])} | {tick(c['back-2']['selected'])} | {tick(c['folded']['selected'])} | "
            f"{sho} | {snip} | {exp} | **{r['status']}** |"
        )
    md.append("")

    # Action lists
    md.append("## Listes d'action\n")
    for cat in ["A", "A-sel", "F2B2", "B", "C", "D", "NOSHO"]:
        bucket = [r for r in rows if r["status"] == cat]
        if not bucket:
            continue
        md.append(f"### {cat} ({len(bucket)})\n")
        for r in bucket:
            md.append(f"- `{r['printify_id']}` — {r['title']}  (`{r['handle']}`)")
        md.append("")

    OUT_MD.write_text("\n".join(md))
    print(f"\nWrote {OUT_MD.relative_to(REPO_ROOT)}")
    print(f"Wrote {OUT_JSON.relative_to(REPO_ROOT)}")
    print("\nSummary:")
    for s in ["OK", "A", "A-sel", "F2B2", "B", "C", "D", "NOSHO"]:
        print(f"  {s:<6} : {status_counts.get(s, 0)}")


if __name__ == "__main__":
    audit()
