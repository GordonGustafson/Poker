# Poker
It's just poker.

Example input:
    {'past_moves': [{'folded': False, 'name': 'Alec', 'bet': 2}, {'folded': False, 'name': 'Lukas', 'bet': 4}, {u'folded': False, u'name': 'Alec', u'bet': 4}, {u'folded': False, u'name': 'Lukas', u'bet': 4}, {u'folded': False, u'name': 'Lukas', u'bet': 4}, {u'folded': False, u'name': 'Lukas', u'bet': 4}], 'money': 24, 'pot': 16, 'hand': [{'rank': 13, 'suit': 'S'}, {'rank': 8, 'suit': 'H'}], 'players': ['Alec', 'Lukas'], 'board': [{'rank': 13, 'suit': 'D'}, {'rank': 3, 'suit': 'C'}, {'rank': 10, 'suit': 'S'}, {'rank': 14, 'suit': 'H'}, {'rank': 6, 'suit': 'D'}], 'dealer': 'Lukas'}

Example output:
    {'folded': False, 'bet': 4}

The bet is the current bet for each round. If the current bet is 4, and you want to raise 2, your bet is 6. If you want to call, just reply with the same bet as the last person.
