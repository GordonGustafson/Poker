class Player:
    def __init__(self, name, endpoint, money):
        self.name = name
        self.endpoint = endpoint
        self.money = money
        self.has_folded = False
        self.hand = None
        self.in_pot_total = 0

        # TODO: eliminate these? I think they're all redundant or better stored elsewhere.
        self.side_pot = 0
        self.in_pot_this_round = 0


    def get_move(self, gamestate):
        headers = {"content-type": "application/json"}
        r = requests.post(self.endpoint, data=json.dumps(gamestate), headers=headers)
        if r.headers['Content-Type'] != 'application/json':
            return {'name': self.name, 'fold': True, 'bet':0}
        else:
            move = r.json()
            # While the Game knows what player this move was for, we record
            # the player's name so that other bots will see it in the game's
            # list of past moves.
            move['name'] = self.name
            return move
