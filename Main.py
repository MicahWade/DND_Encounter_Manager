import Encounter
import Database
import os
from flask import *
from werkzeug.security import generate_password_hash, check_password_hash
import user
from setup.mapObjects.mapEntitiesSQL import importMapEntities
from setup.sqlEnter import insert_assets_from_json
from dotenv import load_dotenv
from defults import create_default_weapons, create_default_enemys

app = Flask(__name__)

load_dotenv()

app.secret_key = os.environ.get("FLASK_SECRET_KEY")

@app.route("/")
def mainPage():
    return render_template("home.html")

@app.route("/enemy/<id>")
def enemy(id):
    if 'userid' not in session:
        return redirect(url_for('login'))
    server = Database.Database(False)
    enemy = server.GetEnemy(id)
    if enemy is None:
        return "Bad Enemy Id", 404
    return render_template("enemy.html", enemy=enemy)
# TODO: Make User ID
@app.route("/enemys/remove/<name>", methods=["GET"])
def removeEnemy(name):
    if 'userid' not in session:
        return redirect(url_for('login'))
    server = Database.Database(False)
    server.RemoveEnemyName(name)
    return redirect(url_for('enemys'))

@app.route("/search/enemy/<term>", methods=["GET"])
def searchEnemys(term):
    server = Database.Database(False)
    results = server.searchEnemys(term)
    return jsonify({'enemys': results})

@app.route("/map/floor/get/<path:path>")
def getFloor(path):
    server = Database.Database(False)
    results = server.GetFloors(path)
    return jsonify(results)

@app.route("/enemys")
def enemys():
    if 'userid' not in session:
        return redirect(url_for('login'))
    server = Database.Database(False)
    enemys = server.GetEnemys()
    return render_template("enemys.html", items = enemys)

@app.route("/enemys/create", methods=["GET", "POST"])
def createEnemy():
    if 'userid' not in session:
        return redirect(url_for('login'))
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
        # New fields
        type_ = request.form.get("type")
        alignment = request.form.get("alignment")
        languages = request.form.get("languages")
        skills = request.form.get("skills")
        saving_throws = request.form.get("saving_throws")
        senses = request.form.get("senses")
        multiattack = request.form.get("multiattack")
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

        server = Database.Database(False)
        for i in range(1, weaponAmount+1):
            weapon_id = request.form.get(f"weapon_{i}")
            if(weapon_id == 0 or weapon_id == "0"):
                weapon_name = request.form.get(f"weapon_name_{i}")
                weapon_type = request.form.get(f"weapon_type_{i}")
                weapon_attackModifier = request.form.get(f"weapon_attackModifier_{i}")
                weapon_damageType = request.form.get(f"weapon_damageType_{i}")
                weapon_damageDice = request.form.get(f"weapon_damageDice_{i}")
                weapon_DiceAmount = request.form.get(f"weapon_amount_{i}")
                weapon_properties = request.form.get(f"weapon_properties_{i}")
                # Check for missing fields
                if (
                    weapon_name is None or weapon_name == "" or
                    weapon_type is None or weapon_type == "" or
                    weapon_attackModifier is None or weapon_attackModifier == "" or
                    weapon_damageType is None or weapon_damageType == "" or
                    weapon_damageDice is None or weapon_damageDice == "" or
                    weapon_DiceAmount is None or weapon_DiceAmount == "" or
                    weapon_properties is None
                ):
                    print(f"Weapon {i} fields missing or invalid!")
                    return "Weapon fields missing or invalid", 400
                try:
                    weapon_damageDice = int(weapon_damageDice)
                    weapon_attackModifier = int(weapon_attackModifier)
                    weapon_DiceAmount = int(weapon_DiceAmount)
                    weapons.append(Encounter.Weapon(
                        weapon_name,
                        weapon_type,
                        weapon_properties.split(','),
                        weapon_attackModifier,
                        weapon_damageType,
                        weapon_DiceAmount,
                        weapon_damageDice,
                        weapon_attackModifier
                    ))
                except ValueError:
                    print("Invalid data format")
            else:
                weapons.append(server.GetWeapon(weapon_id))
        # Create Enemy object
        enemy = Encounter.Enemy(
            id = 0,
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
            weapon=weapons,
            type=type_,
            alignment=alignment,
            languages=languages,
            skills=skills,
            saving_throws=saving_throws,
            senses=senses,
            multiattack=multiattack
        )
        # Add enemy to the database
        server.AddEnemy(enemy)

        # Redirect to the enemies list page
        return redirect(url_for('enemys'))
    else:
        return render_template("enemysCreate.html")

@app.route("/encounter")
def encounter():
    if 'userid' not in session:
        return redirect(url_for('login'))
    return render_template("encounter.html")

@app.route("/encounter/create")
def encounterCreate():
    if 'userid' not in session:
        return redirect(url_for('login'))
    return render_template("encounterCreate.html")

@app.route("/map/search/<term>", methods=["GET"])
def searchMap(term):
    server = Database.Database(False)
    results = server.searchMap(term)
    return results

@app.route("/map/get/<title>")
def getMap(title):
    server = Database.Database(False)
    result = server.GetMap(title)
    if result is None:
        return jsonify({"error": "Map not found"}), 404
    # result is (Path, Variants, Size)
    return jsonify({
        "image_path": result[0],
        "variants": result[1],
        "size": result[2],
        "floor": result[3]
    })

@app.route("/settings")
def settings():
    if 'userid' not in session:
        return redirect(url_for('login'))
    return render_template("settings.html")

@app.route("/weapon/get", methods=["GET"])
def getWeaponInfo():
    if 'userid' not in session:
        return redirect(url_for('login'))
    server = Database.Database(False)
    weapon = server.GetWeapon(0)
    if request.method == "GET":
        try:
            weapon_id = request.args.get("weapon")
            server = Database.Database(False)
            weapon = server.GetWeapon(int(weapon_id))
            if weapon is None:
                return "Not found", 404
            return jsonify(weapon.JsonDetails())
        except:
            return "Not found", 404
    else: 
        return "Error Wrong type of request", 405
# Responce Need to be a json
# { "redirect": "/dashboard" }
# Account Managment
@app.route("/login", methods=["GET", "PUT"])
def login():
    if 'userid' in session:
        return redirect(url_for('mainPage'))
    if request.method == "PUT":
        data = request.get_json()
        email = data["email"]
        password = data["password"]

        db = Database.Database(False)
        user = db.getUserByEmail(email)
        if user and check_password_hash(user['password'], password):
            session['userid'] = user['userid']
            session['email'] = email
            return jsonify({ "redirect": "/" }), 200
        else:
            return jsonify({"Email or Password where Incorect"})
    elif request.method == "GET":
        return render_template("login.html")
    else:
        return jsonify({"Email or Password where Incorect"}), 405

@app.route("/register", methods=["POST", "PUT" ])
def register():
    if 'userid' in session:
        return redirect(url_for('mainPage'))
    if request.method == "POST":
        if request.is_json:
            db = Database.Database(False)
            data = request.get_json()
            # Only check email, firstname, lastname for POST (email uniqueness check)
            check_data = {
                "firstname": data.get("firstname", ""),
                "lastname": data.get("lastname", ""),
                "email": data.get("email", ""),
                "password": data.get("password", "")
            }
            valid, error = user.validate_registration(check_data)
            if not valid:
                return jsonify({"unique": False, "error": error}), 400

            user_obj = db.getUserByEmail(data.get("email", ""))
            resp = { "unique": user_obj is None }
            return jsonify(resp)
        else:
            return redirect(url_for('login'))
    if request.method == "PUT":
        db = Database.Database(False)
        data = request.get_json()
        # Validate all fields for full registration
        valid, error = user.validate_registration(data)
        if not valid:
            return error, 400

        email = data.get("email", "")
        user_obj = db.getUserByEmail(email)
        if user_obj is not None:
            return "Email Acount already exists.", 409

        hashed_pw = generate_password_hash(data.get("password", ""))
        fullname = data.get("firstname", "") + " " + data.get("lastname", "")
    
        userid = db.createUser(fullname, email, hashed_pw)
        session['userid'] = userid
        session['email'] = email
        return jsonify({ "redirect": "/" }), 200
    else:
        redirect(url_for("login"))

@app.route("/map/objects/get/<path:path>", methods=["GET"])
def mapObjects(path):
    db = Database.Database(False)
    mapObjects = db.GetMapObjects(path)
    print()
    return jsonify(mapObjects)

# Error Handling
@app.errorhandler(405)
def method_not_allowed(error):
    return jsonify({'error': 'Method not allowed'}), 405

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Resource not found'}), 404

if __name__ == "__main__":
    server = Database.Database(True)
    if server.wasfirst:
        insert_assets_from_json(server)
        importMapEntities(server)
        create_default_enemys()
        create_default_weapons()
    app.run(debug=True, port=3333)
    app.add_url_rule(
        "/favicon.ico",
        endpoint="favicon",
        redirect_to=url_for("static", filename="favicon.ico"),
    )