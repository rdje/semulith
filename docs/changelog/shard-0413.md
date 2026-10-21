# DEV_NOTES shard — _(2026-10-20 … _(2026-10-19

> Sharded from `DEV_NOTES.md` under its 48 KiB ceiling (`doctrine/readme_routes.tsv`).
> Entries in a shard are **never edited after the shard** — git history is canonical.

## _(2026-10-20 UTC)_ — bounded per-file output provenance (ARTIFACT-CLEANUP.15)

From clean7f732ab/brief0/host census OK, isolate the provenance record/reader
before producer/plan integration .17, guarded core .16 and host/operator .14.
P1 remains open: legacy metadata planning can select an input solely by cache
name/path. No cache-unlink API or new project cleanup event is introduced here.

The tracked probe's --cargo-contract invokes only public Cargo clean --dry-run
--verbose --offline --profile dev in a disposable owned workspace. Cargo lists
both a cache-shaped toy and a profile input; the third input outside that profile
is not listed, and all three bytes remain exact. Metadata/root/profile scope
therefore cannot attest per-file generation. The earlier owned five-input
Cargo1.95.0/metadata/dry-run observation is retained in cargo-contract.json.

Add artifact_output_provenance: closed canonical bounded ledger/observations
with UTC time, current-file recorder/producer identities, fixed host test command,
explicit target/intermediate roots, successful plain-zero exit, and exact
before/after facts. Only absent-before or changed-digest outputs qualify. An
unchanged unknown input cannot gain authority from timestamp/inode churn.
Known C-engine/C-guest roots are only the future protocol; producers are not yet
connected. Unknown namespaces, release/cross-target paths, aliases and malformed
records refuse. Current approval matches supplied anchored census facts, tracked
case/Unicode aliases, recorder/actor source snapshots and a single-link output.
It does not reopen supplied outputs or attest loaded code/independent origin;
caller quiescence and later per-file mutation revalidation remain necessary.

Ledger16MiB/65,536 sorted unique outputs; record32KiB, source1MiB, file512MiB.
Absent ledger grants no outputs; unsafe/malformed reads refuse. Historical
source records decode after changes but cannot match current approval. Root
pathname/device/inode guards surround reads and precede authority return.

QA controls caught two implementation gaps before publication: D3 accepted an
old root descriptor after an owned fixture rename (23 tests/1 failure/0 errors),
fixed by before/after root guards with separate start/return omissions. D5
accepted release output for the fixed host cargo-test command (25/1/0), fixed by
the debug-only contract. D4 was an inline documentation editor reusing a leaf-local
offset for the full-document prefix. Restore the complete saved predecessor
prefix and retain new spans; all old nodes/history inverses are verified. The
truncated working copy was never committed; no source history was lost.

25 tests normal/O and13 copied-source omissions each1 failure/0 errors give28
exact outcomes; gate76 and derived1633 literal arms. Early controls demonstrated
why whole-codec reconstruction could mask a missing stage guard: command/return
controls now target that stage directly; oversized decode asserts no JSON parse.
Current-fact omission uses one failing unit rather than five subtest failures.
Cold copied reader needs no Git or producer execution. Focused/source/history/
capacity/rendered checks and normal COMMIT follow. Promotion declined: existing
output-only, locality, claim and tools-first policies govern this repair.

Final focused16/books7/native3/scope pass:18 files/protected1460/97 old entries,
3844B whole0384/0385; all prior task text and caps retained. Staged checks follow.

## _(2026-10-20 UTC)_ — record recoverable cleanup intent (ARTIFACT-CLEANUP.13)

From clean e9b4532/brief0/actual host census OK, split journal-only .13 before
anchored core .15 and host-bound CLI .14. The retained legacy release replay
already proves an unlink can precede a failed post-check/no receipt. Establish
metadata framing first; no cache-unlink API or real cleanup event in this unit.

Add artifact_cleanup_journal: exclusive attempt.jsonl binds the canonical saved
plan, candidate count and current recorder/actor file identities. Sequential
intent/return records and explicit terminal state reject incomplete success.
A torn last line retains only size/digest; pending intent stays unresolved.
Inspection reports recorded observations, not current absence, actor origin or
loaded-code attestation; it invokes no Git/producer and reads historical sources.
16MiB journal,32KiB frame, two events/candidate plus begin/finish,1MiB per source,
2KiB error detail. Saved plan16MiB separate; no peak-RAM/power-failure claim.

Apple fsync manual identifies drive-buffer loss/reordering across power failure.
Owned fixture file/directory fsync and F_FULLFSYNC read/write succeed. Synchronize
saved plan and every ancestor before yielding; flush each accepted frame, require
Darwin F_FULLFSYNC and fail closed on unavailable/failed barriers. Validate root,
parent, file identity/single-link/size and saved plan before every append. Failed
writes poison the writer; preserve bytes rather than append into damaged framing.
Caller quiescence remains necessary; this is not a namespace/storage transaction.

26 tests normal/O, ten copied-source omissions each1 assertion/zero errors:
22 exact journal outcomes. Include close-error descriptor cleanup, short/torn
writes, fsync/full-sync failures, prefix uncertainty, canonical/closed schemas,
byte/frame/count bounds, source/plan/path changes and cold4 inspect CLI, no Git,
valid parent cwd/process launch denied. Actual narrow source-bound plan/barrier/
writer/reader smoke yields incomplete intent0/returns0; owned dummy cache intact.

Expand ARTIFACT-COHORT to48 outcomes/derive1631 literal sites. Move the complete
cleanup teaching fragment into bounded docs/toolbox/artifacts.md with only two
explicit include rebases; nested rendering preserves original examples and adds
shared journal usage. Book authored bytes524076/524288; no raised cap or unbounded
neighbor. All old producer/capture/event data and CPU/board/replay status stay
exact. Focused/source/history/rendered checks and normal COMMIT follow before .15.
New owned P1 finding: a retained-input fixture matches the current path/name
class without Cargo output provenance. No input was deleted. .15 must bind
regenerable output ownership before exposing mutation; book/help calls the
candidate list provisional. Probe input-candidate.log records the counterexample.
Focused16/books7/normal-print/source-history scope normal/O pass.18 files/
protected1456/1Gitlink/98 whole old entries;0382/0383 retain4030B. Task/index
inverses2, book fragment/rebases2 and prior planner/gate exact; staged COMMIT next.
Promotion declined: existing durability/claim policies govern this implementation.

## _(2026-10-20 UTC)_ — retain the historical cleanup producer (ARTIFACT-CLEANUP.12)

Continue from clean847be8c exact18/message/diff/brief0 and actual host census OK.
Split the remaining activity into historical retention/replay .12, guarded core/
journal .13, and host-census/CLI .14; all detailed before code. Original AC0067
helper still lived only in ignored target. Preserve its5815 bytes as passive
scripts/fixtures/artifact_cleanup_0067.py.txt, SHA0396e669f9b798f010dcbe67b5f3462497afbcff478d353c7d989b9b2bd307e9.
A tracked8KiB descriptor reader authenticates it before copied execution.

Five tests normal/O show debug success and release-D1: original helper unlinks
the fixture cache, then rejects its stray post-check without a receipt. Retained
input bytes survive, caller cwd restored; only public Git root/inventory reads
mocked. No real cache cleanup. Changed/oversized/linked/nested-Git inputs refuse;
pin omission in a copied reader loses one assertion/zero errors per mode. Cold
three-file CLI, no Git/valid parent cwd, passes both modes. Historical event and
instrument identities remain distinct from the later planner and future delete.

Expand ARTIFACT-COHORT:26 gate outcomes total, original26 planner tests/10 guard
omissions plus5 legacy tests/one pin omission per mode. Public enumeration derives
1629 literal sites,40 doctrines/42 routes unchanged. Partition the exact existing
78B tool row into a bounded artifact family; preserve all older toolbox text and
add its root index link. Book table grows4B, full new teaching stays in shared
CLI usage; fixed capacities and all prior examples preserved. Focused/source/
history/rendered verification and normal COMMIT follow before .13. Original37
producer modules/native3/capture remain exact; CPU/board/replay state unchanged.
Focused16/books7/normal-print and scope normal/O pass.18 files/protected1452/
1Gitlink/98 whole old entries; native0380/0381 retain3172B. Task/index inverses2,
planner code/gate preserved;78B row moved verbatim. Staged checks/normal COMMIT.
Promotion declined: repairs adoption of existing source-durability/claim policies.

## _(2026-10-20 UTC)_ — durable bounded cleanup plans (ARTIFACT-CLEANUP.11)

The AC0067 helper and controls existed only in ignored target, contrary to
TOOLBOX first-class instrument requirements. Own the priority1 repair before
P4 policy. The exact legacy helper on an owned release-cache fixture selected
one file and simultaneously labeled it stray; deleting it made the retained
stray post-check fail without a result receipt. AC0067 had debug caches only;
its historical event/helper/receipt remains exact. Plan/check slice .11 first;
anchored delete/partial outcomes .12 next, without another real cleanup event.

Add stdlib artifact_cleanup and tracked copied-fixture probe/gate. Bound the
complete selected bin/log projection, paths/counts/depth/hash bytes/JSON/source
and public Git reads. Fix runtime root before Git and publication; use both HEAD
and index tracked inventories, Unicode/case aliases and hard-link protection.
Descriptor traversal checks same-device/non-symlink/non-Git boundaries before
and after operations. Source identity is current file bytes, not loaded-code
attestation; no atomic snapshot/peak RAM claim. Immutable closed plan and
exclusive output in reserved target/artifact-cleanup, excluded from census.
Unknown files retained; release/deps strays belong only to the retained set.
No deletion operation yet. After-state equality observes state, not its actor.

Review controls found a test-only os.stat patch missing the runtime capability
set; fix the fixture, retain the production check. Add pre-traversal depth
checks, descriptor-close-error coverage and canonical shared-ancestor exclusions.
Public progress reader accepts direct numeric IDs; nested .11.1/.11.2 refused
foreign leaf. Use .11/.12 under the owned activity, leave the reader unchanged.
26 tests normal/O and ten separately failing guard omissions per mode yield
22 exact outcomes. No actual cache/input/repository metadata is modified by tests.

D2 review: a declared foreign-device fixture opened one directory before
refusal. Stop the owned pending commit terminal143; HEAD568234a unchanged.
Move device rejection before open; retain after-open identity/device checks.
The new copied control sees0 opens; omitting it loses1 assertion/0 errors.
Known foreign Git markers also refuse before any public query, independently controlled.
All26 tests normal/O and22 outcomes reverified before recommit.

Register ARTIFACT-COHORT and all mirrors. Public enumeration derives40 doctrines
and1627 literal self-test sites, not the22 expanded outcomes. Book adds only a
shared source include plus a compact doctrine row:524281/524288 authored bytes.
Toolbox near-cap row points to full help/book; old text and fixed caps preserved.
Focused16 checks pass; seven fresh books/normal-print new and old teaching exact.
Actual CLI plan/check matched18 candidates/78250715B and18219 retained files/
152775548B, plan6836479B. Early check refused missing plan; join planner before
repeat. Scope18/protected1447/1 opaque Gitlink/98 whole old entries;0378/0379
retain3504B. Full task/index inverses2, book inverses2/governance inverses4; all
capacities/native capture/input bytes exact. Staged checks then normal COMMIT.
Final Git-marker scope:6/46717788B match; current source identity exact.
Promotion declined: existing policies apply.

## _(2026-10-19 UTC)_ — retain method evidence during due cleanup (ARTIFACT-CLEANUP.10)

Prior2026-10-18T23:00:27Z is over24h old. Own .10 from clean59e210a after
P4-0283 exact20 files/message/normal hooks/brief0 and actual host census OK.
Read standing exclusions/task/book/latest record before ownership. Reuse .9
helper with only output root target/artifact-cleanup-0067 changed. Census
project target/.app-data without symlink, nested-Git or foreign-device traversal.
Select only untracked single-link Cargo incremental dep-graph/query-cache/
work-products bins. Retain all diagnostic/reference/capture logs, dependency
source fixtures and unknown classes; no other repository write or input deletion.

Saved plan18files/78250724B: C-engine6/46717790B and C-guest-image12/31532934B.
Retained18121bin/log files/152718645B, four nested-Git skips/0strays. Both normal
and optimized intact-plan preflights pass; each damaged identity/totals plan
refuses before deletion. The first control invocation preceded plan completion
and refused FileNotFoundError. Join census before restart; no deletion or plan
mutation then. Six complete controls joined, original plan restored exactly,
actual pre-delete host census green. Complete cohort/retained identities checked
again, then each path/device/inode/mtime/size/SHA revalidated before unlink.
At2026-10-19T23:07:45.637459Z,18saved paths removed, immediate selected residue0,
retained counts/bytes/SHA exact. All native observations/results and source inputs
remain protected. Later hooks may regenerate caches or update diagnostic logs;
this record describes the immediate measured cleanup event.

Overwrite the single anchored latest record. Existing book direct include carries
it; original teaching and all fixed caps stay exact. Own task/index/MEM/CH/DEV,
whole-oldest entry rollover if needed, complete task/index/head inverses, focused
checks/seven books/normal-print latest receipt and normal COMMIT/actual final
host census. Focused13/books7/normal-print receipt and whole task/index/head inverse proof pass.
Scope8/protected1452/1Gitlink/97 old entries; CH0377 retains636B whole.
The active index shorthand was refused by FRONTIER-SYNC; correct to the full
leaf ID before verification, then retire it only after completion. LIVE42routes/39doctrines/1625arms,CPU14/18,
BOARD10/12,replay4/4green unchanged. Next full source/risk/feature policy and
status integration; preserve the canonical capture. No full CI or push.
Promotion declined: existing safe-cohort/locality/retention contracts apply.

