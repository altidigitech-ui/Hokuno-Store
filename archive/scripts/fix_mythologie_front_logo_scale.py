#!/usr/bin/env python3
"""Fix front logo scale on all 21 Mythologie t-shirts (19.29 → 53.59 in Printify UI)."""

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

SCALE_RATIO = 53.59 / 19.29  # 2.778123...

# All 21 Mythologie t-shirts (10 light + 10 dark standard + 1 dark v2)
PRODUCTS = [
    # Light
    ("6846b317f4071352350c150a", "Luffy light"),
    ("6849a0426ab7f1ef5d069673", "Zoro light"),
    ("6849a4237483e9399e0d4444", "Nami light"),
    ("6849a898e27810926a088854", "Ussop light"),
    ("6849a6e0bd30bb1f1304c67e", "Sanji light"),
    ("69f75c68a0d5e53b4103a9f3", "Choper light"),
    ("6849a62c7483e9399e0d44b5", "Franky light"),
    ("69f75c6f83a8608fd80e5707", "Robin light"),
    ("6849a7abf43bb403450bd907", "Brook light"),
    ("6849a4e7d5b83610460568ba", "Jinbe light"),
    # Dark standard
    ("6849b61fd0482255940866ea", "Luffy noir"),
    ("6849c1ce6ab7f1ef5d069e35", "Zoro noir"),
    ("6849c07b943f652c190bd88d", "Nami noir"),
    ("6849c298b5bde8e15300e417", "Ussop noir"),
    ("6849be2de27810926a088d94", "Sanji noir"),
    ("6849a7517483e9399e0d44ef", "Choper noir"),
    ("6849bfd6943f652c190bd86d", "Franky noir"),
    ("6849a8397483e9399e0d455d", "Robin noir"),
    ("69f87c8cbe136844f0003b0a", "Brook noir"),
    ("6849c0fc9bf7aebaf704867b", "Jinbe noir"),
    # Dark v2
    ("6849c4469bf7aebaf7048740", "Brook noir v2"),
]


def get_product(product_id: str) -> dict:
    resp = requests.get(f"{BASE}/shops/{SHOP_ID}/products/{product_id}.json", headers=HEADERS)
    resp.raise_for_status()
    return resp.json()


def fix_front_scale(product_id: str, product: dict) -> None:
    areas = product["print_areas"]
    all_variant_ids = areas[0]["variant_ids"]

    back_image = None
    front_img = None

    for area in areas:
        for ph in area["placeholders"]:
            pos = ph["position"]
            imgs = ph.get("images", [])
            if pos == "back" and imgs:
                old = imgs[0]
                back_image = {
                    "id": old["id"],
                    "x": old["x"], "y": old["y"],
                    "scale": old["scale"],
                    "angle": old.get("angle", 0),
                    "flipX": old.get("flipX", False),
                    "flipY": old.get("flipY", False),
                }
            elif pos == "front" and imgs:
                old = imgs[0]
                front_img = {
                    "id": old["id"],
                    "x": old["x"], "y": old["y"],
                    "scale": old["scale"] * SCALE_RATIO,
                    "angle": old.get("angle", 0),
                    "flipX": old.get("flipX", False),
                    "flipY": old.get("flipY", False),
                }

    if not front_img:
        print("  SKIP — no front image found")
        return

    placeholders = []
    if back_image:
        placeholders.append({"position": "back", "images": [back_image]})
    placeholders.append({"position": "front", "images": [front_img]})

    resp = requests.put(
        f"{BASE}/shops/{SHOP_ID}/products/{product_id}.json",
        headers=HEADERS,
        json={"print_areas": [{"variant_ids": all_variant_ids, "placeholders": placeholders}]},
    )
    if not resp.ok:
        print(f"\n  ERROR {resp.status_code}: {resp.text[:300]}")
    resp.raise_for_status()


def main():
    total = len(PRODUCTS)
    ok = 0
    for i, (pid, label) in enumerate(PRODUCTS, 1):
        print(f"[{i:02d}/{total}] {label} ({pid}) ...", end=" ", flush=True)
        product = get_product(pid)
        time.sleep(0.2)
        fix_front_scale(pid, product)
        print("OK")
        ok += 1
        time.sleep(0.2)
    print(f"\n=== Terminé : {ok}/{total} t-shirts mis à jour ===")


if __name__ == "__main__":
    main()
