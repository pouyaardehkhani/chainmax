# Reproduction

Tested locally on Windows x64 with Python 3.12.0. Use Python 3.12 and an isolated
environment. Pinned OR-Tools 9.15.6755, PySAT 1.9.dev17, and Pindakaas 0.6.1 have
compatible Windows wheels. This project does not use the older PBLib PB binding.
The complete resolved dependency set is in requirements.lock.

From the ChainMax project root in PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.lock
python -m pip install --no-build-isolation --no-deps -e .
python -m chainmax doctor
python -m pytest -q
python -m chainmax build --config configs/v1.yaml --accepted-limit 40
python -m chainmax build --config configs/v1.yaml --accepted-limit 100 --resume
python -m chainmax build --config configs/v1.yaml --accepted-limit 1000 --resume
python -m chainmax audit --dataset data/chainmax-1k.jsonl --all
python -m chainmax package --dataset data/chainmax-1k.jsonl --output releases/v1.0.0
```

On POSIX, activate `.venv/bin/activate`; all `python -m` commands are identical.
Linux is covered by the provided CI configuration but is not claimed as a locally
executed full 1,000-instance build.

Accepted limits are cumulative. IDs traverse the 40 family/level cells in order,
then repeat; 25 rounds produce exact quotas. Candidate seeds are the first eight
hexadecimal digits of SHA-256(`master_seed:instance_id:attempt`) interpreted as an
unsigned integer. Attempt numbers and rejected candidates remain in append-only
ledgers. Regenerating the *accepted* artifacts requires their recorded seed,
attempt, frozen configuration, and pinned sources; timeout filtering can select
different accepted attempt numbers on another machine. Exact repeat of a new
wall-time-filtered build is therefore not guaranteed. The audit reproduces every
accepted input, IR, WCNF, mapping, and statement from its recorded provenance.

Never launch two writers. The build uses an exclusive PID lock. After a hard crash,
check that PID is gone before removing a stale audit/build.lock. Completed
directories contain recovery records and are recovered after catalog-write
interruption. Incomplete staging directories are preserved in audit/ rather than
deleted. Atomic replace protects each file. Existing accepted IDs cannot be
overwritten; configuration changes are rejected during resume. Old calibration
artifacts live under audit/calibration_initial/ and are not additional corpus IDs.

Limits: two worker processes, 45 seconds and 1,536 MiB resident memory per active
candidate worker, CP-SAT at most 15 seconds with zero absolute/relative gap,
and eight attempts per ID. Resident limits include the persistent interpreter
and imported solver libraries; these are polled every 40 ms, not a kernel-level
allocation cap. Interrupted/inconclusive attempts are not accepted as infeasible.
The observed construction statistics are in the local audit/quality_report.json.

The audit does not rerun optimization: it validates schemas and every checksum,
regenerates deterministic artifacts, reparses WCNF, recomputes both costs, and
checks complete stored native and Boolean witnesses. Original completed optimal
solver evidence is stored per record. To independently rerun solvers on an input:

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

The release package is provisional until human review requirements are met.
See [annotation guidelines](annotation_guidelines.md). Full data stay outside Git.
