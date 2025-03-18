import Encounter
from flask import *

app = Flask(__name__)

@app.route("/")
def mainPage():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)

    
# Encounter.EncounterMenu()