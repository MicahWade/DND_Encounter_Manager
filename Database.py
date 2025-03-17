import sqlite3
import os

class EncounterDatabase():

    server = "Temp Server"

    def SetupTables(self):
        if self.server == "Temp Server":
            raise "Server Not Setup yet"
            return
        cursor = self.server.cursor()

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS Encounters (
            EncounterID INTEGER,
            Name TEXT,
            CR INTEGER
        )
        ''')
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS Enemys (
            EnemyID INTEGER,
            Name TEXT,
            Initiative INTEGER,
            CR INTEGER
        )
        ''')
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS EncounterEnemys (
            EncounterID INTEGER,
            EnemyID INTEGER,
            PRIMARY KEY (EncounterID, EnemyID),
            FOREIGN KEY (EncounterID) REFERENCES Encounters(EncounterID)
            FOREIGN KEY (EnemyID) REFERENCES Enemys(EnemyID)
        )
        ''')


    def __init__(self):
        path = os.path.expanduser('~/Documents/Dnd_Encounter')
        if not os.path.exists(path):
            os.makedirs(path)
        try:
            self.server = sqlite3.connect(f"{path}/Encounter.db")
            self.SetupTables()
        except Exception as e:
            print(f"Count Not Connect to server This is the Issue {e}")




test = EncounterDatabase()
