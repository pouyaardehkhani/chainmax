"""Ground domain rules into a typed linear/Boolean IR. Never used by the native solver."""
from itertools import product
from .domain import decisions, key, ages


def build_ir(d):
    vs = decisions(d)
    cs = []
    def lin(rule, terms, sense, rhs):
        merged = {}
        for v, c in terms:
            if v in vs:
                merged[v] = merged.get(v, 0) + c
        cs.append({"id": f"c{len(cs):06}", "type": "linear", "terms": [
            {"var": v, "coefficient": c} for v, c in sorted(merged.items()) if c],
            "sense": sense, "rhs": rhs, "source": rule})
    def group(prefix):
        return [v for v in vs if v.startswith(prefix)]
    ps = {p["id"]: p for p in d["products"]}
    for n, p, t in product(d["locations"], d["products"], range(d["periods"])):
        for a in ages(p):
            terms = [(key("inventory", n["id"], p["id"], t, a), 1),
                     (key("dispose", n["id"], p["id"], t, a), 1),
                     (key("serve", n["id"], p["id"], t, a), 1)]
            prev_age = a - 1 if p["shelf_life"] else a
            if t and prev_age >= 0:
                terms.append((key("inventory", n["id"], p["id"], t-1, prev_age), -1))
            rhs = sum(s["quantity"] for s in d["initial_stock"] if t == 0 and (s["node"], s["product"], s["age"]) == (n["id"], p["id"], a))
            for r in d["routes"]:
                if r["source"] == n["id"]:
                    terms.append((key("ship", r["id"], p["id"], t, a), 1))
                if r["destination"] == n["id"]:
                    depart_age = a - r["lead_time"] if p["shelf_life"] else a
                    terms.append((key("ship", r["id"], p["id"], t-r["lead_time"], depart_age), -1))
            for r in d["recipes"]:
                if r["node"] == n["id"] and a == 0:
                    coefficient = sum(i["quantity"] for i in r["inputs"] if i["product"] == p["id"])
                    if r["output"] == p["id"]:
                        coefficient -= r["output_quantity"]
                    terms.append((key("produce", r["id"], t), coefficient))
            lin("balance/initial_stock/routes/recipes", terms, "eq", rhs)
    for dem in d["demands"]:
        lin("demands", [(key("serve", dem["node"], dem["product"], dem["period"], a), 1) for a in ages(ps[dem["product"]])], "eq", dem["quantity"])
    for n, t in product(d["locations"], range(d["periods"])):
        stored = [(v, ps[spec["meaning"][2]]["volume"]) for v, spec in vs.items() if spec["meaning"][0] == "inventory" and spec["meaning"][1] == n["id"] and spec["meaning"][3] == t]
        lin("locations/storage_capacity", stored, "le", n["storage_capacity"])
        outgoing = [(v, ps[vs[v]["meaning"][2]]["volume"]) for r in d["routes"] if r["source"] == n["id"] for v in group(key("ship", r["id"])+":") if vs[v]["meaning"][3] == t]
        lin("locations/throughput_capacity", outgoing, "le", n["throughput_capacity"])
        if n["opening_cost"]:
            lin("locations/opening_cost", outgoing + [(key("open", n["id"]), -n["throughput_capacity"])], "le", 0)
    for r, t in product(d["routes"], range(d["periods"])):
        flows = [v for v in group(key("ship", r["id"])+":") if vs[v]["meaning"][3] == t]
        volume = [(v, ps[vs[v]["meaning"][2]]["volume"]) for v in flows]
        lin("routes/capacity", volume, "le", r["capacity"])
        active = key("active", r["id"], t)
        if active in vs:
            lin("routes/activation", [(v, 1) for v in flows] + [(active, -sum(vs[v]["upper"] for v in flows))], "le", 0)
            lin("routes/minimum_lot", [(v, 1) for v in flows] + [(active, -max(1, r["minimum_lot"]))], "ge", 0)
        truck = key("trucks", r["id"], t)
        if truck in vs:
            lin("routes/truck_capacity", volume + [(truck, -r["truck_capacity"])], "le", 0)
    for t in range(d["periods"]):
        if d["sourcing"]["max_active_suppliers"] is not None:
            for n in d["locations"]:
                if n["role"] == "market":
                    lin("sourcing/max_active_suppliers", [(key("active", r["id"], t), 1) for r in d["routes"] if r["destination"] == n["id"]], "le", d["sourcing"]["max_active_suppliers"])
        for a, b in d["sourcing"]["dependencies"]:
            lin("sourcing/dependencies", [(key("active", a, t), 1), (key("active", b, t), -1)], "le", 0)
    return {"schema_version": "1.0.0", "variables": [{k: v for k, v in s.items() if k != "cost"} for s in vs.values()], "constraints": cs,
            "objective": {"sense": "min", "constant": d["objective_constant"], "terms": [{"var": v, "coefficient": s["cost"]} for v, s in vs.items() if s["cost"]]}}


def render_math(ir):
    rows = ["# Bounded integer reference model", "", "Minimize " + str(ir["objective"]["constant"]) + " + " + " + ".join(f'{x["coefficient"]} {x["var"]}' for x in ir["objective"]["terms"]), "", "## Variables", ""]
    rows += [f'- `{v["name"]}`: {v["kind"]} in [{v["lower"]}, {v["upper"]}], {v["unit"]}.' for v in ir["variables"]]
    rows += ["", "## Hard constraints", ""]
    for c in ir["constraints"]:
        if c["type"] == "linear":
            rows.append(f'- {c["id"]}: ' + (" + ".join(f'{x["coefficient"]} {x["var"]}' for x in c["terms"]) or "0") + f' {c["sense"]} {c["rhs"]}. Source: {c["source"]}.')
        else:
            rows.append(f'- {c["id"]}: {c}')
    return "\n".join(rows) + "\n"
