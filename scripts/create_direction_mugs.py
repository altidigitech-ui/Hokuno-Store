#!/usr/bin/env python3
"""Create all Direction mugs: FR + EN, light (white mug) + dark (black mug)."""

import os
import base64
import time
import requests

SHOP_ID = "22774508"
API_TOKEN = os.environ["PRINTIFY_API_TOKEN"]
HEADERS = {
    "Authorization": f"Bearer {API_TOKEN}",
    "Content-Type": "application/json",
    "User-Agent": "ClaudeCode-Hokuno/1.0",
}
BASE = "https://api.printify.com/v1"

BLUEPRINT_WHITE = 478   # Ceramic Mug (11oz, 15oz) — white
BLUEPRINT_BLACK = 479   # Black Mug (11oz, 15oz)
PROVIDER = 28           # District Photo

VARIANT_WHITE_11 = 65216
VARIANT_WHITE_15 = 104692
VARIANT_BLACK_11 = 65217
VARIANT_BLACK_15 = 104470

# Kanji logo image (same for all mugs)
KANJI_ID = "6846fd1c1a6d958e91819b36"
KANJI_X, KANJI_Y, KANJI_SCALE = 0.185251909825794, 0.4999999999999999, 0.2642680122984014

# Character position (same for all mugs — from Direction Luffy mug template)
CHAR_X, CHAR_Y, CHAR_SCALE = 0.811959061470855, 0.5, 0.30840077035223423

# name_key → (printify_title_name, file_name, position_number)
CHARACTERS = [
    ("LUFFY",  "Luffy",   "1/10"),
    ("ZORO",   "Zoro",    "2/10"),
    ("NAMI",   "Nami",    "3/10"),
    ("USSOP",  "Ussop",   "4/10"),
    ("SANJI",  "Sanji",   "5/10"),
    ("CHOPER", "Chopper", "6/10"),
    ("FRANKY", "Francky", "7/10"),
    ("ROBIN",  "Robin",   "8/10"),
    ("BROOK",  "Brook",   "9/10"),
    ("JINBE",  "Jimbe",   "10/10"),
]

DESCRIPTION_FR = (
    "<p>Profitez de votre boisson préférée dans cette tasse en céramique Hokuno. "
    "Design exclusif imprimé en haute qualité, BPA-free, compatible micro-ondes et lave-vaisselle.</p>"
)
DESCRIPTION_EN = (
    "<p>Enjoy your favourite drink in this Hokuno ceramic mug. "
    "Exclusive design in high-quality print, BPA-free, microwave and dishwasher safe.</p>"
)


def upload_image(path: str, filename: str) -> str:
    with open(path, "rb") as f:
        contents = base64.b64encode(f.read()).decode("utf-8")
    resp = requests.post(
        f"{BASE}/uploads/images.json",
        headers=HEADERS,
        json={"file_name": filename, "contents": contents},
    )
    resp.raise_for_status()
    return resp.json()["id"]


def create_mug(title: str, blueprint: int, variant_11: int, variant_15: int,
               char_image_id: str, description: str) -> str:
    payload = {
        "title": title,
        "description": description,
        "blueprint_id": blueprint,
        "print_provider_id": PROVIDER,
        "variants": [
            {"id": variant_11, "price": 1490, "is_enabled": True},
            {"id": variant_15, "price": 1890, "is_enabled": True},
        ],
        "print_areas": [{
            "variant_ids": [variant_11, variant_15],
            "placeholders": [{
                "position": "front",
                "images": [
                    {
                        "id": KANJI_ID,
                        "x": KANJI_X, "y": KANJI_Y,
                        "scale": KANJI_SCALE,
                        "angle": 0, "flipX": False, "flipY": False,
                    },
                    {
                        "id": char_image_id,
                        "x": CHAR_X, "y": CHAR_Y,
                        "scale": CHAR_SCALE,
                        "angle": 0, "flipX": False, "flipY": False,
                    },
                ]
            }]
        }],
    }
    resp = requests.post(
        f"{BASE}/shops/{SHOP_ID}/products.json",
        headers=HEADERS,
        json=payload,
    )
    if not resp.ok:
        print(f"\n  ERROR {resp.status_code}: {resp.text[:300]}")
    resp.raise_for_status()
    return resp.json()["id"]


def main():
    repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    results = []

    # Cache des uploads pour éviter les doublons
    uploaded = {}

    batches = [
        # (lang, variant_type, blueprint, v11, v15, folder_suffix, img_folder, title_fn, desc)
        ("FR", "light", BLUEPRINT_WHITE, VARIANT_WHITE_11, VARIANT_WHITE_15,
         "direction-fr-light",
         lambda nom, num: f"tasse en céramique direction {nom.lower()} (11oz, 15oz) {num}",
         DESCRIPTION_FR),
        ("FR", "dark", BLUEPRINT_BLACK, VARIANT_BLACK_11, VARIANT_BLACK_15,
         "direction-fr-dark",
         lambda nom, num: f"tasse en céramique direction {nom.lower()} noire (11oz, 15oz) {num}",
         DESCRIPTION_FR),
        ("EN", "light", BLUEPRINT_WHITE, VARIANT_WHITE_11, VARIANT_WHITE_15,
         "direction-en-light",
         lambda nom, num: f"ceramic mug direction {nom.lower()} (11oz, 15oz) {num}",
         DESCRIPTION_EN),
        ("EN", "dark", BLUEPRINT_BLACK, VARIANT_BLACK_11, VARIANT_BLACK_15,
         "direction-en-dark",
         lambda nom, num: f"ceramic mug direction {nom.lower()} black (11oz, 15oz) {num}",
         DESCRIPTION_EN),
    ]

    for lang, variant, blueprint, v11, v15, img_folder, title_fn, desc in batches:
        print(f"\n{'='*60}")
        print(f"  {lang} — {variant.upper()} ({img_folder})")
        print(f"{'='*60}")

        for print_name, file_name, number in CHARACTERS:
            img_path = os.path.join(repo_root, "exports", img_folder, f"{file_name}.png")
            upload_key = f"{img_folder}/{file_name}"
            title = title_fn(print_name, number)

            print(f"\n  [{print_name}] {title}")

            if not os.path.exists(img_path):
                print(f"  ⚠ Image introuvable : {img_path}")
                continue

            if upload_key not in uploaded:
                print(f"  Upload {file_name}.png...", end=" ", flush=True)
                fname = f"{file_name.lower()}-{img_folder}.png"
                uploaded[upload_key] = upload_image(img_path, fname)
                print(f"ID={uploaded[upload_key]}")
                time.sleep(0.2)
            else:
                print(f"  Image déjà uploadée : {uploaded[upload_key]}")

            print(f"  POST mug...", end=" ", flush=True)
            new_id = create_mug(title, blueprint, v11, v15, uploaded[upload_key], desc)
            print(f"OK → {new_id}")
            results.append({"id": new_id, "title": title, "lang": lang, "variant": variant})
            time.sleep(0.3)

    print(f"\n{'='*60}")
    print(f"RÉCAPITULATIF — {len(results)}/40 mugs créés")
    print(f"{'='*60}")
    for r in results:
        print(f"  [{r['lang']} {r['variant']}] {r['id']}  {r['title']}")


if __name__ == "__main__":
    main()
