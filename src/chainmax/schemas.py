"""Closed structural schemas plus semantic validation and integer range safety."""
import json
from pathlib import Path
from functools import lru_cache
from jsonschema import Draft202012Validator

SCHEMAS = Path(__file__).resolve().parents[2] / "schemas"
LIMIT = 2**60


@lru_cache
def validator(name):
    return Draft202012Validator(json.loads((SCHEMAS/f"{name}.schema.json").read_text(encoding="utf-8")))


def validate(name, obj):
    validator(name).validate(obj)


def validate_ir(ir):
    validate("model_ir", ir)
    vs = {v["name"]: v for v in ir["variables"]}
    if len(vs) != len(ir["variables"]):
        raise ValueError("duplicate variables")
    if [v["name"] for v in ir["variables"]] != sorted(vs):
        raise ValueError("variables must be sorted")
    ids = [c["id"] for c in ir["constraints"]]
    if len(ids) != len(set(ids)):
        raise ValueError("duplicate constraint IDs")
    for v in vs.values():
        if v["lower"] > v["upper"] or v["upper"] >= LIMIT or (v["kind"] == "boolean" and (v["lower"], v["upper"]) != (0, 1)):
            raise ValueError("invalid finite bounds")
    def terms(ts):
        seen = set()
        magnitude = 0
        for t in ts:
            if t["var"] not in vs or t["var"] in seen:
                raise ValueError("unknown or duplicate variable reference")
            seen.add(t["var"])
            magnitude += abs(t["coefficient"]) * vs[t["var"]]["upper"]
        if magnitude >= LIMIT:
            raise ValueError("numeric overflow risk")
    terms(ir["objective"]["terms"])
    # The sum of binary soft weights may exceed the bounded objective maximum.
    if sum(t["coefficient"] * ((1 << (vs[t["var"]]["upper"]-vs[t["var"]]["lower"]).bit_length())-1) for t in ir["objective"]["terms"]) >= LIMIT:
        raise ValueError("soft-weight overflow risk")
    for c in ir["constraints"]:
        if c["type"] == "linear":
            terms(c["terms"])
        elif c["type"] == "indicator":
            a = c["activation"]["var"]
            if a not in vs or vs[a]["kind"] != "boolean":
                raise ValueError("indicator requires Boolean activation")
            terms(c["body"]["terms"])
        else:
            if any(l["var"] not in vs or vs[l["var"]]["kind"] != "boolean" for l in c["literals"]):
                raise ValueError("clause requires Boolean variables")


def validate_domain(d):
    validate("domain", d)
    nodes = {n["id"] for n in d["locations"]}
    products = {p["id"]: p for p in d["products"]}
    routes = {r["id"] for r in d["routes"]}
    if len(nodes) != len(d["locations"]) or len(products) != len(d["products"]) or len(routes) != len(d["routes"]) or len({r["id"] for r in d["recipes"]}) != len(d["recipes"]):
        raise ValueError("duplicate entity")
    # Zero-lead arcs must form a DAG, avoiding same-period circulation ambiguity.
    edges = [(r["source"], r["destination"]) for r in d["routes"] if r["lead_time"] == 0]
    remaining = set(nodes)
    while remaining:
        roots = {n for n in remaining if not any(b == n and a in remaining for a, b in edges)}
        if not roots:
            raise ValueError("zero-lead route cycle")
        remaining -= roots
    for r in d["routes"]:
        if r["source"] not in nodes or r["destination"] not in nodes or any(p not in products for p in r["products"]) or not r["products"]:
            raise ValueError("invalid route reference")
        if bool(r["truck_capacity"]) != bool(r["max_trucks"]) or (not r["truck_capacity"] and r["truck_cost"]):
            raise ValueError("inconsistent truck settings")
    for s in d["initial_stock"]:
        if s["node"] not in nodes or s["product"] not in products or s["age"] >= (products[s["product"]]["shelf_life"] or 1):
            raise ValueError("invalid initial stock")
    demand_keys = [(x["node"], x["product"], x["period"]) for x in d["demands"]]
    if len(demand_keys) != len(set(demand_keys)):
        raise ValueError("duplicate demand")
    for x in d["demands"]:
        if x["node"] not in nodes or x["product"] not in products or x["period"] >= d["periods"]:
            raise ValueError("invalid demand reference")
    for r in d["recipes"]:
        if r["node"] not in nodes or r["output"] not in products or products[r["output"]]["shelf_life"] or any(i["product"] not in products or products[i["product"]]["shelf_life"] for i in r["inputs"]) or r["output"] in [i["product"] for i in r["inputs"]]:
            raise ValueError("unsupported recipe")
    # v1 recipes have raw-only inputs; no within-period production cycles.
    outputs = {r["output"] for r in d["recipes"]}
    if any(i["product"] in outputs for r in d["recipes"] for i in r["inputs"]):
        raise ValueError("chained recipes unsupported")
    for a, b in d["sourcing"]["dependencies"]:
        if a not in routes or b not in routes:
            raise ValueError("invalid dependency")
