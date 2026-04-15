import unittest

from src.model.card import Card
from src.model.hand import Hand


class TestHand(unittest.TestCase):

    def test_one_pair(self):
        hand = Hand('first hand', [
            Card('4', 'CLUB'),
            Card('QUEEN', 'SPADE'),
            Card('4', 'HEART'),
            Card('6', 'CLUB'),
            Card('ACE', 'DIAMOND')
        ])
        hand.sort()
        self.assertTrue(hand.is_one_pair())
        self.assertFalse(hand.is_two_pairs())

    def test_two_pairs(self):
        hand = Hand('second hand', [
            Card('3', 'CLUB'),
            Card('JACK', 'HEART'),
            Card('JACK', 'CLUB'),
            Card('2', 'CLUB'),
            Card('3', 'DIAMOND')
        ])
        hand.sort()
        self.assertTrue(hand.is_two_pairs())
        self.assertFalse(hand.is_one_pair())

    def test_three_of_a_kind(self):
        hand = Hand('second hand', [
            Card('3', 'CLUB'),
            Card('JACK', 'HEART'),
            Card('JACK', 'CLUB'),
            Card('2', 'CLUB'),
            Card('JACK', 'DIAMOND')
        ])
        hand.sort()
        self.assertFalse(hand.is_one_pair())
        self.assertFalse(hand.is_two_pairs())
        self.assertTrue(hand.is_three_of_a_kind())

    def test_four_of_a_kind(self):
        hand = Hand('sixth hand', [
            Card('JACK', 'SPADE'),
            Card('JACK', 'HEART'),
            Card('JACK', 'CLUB'),
            Card('JACK', 'DIAMOND'),
            Card('ACE', 'CLUB')
        ])
        hand.sort()
        self.assertFalse(hand.is_three_of_a_kind())
        self.assertTrue(hand.is_four_of_a_kind())

    def test_full_house(self):
        hand = Hand('seventh hand', [
            Card('JACK', 'SPADE'),
            Card('JACK', 'HEART'),
            Card('JACK', 'CLUB'),
            Card('ACE', 'DIAMOND'),
            Card('ACE', 'CLUB')
        ])
        hand.sort()
        self.assertTrue(hand.is_full_house())

    def test_straight(self):
        hand = Hand('third hand', [
            Card('3', 'CLUB'),
            Card('4', 'HEART'),
            Card('5', 'CLUB'),
            Card('6', 'DIAMOND'),
            Card('7', 'SPADE')
        ])
        hand.sort()
        self.assertTrue(hand.is_straight())

    def test_flush(self):
        hand = Hand('flush hand', [
            Card('2', 'CLUB'),
            Card('6', 'CLUB'),
            Card('7', 'CLUB'),
            Card('JACK', 'CLUB'),
            Card('ACE', 'CLUB')
        ])
        hand.sort()
        self.assertTrue(hand.is_flush())
        self.assertFalse(hand.is_straight_flush())

    def test_royal_flush(self):
        hand = Hand('royal hand', [
            Card('10', 'HEART'),
            Card('JACK', 'HEART'),
            Card('QUEEN', 'HEART'),
            Card('KING', 'HEART'),
            Card('ACE', 'HEART')
        ])
        hand.sort()
        self.assertTrue(hand.is_royal_flush())

    def test_which_nothing_hand_is_higher(self):
        hand3 = Hand('third hand', [
            Card('JACK', 'SPADE'),
            Card('JACK', 'HEART'),
            Card('QUEEN', 'CLUB'),
            Card('ACE', 'DIAMOND'),
            Card('ACE', 'CLUB')
        ])
        hand3.sort()
        hand4 = Hand('fourth hand', [
            Card('JACK', 'CLUB'),
            Card('JACK', 'DIAMOND'),
            Card('QUEEN', 'DIAMOND'),
            Card('ACE', 'HEART'),
            Card('ACE', 'SPADE')
        ])
        hand4.sort()
        self.assertTrue(hand3.compare(hand4), "hand3 should be higher than hand4")
        hand3.replace_card(2, Card('KING', 'DIAMOND'))
        self.assertTrue(hand4.compare(hand3), "hand4 should be higher than hand3 this time")

    def test_evaluate_hand(self):
        hand = Hand('first hand', [
            Card('4', 'CLUB'),          # index 4
            Card('QUEEN', 'SPADE'),     # index 1
            Card('4', 'HEART'),         # index 3
            Card('6', 'CLUB'),          # index 2
            Card('ACE', 'DIAMOND')      # index 0
        ])
        hand.sort()
        self.assertEqual(hand.evaluate(), 'PAIR')
        hand.replace_card(2, Card('QUEEN', 'DIAMOND'))
        self.assertEqual(hand.evaluate(), '2PAIRS')
        hand.replace_card(0, Card('QUEEN', 'CLUB'))
        self.assertEqual(hand.evaluate(), 'FULL_HOUSE')
        hand.replace_card(3, Card('QUEEN', 'HEART'))
        self.assertEqual(hand.evaluate(), 'CROWN')


# if __name__ == '__main__':
#     unittest.main()