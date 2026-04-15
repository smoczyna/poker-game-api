from model.card import Card
from model.constants import SUITS, RANKS

__author__ = 'smok'

class Deck(object):

    def __init__(self):
        self.pile = []
        for suit in SUITS:
            for rank in RANKS:
                self.pile.append(Card(rank, suit))

    def pretty_print(self):
        for card in self.pile:
            card.pretty_print()

    def shuffle(self):
        import random
        random.shuffle(self.pile)

    def serve_hand(self):
        i = 0
        cards = []
        while i < 5:
            cards.append(self.pile.pop())
            i += 1

        return cards

