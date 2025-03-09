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


def encounterMenu():
    while True:
        print("Encounter Menu")
        print("1. Players")
        print("2. Start Encounter")
        print("3. Settings")
        print("4. Exit")
        choice = intInput()
        if choice == 1:
            playersMenu()
        elif choice == 2:
            encounterMenu()
        elif choice == 3:
            settingsMenu()
        elif choice == 4:
            return
    
def playersMenu():
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

def encounterMenu():
    ...

def settingsMenu():
    ...


def intInput():
    return int(msvcrt.getch().decode('utf-8') if os.name == 'nt' else getch.getch())