from typing import Dict
from diplomacy import Game
from diplomacy.engine.game import Power
from diplomacy.utils.export import to_saved_game_format, from_saved_game_format

# PARAMETERS
A = 1
B = 4
C = 16

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
