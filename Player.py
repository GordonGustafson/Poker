

class Player:
    def __init__(self, id, url, money):
        self.id = id
        self.endpoint = url  
        self.money = money
        self.has_folded = False
        self.hand = None