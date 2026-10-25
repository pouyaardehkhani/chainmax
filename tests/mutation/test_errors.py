import json
from pathlib import Path
from copy import deepcopy
import pytest
from pysat.solvers import Solver
from pysat.formula import WCNF
from chainmax.domain import fixture
from chainmax.model_builder import build_ir
from chainmax.encoding import compile_wcnf,solve
from chainmax.native_reference import solve as native
from chainmax.checking import check
from chainmax.rendering import render,consistency

def load(f): return json.loads(Path(f"tests/fixtures/{f}.json").read_text())

def test_missing_demand_is_detected():
    d=fixture(); ir=build_ir(d)
    ir["constraints"]=[c for c in ir["constraints"] if c["source"]!="demands"]
    bad=solve(*compile_wcnf(ir))
    assert bad["cost"]==0 and not check(d,bad["assignment"])["valid"]

def test_reverse_capacity_detected_with_counterexample():
    d=fixture(); d["routes"][0]["capacity"]=1
    ir=build_ir(d)
    for c in ir["constraints"]:
        if c["source"]=="routes/capacity" and any(t["var"].startswith("ship:A:") for t in c["terms"]): c["sense"]="ge"
    # A=0,B=2 cannot meet demand, but is a valid partial-bound domain witness;
    # compare a demand-two variant to make the wrong lower capacity visible.
    d["demands"][0]["quantity"]=2
    a=native(d)["assignment"]
    a["ship:A:P:0:0"]=0; a["ship:B:P:0:0"]=2
    a["inventory:A:P:0:0"]=2; a["inventory:B:P:0:0"]=0
    assert check(d,a)["valid"]
    ir=build_ir(d)
    for c in ir["constraints"]:
        if c["source"]=="routes/capacity" and any(t["var"].startswith("ship:A:") for t in c["terms"]): c["sense"]="ge"
    from chainmax.checking import ir_feasible
    assert not ir_feasible(ir,a)

@pytest.mark.parametrize("f,source",[("F03","locations/opening_cost"),("F04","routes/activation")])
def test_removed_fixed_charge_link(f,source):
    d=load(f); ir=build_ir(d)
    ir["constraints"]=[c for c in ir["constraints"] if c["source"]!=source]
    bad=solve(*compile_wcnf(ir))
    assert not check(d,bad["assignment"])["valid"]

def test_changed_shipping_coefficient():
    d=fixture(); ir=build_ir(d)
    next(t for t in ir["objective"]["terms"] if t["var"]=="ship:A:P:0:0")["coefficient"]=1
    bad=solve(*compile_wcnf(ir))
    assert bad["cost"]!=check(d,bad["assignment"])["cost"]

def test_shifted_arrival():
    d=load("F06"); a=native(d)["assignment"]
    d["routes"][0]["lead_time"]=0
    assert not check(d,a)["valid"]

def test_expiry_boundary():
    d=load("F09"); d["periods"]=3; d["demands"][0]["period"]=2
    d["routes"][0]["lead_time"]=2
    assert native(d)["status"]=="INFEASIBLE"
    w=solve(*compile_wcnf(build_ir(d)))
    assert w["status"]=="INFEASIBLE"
    # One period earlier, the same item arrives at the last usable age.
    d["demands"][0]["period"]=1; d["routes"][0]["lead_time"]=1
    assert native(d)["status"]=="OPTIMAL"

@pytest.mark.parametrize("factor",[0,2])
def test_omitted_or_double_truck_charge(factor):
    d=load("F07"); a=native(d)["assignment"]; ir=build_ir(d)
    next(t for t in ir["objective"]["terms"] if t["var"].startswith("trucks:"))["coefficient"]*=factor
    assert solve(*compile_wcnf(ir))["cost"]!=check(d,a)["cost"]

def test_wrong_bill_of_materials():
    d=load("F10"); a=native(d)["assignment"]
    d["recipes"][0]["inputs"][0]["quantity"]=2
    assert not check(d,a)["valid"]

def test_numeric_and_unit_description_mutations():
    d=fixture(); text=render(d)
    assert consistency(d,text)
    assert not consistency(d,text.replace('"quantity": 3','"quantity": 4'))
    assert not consistency(d,text.replace("currency is cents","currency is dollars"))

def test_two_products_compete_for_capacity():
    d=load("F05")
    d["initial_stock"].append({"node":"A","product":"Q","age":0,"quantity":1})
    d["demands"].append({"node":"M","product":"Q","period":0,"quantity":1})
    assert native(d)["status"]=="INFEASIBLE"
    assert solve(*compile_wcnf(build_ir(d)))["status"]=="INFEASIBLE"

def test_composed_activation_trucks_minimum_lot():
    d=load("F07"); d["routes"][0].update(fixed_cost=2,minimum_lot=1)
    d["locations"][0]["opening_cost"]=4
    a=native(d); b=solve(*compile_wcnf(build_ir(d)))
    assert a["cost"]==b["cost"]==11
    assert check(d,b["assignment"])["valid"]

def test_binary_bound_omission_counterexample():
    from test_encoding import small_ir
    ir=small_ir("ge",0,(0,0)); ir["objective"]["terms"]=[]
    text,vm=compile_wcnf(ir)
    fix=vm["variables"]["x"]["bits"] # 11 represents 3 > upper 2
    with Solver(name="g3",bootstrap_with=WCNF(from_string=text).hard) as s: assert not s.solve(assumptions=fix)
    with Solver(name="g3") as s: assert s.solve(assumptions=fix)
