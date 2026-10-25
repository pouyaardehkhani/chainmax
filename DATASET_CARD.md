# chainmax-2k dataset card

Version 1.0.0. Exactly 2,000 unique base problems in one labeled corpus, without
dataset splits, model training or fine-tuning. Each of ten families has 200 records;
each of the 40 family/level cells has 50. All 2,000 are CROSS_CHECKED. Human
description/template consistency review is pending: 0/2,000 primary
and 0/200 stratified independent second reviews.
Reference status: **INCOMPLETE_RELEASE**. Public availability does not imply human approval.

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
`{"COMPLETED_OPTIMAL": 2000, "TIMEOUT": 49}`.
Accepted 2,000 of 2,049 recorded attempts
(97.61%). Zero audit errors; zero exact business duplicates.
There are 544 topology signatures, of which 163 repeat,
covering 1619 records. Signature grouping omits numerical values;
it is a near-duplicate screening report, not general graph-isomorphism or semantic
equivalence detection. Full membership and per-cell outcomes are in the quality report.

| Encoding statistic | Minimum | Mean | Maximum |
| --- | ---: | ---: | ---: |
| variables | 22 | 543.15 | 9,734 |
| clauses | 54 | 1,879.84 | 35,850 |
| wcnf_bytes | 631 | 32,580.92 | 713,885 |

Combined native/MaxSAT reference time per accepted candidate: mean 0.392s,
maximum 41.773s, excluding generation, encoding and file writes. These
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
a final reviewed release. Repository: [https://github.com/pouyaardehkhani/chainmax](https://github.com/pouyaardehkhani/chainmax).

Code is MIT; data CC BY 4.0, selected by the owner. Creator identity was verified
through the connected GitHub account: Pouya Ardehkhani (pouyaardehkhani). Cite version,
source revision, config hash and checksum; no DOI or paper is fabricated. Dependency
licenses remain their own. See CITATION.cff, DATA_LICENSE and THIRD_PARTY_NOTICES.md.
