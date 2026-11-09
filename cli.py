from game import Game
from interface import Interface

class CLI(Interface):
    def __init__(self, socket):
        self.socket = socket

    def send(self, string: str):
        self.socket.send(string.encode())

    def receive(self) -> str:
        return self.socket.recv(1024).decode("utf-8")

    def join_room(self, rooms: dict[str, Game]) -> str:
        while True:
            self.send("QUESTION What's the room's name:\t")
            request = self.receive()
            if request == '\n':
                self.send("KO Cant join room with empty name!\t")
                continue
            request = request[:-1]
            if rooms.get(request, "error") != "error":
                break
            self.send("KO Room doesn't exists!\t")
        self.send(f"OK Room '{request}' joined.\t")
        return request

    def create_room(self, rooms: dict[str, Game]) -> dict[str, Game]:
        while True:
            self.send("QUESTION What's your room name:\t")
            request = self.receive()
            if request == '\n':
                self.send("KO Cant create room with empty name!\t")
                continue
            request = request[:-1]
            if rooms.get(request, "error") == "error":
                break
            self.send("KO Room already exists!\t")
        self.send(f"OK Room created {request}.\t")
        return {request: Game()}

    def ask_name(self, room: Game, role: str='join') -> str:
        while True:
            self.send("QUESTION What's your username:\t")
            request = self.receive()
            if request == '\n':
                self.send("KO Cant create empty username!\t")
                continue
            request = request[:-1]
            players = [player.name for player in room.players]
            if request in players:
                self.send("KO User already exists!\t")
                continue
            self.send("CHECK Are you sure ? yes[y]/Enter | no[n]\t")
            check = self.receive()
            if check in ["no\n", "n\n"]:
                continue
            break
        self.send(f"OK Joined with username {request}\t")
        self.send(role.upper()+"\t")
        return request

    def start(self, game: Game):
        while True:
            self.send("CHECK Type 'start' to start the game\t")
            while True:
                request = self.receive()
                if request != 'start\n':
                    self.send("KO Don't understand this command.\t")
                    continue
                break
            self.send(
                "CHECK Would you like to start? Players are:\n"
                f"{'\n'.join([player.name for player in game.players])}\n"
                "Yes[y]/Enter | No[n]\t"
                    )
            check = self.receive()
            if check in ["no\n", "n\n"]:
                continue
            for player in game.players:
                player.send("START\t")
            break
