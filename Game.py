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
    def __init__(self, players):
        self.players = deque(players)

    def play_until_single_winner(self):
        self.small_blind = INITIAL_SMALL_BLIND
        self.big_blind   = INITIAL_BIG_BLIND
        # Removing bankrupt players *before* the first hand ensures
        # that a game with all bankrupt players ends immmediately.
        self.remove_bankrupt_players()
        self.dealer = self.players[0]
        self.board = []
        while len(self.players) > 1:
            self.play_hand()
            self.remove_bankrupt_players()

    def play_hand(self):
        self.start_hand()
        for round_type in [RoundType.PRE_FLOP, RoundType.FLOP, RoundType.TURN, RoundType.RIVER]:
            if self.more_than_one_player_left_in_hand():
                self.play_round(round_type)
            else:
                break

        self.distribute_winnings()

    def all_players_met_highest_bet_or_folded(self):
        largest_in_pot_total = max(player.in_pot_total for player in self.players)
        return all(player.in_pot_total == largest_in_pot_total
                   or player.has_folded
                    for player in self.players)

    def play_round(self, round_type):
        self.start_round(round_type)

        num_active_players = len([player for player in self.players
                                 if not player.has_folded
                                  and player.money > 0])
        for _ in range(0, num_active_players):
            self.player_turn(self.players[0])
            self.players.rotate(-1)

        while not self.all_players_met_highest_bet_or_folded():
            self.player_turn(self.players[0])
            self.players.rotate(-1)

    def get_gamestate(self, player):
        """Returns the current game state to a specific player"""
        return {'pot': sum(player.in_pot_total for player in self.players),
                'board': self.board,
                # TODO: make this JSON friendly?
                'players': self.players,
                'hand': player.hand,
                'money': player.money,
                'dealer': self.dealer.name,
                'past_moves': self.round_moves}

    def player_turn(self, player):
        move = player.get_move(self.get_gamestate(player))
        self.handle_move(player, move)

    def handle_move(self, player, move):

        if player.money == 0:
            # TODO: consider what should happen if this case occurs
            raise Exception("Found bankrupt player during the game")

        # amount required to call
        minimum_bet = (max(player.in_pot_total for player in self.players)
                       - player.in_pot_total)
        player_bet = move["bet"]
        did_not_bet_minimum_when_able_to = player_bet < minimum_bet < player.money
        bet_more_than_they_have = player_bet > player.money
        made_illegal_bet = did_not_bet_minimum_when_able_to or bet_more_than_they_have
        if move["folded"] or made_illegal_bet:
            player.has_folded = True
        else:
            player.money -= player_bet
            player.in_pot_total += player_bet

        self.hand_moves.append(move)
        self.round_moves.append(move)

    def start_hand(self):
        self.board = []
        self.deck = cards.new_shuffled_deck()
        self.hand_moves = []
        self.round_moves = []

        for player in self.players:
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
            while self.dealer != self.players[0]:
                self.players.rotate(-1)

            #point the queue to the small blind.
            self.players.rotate(-1)

    def remove_bankrupt_players(self):
        """Removes bankrupt players from the player queue"""
        self.players = deque(player for player in self.players if player.money > 0)

    def more_than_one_player_left_in_hand(self):
        """Returns True if and only if more than one person didn't fold."""
        return len(player for player in self.players if not player.has_folded) > 1

    def _get_winnings_map(self):
        """
        Returns a dictionary from player names to the amount of money they won
        from the current pot.
        """
        # TODO: implement side pots
        # TODO: implement ties
        winning_player = max(self.players,
                             key=lambda player: holdem_hand_value(self.community_cards,
                                                                  player.hand))
        return {winning_player.name: sum(p.in_pot_total for p in players)}

        # # Folded hands can't compete for any pots.
        # pot_thresholds = set(player.in_pot_total for player in self.players
        #                      if not player.has_folded)

    def distribute_winnings(self):
        for winning_player_name, amount_won in self._get_winnings_map().iteritems():
            winning_player = next(p for p in self.players
                                  if p.name == winning_player_name)
            winning_player.money += amount_won

