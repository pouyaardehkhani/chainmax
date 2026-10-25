"""Direct integer business accounting. This checker does not inspect the IR or clauses."""
from itertools import product
from .domain import decisions, ages, key


def check(d, assignment):
    errors = []
    specs = decisions(d)
    if set(assignment) != set(specs):
        return {"valid": False, "errors": ["missing or unknown decisions"], "cost": None}
    for name, v in assignment.items():
        if type(v) is not int or not specs[name]["lower"] <= v <= specs[name]["upper"]:
            errors.append(f"domain:{name}")
    if errors:
        return {"valid": False, "errors": errors, "cost": None}
    products = {p["id"]: p for p in d["products"]}
    routes = {r["id"]: r for r in d["routes"]}
    # Explicit event ledger: quantities enter/leave business stock buckets.
    ledger = {}
    def event(n, p, t, a, q):
        bucket = (n, p, t, a)
        ledger[bucket] = ledger.get(bucket, 0) + q
    for s in d["initial_stock"]:
        event(s["node"], s["product"], 0, s["age"], s["quantity"])
    cost = d["objective_constant"]
    shipped, volumes, inventory_volume, outbound = {}, {}, {}, {}
    for name, value in assignment.items():
        meaning = specs[name]["meaning"]
        kind = meaning[0]
        if kind == "ship":
            _, rid, pid, t, a = meaning
            r = routes[rid]
            event(r["source"], pid, t, a, -value)
            arrival_age = a + r["lead_time"] if products[pid]["shelf_life"] else a
            event(r["destination"], pid, t+r["lead_time"], arrival_age, value)
            shipped[rid, t] = shipped.get((rid, t), 0) + value
            volume = products[pid]["volume"] * value
            volumes[rid, t] = volumes.get((rid, t), 0) + volume
            outbound[r["source"], t] = outbound.get((r["source"], t), 0) + volume
            cost += r["unit_cost"] * value
        elif kind == "inventory":
            _, n, p, t, a = meaning
            event(n, p, t, a, -value)
            if t+1 < d["periods"]:
                next_age = a+1 if products[p]["shelf_life"] else a
                event(n, p, t+1, next_age, value)
            inventory_volume[n, t] = inventory_volume.get((n, t), 0) + value*products[p]["volume"]
            cost += products[p]["holding_cost"] * value
        elif kind in ("serve", "dispose"):
            _, n, p, t, a = meaning
            event(n, p, t, a, -value)
            if kind == "dispose":
                cost += products[p]["disposal_cost"] * value
        elif kind == "produce":
            _, rid, t = meaning
            r = next(r for r in d["recipes"] if r["id"] == rid)
            for ingredient in r["inputs"]:
                event(r["node"], ingredient["product"], t, 0, -ingredient["quantity"] * value)
            event(r["node"], r["output"], t, 0, r["output_quantity"] * value)
            cost += r["cost"] * value
        elif kind == "open":
            cost += next(n["opening_cost"] for n in d["locations"] if n["id"] == meaning[1]) * value
        elif kind == "active":
            cost += routes[meaning[1]]["fixed_cost"] * value
        elif kind == "trucks":
            cost += routes[meaning[1]]["truck_cost"] * value
    for bucket, net in ledger.items():
        if net != 0:
            errors.append(f"stock_balance:{bucket}:{net}")
    for dem in d["demands"]:
        fulfilled = sum(assignment[key("serve", dem["node"], dem["product"], dem["period"], a)] for a in ages(products[dem["product"]]))
        if fulfilled != dem["quantity"]:
            errors.append("exact_demand")
    for r, t in product(d["routes"], range(d["periods"])):
        total, volume = shipped.get((r["id"], t), 0), volumes.get((r["id"], t), 0)
        if volume > r["capacity"]:
            errors.append("route_capacity")
        active = assignment.get(key("active", r["id"], t))
        if active is not None and ((total > 0) != bool(active) or (active and total < max(1, r["minimum_lot"]))):
            errors.append("activation_or_minimum_lot")
        trucks = assignment.get(key("trucks", r["id"], t))
        if trucks is not None and volume > r["truck_capacity"] * trucks:
            errors.append("truck_capacity")
    for n, t in product(d["locations"], range(d["periods"])):
        dispatch = outbound.get((n["id"], t), 0)
        if dispatch > n["throughput_capacity"] or inventory_volume.get((n["id"], t), 0) > n["storage_capacity"]:
            errors.append("location_capacity")
        if n["opening_cost"] and dispatch > 0 and not assignment[key("open", n["id"])]:
            errors.append("warehouse_closed")
    for t in range(d["periods"]):
        limit = d["sourcing"]["max_active_suppliers"]
        if limit is not None:
            for n in d["locations"]:
                if n["role"] == "market" and sum(assignment.get(key("active", r["id"], t), 0) for r in d["routes"] if r["destination"] == n["id"]) > limit:
                    errors.append("supplier_limit")
        for a, b in d["sourcing"]["dependencies"]:
            if assignment.get(key("active", a, t), 0) > assignment.get(key("active", b, t), 0):
                errors.append("sourcing_dependency")
    return {"valid": not errors, "errors": errors, "cost": cost}


def ir_feasible(ir, a):
    if set(a) != {v["name"] for v in ir["variables"]}:
        return False
    for v in ir["variables"]:
        if type(a[v["name"]]) is not int or not v["lower"] <= a[v["name"]] <= v["upper"]:
            return False
    def linear(c):
        lhs = sum(t["coefficient"]*a[t["var"]] for t in c["terms"])
        return {"eq": lhs == c["rhs"], "le": lhs <= c["rhs"], "ge": lhs >= c["rhs"]}[c["sense"]]
    for c in ir["constraints"]:
        if c["type"] == "linear" and not linear(c):
            return False
        if c["type"] == "clause" and not any(bool(a[l["var"]]) == l["positive"] for l in c["literals"]):
            return False
        if c["type"] == "indicator" and a[c["activation"]["var"]] == c["activation"]["value"] and not linear(c["body"]):
            return False
    return True
