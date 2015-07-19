import json
from Player import Player

class Game:
    
    #gamestate
    def __init__(self, players) :
        self.pot = 0
        self.board = card
        self.deck = [cards]
        for new_player in players:
            self.remaining_players.append(Player(new_player))
        self.dealer_index = 0
        self.current_player_index = one after the dealer
        self.past_moves = [all previous moves]




    def hand_in_progress():
        #checks to see if a hand is in progress



    def player_move(): #takes a response from the player 
        #modifies the game variables

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