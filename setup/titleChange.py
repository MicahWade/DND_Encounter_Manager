import json
from pathlib import Path
import ollama

BASE_DIR = (Path(__file__).parent / "../static").resolve()

with open('assets.json', 'r') as f:
    assets = json.load(f)

choice = input("Process (o)ne asset or (a)ll? [o/a]: ").strip().lower()
if choice == 'o':
    for idx, asset in enumerate(assets):
        print(f"{idx}: {asset['title']}")
    idx = int(input("Enter index of asset to process: "))
    assets_to_process = [assets[idx]]
else:
    assets_to_process = assets

def generate_title(current_title, model='llama3'):
    prompt = (
        "Rewrite the following title to be a concise, descriptive title using 2-4 words. "
        "Do not use D&D-specific terms or punctuation. Only return the new title.\n\n"
        f"Original title: {current_title}"
    )
    try:
        response = ollama.chat(
            model=model,
            messages=[
                {
                    'role': 'user',
                    'content': prompt
                }
            ]
        )
        return response['message']['content'].strip()
    except Exception as e:
        print(f"Error processing '{current_title}': {e}")
        return ""

for asset in assets_to_process:
    current_title = asset['title']
    # Only process if asset is a map
    if asset.get('type', '').lower() == 'map':
        print(f"Processing: {current_title}")
        new_title = generate_title(current_title)
        print(f"Suggested title: {new_title}")
        if new_title:
            asset['title'] = new_title
    else:
        print(f"Skipping (not a map): {current_title}")

with open('assets.json', 'w') as f:
    json.dump(assets, f, indent=4)
print("Done.")