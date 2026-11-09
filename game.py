from random import shuffle
from classes import Rank, Player, Deck, Card, Color
from classes.cards import ColorCard, Pirate, Siren, WhiteWhale


class Game:

    class RPS:
        def __init__(self):
            self.skullking = False
            self.pirate = False
            self.siren = False
            self.whale = 0
            self.kraken = 0

    def __init__(self):
        self.players: list[Player] = []
        self.ante = 1
        self.start = 0
        self.deck = Deck.new()
        shuffle(self.deck)

    def add_player(self, name: str, client, room: str) -> str:
        for player in self.players:
            if player.name == name:
                return "Player already exists. Choose another username"
        from classes.cli import CLI
        self.players.append(Player(name, CLI(client)))
        return f"Player '{name}' joined room {room}"

    def sendall(self, message: str):
        for player in self.players:
            player.send(message)

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
        # for player in self.players:
            # print(f"{player.name}'s cards:")
            # print(f"- {"\n- ".join(str(card) for card in player.hand)}")

    def plis(self):
        self.pli: list[Card] = []
        self.checks = self.RPS()
        self.first_color = Color.NONE
        for player in self.players:
            try:
                name, card = player.play(self.first_color, self.checks.whale)
            except AttributeError:
                name, card = player.play(Color.NONE, self.checks.whale)
            for p in self.players:
                if p.name != player.name:
                    p.send("OK - "+name+'\t')
            self.pli.append(card)
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
        self.sort()
        self.sendall(f"OK \033[2J\033[HPlayed cards:\n- {"\n- ".join(str(card) + f" {card.owner}" for card in self.pli)}")
        w_card = self.pli[0]
        if self.checks.skullking and self.checks.siren and self.checks.kraken >= self.checks.whale:
            w_card = next(c for c in self.pli if c.rank == Rank.SIREN)
        self.sendall(f"OK Winning card: {w_card}, owned by {w_card.owner}")
        if self.checks.kraken > self.checks.whale:
            self.sendall('OK , but Kraken killed them all !\t')
        elif type(self.pli[0]).__name__ == "WhiteWhale":
            self.sendall('OK , and none of you were worthy of the White Whale !\t')
        else:
            for player in self.players:
                if player.name == w_card.owner:
                    player.score += 1
                    player.wins.append(self.pli)
                    break
        r_index = self.player_index(w_card.owner)
        self.players = self.players[r_index:] + self.players[:r_index]

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
