# Reproducing chainmax-2k

Use Python 3.12 and requirements.lock. The local environment is Windows x64 with
Python 3.12.0, OR-Tools 9.15.6755, PySAT 1.9.dev17 and Pindakaas 0.6.1. Pindakaas
provides the pinned pseudo-Boolean implementation. The repository contains the full
2,000-record corpus and its archive, following the owner's revised storage policy.

From the project root in PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.lock
python -m pip install --no-build-isolation --no-deps -e .
python -m chainmax doctor
python -m pytest -q
python -m chainmax audit --dataset data/chainmax-2k.jsonl --all
```

On POSIX activate `.venv/bin/activate`. The workflow checks both Windows and Linux;
do not infer that a full local Linux construction was performed.

## Fresh incremental construction

A clone already contains all 2,000 records. To exercise incremental generation,
create a fresh workspace while retaining the installed package:

```powershell
New-Item -ItemType Directory -Force build/reproduction | Out-Null
Copy-Item -Recurse configs build/reproduction/configs
Push-Location build/reproduction
python -m chainmax build --config configs/v1.yaml --accepted-limit 40
python -m chainmax build --config configs/v1.yaml --accepted-limit 100 --resume
python -m chainmax build --config configs/v1.yaml --accepted-limit 2000 --resume
python -m chainmax audit --dataset data/chainmax-2k.jsonl --all
Pop-Location
```

Choose a new directory if build/reproduction already contains a prior build.
For a quick fresh-construction check, `python scripts/ci_smoke.py` creates an
isolated four-record corpus and audits it without altering the committed dataset.
The archive is prepared from the main project root with:

```powershell
python -m chainmax package --dataset data/chainmax-2k.jsonl --output releases/v1.0.0
```

The accepted limit is cumulative. IDs traverse the 40 family/level cells, repeating
for 50 rounds, giving 200 per family and 50 per cell. Seeds are the first eight
hexadecimal digits of SHA-256(`master_seed:instance_id:attempt`) as an unsigned
integer. All exclusions/attempts are logged. Requiring optimal reference solutions
creates a tractability filter: new wall-time-filtered builds may select different
accepted attempts on different machines. Regeneration of the *accepted* input,
IR, WCNF, mapping and text uses the seed and config recorded in each instance.
Runtime, timestamps and optimal witnesses can vary.

## Preserved 1K core and expansion

The 2K corpus retains the first 1,000 business problems and solver results. Original
construction uses configs/chainmax-1k.yaml, whose hash is unchanged. Their original
source revision, seed and configuration hash remain in provenance. A typed optional
dataset_migration annotation records the new dataset config hash, old catalog
hash, migration source revision and date. New IDs use configs/v1.yaml. Audit selects
the actual construction config for each record and verifies both paths faithfully.

The one-time `scripts/expand_to_2k.py` is for migrating the old local 1K build;
it must not be rerun on an already migrated catalog. Its durable journal supports
resuming the metadata migration. It verifies every old artifact hash, updates only
dataset identity and provenance metadata, retains the original archive, and records
the result in audit/migration_report.json. The original non-provenance hashes are
preserved in audit/history/chainmax-1k-preserved-artifacts.json. The old catalog is
inside the historical archive; the current corpus has one catalog and no splits.

## Limits and resume

Two persistent isolated workers; CP-SAT 15 seconds, candidate wall time 45 seconds,
resident worker memory 1,536 MiB, eight attempts per ID. Resident memory includes
the interpreter and libraries and is polled every 40 ms, rather than enforced by
a kernel allocation limit. CP-SAT absolute and relative gap tolerances are zero.
Incomplete, interrupted or feasible-only runs are never labeled optima/infeasible.

An exclusive PID lock prevents simultaneous writers. After a hard crash, verify
that the recorded process is gone before removing a stale audit/build.lock.
Atomic writes and local recovery records protect accepted IDs; configuration
changes require an explicit valid migration. Incomplete staging directories are
preserved in local audit scratch. They and redundant recovery files are excluded
from publication. Input/solver artifacts are never silently changed under an ID.

## What the audit verifies

`audit --all` checks every schema, reference path and checksum; regenerates accepted
input, IR, mathematical rendering, WCNF, variable map and text; directly checks both
business solutions; reparses WCNF; evaluates hard clauses and exact soft cost; and
checks quotas, IDs, duplicates, backend statuses and objective transforms. It uses
stored completed-optimal evidence rather than rerunning both optimizers.

To rerun the reference backends on a tiny example:

```python
import json
from pathlib import Path
from chainmax.native_reference import solve as native
from chainmax.encoding import compile_wcnf, solve as maxsat
from chainmax.model_builder import build_ir
from chainmax.checking import check
d = json.loads(Path("tests/fixtures/nine_cent.json").read_text())
a, b = native(d), maxsat(*compile_wcnf(build_ir(d)))
assert a["status"] == b["status"] == "OPTIMAL"
assert a["cost"] == b["cost"] == 9
assert check(d, b["assignment"])["valid"]
```

Packaging checks every member through decompression and writes archive/manifest
SHA-256 hashes. `scripts/check_publication.py --tracked` checks the committed corpus,
complete required files, archive checksum, excluded scratch paths and GitHub's
100 MiB per-file threshold. Human review remains a separate pending requirement.
