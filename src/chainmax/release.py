"""Recompute evidence, expose review gaps, and prepare an explicitly provisional bundle."""
import collections
import datetime
import gzip
import io
import json
import subprocess
import tarfile
from pathlib import Path
from pysat.formula import WCNF
from .io import atomic,dumps,digest,versions,source_hash
from .pipeline import read_catalog,load_config,save_catalog,construction_config
from .identity import DATASET_NAME,DATASET_VERSION,CATALOG_PATH,ARCHIVE_NAME
from .schemas import validate,validate_ir,validate_domain
from .checking import check
from .model_builder import build_ir,render_math
from .encoding import compile_wcnf,decode
from .rendering import consistency
from .generators import generate


def safe_path(root, relative):
    p=(root/relative).resolve()
    if not p.is_relative_to(root.resolve()) or Path(relative).is_absolute() or ".." in Path(relative).parts:
        raise ValueError("unsafe artifact path")
    return p


def business_hash(d):
    return digest(dumps({k:v for k,v in d.items() if k not in ("narrative_template","family","structural_level","features","schema_version")}))


def topology_hash(d):
    return digest(dumps({"periods":d["periods"],"products":[(p["id"],p["shelf_life"]) for p in d["products"]],
                         "routes":[(r["source"],r["destination"],r["products"],r["lead_time"],r["mode"]) for r in d["routes"]],
                         "recipes":[(r["node"],r["output"],[i["product"] for i in r["inputs"]]) for r in d["recipes"]]}))


def audit(root,dataset):
    records=read_catalog(dataset)
    config,ch=load_config(root/"configs/v1.yaml")
    errors=[]
    ids=set()
    exact=collections.defaultdict(list)
    topologies=collections.defaultdict(list)
    cells=collections.Counter()
    assurance=collections.Counter()
    primary=second=0
    sizes=[]; times=[]; bindings=[]
    revisions=collections.Counter()
    review_queue=[]
    target=config["target_base_instances"]
    second_required=config["review"]["minimum_second_review_records"]
    sample_ids={f"cmx_{i:06}" for i in range(1,second_required+1)}
    for record in records:
        iid=record.get("instance_id","unknown")
        try:
            validate("instance",record)
            if iid in ids: raise ValueError("duplicate ID")
            ids.add(iid)
            original_config=construction_config(root,record,config,ch)
            d=record["problem"]["data"]
            validate_domain(d)
            if any(record[k]!=d[k] for k in ("family","structural_level","features","units")):
                raise ValueError("catalog metadata differs from business data")
            if record["verification"]["assurance_level"] == "UNVERIFIED":
                raise ValueError("unverified record cannot enter the corpus")
            for path,h in record["content_hashes"].items():
                if digest(safe_path(root,path).read_bytes()) != h:
                    raise ValueError(f"checksum mismatch: {path}")
            def load(name):
                return json.loads(safe_path(root,record["reference"][name]).read_text(encoding="utf-8"))
            if load("input")!=d: raise ValueError("input differs from catalog")
            ir=load("ir"); validate_ir(ir)
            vm=load("variable_map"); validate("variable_map",vm)
            if ir!=build_ir(d): raise ValueError("IR regeneration mismatch")
            text,mapping=compile_wcnf(ir)
            if vm!=mapping or text!=safe_path(root,record["reference"]["wcnf"]).read_text(): raise ValueError("encoding regeneration mismatch")
            if render_math(ir)!=safe_path(root,record["reference"]["mathematical"]).read_text(): raise ValueError("mathematical rendering mismatch")
            if not consistency(d,record["problem"]["description"]) or record["problem"]["description"]!=safe_path(root,record["reference"]["description"]).read_text(): raise ValueError("description mismatch")
            profile={**original_config["profiles"][d["structural_level"]],**original_config.get("family_profile_overrides",{}).get(d["family"],{}).get(d["structural_level"],{})}
            regenerated,_=generate(d["family"],d["structural_level"],record["provenance"]["seed"],profile)
            if regenerated!=d: raise ValueError("seed reproduction mismatch")
            verification=load("verification")
            if verification!=record["verification"] or load("provenance")!=record["provenance"] or load("review")!=record["review"]: raise ValueError("evidence copy mismatch")
            if verification["native"]["status"]!="OPTIMAL" or verification["maxsat"]["status"]!="OPTIMAL": raise ValueError("backend not optimal")
            if verification["native"]["absolute_gap_limit"]!=0 or verification["native"]["relative_gap_limit"]!=0: raise ValueError("nonzero optimality gap")
            solution=load("solution")
            checks=[check(d,solution[k]) for k in ("native_assignment","maxsat_assignment")]
            if not all(c["valid"] and c["cost"]==record["reference_optimum"] for c in checks): raise ValueError("business solution invalid")
            if checks!=[verification["native_checker"],verification["maxsat_checker"]]: raise ValueError("checker evidence mismatch")
            w=WCNF(from_string=text)
            signed=set(solution["boolean_assignment"])
            if any(x in signed and -x in signed for x in signed) or {abs(x) for x in signed} != set(range(1,w.nv+1)): raise ValueError("incomplete Boolean witness")
            if any(not any(l in signed for l in c) for c in w.hard): raise ValueError("unsatisfied hard clause")
            violation=sum(weight for c,weight in zip(w.soft,w.wght) if not any(l in signed for l in c))
            if decode(list(signed),vm)!=solution["maxsat_assignment"]: raise ValueError("decoder mismatch")
            transform=record["objective_transform"]
            costs=[violation*transform["multiplier"]+transform["offset"],verification["maxsat"]["cost"],verification["native"]["cost"],solution["cost"],verification["native"]["best_bound"]]
            if any(c!=record["reference_optimum"] for c in costs) or violation!=verification["maxsat"]["violation_cost"] or w.topw<=sum(w.wght): raise ValueError("cost/transform mismatch")
            planted=json.loads((safe_path(root,record["reference"]["input"]).parent/"feasibility_witness.json").read_text())
            if not check(d,planted)["valid"]: raise ValueError("invalid planted witness")
            exact[business_hash(d)].append(iid); topologies[topology_hash(d)].append(iid)
            cells[d["family"]+"/"+d["structural_level"]]+=1
            assurance[verification["assurance_level"]]+=1
            revisions[record["provenance"]["source_tree_hash"]]+=1
            sizes.append({"variables":vm["variable_count"],"clauses":vm["hard_clauses"]+vm["soft_clauses"],"wcnf_bytes":len(text)})
            times.append(verification["native"]["seconds"]+verification["maxsat"]["seconds"])
            a=solution["native_assignment"]
            bindings.append(sum(1 for c in ir["constraints"] if c["type"]=="linear" and c["sense"]!="eq" and sum(t["coefficient"]*a[t["var"]] for t in c["terms"])==c["rhs"]))
            review=record["review"]
            if review["primary"] and review["second"] and review["primary"]["reviewer"]==review["second"]["reviewer"]:
                raise ValueError("primary and second reviewers must differ")
            if review["primary"] and review["primary"]["approved"]: primary+=1
            if review["second"] and review["second"]["approved"]: second+=1
            review_queue.append({"instance_id":iid,"description":record["reference"]["description"],"input":record["reference"]["input"],"model":record["reference"]["mathematical"],
                                 "second_review_required":iid in sample_ids,"primary":review["primary"],"second":review["second"]})
        except Exception as e:
            errors.append({"instance_id":iid,"error":str(e)})
    duplicate_groups=[v for v in exact.values() if len(v)>1]
    if duplicate_groups: errors.append({"error":"exact business duplicates","groups":duplicate_groups})
    ledger=read_catalog(root/"audit/candidate_ledger.jsonl")
    outcomes=collections.Counter(r["status"] for r in ledger)
    calibration_path=root/"audit/history/calibration_initial-candidate_ledger.jsonl"
    calibration=read_catalog(calibration_path if calibration_path.exists() else root/"audit/calibration_initial/candidate_ledger.jsonl")
    by_cell=collections.defaultdict(collections.Counter)
    for r in ledger: by_cell[r["family"]+"/"+r["level"]][r["status"]]+=1
    quota_ok=len(records)==target and len(cells)==40 and set(cells.values())=={config["instances_per_family_level"]} and ids=={f"cmx_{i:06}" for i in range(1,target+1)}
    sample_reviewed=sum(bool(r["second"] and r["second"]["approved"]) for r in review_queue if r["second_review_required"])
    ready=not errors and quota_ok and primary==target and sample_reviewed>=second_required
    def stats(values):
        return {"min":min(values,default=0),"max":max(values,default=0),"mean":sum(values)/len(values) if values else 0}
    report={"status":"RELEASE_READY" if ready else "INCOMPLETE_RELEASE", "record_count":len(records),"errors":errors,"quota_satisfied":quota_ok,
            "family_counts":dict(collections.Counter(r["family"] for r in records)),"family_level_counts":dict(sorted(cells.items())),"assurance_counts":dict(assurance),
            "primary_reviews_completed":primary,"second_reviews_completed":second,"stratified_second_reviews_completed":sample_reviewed,
            "release_blockers":([] if primary==target else ["Human consistency review required for every description"])+([] if sample_reviewed>=second_required else [f"Stratified second review required for at least {second_required} descriptions"])+([] if quota_ok else ["Corpus quotas incomplete"]),
            "target_record_count":target,"second_reviews_required":second_required,
            "exact_duplicate_groups":duplicate_groups,"topology_group_count":len(topologies),"repeated_topology_groups":[v for v in topologies.values() if len(v)>1],
            "near_duplicate_method":"Identical topology/product-eligibility/lead-time/shelf-life signature; numeric values omitted. This is a screening report, not a semantic equivalence proof.",
            "encoder_statistics":{k:stats([s[k] for s in sizes]) for k in ("variables","clauses","wcnf_bytes")},"reference_seconds":stats(times),"binding_inequalities":stats(bindings),
            "candidate_outcomes":dict(outcomes),"candidate_outcomes_by_family_level":{k:dict(v) for k,v in sorted(by_cell.items())},"construction_attempts":len(ledger),
            "calibration_outcomes":dict(collections.Counter(r["status"] for r in calibration)),
            "source_tree_hash_counts":dict(revisions),"audit_scope":"Every artifact rehashed; models and encodings regenerated; both stored solutions checked; WCNF hard/soft clauses evaluated. Optimizers are not rerun by this audit.",
            "checked_at":datetime.datetime.now(datetime.timezone.utc).isoformat()}
    atomic(root/"audit/quality_report.json",dumps(report))
    atomic(root/"audit/review_queue.jsonl","".join(json.dumps(r,sort_keys=True)+"\n" for r in review_queue))
    return report


def import_reviews(root,path):
    """Import explicit human attestations; no automatic approval or inferred reviewer."""
    updates=read_catalog(path)
    records=read_catalog(root/CATALOG_PATH)
    by_id={r["instance_id"]:r for r in records}
    changes=[]
    for u in updates:
        if set(u)!={"instance_id","kind","review"} or u["kind"] not in ("primary","second"):
            raise ValueError("invalid review import shape")
        rec=by_id[u["instance_id"]]
        if rec["review"][u["kind"]] is not None: raise ValueError("review already exists; retain original and resolve separately")
        v=u["review"]
        if not v.get("reviewer") or not v.get("date") or not v.get("approved"):
            raise ValueError("requires explicit human reviewer, date, and approval")
        datetime.date.fromisoformat(v["date"])
        rec["review"][u["kind"]]=v
        if rec["review"]["primary"] and rec["review"]["second"] and rec["review"]["primary"]["reviewer"]==rec["review"]["second"]["reviewer"]:
            raise ValueError("second review requires a different reviewer")
        if rec["review"]["primary"] and rec["review"]["primary"]["approved"]: rec["review"]["status"]="APPROVED"
        txt=dumps(rec["review"])
        rec["content_hashes"][rec["reference"]["review"]]=digest(txt)
        validate("instance",rec)
        changes.append((rec,txt))
    for rec,txt in changes:
        atomic(root/rec["reference"]["review"],txt)
        atomic((root/rec["reference"]["review"]).parent/"_record.json",dumps(rec))
    save_catalog(root,records)


def package(root,dataset,output):
    report=audit(root,dataset)
    if report["errors"]: raise ValueError("audit errors prevent packaging")
    output=root/output if not output.is_absolute() else output
    output.mkdir(parents=True,exist_ok=True)
    records=read_catalog(dataset)
    # Report readiness truthfully even though a provisional review bundle is useful.
    source_commit=subprocess.run(["git","rev-parse","HEAD"],cwd=root,capture_output=True,text=True).stdout.strip() or None
    files={CATALOG_PATH:dataset.read_bytes()}
    for rec in records:
        for p in rec["content_hashes"]: files[p]=(root/p).read_bytes()
    for p in ("audit/quality_report.json","audit/build_manifest.json","audit/candidate_ledger.jsonl","audit/rejected_candidates.jsonl","audit/review_queue.jsonl","README.md","DATASET_CARD.md","DATA_LICENSE","DATASET_NOTICE.md","configs/v1.yaml","configs/chainmax-1k.yaml","requirements.lock"):
        files[p]=(root/p).read_bytes()
    for p in (root/"audit/history").glob("*.json*"):
        files[p.relative_to(root).as_posix()]=p.read_bytes()
    archive=output/ARCHIVE_NAME
    # Deterministic tar metadata; run-dependent evidence remains explicitly included.
    with archive.open("wb") as raw:
        with gzip.GzipFile(filename="",mode="wb",fileobj=raw,mtime=0) as gz:
            with tarfile.open(fileobj=gz,mode="w") as tar:
                for name,data in sorted(files.items()):
                    info=tarfile.TarInfo(name); info.size=len(data); info.mtime=0; info.mode=0o644
                    tar.addfile(info,io.BytesIO(data))
    checksum=digest(archive.read_bytes())
    manifest={"dataset_name":DATASET_NAME,"dataset_version":DATASET_VERSION,"status":report["status"],"publication_status_at_packaging":"UPLOAD_PENDING","publication_receipt":"PUBLICATION.json","record_count":len(records),
              "family_counts":report["family_counts"],"family_level_counts":report["family_level_counts"],"assurance_counts":report["assurance_counts"],
              "release_blockers":report["release_blockers"],"source_commit":source_commit,"source_tree_hash":source_hash(root),
              "config_hash":digest((root/"configs/v1.yaml").read_bytes()),"tool_versions":versions(),"archive_sha256":checksum,"archive_bytes":archive.stat().st_size,
              "encoding_dialect":"legacy_dimacs_wcnf","catalog_path":CATALOG_PATH,"files":{n:digest(b) for n,b in sorted(files.items())}}
    atomic(output/"release_manifest.json",dumps(manifest))
    atomic(output/"SHA256SUMS",f"{checksum}  {archive.name}\n{digest((output/'release_manifest.json').read_bytes())}  release_manifest.json\n")
    atomic(output/"release_notes.md",f"# {DATASET_NAME} v{DATASET_VERSION}\n\nReference status: {report['status']}.\n\n{len(records)} cross-checked problems. This is a provisional corpus with human review pending.\n\n"+"\n".join(f"- {x}" for x in report["release_blockers"])+"\n")
    # Verify every member and its checksum through a fresh decompression stream.
    with tarfile.open(archive,"r:gz") as tar:
        members=tar.getmembers()
        if {m.name for m in members}!=set(files): raise ValueError("archive path mismatch")
        for member in members:
            if not member.isfile() or digest(tar.extractfile(member).read())!=manifest["files"][member.name]: raise ValueError("archive member checksum mismatch")
    return {k:manifest[k] for k in ("status","record_count","archive_sha256","archive_bytes","release_blockers")}
