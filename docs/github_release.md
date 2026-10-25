# GitHub publication policy

The owner requested expanding to 2,000 records, naming the dataset `chainmax-2k`,
and committing the full dataset and archive to GitHub. This supersedes the earlier
ChainMax-1K plan's no-data rule. The Python package/project and repository remain
`chainmax`. The connected account is verified as `pouyaardehkhani`.

Repository description:

> chainmax-2k: 2,000 synthetic supply-chain problems with cross-checked formulations, MaxSAT encodings, and optimal solutions.

## Included contents

- Code, pinned dependencies, configuration, schemas, tests and documentation.
- data/chainmax-2k.jsonl and every referenced problem/model/solver/verification file.
- Candidate and rejection ledgers, quality/build reports, review queue and migration
  evidence, including historical audit summaries.
- The full checksummed 2K archive, manifest and release notes under releases/v1.0.0/.
- The preserved original 1K archive and manifest in its historical release folder.

Virtual environments, credentials, caches, extraction copies, incomplete staging,
build locks and redundant recovery files remain local. They are construction tools,
not corpus contents. The original development plan is retained as historical context
with a clear supersession notice.

## Publication sequence

1. Complete both reference paths and the full audit for all 2,000 records. Retain
   pending human review flags; publish this as a provisional corpus.
2. Run correctness tests, fresh construction smoke checks and publication preflight.
   Check every Git blob is below GitHub's 100 MiB limit and that all required data
   files and the archive are tracked. Do not commit scratch directories.
3. Create the public repository `pouyaardehkhani/chainmax` with the description above,
   using the verified authenticated account; reuse it if an authorized existing
   repository is supplied. Record actual creation output before claiming success.
4. Update README/repository metadata using the actual created URL, package the final
   archive, and commit source, complete data, audit evidence and release files.
5. Push main, verify the remote commit and required file paths, and inspect CI results.
6. Record the actual upload receipt in PUBLICATION.json. The receipt identifies the
   initial data commit and archive checksum; it is not a human review approval.

When human reviews are later completed, import actual attestations, resolve issues,
rerun audit and create a new reviewed package/version. Public availability now does
not imply completion of human/domain-expert review or a checked formal proof.

The package manifest is external to the archive to avoid checksum self-reference.
It records construction/packaging source provenance, exact counts, configuration,
tool versions, member hashes and archive hash. SHA256SUMS verifies the archive and
external manifest. Git clone gives the full corpus; the archive provides a separate
portable download of the same catalog and reference artifacts.
