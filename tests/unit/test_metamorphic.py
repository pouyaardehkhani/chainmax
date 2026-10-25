import json
from copy import deepcopy
from chainmax.domain import fixture
from chainmax.native_reference import solve
from chainmax.model_builder import build_ir
from chainmax.encoding import compile_wcnf

def test_rename():
    d=fixture(); renamed=json.loads(json.dumps(d).replace('"A"','"ALPHA"'))
    assert solve(d)["cost"]==solve(renamed)["cost"]

def test_scale_all_costs():
    d=fixture(); before=solve(d)["cost"]
    for r in d["routes"]:
        for k in ("unit_cost","fixed_cost","truck_cost"): r[k]*=3
    assert solve(d)["cost"]==3*before

def test_add_optional_route_and_tighten_capacity():
    d=fixture(); before=solve(d)["cost"]
    r=deepcopy(d["routes"][1]); r.update(id="CHEAP",unit_cost=1); d["routes"].append(r)
    assert solve(d)["cost"]<=before
    d=fixture(); d["routes"][0]["capacity"]=1
    assert solve(d)["cost"]>=before

def test_deterministic_encoding():
    ir=build_ir(fixture())
    assert compile_wcnf(ir)==compile_wcnf(ir)
