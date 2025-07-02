import json
from pathlib import Path
import ollama
from PIL import Image  # Add this import

# Set your base directory relative to the script
BASE_DIR = (Path(__file__).parent / "../static").resolve()

# Load assets from JSON
with open('assets.json', 'r') as f:
    assets = json.load(f)

# User selection: one or many
choice = input("Process (o)ne asset or (a)ll? [o/a]: ").strip().lower()
if choice == 'o':
    for idx, asset in enumerate(assets):
        print(f"{idx}: {asset['title']}")
    idx = int(input("Enter index of asset to process: "))
    assets_to_process = [assets[idx]]
else:
    assets_to_process = assets

def ensure_supported_image(image_path):
    """Convert .webp images to .png for compatibility with Ollama."""
    if image_path.suffix.lower() == ".webp":
        png_path = image_path.with_suffix(".png")
        if not png_path.exists():
            try:
                with Image.open(image_path) as im:
                    im.save(png_path)
                print(f"Converted {image_path} to {png_path}")
            except Exception as e:
                print(f"Failed to convert {image_path}: {e}")
                return image_path  # fallback to original
        return png_path
    return image_path

def generate_tags(image_path, model='llava'):
    # Use the Ollama Python library to send the image and prompt
    prompt = "List 5-10 relevant, concise, single-word tags for this image, separated by commas. Do not provide a description or use D&D-specific terms."
    try:
        response = ollama.chat(
            model=model,
            messages=[
                {
                    'role': 'user',
                    'content': prompt,
                    'images': [str(image_path)]
                }
            ]
        )
        # Extract the response content
        return response['message']['content']
    except Exception as e:
        print(f"Error processing {image_path}: {e}")
        return ""

for asset in assets_to_process:
    image_path = (BASE_DIR / asset['path']).resolve()
    image_path = ensure_supported_image(image_path)
    print(f"Processing: {asset['title']} ({image_path})")
    tags_caption = generate_tags(image_path)
    print(tags_caption)
    # Append new tags to the existing Tags field
    if tags_caption:
        # Remove leading/trailing whitespace and ensure comma separation
        asset['Tags'] = f"{asset['Tags'].strip()},{tags_caption.strip()}"
    else:
        # If no tags generated, keep the original
        asset['Tags'] = asset['Tags'].strip()

# Save updated assets.json
with open('assets.json', 'w') as f:
    json.dump(assets, f, indent=4)
print("Done.")