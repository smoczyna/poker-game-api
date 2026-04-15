import unittest

from model.game import Game


class TestGame(unittest.TestCase):

    def setUp(self):
        self.game = Game()

    def test_new_game(self):
        assert self.game is not None and self.game.deck is not None and len(self.game.deck.pile) == 52

    def test_game_flow(self):
        self.game.add_hand("test1")
        self.game.add_hand("test2")
        assert self.game.hands["test1"] is not None
        assert self.game.hands["test2"] is not None
        self.game.serve_all_hands()
        assert self.game.hands["test1"].cards is not None and len(self.game.hands["test1"].cards) == 5
        assert self.game.hands["test2"].cards is not None and len(self.game.hands["test2"].cards) == 5
        assert len(self.game.deck.pile) == 42
        self.game.replace_cards("test1", [0, 1, 2])
        self.game.replace_cards("test2", [0, 1, 2])
        assert self.game.hands["test1"].cards is not None and len(self.game.hands["test1"].cards) == 5
        assert self.game.hands["test2"].cards is not None and len(self.game.hands["test2"].cards) == 5
        assert len(self.game.deck.pile) == 36

