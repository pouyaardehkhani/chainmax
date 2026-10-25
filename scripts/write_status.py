"""Write current 2K documentation from the measured audit, never from target-only claims."""
import json
from pathlib import Path
import yaml

root=Path.cwd()
config=yaml.safe_load((root/"configs/v1.yaml").read_text())
r=json.loads((root/"audit/quality_report.json").read_text())
assert r["record_count"]==config["target_base_instances"]==2000 and r["quota_satisfied"] and not r["errors"]
publication=json.loads((root/"PUBLICATION.json").read_text()) if (root/"PUBLICATION.json").exists() else {}
repository=publication.get("repository_url")
repo_text=f"Repository: [{repository}]({repository})." if repository else "GitHub publication is being prepared for the verified account `pouyaardehkhani`, repository `chainmax`."
readme='''# chainmax-2k

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

@REPOSITORY@

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
$expected = ((Get-Content SHA256SUMS | Select-Object -First 1) -split '\\s+')[0]
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
.\\.venv\\Scripts\\Activate.ps1
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
'''.replace('@REPOSITORY@',repo_text)
(root/"README.md").write_text(readme,encoding="utf-8",newline="\n")

stats=r["encoder_statistics"]
groups=r["repeated_topology_groups"]
card=f'''# chainmax-2k dataset card

Version 1.0.0. Exactly 2,000 unique base problems in one labeled corpus, without
dataset splits, model training or fine-tuning. Each of ten families has 200 records;
each of the 40 family/level cells has 50. All 2,000 are CROSS_CHECKED. Human
description/template consistency review is pending: {r['primary_reviews_completed']}/2,000 primary
and {r['stratified_second_reviews_completed']}/200 stratified independent second reviews.
Reference status: **{r['status']}**. Public availability does not imply human approval.

## Intended use and origin

Inference-only formulation from English and numerical data, followed by MaxSAT
optimization against exact reference optima. Descriptions and answers are separate;
later prompt construction must hide the query answer. No LLM experiments or deadline
benchmarks are included. These are realistic synthetic planning problems, not
operational company data or industrial deployment results. No domain-expert review
has been claimed. Structural levels describe dimensions and interactions, not hardness.

The first 1,000 retain their original business inputs, models, encodings, costs and
solutions. Their construction provenance is preserved with a dataset-migration
annotation. New IDs cmx_001001 through cmx_002000 expand every cell from 25 to 50.
The migration report and preserved hashes are in audit/; historical 1K packaging is
kept separately from the current single corpus. No optional paraphrase counts as a
new base problem.

## Business and annotation methodology

Finite nonnegative integer quantities, Boolean activations, integer cents and exact
demand without shortages. Inputs specify routes, capacities, initial stock, timing,
age/expiry/disposal, activation scope, modes, truck counts and integer recipes.
Production is immediately available from raw inputs; truck costs supplement shipping.
Multiple optimal assignments are allowed. See docs/semantics.md and the full rules
in every description. Controlled wording includes verbatim input tables; numerical,
unit and leakage checks cannot establish natural-language semantic equivalence.
Required human review is described in docs/annotation_guidelines.md.

Native CP-SAT builds directly from domain tables, with zero absolute/relative gaps.
The separate typed IR compiles through binary expansion and signed PB normalization
to legacy DIMACS WCNF using pinned BDD encoding, then RC2 solves it. An independent
business event ledger checks both decoded plans and exact costs. CROSS_CHECKED is
cross-implementation evidence, not a formal optimality certificate. Tiny fixtures
exhaust all business assignments and auxiliary extensions. Mutation and metamorphic
tests cover boundaries, charges, timing, units and encoding bounds.

## Construction and selection effects

Two isolated workers, 45 seconds and 1,536 MiB resident memory per candidate,
15 seconds for native solving and eight attempts per ID. Memory is polled, not a
kernel allocation cap. Reference-optimality acceptance imposes a tractability filter.
Timeouts are never reported as infeasibility. Seeds, settings and all candidate
outcomes are retained. Initial calibration reduced large time/product dimensions
through explicit frozen config overrides; no hardness claim was made.

Current candidate outcomes (including the retained 1K construction):
`{json.dumps(r['candidate_outcomes'],sort_keys=True)}`.
Accepted 2,000 of {r['construction_attempts']:,} recorded attempts
({2000/r['construction_attempts']:.2%}). Zero audit errors; zero exact business duplicates.
There are {r['topology_group_count']} topology signatures, of which {len(groups)} repeat,
covering {sum(map(len,groups))} records. Signature grouping omits numerical values;
it is a near-duplicate screening report, not general graph-isomorphism or semantic
equivalence detection. Full membership and per-cell outcomes are in the quality report.

| Encoding statistic | Minimum | Mean | Maximum |
| --- | ---: | ---: | ---: |
'''
for key in ("variables","clauses","wcnf_bytes"):
    s=stats[key]; card+=f"| {key} | {s['min']:,} | {s['mean']:,.2f} | {s['max']:,} |\n"
times=r["reference_seconds"]
card+=f'''
Combined native/MaxSAT reference time per accepted candidate: mean {times['mean']:.3f}s,
maximum {times['max']:.3f}s, excluding generation, encoding and file writes. These
are construction observations, not a solver performance experiment.

## Reproducibility, availability and licenses

Use configs/v1.yaml and requirements.lock. Retained 1K records use the preserved
configs/chainmax-1k.yaml through their original config hash and explicit migration.
Audit reproduces deterministic input, IR, WCNF, mappings and statements from accepted
seeds. Runtime, timestamps and witnesses can vary; new wall-time-filtered builds can
accept different attempts. See docs/reproduction.md.

The owner explicitly requested including source, complete data, audit evidence and
archive in the GitHub repository. That supersedes the historical no-data policy.
The checksummed archive is releases/v1.0.0/chainmax-2k-v1.0.0.tar.gz. All package
members are rehashed through decompression. Human review remains required before
a final reviewed release. {repo_text}

Code is MIT; data CC BY 4.0, selected by the owner. Creator identity was verified
through the connected GitHub account: Pouya Ardehkhani (pouyaardehkhani). Cite version,
source revision, config hash and checksum; no DOI or paper is fabricated. Dependency
licenses remain their own. See CITATION.cff, DATA_LICENSE and THIRD_PARTY_NOTICES.md.
'''
(root/"DATASET_CARD.md").write_text(card,encoding="utf-8",newline="\n")
report=f'''# chainmax-2k build report

Exactly 2,000 unique base problems, 200 per family and 50 per family/level cell,
in one labeled corpus without splits. Both reference optimizers completed with
matching exact integer costs for every record; independent business checks passed.
The full artifact audit reports zero errors and zero exact duplicates. Assurance
is CROSS_CHECKED; no formal proof certificate or human approval is claimed.

All original 1K business and solver artifacts are preserved. Only dataset identity,
explicit migration provenance, its checksum and catalog/recovery metadata changed.
Original seeds/config/source revisions remain recorded. New records occupy IDs
cmx_001001 through cmx_002000. Migration evidence is in audit/migration_report.json.

The checksummed bundle is releases/v1.0.0/chainmax-2k-v1.0.0.tar.gz, with an external
release manifest and SHA256SUMS. Packaging decompresses and verifies every member.
Source, full corpus, reference artifacts, audit evidence and archive are included in
Git at the owner's explicit request. Temporary construction files remain local.

## Remaining review requirements

- Complete 2,000 actual human description/template consistency reviews.
- Complete 200 stratified second reviews with a different reviewer, plus disputes.
- Resolve issues, import attestations, rerun audit and regenerate the package.

Current primary reviews: {r['primary_reviews_completed']}; stratified second reviews:
{r['stratified_second_reviews_completed']}. Status: {r['status']}.

## Publication

{repo_text}
Upload receipts, once available, are recorded in PUBLICATION.json. A public
provisional corpus is distinct from a completed human-reviewed release. Code is
MIT and data CC BY 4.0, as selected by the owner.
'''
(root/"BUILD_REPORT.md").write_text(report,encoding="utf-8",newline="\n")
print("Updated 2K README, dataset card and build report from the measured audit.")
