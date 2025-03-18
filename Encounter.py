import os
import Database
import random
if(os.name == 'nt'):
    import msvcrt  # Import for capturing key presses on Windows
else:
    import getch  # Import for capturing key presses on Linux

dataBase = dataBase.EncounterDatabase()

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

class Enemy:
    name = ""
    heath = 0
    initiativeModifier = 0
    initiatave = 0
    CR = 0
    def __init__(self, name, heath, initiativeModifier, CR):
        self.name = name
        self.heath = heath
        self.initiativeModifier = initiativeModifier
        self.CR = CR
    
    def Roll(self):
        self.inititave = random.randint(1, 20) + self.initiativeModifier 


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

currentEncouter = Encounter()

def EncounterMenu():
    while True:
        print("Encounter Menu")
        print("1. Players")
        print("2. New Encounter")
        print("3. Load Encounter")
        print("4. Load Template")
        print("5. Create Template")
        print("6. Settings")
        print("7. Exit")
        choice = intInput()
        if choice == 1:
            PlayersMenu()
        elif choice == 2:
            NewEncounter()
        elif choice == 3:
            LoadEncounter()
        elif choice == 4:
            LoadTemplate()
        elif choice == 5:
            CreateTemplate()
        elif choice == 6:
            SettingsMenu()
        elif choice == 7:
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
            playerName = input()
            print("Enter Player Initiative:")
            playerInit = int(input())
            player = Player()
            player.name = playerName
            player.initiative = playerInit
            players.append(player)
        elif choice == 2:
            print("Select Player to Remove")
            for i, player in enumerate(players):
                print(f"{i+1}. {player.name}")
            choice = intInput()
            players.pop(choice-1)
        elif choice == 3:
            print("Player List")
            for player in players:
                print(f"{player.name} - {player.initiative}")
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
    

def LoadEncounter():
    ...

def LoadTemplate():
    ...

def CreateTemplate():
    ...

def SettingsMenu():
    ...

def CreateEnemy():
    print("Enter Enemy Name:")
    enemyName = input()
    print("Enter Enemy initiative modifier:")
    enemyInit = int(input())
    enemy = Enemy()
    enemy.name = enemyName
    enemy.initiative = enemyInit
    Clear()
    return enemy


def Clear():
    if os.name == 'nt':
        os.system('cls')
    else:
       os.system('clear')

def intInput():
    return int(msvcrt.getch().decode('utf-8') if os.name == 'nt' else getch.getch())