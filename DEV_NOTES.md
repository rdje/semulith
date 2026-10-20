# DEV_NOTES.md

## _(2026-10-20 UTC)_ — version support-source records (ARTIFACT-CLEANUP.22)

AC0075 follows 43f07ab with normal hooks, exact 17-file scope, empty untracked
brief and actual host census OK. Split the support-source interface from .21's
publication transaction so the old record contract stays independently testable.
The tracked --support-contract diagnostic loads current or exact committed codec
initializers through bounded read-only Git. At 43f07ab it reports support_field
false, captured_selector false and no fixed sources; current code reports both
true and the exact Cargo runner/census paths. It performs no build or capture.

Version 1 keeps the original serialized field set and exact roundtrip bytes.
Version 2 adds zero or two closed support-source records: artifact_cargo.py and
artifact_cleanup.py, ordered exactly. Zero explicitly retains an unbound legacy
row in a mixed ledger. require_captured=True rejects such rows and checks both
support identities against current anchored sources. Legacy read-only matching
remains available. This is a record/source/file predicate, not an attestation
that a process ran; .21 must still provide actual successful observations and
.17 must require strict selection before any mutation authority exists.

Thirty-one provenance tests cover v1/v2 roundtrips, mixed-ledger preservation,
strict legacy refusal, each changed support source, closed names/order/shapes,
plain boolean selection and cold copied readers for both formats. Sixteen
individually failing guard omissions run normal/O, including three new ones.
The complete artifact gate has 100 outcomes; literal guard sites remain 1637.
No actual ledger publication, candidate selection, cache unlink or cleanup event
changes. Existing source/file/root/bounds controls remain intact.

D11 closes in the same documentation sync: COMMIT.md said "both books", while
Makefile52-54 builds the project and every unit book. Replace the stale count
with that stable contract. The public target, suite and push policy are exact.
Shared CLI teaching in the book, toolbox and doctrine row describe the new
version boundary. Current LIVE_STATUS is reviewed and unchanged: CPU 14/18,
board 10/12, replay 4/4 green; full processor qualification remains pending.

## _(2026-10-20 UTC)_ — bind public Cargo invocations (ARTIFACT-CLEANUP.20)

AC0074 splits .17 at a safe command boundary. The actual producer launch
extractor observes both old commands: absolute manifest, CARGO_TARGET_DIR only,
no explicit build.build-dir. The new control fails1/0errors before integration.
The shared helper now emits the exact13-argument public command accepted by the
existing per-file record protocol. Both target and intermediate paths retain
c-engine-build/c-guest-image-build; no historical output path is moved.

The helper validates runtime agreement, the public Git root/inventory boundary,
source/manifest snapshots and source/input/output/store/temp ancestors before
launch. Ambient Cargo/compiler/Git overrides are removed; Cargo home and temp
stay on-volume. Project Cargo configuration/build inputs remain trusted, and
the installed Rust toolchain is a necessary read-only external dependency.
No arbitrary configuration interpreter or build sandbox is claimed. Descriptor
and source/manifest checks repeat after the child; caller quiescence remains a
precondition. Each pipe is capped8MiB, elapsed time300seconds. The owned session
is killed and its leader joined after ordinary completion and every interrupted,
overflowing or timed-out run, including closed-pipe children. Partial captured
bytes cannot become a successful returned observation.

Controls:17 tests normal/O, eight targeted omissions each1failure/0errors;18
new outcomes bring ARTIFACT-COHORT to94. A cold copied actual Cargo build generates
incremental outputs and preserves a seeded cache-shaped input byte-exact, while
publishing no provenance. Both actual repository producers pass: engine18 tests,
guest2 tests. The descendant test uses an owned start/completion witness rather
than ps, which the restricted environment refuses; removing the group kill lets
that child publish its completion witness and loses one assertion. Its finally
block terminates exactly the observed owned child. Two pipe subcases aggregate
into one failure for the gate's singular-omission contract. Initial incomplete
control attempts remain diagnostic; the final complete94-outcome run is green.

No ledger, candidate-selection or deletion operation changes here. .21 owns
anchored before/after capture, complete helper/producer pins and atomic current
ledger publication; .17 then fixes P1 with strict plan selection. .16 journal/core
and .14 fresh host workflow still precede operator mutation. Historical source,
plans, events and original native capture remain unchanged. External policy
review: README/containment/guide diff21f4d3d..HEAD empty; claim source SHA9f99df25
unchanged. No source policy adoption is needed in this slice.

## _(2026-10-20 UTC)_ — retain the completed cleanup ledger (ARTIFACT-CLEANUP.19)

Own AC0073 after clean839e931/brief0/actual host census OK. The task family has
79 bytes left. Source root76937B/942 lines contains a38891B current graph prefix
and38046B/384-line completed checklist/log suffix. Thirteen acceptance sections
plus verification, commit and changelog history are the scaling term. Preserve
all19 nodes, child groups, goals, decisions, questions, blockers and frontier.

The all-owned tracked reference census names this root only in KNOWLEDGE_MAP
and the task index: two external records, no anchored links or live includes.
Generic progress/acceptance readers still consume the complete live node graph.
Store both the complete committed predecessor and exact removed suffix as plain
Markdown under a new finite terminal. All content stays directly browsable;
there is no compressed-only narrative, Git-history dependency or extraction.
The two products overlap: suffix is part of predecessor. Unretained bytes zero;
source identity, extracted history and current working set are separate measures.
Earlier P4/qualification/changelog seals and all their bounds remain unchanged.

The four-file terminal is119258B: two content-addressed Markdown originals, a
closed descriptor1300B and bounded retention page2975B. Its exact registry
ceiling permits no append. The descriptor binds source839e931, source Git blob
and mode, each original's SHA/bytes/lines, suffix offset38891, retention owner,
current path and independent raw narrative/section limits. The pinned reader
checks complete coverage, modes, identities, extraction equality and one live
pointer before output. Every old node/order/completed status/child group remains
live. New narrative counts embedded markup:16KiB health/32KiB ceiling, named
section ceilings,75% warning and90% rollover-required before ordinary growth.
This is the narrow ledger transition, not full containment-doctrine adoption.

The separate publishing gate uses bounded read-only Git queries. First publish
requires the exact committed source, complete prefix inverse apart from owned
.19 state/frontier, matching staged/working data and all wiring. Later checks
freeze the terminal against HEAD, retain completed live ledger entries and
node progress in both views, and need no source fetch in a shallow clone.
The checked reader itself uses neither Git nor network. Cold copied CLI reads
both originals with PATH empty, leaves all files unchanged, and refuses a bad
pointer before any original output. Independent direct Markdown bytes agree.

QA: the first probe had an invalid non-ASCII bytes literal; use explicit UTF-8
encoding before running controls. D6 then reproduced a parent symlink traversed
before refusal:33 tests/1 failure/0 errors. Validate every ancestor before the
first directory census. D7's pure publishing judge accepted an executable live
view and crashed on a missing published live root:35 tests/2 failures/1 error,
including D6. Give that judge its own complete mode/presence contracts. The host
reader's working-mode guard was already present. All cases use disposable owned
fixtures; no foreign repository or canonical evidence is touched. Fixed40 tests
normal/O pass;18 omissions per mode each give exactly1 failure/0 errors,38 total
outcomes. Physical missing-member, extra-directory and leaf-symlink cases join
the final guard set. These controls remain tracked; two wrappers join TASK-HISTORY (52 arms).

Book usage is included from the retention page. LIVE changes only43→44 governed
routes and1633→1635 literal sites;40 doctrines/CPU14/18/BOARD10/12/replay4/4green
remain. Native3/original37/capture/events and previous teaching must stay exact.
Focused checks, whole-source/history inverses, staged checks and normal COMMIT
follow. P1 remains owned by .17 actual build/provenance selection, then .16 core
and .14 host CLI before P4 policy/status. No cache deletion or push here.
D8 then accepted invalid UTF-8 in the new ledger (39 tests/1 failure/0 errors):
only the graph prefix was decoded. Validate the complete live task before any
original output; the final malformed-input and guard-omission controls cover it.
Initial focused routing check correctly rejected the new row in governance:
16827B exceeded its16384B part cap. Route this cleanup-specific tool to the
existing artifacts toolbox instead; old rows/limits remain intact.
Final focused17/books7/native3/source-history proof:21 files/protected1468/
1Gitlink/97 old entries;7210B whole0388/0389. Full predecessor and suffix remain
exact; live graph and all earlier teaching/captures/bounds are retained.
D9: the normal full hook refused FIXTURE-FINGERPRINT before creating a commit.
I used `path` with root-relative locators, but the established fixture contract
resolves that field beside its JSON record. The join duplicated the directory;
both real originals were present. This unpublished descriptor now uses explicit
root-relative `object` locators, rejected legacy-field controls and the existing
specialized digest verifier. Generic fixture code stays exact. Add its gate to
the focused set;40 tests normal/O/18 omissions and all data identities must pass
before normal commit retry. Metadata1300B/page2975B give exact terminal119258B;
only this new unpublished declaration changes size, no old ceiling increases.
D10: a broad focused-count replacement changed two prior DEV counters. Rebuild
all retained prior entries from839e931 minus the exact0388 suffix, preserving
only this new entry. The full inverse proves original bytes/order restored;
future edits stay inside this first section. No commit contains that error.
D9/D10 final verification: expanded focused17, fingerprint re-derivation,
40 tests normal/O/18 omissions, seven books and complete source/history proofs
pass. The first failed hook remains in commit-attempt-1.log. Retry the normal
hook with exact21 files and all old source bytes/ceilings retained.
Promotion declined: applies the adopted task-ledger transition contract.

## _(2026-10-20 UTC)_ — bound workflow guidance and align the template (ARTIFACT-CLEANUP.18)

From clean70516a7/brief0/actual host census OK, the task family has352B of
headroom. Own AC0072 before edits; transfer repeated template guidance into the
existing setup guide under its own finite contract. Do not remove task history,
change frozen archives or raise any old ceiling. This also stops new trees
copying the same long policy explanation into every task file.

Before-state: TEMPLATE has five labels and omits REPRODUCE / ISSUE from the six
required by DOCTRINE_ENFORCEMENT and the book. The guide recommends .2.1, but the
public task_source.direct_leaves contract rejects OWNED.2.1 as a foreign leaf;
OWNED.2/.3 both parse. Correct the guide to direct numeric IDs and activity
grouping; do not weaken or modify the source reader.

Keep the complete old1898B evidence section and316B general criteria in the guide,
adding the missing sixth box. The compact copyable template preserves metadata,
graph/frontier and logs, with a leaf-qualified six-box checklist and a direct
guidance link. Template3414→1804B releases1610B from the task family. The guide
grows1704→4259B/78lines; register it as a canonical normative destination, health
100lines/5120B and ceilings128lines/6144B. It is a controlled destination rather
than unbounded overflow. All old registry rows/ceilings remain exact.

The book includes the shared guide anchor. Render QA found a plain angle-bracket
placeholder treated as markup; fence the complete copyable Markdown checklist.
All placeholder text is now visible in normal and print output. The template's
new placeholders use inline code. Complete original-template reconstruction
and guide inverses retain all guidance; only the unsupported nested-ID advice
changes meaning. A materialized OWNED.md parses as proposed with OWNED.1 pending;
its six labels exactly match the normative checklist. No runtime or parser change.

Routing/derived counts/book builds pass;43 governed destinations,40 doctrines/
1633 arms and CPU14/18/BOARD10/12/replay4/4green. Original native3/41514B exact;
no capture, cache mutation or new cleanup event. Focused/source/history/cap
checks and normal COMMIT follow before .17 actual-build/provenance selection.
Promotion declined: applies existing workflow/containment policy without a new
cross-cutting decision. Detailed original records remain in their existing homes.

Final focused16/books7/scope pass:13 files/protected1467/97 old entries;4001B
whole0386/0387. Task family3145649/3145728 (79B left): template
contribution shrank1610B, while unit tracking consumed the room. Retain the
completed ledger in .19 before further ordinary growth; all history stays exact.

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

## _(2026-10-19)_ — check the retained finite DIV method (P4-SYSTEM.14 a42ao)

Tools-first baseline: the actual lower evaluator binds85 files/1048756B and all
separate findings, yet leaves method/policy pending. Input influence reachability
alone does not bind the evidence fingerprint; a self-consistent forged receipt
can establish bytes without actual execution provenance. Compose public owners
in matched_gpr_adequacy and read-only review_div_method: independently selected
73 inputs, exact native generator, only12 observation hashes/sizes+3 exits may
change the plan, and actual evidence node selects its planned SHA. Curate the
original measured record identity from reviewed source/declaration/capture history;
trust remains the tracked collector/procedure, no independent attestation or
ancestry credit. Method satisfied; full policy pending; replay not checked.
Require typed complete findings, exact manifest/artifact selection and released
payloads. Preserve independent findings after late checker refusal. One128MiB
native/evaluation allowance charges1100198B (51442+1048756); failed calls retain
reservations, malformed receipts refuse. Snapshot33759B within16MiB; preparation,
schema/tool I/O and39-module census/recheck remain separately bounded. Old producer
population37 and all original artifacts/pins remain exact; no Sail rerun.
Twenty tests normal/O pass;14 targeted omissions lose4/1/4/2/2/1/2/1/3/4/1/1/1/1,
no errors,30 matrix outcomes. Copied103-file runtime has no Git/materials/binary,
processes denied and valid parent cwd. Includes fully consistent forged stdout,
exact/short allowances, missing/stale data and late source drift. Fixture QA:
first forgery used output instead of codec observation, reproduced20/1/0 and
corrected before guard audit; production was unchanged by that fixture repair.
Retain four whole an records2184B in the existing task-claims artifact; old128068B prefix exact.
New model chapter/toolbox/decision includes; public arm enumerator1625 (+2literal
score sites, not expanded loop count). CPU14/18/BOARD10/12/replay4/4 unchanged.
Focused17/books7/rendered5/examples3/scope normal/O pass; whole history6009B retained0375/0376; source-owner inverses2/eight damaged refusals. Evidence target/p4-system-14/a42ao.
Promotion declined: existing caller authority, provenance and finite-method rules.
Task count108 exceeded107. TASK-PRESERVATION also refused an append to published
part19: whole published archive blobs are immutable. Restore part19 exactly in
both views. Compact only new reconstruction metadata and retain all4 original
records2184B under one address in existing task-claims; old128068B prefix exact.
A broad wording replacement touched an older CH0247 phrase; whole-history
proof caught it. Rebuild the old tail from BASE and its exact moved suffix.
Diff whitespace reports only original trailing blank separators in the two new
whole-entry shards; all other changes pass. Preserve those original bytes.
No capacity increase, history trim or gate exception. Focused acceptance also
required explicit rc=0 in each evidence bullet; retain actual command outcomes.
A root-wide status-text query entered vendor accidentally. Its results were
unused; no vendor writes. Restrict searches to explicit project-owned paths.
Next full source/risk/feature policy and qualification/status integration.

## _(2026-10-19)_ — synchronize completed capture and replay teaching (P4-SYSTEM.14 a42an)

The two canonical decision includes/index and adjacent evidence/reference/collector
chapters still claimed collection/retention pending after c91d08f5 retained it.
Native format is matched-gpr-v1; v2 names the DIV case, so the no-v1-capture claim
was also stale. Gaps, P4 overview and architecture detector prose still placed GC
reduction/CLI support in the future after .16 closed. Reproduction: scoped nine-
source census/native record plus generated GS report G-REPLAY4/4green.
Root cause: completion-state teaching missed the canonical include/index owners
and neighboring replay paragraphs. Correct only current-state prose, keep dated
census historical, preserve protocol/limits/trust boundaries and every example.
The canonical command's absent-name preflight differs from the low-level API's
owned-output clearing; describe both accurately. No capture rerun or code change.
Full method/policy qualification and CPU acceptance remain pending.
Four complete closed am records2574B retained with source/owner metadata; fixed
caps. Focused17/books7/rendered9/scope normal/O pass;46 complete examples exact.
CH0374 whole1107B; inverses2/eight damaged refusals. Evidence target/p4-system-14/a42an. Promotion declined: existing canonical-owner lockstep
and currentness doctrine; next full policy/status integration.

## _(2026-10-19)_ — retain the first canonical DIV capture (P4-SYSTEM.14 a42am)

Committedb160c66e source/declarations and all73 input pins precede the one capture.
Public bounded executable pin matched3801664B. Fresh PIDs39909/39914/39918 exited0;
12 observations14830B, measured record9928B, derived verification7093B retained.
All27 source/GPR boundaries: baseline/repeat AGREE, control DIVERGE only step2 x7
(-3 actual/-4 expected). Three2298B traces hash64551458d50ec4345b716abd9f2caf4b42053d6f3a8640735ee539d89a968bde.
Independent normal/O checks restore only measured metadata to the exact plan,
authenticate all observations and reproduce separate matched findings offline.
Charge24337600B within128MiB;85 authenticated files1048756B/33759B snapshots.

Add one real-retained, process-denied command test:19 normal/O; seven omission
losses unchanged6/1/1/1/2/1/1,0 errors. Ten101-file offline-copy outcomes cover
valid/missing/stale/refused raw data with no Git/materials/binary. All producer
logic/native declarations remain byte-exact. Family22files/fixed caps. Complete
policy/qualification/REQ-GC-M/OB-GC-M/CPU closure remain pending; no broader credit.
Derived receipt initially collided with generic record-relative path fingerprints.
Tool reproduction and existing .4 precedent establish root cause: name root-relative
identities object, map explicitly for native readers; no exclusion or cap change.
Focused17/books7/examples6/surfaces8/scope pass normal/O; legacy8+38+4 exact.
Whole predecessor entries5007B retained0372/0373. Evidence target/p4-system-14/a42am.
Four whole al records2498B/inverses2/eight damaged refusals; promotion
declined under existing bounded-capture/retention/independent-findings doctrine.
Never rerun or overwrite historical outputs; next full source/risk/feature policy.

## _(2026-10-19)_ — retain exact DIV predeclarations (P4-SYSTEM.14 a42al)

Curate planned-experiment.sexp9901B, dependencies.sexp14488B and authorities.sexp
17125B from the composed public owners before canonical execution:41514B total.
Validate raw planned schema/scoped graph,64-child codec and73-input inventory;
check native authority grammar, fresh names/parents, exclusive complete writes,
then anchored pin/size/equality and independent re-preparation. No Sail process.
The evidence family now holds8 files within unchanged22/16MiB/4MiB bounds.

Add actual retained-package comparison to the command controls, so stale native
files fail before execution. Suite18 normal/O; same seven omission losses
6/1/1/1/2/1/1 with0 errors. The source/authority reports now describe separate
verification obligations without falsely claiming whether external data exists.
An87-file copy with parent cwd available and no Git/materials/binary delegates
only to an explicit recording mock. Valid/status/prose cases bind73 inputs and
all separate reviews; six missing/changed native states stop before delegation.
Eighteen copied outcomes pass across both modes. These are not Sail observations.

Adjacent capture-plan text still said final execution composition/inventory were
pending after0279 implemented them; source/book comparison reproduced the stale
paragraph. Correct that section and all current declaration-state teaching;
preserve every old example and add actual native verification. Declarations are
readiness claims, not observed successes. Once observations exist, keep their
original declarations; affected source changes need separately owned revalidation.
Retain five complete closed ak/y records3534B with source/owner inverse metadata
inside task-claims, inverses2/nine damaged refusals; CH0371 whole1303B retained.
Focused17/books7/examples4/surfaces5/scope pass normal/O.
Evidence target/p4-system-14/a42al. Promotion declined: existing source-closure,
currentness and bounded-retention rules. Next commit declarations, then fresh
Sail baseline/repeat/control, retain/evaluate outputs and complete full policy.

## _(2026-10-19)_ — compose the finite DIV command (P4-SYSTEM.14 a42ak)

capture_div now composes the exact native plan/dependencies/authority declaration
from current validated views and the independently enumerated37-module/64-child
source/data review. Nine principals plus64 children supply the separate73-input
inventory; existing input/author/impact owners freeze it. One conservative edge
per input reaches planned evidence; initial old/new projections are equal, with
no earlier canonical capture claim. Selected retained identity and prepared image
bind separately; live status/view hashes stay outside execution inputs.

Raw schema/scoped graph precedes mapping/binding. Three native documents remain
within64KiB each; --declare writes none and launches no reference. Five curated
principals read twice at64KiB each, plus three64KiB declaration reads for capture,
stay separate from existing review/tool I/O and combined128MiB/16MiB envelopes.
--capture requires all exact native predeclarations before delegating the existing
combined helper with input/author/impact/property authorities. Operator commits
source and declarations first; no Git attestation is invented. Measured record/
findings return to the caller for bounded retention, with no qualification.

The84-file copied runtime keeps parent cwd available. Synthetic executable pins
are explicit fixture identities, not Sail. Three fresh processes, all27 source
values, repeat bytes, wrong quotient, separate review findings and executable-
absent offline evaluation compose successfully. Reuse refuses/preserves bytes;
exit7 keeps a real baseline receipt and stops before repeat. First output-reuse
fixture lacked its binary and correctly returned unavailable before freshness;
install the synthetic binary before asserting reuse refusal. Declaration subcase
cleanup now runs in finally; injected assertion failures prove independence.
Unavailable input findings use CaptureUnavailable/OSError and retain the owner
reason; do not infer a missing file from permission-denied or other I/O failures.

17 controls x2/16 exact outcomes; omissions lose6/1/1/1/2/1/1,0 errors. Focused17,
books7/examples3/surfaces5, legacy8+38 and scope/inverses pass normal/O. Six complete
closed aj/aa/z records3566B retain source/owner inverses2/ten damaged refusals;
whole DEV/CH entries5666B retained0369/0370. Evidence target/p4-system-14/a42ak.
All caps fixed; no canonical outputs/reference run or CPU/board acceptance.
Next curate/commit three exact native declarations, then fresh Sail/full policy.
Promotion declined in leaf: existing source-closure/bounded-reader/authority rules.

## _(2026-10-19)_ — seal a second finite history segment (LIVE-CONTAINMENT.4 .4j)

LC0049 interrupts the next feature slice only for measured rollover failure:
ordinary history159 files/782755B leaves3677B, while DEV leaves17B and its
oldest whole entry3787B already exceeds family room before wrapper/manifest.
Use standing archive delegation retained from LC0041; the existing finite
archive topology and public reader suffice. No runtime implementation changes.

Capture exactly158 closed shards and their15010B manifest from a5bf45798255bca41d73f284bfe6987f48fc351f:
159 originals782755B/11200LF. Independent Git tree/mode/blob checks, two identical
serializations and all159 Python/tar member comparisons bind complete source.
The new276917B object SHA89ad7214ebbf637cc48dc4468f3d43fb7d0f2eb08a43fa5c4ab42118ba8df2b5
is a distinct immutable segment. Old284500B object and descriptor stay exact.
Relocated normal/O public CLI authenticates368 shards across two objects without
local Git/materials/extraction. New corruption and old descriptor changes refuse.
Only after published-copy comparison retire exactly158 known sources; residue0.

Separate bounded LC0049-CAPACITY record in task-claims reviews this one expanded
finite terminal:4 files,565623B health,581897B ceiling = two fixed objects561417B
plus existing index16384/front4096 bounds. The old finite contract covered one
segment; this exact source-defined addition expands only that archive contract.
Ordinary/history-head and all other capacities and reader limits stay fixed.
No new decision file or general lifecycle change: this is a finite implementation
of the standing delegation. Future seals require fresh ownership/review.

The two manifest snapshots share a former logical path at distinct capture
boundaries; logical shard sets are disjoint. Complete-source identity, semantic
closure, live dimensions and unretained residue are separate products. No source
bytes are lost. Current live receipts remain native; numbering starts0367 after
retired0366. Two external textual references are historical/source-pinned, with
no live integration read. Existing263-outcome query qualification remains pinned
to23fdb8 and its original222 members; current two-object proof is separate.

Retain the complete closed LC0041 record5552B in existing task-claims with source/
owner inverses; keep its standing authority recoverable. Main book changes only
current archive teaching, preserves old examples and adds the new-segment read;
its family shrinks8B. Public reader/partition/probes remain byte-exact.17 focused,
44 history controls,263 source-pinned queries x2/0 defects, seven books/four complete
examples/three rendered surfaces pass. Scope1415 protected files/1Gitlink/95 prior
live entries; whole4747B live predecessor rollover, full LC0041 source/owner
inverses2/seven damaged refusals. All other caps fixed; normal COMMIT required.
Automatic approval review twice rejected the commit: recorded delegation did not
supply trusted user approval for158 retirements. Director2026-10-19 explicitly
answered “Approve LC0049 and continue” to the158-source verified archive migration,
finite terminal bound and local commit without push. That scope is now directly
authorized; normal COMMIT/postconditions remain required. The app-control safety
boundary prevented changing its permission selector; no setting was altered.
After COMMIT return to P4.14 execution/authorities.
Evidence target/live-containment/history-rollover; promotion declined (existing
finite archive, bounded-reader and source-preservation contracts).

## _(2026-10-19)_ — review current authority loaders (P4-SYSTEM.14 a42aj)

Review the public authority API alongside the producer route:37 modules,27
execution data,13 current views/39 unique data,64 children,79 files. Trace
Path.open before delegation, reject writes/processes, bind returned view facts.
Keep live views outside flat execution pins; outer and nested snapshot/tool I/O
contracts stay separate.31 controls pass normal/O;18 guard omissions discriminate
with0 errors (five new guards lose1 each). Copied79-file reports match both modes;
legacy authority18/three omissions remain exact. Whole history/task records and
Fix adjacent prepared-input35/63 teaching drift to37/64; rendered check added.
No capture/qualification.17 focused/seven books/one example/four surfaces and scope
pass. target/p4-system-14/a42aj; normal COMMIT.

## _(2026-10-19)_ — select current DIV capture authorities (P4-SYSTEM.14 a42ai)

Add read-only capture_div.review_authorities/--review-authorities. Freeze the
current public Scope, selected ReferenceIdentity, reviewed PropertyAuthority and
thirteen immutable view identities. Predeclare seven catalogue/contract views,
five schemas and the scope owner's registry; use the existing review snapshots
with1MiB/member,8MiB/shared pass and two passes. Public schema/catalogue/scope I/O
remains separate, under a trusted quiescent runtime with before/after byte checks;
no atomic-set or total-RAM guarantee. No binary, capture, acquired source, process
or authority-file publication. JSON is diagnostic provenance, never execution pins.

Validate all raw roots/parts and expanded obligations before canonical mapping;
reuse the sole include expander and existing record/dossier mappers. Reject duplicate
IDs before selection and use public effective scope, including supersession/cycles.
Bind the selected DIV semantic authority to the independently reviewed case.
Derived status changes provenance but not that projection; parent prose likewise
does not change selected execution identity. Current binary-pin changes are only
declarations here; binary/retained-identity authentication stays with execution.
Catalogue/contract integrity and full policy remain existing gate obligations.

Prototype defect reproduced in an owned50-file copy: an alternate valid registry
could be read while provenance still listed only the original13 views. Bind the
sole registry path before scope delegation, and retain the same fixture's refusal.
The actual unknown include/registry controls observe that neither path is opened;
the registry-binding omission loses one assertion in both modes.

Initial probe fixture assumed its first form was the document, overlooking native
outer structured comments. Correct the fixture's document selection, preserving
the error log; no production guard weakened. Final18 controls pass normal/O;
raw/registry/semantic omissions lose3/1/3 assertions,0 errors. Fifty-file copies
without binary/materials cover actual13-view reads, eight validations before maps,
immutable detached facts, shared aggregate-before-tools, direct bounds, safe paths,
duplicates, missing/foreign/superseded authority, semantic/status changes and drift.

The existing producer review stays35modules/27data/63children/66files965337B;
its old route does not yet review the future final entrypoint. Re-review that
route before final manifest/inventory/author/impact composition and capture.
No qualification or acceptance credit. Promotion declined in leaf: established
canonical-authority, bounded-reader and isolation contracts. Whole prior ah/ab
records retained with inverses; whole history/caps preserved. Focused/books/scope
verification pass:17 focused checks/seven books/two complete examples/three rendered
surfaces.1569 protected files/1Gitlink/93 whole old entries and all old production/
probes exact except regression registration. Six complete prior ah/ab records3137B
retain source/owner inverses2/ten damaged refusals; CH0365 preserves one whole oldest
1104B entry. All caps fixed. LIVE derives1621arms only;42routes,CPU14/18,BOARD10/12,
replay4/4green unchanged. Final route/manifest/reviews/capture/policy remain pending.
Normal COMMIT applies.

