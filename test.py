from diplomacy import Game
from diplomacy.engine.game import Power
from diplomacy.utils.export import to_saved_game_format, from_saved_game_format
from service import GameFormatter
import pathlib
import json
import html

def printer(game):
    print(game.phase)
    print(game.ordered_units)
    print(game.dislodged)
    print(game.result)
    game.render(incl_orders=True,incl_abbrev=True, output_path="D:\\code\\python\\alexander2\\imgs\\1.svg")
    
    print("==================")

# def get_all_orders(game: Game, power: str):
#         given_orders = game.get_power(power).orders
#         units = game.map.units[power.name]
        
#         orders = []
#         for unit in units:
#             if unit in given_orders:
#                 orders.append("%s %s" % (unit, given_orders[unit]))
#             elif(game.phase_type == 'M'):
#                 orders.append("%s H" % unit)        
#         return orders


game = Game(map_name="standard")
power = game.get_power("FRANCE")
game.set_orders("FRANCE", ["A PAR - GAS"])
print(game.map.locs)
game.process()
# print(GameFormatter.previously_applied_orders(game, power))
# with open(r'D:\code\python\alexander2\data2.json', "w") as file:
#     file.write(html.escape(json.dumps(to_saved_game_format(game))))

# print(html.escape(json.dumps(to_saved_game_format(game))))
# print(get_all_orders(game, power))

