#!/usr/bin/env python3
"""Update back print area of all Direction FR t-shirts with new images."""

import os
import base64
import json
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

# Mapping: Printify title keyword → image filename
CHAR_MAP = {
    "LUFFY": "Luffy",
    "ZORO": "Zoro",
    "NAMI": "Nami",
    "USSOP": "Ussop",
    "SANJI": "Sanji",
    "CHOPER": "Chopper",
    "FRANKY": "Francky",
    "ROBIN": "Robin",
    "BROOK": "Brook",
    "JINBE": "Jimbe",
}

# Direction FR products (light then dark)
PRODUCTS = {
    # Light (fond blanc → image noire)
    "684c63107a567575d002f21b": ("LUFFY", "light"),
    "684c63e57a567575d002f24c": ("ZORO", "light"),
    "684c64317a567575d002f25a": ("NAMI", "light"),
    "684c648061f0867d160dcdbb": ("USSOP", "light"),
    "684c64cdf8df6e09820d1487": ("SANJI", "light"),
    "684c65141d7c908d840c5e16": ("CHOPER", "light"),
    "684c656856fb86136206591f": ("FRANKY", "light"),
    "684c65b97a567575d002f2d6": ("ROBIN", "light"),
    "684c65fbdb8b74bc2d0b88bd": ("BROOK", "light"),
    "684c664a7a567575d002f304": ("JINBE", "light"),
    # Dark (fond noir → image blanche)
    "684c68d987f5fc4a8101133d": ("LUFFY", "dark"),
    "684c693fb2d4e68c870de492": ("ZORO", "dark"),
    "684c699f902f42fe2e080880": ("NAMI", "dark"),
    "684c6a3fb41682e82d0b4390": ("USSOP", "dark"),
    "684c69f1586f185e4005b09f": ("SANJI", "dark"),
    "684c6a84b41682e82d0b43ac": ("CHOPER", "dark"),
    "684c6ac6f3b91cf7810bf3c6": ("FRANKY", "dark"),
    "684c6b157a567575d002f416": ("ROBIN", "dark"),
    "684c6b5587f5fc4a810113bf": ("BROOK", "dark"),
    "684c6b98f3b91cf7810bf40a": ("JINBE", "dark"),
}


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


def get_product(product_id: str) -> dict:
    resp = requests.get(
        f"{BASE}/shops/{SHOP_ID}/products/{product_id}.json",
        headers=HEADERS,
    )
    resp.raise_for_status()
    return resp.json()


def update_product_back(product_id: str, new_image_id: str, product: dict) -> None:
    print_areas = product["print_areas"]

    # Trouver la back placeholder et sa position actuelle
    back_x, back_y, back_scale, back_angle = 0.5, 0.5, 1.0, 0
    all_variant_ids = []
    for area in print_areas:
        all_variant_ids = area["variant_ids"]
        for ph in area["placeholders"]:
            if ph["position"] == "back" and ph.get("images"):
                old = ph["images"][0]
                back_x = old["x"]
                back_y = old["y"]
                back_scale = old["scale"]
                back_angle = old["angle"]

    # N'envoyer que le placeholder back avec la nouvelle image
    payload = {
        "print_areas": [{
            "variant_ids": all_variant_ids,
            "placeholders": [{
                "position": "back",
                "images": [{
                    "id": new_image_id,
                    "x": back_x,
                    "y": back_y,
                    "scale": back_scale,
                    "angle": back_angle,
                    "flipX": False,
                    "flipY": False,
                }]
            }]
        }]
    }

    resp = requests.put(
        f"{BASE}/shops/{SHOP_ID}/products/{product_id}.json",
        headers=HEADERS,
        json=payload,
    )
    if not resp.ok:
        print(f"\n  ERROR {resp.status_code}: {resp.text[:500]}")
    resp.raise_for_status()


def main():
    repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    for product_id, (char_key, variant) in PRODUCTS.items():
        char_name = CHAR_MAP[char_key]
        folder = f"direction-fr-{variant}"
        img_path = os.path.join(repo_root, "exports", folder, f"{char_name}.png")
        filename = f"{char_name.lower()}-direction-{variant}.png"

        print(f"\n[{variant.upper()}] {char_key} ({char_name})")

        if not os.path.exists(img_path):
            print(f"  ⚠ Image introuvable : {img_path}")
            continue

        print(f"  Upload {filename}...", end=" ", flush=True)
        image_id = upload_image(img_path, filename)
        print(f"ID={image_id}")
        time.sleep(0.2)

        print(f"  GET produit...", end=" ", flush=True)
        product = get_product(product_id)
        print(f"OK ({product['title']})")
        time.sleep(0.2)

        print(f"  PUT back placeholder...", end=" ", flush=True)
        update_product_back(product_id, image_id, product)
        print("OK")
        time.sleep(0.2)

    print("\n=== Terminé ===")


if __name__ == "__main__":
    main()
