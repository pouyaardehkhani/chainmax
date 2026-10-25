# Local build report

ChainMax-1K v1.0.0 contains exactly 1,000 unique base problems, 100 per family,
25 per family/level cell, in one labeled corpus without dataset splits.
All 1,000 have completed CP-SAT and RC2 optimization, exact integer cost agreement,
independent business checks and CROSS_CHECKED assurance. The artifact audit has
zero errors and zero exact business duplicates. All 63 software tests passed.

The source-only checkout passed those tests, the nine-cent doctor, a four-record
build and full small-corpus audit. README/reproduction Python examples and local
documentation links were checked. Earlier accepted artifact checksums stayed
unchanged through construction. Concurrent writers were refused. Dependency
compatibility checks passed. Generated data/audit/release files are excluded from
Git, and the tracked-file guard returns no entries.

The final source revision for construction is recorded in every instance's
provenance. A separate package manifest records the packaging source revision,
config hash, dependency versions, exact quotas, archive and member checksums.
The prepared archive is releases/v1.0.0/chainmax-1k-v1.0.0.tar.gz; use SHA256SUMS
and release_manifest.json from the same directory. The packaging command verifies
all members through decompression before reporting success.

## Remaining acceptance requirements

- Complete actual human consistency review of all 1,000 descriptions and templates.
- Complete distinct second review for the 100 stratified records in the review
  queue, plus any disputed cases; resolve issues and expand review if needed.
- Import the attestations, rerun audit, and regenerate the final release archive.

No reviewer approval, domain-expert review or formal proof certificate has been
fabricated. The build is **INCOMPLETE_RELEASE** despite complete automated reference
verification. See audit/quality_report.json and audit/review_queue.jsonl.

## Publication still pending

Source repository destination and separate data hosting have not been supplied.
Nothing has been pushed or published. DATASET_DOWNLOAD_URL remains a clearly
labeled placeholder. Once review is complete, follow docs/github_release.md to
verify destinations, publish source and matching data bundle, and replace it.
Code is MIT and data CC BY 4.0, as selected by the owner.
