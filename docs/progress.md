# Construction progress

M0: Created ChainMax project, README, ignored generated directories, Python 3.12
environment, pinned dependencies, closed schemas and finite business conventions.
Code license selected by the owner: MIT; data: CC BY 4.0. Hosting pending.

M1: Implemented direct stock/cost checker and mathematical rendering. Tiny fixtures
for all ten families exhaustively check business/IR/projected-CNF equivalence.

M2: Nine-cent fixture and transport vertical slice agree through native CP-SAT,
RC2, decoder, and direct checker. CP-SAT zero gap tolerances are explicit.

M3: All ten family generators implemented with independently checked feasibility
witnesses, finite bounds, production, shared product capacity, ages, lead times,
opening charges, route activation, sourcing, and trucks/modes.

M4 calibration: Initial configuration is preserved in calibration-initial.yaml.
38 candidates completed optimally; 20 engineering failures arose from an overly
small schema seed bound (fixed to unsigned 32 bits); 8 timed out. Two outstanding
slots were interrupted for calibration. Their audit trail and artifacts are
preserved locally in audit/calibration_initial/, outside the final corpus.
Large time-expanded binary-cost MaxSAT models dominated construction. Explicit
family overrides in v1.yaml reduce F06 L4 product count and F09 upper-level product,
quantity, and horizon dimensions. No hardness claim is made. Accepted calibration
artifacts were archived, not overwritten under the frozen configuration.

52 software tests passed at this point, including all ten exhaustive fixtures,
signed coefficients, indicators, expiry boundary, deliberate model/cost/text
mutations, and metamorphic transformations. Human review is not performed by these
automated tests. The frozen configuration will be measured on 40 and then 100
records before the remaining corpus is generated.

M4 frozen run: 40 and then 100 records completed optimally. Full deterministic
artifact regeneration, schema and checksum validation, WCNF parsing, both stored
business solutions and Boolean clause/cost checks passed for all 100. One candidate
timed out and its next recorded attempt completed. The prepared 100-record package
was decompressed and every member hash verified. No quotas or human reviews were
claimed complete. These pre-commit construction artifacts are retained in
audit/calibration_frozen100/ so the final corpus can be rebuilt from the committed
source revision with a non-null commit recorded on every final instance.

M5/M6 automated work: exactly 1,000 records constructed with all 40 cell quotas
satisfied; 1012 candidate outcomes recorded. Full artifact audit: zero errors,
zero exact duplicates. 63 tests, source-only smoke build/audit, documented Python
examples and links passed. All final records identify the construction source
commit. Human review remains incomplete (0/1,000 primary, 0/100 stratified second),
so final acceptance is INCOMPLETE_RELEASE. The package is prepared for review,
not published. See BUILD_REPORT.md for the remaining work.

## chainmax-2k expansion and publication

The owner requested 2,000 records and publication of the full data and archive.
All original 1K business/solver artifact hashes were preserved through the explicit
migration. The expansion reached 2,000 CROSS_CHECKED records, 200 per family and
50 per cell, with zero full-audit errors and zero exact business duplicates.
All 65 tests passed, as did the fresh construction smoke test, documentation
examples/links, staged publication checks, and fresh extraction of all 22,023
archive members. The 31,674,439-byte archive checksum is in SHA256SUMS.
The public pouyaardehkhani/chainmax repository was created with its description.
Actual upload receipts are recorded separately in PUBLICATION.json. Human review
remains pending: 2,000 primary and 200 stratified second reviews.
