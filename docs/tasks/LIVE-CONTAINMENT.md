# LIVE-CONTAINMENT: every live surface has a lifecycle, a bound, and true content

## Metadata

- Tree ID: `LIVE-CONTAINMENT`
- Status: `active`
- Roadmap lane: cross-cutting maintenance — session-directive §18 (live-document size
  containment, the external guide adopted by project-owned copy) and `README_POLICY.md`'s
  own trigger ("when one fires, the containment doctrine is adopted rather than the
  ceiling raised")
- Gate: none of its own — README-ROUTING-CLOSURE, FRONTIER-SYNC and KNOWLEDGE-MAP judge it
- Created: `2026-10-06`
- Owner: repo-local workflow

## Goal

Keep the live documents every session reads both TRUE and BOUNDED: correct the orientation
sources that drifted from the repository, give the governance surfaces that sit at their
ceilings real headroom by applying their declared pressure controls (never by raising a
number), and adopt the live-document containment doctrine the README policy names as the
answer once ceilings fire.

## Non-Goals

- **No ceiling is raised** without a reviewed decision that the surface's contract expanded
  (the registry's own rule); this tree applies controls, it does not widen numbers.
- **No durable information is dropped**: a surface that sheds content routes it to a
  canonical, retrievable home first (the guide's non-negotiable answer).
- Existing append-history heads keep their lossless shard control. `.4` now owns the
  aggregate archive transition exposed by the `2026-10-08` pressure census; sharding
  alone controls per-file size, not aggregate growth.

## Acceptance Criteria

1. The orientation sources state what the repository is today, each claim measured.
2. `docs/TASK_TREE.md`, `TOOLBOX.md` and `DOCTRINE_ENFORCEMENT.md` regain headroom through
   their declared controls, with every gate that mirrors them green.
3. The containment doctrine is adopted by project-owned copy with this repository's own
   inventory and measurements (the guide's Phase 2), or explicitly deferred with a trigger.

## Task Tree

- ID: `LIVE-CONTAINMENT`
  Status: `active`
  Goal: true and bounded live surfaces
  Children: `LIVE-CONTAINMENT.1`, `LIVE-CONTAINMENT.2`, `LIVE-CONTAINMENT.3`, `LIVE-CONTAINMENT.4`

- ID: `LIVE-CONTAINMENT.1` — **the closed-tree register: completed trees leave the index**
  Status: `done` (`2026-10-06`, `SEMULITH-LC-0001`)
  Goal: `docs/TASK_TREE.md` (8,172 / 8,192 B; 31 rows, 22 of them completed trees) applies its
  own registered control — "one row per active tree; completed trees leave the index" — by
  moving every completed tree's row, verbatim, into a closed-tree register
  (`docs/TASK_TREE_CLOSED.md`, registered with its own bound), and FRONTIER-SYNC learns the
  register: CLOSURE over the union (every tree file in exactly one of the two), a completed
  tree in the active index is a breach, a non-completed tree in the register is a breach, and
  the COUNT check covers both files.
  Acceptance: the index below its health target; the move enumerated (rows before == rows
  after across both files, byte-identical); FRONTIER-SYNC's new arms observed RED before the
  real files depend on them; every mirror gate green.
  Result: **met.** 22 completed rows moved verbatim (31 = 9 open + 22 moved; every moved row
  byte-identical in the register), the index 8,172 → 4,053 B with this tree's own row added;
  `docs/TASK_TREE_CLOSED.md` (4,861 B) registered (health 8 / ceiling 16 KiB); FRONTIER-SYNC
  gates both files — run against the real pre-move index it reports 22 `COMPLETED IN INDEX`
  (rc=1). The book includes both anchors live.
  Verification: `2026-10-06` — the Verification Log below.
  Commit: `SEMULITH-LC-0001`
  `promotion: declined (the lesson — a registered pressure control nothing enforces is a wish — is mechanized: FRONTIER-SYNC now refuses a completed tree in the index).`

- ID: `LIVE-CONTAINMENT.2` — **the stale orientation sources**
  Status: `done` (`2026-10-06`, `SEMULITH-LC-0002`)
  Goal: correct the three measured drifts: `knowledge-map/subsystems.md` (the one
  hand-curated input to the derived Knowledge Map) describes a `crates/app/` scaffold
  placeholder that does not exist and omits the definition, unit, schema, materials and
  book subsystems; the workspace `Cargo.toml` header still tells the reader to "rename/replace
  the starter `app` crate"; `README_POLICY.md`'s local adoption note says "this repository has
  no measured pressure … the largest live surface is `CHANGELOG.md` at 16,228 bytes".
  Acceptance: each corrected statement measured against the tree; the derived map
  regenerated; `make check` + `make gate` green.
  Result: **met.** The map's subsystem section now names the four real crates (their
  roles and the CLI's nine subcommands read from the sources), the definition fragments and
  their semantics, the six unit directories, the schemas/materials, and both book
  families; the workspace header names its members; the README policy's adoption note
  states the measured firings and routes the doctrine adoption to `.4` (the policy's
  decision itself unchanged — it changes by reviewed decision).
  Verification: `2026-10-06` — the Verification Log below.
  Commit: `SEMULITH-LC-0002`
  `promotion: declined (per-surface drift, corrected; the class — hand-curated orientation text — is .4's inventory question).`

- ID: `LIVE-CONTAINMENT.3` — **headroom for TOOLBOX.md and DOCTRINE_ENFORCEMENT.md**
  Status: `done` (`2026-10-06`, `SEMULITH-LC-0003`)
  Goal: `TOOLBOX.md` (20,478 / 20,480 B) and `DOCTRINE_ENFORCEMENT.md` (32,669 / 32,768 B) —
  both "one row per" normative tables — are partitioned behind a bounded index (the book's
  `partitioned` precedent), so the next tool or doctrine can be registered.
  Acceptance: both below their health targets; REGISTRY-MIRROR, MEMORY-ARCH and
  README-ROUTING-CLOSURE green; no row lost (an enumerated before/after census).
  Result: **met.** `DOCTRINE_ENFORCEMENT.md` 32,669 → ~11 KB: the 35 long-form project
  rows moved verbatim into `docs/doctrines/{governance,definition,evidence,board}.md`, the
  parent keeping a complete id → family index (still a full REGISTRY-MIRROR mirror), and
  REGISTRY-MIRROR now also judges the families' union in a new project scope (13/13 arms; RED
  when one long-form row is removed). `TOOLBOX.md` 20,478 → ~3.2 KB: the 76 rows moved
  verbatim into `docs/toolbox/{governance,definition,composition,execution}.md` behind a
  family index. Both families registered (partitioned, bounded per part).
  Verification: `2026-10-06` — the Verification Log below.
  Commit: `SEMULITH-LC-0003`
  `promotion: declined (the census lesson — a verbatim-move check that reuses the mover's own row filter cannot see what the filter drops — is the existing card a-survey-that-found-things-can-still-have-missed-things.md in another costume).`

- ID: `LIVE-CONTAINMENT.4` — **adopt the live-document containment doctrine**
  Status: `active`
  Goal: the guide's Phase 2 (`/Volumes/SSD/Documents/github/fsmgen/docs/LIVE_DOCUMENT_SIZE_CONTAINMENT_ADOPTION_GUIDE.md`,
  read-only external policy reference; the doctrine 32,730 B): a project-owned
  `LIVE_DOCUMENT_SIZE_CONTAINMENT.md`, this repository's own inventory and classifications
  reconciled with `doctrine/readme_routes.tsv`, and the checker contract wired — or an
  explicit deferral with its trigger, recorded.
  Acceptance: the guide's adoption checklist, project-owned and measured.
  Verification: pending
  Commit: pending

## Current Frontier

| Order | Leaf | Status | Why next |
| --- | --- | --- | --- |
| 1 | `LIVE-CONTAINMENT.4` | `pending` | D79 packets captured; causal analysis/D80/adoption scheduled alongside CPU delivery |

### .4o / SEMULITH-LC-0054 — the tree's closed rows move to an archive part (complete)

Owned on clean 11dae86. This file stands at about 127.6 KB of the task family's 131,072-byte per-part ceiling
(`decision_containment-reset.md`); its four row sections — the LC0027 checklist, the acceptance checklist, the
verification log and the commit log, all ticked rows of closed slices — measure about 43 KB. Apply the family's
standing mechanism, as P4-SYSTEM did at a42ar and a42ba: the four bodies move verbatim into
docs/tasks/archive/LIVE-CONTAINMENT-rows.md (one anchor each, every span's SHA256 listed in the part and found
once), each heading staying with one pointer; no seal, reader or inverse map; no unticked row may move.
Evidence target/live-containment/lc0054.

Done 2026-10-23 by target/live-containment/lc0054/move_closed_rows.py (move.log): the LC0027 checklist (153 B,
`4eafaa0d…`), the acceptance checklist (16,695 B, `6b43dcc1…`), the verification log (18,547 B, `95b491e1…`)
and the commit log (7,212 B, `32863f7a…`) moved verbatim — the script refuses an unticked row, asserts each
span occurs once and replaces exactly once, then finds each span byte-identical in the part with its listed
digest; this file 128,385 → 86,120 B (0.66× of the per-part ceiling), the part 44,208 B. Each heading keeps
`Closed rows: [retained verbatim](archive/LIVE-CONTAINMENT-rows.md#<anchor>)`; later rows append below it.
Checks (checks.log): DOCPATH, TREE-CLAIMS, FRONTIER-SYNC (35 trees), README-ROUTING-CLOSURE, TASK-HISTORY-LINKS,
SEAM-INTEGRITY (1,397 current acceptance boxes match), BOOK-INDEX, CLEANUP-TASK-HISTORY rc 0; focused checks
rc 0. No code changed. Commit: SEMULITH-LC-0054.

### .4n / SEMULITH-LC-0053 — LIVE_STATUS rows back to states (complete)

Owned on clean 267fc77. LIVE_STATUS.md stands at 6,137 of its 6,144-byte ceiling (registry row
`LIVE_STATUS.md`: hot_live, health 45 lines / 4,096 B, ceiling 90 / 6,144, owner "COMMIT.md; rows are
states, not prose"), 49 lines, health passed long ago; the next status note any unit writes crosses it.
Apply the row's declared control, not a raise: each Notes cell keeps the state, the tree pointer with its
leaf count, every caveat that limits a claim (`incomplete`, "declared not implemented", "cited not
verified", "uncredited", "unclaimed") and every count DERIVED-COUNTS and TREE-CLAIMS re-derive; narrative
history leaves the cell only where its tree record already carries it (each dropped phrase located by
grep in docs/tasks/ before the cut). The book's status chapter includes the file verbatim, so the
director's view changes with it. Evidence target/live-containment/lc0053.

Done 2026-10-23: 22 Notes cells cut to their states (LIVE_STATUS.before.md kept), 6,137 → 4,771 B, 49 lines
unchanged — 1,373 B of headroom under the ceiling, still above the 4,096-byte health target, so the
warning keeps printing; no ceiling moved. Kept in every cell: the tree pointer and leaf count, the
caveats (G0 `incomplete` with 68 checks unimplemented and "matched on the ISA, not the platform", 72
checks "declared not implemented", "cited not verified", "closure qualifies no processor/board", "no
oracle claim", "TI C6000 / SHARC unclaimed", "uncredited") and the three derived counts (40 registered,
1653 self-test arms, 49 chapters). Homes located before the cut (homes.log): D52–57 in this tree, the
mirror list in MIRROR-DRIFT, the 34 aligned steps in P1-LAB, boundary items "four in scope, six out" in
P0-PROFILE, "three G0 criteria are met" in P0-PROFILE, the extraction contract and `.18` in
MODEL-METHOD, criterion 6 / `c-scope.c` / 129/129 / 642/642 in P2-SCALAR and P1-LAB, TI/VLIW
slice-gating in P3-BREADTH, `.16` replay in P4-SYSTEM and the history shards, PLATFORM-GEN in P5-BOARD,
eADL in AG-OS; numbers that left the file (`diff` of the number sets): 129/129, 642/642, 52, 57, `.9`,
`.16`, `.18`, 4864 (now 4,864). Checks (checks.log): TREE-CLAIMS ok (5 live documents), DERIVED-COUNTS ok
(3 claims), README-ROUTING-CLOSURE ok, LIVE-DOC-CURRENCY ok, DOCPATH ok; focused checks with `make book`
rc 0. This tree's own file stands at about 128 KB of its 131,072-byte part ceiling: its closed records
move to an archive part next, as P4-SYSTEM's did (a42ba). Commit: SEMULITH-LC-0053.

### .4m / SEMULITH-LC-0052 — containment reset by director ruling (complete)

Owned on clean 2634e94. The family stood at 3,143,298 of 3,145,728 B (108 of 116 files), 2,430 B
of room, and docs/book/ at 524,247 of 524,288 B, so no unit record could land; slice (m) had been
scheduled as a second task-history seal. Raised as a blocker and discussed instead of built: the
director rejected the seal, ruled the book (and the unit books built by the same `make book`)
outside size containment, approved ungoverning the task family's aggregate and count with the
per-part 131,072 B kept, and accepted cutting per-unit duplication. Words and measurements:
docs/decisions/decision_containment-reset.md. Landed: the three registry rows (book and models
all 0; tasks 0 / 0 / 131072); the closed .4c–.4g records (10,610 B / 152 LF, SHA256
69e7147006e14f52e6a6f688d73d2862cea78d3f1c410ec88d1a13cb6c6941bf) moved verbatim into
docs/tasks/archive/LIVE-CONTAINMENT-adoption.md with their headings left as stubs, no inverse
map; COMMIT.md, DOCTRINE_ENFORCEMENT.md and docs/TASK_TREE_README.md say a unit is recorded once
(record + acceptance rows; the log sections below stop growing); the local adoption note, the
book's task-trees chapter and MEMORY.md carry the ruling; CHANGELOG.md and DEV_NOTES.md sharded.
Verification: routes rc=1 RED with this record and the part staged under the old row (OVER
CEILING docs/tasks/: 3,148,764 aggregate bytes > 3145728), rc=0 GREEN under the new rows at
3,148,757 B; self-test 94 pass / 0 fail; focused checks rc=0; seven books; `handoff: OK`.
Commit: SEMULITH-LC-0052. Evidence target/live-containment/lc0052. Next: P4-SYSTEM.14 a42ar,
after P4's closed records move into an ordinary archive part the same way.

### .4l / SEMULITH-LC-0051 — task-family count for retention continuation (complete)

Owned on clean a658e24. The family stood at 107/107 since 2026-10-12 (33+1+42+31), with
P4-SYSTEM.md, task-claims.md and reader-records-retention.md within 200 B of the per-part
ceiling and every terminal at its count, so neither P4.14 a42ap nor this tree could record
a unit. Cut the first complete-records continuation (task-claims-2.md) by retiring the whole
.4j record and acceptance (3,281 B, inverses exact) and re-derive the count 107 → 116 =
33+1+42+40 with its authority docs/decisions/decision_task-family-count-rederivation-retention.md;
health 64, bytes and per-part unchanged. Evidence target/live-containment/lc0051.
promotion: declined (the count precedents carry the rule). Next: P4.14 a42ap retires a42ao
through the continuation; slice (m) owns the aggregate seal (3,134,069 of 3,145,728 B).

### .4k / SEMULITH-LC-0050 — docs/decisions/ family capacity (complete)

Routed in `2026-10-20` by SEMULITH-AC-0077 (OVER CEILING docs/decisions/: 262242 > 262144
with one index row added). Measured at b70b2f5: 59 records, 26 landed 2026-10-02..12 and
none since while 113 B remained. Superseded partition (2 records, both in part), a second
terminal and duplicates were measured and rejected in the authority record, which lands
with the row: docs/decisions/decision_decisions-family-second-rederivation.md — both axes
2×, health 64 / 278,528, per-part fixed; the index is the next bite. Evidence
target/live-containment/lc0050. promotion: declined (the precedent record carries the
rule). Next: P4-SYSTEM retention capacity, then P4.14 a42ap.

### .4j / SEMULITH-LC-0049 — second finite history seal (verified; directly approved)

Closed record: [complete original record](artifacts/live-containment/task-claims-2.md#lc0051-4j-record).

### Delivery priority and capture handoff — P4-0249

Director's2026-10-18 stall/resumption questions trigger this priority review.
`git log -40 --format=%s` at cb39c69 lists only LC/AC subjects; CPU13/18 and
board10/12 remain unchanged, no MCU is registered, DSP subset has not expanded.
Own priority1 delivery-stagnation risk: maintenance became an open-ended serial
prerequisite. Count prerequisite is already complete; P4's .16 runtime state
contract does not depend on completing this containment graph or packet analysis.
After clean2a97c46/brief0/host0, P4-SYSTEM.16a/SEMULITH-P4-0249 owns the concrete
RV64GC snapshot/resume feature next. .14 evidence remains owned and open. Only
an actual correctness/review blocker interrupts the scoped feature; other defects
stay scheduled with owners. No quality/gate/history/locality rule is waived.

Terminal capture packet-20261017T225917Z-fbcd89 is complete:480observations,
155525packets/13015088B, all four owned ports,0unjudgeable; working-after saved.
PCAP SHA25657caa0279593d78a39727321bfcb1e523222e6ecf5d1363b03e05ff53152c844.
Only the pending Git parent was briefly SIGSTOP-held to preserve capture's
source/index/HEAD guard, then SIGCONT-resumed after the capture exited; AC0065
normal COMMIT and final host census passed. No rerun is needed. Packet access is
unblocked; LC0045/48 retain D79 analysis, LC0046 D80, .4i full adoption. Captured
packets/passing replays alone do not establish D79 cause or CPU acceptance.

## Approved task-history migration — .4c / SEMULITH-LC-0006

Closed unit: [complete original record](archive/LIVE-CONTAINMENT-adoption.md#approved-task-history-migration--4c--semulith-lc-0006).

## .4d / SEMULITH-LC-0007 — standalone temporary storage

Closed unit: [complete original record](archive/LIVE-CONTAINMENT-adoption.md#4d--semulith-lc-0007--standalone-temporary-storage).

## .4e / SEMULITH-LC-0008 — complete the book's temporary-control review surface

Closed unit: [complete original record](archive/LIVE-CONTAINMENT-adoption.md#4e--semulith-lc-0008--complete-the-books-temporary-control-review-surface).

## .4f / SEMULITH-LC-0009 — truthful orientation before inventory adoption

Closed unit: [complete original record](archive/LIVE-CONTAINMENT-adoption.md#4f--semulith-lc-0009--truthful-orientation-before-inventory-adoption).

## .4g / SEMULITH-LC-0010 — adopt the local neutral containment contract

Closed unit: [complete original record](archive/LIVE-CONTAINMENT-adoption.md#4g--semulith-lc-0010--adopt-the-local-neutral-containment-contract).

<a id="4h--revision-pinned-task-capacity-review-active"></a>

## .4h — revision-pinned task-capacity review (complete)

LC0015 fixed D51; LC0021 applied the separately reviewed count authority.
All eleven review/repair units below are complete. Their original planning
introduction is retained verbatim in reader-records-retention.md under
docs/tasks/artifacts/live-containment; the original incoming anchor above
remains available. Current full adoption is .4i, with count107/health64 debt
and every other bound unchanged.

### .4h1 / SEMULITH-LC-0011 — contain duplicated decision-index summaries

Closed unit: [complete original record](archive/LIVE-CONTAINMENT.md#4h1--semulith-lc-0011--contain-duplicated-decision-index-summaries).

### .4h2 / SEMULITH-LC-0012 — qualify capacity inputs before authority review

Closed unit: [complete original record](archive/LIVE-CONTAINMENT.md#4h2--semulith-lc-0012--qualify-capacity-inputs-before-authority-review).

### .4h3 / SEMULITH-LC-0013 — refuse unmeasurable family inventories

Closed unit: [complete original record](archive/LIVE-CONTAINMENT.md#4h3--semulith-lc-0013--refuse-unmeasurable-family-inventories).

### .4h4 / SEMULITH-LC-0014 — qualify the remaining route-checker reads

Closed unit: [complete original record](archive/LIVE-CONTAINMENT.md#4h4--semulith-lc-0014--qualify-the-remaining-route-checker-reads).

### .4h5 / SEMULITH-LC-0015 — correct the retained count receipt's classification

Closed unit: [complete original record](archive/LIVE-CONTAINMENT.md#4h5--semulith-lc-0015--correct-the-retained-count-receipts-classification).

### .4h6a / SEMULITH-LC-0016 — contain navigation before capacity authority

Closed unit: [complete original record](archive/LIVE-CONTAINMENT.md#4h6a--semulith-lc-0016--contain-navigation-before-capacity-authority).

### .4h6b / SEMULITH-LC-0017 — correct the five-unit composition receipt

Closed unit: [complete original record](archive/LIVE-CONTAINMENT.md#4h6b--semulith-lc-0017--correct-the-five-unit-composition-receipt).

### .4h6c1 / SEMULITH-LC-0018 — qualify remaining registry projections

Closed unit: [complete original record](archive/LIVE-CONTAINMENT.md#4h6c1--semulith-lc-0018--qualify-remaining-registry-projections).

### .4h6c2 / SEMULITH-LC-0019 — refuse unavailable registry projections

Closed unit: [complete original record](archive/LIVE-CONTAINMENT.md#4h6c2--semulith-lc-0019--refuse-unavailable-registry-projections).

### .4h6c3 / SEMULITH-LC-0020 — review separate task-count authority

Closed unit: [complete original record](archive/LIVE-CONTAINMENT.md#4h6c3--semulith-lc-0020--review-separate-task-count-authority).

### .4h6c4 / SEMULITH-LC-0021 — apply reviewed count authority

Closed unit: [complete original record](archive/LIVE-CONTAINMENT.md#4h6c4--semulith-lc-0021--apply-reviewed-count-authority).

### .4i — complete containment adoption (active)

Count prerequisite is complete at3615547; full adoption is not. Follow the
locally owned contract's checklist with separately committed children:
.4i1 local inventory/integration contract and closed source inputs;
.4i2 complete transitive surface/reader/author/terminal graph;
.4i3 utility, consumers, canonical authority and lifecycle decisions;
.4i4 explicit derived-state fields, reviewed survivors/limits and transition debt;
.4i5 local neutral-checker qualification and revision-aware adapters;
.4i6 unconditional resulting-tree integration with fail-closed coverage;
.4i7 independently owned atomic migrations for measured debt;
.4i8 complete coverage/retrieval/pressure/field truth and adoption signoff.
Do not combine unrelated families or classify by file age/number-shaped prose.
Do not change direct browsing or delete unique material without the required
review/retention authority. Existing guards stay unconditional during adoption.

### .4i1 / SEMULITH-LC-0022 — qualify inventory inputs and local contract

Closed record: [complete original record](archive/LIVE-CONTAINMENT-readers.md#4i1--semulith-lc-0022--qualify-inventory-inputs-and-local-contract).

### .4i2 — complete graph inventory (active, decomposed)

Follow inventory-contract.md's discovery procedure in independently committed
children: .4i2a closed source/member/include and actual rendered-link evidence;
.4i2b transitive index/query/generated expansion and reader-candidate review;
.4i2c emitted author-route census through isolated public failure cases;
.4i2d terminal/exclusion/overlap reconciliation and omission qualification.
No child alone claims complete semantic coverage. Keep unresolved candidates
explicit until actual consumers are reviewed; utility/lifecycle decisions stay .4i3.
While capturing author hints, .4i2c also qualifies public enforcer source-read
preconditions, including DERIVED-COUNTS registry projections; do not infer a
direct-call contract from sibling registration order. This is a pending
assessment, not a measured defect verdict.

### .4i2b3 — include-reader qualification (complete scoped reader repair)

Immutable input: cad73f376766572119490b157a98b69ce5ad04f7. LC0028 owned
this child on clean cad73f3 after normal hooks, exact13-file postcheck,
brief0 and unrestricted host0. Collection begins with only owned task/pointer
changes; every executed source/target matches immutable source. Separate
.4i2b4 owns index/query expansion, .4i2b5 generated-navigation/resource review;
.4i2c author hints and .4i2d terminal/exclusion/overlap closure remain open.
No child alone claims semantic graph coverage, utility/lifecycle authority or
full adoption. Caps, archives, Gitlink boundary and CPU/MCU/DSP/board stay fixed.

#### .4i2b3a / SEMULITH-LC-0028 — qualify actual readers and source-validity gap

Closed record: [complete original record](archive/LIVE-CONTAINMENT-readers.md#4i2b3a--semulith-lc-0028--qualify-actual-readers-and-source-validity-gap).

#### .4i2b3b — priority1 D65 include source/selection repair (complete)

Status: complete scoped repair at LC0030; owned by LIVE-CONTAINMENT.4. LC0028 commit
b6a21234d47bc1423883c4dc4425bfe42b6df632 passed normal hooks, exact8-file
postcheck, brief0 and unrestricted host0 before activation. LC0029 qualifies
the reusable source validator; LC0030 integrates/qualifies the actual guard.
D65 is fixed by LC0030 actual public/default verification below. Review actual chapter input
and existing book/registry/preprocessor contracts; use public mdbook protocol/
CLI only. Qualify project-owned source/selection validity, positive whole/
anchor/range/fenced/nested behavior, missing/duplicate selectors, unavailable/
unsafe sources and actual predicate omissions normal/O. Preserve old controls,
current seven-book content, source ownership, all caps and archive contracts.
Only after verified repair may .4i2b3 source-validity signoff close and wider
index/query/generated reader review resume. Full adoption stays .4i3–8.

##### .4i2b3b1 / SEMULITH-LC-0029 — qualify before-links include validation

Closed record: [complete original record](archive/LIVE-CONTAINMENT-readers.md#4i2b3b1--semulith-lc-0029--qualify-before-links-include-validation).

##### .4i2b3b2 / SEMULITH-LC-0030 — integrate and close D65

Closed record: [complete original record](archive/LIVE-CONTAINMENT-readers.md#4i2b3b2--semulith-lc-0030--integrate-and-close-d65).

### .4i2b4 — index/query expansion (active, decomposed)

Retain completed records first (.4i2b4a/LC0031); qualify index/query consumers
next (.4i2b4b/LC0032). Generated/resources .4i2b5 and full .4i3–8 remain open.

#### .4i2b4a / SEMULITH-LC-0031 — retain complete closed reader records

Owned on clean4e99991 after normal hooks/exact27-file postcheck/brief0/host0.
Root129969/131072B leaves1103B. Before new query work, copy nine complete closed
LC0022–30 units into new ordinary docs/tasks/archive/LIVE-CONTAINMENT-readers.md;
retain original heading/anchor stubs, ordering, every source byte and full root
inverse. Own docs/tasks/artifacts/live-containment/reader-records-retention.md,
new native before/after heading/link consumers, literal read and book route.
Qualify D70 correction scope case-insensitively; preserve old counts with an
explicit source-pinned addendum. D71: the parent .4h heading/plan still says
active/D51 pending despite LC0015/21 closure. Own a source-pinned full planning
copy, current closure text and preservation of its native incoming anchor. Keep every older archive/seal/mode, all caps,
whole old CH/DEV entries and source identities exact. Run focused/books/rendered/
literal/inverse checks and normal COMMIT; then .4i2b4b. Outputs under
 target/live-containment/reader-records-retention. Own tracked
scripts/qualify_reader_record_retention.py and its toolbox discovery row: replay
retained maps/full source/native consumers and deliberate corruption controls.
Existing guard, CPU and adoption behavior stays unchanged; qualify the producer
before normal COMMIT.

Verified LC0031 result (`2026-10-12`): nine complete LC0022–30 units and the
complete LC0027 checklist retained as ten source-ordered spans61745B/869LF,
SHAb35de12b250dab9e18c10bad92687b230652009663518cf285a2f22db142f7f5.
New ordinary archive63161B/SHA30c2d38cc48b54282b639aca630799073ec31f69dd689bc47b6e8fb5b85342cc
copied/authenticated before retirement; all ten original native headings/anchors
route to complete records. Both archived articles remain whole-byte exact;
only actual generated search-resource identities vary. The one raw ]( token
belongs to explanatory prose, not a link. No include/reference/HTML candidates
in those spans. Root130572→71073B at retirement, before owned closure receipts.
Current complete source inverse/offsets/native results and all controls:
docs/tasks/artifacts/live-containment/reader-records-retention.md.

D71 fixed: .4h is complete, D51 closedLC0015/count authority appliedLC0021.
Its full965B historical intro is retained, with its original native incoming
anchor preserved. Restore/copy-verify/reapply corrected the initial planning
copy order. D70 scoped addendum: immutable-source case-insensitive census finds
seven historical claims plus one correction mention, including two capitals
missed by the old lowercase count. Original receipts remain exact; subset5,
full handoff24 both qualify normal/O. No runtime or milestone count changes.

- [x] **ROOT CAUSE** — `python3 target/live-containment/reader-records-retention/assess.py` rc=0 pins source4e99991/1438 identities and root129969/131072B; ten whole spans and D70 eight occurrences. Native before render derives exact IDs; .4h capture contradicts completed LC0015/21 records.
- [x] **ADDRESSED** — `python3 scripts/qualify_reader_record_retention.py --working --output target/live-containment/reader-records-retention/reproduce` rc=0: ten original native targets/direct links plus the original phase anchor; both complete archived articles/whole HTML except authenticated search references agree. Whole root/phase/book/source inverses and changed/missing payload controls qualify normal/O; D71 fixed, D70 correction complete.
- [x] **NO REGRESSION** — `bash target/live-containment/reader-records-retention/focused.sh` rc=0: focused12/sharder12/seven books, scaffold5/full handoff24 normal/O. Whole105 prior CH/DEV entries/order/source and older published archives/seals/modes remain exact; receipt mutations refuse jointly. Complete normal/print reader section and twelve literal reads pass before normal COMMIT.
- [x] **LOCKSTEP** — task/pointer/CH/DEV/book and canonical retention record align; LIVE1571/caps/CPU/MCU/DSP/board/full-adoption scope unchanged. promotion: declined (existing containment contract and concrete retained evidence own this transition).

#### .4i2b4b — qualify index/query expansion (active, decomposed)

Project-book index first (.4i2b4b1/LC0032); orientation/record indexes next
(.4i2b4b2), then catalogue/archive queries and reconciliation (.4i2b4b3).
Generated navigation/resources remain .4i2b5; full graph/adoption stays open.

##### .4i2b4b1 / SEMULITH-LC-0032 — qualify the project-book index consumer

Owned on clean32f9c31 after normal hooks/exact12-file postcheck/brief0/host0.
Pin all1443 immutable identities and actual HEAD/index/working inputs. Discover
only through the owned Git tree; Gitlinks remain opaque. An earlier broad
filename search listed Gitlink paths; no implementation content or inferred
assumption is consumed. All following discovery excludes that boundary.
Own scripts/qualify_book_index.py, its toolbox row and the canonical record
 docs/tasks/artifacts/live-containment/book-index-consumer.md. Execute both
public project index interfaces in isolated repository-volume fixtures normal/O;
observe exact source reads, terms, chapter membership/order, exclusions and
output. Qualify missing/changed/invalid inputs, independent membership and real
omissions before repairs; record every observed defect with a scheduled owner.
No existing generator/guard behavior change in this assessment unit. Preserve
all older receipts/archives/modes, full CH/DEV entries and fixed caps; teach the
actual index scope in the mdBook. Outputs: target/live-containment/book-index-consumer.
D72 candidate: BOOK-APPARATUS metadata says done while its root task entry says
active and .1 commit says pending. Reconcile with canonical records and tools in
.4i2b4b2 before classifying or correcting; no historical receipt is rewritten.

D73 verified normal (`2026-10-12`): actual source read failure produces traceback/
exit1 in both public interfaces; invalid UTF-8 also gives generator traceback1.
The generator promises unsupported/unjudgeable inputs refuse2; the wrapper
classifies a real failed read as index drift1. Missing-source cases do refuse2.
Reproduce: python3 scripts/qualify_book_index.py --output target/live-containment/book-index-consumer/reproduce.
Exit0 means measurement complete; inspect observations, not a green safety claim.
Root cause: uncaught Path.read_text errors in gen_book_index.py; the shell's
actual generator failure branch rewrites all nonzero results to1. Priority1;
owner .4i2b4b1r/LC0033 repairs and verifies these boundaries immediately after
this assessment COMMIT, before other query readers. Qualification producer
also owns actual-read digest/omission controls and a working-code replay mode.

Verified LC0032 assessment (`2026-10-12`): all1443 source identities pinned,
54 fixture inputs; independent declaration/term expansion reproduces all49
chapters/40 terms and53 actual source reads in exact order with full content
identities. Both public baselines pass. The index scans raw source chapters,
not expanded includes; glossary/index discussion occurrences are deliberately
excluded. Complete memberships, terms/aliases/hits, source pins and child
verdicts: docs/tasks/artifacts/live-containment/book-index-consumer.md.

Normal/O and actual-working-code replay agree. Twelve input cases across both
public interfaces produce24 observations per mode. Five real read classes
(SUMMARY/chapter/canonical glossary/acronyms/generated index) plus two invalid
UTF-8 generator cases expose12 D73 verdict defects per mode. Every injected
read fault fires exactly once. Three real copied generator omissions (chapter,
term, discussions) return drift1; omitted-read and forged-read-digest ledger
controls refuse2. No actual source/index/mode changes; Gitlinks stay opaque.

- [x] **ROOT CAUSE** — `python3 scripts/qualify_book_index.py --output target/live-containment/book-index-consumer/final-normal` rc=0 measures12 original D73 child failures with traceback1; exact stack reaches Path.read_text and wrapper's failure branch. Exit0 marks completed measurement, not absence of defects. D73 priority1 repair is owned immediately next.
- [x] **ADDRESSED** — tracked producer normal/O and `--working-code` rc=0 reproduce49 chapters/40 terms/53 full actual reads,54 input pins,24 observations, three real omissions and two independent ledger refusals per mode. Complete retained source/consumer record and replay commands are canonical; existing generator/guard semantics are unchanged.
- [x] **NO REGRESSION** — `bash target/live-containment/book-index-consumer/focused.sh` rc=0: focused12/sharder12/seven books; original six BOOK-INDEX controls normal/O, whole normal/print teaching and literal tracked replay also pass. Whole old CH/DEV entries/order, every older archive/seal and protected source modes/Gitlink remain exact; staged full inverse and normal COMMIT are required before LC0033.
- [x] **LOCKSTEP** — task/pointer/CH/DEV/book/toolbox and canonical record align; LIVE1571, all caps, CPU/MCU/DSP/board and full graph/adoption scope unchanged. promotion: declined (existing inventory contract and source-pinned consumer evidence own this assessment).

##### .4i2b4b1r / SEMULITH-LC-0033 — repair D73 public index refusal

Owned on clean6bd4618 after normal hooks/exact11-file postcheck/brief0/host0.
Own gen_book_index.py's complete input/output exception boundary and
check_book_index.sh's actual verdict branch: preserve valid output and drift1,
refuse unjudgeable input2, retain all original six controls. Extend tracked
qualify_book_index.py with a clean-verdict selector, actual read/write/launch
failures and copied real omissions, normal/O. Own relevant toolbox, doctrine
registry/mirrors/LIVE derived arm count and book teaching. Append complete
source-pinned repair evidence to book-index-consumer.md without changing any
published prefix byte; own full root/book/source/history inverses and exact
modes. No new task artifact or cap, processor/MCU/DSP/board qualification or
full graph/adoption change. Outputs: target/live-containment/book-index-refusal.
D73 is priority1; close it before other index/query consumers .4i2b4b2–3.

Verified LC0033 (`2026-10-12`): D73 fixed. Generator's complete generate/compare
boundary catches named Refusal/OSError/UnicodeError and returns2 without a
traceback. The actual wrapper accepts only named drift1; failed/unknown launches
and typed input refusal retain2. Valid bytes, public arguments and all original
six controls remain exact. Four new verdict controls pass: ten total normal/O;
fresh DERIVED-COUNTS enumerates1575 arms,39 doctrines/49 chapters/39 routes.

Expanded tracked actual-interface probe:16 input cases/28 observations per
mode. Five actual read classes, one output write and three failed-launch
statuses each inject exactly once; invalid source UTF-8 is named refusal2.
Before:16 defective outcomes per mode and clean-verdict selector exits1;
after:0 defects, exits0, both valid baselines/index bytes and full49/40/53
source expansion agree. Real copied I/O/Unicode/wrapper refusal omissions
exit1 normal/O (11/2/8 defective outcomes); original three generator omissions
still drift1 and two corrupted ledger controls refuse2. No source/index/mode
mutation. Complete source-pinned repair capture appends to the LC0032 record;
its published64688B prefix and all older archives/seals stay exact.
Default historical population24/12 is retained normal/O; explicit extended
source replay gives28/16, current working-code replay28/0. During preparation
new cases changed the default population; restore its legacy boundary before publication.

- [x] **ROOT CAUSE** — `python3 scripts/qualify_book_index.py --working-code --require-clean --output target/live-containment/book-index-refusal/before-normal` rc=1: original16 wrong child outcomes; actual read/write/launch fault counts each1. Stack/branch evidence pins uncaught I/O/Unicode and lost actual generator verdict; source6bd4618.
- [x] **ADDRESSED** — the same tracked working-code clean-verdict probe at after-normal/after-optimized rc=0: all28 observations expected,0 D73 defects, valid49 chapters/40 terms/53 full reads/index bytes exact. Three copied real refusal omissions each rc=1 normal/O; original three omissions and two ledger controls retain their named failures. D73 closed.
- [x] **NO REGRESSION** — `bash target/live-containment/book-index-refusal/focused.sh` rc=0: focused12/sharder12/seven books; original six plus four new index controls normal/O. Full source/history/mode/cap inverses, whole normal/print teaching and literal clean replay pass; staged inverse and normal COMMIT required before next consumer.
- [x] **LOCKSTEP** — current doctrine/registry/toolbox/book/task/CH/DEV/pointer align; LIVE changes only derived arm count1571→1575. No cap, processor/MCU/DSP/board or full graph/adoption qualification. promotion: declined (existing source-pinned consumer contract and its appended repair evidence own the lesson).

##### .4i2b4b2 / SEMULITH-LC-0034 — qualify orientation and record indexes

Qualify actual Knowledge Map and decision/knowledge/task index members,
exclusions, failed inputs and independent omissions; reconcile D72 first.

Owned on clean50a102b after exact16-file postcheck/brief0/host0. Pin the
owned Git tree; keep Gitlinks opaque. Own scripts/qualify_orientation_indexes.py
and one canonical artifact orientation-indexes.md (task-family slot107/107),
its toolbox route and bounded book teaching. Measure actual map generator/guard
and MEMORY-ARCH through isolated on-volume copies, normal/O; independently
reconcile task/decision/knowledge inventories, exclusions and links. Inject
actual reader/tool failures and omit real members; record source-pinned verdicts
and schedule every defect. Reconcile both BOOK-APPARATUS commits before D72
current-field corrections, retaining its whole original file first. No other
consumer repair in this assessment unit; repair follows COMMIT if needed.
Preserve published receipts, old live history, modes and fixed caps; no processor
qualification or full graph/adoption claim. Outputs: target/live-containment/orientation-indexes.

Verified LC0034 (`2026-10-12`):207 immutable inputs from all1448 source identities;
independent33 task/59 decision/29 knowledge memberships and complete map bytes
agree. All Markdown rosters have exact owned destinations; nested task records,
templates and index files are explicitly excluded from map membership. Three
actual generator omissions and three independent roster omissions refuse2,
normal/O. Seventeen public observations agree completely except mode;11 wrong
source verdicts. Real faults execute exactly1 sed/2 ls/2 sort/59 grep calls;
a failed actual generator emits exact map then exits42 once, guard wrongly0.

D72 FIXED: `git log -- docs/tasks/BOOK-APPARATUS.md` identifies BA0001 fd4ca402
and BA0002 48b37729 only. Read both whole commit messages/stat and relevant tree
deltas: metadata/.2 closed at BA0002, root active and .1 pending stayed stale.
Copy/authenticate complete21612B original before correcting those two current
fields; historical logs/receipts and every other byte stay exact.
D74 priority1: generator hides missing curated input and failed sed/ls/sort;
checker loses generator exit status (9 wrong outcomes). D75 priority1: comment-only
decision filename passes and failed grep42 becomes breach1 (2 wrong outcomes).
Both owned/scheduled .4i2b4b2r/LC0035 immediately after this COMMIT. No other
reader repair in the assessment; cap107 is unchanged, last pooled slot used.

- [x] **ROOT CAUSE** — `python3 scripts/qualify_orientation_indexes.py --require-clean --output target/live-containment/orientation-indexes/final-normal` rc=1:17 actual observations/11 wrong verdicts,207 source pins and33/59/29 memberships; actual shell/tool failures locate D74 process-status loss and D75 substring matching. Complete capture: artifacts/live-containment/orientation-indexes.md.
- [x] **ADDRESSED** — the same producer under `python3 -O` at final-optimized rc=1 reproduces all17 observations exactly; three real generator omissions and three roster omissions refuse2. Whole21612B D72 source retained/authenticated before two corrected current fields; original histories stay exact. D74/D75 explicitly remain open with immediate LC0035 repair, no healthy-reader claim.
- [x] **NO REGRESSION** — `bash target/live-containment/orientation-indexes/focused.sh` rc=0: focused12/sharder12/seven books, scaffold5/full handoff24 normal/O. Complete old live history/order and protected identities/modes/Gitlink, fixed caps and source inverses pass; normal/print whole teaching, literal historical/current commands and fresh links verified before normal COMMIT.
- [x] **LOCKSTEP** — task/CH/DEV/pointer/toolbox/book and canonical capture align. LIVE1575 and CPU/MCU/DSP/board/full graph/adoption scope unchanged. promotion: declined (source-pinned consumer record owns this finite qualification and scheduled repairs).

##### .4i2b4b2r / SEMULITH-LC-0035 — repair D74/D75 orientation and record readers

Repair named missing/unreadable map sources, tool/discovery failures and actual
generator status propagation; reject comment-only decision listings, refuse
unavailable index evidence. Preserve complete valid map and memberships, original
LC0034 capture, old controls/caps/seals. Working-code actual interface matrix must
be healthy normal/O, and real copied refusal/membership omissions must discriminate.
Continue catalogue/archive queries .4i2b4b3 only after this normal COMMIT.

Owned on cleand0943de after exact12-file postcheck/brief0/host0. Own complete
map generation/guard failure boundaries, MEMORY-ARCH decision row/read checks,
tracked working-code qualification and real omissions. Preserve valid map bytes,
all207 historical inputs/17 observations and the complete LC0034 artifact prefix.
Reuse its canonical artifact within131072B; no new task-family member or cap.
Own scaffold retention of these three repairs, actual public sync probes and
normal/O failure controls; update all affected mirrors/book/live counts if needed.
Map/record failure status and membership are the finite acceptance, not full
Markdown/adoption/graph/processor authority. Outputs: target/live-containment/orientation-repair.

Verified LC0035 (`2026-10-12`): D74/D75 FIXED. Complete map stdout is emitted
only after checked curated read, regular inventory discovery/sort and output.
Actual guard captures/checks generator status before diff; unavailable inputs/
comparisons refuse2, missing/drifted map remains1. MEMORY-ARCH reads UTF-8 with
checked I/O, removes HTML comments/fenced examples, quotes literal filename
regex data, requires anchored table links and distinguishes no-match1/refusal2.
Valid complete map bytes and33/59/29 source memberships remain exact.

Original legacy17 observations/11 wrong verdicts replay all fields exactly;
extended immutable21/14 qualifies prose/commented/fenced decisions and valid
one-line comments. Current22/0 normal/O includes actual normalization-tool
failure. Every current injected tool fault/failed generator main fires once.
Real copied map/guard/row omission probes fail1 with2/5/1 wrong outcomes per
mode; three real map expansions and three independent roster omissions still
refuse2 in every scenario. Five full normal/O scenarios reconstruct losslessly
from the unchanged published109161B LC0034 record prefix and compact deltas.

Scaffold retains all three repairs. Seven subset/26 full public tests normal/O
preserve all five original methods and add two stale/different-source controls.
Individually restoring each reader to the updater overwrite list makes both
new cases fail:7 tests/2 failures/0 errors normal/O. No upstream-state claim.
Fresh DERIVED-COUNTS keeps1575 shell arms; Python method count is separate.
All caps/old archives/seals/current historical captures remain exact.

- [x] **ROOT CAUSE** — `python3 scripts/qualify_orientation_indexes.py --extended --require-clean --output target/live-containment/orientation-repair/before-final-normal` rc=1:21 observations/14 wrong outcomes, reproduced normal/O. Actual missing/tool inputs and generator42 status locate D74; prose/comment/fence cases locate D75's substring reader.
- [x] **ADDRESSED** — `python3 scripts/qualify_orientation_indexes.py --working-code --require-clean --output target/live-containment/orientation-repair/after-final-normal` rc=0:22 observations/0 wrong outcomes normal/O, exact complete map and memberships. Three real repair omissions fail1 (2/5/1 wrong outcomes); three map/three roster controls discriminate. D74/D75 closed; original legacy fields and full prefix stay exact.
- [x] **NO REGRESSION** — `bash target/live-containment/orientation-repair/focused.sh` rc=0: focused12/sharder12/seven books, scaffold7/full handoff26 normal/O. Individual updater omissions fail1, seven tests/two failures each. Whole old history/protected modes/Gitlink, source inverses, fixed caps, normal/print teaching/literal commands and fresh navigation qualify before normal COMMIT.
- [x] **LOCKSTEP** — task/pointer/CH/DEV/book/toolbox/capture and public sync align; LIVE1575/CPU/MCU/DSP/board/full graph/adoption unchanged. promotion: declined (source-pinned consumer record owns the repaired boundary and finite retained controls).

##### .4i2b4b3 / SEMULITH-LC-0036 — qualify catalogue/archive queries (complete)

Reconcile actual catalogue/archive query expansion, output membership/exclusions,
failed inputs and real omissions against independently pinned owned sources.
Keep published prefixes/caps/seals exact; reuse a suitable existing canonical
artifact, never add a108th task-family file. Generated navigation stays .4i2b5;
full graph/adoption remains open. Qualify before making any additional repair.

Owned on clean23fdb8a after exact16-file postcheck/brief0/host0. Pin all1454
owned source identities, keeping Gitlinks opaque. Own scripts/qualify_query_consumers.py
and an append-only LC0036 phase in artifacts/live-containment/graph-census.md;
retain/authenticate its whole published prefix and old live book explanation
before updates. No108th task-family file or cap/seal extension. Qualify the
actual record_catalog.py, history_archive.py and task_history_archive.py CLIs
in isolated same-volume fixtures normal/O: all six root catalogues/two parts,
all210 sealed shards/twelve P4 originals, full source/member/order/byte/trace
reconciliation, exclusions, failed/corrupt reads and real consumer omissions.
Public named refusal1 is preserved as these existing interfaces specify; the
inventory adapter's cannot-judge2 is separate. Record/schedule every actual
defect before repair; no existing consumer behavior change in this assessment.
Update relevant toolbox/live/book records; prove complete old source/history/
modes/prefixes and fixed limits. Outputs: target/live-containment/query-consumers.

D76 verified source23fdb8a: an invalid gzip deflate block with correctly updated
outer object identity produces zlib.error/traceback1 instead of the public named
refusal1. No original bytes are emitted. Reproduce with tracked producer:
`python3 scripts/qualify_query_consumers.py --require-clean --output target/query-deflate`
returns1; result.json and invalid-deflate stderr capture the actual refusal failure.
Root cause: history_archive.py load_archives catches OSError/EOFError/TarError
around decompression but omits zlib.error; main also leaves it uncaught. Priority1,
owner .4i2b4b3r / LC0037, immediate after this qualification COMMIT, before .4i2b5.
Deep JSON2048 was measured as named refusal1, so no JSON defect is classified.


Verified LC0036 (2026-10-12): source23fdb8a/1454 immutable identities;30 selected
pins; all six roots/two parts,210 history/twelve P4 originals exact normal/O.
All263 actual outcomes/complete byte traces reconciled. One source defect D76;
--require-clean1 in both modes, no successful-signoff claim. Three actual
consumer omissions give child0/qualification1; seven independent ledger
corruptions refuse2. Public commands in no-.git fixtures make zero Git calls.
Complete ordered normal/O captures reconstruct losslessly from graph-census's
append, whose whole5135B published prefix and old book section are retained.
No existing consumer, archive, historical record, capacity or acceptance changes.

- [x] **ROOT CAUSE** — `python3 scripts/qualify_query_consumers.py --require-clean --output target/live-containment/query-consumers/final-normal` (with owned `--addition scripts/qualify_query_consumers.py` before tracking) rc=1:263 observations, D76 only. Trace and invalid gzip/outer identity prove actual uncaught zlib.error; current code never catches it.
- [x] **ADDRESSED** — `python3 scripts/qualify_query_consumers.py --output target/query-replay` rc=0: assessment complete; all222 originals and six full expansions match independent source/capture membership/order/bytes/modes. Actual read/exclusion/fault/forgery protocols and complete result fields retained; normal/O source-defect1 and all3+7 omission controls exact. D76 is explicitly owned for immediate repair, not closed here.
- [x] **NO REGRESSION** — `bash target/live-containment/query-consumers/focused.sh` rc=0: focused12/sharder12/seven books/scaffold7/full handoff26 normal/O. Whole source/history/prefix/inverse/mode/cap and rendered/literal checks qualify before normal COMMIT; no Rust change.
- [x] **LOCKSTEP** — pointer/task/CH/DEV/book/toolbox/capture align. LIVE1575/CPU/MCU/DSP/board and full graph/adoption remain unchanged. promotion: declined (bounded source-pinned consumer record owns this assessment).

##### .4i2b4b3r / SEMULITH-LC-0037 — repair D76 malformed gzip refusal (complete)

Immediately after LC0036 normal COMMIT, catch the verified zlib decompression
failure through the public history reader's named refusal1, no traceback/stdout.
Preserve valid sealed originals and all existing refusal contracts. Replay
the immutable LC0036 source263/1 fields unchanged; working-code normal/O must
be263/0. Add an actual catch omission proving the repaired boundary fails1.
Retain existing3 consumer/seven ledger controls and all archive controls;
append evidence to the same graph-census artifact without editing its prefix.
Update book/live docs and preserve full source/history/modes/seals/fixed caps.
Commit normally, exact postcheck/brief0/host0, then resume generated navigation
.4i2b5. No full graph/adoption or processor acceptance credit.

Owned on cleane2dad9a after normal hooks/exact11-file postcheck/brief0/host0.
Pin all1457 owned identities; Gitlink opaque. Own history_archive.py catch,
probe_history_archive.py public normal/O deflate regression and its permanent
SHARD-FREEZE arm; qualify actual catch removal through qualify_query_consumers.py.
Re-derive LIVE controls and relevant toolbox count; preserve all old controls.
Retain whole published graph-census prefix before an append-only repair capture,
all original immutable query fields apart from named runtime stderr path digests,
and every old source/history/mode. Update book/live guidance within fixed caps.
Outputs target/live-containment/query-repair; no archive or authority change.


Verified LC0037 (2026-10-12): D76 FIXED by catching zlib.error at actual gzip
decompression. Named HISTORY-ARCHIVE refusal1/no stdout/no traceback now holds.
All263 working observations are correct normal/O, all222 original outputs and
full source traces remain exact. Immutable source263/1 replays unchanged apart
from named fixture-path stderr digests. Three old consumer/seven ledger controls
remain; actual removal of just the new catch restores traceback1 and fails
qualification1. Whole published115053B prefix and old book seam retained.
New permanent public regression first fails2 before repair, SHARD-FREEZE43/1;
after repair exact stderr/exit1 checked normal/O, permanent44/0 in both modes.
Re-derived shell arms1576; LIVE changed only that current count.

- [x] **ROOT CAUSE** — `python3 scripts/probe_history_archive.py --mutation invalid-deflate` rc=2 before catch; `bash scripts/check_changelog_shards.sh --self-test` rc=1:43 pass/1 fail. Correctly updated outer identity reaches actual deflate decoding; omitted zlib.error causes public traceback1 rather than named refusal1.
- [x] **ADDRESSED** — `python3 scripts/qualify_query_consumers.py --working-code --require-clean --output target/live-containment/query-repair/working-normal` rc=0:263/0 normal/O; further actual catch omission fails1, traceback1/no stdout. Immutable source263/1 remains; original3+7 controls preserved. Public regression rc=1 named/no traceback normal/O; permanent44/0 rc=0 normal/O.
- [x] **NO REGRESSION** — `bash target/live-containment/query-repair/focused.sh` rc=0: focused12/sharder12/seven books/scaffold7/full handoff26 normal/O; complete legacy/current raw fields, old source/history/prefix/modes, staged inverse/fixed caps and normal/print/literal checks qualify before normal COMMIT. No Rust change.
- [x] **LOCKSTEP** — pointer/task/CH/DEV/book/toolbox/capture/LIVE1576 align. CPU/MCU/DSP/board, complete graph and adoption remain open. promotion: declined (existing source-pinned query record owns this repaired contract).

##### .4i2b5 — generated navigation/resources (active, decomposed)

After LC0037 normal COMMIT/exact postcheck/brief0/host0, pin a fresh source and
qualify actual generated navigation/resource expansion across seven registered
books. Reconcile complete source/output membership, reader routes, exclusions
and failures against independent evidence; execute real producer omissions.
Use only public mdBook commands and owned code/contracts; Gitlinks opaque.
Own defects and schedule verified repairs immediately when blocking. Retain
whole published prefixes/history/modes and fixed caps without a108th task file.
Select a suitable existing canonical artifact and teach actual scope in book.
Generated ignored bundles remain on volume and source identities must not move
during qualification. Author hints/reconciliation remain .4i2c/d; no complete
graph, utility, capacity, adoption or processor acceptance credit here.


###### .4i2b5a / SEMULITH-LC-0038 — qualify the actual navigation consumer (complete)

Owned on clean213f818 after normal hooks/exact15-file postcheck/brief0/host0.
Pin1459 owned identities; Gitlinks opaque. Decompose safe units: actual owned
book_navigation.py first here; generated TOC/search next .4i2b5b, then resource
routes .4i2b5c. Keep every generated resource candidate open until qualified.
Own scripts/qualify_book_navigation.py and an append-only navigation phase in
artifacts/live-containment/include-readers.md, preserving its whole17280B prefix.
No108th task file or cap/retention change. Execute the actual public navigation
preprocessor in isolated same-volume copies normal/O, capturing complete input
and output chapters after includes, and all fresh seven-book outputs. Reconcile
declared task/history/sibling rewrites and exclusions with independent rendered
evidence; preserve labels, examples and non-route content. Qualify actual
input/refusal contracts, original26 controls, and real copied-consumer omissions.
Log/schedule every verified defect before repairs; this unit assesses existing
behavior. Retain old book seam before teaching current scope; full source,
history, modes, prefixes and fixed caps must qualify before normal COMMIT.
Outputs target/live-containment/navigation-consumer; full graph/adoption open.

D77 verified source213f818: public book_navigation.py accepts depth20 of the
valid nested Chapter/sub_items shape (rc0), but depth1200 gives RecursionError/
traceback1 with zero stdout. Root cause is copy.deepcopy(book) in _preprocess,
before traversal; main catches ValueError/OSError/TypeError but not this runtime
depth failure. This is a named-refusal contract defect, not a generic Markdown
coverage claim. Captures target/live-containment/navigation-consumer/depth-*.stderr
retain the actual exception. Reproduction will be part of the tracked fresh-output
qualifier before this assessment closes. Priority1 owner .4i2b5ar / LC0039,
immediate after LC0038 normal COMMIT and before .4i2b5b generated TOC/search.


Verified LC0038 (2026-10-12): source213f818/1459 identities, all seven books/
93 full chapters/344 outputs. Capturing actual consumer leaves every byte
unchanged. Independent complete HTML transformation reconciles54 source/110
rendered rewrites in12 files and all3240 hyperlinks/exclusions normal/O.
Actual complete registry reads are pinned/traced, with no body-read claim for
task/history existence checks. Original26 controls and three actual public
consumer omissions discriminate. Sixteen public observations expose only D77;
--require-clean1 in both modes. Assessment complete, not reader signoff.
Whole17280B prefix/old book seam retained; inline bounded metadata encoding
retains complete rows/manifests/cases/trace/body fingerprints, with fresh pinned
source replay and explicit generated-diagnostic/non-archival boundaries.

- [x] **ROOT CAUSE** — `python3 scripts/qualify_book_navigation.py --require-clean --output target/live-containment/navigation-consumer/read-normal` (with owned `--addition scripts/qualify_book_navigation.py` before tracking) rc=1:16 observations/one D77 normal/O. Depth20 succeeds0; depth1200 deepcopy produces public traceback1/no stdout, not named refusal2.
- [x] **ADDRESSED** — `python3 scripts/qualify_book_navigation.py --output target/nav-replay` rc=0: assessment complete, all93 source chapters/344 outputs/54 source edits/110 rendered routes exact. Whole independent source/HTML/metadata agreement, complete canonical reads, original26 controls and three copied real omissions hold normal/O. D77 owned for immediate LC0039 repair, not closed here.
- [x] **NO REGRESSION** — `bash target/live-containment/navigation-consumer/focused.sh` rc=0: focused12/sharder12/seven books/scaffold7/full handoff26 normal/O. Complete source/history/prefix/book/inverse/modes/fixed caps and normal/print/literal teaching qualify before normal COMMIT. No Rust or existing consumer change.
- [x] **LOCKSTEP** — task/pointer/CH/DEV/book/toolbox/capture align; LIVE1576/CPU/MCU/DSP/board/full graph/adoption unchanged. promotion: declined (source-pinned navigation record owns this assessment).

###### .4i2b5ar / SEMULITH-LC-0039 — repair D77 navigation nesting refusal (complete)

Owned2026-10-16 from clean f608639 after AC0064 hooks, exact9-file postcheck,
brief0 and unrestricted host census0. Read the leaf requirements, actual
book_navigation.py API/CLI and all26 original probe methods, complete tracked
qualifier and current model-book teaching before code changes. All work and
scratch remain in this tree/target/live-containment/navigation-repair. Preserve
the complete LC0038 capture prefix and legacy16/1 while qualifying current16/0.

Immediately after LC0038 normal COMMIT/exact postcheck/brief0/host0, convert
the verified deepcopy depth failure into named navigation refusal2, zero
stdout/traceback, through the public API and CLI. Preserve all valid source/
rendered bytes and original26 component methods. Add permanent depth regression
coverage normal/O and an actual catch omission. Keep immutable source16/1
replay explicit; working-code assessment must be16/0 with all93 chapters/
344 outputs/54 source/110 rendered edits and original three route omissions.
Append repair evidence to the same artifact without changing its published
prefix. Update book/live/toolbox guidance, preserve whole history/source/modes/
caps and commit normally. Then continue generated TOC/search .4i2b5b, resources
.4i2b5c; no complete graph/adoption or processor acceptance credit.

Verified LC0039 (2026-10-16): D77 FIXED. Public preprocess catches the
observed RecursionError and raises NavigationRefused with a named depth reason;
main's existing refusal path emits2, zero stdout and no traceback. No invented
numeric depth limit or recursion-limit adjustment. Depth20 remains unchanged0.
The permanent test first records27tests/two CLI failures and one API error in
both parent modes; after repair27/0 normal/O, including explicit normal/-O
children with inherited PYTHONOPTIMIZE removed. All original26 method ASTs exact.

Working replay overlays only the authenticated consumer/probe bytes on the
same immutable1459-identity data copy. Original copy authenticates before
application; all original and three omission fixtures verify against explicit
working byte/mode expectations afterward. Legacy16/1 remains; current16/0 in
both modes, all93 chapters/344 outputs/54 source/110 rendered rewrites and
3240 hyperlinks/exclusions exact. All three route omissions remain actual.
Removing only the new catch restores public depth1200 traceback1/no stdout
and qualification1; the other15 cases remain correct. Complete four matrices
reconstruct losslessly from the published capture and explicit patches/added
fields. Retain the full106266B artifact prefix and complete old book seam.
Focused checks, seven books, normal/print/literal teaching, whole source/history/
mode/cap inverses and normal COMMIT qualify this repair. No LIVE1576, CPU,
MCU, DSP, board, complete graph or adoption acceptance change.

- [x] **ROOT CAUSE** — `python3 scripts/probe_book_navigation.py` rc=1 before repair normal/O:27 tests, failures2/errors1; new API/depth1200 public CLI reproduces deepcopy RecursionError. Original26 methods pass. Immutable qualifier --require-clean rc=1,16/1 normal/O.
- [x] **ADDRESSED** — `python3 scripts/qualify_book_navigation.py --working-code --require-clean --output target/live-containment/navigation-repair/working-normal` rc=0:16/0 normal/O; exact named depth refusal2/no stdout/traceback. Actual catch omission restores D77 and fails qualification1; old three route omissions discriminate. Permanent27/0 normal/O.
- [x] **NO REGRESSION** — focused.sh/verify.py/history.py/rendered/literal checks rc=0 normal/O where applicable:focused12/sharder12/seven books, complete93-chapter/344-output transformations, whole published prefix/book/history/source/modes/fixed caps and staged inverse exact. Normal COMMIT hooks/postcheck complete before LC0040. No Rust change.
- [x] **LOCKSTEP** — task/MEM/CH/DEV/book/toolbox/capture align; immutable source results remain explicit. promotion: declined (the source-pinned navigation record owns this depth contract).

###### .4i2b5b — generated TOC/search (active, decomposed)

After LC0039 normal COMMIT/exact postcheck/brief0/unrestricted host0, pin fresh
source/input identities and qualify actual public mdBook-generated navigation
and search across seven books. Reconcile complete chapter/output membership,
TOC hierarchy, search document membership/routes, canonical inputs, actual
exclusions and all untouched content through independent evidence. Use public
commands/contracts, never Gitlink or dependency implementation assumptions.
Execute actual supported producer/configuration omissions, retain raw complete
captures on volume and compact durable reconstruction metadata in an existing
owned artifact. Log/own/schedule every verified defect before repairing it.
Preserve published prefixes, whole history/source/modes and fixed capacities;
no108th task file. Keep resource routes .4i2b5c, author hints/reconciliation
.4i2c/d, full graph/adoption and processor qualification explicitly open.
Update current book teaching and complete the normal COMMIT workflow.

###### .4i2b5b1 / SEMULITH-LC-0040 — qualify chapter TOC data (complete)

Owned2026-10-16UTC from clean718bbd9 after LC0039 normal hooks, exact13-file
postcheck/brief0/unrestricted host0. Read inventory-contract .4i2, current
models chapter, complete include-source-integration record, registry/books/
SUMMARY inputs and owned capture/copy/path interfaces before changes. Pin the
fresh1466-identity source. Use public mdBook0.5.4 commands and generated data;
all Gitlinks opaque, other repositories read-only. Own the tracked producer
scripts/qualify_book_toc.py and target/live-containment/chapter-toc scratch.

Scope: independently reconstruct the seven SUMMARY chapter/part hierarchy,
paths, labels and numbering, reconcile captured full mdBook chapter metadata
and both generated chapter-contents representations (toc.html and toc JS data).
Authenticate complete immutable source copies before/after, canonical inputs,
all actual output membership/bytes and an unchanged capture baseline normal/O.
Qualify actual supported SUMMARY omissions/renaming/hierarchy changes against
the complete original contract; native producer success alone is insufficient.
Retain every candidate/row and name exclusions explicitly. Runtime per-page
heading insertion is .4i2b5b2; search is .4i2b5b3; resource loading is .4i2b5c.
Do not claim browser runtime, full graph/adoption or processor qualification.

Append a bounded complete reconstruction capture to existing canonical
artifacts/live-containment/include-source-integration.md, preserving its full
24876B published prefix. All fixed caps/count107 remain unchanged; keep the
whole old book teaching before compact current guidance. Preserve source,
history, modes and complete inverses; update MEM/CH/DEV/toolbox/book; focused
checks/seven books/rendered/literal commands and normal COMMIT close this unit.
Log and own any verified product defect before repair; no speculative fixes.
promotion: declined (source-pinned generated-navigation evidence owns the scope).

Verified TOC data/controls below pass normal/O. The capture API lacked its own
no-fetch guard (CLI had it): a proxy before its first Git read failed. source_manifest
now sets the flag; codec.py rc=0 verifies the guard normal/O.

- [x] **ROOT CAUSE** — `python3 scripts/qualify_book_toc.py --addition scripts/qualify_book_toc.py --require-clean --output target/live-containment/chapter-toc/prepare-normal` rc=0:source1466/107 pins, seven books/93 chapters/14 TOCs,0 wrong verdicts; prior navigation qualification left chapter TOC data open.
- [x] **ADDRESSED** — same qualifier normal/O rc=0:100 complete chapter/part rows match protocol and both generated forms;344 outputs capture-exact, three real SUMMARY controls build0/qualification1. codec.py rc=0 normal/O:complete inverse and six damaged-input refusals.
- [x] **NO REGRESSION** — focused.sh/history.py/verify.py/rendered.py rc=0 normal/O where applicable:focused12/sharder12/seven books; whole prior source/history/modes/book/prefix/cap and staged inverses exact; normal COMMIT required. No Rust/LIVE/processor/adoption change.
- [x] **LOCKSTEP** — task/MEM/CH/DEV/book/toolbox/capture align; heading/search/resources remain open. promotion: declined (source-pinned generated-navigation record owns the scope).

###### .4i2b5b1h / SEMULITH-LC-0041 — contain task-family byte pressure (complete)

[Complete record and standing archive delegation](artifacts/live-containment/task-claims.md#lc0049-lc0041).

###### .4i2b5b2 / SEMULITH-LC-0042 — qualify per-page heading navigation (complete)

Complete assessment: docs/tasks/artifacts/live-containment/include-source-integration.md,
phase LC0042. Immutable1226311/1477 identities:120 pages/1406 source headings/589
navigation entries; normal/O exposes only D78. Four execution witnesses, three
producer omissions/fallback cause and nine damaged-frame controls discriminate.
The whole closed task record, including calibration/ownership/acceptance evidence,
is retained byte-exact from5c72864 in the LC0043 phase of
docs/tasks/artifacts/live-containment/include-source-validator.md.
No processor/graph/adoption credit. D78 is priority1, immediate LC0043 below.

###### .4i2b5b2r / SEMULITH-LC-0043 — repair authored-index active context (complete)

D78 corrected:120 current page contracts/1408 headings/590 entries pass normal/O;
all six aliases, source bodies and full source/current metadata remain exact.
Three actual repair omissions/seven damaged frames discriminate. Complete
assessment/failed D79 witness: include-source-validator record phase LC0043.
Whole closed task record, including ownership/calibration/acceptance, is retained
fromf3c5e81 in docs/tasks/artifacts/live-containment/reader-records-retention.md,
LC0044 phase. D79 remains priority1, immediate owner below; concurrent-load,
resource completeness, full graph/adoption and processor acceptance stay open.

###### .4i2b5b2r.d / SEMULITH-LC-0044 — trace the missing Mark dependency (complete finite forensic slice)

Whole closed LC0044 forensic unit from4c14bf7, including its complete plan
and acceptance: docs/tasks/artifacts/live-containment/reader-records-retention.md,
LC0048 phase. D79 capture/analysis stays open below; D80 follows.

###### .4i2b5b2r.d2 / SEMULITH-LC-0045 — tool delivery retained; capture pending

Whole LC0045/47 unit from4c14bf7, including acceptance and app witness:
docs/tasks/artifacts/live-containment/reader-records-retention.md, LC0048 phase.

###### .4i2b5b2r.d2v / SEMULITH-LC-0048 — repair terminal mdBook selection (complete)

Owned clean4c14bf7 before code changes. User's222353 run refuses before sudo
with unreviewed mdBook version; early failure leaves no failure.json/version
stdout. Census: project/Homebrew0.5.4, user Cargo0.5.2; exact terminal resolution
was not recorded. Reproduce Cargo-first PATH, preserve strict frozen version
checks, select verified project-local0.5.4 through the existing installer and
retain setup/version/preparation failures. Own capture tool/tests, whole closed LC0044/45/47 units'
exact retention, book/MEM/CH/DEV sync and normal COMMIT; no global shell/tool
change. D79 stays priority1/open; D80 follows. LC0047 app disposition remains.
Artifact cleanup is due; execute its owned slice after this clean commit.

- [x] **ROOT CAUSE** — controlled Cargo-first `python3` version probe rc=0 records stdout0.5.2 and the frozen guard's exact refusal in target/live-containment/capture-version/before.json. Original222353 output has no sudo/capture directory; preparation precedes authentication and lay outside failure.json recording. Original terminal executable remains unknown; do not overclaim its identity.
- [x] **ADDRESSED** — `python3 scripts/capture_book_dependencies.py --self-test` normal/O rc=0:33controls/0fail/0privileged; preserve original24. Version/setup/missing/symlink faults refuse with retained diagnostics, early setup/compiler failures write failure.json. Cargo-first `python3 scripts/capture_book_dependencies.py --check-preparation` host rc=0, selected project0.5.4, immutable builds/WebKit/four closures, no sudo; output packet-20261017T223050Z-6ac03d.
- [x] **NO REGRESSION** — focused13/sharder12/seven books and target/live-containment/capture-version/verify.py normal/O rc=0 qualify source/history/whole closed-unit retention and normal/print teaching. Frozen strict version guard and earlier producers remain exact; setup uses the published pinned installer. Normal COMMIT/postcheck completes publication; no Rust changed or push.
- [x] **LOCKSTEP** — MEM/CH/DEV/task/book's toolbox include agree, fixed caps and LIVE_STATUS unchanged. promotion: declined (scoped integration repair; existing tools-first/locality/pinned-version contracts suffice). D79 priority1/open, D80 afterward, LC0047 app disposition remains pending.

LC0047 runtime update after cb39c69, owned by ARTIFACT-CLEANUP.8/AC0065:
actual host census now rc=0/handoff: OK; the prior app handles are no longer
observed. No app termination or sanctioned-process change was made. Original
LC0047 witness stays retained; this external-state blocker is cleared at this
measurement. Final census remains required; D79 terminal capture is next.

###### .4i2b5c.404 / SEMULITH-LC-0046 — qualify and repair 404 asset bases (pending)

Priority1 D80: actual generated seven-book 404 pages use origin-root base URLs;
shared collection serving requests css/scripts outside their book and gets404.
Reproduce through the published serving/configuration interface; distinguish
local file/shared-root/hosted fallback contracts and fix the owned integration.
Do not alter mdBook/Gitlink internals or claim resource completeness from heading
success. Keep all URLs/old captures/prefixes/history/modes/caps exact or record
owned explicit transitions; book/live sync and normal COMMIT before search.
Immediate after D79 tracing/repair; current owner .4i2b5c.404.

###### .4i2b5b3 — qualify generated search (pending)

After heading navigation, qualify full seven-book search document membership,
routes/labels/content contracts, actual inputs, normalization and omissions.
Inspect large generated indexes structurally, never dump entire lines. Preserve
published captures, whole history/source/modes and fixed limits; resources
remain .4i2b5c. No complete graph/adoption/processor acceptance claim.

### .4i2b1 / SEMULITH-LC-0024 — correct composition progress and count discrimination

Closed record: [complete original record](archive/LIVE-CONTAINMENT-readers.md#4i2b1--semulith-lc-0024--correct-composition-progress-and-count-discrimination).

### .4i2b2 — priority1 D59 source parser and bare-ratio coverage

Status: complete; LC0025 qualified sources/projections, LC0026 retained
closed units, and LC0027 repaired D59/D64. Commitcad73f3 passed normal hooks,
exact13-file postcheck, brief0 and host handoff0 before reader review resumed.
Owner: LIVE-CONTAINMENT.4. Actual public TREE-CLAIMS reports0 with a stale bare
composition ratio (D58); assessment.json enumerates every ratio after a tree
reference across all four live files. Candidate binding is not semantic truth:
MODEL-METHOD's later52/52 is instruction coverage; P1/P2's later129/129 and642/642
are guest/observation coverage. At5bdaa14 its parser measures MODEL-METHOD6/6,
P3-BREADTH6/7 and P4-SYSTEM4/18, while the live rows state18/18,8/8 and13/18.
Tools locate archived summaries, slice-gated status and bold done as source
preconditions requiring qualification, not evidence that every live count is
wrong. Reproduce each source boundary via public interfaces and records, log
any further confirmed defect, then fix source decoding before adding a scoped
bare leading-progress-ratio grammar. Preserve archival immutability; do not
rewrite source tasks to fit summaries. Correct any independently established
stale live counts in lockstep. Qualify statuses/summary uniqueness, omissions,
old controls, history exclusion, nearest-tree binding and later non-task ratios.
No generic Markdown coverage claim. LC0027 supports explicit leaf counts
and scoped leading ratios; later bare instruction/observation ratios stay excluded.

#### .4i2b2a / SEMULITH-LC-0025 — qualify source and progress-reader boundaries

Closed record: [complete original record](archive/LIVE-CONTAINMENT-readers.md#4i2b2a--semulith-lc-0025--qualify-source-and-progress-reader-boundaries).

#### .4i2b2h — whole closed-unit part containment before code repair

Closed record: [complete original record](archive/LIVE-CONTAINMENT-readers.md#4i2b2h--whole-closed-unit-part-containment-before-code-repair).

#### .4i2b2b — repair qualified task source and mirrored progress

Closed record: [complete original record](archive/LIVE-CONTAINMENT-readers.md#4i2b2b--repair-qualified-task-source-and-mirrored-progress).

### .4i2a / SEMULITH-LC-0023 — collect closed graph inventory evidence

Closed record: [complete original record](archive/LIVE-CONTAINMENT-readers.md#4i2a--semulith-lc-0023--collect-closed-graph-inventory-evidence).

## Decisions

- `2026-10-21` director ruling (`SEMULITH-LC-0052`): the book and the unit books carry no
  size ceiling; the task family's aggregate and count are ungoverned, per-part kept; a second
  seal rejected; per-unit duplication cut. Words: docs/decisions/decision_containment-reset.md.

- `2026-10-10` .4b (`SEMULITH-LC-0005`), owned on clean47cb436: review12 closed
  P4 archive files only. Prototype/consumers/retrieval proof:
  docs/decisions/decision_task-history-seal-review.md; evidence
  target/live-containment/task-history-review. No removal/cap/checker change.
  .4c/LC0006: director approved2026-10-10; own bounded reader, freeze, controls, stubs and atomic migration.

- `2026-10-08` (director approval / .4a ownership before code): the director explicitly
  approved the proposed tracked archive of 210 older shards, with byte-exact retrieval
  and the browsing change. Implement only this finite pressure prerequisite now.
  Descriptor/index fail closed on unknown fields, unsafe paths, changed/missing objects,
  oversized metadata/payload, duplicate/extra members and per-member identity mismatch.
  The descriptor is immutable after commit; authenticate archived manifest rows alongside
  the live SHA manifest, retaining append-only and heading uniqueness across both.
  Keep only active rows in the live manifest so it does not grow with sealed history.
  Preserve shard numbering across archived names to avoid reusing retired logical paths.
  Read/check never extract to disk or invoke Git; ordinary clones retain the tracked
  artifact. One finite terminal (three files, one sealed object) is registered without
  raising any existing cap. A future seal needs its own owned authority/transition.
  Add permanent positive/negative archive controls plus the existing 14 shard controls.
  Route all temporary gate files to target on the repository volume; the current
  freeze wrapper's unqualified mktemp violates locality when run outside the hook.
  Verify the 211-member capture before deleting exactly its 210 proven duplicate files;
  full logical partition and predecessor comparison must pass before commit.

- `2026-10-08` (ownership before archive experiment): P4.12 e1c1 routes an immediate
  commit-continuity dependency here. At its completed doc update, docs/changelog has
  212 files / 784,318 B against 786,432 B; CHANGELOG is 65,528 / 65,536 B and its
  next whole-record cut needs 2,377 B before header/manifest. Current aggregate
  headroom is 2,114 B. The guide's Phase 2 requires a rolling ledger to transition
  sealed history before aggregate growth becomes unbounded; the older calendar-based
  doubling records do not demonstrate a changed user contract under the newer policy.
  Do not raise a cap or delete frozen history. Prepare a deterministic, same-volume
  compressed archive of the 210 already-sealed shards captured at ff75610, preserve
  their manifest, verify all members byte-for-byte and record tool-neutral retrieval.
  This is a disposable read-only-source prototype, not an adopted migration. Present
  the concrete lifecycle/browsing choice before any live removal or checker change.
  The external guide's Stop conditions requires direction when a lifecycle choice
  changes what users can directly browse; the recommended query-first terminal does.

- `2026-10-06` (measured before opening): the drifts were found while registering
  `CITATION-QUOTES` (`SEMULITH-CA-0001`) — the Knowledge Map's subsystem paragraph names
  `crates/app/` (`ls crates/` → `semulith-cli semulith-core semulith-dsp56300
  semulith-verify`; no `app`), and three governance surfaces finished that commit within
  0.1–0.3 % of their ceilings after their new rows were tightened to fit. Tightening wording
  to pass a cap is the guide's named anti-pattern; this tree owns the real answer.

## Approved archive lifecycle decision — `.4` slice (a)

**Approved on 2026-10-08; implemented by slice (a).** The exact capture/proposal below is retained as decision evidence. The recommended
choice is a query-first `archive_terminal`: seal the 210 older Markdown shards and
manifest in one immutable, tracked, content-addressed gzip/tar artifact, with a small
tracked descriptor and a deterministic retrieval verifier. Retain recent shards and
both bounded heads. Historical content becomes retrievable by logical filename through
ordinary tar/Python tools instead of being directly browsable as 210 Markdown files.
A Git-history-only terminal is an alternative, but requires an explicit reachability,
backup and shallow-clone recovery contract. A cap increase lacks contract-expansion
proof and is excluded by this tree's adopted trigger.

Read-only-source prototype (same-volume, disposable, not the adopted destination):

- Capture: `ff75610f794b60a5bbe63c432bd4c78ebe163527`; its SHARDS.sha256 lists 210 shards.
- `python3` prototype: all 210 Git blobs equal their working files and pinned SHA-256
  rows; tar/gzip round-trip authenticates all 211 members, including that manifest.
- Complete source 781,740 B; deterministic USTAR 952,320 B; gzip (mtime=0, empty
  filename, level 9) 284,500 B (Python 3.14.7, zlib 1.2.12). SHA-256:
  `4cbc226272062441fa50998df217db74f7f2a069de54690f5a9dec9e107e4be7`.
- Prototype: `target/live-containment/history-review.tar.gz`; exact reproduction is
  from the named commit's sorted logical paths, USTAR metadata (mode 0644, all other
  fields zero/empty) and gzip settings above. No off-volume cache or workspace.
- Tool-neutral member retrieval:
  `tar -xOf target/live-containment/history-review.tar.gz docs/changelog/shard-0001.md`.
  Retrieval of every member was executed and asserted byte-exact, not merely sampled.
- The new live shard-0209 stays outside this proposed capture. Removing only the 210
  captured live copies after approval would leave that recent shard and its live
  manifest, restoring the ordinary family's headroom without changing frozen bytes.

Proposed transaction after lifecycle direction: own a bounded `.4` migration slice;
store the immutable artifact under `docs/history/sealed/` and one finite descriptor;
verify former paths, exact counts/bytes/digests, record order/uniqueness and full
retrieval; extend SHARD-FREEZE to authenticate archived rows through that descriptor
while retaining its append-only guarantee; wire terminal pressure/path/retrieval
checks and positive/negative controls unconditionally; update routes/book; remove
only the proven duplicates; commit atomically. The project owns retention: tracked
artifact survives ordinary clones, no Git-history condition, no new content appended
to this sealed object. Missing/corrupt archive or descriptor fails closed; recovery is
restoration of the exact digest from the committed artifact. Other archive transitions
need their own finite capture; this descriptor is not an unrestricted overflow sink.

The lifecycle choice changes direct historical browsing. The source guide's
Stop conditions says: “a lifecycle choice would change what users can directly browse”.
The director supplied that direction on 2026-10-08 before removal or implementation.
The cache slice can finish cleanly first; staged C/counts resume after containment.

## Open Questions

- Does `.3` adopt the full checker package (`live-document-size/` in the donor) or map its
  contracts onto the existing README-ROUTING-CLOSURE registry? Measured at `.3`.
- Found 2026-10-21 by `P4-SYSTEM.14` a42ar: `docs/book/src/working/task-trees.md` carries
  number–word joins with the space removed ("becomes151+9, total160", "pooled107 files;108
  breaches", "Health64"; the "cover33 tasks … and29 lesson cards" line is repaired in
  that commit) — a compaction made under the book's former ceiling. The ceiling is 0 since
  `SEMULITH-LC-0052`; a readability restoration pass of that page is due as an LC slice.
- Found 2026-10-21 by `P4-SYSTEM.14` a42ar: `docs/knowledge/` stands at its file ceiling (30 of
  30 files, 97 % of 98,304 B; health 12 files / 20,480 B, so the health line has never been a
  warning). The 31st card (98,684 B) was refused by README-ROUTING-CLOSURE and the lesson was
  promoted into an existing decision record instead. The same shape as `profiles/`
  (decision_profiles-family-corpus-second-rederivation): the next lesson card cannot land without a
  reviewed re-derivation or the director's ungovern word. Director's call.

## Blockers

- None.

## Acceptance Checklist (LC0027 task-source repair — LIVE-CONTAINMENT.4i2b2b)

Closed rows: [retained verbatim](archive/LIVE-CONTAINMENT-rows.md#acceptance-lc0027).

## Acceptance Checklist (required for any leaf that lands a CODE change)

Closed rows: [retained verbatim](archive/LIVE-CONTAINMENT-rows.md#acceptance-rows).

## Verification Log

Closed rows: [retained verbatim](archive/LIVE-CONTAINMENT-rows.md#verification-log).

## Commit Log

Closed rows: [retained verbatim](archive/LIVE-CONTAINMENT-rows.md#commit-log).

## Changelog

- `2026-10-06`: `.3` done (`SEMULITH-LC-0003`) — TOOLBOX and DOCTRINE_ENFORCEMENT partitioned
  into family files behind bounded indexes; REGISTRY-MIRROR judges the doctrine families' union.
- `2026-10-06`: `.2` done (`SEMULITH-LC-0002`) — the orientation map names the real crates and
  subsystems; the scaffold header and the policy note's stale measurements corrected.
- `2026-10-06`: `.1` done (`SEMULITH-LC-0001`) — completed trees leave the index: 22 rows
  moved verbatim into `docs/TASK_TREE_CLOSED.md`, FRONTIER-SYNC gates both files.
- `2026-10-06`: Created after `SEMULITH-CA-0001` measured the stale orientation map and the
  three governance surfaces at their ceilings.
