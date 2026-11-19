from classes.values import PirateKind

from .cards import Card, Color, ColorCard, Pirate, Escape, Mermaid, Loot, SkullKing, Kraken, WhiteWhale

class Deck:
    @classmethod
    def new(cls) -> list[Card]:
        deck: list[Card] = []
        for color in Color:
            if color in [Color.NONE, Color.ESCAPE]:
                continue
            for i in range(14):
                deck.append(ColorCard(i+1, color))
        for kind in PirateKind:
            deck.append(Pirate(kind))
        for i in range(5):
            deck.append(Escape())
        for i in range(2):
            deck.append(Mermaid())
        for i in range(2):
            deck.append(Loot())
        deck.append(SkullKing())
        deck.append(Kraken())
        deck.append(WhiteWhale())
        # print("Hello")
        # for card in deck:
        #     if card.value in (0, 14):
        #         print(card)
        # print("GB")
        return deck
