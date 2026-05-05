import os
import requests
import time

API_TOKEN = os.environ.get("PRINTIFY_API_TOKEN")
SHOP_ID = "22774508"
HEADERS = {
    "Authorization": f"Bearer {API_TOKEN}",
    "Content-Type": "application/json"
}

# Full product_id → (number, total)
ID_TO_NUMBER = {
    # WANTED Light /17
    "6849d4756ab7f1ef5d06a2e9": (1, 17),
    "684b39093a95f8f9ac0cd9d7": (2, 17),
    "684b2dfacd0c3157940915f8": (3, 17),
    "684b300c4dfca61d6e03f94c": (4, 17),
    "684b2d165ea5d8765401f04f": (5, 17),
    "6849f9d953576a8a950e2eee": (6, 17),
    "684b2ef790d6792b870a98b8": (7, 17),
    "684b35628ad27b8d90055159": (8, 17),
    "6849f7fc8b94b5b93d0fcd10": (9, 17),
    "684b33afa9314bdcdf0d53d7": (10, 17),
    "684b327cb0ad75db150b79d1": (11, 17),
    "684b3fee2c4daa76ec095919": (12, 17),
    "684b3a018b6650a870003b88": (13, 17),
    "684b37628ad27b8d900551ef": (14, 17),
    "684b3118ff145207d801891c": (15, 17),
    "684b2b09a9314bdcdf0d5220": (16, 17),
    "684b40a48ad27b8d90055440": (17, 17),
    # WANTED Noir /17
    "684b42ddc1b6866d8600db8f": (1, 17),
    "684b52a24a52709620072dec": (2, 17),
    "684b4e188ad27b8d900556b7": (3, 17),
    "684b4f338ad27b8d900556ff": (4, 17),
    "684b4d774a52709620072c94": (5, 17),
    "684b4b9d8ad27b8d9005563e": (6, 17),
    "684b4ead8b6650a870003f9e": (7, 17),
    "684b515f5ea5d8765401f813": (8, 17),
    "684b44995ea5d8765401f580": (9, 17),
    "684b50d6c1b6866d8600de29": (10, 17),
    "684b50508ad27b8d90055731": (11, 17),
    "684b53a2a9314bdcdf0d5a62": (12, 17),
    "684b532f90d6792b870aa071": (13, 17),
    "684b520eff145207d8018ff7": (14, 17),
    "684b4fc190d6792b870a9fae": (15, 17),
    "684b4c7eea64cf1036087f88": (16, 17),
    "684b5414b0ad75db150b812b": (17, 17),
    # WANTED Mugs /17
    "684eb0d009bce0c2370d8203": (1, 17),
    "684ed8bad504d7af62062375": (2, 17),
    "684ed2d0d504d7af6206223c": (3, 17),
    "684ed4c5047ae76743047c14": (4, 17),
    "684ed212047ae76743047b84": (5, 17),
    "684ecee209bce0c2370d881a": (6, 17),
    "684ed400b41682e82d0bcceb": (7, 17),
    "684ed7650944c2e20d0f4c2f": (8, 17),
    "684ecdff047ae76743047ab5": (9, 17),
    "684ed66f09bce0c2370d899e": (10, 17),
    "684ed563b41682e82d0bcd1d": (11, 17),
    "684eda3e09bce0c2370d8a5d": (12, 17),
    "684ed9831d7c908d840ce998": (13, 17),
    "684ed81609bce0c2370d89f1": (14, 17),
    "684ed552047ae76743047c2d": (15, 17),
    "684ecfa38a7f6f02b7056fe0": (16, 17),
    "684dc28bb2d4e68c870e3445": (17, 17),
    # DIRECTION Light /10
    "684c63107a567575d002f21b": (1, 10),
    "684c63e57a567575d002f24c": (2, 10),
    "684c64317a567575d002f25a": (3, 10),
    "684c648061f0867d160dcdbb": (4, 10),
    "684c64cdf8df6e09820d1487": (5, 10),
    "684c65141d7c908d840c5e16": (6, 10),
    "684c656856fb86136206591f": (7, 10),
    "684c65b97a567575d002f2d6": (8, 10),
    "684c65fbdb8b74bc2d0b88bd": (9, 10),
    "684c664a7a567575d002f304": (10, 10),
    # DIRECTION Noir /10
    "684c68d987f5fc4a8101133d": (1, 10),
    "684c693fb2d4e68c870de492": (2, 10),
    "684c699f902f42fe2e080880": (3, 10),
    "684c6a3fb41682e82d0b4390": (4, 10),
    "684c69f1586f185e4005b09f": (5, 10),
    "684c6a84b41682e82d0b43ac": (6, 10),
    "684c6ac6f3b91cf7810bf3c6": (7, 10),
    "684c6b157a567575d002f416": (8, 10),
    "684c6b5587f5fc4a810113bf": (9, 10),
    "684c6b98f3b91cf7810bf40a": (10, 10),
    # DIRECTION Mug /10 (Luffy only)
    "684d56c509bce0c2370d3254": (1, 10),
    # MYTHOLOGIE Light /10 (skip 6=Choper, 8=Robin — no light version)
    "6846b317f4071352350c150a": (1, 10),
    "6849a0426ab7f1ef5d069673": (2, 10),
    "6849a4237483e9399e0d4444": (3, 10),
    "6849a898e27810926a088854": (4, 10),
    "6849a6e0bd30bb1f1304c67e": (5, 10),
    "6849a62c7483e9399e0d44b5": (7, 10),
    "6849a7abf43bb403450bd907": (9, 10),
    "6849a4e7d5b83610460568ba": (10, 10),
    # MYTHOLOGIE Noir /10
    "6849b61fd0482255940866ea": (1, 10),
    "6849c1ce6ab7f1ef5d069e35": (2, 10),
    "6849c07b943f652c190bd88d": (3, 10),
    "6849c298b5bde8e15300e417": (4, 10),
    "6849be2de27810926a088d94": (5, 10),
    "6849a7517483e9399e0d44ef": (6, 10),
    "6849bfd6943f652c190bd86d": (7, 10),
    "6849a8397483e9399e0d455d": (8, 10),
    "6849c4469bf7aebaf7048740": (9, 10),
    "6849c0fc9bf7aebaf704867b": (10, 10),
    # MYTHOLOGIE Mug /10 (Luffy only)
    "684d59ac1d7c908d840c9497": (1, 10),
    # MYTHOLOGIE Coque /10 (Zoro only)
    "684d613ffef859492303a65a": (2, 10),
}

def get_all_products():
    all_products = []
    page = 1
    while True:
        resp = requests.get(
            f"https://api.printify.com/v1/shops/{SHOP_ID}/products.json?page={page}&limit=50",
            headers=HEADERS
        )
        data = resp.json()
        products = data.get("data", [])
        all_products.extend(products)
        last_page = data.get("last_page", 1)
        if page >= last_page:
            break
        page += 1
    return all_products

def rename_product(product_id, new_title):
    resp = requests.put(
        f"https://api.printify.com/v1/shops/{SHOP_ID}/products/{product_id}.json",
        headers=HEADERS,
        json={"title": new_title}
    )
    return resp.status_code, resp.text[:200]

print("Fetching products...")
products = get_all_products()
print(f"Found {len(products)} products\n")

renames = []
skipped = []
for p in products:
    pid = p["id"]
    current_title = p["title"]
    if pid in ID_TO_NUMBER:
        n, total = ID_TO_NUMBER[pid]
        new_title = f"{current_title} {n}/{total}"
        renames.append((pid, current_title, new_title))
    else:
        skipped.append((pid, current_title))

print(f"Products to rename: {len(renames)}")
if skipped:
    print(f"Products skipped (not in map): {len(skipped)}")
    for pid, title in skipped:
        print(f"  SKIP {pid}: {title}")

print("\nStarting renames...\n")
success = 0
errors = []
for i, (pid, old_title, new_title) in enumerate(renames):
    status, body = rename_product(pid, new_title)
    if status == 200:
        success += 1
        print(f"[{i+1:02d}/{len(renames)}] OK  {old_title}  →  {new_title}")
    else:
        errors.append((pid, old_title, new_title, status, body))
        print(f"[{i+1:02d}/{len(renames)}] ERR {old_title} (HTTP {status}): {body}")
    time.sleep(0.2)

print(f"\n{'='*60}")
print(f"Done: {success}/{len(renames)} renamed successfully")
if errors:
    print(f"\nERRORS ({len(errors)}):")
    for pid, old, new, status, body in errors:
        print(f"  {pid}: {old} → {new} (HTTP {status})")
