#!/usr/bin/env python3
"""Create 9 missing Mythologie ceramic mugs (white, blueprint 478).

Image IDs are extracted from the back print area of existing Mythologie light t-shirts.
Luffy (#1) already exists — only 2/10 → 10/10 are created here.
"""

import os
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

BLUEPRINT = 478     # Ceramic Mug (11oz, 15oz) — white
PROVIDER = 28       # District Photo

VARIANT_11OZ = 65216
VARIANT_15OZ = 104692

# Kanji logo — identical to all other Hokuno mugs
KANJI_ID = "6846fd1c1a6d958e91819b36"
KANJI_X, KANJI_Y, KANJI_SCALE = 0.18947903032055102, 0.4999999999999999, 0.2642680122984014

# Character image position (mirrored with kanji, same layout as Luffy mug)
CHAR_X, CHAR_Y, CHAR_SCALE = 0.8108657430498314, 0.5000000000000001, 0.2642680122984017

# Image IDs extracted from the back print area of existing Mythologie light t-shirts
# Luffy (1/10) omitted — mug already exists: 684d59ac1d7c908d840c9497
CHARACTERS = [
    ("ZORO",   "2/10",  "6849a360c59a53b3165fb418"),
    ("NAMI",   "3/10",  "6849a4b100bea310eabbdcf8"),
    ("USSOP",  "4/10",  "6849a8c1a1d95426c8efdc9f"),
    ("SANJI",  "5/10",  "6849c84c91e098bfd91ecb4e"),
    ("CHOPER", "6/10",  "69f75c06560bc95fadde4b51"),
    ("FRANKY", "7/10",  "6849a6b8e6ef754c7bb37fba"),
    ("ROBIN",  "8/10",  "69f75c0842248aefa9f20210"),
    ("BROOK",  "9/10",  "6849a7e0dd22070cbb60d3f0"),
    ("JINBE",  "10/10", "6849a523b90ea25c3065f05f"),
]

DESCRIPTION = (
    "<p>Profitez de votre boisson préférée dans cette tasse en céramique Hokuno. "
    "Design exclusif imprimé en haute qualité, BPA-free, compatible micro-ondes et lave-vaisselle.</p>"
)


def create_mug(name: str, num: str, char_image_id: str) -> str:
    title = f"MYTHOLOGIE {name} Ceramic Mug, (11oz, 15oz) {num}"
    payload = {
        "title": title,
        "description": DESCRIPTION,
        "blueprint_id": BLUEPRINT,
        "print_provider_id": PROVIDER,
        "variants": [
            {"id": VARIANT_11OZ, "price": 1490, "is_enabled": True},
            {"id": VARIANT_15OZ, "price": 1890, "is_enabled": True},
        ],
        "print_areas": [{
            "variant_ids": [VARIANT_11OZ, VARIANT_15OZ],
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
                ],
            }],
        }],
    }
    resp = requests.post(
        f"{BASE}/shops/{SHOP_ID}/products.json",
        headers=HEADERS,
        json=payload,
    )
    if not resp.ok:
        print(f"\n  ERROR {resp.status_code}: {resp.text[:400]}")
    resp.raise_for_status()
    return resp.json()["id"]


def main():
    results = []
    print(f"Creating {len(CHARACTERS)} Mythologie mugs...\n")

    for name, num, char_image_id in CHARACTERS:
        title = f"MYTHOLOGIE {name} Ceramic Mug, (11oz, 15oz) {num}"
        print(f"  [{num}] {name}...", end=" ", flush=True)
        new_id = create_mug(name, num, char_image_id)
        print(f"OK → {new_id}")
        results.append((name, num, new_id))
        time.sleep(0.3)

    print(f"\n{'='*60}")
    print(f"DONE — {len(results)}/9 mugs créés")
    print(f"{'='*60}")
    print("\nAjouter dans INVENTAIRE.md + mythologie.json :")
    for name, num, pid in results:
        print(f'  | #{num.split("/")[0]:>2} | MYTHOLOGIE {name} Ceramic Mug, (11oz, 15oz) {num} | `{pid}` | 2 |')


if __name__ == "__main__":
    main()
