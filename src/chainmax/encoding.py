"""Deterministic binary integer -> signed PB normalization -> BDD CNF -> WCNF."""
import time
from pysat.pb import PBEnc, EncType
from pysat.formula import WCNF
from pysat.examples.rc2 import RC2
from .schemas import validate_ir


def compile_wcnf(ir):
    validate_ir(ir)
    w = WCNF()
    mapping = {}
    top = 0
    for v in ir["variables"]:
        width = (v["upper"]-v["lower"]).bit_length()
        bits = list(range(top+1, top+width+1))
        top += width
        mapping[v["name"]] = {**v, "bits": bits}
    primary_end = top

    def encode(terms, sense, rhs, guard=None):
        nonlocal top
        merged = {}
        for term in terms:
            var = mapping[term["var"]]
            coeff = term["coefficient"]
            rhs -= coeff * var["lower"]
            for k, bit in enumerate(var["bits"]):
                merged[bit] = merged.get(bit, 0) + coeff * (1 << k)
        lits, weights = [], []
        for bit, c in sorted(merged.items()):
            if not c:
                continue
            lits.append(bit if c > 0 else -bit)
            weights.append(abs(c))
            if c < 0:
                rhs -= c
        total = sum(weights)
        if sense == "ge":
            lits = [-x for x in lits]
            rhs, sense = total-rhs, "le"
        if (sense == "le" and rhs >= total) or (sense == "eq" and not lits and rhs == 0):
            clauses = []
        elif rhs < 0 or (sense == "eq" and rhs > total):
            clauses = [[]]
        else:
            method = PBEnc.equals if sense == "eq" else PBEnc.atmost
            enc = method(lits=lits, weights=weights, bound=rhs, top_id=top, encoding=EncType.bdd)
            top = max(top, enc.nv)
            clauses = enc.clauses
        for clause in clauses:
            w.append(([guard] if guard is not None else []) + clause)
    for v in ir["variables"]:
        encode([{"var": v["name"], "coefficient": 1}], "le", v["upper"])
    for c in ir["constraints"]:
        if c["type"] == "linear":
            encode(c["terms"], c["sense"], c["rhs"])
        elif c["type"] == "clause":
            clause = []
            for l in c["literals"]:
                bit = mapping[l["var"]]["bits"][0]
                clause.append(bit if l["positive"] else -bit)
            w.append(clause)
        else:
            bit = mapping[c["activation"]["var"]]["bits"][0]
            guard = -bit if c["activation"]["value"] else bit
            encode(c["body"]["terms"], c["body"]["sense"], c["body"]["rhs"], guard)
    offset = ir["objective"]["constant"]
    for term in ir["objective"]["terms"]:
        v, coeff = mapping[term["var"]], term["coefficient"]
        offset += coeff * v["lower"]
        if coeff:
            for k, bit in enumerate(v["bits"]):
                w.append([-bit], weight=coeff*(1 << k))
    w.nv = max(w.nv, top)
    w.topw = sum(w.wght)+1
    rows = [f"p wcnf {w.nv} {len(w.hard)+len(w.soft)} {w.topw}"]
    rows += [f'{w.topw} ' + " ".join(map(str, c)) + (" " if c else "") + "0" for c in w.hard]
    rows += [f'{weight} ' + " ".join(map(str, c)) + " 0" for c, weight in zip(w.soft, w.wght)]
    text = "\n".join(rows)+"\n"
    return text, {"schema_version": "1.0.0", "variables": mapping,
                  "primary_end": primary_end, "auxiliary_range": [primary_end+1, w.nv],
                  "encoder": "pindakaas/PySAT PBEnc BDD", "dialect": "legacy_dimacs_wcnf",
                  "variable_count": w.nv, "hard_clauses": len(w.hard), "soft_clauses": len(w.soft),
                  "soft_weight_sum": sum(w.wght), "top": w.topw,
                  "objective_transform": {"multiplier": 1, "offset": offset}}


def decode(model, mapping):
    signed = set(model)
    all_ids = {abs(x) for x in model}
    if any(bit not in all_ids for v in mapping["variables"].values() for bit in v["bits"]):
        raise ValueError("incomplete primary assignment")
    return {name: v["lower"] + sum((1 << k) for k, bit in enumerate(v["bits"]) if bit in signed) for name, v in mapping["variables"].items()}


def solve(text, mapping):
    start = time.perf_counter()
    formula = WCNF(from_string=text)
    with RC2(formula, solver="g3", adapt=False) as solver:
        model = solver.compute()
        if model is None:
            return {"status": "INFEASIBLE", "seconds": time.perf_counter()-start}
        assignment = decode(model, mapping)
        signed = set(model)
        if any(not any(lit in signed for lit in clause) for clause in formula.hard):
            raise ValueError("RC2 model violates a hard clause")
        violation = sum(weight for clause, weight in zip(formula.soft, formula.wght) if not any(lit in signed for lit in clause))
        if violation != solver.cost:
            raise ValueError("RC2 violation cost mismatch")
        return {"status": "OPTIMAL", "assignment": assignment, "cost": violation+mapping["objective_transform"]["offset"],
                "violation_cost": violation, "boolean_assignment": model, "seconds": time.perf_counter()-start}
