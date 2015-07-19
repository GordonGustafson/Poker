import json
from Player import Player
from collections import deque

class Game:
    #constants
    SMALL_BLIND = 2
    BIG_BLIND = 4


    #equivilant to new game
    def __init__(self, players) :
        self.pot = 0
        self.last_pot = 0
        self.board = []
        self.deck = [] # TODO: gordon should this be None or a list
        self.players = deque() 
        for new_player in players.keys():
            self.players.append(Player(new_player,
                                players[new_player]['endpoint'],
                                players[new_player]['money']))
        self.dealer = self.players[0]
        self.hand_moves = []
        self.round_moves = []
        self.bet = 0
        self.last_player = None


    def new_hand(self):
        self.pot = 0
        self.last_pot = 0
        self.board = []
        self.deck =  shuffle_new_deck # TODO: gordon #a fresh deck of cards
        self.hand_moves = []
        self.round_moves = []

        #turning all folded players to False. Giving each player two cards
        for player in self.players:
            player.has_folded = False
            player.hand = self.deck.two cards # TODO: gordon # give two cards to a player.
        
        #cycling through players to find the dealer
        while self.dealer != self.players[0]:
            self.players.rotate(-1)

        #setting the dealer to the player after the previous dealer
        self.players.rotate(-1)
        self.dealer = self.players[0] 

        #small blind/big blind handling
        for blind in [SMALL_BLIND, BIG_BLIND]
            self.players.rotate(-1)
            current_player = self.players[0]
            if current_player.money < blind:
                current_player.side_pot = current_player.money * self.players.count()
                game.pot += current_player.money
                bet = current_player.money
                current_player.money = 0
            else: 
                bet = blind
                game.pot += blind
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


    """
        Adds cards to the board depending on the round being played.
        Round_id == 0: Pre-flop (add 0 cards)
        Round_id == 1: Flop (add 3 cards)
        Round_id == 2: Turn (add 1 card)
        Round_id == 3: River (add 1 card)

        Also, re-orders the queue for next round
    """
    def round_start(self, number): 
        if number == 1:
            self.board.append() # TODO: gordon #append 3 new cards 
        if number == 2:
            self.board.append() # TODO: gordon #append 1 new card
        if number == 3:
            self.board.append() # TODO: gordon #append 1 new card

        for player in self.players:
            player.total_in_pot += player.in_pot
            player.in_pot = 0

        if number != 0:
            while self.dealer != self.players[0]:
                self.players.rotate(-1)

            #point the queue to the small blind.
            self.players.rotate(-1)
            self.last_player = self.players[0]


    """
        Returns the current game state to a specific player
    """
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
            if player.all_in:
                player.side_pot = self.calculate_side_pot()
                if player.side_pot < equal_dist:
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

    def calculate_side_bot(self):
