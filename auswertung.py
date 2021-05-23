from diplomacy.engine.power import Power
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
from tabulate import tabulate
import progressbar as pb

variant = 'standard'

class CountryResult:
    name:str = ""
    solo:int = 0
    draw:int = 0
    survived:int = 0
    defeated:int = 0
    average_scs:float = 0
    count:int = 0

    def __init__(self, name:str) -> None:
        self.name = name
        pass

    def strength(self) -> int:
        return (15 * self.solo + 5 * self.draw + 1 * self.survived) / self.count

    def addData(self, typ:str, scs:int):
        if typ == "SOLO":
            self.solo += 1
        elif typ=="DRAW":
            self.draw += 1
        elif typ=="SURVIVED":
            self.survived += 1
        elif typ=="DEFEATED":
            self.defeated += 1
        self.count += 1
        self.average_scs += (scs - self.average_scs) / self.count
    
    def toTableArray(self) -> list:
        # headers = ["Power", "Solos", "Draws", "Survived", "Defeated", "Avg. Scs", "Strength"]
        return [self.name, self.solo, self.draw, self.survived, self.defeated, self.average_scs, self.strength()]


def get_data(game: Game) -> dict:
    data = {
        "SOLO": [],
        "DRAW": [],
        "SURVIVED": [],
        "DEFEATED": [],
    }
    solo = [power.name for power in game.powers.values() if len(power.centers) >= game.win]
    if len(solo) == 1:
        # SOLO
        data["SOLO"] = solo
        data["SURVIVED"] = [power.name for power in game.powers.values() if len(power.centers) > 0 and power.name != data["SOLO"]]
        data["DEFEATED"] = [power.name for power in game.powers.values() if len(power.centers) == 0]
    else:
        data["DRAW"] = [power.name for power in game.powers.values() if len(power.centers) >= 0]
        data["DEFEATED"] = [power.name for power in game.powers.values() if len(power.centers) == 0]
    return data


    

    

powerdict = {key: CountryResult(key) for key in Game('standard').powers.keys()}

file_count = len([y for y in Path(".\data\standard").rglob("*.json")])
widgets = ['Time to parse all json files: ', pb.Percentage(), ' ', 
            pb.Bar(marker=pb.RotatingMarker()), ' ', pb.ETA()]
#initialize timer
timer = pb.ProgressBar(widgets=widgets, maxval=file_count).start()
i = 0
for path in Path(".\data\standard").rglob("*.json"):
    # print(path.name)
    game = from_saved_game_format(json.loads(path.read_text()))
    data = get_data(game)
    timer.update(i)
    for p in game.powers.values():
        s = [typ for typ, l  in data.items() if p.name in l]
        powerdict[p.name].addData(s[0], len(p.centers))

    i += 1
    # break;

print(" ")
print(" ")
print("Number of games: {0}".format(file_count))
print(" ")
headers = ["Power", "Solos", "Draws", "Survived", "Defeated", "Avg. Scs", "Strength"]
table = [power.toTableArray() for power in powerdict.values()]

print(tabulate(table, headers=headers))

