from diplomacy.utils.strings import PREVIOUS_PHASE
from flask import Flask, jsonify, abort, request, redirect
from diplomacy import Game
from diplomacy.utils.export import to_saved_game_format, from_saved_game_format
import json
import uuid
import base64
from app import return_api_result
from orders import get_best_orders
from pathlib import Path
from datetime import date, datetime, timedelta


def assignDumbOrders(game: Game):
    for p in game.powers.values():
        orders = get_best_orders(game, p)
        game.set_orders(p.name, orders)

def adjudicateWholeGame(variant: str):
    game = Game('standard')
    foldername = uuid.uuid4().__str__()
    while game.phase != "COMPLETED":
        assignDumbOrders(game)
        previous_phase = game.get_current_phase()
        previous_svg = game.render(incl_orders=True, incl_abbrev=True)
        game.process()
        res = return_api_result(game=game, previous_phase=previous_phase, previous_svg=previous_svg)

        filename = str(len(game.state_history) - 1) + '_' + game.get_current_phase() + '.json'
        path = Path("./data/" + foldername)
        path.mkdir(parents=True, exist_ok=True)
        
        path.joinpath(filename).write_text(json.dumps(res))
    # path.write_text(json.dumps(to_saved_game_format(game), indent=4))
    # print(game.outcome)

while True:
    start = datetime.now()
    adjudicateWholeGame("standard")
    end = datetime.now()
    print((end-start).total_seconds())





