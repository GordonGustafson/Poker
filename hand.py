from cards import players_with_best_holdem_hands
import utils


class Hand:
    def __init__(self, players, deck):
        """
        PRECONDITION: all `players` are non-bankrupt
        """
        assert all(p.money > 0 for p in players.values())

        dealt_cards = utils.chunks_of_sizes(deck, [3, 1, 1] + [2] * len(players))
        # The flop, turn, and river are the first three chunks, then the hands
        flop, turn, river = dealt_cards[:3]
        player_hands = dealt_cards[3:]

        self.players = players            # Dict of names to PlayerStates
        self.flop = flop                  # List of Cards in the flop
        self.turn = turn                  # List of Cards in the turn
        self.river = river                # List of Cards in the river
        self.pot = 0                      # money in pot
        self.max_in_pot_this_round = 0    # round ends when each player
                                          # has bet this amount or folded

        for player, cards in zip(self.players.values(), player_hands):
            player.start_hand(cards)

    def _transfer_money_to_pot(self, player_name, amount):
        player = self.players[player_name]
        assert player.money >= amount, "transferred more than player's money"

        player.money -= amount
        self.pot += amount
        player.in_pot_this_round += amount

    def _post_blind(self, player_name, amount):
        player = self.players[player_name]
        # TODO: handle all-in situations
        self._transfer_money_to_pot(player_name, min(amount, player.money))

    def post_blinds(self, small_blind_name, small_blind_amount,
                          big_blind_name,   big_blind_amount):
        self._post_blind(small_blind_name, small_blind_amount)
        self._post_blind(big_blind_name,   big_blind_amount)
        self.max_in_pot_this_round = big_blind_amount

    def start_round(self):
        for player in self.players.values():
            player.start_round()

    def bet(self, player_name, amount):
        player = self.players[player_name]
        # TODO: if we're going to allow bankrupt players to win the whole pot
        # instead of only the appropriate side-pot, we should prevent them from
        # taking further turns.
        # assert player.money > 0, "bankrupt player made a bet"

        # amount required to call
        min_bet = self.max_in_pot_this_round - player.in_pot_this_round
        did_not_bet_min_when_able = amount < min_bet <= player.money
        bet_more_than_they_have = amount > player.money
        made_illegal_bet = did_not_bet_min_when_able or bet_more_than_they_have
        if made_illegal_bet:
            self.fold(player_name)
        else:
            self._transfer_money_to_pot(player_name, amount)
            self.max_in_pot_this_round = \
                max(self.max_in_pot_this_round, player.in_pot_this_round)
            player.has_had_turn = True

    def fold(self, player_name):
        player = self.players[player_name]
        player.has_folded = True
        player.has_had_turn = True

    def distribute_pot_to_winners(self):
        community_cards = self.flop + self.turn + self.river
        non_folded_players = [p for p in self.players.values() if not p.has_folded]
        winners = players_with_best_holdem_hands(community_cards, non_folded_players)
        # TODO: only distribute whole chips and put leftovers in the next pot
        for winner in winners:
            winner.money += self.pot / len(winners)
        # ATM this is just to obey 'least surprise'
        self.pot = 0

    def bot_info_for_player(self, player_name):
        { "player_info": self.players[player_name],
          "board":
          "pot":
          "min_bet":

    def round_is_over(self):
        non_folded_players = [p for p in self.players.values() if not p.has_folded]
        return (self.only_one_non_folded_player()
            or (all(p.has_had_turn for p in non_folded_players)
                and utils.all_equal([p.in_pot_this_round for p in non_folded_players])))

    def only_one_non_folded_player(self):
        return len([p for p in self.players.values() if not p.has_folded]) == 1

    def non_bankrupt_player_names(self):
        return [n for n, p in self.players.items() if p.money > 0]
