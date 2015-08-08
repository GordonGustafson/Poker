import requests
import json
import argparse
from Game import Game, RoundType

def create_player_from_string(string):
    player_data = string.split(',')
    # Requires that the argument order is name, endpoint, money:
    return Player(*player_data)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-players', '--players', type=create_player_from_string, nargs='+', help='The bots to play the game. Format is name,endpoint,money')
    args = parser.parse_args()
    game = Game(args.players)
    game.play()
