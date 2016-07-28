# import requests
# import json
# import argparse
# from Game import Game, RoundType

# def create_player_from_string(string):
#     player_data = string.split(',')
#     # Requires that the argument order is name, endpoint, money:
#     return Player(*player_data)

# if __name__ == "__main__":
#     parser = argparse.ArgumentParser()
#     parser.add_argument('-players', '--players', type=create_player_from_string, nargs='+', help='The bots to play the game. Format is name,endpoint,money')
#     args = parser.parse_args()
#     game = Game(args.players)
#     game.play()

from table import SingleTableTournament

ALWAYS_FOLDS = "always_folds"
ALWAYS_BETS_FIVE = "always_bets_five"

def move_generator(name):
    if name == ALWAYS_FOLDS:
        return -1
    elif name == ALWAYS_BETS_FIVE:
        return 5
    else:
        raise ValueError("Unrecognized name in move_generator")

if __name__ == "__main__":
    players_in_turn_order = [ALWAYS_BETS_FIVE, ALWAYS_FOLDS]
    starting_money = 20
    big_blind = 4
    small_blind = 2
    tournament = SingleTableTournament(move_generator,
                                       players_in_turn_order,
                                       starting_money,
                                       big_blind,
                                       small_blind)
