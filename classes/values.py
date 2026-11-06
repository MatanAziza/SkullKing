from enum import Enum

class Color(Enum):
    NONE=None
    VIOLET="Violet"
    YELLOW="Yellow"
    GREEN="Green"
    BLACK="Black"

class SColor(Enum):
    NONE=None
    VIOLET="\033[0;35m"
    YELLOW="\033[0;33m"
    GREEN="\033[0;32m"
    BLACK="\033[0;37m"
    SIREN="\033[0;36m"
    PIRATE="\033[0;31m"
    KRAKEN="\033[1;35m"
    WHITEWHALE="\033[1;37m"
    SKULLKING="\033[40m"
    FLEE="\033[0;37m"
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
