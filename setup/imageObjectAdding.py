import json
from PIL import Image, ImageDraw, ImageFont, ImageTk
import tkinter as tk
import os

def read_asset_json(file_path: str) -> dict:
    if not os.path.exists(file_path):
        save_asset_json(file_path, {})
    with open(file_path, 'r') as file:
        return json.load(file)

def save_asset_json(file_path: str, data: dict):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)

def get_user_input():
    print("What would you like to add?")
    print("Options: assets, entity, player entry, level down, level up (or type 'exit' to finish)")
    user_input = input().strip().lower()

    if user_input == 'entity':
        faction = input("Enter the faction for the entity (e.g., red team): ")
        return {'type': 'entity', 'faction': faction}
    elif user_input in ['assets', 'player entry', 'level down', 'level up']:
        return {'type': user_input}
    elif user_input == 'exit':
        return None
    else:
        print("Invalid option. Please try again.")
        return get_user_input()

def display_image_with_grid(image_path: str, map_data: dict):
    # Load the background image
    background = Image.open('../static/' + image_path).convert('RGBA')
    draw = ImageDraw.Draw(background)
    width, height = [int(x) for x in map_data['size'].split('x')]

    # Create a transparent overlay image
    overlay = Image.new('RGBA', (background.width, background.height), (0, 0, 0, 0))
    draw_overlay = ImageDraw.Draw(overlay)

    line_width = 5
    grid_color = (0, 0, 0, int(255 * 0.75))  # RGBA values for black with 75% opacity
    text_color = (204, 204, 204, int(255 * 0.75))  # RGBA values for lightgrey with 75% opacity

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

    return result_image, width, height, map_data

def on_canvas_click(event, canvas, cell_width, cell_height, width, map_data):
    box_number = (event.y // cell_height) * width + (event.x // cell_width)
    print(f"Box number clicked: {box_number}")
    
    # Pass the 'width' parameter to handle_user_input
    handle_user_input(canvas, cell_width, cell_height, map_data, box_number, width)

def handle_user_input(canvas, cell_width, cell_height, map_data, box_number, width):
    adding = True
    while adding:
        new_object = get_user_input()
        if new_object is None:
            print("Exiting...")
            break

        mapEntities_file_path = 'mapEntities.json'
        entities = read_asset_json(mapEntities_file_path)

        if map_data['path'] not in entities:
            entities[map_data['path']] = []

        # Use the correct 'width' to compute x and y
        box_y = (box_number // width) + 1
        box_x = (box_number % width) + 1

        if new_object['type'] == 'entity':
            entities[map_data['path']].append({
                "x": box_x,
                "y": box_y,
                "type": new_object['type'],
                "faction": new_object.get('faction', None)
            })
            adding = False
        else:
            entities[map_data['path']].append({
                "x": box_x,
                "y": box_y,
                "type": new_object['type']
            })
            adding = False

        save_asset_json(mapEntities_file_path, entities)

def main():
    assets = read_asset_json('assets.json')
    for asset in assets:
        if asset['type'] == 'map':
            try:
                result_image, width, height, map_data = display_image_with_grid(asset['path'], asset)
                
                # Check if the image path already exists in mapEntities
                mapEntities_file_path = 'mapEntities.json'
                # Initialize entities to an empty dictionary if the file is empty or invalid
                try:
                    entities = read_asset_json(mapEntities_file_path)
                except json.JSONDecodeError:
                    entities = {}

                if map_data['path'] in entities:
                    print(f"Image {asset['path']} already processed. Skipping...")
                    continue

                # Create a Tkinter window
                root = tk.Tk()
                root.title("Image Grid")

                global cell_width, cell_height
                cell_width = result_image.width // width
                cell_height = result_image.height // height

                # Create a canvas to display the image and bind click events
                canvas = tk.Canvas(root, width=result_image.width, height=result_image.height)
                canvas.pack()

                # Convert PIL Image to PhotoImage for Tkinter
                photo = ImageTk.PhotoImage(result_image)

                # Draw the grid on the canvas
                for i in range(width + 1):
                    x1, y1, x2, y2 = i * cell_width, 0, i * cell_width, result_image.height
                    canvas.create_line(x1, y1, x2, y2, fill='black', width=5)

                for i in range(height + 1):
                    x1, y1, x2, y2 = 0, i * cell_height, result_image.width, i * cell_height
                    canvas.create_line(x1, y1, x2, y2, fill='black', width=5)

                # Draw the numbers on the canvas
                for x in range(width):
                    for y in range(height):
                        cell_x1, cell_y1 = x * cell_width, y * cell_height
                        cell_x2, cell_y2 = (x + 1) * cell_width, (y + 1) * cell_height
                        text = f"{y * width + x}"

                        # Calculate the center position
                        text_x = cell_x1 + (cell_width // 2)
                        text_y = cell_y1 + (cell_height // 2)

                        canvas.create_text(text_x, text_y, text=text, fill='lightgrey')

                # Bind click event to the canvas
                canvas.bind('<Button-1>', lambda e: on_canvas_click(e, canvas, cell_width, cell_height, width, map_data))

                # Display the image on the canvas
                canvas.create_image(0, 0, anchor=tk.NW, image=photo)

                root.mainloop()
            except (ValueError, KeyError) as e:
                print(f"Error displaying grid or image for {asset.get('title', 'Unknown')}: {e}")

if __name__ == "__main__":
    main()