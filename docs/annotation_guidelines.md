# Human description review

Automated checks do not constitute human approval. Every released description
requires a primary consistency review against input.json and reference_model.md.
At least 200 stratified instances need a second, distinct reviewer. All disputed
cases need second review and resolved issues. Expand the sample if a systematic
error is found. Domain-expert review has not been performed.

The local `audit/review_queue.jsonl` identifies every description and its input
and mathematical files. The second-review sample contains 20 records per family:
5 at each of L1, L2, L3 and L4 (the first 200 IDs). Inspect every input value, entity, unit,
capacity, activation, time/age boundary, recipe requirement, and cost scope.
Match reference obligations to source tables and the numbered business rules.
Confirm the description neither discloses the optimum nor leaves a rule ambiguous.

Record identity or pseudonym, ISO date, issues found, resolution, and explicit
approval. Import actual completed reviews with:

```
python -m chainmax review-import --file completed_reviews.jsonl
```

Each line has the shape below; the values are an illustrative format, not an
actual attestation. Populate them only after a person completes review.

```
{"instance_id":"cmx_000001","kind":"primary","review":{"reviewer":"ACTUAL_REVIEWER","date":"YYYY-MM-DD","issues":[],"resolution":"ACTUAL_REVIEW_RESULT","approved":true}}
```

Use kind `second` for the independent second review. Approval imports do not
alter the problem or its optimum. They update review files, checksums, catalog,
and recovery records. Rerun audit and packaging afterwards. Do not reuse a
reviewer's identity for another person or approve unresolved discrepancies.
