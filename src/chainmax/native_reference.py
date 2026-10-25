"""CP-SAT model constructed directly from business tables, without the IR."""
import time
from ortools.sat.python import cp_model
from .domain import decisions, key, ages


def solve(d, seconds=30):
    start = time.perf_counter()
    m = cp_model.CpModel()
    specs = decisions(d)
    x = {k: m.new_int_var(v["lower"], v["upper"], k) for k, v in specs.items()}
    def get(*parts):
        return x.get(key(*parts), 0)
    products = {p["id"]: p for p in d["products"]}
    for t in range(d["periods"]):
        for loc in d["locations"]:
            node = loc["id"]
            stock_volume = []
            dispatch_volume = []
            for p in d["products"]:
                pid = p["id"]
                for age in ages(p):
                    available = sum(s["quantity"] for s in d["initial_stock"] if t == 0 and s["node"] == node and s["product"] == pid and s["age"] == age)
                    if t > 0 and (p["shelf_life"] is None or age > 0):
                        available += get("inventory", node, pid, t-1, age if p["shelf_life"] is None else age-1)
                    used = get("serve", node, pid, t, age) + get("dispose", node, pid, t, age)
                    for route in d["routes"]:
                        if route["source"] == node:
                            dispatched = get("ship", route["id"], pid, t, age)
                            used += dispatched
                            dispatch_volume.append(p["volume"] * dispatched)
                        if route["destination"] == node:
                            original_age = age - route["lead_time"] if p["shelf_life"] else age
                            available += get("ship", route["id"], pid, t-route["lead_time"], original_age)
                    if age == 0:
                        for recipe in d["recipes"]:
                            if recipe["node"] != node:
                                continue
                            batches = get("produce", recipe["id"], t)
                            if recipe["output"] == pid:
                                available += recipe["output_quantity"] * batches
                            for ingredient in recipe["inputs"]:
                                if ingredient["product"] == pid:
                                    used += ingredient["quantity"] * batches
                    inventory = get("inventory", node, pid, t, age)
                    m.add(available == used + inventory)
                    stock_volume.append(p["volume"] * inventory)
            m.add(sum(stock_volume) <= loc["storage_capacity"])
            m.add(sum(dispatch_volume) <= loc["throughput_capacity"])
            if loc["opening_cost"]:
                m.add(sum(dispatch_volume) <= loc["throughput_capacity"] * get("open", node))
        for demand in d["demands"]:
            if demand["period"] == t:
                m.add(sum(get("serve", demand["node"], demand["product"], t, a) for a in ages(products[demand["product"]])) == demand["quantity"])
        for route in d["routes"]:
            quantities = [(spec["meaning"][2], x[name]) for name, spec in specs.items() if spec["meaning"][0] == "ship" and spec["meaning"][1] == route["id"] and spec["meaning"][3] == t]
            volume = sum(products[p]["volume"] * q for p, q in quantities)
            total = sum(q for _, q in quantities)
            m.add(volume <= route["capacity"])
            active = key("active", route["id"], t)
            if active in x:
                m.add(total <= sum(specs[name]["upper"] for name in specs if specs[name]["meaning"][0] == "ship" and specs[name]["meaning"][1] == route["id"] and specs[name]["meaning"][3] == t) * x[active])
                m.add(total >= max(1, route["minimum_lot"]) * x[active])
            if key("trucks", route["id"], t) in x:
                m.add(volume <= route["truck_capacity"] * get("trucks", route["id"], t))
        limit = d["sourcing"]["max_active_suppliers"]
        if limit is not None:
            for loc in d["locations"]:
                if loc["role"] == "market":
                    m.add(sum(get("active", r["id"], t) for r in d["routes"] if r["destination"] == loc["id"]) <= limit)
        for a, b in d["sourcing"]["dependencies"]:
            m.add(get("active", a, t) <= get("active", b, t))
    m.minimize(d["objective_constant"] + sum(specs[k]["cost"] * value for k, value in x.items()))
    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = seconds
    solver.parameters.num_search_workers = 1
    solver.parameters.random_seed = 0
    solver.parameters.absolute_gap_limit = 0.0
    solver.parameters.relative_gap_limit = 0.0
    status = solver.solve(m)
    name = solver.status_name(status)
    if status != cp_model.OPTIMAL:
        return {"status": name, "seconds": time.perf_counter()-start}
    assignment = {k: solver.value(v) for k, v in x.items()}
    cost = d["objective_constant"] + sum(specs[k]["cost"] * v for k, v in assignment.items())
    return {"status": name, "assignment": assignment, "cost": cost, "seconds": time.perf_counter()-start,
            "absolute_gap_limit": 0, "relative_gap_limit": 0, "best_bound": round(solver.best_objective_bound)}
