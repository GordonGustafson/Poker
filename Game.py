from Player import Player
import cards

import copy
import json
from collections import deque

SMALL_BLIND = 2
BIG_BLIND = 4

# The closest we can get to an Enum in python 2.7
class RoundType():
    PRE_FLOP = object()
    FLOP = object()
    TURN = object()
    RIVER = object()


class Game:
    def __init__(self, players) :
        self.players = deque()
        self.player_dict = {}
        for new_player in players.keys():
            p = Player(new_player,
                       players[new_player]['endpoint'],
                       int(players[new_player]['money']))
            self.players.append(p)
            self.player_dict.update({new_player: p})
        self.dealer = self.players[0]


    def new_hand(self):
        self.pot = 0
        self.board = []
        self.deck = cards.new_shuffled_deck()
        self.hand_moves = []
        self.round_moves = []
        self.bet = 0
        self.last_player = None

        #turning all folded players to False. Giving each player two cards
        for player in self.players:
            player.has_folded = False
            player.hand = self.deck[0:2] # give the player the 'top' two cards
            self.deck   = self.deck[2:]  # the remaining cards form the new deck

        #cycling through players to find the dealer
        while self.dealer != self.players[0]:
            self.players.rotate(-1)

        #setting the dealer to the player after the previous dealer
        self.players.rotate(-1)
        self.dealer = self.players[0]

        #small blind/big blind handling
        for blind in [SMALL_BLIND, BIG_BLIND]:
            self.players.rotate(-1)
            current_player = self.players[0]
            if current_player.money < blind:
                current_player.in_pot += current_player.money
                current_player.all_in = True
                self.pot += current_player.money
                bet = current_player.money
                current_player.money = 0
            else:
                current_player.in_pot += blind
                bet = blind
                self.pot += blind
                current_player.money -= blind

            #storing the changes to big/small blind
            to_append = {'name':current_player.name,'folded':False,'bet':bet}
            self.hand_moves.append(to_append)
            self.round_moves.append(to_append)

        #setting the bet.
        self.bet = BIG_BLIND

        #pointing the queue to the player after the bigblind and assigning to last_player
        self.players.rotate(-1)
        self.last_player = self.players[0]


    def round_start(self, round_type):
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
                player.total_in_pot += player.in_pot
                player.in_pot = 0

            while self.dealer != self.players[0]:
                self.players.rotate(-1)

            #point the queue to the small blind.
            self.players.rotate(-1)
            self.last_player = self.players[0]


    def get_gamestate(self, player):
        """Returns the current game state to a specific player"""

        gamestate = {'pot':self.pot,
            'board':self.board,
            'players': [player.name for player in self.players],
            'hand': player.hand,
            'dealer':self.dealer.name,
            'past_moves':self.round_moves}
        return gamestate


    def last_man_standing(self):
        """Updates the player queue to remove bankrupt players before hand begins and returns True
        if and only if only one player is left with money.
        """
        players_to_remove = [player for player in self.players if player.money <= 0]
        for bankrupt_player in players_to_remove:
            self.players.remove(bankrupt_player)
        return (False if len(self.players) > 1 else True)


    def active_hand(self):
        """Returns True if and only if more than one person didn't fold."""
        return True if sum(1 for player in self.players if not player.has_folded) > 1 else False



    def calculate_side_pot(self, player):
        sidepot = 0
        for p in players:
            sidepot += min(p.total_in_pot, player.total_in_pot)

        return sidepot


    """
        Distributes the pot among the players according to their side_pot values and how
        good their hand is.
    """
    def distribute_wealth(self):
        """Distributes the pot among the players according to their side_pot
        values and how good their hand is.
        """
        def get_gains(total_wealth, num_ppl):
            """Returns a list of earnings for each player by arbitrarily assigning the
            remaining wealth when not perfectly divisible.
            """
            surplus = total_wealth % len(best_players)
            gains = [float(total_wealth)/len(best_players)]*len(best_players)
            for i in range(surplus):
                gains[i] += 1
            return gains

        hands_dict = {player.hand: player for player in self.players}
        hands = [player.hand for player in self.players]

        while self.pot > 0:
            best_hands = cards.best_holdem_hands(self.board, hands)

            equal_dist = float(total_wealth)/len(best_players)
            players_to_remove = []
            count = 0
            # Distribute wealth to players with small side_pots
            for hand in best_hands:
                player = hands_dict[hand]
                if player.all_in:
                    player.side_pot = self.calculate_side_pot(player)
                        if player.side_pot < equal_dist:
                        player.money += player.side_pot
                        self.pot -= player.side_pot
                        players_to_remove.append(hand)
                        count += 1

            #Remove players that earned money from best_players
            for player in players_to_remove:
                best_hands.remove(player)

            if count > 0:
                continue

            else:
                if len(best_hands) == 0 and self.pot > 0:
                    continue
                else:
                    gains = get_gains(self.pot, len(best_hands))
                    for hand in best_hands:
                        hands_dict[hand].money += gains
                        pot -= gains
