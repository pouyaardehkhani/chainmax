import itertools
import json
import math
from pathlib import Path
import pytest
from pysat.solvers import Solver
from pysat.formula import WCNF
from chainmax.domain import decisions
from chainmax.checking import check,ir_feasible
from chainmax.model_builder import build_ir
from chainmax.encoding import compile_wcnf,solve
from chainmax.native_reference import solve as native


@pytest.mark.parametrize("path",sorted(Path("tests/fixtures").glob("F*.json")))
def test_exhaustive_business_ir_and_projected_cnf(path):
    d = json.loads(path.read_text())
    specs = decisions(d)
    names = list(specs)
    ranges = [range(s["upper"]+1) for s in specs.values()]
    assert math.prod(map(len,ranges)) <= 100000
    ir=build_ir(d)
    text,vm=compile_wcnf(ir)
    w=WCNF(from_string=text)
    optimum=None
    with Solver(name="g3",bootstrap_with=w.hard) as sat:
        for values in itertools.product(*ranges):
            a=dict(zip(names,values))
            checked=check(d,a)
            assumptions=[]
            for name,v in a.items():
                assumptions += [bit if v & (1<<k) else -bit for k,bit in enumerate(vm["variables"][name]["bits"])]
            assert checked["valid"] == ir_feasible(ir,a) == sat.solve(assumptions=assumptions), a
            if checked["valid"]:
                positive=set(x for x in assumptions if x>0)
                violated=sum(weight for c,weight in zip(w.soft,w.wght) if -c[0] in positive)
                assert violated+vm["objective_transform"]["offset"] == checked["cost"]
                optimum = checked["cost"] if optimum is None else min(optimum,checked["cost"])
    assert optimum is not None
    assert solve(text,vm)["cost"] == native(d)["cost"] == optimum


def test_nine_cent_four_paths():
    d=json.loads(Path("tests/fixtures/nine_cent.json").read_text())
    feasible=[]
    for a,b in itertools.product(range(3),repeat=2):
        if a+b==3: feasible.append((2*a+5*b,a,b))
    assert sorted(feasible)==[(9,2,1),(12,1,2)]
    n=native(d); w=solve(*compile_wcnf(build_ir(d)))
    assert n["cost"]==w["cost"]==9
    assert check(d,n["assignment"])["valid"] and check(d,w["assignment"])["valid"]
