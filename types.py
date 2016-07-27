import collections

# money amounts are stored as integers

SUITS = ["C", "D", "H", "S"]
RANKS = range(2, 15)  # 2 through 14

Card = collections.namedtuple("Card",
    ["suit",  # element of SUITS
     "rank",  # element of RANKS
    ])

PlayerState = collections.namedtuple("PlayerState",
    ["name",      # string identifying the player
     "endpoint",  # URL that returns the player's move
     "money",     # money currently held
     "hole_cards",        # List of hole cards currently held
     "has_folded",        # whether player has folded this hand
     "has_had_turn",      # whether player has had a turn this hand
     "in_pot_this_round"  # money player has put in pot this round
    ])


# The closest we can get to an Enum in python 2.7
class RoundType:
    PRE_FLOP = object()
    FLOP = object()
    TURN = object()
    RIVER = object()

    ROUND_ORDER = [PRE_FLOP, FLOP, TURN, RIVER]


HandState = collections.namedtuple("HandState",
    ["player_states",  # frozendict of player names to PlayerStates
     "flop",   # List of Cards in the flop
     "turn",   # List of Cards in the turn
     "river",  # List of Cards in the river
     "pot",    # money in pot
     "bet",    # amount each player must put in pot to stay in this round
    ])

TableState = collections.namedtuple("TournamentState",
    ["hand_state",    # HandState for the current hand
     "big_blind",     # amount of the big blind for the current hand
     "small_blind",   # amount of the small blind for the current hand
     "player_order",  # List of player names in turn order
     "dealer_name",   # name of the player that deals in the current hand
     "next_player_name_to_act"  # name of next player to take turn
     "current_round",           # the current RoundType being played
                                # None if the round has just ended.
    ])
