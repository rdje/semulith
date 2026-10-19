# DEV_NOTES shard — _(2026-10-18)_ … _(2026-10-18)_

> Sharded from `DEV_NOTES.md` under its 48 KiB ceiling (`doctrine/readme_routes.tsv`).
> Entries in a shard are **never edited after the shard** — git history is canonical.

## _(2026-10-18)_ — collect three fresh runs under one allowance (P4-SYSTEM.14 a42x)

At e4aee6b, three standalone process/receipt calls read46364B in the synthetic
fixture, but the helpers exposed neither a per-call limit nor a charge and no
unit collector existed. The old process helper resets remaining=TOTAL_BYTES on
each call; publication has its separately bounded supplemental reads. This is a
scoped collection gap, not evidence of an accepted experiment exceeding its cap.

Add max_read_bytes and an appended default-zero charged_read_bytes result field.
Validate integers/inclusive0..128MiB before I/O; retain original positional fields.
The process helper still defaults128MiB. Publication defaults None to retain the
original128MiB process plus8716288B supplemental allowance; an explicit integer
shares that allowance across process and publication reads. Reserve before each
bounded reader/delegation and refund only complete, validated matching metadata.
Failures/invalid findings retain their full reservation because partial reader
consumption is not always exposed. Exact-limit succeeds and one-byte-short
refuses for the process, publication and complete unit, with independent measured
reader totals. This budget covers artifact reads, not schema/runtime I/O or RAM.

The new UnitRequest freezes all3requests before any artifact I/O. Require common
binary/budget/seven inputs, identical baseline/repeat inputs, a distinct control
expectation, nine principal IDs and twelve disjoint output identities/paths.
Anchor every protected input and output parent; require all12output names absent.
Reserve all names exclusively to catch actual case/normalization aliases across
runs before any child. Remove only owned reservations; replacement inode survives.
An observed new Git boundary revokes cleanup authority, leaving earlier empty
reservations rather than deleting inside it. Existing captures refuse unchanged.

Pass the remaining allowance through the three receipt-producing calls. Validate
charged metadata, output identities/sizes/digests and distinct observed PIDs before
refunding a delegate. Invalid findings consume its entire allowance. Keep reached
process findings; a recorded nonzero/signal exit yields failed and stops before the
next process, retaining the failed receipt. Missing output cannot reuse older
success. Only three zero-exit processes/twelve outputs yield recorded; no trace
comparison, complete closure, canonical experiment or qualification follows.
A later combined collection/evaluation pipeline must carry this charge forward;
retained-snapshot limits belong to that later stage.

Probe26/0/0 normal/O and16 independent omissions lose1/2/3/2/1/1/2/12/1/1/1/4/4/9/3/1
assertions without errors. The first malformed-limit check's helper comparison
against a string/None produced harness errors; restrict that comparison to valid
integer limits and require zero charge otherwise. An initial metadata-mutation
subtest left its result assertion outside the subtest, causing UnboundLocalError;
move the assertions into that same scope before counting discriminating results.
All62 old collector/publication positive/omission outcomes remain exact; only two
publication mutation source patterns follow the new allowance statements. All
old assertions and old collector probe remain unchanged. Re-derived arms1602;
39 doctrines, CPU14/18 and BOARD10/12 unchanged.

Tracked optional --real-sail-smoke calls the unit collector once, delegating the
existing owned smoke's public plan and declared output naming scheme. Match each
subsequent comparison request to the complete frozen unit; do not launch another
process for it. Normal/O: three fresh zero-exit process receipts,23314397 charged
read bytes under134217728,2298B identical traces with unchanged
SHA64551458d50ec4345b716abd9f2caf4b42053d6f3a8640735ee539d89a968bde,
AGREE/AGREE/DIVERGE at step2/x7 -3 versus -4. Receipt bytes/pins checked; unique
on-volume scratch removed. The prospective envelope still uses synthetic IDs and
an incomplete dependency list, with no raw scoped-record/closure or CPU credit.

Keep .16's live goal/status/acceptance and all native headings. Retain its complete
closed technical suffix and the whole closed w design5481B in the existing task
artifact; both complete source/owner inverses and6damaged controls pass. Preserve
old artifact prefix. DEV's oldest whole a42m entry5227B moves to0350; exact ordered
completeness and manifest-prefix checks apply. No ceiling/seal changes.
Evidence target/p4-system-14/a42x; promotion: declined (existing bounded-reader,
provenance, task-history and POSIX process contracts; no new cross-cutting policy).

