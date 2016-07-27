import types
import player
import cards


def new(players):




def start_hand(self):
    # cycling through players to find the dealer
    # make this a method, it is used multiple times
    while self.dealer != self.players[0]:
        self.players.rotate(-1)

    #setting the dealer to the player after the previous dealer
    self.players.rotate(-1)
    self.dealer = self.players[0]

    #small blind/big blind handling
    for blind in [self.small_blind, self.big_blind]:
        self.players.rotate(-1)
        # TODO: replace this with the betting abstraction
        handle_move(self.players[0], {"bet": blind})
        # posting a blind doesn't count as a chance to act (blinds can still raise later)
        self.players[0].has_had_chance_to_act = False

    #pointing the queue to the player after the big blind
    self.players.rotate(-1)


def play_tournament(self):
    self.small_blind = INITIAL_SMALL_BLIND
    self.big_blind   = INITIAL_BIG_BLIND
    # Removing bankrupt players *before* the first hand ensures
    # that a game with all bankrupt players ends immmediately.
    self.remove_bankrupt_players()
    self.dealer = self.players[0]
    while self.more_than_one_player_left_in_game():
        self.play_hand()
        self.remove_bankrupt_players()


def play_hand(self):
    self.start_hand()
    for round_type in [RoundType.PRE_FLOP, RoundType.FLOP, RoundType.TURN, RoundType.RIVER]:
        if self.more_than_one_player_left_in_hand():
            self.play_round(round_type)
        else:
            break

    # TODO: implement this using stuff from cards.py
    self.distribute_wealth(self.evaluate_hands())

def play_round(self, round_type):
    def round_is_over():
        return all(self.players, lambda player: player.has_had_chance_to_act) \
            and utils.all_equal(player.in_pot_this_round for player in self.players)

    self.start_round(round_type)

    while not round_is_over():
        self.player_turn(self.players[0])
        self.players.rotate(-1)


def start_round(self, round_type):
    if round_type != RoundType.PRE_FLOP:
        for player in self.players:
            player.in_pot_this_round = 0

        while self.dealer != self.players[0]:
            self.players.rotate(-1)

        #point the queue to the small blind.
        self.players.rotate(-1)



def remove_bankrupt_players(self):
    """Removes bankrupt players from the player queue"""
    self.players = [player for player in self.players if player.money > 0]

def more_than_one_player_left_in_game(self):
    return len(self.players) > 1

def more_than_one_player_left_in_hand(self):
    """Returns True if and only if more than one person didn't fold."""
    return len(player for player in self.players if not player.has_folded) > 1
