"""Duplicate the Black Mug template across 46 Wanted + 10 Mythologie characters.

Template: 6a062df26c82d6fc6e065dda  "Black Mug Wanted Luffy EN (11oz, 15oz)"
          BP 479 (Black ceramic mug) — PP 99 (Printify Choice)

For each target character we:
  1. POST /v1/shops/{shop_id}/products.json with a payload that:
     - Reuses the kanji-otaku.PNG image from the template (left side)
     - Plugs in the character's own design image (right side), keeping the
       scale/x/y values from the character's existing white mug source so the
       layout matches what the customer already knows.
     - Enables 11oz @ 29.99€ (price=2999) and 15oz @ 34.99€ (price=3499)
     - Reuses the character's existing mug description (brand voice + lore)
  2. Sleep 0.4s (Printify rate limit)

Scope:
    Wanted     : 46 characters
    Mythologie : 10 characters
    Direction  : SKIP (already has PP 28 black mugs)
    Total      : 56 new Printify products

Run:
    python scripts/mockup-pipeline/10_duplicate_black_mugs.py --dry-run     # show first 3 payloads, no API call
    python scripts/mockup-pipeline/10_duplicate_black_mugs.py --first 3     # actually create first 3 only (for live sanity check)
    python scripts/mockup-pipeline/10_duplicate_black_mugs.py               # create all 56
    python scripts/mockup-pipeline/10_duplicate_black_mugs.py --resume      # skip targets that already have a created product log
"""
from __future__ import annotations

import datetime
import json
import sys
import time
from pathlib import Path

import requests
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

sys.path.insert(0, str(Path(__file__).resolve().parent))

import config  # noqa: E402
import printify_client  # noqa: E402

# ─── Constants ──────────────────────────────────────────────────────────────

TEMPLATE_ID = "6a062df26c82d6fc6e065dda"

# BP 479 (Black Mug) variants from the template
VARIANT_11OZ = 65217
VARIANT_15OZ = 104470
PRICE_11OZ = 2999  # 29.99 €
PRICE_15OZ = 3499  # 34.99 €

# Kanji image (left side) — keep as-is from template
KANJI_IMG = {
    "id":    "6855cdf5497f81596940eff2",
    "name":  "kanji otaku .PNG",
    "type":  "image/png",
    "x":     0.15556006699487362,
    "y":     0.4999893357659589,
    "scale": 0.31112013398974775,
    "angle": 0,
}

COLLECTION_LABEL = {"WANTED": "Wanted", "MYTHOLOGIE": "Mythologie"}

LOG_DIR = config.LOG_DIR
CREATED_LOG = LOG_DIR / "fix10-created.json"  # {slug: {product_id, title}}


# ─── Printify Admin API helpers ─────────────────────────────────────────────

class PrintifyAdminError(RuntimeError):
    pass


def _headers():
    return {
        "Authorization": f"Bearer {config.PRINTIFY_TOKEN}",
        "User-Agent":    "Hokuno-Black-Mug-Duplicator/1.0",
        "Content-Type":  "application/json",
        "Accept":        "application/json",
    }


@retry(
    reraise=True,
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=2, min=2, max=10),
    retry=retry_if_exception_type((requests.RequestException, PrintifyAdminError)),
)
def _post(path: str, body: dict):
    url = f"{config.PRINTIFY_BASE_URL}{path}"
    r = requests.post(url, headers=_headers(), json=body, timeout=60)
    if r.status_code == 429:
        raise PrintifyAdminError(f"Throttled: {r.text[:300]}")
    if r.status_code >= 500:
        raise PrintifyAdminError(f"Server {r.status_code}: {r.text[:300]}")
    if r.status_code >= 400:
        # 4xx — non-retryable, raise immediately
        raise RuntimeError(f"HTTP {r.status_code}: {r.text[:500]}")
    return r.json() if r.text else {}


def create_product(payload: dict) -> dict:
    return _post(f"/shops/{config.PRINTIFY_SHOP_ID}/products.json", payload)


def publish_product(product_id: str) -> dict:
    body = {
        "title": True, "description": True, "images": True,
        "variants": True, "tags": True, "key_features": True,
        "shipping_template": False,
    }
    return _post(
        f"/shops/{config.PRINTIFY_SHOP_ID}/products/{product_id}/publish.json",
        body,
    )


# ─── Payload builder ────────────────────────────────────────────────────────

def build_payload(target: dict, source_desc: str) -> dict:
    """Compose the POST body for one new product."""
    col_label = COLLECTION_LABEL[target["collection"]]
    new_title = f"Black Mug {col_label} {target['name']} (11oz, 15oz)"

    design_img = {
        "id":    target["design_img_id"],
        "name":  target["design_img_name"],
        "type":  "image/png",
        "x":     target["design_x"],
        "y":     target["design_y"],
        "scale": target["design_scale"],
        "angle": 0,
    }

    return {
        "title":              new_title,
        "description":        source_desc or "",
        "blueprint_id":       479,
        "print_provider_id":  99,
        "variants": [
            {"id": VARIANT_11OZ, "price": PRICE_11OZ, "is_enabled": True},
            {"id": VARIANT_15OZ, "price": PRICE_15OZ, "is_enabled": True},
        ],
        "print_areas": [
            {
                "variant_ids": [VARIANT_11OZ, VARIANT_15OZ],
                "placeholders": [
                    {
                        "position": "front",
                        "images":   [KANJI_IMG, design_img],
                    }
                ],
            }
        ],
        "tags": ["Mugs", "Black base", "Ceramic", col_label, target["name"]],
    }


# ─── Targets ────────────────────────────────────────────────────────────────

def load_targets() -> list[dict]:
    """Read the design map saved by the previous discovery step."""
    raw = json.load(open("/tmp/char_design_map.json"))
    targets = []
    for key, data in raw.items():
        col, slug = key.split("/", 1)
        if col not in ("WANTED", "MYTHOLOGIE"):
            continue
        if not data.get("design_img_id"):
            continue
        targets.append({
            "collection": col,
            "slug":       slug,
            "name":       data["name"],
            "design_img_id":   data["design_img_id"],
            "design_img_name": data["design_img_name"],
            "design_x":        data["design_x"],
            "design_y":        data["design_y"],
            "design_scale":    data["design_scale"],
            "src_product_id":  data["src_product_id"],
            "src_handle":      data["src_handle"],
        })
    # Stable order: collection then slug
    targets.sort(key=lambda t: (t["collection"], t["slug"]))
    return targets


def load_source_descriptions(targets: list[dict], all_products: list[dict]) -> dict[str, str]:
    by_id = {p["id"]: p for p in all_products}
    out: dict[str, str] = {}
    for t in targets:
        sp = by_id.get(t["src_product_id"])
        out[t["slug"]] = (sp.get("description") or "") if sp else ""
    return out


# ─── Main ───────────────────────────────────────────────────────────────────

def run() -> int:
    dry_run     = "--dry-run" in sys.argv
    resume      = "--resume"  in sys.argv
    first_n: int | None = None
    for i, a in enumerate(sys.argv):
        if a == "--first" and i + 1 < len(sys.argv):
            first_n = int(sys.argv[i + 1])

    config.ensure_dirs()
    config.require_printify_token()

    targets = load_targets()
    print(f"→ {len(targets)} targets loaded (Wanted+Mythologie, Direction skipped)")

    # Resume support
    created = {}
    if resume and CREATED_LOG.exists():
        created = json.loads(CREATED_LOG.read_text())
        print(f"  resume: skipping {len(created)} already-created targets")
        targets = [t for t in targets if t["slug"] not in created]

    if first_n is not None:
        targets = targets[:first_n]
        print(f"  --first {first_n} → limited to {len(targets)} targets")

    # Pull source descriptions
    print("→ Fetching Printify catalog to read source mug descriptions…")
    all_products = printify_client.list_all_products()
    descs = load_source_descriptions(targets, all_products)

    if dry_run:
        # Print 3 sample payloads (first per collection if possible)
        seen_cols = set()
        shown = 0
        for t in targets:
            if shown >= 3 or (t["collection"] in seen_cols and shown >= 2):
                continue
            seen_cols.add(t["collection"])
            shown += 1
            payload = build_payload(t, descs.get(t["slug"], ""))
            # Hide description body in dry-run print (it's long)
            preview = dict(payload)
            preview["description"] = preview["description"][:120] + ("…" if len(preview["description"]) > 120 else "")
            print(f"\n--- DRY-RUN payload [{t['collection']}/{t['slug']}] ---")
            print(json.dumps(preview, indent=2, ensure_ascii=False))
        return 0

    # Live creation
    started = datetime.datetime.now()
    successes = 0
    errors: list[dict] = []
    for i, t in enumerate(targets, 1):
        payload = build_payload(t, descs.get(t["slug"], ""))
        try:
            new_product = create_product(payload)
            new_pid = new_product.get("id") or new_product.get("product", {}).get("id")
            if not new_pid:
                raise RuntimeError(f"Create OK but no id in response: {new_product}")

            time.sleep(0.4)
            publish_resp = publish_product(new_pid)

            created[t["slug"]] = {
                "product_id": new_pid,
                "title":      payload["title"],
                "collection": t["collection"],
            }
            CREATED_LOG.write_text(json.dumps(created, indent=2, ensure_ascii=False))
            successes += 1
            print(f"  [{i:>3}/{len(targets)}] {t['collection']:<12} {t['name']:<22} → OK  product_id={new_pid}")
        except Exception as e:  # noqa: BLE001
            errors.append({"slug": t["slug"], "error": str(e)[:300]})
            print(f"  [{i:>3}/{len(targets)}] {t['collection']:<12} {t['name']:<22} → ERROR: {str(e)[:160]}")

        time.sleep(0.4)  # printify rate limit

    elapsed = (datetime.datetime.now() - started).total_seconds()
    print("\n" + "=" * 70)
    print(f"BLACK MUG DUPLICATION DONE — {successes}/{len(targets)} OK, {len(errors)} errors  ({int(elapsed//60)}m{int(elapsed%60)}s)")
    print("=" * 70)
    if errors:
        print("\nErrors:")
        for e in errors[:10]:
            print(f"  {e['slug']}  →  {e['error']}")
    print(f"\nCreated log : {CREATED_LOG.relative_to(config.REPO_ROOT)}")
    print(f"Next step   : regenerate mockups for the new products (rembg + bg-replace), then update character-map.json")
    return 0 if not errors else 2


if __name__ == "__main__":
    sys.exit(run())
