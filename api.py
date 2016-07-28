def player_turn(self, player):
    def get_gamestate(self, player):
        """Returns the current game state to a specific player"""
        return {'pot':self.pot,
                'board':self.board,
                'players': [player.name for player in self.players],
                'hand': player.hand,
                'money': player.money,
                'dealer':self.dealer.name}

    move = player.get_move(get_gamestate(player))
    self.handle_move(player, move)
