import sqlite3

class EncounterDatabase():
    server = sqlite3.connect('Encounter.db')
    