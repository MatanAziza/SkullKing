from random import shuffle
import threading
import queue
from classes import Rank, Player, Deck, Card, Color
from classes.cards import Pirate
from classes.values import PirateKind


class Game:

    class RPS:
        def __init__(self):
            self.skullking: bool = False
            self.pirate: bool = False
            self.siren: bool = False
            self.whale: bool = False
            self.kraken: bool = False

    def __init__(self):
        self.players: list[Player] = []
        self.ante = 1
        self.start = 0
        self.deck = Deck.new()
        self.deck_round = Deck()
        shuffle(self.deck)

    def player_index(self, name: str):
        for i, player in enumerate(self.players):
            if player.name == name:
                return i
        return 0

    def sendall(self, message: str):
        for player in self.players:
            try:
                player.ok(message)
            except BrokenPipeError:
                raise BrokenPipeError(player.name)

    def hands_recap(self):
        final = f"\033[2J\033[H====== Round n°{self.ante} ======\nStarting player: {self.players[0].name}\n"
        for player in self.players:
            announces = f"{player.announces()}\n"
            final += announces
        final += "\nCards played:"
        return final

    def add_player(self, name: str, cli, room: str) -> str:
        for player in self.players:
            if player.name == name:
                return "Player already exists. Choose another username"
        self.players.append(Player(name, cli))
        return f"Player '{name}' joined room {room}"

    def remove_player(self, name: str) -> str:
        for i, player in enumerate(self.players):
            if player.name == name:
                self.players.pop(i)
                return f"'{name}' has been removed"
        return f"Player '{name}' doesn't exist"

    def deal(self):
        self.deck_round = self.deck.copy()
        shuffle(self.deck_round)
        for player in self.players:
            player.reset_round()
        for _ in range(self.ante):
            for player in self.players:
                player.hand.append(self.deck_round.pop(0).own(player.name))

    def bets(self):
        barrier = threading.Barrier(len(self.players))
        threads = []
        for player in self.players:
            t = threading.Thread(target=player.bet, args=(barrier,f"{self.hands_recap()}",))
            threads.append(t)
            t.start()
        for t in threads:
            t.join()
        bets = "\033[2J\033[HPlayers bets:\n" + '\n'.join([player.announces() for player in self.players])+""
        try:
            self.sendall(bets)
        except BrokenPipeError as e:
            raise BrokenPipeError(e.args[0])

    def next(self, name: str, reset: bool, round: int):
        ok = False
        for player in self.players:
            if reset:
                player.reset_round()
            if player.name == name:
                t = threading.Thread(target=player.signal, args=(self, f"{self.hands_recap()}" ,))
                t.start()
                ok = True
            else:
                player.ok(f"Waiting for the host to {["start", "continue"][round != 0]}...")
        if not ok:
            return
        t.join()

    def plis(self):
        self.pli: list[Card] = []
        self.checks = self.RPS()
        self.first_color = Color.FLEE
        next_starter = ""
        for player in self.players:
            try:
                name, card = player.play(self.first_color, self.checks.whale)
                for p in self.players:
                    if p.name != player.name:
                        p.ok("- "+name)
                match card.rank:
                    case Rank.SKULLKING:
                        self.checks.skullking = True
                    case Rank.SIREN:
                        self.checks.siren = True
                    case Rank.PIRATE:
                        self.checks.pirate = True
                match type(card).__name__:
                    case "Kraken":
                        self.checks.kraken = True
                        self.checks.whale = False
                    case "WhiteWhale":
                        self.checks.kraken = False
                        self.checks.whale = True
                if type(card).__name__ == "Pirate":
                    next_starter = self.pirates(card, player)
                self.pli.append(card)
                if self.first_color == Color.FLEE:
                    self.first_color = self.pli[-1].color
            except BrokenPipeError:
                raise BrokenPipeError(player.name)
        self.sort()
        self.sendall(f"\033[2J\033[HPlayed cards:\n- {"\n- ".join(str(card) + f" {card.owner}" for card in self.pli)}")
        w_card = self.pli[0]
        # if self.checks.skullking and self.checks.siren and self.checks.kraken >= self.checks.whale:
        #     w_card = next(c for c in self.pli if c.rank == Rank.SIREN)
        self.sendall(f"Winning card: {w_card}, owned by {w_card.owner}")
        if type(self.pli[0]).__name__ == "WhiteWhale":
            self.sendall(', and none of you were worthy of the White Whale !')
        if self.checks.kraken:
            self.sendall(', but Kraken killed them all !')
        else:
            w_index = self.player_index(w_card.owner)
            self.players[w_index].score += 1
            self.players[w_index].wins.append(self.pli)
        if not next_starter:
            next_starter = w_card.owner
        r_index = self.player_index(next_starter)
        self.players = self.players[r_index:] + self.players[:r_index]

    def sort(self):
        if self.checks.whale:
            self.pli.sort(key=lambda card: card.value, reverse=True)
            if not [c for c in self.pli if c.value != 0]:
                while type(self.pli[0]).__name__ != "WhiteWhale":
                    self.pli = self.pli[1:] + self.pli[:1]
            return
        self.pli.sort(key=lambda card: card.value, reverse=True)
        try:
            self.pli.sort(key=lambda card: card.color == self.first_color, reverse=True)
        except AttributeError:
            pass
        self.pli.sort(key=lambda card: card.rank.value, reverse=True)
        if self.checks.skullking and self.checks.siren and not self.checks.whale:
            i = 0
            for i, card in enumerate(self.pli):
                if card.rank == Rank.SIREN:
                    break
            siren = self.pli.pop(i)
            self.pli.insert(0, siren)
            print(self.pli)

    def loot(self):
        for w_id in range(len(self.players)):
            if self.players[w_id].score != self.players[w_id].announce or not self.players[w_id].wins:
                return
            for pli in self.players[w_id].wins:
                owners = []
                for card in pli:
                    if type(card).__name__ == "Loot":
                        owners.append(self.player_index(card.owner))
                for owner in owners:
                    if self.players[owner].score != self.players[owner].announce:
                        continue
                    self.players[w_id].loot += 20
                    if self.players[owner].name != self.players[w_id].name:
                        self.players[owner].loot += 20
            for player in self.players:
                player.ok(f"- {player.name}'s loot: {player.loot}")

    def recap(self):
        final = "\033[2J\033[H"
        r_name = []
        r_points = []
        r_round = []
        self.loot()
        for player in self.players:
            announces = f"{player.announces()} -> "
            points, hands = player.scores(self.ante)
            player.points += points
            final += f"{announces}\n{hands}\n"
            r_name.append(player.name)
            r_points.append(player.points)
            r_round.append(points)
        oz = sorted(zip(r_points, r_name, r_round), reverse=True)
        z = [f"{x} with {y} points ({z} points this round)" for y, x, z in oz]
        ranking = "\n".join([f"{i+1} - {elem}" for i, elem in enumerate(z)])
        final += ranking
        self.sendall(final)
        return oz

    def pirates(self, card, player):
        assert isinstance(card, Pirate)
        match card.kind:
            case PirateKind.ROSIE:
                return self.next_starter("", player.name)
            case PirateKind.RASCAL:
                self.rascal(player.name)
            case PirateKind.HARRY:
                player.harry = 1
            case PirateKind.WILL:
                self.will(player.name)
            case PirateKind.JUANITA:
                self.juanita(player.name)
            case PirateKind.TIGRESS:
                self.tigress(player.name, card)
        return ''

    def tigress(self, tigress: str, card: Card):
        for player in self.players:
            if player.name == tigress:
                t = threading.Thread(target=PirateKind.tigress, args=(player, card, self,))
                t.start()
            else:
                player.ok("\nWaiting for the Tigress to chose the better way...")
        t.join()

    def juanita(self, juanita: str):
        for player in self.players:
            if player.name == juanita:
                t = threading.Thread(target=PirateKind.juanita, args=(player, self))
                t.start()
            else:
                player.ok("\nWaiting for Juanita to scheme her plans...")
        t.join()

    def will(self, will: str):
        for player in self.players:
            if player.name == will:
                t = threading.Thread(target=PirateKind.will, args=(player, self))
                t.start()
            else:
                player.ok("\nWaiting for Will to steal some cards...")
        t.join()

    def rascal(self, rascal: str):
        for player in self.players:
            if player.name == rascal:
                t = threading.Thread(target=PirateKind.rascal, args=(player, self,))
                t.start()
            else:
                player.ok("\nWaiting for Rascal to go all in...")
        t.join()

    def next_starter(self, winner: str, rosie: str):
        if rosie:
            q = queue.Queue()
            for player in self.players:
                if player.name == rosie:
                    t = threading.Thread(target=PirateKind.rosie, args=(player, self, q,))
                    t.start()
                else:
                    player.ok("\nWaiting for Rosie to chose who will start...")
            t.join()
            return q.get()

    def end(self, name: str, oz):
        ok = False
        for player in self.players:
            player.reset_round()
            if player.name == name:
                t = threading.Thread(target=player.signal, args=(self, f"Winner is {oz[0][1]} with {oz[0][0]} points. GG!" ,))
                t.start()
                ok = True
            else:
                player.ok("Waiting for the host to finish game...")
        if not ok:
            return
        t.join()

    def recover(self, p_name: str, name) -> str:
        try:
            print(self.remove_player(p_name))
            if p_name == name:
                try:
                    name = self.players[0].name
                except IndexError:
                    print("All players left room")
                    return ""
                self.sendall(f"{p_name} was host. New host is {name}")
            self.sendall(f"{p_name} has left the game. Round will be started again.")
            self.next(name, True, 1)
            return name
        except BrokenPipeError as player_name:
            return self.recover(player_name.args[0], name)

