import json
from Player import Player

class Game:
    
    #equivilant to new game
    def __init__(self, players) :
        self.pot = 0
        self.last_pot = 0
        self.board = []
        self.deck = shuffle_new_deck #a fresh deck of cards
        for new_player in players.keys():
            self.remaining_players.append(Player(new_player,
                                                 players[new_player]['url'],
                                                 players[new_player]['money']))
        self.dealer_index = 0
        self.past_moves = []
        self.past_round_moves = []
        self.bet = 0


    def new_hand():
        self.pot = 0
        self.last_pot = 0
        self.board = []
        for player in self.players:
            player.has_folded = False
        self.dealer_index += 1
        self.bet = 0

    #returns the current game state to a specific player
    def game_state(self, playername):
        modified_players = self.players.copy()
        for player in modified_players:
            if player.name != playername:
                del player.hand

        gamestate = {'pot':self.pot,
        'board':self.board,
        'players':modified_players,
        'dealer_index':self.dealer_index,
        'current_player_index':self.current_player_index,
        'past_moves':self.past_moves}

        return json.dumps(gamestate) 