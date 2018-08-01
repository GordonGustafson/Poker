class Player(object):
    def __init__(self, name, money):
        self.name = name
        self.money = money
        self.has_folded = False
        self.hand = None
        self.in_pot_total = 0

    def get_move(self, gamestate):
        return {"bet": 0}
