from common.database import Database
from model.constants import RESULTS
from model.deck import Deck
from model.hand import Hand

__author__ = 'smok'

class Game(object):

    def __init__(self):
        self.deck = Deck()
        self.deck.shuffle()
        self.hands = {}
        self.phase = 'NEW'
        self.winner = None
        self.results = {}

    def add_hand(self, name):
        self.hands[name] = Hand(name)

    def serve_all_hands(self):
        for k in self.hands.keys():
            hand = self.hands[k]
            cards = [self.deck.pile.pop() for i in range(5)]
            hand.add_cards(cards)
        self.phase = 'SERVED'

    def replace_cards(self, hand_name, indexes):
        if hand_name in self.hands:
            hand = self.hands[hand_name]
            for i in range(len(indexes)):
                val = indexes[i]
                hand.replace_card(val, self.deck.pile.pop())
        self.phase = 'REPLACE'

    def print_hand(self, name):
        hand = self.hands[name]
        hand.pretty_print()

    def print_hands(self):
        for i in self.hands.keys():
            print("Hand name: " + i)
            hand = self.hands[i]
            hand.pretty_print()
            print("***")

    def resolve(self):
        winner_figure = 'NOTHING'
        winner_value = 0
        for hand in self.hands.values():
            hand_figure = hand.evaluate()
            hand_val = (RESULTS.index(hand_figure) + 1) * 10
            self.results[hand.name] = (hand_figure, hand_val)
            if winner_figure < hand_figure:
                winner_figure = hand_figure
                winner_value = hand_val
                winner_name = hand.name
            else:
                if winner_value < hand_val:
                    winner_figure = hand_figure
                    winner_value = hand_val
                    winner_name = hand.name

        self.winner = (winner_name, hand_figure, winner_value)
        self.phase = 'RESOLVED'

    def json(self):
        return {
            "hands": [hand.json() for hand in self.hands.values()],
            "phase": self.phase,
            "winner": "" if self.winner is None else self.winner,
            "results": self.results
        }

    def save_game(self):
        Database.insert("games", self.json())
