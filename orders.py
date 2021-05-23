import random
from pathlib import Path
from typing import Dict
from diplomacy import Game
from diplomacy.engine.game import Power
from diplomacy.utils.export import to_saved_game_format, from_saved_game_format
import json
import base64

# PARAMETERS
A = 1
B = 4
C = 16

THRESHOLD_PLAY_ALTERNATIVE = 50

# Sw = {"SPRING": 1000, "FALL": 1000, "WINTER": 0}
# Cw = {"SPRING": 1000, "FALL": 1000, "WINTER": 0}
# Aw = {"SPRING": 700, "FALL": 600, "WINTER": 0}
# Dw = {"SPRING": 300, "FALL": 400, "WINTER": 1000}

Sw = {"SPRING": 1000, "FALL": 1000, "WINTER": 0}
Cw = {"SPRING": 1000, "FALL": 1000, "WINTER": 0}
Aw = {"SPRING": 700, "FALL": 600, "WINTER": 100}
Dw = {"SPRING": 300, "FALL": 400, "WINTER": 1000}

Pw = [1000, 100, 30, 10, 6, 5, 4, 3, 2, 1]


def get_best_orders(game: Game, power: Power):

    
    # Unit Positions dict("location" => power:"POWER", type: "A", "loc": location)
    unit_positions = {}
    for power_name, locations in game.get_units().items():
        for l in locations:
            unit_positions[l[2:]] = {
                "power": power_name, "type": l[0], "loc": l[2:]}

    # Center Ownerships
    center_ownership = {}
    for power_name, location in game.get_centers().items():
        for l in location:
            for r in game.map.find_coasts(l):
                center_ownership[r] = power_name

    # Calculating Powersizes
    power_sizes = {}
    p: Power
    for p in game.powers.values():
        num_sc = len(p.centers)
        power_sizes[p.name] = A * num_sc ^ 2 + B * num_sc + C

    # Assigning Attack and Defense Values
    attack_values = {}
    defense_values = {}

    for loc in game.map.locs:
        loc = loc.upper()
        attack_values[loc] = 0
        defense_values[loc] = 0
        if (
            center_ownership.get(loc) != power.name
            and center_ownership.get(loc) is not None
        ):
            attack_values[loc] = power_sizes.get(center_ownership.get(loc))
        if center_ownership.get(loc) == power.name:
            # Check if location can be attacked
            attackable_powers = [0]
            unit: dict
            for unit in unit_positions.values():
                if game.map.abuts(unit.get("type"), unit.get("loc"), "-", loc) and unit.get("power") != power.name:
                    attackable_powers.append(
                        # if region r contains a supply center and is occupied by us
                        # equal to the power size of the strongest power that might attack it 
                        # TODO: Implementation correct? Could be ambiguous
                        power_sizes.get(unit.get("power")) or 0)
            defense_values[loc] = max(attackable_powers)

    # Proximity Map Values
    proximity_map = {}

    aw = calculate_parameter(game.phase, Aw)
    dw = calculate_parameter(game.phase, Dw)
    # Calculate zero order
    locs = {}
    for l in game.map.locs:
        l = l.upper()
        locs[l] = aw * attack_values[l] + dw * defense_values[l]

    proximity_map[0] = locs
    for i in range(1,10):
        locs = {}
        for l in game.map.locs:
            l = l.upper()
            adjacencies = game.map.abut_list(l)
            adj_values = [proximity_map[i-1][l]]
            for a in adjacencies:
                a = a.upper()
                adj_values.append(proximity_map[i-1][a])
            locs[l] = sum(adj_values) / len(adj_values)
        proximity_map[i] = locs
            
    # Competition and Strength Values
    strength_values = {}
    competition_values = {}
    for loc in game.map.locs:
        loc = loc.upper()
        adjacencies = game.map.abut_list(loc)
        adjacent_units = list(filter(lambda x: x is not None, [unit_positions.get(key) for key in game.map.abut_list(loc)]))
        # own_units = list(filter(lambda x: x.get("power") == power.name, adjacent_units))
        # strength_values[loc] = len(own_units)

        unit_neighbour_count = {}
        for p in game.powers.values():
            unit_neighbour_count[p.name.upper()] = 0
        for a in adjacent_units:
            unit_neighbour_count[a["power"]] += 1

        strength_values[loc] = unit_neighbour_count[power.name]
        # Remove the current power
        unit_neighbour_count.pop(p.name.upper(), None)
        competition_values[loc] = max(unit_neighbour_count.values())

    # Calculating Destination Values
    sw = calculate_parameter(game.phase, Sw)
    cw = calculate_parameter(game.phase, Cw)
    destination_values = {}
    for loc in game.map.locs:
        loc = loc.upper()
        value = 0
        for i in range(0,10):
            value += Pw[i] * proximity_map[i][loc]
        value += strength_values[loc] * sw - competition_values[loc] * cw 
        destination_values[loc] = value

    # Remove all impassable Destinations aka. SHUT
    for location, loc_type in game.map.loc_type.items():
        if loc_type == "SHUT":
            destination_values.pop(location.upper(), None)
    

    ## -------

    if game.phase_type == "M":
    # Determining Moves
        units_to_order = list(filter(lambda x: x.get("power") == power.name ,unit_positions.values()))
        destinations = {}
        for unit in units_to_order:
            # All possible Destination Values
            loc = unit["loc"].upper()
            adjacencies = [a.upper() for a in game.map.abut_list(loc) if game.map.abuts(unit["type"], loc, '-', a.upper())]
            adjacencies.append(loc)
            data = {region: destination_values[region] for region in adjacencies}
            ranked_provinces = dict(sorted(data.items(), key=lambda x: x[1], reverse=True))
            destination_selected = False
            i = 0
            while not destination_selected:
                i = 0 if i >= (len(ranked_provinces) - 1) else i
                dva = ranked_provinces[list(ranked_provinces.keys())[i]]
                dvb = ranked_provinces[list(ranked_provinces.keys())[i + 1]]
                # next_province_chance = ((dva -dvb) / dva) * 500
                next_province_chance = ((dva -dvb) / dva) * 100
                random_number = random.randint(0,100)
                if random_number > THRESHOLD_PLAY_ALTERNATIVE or random_number < next_province_chance * 0.5:
                    destination_selected = True
                    destinations[loc] = list(ranked_provinces.keys())[i]
                i += 1
                
    # Returning orders
        orders = []
        ordered = {}

        # source => destination
        should_hold = {k: v for k, v in destinations.items() if v == k}
        # source => destination without holds
        should_secure_position = {k: v for k, v in destinations.items() if v != k}
        
        # destination => [moveable, ber, bul]
        target_secure = {} 
        for key, value in sorted(should_secure_position.items()):
            target_secure.setdefault(value, []).append(key)


        # target_defend = [value for value in target_secure.keys() if value in should_hold]
        target_attack = [value for value in target_secure.keys() if value not in should_hold]

        # target => source
        target_move_order = {}

        # target => [sources]
        target_support_move = {}
        # target => [sources]
        target_support_hold = {}

        # Determine Mover as the province with the lowest Destination Value
        for target, sources in target_secure.items():
            if target in target_attack:
                # sources = ['BUL', 'MAR', 'BEL', 'STP']
                mover = {key: destination_values[key] for key in sources}
                target_move_order[target] = min(mover, key=mover.get)
                
        # Determine all supports
        for target, sources in target_secure.items():
            for source in (x for x in sources if x not in target_move_order.get(target, [])):
                if target in should_hold:
                    # SH
                    target_support_hold.setdefault(target, []).append(source)
                else:
                    target_support_move.setdefault(target, []).append(source)


        # TODO: Some support moves for hold orders
        

        for target, source in target_move_order.items():
            unit = unit_positions[source]
            orders.append("{0} {1} - {2}".format(unit["type"], unit["loc"], target))

        for target, sources in target_support_move.items():
            for source in sources:
                unit = unit_positions[source]
                supporting = unit_positions[target_move_order[target]]
                orders.append("{0} {1} S {2} {3} - {4}".format(unit["type"], unit["loc"], supporting["type"], supporting["loc"], target))

        for target, sources in target_support_hold.items():
            for source in sources:
                unit = unit_positions[source]
                supporting = unit_positions[target]
                orders.append("{0} {1} S {2} {3}".format(unit["type"], unit["loc"], supporting["type"], supporting["loc"]))

        # for unit_loc, dest_loc in destinations.items():
        #     u = unit_positions[unit_loc]
        #     if unit_loc == dest_loc:
        #         # Unit should hold
                
        #         # Determine if could give support
                

        #         orders.append("{0} {1} H".format(u["type"], u["loc"]))
        #     else:
        #         # Same destinations
        #         orders.append("{0} {1} - {2}".format(u["type"], u["loc"], dest_loc))
        #         ordered
        return orders



    elif game.phase_type == "R":
        orders = []
        retreat_locations = []
        for unit_description, targets in power.retreats.items():
            target_locations = {key: destination_values[key] for key in targets if key not in retreat_locations}
            loc = max(target_locations, key=target_locations.get, default=None)
            if loc is not None:
                retreat_locations.append(loc)
                orders.append("{0} - {1}".format(unit_description, loc))
            else:
                orders.append("{0} D".format(unit_description))
        return orders

    elif game.phase_type == "A":
        build_count = len(power.centers) - len(power.units)
        orders = []
        # Needs destroy
        # Todo: Little randomness
        if build_count < 0:
            units_to_order = list(filter(lambda x: x.get("power") == power.name ,unit_positions.values()))
            locations = [d['loc'] for d in units_to_order] 
            disbands_needed = abs(build_count)
            target_locations = {key: destination_values[key] for key in locations}
            # Currently this is just two random values as it seems all values are dependend on the parameters
            locations = sorted(target_locations, key=target_locations.get)[:disbands_needed]
            for l in locations:
                p = unit_positions[l]
                orders.append("{0} {1} D".format(p['type'], p['loc']))
            return orders


        # Needs build
        # Todo: Little randomness
        elif build_count > 0:
            orders = []
            builds_needed = abs(build_count)
            # Get owned centers and home centers AND has no unit on it
            buildable = [loc for loc in power.centers if loc in power.homes and unit_positions.get(loc) is None]
            target_locations = {key: destination_values[key] for key in buildable}
            locations = sorted(target_locations, key=target_locations.get, reverse=True)[:builds_needed]

            # Determine Unit Type random
            for l in locations:
                fleetstring = "F " + l
                armystring = "A " + l
                order = None
                fleet = game.map.is_valid_unit(fleetstring)
                army = game.map.is_valid_unit(armystring)
                if fleet and army:
                    order = fleetstring if random.random() > 0.5 else armystring
                elif army:
                    order = armystring
                elif fleet:
                    order = fleetstring
                orders.append(order + " B")
            return orders







    print(game.map_name, power.name)

def calculate_parameter(phase_long: str, parameter: dict):
    if "SPRING" in phase_long:
        return parameter.get("SPRING") or 0
    if "FALL" in phase_long:
        return parameter.get("FALL") or 0
    if "WINTER" in phase_long:
        return parameter.get("WINTER") or 0

# # game = Game(map_name="standard")
# path = r'.\integration\storage\app\dumbsingle\2021-05-20T18-41-57\state\14_S1905M.txt'
# data = Path(path).read_text()
# data = json.loads(base64.b64decode(data).decode())
# game = from_saved_game_format(data)
# # game.clear_centers("FRANCE")
# # game.clear_units("FRANCE")
# # game.set_units("FRANCE", ['A BUR', 'A PIE', 'A LVN', 'A PRU'], True)
# # game.set_units("FRANCE", ['A LVN'], True)
# # game.set_centers("FRANCE", ["PAR", "BRE", "MAR"], True)
# # game.process()
# # game.process()
# power = game.get_power("FRANCE")
# # game.process()


# get_best_orders(game, power)
