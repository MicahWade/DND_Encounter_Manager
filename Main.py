import Encounter
import Database
import os
from flask import *
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

env_path = os.path.join(os.path.dirname(__file__), '.env')
secret_key = None
if os.path.exists(env_path):
    with open(env_path, 'r') as f:
        for line in f:
            if line.startswith('FLASK_SECRET_KEY='):
                secret_key = line.strip().split('=', 1)[1]
                break
if not secret_key:
    raise RuntimeError(".env file missing FLASK_SECRET_KEY or file not found")
app.secret_key = secret_key

@app.route("/")
def mainPage():
    return render_template("home.html")

@app.route("/enemy/<name>")
def enemy(name):
    if 'userid' not in session:
        return redirect(url_for('login'))
    server = Database.Database(False)

    enemy = server.GetEnemyName(name)
    print(enemy.weapons)
    return render_template("enemy.html", enemy=enemy)

@app.route("/enemys/remove/<name>")
def removeEnemy(name):
    if 'userid' not in session:
        return redirect(url_for('login'))
    server = Database.Database(False)
    server.RemoveEnemyName(name)
    return redirect(url_for('enemys'))

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
            weapon_type = request.form.get(f"weapon_{i}")
            weapon_name = request.form.get(f"weapon_name_{i}")
            weapon_attackModifier = request.form.get(f"weapon_attackModifier_{i}")
            weapon_damageDice = request.form.get(f"weapon_damageDice_{i}")
            weapon_DiceAmount = request.form.get(f"weapon_amount_{i}")
            weapon_properties = request.form.get(f"weapon_properties_{i}")
            weapon_damageDice = int(weapon_damageDice)
            weapon_attackModifier = int(weapon_attackModifier)
            weapon_DiceAmount = int(weapon_DiceAmount)
            weapon_type = int(weapon_type)
            # Create Weapon object
            try:
                if weapon_type == 0:
                    weapons.append(Encounter.Weapon(
                        name=weapon_name,
                        weaponType="",  # You may need to adjust this based on (1,1)properties,
                        properties=weapon_properties.split(", "),
                        attackModifier=weapon_attackModifier,
                        damageType="slashing",  # You may need to adjust this based on your input
                        damageDiceAmount=weapon_DiceAmount,
                        diceType=weapon_damageDice,
                        damageModifier=0
                    ))
                elif weapon_type > 0 and weapon_type <= 33:
                    weapons.append(weapon_type)
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
        server = Database.Database(False)
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
    print(weapon)
    if request.method == "GET":
        try:
            weapon_id = request.args.get("weapon")
            server = Database.Database(False)
            weapon = server.GetWeapon(int(weapon_id))
            if weapon is None:
                return "Not found", 404
            print(weapon)
            print(weapon.JsonDetails())
            return jsonify(weapon.JsonDetails())
        except:
            return "Not found", 404
    else: 
        return "Error Wrong type of request", 405
# Responce Need to be a json
# { "redirect": "/dashboard" }
# Account Managment
@app.route("/login", methods=["GET", "POST"])
def login():
    if 'userid' in session:
        return redirect(url_for('mainPage'))
    if request.method == "POST":
        data = request.get_json()
        email = data["email"]
        password = data["password"]

        db = Database.Database(False)
        user = db.getUserByEmail(email)
        if user and check_password_hash(user['password'], password):
            session['userid'] = user['userid']
            session['email'] = email
            return redirect(url_for('mainPage'))
    elif request.method == "GET":
        return render_template("login.html")
    else:
        return "Wrong Method", 405

@app.route("/register", methods=["POST"])
def register():
    if 'userid' in session:
        return redirect(url_for('mainPage'))
    if request.method == "POST":
        db = Database.Database(False)
        data = request.get_json()
        
        email = data["email"]
        user = db.getUserByEmail(email)

        if user is None:
            return "Email Acount already exists.", 409

        hashed_pw = generate_password_hash(data["password"])
        fullname = data["firstname"] + " " + data["lastname"]
    
        userid = db.createUser(fullname, email, hashed_pw)
        session['userid'] = userid
        session['email'] = email
        return jsonify({ "redirect": "/" }), 200
    else:
        redirect(url_for("login"))

    

if __name__ == "__main__":
    server = Database.Database(True)
    app.run(debug=True, port=3333)
    app.add_url_rule(
        "/favicon.ico",
        endpoint="favicon",
        redirect_to=url_for("static", filename="favicon.ico"),
    )