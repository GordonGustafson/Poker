def turn(player_name, response):
    player = game.players_dict[player_name]

    if response["action"] == "check":
        if game.bet == 0:
            pass
        else:
            player.folded = True
            response["action"] = "fold"

    elif response["action"] == "call":
        # check if player can afford it
        if game.bet - player.in_pot - player.money >= 0:
            call = game.bet - player.in_pot
            game.pot += call
            player.money -= call
            player.in_pot += call
        else:
            response["action"] = "all in"
            player.side_pot = go_all_in(player)

    elif response["action"] == "raise":
        # check if player can afford it
        rays = response["bet"] - player.in_pot
        if rays - player.in_pot - player.money >= 0:
            pot += rays
            bet = rays
            player.money -= rays
            player.in_pot += rays

            game.last_player = player
        else:
            response["action"] == "all in"
            player.side_pot = go_all_in(player)

    else:
        player.folded = True
        response["action"] = "fold"

    move = {"name": player_name, "action": response["action"]}
    if "bet" in response:
        move.update({"bet": bet})

    game.hand_moves.append(move)
    game.round_moves.append(move)

    return (not player.folded)

def go_all_in(player):
    side_pot = game.last_pot + player.money * len(game.remaining_players)
    game.pot += player.money
    player.money = 0
    return side_pot
