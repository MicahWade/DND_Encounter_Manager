import json
import os

def insert_assets_from_json(db, json_path="setup/assets.json"):
    # Check if all relevant tables are empty
    tables = ["Asset", "Maps", "EnemyToken", "PlayerToken"]
    is_empty = True
    for table in tables:
        cursor = db.server.execute(f"SELECT COUNT(*) FROM {table}")
        count = cursor.fetchone()[0]
        if count > 0:
            is_empty = False
            break

    if not is_empty:
        print("Database already contains asset/map/token data. Skipping import.")
        return

    with open(json_path, "r", encoding="utf-8") as f:
        assets = json.load(f)

    for entry in assets:
        entry_type = entry.get("type", "").lower()
        title = entry.get("title", "")
        path = entry.get("path", "")
        size = entry.get("size", "")
        variants = entry.get("variants", "")
        tags = entry.get("Tags", "")
        tag_list = [t.strip() for t in tags.replace('"', '').replace("'", '').replace("\n", ",").split(",") if t.strip()]

        if entry_type == "map":
            cursor = db.server.execute(
                "INSERT INTO Maps (Title, Path, Variants, Size) VALUES (?, ?, ?, ?)",
                (title, path, variants, size)
            )
            map_id = cursor.lastrowid
            for tag in tag_list:
                db.server.execute(
                    "INSERT INTO MapTags (MapID, Tag) VALUES (?, ?)",
                    (map_id, tag)
                )
        elif entry_type == "asset":
            cursor = db.server.execute(
                "INSERT INTO Asset (Title, Path, Size) VALUES (?, ?, ?)",
                (title, path, size)
            )
            asset_id = cursor.lastrowid
            for tag in tag_list:
                db.server.execute(
                    "INSERT INTO AssetTag (AssetID, Tag) VALUES (?, ?)",
                    (asset_id, tag)
                )
        elif entry_type == "enemy":
            cursor = db.server.execute(
                "INSERT INTO EnemyToken (Title, Path, Size) VALUES (?, ?, ?)",
                (title, path, size)
            )
            enemy_id = cursor.lastrowid
            for tag in tag_list:
                db.server.execute(
                    "INSERT INTO EnemyTag (EnemyID, Tag) VALUES (?, ?)",
                    (enemy_id, tag)
                )
        elif entry_type == "player":
            cursor = db.server.execute(
                "INSERT INTO PlayerToken (Title, Path, Size) VALUES (?, ?, ?)",
                (title, path, size)
            )
            player_id = cursor.lastrowid
            for tag in tag_list:
                db.server.execute(
                    "INSERT INTO PlayerTag (PlayerID, Tag) VALUES (?, ?)",
                    (player_id, tag)
                )
        else:
            print(entry_type)
        db.server.commit()