from diplomacy.utils.strings import PREVIOUS_PHASE
from flask import Flask, jsonify, abort, request
# from flask import jsonify
from diplomacy import Game
from diplomacy.utils.export import to_saved_game_format, from_saved_game_format
import json
import base64

app = Flask(__name__)

# TODO: Make an issue about the timestamp. It seems to be off time by one hour even though my timezone is configured correctly
# TODO: Minify JSON Output
# TODO: Minify SVG Output (at least Whitespace)

# A list of valid variants
valid_variants = ['standard']
version = 'v0.3'


@app.route('/'+ version + '/variants')
def variants():
    json_array = dict()
    for variant in valid_variants:
        game = Game(map_name=variant)
        json_array[variant] = {
            "powers": list(game.get_map_power_names()),
            "default_end_of_game": game.win
            }

    return jsonify(json_array)

@app.route('/'+ version + '/adjudicate/<variant_name>')
def basic_instance(variant_name):
    if variant_name not in valid_variants:
        abort(404)
    game = Game(map_name=variant_name)
    # ! This could cause bugs, I'm not sure about the behaviour.
    game.rules = []
    return return_api_result(game)


@app.route('/'+ version + '/adjudicate', methods=['POST'])
def adjudicator():
    if not request.is_json:
        abort(418, 'Please use Application Type JSON')
    jsonb = request.get_json()
    data = json.loads(base64.b64decode(jsonb["previous_state_encoded"]).decode())
    game = from_saved_game_format(data)
    game.clear_orders()
    game.rules = []
    print(jsonb["orders"])
    for power, instructions in jsonb["orders"].items():
        game.set_orders(power, instructions)
    previous_phase = game.get_current_phase()
    previous_svg = game.render(incl_orders=True, incl_abbrev=True)
    game.process()
    
    return return_api_result(game, previous_svg=previous_svg, previous_phase=previous_phase)


def return_possible_orders(game):
    # TODO: Better variable names, for now it does its job
    possible_orders = game.get_all_possible_orders()

    possibilities = dict()
    for power in game.get_map_power_names():
        loc = []
        dicto = {
            "name": power
        }
        units = dict()
        for loc in game.get_orderable_locations(power):
            units[loc] = possible_orders[loc]
        # dicto["units"] = units
        possibilities[power] = units
    return possibilities

def return_phase_data(game):
    # TODO: Better variable names, for now it does its job

    possibilities = dict()
    for power in game.powers:
        p = game.powers[power]
        possibilities[p.name] = {
            "unit_count": len(p.units),
            "supply_center_count": len(p.centers),
            "home_center_count": len(p.homes)
        }
    
    return possibilities

def return_api_result(game: Game, previous_svg="", previous_phase=""):
    adjudicated = game.render(incl_orders=True, incl_abbrev=True)
    savedGame = to_saved_game_format(game)
    
    return {
        "phase_type": game.phase_type,
        "phase_power_data": return_phase_data(game),
        "phase_long": game.map.phase_long(game.get_current_phase()),
        "phase_short": game.get_current_phase(),
        "svg_with_orders": previous_svg,
        "svg_adjudicated": adjudicated,
        "current_state_encoded": base64.b64encode(json.dumps(savedGame).encode()).decode(),
        "possible_orders": return_possible_orders(game),
        "applied_orders": game.order_history[previous_phase] if previous_phase != "" else {},
        "winners": game.outcome[1:]
    }

