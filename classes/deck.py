from typing import List
from .cards import Card, Color, ColorCard, Pirate, Flee, Siren, Loot, SkullKing, Kraken, WhiteWhale

class Deck:
	@classmethod
	def new(cls) -> List[Card]:
		deck: List[Card] = []
		for color in Color:
			if color == Color.NONE:
				continue
			for i in range(14):
				deck.append(ColorCard(i+1, color))
		for i in range(5):
			deck.append(Pirate())
		for i in range(5):
			deck.append(Flee())
		for i in range(2):
			deck.append(Siren())
		for i in range(2):
			deck.append(Loot())
		deck.append(SkullKing())
		deck.append(Kraken())
		deck.append(WhiteWhale())
		return deck
