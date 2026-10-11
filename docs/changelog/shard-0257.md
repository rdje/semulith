# DEV_NOTES shard — _(2026-10-11)_ … _(2026-10-11)_

> Sharded from `DEV_NOTES.md` under its 48 KiB ceiling (`doctrine/readme_routes.tsv`).
> Entries in a shard are **never edited after the shard** — git history is canonical.

## _(2026-10-11)_ — bind authenticated Sail receipts (P4-SYSTEM.14 a31)

Add matched_gpr_receipt.read_run_receipt as one finite dependency of the complete
method evaluator. Caller first validates raw parent schema/graph and separately
checks current reference identity. Freeze selected canonical fields before I/O:
1..8 inputs, exactly4 unique output roles including the receipt,1..11 ordered argv,
integer exit, exact input/output run membership, one collector, safe unique paths
and used Sail ID/digest fields. Used context text caps at65536 characters separately
from the receipt's64KiB byte bound and caller-owned allocation. Eight principal
roles, fixed invocation, reference-producer version and three-run method relations
remain separate; a small consistent context grants no coverage credit.

Derive the sole receipt from its run observations; take one bounded authenticated
observation snapshot, then reuse parse_capture's raw-schema/single mapper. Bind
run ID/kind/argv/exit, candidate/binary SHA, collector, complete unordered input
ID/digest inventory and all three output ID/role/path/size/digests. Frozen facts
retain argv/exit and host/tool provenance; a matched receipt can record a nonzero
or signal exit. No other declared files or cache/binary are opened, argv is never
executed, no file is reopened after pinning, and no attestation/qualification is
inferred. Missing/changed/unsafe bytes remain unavailable/stale/refused separately.

Initial42 controls passed. A deliberate schema-file I/O injection then exposed one
new wrapper-boundary OSError among43 tests: the pure artifact parser normalizes
document errors but can propagate tool-file I/O. Keep that public parser intact;
this authenticated consumer now returns unavailable with the already-matched pin.
The omission control converts any escaped OSError to an explicit assertion failure.
Final43/0/0 normal/optimized; eleven omissions1/4/2/2/2/6/2/4/5/1/1 discriminate
without errors. PROFILE-CONSISTENCY104/0; explicit24 new outer calls preserve the
literal enumerator, which rederives39 doctrines/909 arms. Teach a full synthetic
receipt writer/reader/failure/contradictory-argv example; dummy other-file pins are
explicit and no process is claimed; synthetic failed-run verdict also reads
REFUSED. Focused17/sharder12/0/seven books/3044 rendered links/full literal
commands pass; before/canonical/contract/history/scope rc=0 preserve243 canonical
dictionaries/legacy ASTs/dispatch, entire old method/checker/append/root and1300
other files. All98 predecessor entries and actual old/published rc+digest rewrite
controls hold. Final changed-fixture/docs checks and staged/hooks/brief0 required.
Fixed seals/caps/canonical records/CPU status remain unchanged.
Next fixed invocation/principal/producer binding, closure/aggregate evaluator,
reviewed collector, measured retention/cases, canonical captures and full policy.

