import os

class Player:
    name = ""
    initiative = -20
    def __init__(self, name):
        self.name = name

class Weapon:
    weaponid = None
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
    def __init__(self, name: str, weaponType: str, properties: list[str], attackModifier: int, damageType: str, damageDiceAmount: int, diceType: int, damageModifier: int, weaponid: int = None):
        self.name = name
        self.weaponType = weaponType
        self.properties = properties
        self.attackModifier = attackModifier
        self.damageType = damageType
        self.damageDiceAmount = damageDiceAmount
        self.diceType = diceType
        self.damageModifier = damageModifier
        if weaponid != None:
            self.weaponid = weaponid
    def JsonDetails(self):
        return {
            "name": self.name,
            "weaponType": self.weaponType,
            "attackmodifier": self.attackModifier,
            "damageType": self.damageType,
            "dicetype": self.diceType,
            "damgedice": self.damageDiceAmount,
            "properties": ", ".join(self.properties),
        }

class Enemy:
    id = None
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
    # New fields
    type = ""
    alignment = ""
    languages = ""
    skills = ""
    saving_throws = ""
    senses = ""
    multiattack = ""
    def __init__(self, id: int, name: str, size: str, health: int, speed: int, CR: int, STR: int, DEX: int, CON: int, INT: int, WIS: int, CHA: int, weapon: list, type: str = "", alignment: str = "", languages: str = "", skills: str = "", saving_throws: str = "", senses: str = "", multiattack: str = ""):
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
        self.id = id
        self.type = type
        self.alignment = alignment
        self.languages = languages
        self.skills = skills
        self.saving_throws = saving_throws
        self.senses = senses
        self.multiattack = multiattack


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