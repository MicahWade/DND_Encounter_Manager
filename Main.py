import Encounter
import Database
from flask import *

app = Flask(__name__)


@app.route("/")
def mainPage():
    return render_template("index.html")
    
# TODO: Will need to find better soltion
@app.route("/enemys")
def enemys():
    server = Database.EncounterDatabase()
    enemys = server.GetEnemys()
    return render_template("enemys.html", items = enemys)

@app.route("/enemys/create", methods=["GET", "POST"])
def createEnemy():
    if request.method == "POST":
        server = Database.EncounterDatabase()
        name = request.form.get("name")
        hp = request.form.get("hp")
        initiativeModifier = request.form.get("initiativeModifier")
        CR = request.form.get("CR")
        if name and hp and CR and initiativeModifier:
            enemy = Encounter.Enemy(name, hp, initiativeModifier, CR)
            server.AddEnemy(enemy)
            
            return redirect(url_for('enemys'))
        else:
            return "Missing data"
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