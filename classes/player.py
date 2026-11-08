from .values import Color, Rank
from .cards import Card, Pirate
import socket

class Player:
    def __init__(self, name: str, client):
        self.hand: list[Card] = []
        self.wins: list[list[Card]] = []
        self.name = name
        self.client: socket.socket = client
        self.points = 0
        self.score = 0
        self.announce = 0

    def clear_hand(self):
        self.hand.clear()

    def send(self, string: str):
        self.client.send(string.encode())

    def receive(self) -> str:
        return self.client.recv(1024).decode("utf-8")

    def announces(self):
        return f"{self.name}'s hands: {self.score}/{self.announce}"

    def scores(self, ante: int):
        score = 0;
        for pli in self.wins:
            print(", ".join([f"{card}" for card in pli]))
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
        return score

    def show_hand(self):
        return "\n".join([f"{i+1} - " + f"{card}" for i, card in enumerate(self.hand)])

    def bet(self):
        self.send(
            f"OK \033[2J\033[HThis is your hand {self.name}:\n"
            f"{self.show_hand()}\n"
                )
        while True:
            self.send(
                "QUESTION How many hands will you bet ?\n")
            index = self.receive()[:-1]
            try:
                i = int(index)
            except ValueError:
                self.send("KO Cant bet that! That's not a number!")
                continue
            if i > len(self.hand):
                self.send("Ko Cant bet that! You don't have that many cards!")
                continue
            if i < 0:
                self.send("KO Cant bet that! You can't bet a negative number!")
                continue
            self.announce = i
            self.send(f"OK. You bet {i} hands.")
            break

    def play(self, color: Color, whale):
        print(f"Which card do you you want to play, {self.name}?")
        self.show_hand()
        while True:
            index = input("> ")
            if not index.isnumeric():
                print("Cant play that! That's not a number!")
                continue
            i = int(index)
            if i > len(self.hand) or i == 0:
                print("Cant play that! You don't have a card with this index!")
                continue
            i = int(index) - 1
            suggested = self.hand[i]
            break
        if suggested.color != color and color != Color.NONE:
            can_play_card = True
            if suggested.color == Color.NONE:
                return self.hand.pop(i)
            for card in self.hand:
                if card.color == color or card.color == Color.BLACK and suggested.color != Color.BLACK:
                    can_play_card = False
                    break
            if can_play_card or whale:
                return self.hand.pop(i)
            print(f"Can't play {suggested} because you have something else to play")
            return self.play(color, whale)
        return self.hand.pop(i)
