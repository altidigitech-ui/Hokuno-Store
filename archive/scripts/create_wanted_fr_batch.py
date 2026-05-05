#!/usr/bin/env python3
"""
Create Wanted FR products (light + dark) for the 29 missing characters (18-46).
Templates: KUMA EN products (same blueprint/provider/positions).
Images: exports/wanted-fr/{N}.png (already cropped, 1198x1690).
Updates wanted.json tshirt_fr_light / tshirt_fr_dark after each success.
"""

import base64, json, os, subprocess, tempfile, time
from pathlib import Path

TOKEN = os.environ.get('PRINTIFY_API_TOKEN', '')
SHOP_ID = '22774508'
BASE_URL = f'https://api.printify.com/v1/shops/{SHOP_ID}'
UPLOAD_URL = 'https://api.printify.com/v1/uploads/images.json'
EXPORTS_DIR = Path('exports/wanted-fr')
WANTED_JSON = Path('collections/wanted.json')

# These image IDs exist on Printify but are invalid for product creation
INVALID_IMAGE_IDS = {'5941187eb8e7e37b3f0e62e5'}

# KUMA EN products used as templates (blueprint/provider/variants/print_areas)
KUMA_LIGHT_ID = '69f630759110dda91005f3c6'
KUMA_DARK_ID  = '69f631d6b3bda8532c0c20f7'

# (png_number, json_index_0based, display_number_1based)
# png_number = filename in exports/wanted-fr/ (N.png)
# json_index = position in personnages[] array
# display_number = N/46
CHARACTERS = [
    (18, 17, 18),
    (19, 18, 19),
    (20, 19, 20),
    (21, 20, 21),
    (22, 21, 22),
    (23, 22, 23),
    (24, 23, 24),
    (25, 24, 25),
    (26, 25, 26),
    (27, 26, 27),
    (28, 27, 28),
    (29, 28, 29),
    (30, 29, 30),
    (31, 30, 31),
    (32, 31, 32),
    (33, 32, 33),
    (34, 33, 34),
    (35, 34, 35),
    (36, 35, 36),
    (37, 36, 37),
    (38, 37, 38),
    (39, 38, 39),
    (40, 39, 40),
    (41, 40, 41),
    (42, 41, 42),
    (43, 42, 43),
    (44, 43, 44),
    (45, 44, 45),
    (46, 45, 46),
]


def api_get(url):
    r = subprocess.run(
        ['curl', '-s', '-H', f'Authorization: Bearer {TOKEN}',
         '-H', 'User-Agent: ClaudeCode-Hokuno/1.0', url],
        capture_output=True, text=True, timeout=30
    )
    return json.loads(r.stdout)


def post_json(url, data):
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        json.dump(data, f)
        path = f.name
    try:
        r = subprocess.run(
            ['curl', '-s', '-X', 'POST', url,
             '-H', f'Authorization: Bearer {TOKEN}',
             '-H', 'Content-Type: application/json',
             '-H', 'User-Agent: ClaudeCode-Hokuno/1.0',
             '-d', f'@{path}'],
            capture_output=True, text=True, timeout=90
        )
        return json.loads(r.stdout)
    finally:
        os.unlink(path)


def upload_image(png_path, file_name):
    with open(png_path, 'rb') as f:
        b64 = base64.b64encode(f.read()).decode()
    resp = post_json(UPLOAD_URL, {'file_name': file_name, 'contents': b64})
    if 'id' not in resp:
        raise RuntimeError(f'Upload failed: {resp}')
    print(f'  [upload] id={resp["id"]}  {resp["width"]}×{resp["height"]}')
    return resp['id']


def build_print_areas(template_areas, new_image_id):
    new_areas = []
    for area in template_areas:
        new_area = {'variant_ids': area['variant_ids']}
        if 'font_color' in area:
            new_area['font_color'] = area['font_color']
        if 'font_family' in area:
            new_area['font_family'] = area['font_family']
        new_area['placeholders'] = []
        for ph in area.get('placeholders', []):
            images = ph.get('images', [])
            if not images:
                continue
            new_ph = {'position': ph['position']}
            if 'decoration_method' in ph:
                new_ph['decoration_method'] = ph['decoration_method']
            if ph['position'] == 'back':
                orig = images[0]
                new_ph['images'] = [{
                    'id': new_image_id,
                    'x': orig['x'], 'y': orig['y'],
                    'scale': orig['scale'], 'angle': orig['angle'],
                    'flipX': orig.get('flipX', False),
                    'flipY': orig.get('flipY', False),
                }]
            else:
                valid = [
                    {'id': img['id'], 'x': img['x'], 'y': img['y'],
                     'scale': img['scale'], 'angle': img['angle'],
                     'flipX': img.get('flipX', False), 'flipY': img.get('flipY', False)}
                    for img in images if img['id'] not in INVALID_IMAGE_IDS
                ]
                if not valid:
                    continue
                new_ph['images'] = valid
            new_area['placeholders'].append(new_ph)
        new_areas.append(new_area)
    return new_areas


def create_product(title, template, new_image_id):
    variants = [{'id': v['id'], 'price': v['price'], 'is_enabled': v['is_enabled']}
                for v in template['variants']]
    print_areas = build_print_areas(template['print_areas'], new_image_id)
    payload = {
        'title': title,
        'blueprint_id': template['blueprint_id'],
        'print_provider_id': template['print_provider_id'],
        'variants': variants,
        'print_areas': print_areas,
    }
    resp = post_json(f'{BASE_URL}/products.json', payload)
    if 'id' not in resp:
        raise RuntimeError(f'Product creation failed: {resp}')
    return resp['id']


def update_wanted_json(json_idx, light_id, dark_id):
    with open(WANTED_JSON) as f:
        data = json.load(f)
    chars = data['personnages']
    ids = chars[json_idx].setdefault('printify_product_ids', {})
    if light_id:
        ids['tshirt_fr_light'] = light_id
    if dark_id:
        ids['tshirt_fr_dark'] = dark_id
    with open(WANTED_JSON, 'w') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def sleep(s=3):
    time.sleep(s)


def main():
    if not TOKEN:
        raise SystemExit('PRINTIFY_API_TOKEN not set')

    print('Fetching KUMA EN light template...')
    light_tpl = api_get(f'{BASE_URL}/products/{KUMA_LIGHT_ID}.json')
    print(f'  Light: {light_tpl["title"]}  variants={len(light_tpl["variants"])}')
    sleep(2)

    print('Fetching KUMA EN dark template...')
    dark_tpl = api_get(f'{BASE_URL}/products/{KUMA_DARK_ID}.json')
    print(f'  Dark:  {dark_tpl["title"]}  variants={len(dark_tpl["variants"])}')
    sleep(2)

    with open(WANTED_JSON) as f:
        wanted_data = json.load(f)
    chars = wanted_data['personnages']

    total = len(CHARACTERS)
    for idx, (png_num, json_idx, display_num) in enumerate(CHARACTERS, 1):
        name = chars[json_idx]['nom']
        name_upper = name.upper()
        png_path = EXPORTS_DIR / f'{png_num}.png'

        print(f'\n[{idx}/{total}] {png_path.name} — {name} ({display_num}/46)')

        if not png_path.exists():
            print(f'  ERROR: {png_path} not found, skipping')
            continue

        # Upload FR image
        try:
            sleep(2)
            image_id = upload_image(png_path, f'{png_num}-{name.lower().replace(" ", "-")}-wanted-fr.png')
        except Exception as e:
            print(f'  ERROR upload: {e}')
            continue

        # Create light
        light_title = f'T-SHIRT {name_upper} WANTED {display_num}/46'
        try:
            sleep(3)
            light_id = create_product(light_title, light_tpl, image_id)
            print(f'  [light] {light_title} → {light_id}')
        except Exception as e:
            print(f'  ERROR light: {e}')
            light_id = ''

        # Create dark
        dark_title = f'T-SHIRT {name_upper} WANTED NOIR {display_num}/46'
        try:
            sleep(3)
            dark_id = create_product(dark_title, dark_tpl, image_id)
            print(f'  [dark]  {dark_title} → {dark_id}')
        except Exception as e:
            print(f'  ERROR dark: {e}')
            dark_id = ''

        # Save to JSON
        if light_id or dark_id:
            update_wanted_json(json_idx, light_id, dark_id)
            print(f'  [json] wanted.json updated')

        sleep(3)

    print('\n✅ Batch complete.')


if __name__ == '__main__':
    main()
