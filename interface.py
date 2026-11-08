from abc import ABC, abstractmethod
from main import Game

class Interface(ABC):
    def __init__(self, socket):
        self.socket = socket

    @abstractmethod
    def join_room(self, rooms: dict[str, Game]) -> str:
        pass

    @abstractmethod
    def create_room(self, rooms: dict[str, Game]) -> dict[str, Game]:
        pass

    @abstractmethod
    def ask_name(self, room: Game) -> str:
        pass
