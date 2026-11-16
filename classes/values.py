from enum import Enum

class Color(Enum):
    NONE=None
    FLEE="Flee"
    VIOLET="Violet"
    YELLOW="Yellow"
    GREEN="Green"
    BLACK="Black"

class SColor(Enum):
    NONE=None
    VIOLET="\033[0;95m"
    YELLOW="\033[0;33m"
    GREEN="\033[0;32m"
    BLACK="\033[0;90m"
    SIREN="\033[1;36m"
    PIRATE="\033[1;31m"
    KRAKEN="\033[1;35m"
    WHITEWHALE="\033[1;97m"
    SKULLKING="\033[7;01m"
    FLEE="\033[0;97m"
    LOOT="\033[1;33m"

class Rank(Enum):
    COLOR=0
    CREATURE=0
    FLEE=0
    LOOT=0
    BLACK=1
    SIREN=2
    PIRATE=3
    SKULLKING=4

class PirateKind(Enum):
    ROSIE="Rosie the Sweetheart"
    RASCAL="Rascal the Gambler"
    WILL="Will the Bandit"
    JUANITA="Juanita Jade"
    HARRY="Harry the Giant"

    def fn(self):
        print("test")
