import unittest
from cards import *

class FiveCardHandsTest(unittest.TestCase):
    def assert_value_equals(self, hand_string, expected_value):
        hand = parse_hand(hand_string)
        value = five_card_hand_value(hand)
        self.assertEqual(value, expected_value)

    def assert_comparison_equals(self, left_hand_string, right_hand_string, expected_value):
        left_hand  = parse_hand(left_hand_string)
        right_hand = parse_hand(right_hand_string)
        self.assertEqual(compare_five_card_hands(left_hand, right_hand), expected_value)

    def test_hand_values(self):
        self.assert_value_equals("TC 9D 6H 3S 2C", [HandType.HIGH_CARD,       10, 9, 6, 3, 2])
        self.assert_value_equals("TC TD 6H 3S 2C", [HandType.PAIR,            10, 6, 3, 2])
        self.assert_value_equals("TC TD 6H 6S 2C", [HandType.TWO_PAIR,        10, 6, 2])
        self.assert_value_equals("TC TD TH 6S 2C", [HandType.THREE_OF_A_KIND, 10, 6, 2])
        self.assert_value_equals("TC 9D 8H 7S 6C", [HandType.STRAIGHT,        10, 9, 8, 7, 6])
        self.assert_value_equals("TC 9C 6C 3C 2C", [HandType.FLUSH,           10, 9, 6, 3, 2])
        self.assert_value_equals("TC TD TS 9H 9C", [HandType.FULL_HOUSE,      10, 9])
        self.assert_value_equals("TC TD TS TH 9C", [HandType.FOUR_OF_A_KIND,  10, 9])
        self.assert_value_equals("TC 9C 8C 7C 6C", [HandType.STRAIGHT_FLUSH,  10, 9, 8, 7, 6])

    def test_cross_hand_type_comparisons(self):
        self.assert_comparison_equals("TC TD 6H 3S 2C", "TC 9D 6H 3S 2C", 1)
        self.assert_comparison_equals("TC TD 6H 6S 2C", "TC TD 6H 3S 2C", 1)
        self.assert_comparison_equals("TC TD TH 6S 2C", "TC TD 6H 6S 2C", 1)
        self.assert_comparison_equals("TC 9D 8H 7S 6C", "TC TD TH 6S 2C", 1)
        self.assert_comparison_equals("TC 9C 6C 3C 2C", "TC 9D 8H 7S 6C", 1)
        self.assert_comparison_equals("TC TD TS 9H 9C", "TC 9C 6C 3C 2C", 1)
        self.assert_comparison_equals("TC TD TS TH 9C", "TC TD TS 9H 9C", 1)
        self.assert_comparison_equals("TC 9C 8C 7C 6C", "TC TD TS TH 9C", 1)

        # these are just the last paragraph reversed:
        self.assert_comparison_equals("TC 9D 6H 3S 2C", "TC TD 6H 3S 2C", -1)
        self.assert_comparison_equals("TC TD 6H 3S 2C", "TC TD 6H 6S 2C", -1)
        self.assert_comparison_equals("TC TD 6H 6S 2C", "TC TD TH 6S 2C", -1)
        self.assert_comparison_equals("TC TD TH 6S 2C", "TC 9D 8H 7S 6C", -1)
        self.assert_comparison_equals("TC 9D 8H 7S 6C", "TC 9C 6C 3C 2C", -1)
        self.assert_comparison_equals("TC 9C 6C 3C 2C", "TC TD TS 9H 9C", -1)
        self.assert_comparison_equals("TC TD TS 9H 9C", "TC TD TS TH 9C", -1)
        self.assert_comparison_equals("TC TD TS TH 9C", "TC 9C 8C 7C 6C", -1)

        self.assert_comparison_equals("TC 9D 6H 3S 2C", "TC 9D 6H 3S 2C", 0)
        self.assert_comparison_equals("TC TD 6H 3S 2C", "TC TD 6H 3S 2C", 0)
        self.assert_comparison_equals("TC TD 6H 6S 2C", "TC TD 6H 6S 2C", 0)
        self.assert_comparison_equals("TC TD TH 6S 2C", "TC TD TH 6S 2C", 0)
        self.assert_comparison_equals("TC 9D 8H 7S 6C", "TC 9D 8H 7S 6C", 0)
        self.assert_comparison_equals("TC 9C 6C 3C 2C", "TC 9C 6C 3C 2C", 0)
        self.assert_comparison_equals("TC TD TS 9H 9C", "TC TD TS 9H 9C", 0)
        self.assert_comparison_equals("TC TD TS TH 9C", "TC TD TS TH 9C", 0)
        self.assert_comparison_equals("TC 9C 8C 7C 6C", "TC 9C 8C 7C 6C", 0)


    def test_within_hand_type_comparison(self):
        self.assert_comparison_equals("TC 9D 6H 3S 2C", "AC 8D 5H 3S 2C", -1)

        self.assert_comparison_equals("TC TD 7H 3S 2C", "TC TD 6H 3S 2C", 1)
        self.assert_comparison_equals("JC JD 6H 3S 2C", "TC TD AH 3S 2C", 1)

        self.assert_comparison_equals("QC QD 6H 6S 2C", "TC TD 9H 9S 2C", 1)
        self.assert_comparison_equals("QC QD 6H 6S 2C", "QC QD 9H 9S 2C", -1)

        self.assert_comparison_equals("TC TD TH 6S 2C", "AC AD AH 6S 2C", -1)
        self.assert_comparison_equals("AC AD AH 6S 3C", "AC AD AH 6S 2C", 1)

        self.assert_comparison_equals("9D 8H 7S 6C 5C", "TC 9D 8H 7S 6C", -1)

        self.assert_comparison_equals("TC 9C 6C 3C 2C", "JC 9C 6C 3C 2C", -1)

        self.assert_comparison_equals("TC TD TS 9H 9C", "TC TD TS JH JC", -1)
        self.assert_comparison_equals("TC TD TS 9H 9C", "2C 2D 2S JH JC", 1)

        self.assert_comparison_equals("2C 2D 2S 2H 9C", "AC AD AS AH 9C", -1)
        self.assert_comparison_equals("2C 2D 2S 2H 9C", "2C 2D 2S 2H TC", -1)

        self.assert_comparison_equals("AC 2C 3C 4C 5C", "TC JC QC KC AC", -1)
        self.assert_comparison_equals("2C 3C 4C 5C 6C", "3C 4C 5C 6C 7C", -1)



class HoldemHandsTest(unittest.TestCase):
    def assert_value_equals(self, community_string, hand_string, expected_value):
        community_cards = parse_hand(community_string)
        hand = parse_hand(hand_string)
        value = holdem_hand_value(community_cards, hand)
        self.assertEqual(value, expected_value)

    def assert_comparator_result_equals(self, left_hand_string, right_hand_string, comparator, expected_value):
        left_hand  = parse_hand(left_hand_string)
        right_hand = parse_hand(right_hand_string)
        self.assertEqual( comparator(left_hand, right_hand), expected_value)

    def assert_best_holdem_hands_equals(self, community_cards_string, hand_strings, expected_hand_strings):
        community_cards = parse_hand(community_cards_string)
        hands          = [parse_hand(hand_string) for hand_string in hand_strings]
        expected_hands = [parse_hand(hand_string) for hand_string in expected_hand_strings]
        best_hands = best_holdem_hands(community_cards, hands)
        # don't consider ordering when comparing the results:
        self.assertEqual(sorted(best_hands), sorted(expected_hands))

    def test_hand_values(self):
        self.assert_value_equals("TC 9D 6H 3S 2C", "AC KC", [HandType.HIGH_CARD,       14, 13, 10, 9, 6])
        self.assert_value_equals("TC 9D 6H 3S 2C", "6D KC", [HandType.PAIR,            6, 13, 10, 9])
        self.assert_value_equals("TC TD 4H 6S 2C", "6C KC", [HandType.TWO_PAIR,        10, 6, 13])
        self.assert_value_equals("TC TD 7H 6S 2C", "TS KC", [HandType.THREE_OF_A_KIND, 10, 13, 7])
        self.assert_value_equals("TC 9D 8H AS 3C", "7C JC", [HandType.STRAIGHT,        11, 10, 9, 8, 7])
        self.assert_value_equals("TD 9D 6C 3C 2C", "AC KC", [HandType.FLUSH,           14, 13, 6, 3, 2])
        self.assert_value_equals("TC TD TS 9H 9C", "AC AC", [HandType.FULL_HOUSE,      10, 14])
        self.assert_value_equals("TC TD TS 2H 9C", "TH KC", [HandType.FOUR_OF_A_KIND,  10, 13])
        self.assert_value_equals("TC 9C 8C 7C 6C", "AC KC", [HandType.STRAIGHT_FLUSH,  10, 9, 8, 7, 6])

    def test_holdem_hand_comparator(self):
        comparator = get_holdem_hand_comparator(parse_hand("TC 9C 6C 3S 2H"))
        self.assert_comparator_result_equals("AS 4D", "KS 5D", comparator, 1)
        self.assert_comparator_result_equals("2S 4D", "KS 5D", comparator, 1)
        self.assert_comparator_result_equals("2S 4D", "3D 5D", comparator, -1)
        self.assert_comparator_result_equals("TS 4D", "3D 2D", comparator, -1)
        self.assert_comparator_result_equals("TS TD", "3D 2D", comparator, 1)
        self.assert_comparator_result_equals("TS TD", "4D 5D", comparator, -1)
        self.assert_comparator_result_equals("7S 8D", "4D 5D", comparator, 1)
        self.assert_comparator_result_equals("7S 8D", "AC 4C", comparator, -1)
        self.assert_comparator_result_equals("7C 8C", "AC 4C", comparator, 1)

    def test_best_holdem_hands(self):
        self.assert_best_holdem_hands_equals("TC 9C 6C 3S 2H", ["AS 4D", "KS 5D", "2S 4D", "3D 5H"], ["3D 5H"])
        self.assert_best_holdem_hands_equals("TC 9C 6C 3S 2H", ["TH 4D", "3D 2D", "TS TD", "3D 5D"], ["TS TD"])
        self.assert_best_holdem_hands_equals("TC 9C 6C 3S 2H", ["TH 9D", "TS 9H", "3D 2D", "3D 5D"], ["TH 9D", "TS 9H"])
