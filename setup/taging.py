import json
import os
from PIL import Image
import torch
import deepdanbooru as dd
import numpy as np

# Setup
device = "cuda" if torch.cuda.is_available() else "cpu"

defultWordList = ["location", 'map', "dungeon"]

# Simulated tag generation function
def generate_tags(image_path, min_tags=5, max_tags=15):


    # Path to your DeepDanbooru model directory
    model_path = 'deepdanbooru-v4-20200814-sgd-e30/model-resnet_custom_v4.h5'

    # Load model
    model = dd.project.load_model_from_project(model_path, compile_model=True)

    # Load tags
    with open(os.path.join(model_path, 'tags.txt'), 'r', encoding='utf-8') as f:
        tags = [tag.strip() for tag in f.readlines()]

    # Load and preprocess image
    image = Image.open(image_path).convert('RGB')
    image = image.resize((512, 512))
    image_array = np.array(image).astype(np.float32) / 255.0
    image_array = np.expand_dims(image_array, 0)

    # Predict
    predictions = model.predict(image_array)[0]

    # Get top tags
    tag_confidence = list(zip(tags, predictions))
    tag_confidence.sort(key=lambda x: x[1], reverse=True)
    selected_tags = [tag for tag, conf in tag_confidence if conf > 0.5][:max_tags]

    return selected_tags

# Function to process images
def process_images(assets, process_all=True, index=0):
    results = []
    parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../static'))
    if process_all:
        for asset in assets:
            try:
                image_path = os.path.join(parent_dir, asset['path'])
                with Image.open(image_path) as img:
                    img.verify()  # Verify that the file is a valid image
            except Exception as e:
                print(f"Error opening image {image_path}: {e}")
                continue
            new_tags = generate_tags(image_path)
            results.append({'title': asset['title'], 'new_tags': new_tags})
    else:
        asset = assets[index]
        try:
            image_path = os.path.join(parent_dir, asset['path'])
            with Image.open(image_path) as img:
                img.verify()
        except Exception as e:
            print(f"Error opening image {image_path}: {e}")
            return []
        new_tags = generate_tags(image_path)
        results.append({'title': asset['title'], 'new_tags': new_tags})
    return results

# Main script
if __name__ == "__main__":
    # Load assets.json
    with open('assets.json', 'r') as file:
        assets = json.load(file)

    # Toggle: set process_all to True for all images, False for one image (by index)
    process_all = False  # Set to False to process a single image
    index = 0           # Index of the image to process if process_all is False


    results = process_images(assets, process_all=process_all, index=index)
    for result in results:
        print(f"Title: {result['title']}")
        print(f"Generated Tags: {result['new_tags']}")
        print()
