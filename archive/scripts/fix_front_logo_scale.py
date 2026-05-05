#!/usr/bin/env python3
"""Fix front logo scale on all 40 Direction products (33.03 → 59.53 in Printify UI)."""

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

LOGO_IMAGE_ID = "69f79f1270e1b9ced794f3ab"
LOGO_X     = 0.8473487724188791
LOGO_Y     = 0.1171944277699074
LOGO_SCALE = 0.14075527835881743  # 59.53 en UI (était 33.03 = 0.07810)

ALL_PRODUCTS = [
    "684c63107a567575d002f21b", "684c63e57a567575d002f24c", "684c64317a567575d002f25a",
    "684c648061f0867d160dcdbb", "684c64cdf8df6e09820d1487", "684c65141d7c908d840c5e16",
    "684c656856fb86136206591f", "684c65b97a567575d002f2d6", "684c65fbdb8b74bc2d0b88bd",
    "684c664a7a567575d002f304",
    "684c68d987f5fc4a8101133d", "684c693fb2d4e68c870de492", "684c699f902f42fe2e080880",
    "684c6a3fb41682e82d0b4390", "684c69f1586f185e4005b09f", "684c6a84b41682e82d0b43ac",
    "684c6ac6f3b91cf7810bf3c6", "684c6b157a567575d002f416", "684c6b5587f5fc4a810113bf",
    "684c6b98f3b91cf7810bf40a",
    "69f79ad4a5ddadd686033eb1", "69f79ae2bb69c26a6c044f39", "69f79aefa1a4c45aad04f22e",
    "69f79afa2592a8ad8e0e7625", "69f79b0fa5ddadd686033edf", "69f79b1925819cdf3d04cfda",
    "69f79b22a5ddadd686033ee6", "69f79b2a4c4cd0e2bd0ade85", "69f79b3483a8608fd80e7e92",
    "69f79b3e782c77f6f105bfb1",
    "69f79b4a38c22e9be806ef68", "69f79b5809f3b73024016bab", "69f79b62e8580fe5eb0596b2",
    "69f79b6ef9374ed4f1053744", "69f79b7aa1a4c45aad04f2bb", "69f79b85782c77f6f105bffe",
    "69f79b8f5da263f75f04578c", "69f79ba0f9374ed4f1053781", "69f79bac38c22e9be806efde",
    "69f79bb95da263f75f0457b1",
]


def get_product(product_id: str) -> dict:
    resp = requests.get(f"{BASE}/shops/{SHOP_ID}/products/{product_id}.json", headers=HEADERS)
    resp.raise_for_status()
    return resp.json()


def update_logo_scale(product_id: str, product: dict) -> None:
    areas = product["print_areas"]
    all_variant_ids = areas[0]["variant_ids"]

    back_image = None
    for area in areas:
        for ph in area["placeholders"]:
            if ph["position"] == "back" and ph.get("images"):
                old = ph["images"][0]
                back_image = {
                    "id": old["id"],
                    "x": old["x"], "y": old["y"],
                    "scale": old["scale"], "angle": old.get("angle", 0),
                    "flipX": old.get("flipX", False), "flipY": old.get("flipY", False),
                }

    placeholders = []
    if back_image:
        placeholders.append({"position": "back", "images": [back_image]})
    placeholders.append({
        "position": "front",
        "images": [{
            "id": LOGO_IMAGE_ID,
            "x": LOGO_X, "y": LOGO_Y,
            "scale": LOGO_SCALE,
            "angle": 0, "flipX": False, "flipY": False,
        }]
    })

    resp = requests.put(
        f"{BASE}/shops/{SHOP_ID}/products/{product_id}.json",
        headers=HEADERS,
        json={"print_areas": [{"variant_ids": all_variant_ids, "placeholders": placeholders}]},
    )
    if not resp.ok:
        print(f"\n  ERROR {resp.status_code}: {resp.text[:300]}")
    resp.raise_for_status()


def main():
    total = len(ALL_PRODUCTS)
    for i, pid in enumerate(ALL_PRODUCTS, 1):
        print(f"[{i:02d}/{total}] {pid} ...", end=" ", flush=True)
        product = get_product(pid)
        time.sleep(0.2)
        update_logo_scale(pid, product)
        print(f"OK ({product['title']})")
        time.sleep(0.2)
    print(f"\n=== Terminé : {total}/{total} produits mis à jour ===")


if __name__ == "__main__":
    main()
