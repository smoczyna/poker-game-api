from model.constants import rank_value, suit_value

__author__ = 'smok'

class Card(object):

    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit

    def __repr__(self):
        return self.rank + '  ' + self.suit

    def __eq__(self, other):
        return self.rank == other.rank and self.suit == other.suit

    def compare(self, other, ranks_only=False):
        if rank_value[self.rank] == rank_value[other.rank]:
            if ranks_only:
                return 0
            else:
                if suit_value[self.suit] > suit_value[other.suit]:
                    return 1
                elif suit_value[self.suit] < suit_value[other.suit]:
                    return -1
                else:
                    return 0
        elif rank_value[self.rank] > rank_value[other.rank]:
            return 1
        else:
            return -1

    def pretty_print(self):
        print("Card:[" + str(self.suit) + "," + str(self.rank) + "]")

    def json(self):
        return {
            "rank": self.rank,
            "suit": self.suit
        }