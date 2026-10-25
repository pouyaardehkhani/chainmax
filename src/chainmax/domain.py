"""Business vocabulary and finite decision domains, shared by independent backends."""
from itertools import product

FAMILIES = {
    "F01": "Capacitated warehouse-to-market transport",
    "F02": "Multi-echelon distribution", "F03": "Warehouse activation",
    "F04": "Route activation", "F05": "Multiple products",
    "F06": "Inventory and lead times", "F07": "Truck and mode decisions",
    "F08": "Minimum lots and sourcing rules", "F09": "Perishable products",
    "F10": "Production and distribution",
}


def key(*parts):
    return ":".join(map(str, parts))


def ages(p):
    return range(p["shelf_life"] or 1)


def decisions(d):
    """Declarations only. No business constraints or model coefficients here."""
    out = {}
    bound = sum(s["quantity"] for s in d["initial_stock"]) + sum(
        r["capacity"] * r["output_quantity"] * d["periods"] for r in d["recipes"])
    bound = max(1, bound)

    def add(parts, upper, cost, unit, kind="integer"):
        name = key(*parts)
        out[name] = {"name": name, "kind": kind, "lower": 0, "upper": upper,
                     "cost": cost, "unit": unit, "meaning": list(parts)}

    ps = {p["id"]: p for p in d["products"]}
    for n, p, t in product(d["locations"], d["products"], range(d["periods"])):
        for a in ages(p):
            expiry = p["shelf_life"] is not None and a == p["shelf_life"] - 1
            add(("inventory", n["id"], p["id"], t, a), 0 if expiry else bound,
                p["holding_cost"], "item")
            if p["shelf_life"] is not None:
                add(("dispose", n["id"], p["id"], t, a), bound, p["disposal_cost"], "item")
        if n["opening_cost"]:
            add(("open", n["id"]), 1, n["opening_cost"], "activation", "boolean")
    for r, t in product(d["routes"], range(d["periods"])):
        if t + r["lead_time"] >= d["periods"]:
            continue
        for pid in r["products"]:
            p = ps[pid]
            for a in ages(p):
                if p["shelf_life"] is not None and a + r["lead_time"] >= p["shelf_life"]:
                    continue
                add(("ship", r["id"], pid, t, a), min(bound, r["capacity"] // p["volume"]),
                    r["unit_cost"], "item")
        if r["fixed_cost"] or r["minimum_lot"] or d["sourcing"]["max_active_suppliers"] is not None or d["sourcing"]["dependencies"]:
            add(("active", r["id"], t), 1, r["fixed_cost"], "activation", "boolean")
        if r["truck_capacity"]:
            add(("trucks", r["id"], t), r["max_trucks"], r["truck_cost"], "truck")
    for demand in d["demands"]:
        p = ps[demand["product"]]
        for a in ages(p):
            add(("serve", demand["node"], p["id"], demand["period"], a), demand["quantity"], 0, "item")
    for r, t in product(d["recipes"], range(d["periods"])):
        add(("produce", r["id"], t), r["capacity"], r["cost"], "batch")
    return dict(sorted(out.items()))


def fixture():
    return {
        "schema_version": "1.0.0", "family": "F01", "structural_level": "L1",
        "features": ["transport"], "periods": 1,
        "units": {"quantity": "item", "currency": "cent", "time": "period", "capacity": "volume_unit", "truck": "truck", "production": "batch"},
        "products": [{"id": "P", "volume": 1, "shelf_life": None, "holding_cost": 0, "disposal_cost": 0}],
        "locations": [{"id": n, "role": "market" if n == "M" else "warehouse", "storage_capacity": 4, "throughput_capacity": 4, "opening_cost": 0} for n in ("A", "B", "M")],
        "initial_stock": [{"node": n, "product": "P", "age": 0, "quantity": 2} for n in ("A", "B")],
        "demands": [{"node": "M", "product": "P", "period": 0, "quantity": 3}],
        "routes": [{"id": n, "source": n, "destination": "M", "products": ["P"], "lead_time": 0, "capacity": 2, "unit_cost": c,
                    "fixed_cost": 0, "minimum_lot": 0, "truck_capacity": 0, "max_trucks": 0, "truck_cost": 0, "mode": "standard"} for n, c in (("A", 2), ("B", 5))],
        "recipes": [], "sourcing": {"max_active_suppliers": None, "dependencies": []},
        "objective_constant": 0, "narrative_template": 0,
    }
