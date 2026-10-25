# Contributing

Report incorrect descriptions, missing business rules, invalid formulas, encoding
defects, cost disagreements, or reproduction errors with the instance ID, version,
config hash, tool versions, exact command, and a minimal counterexample.
Use the repository's issue tracker once publication is complete. Do not include
credentials or operational company data. The full synthetic corpus and archive
are intentionally committed under the owner's revised publication policy.

Run `python -m pytest -q` and `python -m chainmax doctor` after changes. Domain
changes need independent native-model and checker changes plus counterexample
tests. Changing a frozen generation configuration requires a recorded revision;
never overwrite an accepted version/ID with a new problem.

See [annotation guidelines](docs/annotation_guidelines.md),
[semantics](docs/semantics.md), and the [dataset card](DATASET_CARD.md).
