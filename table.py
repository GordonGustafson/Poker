from player import Player
from hand import Hand
import cards

import itertools
from enum import Enum

RoundType = Enum("RoundType", names=["PRE_FLOP", "FLOP", "TURN", "RIVER"])

ROUND_ORDER = [RoundType.PRE_FLOP,
               RoundType.FLOP,
               RoundType.TURN,
               RoundType.RIVER]


class SingleTableTournament:
    # Currently this constructor plays out the entire tournament!
    def __init__(self,
                 move_generator,
                 names_in_turn_order,  # dealer is first
                 starting_money,
                 big_blind,
                 small_blind):
        assert starting_money >= big_blind >= small_blind > 0

        # Some fields are easier to store as instance variables instead of
        # passing them around

        # function from name -> amount bet
        self.move_generator = move_generator
        # List of remaining player names in turn order
        self.remaining_player_order = names_in_turn_order

        # blind amount for hand_state
        self.big_blind = big_blind
        # blind amount for hand_state
        self.small_blind = small_blind

        players = {name: Player(name, starting_money) for name in names_in_turn_order}

        self.play_tournament(players, names_in_turn_order[0])

    def play_tournament(self, remaining_players, first_dealer_name):
        # Removing bankrupt players *before* the first hand ensures
        # that a tournament with all bankrupt players ends immediately.
        for dealer_name in self._turn_sequence_starting_from(first_dealer_name):
            if len(self.remaining_player_order) == 1:
                break
            # players are never removed from the turn sequence!
            elif remaining_players[dealer_name].is_bankrupt():
                continue
            else:
                print("starting hand")
                hand_state = self.play_hand(remaining_players, dealer_name)
                self.remaining_player_order = \
                    [n for n in self.remaining_player_order
                     if n in hand_state.non_bankrupt_player_names()]
                remaining_players = {name: remaining_players[name]
                                     for name in hand_state.non_bankrupt_player_names()}

        print(self.remaining_player_order)
        print(self.remaining_player_order[0] + " is the winner!")

    def play_hand(self, players, dealer_name):
        # TODO: special case first hand of the game
        hand_state = Hand(players, cards.new_shuffled_deck())
        small_blind_name, big_blind_name = \
            itertools.islice(self._turn_sequence_starting_from(dealer_name), 2)

        hand_state.post_blinds(small_blind_name, self.small_blind,
                               big_blind_name,   self.big_blind)

        for round_type in ROUND_ORDER:
            if hand_state.only_one_non_folded_player():
                break
            else:
                self.play_round(hand_state, round_type, dealer_name)

        hand_state.distribute_pot_to_winners()
        return hand_state

    def play_round(self, hand_state, round_type, dealer_name):
        hand_state.start_round()

        small_blind_name, big_blind_name, after_big_blind_name = \
            itertools.islice(self._turn_sequence_starting_from(dealer_name), 3)
        first_player = after_big_blind_name if round_type == RoundType.PRE_FLOP \
                       else small_blind_name

        for player_name in self._turn_sequence_starting_from(first_player):
            if hand_state.round_is_over():
                return
            elif hand_state.players[player_name].has_folded:
                continue
            else:
                # TODO: provide current game state to bots
                self.player_turn(hand_state, player_name)

    def player_turn(self, hand_state, player_name):
        # TODO: enable checking for whether the bot folded
        bet = self.move_generator(player_name)
        print(player_name + " bets " + str(bet))
        if bet == -1:
            hand_state.fold(player_name)
        else:
            hand_state.bet(player_name, bet)

    def _turn_sequence_starting_from(self, starting_player):
        return itertools.dropwhile(lambda name: name != starting_player,
                                   itertools.cycle(self.remaining_player_order))
