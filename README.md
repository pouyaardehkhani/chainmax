# ChainMax-1K

A Verified Supply-Chain Benchmark for LLM Formulation and MaxSAT Optimization.

ChainMax-1K supports formulation of a mathematical optimization model from language
and structured data, followed by weighted partial MaxSAT optimization. It contains
realistic synthetic planning problems with exact demand, bounded integer quantities,
Boolean activations, and nonnegative integer costs in cents. It is one labeled
corpus with no training or dataset splits. No models are trained or fine-tuned.

**Status:** All 1,000 local base problems have completed independent reference
verification. The full artifact audit and 63 software tests pass. Required human description reviews are
pending. This is not a published release or a claim of domain-expert approval.
Source and generated data are separate. The intended source repository is named
`chainmax`; its remote owner/destination has not been configured.
See the [local build report](BUILD_REPORT.md) for completed checks and outstanding
human-review requirements.

## Quick start

Tested on Windows x64 with Python 3.12.0. Run from the project root:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.lock
python -m pip install --no-build-isolation --no-deps -e .
python -m chainmax doctor
python -m pytest -q
```

The doctor solves the nine-cent fixture with both solvers. The full resolved lock
pins OR-Tools 9.15.6755, PySAT 1.9.dev17, and Pindakaas 0.6.1. No paid model API is
needed. See [reproduction](docs/reproduction.md) for resource limits and POSIX setup.

## Download the dataset

Dataset download: DATASET_DOWNLOAD_URL

The full dataset is hosted separately from the source repository. This repository
does not include the data/ folder. DATASET_DOWNLOAD_URL is a placeholder; replace
it with the actual archive URL when hosted. Verify SHA256SUMS before extracting
the archive in this project root to create data/.

After obtaining the archive and accompanying SHA256SUMS/manifest, verify in
PowerShell from their directory, then extract from the project root:

```powershell
$expected = ((Get-Content SHA256SUMS | Select-Object -First 1) -split '\s+')[0]
$actual = (Get-FileHash chainmax-1k-v1.0.0.tar.gz -Algorithm SHA256).Hash.ToLowerInvariant()
if ($actual -ne $expected) { throw 'Dataset checksum mismatch' }
tar -xzf chainmax-1k-v1.0.0.tar.gz
python -m chainmax audit --dataset data/chainmax-1k.jsonl --all
```

Keep the checksum files with the archive. The local prepared bundle is provisional
until human review is complete; see its release manifest for exact status.

## Load an instance

```python
import json
from pathlib import Path
root = Path.cwd()
with (root / "data/chainmax-1k.jsonl").open(encoding="utf-8") as catalog:
    instance = json.loads(next(catalog))
print(instance["instance_id"], instance["family"], instance["structural_level"])
print(instance["problem"]["description"])
print(instance["problem"]["data"]["demands"])
reference_model = json.loads((root / instance["reference"]["ir"]).read_text())
print(reference_model["objective"])
```

Descriptions and answers are separate fields. A later inference-only application
can choose its own prompt views; query reference answers must not enter its input.
No ICL selection, LLM experiments, leaderboard, or solver deadline evaluation is
implemented here.

## Worked example

Warehouse A holds two items and B holds two. A market requires exactly three.
Shipping costs two cents per item from A and five from B; unused stock may remain.

```
x_A, x_B integer in [0, 2]
x_A + x_B = 3
minimize 2*x_A + 5*x_B
```

The feasible shipping plans are (1,2), cost 12, and (2,1), cost **9 cents**.
Enumeration, CP-SAT, RC2, and the direct checker agree on 9. The executable input
is [tests/fixtures/nine_cent.json](tests/fixtures/nine_cent.json).

## Coverage

The corpus contains 100 base problems per family and 25 in every family/level
cell: ten families Ã— four structural levels Ã— 25 = 1,000. L1â€“L4 describe topology,
dimensions and interacting features, not measured solver hardness. Narrative
template choice is independent of level. [Configuration](configs/v1.yaml) records
dimensions, calibrated family overrides, seeds, and resource/attempt budgets.

| ID | Family | Base count |
| --- | --- | ---: |
| F01 | Capacitated warehouse-to-market transport | 100 |
| F02 | Multi-echelon distribution | 100 |
| F03 | Warehouse activation | 100 |
| F04 | Route activation | 100 |
| F05 | Multiple products with shared capacity | 100 |
| F06 | Inventory and lead times | 100 |
| F07 | Integer trucks and mode eligibility | 100 |
| F08 | Minimum lots and sourcing dependencies | 100 |
| F09 | Perishable products, ages, expiry and disposal | 100 |
| F10 | Production, integer bills of materials and distribution | 100 |

## Ground truth and assurance

Domain data are authoritative. CP-SAT constructs a native model directly from
business tables. Separately, a typed IR compiles to WCNF and PySAT RC2 solves it.
A direct event-ledger checker checks both decoded business assignments and
recomputes integer costs. Core acceptance requires both solvers to terminate
optimally and exact cost agreement. CP-SAT absolute and relative gap limits are
zero. A planted witness establishes feasibility only. Timeouts, incomplete results,
resource failures, and disagreements are recorded and never labeled optima.

`CROSS_CHECKED` means both optimizers completed and direct checks agree;
`EXHAUSTIVE` additionally means every tiny business assignment was enumerated;
`PROOF_CHECKED` requires an independently checked certificate; `UNVERIFIED` means
required evidence is missing. The local corpus uses CROSS_CHECKED; no checked
formal proof is claimed. Software fixtures test projected equivalence of the IR
and CNF, plus targeted mutations, time/age boundaries and metamorphic properties.

Automated numerical/text consistency checks do not establish English semantic
equivalence. All 1,000 descriptions need primary human consistency review and at
least 100 stratified descriptions need independent second review. None has been
fabricated. See [annotation guidelines](docs/annotation_guidelines.md).

## WCNF conventions

Legacy DIMACS: `p wcnf variables clauses top`, then integer weight, signed literals,
and terminating zero. Hard clauses use `top = sum(soft weights) + 1`. Every bounded
integer uses binary bits with hard domain restrictions (including upper bound zero).
Signed pseudo-Boolean constraints compile with pinned BDD encoding. Nonzero costs
produce soft unit clauses on negated decision bits. Minimized violated-soft-clause
cost maps to business cost as `multiplier * violation_cost + offset`.
Each variable map records primary bits, finite domains, business meanings, auxiliary
range, clause/weight statistics, encoder, dialect, and objective transform.
There is no reconstruction-destroying preprocessing. See [semantics](docs/semantics.md).

## Repository and extracted dataset

Tracked source contains `src/chainmax/`, `configs/`, `schemas/`, `tests/fixtures/`,
`docs/`, requirements.lock, licenses, citation metadata and CI. The source repository
excludes the entire data/ directory, generated audit/ records and releases/ assets.
Downloading or generating data creates these ignored local paths:

```
data/chainmax-1k.jsonl
data/instances/cmx_000001/ ... cmx_001000/
  problem.md, input.json, reference_model.json, reference_model.md
  reference.wcnf, variable_map.json, reference_solution.json
  verification.json, provenance.json, review.json, feasibility_witness.json
audit/candidate_ledger.jsonl, rejected_candidates.jsonl, build_manifest.json
audit/quality_report.json, review_queue.jsonl
releases/v1.0.0/chainmax-1k-v1.0.0.tar.gz
releases/v1.0.0/SHA256SUMS, release_manifest.json, release_notes.md
```

Locally generated `_record.json` files support crash recovery; the archive's single
catalog is authoritative and those redundant recovery copies are not needed.

## Schema

Catalog records include identity/version, family/level/features, explicit units,
problem description/data/assumptions, artifact references, exact optimum and
objective transform, verification, provenance, review, and artifact SHA-256 hashes.
There is no split field. Machine-readable schemas:
[instance](schemas/instance.schema.json), [domain](schemas/domain.schema.json),
[IR](schemas/model_ir.schema.json), [variable map](schemas/variable_map.schema.json),
[verification](schemas/verification.schema.json).

## Reproduce and audit

```powershell
python -m chainmax build --config configs/v1.yaml --accepted-limit 40
python -m chainmax build --config configs/v1.yaml --accepted-limit 100 --resume
python -m chainmax build --config configs/v1.yaml --accepted-limit 1000 --resume
python -m chainmax audit --dataset data/chainmax-1k.jsonl --all
python -m chainmax package --dataset data/chainmax-1k.jsonl --output releases/v1.0.0
```

Accepted limits are cumulative; use `--resume` when a catalog already exists.
Frozen configuration, immutable IDs, atomic files and recovery records protect
accepted instances. The configuration enforces two isolated workers, 45 seconds
and 1,536 MiB resident memory per candidate, 15 seconds for native solving and
eight attempts per ID. Audit regenerates every accepted deterministic artifact
from recorded provenance and rechecks stored solutions; it does not rerun solvers.
Fresh wall-time-filtered builds can accept different attempt numbers on different
machines. See [reproduction](docs/reproduction.md) and [progress](docs/progress.md).

Packaging verifies decompressed member checksums and prepares a provisional bundle
when human review is pending. Its manifest records readiness without claiming final
release acceptance. [Publication instructions](docs/github_release.md) describe the
remaining remote steps and the source/data separation.

## Limitations, citation and licenses

These are deterministic, discrete, realistic synthetic problems, not operational
company records or industrial deployment results. Small bounded dimensions and
complete-reference acceptance impose a tractability filter. Structural levels are
not hardness labels; repeated topologies and numeric diversity are reported by the
audit. The controlled wording and templates await human review. Uncertainty,
continuous quantities, vehicle tours, arbitrary nonlinear costs and multiple
objectives are outside v1. No LLM performance measurements have been conducted.

Code: [MIT](LICENSE). Dataset: [CC BY 4.0](DATA_LICENSE), selected by the owner;
see [attribution notice](DATASET_NOTICE.md). See [dependency notices](THIRD_PARTY_NOTICES.md)
for the licenses reported by the installed distributions.
Use [CITATION.cff](CITATION.cff) and cite ChainMax-1K version 1.0.0, creator pseudonym
pouyaardehkhani, source revision, config hash and archive checksum for a local build.
No DOI or hosted release URL is claimed. See the [dataset card](DATASET_CARD.md)
and [contribution guidance](CONTRIBUTING.md) for limitations and reporting errors.
