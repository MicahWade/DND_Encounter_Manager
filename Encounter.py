import os
if(os.name == 'nt'):
    import msvcrt  # Import for capturing key presses on Windows
else:
    import getch  # Import for capturing key presses on Linux

def encounterMenu():
    while True:
        print("Encounter Menu")
        print("1. Players")
        print("2. Start Encounter")
        print("3. Exit")
        choice = intInput()
        if choice == 1:
            print("Players")
        elif choice == 2:
            print("Start Encounter")
        elif choice == 3:
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

def intInput():
    return int(msvcrt.getch().decode('utf-8') if os.name == 'nt' else getch.getch())