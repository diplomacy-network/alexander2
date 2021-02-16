from diplomacy import Game
from diplomacy.engine.game import Power
from diplomacy.utils.export import to_saved_game_format, from_saved_game_format
import pathlib
import json

def printer(game):
    print(game.phase)
    print(game.ordered_units)
    print(game.dislodged)
    print(game.result)
    game.render(incl_orders=True,incl_abbrev=True, output_path="D:\\code\\python\\alexander2\\imgs\\1.svg")
    
    print("==================")

def get_all_orders(game: Game, power: Power):
        given_orders = power.orders
        units = game.map.units[power.name]
        
        orders = []
        for unit in units:
            if unit in given_orders:
                orders.append("%s %s" % (unit, given_orders[unit]))
            elif(game.phase_type == 'M'):
                orders.append("%s H" % unit)        
        return orders


game = Game(map_name="standard")
power = game.get_power("FRANCE")
game.set_orders("FRANCE", ["A PAR - GAS"])
game.process()
print(game.ordered_units)
print(get_all_orders(game, power))

