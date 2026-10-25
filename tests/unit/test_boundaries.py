import json
from pathlib import Path
import pytest
from chainmax.native_reference import solve as native
from chainmax.encoding import compile_wcnf,solve
from chainmax.model_builder import build_ir
from chainmax.schemas import validate_domain


@pytest.mark.parametrize("family",[f"F{i:02}" for i in range(1,11)])
def test_feature_infeasible_boundary(family):
    d=json.loads(Path(f"tests/fixtures/{family}.json").read_text())
    if family=="F01": d["routes"]=[]
    elif family=="F02": d["initial_stock"][0]["quantity"]=0
    elif family=="F03": d["locations"][0]["throughput_capacity"]=0
    elif family=="F04": d["routes"][0]["minimum_lot"]=2
    elif family=="F05": d["routes"][0]["products"]=["Q"]
    elif family=="F06": d["routes"][0]["lead_time"]=2
    elif family=="F07":
        d["initial_stock"][0]["quantity"]=d["demands"][0]["quantity"]=2
        d["routes"][0]["capacity"]=2
        for n in d["locations"]: n["throughput_capacity"]=n["storage_capacity"]=2
    elif family=="F08": d["routes"][0]["minimum_lot"]=2
    elif family=="F09":
        d["initial_stock"][0]["age"]=1
        d["periods"]=2; d["demands"][0]["period"]=1
    elif family=="F10": d["recipes"][0]["inputs"][0]["quantity"]=2
    validate_domain(d)
    assert native(d)["status"]=="INFEASIBLE"
    assert solve(*compile_wcnf(build_ir(d)))["status"]=="INFEASIBLE"


def test_supplier_limit_and_directional_dependency():
    from chainmax.domain import fixture
    d=fixture()
    d["initial_stock"][0]["quantity"]=d["initial_stock"][1]["quantity"]=1
    d["demands"][0]["quantity"]=2
    d["sourcing"]["max_active_suppliers"]=1
    assert native(d)["status"]==solve(*compile_wcnf(build_ir(d)))["status"]=="INFEASIBLE"
    d["sourcing"]["max_active_suppliers"]=2
    assert native(d)["status"]=="OPTIMAL"
    d["sourcing"]["dependencies"]=[["A","B"]]
    d["initial_stock"][1]["quantity"]=0; d["demands"][0]["quantity"]=1
    assert native(d)["status"]==solve(*compile_wcnf(build_ir(d)))["status"]=="INFEASIBLE"
