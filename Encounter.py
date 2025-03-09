import os
if(os.name == 'nt'):
    import msvcrt  # Import for capturing key presses on Windows
else:
    import getch  # Import for capturing key presses on Linux

class Player:
    name = ""
    initiative = 0

class Enemy:
    name = ""
    initiative = 0

class Encounter:
    characters = []
    currentTurn = 0
    def addCharacter(self, character):
        self.characters.append(character)
    def removeCharacter(self, character):
        self.characters.remove(character)
    def sortCharacters(self):
        self.characters.sort(key=lambda x: x.initiative)


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
        print("3. Back")
        choice = intInput()
        if choice == 1:
            print("Enter Player Name:")
            playerName = input()
            print("Enter Player Initiative:")
            playerInit = int(input())
        elif choice == 2:
            print("Remove Player")
        elif choice == 3:
            return

def NewEncounter():
    ...

def LoadEncounter():
    ...

def LoadTemplate():
    ...

def CreateTemplate():
    ...

def SettingsMenu():
    ...

def Clear():
    name = os.name

    # for windows
    if name == 'nt':
        _ = os.system('cls')

    # for mac and linux(here, os.name is 'posix')
    else:
        _ = os.system('clear')

def intInput():
    return int(msvcrt.getch().decode('utf-8') if os.name == 'nt' else getch.getch())