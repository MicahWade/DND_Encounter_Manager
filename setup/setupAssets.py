import os
import sys
import json
import shutil
import zipfile
import re

DOWNLOADS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), './downloads'))
STATIC_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../static'))
ASSETS_JSON_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), 'assets.json'))

def log_and_exit(msg):
    print(msg)
    sys.exit(1)

def ensure_dir(path):
    os.makedirs(path, exist_ok=True)

def load_assets_json():
    if os.path.exists(ASSETS_JSON_PATH):
        with open(ASSETS_JSON_PATH, 'r', encoding='utf-8') as f:
            try:
                return json.load(f)
            except Exception:
                return []
    return []

def save_assets_json(data):
    with open(ASSETS_JSON_PATH, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4)

def asset_exists(assets_json, path):
    return any(entry['path'] == path for entry in assets_json)

def parse_size_from_name(name):
    match = re.search(r'(\d+)x(\d+)', name)
    if match:
        return f"{match.group(1)}x{match.group(2)}"
    return ""

def parse_variants(names):
    variants = set()
    for name in names:
        for v in ['Night', 'Day', 'Light', 'Dark']:
            if v.lower() in name.lower():
                variants.add(v)
    return ', '.join(sorted(variants)) if variants else "None"

def get_title_from_filename(filename):
    # Try to extract a title like "Chest3" from "Chest (1x1) 3.png"
    # Remove extension first
    name = os.path.splitext(filename)[0]
    # Remove size in brackets and trailing numbers
    name = re.sub(r'\(\d+x\d+\)', '', name)
    name = name.strip()
    # If there is a trailing number, attach it to the title
    match = re.match(r'(.+?)\s*(\d*)$', name)
    if match:
        return (match.group(1).replace(' ', '') + (match.group(2) if match.group(2) else '')).strip()
    return name

def process_zip(zip_path, assets_json):
    zip_name = os.path.splitext(os.path.basename(zip_path))[0]
    try:
        with zipfile.ZipFile(zip_path, 'r') as z:
            members = z.namelist()
            extracted_dir = os.path.splitext(zip_path)[0]
            if not os.path.exists(extracted_dir):
                z.extractall(extracted_dir)
    except Exception as e:
        log_and_exit(f"Failed to extract {zip_path}: {e}")

    def find_dirs(pattern):
        return [os.path.join(extracted_dir, d) for d in os.listdir(extracted_dir) if pattern in d]

    # Assets (300 DPI)
    for asset_dir in find_dirs('Assets (300 DPI)'):
        for root, _, files in os.walk(asset_dir):
            for file in files:
                # Group floors together
                if 'floor' in file.lower():
                    dst_dir = os.path.join(STATIC_DIR, 'images', 'assets', 'floors')
                else:
                    dst_dir = os.path.join(STATIC_DIR, 'images', 'assets')
                ensure_dir(dst_dir)
                dst = os.path.join(dst_dir, file)
                rel_dst = os.path.relpath(dst, STATIC_DIR).replace("\\", "/")
                if os.path.exists(dst) or asset_exists(assets_json, rel_dst):
                    continue
                src = os.path.join(root, file)
                size = parse_size_from_name(file)
                title = get_title_from_filename(file)
                shutil.copy2(src, dst)
                assets_json.append({
                    "title": title,
                    "type": "asset",
                    "Tags": zip_name,
                    "path": rel_dst,
                    "variants": "None",
                    "size": size or ""
                })

    # Maps - 300 DPI (Print)
    for map_dir in find_dirs('Maps - 300 DPI'):
        map_files = []
        for root, _, files in os.walk(map_dir):
            for file in files:
                map_files.append((root, file))
        # Group by base name for variants
        base_names = {}
        for root, file in map_files:
            # Remove variant keywords for base
            base = re.sub(r' - (Night|Day|Light|Dark).*', '', file, flags=re.IGNORECASE)
            base_names.setdefault(base, []).append((root, file))
        for base, variants in base_names.items():
            variant_names = [file for _, file in variants]
            variant_str = parse_variants(variant_names)
            size = parse_size_from_name(base)
            # If only one variant, do not use a subfolder
            if len(variants) == 1:
                root, file = variants[0]
                # Group floors together
                if 'floor' in file.lower():
                    dst_dir = os.path.join(STATIC_DIR, 'images', 'maps', 'floors')
                else:
                    dst_dir = os.path.join(STATIC_DIR, 'images', 'maps')
                ensure_dir(dst_dir)
                dst = os.path.join(dst_dir, file)
                rel_dst = os.path.relpath(dst, STATIC_DIR).replace("\\", "/")
                if os.path.exists(dst) or asset_exists(assets_json, rel_dst):
                    continue
                src = os.path.join(root, file)
                shutil.copy2(src, dst)
                assets_json.append({
                    "title": get_title_from_filename(file),
                    "type": "map",
                    "Tags": zip_name,
                    "path": rel_dst,
                    "variants": variant_str,
                    "size": size or parse_size_from_name(file) or ""
                })
            else:
                # Multiple variants: use a subfolder
                subfolder = re.sub(r'[^a-zA-Z0-9_]', '_', base)
                # Group floors together
                if 'floor' in base.lower():
                    dst_dir = os.path.join(STATIC_DIR, 'images', 'maps', 'floors')
                else:
                    dst_dir = os.path.join(STATIC_DIR, 'images', 'maps', subfolder)
                ensure_dir(dst_dir)
                for root, file in variants:
                    src = os.path.join(root, file)
                    dst = os.path.join(dst_dir, file)
                    rel_dst = os.path.relpath(dst, STATIC_DIR).replace("\\", "/")
                    if os.path.exists(dst) or asset_exists(assets_json, rel_dst):
                        continue
                    shutil.copy2(src, dst)
                    assets_json.append({
                        "title": get_title_from_filename(file),
                        "type": "map",
                        "Tags": zip_name,
                        "path": rel_dst,
                        "variants": variant_str,
                        "size": size or parse_size_from_name(file) or ""
                    })

    # Tokens
    for token_dir in find_dirs('Tokens'):
        is_hero = 'hero' in zip_name.lower()
        token_type = "player" if is_hero else "enemy"
        dst_dir = os.path.join(STATIC_DIR, 'images', 'tokens', 'hero' if is_hero else '')
        ensure_dir(dst_dir)
        for root, _, files in os.walk(token_dir):
            for file in files:
                src = os.path.join(root, file)
                dst = os.path.join(dst_dir, file)
                rel_dst = os.path.relpath(dst, STATIC_DIR).replace("\\", "/")
                if os.path.exists(dst) or asset_exists(assets_json, rel_dst):
                    continue
                shutil.copy2(src, dst)
                assets_json.append({
                    "title": get_title_from_filename(file),
                    "type": token_type,
                    "Tags": zip_name,
                    "path": rel_dst,
                    "variants": "None",
                    "size": parse_size_from_name(file) or ""
                })

    # Audio by RPG Audio Vault
    for audio_dir in find_dirs('Audio by RPG Audio Vault'):
        for root, dirs, files in os.walk(audio_dir):
            for file in files:
                src = os.path.join(root, file)
                ext = os.path.splitext(file)[1].lower()
                if ext == '.mp3':
                    dst_dir = os.path.join(STATIC_DIR, 'sound', 'Maps')
                elif ext == '.mp4':
                    dst_dir = os.path.join(STATIC_DIR, 'sound', 'Effects')
                else:
                    continue  # Only copy .mp3 or .mp4
                ensure_dir(dst_dir)
                dst = os.path.join(dst_dir, file)
                if os.path.exists(dst):
                    continue
                shutil.copy2(src, dst)
        # No JSON update for audio files

def main():
    if not os.path.isdir(DOWNLOADS_DIR):
        log_and_exit(f"Downloads directory not found: {DOWNLOADS_DIR}")

    zip_files = [f for f in os.listdir(DOWNLOADS_DIR) if f.lower().endswith('.zip')]
    if not zip_files:
        log_and_exit("No ZIP files found in downloads directory.")

    assets_json = load_assets_json()
    for zip_file in zip_files:
        zip_path = os.path.join(DOWNLOADS_DIR, zip_file)
        process_zip(zip_path, assets_json)

    save_assets_json(assets_json)
    print("Processing complete. Assets JSON updated.")

if __name__ == '__main__':
    main()
