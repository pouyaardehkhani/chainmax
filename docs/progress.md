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
