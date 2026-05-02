#!/usr/bin/env python3
"""Create 34 EN Wanted t-shirts on Printify (17 light + 17 dark).

Copies structure from existing FR products, replacing only the artwork image.
Titles: T-SHIRT {NOM} WANTED EN {N}/17  (light)
        T-SHIRT {NOM} WANTED NOIR EN {N}/17  (dark)
"""

import os
import sys
import json
import time
import base64
import requests

SHOP_ID = "22774508"
API_TOKEN = os.environ.get("PRINTIFY_API_TOKEN")
if not API_TOKEN:
    print("ERROR: PRINTIFY_API_TOKEN not set")
    sys.exit(1)

BASE_URL = "https://api.printify.com/v1"
HEADERS = {
    "Authorization": f"Bearer {API_TOKEN}",
    "Content-Type": "application/json",
    "User-Agent": "ClaudeCode-Hokuno/1.0",
}
PNG_DIR = os.path.join(os.path.dirname(__file__), "..", "exports", "wanted-en")
RESULTS_FILE = os.path.join(PNG_DIR, "results.json")

# Printify-internal SVG asset not accessible via uploads API — must be skipped
INVALID_IMAGE_IDS = {"5941187eb8e7e37b3f0e62e5"}

# n = canonical number (matches INVENTAIRE.md and TODO.md order)
# png = page number in "Copie de THE END" Canva export
# image_id = already uploaded in previous run (skip re-upload if set)
CHARACTERS = [
    {"n":  1, "nom": "LUFI",              "png": "1.png",  "image_id": "69f5e8211219a6da0d033a50", "fr_light": "6849d4756ab7f1ef5d06a2e9", "fr_dark": "684b42ddc1b6866d8600db8f"},
    {"n":  2, "nom": "CHANKS",            "png": "28.png", "image_id": "69f5e824dca9c48965ea9a2f", "fr_light": "684b39093a95f8f9ac0cd9d7", "fr_dark": "684b52a24a52709620072dec"},
    {"n":  3, "nom": "ROROROA ZORO",      "png": "22.png", "image_id": "69f5e828dfe700dfcd70ce00", "fr_light": "684b2dfacd0c3157940915f8", "fr_dark": "684b4e188ad27b8d900556b7"},
    {"n":  4, "nom": "NAMY",              "png": "2.png",  "image_id": "69f5e82b04c54cc960a14629", "fr_light": "684b300c4dfca61d6e03f94c", "fr_dark": "684b4f338ad27b8d900556ff"},
    {"n":  5, "nom": "SANDJI",            "png": "3.png",  "image_id": "69f5e82eb1c028526c57adb7", "fr_light": "684b2d165ea5d8765401f04f", "fr_dark": "684b4d774a52709620072c94"},
    {"n":  6, "nom": "SHOPER",            "png": "26.png", "image_id": "69f5e83356d1a62e45d3c07f", "fr_light": "6849f9d953576a8a950e2eee", "fr_dark": "684b4b9d8ad27b8d9005563e"},
    {"n":  7, "nom": "NIKO ROBINE",       "png": "11.png", "image_id": "69f5e836b106202848a25a80", "fr_light": "684b2ef790d6792b870a98b8", "fr_dark": "684b4ead8b6650a870003f9e"},
    {"n":  8, "nom": "FRANCKY",           "png": "32.png", "image_id": "69f5e8397fc78d304b2ee2a1", "fr_light": "684b35628ad27b8d90055159", "fr_dark": "684b515f5ea5d8765401f813"},
    {"n":  9, "nom": "BROOCK",            "png": "17.png", "image_id": "69f5e83d387089c17e238444", "fr_light": "6849f7fc8b94b5b93d0fcd10", "fr_dark": "684b44995ea5d8765401f580"},
    {"n": 10, "nom": "GOD USSOP",         "png": "31.png", "image_id": "69f5e841dfe700dfcd70ce01", "fr_light": "684b33afa9314bdcdf0d53d7", "fr_dark": "684b50d6c1b6866d8600de29"},
    {"n": 11, "nom": "GYMBEY",            "png": "12.png", "image_id": "69f5e844e3d8599eeb006fc7", "fr_light": "684b327cb0ad75db150b79d1", "fr_dark": "684b50508ad27b8d90055731"},
    {"n": 12, "nom": "BAGGY",             "png": "14.png", "image_id": "69f5e84828f108eac4afbe88", "fr_light": "684b3fee2c4daa76ec095919", "fr_dark": "684b53a2a9314bdcdf0d5a62"},
    {"n": 13, "nom": "CAIDO",             "png": "20.png", "image_id": "69f5e84b1219a6da0d033a54", "fr_light": "684b3a018b6650a870003b88", "fr_dark": "684b532f90d6792b870aa071"},
    {"n": 14, "nom": "DOFLAMYNGO",        "png": "24.png", "image_id": "69f5e84fdfe700dfcd70ce03", "fr_light": "684b37628ad27b8d900551ef", "fr_dark": "684b520eff145207d8018ff7"},
    {"n": 15, "nom": "MARSHAL DI TITTCH", "png": "21.png", "image_id": "69f5e85304c54cc960a1462c", "fr_light": "684b3118ff145207d801891c", "fr_dark": "684b4fc190d6792b870a9fae"},
    {"n": 16, "nom": "SHARLOT LINLINE",   "png": "10.png", "image_id": "69f5e856b65b218c99f7d8af", "fr_light": "684b2b09a9314bdcdf0d5220", "fr_dark": "684b4c7eea64cf1036087f88"},
    {"n": 17, "nom": "ALABASTARDS",       "png": "4.png",  "image_id": "69f5e85acbc82c970fed993a", "fr_light": "684b40a48ad27b8d90055440", "fr_dark": "684b5414b0ad75db150b812b"},
]


def sleep():
    time.sleep(0.2)


def get_product(product_id):
    sleep()
    r = requests.get(f"{BASE_URL}/shops/{SHOP_ID}/products/{product_id}.json", headers=HEADERS, timeout=30)
    r.raise_for_status()
    return r.json()


def upload_image(png_path, file_name):
    sleep()
    with open(png_path, "rb") as f:
        contents = base64.b64encode(f.read()).decode("utf-8")
    r = requests.post(
        f"{BASE_URL}/uploads/images.json",
        headers=HEADERS,
        json={"file_name": file_name, "contents": contents},
        timeout=120,
    )
    r.raise_for_status()
    return r.json()


def build_variants(fr_variants):
    return [
        {"id": v["id"], "price": v["price"], "is_enabled": v["is_enabled"]}
        for v in fr_variants
    ]


def build_print_areas(fr_print_areas, new_image_id):
    """Copy print_areas from FR product.

    - back: replace artwork image with new EN image (same position/scale/angle)
    - front / neck: keep existing image IDs unchanged (logo + label, language-neutral)
    - right_sleeve / left_sleeve: skip if empty — API rejects empty images arrays
    """
    new_areas = []
    for area in fr_print_areas:
        new_area = {"variant_ids": area["variant_ids"]}
        if "font_color" in area:
            new_area["font_color"] = area["font_color"]
        if "font_family" in area:
            new_area["font_family"] = area["font_family"]
        new_area["placeholders"] = []
        for ph in area.get("placeholders", []):
            images = ph.get("images", [])
            if not images:
                continue  # skip empty sleeve placeholders

            new_ph = {"position": ph["position"]}
            if "decoration_method" in ph:
                new_ph["decoration_method"] = ph["decoration_method"]

            if ph["position"] == "back":
                # Replace artwork with new EN image, keep exact positioning
                new_ph["images"] = [
                    {
                        "id": new_image_id,
                        "x": img["x"],
                        "y": img["y"],
                        "scale": img["scale"],
                        "angle": img["angle"],
                        "flipX": img.get("flipX", False),
                        "flipY": img.get("flipY", False),
                    }
                    for img in images
                ]
            else:
                # Keep existing images (front logo, neck label — language-neutral)
                # Skip Printify-internal SVG assets that can't be referenced in new products
                valid = [
                    {
                        "id": img["id"],
                        "x": img["x"],
                        "y": img["y"],
                        "scale": img["scale"],
                        "angle": img["angle"],
                        "flipX": img.get("flipX", False),
                        "flipY": img.get("flipY", False),
                    }
                    for img in images
                    if img["id"] not in INVALID_IMAGE_IDS
                ]
                if not valid:
                    continue
                new_ph["images"] = valid
            new_area["placeholders"].append(new_ph)
        new_areas.append(new_area)
    return new_areas


def create_product(title, fr_product, print_areas):
    sleep()
    payload = {
        "title": title,
        "description": fr_product.get("description", ""),
        "blueprint_id": fr_product["blueprint_id"],
        "print_provider_id": fr_product["print_provider_id"],
        "variants": build_variants(fr_product["variants"]),
        "print_areas": print_areas,
    }
    r = requests.post(
        f"{BASE_URL}/shops/{SHOP_ID}/products.json",
        headers=HEADERS,
        json=payload,
        timeout=60,
    )
    r.raise_for_status()
    return r.json()


results = {}
errors = []

print(f"Starting: {len(CHARACTERS)} characters × 2 versions = {len(CHARACTERS)*2} products")
print("=" * 60)

for char in CHARACTERS:
    n = char["n"]
    nom = char["nom"]
    png_file = char["png"]
    print(f"\n[{n:02d}/17] {nom}", flush=True)

    try:
        # Use pre-uploaded image_id if available, else upload now
        if char.get("image_id"):
            image_id = char["image_id"]
            print(f"  → Reusing image_id: {image_id}", flush=True)
        else:
            png_path = os.path.join(PNG_DIR, png_file)
            if not os.path.exists(png_path):
                raise FileNotFoundError(f"PNG not found: {png_path}")
            safe_name = nom.lower().replace(" ", "-")
            print(f"  → Upload {png_file} ({os.path.getsize(png_path)//1024}KB)...", flush=True)
            img_resp = upload_image(png_path, f"{safe_name}-wanted-en.png")
            image_id = img_resp["id"]
            print(f"  ✓ image_id: {image_id}", flush=True)

        # EN Light
        print(f"  → GET FR Light {char['fr_light']}...", flush=True)
        fr_light = get_product(char["fr_light"])
        en_light_title = f"T-SHIRT {nom} WANTED EN {n}/17"
        print(f"  → POST {en_light_title}...", flush=True)
        light_resp = create_product(en_light_title, fr_light, build_print_areas(fr_light["print_areas"], image_id))
        en_light_id = light_resp["id"]
        print(f"  ✓ EN Light: {en_light_id}", flush=True)

        # EN Dark
        print(f"  → GET FR Dark {char['fr_dark']}...", flush=True)
        fr_dark = get_product(char["fr_dark"])
        en_dark_title = f"T-SHIRT {nom} WANTED NOIR EN {n}/17"
        print(f"  → POST {en_dark_title}...", flush=True)
        dark_resp = create_product(en_dark_title, fr_dark, build_print_areas(fr_dark["print_areas"], image_id))
        en_dark_id = dark_resp["id"]
        print(f"  ✓ EN Dark: {en_dark_id}", flush=True)

        results[nom] = {
            "n": n,
            "png": png_file,
            "image_id": image_id,
            "en_light_id": en_light_id,
            "en_dark_id": en_dark_id,
        }

    except requests.HTTPError as e:
        body = ""
        try:
            body = e.response.json()
        except Exception:
            body = e.response.text[:200]
        print(f"  ✗ HTTP {e.response.status_code}: {body}", flush=True)
        errors.append({"n": n, "nom": nom, "error": f"HTTP {e.response.status_code}: {body}"})

    except Exception as e:
        print(f"  ✗ ERROR: {e}", flush=True)
        errors.append({"n": n, "nom": nom, "error": str(e)})

# Save results
with open(RESULTS_FILE, "w", encoding="utf-8") as f:
    json.dump({"results": results, "errors": errors}, f, indent=2, ensure_ascii=False)

print("\n" + "=" * 60)
print(f"✅ Created: {len(results)}/17 characters ({len(results)*2} products)")
if errors:
    print(f"❌ Errors:  {len(errors)}")
    for e in errors:
        print(f"   [{e['n']:02d}] {e['nom']}: {e['error']}")
print(f"Results → {RESULTS_FILE}")
