import Encounter
import Database
from flask import *

app = Flask(__name__)


@app.route("/")
def mainPage():
    return render_template("home.html")

@app.route("/enemy/<name>")
def enemy(name):
    server = Database.EncounterDatabase()

    enemy = server.GetEnemyName(name)
    return render_template("enemy.html", enemy=enemy)

# TODO: Will need to find better soltion
@app.route("/enemys")
def enemys():
    server = Database.EncounterDatabase()
    enemys = server.GetEnemys()
    return render_template("enemys.html", items = enemys)

@app.route("/enemys/create", methods=["GET", "POST"])
def createEnemy():
    if request.method == "POST":
        try:
            # Get form data
            name = request.form.get("name")
            hp = int(request.form.get("hp"))
            initiativeModifier = int(request.form.get("initiativeModifier"))
            CR = float(request.form.get("CR"))
            STR = int(request.form.get("STR"))
            DEX = int(request.form.get("DEX"))
            CON = int(request.form.get("CON"))
            speed = int(request.form.get("speed"))
            weapon_name = request.form.get("weapon1_name")
            weapon_description = request.form.get("weapon1_description")
            weapon_attackModifier = int(request.form.get("weapon1_attackModifier"))
            weapon_damageDice = request.form.get("weapon1_damageDice")
            
            if not all([name, hp, initiativeModifier, CR, STR, DEX, CON, speed, weapon_name]):
                return "Missing required data", 400
            
            # Parse weapon damage dice (e.g., "2d6+3 slashing")
            if " " in weapon_damageDice:
                damage_part = weapon_damageDice.split()[0]
                damage_type = weapon_damageDice.split()[1]
            else:
                damage_part = weapon_damageDice
                damage_type = "bludgeoning"
            
            if "+" in damage_part:
                dice, damageModifier = damage_part.split("+")
                damageModifier = int(damageModifier)
            else:
                dice = damage_part
                damageModifier = 0
            
            # Extract dice type
            if "d" in dice:
                diceAmount, diceType = dice.split("d")
                diceAmount = int(diceAmount)
                diceType = int(diceType)
            else:
                diceAmount = 1
                diceType = 4
            
            # Create weapon properties
            properties = []
            if weapon_description:
                properties = weapon_description.split(',')
            
            # Create weapon object
            weapon = Weapon(
                name=weapon_name,
                description=weapon_description,
                weaponType=" melee",  # You can modify this based on weapon type
                properties=properties,
                attackModifier=weapon_attackModifier,
                damageType=damage_type,
                damageDiceAmount=diceAmount,
                diceType=diceType,
                damageModifier=damageModifier
            )
            
            # Create enemy object
            enemy = Enemy(
                
                name=name,
                size="Medium",  # Add logic to select size based on input if needed
                heath=hp,
                speed=speed,
                CR=CR,
                STR=STR,
                DEX=DEX,
                CON=CON,
                INT=10,  # Add fields for INT, WIS, CHA in the form if needed
                WIS=10,
                CHA=10,
                weapon=[weapon]
            )
            
            # Save enemy to database
            server = Database.EncounterDatabase()
            server.AddEnemy(enemy)
            
            return redirect(url_for('enemys'))
        except ValueError:
            return "Invalid input format", 400
        except CastError:
            return "Invalid data type conversion", 400
        except Exception as e:
            print(f"Error creating enemy: {e}")
            return "An error occurred while creating the enemy", 500
    else:
        return render_template("enemysCreate.html")

@app.route("/encounter")
def encounter():
    return render_template("encounter.html")
@app.route("/settings")
def settings():
    return render_template("settings.html")

if __name__ == "__main__":
    app.run(debug=True, port=3333)


# Encounter.EncounterMenu()