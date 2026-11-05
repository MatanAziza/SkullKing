from typing import List
from random import shuffle
from .values import Color
from .cards import Card

class Player:
	def __init__(self, name: str):
		self.hand: List[Card] = []
		self.wins: List[List[Card]] = []
		self.name = name
		self.points = 0
		self.score = 0
		self.announce = 0

	def clear_hand(self):
		self.hand.clear()

	def scores(self):
		return f"{self.name}'s hands: {self.score}/{self.announce}"

	def play(self, color: Color, whale):
		print(f"Which card do you you want to play, {self.name}?")
		print("\n".join([f"{i+1} - " + f"{card}" for i, card in enumerate(self.hand)]))
		while True:
			index = input("> ")
			if not index.isnumeric():
				print("Cant play that! That's not a number!")
				continue
			i = int(index)
			if i > len(self.hand) or i == 0:
				print("Cant play that! You don't have a card with this index!")
				continue
			i = int(index) - 1
			suggested = self.hand[i]
			break
		if suggested.color != color and color != Color.NONE:
			can_play_card = True
			if suggested.color == Color.NONE:
				return self.hand.pop(i)
			for card in self.hand:
				if card.color == color or card.color == Color.BLACK and suggested.color != Color.BLACK:
					can_play_card = False
					break
			if can_play_card or whale:
				return self.hand.pop(i)
			print(f"Can't play {suggested} because you have something else to play")
			return self.play(color, whale)
		return self.hand.pop(i)
