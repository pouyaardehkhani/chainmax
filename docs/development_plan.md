> Historical 1K specification. The owner subsequently requested 2,000 records, the name chainmax-2k, and inclusion of the full dataset and archive in GitHub. Those later instructions supersede this document on naming, size, and storage policy. See README.md and configs/v1.yaml.

# ChainMax-1K: Codex dataset development plan

**Purpose:** Give Codex an implementation plan for creating ChainMax-1K, a verified supply-chain dataset for inference-only LLM formulation methods, including in-context learning.

**Status:** Implementation specification. This document does not claim that the generator or dataset has been built.

**Target:** Exactly 1,000 unique base problems in one labeled corpus.

**Dataset policy:** No training, validation, development, demonstration, or test splits. No model training or fine-tuning. The same corpus contains problem descriptions and their reference answers. Incremental construction batches and software test fixtures are engineering tools, not dataset partitions.

**Scope boundary:** Build the dataset, reference formulations, MaxSAT encodings, optimal solutions, quality evidence, and a GitHub-ready repository with its README and release files. LLM experiments, ICL prompt selection, model comparisons, repeated generation runs, and solver deadline evaluations are outside this project. This document is the plan for a later Codex run; updating the plan does not create the dataset or publish a repository.

## 0. Dataset identity, project folder, and repository

Use these names consistently in source code, metadata, documentation, and release files.

| Item | Required name |
| --- | --- |
| Project / benchmark | ChainMax |
| Dataset release | ChainMax-1K |
| Dataset slug | chainmax-1k |
| Local project root folder | chainmax/ |
| GitHub repository name | chainmax |
| Python import package | chainmax |
| Distribution name in pyproject.toml | chainmax-dataset |
| Main catalog, relative to the project root | data/chainmax-1k.jsonl |
| Instance folders | data/instances/cmx_000001/ through data/instances/cmx_001000/ |
| Initial release tag | v1.0.0 |
| Full dataset archive | chainmax-1k-v1.0.0.tar.gz |
| Archive checksum file | SHA256SUMS |
| Root project README | chainmax/README.md |
| README dataset download placeholder | DATASET_DOWNLOAD_URL |
| Data location during construction | chainmax/data/ locally; excluded from Git |
| GitHub source repository policy | No tracked data/ directory or generated corpus |

Recommended project subtitle: **A Verified Supply-Chain Benchmark for LLM Formulation and MaxSAT Optimization.**

The 1K suffix identifies the 1,000-instance corpus. Keep semantic release versions separate from the dataset name.

Run project commands from the chainmax/ root. Create that folder when working in a new parent workspace; if the checkout already is the ChainMax project root, reuse it rather than creating a nested chainmax/chainmax/ directory.

The GitHub owner and final repository URL are not specified here. Use the owner's actual supplied or verified destination when publishing later. Do not invent an account, URL, DOI, paper link, or release link.

Create the README during project initialization and maintain it as implementation progresses. It is a required deliverable, not a task left to the owner after dataset generation.

## 1. Deliverable and success criteria

Produce a reproducible corpus of supply-chain problems that supports two later tasks:

1. Translate a natural-language description and its data into an optimization formulation.
2. Solve a correct formulation with a weighted partial MaxSAT solver and compare its result with a verified reference optimum.

Each of the 1,000 records must provide:

- A complete English problem description and structured numerical data.
- A bounded integer reference model with hard constraints and a cost-minimization objective.
- A human-readable mathematical rendering of that model.
- A weighted partial MaxSAT encoding in a declared WCNF dialect.
- A map from Boolean variables to business decisions.
- An optimal business-level solution and its exact integer cost.
- Evidence from independent reference-solving paths.
- Provenance, generation settings, checksums, and review records.

The core release contains 1,000 feasible problems with established optimal costs. Infeasible, ambiguous, or unresolved candidates remain in an audit ledger and do not receive invented optimum labels. Deliberately infeasible examples belong in software fixtures for v1, rather than changing the 1,000-record target.

Do not present a planted feasible solution as an optimum. Do not treat a solver timeout as infeasibility.

## 2. Fixed decisions for v1

| Decision | v1 rule |
| --- | --- |
| Dataset name | ChainMax-1K |
| Project folder and GitHub repository | chainmax |
| Corpus size | Exactly 1,000 unique base problems |
| Splits | None; no split field or split manifests |
| Learning setup | Inference only; no weight updates |
| Problem setting | Deterministic planning with known input data |
| Quantity domains | Bounded nonnegative integers; Boolean activation decisions |
| Cost representation | Integer minor currency units, with explicit units |
| Objective | One scalar total cost to minimize |
| Required demand | Exact fulfillment at the specified place and period |
| Shortages | Disallowed in v1 |
| Main target format | A typed, machine-readable optimization IR |
| Solver encoding | Deterministic compilation of the IR to weighted partial MaxSAT |
| Reference solving | Native domain model in OR-Tools CP-SAT plus WCNF solved with PySAT RC2 |
| Core assurance | Both reference paths terminate optimally, agree on cost, and pass independent solution checking |
| Language generation | Controlled English and varied reviewed templates; no paid model API required |
| Added paraphrases | Optional variants attached to an existing base ID; never counted as new base problems |

Keep size, family quotas, resource limits, and generation seeds in configuration. Changing the target or domain assumptions requires a new recorded configuration, not a silent adjustment.

All reference optimization calls in this plan exist to construct ground truth. They are not the later solver benchmarking experiment.

## 3. Corpus composition

Create ten problem families, with 100 base problems per family.

| ID | Family | Main modeling feature | Count |
| --- | --- | --- | ---: |
| F01 | Capacitated warehouse-to-market transport | Supply, demand, allowed routes, unit shipping costs | 100 |
| F02 | Multi-echelon distribution | Suppliers, intermediate warehouses, and flow conservation | 100 |
| F03 | Warehouse activation | Fixed operating costs and capacity conditional on opening | 100 |
| F04 | Route activation | Fixed route charges linked to permitted shipments | 100 |
| F05 | Multiple products | Products sharing transportation or storage capacity | 100 |
| F06 | Inventory and lead times | Period balances, arrivals, holding costs, initial inventory | 100 |
| F07 | Truck and mode decisions | Integer truck counts, vehicle capacities, mode eligibility | 100 |
| F08 | Minimum lots and sourcing rules | Minimum active orders, supplier limits, logical dependencies | 100 |
| F09 | Perishable products | Age-indexed inventory, shelf life, expiry, permitted disposal | 100 |
| F10 | Production and distribution | Bounded production, integer bills of materials, downstream shipping | 100 |
| | **Total** | | **1,000** |

Families can combine compatible features. Record the complete feature list; the family identifies the principal modeling challenge.

Within each family, create 25 problems at each of four structural levels:

- **L1:** Small topology and few interacting constraints.
- **L2:** More entities and one additional coupling feature.
- **L3:** Larger dimensions and several shared capacities or time relationships.
- **L4:** Compositions of supported features with tighter interactions.

This gives 10 families × 4 levels × 25 instances = 1,000.

These are structural levels, not claims about measured solver hardness. Record empirical construction runtime separately. Calibrate dimensions before bulk generation; adding variables or tightening a constraint does not guarantee a harder search problem.

Vary:

- Network topology and permitted routes.
- Supply-to-demand ratios and capacity slack.
- Cost structure, including tied and unique optima.
- Product counts and planning periods where applicable.
- Lead times, shelf lives, minimum lots, and activation rules.
- The mix of binding and nonbinding constraints.
- Narrative presentation independently of structural level.

Avoid filling a family with renamed copies of one instance or with one numerical perturbation pattern.

## 4. Mathematical and business semantics

Write a concise specification before implementing generators.

### 4.1 Common conventions

- Every numerical value has a declared unit.
- Input data completely determine the mathematical problem.
- Warehouses can retain unused stock unless an explicit terminal rule states otherwise.
- Routes absent from the input are unavailable.
- All decision variables have finite bounds.
- Every required market demand is met exactly.
- Costs are nonnegative integer coefficients in v1; zero-cost terms are omitted from soft clauses.
- Fixed costs are charged once at their declared scope: per route, warehouse, or operating period.
- A fixed charge must be linked to its triggering decision with hard constraints.
- Available initial stock is distinguished from newly purchased or produced stock.
- Multiple optimal solutions are permitted; the reference solution is one witness.
- Variable bounds are mathematical constraints, not merely solver hints.

### 4.2 Time and inventory

Use periods 0 through T-1. State the ordering of arrivals, production availability, demand fulfillment, and departures within a period.

A shipment dispatched in period t with lead time L arrives in period t+L. Explicitly prohibit or account for departures whose arrival would fall beyond the horizon.

Specify initial inventory, end-of-period inventory, storage capacities, and terminal requirements. Never allow negative stock or use goods before arrival.

For perishability, define the age of initial stock, how age advances during storage and transport, when expiry occurs, and whether disposal is allowed and charged. Test a shipment arriving exactly at the shelf-life boundary.

### 4.3 Special features

For truck counts, state whether truck costs replace or supplement per-unit transportation costs.

For minimum lots, define the relationship between a zero shipment and an inactive order. Use valid instance-specific upper bounds for activation links.

For production, use integer input requirements and output quantities with explicit timing. State whether production is immediately available or available in the next period.

Defer uncertainty, continuous quantities, arbitrary nonlinear costs, detailed vehicle-tour routing, and multiobjective optimization beyond v1.

## 5. Data contract and file layout

Use one authoritative JSONL catalog with exactly one record per base problem. Companion files are referenced by relative paths.

**The GitHub repository must not contain the data/ folder or the generated corpus.** The source repository contains code, configuration, schemas, documentation, and small software fixtures. Dataset files exist locally during construction and are distributed separately through the download location in the README.

Tracked source-repository layout:

~~~text
chainmax/
  pyproject.toml
  dependency lock file
  README.md
  DATASET_CARD.md
  CHANGELOG.md
  CITATION.cff
  LICENSE
  DATA_LICENSE
  CONTRIBUTING.md
  .gitignore
  .github/
    workflows/
      ci.yml
  configs/
    v1.yaml
  schemas/
    instance.schema.json
    domain.schema.json
    model_ir.schema.json
    variable_map.schema.json
    verification.schema.json
  src/chainmax/
    __init__.py
    __main__.py
    cli.py
    schemas.py
    domain/
    generators/
    model_builder/
    encoding/
    native_reference/
    checking/
    rendering/
    release/
  tests/
    unit/
    exhaustive/
    mutation/
    fixtures/
  docs/
    semantics.md
    annotation_guidelines.md
    reproduction.md
    github_release.md
~~~

Generated local artifacts, all excluded from Git:

~~~text
chainmax/
  data/
    chainmax-1k.jsonl
    instances/
      cmx_000001/
        problem.md
        input.json
        reference_model.json
        reference_model.md
        reference.wcnf
        variable_map.json
        reference_solution.json
        verification.json
        provenance.json
        review.json
  audit/
    candidate_ledger.jsonl
    rejected_candidates.jsonl
    build_manifest.json
    quality_report.json
  releases/
    v1.0.0/
      chainmax-1k-v1.0.0.tar.gz
      SHA256SUMS
      release_manifest.json
      release_notes.md
~~~ 

This is a proposed repository layout, not a list of already-created files. Private solver scratch files should not be required by the release.

Keep small software fixtures under tests/fixtures/ and readable examples inline in the README or documentation. Do not place committed examples in a data/ directory.

Include the following root-anchored exclusions in .gitignore from project initialization:

~~~gitignore
/data/
/audit/
/releases/
~~~

Also exclude virtual environments, caches, temporary solver files, and credentials. Do not add a data/.gitkeep file or an ignore exception that commits part of the generated corpus.

.gitignore does not remove files already tracked by Git. If a data/ folder was previously tracked, remove it from the Git index while preserving the local working copies. Verify that git ls-files -- data/ returns no entries before preparing a commit or publishing.

Use a versioned GitHub Release asset or external dataset hosting for the complete corpus and large solver artifacts. The root README must contain the explicit placeholder DATASET_DOWNLOAD_URL until the owner supplies the actual hosted location. Document the storage policy in docs/github_release.md.

The archive must restore data/chainmax-1k.jsonl and its complete companion artifacts at the documented relative paths. Include a release manifest recording the source commit, config hash, dependency versions, exact record counts, and archive checksums. Source and data must identify the same release.

Use the root README to explain both how to download the separately hosted data and how to regenerate it. Before a real download location is available, show DATASET_DOWNLOAD_URL as clearly labeled placeholder text. Publication preparation is part of dataset creation; do not fabricate a successful upload or a live URL.

The catalog must contain:

| Field | Required content |
| --- | --- |
| dataset_name, dataset_version | ChainMax-1K and the semantic data version |
| instance_id | Stable, unique base-problem ID |
| schema_version | Explicit schema version |
| family, structural_level, features | Modeling metadata |
| source_type | Synthetic for generated v1 instances |
| units | Quantity, currency, time, and any capacity-conversion units |
| problem | Description, structured data, explicit assumptions |
| reference | Paths to IR, mathematical rendering, WCNF, mapping, and solution |
| reference_optimum | Exact integer minimum business cost |
| objective_transform | Business cost = multiplier × WCNF violation cost + offset |
| verification | Status, assurance level, backend records, checker results |
| provenance | Seeds, configuration hash, source revision, tool versions |
| review | Description consistency and annotation decisions |
| content_hashes | Checksums for deterministic artifacts |

Do not create a split field. All 1,000 labeled records belong to the same corpus.

Descriptions and reference answers remain distinct fields so a later ICL application can select what enters a prompt. Do not build that application in this project.

### 5.1 Reference intermediate representation

Use a closed, typed schema rather than arbitrary executable code.

Support:

- Named bounded integer and Boolean variables.
- Grounded linear constraints with integer coefficients and explicit senses.
- Hard Boolean clauses.
- Supported indicator constraints with clear activation semantics.
- A linear minimization objective with an explicit constant.
- Stable constraint IDs and links to the business rules they implement.

Use a deterministic ordering for variables, terms, and constraints. Preserve source links from each constraint to the relevant narrative rule or data table. Keep those gold annotation links out of the problem description.

Reject unsupported expressions, missing bounds, duplicate variable declarations, invalid references, and numeric overflow risks.

### 5.2 Minimal worked fixture

Use this as an early engineering fixture, not as a substitute for the corpus:

- Warehouse A has two pallets; warehouse B has two pallets.
- A market needs exactly three pallets.
- Shipping costs two cents per pallet from A and five cents from B.
- Unused warehouse stock is allowed.
- There are no other costs or capacity restrictions.

Reference model:

~~~text
Variables:
  x_A, x_B are integers in [0, 2].

Hard constraint:
  x_A + x_B = 3.

Objective:
  minimize 2*x_A + 5*x_B.

Feasible plans:
  (x_A, x_B) = (1, 2), cost 12.
  (x_A, x_B) = (2, 1), cost 9.

Reference optimum:
  9 cents, witnessed by (2, 1).
~~~

The native solver, WCNF solver, direct business checker, and exhaustive enumerator must agree.

## 6. Reference construction and assurance

Use the following pipeline for every candidate.

1. Generate structured domain data and a feasible witness.
2. Validate schema, units, bounds, and supported features.
3. Build the reference IR and its mathematical rendering.
4. Independently build a native CP-SAT model from domain data.
5. Compile the IR to WCNF and produce a decoder.
6. Solve both reference models to optimality under recorded construction limits.
7. Decode both solutions and check them directly against domain data.
8. Recompute both costs with exact integer arithmetic.
9. Require agreement with the transformed WCNF violation cost.
10. Render the problem description using input data alone.
11. Complete description consistency checks and review.
12. Accept the candidate only after all release requirements pass.

The native backend must not read constraints generated by the IR-to-WCNF pipeline. The business solution checker must not accept a plan merely because it satisfies the encoded clauses. These independent paths reduce shared implementation errors.

### 6.1 Assurance levels

Use explicit labels:

- **EXHAUSTIVE:** A tiny instance is fully enumerated and agrees with both reference backends.
- **CROSS_CHECKED:** Both reference backends establish optimality, their exact recomputed costs agree, and all solution checks pass.
- **PROOF_CHECKED:** An independently checked optimality certificate is also available.
- **UNVERIFIED:** Any necessary step is incomplete or inconclusive.

Every released core instance must reach at least CROSS_CHECKED. Do not describe cross-solver agreement as an independently checked formal proof. Store certificates when supported, but do not make unsupported proof production a hidden dependency.

For CP-SAT, accept OPTIMAL only with both absolute and relative optimality-gap stopping tolerances configured to zero. A FEASIBLE result is insufficient. Check the installed backend's status semantics.

For RC2, require completed optimization and a complete decoded solution. An interrupted run or incumbent-only result is insufficient.

If a proof-checking backend is later added, record its exact proof format, checker version, and checker result.

### 6.2 Construction resource limits

Use configurable per-candidate time and memory limits. Choose concrete limits after measuring the initial construction batches; record every value.

Store completed-optimal, feasible-only, timeout, resource failure, infeasible, malformed, and backend-disagreement outcomes separately in the candidate ledger.

Retry only with recorded settings and seeds. If a family or level cannot reach its quota within a declared attempt budget, report the shortage and revise the versioned generation configuration. Do not silently lower the difficulty or promote a best-known value to an optimum.

Report acceptance and rejection counts by family and level. Requiring complete reference solutions creates a tractability filter; disclose it in the dataset card.

## 7. MaxSAT encoding requirements

Implement encoding as a deterministic compiler.

For a variable x in [0, U], use enough bits to represent U and add hard constraints excluding values greater than U. Preserve the special case U=0.

For a nonnegative objective term c*x with binary expansion x = sum(2^k*b_k), add a soft unit clause NOT b_k with weight c*2^k for every nonzero coefficient. A Boolean activation cost f*y becomes a soft clause NOT y of weight f.

Store objective constants and any normalization in the objective transform. The cost of falsified soft clauses must map back exactly to the original business objective.

Convert linear constraints to pseudo-Boolean constraints, then to CNF using a pinned implementation. Normalize signed coefficients carefully; test equalities, lower bounds, and upper bounds independently.

Use hard clauses for business requirements. Do not approximate a hard requirement by choosing a large soft weight.

Choose the legacy DIMACS WCNF dialect for the initial PySAT integration:

~~~text
p wcnf <variables> <clauses> <top>
<weight-or-top> <signed literals> 0
~~~

Set top strictly greater than the sum of soft weights and document that dialect in the manifest. If the modern hard-clause-marker dialect is exported, label it separately and test conversion. A file called WCNF is not sufficient evidence of parser compatibility.

Record:

- Primary variable bit positions, domains, and semantic names.
- Auxiliary-variable ranges and encoder choices.
- Clause and variable counts.
- Soft-weight sums and arithmetic-range checks.
- Encoder version and output checksum.
- Objective transform and solution decoding rules.

Do not simplify or preprocess away variables without preserving a valid reconstruction map.

## 8. Natural-language and annotation workflow

Start with controlled, complete English and explicit tables. The renderer receives problem data and business rules, never optimal decisions, optimal costs, or solver logs.

Create several reviewed narrative templates per family. Vary sentence structure, ordering, terminology, and table presentation while preserving a single interpretation.

Every description must state or supply:

- Entity roles and all relevant input values.
- What may be decided.
- Demand fulfillment rules.
- Capacities and compatibility restrictions.
- Time, lead-time, and inventory conventions when relevant.
- Which costs apply and when.
- The objective.
- Applicable assumptions needed to eliminate ambiguity.

Use rule IDs and table-cell references in private annotations to check that all reference obligations have a corresponding source in the problem statement.

Automated checks must verify numerical values, units, entity references, completeness, and absence of accidental answer leakage. Automated text checks do not establish natural-language semantic equivalence by themselves.

Require a recorded human consistency review for each released description, using the input data and rendered reference model. Record reviewer identity or pseudonym, review date, issues found, and resolution.

Second-review a stratified sample of at least 100 records and all disputed cases. Expand review if systematic errors are found. If human review is unavailable, report that missing release condition; do not invent reviewer approvals.

Optional paraphrases remain attached to their original base ID. They do not increase the count above 1,000.

## 9. Codex implementation milestones

Work sequentially, keep changes reviewable, and update a progress log after each milestone. The stages below are engineering milestones, not dataset splits.

### M0 — Repository and specification

Tasks:

- Inspect the target workspace and applicable repository instructions.
- Create or reuse the chainmax/ project root and apply the names in Section 0.
- Create the Python package, configuration, and dependency lock.
- Create the root README.md immediately, with an honest under-construction status.
- Add the intended GitHub repository layout, citation metadata, license documentation, contribution guidance, and generated-file exclusions.
- Add /data/, /audit/, and /releases/ to .gitignore before generating any records.
- Add the README's DATASET_DOWNLOAD_URL placeholder and explain that data files are hosted separately from the repository.
- Write semantics.md and schema drafts.
- Pin compatible versions after an actual installation smoke check.
- Add the single-corpus/no-splits policy to README and the dataset card.
- Define deterministic seed derivation and immutable IDs.

Done when the worked fixture is representable without an unresolved domain assumption, the project identity is consistent, and a root README exists.

### M1 — Data models and independent checking

Tasks:

- Implement schemas and a safe IR parser.
- Implement direct evaluation of business feasibility and integer cost.
- Implement mathematical rendering.
- Implement an exhaustive enumerator for tiny fixtures.
- Add fixtures exercising each basic constraint and cost type.

Done when known valid and invalid plans are classified correctly and the worked fixture yields optimum 9.

### M2 — One complete vertical slice

Tasks:

- Implement the F01 generator.
- Implement a native CP-SAT reference model.
- Implement binary/PB/WCNF compilation and variable mapping.
- Implement RC2 invocation and solution decoding.
- Generate the description and verification records.
- Export one complete catalog record.

Done when several small F01 instances agree across enumeration, CP-SAT, RC2, and the independent business checker.

### M3 — All supported features

Tasks:

- Implement F02 through F10 using shared domain primitives.
- Add one small readable fixture and one boundary fixture for every feature.
- Add feature-composition fixtures.
- Keep native-model construction and domain checking independent of the WCNF compiler.
- Define the four structural profiles per family.

Done when all ten families can complete the full construction pipeline.

### M4 — Correctness and initial corpus batches

Tasks:

- Construct an initial batch of 40 records: one per family-level cell.
- Review their wording and inspect numerical and structural diversity.
- Construct up to 100 accepted records in the same growing corpus.
- Measure construction cost, encoding growth, and rejection reasons.
- Calibrate profiles and generation limits, then freeze a configuration version.

These records may remain in the final corpus if they satisfy the frozen specification. Regenerate changed records with recorded provenance; do not count earlier superseded versions.

Done when construction is feasible at the planned scale and no unresolved systemic defect remains.

### M5 — Reproducible bulk generation

Tasks:

- Generate until every family-level cell contains 25 accepted unique base problems.
- Persist progress after every candidate.
- Resume safely after interruption.
- Keep an append-only candidate ledger.
- Apply exact duplicate checks and structural-diversity audits.
- Complete the required description reviews.

Done when all quotas sum to exactly 1,000 accepted records and every record has completed reference verification.

### M6 — Dataset audit and packaging

Tasks:

- Validate all schemas, relative paths, checksums, and ID uniqueness.
- Recheck every stored solution and objective.
- Parse every released WCNF with the supported reader.
- Compare all stored objective transforms and backend outcomes.
- Audit duplicate and near-duplicate groups.
- Produce the quality report, dataset card, and reproduction instructions.
- Build a release archive with a manifest and checksums.
- Finalize the GitHub README against the actual generated corpus and verified commands.
- Prepare release notes, citation information, applicable license files, and docs/github_release.md.
- Add a CI workflow for software correctness checks and small fixture audits; do not run LLM experiments or the full reference-solving workload on every push.
- Add a CI guard that fails if git ls-files -- data/ returns any tracked files.
- Check that a source-only checkout can load software fixtures and audit a separately obtained local corpus using the README.
- If a real download URL is supplied, test the download-and-extract instructions; otherwise retain the clearly labeled placeholder and report that hosting is pending.

Done when all release acceptance checks pass from a clean environment and the repository is ready for GitHub publication with a complete README and reproducible data release.

## 10. Required correctness checks

These checks target real modeling risks, rather than duplicating implementation details.

### 10.1 Tiny-instance exhaustive checks

For tiny instances of every family:

- Enumerate all bounded business assignments where tractable.
- Compare domain feasibility with reference-IR feasibility.
- For each assignment, fix the primary bits and check whether a satisfying auxiliary extension exists.
- Require that such an extension exists exactly for feasible business assignments.
- Verify that the minimum encoding cost over valid auxiliary extensions equals the business cost.
- Compare the global optimum across enumeration and both solvers.

This verifies projected semantics instead of requiring identical auxiliary assignments.

### 10.2 Mutation checks

Introduce deliberate errors and require the relevant checks to detect them:

- Omit a demand constraint.
- Reverse a capacity inequality.
- Allow an out-of-range binary integer value.
- Remove a fixed-charge activation link.
- Change a transportation coefficient.
- Shift an arrival by one period.
- Allow expired goods to satisfy demand.
- Double-charge or omit a truck cost.
- Misstate a production input requirement.
- Change a number or unit in the description.

Retain concrete counterexamples where possible.

### 10.3 Metamorphic checks

Use transformations with known consequences:

- Rename entities: feasible business decisions and optimum are preserved under the mapping.
- Scale all costs by a positive integer: optimum cost scales by that factor.
- Add an unused optional route: the feasible set can expand and the optimum cannot worsen, assuming all other rules remain fixed.
- Tighten a capacity: the feasible set can shrink; the optimum cannot improve if feasibility remains.
- Reorder records or resume construction: accepted deterministic artifacts remain unchanged.

### 10.4 Reproducibility checks

Separate deterministic artifacts from run-dependent metadata.

Input data, reference IR, WCNF, variable maps, and controlled descriptions should reproduce identically with the same pinned configuration. Runtime, timestamps, and solver witnesses can vary; require consistent feasibility and optimum rather than byte-identical logs or an identical optimal assignment.

Never claim full mathematical equivalence of two large formulations solely because one optimum agrees.

## 11. Proposed CLI and configuration

The commands below are implementation targets. Codex must implement and test them before documenting them as usable.

~~~bash
python -m chainmax doctor
python -m chainmax build --config configs/v1.yaml --accepted-limit 40
python -m chainmax build --config configs/v1.yaml --accepted-limit 100 --resume
python -m chainmax build --config configs/v1.yaml --accepted-limit 1000 --resume
python -m chainmax audit --dataset data/chainmax-1k.jsonl --all
python -m chainmax package --dataset data/chainmax-1k.jsonl --output releases/v1.0.0
~~~

The accepted limit is the cumulative corpus size, not the number of new records appended by that invocation.

Minimum configuration:

~~~yaml
schema_version: "1.0.0"
project_name: ChainMax
project_folder: chainmax
dataset_name: ChainMax-1K
dataset_slug: chainmax-1k
dataset_version: "1.0.0"
github_repository_name: chainmax
seed: 20261025
target_base_instances: 1000
instances_per_family: 100
instances_per_family_level: 25
structural_levels: [L1, L2, L3, L4]
quantity_domain: bounded_integer
cost_unit: cent
demand_policy: exact
shortages_allowed: false
reference:
  native_backend: ortools_cp_sat
  maxsat_backend: pysat_rc2
  require_both_optimal: true
  require_exact_cost_agreement: true
encoding:
  format: legacy_dimacs_wcnf
  integer_encoding: binary
review:
  require_primary_review_for_every_record: true
  minimum_second_review_records: 100
~~~

Add explicit resource limits, family parameters, encoder configuration, and candidate-attempt budgets before freezing the build. Do not put a splits section in this configuration.

The build must not overwrite a completed record with a different problem under the same version and ID. Use atomic writes, stable checksums, and an explicit resume state.

## 12. Release acceptance checklist

- [ ] ChainMax, ChainMax-1K, folder names, import paths, and artifact names follow Section 0.
- [ ] Exactly 1,000 unique base records exist in one corpus.
- [ ] Each family has 100 records; each family-level cell has 25.
- [ ] No split assignments, manifests, or training workflow exist.
- [ ] Every problem has complete input data and explicit units.
- [ ] Every description has a completed consistency review.
- [ ] The second-review requirement is satisfied.
- [ ] Every variable has a finite declared domain.
- [ ] Every reference IR validates against its schema.
- [ ] Every WCNF parses in the declared supported dialect.
- [ ] Every decoder reconstructs valid business-level decisions.
- [ ] Both reference paths finish optimally for every released record.
- [ ] Recomputed native, decoded, and transformed WCNF costs agree exactly.
- [ ] Assurance levels accurately distinguish cross-checking from checked proofs.
- [ ] Tiny exhaustive checks and targeted mutation checks pass.
- [ ] Exact duplicates are absent and near-duplicate patterns are reported.
- [ ] All candidate exclusions and unresolved cases are logged.
- [ ] Configuration, source revision, dependency versions, and seeds are recorded.
- [ ] Rebuilding deterministic artifacts succeeds from the documented environment.
- [ ] All packaged paths and checksums validate.
- [ ] Dataset limitations and construction selection effects are disclosed.
- [ ] The root README.md exists and satisfies every requirement in Section 14.
- [ ] The README contains DATASET_DOWNLOAD_URL as an explicit placeholder until a real hosted dataset URL is supplied.
- [ ] No data/ directory or generated corpus is tracked in Git.
- [ ] git ls-files -- data/ returns no entries, and CI enforces this rule.
- [ ] Generated audit records and release archives are excluded from Git history.
- [ ] README counts, example outputs, reference statuses, and commands match actual artifacts.
- [ ] Code and dataset licensing are stated accurately and the citation metadata are truthful.
- [ ] The repository includes small, meaningful CI checks and excludes transient solver files.
- [ ] The versioned release archive, SHA256SUMS, manifest, and release notes are prepared.
- [ ] The GitHub publication instructions distinguish the source repository from dataset hosting and contain no invented live links.

If any required condition is unmet, produce a truthful incomplete-build report and the remaining work list. Do not replace missing checks with optimistic status fields.

## 13. Dataset card contents

Document:

- Intended use: inference-only natural-language formulation and subsequent MaxSAT solving.
- One labeled corpus of 1,000 base problems, with no splits.
- Synthetic provenance and the extent of domain-expert review.
- Family and structural-level composition.
- Complete business semantics and domain restrictions.
- Annotation and reference-solving methodology.
- Assurance levels and any available certificates.
- Construction limits, acceptance rates, and rejected-candidate statistics.
- Encoder choices, size statistics, and objective normalization.
- Structural and numerical diversity, plus duplicate-audit results.
- Cost and solution conventions, including multiple optima.
- Version history, reproduction commands, and artifact checksums.
- Licensing decisions and dependency notices.
- ChainMax-1K identity, GitHub repository destination when known, and versioned data availability.

Describe the corpus as realistic synthetic supply-chain planning instances. Do not claim that it contains operational company data or demonstrates industrial deployment performance.

A later ICL experiment should construct its own prompt views from record fields and keep the query's reference answer out of its input. Implementing that experiment is outside this dataset-creation plan.

## 14. Required GitHub README and publication preparation

The future Codex implementation must create and finish chainmax/README.md. Merely mentioning a README in the file tree does not satisfy this requirement.

### 14.1 Required README contents

Use the title **ChainMax-1K** and the project subtitle from Section 0. Include:

1. **Overview:** What ChainMax-1K contains and the two later tasks it supports: formulation from language and data, followed by MaxSAT optimization.
2. **Dataset facts:** Actual base-instance count, family counts, structural levels, synthetic provenance, integer domains, and cost units. State that it is one labeled corpus with no training or dataset splits.
3. **Project status and data availability:** Clearly distinguish construction in progress, a verified local build, and a published release.
4. **Quick start:** Tested installation and environment instructions, including the actual compatible Python version and locked dependency setup.
5. **Download and verify:** A clearly labeled DATASET_DOWNLOAD_URL placeholder, instructions for replacing it with the actual hosted dataset link, checksum verification, and extraction into the local data/ folder. State explicitly that the GitHub repository does not include data/.
6. **Load an instance:** A small executable Python example that reads data/chainmax-1k.jsonl, shows one problem's input fields, and locates its reference artifacts.
7. **One worked example:** A readable description, a small reference formulation, and the verified optimum; use the nine-cent fixture or another actually checked example.
8. **Repository and dataset layout:** Distinguish tracked source files from the local, ignored data/, audit/, and releases/ directories. Show the catalog path and per-instance files after extraction or generation.
9. **Schema:** Core record fields and links to the machine-readable schemas.
10. **Coverage:** The ten problem families, four structural levels, and the distinction between structure and measured solver difficulty.
11. **Ground truth and assurance:** Independent reference paths, direct business solution checks, exact cost comparisons, and honest assurance labels.
12. **WCNF conventions:** Declared format dialect, the minimized violated-soft-clause cost, objective transforms, and how Boolean assignments map back to business decisions.
13. **Reproduce the dataset:** Tested commands for incremental construction, resume, full audit, and packaging, including construction resource requirements and description-review requirements.
14. **Limitations:** Supported discrete deterministic models, reference-solver tractability filtering, and the extent of human review. Do not claim operational company data or unperformed LLM experiments.
15. **Citation and licenses:** A truthful citation, CITATION.cff when its required metadata are available, and separate clarity about code and data licensing.
16. **Contributions and issue reporting:** Where to report a bad description, incorrect formula, reference-cost disagreement, or reproduction problem. Link CONTRIBUTING.md and DATASET_CARD.md.

Keep detailed semantics and annotation instructions in their linked documents. Use relative links for repository files. Keep the dataset download location as an explicit placeholder until the real URL is known; use the actual URL when provided. Verify local documentation links and every executable quick-start example.

The README must initially contain a download section equivalent to:

~~~markdown
## Download the dataset

Dataset download: DATASET_DOWNLOAD_URL

The full ChainMax-1K dataset is hosted separately from this GitHub
repository. This repository does not include the data/ folder.
DATASET_DOWNLOAD_URL is a placeholder; replace it with the actual
dataset archive URL when the dataset is hosted.

After downloading, verify the supplied SHA256SUMS and extract the
archive into the project root to create the local data/ folder.
~~~

Render the placeholder as text, rather than pretending it is an active download. Do not manufacture a GitHub Release URL. An actual dataset-hosting URL can replace the placeholder later without changing the repository's no-data policy.

Create a draft README at M0. At M6, update it from the actual catalog, quality report, and package manifest so totals and verification claims are consistent. Retain the requested download placeholder while hosting is pending. Do not fill it with claimed experiment results, unrun success badges, fabricated authors, or fabricated DOIs.

### 14.2 GitHub repository and data release

Prepare the repository with the name chainmax. Document the actual owner and repository URL when that destination is known.

Required publication preparation:

- Source code, locked dependencies, schemas, configs, the complete README, dataset card, and reproduction documentation.
- A concise description for the GitHub repository: "ChainMax-1K: verified supply-chain problems for LLM formulation and MaxSAT optimization."
- Small software fixtures under tests/fixtures/ and inline documentation examples sufficient to inspect the schema; no committed data/ directory or generated corpus.
- Applicable code and dataset license files. Use the owner's stated choices; if they are unavailable, record the unresolved licensing decision rather than inventing a grant.
- Accurate citation metadata and contribution guidance.
- A lightweight CI workflow for correctness tests and small example audits.
- A versioned full dataset archive, SHA256SUMS, manifest, and release notes.
- A documented download, extraction, and audit procedure.

Distribute full data bundles and large WCNF artifacts through separately hosted downloads, such as GitHub Release assets or external dataset storage. Keep them out of the source repository. Check applicable asset limits when selecting the actual hosting destination; document any packaging chunks under a single catalog and manifest. Packaging must preserve the single-corpus/no-splits policy.

Keep data/, generated audit records, release archives, caches, virtual environments, temporary solver files, and credentials out of Git history. Enforce the no-data rule with both .gitignore and a tracked-file guard.

Write docs/github_release.md with a concrete future publication sequence: confirm the source-repository destination and separate data-hosting destination, verify that data/ is untracked, verify the source commit and package manifest, create or reuse the source repository, push only source and documentation, create the matching version tag, publish the dataset bundle through the chosen hosting service, and replace DATASET_DOWNLOAD_URL with the actual hosted link. Reuse an existing ChainMax repository when supplied.

Executing those remote actions is a later operation, separate from writing this development plan. Never mark the repository or release as published without an actual successful publication result. If the future Codex run covers creation only, finish with the GitHub-ready files and publication instructions.

### 14.3 README acceptance checks

- The root README uses ChainMax-1K and all named paths consistently.
- The README explicitly states one corpus, 1,000 verified base problems after completion, no training, and no dataset splits.
- All local documentation and example links resolve.
- Installation, instance-loading, audit, and packaging instructions have been exercised.
- Counts and assurance claims agree with the release manifest and quality report.
- The download section contains the requested explicit DATASET_DOWNLOAD_URL placeholder while hosting is pending, or the actual supplied URL once hosted.
- The README states that the source repository excludes data/ and explains how downloading or local generation creates it.
- git ls-files -- data/ has no entries.
- Citation, ownership, license, and version metadata reflect known information.
- A user can understand and obtain the dataset from the README without reading this development plan.

## 15. Codex handoff prompt

~~~text
Implement the dataset-creation project described in
SUPPLY_CHAIN_DATASET_DEVELOPMENT_PLAN.md.

Name the project ChainMax and the 1,000-instance dataset ChainMax-1K.
Create or reuse the project folder chainmax/ and use chainmax as the
GitHub repository name and Python import package. Use the naming and
release paths in Section 0 consistently.

Create exactly 1,000 unique, verified supply-chain base problems in one
labeled corpus. Do not create dataset splits. Do not train or fine-tune
a model. Do not implement an LLM evaluation harness, ICL experiment,
leaderboard, or solver deadline benchmark.

Use the staged milestones in the plan. Begin with the domain specification,
typed schemas, independent business solution checker, and the tiny fixture.
Then complete one vertical slice through native CP-SAT modeling, WCNF
compilation, RC2 solving, decoding, and exact cost checking before expanding
to the other families.

Treat the domain data as the source of truth. Keep the native reference
builder and business checker independent of the WCNF compiler. Preserve
all bounds, hard constraints, objective terms, units, and time conventions.

Do not label a feasible incumbent as an optimum. Require both reference
backends to complete optimally and exact recomputed costs to agree.
Record timeouts, disagreements, and rejected candidates without hiding
them. Never fabricate review approvals, solver results, or proof evidence.

Build incrementally and resume safely. Keep all records in the same
corpus throughout construction. Make family counts and resource limits
configurable, then freeze and record the release configuration.

Create the root README.md at project initialization and finish it after
generation and audit. Follow Section 14 for its required contents.
The README must contain the clearly labeled DATASET_DOWNLOAD_URL
placeholder until an actual separately hosted dataset URL is provided.
The GitHub source repository must not contain a tracked data/ folder or
the generated corpus. Ignore /data/, /audit/, and /releases/ from the
start, and enforce the no-data rule with a tracked-file check in CI.
Prepare a GitHub-ready repository with accurate installation, loading,
reproduction, data-download, citation, licensing, and release instructions.
Use actual build results and real publication metadata. Prepare the
versioned data archive, checksums, manifest, and release notes. Do not
invent a repository owner, a publication result, or a live download URL.

After each milestone, report implemented components, meaningful checks,
remaining limitations, and the next milestone. Continue independently on
authorized engineering work. If an external dependency, construction
budget, or human review requirement is unavailable, report the concrete
blocker and continue with independent work that can still be completed.

Deliver the generator source, dependency lock, one dataset catalog,
reference artifacts, candidate ledger, quality report, dataset card,
complete GitHub README, citation and license documentation, reproduction
and publication instructions, and a checksummed release archive.
~~~

## 16. Primary implementation references

Consult the installed versions and pin the actual dependencies used. The links below document relevant capabilities; they do not guarantee that arbitrary versions interoperate.

1. [PySAT formula and WCNF representations](https://pysathq.github.io/docs/html/api/formula.html).
2. [PySAT pseudo-Boolean encodings](https://pysathq.github.io/docs/html/api/pb.html).
3. [PySAT RC2 MaxSAT solver](https://pysathq.github.io/docs/html/api/examples/rc2.html).
4. [OR-Tools CP-SAT solver and statuses](https://developers.google.com/optimization/cp/cp_solver).
5. [MaxSAT Evaluation 2023 input/output dialect and status rules](https://maxsat-evaluations.github.io/2023/rules.html).
6. [GitHub repository README guidance](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-readmes).
7. [GitHub Releases and release assets](https://docs.github.com/en/repositories/releasing-projects-on-github/about-releases).

The reference solvers support the proposed construction paths [3, 4].
Pseudo-Boolean compilation and WCNF handling are documented in [1, 2].
The legacy and modern WCNF dialects differ; choose and test the declared
format rather than assuming compatibility from a filename [5].
GitHub README conventions and versioned release packaging are documented
in [6, 7]; check current service limits when preparing the real release.

