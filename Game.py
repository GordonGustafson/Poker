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

    def 


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
