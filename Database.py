import sqlite3
import os
import Encounter

class EncounterDatabase():
    server = "Temp Server"

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
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS Weapon(
            WeaponID INTEGER PRIMARY KEY,
            Name TEXT,
            Description TEXT,
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

    def __init__(self):
        path = os.path.expanduser('~/Documents/Dnd_Encounter')
        if not os.path.exists(path):
            os.makedirs(path)
        try:
            self.server = sqlite3.connect(f"{path}/Encounter.db")
            self.SetupTables()
        except Exception as e:
            print(f"Could Not Connect to server This is the Issue {e}")

    def AddEncounter(self, encounter):
        enemyDataBaseID = []
        for enemy in encounter.characters:
            dataBaseEnemy = self.server.execute(f"SELECT EnemyID, Name FROM Enemys WHERE {enemy.name}")
            print(dataBaseEnemy) # Should be a list
            if dataBaseEnemy is not None:
                enemyDataBaseID.append(dataBaseEnemy[0])
            else:
                enemyDataBaseID.append(self.AddEnemy(enemy))
        # Checks that the encounter is not in the database allready 
        dataBaseEncounter = self.server.execute(f"SELECT Name FROM Encounters WHERE {encounter.name}")
        if dataBaseEncounter is None:
            self.server.execute(f"INSERT INTO Encounters (Name, CR) VALUES (\"{encounter.name}\",{encounter.CR})")
            # Adds connection between Enemy and Encounters
            encounterID =  self.server.lastrowid()
            for enemyID in enemyDataBaseID:
                self.server.execute(f"INSERT INTO EncounterEnemys (EncounterID, EnemyID) VALUES ({encounterID}, {enemyID})")
        else:
            raise f"DataBase Allready Has Encounter {encounter.name}"
        self.server.commit()

    def AddWeapons(self, enemyID, weapon):
        params = (weapon.name, weapon.description, weapon.weaponType, ",".join(weapon.properties), weapon.attackModifier, weapon.damageType, weapon.damageDiceAmount, weapon.diceType, weapon.damageModifier) 
        cursor = self.server.execute(f"INSERT INTO WEAPON VALUES (NULL, ?, ?, ?, ?, ?, ?, ?, ?, ?)", params)
        ID = cursor.lastrowid
        cursor.execute(f"INSERT INTO EnemyWeapon (WeaponID, EnemyID) VALUES ({ID}, {enemyID})")
        self.server.commit()
            
    #TODO: Could be threaded in Future
    def AddEnemy(self, enemy):
        cursor = self.server.execute(f"INSERT INTO Enemys (Name, Size, Health, Speed, CR, STR, DEX, CON, INT, WIS, CHA) VALUES (\'{enemy.name}\', \'{enemy.size}\', {enemy.health}, {enemy.speed}, {enemy.CR}, {enemy.STR}, {enemy.DEX}, {enemy.CON}, {enemy.INT}, {enemy.WIS}, {enemy.CHA})")
        ID = cursor.lastrowid # My need to change so that it can 
        print(ID)
        self.server.commit()
        for weapon in enemy.weapons:
            self.AddWeapons(ID, weapon)
        return ID

    def AddPlayer(self, Player):
        self.server.execute(f"INSERT INTO Players (Name) VALUES (\"{Player.name}\")")
        self.server.commit()

    def GetWeapon(self, ID):
        weaponDB = self.server.execute(f"SELECT * FROM Weapon WHERE WeaponID ='{ID}'")
        for weapon in weaponDB:
            weaponClass = Encounter.Weapon(weapon[1], weapon[2], weapon[3], weapon[4].split(','), weapon[5], weapon[6], weapon[7], weapon[8], weapon[9])
        return weaponClass

    def GetWeapons(self, ID):
        weapons = []
        weaponsDB = self.server.execute(f"SELECT WeaponID FROM EnemyWeapon WHERE EnemyID ='{ID}'")
        for weaponID in weaponsDB:
            weapons.append(self.GetWeapon(weaponID[0]))        
        return weapons    

    def GetPlayers(self):
        players = []
        playersDB = self.server.execute(f"SELECT * FROM Players")
        for player in playersDB:
            players.append(Encounter.Player(player[1]))
        
        return players

    def GetEncounters(self):
        encounters = []
        encountersDB = self.server.execute("SELECT ID, EncounterID FROM Encounters")
        for encounter in encountersDB:
            encounters.append([encounter[0][0], encounter[0][1]])

    def GetEnemyName(self, EnemyName):
        enemyDB = self.server.execute(f"SELECT EnemyID, Name, Size, Health, Speed, CR, STR, DEX, CON, INT, WIS, CHA FROM Enemys WHERE Name ='{EnemyName}'")
        name = ""
        health = 0
        speed = 0
        CR = 0
        STR = 0
        DEX = 0
        CON = 0
        INT = 0
        WIS = 0
        CHA = 0
        weapon = []


        for enemy in enemyDB:
            weapon = self.GetWeapons(enemy[0])
            name = enemy[1]
            size = enemy [2]
            health = enemy[3]
            speed = enemy[4]
            CR = enemy[5]
            STR = enemy[6]
            DEX = enemy[7]
            CON = enemy[8]
            INT = enemy[9]
            WIS = enemy[10]
            CHA = enemy[11]
            
        return Encounter.Enemy(name, size, health, speed, CR, STR, DEX, CON, INT, WIS, CHA, weapon)

    def GetEnemy(self, EnemyID):
        enemyDB = self.server.execute(f"SELECT * FROM Enemys WHERE {EnemyID}")
        enemyWeapons = self.GetWeapons(EnemyID)
        return Encounter.Enemy(enemyDB[0][1], enemyDB[0][2], enemyDB[0][3], enemyDB[0][4], enemyDB[0][5], enemyDB[0][6], enemyDB[0][7], enemyDB[0][8], enemyDB[0][9], enemyDB[0][10], enemyDB[0][11], enemyWeapons)

    def GetEncounter(self, EncounterID):
        # Get Enemys
        enemysDB = self.server.execute(f"""
        SELECT Enemys.*
        FROM Encounters
        INNER JOIN EncounterEnemys ON Encounters.EncounterID = EncounterEnemys.EncounterID
        INNER JOIN Enemys ON EncounterEnemys.EnemyID = Enemys.EnemyID
        WHERE Encounters.EncounterID = {EncounterID};
        """)
        enemys = []
        for enemyDB in enemysDB:
            enemys.append(Encounter.Enemy(enemyDB[1], enemyDB[2], enemyDB[3], enemyDB[4]))

        # Get Encounter
        encounterDB = self.server.execute(f"SELECT * FROM Encounter WHERE {EncounterID}")
        encounter = Encounter.Encounter(encounterDB[0][1], enemys, encounterDB[0][2])
    
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