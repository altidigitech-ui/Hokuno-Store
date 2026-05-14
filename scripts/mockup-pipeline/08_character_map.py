"""Build shopify-theme/assets/character-map.json from Printify titles.

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


# Slugs where the FR tee files on Printify have the wrong character design
# uploaded (data quality issue at the source). As a thumbnail workaround we
# point the FR card's image to the corresponding EN tee handle (which has the
# correct artwork). The products inside the FR group are left untouched —
# they remain accessible but the product page on Shopify will still show the
# bad artwork until the design is re-uploaded on Printify.
FR_CARD_IMAGE_USE_EN: dict[str, set[str]] = {
    "WANTED": {
        "bartolomiou-kouma", "boha-ancock", "crocockdile", "dracule-miok",
        "eustash-cap-kid", "gayko-mauria", "harllong", "iamato", "iwankoff",
        "kobi", "momonosucke", "monki-di-dragone", "portgas-di-ase",
        "sabot", "trafalgar-di-low",
    }
}


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
    "DESIGN HOKUNO": {
        "alphabet": False,
        "groups": [
            {"key": "dark",  "label": "Dark"},
            {"key": "light", "label": "Light"},
        ],
    },
}


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
        broken_fr = FR_CARD_IMAGE_USE_EN.get(col, set())
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
            # FR thumbnail workaround for Printify design-mismatch products:
            # use the EN light tee's correct artwork as the FR card image.
            if slug in broken_fr and payload.get("fr") and payload.get("en"):
                en_items = payload["en"]["items"]
                substitute = None
                for it in en_items:
                    if it["ptype"] == "tshirt" and not it["dark"]:
                        substitute = it["handle"]; break
                if not substitute:
                    for it in en_items:
                        if it["ptype"] == "tshirt":
                            substitute = it["handle"]; break
                if substitute:
                    payload["fr"]["image_handle"] = substitute
                    payload["fr"]["image_substituted"] = True
            entries_out[slug] = payload

        out[col] = {
            "alphabet": layout["alphabet"],
            "groups": layout["groups"],
            "entries": entries_out,
        }

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
        n_entries = len(payload["entries"])
        n_items = sum(
            len(e[g["key"]]["items"]) for e in payload["entries"].values() for g in payload["groups"]
        )
        total_items += n_items
        groups = ", ".join(g["label"] for g in payload["groups"])
        print(f"  {col:<14} entries={n_entries:>3}  items={n_items:>3}  groups=[{groups}]  alphabet={payload['alphabet']}")
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
    OUT_FILE.write_text(json.dumps(char_map, ensure_ascii=False, indent=2))
    size_kb = OUT_FILE.stat().st_size / 1024
    print(f"\n✓ Wrote {OUT_FILE.relative_to(config.REPO_ROOT)} ({size_kb:.1f} KB)")
    return 0


if __name__ == "__main__":
    sys.exit(run())
