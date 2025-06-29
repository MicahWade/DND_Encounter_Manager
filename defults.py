import os
import json
import Encounter
import Database

def create_default_weapons():
    # Read weapon data from JSON file
    db_instance = Database.Database(False)
    static_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static", "data")
    json_path = os.path.join(static_dir, "weapons.json")
    if not os.path.exists(json_path):
        print("Error Now weapon.json file in static/data/")
    else:
        with open(json_path, "r", encoding="utf-8") as f:
            weapon_data = json.load(f)
        weapons = []
        for weapon in weapon_data:
            weapons.append(
                Encounter.Weapon(
                    weapon["name"],
                    weapon["type"],
                    weapon["properties"],
                    weapon["attackModifier"],
                    weapon["damageType"],
                    weapon["amountOfDice"],
                    weapon["dice"],
                    weapon["damageModifier"]
                )
            )
        for weapon in weapons:
            db_instance.AddWeapon(weapon)

def create_default_enemys():
    db_instance = Database.Database(False)
    static_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static", "data")
    json_path = os.path.join(static_dir, "monsters.json")
    if not os.path.exists(json_path):
        print("Error: No monsters.json file in static/data/")
        return
    with open(json_path, "r", encoding="utf-8") as f:
        monsters = json.load(f)
    for monster in monsters:
        # Collect special abilities but do not use them for now
        special_abilities = monster.get("special_abilities", [])
        # Map JSON fields to Enemy fields, with defaults for missing fields
        name = monster.get("name", "")
        size = monster.get("size", "")
        health = monster.get("hit_points", 0)
        speed = 0
        speed_str = monster.get("speed", "")
        # Try to extract the first number from speed string
        if isinstance(speed_str, str):
            import re
            match = re.search(r"(\d+)", speed_str)
            if match:
                speed = int(match.group(1))
        CR = monster.get("challenge_rating", 0)
        try:
            CR = float(CR)
        except Exception:
            CR = 0
        STR = monster.get("strength", 0)
        DEX = monster.get("dexterity", 0)
        CON = monster.get("constitution", 0)
        INT = monster.get("intelligence", 0)
        WIS = monster.get("wisdom", 0)
        CHA = monster.get("charisma", 0)
        type_ = monster.get("type", "")
        alignment = monster.get("alignment", "")
        languages = monster.get("languages", "")
        skills = []
        # Collect all skill fields (e.g., "perception": 4)
        for k, v in monster.items():
            if k in [
                "acrobatics", "animal_handling", "arcana", "athletics", "deception", "history", "insight",
                "intimidation", "investigation", "medicine", "nature", "perception", "performance", "persuasion",
                "religion", "sleight_of_hand", "stealth", "survival"
            ] and isinstance(v, (int, float)):
                skills.append(f"{k.replace('_', ' ').title()} +{v}")
        skills_str = ", ".join(skills)
        # Saving throws
        saving_throws = []
        for k in ["strength_save", "dexterity_save", "constitution_save", "intelligence_save", "wisdom_save", "charisma_save"]:
            if k in monster and isinstance(monster[k], (int, float)):
                short = k.split("_")[0].upper()
                saving_throws.append(f"{short} +{monster[k]}")
        saving_throws_str = ", ".join(saving_throws)
        senses = monster.get("senses", "")
        multiattack = ""
        # Weapons from actions and legendary_actions
        weapons = []
        # Helper to parse action into a Weapon
        def action_to_weapon(action, is_legendary=False):
            name = action.get("name", "Unknown Action")
            # Try to extract damage info if present
            # Fallbacks if not present
            attack_mod = 0
            damage_type = ""
            damage_dice_amount = 1
            dice_type = 6
            damage_modifier = 0
            properties = []
            # Try to parse damage from action description
            desc = action.get("desc", "")
            import re
            # Example: "Melee Weapon Attack: +7 to hit, reach 5 ft., one target. Hit: 15 (2d8 + 6) slashing damage."
            match = re.search(r"(\d+)d(\d+)(?:\s*\+\s*(\d+))?\)?\s*(\w+)? damage", desc)
            if match:
                damage_dice_amount = int(match.group(1))
                dice_type = int(match.group(2))
                if match.group(3):
                    damage_modifier = int(match.group(3))
                if match.group(4):
                    damage_type = match.group(4).capitalize()
            # Try to get attack modifier
            match2 = re.search(r"\+(\d+) to hit", desc)
            if match2:
                attack_mod = int(match2.group(1))
            # If legendary, add property
            if is_legendary:
                properties.append("Legendary")
            # Try to guess weapon type
            weapon_type = "Melee" if "melee" in desc.lower() else "Ranged" if "ranged" in desc.lower() else "Special"
            return Encounter.Weapon(
                name=name,
                weaponType=weapon_type,
                properties=properties,
                attackModifier=attack_mod,
                damageType=damage_type,
                damageDiceAmount=damage_dice_amount,
                diceType=dice_type,
                damageModifier=damage_modifier,
                weaponid=None
            )
        # Parse normal actions
        for action in monster.get("actions", []):
            if action['name'] == "Multiattack":
                multiattack = action['desc'].replace("(", "").replace(")", "")
            else:
                weapons.append(action_to_weapon(action, is_legendary=False))
        # Parse legendary actions
        for action in monster.get("legendary_actions", []):
            weapons.append(action_to_weapon(action, is_legendary=True))
        # Create and add the enemy
        enemy = Encounter.Enemy(
            id=0,
            name=name,
            size=size,
            health=health,
            speed=speed,
            CR=CR,
            STR=STR,
            DEX=DEX,
            CON=CON,
            INT=INT,
            WIS=WIS,
            CHA=CHA,
            weapon=weapons,
            type=type_,
            alignment=alignment,
            languages=languages,
            skills=skills_str,
            saving_throws=saving_throws_str,
            senses=senses,
            multiattack=multiattack
        )
        db_instance.AddEnemy(enemy)