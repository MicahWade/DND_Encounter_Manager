import os
import json
from PIL import Image

Image.MAX_IMAGE_PIXELS = None

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../static'))
ASSETS_JSON_PATH = os.path.join(os.path.dirname(__file__), 'assets.json')
TARGET_SHORT_SIDE = 1080

with open(ASSETS_JSON_PATH, 'r', encoding='utf-8') as f:
    assets = json.load(f)

for asset in assets:
    if asset.get('type', '').lower() != 'map':
        continue

    original_rel_path = asset['path']
    original_full_path = os.path.join(BASE_DIR, *original_rel_path.split('/'))

    if not os.path.exists(original_full_path):
        continue

    with Image.open(original_full_path) as img:
        w, h = img.size
        if min(w, h) == TARGET_SHORT_SIDE and original_full_path.lower().endswith('.webp'):
            continue

        new_size = (TARGET_SHORT_SIDE, int(h * TARGET_SHORT_SIDE / w)) if w < h else (int(w * TARGET_SHORT_SIDE / h), TARGET_SHORT_SIDE)
        resized_img = img.resize(new_size, Image.LANCZOS)

        new_rel_path = os.path.splitext(original_rel_path)[0] + '.webp'
        new_full_path = os.path.join(BASE_DIR, *new_rel_path.split('/'))

        os.makedirs(os.path.dirname(new_full_path), exist_ok=True)
        resized_img.save(new_full_path, 'WEBP', quality=90)
        asset['path'] = new_rel_path

        if original_full_path.lower() != new_full_path.lower():
            os.remove(original_full_path)

with open(ASSETS_JSON_PATH, 'w', encoding='utf-8') as f:
    json.dump(assets, f, indent=4)