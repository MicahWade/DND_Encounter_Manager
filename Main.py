import Encounter
from flask import *

app = Flask(__name__)

@app.route("/")
def mainPage():
    return render_template("index.html")
@app.route("/enemys")
def ememys():
    return render_template("enemys.html")

@app.route("/nav.html")
def nav():
    return render_template("nav.html")

if __name__ == "__main__":
    app.run(debug=True, port=3333)


# Encounter.EncounterMenu()