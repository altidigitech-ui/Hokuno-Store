#!/usr/bin/env python3
"""
Create FR and EN mugs for all 46 Wanted characters.
- FR mugs: wanted-018 to wanted-046 (17 already exist for wanted-001..017)
- EN mugs: all 46 characters
Updates wanted.json with mug_fr / mug_en product IDs.
"""
import json
import os
import time
import sys
import requests

SHOP_ID = "22774508"
TOKEN = os.environ.get("PRINTIFY_API_TOKEN")
if not TOKEN:
    sys.exit("PRINTIFY_API_TOKEN not set")

HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json",
}
BASE_URL = f"https://api.printify.com/v1/shops/{SHOP_ID}"

# Image IDs that appear on every t-shirt (logo, brand elements, text)
STATIC_IDS = {
    "68499a521d2b297c907ad2fb",  # 73.png
    "6846b70b74049e8a7d617ad8",  # NOM DE LOGO.jpeg
    "6847009f2a23deed8baf0c9c",  # 70.png
    "5941187eb8e7e37b3f0e62e5",  # text_layer.svg
    "6846fd1c1a6d958e91819b36",  # hokuno kanji .PNG (mug logo)
}

LOGO_ID = "6846fd1c1a6d958e91819b36"
BLUEPRINT_ID = 478
PROVIDER_ID = 28

VARIANTS = [
    {"id": 65216, "price": 768, "is_enabled": True},
    {"id": 104692, "price": 1085, "is_enabled": False},
]

LOGO_IMG = {
    "id": LOGO_ID,
    "x": 0.18947903032055102,
    "y": 0.4999999999999999,
    "scale": 0.2642680122984014,
    "angle": 0,
    "flipX": False,
    "flipY": False,
}

POSTER_POS = {
    "x": 0.8108400927911055,
    "y": 0.4999999999999999,
    "scale": 0.283192,
    "angle": 0,
    "flipX": False,
    "flipY": False,
}


def get_main_poster_id(product_id):
    url = f"{BASE_URL}/products/{product_id}.json"
    resp = requests.get(url, headers=HEADERS)
    resp.raise_for_status()
    product = resp.json()
    for pa in product.get("print_areas", []):
        for ph in pa.get("placeholders", []):
            for img in ph.get("images", []):
                if img["id"] not in STATIC_IDS:
                    return img["id"], img.get("name", "")
    return None, None


def create_mug(title, poster_id):
    poster_img = {**POSTER_POS, "id": poster_id}
    payload = {
        "title": title,
        "blueprint_id": BLUEPRINT_ID,
        "print_provider_id": PROVIDER_ID,
        "variants": VARIANTS,
        "print_areas": [
            {
                "variant_ids": [65216, 104692],
                "placeholders": [
                    {
                        "position": "front",
                        "images": [LOGO_IMG, poster_img],
                    }
                ],
                "background": "#ffffff",
            }
        ],
    }
    resp = requests.post(f"{BASE_URL}/products.json", headers=HEADERS, json=payload)
    resp.raise_for_status()
    return resp.json().get("id")


def main():
    json_path = "/workspaces/Hokuno-Store/collections/wanted.json"
    with open(json_path) as f:
        data = json.load(f)

    chars = data["personnages"]
    total = len(chars)
    created = 0
    errors = []

    for i, char in enumerate(chars):
        nom = char["nom"]
        char_id = char["id"]
        ids = char["printify_product_ids"]

        # Migrate existing mug → mug_fr
        if "mug_fr" not in ids:
            ids["mug_fr"] = ids.get("mug", "")
        if "mug_en" not in ids:
            ids["mug_en"] = ""

        print(f"\n[{i+1}/{total}] {nom} ({char_id})")

        # --- FR mug ---
        if not ids["mug_fr"]:
            fr_tshirt = ids.get("tshirt_fr_light", "")
            if not fr_tshirt:
                print(f"  FR: SKIP — no tshirt_fr_light")
            else:
                poster_id, poster_name = get_main_poster_id(fr_tshirt)
                time.sleep(0.3)
                if not poster_id:
                    print(f"  FR: ERROR — no main poster found in {fr_tshirt}")
                    errors.append(f"{char_id} FR: no poster in {fr_tshirt}")
                else:
                    title = f"tasse en céramique wanted {nom.lower()} (11oz, 15oz)"
                    try:
                        mug_id = create_mug(title, poster_id)
                        ids["mug_fr"] = mug_id
                        created += 1
                        print(f"  FR: created {mug_id}  (poster: {poster_name})")
                    except Exception as e:
                        print(f"  FR: ERROR — {e}")
                        errors.append(f"{char_id} FR: {e}")
                    time.sleep(0.4)
        else:
            print(f"  FR: already exists → {ids['mug_fr']}")

        # --- EN mug ---
        if not ids["mug_en"]:
            en_tshirt = ids.get("tshirt_en_light", "")
            if not en_tshirt:
                print(f"  EN: SKIP — no tshirt_en_light")
            else:
                poster_id, poster_name = get_main_poster_id(en_tshirt)
                time.sleep(0.3)
                if not poster_id:
                    print(f"  EN: ERROR — no main poster found in {en_tshirt}")
                    errors.append(f"{char_id} EN: no poster in {en_tshirt}")
                else:
                    title = f"ceramic mug wanted {nom.lower()} (11oz, 15oz)"
                    try:
                        mug_id = create_mug(title, poster_id)
                        ids["mug_en"] = mug_id
                        created += 1
                        print(f"  EN: created {mug_id}  (poster: {poster_name})")
                    except Exception as e:
                        print(f"  EN: ERROR — {e}")
                        errors.append(f"{char_id} EN: {e}")
                    time.sleep(0.4)
        else:
            print(f"  EN: already exists → {ids['mug_en']}")

        # Save after each character (in case of interruption)
        with open(json_path, "w") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"\n{'='*50}")
    print(f"Done — {created} mugs created")
    if errors:
        print(f"{len(errors)} errors:")
        for e in errors:
            print(f"  {e}")


if __name__ == "__main__":
    main()
