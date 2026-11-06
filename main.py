from random import shuffle
from classes import Rank, Player, Deck, Card, Color
from classes.cards import ColorCard, Pirate, Siren, WhiteWhale

class RPS:
    def __init__(self):
        self.skullking = False
        self.pirate = False
        self.siren = False
        self.whale = 0
        self.kraken = 0

class Game:
    def __init__(self, players: list[str] = []):
        self.players: list[Player] = []
        self.ante = 1
        for p in players:
            self.players.append(Player(p))
        self.deck = Deck.new()
        shuffle(self.deck)

    def add_player(self, name: str, room: str) -> str:
        for player in self.players:
            if player.name == name:
                return "Player already exists. Choose another username"
        self.players.append(Player(name))
        return f"Player '{name}' joined room {room}"

    def remove_player(self, name: str) -> str:
        for i, player in enumerate(self.players):
            if player.name == name:
                self.players.pop(i)
                return "Player already exists. Choose another username"
        return f"Player '{name}' doesn't exist"

    def player_index(self, name: str):
        for i, player in enumerate(self.players):
            if player.name == name:
                return i

    def deal(self):
        deck_round = self.deck.copy()
        for _ in range(self.ante):
            for player in self.players:
                player.hand.append(deck_round.pop(0).own(player.name))
        for player in self.players:
            print(f"{player.name}'s cards:")
            print(f"- {"\n- ".join(str(card) for card in player.hand)}")

    def plis(self):
        print("\033[2J\033[H", end='')
        self.pli: list[Card] = []
        self.checks = RPS()
        self.first_color = Color.NONE
        for player in self.players:
            input(f"Press Enter to play, {player.name}")
            print("\033[2J\033[H", end='')
            print("Cards played:")
            if self.pli:
                print(f"{"\n".join([str(card) + f" {card.owner}" for card in self.pli])}")
            try:
                self.pli.append(player.play(self.first_color, self.checks.whale))
            except AttributeError:
                self.pli.append(player.play(Color.NONE, self.checks.whale))
            match self.pli[-1].rank:
                case Rank.SKULLKING:
                    self.checks.skullking = True
                case Rank.SIREN:
                    self.checks.siren = True
                case Rank.PIRATE:
                    self.checks.pirate = True
            match type(self.pli[-1]).__name__:
                case "Kraken":
                    self.checks.kraken += self.checks.whale + 1
                case "WhiteWhale":
                    self.checks.whale += self.checks.kraken + 1
            try:
                if self.first_color == Color.NONE:
                    raise AttributeError
            except AttributeError:
                if self.pli[-1].color != Color.NONE:
                    self.first_color = self.pli[-1].color
            print("\033[2J\033[H", end='')
        self.sort()
        print(f"Played cards:\n- {"\n- ".join(str(card) + f" {card.owner}" for card in self.pli)}")
        w_card = self.pli[0]
        if self.checks.skullking and self.checks.siren and self.checks.kraken >= self.checks.whale:
            w_card = next(c for c in self.pli if c.rank == Rank.SIREN)
        print(f"Winning card: {w_card}, owned by {w_card.owner}")
        if self.checks.kraken > self.checks.whale:
            print(', but Kraken killed them all !')
        elif type(self.pli[0]).__name__ == "WhiteWhale":
            print(', and none of you were worthy of the White Whale !')
        else:
            for player in self.players:
                if player.name == w_card.owner:
                    player.score += 1
                    player.wins.append(self.pli)
                    break
        r_index = self.player_index(w_card.owner)
        self.players = self.players[r_index:] + self.players[:r_index]
        input("Press Enter to continue")

    def play(self):
        for player in self.players:
            player.bet()
        for _ in range(len(self.players[0].hand)):
            self.plis()
        for player in self.players:
            print(f"{player.announces()} -> ", end='')
            print(player.scores(self.ante))

    def sort(self):
        self.pli.sort(key=lambda card: card.value, reverse=True)
        try:
            self.pli.sort(key=lambda card: card.color == self.first_color, reverse=True)
        except AttributeError:
            pass
        self.pli.sort(key=lambda card: card.rank.value, reverse=True)
        if self.checks.whale:
            self.pli.sort(key=lambda card: card.value, reverse=True)
            if not [c for c in self.pli if c.value != 0]:
                while type(self.pli[0]).__name__ != "WhiteWhale":
                    self.pli = self.pli[1:] + self.pli[:1]

if __name__ == "__main__":
    g = Game(["Matan", "Marie", "Nasser"])
    g.ante = 3
    g.deal()
    g.players[0].hand[0] = ColorCard(14, Color.BLACK).own("Matan")
    g.play()
