class Player:
    def __init__(self, name, endpoint, money):
        self.name = name
        self.endpoint = endpoint
        self.money = money
        self.has_folded = False
        self.hand = None
        self.side_pot = 0
        self.all_in = False
        self.in_pot = 0
        self.total_in_pot = 0
