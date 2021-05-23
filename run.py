from diplomacy.utils.strings import PREVIOUS_PHASE
from flask import Flask, jsonify, abort, request, redirect
from diplomacy import Game
from diplomacy.utils.export import to_saved_game_format, from_saved_game_format
import json
import uuid
import base64
from orders import get_best_orders
from pathlib import Path
from datetime import date, datetime, timedelta

def assignDumbOrders(game: Game):
    for p in game.powers.values():
        orders = get_best_orders(game, p)
        game.set_orders(p.name, orders)

def adjudicateWholeGame(variant: str):
    game = Game('standard')
    while game.phase != "COMPLETED":
        assignDumbOrders(game)
        game.process()

    time = datetime.now()
    filename = time.strftime("%Y-%m-%dT%H-%M-%S") + '#' + uuid.uuid4().__str__() +".json"
    path = Path("./data/" + variant)
    path.mkdir(parents=True, exist_ok=True)
    
    path.joinpath(filename).write_text(json.dumps(to_saved_game_format(game)))
    # path.write_text(json.dumps(to_saved_game_format(game), indent=4))
    # print(game.outcome)

while True:
    start = datetime.now()
    adjudicateWholeGame("standard")
    end = datetime.now()
    print((end-start).total_seconds())





