import json
import sqlite3
import Database

def importMapEntities(db: Database.Database) -> None:
    conn = db.server
    try:
        with open('setup/mapEntities.json', 'r') as f:
            map_data = json.load(f)
        
        cursor = conn.cursor()
        for map_path, entities in map_data.items():
            # Get MapID from Maps table using the path
            cursor.execute("SELECT MapID FROM Maps WHERE Path = ?", (map_path,))
            map_id_row = cursor.fetchone()
            
            if not map_id_row:
                continue  # Skip if no matching map found
                
            map_id = map_id_row[0]
            
            # Insert entities for this map
            for entity in entities:
                x = entity['x']
                y = entity['y']
                entity_type = entity['type']
                faction = entity.get('faction')  # Optional field
                
                cursor.execute("""
                    INSERT INTO MapObject 
                    (MapID, Xcoordinate, Ycoordinate, Type, Faction)
                    VALUES (?, ?, ?, ?, ?)
                """, (map_id, x, y, entity_type, faction))
            conn.commit()
        
    
    except Exception as e:
        print(f"Error importing map entities: {e}")