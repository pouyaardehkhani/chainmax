"""Deterministic feasible path sampling; no optimum is planted or assumed."""
import random
from collections import defaultdict
from copy import deepcopy
from .domain import decisions, key


def generate(family, level, seed, profile):
    rng = random.Random(seed)
    li = int(level[1:])
    ns = profile["sources"]
    nm = profile["markets"]
    multi = family == "F05" or (li >= 3 and family in ("F06", "F07", "F09"))
    np = profile["products"] if multi else 1
    timed = family in ("F06", "F09")
    horizon = profile["periods"] if timed else 1
    perishable = family == "F09"
    shelf = horizon + rng.choice([0, 1]) if perishable else None
    shelf = max(2, shelf) if perishable else None
    pids = [f"P{i}" for i in range(np)]
    sources = [f"W{i}" for i in range(ns)]
    markets = [f"M{i}" for i in range(nm)]
    hubs = [f"H{i}" for i in range(1+(li == 4))] if family == "F02" else []
    ps = [{"id": p, "volume": rng.randint(1, 2) if multi else 1, "shelf_life": shelf,
           "holding_cost": rng.randint(0, 3) if timed else 0,
           "disposal_cost": rng.randint(1, 4) if perishable else 0} for p in pids]
    if family == "F10":
        ps.append({"id":"RAW", "volume":1, "shelf_life":None,"holding_cost":0,"disposal_cost":0})
    nodes = [{"id": n, "role": "plant" if family == "F10" and n in sources else "hub" if n in hubs else "market" if n in markets else "supplier" if family == "F02" else "warehouse",
              "storage_capacity": 10000, "throughput_capacity":10000,
              "opening_cost":rng.randint(3, 25) if family == "F03" and n in sources else 0} for n in sources+hubs+markets]
    d = {"schema_version":"1.0.0", "family":family, "structural_level":level,
         "features":["transport", "bounded_inventory", "exact_demand"],"periods":horizon,
         "units":{"quantity":"item","currency":"cent","time":"period","capacity":"volume_unit","truck":"truck","production":"batch"},
         "products":ps,"locations":nodes,"initial_stock":[],"demands":[],"routes":[],"recipes":[],
         "sourcing":{"max_active_suppliers":None,"dependencies":[]},"objective_constant":0,"narrative_template":rng.randrange(3)}
    feature = {"F02":"multi_echelon", "F03":"warehouse_activation", "F04":"route_activation", "F05":"shared_product_capacity", "F06":"lead_time", "F07":"integer_trucks_and_modes", "F08":"minimum_lots_and_sourcing", "F09":"age_and_expiry", "F10":"integer_bill_of_materials"}
    if family in feature:
        d["features"].append(feature[family])
    routes = {}
    def route(a, b, mode="standard"):
        rid = f"R_{a}_{b}_{mode}"
        if rid not in routes:
            lead = rng.randint(1, min(2, horizon-1)) if family == "F06" else (rng.randint(0, 1) if perishable and li >= 2 else 0)
            routes[rid] = {"id":rid,"source":a,"destination":b,"products":list(pids),"lead_time":lead,"capacity":10000,
                           "unit_cost":rng.randint(0, 12),"fixed_cost":rng.randint(2, 17) if family in ("F04","F08") or (li == 4 and family in ("F05","F07")) else 0,
                           "minimum_lot":rng.randint(1,2) if family == "F08" else 0,
                           "truck_capacity":rng.randint(2,5) if family == "F07" else 0,"max_trucks":0,
                           "truck_cost":rng.randint(2,11) if family == "F07" else 0,"mode":mode}
        return routes[rid]
    # Chosen flow paths generate stock requirements and a feasible witness.
    flow = defaultdict(int)
    batches = defaultdict(int)
    stock = defaultdict(int)
    used_routes = set()
    if family == "F10":
        for src in sources:
            d["recipes"].append({"id":f"B_{src}","node":src,"inputs":[{"product":"RAW","quantity":rng.randint(1,3)}],
                                 "output":pids[0],"output_quantity":rng.randint(1,2),"capacity":1000,"cost":rng.randint(1,8)})
    demand_periods = list(range(1, horizon)) if timed else [0]
    if family == "F06":
        demand_periods = [horizon-1] if horizon <= 3 else [horizon-2, horizon-1]
    if perishable:
        demand_periods = [horizon-1] if li == 1 else [1, horizon-1]
        demand_periods = sorted(set(demand_periods))
    for t in demand_periods:
        for market in markets:
            source_for_lot = rng.choice(sources)
            for pid in pids:
                src = source_for_lot if family == "F08" else rng.choice(sources)
                q = rng.randint(profile["demand_min"], profile["demand_max"])
                if family == "F10":
                    recipe = next(r for r in d["recipes"] if r["node"] == src)
                    q *= recipe["output_quantity"]
                    batch = q // recipe["output_quantity"]
                    batches[recipe["id"],0] += batch
                    stock[src,"RAW"] += batch*recipe["inputs"][0]["quantity"]
                else:
                    stock[src,pid] += q
                d["demands"].append({"node":market,"product":pid,"period":t,"quantity":q})
                path = [src,rng.choice(hubs),market] if hubs else [src,market]
                for a,b in zip(path,path[1:]):
                    r = route(a,b,"road" if family == "F07" else "standard")
                    depart = t-r["lead_time"]
                    if depart < 0:
                        r["lead_time"] = t
                        depart = 0
                    age = depart if perishable else 0
                    flow[r["id"],pid,depart,age] += q
                    used_routes.add(r["id"])
    # Sample optional edges and product/mode eligibility, keeping the planted paths.
    candidates = [(s,h) for s in sources for h in hubs] + [(h,m) for h in hubs for m in markets] if hubs else [(s,m) for s in sources for m in markets]
    for a,b in candidates:
        if rng.random() < profile["extra_route_probability"]:
            route(a,b,"road" if family == "F07" else "standard")
        if family == "F07" and rng.random() < 0.6:
            r = route(a,b,"rail")
            r["products"] = sorted(rng.sample(pids,rng.randint(1,len(pids))))
    pmap = {p["id"]:p for p in ps}
    for r in routes.values():
        maximum = max([sum(q*pmap[p]["volume"] for (rid,p,t,a),q in flow.items() if rid == r["id"] and t == period) for period in range(horizon)] or [0])
        r["capacity"] = max(1, maximum + rng.randint(0,profile["capacity_slack"])) if maximum else rng.randint(2,profile["demand_max"]*np+3)
        if r["truck_capacity"]:
            r["max_trucks"] = (r["capacity"] + r["truck_capacity"]-1)//r["truck_capacity"]
    d["routes"] = sorted(routes.values(),key=lambda r:r["id"])
    if family == "F08":
        d["sourcing"]["max_active_suppliers"] = 1 if li <= 2 else min(2, ns)
        if li >= 2 and len(used_routes) >= 2:
            a,b = rng.sample(sorted(used_routes),2)
            d["sourcing"]["dependencies"] = [[a,b]]
    # Stock slack is sampled independently, including inactive potential sources.
    for src in sources:
        for pid in (["RAW"] if family == "F10" else pids):
            qty = stock[src,pid] + rng.randint(0,profile["stock_slack"])
            if qty:
                d["initial_stock"].append({"node":src,"product":pid,"age":0,"quantity":qty})
    for recipe in d["recipes"]:
        recipe["capacity"] = max(1,batches[recipe["id"],0]+rng.randint(0,2))
    # Derive witness balances independently by executing the chosen events.
    assignment = {v:0 for v in decisions(d)}
    for args,q in flow.items():
        assignment[key("ship",*args)] = q
    for args,q in batches.items():
        assignment[key("produce",*args)] = q
    for dem in d["demands"]:
        age = dem["period"] if perishable else 0
        assignment[key("serve",dem["node"],dem["product"],dem["period"],age)] = dem["quantity"]
    for name, spec in decisions(d).items():
        meaning = spec["meaning"]
        if meaning[0] == "active":
            assignment[name] = int(any(rid == meaning[1] and t == meaning[2] and q for (rid,p,t,a),q in flow.items()))
        elif meaning[0] == "trucks":
            r = routes[meaning[1]]
            vol = sum(q*pmap[p]["volume"] for (rid,p,t,a),q in flow.items() if rid == r["id"] and t == meaning[2])
            assignment[name] = (vol+r["truck_capacity"]-1)//r["truck_capacity"]
        elif meaning[0] == "open":
            assignment[name] = int(any(routes[rid]["source"] == meaning[1] and q for (rid,p,t,a),q in flow.items()))
    # All chosen source goods start at age zero. Internal nodes pass them on.
    for n in nodes:
        for p in ps:
            for t in range(horizon):
                a = t if p["shelf_life"] else 0
                if a >= (p["shelf_life"] or 1):
                    continue
                available = sum(s["quantity"] for s in d["initial_stock"] if s["node"] == n["id"] and s["product"] == p["id"]) if t == 0 else assignment.get(key("inventory",n["id"],p["id"],t-1,a-1 if p["shelf_life"] else 0),0)
                for (rid,pid,dt,da),q in flow.items():
                    r = routes[rid]
                    if pid == p["id"]:
                        if r["destination"] == n["id"] and dt+r["lead_time"] == t:
                            available += q
                        if r["source"] == n["id"] and dt == t:
                            available -= q
                for recipe in d["recipes"]:
                    if recipe["node"] == n["id"]:
                        batch = batches[recipe["id"],t]
                        available += batch*recipe["output_quantity"] if recipe["output"] == p["id"] else 0
                        available -= sum(i["quantity"]*batch for i in recipe["inputs"] if i["product"] == p["id"])
                available -= assignment.get(key("serve",n["id"],p["id"],t,a),0)
                if p["shelf_life"] and a == p["shelf_life"]-1:
                    assignment[key("dispose",n["id"],p["id"],t,a)] = available
                else:
                    assignment[key("inventory",n["id"],p["id"],t,a)] = available
    for n in nodes:
        inventories = [sum(value*pmap[spec["meaning"][2]]["volume"] for name,spec in decisions(d).items() if spec["meaning"][0] == "inventory" and spec["meaning"][1] == n["id"] and spec["meaning"][3] == t for value in [assignment[name]]) for t in range(horizon)]
        outgoing = [sum(q*pmap[p]["volume"] for (rid,p,dt,a),q in flow.items() if routes[rid]["source"] == n["id"] and dt == t) for t in range(horizon)]
        n["storage_capacity"] = max(inventories,default=0)+rng.randint(0,profile["capacity_slack"])
        n["throughput_capacity"] = max(outgoing,default=0)+rng.randint(0,profile["capacity_slack"])
    return d, assignment
