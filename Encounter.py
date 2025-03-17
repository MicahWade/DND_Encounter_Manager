import os
import Database
if(os.name == 'nt'):
    import msvcrt  # Import for capturing key presses on Windows
else:
    import getch  # Import for capturing key presses on Linux

dataBase = dataBase.EncounterDatabase()

class Player:
    name = ""
    initiative = 0

class Enemy:
    name = ""
    initiative = 0
    CR = 0

class Encounter:
    characters = []
    currentTurn = 0
    CR = 0
    def addCharacter(self, character):
        self.characters.append(character)
    def removeCharacter(self, character):
        self.characters.remove(character)
    def sortCharacters(self):
        self.characters.sort(key=lambda x: x.initiative)

players = []
encounters = []

def EncounterMenu():
    while True:
        print("Encounter Menu")
        print("1. Players")
        print("2. New Encounter")
        print("3. Load Encounter")
        print("4. Load Template")
        print("5. Create Template")
        print("6. Settings")
        print("7. Save To DB")
        print("8. Exit")
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
            SaveToDB()
        elif choice == 8:
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
    print("Enter  Name:")

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

def SaveToDB():
    for encounter in encounters:
        dataBase.AddEncounter(encounter)


def Clear():
    if os.name == 'nt':
        os.system('cls')
    else:
       os.system('clear')

def intInput():
    return int(msvcrt.getch().decode('utf-8') if os.name == 'nt' else getch.getch())