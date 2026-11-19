from enum import Enum

class Color(Enum):
    NONE="None"
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
    CREATURE=-3
    FLEE=-2
    LOOT=-1
    COLOR=0
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
    TIGRESS="Tigress"

    @staticmethod
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
                game.sendall(f"{player.name} chose {game.players[i].name} to start.")
                queue.put(game.players[i].name)
                player.check("Press Enter to continue")
                _ = player.receive()
                return
        except BrokenPipeError:
            pass

    @staticmethod
    def rascal(player, game):
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
                game.sendall(f"{player.name} chose to bet {(i-1)*10} points. Good luck!")
                player.rascal = (i-1)*10
                player.check("Press Enter to continue")
                _ = player.receive()
                return
        except BrokenPipeError:
            pass

    @staticmethod
    def will(player, game):
        try:
            if len(player.hand) == 0:
                player.ok("You don't have anymore cards to play next turn.")
                return
            cards = [game.deck_round.pop(0), game.deck_round.pop(0)]
            player.ok(
                "You can trade one of those two cards for one in your deck:\n"
                f"Cards:\n1 - {cards[0]}\n2 - {cards[1]}\n"
                    f"Your hand:\n{player.show_hand()}")
            while True:
                player.question(
                    "\nWhich card do you want to take ?\n"
                    f"0 - None\n1 - {cards[0]}\n2 - {cards[1]}"
                        )
                index = player.receive()[:-1]
                try:
                    i = int(index)
                except ValueError:
                    player.ko("Can't do that! That's not a number!")
                    continue
                if i == 0:
                    player.ok("You kept your hand")
                    player.check("Press Enter to continue")
                    _ = player.receive()
                    return
                if i not in [1, 2]:
                    player.ko("Can't take this card! That's not an option.")
                    continue
                i -= 1
                player.question(
                    "\nWhich card do you want to trade it for ?\n"
                        )
                index = player.receive()[:-1]
                try:
                    j = int(index)
                except ValueError:
                    player.ko("Can't do that! That's not a number!")
                    continue
                j -= 1
                if not (0<=j<len(player.hand)) :
                    player.ko("Can't trade this card! That's not an option.")
                    continue
                card = player.hand.pop(j)
                player.ok(f"You traded {cards[i]} for {card}")
                player.hand.insert(j, cards.pop(i).own(player.name))
                game.deck_round.insert(0, cards[0])
                game.deck_round.insert(0, card.own("None"))
                player.check("Press Enter to continue")
                _ = player.receive()
                return
        except BrokenPipeError:
            pass

    @staticmethod
    def juanita(player, game):
        copy = game.deck_round.copy()
        copy.sort(key=lambda card: card.value, reverse=True)
        copy.sort(key=lambda card: card.color.value)
        copy.sort(key=lambda card: card.rank.value, reverse=True)
        copy.sort(key=lambda card: card.rank.name == Rank.CREATURE, reverse=True)
        try:
            while True:
                player.ok(
                    "This is the remaining deck:\n"
                    f"{', '.join([str(card) for card in copy])})"
                        )
                player.check("Press Enter to continue")
                _ = player.receive()
                return
        except BrokenPipeError:
            pass

    @staticmethod
    def tigress(player, card, game):
        try:
            while True:
                player.question(
                    "\nDo you want to play the Tigress as:\n"
                    "1 - A 🪎 \033[1;31mPirate\033[0;97m🪎 \n2 - A 🏳️  Flee 🏳️ \n"
                        )
                index = player.receive()[:-1]
                try:
                    i = int(index)
                except ValueError:
                    player.ko("Can't do that! That's not a number!")
                    continue
                if i not in [1, 2]:
                    player.ko("Can't make this choice! That's not an option.")
                    continue
                if i == 2:
                    card.rank = Rank.FLEE
                game.sendall(f"{player.name} is playing The Tigress as a {["Pirate", "Flee"][i-1]}")
                player.check("Press Enter to continue")
                _ = player.receive()
                return
        except BrokenPipeError:
            pass
