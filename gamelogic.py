import requests

def startGame():
    

def gameLoop():
    


def turn(player):
    game = getGame()

    state = get_game_state(game)
    res = requests.get(player.endpoint, state).json()

    if res["action"] == "fold":
        player.folded = True

    else:
        last_bet = game.get_last_bet()

        if res["action"] == "check":
            #stuff

        elif res["action"] == "call":
            # 
