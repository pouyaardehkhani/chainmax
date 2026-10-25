"""Maintain closed JSON schemas from compact declarations; run from project root."""
import json
from pathlib import Path

def obj(properties, required=None):
    return {"type": "object", "properties": properties, "required": list(properties) if required is None else required, "additionalProperties": False}
def arr(items, **extra):
    return {"type": "array", "items": items, **extra}
def enum(*values):
    return {"enum": list(values)}
def nullable(t):
    return {"anyOf": [t, {"type": "null"}]}
S = {"type": "string", "minLength": 1}
ID = {"type": "string", "pattern": "^[A-Za-z][A-Za-z0-9_]*$"}
I = {"type": "integer", "minimum": -(2**60)+1, "maximum": 2**60-1}
N = {"type": "integer", "minimum": 0, "maximum": 10**9}
P = {"type": "integer", "minimum": 1, "maximum": 10**9}
B = {"type": "boolean"}
V = enum("1.0.0")
number = {"type": "number", "minimum": 0}
mapping = lambda t: {"type": "object", "additionalProperties": t}
units = obj({"quantity": enum("item"), "currency": enum("cent"), "time": enum("period"), "capacity": enum("volume_unit"), "truck": enum("truck"), "production": enum("batch")})
domain = obj({
    "schema_version": V, "family": enum(*[f"F{i:02}" for i in range(1,11)]), "structural_level": enum("L1","L2","L3","L4"),
    "features": arr(S, uniqueItems=True), "periods": P, "units": units,
    "products": arr(obj({"id": ID,"volume":P,"shelf_life":nullable(P),"holding_cost":N,"disposal_cost":N}), minItems=1),
    "locations": arr(obj({"id":ID,"role":enum("warehouse","supplier","hub","market","plant"),"storage_capacity":N,"throughput_capacity":N,"opening_cost":N}), minItems=1),
    "initial_stock": arr(obj({"node":ID,"product":ID,"age":N,"quantity":N})),
    "demands": arr(obj({"node":ID,"product":ID,"period":N,"quantity":P}), minItems=1),
    "routes": arr(obj({"id":ID,"source":ID,"destination":ID,"products":arr(ID,uniqueItems=True),"lead_time":N,"capacity":N,"unit_cost":N,
                       "fixed_cost":N,"minimum_lot":N,"truck_capacity":N,"max_trucks":N,"truck_cost":N,"mode":enum("standard","road","rail")})),
    "recipes":arr(obj({"id":ID,"node":ID,"inputs":arr(obj({"product":ID,"quantity":P}),minItems=1),"output":ID,"output_quantity":P,"capacity":P,"cost":N})),
    "sourcing":obj({"max_active_suppliers":nullable(P),"dependencies":arr(arr(ID,minItems=2,maxItems=2))}),
    "objective_constant":N, "narrative_template":enum(0,1,2),
})
term = obj({"var":S,"coefficient":I})
body = obj({"terms":arr(term),"sense":enum("eq","le","ge"),"rhs":I})
lin = obj({"id":S,"type":enum("linear"),**body["properties"],"source":S})
clause = obj({"id":S,"type":enum("clause"),"literals":arr(obj({"var":S,"positive":B})),"source":S})
indicator = obj({"id":S,"type":enum("indicator"),"activation":obj({"var":S,"value":enum(0,1)}),"body":body,"source":S})
variable = obj({"name":S,"kind":enum("integer","boolean"),"lower":N,"upper":N,"unit":S,"meaning":arr({"anyOf":[S,N]})})
ir = obj({"schema_version":V,"variables":arr(variable),"constraints":arr({"oneOf":[lin,clause,indicator]}),
          "objective":obj({"sense":enum("min"),"constant":N,"terms":arr(obj({"var":S,"coefficient":N}))})})
transform = obj({"multiplier":P,"offset":I})
vm = obj({"schema_version":V,"variables":mapping(obj({**variable["properties"],"bits":arr(P)})),"primary_end":N,"auxiliary_range":arr(N,minItems=2,maxItems=2),
          "encoder":S,"dialect":enum("legacy_dimacs_wcnf"),"variable_count":N,"hard_clauses":N,"soft_clauses":N,"soft_weight_sum":N,"top":P,"objective_transform":transform})
backend = obj({"status":S,"seconds":number,"cost":N},["status","seconds","cost"])
# Additional backend evidence is explicitly enumerated.
backend["properties"].update({"absolute_gap_limit":N,"relative_gap_limit":N,"best_bound":I,"violation_cost":N})
verification = obj({"status":enum("VERIFIED"),"assurance_level":enum("CROSS_CHECKED","EXHAUSTIVE","PROOF_CHECKED","UNVERIFIED"),
                    "native":backend,"maxsat":backend,"native_checker":obj({"valid":B,"errors":arr(S),"cost":N}),
                    "maxsat_checker":obj({"valid":B,"errors":arr(S),"cost":N}),"exact_cost_agreement":B})
review = obj({"automated_consistency":B,"primary":nullable(obj({"reviewer":S,"date":S,"issues":arr(S),"resolution":S,"approved":B})),
              "second":nullable(obj({"reviewer":S,"date":S,"issues":arr(S),"resolution":S,"approved":B})),"status":enum("PENDING_HUMAN_REVIEW","APPROVED")})
provenance = obj({"seed":{"type":"integer","minimum":0,"maximum":2**32-1},"attempt":N,"config_hash":S,"source_revision":nullable(S),"source_tree_hash":S,"tool_versions":mapping(S),"generated_at":S})
provenance["properties"]["dataset_migration"] = obj({"from_dataset":enum("ChainMax-1K"),"from_catalog_sha256":S,"dataset_config_hash":S,"migration_source_revision":S,"migrated_at":S})
record = obj({"dataset_name":enum("chainmax-2k"),"dataset_version":V,"instance_id":{"type":"string","pattern":"^cmx_[0-9]{6}$"},"schema_version":V,
              "family":domain["properties"]["family"],"structural_level":domain["properties"]["structural_level"],"features":arr(S),"source_type":enum("synthetic"),"units":units,
              "problem":obj({"description":S,"data":domain,"assumptions":arr(S)}),"reference":obj({k:S for k in ("input","ir","mathematical","wcnf","variable_map","solution","verification","provenance","review","description")}),
              "reference_optimum":N,"objective_transform":transform,"verification":verification,"provenance":provenance,"review":review,"content_hashes":mapping(S)})
for name, schema in {"domain":domain,"model_ir":ir,"variable_map":vm,"verification":verification,"instance":record}.items():
    schema = {"$schema":"https://json-schema.org/draft/2020-12/schema",**schema}
    Path(f"schemas/{name}.schema.json").write_text(json.dumps(schema,indent=2)+"\n",encoding="utf-8",newline="\n")
