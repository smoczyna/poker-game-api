RANKS = ("2", "3", "4", "5", "6", "7", "8", "9", "10", "JACK", "QUEEN", "KING", "ACE")
SUITS = ("CLUB", "DIAMOND", "HEART", "SPADE")

rank_value = {r: i for i, r in enumerate(RANKS)}
suit_value = {s: i for i, s in enumerate(SUITS)}

RESULTS = ("NOTHING", "PAIR", "2PAIRS", "TRIP", "STRAIGHT", "FLUSH", "FULL_HOUSE", "CROWN", "STRAIGHT_FLUSH", "ROYAL_FLUSH")

CARD_REPR = "Card [ {} , {} ]"
HAND_VALUE = "{} value is: [ {} : {} ]"
VALUE_NOT_COUNTED = "winner unknown yet"
WINNING_HAND = "Winning hand: {}"
HAND_NAME = "Hand name: {}"
CARD_NAME_PATTERN = '{}_of_{}s.png'
