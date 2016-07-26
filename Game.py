from Player import Player
import cards

from collections import deque


# The closest we can get to an Enum in python 2.7
class RoundType():
    PRE_FLOP = object()
    FLOP = object()
    TURN = object()
    RIVER = object()

INITIAL_SMALL_BLIND = 2
INITIAL_BIG_BLIND = 4

class Game:
    def __init__(self, players) :
        self.players = deque(players)

    def play(self):
        self.small_blind = INITIAL_SMALL_BLIND
        self.big_blind   = INITIAL_BIG_BLIND
        # Removing bankrupt players *before* the first hand ensures
        # that a game with all bankrupt players ends immmediately.
        self.remove_bankrupt_players()
        self.dealer = self.players[0]
        while self.more_than_one_player_left_in_game():
            play_hand():
            self.remove_bankrupt_players()

    def play_hand(self):
        self.start_hand()
        for round_type in [RoundType.PRE_FLOP, RoundType.FLOP, RoundType.TURN, RoundType.RIVER]:
            if self.more_than_one_player_left_in_hand():
                self.play_round(round_type)
            else:
                break;

        # TODO: implement this using stuff from cards.py
        self.distribute_wealth(self.evaluate_hands())

    def play_round(self, round_type)
        def round_is_over():
            return all(lambda player: player.has_had_chance_to_act) \
                and utils.all_equal(player.in_pot_this_round for player in self.players)

        self.start_round(round_type)

        while not round_is_over():
            player_turn(self.players[0])
            self.players.rotate(-1)


    def player_turn(self, player):
        def get_gamestate(self, player):
            """Returns the current game state to a specific player"""
            return {'pot':self.pot,
                    'board':self.board,
                    'players': [player.name for player in self.players],
                    'hand': player.hand,
                    'money': player.money,
                    'dealer':self.dealer.name,
                    'past_moves':self.round_moves}

        move = player.get_move(get_gamestate(player))
        self.handle_move(player, move)


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

        self.hand_moves.append(move)
        self.round_moves.append(move)


    def start_hand(self):
        self.pot = 0
        self.board = []
        self.deck = cards.new_shuffled_deck()
        self.hand_moves = []
        self.round_moves = []
        self.bet = 0

        for player in self.players:
            player.in_pot_this_round = 0
            player.in_pot_total = 0
            player.has_folded = False
            player.hand = self.deck[0:2] # give the player the 'top' two cards
            self.deck   = self.deck[2:]  # the remaining cards form the new deck

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


    def start_round(self, round_type):
        """Adds cards to the board depending on the round being played.
        Also, re-orders the queue for next round
        """
        if round_type == RoundType.FLOP:
            self.board.extend(self.deck[0:3]) # add the top three cards to the board
            self.deck = self.deck[3:]         # the remaining cards form the new deck
        if round_type == RoundType.TURN:
            self.board.extend(self.deck[0:1])
            self.deck = self.deck[1:]
        if round_type == RoundType.RIVER:
            self.board.extend(self.deck[0:1])
            self.deck = self.deck[1:]


        if round_type != RoundType.PRE_FLOP:
            for player in self.players:
                player.in_pot_total += player.in_pot_this_round
                player.in_pot_this_round = 0

            while self.dealer != self.players[0]:
                self.players.rotate(-1)

            #point the queue to the small blind.
            self.players.rotate(-1)



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



    def remove_bankrupt_players(self):
        """Removes bankrupt players from the player queue"""
        self.players = deque(player for player in self.players if player.money > 0)

    def more_than_one_player_left_in_game(self):
        return len(self.players) > 1

    def more_than_one_player_left_in_hand(self):
        """Returns True if and only if more than one person didn't fold."""
        return len(player for player in self.players if not player.has_folded) > 1
