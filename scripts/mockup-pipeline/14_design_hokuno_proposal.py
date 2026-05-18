"""Fix 14 — Build a proposal for the new 3-level Design Hokuno structure.

Outputs a draft JSON at output/design-hokuno-proposal.json with the new
shape: types → designs → dark/light → items. NO production files are
touched. The user reviews + approves before we wire it into
08_character_map.py and collection.liquid.

Categorization rules (per user spec):
  - "Polo"            → polo
  - "Short"           → short
  - "Coque" / "Case"  → accessoires
  - "Casquette"/"Bob" → accessoires
  - "Claquette"       → accessoires
  - "Maillot"         → accessoires (could split later)
  - "T-Shirt"/"T-shirt" → tshirt
  - everything else   → accessoires

Design extraction (case-insensitive, longest-match first):
  HO KU NO, HKN, TARGET, EMPREINTE, ORBITE, SIGNATURE, SPORT,
  BOUSSOLE, PATTERN  → that design
  anything else      → "hokuno"  (plain Hokuno-logo merch)
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import config  # noqa: E402
import printify_client  # noqa: E402
import collection_detector  # noqa: E402
import mockup_selector  # noqa: E402


OUT_PROPOSAL = config.REPO_ROOT / "output" / "design-hokuno-proposal.json"


# Category routing
CATEGORY_LABEL = {
    "tshirt":      "T-SHIRT",
    "polo":        "POLO",
    "short":       "SHORT",
    "accessoires": "ACCESSOIRES",
}
CATEGORY_ORDER = ["tshirt", "polo", "accessoires", "short"]


def categorize(title: str) -> str:
    u = title.upper()
    if "POLO" in u:                                     return "polo"
    if "SHORT" in u:                                    return "short"
    if "COQUE" in u or " CASE" in u:                    return "accessoires"
    if "CASQUETTE" in u or " BOB " in f" {u} ":         return "accessoires"
    if "CLAQUETTE" in u or "MAILLOT" in u:              return "accessoires"
    if re.search(r"\bT[- ]?SHIRT\b", u):                return "tshirt"
    return "accessoires"


# Sub-type detection for ACCESSOIRES (level 2 axis = sub-type, not design)
# Order matters — first match wins. Bob is matched as a whole word so
# "Bob Hokuno…" matches but a stray "BOB" inside another word does not.
_ACCESSORY_SUBTYPE_RULES: list[tuple[str, str, str]] = [
    # (regex pattern, slug, label)
    (r"\bBOB\b",        "bob",       "Bob"),
    (r"\bCASQUETTE\b",  "casquette", "Casquette"),
    (r"\bCLAQUETTE\b",  "claquette", "Claquette"),
    (r"\bMAILLOT\b",    "maillot",   "Maillot"),
    (r"\bCOQUE\b",      "coque",     "Coque"),
    (r"\bCASE\b",       "coque",     "Coque"),
]


def detect_accessory_subtype(title: str) -> tuple[str, str]:
    """Return (slug, label). Fallback bucket = (hokuno, Hokuno) for stray accessories."""
    u = title.upper()
    for pattern, slug, label in _ACCESSORY_SUBTYPE_RULES:
        if re.search(pattern, u):
            return slug, label
    return "hokuno", "Hokuno"


# Design tokens, longest-first to avoid partial matches
DESIGN_TOKENS: list[tuple[str, str, str]] = [
    # (needle, slug, label)
    ("HO KU NO",  "ho-ku-no",  "Ho Ku No"),
    ("EMPREINTE", "empreinte", "Empreinte"),
    ("SIGNATURE", "signature", "Signature"),
    ("BOUSSOLE",  "boussole",  "Boussole"),
    ("PATTERN",   "pattern",   "Pattern"),
    ("ORBITE",    "orbite",    "Orbite"),
    ("TARGET",    "target",    "Target"),
    ("SPORT",     "sport",     "Sport"),
    ("HKN",       "target",    "Target"),  # HKN is the Target design abbreviation
]


def detect_design(title: str) -> tuple[str, str]:
    u = title.upper()
    for needle, slug, label in DESIGN_TOKENS:
        if needle in u:
            return slug, label
    return "hokuno", "Hokuno"


def normalize_handle(raw: str | None) -> str | None:
    if not raw:
        return None
    h = raw.rstrip("/").split("/products/")[-1]
    return h.split("?", 1)[0].split("#", 1)[0] or None


def format_price(cents: int) -> str:
    euros = cents / 100.0
    return f"{euros:,.2f}".replace(",", " ").replace(".", ",") + " €"


def parse_product(product: dict) -> dict | None:
    title = (product.get("title") or "").strip()
    if collection_detector.detect_collection(product) != "DESIGN HOKUNO":
        return None
    handle = normalize_handle((product.get("external") or {}).get("handle"))
    if not handle:
        return None
    dark = mockup_selector.is_dark_product(product)
    category = categorize(title)
    # For ACCESSOIRES the level-2 axis is sub-type (bob, casquette, …);
    # for the other categories it's design (boussole, empreinte, …).
    if category == "accessoires":
        bucket_slug, bucket_label = detect_accessory_subtype(title)
    else:
        bucket_slug, bucket_label = detect_design(title)
    enabled = [v for v in product.get("variants", []) if v.get("is_enabled")]
    cents = min((v.get("price", 0) or 0 for v in enabled), default=0)
    return {
        "id": product["id"],
        "handle": handle,
        "title": title,
        "category": category,
        "bucket_slug": bucket_slug,
        "bucket_label": bucket_label,
        "dark": dark,
        "price_cents": cents,
        "price": format_price(cents),
    }


def pick_category_image(category: str, items: list[dict]) -> str | None:
    """Card image for the category (level 1).
    - tshirt: first dark t-shirt
    - polo:   first dark polo
    - accessoires: dark CASQUETTE first, then any casquette, then any dark item
    - short:  first item (no dark variants exist)
    """
    if not items:
        return None
    if category == "accessoires":
        # User picked Casquette dark as the level-1 visual for ACCESSOIRES.
        for it in items:
            if it["bucket_slug"] == "casquette" and it["dark"]:
                return it["handle"]
        for it in items:
            if it["bucket_slug"] == "casquette":
                return it["handle"]
    for it in items:
        if it["dark"]:
            return it["handle"]
    return items[0]["handle"]


def pick_design_image(items: list[dict], dark: bool) -> str | None:
    """Image for the design card inside a category (level 2)."""
    filtered = [i for i in items if i["dark"] == dark]
    if not filtered:
        return None
    return filtered[0]["handle"]


def build_proposal(products: list[dict]) -> dict:
    parsed = [p for p in (parse_product(pr) for pr in products) if p]

    # Group: category → bucket (design or accessory sub-type) → list[item]
    by_cat: dict[str, dict[str, list[dict]]] = {c: {} for c in CATEGORY_ORDER}
    for p in parsed:
        by_cat[p["category"]].setdefault(p["bucket_slug"], []).append(p)

    out: dict = {
        "type_navigation": True,
        "alphabet": False,
        "groups": [
            {"key": "dark",  "label": "Dark"},
            {"key": "light", "label": "Light"},
        ],
        "types": {},
    }
    type_order: list[str] = []
    for cat in CATEGORY_ORDER:
        buckets = by_cat[cat]
        if not buckets:
            continue
        type_order.append(cat)

        # All items in this category, used for the category card image
        all_items_in_cat = [it for bk in buckets.values() for it in bk]
        cat_image = pick_category_image(cat, all_items_in_cat)

        buckets_out: dict = {}
        # Order buckets alphabetically by label, pin "hokuno" catch-all last
        sorted_bucket_slugs = sorted(
            buckets.keys(),
            key=lambda s: (s == "hokuno", buckets[s][0]["bucket_label"].lower()),
        )
        for bs in sorted_bucket_slugs:
            items = sorted(buckets[bs], key=lambda x: (x["dark"], x["title"]))
            dark_items = [i for i in items if i["dark"]]
            light_items = [i for i in items if not i["dark"]]
            bucket_payload: dict = {
                "name": items[0]["bucket_label"],
                "slug": bs,
            }
            # Only emit a sub-group when it has at least one product —
            # hides empty Dark/Light cards in the niveau 2 view.
            if dark_items:
                bucket_payload["dark"] = {
                    "image_handle": pick_design_image(items, dark=True),
                    "items": [
                        {"handle": it["handle"], "title": it["title"],
                         "price": it["price"], "dark": True}
                        for it in dark_items
                    ],
                }
            if light_items:
                bucket_payload["light"] = {
                    "image_handle": pick_design_image(items, dark=False),
                    "items": [
                        {"handle": it["handle"], "title": it["title"],
                         "price": it["price"], "dark": False}
                        for it in light_items
                    ],
                }
            buckets_out[bs] = bucket_payload

        out["types"][cat] = {
            "label": CATEGORY_LABEL[cat],
            "slug": cat,
            "image_handle": cat_image,
            "designs": buckets_out,
        }

    out["type_order"] = type_order
    return out


def print_overview(prop: dict) -> None:
    print("\n" + "=" * 78)
    print("DESIGN HOKUNO — PROPOSED 3-LEVEL STRUCTURE")
    print("=" * 78)
    for cat in prop["type_order"]:
        node = prop["types"][cat]
        print(f"\n┌─ [{cat}] {node['label']}")
        print(f"│  image_handle = {node['image_handle']}")
        for ds_slug, ds in node["designs"].items():
            n_dark = len(ds.get("dark", {}).get("items", []))
            n_light = len(ds.get("light", {}).get("items", []))
            print(f"├──── [{ds_slug}] {ds['name']}  (dark={n_dark}, light={n_light})")
            if "dark" in ds:
                print(f"│         dark.image  = {ds['dark']['image_handle']}")
            if "light" in ds:
                print(f"│         light.image = {ds['light']['image_handle']}")
            for grp in ("dark", "light"):
                if grp not in ds:
                    continue
                for it in ds[grp]["items"]:
                    short = it["title"][:55]
                    print(f"│           {grp}: {short:<58} {it['price']}")


def run() -> int:
    config.ensure_dirs()
    config.require_printify_token()

    print("→ Fetching all Printify products…")
    products = printify_client.list_all_products()
    print(f"  {len(products)} products fetched")

    prop = build_proposal(products)
    print_overview(prop)

    OUT_PROPOSAL.parent.mkdir(parents=True, exist_ok=True)
    OUT_PROPOSAL.write_text(json.dumps(prop, ensure_ascii=False, indent=2))
    print(f"\nWrote proposal to {OUT_PROPOSAL.relative_to(config.REPO_ROOT)}")
    print("(No production files touched.)")
    return 0


if __name__ == "__main__":
    sys.exit(run())
