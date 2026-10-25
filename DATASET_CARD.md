# ChainMax-1K dataset card

Version 1.0.0, local construction; unpublished. The target is one labeled corpus
of 1,000 unique base problems, with no dataset splits and no model training.
All 1,000 local base problems have completed reference cross-checking and the
full artifact audit.
Human consistency reviews are pending for every description. There has been no
domain-expert review. License choices are MIT code and CC BY 4.0 data.

## Intended use

Inference-only translation of complete English and numerical input into a bounded
integer formulation, followed by MaxSAT optimization against exact reference costs.
Descriptions and gold answers are stored separately. A future ICL application
must construct its own prompt views and hide the query reference answer. That
application, LLM comparisons, repeated generation experiments and solver deadline
benchmarks are outside this project.

## Composition and origin

Synthetic, deterministic, realistic supply-chain planning data generated from
sampled feasible paths, with independent variation in demands, costs, slack,
routes, product/mode eligibility, periods, ages, lot sizes and recipes. The target
has 100 records per F01â€“F10 and 25 per L1â€“L4 cell; see [README](README.md). Levels
describe structural dimensions/couplings, not empirical hardness. Narrative
templates vary independently and do not create extra base IDs. No operational
company data or industrial deployment evidence is included.

## Business semantics

Finite nonnegative integer item quantities and Boolean activations; currency in
cents; exact demand without shortages. Allowed routes, initial stock, end stock,
shared volume capacity, activation scope, lead times, expiry/disposal and integer
bills of materials are explicit. Truck costs supplement shipping. Production
uses raw inputs and is immediately available. Multiple optima are allowed;
stored assignments are witnesses, not unique-answer claims. Detailed conventions
are in [semantics](docs/semantics.md) and are repeated in each statement.

## Reference and annotation methodology

Independent native CP-SAT and IR-to-WCNF/PySAT RC2 paths must both complete
optimally. CP-SAT uses zero absolute and relative gap tolerances. A direct business
checker independently recomputes feasibility and exact cost for both solutions.
WCNF binary bits, signed PB normalization, BDD encoding and legacy DIMACS dialect
are pinned. Objective constants are stored in a multiplier/offset transformation;
hard requirements are never soft penalties. No formally checked optimality proof
is claimed. Corpus assurance is CROSS_CHECKED. Tiny fixtures additionally exhaust
all business assignments and auxiliary extensions. Mutation and metamorphic tests
cover known formulation risks.

Every statement contains complete controlled English and verbatim input tables.
Automated checks compare all numbers/units/data and deterministic renderings and
screen answer leakage. They do not establish semantic equivalence or substitute
for human review. The pending workflow requires primary review for every record
and distinct second review for a stratified 100, plus all disputes; see
[annotation guidelines](docs/annotation_guidelines.md).

## Construction limits and selection effects

Two isolated workers; native limit 15 seconds, per-candidate wall limit 45 seconds,
resident-memory limit 1,536 MiB, eight attempts per ID. Persistent worker memory is
polled rather than kernel-enforced. Timeouts/inconclusive results are not declared
infeasible. Complete reference acceptance creates a tractability filter. Initial
calibration exposed costly time-expanded models and a seed-schema engineering bug;
the initial config/ledger is preserved separately. Explicit family overrides in
the frozen config reduce the largest time/product profiles; no silent hardness
claim or change in corpus quotas was made. Final observed statistics are written
below after the complete audit.

## Reproduction, availability and attribution

[Reproduction commands](docs/reproduction.md) regenerate deterministic artifacts
from accepted seeds and pinned tools. Wall-time filtering can select different
attempt numbers on another machine; runtime, timestamps and optimal witnesses can
vary. Exact duplicate checks exclude family/level/template metadata; topology
screening reports repeated signatures without claiming general semantic or graph
isomorphism detection.

Source Git excludes data/, audit/, and releases/. Dataset download:
DATASET_DOWNLOAD_URL (placeholder, no published host). The prepared archive
restores the single catalog and complete companions, with external manifest,
SHA256SUMS and release notes. Human review must finish before final release.
See [publication procedure](docs/github_release.md), [citation](CITATION.cff),
[data license](DATA_LICENSE), [notice](DATASET_NOTICE.md), and [changelog](CHANGELOG.md).
Creator/owner pseudonym comes from existing Git configuration; the remote
repository destination, DOI, and publication date have not been invented.

## Observed local-build statistics

The final corpus has 1,000 records, 100 per family, 25 per cell,
and 1,000 CROSS_CHECKED labels. The full audit
reported zero errors and zero exact business duplicates.

Frozen-build candidate outcomes: `{"COMPLETED_OPTIMAL": 1000, "TIMEOUT": 12}`.
Accepted 98.81% of 1,012 recorded candidate attempts. Initial
calibration outcomes (outside the corpus): `{"COMPLETED_OPTIMAL": 38, "MALFORMED_OR_ERROR": 20, "TIMEOUT": 8}`.
The separately archived frozen 100-record calibration run completed 100 optima
and one timeout. See the candidate ledgers for per-cell outcomes and seeds.

| Encoding statistic | Minimum | Mean | Maximum |
| --- | ---: | ---: | ---: |
| variables | 24 | 539.32 | 9,577 |
| clauses | 57 | 1,864.24 | 35,850 |
| wcnf_bytes | 648 | 32,276.68 | 713,885 |

Combined native and MaxSAT reference time: mean 0.471 s, maximum
41.773 s per accepted candidate, excluding generation, encoding and file
writes. These are construction observations, not a solver benchmark. There are
329 topology signatures; 106 signatures repeat,
covering 777 records. Repeated topology alone does not imply
duplicate numerical/business problems. The full group membership and screening
method are in audit/quality_report.json.

Human primary reviews: 0/1,000. Independent
stratified second reviews: 0/100.
Status remains **INCOMPLETE_RELEASE** until the listed review requirements are met.
