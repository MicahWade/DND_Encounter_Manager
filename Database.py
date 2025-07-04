import sqlite3
import os
import Encounter

class Database():
    server = "Temp __server"
    wasfirst = False
    
    def __SetupTables(self):

        if self.server == "Temp __server":
            raise Exception("__server Not Setup yet")
        cursor = self.server.cursor()

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS Encounters (
            EncounterID INTEGER PRIMARY KEY,
            Name TEXT,
            CR INTEGER
        )
        ''')
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
            CHA INTEGER,
            Type TEXT,
            Alignment TEXT,
            Languages TEXT,
            Skills TEXT,
            SavingThrows TEXT,
            Senses TEXT,
            Multiattack TEXT
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
        CREATE TABLE IF NOT EXISTS MapTags (
            MapID INTEGER,
            Tag TEXT,
            FOREIGN KEY (MapID) REFERENCES Maps(MapID))
        ''')
        cursor.execute('''
        CREATE INDEX IF NOT EXISTS MapTagsIndex ON MapTags (Tag);
        ''')
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS Maps (
            MapID INTEGER PRIMARY KEY,
            Title TEXT,
            Path TEXT,
            Variants TEXT,
            Size TEXT
        )
        ''')
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS Floor (
            FloorNumber INTEGER,
            MapID INTEGER,
            FOREIGN KEY (MapID) REFERENCES Maps(MapID))
        ''')
        cursor.execute('''CREATE INDEX IF NOT EXISTS FloorMapID ON Floor (MapID)''')
        cursor.execute('''CREATE INDEX IF NOT EXISTS MapsTitle ON Maps (Title);''')
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS PlayerTag (
            PlayerID INTEGER,
            Tag TEXT,
            FOREIGN KEY (PlayerID) REFERENCES PlayerToken(PlayerID))
        ''')
        cursor.execute('''
        CREATE INDEX IF NOT EXISTS PlayerTagsIndex ON PlayerTag (Tag);
        ''')
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS PlayerToken (
            PlayerID INTEGER PRIMARY KEY,
            Title TEXT,
            Path TEXT,
            Size TEXT
        )
        ''')
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS EnemyTag (
            EnemyID INTEGER,
            Tag TEXT,
            FOREIGN KEY (EnemyID) REFERENCES EnemyToken(EnemyID))
        ''')
        cursor.execute('''
        CREATE INDEX IF NOT EXISTS EnemyTagsIndex ON EnemyTag (Tag);
        ''')
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS EnemyToken (
            EnemyID INTEGER PRIMARY KEY,
            Title TEXT,
            Path TEXT,
            Size TEXT
        )
        ''')
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS AssetTag (
            AssetID INTEGER,
            Tag TEXT,
            FOREIGN KEY (AssetID) REFERENCES Asset(AssetID))
        ''')
        cursor.execute('''CREATE INDEX IF NOT EXISTS AssetTagsIndex ON AssetTag (Tag);''')
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS Asset (
            AssetID INTEGER PRIMARY KEY,
            Title TEXT,
            Path TEXT,
            Size TEXT
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
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS User (
            UserID INTEGER PRIMARY KEY,
            FullName TEXT,
            Email TEXT UNIQUE,
            Password TEXT
        )''')
        cursor.execute('''
        CREATE INDEX IF NOT EXISTS NameEnemy 
        ON Enemys (Name); ''')
        self.server.commit()
        if result is None:
            self.wasfirst = True

    def __init__(self, first):
        path = os.path.expanduser('~/Documents/Dnd_Encounter')
        if not os.path.exists(path):
            os.makedirs(path)
        try:
            self.server = sqlite3.connect(f"{path}/Encounter.db")
        except Exception as e:
            print(f"Could Not Connect to __server This is the Issue {e}")
        if first:
            self.__SetupTables()




    #region Add
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
        weaponID = cursor.lastrowid
        if(enemyID is not None):
            self.server.execute("INSERT INTO EnemyWeapon (WeaponID, EnemyID) VALUES (?, ?)", (weaponID, enemyID))
        self.server.commit()

    def AddPremadeWeapon(self, weaponid, enemyID):
        self.server.execute("INSERT INTO EnemyWeapon (WeaponID, EnemyID) VALUES (?, ?)", (weaponid, enemyID))
        self.server.commit()
            
    #TODO: Could be threaded in Future
    def AddEnemy(self, enemy):
        # Insert with new fields
        cursor = self.server.execute(
            "INSERT INTO Enemys (Name, Size, Health, Speed, CR, STR, DEX, CON, INT, WIS, CHA, Type, Alignment, Languages, Skills, SavingThrows, Senses, Multiattack) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (
                enemy.name, enemy.size, enemy.health, enemy.speed, enemy.CR, enemy.STR, enemy.DEX, enemy.CON, enemy.INT, enemy.WIS, enemy.CHA,
                getattr(enemy, "type", ""), getattr(enemy, "alignment", ""), getattr(enemy, "languages", ""), getattr(enemy, "skills", ""), getattr(enemy, "saving_throws", ""), getattr(enemy, "senses", ""), getattr(enemy, "multiattack", "")
            )
        )
        enemyID = cursor.lastrowid
        self.server.commit()
        for weapon in enemy.weapons:
            if weapon.weaponid != None and weapon.weaponid != 0:
                self.AddPremadeWeapon(weapon.weaponid, enemyID)
            else: 
                self.AddWeapon(weapon, enemyID)
        return enemyID

    def AddPlayer(self, Player):
        self.server.execute(f"INSERT INTO Players (Name) VALUES (\"{Player.name}\")")
        self.server.commit()
    #endregion



    # region GET
    def GetWeapon(self, ID):
        weaponDB = self.server.execute(f"SELECT * FROM Weapon WHERE WeaponID ='{ID}'")
        weaponClass = None
        for weapon in weaponDB:
            weaponClass = Encounter.Weapon(weapon[1], weapon[2], weapon[3].split(","), weapon[4], weapon[5], weapon[6], weapon[7], weapon[8], weapon[0])
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
            weapons.append(Encounter.Weapon(weapon[1], weapon[2], weapon[3].split(","), weapon[4], weapon[5], weapon[6], weapon[7], weapon[8]))        
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
    def GetFloors(self, path):
        print(path)
        term = path.split("Floor")[0]
        print(f"term {term}")
        # Join Maps and Floor to get all floors for maps matching the path term
        floors = self.server.execute(
            """
            SELECT f.FloorNumber, m.Path, m.Size
            FROM Maps m
            JOIN Floor f ON m.MapID = f.MapID
            WHERE m.Path LIKE ?
            """,
            (f"{term}%",)
        ).fetchall()
        return floors


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
            return Encounter.Enemy(enemyRow[0], enemyRow[1], enemyRow[2], enemyRow[3], enemyRow[4], enemyRow[5], enemyRow[6], enemyRow[7], enemyRow[8], enemyRow[9], enemyRow[10], enemyRow[11], weapon)
        return None

    def GetEnemy(self, EnemyID):
        # Use JOIN to get enemy by ID
        enemyDB = self.server.execute("""
            SELECT EnemyID, Name, Size, Health, Speed, CR, STR, DEX, CON, INT, WIS, CHA, Type, Alignment, Languages, Skills, SavingThrows, Senses, Multiattack
            FROM Enemys
            WHERE EnemyID = ?
        """, (EnemyID,))
        enemyRow = enemyDB.fetchone()
        if enemyRow:
            enemyWeapons = self.GetWeapons(EnemyID)
            return Encounter.Enemy(
                enemyRow[0], enemyRow[1], enemyRow[2], enemyRow[3], enemyRow[4], enemyRow[5], enemyRow[6], enemyRow[7], enemyRow[8], enemyRow[9], enemyRow[10], enemyRow[11], enemyWeapons,
                type=enemyRow[12] if len(enemyRow) > 12 else "",
                alignment=enemyRow[13] if len(enemyRow) > 13 else "",
                languages=enemyRow[14] if len(enemyRow) > 14 else "",
                skills=enemyRow[15] if len(enemyRow) > 15 else "",
                saving_throws=enemyRow[16] if len(enemyRow) > 16 else "",
                senses=enemyRow[17] if len(enemyRow) > 17 else "",
                multiattack=enemyRow[18] if len(enemyRow) > 18 else ""
            )
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
    
    def GetMap(self, title):
        mapDB = self.server.execute(
            '''SELECT MapID, Path, Variants, Size FROM Maps WHERE Title = ?''', (title,)
        ).fetchone()
        if not mapDB:
            return None
        map_id, path, variants, size = mapDB
        floor = self.server.execute(
            '''SELECT FloorNumber FROM Floor WHERE MapID = ?''', (map_id,)
        ).fetchone()
        floor_number = floor[0] if floor else 0
        return (path, variants, size, floor_number)

    def GetEnemys(self):
        try:
            enemysDB = self.server.execute(f"SELECT EnemyID, Name, CR FROM Enemys ORDER BY RANDOM() LIMIT 20")
            enemyList = []
            for enemyDB in enemysDB:
                enemyList.append([enemyDB[1], enemyDB[2], enemyDB[0]])
            return enemyList
        except Exception as e:
            print(e)
            return []
    #endregion



    #region Search
    def searchEnemys(self, term):
        try:
            enemyList = self.server.execute(f"SELECT EnemyID, Name, CR FROM Enemys WHERE LOWER(Name) LIKE ? ORDER BY Name LIMIT 20", (f"%{term}%",)).fetchall()
            return enemyList
        except Exception as e:
            print(e)
            return []
        
    def searchMap(self, term):
        searchterm = f"{term}%"
        titleTerm = f"%{term}%"
        mapdb = self.server.execute(f"SELECT DISTINCT map.Title, map.Path FROM Maps map LEFT JOIN MapTags tag ON map.MapID = tag.MapID WHERE map.Title LIKE ? OR tag.Tag LIKE ? LIMIT 10", (titleTerm, searchterm)).fetchall()
        return mapdb

    #endregion



    #region Remove
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
    #endregion
    
    # region User name auth
    def createUser(self, fullname, email, passwordHash):
        cursor = self.server.cursor()
        cursor.execute("INSERT INTO User (FullName, Email, Password) VALUES (?, ?, ?)", (fullname, email, passwordHash))
        self.server.commit()
        return cursor.lastrowid

    def getUserByEmail(self, email):
        cursor = self.server.cursor()
        cursor.execute("SELECT UserID, FullName, Email, Password FROM User WHERE Email = ?", (email,))
        row = cursor.fetchone()
        if row:
            return {'userid': row[0], 'fullname': row[1], 'email': row[2], 'password': row[3]}
        return None

    #endregion