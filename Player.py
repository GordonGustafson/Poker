

class Player:
    def __init__(self, name, endpoint, money):
        self.name = name
        self.endpoint = endpoint  
        self.money = money
        self.has_folded = False
        self.hand = None
        self.side_pot = 0
        self.total_bet_this_round = 0