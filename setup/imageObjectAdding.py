import json
from PIL import Image, ImageDraw, ImageFont
import matplotlib.pyplot as plt

def read_asset_json(file_path: str) -> list:
    with open(file_path, 'r') as file:
        return json.load(file)

def display_image_with_grid(image_path: str, map_data: dict):
    # Load the background image
    background = Image.open('../static/' + image_path).convert('RGBA')
    draw = ImageDraw.Draw(background)
    width, height = [int(x) for x in map_data['size'].split('x')]

    # Create a transparent overlay image
    overlay = Image.new('RGBA', (background.width, background.height), (0, 0, 0, 0))
    draw_overlay = ImageDraw.Draw(overlay)
    line_width = 5
    grid_color = 'black'
    text_color = 'lightgrey'

    # Draw grid on the overlay
    for i in range(width + 1):
        line_x = i * (background.width // width)
        draw_overlay.line([(line_x, 0), (line_x, background.height)], fill=grid_color, width=line_width)

    for i in range(height + 1):
        line_y = i * (background.height // height)
        draw_overlay.line([(0, line_y), (background.width, line_y)], fill=grid_color, width=line_width)

    # Draw numbers on the overlay
    font_size = 50
    font = ImageFont.truetype('arial.ttf', font_size)  # You may need to specify the path to a TrueType font file

    for x in range(width):
        for y in range(height):
            cell_width = background.width // width
            cell_height = background.height // height
            text = f"{y * width + x}"
            text_bbox = draw_overlay.textbbox((0, 0), text, font=font)
            text_width = text_bbox[2] - text_bbox[0]
            text_height = text_bbox[3] - text_bbox[1]

            # Calculate the center position
            text_x = x * cell_width + (cell_width - text_width) // 2
            text_y = y * cell_height + (cell_height - text_height) // 2

            draw_overlay.text((text_x, text_y), text, fill=text_color, font=font)

    # Merge the background and overlay images
    result_image = Image.alpha_composite(background.convert('RGBA'), overlay)

    # Display image
    plt.imshow(result_image)
    plt.axis('off')
    plt.show()

def main():
    assets = read_asset_json('assets.json')
    for asset in assets:
        if asset['type'] == 'map':
            try:
                display_image_with_grid(asset['path'], asset)
            except (ValueError, KeyError) as e:
                print(f"Error displaying grid or image for {asset.get('title', 'Unknown')}: {e}")

if __name__ == "__main__":
    main()