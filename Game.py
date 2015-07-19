import json
from Player import Player
from collections import deque

class Game:
    
    #equivilant to new game
    def __init__(self, players) :
        self.pot = 0
        self.last_pot = 0
        self.board = []
        self.deck = shuffle_new_deck #TODO: gordon #a fresh deck of cards
        self.players = Queue() 
        for new_player in players.keys():
            self.players.put(Player(new_player,
                             players[new_player]['endpoint'],
                             players[new_player]['money']))
        dealer = None
        self.hand_moves = []
        self.round_moves = []
        self.bet = 0
        self.last_player = None

    def new_hand():
        self.pot = 0
        self.last_pot = 0
        self.board = []
        self.hand_moves = []
        self.round_moves = []
        for player in self.players:
            player.has_folded = False
            player.hand = deck.two cards # TODO: gordon # give two cards to a player.
        self.bet = 0

    #returns the current game state to a specific player
    def get_game_state(self, playername):
        modified_players = self.players.copy()
        for player in modified_players:
            if player.name != playername:
                del player.hand

        gamestate = {'pot':self.pot,
        'board':self.board,
        'players':modified_players,
        'dealer_index':self.dealer_index,
        'past_moves':self.past_moves}

        return json.dumps(gamestate) 

    """
        Updates the player queue to remove bankrupt players before hand begins and returns True 
        if and only if only one player is left with money.
    """
    def last_man_standing():
        players_to_remove = [player for player in self.players if player.money <= 0]
        for bankrupt_player in players_to_remove:
            self.players.remove(bankrupt_player)
        return (False if len(self.players) > 1 else True)

    """
        Returns True if and only if more than one person didn't fold.
    """
    def active_hand():
        return True if sum(1 for player in self.players if not player.has_folded) > 1 else False

    """
        Adds cards to the board depending on the round being played.
        Round_id == 0: Pre-flop (add 0 cards)
        Round_id == 1: Flop (add 3 cards)
        Round_id == 2: Turn (add 1 card)
        Round_id == 3: River (add 1 card)
    """
    def deal_cards_to_board(round_id):
        #TODO: Gordon
        pass

    """
        Distributes the pot among the players according to their side_pot values and how 
        good their hand is.
    """
    def distribute_wealth(winning_player_lists):
        def get_gains(total_wealth, num_ppl):
            surplus = total_wealth % len(best_players)
            gains = [float(total_wealth)/len(best_players)]*len(best_players)
            for i in range(surplus):
                gains[i] += 1
            return gains

        best_players = winning_player_lists[0]
        second_best_players = winning_player_lists[1]
        equal_dist = float(total_wealth)/len(best_players)
        count = 0
        for player in best_players:
            if player.side_pot > 0 and player.side_pot < equal_dist:
                player.money += player.side_pot
                self.pot -= player.side_pot
                best_players.remove(player)
                count += 1

        if count > 0:
            distribute_wealth([best_players, second_best_players])
        else:
            if len(best_players) == 0 and self.pot > 0:
                distribute_wealth([second_best_players, []])
            else:
                gains = get_gains(self.pot, len(best_players))
                for i in range(len(best_players)):
                    best_players[i].money += gains
