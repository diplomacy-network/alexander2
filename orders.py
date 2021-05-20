from genericpath import exists
from math import e, radians
import random
from typing import Dict
from diplomacy import Game
from diplomacy.engine.game import Power
from diplomacy.utils.export import to_saved_game_format, from_saved_game_format

# PARAMETERS
A = 1
B = 4
C = 16

THRESHOLD_PLAY_ALTERNATIVE = 50

Sw = {"SPRING": 1000, "FALL": 1000, "WINTER": 0}
Cw = {"SPRING": 1000, "FALL": 1000, "WINTER": 0}
Aw = {"SPRING": 700, "FALL": 600, "WINTER": 0}
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
    state = game.get_state()
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
                next_province_chance = ((dva -dvb) / dva) * 500
                random_number = random.randint(0,100)
                if random_number > THRESHOLD_PLAY_ALTERNATIVE or random_number < next_province_chance:
                    destination_selected = True
                    destinations[loc] = list(ranked_provinces.keys())[i]
                i += 1
                
    # Returning orders
        return ["A PAR - MAR"]


    else:
        print("ELSE")





    print(game.map_name, power.name)

def calculate_parameter(phase_long: str, parameter: dict):
    if "SPRING" in phase_long:
        return parameter.get("SPRING") or 0
    if "FALL" in phase_long:
        return parameter.get("FALL") or 0
    if "WINTER" in phase_long:
        return parameter.get("WINTER") or 0

game = Game(map_name="standard")
power = game.get_power("FRANCE")


get_best_orders(game, power)
