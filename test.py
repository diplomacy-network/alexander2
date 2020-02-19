from diplomacy import Game
from diplomacy.utils.export import to_saved_game_format

import json
game = Game(map_name='standard')
next_possible_orders = game.get_all_possible_orders()
print(next_possible_orders)
# for loc in next_possible_orders:
#   if next_possible_orders[loc]:
#     print('Possible orders at', loc, next_possible_orders[loc])
# print(json.dumps(to_saved_game_format(game), indent=4, sort_keys=True))
