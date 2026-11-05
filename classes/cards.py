from .values import Color, SColor, Rank

class Card:
	def __init__(self):
		self.color = Color.NONE

	def __str__(self) -> str:
		return f"{SColor[type(self).__name__.upper()].value}{type(self).__name__}\033[0;37m"

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
		return f"{SColor[self.color.name].value}{str(self.color.value)} {self.value}\033[0;37m"

class Siren(Card):
	def __init__(self):
		super().__init__()
		self.bonus = 20
		self.value = 0
		self.rank = Rank.SIREN

class Pirate(Card):
	def __init__(self):
		super().__init__()
		self.bonus = 30
		self.value = 0
		self.rank = Rank.PIRATE
		
class SkullKing(Card):
	def __init__(self):
		super().__init__()
		self.bonus = 40
		self.value = 0
		self.rank = Rank.SKULLKING

class Creature(Card):
	def __init__(self):
		super().__init__()
		self.bonus = 0
		self.value = 0
		self.rank = Rank.CREATURE

class Kraken(Creature):
	def __init__(self):
		super().__init__()

class WhiteWhale(Creature):
	def __init__(self):
		super().__init__()

class Flee(Card):
	def __init__(self):
		super().__init__()
		self.bonus = 0
		self.value = 0
		self.rank = Rank.FLEE
		
class Loot(Card):
	def __init__(self):
		super().__init__()
		self.bonus = 0
		self.value = 0
		self.rank = Rank.LOOT