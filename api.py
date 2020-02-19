from flask import Flask, jsonify, abort, request
# from flask import jsonify
from diplomacy import Game
from diplomacy.utils.export import to_saved_game_format, from_saved_game_format
import json

app = Flask(__name__)

# TODO: Make an issue about the timestamp. It seems to be off time by one hour even though my timezone is configured correctly
# TODO: Minify JSON Output
# TODO: Minify SVG Output (at least Whitespace)

# A list of valid variants
valid = ['standard']


@app.route('/variants')
def variants():
    return jsonify(valid)


@app.route('/variants/<variant_name>')
def variant_display(variant_name):
    if variant_name not in valid:
        abort(404)
    game = Game(map_name=variant_name)
    list(Game().get_map_power_names())
    return {
        "name": variant_name,
        "powers": list(game.get_map_power_names())
    }


@app.route('/adjudicate/<variant_name>')
def basic_instance(variant_name):
    if variant_name not in valid:
        abort(404)
    game = Game(map_name=variant_name)
    # ! This could cause bugs, I'm not sure about the behaviour.
    game.rules = []
    return {
        "phase": game.map.phase_long(game.get_current_phase()),
        "svg_with_orders": "",
        "svg_adjudicated": game.render(incl_orders=False, incl_abbrev=True),
        "current_state": to_saved_game_format(game),
        "possible_orders": return_possible_orders(game)
    }

@app.route('/adjudicate', methods=['POST'])
def adjudicator():
    if not request.is_json:
        abort(418, 'Please use Application Type JSON')
    json = request.get_json()

    game = from_saved_game_format(json["previous_state"])
    game.clear_orders()
    for order in json["orders"]:
        game.set_orders(order["power"], order["instructions"])
    previous_svg = game.render(incl_orders=True, incl_abbrev=True)
    game.process()
    adjudicated = game.render(incl_orders=True, incl_abbrev=True)
    return {
        "phase": game.map.phase_long(game.get_current_phase()),
        "svg_with_orders": previous_svg,
        "svg_adjudicated": adjudicated,
        "current_state": to_saved_game_format(game),
        "possible_orders": return_possible_orders(game)
    }


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
