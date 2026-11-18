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

    def rosie(player, game, queue):
        try:
            while True:
                player.question(
                    "\nWhich player do you want to start ?\n"
                    f"{'\n'.join([f"{i+1} - {player.name}" for i, player in enumerate(game.players)])}"
                        )
                index = player.receive()[:-1]
                try:
                    i = int(index)
                except ValueError:
                    player.ko("Can't do that! That's not a number!")
                    continue
                i -= 1
                if i >= len(game.players):
                    player.ko(f"Can't make player {i + 1} start! There's not that many players!")
                    continue
                if i < 0:
                    player.ko(f"Can't make player {i + 1} start! There's no player 0!")
                    continue
                player.ok(f"You chose {game.players[i].name} to start.")
                queue.put(game.players[i].name)
                return
        except BrokenPipeError:
            pass

    def rascal(player):
        try:
            while True:
                player.question(
                    "\nHow many points do you want to bet:\n"
                    "1 - 0 points,\n2 - 10 points or\n3 - 20 points ?"
                        )
                index = player.receive()[:-1]
                try:
                    i = int(index)
                except ValueError:
                    player.ko("Can't do that! That's not a number!")
                    continue
                if i not in [1, 2, 3]:
                    player.ko("Can't place this bet! That's not an option.")
                    continue
                player.ok(f"You chose to bet {(i-1)*10} points. Good luck!")
                player.rascal = (i-1)*10
                return
        except BrokenPipeError:
            pass

    def will():
        pass

    def juanita():
        pass

    def harry():
        pass
