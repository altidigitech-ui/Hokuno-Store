#!/usr/bin/env python3
"""Create Direction EN t-shirts (light + dark) using FR products as templates."""

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

# FR templates → EN products to create
# (fr_product_id, char_key, char_name, number, variant)
TEMPLATES = [
    # Light (blanc)
    ("684c63107a567575d002f21b", "LUFFY",   "Luffy",   "1/10",  "light"),
    ("684c63e57a567575d002f24c", "ZORO",    "Zoro",    "2/10",  "light"),
    ("684c64317a567575d002f25a", "NAMI",    "Nami",    "3/10",  "light"),
    ("684c648061f0867d160dcdbb", "USSOP",   "Ussop",   "4/10",  "light"),
    ("684c64cdf8df6e09820d1487", "SANJI",   "Sanji",   "5/10",  "light"),
    ("684c65141d7c908d840c5e16", "CHOPER",  "Chopper", "6/10",  "light"),
    ("684c656856fb86136206591f", "FRANKY",  "Francky", "7/10",  "light"),
    ("684c65b97a567575d002f2d6", "ROBIN",   "Robin",   "8/10",  "light"),
    ("684c65fbdb8b74bc2d0b88bd", "BROOK",   "Brook",   "9/10",  "light"),
    ("684c664a7a567575d002f304", "JINBE",   "Jimbe",   "10/10", "light"),
    # Dark (noir)
    ("684c68d987f5fc4a8101133d", "LUFFY",   "Luffy",   "1/10",  "dark"),
    ("684c693fb2d4e68c870de492", "ZORO",    "Zoro",    "2/10",  "dark"),
    ("684c699f902f42fe2e080880", "NAMI",    "Nami",    "3/10",  "dark"),
    ("684c6a3fb41682e82d0b4390", "USSOP",   "Ussop",   "4/10",  "dark"),
    ("684c69f1586f185e4005b09f", "SANJI",   "Sanji",   "5/10",  "dark"),
    ("684c6a84b41682e82d0b43ac", "CHOPER",  "Chopper", "6/10",  "dark"),
    ("684c6ac6f3b91cf7810bf3c6", "FRANKY",  "Francky", "7/10",  "dark"),
    ("684c6b157a567575d002f416", "ROBIN",   "Robin",   "8/10",  "dark"),
    ("684c6b5587f5fc4a810113bf", "BROOK",   "Brook",   "9/10",  "dark"),
    ("684c6b98f3b91cf7810bf40a", "JINBE",   "Jimbe",   "10/10", "dark"),
]

DESCRIPTION = (
    "<p>The unisex heavy cotton tee is the basic staple of any wardrobe. It is the foundation "
    "upon which casual fashion grows. All it needs is a personalized design to elevate things "
    "to profitability. The specially spun fibers provide a smooth surface for premium printing "
    "vividity and sharpness. No side seams mean there are no itchy interruptions under the arms. "
    "The shoulders have tape for improved durability.</p><br/>"
    "<p>.: Made with medium fabric (5.3 oz/yd² (180 g/m²)) consisting of 100% cotton for "
    "year-round comfort that is sustainable and highly durable.<br/>"
    ".: The classic fit of this shirt ensures a comfy, relaxed wear while the crew neckline "
    "adds that neat, timeless look that can blend into any occasion, casual or semi-formal.<br/>"
    ".: The tear-away label means a scratch-free experience with no irritation or discomfort "
    "whatsoever.<br/>"
    ".: Made using 100% US cotton that is ethically grown and harvested.</p>"
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


def get_product(product_id: str) -> dict:
    resp = requests.get(
        f"{BASE}/shops/{SHOP_ID}/products/{product_id}.json",
        headers=HEADERS,
    )
    resp.raise_for_status()
    return resp.json()


def build_print_areas(template: dict, new_back_image_id: str) -> list:
    """Copy template print_areas, replace back image with new EN image."""
    areas = template["print_areas"]
    result = []
    for area in areas:
        placeholders = []
        for ph in area["placeholders"]:
            if not ph.get("images"):
                continue  # skip empty (right_sleeve, left_sleeve)

            if ph["position"] == "back":
                old = ph["images"][0]
                placeholders.append({
                    "position": "back",
                    "images": [{
                        "id": new_back_image_id,
                        "x": old["x"],
                        "y": old["y"],
                        "scale": old["scale"],
                        "angle": old["angle"],
                        "flipX": old.get("flipX", False),
                        "flipY": old.get("flipY", False),
                    }]
                })
            else:
                # Keep front/neck as-is (same logo, same small character)
                images = []
                for img in ph["images"]:
                    images.append({
                        "id": img["id"],
                        "x": img["x"],
                        "y": img["y"],
                        "scale": img["scale"],
                        "angle": img["angle"],
                        "flipX": img.get("flipX", False),
                        "flipY": img.get("flipY", False),
                    })
                placeholders.append({
                    "position": ph["position"],
                    "images": images,
                })

        result.append({
            "variant_ids": area["variant_ids"],
            "placeholders": placeholders,
        })
    return result


def create_product(title: str, template: dict, print_areas: list) -> str:
    payload = {
        "title": title,
        "description": DESCRIPTION,
        "blueprint_id": template["blueprint_id"],
        "print_provider_id": template["print_provider_id"],
        "variants": [
            {"id": v["id"], "price": v["price"], "is_enabled": v["is_enabled"]}
            for v in template["variants"]
        ],
        "print_areas": print_areas,
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
    repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    results = []

    for fr_id, char_key, char_name, number, variant in TEMPLATES:
        folder = f"direction-en-{variant}"
        img_path = os.path.join(repo_root, "exports", folder, f"{char_name}.png")
        suffix = " NOIR" if variant == "dark" else ""
        title = f"T-SHIRT {char_key} DIRECTION EN{suffix} {number}"

        print(f"\n[{variant.upper()}] {char_key} — {title}")

        if not os.path.exists(img_path):
            print(f"  ⚠ Image introuvable : {img_path}")
            continue

        print(f"  Upload {char_name.lower()}-direction-en-{variant}.png...", end=" ", flush=True)
        image_id = upload_image(img_path, f"{char_name.lower()}-direction-en-{variant}.png")
        print(f"ID={image_id}")
        time.sleep(0.2)

        print(f"  GET template FR...", end=" ", flush=True)
        template = get_product(fr_id)
        print("OK")
        time.sleep(0.2)

        print_areas = build_print_areas(template, image_id)

        print(f"  POST création produit...", end=" ", flush=True)
        new_id = create_product(title, template, print_areas)
        print(f"OK → {new_id}")
        results.append({"id": new_id, "title": title})
        time.sleep(0.3)

    print("\n=== Récapitulatif ===")
    for r in results:
        print(f"  {r['id']}  {r['title']}")
    print(f"\nTotal créés : {len(results)}/20")


if __name__ == "__main__":
    main()
