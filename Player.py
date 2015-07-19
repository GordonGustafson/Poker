

class Player:
    def __init__(self, name, url, money):
        self.name = name
        self.endpoint = url  
        self.money = money
        self.has_folded = False
        self.hand = None
        self.total_bet_this_round = 0