import requests 
import json
import argparse
from Game import Game

def request_player(player, gamestate):
    r = requests.post(player.endpoint, data=gamestate)
    if r.headers['Content-Type'] != 'application/json':
        return {'name': player.name, 'fold': True, 'bet':0}
    else:
        move = r.json()
        move['name'] = player.name
        return move

def player_info_tuple(s):
    return tuple(s.split(','))

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('-player_endpoints', '--player_endpoints', type=player_info_tuple, nargs='+', help='Endpoints of bots playing')
    args = parser.parse_args()

    player_info = {}
    for p in args.player_endpoints:
        player_info[p[0]] = {'endpoint':p[1], 'money':p[2]}

    game = Game(player_info)
    while not game.last_man_standing():
        game.new_hand()
        for round_id in range(4):
            if game.active_hand():
                game.round_start(round_id)    
                next_player = game.players.get()
                while next_player != game.last_player:
                    player_turn(player, request_player(player, game.get_gamestate()))
                    game.players.put(next_player)
            else:
                break
        game.distribute_wealth(game.evaluate_hands())






