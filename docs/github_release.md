# Future publication sequence

No remote repository or dataset release has been published. The intended repository
name is `chainmax`; the owner/destination and data hosting service must be supplied
or verified before publishing. Do not infer them from a local user name.

Repository description: ChainMax-1K: verified supply-chain problems for LLM
formulation and MaxSAT optimization.

1. Complete all primary human description reviews and the stratified 100-record
   independent second review, resolving all disputed cases. Rerun tests and audit.
2. Confirm the actual source repository destination and separate dataset hosting
   destination. Reuse an existing ChainMax repository when supplied. Check current
   hosting limits against the actual archive size before selecting the destination.
3. Verify `git ls-files -- data/ audit/ releases/` returns no entries. Keep the
   root-anchored exclusions and CI tracked-file guard. Never add data/.gitkeep.
4. Commit only code, locked dependencies, configs, schemas, small fixtures, and
   documentation. Verify the commit, frozen config hash, and package manifest.
   Regenerate the package after review imports and final source changes.
5. Create or reuse the confirmed source repository, push source/documents, and
   create the matching `v1.0.0` tag after all acceptance requirements pass.
6. Publish chainmax-1k-v1.0.0.tar.gz, SHA256SUMS, release_manifest.json, and
   release_notes.md through the chosen dataset host or versioned release assets.
   These generated files remain excluded from source Git history.
7. Verify an actual download, archive checksum, extracted catalog count, complete
   artifacts, and full audit. The archive restores data/chainmax-1k.jsonl and all
   data/instances/cmx_*/ companions from the project root.
8. Replace the README's textual DATASET_DOWNLOAD_URL with the verified actual URL.
   Record publication results only after the remote actions succeed.

The manifest is external to the archive to avoid self-referential checksum claims.
It records every member hash, archive hash, source revision, exact quotas, config
hash and versions. SHA256SUMS hashes both the archive and external manifest. Audit
logs, reviewer queue, dataset card, input config and license accompany the data.
The source checkout and dataset bundle are separate; neither should be mistaken
for a published final release while human review remains pending.
