"""Build shopify-theme/assets/character-map.json from Printify titles.

Adds a top-level `_cache_bust` timestamp on each write so the storefront
sees a different file payload and forces the CDN+browser to refetch even
when the rest of the map is unchanged.

Output structure (one entry per Hokuno collection):

    {
      "WANTED": {
        "alphabet": true,
        "groups": [
          {"key": "fr",          "label": "FR"},
          {"key": "en",          "label": "EN"},
          {"key": "accessories", "label": "Accessoires"}
        ],
        "entries": {
          "sanji": {
            "name": "Sanji",
            "image_handle": "t-shirt-sanji-wanted-noir-5-46",
            "fr":          [{"handle","title","price","dark","ptype"}, …],
            "en":          [...],
            "accessories": [...]
          },
          …
        }
      },
      "DIRECTION":     same shape as WANTED
      "MYTHOLOGIE":    groups = [clothing, accessories]; alphabet true
      "DESIGN HOKUNO": groups = [dark, light]; alphabet false
    }

The JS layer renders one card per non-empty group of each entry; collections
where alphabet=false skip the A-Z bar.

Run:
    python scripts/mockup-pipeline/08_character_map.py
    python scripts/mockup-pipeline/08_character_map.py --dry-run
"""
from __future__ import annotations

import datetime
import json
import re
import sys
import unicodedata
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import config  # noqa: E402
import printify_client  # noqa: E402
import collection_detector  # noqa: E402
import mockup_selector  # noqa: E402


OUT_FILE = config.SHOPIFY_ASSETS_DIR / "character-map.json"


# ─── Title parsing ─────────────────────────────────────────────────────────

def _strip_accents(s: str) -> str:
    return "".join(
        c for c in unicodedata.normalize("NFKD", s)
        if not unicodedata.combining(c)
    )


def _normalize_handle(raw: str | None) -> str | None:
    if not raw:
        return None
    h = raw.rstrip("/").split("/products/")[-1]
    return h.split("?", 1)[0].split("#", 1)[0] or None


def _title_case_name(s: str) -> str:
    """Title-case a name while preserving 'Di', 'Le' etc. as written by us."""
    parts = re.split(r"\s+", s.strip())
    return " ".join(p.capitalize() for p in parts if p)


def _slug(s: str) -> str:
    s = _strip_accents(s).lower()
    s = re.sub(r"[^a-z0-9]+", "-", s).strip("-")
    return s


# Slug aliases — fold short/typo'd parsed slugs into the canonical character slug.
# Tasse "Tittch" / "Zoro" sont des mugs Wanted nommés par diminutif alors que
# les tees portent le nom complet — on les ramène sur le bon perso.
ALIAS_BY_COLLECTION = {
    "WANTED": {
        "tittch": "marshal-di-tittch",
        "zoro":   "rororoa-zoro",
    },
}


def _resolve_slug(collection: str, slug: str) -> str:
    return ALIAS_BY_COLLECTION.get(collection, {}).get(slug, slug)


# Manual display-name overrides. Use when the parser extracts a name that
# doesn't match the canonical Hokuno character (e.g. Printify title typos).
# Key = final slug (post-alias). Value = display name to show on the card.
# Empty by default — add entries as Hokuno team validates the rendered cards.
NAME_OVERRIDES_BY_COLLECTION: dict[str, dict[str, str]] = {
    "WANTED": {
        # "wrong-slug": "Correct Name",
    },
    "DIRECTION": {},
    "MYTHOLOGIE": {},
    "DESIGN HOKUNO": {},
}


def _apply_name_override(collection: str, slug: str, parsed_name: str) -> str:
    return NAME_OVERRIDES_BY_COLLECTION.get(collection, {}).get(slug, parsed_name)




def detect_language(title: str) -> str | None:
    """Return 'en' if title carries an explicit EN tag, 'fr' if it carries FR,
    None if no language marker (used for collections without FR/EN split).
    """
    u = title.upper()
    if re.search(r"\bEN\b", u):
        return "en"
    if re.search(r"\bFR\b", u):
        return "fr"
    return None


# Per-collection character/design extraction

def extract_wanted(upper: str, ptype: str) -> str | None:
    if ptype == "tshirt":
        m = re.match(r"^T[- ]?SHIRT\s+(.+?)\s+WANTED\b", upper)
        if m:
            return _clean_name(m.group(1))
    if ptype == "mug":
        m = re.search(r"WANTED\s+(.+?)\s+\(", upper)
        if m:
            return _clean_name(m.group(1))
    if ptype == "phonecase":
        # Single product: "Coque Wanted The End Brique Saga 1"
        m = re.search(r"WANTED\s+(.+?)$", upper)
        if m:
            return _clean_name(m.group(1))
    return None


def extract_direction(upper: str, ptype: str) -> str | None:
    if ptype == "tshirt":
        m = re.match(r"^T[- ]?SHIRT\s+(.+?)\s+DIRECTION\b", upper)
        if m:
            return _clean_name(m.group(1))
    if ptype == "mug":
        m = re.search(
            r"DIRECTION\s+(.+?)(?:\s+(?:BLACK|NOIRE))?\s+\(",
            upper,
        )
        if m:
            return _clean_name(m.group(1))
    return None


def extract_mythologie(upper: str, ptype: str) -> str | None:
    if ptype == "tshirt":
        m = re.match(r"^T[- ]?SHIRT\s+(.+?)\s+MYTHOLOGIE\b", upper)
        if m:
            return _clean_name(m.group(1))
    if ptype == "mug":
        # Old format: "MYTHOLOGIE X Ceramic Mug, (11oz, 15oz)"
        m = re.search(r"MYTHOLOGIE\s+(.+?)\s+CERAMIC\s+MUG", upper)
        if m:
            return _clean_name(m.group(1))
        # New format: "Black Mug Mythologie X (11oz, 15oz)"
        m = re.search(r"MYTHOLOGIE\s+(.+?)\s+\(", upper)
        if m:
            return _clean_name(m.group(1))
    if ptype == "phonecase":
        m = re.search(r"DARK\s+(.+?)\s+MYTHOLOGIE\b", upper)
        if m:
            return _clean_name(m.group(1))
    return None


# Known design names for the DESIGN HOKUNO collection
_DESIGN_TOKENS = (
    ("HO KU NO",  "Ho Ku No"),
    ("BOUSSOLE",  "Boussole"),
    ("SIGNATURE", "Signature"),
    ("EMPREINTE", "Empreinte"),
    ("ORBITE",    "Orbite"),
    ("TARGET",    "Target"),
    ("HKN",       "Target"),
    ("SPORT",     "Sport"),
)


def extract_design_hokuno(upper: str, ptype: str) -> str | None:
    if "SHORT DE BAIN" in upper:
        return "Short de Bain"
    for needle, label in _DESIGN_TOKENS:
        if needle in upper:
            return label
    # Catch-all bucket — Bob/Casquette/Maillot/plain "Design Hokuno" tees etc.
    return "Hokuno"


def _clean_name(s: str) -> str:
    s = re.sub(r"\b(NOIR|DARK|BLACK|NOIRE|EN|FR|XL)\b", "", s, flags=re.I)
    s = re.sub(r"\d+/\d+", "", s)
    s = re.sub(r"\s+", " ", s).strip()
    return _title_case_name(s)


def parse_product(product: dict) -> dict | None:
    title = (product.get("title") or "").strip()
    upper = title.upper()
    collection = collection_detector.detect_collection(product)
    ptype = mockup_selector.detect_product_type(product)
    dark = mockup_selector.is_dark_product(product)
    lang = detect_language(title)
    handle = _normalize_handle((product.get("external") or {}).get("handle"))
    if not handle:
        return None

    if collection == "WANTED":
        name = extract_wanted(upper, ptype)
    elif collection == "DIRECTION":
        name = extract_direction(upper, ptype)
    elif collection == "MYTHOLOGIE":
        name = extract_mythologie(upper, ptype)
    else:
        name = extract_design_hokuno(upper, ptype)

    if not name:
        return None

    # Cheapest enabled price → euros formatted like "37,99 €"
    enabled = [v for v in product.get("variants", []) if v.get("is_enabled")]
    cents = min((v.get("price", 0) or 0 for v in enabled), default=0)
    euros = cents / 100.0
    price_str = f"{euros:,.2f}".replace(",", " ").replace(".", ",") + " €"

    return {
        "collection": collection,
        "name": name,
        "slug": _slug(name),
        "handle": handle,
        "title": title,
        "price": price_str,
        "price_cents": cents,
        "dark": dark,
        "language": lang,
        "ptype": ptype,
    }


# ─── Grouping per collection ───────────────────────────────────────────────

def _group_for(collection: str, parsed: dict) -> str:
    ptype = parsed["ptype"]
    lang = parsed["language"]
    dark = parsed["dark"]

    if collection in ("WANTED", "DIRECTION"):
        if ptype == "tshirt":
            return lang or "fr"  # tees without language tag = FR
        return "accessories"
    if collection == "MYTHOLOGIE":
        return "clothing" if ptype == "tshirt" else "accessories"
    if collection == "DESIGN HOKUNO":
        return "dark" if dark else "light"
    return "accessories"


COLLECTION_LAYOUT = {
    "WANTED": {
        "alphabet": True,
        "groups": [
            {"key": "fr",          "label": "FR"},
            {"key": "en",          "label": "EN"},
            {"key": "accessories", "label": "Accessoires"},
        ],
    },
    "DIRECTION": {
        "alphabet": True,
        "groups": [
            {"key": "fr",          "label": "FR"},
            {"key": "en",          "label": "EN"},
            {"key": "accessories", "label": "Accessoires"},
        ],
    },
    "MYTHOLOGIE": {
        "alphabet": True,
        "groups": [
            {"key": "clothing",    "label": "Vêtements"},
            {"key": "accessories", "label": "Accessoires"},
        ],
    },
    # DESIGN HOKUNO uses a 3-level type/design/group structure, built
    # separately by build_design_hokuno_block() and spliced into the output.
}


# ─── DESIGN HOKUNO — 3-level type navigation ───────────────────────────────
DH_CATEGORY_LABEL = {
    "tshirt":      "T-SHIRT",
    "polo":        "POLO",
    "short":       "SHORT",
    "accessoires": "ACCESSOIRES",
}
DH_CATEGORY_ORDER = ["tshirt", "polo", "accessoires", "short"]


def _dh_categorize(title: str) -> str:
    u = title.upper()
    if "POLO" in u:                                     return "polo"
    # Maillot de bain = swim trunk → same category as shorts (BP 978 anyway).
    if "SHORT" in u or "MAILLOT" in u:                  return "short"
    if "COQUE" in u or " CASE" in u:                    return "accessoires"
    if "CASQUETTE" in u or re.search(r"\bBOB\b", u):    return "accessoires"
    if "CLAQUETTE" in u:                                return "accessoires"
    if re.search(r"\bT[- ]?SHIRT\b", u):                return "tshirt"
    return "accessoires"


_DH_ACCESSORY_SUBTYPE_RULES: list[tuple[str, str, str]] = [
    (r"\bBOB\b",        "bob",       "Bob"),
    (r"\bCASQUETTE\b",  "casquette", "Casquette"),
    (r"\bCLAQUETTE\b",  "claquette", "Claquette"),
    (r"\bCOQUE\b",      "coque",     "Coque"),
    (r"\bCASE\b",       "coque",     "Coque"),
]


def _dh_accessory_subtype(title: str) -> tuple[str, str]:
    u = title.upper()
    for pattern, slug, label in _DH_ACCESSORY_SUBTYPE_RULES:
        if re.search(pattern, u):
            return slug, label
    return "hokuno", "Hokuno"


_DH_DESIGN_TOKENS: list[tuple[str, str, str]] = [
    ("HO KU NO",  "ho-ku-no",  "Ho Ku No"),
    ("EMPREINTE", "empreinte", "Empreinte"),
    ("SIGNATURE", "signature", "Signature"),
    ("BOUSSOLE",  "boussole",  "Boussole"),
    ("PATTERN",   "pattern",   "Pattern"),
    ("ORBITE",    "orbite",    "Orbite"),
    ("TARGET",    "target",    "Target"),
    ("SPORT",     "sport",     "Sport"),
    ("HKN",       "target",    "Target"),
]


def _dh_design(title: str) -> tuple[str, str]:
    u = title.upper()
    for needle, slug, label in _DH_DESIGN_TOKENS:
        if needle in u:
            return slug, label
    return "hokuno", "Hokuno"


def _dh_parse_product(product: dict) -> dict | None:
    title = (product.get("title") or "").strip()
    if collection_detector.detect_collection(product) != "DESIGN HOKUNO":
        return None
    handle = _normalize_handle((product.get("external") or {}).get("handle"))
    if not handle:
        return None
    category = _dh_categorize(title)
    if category == "accessoires":
        bucket_slug, bucket_label = _dh_accessory_subtype(title)
    else:
        bucket_slug, bucket_label = _dh_design(title)
    enabled = [v for v in product.get("variants", []) if v.get("is_enabled")]
    cents = min((v.get("price", 0) or 0 for v in enabled), default=0)
    euros = cents / 100.0
    price = f"{euros:,.2f}".replace(",", " ").replace(".", ",") + " €"
    return {
        "handle":       handle,
        "title":        title,
        "category":     category,
        "bucket_slug":  bucket_slug,
        "bucket_label": bucket_label,
        "dark":         mockup_selector.is_dark_product(product),
        "price":        price,
    }


def _dh_pick_category_image(category: str, items: list[dict]) -> str | None:
    """Level-1 card image for a category."""
    if not items:
        return None
    if category == "accessoires":
        # Per design spec: ACCESSOIRES card uses a dark casquette
        for it in items:
            if it["bucket_slug"] == "casquette" and it["dark"]:
                return it["handle"]
        for it in items:
            if it["bucket_slug"] == "casquette":
                return it["handle"]
    if category == "short":
        # Shorts have no real dark/light split (the maillot is white-bodied
        # like the rest); pick a vibrant colored short for the category card
        # so it doesn't render as a white blob.
        for color_word in ("bleu", "rouge", "vert", "jaune", "rose", "bleu-ciel", "pattern"):
            for it in items:
                if color_word in it["handle"].lower():
                    return it["handle"]
    for it in items:
        if it["dark"]:
            return it["handle"]
    return items[0]["handle"]


def _dh_pick_bucket_image(items: list[dict], dark: bool) -> str | None:
    for it in items:
        if it["dark"] == dark:
            return it["handle"]
    return None


def build_design_hokuno_block(products: list[dict]) -> dict:
    """Return the 3-level type-navigation structure for DESIGN HOKUNO.

    Shape:
      {
        "type_navigation": true,
        "alphabet": false,
        "groups": [{"key":"dark","label":"Dark"},{"key":"light","label":"Light"}],
        "type_order": ["tshirt","polo","accessoires","short"],
        "types": {
          "tshirt": {
            "label": "T-SHIRT",
            "slug":  "tshirt",
            "image_handle": "...",
            "designs": {
              "empreinte": {
                "name": "Empreinte",
                "slug": "empreinte",
                "dark":  {"image_handle": "...", "items": [...]},  // omitted if 0 items
                "light": {"image_handle": "...", "items": [...]}   // omitted if 0 items
              },
              ...
            }
          },
          "accessoires": {...designs keyed by sub-type (bob/casquette/.../coque)...},
          ...
        }
      }
    """
    parsed = [p for p in (_dh_parse_product(pr) for pr in products) if p]

    by_cat: dict[str, dict[str, list[dict]]] = {c: {} for c in DH_CATEGORY_ORDER}
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
    for cat in DH_CATEGORY_ORDER:
        buckets = by_cat[cat]
        if not buckets:
            continue
        type_order.append(cat)

        all_items_in_cat = [it for bk in buckets.values() for it in bk]
        cat_image = _dh_pick_category_image(cat, all_items_in_cat)

        # SHORT category is flat: shorts/maillots all share the same silhouette
        # and don't really split along Dark/Light. Niveau 1 click → product grid.
        if cat == "short":
            flat_items = sorted(
                all_items_in_cat,
                key=lambda x: (x["bucket_slug"] != "hokuno",
                               not x["dark"], x["title"]),
            )
            out["types"][cat] = {
                "label":        DH_CATEGORY_LABEL[cat],
                "slug":         cat,
                "image_handle": cat_image,
                "flat":         True,
                "items": [
                    {"handle": it["handle"], "title": it["title"],
                     "price": it["price"], "dark": it["dark"]}
                    for it in flat_items
                ],
            }
            continue

        buckets_out: dict = {}
        sorted_bucket_slugs = sorted(
            buckets.keys(),
            key=lambda s: (s == "hokuno", buckets[s][0]["bucket_label"].lower()),
        )
        for bs in sorted_bucket_slugs:
            items = sorted(buckets[bs], key=lambda x: (x["dark"], x["title"]))
            dark_items  = [i for i in items if i["dark"]]
            light_items = [i for i in items if not i["dark"]]
            bucket_payload: dict = {
                "name": items[0]["bucket_label"],
                "slug": bs,
            }
            # Only emit sub-groups that actually have products — hides empty
            # Dark/Light cards in the niveau 2 view (e.g. Signature is dark-only).
            if dark_items:
                bucket_payload["dark"] = {
                    "image_handle": _dh_pick_bucket_image(items, dark=True),
                    "items": [
                        {"handle": it["handle"], "title": it["title"],
                         "price": it["price"], "dark": True}
                        for it in dark_items
                    ],
                }
            if light_items:
                bucket_payload["light"] = {
                    "image_handle": _dh_pick_bucket_image(items, dark=False),
                    "items": [
                        {"handle": it["handle"], "title": it["title"],
                         "price": it["price"], "dark": False}
                        for it in light_items
                    ],
                }
            buckets_out[bs] = bucket_payload

        out["types"][cat] = {
            "label":        DH_CATEGORY_LABEL[cat],
            "slug":         cat,
            "image_handle": cat_image,
            "designs":      buckets_out,
        }

    out["type_order"] = type_order
    return out


def _pick_image_for_group(items: list[dict], group_key: str) -> str | None:
    """Pick the most representative product handle for a group's card image.

    Per group preferences (first match wins):
      - fr           : light tee → dark tee → any tee → first item
      - en           : dark tee  → light tee → any tee → first item
      - accessories  : mug → phonecase → casquette → first item
      - clothing     : light tee → dark tee → any tee → first item
      - dark         : dark tee → dark anything → first item
      - light        : light tee → light anything → first item
    """
    if not items:
        return None

    PREFERENCES = {
        "fr": [
            lambda i: i["ptype"] == "tshirt" and not i["dark"],
            lambda i: i["ptype"] == "tshirt" and i["dark"],
            lambda i: i["ptype"] == "tshirt",
        ],
        "en": [
            lambda i: i["ptype"] == "tshirt" and i["dark"],
            lambda i: i["ptype"] == "tshirt" and not i["dark"],
            lambda i: i["ptype"] == "tshirt",
        ],
        "accessories": [
            # Dark mug EN  (handle starts "ceramic-mug-…-black-…")
            lambda i: i["ptype"] == "mug" and i["dark"] and i["handle"].startswith("ceramic-mug"),
            # Dark mug FR  (handle starts "tasse-en-ceramique-…-noire-…")
            lambda i: i["ptype"] == "mug" and i["dark"],
            # Any mug (fallback for collections like Wanted/Mythologie where BP 478 has no dark variant)
            lambda i: i["ptype"] == "mug",
            # Dark phonecase
            lambda i: i["ptype"] == "phonecase" and i["dark"],
            # Any phonecase
            lambda i: i["ptype"] == "phonecase",
            # Casquette / bob
            lambda i: i["ptype"] == "casquette",
        ],
        "clothing": [
            lambda i: i["ptype"] == "tshirt" and not i["dark"],
            lambda i: i["ptype"] == "tshirt" and i["dark"],
            lambda i: i["ptype"] == "tshirt",
        ],
        "dark": [
            lambda i: i["ptype"] == "tshirt",
            lambda i: i["dark"],
        ],
        "light": [
            lambda i: i["ptype"] == "tshirt",
            lambda i: not i["dark"],
        ],
    }
    for pred in PREFERENCES.get(group_key, []):
        for it in items:
            if pred(it):
                return it["handle"]
    return items[0]["handle"]


def build_map(products: list[dict]) -> tuple[dict, list[dict]]:
    """Return (character_map, unmatched_list)."""
    raw = defaultdict(lambda: defaultdict(lambda: {
        "_items_by_group": defaultdict(list),
        "_name": None,
    }))
    unmatched: list[dict] = []

    for product in products:
        # DESIGN HOKUNO is built separately via build_design_hokuno_block().
        if collection_detector.detect_collection(product) == "DESIGN HOKUNO":
            continue
        parsed = parse_product(product)
        if not parsed:
            unmatched.append({
                "id": product.get("id"),
                "title": product.get("title"),
                "reason": "no name / no handle",
            })
            continue
        col = parsed["collection"]
        slug = _resolve_slug(col, parsed["slug"])
        group = _group_for(col, parsed)

        entry = raw[col][slug]
        # Prefer the longer/more complete name when aliases collide
        if not entry["_name"] or len(parsed["name"]) > len(entry["_name"]):
            entry["_name"] = parsed["name"]
        entry["_items_by_group"][group].append(parsed)
        entry["_slug"] = slug
        entry["_collection"] = col

    out: dict = {}
    for col, layout in COLLECTION_LAYOUT.items():
        entries_in = raw.get(col, {})
        entries_out: dict = {}
        for slug in sorted(entries_in.keys()):
            entry = entries_in[slug]
            display_name = _apply_name_override(col, slug, entry["_name"])
            payload = {"name": display_name, "slug": slug}
            for grp in layout["groups"]:
                items = entry["_items_by_group"].get(grp["key"], [])
                items_sorted = sorted(
                    items,
                    key=lambda x: (x["dark"], x["ptype"], x["title"]),
                )
                payload[grp["key"]] = {
                    "image_handle": _pick_image_for_group(items_sorted, grp["key"]),
                    "items": [
                        {
                            "handle": it["handle"],
                            "title": it["title"],
                            "price": it["price"],
                            "dark": it["dark"],
                            "ptype": it["ptype"],
                        }
                        for it in items_sorted
                    ],
                }
            entries_out[slug] = payload

        out[col] = {
            "alphabet": layout["alphabet"],
            "groups": layout["groups"],
            "entries": entries_out,
        }

    # Splice in the 3-level Design Hokuno block.
    out["DESIGN HOKUNO"] = build_design_hokuno_block(products)

    return out, unmatched


# ─── Main ──────────────────────────────────────────────────────────────────

def run() -> int:
    dry = "--dry-run" in sys.argv
    config.ensure_dirs()
    config.require_printify_token()

    print("→ Fetching all Printify products…")
    products = printify_client.list_all_products()
    print(f"  {len(products)} products fetched")

    char_map, unmatched = build_map(products)

    print("\n=== Stats per collection ===")
    total_items = 0
    for col, payload in char_map.items():
        if payload.get("type_navigation"):
            n_types = len(payload.get("types") or {})
            n_items = 0
            for t in payload["types"].values():
                if t.get("flat"):
                    n_items += len(t.get("items") or [])
                else:
                    for ds in t.get("designs", {}).values():
                        for grp_key in ("dark", "light"):
                            bk = ds.get(grp_key)
                            if bk:
                                n_items += len(bk.get("items") or [])
            type_labels = ", ".join(payload["types"][c]["label"] for c in payload["type_order"])
            print(f"  {col:<14} types={n_types:>3}  items={n_items:>3}  [{type_labels}]  type_navigation=True")
        else:
            n_entries = len(payload["entries"])
            n_items = sum(
                len(e[g["key"]]["items"]) for e in payload["entries"].values() for g in payload["groups"]
            )
            groups = ", ".join(g["label"] for g in payload["groups"])
            print(f"  {col:<14} entries={n_entries:>3}  items={n_items:>3}  groups=[{groups}]  alphabet={payload['alphabet']}")
        total_items += n_items
    print(f"\nTotal items mapped: {total_items}  /  Printify total: {len(products)}")
    print(f"Unmatched: {len(unmatched)}")
    if unmatched:
        print("\n=== Unmatched products ===")
        for u in unmatched:
            print(f"  {u['id']}  {u['title']!r}  → {u['reason']}")

    # 3 entry samples per collection
    print("\n=== Entry samples (3 per collection) ===")
    for col, payload in char_map.items():
        print(f"\n--- {col} ---")
        if payload.get("type_navigation"):
            for cat in payload["type_order"]:
                t = payload["types"][cat]
                print(f"  [{cat}] {t['label']}  image={t['image_handle']}")
                if t.get("flat"):
                    print(f"      └─ FLAT  items={len(t.get('items') or [])}")
                    continue
                for ds_slug, ds in t.get("designs", {}).items():
                    n_dark = len((ds.get("dark") or {}).get("items") or [])
                    n_light = len((ds.get("light") or {}).get("items") or [])
                    print(f"      └─ {ds_slug:<12} {ds['name']:<14} dark={n_dark} light={n_light}")
            continue
        slugs = list(payload["entries"].keys())[:3]
        for slug in slugs:
            e = payload["entries"][slug]
            print(f"  [{slug}] {e['name']}")
            for grp in payload["groups"]:
                bucket = e[grp["key"]]
                items = bucket["items"]
                img = bucket["image_handle"] or "(none)"
                print(f"     {grp['label']:<14} image={img}")
                for it in items[:3]:
                    print(f"        — {it['title'][:55]:<58} {it['price']:>10}")

    if dry:
        print(f"\n(dry-run) would write {OUT_FILE.relative_to(config.REPO_ROOT)}")
        return 0

    OUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    char_map["_cache_bust"] = datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
    OUT_FILE.write_text(json.dumps(char_map, ensure_ascii=False, indent=2))
    size_kb = OUT_FILE.stat().st_size / 1024
    print(f"\n✓ Wrote {OUT_FILE.relative_to(config.REPO_ROOT)} ({size_kb:.1f} KB)  "
          f"[_cache_bust={char_map['_cache_bust']}]")
    return 0


if __name__ == "__main__":
    sys.exit(run())
