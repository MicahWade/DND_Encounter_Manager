import Encounter
from flask import *

app = Flask(__name__)

@app.route("/")
def mainPage():
    return render_template("index.html")
@app.route("/enemys")
def ememys():
    return render_template("enemys.html")

@app.route("/encounter")
def nav():
    return render_template("encounter.html")
@app.route("/settings")
def nav():
    return render_template("settings.html")

if __name__ == "__main__":
    app.run(debug=True, port=3333)


# Encounter.EncounterMenu()