from Player import Player

class HTTPPlayer(Player):
    def __init__(self, name, endpoint, money):
        self.endpoint = endpoint
        super(HTTPPlayer, self).__init(name, money)

    def get_move(self, gamestate):
        headers = {"content-type": "application/json"}
        r = requests.post(self.endpoint, data=json.dumps(gamestate), headers=headers)
        if r.headers['Content-Type'] != 'application/json':
            return {'name': self.name, 'bet':0}
        else:
            move = r.json()
            # While the Game knows what player this move was for, we record
            # the player's name so that other bots will see it in the game's
            # list of past moves.
            move['name'] = self.name
            return move
