"""Candidate verification, immutable artifacts, cumulative construction, safe resume."""
import datetime
import json
import subprocess
import time
from collections import Counter, deque
from pathlib import Path
import yaml
from .io import atomic,digest,dumps,source_hash,versions
from .domain import FAMILIES
from .generators import generate
from .model_builder import build_ir,render_math
from .schemas import validate,validate_ir,validate_domain
from .rendering import render,consistency,ASSUMPTIONS
from .checking import check
from .native_reference import solve as solve_native
from .encoding import compile_wcnf,solve as solve_maxsat


def make_candidate(job):
    d, planted = generate(job["family"],job["level"],job["seed"],job["profile"])
    validate_domain(d)
    witness_check = check(d,planted)
    if not witness_check["valid"]:
        raise ValueError(f"planted feasibility error: {witness_check}")
    ir = build_ir(d)
    validate_ir(ir)
    native = solve_native(d,job["native_seconds"])
    if native["status"] != "OPTIMAL":
        return {"status": "FEASIBLE_ONLY" if native["status"] == "FEASIBLE" else "INFEASIBLE" if native["status"] == "INFEASIBLE" else "NATIVE_INCONCLUSIVE", "backend":native}
    text, mapping = compile_wcnf(ir)
    maxsat = solve_maxsat(text,mapping)
    if maxsat["status"] != "OPTIMAL":
        return {"status":"BACKEND_DISAGREEMENT", "native":native["status"],"maxsat":maxsat["status"]}
    nc,mc = check(d,native["assignment"]),check(d,maxsat["assignment"])
    if not nc["valid"] or not mc["valid"] or len({nc["cost"],mc["cost"],native["cost"],maxsat["cost"]}) != 1:
        return {"status":"BACKEND_DISAGREEMENT","native_checker":nc,"maxsat_checker":mc}
    description = render(d)
    review = {"automated_consistency":consistency(d,description),"primary":None,"second":None,"status":"PENDING_HUMAN_REVIEW"}
    if not review["automated_consistency"]:
        raise ValueError("description consistency check failed")
    metadata = lambda s: {k:v for k,v in s.items() if k not in ("assignment","boolean_assignment")}
    verification = {"status":"VERIFIED","assurance_level":"CROSS_CHECKED","native":metadata(native),"maxsat":metadata(maxsat),
                    "native_checker":nc,"maxsat_checker":mc,"exact_cost_agreement":True}
    validate("verification",verification)
    provenance = {**job["provenance"],"seed":job["seed"],"attempt":job["attempt"],"generated_at":datetime.datetime.now(datetime.timezone.utc).isoformat()}
    solution = {"cost":native["cost"],"native_assignment":native["assignment"],"maxsat_assignment":maxsat["assignment"],"boolean_assignment":maxsat["boolean_assignment"],
                "multiple_optima_permitted":True}
    artifacts = {"input.json":dumps(d),"problem.md":description,"reference_model.json":dumps(ir),"reference_model.md":render_math(ir),
                 "reference.wcnf":text,"variable_map.json":dumps(mapping),"reference_solution.json":dumps(solution),"verification.json":dumps(verification),
                 "provenance.json":dumps(provenance),"review.json":dumps(review),"feasibility_witness.json":dumps(planted)}
    prefix = f'data/instances/{job["instance_id"]}/'
    refs = dict(zip(("input","description","ir","mathematical","wcnf","variable_map","solution","verification","provenance","review"),
                    [prefix+x for x in ("input.json","problem.md","reference_model.json","reference_model.md","reference.wcnf","variable_map.json","reference_solution.json","verification.json","provenance.json","review.json")]))
    record = {"dataset_name":"ChainMax-1K","dataset_version":"1.0.0","schema_version":"1.0.0","instance_id":job["instance_id"],
              "family":d["family"],"structural_level":d["structural_level"],"features":d["features"],"source_type":"synthetic","units":d["units"],
              "problem":{"description":description,"data":d,"assumptions":ASSUMPTIONS},"reference":refs,"reference_optimum":native["cost"],
              "objective_transform":mapping["objective_transform"],"verification":verification,"provenance":provenance,"review":review,
              "content_hashes":{prefix+n:digest(t) for n,t in artifacts.items()}}
    validate("instance",record)
    return {"status":"COMPLETED_OPTIMAL", "record":record,"artifacts":artifacts,"input_hash":digest(dumps(d)),"witness_cost":witness_check["cost"]}


def load_config(path):
    raw = Path(path).read_bytes()
    c = yaml.safe_load(raw)
    if c["target_base_instances"] != len(FAMILIES)*len(c["structural_levels"])*c["instances_per_family_level"] or c["instances_per_family"] != len(c["structural_levels"])*c["instances_per_family_level"]:
        raise ValueError("inconsistent quotas")
    if c["dataset_name"] != "ChainMax-1K" or c["dataset_version"] != "1.0.0" or "splits" in c:
        raise ValueError("unsupported identity/policy")
    return c,digest(raw)


def read_catalog(path):
    path = Path(path)
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()] if path.exists() else []


def save_catalog(root, records):
    atomic(root/"data/chainmax-1k.jsonl", "".join(json.dumps(r,sort_keys=True)+"\n" for r in sorted(records,key=lambda r:r["instance_id"])))


def build(root, config_path, limit, resume=False):
    from .workers import Pool
    c,ch = load_config(config_path)
    if limit < 1 or limit > c["target_base_instances"]:
        raise ValueError("accepted-limit outside configured corpus")
    catalog = root/"data/chainmax-1k.jsonl"
    # A single writer owns catalog and resume state. A stale lock must be inspected.
    lock=root/"audit/build.lock"
    lock.parent.mkdir(parents=True,exist_ok=True)
    # Acquire in the CLI wrapper so all early-return/error paths release it.
    records = read_catalog(catalog)
    if records and not resume:
        raise ValueError("catalog exists; use --resume")
    if any(r["provenance"]["config_hash"] != ch for r in records):
        raise ValueError("configuration differs from immutable accepted records")
    revision = subprocess.run(["git","rev-parse","HEAD"],cwd=root,capture_output=True,text=True).stdout.strip() or None
    provenance = {"config_hash":ch,"source_revision":revision,"source_tree_hash":source_hash(root),"tool_versions":versions()}
    previous = read_catalog(root/"audit/candidate_ledger.jsonl")
    attempts = Counter()
    for row in previous:
        attempts[row["instance_id"]] = max(attempts[row["instance_id"]],row["attempt"]+1)
    # Recover a fully written directory after a crash before catalog commit.
    for completed in sorted((root/"data/instances").glob("*/_record.json")):
        rec = json.loads(completed.read_text())
        if rec["instance_id"] not in {r["instance_id"] for r in records}:
            if rec["provenance"]["config_hash"] != ch:
                raise ValueError("orphan record config mismatch")
            for path,h in rec["content_hashes"].items():
                if digest((root/path).read_bytes()) != h:
                    raise ValueError("orphan checksum mismatch")
            records.append(rec)
    existing = {r["instance_id"] for r in records}
    hashes = {digest(dumps(r["problem"]["data"])) for r in records}
    pending = deque(i for i in range(1,limit+1) if f"cmx_{i:06}" not in existing)
    pool = Pool(c["resources"]["worker_processes"],c["resources"]["candidate_seconds"],c["resources"]["candidate_memory_mb"])
    running = 0
    failures = []
    ledger = root/"audit/candidate_ledger.jsonl"
    ledger.parent.mkdir(parents=True,exist_ok=True)
    def job(i):
        cell = (i-1)%40
        family,level = f"F{cell//4+1:02}", f"L{cell%4+1}"
        iid = f"cmx_{i:06}"
        attempt = attempts[iid]
        seed = int(digest(f'{c["seed"]}:{iid}:{attempt}')[:8],16)
        profile = {**c["profiles"][level],**c.get("family_profile_overrides",{}).get(family,{}).get(level,{})}
        return {"instance_id":iid,"family":family,"level":level,"seed":seed,"profile":profile,"native_seconds":c["resources"]["native_seconds"],"attempt":attempt,"provenance":provenance}
    try:
        while pending or running:
            while pending:
                i = pending[0]
                if attempts[f"cmx_{i:06}"] >= c["resources"]["attempts_per_slot"]:
                    failures.append(i)
                    pending.popleft()
                    continue
                if not pool.submit(job(i)):
                    break
                pending.popleft()
                running += 1
            result = pool.poll()
            if result is None:
                time.sleep(0.04)
                continue
            j,outcome = result
            running -= 1
            iid = j["instance_id"]
            attempts[iid] += 1
            if outcome["status"] == "COMPLETED_OPTIMAL" and outcome["input_hash"] in hashes:
                outcome = {"status":"EXACT_DUPLICATE"}
            row = {k:j[k] for k in ("instance_id","family","level","seed","attempt")}
            row.update({"status":outcome["status"],"config_hash":ch,"source_tree_hash":provenance["source_tree_hash"],"timestamp":datetime.datetime.now(datetime.timezone.utc).isoformat()})
            if outcome["status"] == "COMPLETED_OPTIMAL":
                rec = outcome["record"]
                folder = root/"data/instances"/iid
                if folder.exists():
                    raise ValueError(f"immutable directory already exists: {iid}")
                staging = root/"data/instances"/(".staging_"+iid)
                if staging.exists():
                    # Preserve incomplete files and restart the same deterministic job.
                    quarantine=root/"audit/interrupted_staging"/(iid+"_"+str(time.time_ns()))
                    quarantine.parent.mkdir(parents=True,exist_ok=True)
                    staging.rename(quarantine)
                staging.mkdir(parents=True)
                for name,txt in outcome["artifacts"].items():
                    atomic(staging/name,txt)
                atomic(staging/"_record.json",dumps(rec))
                staging.rename(folder)
                records.append(rec)
                hashes.add(outcome["input_hash"])
                save_catalog(root,records)
                row["witness_cost"] = outcome["witness_cost"]
            else:
                row["detail"] = {k:v for k,v in outcome.items() if k != "status"}
                with (root/"audit/rejected_candidates.jsonl").open("a",encoding="utf-8") as f:
                    f.write(json.dumps(row,sort_keys=True)+"\n")
                pending.append(int(iid[4:]))
            with ledger.open("a",encoding="utf-8") as f:
                f.write(json.dumps(row,sort_keys=True)+"\n")
                f.flush()
            if len(records)%10 == 0 or outcome["status"] != "COMPLETED_OPTIMAL":
                print(f'{len(records)} verified / {limit}; {iid}: {outcome["status"]}',flush=True)
            atomic(root/"audit/build_manifest.json",dumps({"status":"LOCAL_CONSTRUCTION_HUMAN_REVIEW_PENDING","accepted_count":len(records),"config_hash":ch,"source":provenance,"config":c,"failed_slots":failures}))
    finally:
        for slot in pool.slots:
            if slot["job"] is not None:
                interrupted=slot["job"]
                row={k:interrupted[k] for k in ("instance_id","family","level","seed","attempt")}
                row.update({"status":"INTERRUPTED","config_hash":ch,"source_tree_hash":provenance["source_tree_hash"],"timestamp":datetime.datetime.now(datetime.timezone.utc).isoformat()})
                with ledger.open("a",encoding="utf-8") as f: f.write(json.dumps(row,sort_keys=True)+"\n")
                with (root/"audit/rejected_candidates.jsonl").open("a",encoding="utf-8") as f: f.write(json.dumps(row,sort_keys=True)+"\n")
        pool.close()
    (root/"audit/rejected_candidates.jsonl").touch(exist_ok=True)
    save_catalog(root,records)
    print(f"Verified corpus size: {len(records)}; human review is pending; exhausted slots: {failures}",flush=True)
    return len(records)
