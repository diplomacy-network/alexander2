from diplomacy import Game
from diplomacy.utils.export import to_saved_game_format, from_saved_game_format

import json
game = Game(map_name='standard')
possible_orders = game.get_all_possible_orders()
game.win = 12
saved = to_saved_game_format(game)
game2 = from_saved_game_format(saved)
print(game2.win)
# print(game.map.phase_long(game.get_current_phase()))
# print(game.map.find_next_phase(game.map.phase_long(game.get_current_phase())))
# print(game.get_orderable_locations())
# with open('game_with_arrow.svg', 'w') as out_file:
#     out_file.write(game.render(incl_orders=True, incl_abbrev=True))

next_possible_orders = game.get_all_possible_orders()
# print(next_possible_orders)
# for loc in next_possible_orders:
#   if next_possible_orders[loc]:
#     print('Possible orders at', loc, next_possible_orders[loc])
# print(json.dumps(to_saved_game_format(game), indent=4, sort_keys=True))
