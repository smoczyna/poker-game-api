import unittest

from model import deck
from src.model.deck import Deck
from src.model.hand import Hand

class TestDeck(unittest.TestCase):

    def setUp(self):
        self.deck = Deck()
        self.deck.shuffle()

    def test_deck(self):
        self.assertEqual(len(self.deck.pile), 52)

    def test_serve_hand(self):
        self.deck.shuffle()
        cards = self.deck.serve_hand()
        self.assertEqual(len(cards), 5, "hand should have 5 cards")
        self.assertEqual(len(self.deck.pile), 47, "deck should have 47 cards left")

# if __name__ == '__main__':
#     unittest.main()

