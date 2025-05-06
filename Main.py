import Encounter
import Database
import os
from flask import *

app = Flask(__name__)


@app.route("/")
def mainPage():
    return render_template("home.html")

@app.route("/enemy/<name>")
def enemy(name):
    server = Database.EncounterDatabase()

    enemy = server.GetEnemyName(name)
    print(enemy.weapons)
    return render_template("enemy.html", enemy=enemy)

@app.route("/enemys/remove/<name>")
def removeEnemy(name):
    server = Database.EncounterDatabase()
    server.RemoveEnemyName(name)
    return redirect(url_for('enemys'))

# TODO: Will need to find better soltion
@app.route("/enemys")
def enemys():
    server = Database.EncounterDatabase()
    enemys = server.GetEnemys()
    return render_template("enemys.html", items = enemys)

@app.route("/enemys/create", methods=["GET", "POST"])
def createEnemy():
    if request.method == "POST":
        name = request.form.get("name")
        hp = request.form.get("hp")
        CR = request.form.get("CR")
        # TODO: Check Size
        size = request.form.get("size")
        STR = request.form.get("STR")
        DEX = request.form.get("DEX")
        CON = request.form.get("CON")
        INT = request.form.get("INT")
        WIS = request.form.get("WIS")
        CHA = request.form.get("CHA")
        speed = request.form.get("speed")
        weaponAmount = request.form.get("weaponAmount")

        # weapon_name = request.form.get("weapon_name")
        # weapon_description = request.form.get("weapon_description")
        # weapon_attackModifier = request.form.get("weapon_attackModifier")
        # weapon_damageDice = request.form.get("weapon_damageDice")
        # weapon_amount = request.form.get("weapon_amount")
        # weapon_properties = request.form.get("weapon_properties")

        # Convert numeric fields to appropriate types
        try:
            hp = int(hp)
            CR = float(CR)
            STR = int(STR)
            DEX = int(DEX)
            CON = int(CON)
            INT = int(INT)
            WIS = int(WIS)
            CHA = int(CHA)
            speed = int(speed)
            weaponAmount = int(weaponAmount)
        except ValueError:
            return "Invalid data format"

        weapons = []


        for i in range(1, weaponAmount+1):
            weapon_name = request.form.get(f"weapon_name_{i}")
            weapon_description = request.form.get(f"weapon_description_{i}")
            weapon_attackModifier = request.form.get(f"weapon_attackModifier_{i}")
            weapon_damageDice = request.form.get(f"weapon_damageDice_{i}")
            weapon_DiceAmount = request.form.get(f"weapon_amount_{i}")
            weapon_properties = request.form.get(f"weapon_properties_{i}")
            print(weapon_damageDice)
            weapon_damageDice = int(weapon_damageDice)
            weapon_attackModifier = int(weapon_attackModifier)
            weapon_DiceAmount = int(weapon_DiceAmount)
            # Create Weapon object
            try:
                weapons.append(Encounter.Weapon(
                    name=weapon_name,
                    description=weapon_description,
                    weaponType="",  # You may need to adjust this based on (1,1)properties,
                    properties=weapon_properties.split(","),
                    attackModifier=weapon_attackModifier,
                    damageType="slashing",  # You may need to adjust this based on your input
                    damageDiceAmount=weapon_DiceAmount,
                    diceType=weapon_damageDice,
                    damageModifier=0
                ))
            except ValueError:
                print("Invalid data format")

        # Create Enemy object
        enemy = Encounter.Enemy(
            name=name,
            size=size,
            health=hp,
            speed=speed,
            CR=CR,
            STR=STR,
            DEX=DEX,
            CON=CON,
            INT=INT,
            WIS=WIS,
            CHA=CHA,
            weapon=weapons
        )

        # Add enemy to the database
        server = Database.EncounterDatabase()
        server.AddEnemy(enemy)

        # Redirect to the enemies list page
        return redirect(url_for('enemys'))
    else:
        return render_template("enemysCreate.html")

@app.route("/encounter")
def encounter():
    return render_template("encounter.html")
@app.route("/settings")
def settings():
    return render_template("settings.html")

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),'favicon.ico', mimetype='image/vnd.microsoft.icon')

if __name__ == "__main__":
    app.run(debug=True, port=3333)
    app.add_url_rule(
    "/favicon.ico",
    endpoint="favicon",
    redirect_to=url_for("static", filename="favicon.ico"),
    )
# Encounter.EncounterMenu()