import os
from PIL import Image

Image.MAX_IMAGE_PIXELS = None

SOURCE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../static/images'))
THUMB_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../static/thumbnails'))
THUMB_SIZE = (180, 180)

def crop_center_square(img):
    w, h = img.size
    min_dim = min(w, h)
    left = (w - min_dim) // 2
    top = (h - min_dim) // 2
    right = left + min_dim
    bottom = top + min_dim
    return img.crop((left, top, right, bottom))

for root, _, files in os.walk(SOURCE_DIR):
    for filename in files:
        if not filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif', '.tiff')):
            continue
        rel_dir = os.path.relpath(root, SOURCE_DIR)
        thumb_dir = os.path.join(THUMB_DIR, rel_dir)
        os.makedirs(thumb_dir, exist_ok=True)
        thumb_name = os.path.splitext(filename)[0] + '.webp'
        thumb_path = os.path.join(thumb_dir, thumb_name)
        if os.path.exists(thumb_path):
            continue
        img_path = os.path.join(root, filename)
        with Image.open(img_path) as img:
            img = crop_center_square(img)
            img = img.resize(THUMB_SIZE, Image.LANCZOS)
            img.save(thumb_path, 'WEBP')