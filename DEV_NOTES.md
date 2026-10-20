# DEV_NOTES.md

## _(2026-10-20 UTC)_ — the decisions family re-derived a second time (LIVE-CONTAINMENT.4k)

LC0050 after b70b2f5, clean tree and `handoff: OK`. The routed-in finding
reproduced exactly: with only the new record's index row added, the route
checker reported OVER CEILING docs/decisions/: 262287 > 262144. The census
behind the decision: 59 records, 26 of them landed 2026-10-02..12 and none in
the eight days since, while two units withheld or edited records to fit —
the cap was already suppressing layer C. The alternatives the routing asked
for were measured before the 2× re-derivation: the two superseded records are
superseded in part (8,829 B, still cited), a second terminal forks layer C,
and no duplicate exists. The lesson is not new; it is the first record's
grounds observed a second time, so it stays in the tree (promotion declined).
What is new is the measurement that the next bite is the index's per-part
ceiling (13,234 B at 59 rows), which an index partition must answer, and the
next containment unit is the P4 tree's own retention capacity: its file,
its complete-records artifact and the task family are all within 200 B or
0 files of their ceilings, so P4.14 a42ap cannot record itself yet.

## _(2026-10-20 UTC)_ — the first cleanup through the supported act (ARTIFACT-CLEANUP.24)

AC0081 after cfca1c2, clean tree and `handoff: OK`, at 23 h under the roughly
24 h cadence. The four acts ran in target/artifact-cleanup/AC0081 with the run
log inside the work directory, so the plan stayed exact. Plan: 19 cache-named
candidates and 18,724 retained files. Strict selection approved 6 (the latest
captured engine, guest and core sessions) and left 13 unrecorded: the .13
smoke-input fixture and the sessions the pre-commit hook's failing mutation
builds leave behind, which capture never records and rustc garbage-collects on
the next successful build. The act's own census returned `handoff: OK`, the
guarded core revalidated and removed exactly the six, residue 0, and the
journal finished `recorded-complete` at `verified`. `--inspect` reads plan,
selection and journal back with current pins. The one-entry record is
overwritten from the receipt. This is the first event whose every step is a
tracked instrument with its own controls; the old scratch helper and its
receipts keep their historical identity.

## _(2026-10-20 UTC)_ — the supported cleanup act (ARTIFACT-CLEANUP.14)

AC0080 from clean 1ed7cbe. The host census was a handoff ritual the unlink
path could not prove had run. The operator module is now the single deleting
command. `--delete` starts the public census script as a bounded child of the
repository root in its own session (GIT_* stripped, on-volume TMPDIR, 60 s
deadline, 1 MiB output bound, group kill on timeout) and proceeds only on exit
0 with the `handoff: OK` verdict line. Exit 1 refuses as project work running;
exit 2, a timeout, empty or oversized output or a missing verdict refuse as
unavailable, because an absent snapshot is not an empty process set. The
census keeps its own user, sanctioned exemptions and observation limits; this
act does not reimplement or wrap its judgement, only its moment. Then the
guarded core runs and one JSON receipt reports disposition, stage, counts,
failure and the journal path; `--inspect` reports plan, selection and journal
without a census or mutation. Exit codes: 0 complete/nothing, 1 stale or
partial, 2 refused, 130 interrupted with the journal written.

Controls stub the census script inside the fixture with a case file, so green,
running, unavailable, empty, oversized, timed-out and verdict-less censuses and
partial/interrupted attempts are exercised without touching the host process
table or any real cache: 10 tests normal/O and three omissions. A second act
on the same work directory refuses as stale and, thanks to D14, names the
first gone member; the usage text says to plan and select into a new directory
instead. The priority1 durable-instrument activity closes; .24 is the first
recurring cleanup through the act, due after 2026-10-20T23:07Z.

## _(2026-10-20 UTC)_ — guarded deletion core (ARTIFACT-CLEANUP.16)

AC0079 from clean 6740f24. Three records existed and nothing bound them at the
moment of mutation. The journal's sequence rule expected intents over the whole
plan, so an attempt restricted to the strict selection could never record
`complete`; a version-2 begin now carries the selection digest and the sorted
approved plan indices, intents must follow those indices and completion needs
every approved return. Legacy version-1 journals stay readable.

The guarded core is the repository's only unlink path. Its preflight re-runs
strict selection (fresh census, tracked inventory, ledger and pins) and requires
equality with the saved selection, so authority is current at the moment of
use. Each approved file is then reopened through its parent descriptor, which
refuses symlink, foreign-volume and nested-Git ancestors; the candidate must
still be untracked and its device, inode, mode, single link, size, mtime, ctime
and digest must equal the plan's fact. The intent is flushed before the unlink,
the return recorded after, and the file must be absent. A refusal, an unlink
error or residue finishes the journal as failed at its stage with the count
already removed; an interruption is recorded and propagates. The after-state
must equal the plan minus the approved files, named by the same difference()
that now makes stale verdicts explain themselves (D14).

The identity check before unlink is defense in depth: the descriptor snapshot
already refuses on any identity change, so the discriminating seam removes
both lines together. Twelve tests and four omissions cover unlink errors,
residue, a rewritten retained file during the attempt, a parent replaced by a
symlink, a failed durable intent, interruption, an empty selection and the
cold dry-run CLI, which has no delete option. Only owned fixture caches are
ever removed; the supported act with the fresh host census is .14.

## _(2026-10-20 UTC)_ — select strictly against the published ledger (ARTIFACT-CLEANUP.17)

AC0078 from clean 962c91c. The baseline at b18971e was measured before any
code change: a real plan held 19 candidates and the strict reader approved
none. The comparison log pinpointed two causes. D12: the pre-commit hook runs
the producers' mutation controls, whose builds fail by design; capture returned
early and published nothing while rustc garbage-collected the recorded session
directories, so rows named files that no longer existed. D13: rustc seeds each
new session by hard-linking the previous session's files, which moves ctime on
an unchanged inode, and exact Fact equality rejected those rows.

Fixes: a failed build now records nothing but still publishes a merge whose
only effect can be retiring rows for files it removed; the reader compares
every identity field except ctime_ns and still requires one link. Both have
discriminating controls. The planner itself is unchanged: selection is a new
module beside it. decide() re-censuses the plan's scopes and refuses a stale
plan or a changed tracked inventory, then intersects the candidates with
authorize(require_captured=True) and records the approved/unrecorded partition,
byte totals, plan/tracked/ledger digests and the selector, planner and reader
source identities. publish() exclusively creates selection.json beside the
still-identical plan; inspect() decodes it against the plan and reports whether
the pinned sources are current. A forged ledger row for a cache-named input
refuses the whole ledger, so P1 closes: a name never grants ownership.

Controls: 11 tests normal/O and five omissions, each one failure and zero
errors; the gate has 128 outcomes and the literal arm count is 1639. A first
partition seam did not discriminate because the byte-sum checks caught the
same variants; the variants now keep byte sums consistent so only the partition
rule catches them. Actual engine and guest captures followed by plan and
selection on the real tree are in target/artifact-cleanup-0078. Guarded
deletion (.16) must bind plan, selection and journal and revalidate every
file immediately before unlink; the host-bound operator workflow is .14.

Two real selections went stale first. The verdict named nothing; a plan diff
showed exactly one retained member changed: the run log I was writing under
target/artifact-cleanup-0078, inside the census scope, growing between plan
and selection. Run logs belong in the selected workdir, as the planner's usage
already says; the third run kept its log there and selected 9 of 19. The
nameless stale verdict is owned as D14 under .16.

## _(2026-10-20 UTC)_ — second ledger generation (ARTIFACT-CLEANUP.23)

AC0077 from clean b18971e. The reader reported 12,947 live narrative bytes with the
75% warning raised, and the next checklist would have crossed the 90% line where
ordinary growth refuses. The generation-1 design pinned one source, one owner and
one descriptor digest and froze the four-file directory, so a rollover was
structurally impossible without an owned transition.

The descriptor becomes schema 2 with a generations list. Each entry keeps the
generation-1 fields plus its own front-page digest and a predecessor_pointer: the
digest of the descriptor it superseded, which the reader re-derives from the
retained entries (`encoding`) rather than storing old descriptors. A later
generation's retired suffix must begin with the previous generation's exact pointer
and its predecessor prefix must preserve the earlier graph, so the chain
authenticates itself without Git. The current descriptor must equal its canonical
encoding. The publisher accepts exactly one new generation per transition: HEAD is
the source, HEAD's live task is the predecessor, earlier objects stay byte-exact in
staged and working views, and the owner's state plus the frontier are the only
prefix changes. Generation 2 retains the b18971e predecessor (58,246 B) and its
13,433 B suffix; the live narrative resets to this leaf's own records.

Controls: 45 tests normal/O and 20 omissions, each one failure and zero errors; the
new seams are the canonical-encoding check and the one-generation count rule. A
first earlier-generation freeze seam could not discriminate because the chain
digest and object digests already pin every earlier object; it was removed. The registry row is re-derived to 6 files / 192,801 B under
this leaf's authority; the per-part bound stays 76,937. A decision record was
drafted first and withdrawn: README-ROUTING-CLOSURE fired OVER CEILING on
docs/decisions/ (262,242 > 262,144 B with only its index row added), the family
is past its warning with no owner, and raising a ceiling to land content is the
failure the registry header names. The pressure is routed to LIVE-CONTAINMENT.4
slice (k); the trimmed draft is retained in target/artifact-cleanup-0077.

Owned for .17, measured after AC0076's commit: D12, the hook's deliberately failing
mutation builds publish nothing while rustc still garbage-collects recorded session
directories, so the ledger names files that no longer exist; D13, rustc hard-links
the previous session's files into the next one, moving ctime on unchanged recorded
inodes so exact-fact matching rejects them. Evidence: target/artifact-cleanup-0078.

## _(2026-10-20 UTC)_ — capture and atomically publish bound build outputs (ARTIFACT-CLEANUP.21)

AC0076 resumes PNT from clean 47d69ef on the director's instruction. The
--publication-contract diagnostic, loading that revision's codec through
bounded read-only Git, reports census/observe/merge/publish all false and the
runner returned the process without observing its output root; no ledger
existed under target/artifact-cleanup. That is the gap between the .15/.22
record contract and any actual observation.

The recorder gains four functions. census walks one producer's
debug/incremental root exactly three levels deep through the planner's
descriptor traversal, hashes only the three cache names, and refuses alias
collisions and entry/record bounds. observe pairs before/after facts: a new
path or a changed digest becomes a v2 row; an unchanged digest, a tracked
alias or a hard-linked file is left unclaimed. merge replaces same-path rows,
retires this producer's rows whose files are absent from the fresh census and
keeps every other row byte-for-byte, legacy rows staying unbound. publish
rechecks all four pins against current sources, takes a non-blocking flock on
output-provenance.lock (a held lock refuses: quiescence is the caller's
precondition), writes a uniquely named temporary, fsyncs plus F_FULLFSYNC,
renames over the ledger, fsyncs the directory and reads the result back. The
previous ledger is never opened for writing; a rename or write failure keeps
it exact and retains the partial under its reported name.

The runner splits _invoke from run and adds capture: a bounded cargo
--version, the census before and after the bound process, then publication.
A nonzero build returns without publishing. The redundant source recheck
between build and publication was dropped because publish already refuses
stale pins; a control could not discriminate it. Both producers call capture
and print one output provenance line.

Controls: provenance 42 tests normal/O with 22 omissions, Cargo 23 tests with
10 omissions, each omission one failure and zero errors; the gate has 116
outcomes and the literal arm count stays 1637. The first probe draft called an
empty publish before creating the support pin fixture; the refusal was
correct and the test now creates its pins first. Actual engine and guest runs
published the first real v2 ledger. Strict selection against it is .17.

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

