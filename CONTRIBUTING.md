# Contributing

Report incorrect descriptions, missing business rules, invalid formulas, encoding
defects, cost disagreements, or reproduction errors with the instance ID, version,
config hash, tool versions, exact command, and a minimal counterexample.
No public repository destination is configured yet; share reports with the owner
until the source repository is published. Do not include credentials or operational
company data. Keep generated corpus files out of Git.

Run `python -m pytest -q` and `python -m chainmax doctor` after changes. Domain
changes need independent native-model and checker changes plus counterexample
tests. Changing a frozen generation configuration requires a recorded revision;
never overwrite an accepted version/ID with a new problem.

See [annotation guidelines](docs/annotation_guidelines.md),
[semantics](docs/semantics.md), and the [dataset card](DATASET_CARD.md).
