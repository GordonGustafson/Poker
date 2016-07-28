class Player:
    def __init__(self, name, money):
        self.name = name            # string identifying the player
        self.money = money          # money currently held
        self.hole_cards = None      # List of hole cards currently held
        self.has_folded = False     # whether player has folded this hand
        self.has_had_turn = False   # whether player has had a turn this hand
        self.in_pot_this_round = 0  # money player has put in pot this round

    def start_hand(self, new_hole_cards):
        self.hole_cards = new_hole_cards
        self.has_folded = False
        self.has_had_turn = False
        self.in_pot_this_round = 0

    def start_round(self):
        self.has_had_turn = False
        self.in_pot_this_round = 0

    def is_bankrupt(self):
        # TODO: consider how to handle negative money
        return self.money <= 0
