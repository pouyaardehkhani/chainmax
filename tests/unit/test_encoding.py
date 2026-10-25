from copy import deepcopy
import itertools
import pytest
from pysat.formula import WCNF
from pysat.solvers import Solver
from chainmax.encoding import compile_wcnf,decode,solve
from chainmax.schemas import validate_ir


def small_ir(sense="eq",rhs=1,coeff=(-2,3)):
    return {"schema_version":"1.0.0","variables":[{"name":n,"kind":"integer","lower":0,"upper":2,"unit":"item","meaning":[n]} for n in ("x","y")],
            "constraints":[{"id":"c","type":"linear","terms":[{"var":n,"coefficient":c} for n,c in zip(("x","y"),coeff)],"sense":sense,"rhs":rhs,"source":"fixture"}],
            "objective":{"sense":"min","constant":7,"terms":[{"var":"x","coefficient":2}]}}


@pytest.mark.parametrize("sense",["eq","le","ge"])
@pytest.mark.parametrize("rhs",[-8,-1,0,1,8])
def test_signed_pb_projected_semantics(sense,rhs):
    ir=small_ir(sense,rhs)
    text,vm=compile_wcnf(ir)
    w=WCNF(from_string=text)
    assert w.topw>sum(w.wght)
    with Solver(name="g3",bootstrap_with=w.hard) as sat:
        for x,y in itertools.product(range(4),repeat=2):
            fix=[bit if v & (1<<k) else -bit for n,v in (("x",x),("y",y)) for k,bit in enumerate(vm["variables"][n]["bits"])]
            lhs=-2*x+3*y
            truth={"eq":lhs==rhs,"le":lhs<=rhs,"ge":lhs>=rhs}[sense] and x<=2 and y<=2
            assert sat.solve(assumptions=fix)==truth


def test_nonzero_lower_and_zero_domain_and_constant():
    ir=small_ir("ge",0,(1,1))
    ir["variables"][0].update(lower=2,upper=2)
    ir["variables"][1].update(upper=0)
    text,vm=compile_wcnf(ir)
    assert vm["variables"]["x"]["bits"]==vm["variables"]["y"]["bits"]==[]
    assert solve(text,vm)["cost"]==11


def test_boolean_clause_and_indicator():
    ir=small_ir()
    ir["variables"][0].update(kind="boolean",upper=1)
    ir["constraints"]=[{"id":"a","type":"clause","literals":[{"var":"x","positive":True}],"source":"fixture"},
                       {"id":"b","type":"indicator","activation":{"var":"x","value":1},"body":{"terms":[{"var":"y","coefficient":1}],"sense":"eq","rhs":2},"source":"fixture"}]
    r=solve(*compile_wcnf(ir))
    assert r["assignment"]=={"x":1,"y":2}


@pytest.mark.parametrize("mutation",["duplicate","unknown","unsupported","unbounded","overflow","negative_cost"])
def test_reject_unsafe_ir(mutation):
    ir=small_ir()
    if mutation=="duplicate": ir["variables"].append(deepcopy(ir["variables"][0]))
    if mutation=="unknown": ir["constraints"][0]["terms"][0]["var"]="z"
    if mutation=="unsupported": ir["constraints"][0]["type"]="execute_python"
    if mutation=="unbounded": del ir["variables"][0]["upper"]
    if mutation=="overflow": ir["constraints"][0]["terms"][0]["coefficient"]=2**59
    if mutation=="negative_cost": ir["objective"]["terms"][0]["coefficient"]=-1
    with pytest.raises(Exception): validate_ir(ir)
