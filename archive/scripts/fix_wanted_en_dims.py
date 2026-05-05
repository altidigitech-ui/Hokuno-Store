#!/usr/bin/env python3
"""Fix EN Wanted products: correct width/height metadata for front and neck images.

Root cause: when EN products were created via POST without width/height fields,
Printify defaulted all image dimensions to ~1555x2000 (the EN back image size).
This causes the editor to show wrong Scale% (e.g. 18.22% instead of 53.59%).

Fix: PUT with correct width/height taken from the FR product for front/neck images.
The back image keeps its actual EN dimensions (fetched from current EN product).
"""

import os, sys, json, time, requests

SHOP_ID = "22774508"
API_TOKEN = os.environ.get("PRINTIFY_API_TOKEN")
if not API_TOKEN:
    print("ERROR: PRINTIFY_API_TOKEN not set"); sys.exit(1)

BASE_URL = "https://api.printify.com/v1"
INVALID_IMAGE_IDS = {"5941187eb8e7e37b3f0e62e5"}
HEADERS = {
    "Authorization": f"Bearer {API_TOKEN}",
    "Content-Type": "application/json",
    "User-Agent": "ClaudeCode-Hokuno/1.0",
}

CHARACTERS = [
    {"n":  1, "nom": "LUFI",              "image_id": "69f5e8211219a6da0d033a50", "fr_light": "6849d4756ab7f1ef5d06a2e9", "fr_dark": "684b42ddc1b6866d8600db8f", "en_light": "69f6032239e419a2dc02e247", "en_dark": "69f603f5ef66d02ffe02b1ce"},
    {"n":  2, "nom": "CHANKS",            "image_id": "69f5e824dca9c48965ea9a2f", "fr_light": "684b39093a95f8f9ac0cd9d7", "fr_dark": "684b52a24a52709620072dec", "en_light": "69f5ec1fe1b7b9b0b0086b67", "en_dark": "69f5ec26e1b7b9b0b0086b6e"},
    {"n":  3, "nom": "ROROROA ZORO",      "image_id": "69f5e828dfe700dfcd70ce00", "fr_light": "684b2dfacd0c3157940915f8", "fr_dark": "684b4e188ad27b8d900556b7", "en_light": "69f5ec2fcf535c302f083ccd", "en_dark": "69f5ec391cc4ed38fb0b77d1"},
    {"n":  4, "nom": "NAMY",              "image_id": "69f5e82b04c54cc960a14629", "fr_light": "684b300c4dfca61d6e03f94c", "fr_dark": "684b4f338ad27b8d900556ff", "en_light": "69f5ec3fe1b7b9b0b0086b7e", "en_dark": "69f5ec44db88631ee309c0b2"},
    {"n":  5, "nom": "SANDJI",            "image_id": "69f5e82eb1c028526c57adb7", "fr_light": "684b2d165ea5d8765401f04f", "fr_dark": "684b4d774a52709620072c94", "en_light": "69f5ec4b1cc4ed38fb0b77fc", "en_dark": "69f5ec51db88631ee309c0e4"},
    {"n":  6, "nom": "SHOPER",            "image_id": "69f5e83356d1a62e45d3c07f", "fr_light": "6849f9d953576a8a950e2eee", "fr_dark": "684b4b9d8ad27b8d9005563e", "en_light": "69f5ec57ef66d02ffe02a19b", "en_dark": "69f5ec5f1cc4ed38fb0b781b"},
    {"n":  7, "nom": "NIKO ROBINE",       "image_id": "69f5e836b106202848a25a80", "fr_light": "684b2ef790d6792b870a98b8", "fr_dark": "684b4ead8b6650a870003f9e", "en_light": "69f5ec68ecefd0d57d047d32", "en_dark": "69f5ec75cf535c302f083d21"},
    {"n":  8, "nom": "FRANCKY",           "image_id": "69f5e8397fc78d304b2ee2a1", "fr_light": "684b35628ad27b8d90055159", "fr_dark": "684b515f5ea5d8765401f813", "en_light": "69f5ec7bcf535c302f083d29", "en_dark": "69f5ec84db88631ee309c111"},
    {"n":  9, "nom": "BROOCK",            "image_id": "69f5e83d387089c17e238444", "fr_light": "6849f7fc8b94b5b93d0fcd10", "fr_dark": "684b44995ea5d8765401f580", "en_light": "69f5ec8b758757bfa3041238", "en_dark": "69f5ec94cf535c302f083d3b"},
    {"n": 10, "nom": "GOD USSOP",         "image_id": "69f5e841dfe700dfcd70ce01", "fr_light": "684b33afa9314bdcdf0d53d7", "fr_dark": "684b50d6c1b6866d8600de29", "en_light": "69f5ec9a1cc4ed38fb0b7851", "en_dark": "69f5ec9fe1b7b9b0b0086bfc"},
    {"n": 11, "nom": "GYMBEY",            "image_id": "69f5e844e3d8599eeb006fc7", "fr_light": "684b327cb0ad75db150b79d1", "fr_dark": "684b50508ad27b8d90055731", "en_light": "69f5eca5ef66d02ffe02a1d2", "en_dark": "69f5ecacecefd0d57d047d56"},
    {"n": 12, "nom": "BAGGY",             "image_id": "69f5e84828f108eac4afbe88", "fr_light": "684b3fee2c4daa76ec095919", "fr_dark": "684b53a2a9314bdcdf0d5a62", "en_light": "69f5ecb3758757bfa3041249", "en_dark": "69f5ecb9ef66d02ffe02a1db"},
    {"n": 13, "nom": "CAIDO",             "image_id": "69f5e84b1219a6da0d033a54", "fr_light": "684b3a018b6650a870003b88", "fr_dark": "684b532f90d6792b870aa071", "en_light": "69f5ecbf758757bfa304124b", "en_dark": "69f5ecc5ef66d02ffe02a1dc"},
    {"n": 14, "nom": "DOFLAMYNGO",        "image_id": "69f5e84fdfe700dfcd70ce03", "fr_light": "684b37628ad27b8d900551ef", "fr_dark": "684b520eff145207d8018ff7", "en_light": "69f5eccb758757bfa304124d", "en_dark": "69f5ecd14369722b330efb0e"},
    {"n": 15, "nom": "MARSHAL DI TITTCH", "image_id": "69f5e85304c54cc960a1462c", "fr_light": "684b3118ff145207d801891c", "fr_dark": "684b4fc190d6792b870a9fae", "en_light": "69f5ed3adb88631ee309c14d", "en_dark": "69f5ed40348775ebe705b79f"},
    {"n": 16, "nom": "SHARLOT LINLINE",   "image_id": "69f5e856b65b218c99f7d8af", "fr_light": "684b2b09a9314bdcdf0d5220", "fr_dark": "684b4c7eea64cf1036087f88", "en_light": "69f5ed00e1b7b9b0b0086c1b", "en_dark": "69f5ed06348775ebe705b78a"},
    {"n": 17, "nom": "ALABASTARDS",       "image_id": "69f5e85acbc82c970fed993a", "fr_light": "684b40a48ad27b8d90055440", "fr_dark": "684b5414b0ad75db150b812b", "en_light": "69f5ed0d348775ebe705b78d", "en_dark": "69f5ed13e1b7b9b0b0086c22"},
]


def sleep():
    time.sleep(0.2)


def get_product(pid):
    sleep()
    r = requests.get(f"{BASE_URL}/shops/{SHOP_ID}/products/{pid}.json", headers=HEADERS, timeout=30)
    r.raise_for_status()
    return r.json()


def get_back_dims(product):
    """Return stored width/height of the back image from a product."""
    for area in product["print_areas"]:
        for ph in area.get("placeholders", []):
            if ph["position"] == "back":
                for img in ph.get("images", []):
                    return {"width": img.get("width"), "height": img.get("height")}
    return {}


def build_print_areas(fr_product, new_back_image_id, en_back_dims):
    """
    Deep-copy FR print_areas with:
    - back  : new EN image id + EN image dimensions (width/height)
    - front : FR image id + FR dimensions (unchanged)
    - neck  : FR image ids + FR dimensions, minus text_layer SVG
    - sleeves: skipped if empty
    """
    new_areas = []
    for area in fr_product["print_areas"]:
        new_area = {"variant_ids": area["variant_ids"]}
        if "font_color" in area:
            new_area["font_color"] = area["font_color"]
        if "font_family" in area:
            new_area["font_family"] = area["font_family"]
        new_area["placeholders"] = []

        for ph in area.get("placeholders", []):
            pos = ph["position"]
            raw_images = ph.get("images", [])

            if pos == "back":
                valid = raw_images  # keep all back images (there is only one)
            else:
                valid = [img for img in raw_images if img["id"] not in INVALID_IMAGE_IDS]

            if not valid:
                continue  # skip empty sleeves and placeholders emptied by SVG filter

            new_ph = {"position": pos}
            if "decoration_method" in ph:
                new_ph["decoration_method"] = ph["decoration_method"]

            new_imgs = []
            for img in valid:
                if pos == "back":
                    new_imgs.append({
                        "id":     new_back_image_id,
                        "x":      img["x"],
                        "y":      img["y"],
                        "scale":  img["scale"],
                        "angle":  img.get("angle", 0),
                        "flipX":  img.get("flipX", False),
                        "flipY":  img.get("flipY", False),
                        "width":  en_back_dims.get("width", img.get("width")),
                        "height": en_back_dims.get("height", img.get("height")),
                    })
                else:
                    new_imgs.append({
                        "id":     img["id"],
                        "x":      img["x"],
                        "y":      img["y"],
                        "scale":  img["scale"],
                        "angle":  img.get("angle", 0),
                        "flipX":  img.get("flipX", False),
                        "flipY":  img.get("flipY", False),
                        "width":  img.get("width"),
                        "height": img.get("height"),
                    })

            new_ph["images"] = new_imgs
            new_area["placeholders"].append(new_ph)

        new_areas.append(new_area)
    return new_areas


def put_product(pid, print_areas):
    sleep()
    r = requests.put(
        f"{BASE_URL}/shops/{SHOP_ID}/products/{pid}.json",
        headers=HEADERS,
        json={"print_areas": print_areas},
        timeout=60,
    )
    r.raise_for_status()
    return r.json()


errors = []
rows = []

print(f"Fixing width/height metadata for {len(CHARACTERS) * 2} EN products...")
print("=" * 80)

for char in CHARACTERS:
    n   = char["n"]
    nom = char["nom"]
    print(f"\n[{n:02d}/17] {nom}", flush=True)

    for version, fr_id, en_id in [
        ("LIGHT", char["fr_light"], char["en_light"]),
        ("DARK",  char["fr_dark"],  char["en_dark"]),
    ]:
        try:
            print(f"  {version}: GET FR {fr_id}...", flush=True)
            fr = get_product(fr_id)

            print(f"  {version}: GET EN {en_id} (for back dims)...", flush=True)
            en = get_product(en_id)
            en_back_dims = get_back_dims(en)

            print_areas = build_print_areas(fr, char["image_id"], en_back_dims)

            # Spot-check: verify front logo dims match FR
            for area in print_areas:
                for ph in area.get("placeholders", []):
                    if ph["position"] == "front":
                        img = ph["images"][0]
                        print(f"  {version}: front → id={img['id'][:8]}... w={img['width']} h={img['height']} scale={img['scale']:.5f}", flush=True)

            print(f"  {version}: PUT EN {en_id}...", flush=True)
            put_product(en_id, print_areas)
            print(f"  {version}: ✓ OK", flush=True)
            rows.append((n, nom, version, en_id, "✓"))

        except requests.HTTPError as e:
            body = ""
            try:   body = e.response.json()
            except: body = e.response.text[:300]
            print(f"  {version}: ✗ HTTP {e.response.status_code}: {body}", flush=True)
            errors.append({"n": n, "nom": nom, "version": version, "error": str(body)})
            rows.append((n, nom, version, en_id, "✗"))

        except Exception as e:
            print(f"  {version}: ✗ {e}", flush=True)
            errors.append({"n": n, "nom": nom, "version": version, "error": str(e)})
            rows.append((n, nom, version, en_id, "✗"))


print("\n" + "=" * 80)
ok = len([r for r in rows if r[4] == "✓"])
print(f"✅ Corrigés : {ok}/34")
if errors:
    print(f"❌ Erreurs  : {len(errors)}")
    for e in errors:
        print(f"   [{e['n']:02d}] {e['nom']} {e['version']}: {e['error']}")

# Verify first product after fix
print("\n--- Vérification EN DARK LUFI après fix ---")
try:
    en_check = get_product("69f603f5ef66d02ffe02b1ce")
    for area in en_check["print_areas"]:
        for ph in area.get("placeholders", []):
            pos = ph["position"]
            for img in ph.get("images", []):
                print(f"  [{pos}] {img.get('name','?')}: w={img.get('width')} h={img.get('height')} scale={img['scale']:.6f}")
except Exception as e:
    print(f"  Vérif échouée: {e}")
