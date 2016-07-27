from types import PlayerState


def new(name, endpoint, money):
    return PlayerState(name=name,
                       endpoint=endpoint,
                       money=money,
                       hole_cards=None,  # TODO: allows hole_cards to be None???
                       has_folded=False,
                       has_had_turn=False,
                       in_pot_this_round=0)


def start_hand(player, new_hole_cards):
    return player._replace(hole_cards=new_hole_cards,
                           has_folded=False,
                           has_had_turn=False,
                           in_pot_this_round=0)


def start_round(player):
    return player._replace(has_had_turn=False,
                           in_pot_this_round=0)
