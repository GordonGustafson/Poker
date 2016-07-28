import utils

import itertools
import random
import collections

SUITS = ["C", "D", "H", "S"]
RANKS = range(2, 15)  # 2 through 14

Card = collections.namedtuple("Card",
    ["suit",  # element of SUITS
     "rank",  # element of RANKS
    ])

CHAR_TO_RANK = {
    "2" : 2,
    "3" : 3,
    "4" : 4,
    "5" : 5,
    "6" : 6,
    "7" : 7,
    "8" : 8,
    "9" : 9,
    "T" : 10,
    "J" : 11,
    "Q" : 12,
    "K" : 13,
    "A" : 14
}


def parse_card(card_string):
    rank_char = card_string[0]
    rank = CHAR_TO_RANK[rank_char]
    suit = card_string[1]
    return Card(suit=suit, rank=rank)

def parse_hand(hand_string):
    card_strings = hand_string.split()
    return [parse_card(card_string) for card_string in card_strings]

# Run this to see a shuffled deck:
# print [card_to_string(card) for card in new_shuffled_deck()]

def new_shuffled_deck():
    unshuffled_pairs = itertools.product(SUITS, RANKS)
    deck = [Card(suit=pair[0], rank=pair[1]) for pair in unshuffled_pairs]
    random.shuffle(deck)
    return deck


class HandType():
    HIGH_CARD = 1
    PAIR = 2
    TWO_PAIR = 3
    THREE_OF_A_KIND = 4
    STRAIGHT = 5
    FLUSH = 6
    FULL_HOUSE = 7
    FOUR_OF_A_KIND = 8
    STRAIGHT_FLUSH = 9


# Return a comparable list that represents the strength of a hand
def five_card_hand_value(hand):
    suits = [card.suit for card in hand]
    ranks = [card.rank for card in hand]

    is_flush = utils.all_equal(suits)

    descending_ranks = sorted(ranks, reverse=True)
    descending_ranks_relative_to_minimum_rank = [rank - min(ranks) for rank in descending_ranks]
    # If the straight is 5-4-3-2-A, the descending ranks will be equal to [14, 5, 4, 3, 2].
    # For other straights, the descending ranks relative to the min rank will be [4, 3, 2, 1, 0]
    is_straight = descending_ranks == [14, 5, 4, 3, 2] or \
                  descending_ranks_relative_to_minimum_rank == [4, 3, 2, 1, 0]

    if is_straight and is_flush:
        return [HandType.STRAIGHT_FLUSH] + descending_ranks
    if is_straight:
        return [HandType.STRAIGHT] + descending_ranks
    if is_flush:
        return [HandType.FLUSH] + descending_ranks

    # Assuming a hand is not a flush or straight, the HandType is determined by
    # what combinations of your cards have the same rank. For example, in a
    # HIGH_CARD hand, none of the cards have the same rank. In a PAIR hand, two
    # cards have the same rank. In a FULL_HOUSE, three cards have the same rank,
    # and another two cards have the same rank.
    rank_frequencies_dict = collections.Counter(ranks)
    rank_frequencies_values_more_than_one = [freq for freq in rank_frequencies_dict.values() if freq > 1]
    hand_type = {
        () : HandType.HIGH_CARD,
        (2,) : HandType.PAIR,
        (2, 2) : HandType.TWO_PAIR,
        (3,) : HandType.THREE_OF_A_KIND,
        (2, 3) : HandType.FULL_HOUSE,
        (4,) : HandType.FOUR_OF_A_KIND
    }[tuple(sorted(rank_frequencies_values_more_than_one))]

    rank_frequency_pairs = rank_frequencies_dict.items()
    frequency_rank_pairs = [(frequency, rank) for (rank, frequency) in rank_frequency_pairs]
    # Sort so that ranks that we have 4-of-a-kind of come before ranks we have
    # 3-of-a-kind of. Python sorts tuples first by their first element and then
    # by their second element, so TWO_PAIR will have the higher ranked pair
    # first, and HIGH_CARD will have the cards sorted by descending rank.
    descending_frequency_rank_pairs = sorted(frequency_rank_pairs, reverse=True)
    # Since the HAND_TYPE comes first in the return value, we will only use the
    # ranks to compare hands of the same type. Thus, we know that ranks will
    # always be compared with ranks that occur with the same frequency in the
    # other hand, and that ranks of higher frequencies will always be compared
    # before ranks of lower frequencies.
    return [hand_type] + [rank for (frequency, rank) in descending_frequency_rank_pairs]



# return a negative, zero or positive number depending on whether left is considered smaller than, equal to, or larger than the second argument:
def compare_five_card_hands(left, right):
    return utils.cmp( five_card_hand_value(left), five_card_hand_value(right) )


def holdem_hand_value(community_cards, hand):
    all_available_cards = community_cards + hand
    all_possible_five_card_hands = itertools.combinations(all_available_cards, 5)
    all_possible_five_card_hand_values = \
        [five_card_hand_value(hand) for hand in all_possible_five_card_hands]
    return max(all_possible_five_card_hand_values)


def compare_holdem_hands(community_cards, left, right):
    return utils.cmp( holdem_hand_value(community_cards, left), holdem_hand_value(community_cards, right) )


def get_holdem_hand_comparator(community_cards):
    """Takes the community cards as an argument and returns a comparator that
    determines which of two two-card hands is better"""
    return lambda left, right: compare_holdem_hands(community_cards, left, right)


def best_holdem_hands(community_cards, hands):
    """Returns all the hands in that are tied for 'first place'"""
    winning_hand = max(hands, key=lambda hand: holdem_hand_value(community_cards, hand))
    comparator = get_holdem_hand_comparator(community_cards)
    return [hand for hand in hands if comparator(hand, winning_hand) == 0]


def players_with_best_holdem_hands(community_cards, players):
    """Returns all the players that will split the pot"""
    winning_player = max(players, key=lambda player: holdem_hand_value(community_cards, player.hole_cards))
    comparator = get_holdem_hand_comparator(community_cards)
    return [player for player in players if comparator(player.hole_cards, winning_player.hole_cards) == 0]
