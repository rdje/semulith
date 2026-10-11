# DEV_NOTES shard — _(2026-10-11)_ … _(2026-10-11)_

> Sharded from `DEV_NOTES.md` under its 48 KiB ceiling (`doctrine/readme_routes.tsv`).
> Entries in a shard are **never edited after the shard** — git history is canonical.

## _(2026-10-11)_ — authenticate retained Sail reference identity (P4-SYSTEM.14 a30)

Fresh full-CI preflight on clean3960e6b completed all five legs rc0, including
173/17/253 Rust tests and53 smoke-bench arms. This receipt belongs to that
pre-change milestone; it does not claim full CI on this implementation.

Add matched_gpr_identity.read_reference_identity as a finite authenticated method
dependency. Validate request role/ID and used candidate fields before I/O, then
read exactly one immutable pinned descriptor through read_snapshot (64KiB cap).
Validate raw references schema before D's single mapper; require exactly one root,
one Sail candidate and no experiments. Match required id/origin/kind/binary/
binary_sha256 and exact presence/value of release/version/source_commit/asset/
asset_sha256. Do not hash the whole parent dossier, inspect/open the executable
cache, launch a process, bind receipts/producers or claim whole-closure currentness.
Frozen results separate matched/stale/unavailable/refused from underlying pin
findings; expose detached immutable execution fields only on a current match.
A matched pin can still yield invalid syntax or stale execution identity.

The first40-test run exposed this new consumer's KeyError assumption (37 errors):
the established mapper omits absent repeated families. Tools identified the
complete mapper tail; use get(experiment,[]) without changing the mapper. Schema
omission also motivated defensive candidate-count access. Assertion-only mutation
controls use dict.get for optional-result inspection so missing identity fields
produce intended assertion failures rather than harness KeyErrors. Final40/0/0
passes normal/optimized; eight omissions lose4/2/5/1/1/1/20/17 assertions in both
modes, no errors. PROFILE-CONSISTENCY80/0 adds18 outer arms (39 doctrines/885).
First focused registration correctly refused885 versus869: DERIVED-COUNTS counts
literal outer calls. Replace the new loop with18 explicit calls, preserving the
enumerator and all62 old arms; remeasure before accepting the live count.
Actual on-volume files exercise inclusive caps, pre-read oversized refusal,
unsafe/missing/changed pins, schema-before-mapping, all fields/presence, descriptive
metadata, frozen detached results and snapshot reuse after a later path rewrite.
The new reader owns no artifact mutation; fixture lifetimes clean each test.

Teach complete synthetic root-relative writer/reader/staleness example in the GC
book; explicitly separate descriptor pins from executable authentication, replay,
receipt/process attestation, producer ancestry and qualification. Correct a
missing sentence separator in the touched doctrine description. Existing APIs,
canonical records, full history receipts and fixed seals/caps remain protected.
Focused17/sharder12/0/seven books and3038 rendered links/full literal commands
pass. Before/canonical/contract/history/scope tools rc0 protect243 canonical
dictionaries/legacy ASTs, all normative method text/all62 previous checker arms,
1298 other files/modes/Gitlinks and complete old append/task predecessors. The
first published-receipt diagnostic used the pure heads/new-shards sub-check;
inspect both owners and use the full partition judge, which refuses the actual
old shard0241 rc+digest rewrite (MODIFIED ROW). No production archive defect.
No sharding required; all fixed seals/caps remain unchanged. Next a31
receipt/invocation/input/producer binding, then closure/aggregate orchestration,
collector, measured retention/cases, captures and full policy/status consumers.

First COMMIT attempt refuses solely TASK-ACCEPTANCE/SEAM-INTEGRITY: this new
unit's three ticked boxes used rc0, which does not match the declared rc=0 evidence
signature. Inspect the exact enforcer regex, correct only this unit's receipts,
leave all signatures/gates intact and retry hooks. Routine caller/registration/
receipt lessons explicitly declined for promotion in the owning leaf; existing
contracts already own them. No failed hook run is claimed as signoff.

