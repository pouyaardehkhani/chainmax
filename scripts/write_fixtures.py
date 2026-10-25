from copy import deepcopy
import json
from pathlib import Path
from chainmax.domain import fixture

def tiny(family):
    d = fixture()
    d["family"] = family
    d["locations"] = [n for n in d["locations"] if n["id"] != "B"]
    for n in d["locations"]:
        n["storage_capacity"] = n["throughput_capacity"] = 1
    d["initial_stock"] = [{"node":"A","product":"P","age":0,"quantity":1}]
    d["routes"] = [d["routes"][0]]
    d["routes"][0]["capacity"] = 1
    d["demands"][0]["quantity"] = 1
    if family == "F02":
        d["locations"].append({"id":"H","role":"hub","storage_capacity":1,"throughput_capacity":1,"opening_cost":0})
        d["routes"][0]["destination"] = "H"
        r = deepcopy(d["routes"][0]); r.update(id="HM",source="H",destination="M")
        d["routes"].append(r)
    if family == "F03": d["locations"][0]["opening_cost"] = 3
    if family == "F04": d["routes"][0]["fixed_cost"] = 3
    if family == "F05":
        p = deepcopy(d["products"][0]); p["id"] = "Q"; d["products"].append(p)
        d["routes"][0]["products"].append("Q")
    if family == "F06":
        d["periods"] = 2; d["demands"][0]["period"] = 1
        d["routes"][0]["lead_time"] = 1; d["products"][0]["holding_cost"] = 1
    if family == "F07":
        d["routes"][0].update(truck_capacity=1,max_trucks=1,truck_cost=3,mode="road")
    if family == "F08":
        d["routes"][0].update(minimum_lot=1,fixed_cost=1)
        d["sourcing"]["max_active_suppliers"] = 1
    if family == "F09": d["products"][0].update(shelf_life=2,disposal_cost=1)
    if family == "F10":
        p = deepcopy(d["products"][0]); p["id"] = "RAW"; d["products"].append(p)
        d["initial_stock"][0]["product"] = "RAW"
        d["recipes"] = [{"id":"BATCH","node":"A","inputs":[{"product":"RAW","quantity":1}],"output":"P","output_quantity":1,"capacity":1,"cost":3}]
    return d

for i in range(1,11):
    d=tiny(f"F{i:02}")
    Path(f'tests/fixtures/{d["family"]}.json').write_text(json.dumps(d,indent=2)+"\n",encoding="utf-8")
Path('tests/fixtures/nine_cent.json').write_text(json.dumps(fixture(),indent=2)+"\n",encoding="utf-8")
