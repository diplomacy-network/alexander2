
from diplomacy.engine.game import Game, Power



def phase_data(game: Game):
    # TODO: Better variable names, for now it does its job
    possibilities = []
    for power in game.powers:
        p = game.powers[power]
        dicto = {
            "name": p.name,
            "unit_count": len(p.units),
            "supply_centers_count": len(p.centers),
            "home_centers_count": len(p.homes)
        }
        possibilities.append(dicto)
    return possibilities

def possible_orders(game: Game):
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

def previously_applied_orders(game: Game, power: Power): 
    given_orders = power.orders
    print(game.get_units(power.name))

    units = power.units
    
    orders = []
    print(units)
    for unit in units:
        if unit in given_orders:
            orders.append("%s %s" % (unit, given_orders[unit]))
        elif(game.phase_type == 'M'):
            orders.append("%s H" % unit)        
    return orders
