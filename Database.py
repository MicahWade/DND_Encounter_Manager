import sqlite3
import os
import Encounter

class EncounterDatabase():
    server = "Temp Server"

    def CreateDefultWeapons(self):
        weapons = []
        weapons.append(Encounter.Weapon("Longsword", "Melee Weapon (simple)", ["Versatile",], 1, "Slashing", 1, 8, 0))
        weapons.append(Encounter.Weapon("Greatsword", "Melee Weapon (simple)", ["Two-Handed", "Heavy"], 1, "Slashing", 2, 6, 0))
        weapons.append(Encounter.Weapon("Shortsword", "Melee Weapon (simple)", ["Finesse", "Light"], 1, "Piercing", 1, 6, 0))
        weapons.append(Encounter.Weapon("Dagger", "Melee Weapon (simple)", ["Finesse", "Light", "Range", "Thrown"], 1, "Bludgeoning", 1, 4, 0))
        weapons.append(Encounter.Weapon("Light Crossbow", "Ranged Weapon (simple)", ["Two-Handed", "Range", "Loading", "Ammunition"], 1, "Piercing", 1, 8, 0))
        weapons.append(Encounter.Weapon("Club", "simple", ["light",], 1, "Bludgeoning", 1, 4, 0))

        for weapon in weapons:
            self.AddWeapon(weapon)

    def SetupTables(self):
        if self.server == "Temp Server":
            raise "Server Not Setup yet"
            return
        cursor = self.server.cursor()

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS Encounters (
            EncounterID INTEGER PRIMARY KEY,
            Name TEXT,
            CR INTEGER
        )
        ''')
        # IDENTITY(1,1) PRIMARY KEY This increments the ID
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS Enemys (
            EnemyID INTEGER PRIMARY KEY,
            Name TEXT,
            Size TEXT,
            Health INTEGER,
            Speed INTEGER,
            CR INTEGER,
            STR INTEGER,
            DEX INTEGER,
            CON INTEGER,
            INT INTEGER,
            WIS INTEGER,
            CHA INTEGER
        )
        ''')
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS EncounterEnemys (
            EncounterID INTEGER,
            EnemyID INTEGER,
            FOREIGN KEY (EncounterID) REFERENCES Encounters(EncounterID)
            FOREIGN KEY (EnemyID) REFERENCES Enemys(EnemyID)
        )
        ''')
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS Players (
            EncounterID INTEGER PRIMARY KEY,
            Name TEXT
        )
        ''')
        cursor = self.server.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='Weapon'")
        result = cursor.fetchone()
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS Weapon(
            WeaponID INTEGER PRIMARY KEY,
            Name TEXT,
            WeaponType TEXT,
            Properties TEXT,
            AttackModifier INTEGER, 
            DamgeType TEXT,
            AmountOfDice INTEGER,
            Dice INTEGER,
            DamgeModifier INTEGER
        )
        ''')
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS EnemyWeapon(
            WeaponID INTEGER,
            EnemyID INTEGER,
            FOREIGN KEY (WeaponID) REFERENCES Weapon(WeaponID)
            FOREIGN KEY (EnemyID) REFERENCES Enemys(EnemyID)
        )
        ''')
        self.server.commit()
        if result is None:
            self.CreateDefultWeapons()

    def __init__(self, first):
        path = os.path.expanduser('~/Documents/Dnd_Encounter')
        if not os.path.exists(path):
            os.makedirs(path)
        try:
            self.server = sqlite3.connect(f"{path}/Encounter.db")
            if first:
                self.SetupTables()
        except Exception as e:
            print(f"Could Not Connect to server This is the Issue {e}")

    def AddEncounter(self, encounter):
        enemyDataBaseID = []
        for enemy in encounter.characters:
            # Only select EnemyID and Name, and use parameterized query
            dataBaseEnemy = self.server.execute("SELECT EnemyID, Name FROM Enemys WHERE Name = ?", (enemy.name,))
            dataBaseEnemyRow = dataBaseEnemy.fetchone()
            if dataBaseEnemyRow is not None:
                enemyDataBaseID.append(dataBaseEnemyRow[0])
            else:
                enemyDataBaseID.append(self.AddEnemy(enemy))
        # Checks that the encounter is not in the database already 
        dataBaseEncounter = self.server.execute("SELECT Name FROM Encounters WHERE Name = ?", (encounter.name,))
        if dataBaseEncounter.fetchone() is None:
            self.server.execute("INSERT INTO Encounters (Name, CR) VALUES (?, ?)", (encounter.name, encounter.CR))
            # Adds connection between Enemy and Encounters
            encounterID = self.server.execute("SELECT last_insert_rowid()").fetchone()[0]
            for enemyID in enemyDataBaseID:
                self.server.execute("INSERT INTO EncounterEnemys (EncounterID, EnemyID) VALUES (?, ?)", (encounterID, enemyID))
        else:
            raise Exception(f"DataBase Already Has Encounter {encounter.name}")
        self.server.commit()

    def AddWeapon(self, weapon, enemyID = None):
        params = (weapon.name, weapon.weaponType, ",".join(weapon.properties), weapon.attackModifier, weapon.damageType, weapon.damageDiceAmount, weapon.diceType, weapon.damageModifier) 
        cursor = self.server.execute("INSERT INTO Weapon (Name, WeaponType, Properties, AttackModifier, DamgeType, AmountOfDice, Dice, DamgeModifier) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", params)
        if(enemyID is not None):
            ID = self.server.execute("SELECT last_insert_rowid()").fetchone()[0]
            self.server.execute("INSERT INTO EnemyWeapon (WeaponID, EnemyID) VALUES (?, ?)", (ID, enemyID))
        self.server.commit()
            
    #TODO: Could be threaded in Future
    def AddEnemy(self, enemy):
        cursor = self.server.execute(f"INSERT INTO Enemys (Name, Size, Health, Speed, CR, STR, DEX, CON, INT, WIS, CHA) VALUES (\'{enemy.name}\', \'{enemy.size}\', {enemy.health}, {enemy.speed}, {enemy.CR}, {enemy.STR}, {enemy.DEX}, {enemy.CON}, {enemy.INT}, {enemy.WIS}, {enemy.CHA})")
        ID = cursor.lastrowid # My need to change so that it can 
        self.server.commit()
        for weapon in enemy.weapons:
            self.AddWeapon(ID, weapon)
        return ID

    def AddPlayer(self, Player):
        self.server.execute(f"INSERT INTO Players (Name) VALUES (\"{Player.name}\")")
        self.server.commit()

    def GetWeapon(self, ID):
        weaponDB = self.server.execute(f"SELECT * FROM Weapon WHERE WeaponID ='{ID}'")
        weaponClass = None
        for weapon in weaponDB:
            weaponClass = Encounter.Weapon(weapon[1], weapon[2], weapon[3], weapon[4], weapon[5], weapon[6], weapon[7], weapon[8])
        return weaponClass

    def GetWeapons(self, ID):
        weapons = []
        # Use JOIN to get all weapon fields for a given enemy
        weaponsDB = self.server.execute("""
            SELECT w.WeaponID, w.Name, w.WeaponType, w.Properties, w.AttackModifier, w.DamgeType, w.AmountOfDice, w.Dice, w.DamgeModifier
            FROM Weapon w
            INNER JOIN EnemyWeapon ew ON w.WeaponID = ew.WeaponID
            WHERE ew.EnemyID = ?
        """, (ID,))
        for weapon in weaponsDB:
            weapons.append(Encounter.Weapon(weapon[1], weapon[2], weapon[3], weapon[4], weapon[5], weapon[6], weapon[7], weapon[8]))        
        return weapons    

    def GetPlayers(self):
        players = []
        playersDB = self.server.execute("SELECT Name FROM Players")
        for player in playersDB:
            players.append(Encounter.Player(player[0]))
        return players

    def GetEncounters(self):
        encounters = []
        # Only select EncounterID and Name
        encountersDB = self.server.execute("SELECT EncounterID, Name FROM Encounters")
        for encounter in encountersDB:
            encounters.append([encounter[0], encounter[1]])
        return encounters

    def GetEnemyName(self, EnemyName):
        # Use JOIN to get enemy and their weapons in one go
        enemyDB = self.server.execute("""
            SELECT e.EnemyID, e.Name, e.Size, e.Health, e.Speed, e.CR, e.STR, e.DEX, e.CON, e.INT, e.WIS, e.CHA
            FROM Enemys e
            WHERE e.Name = ?
        """, (EnemyName,))
        enemyRow = enemyDB.fetchone()
        if enemyRow:
            weapon = self.GetWeapons(enemyRow[0])
            return Encounter.Enemy(enemyRow[1], enemyRow[2], enemyRow[3], enemyRow[4], enemyRow[5], enemyRow[6], enemyRow[7], enemyRow[8], enemyRow[9], enemyRow[10], enemyRow[11], weapon)
        return None

    def GetEnemy(self, EnemyID):
        # Use JOIN to get enemy by ID
        enemyDB = self.server.execute("""
            SELECT EnemyID, Name, Size, Health, Speed, CR, STR, DEX, CON, INT, WIS, CHA
            FROM Enemys
            WHERE EnemyID = ?
        """, (EnemyID,))
        enemyRow = enemyDB.fetchone()
        if enemyRow:
            enemyWeapons = self.GetWeapons(EnemyID)
            return Encounter.Enemy(enemyRow[1], enemyRow[2], enemyRow[3], enemyRow[4], enemyRow[5], enemyRow[6], enemyRow[7], enemyRow[8], enemyRow[9], enemyRow[10], enemyRow[11], enemyWeapons)
        return None

    def GetEncounter(self, EncounterID):
        # Get Enemys using JOIN, only select required columns
        enemysDB = self.server.execute("""
            SELECT e.EnemyID, e.Name, e.Size, e.Health, e.Speed, e.CR, e.STR, e.DEX, e.CON, e.INT, e.WIS, e.CHA
            FROM EncounterEnemys ee
            INNER JOIN Enemys e ON ee.EnemyID = e.EnemyID
            WHERE ee.EncounterID = ?
        """, (EncounterID,))
        enemys = []
        for enemyDB in enemysDB:
            weapons = self.GetWeapons(enemyDB[0])
            enemys.append(Encounter.Enemy(enemyDB[1], enemyDB[2], enemyDB[3], enemyDB[4], enemyDB[5], enemyDB[6], enemyDB[7], enemyDB[8], enemyDB[9], enemyDB[10], enemyDB[11], weapons))

        # Get Encounter, only select required columns
        encounterDB = self.server.execute("SELECT Name, CR FROM Encounters WHERE EncounterID = ?", (EncounterID,))
        encounterRow = encounterDB.fetchone()
        if encounterRow:
            return Encounter.Encounter(encounterRow[0], enemys, encounterRow[1])
        return None

    def RemovePlayer(self, player):
        self.server.execute(f"DELETE FROM Players WHERE {player.name}")
        self.server.commit()

    def RemoveEnemyName(self, name):
        enemyDB = self.server.execute(f"SELECT EnemyID FROM Enemys WHERE Name ='{name}'")
        self.server.execute(f"DELETE FROM Enemys WHERE Name='{name}'")
        for enemy in enemyDB:
            self.RemoveWeaponEnemyID(enemy[0])
        self.server.commit()
    
    def RemoveWeaponEnemyID(self, ID):
        self.server.execute(f"DELETE FROM EnemyWeapon WHERE EnemyID={ID}")
    
    def GetEnemys(self):
        try:
            enemysDB = self.server.execute(f"SELECT Name, CR  FROM Enemys")
            enemyList = []
            for enemyDB in enemysDB:
                enemyList.append([enemyDB[0], enemyDB[1]])
            return enemyList
        except Exception:
            return []