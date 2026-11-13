from abc import ABC, abstractmethod
from classes.game import Game

class Interface(ABC):
    def __init__(self, socket):
        self.socket = socket

    @abstractmethod
    def send(self, string: str):
        pass

    def receive(self) -> str:
        return self.socket.recv(1024).decode("utf-8")

    @abstractmethod
    def join_room(self, rooms: dict[str, Game]) -> str:
        pass

    @abstractmethod
    def create_room(self, rooms: dict[str, Game]) -> dict[str, Game]:
        pass

    @abstractmethod
    def ask_name(self, room: Game) -> str:
        pass
