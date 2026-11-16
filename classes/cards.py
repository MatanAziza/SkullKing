from .values import Color, PirateKind, Rank, SColor

class Card:
    def __init__(self):
        self.color = Color.NONE
        self.value = 0
        self.bonus = 0
        self.rank = Rank.COLOR
        self.owner = "None"

    def __str__(self) -> str:
        return f"{SColor[type(self).__name__.upper()].value}{type(self).__name__}\033[0;97m"

    def own(self, name: str) -> "Card":
        self.owner = name
        return self

class ColorCard(Card):
    def __init__(self, value: int, color: Color):
        self.value = value
        self.color = color
        self.bonus = (value==14) * 10 * (1 + (color == Color.BLACK) )
        self.rank = Rank.BLACK if color is Color.BLACK else Rank.COLOR

    def __str__(self) -> str:
        return f"{SColor[self.color.name].value}{str(self.color.value)} {self.value}\033[0;97m"

class Siren(Card):
    def __init__(self):
        super().__init__()
        self.bonus = 20
        self.rank = Rank.SIREN

    def __str__(self) -> str:
        return f"🧜 {SColor[type(self).__name__.upper()].value}{type(self).__name__}\033[0;97m 🧜"

class Pirate(Card):
    def __init__(self, kind: PirateKind):
        super().__init__()
        self.bonus = 30
        self.rank = Rank.PIRATE
        self.kind = kind

    def __str__(self) -> str:
        return f"🪎  {SColor[type(self).__name__.upper()].value}{self.kind.value}\033[0;97m 🪎"


class SkullKing(Card):
    def __init__(self):
        super().__init__()
        self.bonus = 40
        self.rank = Rank.SKULLKING

    def __str__(self) -> str:
        return f"☠️  {SColor[type(self).__name__.upper()].value}{type(self).__name__}\033[0;97m ☠️"

class Creature(Card):
    def __init__(self):
        super().__init__()
        self.bonus = 0
        self.rank = Rank.CREATURE

class Kraken(Creature):
    def __init__(self):
        super().__init__()

    def __str__(self) -> str:
        return f"🐙 {SColor[type(self).__name__.upper()].value}{type(self).__name__}\033[0;97m 🐙"

class WhiteWhale(Creature):
    def __init__(self):
        super().__init__()

    def __str__(self) -> str:
        return f"🐋 {SColor[type(self).__name__.upper()].value}{type(self).__name__}\033[0;97m 🐋"

class Flee(Card):
    def __init__(self):
        super().__init__()
        self.bonus = 0
        self.rank = Rank.FLEE
        self.color = Color.FLEE

    def __str__(self) -> str:
        return f"🏳️  {SColor[type(self).__name__.upper()].value}{type(self).__name__}\033[0;97m 🏳️"

class Loot(Card):
    def __init__(self):
        super().__init__()
        self.bonus = 0
        self.rank = Rank.LOOT
        self.color = Color.FLEE

    def __str__(self) -> str:
        return f"🪙 {SColor[type(self).__name__.upper()].value}{type(self).__name__}\033[0;97m 🪙"
