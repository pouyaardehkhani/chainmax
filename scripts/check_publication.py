"""Check that the committed dataset is complete, within blob limits and free of scratch files."""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import subprocess
from chainmax.identity import DATASET_NAME,CATALOG_PATH,ARCHIVE_NAME
from chainmax.pipeline import load_config,read_catalog

p=argparse.ArgumentParser()
p.add_argument("--tracked",action="store_true")
args=p.parse_args()
root=Path.cwd()
config,_=load_config(root/"configs/v1.yaml")
records=read_catalog(root/CATALOG_PATH)
assert len(records)==config["target_base_instances"]==2000
assert all(r["dataset_name"]==DATASET_NAME for r in records)
assert set(Counter((r["family"],r["structural_level"]) for r in records).values())=={50}
assert len({r["instance_id"] for r in records})==2000
expected={CATALOG_PATH}|{path for r in records for path in r["content_hashes"]}
for path in expected:
    assert (root/path).is_file(),f"missing artifact: {path}"
for record in records:
    for path,wanted in record["content_hashes"].items():
        assert hashlib.sha256((root/path).read_bytes()).hexdigest()==wanted,f"artifact checksum mismatch: {path}"
package=root/"releases/v1.0.0"
for line in (package/"SHA256SUMS").read_text().splitlines():
    wanted,name=line.split(None,1)
    assert hashlib.sha256((package/name).read_bytes()).hexdigest()==wanted,name
manifest=json.loads((package/"release_manifest.json").read_text())
assert manifest["record_count"]==2000 and manifest["dataset_name"]==DATASET_NAME
if args.tracked:
    tracked=set(subprocess.run(["git","ls-files","-z"],capture_output=True,check=True).stdout.decode().split("\0"))-{ "" }
    assert expected<=tracked,f"untracked corpus artifacts: {len(expected-tracked)}"
    assert {p for p in tracked if p.startswith("data/")}==expected,"unexpected data files tracked"
    assert f"releases/v1.0.0/{ARCHIVE_NAME}" in tracked,"archive missing from Git"
    for path in tracked:
        parts=Path(path).parts
        assert not any(x in parts for x in (".venv","__pycache__","extracted_release","source_only","migration_work")),path
        assert Path(path).name not in (".env","build.lock","_record.json"),path
        assert (root/path).stat().st_size<100*1024**2,f"GitHub blob limit exceeded: {path}"
print(f"Publication contents verified: {len(records)} records, {len(expected)} data files, archive checksums valid.")
