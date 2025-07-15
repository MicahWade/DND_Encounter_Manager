import json
import os
from PIL import Image, ImageDraw, ImageFont, ImageTk
import tkinter as tk
from tkinter import messagebox

def extract_base_path(path: str) -> str:
    parts = path.split(" - ")
    if len(parts) >= 3:
        return " - ".join(parts[:2] + parts[3:])
    return path  # fallback if format is unexpected

def read_asset_json(file_path: str) -> dict:
    if not os.path.exists(file_path):
        save_asset_json(file_path, {})
    with open(file_path, 'r') as file:
        return json.load(file)

def save_asset_json(file_path: str, data: dict):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)

def get_user_input():
    print("What would you like to add? (or type 'remove' to delete an entity) or 'trap'")
    print("Options: assets, entity, entry, level down, level up (or type 'exit' to finish) or 'remove' or 'trap'")
    user_input = input().strip().lower()

    if user_input == 'entity':
        faction = input("Enter the faction for the entity (e.g., red team): ")
        return {'type': 'entity', 'faction': faction}
    elif user_input == 'remove':
        return {'type': 'remove'}
    elif user_input == 'trap':
        return {'type': 'trap'}  # New option for fall trap
    elif user_input in ['assets', 'entry', 'level down', 'level up']:
        return {'type': user_input}
    elif user_input == 'exit':
        return None
    else:
        print("Invalid option. Please try again.")
        return get_user_input()

def display_image_with_grid(image_path: str, map_data: dict):
    background = Image.open('../static/' + image_path).convert('RGBA')
    draw = ImageDraw.Draw(background)
    width, height = [int(x) for x in map_data['size'].split('x')]

    overlay = Image.new('RGBA', (background.width, background.height), (0, 0, 0, 0))
    draw_overlay = ImageDraw.Draw(overlay)

    line_width = 5
    grid_color = (0, 0, 0, int(255 * 0.75))

    for i in range(width + 1):
        line_x = i * (background.width // width)
        draw_overlay.line([(line_x, 0), (line_x, background.height)], fill=grid_color, width=line_width)

    for i in range(height + 1):
        line_y = i * (background.height // height)
        draw_overlay.line([(0, line_y), (background.width, line_y)], fill=grid_color, width=line_width)

    result_image = Image.alpha_composite(background.convert('RGBA'), overlay)
    return result_image, width, height, map_data

def draw_grid_and_text(canvas, cell_width, cell_height, width, height):
    # Removed canvas.delete("all") to prevent deleting the image
    for i in range(width + 1):
        x1, y1, x2, y2 = i * cell_width, 0, i * cell_width, height * cell_height
        canvas.create_line(x1, y1, x2, y2, fill='black', width=5)
    for i in range(height + 1):
        x1, y1, x2, y2 = 0, i * cell_height, width * cell_width, i * cell_height
        canvas.create_line(x1, y1, x2, y2, fill='black', width=5)

def on_right_click(event, canvas, cell_width, cell_height, width, height, selected_cells):
    box_number = (event.y // cell_height) * width + (event.x // cell_width)
    box_y = (box_number // width) + 1
    box_x = (box_number % width) + 1
    if (box_x, box_y) in selected_cells:
        selected_cells.remove((box_x, box_y))
        print(f"Removed cell ({box_x}, {box_y})")
    else:
        selected_cells.append((box_x, box_y))
        print(f"Added cell ({box_x}, {box_y})")
    draw_grid_and_text(canvas, cell_width, cell_height, width, height)
    for x, y in selected_cells:
        cell_x = (x - 1) * cell_width
        cell_y = (y - 1) * cell_height
        canvas.create_rectangle(cell_x, cell_y, cell_x + cell_width, cell_y + cell_height, outline="red", width=2)

def on_canvas_click(event, cell_width, cell_height, width, map_data):
    box_number = (event.y // cell_height) * width + (event.x // cell_width)
    print(f"Box number clicked: {box_number}")
    handle_user_input(map_data, box_number, width)

def handle_user_input(map_data, box_number, width):
    adding = True
    while adding:
        new_object = get_user_input()
        if new_object is None:
            print("Exiting...")
            break

        mapEntities_file_path = 'mapEntities.json'
        entities = read_asset_json(mapEntities_file_path)

        if map_data['path'] not in entities and not new_object['type'] == 'remove':
            entities[map_data['path']] = []

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
        elif new_object['type'] == 'remove':  # New condition for 'remove'
            mapassets = read_asset_json('assets.json')
            os.remove(f'../static/{map_data['path']}')
            mapassets = [item for item in mapassets if item['path'] != map_data['path']]
            save_asset_json('assets.json', mapassets)
        elif new_object['type'] == 'trap':  # New condition for fall trap
            entities[map_data['path']].append({
                "x": box_x,
                "y": box_y,
                "type": new_object['type']
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

def ObjectAddind():
    assets = read_asset_json('assets.json')
    for asset in assets:
        if asset['type'] == 'map':
            try:
                result_image, width, height, map_data = display_image_with_grid(asset['path'], asset)
                mapEntities_file_path = 'mapEntities.json'
                try:
                    entities = read_asset_json(mapEntities_file_path)
                except json.JSONDecodeError:
                    entities = {}

                if map_data['path'] in entities:
                    print(f"Image {asset['path']} already processed. Skipping...")
                    continue

                current_base_path = extract_base_path(map_data['path'])
                for existing_path, existing_objects in list(entities.items()):
                    existing_base_path = extract_base_path(existing_path)
                    if existing_base_path == current_base_path and existing_path != map_data['path']:
                        if map_data['path'] not in entities:
                            entities[map_data['path']] = []
                        entities[map_data['path']].extend(existing_objects)

                save_asset_json(mapEntities_file_path, entities)
                if map_data['path'] in entities:
                    print(f"Image {asset['path']} variant coppied. Skipping...")
                    continue

                print(map_data['path'])

                root = tk.Tk()
                root.title("Image Grid")

                cell_width = result_image.width // width
                cell_height = result_image.height // height

                canvas = tk.Canvas(root, width=result_image.width, height=result_image.height)

                scrollbar_x = tk.Scrollbar(root, orient=tk.HORIZONTAL, command=canvas.xview)
                scrollbar_y = tk.Scrollbar(root, orient=tk.VERTICAL, command=canvas.yview)

                canvas.configure(xscrollcommand=scrollbar_x.set, yscrollcommand=scrollbar_y.set)

                canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
                scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)
                scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)
                selected_cells = []

                def apply_attribute(selected_cells):

                    if map_data['path'] not in entities:
                        entities[map_data['path']] = []

                    print("Enter attribute to apply (hidden, lava, aid):")
                    attribute = input().strip().lower()

                    if attribute == "entity":
                        faction = input("Enter the faction for the entity (e.g., red team): ")
                        for x, y in selected_cells:
                            entities[map_data['path']].append({
                                "x": x,
                                "y": y,
                                "type": attribute,
                                "faction": faction
                            })
                            print(f"Applied '{attribute}' to cell ({x}, {y})")
                    else:
                        for x, y in selected_cells:
                            entities[map_data['path']].append({
                                "x": x,
                                "y": y,
                                "type": attribute
                            })
                            print(f"Applied '{attribute}' to cell ({x}, {y})")
                    
                    selected_cells = []

                    save_asset_json(mapEntities_file_path, entities)
                    print("Changes saved to mapEntities.json")

                    draw_grid_and_text(canvas, cell_width, cell_height, width, height)
                    for x, y in selected_cells:
                        cell_x = (x - 1) * cell_width
                        cell_y = (y - 1) * cell_height
                        canvas.create_rectangle(cell_x, cell_y, cell_x + cell_width, cell_y + cell_height, outline="red", width=2)

                # Bind key press to root window to ensure focus
                def on_key(event):
                    if event.char == 'a':
                        apply_attribute(selected_cells)

                root.bind('<KeyPress>', on_key)

                # Create the image and draw grid
                photo = ImageTk.PhotoImage(result_image)
                draw_grid_and_text(canvas, cell_width, cell_height, width, height)
                canvas.create_image(0, 0, anchor=tk.NW, image=photo)

                # Bind mouse events
                canvas.bind('<Button-1>', lambda e: on_canvas_click(e, cell_width, cell_height, width, map_data))
                canvas.bind('<Button-3>', lambda e: on_right_click(e, canvas, cell_width, cell_height, width, height, selected_cells))

                canvas.config(scrollregion=canvas.bbox("all"))

                root.mainloop()
            except (ValueError, KeyError) as e:
                print(f"Error displaying grid or image for {asset.get('title', 'Unknown')}: {e}")

def levelFloors():
    assets = read_asset_json('../assets.json')
    floor_data = {}

    for asset in assets:
        if asset['type'] == 'map' and ('floor' in asset['path'].lower() or 'cellar' in asset['path'].lower()):
            base_path = extract_base_path(asset['path'])
            if base_path not in floor_data:
                floor_data[base_path] = []
            floor_data[base_path].append({
                "path": asset['path'],
                "size": int(asset['size'].split('x')[0])
            })

    for base_path, floors in floor_data.items():
        size_set = {floor['size'] for floor in floors}
        if len(size_set) != len(floors):
            print(f"Some floors have the same size. Skipping pop-up.")
            continue

        # If all sizes are different, create a new window with floor images
        root = tk.Tk()
        root.title("Floor Images")

        for floor in floors:
            image_path = '../../static/' + floor['path']
            try:
                img = Image.open(image_path).resize((200, 200), Image.LANCZOS)
                photo = ImageTk.PhotoImage(img)

                def apply_attribute(floor):
                    selected_cells = []
                    print(f"Select cells for {floor['path']}. Press 'a' to apply attribute or any other key to skip.")
                    
                    def on_key(event):
                        if event.char == 'a':
                            apply_attribute(selected_cells)
                        else:
                            root.destroy()

                    root.bind('<KeyPress>', on_key)

                    def click_callback(event, selected_cells):
                        box_number = (event.y // 20) * 10 + (event.x // 20)
                        box_y = (box_number // 10) + 1
                        box_x = (box_number % 10) + 1
                        if (box_x, box_y) in selected_cells:
                            selected_cells.remove((box_x, box_y))
                            print(f"Removed cell ({box_x}, {box_y})")
                        else:
                            selected_cells.append((box_x, box_y))
                            print(f"Added cell ({box_x}, {box_y})")

                    canvas = tk.Canvas(root, width=200, height=200)
                    canvas.pack()
                    
                    for i in range(10):
                        for j in range(10):
                            x1, y1, x2, y2 = i * 20, j * 20, (i + 1) * 20, (j + 1) * 20
                            canvas.create_rectangle(x1, y1, x2, y2, outline="black")
                            canvas.tag_bind(f"rect_{i}_{j}", '<Button-1>', lambda event: click_callback(event, selected_cells))
                            canvas.addtag_withtag(f"rect_{i}_{j}", f"box_{i}_{j}")
                        
                    root.mainloop()

                button = tk.Button(root, image=photo, command=lambda floor=floor: apply_attribute(floor), compound=tk.CENTER)
                button.image = photo
                button.pack(side=tk.LEFT, padx=10, pady=10)

            except Exception as e:
                print(f"Error loading {image_path}: {e}")

def main():
    popups = True
    print("Enter Object or level for Getting Level")
    while popups:
        data = input() 
        if data != None:
            popups = False
            if data == "Object":
                ObjectAddind()
            if data == "level":
                levelFloors()


if __name__ == "__main__":
    main()