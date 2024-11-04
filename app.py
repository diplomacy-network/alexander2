from diplomacy.engine.power import Power
from diplomacy.utils.strings import PREVIOUS_PHASE
from flask import Flask, jsonify, abort, request, redirect, current_app, g as app_ctx
# from flask import jsonify
from diplomacy import Game
from diplomacy.utils.export import to_saved_game_format, from_saved_game_format
import json
import base64
import markdown
import markdown.extensions.fenced_code
from orders import get_best_orders
import time

app = Flask(__name__)

# TODO: Make an issue about the timestamp. It seems to be off time by one hour even though my timezone is configured correctly
# TODO: Minify JSON Output
# TODO: Minify SVG Output (at least Whitespace)

# A list of valid variants
valid_variants = ['standard']
version = 'v0.5'


@app.route('/')
def root():
    return redirect('/' + version)

@app.route('/' + version)
@app.route('/' + version + '/')
def docs():
    readme_file = open("README.md", "r")
    md_template_string = markdown.markdown(
        readme_file.read(), extensions=["fenced_code"]
    )

    return md_template_string

@app.before_request
def logging_before():
    # Store the start time for the request
    app_ctx.start_time = time.perf_counter()


@app.after_request
def logging_after(response):
    # Get total time in milliseconds
    total_time = time.perf_counter() - app_ctx.start_time
    time_in_ms = int(total_time * 1000)
    # Log the time taken for the endpoint 
    current_app.logger.info('%s ms %s %s %s', time_in_ms, request.method, request.path, dict(request.args))
    return response

@app.route('/'+ version + '/variants')
def variants():
    json_array = []
    for variant in valid_variants:
        game = Game(map_name=variant)
        json_array.append({
            "name": variant,
            "powers": list(game.get_map_power_names()),
            "default_end_of_game": game.win
            })
    return jsonify({"variants": json_array})

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
    # print(jsonb)
    data = json.loads(base64.b64decode(jsonb["previous_state_encoded"]).decode())
    game = from_saved_game_format(data)
    game.win = jsonb['scs_to_win']
    game.clear_orders()
    game.rules = []
    # print(jsonb["orders"])
    for orders in jsonb["orders"]:
        try:
            instructions = []
            for instr in orders["instructions"]:
                instructions.append(instr.split("//", 1)[0])
            game.set_orders(orders["power"], instructions)
        except IndexError:
            pass
    previous_phase = game.get_current_phase()
    previous_svg = game.render(incl_orders=True, incl_abbrev=True)
    game.process()
    
    return return_api_result(game, previous_svg=previous_svg, previous_phase=previous_phase)

@app.route('/'+ version + '/dumbbot', methods=['POST'])
def dumbbot():
    if not request.is_json:
        abort(418, 'Please use Application Type JSON')
    jsonb = request.get_json()
    data = json.loads(base64.b64decode(jsonb["current_state_encoded"]).decode())
    powername = jsonb["power"]
    game = from_saved_game_format(data)
    power = game.get_power(powername)
    return jsonify({
        "orders": get_best_orders(game, power) or [],
        "power": powername
    })

def return_possible_orders(game):
    # TODO: Better variable names, for now it does its job
    possible_orders = game.get_all_possible_orders()

    possibilities = []
    for power in game.get_map_power_names():
        loc = []
        dicto = {
            "power": power
        }
        units = []
        for loc in game.get_orderable_locations(power):
            units.append({
                "space": loc,
                "possible_orders": possible_orders[loc]
            })
            # units[loc] = possible_orders[loc]
        dicto["units"] = units
        possibilities.append(dicto)
    return possibilities

def return_phase_data(game: Game) -> list:
    # TODO: Better variable names, for now it does its job

    possibilities = []
    for power in game.powers:
        p: Power
        p = game.powers[power]
        possibilities.append({
            "power": p.name,
            "unit_count": len(p.units),
            "supply_center_count": len(p.centers),
            "home_center_count": len(p.homes)
        })
    return possibilities

def return_applied_orders(game:Game, previous_phase="") -> list:
    
    if previous_phase == "":
        return []
    else:
        orderHistory = game.order_history[previous_phase]
        allOrders = []
        for power, orders in orderHistory.items():
            allOrders.append({
                "power": power,
                "orders": orders
            })
        return allOrders


def return_api_result(game: Game, previous_svg="", previous_phase=""):
    adjudicated = game.render(incl_orders=True, incl_abbrev=True)
    savedGame = to_saved_game_format(game)

    game
    
    return {
        "phase_type": game.phase_type,
        "phase_power_data": return_phase_data(game),
        "phase_long": game.map.phase_long(game.get_current_phase()),
        "phase_short": game.get_current_phase(),
        "svg_with_orders": previous_svg,
        "svg_adjudicated": adjudicated,
        "current_state_encoded": base64.b64encode(json.dumps(savedGame).encode()).decode(),
        "possible_orders": return_possible_orders(game),
        "applied_orders": return_applied_orders(game, previous_phase),
        "winners": game.outcome[1:],
        "winning_phase": game.outcome[0] if len(game.outcome) > 1 else "",
    }


