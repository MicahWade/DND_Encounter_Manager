import os
from Database import EncounterDatabase
import random
if(os.name == 'nt'):
    import msvcrt  # Import for capturing key presses on Windows
else:
    ...
    # import getch  # Import for capturing key presses on Linux

dataBase = EncounterDatabase(False)

class Player:
    name = ""
    initiative = -20
    def __init__(self, name):
        self.name = name

    def EnterInitiative(self):
        while initiative == -20:
            try: 
                print(f"Enter {self.name}'s initiative,")
                self.initiative = int(input())
            except:
                Clear()
        Clear()
        return

class Weapon:
    name = ""
    weaponType = ""
    # Strings
    properties = []
    attackModifier = 0
    damageType = ""
    damageDiceAmount = 1
    # D4 D6 D8 D10 D12
    diceType = 4
    damageModifier = 0
    def __init__(self, name, weaponType, properties, attackModifier, damageType, damageDiceAmount, diceType, damageModifier):
        self.name = name
        self.weaponType = weaponType
        self.properties = properties
        self.attackModifier = attackModifier
        self.damageType = damageType
        self.damageDiceAmount = damageDiceAmount
        self.diceType = diceType
        self.damageModifier = damageModifier
    def JsonDetails(self):
        return {
            "name": self.name,
            "attackmodifier": self.attackModifier,
            "dicetype": self.diceType,
            "damgedice": self.damageDiceAmount,
            "properties": self.properties,
        }

class Enemy:
    name = ""
    size = ""
    health = 0
    speed = 0
    initiatave = 0
    CR = 0
    STR = 0
    DEX = 0
    CON = 0
    INT = 0
    WIS = 0
    CHA = 0
    weapons = []
    def __init__(self, name, size, health, speed, CR, STR, DEX, CON, INT, WIS, CHA, weapon):
        self.name = name
        self.size = size
        self.health = health
        self.speed = speed
        self.CR = CR
        self.STR = STR
        self.DEX = DEX
        self.CON = CON
        self.INT = INT
        self.WIS = WIS
        self.CHA = CHA
        self.weapons = weapon
    
    def Roll(self):
        self.inititave = random.randint(1, 20) + self.DEX 


class Encounter:
    name = ""
    characters = []
    currentTurn = 0
    CR = 0

    def addCharacter(self, character):
        self.characters.append(character)
    def removeCharacter(self, character):
        self.characters.remove(character)
    def sortCharacters(self):
        self.characters.sort(key=lambda x: x.initiative)

    def __init__(self, name, enemys, CR):
        self.name = name
        self.characters = enemys
        self.CR = CR
    def StartEncounter(self, players):
        for enemy in self.characters:
            enemy.Roll()

        for player in players:
            player.EnterInitiative()
            self.addCharacter(player)
        
        self.sortCharacters()
    
        inBattle = True
        while inBattle:
            print("1. Attack")
            print("2. ")

# Funtion to 
def IsEnemy(list):
    for enemy in list:
        ...

currentEncouter = None

def EncounterMenu():
    while True:
        print("Encounter Menu")
        print("1. Players")
        print("2. New Encounter")
        print("3. Mange Encounters")
        print("4. Enemy")
        print("5. Settings")
        print("6. Exit")
        choice = intInput()
        if choice == 1:
            PlayersMenu()
        elif choice == 2:
            NewEncounter()
        elif choice == 3:
            MangeEncounters()
        elif choice == 4:
            EnemyMenu()
        elif choice == 5:
            SettingsMenu()
        elif choice == 6:
            dataBase.server.commit()
            return
        Clear()
    
def PlayersMenu():
    while True:
        print("Players")
        print("1. Add Player")
        print("2. Remove Player")
        print("3. Player List")
        print("4. Back")
        choice = intInput()
        if choice == 1:
            print("Enter Player Name:")
            name = input()
            player = Player(name)
            dataBase.AddPlayer(player)
        elif choice == 2:
            print("Select Player to Remove")
            players = dataBase.GetPlayers()
            for i, player in enumerate(players):
                print(f"{i+1}. {player.name}")
            choice = intInput()
            try:    
                dataBase.RemovePlayer(players[choice-1])
            except:
                ...
        elif choice == 3:
            print("Player List")
            players = dataBase.GetPlayers()
            for player in players:
                print(f"{player.name}")
            input("Press Enter to Continue")
        elif choice == 4:
            return
        Clear()

def NewEncounter():
    encounters = Database.GetEncounters() 
    encountersLen = len(encounters)
    numberInput = 0
    # TODO: Check that start at one not zero
    while numberInput <= 0 or numberInput > encountersLen: 
        [print(f"{i}, {encounter[1]}") for i, encounter in enumerate(encounters)]
        print("Enter Encounter Number:")
        try:
            numberInput = int(input())
        except:
            ...
        Clear()
    currentEncouter = Database.GetEncounter(encounters[numberInput])
    players = Database.GetPlayer
    currentEncouter.StartEncounter(players)

def MangeEncounters():
    ...

def LoadEncounter():
    ...

def LoadTemplate():
    ...

def CreateTemplate():
    ...

def EnemyMenu():
    Clear()
    print("Enemey Menu")
    print("1. Create")
    print("2. Remove")
    print("3. View")
    print("4. Exit")

def SelectEnemy():
    print("Enemys")
    enemys = dataBase.GetEnemys()
    for i, enemy in enumerate(enemys):
        print(f"{i}, {enemy[0]}")
def SettingsMenu():
    ...

def CreateEnemy():
    print("Enter Enemy Name:")
    enemyName = input()
    print("Enter Enemy initiative modifier:")
    enemyInit
    while enemyInit == None:
        try:
            enemyInit = int(input())
        except:
            ...
    print("Enter your HP")
    enemyHP = None
    while enemyHP == None:
        try:
            enemyHP = int(input())
        except:
            ...
    print("Enter your CR")
    enemyCR = None
    while enemyCR == None:
        try:
            enemyCR = int(input())
        except:
            ...
    
    enemy = Enemy(enemyName, enemyHP, enemyInit, enemyCR)
    return enemy


def Clear():
    if os.name == 'nt':
        os.system('cls')
    else:
       os.system('clear')

def intInput():
    while True:
        try:
            return int(msvcrt.getch().decode('utf-8') if os.name == 'nt' else input())
        except:
            ...