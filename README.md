# chainmax-2k

A Verified Supply-Chain Benchmark for LLM Formulation and MaxSAT Optimization.

**2,000 unique synthetic supply-chain problems**, each with a complete input,
bounded integer reference formulation, weighted partial MaxSAT encoding, decoded
solution and exact optimum. Both OR-Tools CP-SAT and PySAT RC2 completed optimally
and their independently checked costs agree. There is one labeled corpus, with no
dataset splits, model training or fine-tuning.

**Human description review is pending.** All 2,000 records are CROSS_CHECKED by
the reference backends; this is a provisional dataset, not domain-expert approval
or a formally proof-checked release. The full artifact audit reports zero errors
and zero exact business duplicates. See [BUILD_REPORT.md](BUILD_REPORT.md).

Repository: [https://github.com/pouyaardehkhani/chainmax](https://github.com/pouyaardehkhani/chainmax).

## Get the data

This repository includes the complete `data/` directory, reference solver artifacts,
audit evidence, and the checksummed archive, as requested by the owner. A Git clone
contains the full corpus immediately. The original 1K plan's separate-hosting policy
was superseded by that request.

- [Full archive](releases/v1.0.0/chainmax-2k-v1.0.0.tar.gz)
- [SHA256SUMS](releases/v1.0.0/SHA256SUMS)
- [Release manifest](releases/v1.0.0/release_manifest.json)
- [Single JSONL catalog](data/chainmax-2k.jsonl)
- [Quality report](audit/quality_report.json)
- [Human review queue](audit/review_queue.jsonl)

Verify the archive and extract into a project root, or use the files from a clone.
From the archive directory in PowerShell:

```powershell
$expected = ((Get-Content SHA256SUMS | Select-Object -First 1) -split '\s+')[0]
$actual = (Get-FileHash chainmax-2k-v1.0.0.tar.gz -Algorithm SHA256).Hash.ToLowerInvariant()
if ($actual -ne $expected) { throw 'Dataset checksum mismatch' }
```

From the project root, extraction uses:

```powershell
tar -xzf releases/v1.0.0/chainmax-2k-v1.0.0.tar.gz
```

## Quick start

Tested on Windows x64, Python 3.12.0. Use Python 3.12 and the locked environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.lock
python -m pip install --no-build-isolation --no-deps -e .
python -m chainmax doctor
python -m pytest -q
python -m chainmax audit --dataset data/chainmax-2k.jsonl --all
```

OR-Tools 9.15.6755, PySAT 1.9.dev17 and Pindakaas 0.6.1 are pinned. No paid model API
is required. On POSIX, activate `.venv/bin/activate`. GitHub Actions checks Windows
and Linux; local execution claims are limited to the platforms actually run.

## Load one instance

```python
import json
from pathlib import Path
root = Path.cwd()
with (root / "data/chainmax-2k.jsonl").open(encoding="utf-8") as catalog:
    instance = json.loads(next(catalog))
print(instance["instance_id"], instance["family"], instance["structural_level"])
print(instance["problem"]["description"])
print(instance["problem"]["data"]["demands"])
model = json.loads((root / instance["reference"]["ir"]).read_text())
print(model["objective"])
```

Descriptions/data and reference answers occupy separate fields. A later inference
application must hide the query's reference answer. ICL prompt selection, LLM
experiments, leaderboards and solver deadline evaluations are outside this project.

## Worked example

Warehouse A holds two items, B holds two, and a market requires exactly three.
Shipping costs two cents per item from A and five from B. Unused stock may remain.

```
x_A, x_B integer in [0, 2]
x_A + x_B = 3
minimize 2*x_A + 5*x_B
```

Feasible plans are (1,2), cost 12, and (2,1), cost **9 cents**. Enumeration, CP-SAT,
RC2 and the direct checker agree on 9. See [the fixture](tests/fixtures/nine_cent.json).
An actual corpus example is [cmx_000001](data/instances/cmx_000001/problem.md), whose
[formulation](data/instances/cmx_000001/reference_model.json),
[WCNF](data/instances/cmx_000001/reference.wcnf) and
[reference solution](data/instances/cmx_000001/reference_solution.json) are included.

## Coverage

There are **200 problems per family**, **50 per family/level cell**: ten families,
four structural levels, and 50 repetitions. L1 through L4 describe topology,
dimensions and interacting features, not measured solver hardness. Template choice
is independent of structural level.

| ID | Family | Base count |
| --- | --- | ---: |
| F01 | Capacitated warehouse-to-market transport | 200 |
| F02 | Multi-echelon distribution | 200 |
| F03 | Warehouse activation | 200 |
| F04 | Route activation | 200 |
| F05 | Multiple products with shared capacity | 200 |
| F06 | Inventory and lead times | 200 |
| F07 | Integer trucks and mode eligibility | 200 |
| F08 | Minimum lots and sourcing dependencies | 200 |
| F09 | Perishable products, ages, expiry and disposal | 200 |
| F10 | Production, integer bills of materials and distribution | 200 |

The first 1,000 business problems and solver artifacts were retained from ChainMax-1K.
An explicit migration changes dataset identity and annotates provenance; original
construction seeds, source revisions and config hashes remain intact. New IDs are
cmx_001001 through cmx_002000. See [migration evidence](audit/migration_report.json)
and [the preserved-artifact hashes](audit/history/chainmax-1k-preserved-artifacts.json).
The historical 1K archive remains under `releases/chainmax-1k-v1.0.0/`; it is not a
second partition of the current corpus.

## Ground truth, schemas and assurance

Domain data are authoritative. CP-SAT constructs a native model directly from
business tables, with zero absolute and relative optimality-gap tolerances.
Separately, a typed IR compiles into WCNF for RC2. A direct event-ledger checker
checks both plans and recomputes exact integer costs. A planted witness establishes
feasibility only. Timeouts and resource failures are logged and never labeled optima.

CROSS_CHECKED means independent optimizers completed and exact checks agreed.
EXHAUSTIVE additionally requires full enumeration of a tiny instance. PROOF_CHECKED
requires an independently checked certificate; none is claimed here. UNVERIFIED
records cannot enter this corpus. Automated text checks do not establish English
semantic equivalence: **2,000 primary human reviews and 200 stratified second
reviews are still pending**. See [annotation guidelines](docs/annotation_guidelines.md).

The closed schemas define [catalog records](schemas/instance.schema.json),
[domain inputs](schemas/domain.schema.json), [reference IR](schemas/model_ir.schema.json),
[Boolean mappings](schemas/variable_map.schema.json), and
[verification](schemas/verification.schema.json). Records include identity,
family/level/features, units, problem/data, artifact references, optimum and objective
transform, verification, provenance, review and artifact SHA-256 hashes. No split
field exists. [Semantics](docs/semantics.md) gives the complete business conventions.

## WCNF conventions

Legacy DIMACS uses `p wcnf variables clauses top`, then weight, signed literals and
zero. Hard clauses have `top = sum(soft weights) + 1`. Bounded integers use binary
bits with hard domain restrictions; signed pseudo-Boolean relations use pinned BDD
encoding. Nonzero costs create soft units on negated decision bits. Business cost
equals `multiplier * violated_soft_cost + offset`. Variable maps preserve primary
bits, finite domains, business meanings, auxiliary ranges and encoder statistics.

## Layout and reproduction

```
data/chainmax-2k.jsonl
data/instances/cmx_000001/ ... cmx_002000/
  problem.md, input.json, reference_model.json, reference_model.md
  reference.wcnf, variable_map.json, reference_solution.json
  verification.json, provenance.json, review.json, feasibility_witness.json
audit/quality_report.json, candidate_ledger.jsonl, rejected_candidates.jsonl
audit/build_manifest.json, review_queue.jsonl, migration_report.json, history/
releases/v1.0.0/chainmax-2k-v1.0.0.tar.gz
releases/v1.0.0/SHA256SUMS, release_manifest.json, release_notes.md
src/chainmax/, configs/, schemas/, tests/, docs/
```

Source, full data, reference artifacts, audit evidence and archives are committed.
Virtual environments, caches, temporary builds and redundant recovery files remain
local. [Publication checks](scripts/check_publication.py) verify tracked corpus
completeness, archive checksums and GitHub's per-file size limit.

```powershell
python -m chainmax build --config configs/v1.yaml --accepted-limit 2000 --resume
python -m chainmax audit --dataset data/chainmax-2k.jsonl --all
python -m chainmax package --dataset data/chainmax-2k.jsonl --output releases/v1.0.0
```

The accepted limit is cumulative. A clone already contains all 2,000 records.
[Reproduction instructions](docs/reproduction.md) explain fresh incremental builds,
accepted-seed reproduction, migration, resource budgets and atomic resume. Current
limits are two isolated workers, 45 seconds and 1,536 MiB resident memory per
candidate, 15 seconds for native solving, and eight attempts per ID. Audit regenerates
every deterministic artifact and checks stored witnesses; it does not rerun the
optimizers. Fresh wall-time-filtered builds can select different accepted attempts.

## Limitations, citation and licenses

These are deterministic, discrete synthetic problems, with no operational company
data or demonstrated industrial deployment. Reference-solver tractability filtering
and small bounded dimensions affect coverage. Repeated topologies and numerical
diversity are reported in the audit. Controlled wording/templates await human review.
Uncertainty, continuous quantities, vehicle tours, arbitrary nonlinear costs and
multiple objectives are outside v1. No LLM performance experiments were performed.

Code: [MIT](LICENSE). Data: [CC BY 4.0](DATA_LICENSE), selected by the owner.
See [attribution](DATASET_NOTICE.md), [dependency notices](THIRD_PARTY_NOTICES.md),
[CITATION.cff](CITATION.cff), [dataset card](DATASET_CARD.md),
[contributions](CONTRIBUTING.md), and [publication procedure](docs/github_release.md).
Cite chainmax-2k v1.0.0, creator Pouya Ardehkhani (`pouyaardehkhani`), source revision,
config hash and archive checksum. No DOI or paper is claimed.
