from src.model.constants import rank_value, suit_value, RESULTS

__author__ = 'smok'

class Hand(object):

    def __init__(self, name, cards=None):
        self.name = name
        self.cards = cards if cards is not None else []
        self.is_resolved = False
        self.value = 0

    def json(self):
        return {
            "name": self.name,
            "cards": [card.json() for card in self.cards]
        }

    def is_served(self):
        return True if len(self.cards) == 5 else False

    def add_cards(self, cards):
        if cards is not None and len(cards) == 5:
            self.cards = cards

    def pretty_print(self, show_sorted=False):
        print("Hand: ", self.name)
        if show_sorted:
            self.sort()
        for card in self.cards:
            print(card.rank, card.suit)
        print('---')

    def sort(self):
        self.cards.sort(key=lambda c: (rank_value[c.rank], suit_value[c.suit]), reverse=True)

    def compare(self, other, ranks_only=False):
        self.sort()
        other.sort()
        res = 0
        for i in range(len(self.cards)):
            if self.cards[i].compare(other.cards[i], ranks_only) == 1:
                res = 1
                break
            elif self.cards[i].compare(other.cards[i], ranks_only) == -1:
                res = -1
                break
            else:
                continue

        if res == 0:
            for i in range(len(self.cards)):
                if self.cards[i] > other.cards[i]:
                    res = 1
                    break
                elif self.cards[i] < other.cards[i]:
                    res = -1
                    break

        return res

    def replace_card(self, index, card):
        self.cards[index] = card
        self.is_resolved = False

    def evaluate(self):
        checks = [
            (self.is_royal_flush, 'ROYAL_FLUSH'),
            (self.is_straight_flush, 'STRAIGHT_FLUSH'),
            (self.is_four_of_a_kind, 'CROWN'),
            (self.is_full_house, 'FULL_HOUSE'),
            (self.is_flush, 'FLUSH'),
            (self.is_straight, 'STRAIGHT'),
            (self.is_three_of_a_kind, 'TRIP'),
            (self.is_two_pairs, '2PAIRS'),
            (self.is_one_pair, 'PAIR'),
        ]
        for check, result in checks:
            if check():
                self.value = RESULTS.index(result)
                return result

        self.value = 0
        return 'NOTHING'

    def get_value(self):
        if not self.is_resolved:
            self.evaluate()
            self.is_resolved = True

        return self.value

    def group_cards(self):
        ranks = {}
        for card in self.cards:
            if len(ranks) == 0 or card.rank not in ranks:
                ranks[card.rank] = [card]
            else:
                ranks[card.rank].append(card)

        return ranks

    def check_pairs(self):
        pairs = 0
        ranks = self.group_cards()
        for v in ranks.values():
            if len(v) == 2:
                pairs += 1
        return pairs

    def is_one_pair(self):
        pairs = self.check_pairs()
        return pairs == 1

    def is_two_pairs(self):
        pairs = self.check_pairs()
        return pairs == 2

    def is_three_of_a_kind(self):
        ranks = self.group_cards()
        for v in ranks.values():
            if len(v) == 3:
                return True
        return False

    def is_straight(self):
        seq = None
        ranks = self.group_cards()
        for v in ranks.values():
            if len(v) == 1:
                if seq is None:
                    seq = rank_value[v[0].rank]
                else:
                    if seq - 1 == rank_value[v[0].rank]:
                        seq -= 1
                    else:
                        return False
            else:
                return False
        return True

    def is_flush(self):
        suit = self.cards[0].suit
        for c in self.cards:
            if c.suit != suit:
                return False
        return True

    def is_full_house(self):
        ranks = self.group_cards()
        has_tree = False
        has_two = False
        if len(ranks) != 2:
            return False
        else:
            for v in ranks.values():
                if len(v) == 3:
                    has_tree = True
                elif len(v) == 2:
                    has_two = True

            return has_tree and has_two

    def is_four_of_a_kind(self):
        ranks = self.group_cards()
        for v in ranks.values():
            if len(v) == 4:
                return True
        return False

    def is_straight_flush(self):
        if self.is_straight():
            suit = self.cards[0].suit
            for c in self.cards:
                if c.suit != suit:
                    return False
            return True
        else:
            return False

    def is_royal_flush(self):
        if self.is_straight_flush() and self.cards[0].rank == 'ACE':
            return True
        else:
            return False


