#!/usr/bin/env python3
"""Generate snippets/printify-keep-positions.liquid — per-handle whitelist of
gallery positions to KEEP for t-shirt products whose image layout the simple
modulo-4 filter can't handle (non-conforming Printify mockup mixes:
mannequins, folded, size-chart, etc.).

Rule for what to keep: Printify camera_label in {"front-2", "back-2", "folded"}
(realistic with-folds mockups + the folded-t-shirt view). Everything else is hidden.

Shopify position ordering (verified): images sorted by
  (is_default desc, original_printify_index asc)
i.e. variant-attached images first (in Printify natural order),
then unattached (in Printify natural order).

Run:
  PRINTIFY_API_TOKEN=... python3 scripts/gen_keep_positions.py

Output: shopify-theme/snippets/printify-keep-positions.liquid
"""

from __future__ import annotations
import json
import os
import sys
import time
from pathlib import Path

import requests

SHOP_ID = "22774508"
KEEP_LABELS = {"front-2", "back-2", "folded"}
REPO_ROOT = Path(__file__).resolve().parents[1]
SNIPPET_PATH = REPO_ROOT / "shopify-theme" / "snippets" / "printify-keep-positions.liquid"


def fetch_all_products(token: str) -> list[dict]:
    headers = {"Authorization": f"Bearer {token}", "User-Agent": "Hokuno-gen-keep-positions/1.0"}
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
        if page >= data["last_page"]:
            break
        time.sleep(0.3)
    return out


def shopify_order(images: list[dict]) -> list[int]:
    """Return Printify indices in the order Shopify would display them."""
    indexed = list(enumerate(images))
    indexed.sort(key=lambda x: (0 if x[1].get("is_default") else 1, x[0]))
    return [i for i, _ in indexed]


def camera_label(img: dict) -> str:
    src = img.get("src", "")
    if "?" not in src:
        return ""
    return src.split("?")[-1].replace("camera_label=", "")


def handle_from_product(p: dict) -> str | None:
    ext = p.get("external") or {}
    h = ext.get("handle", "")
    if "/products/" in h:
        return h.split("/products/")[-1]
    return h or None


def is_tshirt_title(title: str) -> bool:
    return "t-shirt " in title.lower()


def keep_positions_for(p: dict) -> list[int]:
    """1-indexed Shopify positions where camera_label in KEEP_LABELS."""
    order = shopify_order(p["images"])
    out = []
    for shopify_idx, printify_idx in enumerate(order):
        label = camera_label(p["images"][printify_idx])
        if label in KEEP_LABELS:
            out.append(shopify_idx + 1)  # Shopify positions are 1-indexed
    return out


def mod4_filter_predicted(total: int) -> set[int]:
    """1-indexed positions the existing mod-4 rule keeps."""
    if total < 4 or total % 4 != 0:
        return set()
    n = total // 4
    out = set()
    for i in range(total):  # 0-indexed
        if i < n:
            continue
        rel = i - n
        if rel % 3 == 0:
            continue
        out.add(i + 1)
    return out


def main() -> int:
    token = os.environ.get("PRINTIFY_API_TOKEN")
    if not token:
        print("ERROR: PRINTIFY_API_TOKEN env var required", file=sys.stderr)
        return 1

    print("Fetching products from Printify…")
    products = fetch_all_products(token)
    print(f"  {len(products)} products fetched")

    entries: list[tuple[str, list[int], str]] = []
    skipped_mod4 = 0
    skipped_no_handle = 0
    skipped_no_keeps = 0

    for p in products:
        if p.get("blueprint_id") != 6:
            continue
        if not is_tshirt_title(p["title"]):
            continue
        handle = handle_from_product(p)
        if not handle:
            skipped_no_handle += 1
            continue

        total = len(p["images"])
        keeps = keep_positions_for(p)

        if not keeps:
            # No realistic-with-folds mockups → render-all fallback is safer than empty gallery
            skipped_no_keeps += 1
            continue

        # If existing mod-4 rule already produces the same keep set, skip the whitelist entry —
        # but ONLY for uppercase "T-SHIRT " titles, because the Liquid fallback discriminator
        # is case-sensitive and won't catch mixed-case "T-Shirt " products.
        if "T-SHIRT " in p["title"] and set(keeps) == mod4_filter_predicted(total):
            skipped_mod4 += 1
            continue

        entries.append((handle, keeps, p["title"]))

    entries.sort(key=lambda e: e[0])

    print(f"\nSummary:")
    print(f"  whitelist entries: {len(entries)}")
    print(f"  covered by mod-4: {skipped_mod4}")
    print(f"  no realistic mockups (kept as-is): {skipped_no_keeps}")
    print(f"  no Shopify handle: {skipped_no_handle}")

    lines = [
        "{%- comment -%}",
        "  printify-keep-positions.liquid — generated by scripts/gen_keep_positions.py",
        "  Per-handle whitelist of 1-indexed gallery positions to render for t-shirts",
        "  whose Printify mockup mix isn't covered by the modulo-4 filter (mannequins,",
        "  size charts, folded views, custom selections). Do not edit by hand — re-run",
        "  the script after any Printify-side cleanup.",
        "  Used via {% render %} + {% capture %} — outputs the CSV directly so the",
        "  parent template can capture it (variable isolation in render means we can't",
        "  just {% assign %}).",
        "{%- endcomment -%}",
        "{%- case product.handle -%}",
    ]
    for handle, keeps, title in entries:
        csv = ",".join(str(x) for x in keeps)
        lines.append(f"  {{%- when '{handle}' -%}}{csv}{{%- comment -%}} {title} {{%- endcomment -%}}")
    lines.append("{%- endcase -%}")
    lines.append("")

    SNIPPET_PATH.parent.mkdir(parents=True, exist_ok=True)
    SNIPPET_PATH.write_text("\n".join(lines))
    print(f"\nWrote {SNIPPET_PATH.relative_to(REPO_ROOT)} ({len(entries)} entries)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
