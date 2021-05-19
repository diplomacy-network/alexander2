from diplomacy import Game
from diplomacy.engine.game import Power
from diplomacy.utils.export import to_saved_game_format, from_saved_game_format
import pathlib
import json
import html

def printer(game):
    print(game.phase)
    print(game.ordered_units)
    print(game.dislodged)
    print(game.result)
    game.render(incl_orders=True,incl_abbrev=True, output_path="/home/alexw/Code/dnw/alexander2/imgs/1.svg")
    
    print("==================")

def get_all_orders(game: Game, power: str):
        p = game.get_power(power)
        print(p)
        given_orders = game.get_power(p).orders
        print(given_orders)
        units = game.map.units[p.name]
        
        orders = []
        for unit in units:
           if unit in given_orders:
              orders.append("%s %s" % (unit, given_orders[unit]))
           elif(game.phase_type == 'M'):
             orders.append("%s H" % unit)        
        return orders

def return_possible_orders(game):
    # TODO: Better variable names, for now it does its job
    possible_orders = game.get_all_possible_orders()

    possibilities = []
    for power in game.get_map_power_names():
        loc = []
        dicto = {
            "name": power
        }
        units = []
        for loc in game.get_orderable_locations(power):
            cur = {
                "location": loc,
                "instructions": possible_orders[loc]
            }
            units.append(cur)
            # print(loc)
            # print(possible_orders[loc])
        dicto["units"] = units
        possibilities.append(dicto)
    return possibilities

game = Game(map_name="standard")
game.set_orders("FRANCE", ["A PAR-GAS", "A mar-bur"])
# get_all_orders(game, "FRANCE")
power = game.get_power("RUSSIA")
power.clear_units()
power.clear_centers()
game.win = 4

# print(return_possible_orders(game))
game.process()

# Herbst
game.set_orders("FRANCE", ["A GAS-SPA", 
# "A BUR-BEL"
])
game.process()

#  Adjustment
possible = return_possible_orders(game)
game.set_orders("FRANCE", ["A PAR B"])
game.process()
map = game.map
# game._determine_win()
winners = game.outcome[1:]
p = game.get_state()
da = to_saved_game_format(game)

print(game.command)
printer(game)


# print(GameFormatter.previously_applied_orders(game, power))
# with open(r'D:\code\python\alexander2\data2.json', "w") as file:
#     file.write(html.escape(json.dumps(to_saved_game_format(game))))

# print(html.escape(json.dumps(to_saved_game_format(game))))
# print(get_all_orders(game, power))

