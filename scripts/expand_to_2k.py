"""Explicit, restartable metadata migration; all 1K business/solver artifacts stay intact."""
import datetime
import json
import shutil
import subprocess
from pathlib import Path
from chainmax.identity import DATASET_NAME,CATALOG_PATH
from chainmax.io import atomic,digest,dumps
from chainmax.pipeline import read_catalog,save_catalog,load_config
from chainmax.schemas import validate

root=Path.cwd().resolve()
legacy_path=root/"data/chainmax-1k.jsonl"
current_path=root/CATALOG_PATH
if current_path.exists():
    raise SystemExit("2K catalog already exists; migration is complete. Use build --resume.")
work=root/"audit/migration_work"
work.mkdir(parents=True,exist_ok=True)
history=root/"audit/history"
history.mkdir(parents=True,exist_ok=True)
backup=work/"chainmax-1k.jsonl"
if not backup.exists():
    shutil.copyfile(legacy_path,backup)
records=read_catalog(backup)
assert len(records)==1000 and {r["instance_id"] for r in records}=={f"cmx_{i:06}" for i in range(1,1001)}
c,ch=load_config(root/"configs/v1.yaml")
legacy,lh=load_config(root/"configs/chainmax-1k.yaml")
assert c["target_base_instances"]==2000 and legacy["target_base_instances"]==1000
state_path=work/"state.json"
if state_path.exists():
    migration=json.loads(state_path.read_text())
else:
    revision=subprocess.run(["git","rev-parse","HEAD"],capture_output=True,text=True,check=True).stdout.strip()
    migration={"from_dataset":"ChainMax-1K","from_catalog_sha256":digest(backup.read_bytes()),"dataset_config_hash":ch,
               "migration_source_revision":revision,"migrated_at":datetime.datetime.now(datetime.timezone.utc).isoformat()}
    atomic(state_path,dumps(migration))
assert migration["dataset_config_hash"]==ch
preserved={}
for r in records:
    assert r["dataset_name"]=="ChainMax-1K" and r["provenance"]["config_hash"]==lh
    original_provenance=dumps(r["provenance"])
    r["dataset_name"]=DATASET_NAME
    r["provenance"]["dataset_migration"]=migration
    new_provenance=dumps(r["provenance"])
    preserved[r["instance_id"]]={}
    for path,expected in r["content_hashes"].items():
        current=digest((root/path).read_bytes())
        if path==r["reference"]["provenance"]:
            assert current in (digest(original_provenance),digest(new_provenance))
        else:
            assert current==expected,(r["instance_id"],path)
            preserved[r["instance_id"]][path]=expected
    atomic(root/r["reference"]["provenance"],new_provenance)
    r["content_hashes"][r["reference"]["provenance"]]=digest(new_provenance)
    validate("instance",r)
    atomic((root/r["reference"]["input"]).parent/"_record.json",dumps(r))
for name in ("quality_report.json","build_manifest.json"):
    dest=history/("chainmax-1k-"+name)
    if not dest.exists(): shutil.copyfile(root/"audit"/name,dest)
for folder in ("calibration_initial","calibration_frozen100"):
    for name in ("candidate_ledger.jsonl","rejected_candidates.jsonl","build_manifest.json"):
        origin=root/"audit"/folder/name
        dest=history/(folder+"-"+name)
        if origin.exists() and not dest.exists(): shutil.copyfile(origin,dest)
atomic(history/"chainmax-1k-preserved-artifacts.json",dumps(preserved))
save_catalog(root,records)
# Preserve the original versioned archive, manifest, checksums and release notes.
old_release=(root/"releases/v1.0.0").resolve()
historical_release=(root/"releases/chainmax-1k-v1.0.0").resolve()
assert old_release.is_relative_to(root) and historical_release.is_relative_to(root)
if old_release.exists() and not historical_release.exists():
    old_release.rename(historical_release)
legacy_path.unlink(missing_ok=True)  # exact file, backed up above and in the old archive
atomic(root/"audit/migration_report.json",dumps({"status":"COMPLETE","from_dataset":"ChainMax-1K","to_dataset":DATASET_NAME,
    "migrated_records":1000,"business_and_solver_artifacts_preserved":True,"original_catalog_sha256":migration["from_catalog_sha256"],
    "original_config_hash":lh,"dataset_config_hash":ch,"migration":migration,
    "changes":["dataset identity","provenance migration annotation","provenance checksum","catalog and local recovery records"],
    "new_record_range":["cmx_001001","cmx_002000"],"published":False}))
print("Migrated 1,000 records to chainmax-2k; every business, model and solver artifact preserved.")
