import types
import player
import cards
import util


def new(players, deck):
    num_players = len(players)
    dealt_cards = util.chunks_of_sizes(deck, [3, 1, 1] + ([2] * num_players))
    # The flop, turn, and river are the first three chunks, then the hands
    flop, turn, river = dealt_cards
    player_hands = dealt_cards[3:]
    players_with_cards = \
        [player.start_hand(p, cards) for p, cards in zip(players, dealt_cards)]

    return HandState(remaining_player_states=players,
                     flop=flop,
                     turn=turn,
                     river=river,
                     pot=0,
                     current_round=types.RoundType.PRE_FLOP,
                     next_player_name_to_act=players[0])


def post_blinds(big_blind_name,   big_blind_amount,
                small_blind_name, small_blind_amount):


def _process_end_of_move(hand):


def _transfer_money_to_pot(hand, player_name, amount):
    new_player = hand.player_states[player_name]._replace(money=money+amount)
    players    = hand.player_states.copy(**{player_name: new_player})
    return hand._replace(player_states=players, pot=hand.pot + amount)


def bet(hand, player_name, amount):
    money_transferred_hand = _transfer_money_to_pot(hand, player_name, amount)
    return money_transferred_hand.


def fold(hand, player_name):


def start_round(hand):
    return hand._replace(players={name, player.start_round(p)
                                  for name, p in hand.player_states.items()}

class Hand:
    def handle_move(self, player, move):

        if player.money == 0:
            # TODO: consider what should happen if this case occurs
            raise Exception("Found bankrupt player during the game")

        # amount required to call
        minimum_bet = self.bet - player.in_pot_this_round
        player_bet = move["bet"]
        did_not_bet_minimum_when_able_to = player_bet < minimum_bet < player.money
        bet_more_than_they_have = player_bet > player.money
        made_illegal_bet = did_not_bet_minimum_when_able_to or bet_more_than_they_have
        if move["folded"] or made_illegal_bet:
            player.has_folded = True
        else:
            player.money -= player_bet
            self.pot += player_bet
            player.in_pot_this_round += player_bet
            player.in_pot_total += player_bet

            if player.money == 0:
                player.all_in = True

            # TODO: figure out how self.bet works
            self.bet = player.in_pot_this_round + player_bet


    def distribute_wealth(self):
        """Distributes the pot among the players according to their side_pot
        values and how good their hand is.
        """
        def get_gains(total_wealth, num_ppl):
            """Returns a list of earnings for each player by arbitrarily assigning the
            remaining wealth when not perfectly divisible.
            """
            surplus = total_wealth % len(best_players)
            gains = [total_wealth / len(best_players)]*len(best_players)
            for i in range(surplus):
                gains[i] += 1
            return gains

        def calculate_side_pot(player):
            sidepot = 0
            for p in self.players:
                sidepot += min(p.in_pot_total, player.in_pot_total)

            return sidepot

        player_list = list(self.players)

        while self.pot > 0:
            best_players = cards.players_with_best_holdem_hands(self.board, player_list)

            equal_dist = float(self.pot)/len(best_players)
            players_to_remove = []
            count = 0
            # Distribute wealth to players with small side_pots
            for player in best_players:
                if player.all_in:
                    player.side_pot = calculate_side_pot(player)
                    if player.side_pot < equal_dist:
                        player.money += player.side_pot
                        self.pot -= player.side_pot
                        players_to_remove.append(player)
                        count += 1

            #Remove players that earned money from best_players
            for player in players_to_remove:
                player_list.remove(player)

            if count > 0:
                continue

            else:
                if len(best_players) == 0 and self.pot > 0:
                    continue
                else:
                    gains = get_gains(self.pot, len(best_players))
                    for i in range(len(best_players)):
                        best_players[i].money += gains[i]
                        self.pot -= gains[i]



