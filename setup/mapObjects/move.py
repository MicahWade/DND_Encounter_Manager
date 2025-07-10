import json
from typing import Dict, List, Any

def adjustCoordinates(filePath: str) -> None:
    try:
        with open(filePath, 'r') as file:
            data = json.load(file)

        # Adjust x and y values
        for mapKey in data:
            for entity in data[mapKey]:
                if 'x' in entity:
                    entity['x'] -= 1
                if 'y' in entity:
                    entity['y'] -= 1

        # Write updated data back to file
        with open(filePath, 'w') as file:
            json.dump(data, file, indent=2)

    except Exception as e:
        print(f"Error processing file: {e}")

adjustCoordinates("mapEntities.json")