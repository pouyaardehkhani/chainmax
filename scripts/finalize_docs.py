"""Populate truthful local-build facts from the complete successful artifact audit."""
import json
from pathlib import Path

r=json.loads(Path("audit/quality_report.json").read_text())
assert r["record_count"]==1000 and r["quota_satisfied"] and not r["errors"]
readme=Path("README.md")
t=readme.read_text()
t=t.replace("**Status:** 100 local problems have completed independent reference verification\nduring staged construction toward 1,000.","**Status:** All 1,000 local base problems have completed independent reference\nverification. The full artifact audit and 63 software tests pass.")
t=t.replace("The frozen target is 100 base problems per family and 25 in every family/level\ncell:","The corpus contains 100 base problems per family and 25 in every family/level\ncell:")
t=t.replace("| Target count |","| Base count |")
readme.write_text(t,encoding="utf-8",newline="\n")
card=Path("DATASET_CARD.md")
t=card.read_text().replace("100 local problems have completed reference cross-checking during staged build.","All 1,000 local base problems have completed reference cross-checking and the\nfull artifact audit.")
t=t.split("\n## Observed local-build statistics")[0]
stat=r["encoder_statistics"]
attempts=r["construction_attempts"]
groups=r["repeated_topology_groups"]
t+="\n## Observed local-build statistics\n\n"
t+=f"The final corpus has {r['record_count']:,} records, 100 per family, 25 per cell,\nand {r['assurance_counts']['CROSS_CHECKED']:,} CROSS_CHECKED labels. The full audit\nreported zero errors and zero exact business duplicates.\n\n"
t+=f"Frozen-build candidate outcomes: `{json.dumps(r['candidate_outcomes'],sort_keys=True)}`.\nAccepted {1000/attempts:.2%} of {attempts:,} recorded candidate attempts. Initial\ncalibration outcomes (outside the corpus): `{json.dumps(r['calibration_outcomes'],sort_keys=True)}`.\nThe separately archived frozen 100-record calibration run completed 100 optima\nand one timeout. See the candidate ledgers for per-cell outcomes and seeds.\n\n"
t+="| Encoding statistic | Minimum | Mean | Maximum |\n| --- | ---: | ---: | ---: |\n"
for k in ("variables","clauses","wcnf_bytes"):
    s=stat[k];t+=f"| {k} | {s['min']:,} | {s['mean']:,.2f} | {s['max']:,} |\n"
s=r["reference_seconds"]
t+=f"\nCombined native and MaxSAT reference time: mean {s['mean']:.3f} s, maximum\n{s['max']:.3f} s per accepted candidate, excluding generation, encoding and file\nwrites. These are construction observations, not a solver benchmark. There are\n{r['topology_group_count']} topology signatures; {len(groups)} signatures repeat,\ncovering {sum(map(len,groups))} records. Repeated topology alone does not imply\nduplicate numerical/business problems. The full group membership and screening\nmethod are in audit/quality_report.json.\n\n"
t+=f"Human primary reviews: {r['primary_reviews_completed']}/1,000. Independent\nstratified second reviews: {r['stratified_second_reviews_completed']}/100.\nStatus remains **{r['status']}** until the listed review requirements are met.\n"
card.write_text(t,encoding="utf-8",newline="\n")
Path("BUILD_REPORT.md").write_text(f"""# Local build report

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
fabricated. The build is **{r['status']}** despite complete automated reference
verification. See audit/quality_report.json and audit/review_queue.jsonl.

## Publication still pending

Source repository destination and separate data hosting have not been supplied.
Nothing has been pushed or published. DATASET_DOWNLOAD_URL remains a clearly
labeled placeholder. Once review is complete, follow docs/github_release.md to
verify destinations, publish source and matching data bundle, and replace it.
Code is MIT and data CC BY 4.0, as selected by the owner.
""",encoding="utf-8",newline="\n")
with Path("docs/progress.md").open("a",encoding="utf-8",newline="\n") as f:
    f.write(f"\nM5/M6 automated work: exactly 1,000 records constructed with all 40 cell quotas\nsatisfied; {attempts} candidate outcomes recorded. Full artifact audit: zero errors,\nzero exact duplicates. 63 tests, source-only smoke build/audit, documented Python\nexamples and links passed. All final records identify the construction source\ncommit. Human review remains incomplete (0/1,000 primary, 0/100 stratified second),\nso final acceptance is INCOMPLETE_RELEASE. The package is prepared for review,\nnot published. See BUILD_REPORT.md for the remaining work.\n")
print("Updated README, dataset card, build report and milestone log from actual audit.")
