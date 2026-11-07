from main import Game
from interface import Interface

class CLI(Interface):
    def __init__(self, socket):
        self.socket = socket

    def join_room(self, rooms: dict[str, Game]) -> str:
        self.socket.send("QUESTION What's the room's name:".encode())
        while True:
            request = self.socket.recv(1024).decode("utf-8")
            if request == '\n':
                self.socket.send("KO Cant join room with empty name!\nWhat's the room's name:".encode())
                continue
            if rooms.get(request[:-1], "error") != "error":
                break
            self.socket.send("KO Room doesn't exists!\nWhat's the room's name:".encode())
        self.socket.send(f"OK Room '{str(request[:-1])}' joined".encode())
        return request[:-1]

    def create_room(self, rooms: dict[str, Game]) -> dict[str, Game]:
        self.socket.send("QUESTION What's your room name:".encode())
        while True:
            request = self.socket.recv(1024).decode("utf-8")
            if request == '\n':
                self.socket.send("KO Cant create room with empty name!\nWhat's your room name:".encode())
                continue
            if rooms.get(request[:-1], "error") == "error":
                break
            self.socket.send("KO Room already exists!\nWhat's your room name:".encode())
        self.socket.send(f"OK Room created {str(request[:-1])}".encode())
        return {request[:-1]: Game()}

    def ask_name(self, room: Game):
        while True:
            self.socket.send("QUESTION What's your username:".encode())
            request = self.socket.recv(1024).decode("utf-8")
            if request == '\n':
                self.socket.send("KO Cant create empty username!\nWhat's your username:".encode())
                continue
            players = [player.name for player in room.players]
            if request[:-1] in players:
                self.socket.send("KO User already exists!\nWhat's your username:".encode())
                continue
            self.socket.send("CHECK Are you sure ? yes[y]/Enter | no[n]".encode())
            check = self.socket.recv(1024).decode("utf-8")
            if check in ["no\n", "n\n"]:
                continue
            break
        self.socket.send(f"WAIT Joined with username {str(request[:-1])}".encode())
        return request[:-1]

    def start(self, game: Game):
        while True:
            self.socket.send("CHECK Type 'start' to start the game".encode())
            while True:
                request = self.socket.recv(1024).decode("utf-8")
                if request != 'start\n':
                    self.socket.send("KO Don't understand this command.\nType 'start' to start the game".encode())
                    continue
                break
            self.socket.send(
                f"CHECK Would you like to start? Players are:\n{'\n'.join([player.name for player in game.players])}\nYes[y]/Enter | No[n]".encode()
                            )
            check = self.socket.recv(1024).decode("utf-8")
            if check in ["no\n", "n\n"]:
                continue
            for player in game.players:
                player.client.send(f"START".encode())
            break
