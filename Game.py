import json
from Player import Player
import Queue

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
