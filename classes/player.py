from .values import Color, Rank
from .cards import Card, Pirate
import socket

class Player:
    def __init__(self, name: str, interface):
        self.hand: list[Card] = []
        self.wins: list[list[Card]] = []
        self.name = name
        self.interface = interface
        self.points = 0
        self.score = 0
        self.announce = 0

    def clear_hand(self):
        self.hand.clear()

    def send(self, string: str):
        self.interface.send(string)

    def receive(self) -> str:
        return self.interface.receive()

    def announces(self):
        return f"{self.name}'s hands: {self.score}/{self.announce}"

    def scores(self, ante: int) -> tuple[int, str]:
        score = 0
        cards = ""
        for pli in self.wins:
            cards += '['+", ".join([f"{card}" for card in pli])+']\n'
            match pli[0].rank:
                case Rank.PIRATE:
                    bonus = Rank.SIREN
                case Rank.SKULLKING:
                    bonus = Rank.PIRATE
                case Rank.SIREN:
                    bonus = Rank.SKULLKING
                case _:
                    bonus = Rank.COLOR
            score += sum(
                card.bonus
                for card in pli
                if card.rank == bonus or card.value == 14
                    )
        if self.announce == 0:
            score += 10*(not len(self.wins))*ante
        score -= 10*abs(len(self.wins)-self.announce)
        return (score, cards)

    def show_hand(self):
        return "\n".join([f"{i+1} - " + f"{card}" for i, card in enumerate(self.hand)])

    def bet(self, barrier):
        barrier.wait()

        self.send(
            f"OK \033[2J\033[HThis is your hand {self.name}:\n"
            f"{self.show_hand()}"
                )
        while True:
            self.send(
                "QUESTION How many hands will you bet ?"
                    )
            index = self.receive()[:-1]
            try:
                i = int(index)
            except ValueError:
                self.send("KO Cant bet that! That's not a number!")
                continue
            if i > len(self.hand):
                self.send("KO Cant bet that! You don't have that many cards!")
                continue
            if i < 0:
                self.send("KO Cant bet that! You can't bet a negative number!")
                continue
            self.announce = i
            self.send(f"OK You bet {i} hands.")
            break

    def signal(self, game, message: str):
        self.send(
            f"CHECK Press Enter to {["start", "continue"][len(self.hand) != game.ante]} hands."
                )
        _ = self.receive()
        for player in game.players:
            player.send(message)

    def play(self, color: Color, whale) -> tuple[str, Card]:
        self.send(
            f"OK This is your hand {self.name}:\n"
            f"{self.show_hand()}"
                )
        while True:
            self.send(
                "QUESTION Which card do you you want to play ?"
                )
            index = self.receive()[:-1]
            try:
                i = int(index)
            except ValueError:
                self.send("KO Cant bet that! That's not a number!")
                continue
            if i > len(self.hand) or i == 0:
                self.send("KO Cant bet that! You don't have a card with this index!")
                continue
            suggested = self.hand[i-1]
            i -= 1
            break
        if suggested.color != color and color != Color.NONE:
            can_play_card = True
            if suggested.color == Color.NONE:
                return (str(self.hand[i]), self.hand.pop(i))
            for card in self.hand:
                if card.color == color or card.color == Color.BLACK and suggested.color != Color.BLACK:
                    can_play_card = False
                    break
            if can_play_card or whale:
                return (str(self.hand[i]), self.hand.pop(i))
            self.send(f"KO Can't play {suggested} because you have something else to play.")
            return self.play(color, whale)
        return (str(self.hand[i]), self.hand.pop(i))
