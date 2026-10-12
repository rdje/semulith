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
| 1 | `LIVE-CONTAINMENT.4` | `active` | .4i2b4b1r repair D73 public index refusal after LC0032 normal COMMIT |

## Approved task-history migration — .4c / SEMULITH-LC-0006

Director approval2026-10-10 covers the reviewed12 closed P4 histories. Own one
atomic copy/verify/use/retire transition: strict finite descriptor and tracked
object, bounded no-Git reader, deterministic navigation stubs preserving incoming
anchors, unconditional TASK-HISTORY gate and fail-closed controls. The active
P4 graph, original consumer bodies, earlier terminal and existing caps stay exact.
Full containment adoption remains .4 work. This finite slice is complete; verification below.

## .4d / SEMULITH-LC-0007 — standalone temporary storage

Owned on cleanf699474 before census artifacts or code changes. Resolve the
previously logged unqualified mktemp defects in task acceptance and other
entrypoints; enumerate own shell/Python/JS/Rust temporary allocators first.
Keep every allocation on the repository volume even with an external TMPDIR,
including nested gate calls, and verify cleanup/standalone behavior. Repair the
already-owned stale SHARD-FREEZE registry description in this same maintenance
slice. Current-corpus SEAM-INTEGRITY also calls newly staged boxes "committed";
source inspection shows it reads current tracked task files. Own that reporting
correction and its regression control; no historical-preservation claim added.
An actual published task-acceptance probe run returned9pass/1fail at CTRL-4b.
`git log -S`/blame pins d8c2337: the generic gate-shape signature began accepting
WIDGET-COVERAGE, so the old custom-seam fixture no longer isolates that seam.
Own a token-only fixture correction and permanent whole-probe regression arm in
this slice; production acceptance vocabulary stays unchanged.
The expanded census includes executable task artifacts: two more unqualified
WORK allocations, plus synth's qualified allocation without creating its parent
or checking mktemp failure (a following cp could receive an empty scratch root).
Own these same-volume/fail-closed fixes in .4d before editing those files; the
published probe workflows and their behavior remain the verification interface.
Acceptance: targeted before/after controls and full doctrine/book checks; preserve
archive pins, runtime/canonical/profile/frozen data and all existing ceilings.
Then resume P4.14 structured experiments. Full .4 adoption remains open.
Controlled in-memory execution of the new shell shim at optimization levels0/1
shows its assert guard disappears at level1: mock allocator called despite an
unqualified template. No allocation occurred. Own explicit non-assert guards and
an optimized-interpreter negative control here before signoff; retain the mock
proof in target/live-containment/locality/optimization-before.json.
Status: complete; final full CI passes all five legs, Rust173/17/253, seven books.
Evidence: target/live-containment/locality; durable control scope is
docs/decisions/reference_temporary-allocation-controls.md.

## .4e / SEMULITH-LC-0008 — complete the book's temporary-control review surface

Owned on clean1146d1b, brief0/untracked and actual process census OK, before edits.
The rendered task-tree chapter contains only a code-formatted repository path to
reference_temporary-allocation-controls.md, so a book-only reader cannot inspect
its mode matrix, reproduction or limits there. Correct this review-surface gap
with an anchored live include of the authoritative reference body and runnable
positive examples, preserving every prior reference byte through a simple inverse.
Use the existing chapter; keep all ceilings and LIVE/CPU/runtime/archive state exact.
Verify all seven books, rendered first/last content and examples, source inverse,
map/index/caps/table/path/currentness checks, then commit before resuming P4.14.
Status: complete; all seven books and complete source inverses pass.
Evidence target/live-containment/locality-book.

## .4f / SEMULITH-LC-0009 — truthful orientation before inventory adoption

Status: complete; D50 fixed/verified. Owned on clean314b0c4 after exact13-file commit verification,
brief0/untracked and unrestricted handoff0, before edits or scratch writes.
Inventory observation D50, priority2: KNOWLEDGE_MAP.md labels all33 flat task
files "Active task-trees"; its generator enumerates filenames without reading
status. Reproduce from the public generator and independent metadata census;
correct the heading to the complete task-file inventory, retaining every link,
order and other output byte. Verify a heading-only source/output inverse and
that the predecessor's active-set interpretation fails while the new complete
inventory agrees. No filtering or record removal is authorized by this slice.

The current MEMORY pointer also repeats roster details and D49 measurements.
Audit each removed field against its canonical task/index/decision home, then
overwrite it with the selected LC.4 action, required active IDs, in-flight state,
blockers and derive-on-read revision. Preserve the existing TREE-CLAIMS active-ID
contract; no cap or checker semantics change. Publish both orientation meanings
and exact read commands in the existing book chapter. Own target/live-containment/
orientation diagnostics, focused checks, seven books/rendered normal+print,
complete old history/head retention and protected-file/mode proof. Fixed caps,
archive bodies, CPU/canonical/LIVE stay exact; COMMIT before the next slice.
Task-family census on314b0c4:96files/2362533B =33trees/1175978B,
one template/3414B,40archive files/1070409B and22artifacts/112732B.
Full doctrine/inventory/checker adoption and a reviewed capacity remedy remain
LC.4; this slice does not adopt donor measurements or widen a limit.
promotion: declined (the orientation correction and canonical routes are local).

- [x] **ROOT CAUSE** — `python3 target/live-containment/orientation/verify.py`
  rc=0: predecessor labels33 files active; independent Metadata census derives
  six active,23 done and four proposed. Generator enumerates all flat filenames.
- [x] **ADDRESSED** — verify.py normal/O rc=0: heading-only generator/map
  inverses exact, all33 ordered links retained. MEMORY32lines/2871B becomes
  26lines/1461B before final resume wording; eight canonical audit homes resolve,
  six active IDs close. TREE-CLAIMS rc=0 after draft line-wrap correction.
- [x] **NO REGRESSION** — focused.sh/verify.py/rendered.py rc=0 (normal/O for
  verifiers): focused12/sharder12/seven books/3208 fresh+actual links, complete
  normal+print teaching/three literal commands,97 old history entries/whole
  heads and1386 protected regular files/Gitlink exact. Caps/archive/LIVE unchanged.
- [x] **LOCKSTEP** — book/source/map/pointer/history and this owner agree;
  mandatory COMMIT hooks apply. Full doctrine/inventory/checker adoption and
  capacity remedy remain .4; no CPU or qualification credit.

## .4g / SEMULITH-LC-0010 — adopt the local neutral containment contract

Status: complete (contract import only). Owned on clean91a8f59 after exact7-file commit verification,
brief0/untracked and unrestricted handoff0, before scratch or source changes.
Read the current external adoption guide, neutral doctrine and checker contract
in full. Source fsmgen revision a9867e16752e9ea37a873e92c7b955782c5cbf37:
doctrine32730B SHA256beefcc17ed958a1a5b3d55f4ba91cf6458c68c5e91ab715046980444cf723cbf;
exact bytes after its local-adoption-end marker20208B/343lines SHA256
0be4823ed138daff87fd7ed9ff6a9e6fde377a855075b407de97ebca6a293244.
All three reviewed policy files match that committed source; the other repo is
strictly read-only and will not become a build dependency.

Copy only the unchanged neutral doctrine body into a project-owned root copy,
with a separate Semulith authority/phase/locality note bounded to40lines/2048B.
Register that new normative surface with limits derived from those two parts;
no existing cap changes. Wire discovery through canonical CLAUDE.md (AGENTS.md
already routes there), update the README policy's local adoption state, and
include the complete local contract in the existing book chapter. Preserve
README policy's neutral body and all old book teaching outside the new section.
Do not claim complete inventory, field classification, registry/checker adoption
or migration: these remain explicit .4 obligations under the guide's phases.
Re-derive routes/current mirrors only after actual registration. Own
target/live-containment/contract, exact import/source inverses, full prior
history/head retention, protected modes/Gitlink, focused checks, seven books/
complete normal+print teaching, actual examples and COMMIT. Existing seals,
archives, task-file count/caps, CPU and qualification stay unchanged.

D51 owned priority2 for the next .4h capacity review: the old count decision
calls28 flat files live trees; Git6622177 derives27 trees+one template,
nine archives and24artifacts. Git314b0c4 derives33trees+one template,
40archives and22artifacts, with six added trees and none removed. Preserve the
old receipt; append an explicit classification correction and review any remedy
against the actual contract expansion. No count raise is authorized by this
import slice. Exact source inventories: orientation/capacity-baselines.json.
Full inventory/adoption follows; LC.4 owns every remaining pressure remedy.
promotion: declined (the adopted local normative contract owns this policy).

- [x] **ROOT CAUSE** — `python3 target/live-containment/contract/verify.py`
  rc=0: source91a8f59 lacks the local copy; reviewed source neutral body is
  20208B/343lines/SHA0be4823e. Full copy/inventory/checker were pending .4.
- [x] **ADDRESSED** — verify.py normal/O rc=0: exact neutral body plus separate
  1892B/28line note; complete22100B/371line policy under derived383/22256 caps.
  Whole bootstrap/README-neutral/book/registry inverses pass; derive-list rc=0
  reports39 routes,39 doctrines/1441 arms/49 chapters unchanged otherwise.
- [x] **NO REGRESSION** — focused.sh/verify.py/rendered.py rc=0 (normal/O for
  verifiers): focused12/sharder12/seven books/3236 fresh+actual links; all56
  policy blocks in order normal+print and literal22100B read exact. All99 old
  history entries/whole heads and1384 protected regular files/Gitlink exact;
  existing limits, seals, archive bodies and CPU/qualification unchanged.
- [x] **LOCKSTEP** — canonical bootstrap, local README-policy state, complete
  book contract, pointer and owner synchronized; LIVE changes only38→39 routes.
  Full inventory/field/debt/registry/checker/migration adoption remains open;
  .4h owns D51/capacity review after COMMIT. No count increase in this slice.

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

##### .4i2b4b1r / SEMULITH-LC-0033 — repair D73 public index refusal (pending)

Preserve typed input refusal2 in generator and guard, valid bytes and original
six shell controls. Add actual public read/Unicode controls normal/O and copied
omissions; update book/registry mirrors only where actual scope changes.

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

## Blockers

- None.

## Acceptance Checklist (LC0027 task-source repair — LIVE-CONTAINMENT.4i2b2b)

Closed record: [complete original record](archive/LIVE-CONTAINMENT-readers.md#acceptance-checklist-lc0027-task-source-repair--live-containment4i2b2b).

## Acceptance Checklist (required for any leaf that lands a CODE change)

`LIVE-CONTAINMENT.4` slice (e), `SEMULITH-LC-0008`:

- [x] **ROOT CAUSE** — `git show 1146d1b:docs/book/src/working/task-trees.md`
  rc=0 shows only a code-formatted reference path for temporary controls; no
  mode matrix or runnable examples reaches the book-only review surface.
- [x] **ADDRESSED** — source/render verification rc=0: LOCALITY-BOOK: complete
  reference/book inverses exact; five rendered examples and first/last limits present.
  The anchored live include keeps the detailed matrix and limits in their owner.
- [x] **NO REGRESSION** — `make book` rc=0: seven books build. Focused8 rc=0; LOCALITY-BOOK-SCOPE:1269 tracked files unchanged
  rc=0. No code/runtime/
  profile/archive/cap/LIVE change. Earlier reference bytes are all retained.
  promotion: declined (the canonical reference and direct book include are sufficient).

`LIVE-CONTAINMENT.4` slice (d), `SEMULITH-LC-0007`:

- [x] **ROOT CAUSE** — `python3 scripts/probe_temporary_locality.py --mode shell
  --revision f699474` rc=1: TMP-LOCALITY:44/56 shell sites qualified and cleaned;
  Python predecessor0/2 and synth parent control also RED1. Published acceptance
  probes9pass/1fail at CTRL-4b; scoped git log/blame pins generic signature d8c2337.
- [x] **ADDRESSED** — locality modes shell/python/children/parent rc=0:
  TMP-LOCALITY:56/56 shell,2/2 Python,28 child environments and fresh synth parent
  pass. Four named negative modes each rc=1 before a foreign allocation or after
  observing controlled residue. Materials20/0 and comparator4/0 clean all fixtures.
- [x] **NO REGRESSION** — `make ci` rc=0, all five legs, Rust173/17/253,
  seven books; focused11 rc=0, SEAM-INTEGRITY19/0,
  archive46/0, acceptance10/0, waiver5/0, synth6/0. Scope verifier rc=0 preserves
  canonical/runtime/profile/frozen/fixtures/earlier history and archive pins.
- [x] **LOCKSTEP** — `bash scripts/check_derived_counts.sh --list` rc=0 derives
 39doctrines/728arms/38routes/49main chapters/0open upstream issues. Reference,
  doctrine/toolbox/INDEX/map, live docs and task-history book explain the exact
  finite control scope; all earlier caps remain. CPU/P4/P5 milestones unchanged.
  promotion: reference_temporary-allocation-controls.md owns the durable controls.

`LIVE-CONTAINMENT.4` slice (c), `SEMULITH-LC-0006` (approved2026-10-10):

- [x] **ROOT CAUSE** — `git ls-tree -r -l 63ae063 -- docs/tasks/` census, rc=0:
  TASK-HISTORY-CENSUS: 89files/3,145,703B, only25B under3,145,728. Closed historical narratives add a
  scaling term; another split does not reduce the aggregate. The director approved
  the reviewed12-file finite capture and changed browsing before migration.
- [x] **FIX** — exact tracked375029B object plus immutable967B descriptor; bounded
  standard-library reader authenticates all13members before stdout.12 exact stubs
  retain paths/eight anchors; TASK-HISTORY checks identities, predecessor, navigation,
  incoming anchors and absence of live narrative includes unconditionally. No cap grows.
- [x] **ADDRESSED** — `python3` capture/migrate/verify.py rc=0: all12originals
  equal Git47cb436 and review pins;1,144,703B/15,055lines remain retrievable.
  Stubs7,040B release1,137,663B. All27external reference records preserved;
  permanent links checker rc=0 validates16links including archived cross-links.
  The checked reproduction recipe rebuilds exactly the reviewed archive after retirement.
- [x] **NO REGRESSION** — `bash scripts/check_task_history.sh --self-test`
  46pass/0fail; all12Python/tar reads exact in relocated no-Git fixture with no
  extraction or writes. Corrupt valid-path reads emit no stdout; malformed metadata,
  unsafe/duplicate/extra/missing/oversized members, changed pins/stubs/links refuse.
  Focused15 and `make ci` rc=0 (Rust173/17/253, all doctrines, bench, smoke, seven books).
  Full predecessor inverses and unchanged canonical/runtime/frozen/fixtures/earlier
  history proof rc=0; active P4 graph and profile ENVIRONMENT exact.
- [x] **LOCKSTEP** — live docs, decision approval/recipe, terminal, routing and
  doctrine/toolbox mirrors, book/history navigation/index updated. Complete old
  book retrieval section moved verbatim (SHAac1fe971d0c567c86b3a63a22b845c9c284cfb223c0e38b2196b8dbf88372759).
  Derived counts39doctrines/718arms/38routes; CPU/P4/P5 milestones unchanged.
  Evidence: target/live-containment/task-history-seal. Full .4 adoption remains open.
  promotion: declined (the finite decision, checked reader and46 controls encode this transition).


`LIVE-CONTAINMENT.4` slice (a) — approved finite archive (`2026-10-08`, `SEMULITH-LC-0004`):

- [x] **ROOT CAUSE** — Python census: live archive 212 files / 784318 B, 2114 B
  headroom; CHANGELOG 65528 B and next whole record 2377 B. Sharding scales the
  aggregate indefinitely. Director approved the concrete tracked terminal before code.
  Earlier e1c0 archive cap failed at 787026 B. `rg -n mktemp
  scripts/check_changelog_shards.sh` also found a standalone off-volume temporary.
- [x] **FIX** — seal exact ff75610 capture, retain original manifest; bounded strict
  descriptor and content-addressed object own full-source counts/digests. Read/check
  authenticates all members without Git or extraction. Freeze gate authenticates the
  live/archive logical union, immutable predecessor descriptors and heading/location
  uniqueness. Sharder preserves retired names; gate comparison files use target/.
  Retire only exact copied duplicates after verification. Register one finite terminal
  with count 3 / bytes 304980 derived from immutable object plus bounded metadata.
  Existing ceilings unchanged; full doctrine/inventory adoption remains open in .4.
- [x] **ADDRESSED (verified)** — Python copy/verify: 210 original shards plus manifest,
  211 members / 781740 source B / 9639 lines; every source equals its captured Git blob
  and digest, archive digest 4cbc226272062441fa50998df217db74f7f2a069de54690f5a9dec9e107e4be7.
  Post-retirement residue: zero retired files, recent 0209 retained. Reader rc=0:
  HISTORY-ARCHIVE ok (one object, 210 authenticated shards). Freeze rc=0: 213 logical
  rows after two new ordinary cuts. docs/changelog: four files / 8039 B; terminal:
  three files / 287216 B. Self-test 31 pass / 0 fail (old 14 + GREEN/sixteen RED).
  Controlled no-Git fixture retrieves exact bytes and predecessor row, preserves
  retired number 0042→0043, and corruption/path/bounds/schema/duplicates refuse.
- [x] **NO REGRESSION** — sharder self-test 12 pass / 0 fail; all earlier freeze
  controls retained. New head cuts print completeness: CHANGELOG 69 == 68 kept + one
  moved, 65977→63601 B; DEV_NOTES 32 == 31 kept + one moved, 49408→46983 B, order/bytes
  exact. Full logical predecessor digest proof includes all 211 pre-transition rows.
  No Rust, profile or expectation changes. CI-RECOVERY logs three hosted failures and
  the additional Linux nightly-name defect; local green does not certify hosted CI.
- [x] **LOCKSTEP** — live docs, tree/index, CI ownership tree, book, toolbox/doctrine,
  route registry, tracked terminal/descriptor updated. DERIVED-COUNTS derives 37 routes
  and 599 arms; source capture preserved for independent reconstruction. Tool gates,
  book build and commit gate must be green before closure of this slice.
  promotion: declined (strict descriptor and seventeen archive controls encode the lesson).


`LIVE-CONTAINMENT.1` — the closed-tree register (`2026-10-06`, `SEMULITH-LC-0001`):

- [x] **ROOT CAUSE (WHY + WHERE)** — `grep -n "TASK_TREE" doctrine/readme_routes.tsv` → the
  index's registered control reads "one row per active tree; completed trees leave the
  index", and the census of its anchored table: 31 rows, 22 with status `done` — the control
  was never applied because nothing enforced it: FRONTIER-SYNC's CLOSURE rule required EVERY
  tree file to have an index row (`grep -n "UNLISTED TREE" scripts/check_frontier_sync.sh`),
  so obeying the registry would have failed the gate.

- [x] **ADDRESSED (verified)** —

  ```
  $ bash scripts/check_frontier_sync.sh --self-test → FRONTIER-SYNC --self-test: 20 pass / 0 fail
    (16 → 20: the completed-tree arms now judge the register; + COMPLETED IN INDEX,
    OPEN TREE IN REGISTER, DUPLICATE ROW, NO ANCHORS)
  RED — the new check on the real pre-move index (a worktree at HEAD): 22 × "COMPLETED IN
    INDEX … completed trees leave the index", rc=1
  the move: 31 rows = 9 open + 22 moved; every moved row byte-identical in the register
  $ bash scripts/check_frontier_sync.sh → FRONTIER-SYNC: ok (32 tree(s) …)
  $ wc -c docs/TASK_TREE.md docs/TASK_TREE_CLOSED.md → 4053 / 4861
  ```

- [x] **NO REGRESSION** — README-ROUTING-CLOSURE ok (34 governed destinations); TREE-CLAIMS
  ok; DERIVED-COUNTS re-derived (34 destinations, 449 arms); `make book` rc=0 (both anchors
  render); `make gate` → `=== all doctrines green ===`.

- [x] **FIX** — FRONTIER-SYNC reads the optional `TASK_TREE_CLOSED.md` (anchored), runs every
  check on its rows, CLOSURE over the union, plus the three new breaches; the register created
  and registered; the index's prose, COMMIT.md, TASK_TREE_README.md and the book's task-tree
  chapter (both anchors included live) describe the move; the doctrine mirrors updated.

- [x] **LOCKSTEP** — `docs/TASK_TREE.md` (this tree's row), `MEMORY.md` (active trees),
  `LIVE_STATUS.md` (34 / 449), `CHANGELOG.md`, `DEV_NOTES.md`, `DOCTRINE_ENFORCEMENT.md` +
  the book's doctrine row, `doctrine/readme_routes.tsv` (the row + its derivation comment).

`LIVE-CONTAINMENT.2` — the stale orientation sources (`2026-10-06`, `SEMULITH-LC-0002`):

- [x] **ROOT CAUSE (WHY + WHERE)** — hand-curated orientation text with no derivation:
  `grep -n "crates/app" knowledge-map/subsystems.md` → line 6 ("Still the scaffold's
  placeholder `main.rs`"), while `ls crates/` → semulith-cli semulith-core
  semulith-dsp56300 semulith-verify; `head -2 Cargo.toml` → "Rename/replace the starter `app`
  crate"; `grep -n "16,228" README_POLICY.md` → the adoption note's "no measured pressure"
  (CHANGELOG is 64 KiB and shards; four ceilings fired 2026-10-06). The KNOWLEDGE-MAP gate
  proves the map is the function of its sources — never that the curated source is true.

- [x] **ADDRESSED (verified)** —

  ```
  $ grep -c "crates/app" KNOWLEDGE_MAP.md → 0   (was 1)
  $ grep -n 'Some("' crates/semulith-cli/src/main.rs → check-examples, run, demo, bundle,
    replay, snapshot, resume, reduce, bench — the nine the corrected text names
  $ ls profiles/ → the six units the corrected text names
  ```

- [x] **NO REGRESSION** — `make check` rc=0 (the Cargo.toml edit is comment-only);
  `make gate` → `=== all doctrines green ===` (KNOWLEDGE-MAP regenerated).

- [x] **FIX** — `knowledge-map/subsystems.md` (the crates paragraph rewritten; definitions,
  profiles, schema/materials and the two book families added); `Cargo.toml`'s header;
  `README_POLICY.md`'s adoption-note paragraph (measurements only, routed to `.4`).

- [x] **LOCKSTEP** — `KNOWLEDGE_MAP.md` regenerated; this tree; `docs/TASK_TREE.md`;
  `MEMORY.md`; `CHANGELOG.md`.

`LIVE-CONTAINMENT.3` — TOOLBOX/DOCTRINE_ENFORCEMENT headroom (`2026-10-06`, `SEMULITH-LC-0003`):

- [x] **ROOT CAUSE (WHY + WHERE)** — both are "one row per" normative tables with a fixed
  ceiling and no partition: `wc -c TOOLBOX.md DOCTRINE_ENFORCEMENT.md` → 20,478 / 32,669 of
  20,480 / 32,768 B after `SEMULITH-CA-0001`'s rows were tightened to fit (the guide's named
  anti-pattern); the section census → 19,055 B of TOOLBOX is its tool table, 24,966 B of
  DOCTRINE_ENFORCEMENT its project-doctrine table.

- [x] **ADDRESSED (verified)** —

  ```
  the move census (rows before, from HEAD): doctrine rows 35 each exactly once: True;
    tool rows 76 each exactly once: True  (a FIRST pass found 75 — its row filter keyed on
    a backticked first cell and dropped `| any project check's --self-test |`; a second
    census by table position caught it; the move re-run from HEAD)
  $ wc -c TOOLBOX.md DOCTRINE_ENFORCEMENT.md → ~3.2 KB / ~11 KB
  $ bash scripts/check_registry_mirror.sh --self-test → REGISTRY-MIRROR --self-test: 13 pass / 0 fail
  RED — CITATION-QUOTES' long-form row removed from docs/doctrines/definition.md:
    NOT MIRRORED docs-doctrines-union.md: 'CITATION-QUOTES' is registered and has no row
  $ bash scripts/check_registry_mirror.sh → ok (3 document(s) mirror the registry)
  ```

- [x] **NO REGRESSION** — README-ROUTING-CLOSURE ok (36 governed destinations);
  DERIVED-COUNTS re-derived (36 destinations, 451 arms); `make book` rc=0; `make gate` →
  `=== all doctrines green ===`.

- [x] **FIX** — the two partitions (scratch mover `target/live-containment/partition.py`,
  verbatim, census-checked); REGISTRY-MIRROR's `project:` mirror scope + the union
  invocation + 2 arms; the parents' bounded indexes; "Adding a doctrine" and TOOLBOX's
  add-a-row note point at the families; both families registered with derivation comments.

- [x] **LOCKSTEP** — this tree, `docs/TASK_TREE.md`, `MEMORY.md`, `LIVE_STATUS.md` (36 /
  451), `CHANGELOG.md`, `DEV_NOTES.md`, `doctrine/readme_routes.tsv`.


## Verification Log

.4i2b4a: ten whole spans61745B/869LF, nine closed units +LC0027 checklist,
retained in63161B ordinary archive. Ten native headings/routes and old phase
anchor qualify; archived articles unchanged, search resources authenticated.
D71 closure corrected/full965B planning intro retained; D70 seven historical
claims plus correction mention qualified case-insensitively. Whole105 old
live entries/source/order/protected modes/seals remain exact. Focused12/books/
scaffold5/full handoff24 normal/O; normal COMMIT completes the unit.

.4i2b3b2: D65/D68 fixed; public24 bad greens→defect1,16 unsafe2,16 injected
faults2; seven defaults93 expanded chapters/49 edges/344 outputs exact normal/O.
Six actual omissions/mode discriminate; concurrent historical15/16 failures→0/16.
52 aggregate/26 navigation methods,22 shell arms;1571 derived. Retained2180B
whole book receipts;106 old live entries/source/order/protected identities/modes
verified before normal COMMIT. Full graph/adoption/processor acceptance open.

.4i2b3b1 final: component22/old23+26 controls normal/O; seven books93 chapters/
49 includes/all344 output files unchanged.34 public fixtures/eight actual faults,
13 component/four producer copied omissions discriminate normal/O. Tracked
cad73f3 replay exact80700B ledger; D66/D67 fixed, D65 integration next. Whole
reader copy1179B/book+6→524281,107 old entries/1418 protected modes/Gitlink/full
inverses exact. Focused12/books/scaffold24/3242 links/normal+print/literal checks
pass; caps exact. First pending commit interrupted for D67 before HEAD changed;
only restarted normal hooks and final postcheck can complete this unit.

.4i2b3a:1425-source/54-candidate boundary;49 include occurrences/48 targets/
93 full chapter expansions exact,344 output files unchanged normal/O. D65
public interfaces false-green24, valid4; three diagnostic omissions fail1 in
both modes. Whole DEV2490B retained,106 old entries/1418 protected modes/Gitlink
and complete inverses qualify. Focused12/books/seven/3242 links/rendered/literal
pass; no caps, CPU or archive-authority changes. D65 priority1 repair next.

.4i2b2b: D59/D64 repaired; original13/20 controls retained,38/41 normal/O;
12 public cases/mode,11 actual omissions/38 cases and eight real read faults
qualify.105 old entries/1411 protected/Gitlink and full source inverses exact;
focused12/seven books/3242 links/21 Foundation rows/three literal commands and
scaffold24 normal/O pass. Derived1565 arms; other LIVE/caps/CPU unchanged.

.4i2b2h: eleven whole units47486B/684LF retained with11 native anchor links;
1413 protected files/Gitlink/106 old entries and whole source inverses exact.
Focused12/seven books/3242 links/11 literal reads/normal+print pass; normal/O
checks agree. Earlier archives and caps fixed; D59/D64 code repair next.

.4i2b2a: source/D59/D64 qualified, D62/D63 corrected.14 controls/12 public
cases per mode;106 old entries/1406 protected/Gitlink exact. Focused12/seven
books/3242 links/rendered/literal pass; .4i2b2h containment next.

.4i2b1: D58 live composition Done/6 of6; D60 same-total arm13, old12 exact;
seven public cases/mode and copied omission0→2 normal/O. D61 two table joins,
all21 actual normal/print Foundation rows;3244 links and literal13-control
example pass.106 old history entries,1404 protected files/Gitlink and complete
source/book/task/guard/doctrine/live/history inverses exact normal/O;
focused12/sharder12/seven books pass. D59 source/ratio qualification priority1
next; other milestones/caps/canonical/CPU unchanged. Normal COMMIT required.

.4i2a: complete source1411/462 Markdown/53 literal include candidates; retained
seven-book120 HTML pages/3244 hyperlinks,2076 resource candidates and338 paths
outside book source directories. Source versus working rendering explicit;
22 finite refusals normal/O. Full independent source/program/state/output/
protected/history inverses, focused/seven-book/rendered and normal COMMIT
required; focused12/sharder12/seven books/3244 links and five reads pass.
No final graph/adoption claim; .4i2b transitive reader review next.

.4i1: immutable source1408/39 declarations and12 durable input refusals normal/O.
Local contract separates source membership from pending semantic graph coverage,
utility/lifecycle/fields/debt and checker integration. Whole-history/source/
protected inverses, focused12/seven books/rendered/five literal reads and normal
COMMIT required; focused12/sharder12/seven books/3244 links and five reads pass. Existing caps, count107/health64 debt, canonical/profile/CPU
and sealed histories remain exact; .4i2 complete graph inventory follows.

.4h6c4: task-capacity-application check-evidence/verify/history/rendered normal/O
and focused.sh rc=0. Fresh same33 IDs/typed96, exact separate authority and two
precondition refusals; count96→107 only plus dated pointer. Original107 breach1
becomes0; new108 breach1 and65 advisory0. Public normal/O green0/39 routes,
health64 debt; enclosing1407 states and guard94 byte-exact. Whole DEV4026B→0290
preserves104 prior entries; protected/Gitlink/canonical/ordinary/seals exact.
Focused12/sharder12/seven books/full normal+print/four reads and normal COMMIT
required; LIVE/CPU unchanged. .4i full inventory/checker adoption is next.

.4h6c3: task-capacity-review assess/review/verify/history/rendered normal/O and
focused.sh rc=0. Typed27/1/9/24→33/1/40/22, six creation/scopes, four typed/two
metadata refusals; real1405 snapshots exact. Separate107 authority; health64
debt and every registry limit unchanged. Three book-intro clauses compared;
D51/D55 facts and four literal reads/full normal+print remain. Whole CH rollover
retains105 prior entries; protected identities/Gitlink/canonical/seals exact.
Focused12/sharder12/seven books and normal COMMIT required; .4h6c4 applies next.

.4h6c2: registry-repair check-before/check-after/source-inverse/verify/history/
rendered normal/O and focused.sh rc=0. D56 primary faults2/no stdout; removed
seven consumers absent; D57 five malformed fixtures0→2. Public18 per mode,
real1404/pinned programs exact;94 controls,17 omissions/all26 discriminators.
Original68 byte-exact. Whole DEV rollover preserves104 old entries; caps,
canonical/history/seals/CPU exact. Focused12/sharder12/seven books/full normal+
print/three literal reads, handoff probe24/0 normal/O, staged acceptance/seam
and normal hooks required. LIVE routing Done/1518arms; .4h6c3 authority next.

.4h6c1: registry-projections check-evidence/verify/history/rendered normal/O and
focused.sh rc=0: seven actual consumers/14 fault cases green0, single traced
injections and healthy delegates; all raw streams/pins and per-run real1402
identities exact. Whole source/head inverses retain105 prior entries/1393
protected files/Gitlink; DEV3990B→0286/CH1330B→0287; frozen/canonical/caps exact.
Focused12/sharder12/seven books/full normal+print/three literal reads pass.
LIVE routing Mostly Done/D56 priority1 repair .4h6c2 next; CPU unchanged.

.4h6b: five-unit-correction assess/verify/history/rendered normal/O and focused.sh
rc=0: four closed inventories, complete profile deltas and original authority
pins; two wrong-count controls refuse; real1402 identities exact. Whole source/
head inverses,103 prior entries/1394 protected files/Gitlink and all ceilings/
manifest/seals exact. Focused12/sharder12/seven books, full normal+print/three
literal reads pass. D55 fixed; LIVE/CPU unchanged. .4h6c capacity review next.

.4h6a: capacity-navigation verify/history/rendered normal/O and focused.sh rc=0:
nine complete sources/27 clauses; index15526→13122B, free2674B. Whole source/
head/book/task inverses retain104 prior entries; receipt/digest refusals,
protected identities, focused12/sharder12/seven books and literal reads pass.
DEV3668B→0284/CH1417B→0285; all prior archives/seals/caps/LIVE/CPU exact.
D55 diagnosed/owned .4h6b next; separate capacity review .4h6c follows COMMIT.

.4h5: assess.py/verify.py normal/O rc=0: typed source inventories27/1/9/24
and33/1/40/22, six added instances/no removals, two metadata negatives refuse;
real HEAD/index/all1400 identities exact. Whole authority/registry/index/book/
task/head inverses retain original receipt and102 old head entries; protected
bytes/modes/Gitlink, manifests/seals and ceilings exact. Focused12/sharder12/
seven books, full normal+print teaching and two literal reads pass. D51 fixed;
LIVE/CPU unchanged. .4h6 separate capacity review follows COMMIT.

.4h4: final public normal/O replay baseline0; all injected unavailable
file/parser/hint/README/date reads refuse2 without green/stdout. Removed derived
wc/sort consumers receive zero injections. All1398 real tracked identities,
HEAD/index and pinned programs/facades exact. Original32+36 controls68/0;
14 omissions detected normal/O. Handoff24/0/0; old updater5/2/0 normal/O.
Whole source/history/protected-byte/mode inverses,101 prior entries, DEV3021B→
0283/3254B whole rollover and manifest prefix/seals exact. Focused12/sharder12/
seven books, full normal+print teaching and two literal examples pass. D53/D54
fixed; LIVE1492 arms/routing Done, caps/CPU unchanged; D51 .4h5 next.

.4h3: assess.py normal/O rc=0: baseline0; failed73 and partial+stderr
refuse2 without green/stdout; one family listing, all1397 real identities exact.
Permanent32/0 normal/O; nine omission variants refuse normal/O. Complete
checker/book/task/head inverses,101 prior entries,1383 protected regular files/
Gitlink and fixed limits exact. Focused12/sharder12/seven books/3242 links,
normal+print/two literal examples pass; D52 fixed. CH1382B→0282/1619B whole
rollover, manifest prefix exact,74live+210sealed284logical. LIVE routing closure
Done/derived1456 arms; no CPU qualification change. D51 .4h4 next.

.4h2: assess.py rc=0: baseline0/empty stderr; failed73 and partial+stderr
both falsely green0, three scoped listings each. Real HEAD/index/all1397
tracked identities exact. verify.py normal/O: complete book/task/LIVE/head
inverses,99 prior entries and1390 protected regular files/Gitlink exact.
Focused12/sharder12/seven books/3240 fresh+actual links; whole normal+print
teaching and literal checker command pass normal/O. D52 owned priority1,
repair next; LIVE routing closure Mostly Done, other status/caps/CPU unchanged.

.4h1: verify/history/rendered normal/O and focused.sh rc=0: five canonical
identities/15 source clauses, whole index/book/task/head inverses,101 old entries,
1387 protected files/Gitlink and fixed caps exact. INDEX16379→15656B;
decision family261604→260881B. Whole DEV6957B→0280/CH1398B→0281 retained,
receipt+digest refusals discriminate. Focused12/sharder12/seven books/3238links,
normal+print/two literal examples pass; only inherited EOF notices0280:100 and
0281:27, all other whitespace0. D51 remains owned next; LIVE/CPU unchanged.

.4g: verify.py/rendered.py normal/O and focused.sh rc=0: exact20208B neutral
body, bounded1892B note, complete source inverses/99 old entries/1384 protected
files/Gitlink exact. Focused12/sharder12/seven books/3236 links; all56 complete
policy blocks normal+print and literal read pass. Adjacent HTML table cells need
explicit boundaries in the text verifier; complete content agrees after that
normalization. Existing caps/seals/CPU unchanged; full adoption still pending.

.4f: verify.py/rendered.py normal/O and focused.sh rc=0: D50 fixed;33 files/six
active, heading-only/full-book inverses, eight pointer authority homes,97 old
entries/whole heads/1386 protected files/Gitlink exact. Focused12/sharder12/seven
books/3208 links and three literal examples pass; fixed caps and LIVE unchanged.

.4e: seven books, whole reference/book inverses and rendered five-command/first-
last checks, focused8 and protected scope1269unchanged rc=0.

.4d: focused11, shell56/56, Python2/2, children28, four named negatives, parent,
SEAM19/0, acceptance10/0, waiver5/0, synth6/0 and protected scope rc=0.
First full CI refused because registry editing overlapped the running shell reader;
syntax is green, sources fixed for complete rerun (target/live-containment/locality).
Final full CI after explicit-guard hardening rc=0: all five legs/seven books,
Rust173/17/253. Mock optimization levels0/1/2 refuse before allocator; optimized
shell56/56 passes. The two original follow-ups below are resolved by this slice.

.4c: capture/migration/reproduction/consumer/predecessor proof, focused15,46controls,
seven books and full five-leg `make ci` rc=0; byte-exact retention with no cap raise.

.4b: prototype/reproduction/controls/focused9/seven books rc=0.

Registry prose follow-up owned by `.4`: the SHARD-FREEZE description in
scripts/check_doctrines.project.sh still says the physical manifest only grows; the
approved seal preserves append-only logical rows across archive/live manifests instead.
The checker, doctrine family and book already state that contract. Priority: correct
this display text with the scheduled locality/containment follow-up after CI-RECOVERY.

The first commit gate refused the descriptor because FIXTURE-FINGERPRINT resolves
`path` relative to the record directory, while this terminal uses repository-root
identity. The new schema explicitly names its root-relative `object`; SHARD-FREEZE
authenticates that object and every source member, without changing or excluding the
generic fingerprint contract. The frozen object bytes and digests are unchanged.

Additional locality defect owned by `.4`: `scripts/check_task_acceptance.sh` uses
unqualified `mktemp -d`; `printf '%s\n' "$TMPDIR"` on this host returned the OS
temporary directory rather than the repository. The doctrine driver does not override
it. Other standalone entrypoints require a targeted census before a common repair.
Priority: establish repository-local TMPDIR for ongoing runs immediately; schedule the
entrypoint census/repair in `.4` after CI-RECOVERY and before broader containment work.
Do not delete shared OS temporary content or claim standalone locality already fixed.

Slice (a), 2026-10-08: copy/verify/retire exact, archive and partition controls 31/31, sharder 12/12; terminal 287216 B, ordinary shards 8039 B; gates/books at commit.

| Date | Leaf | Checks | Result |
| --- | --- | --- | --- |
| `2026-10-06` | `.3` | the section census; the verbatim moves (35 + 76 rows, each exactly once — the first pass's dropped row caught by a positional census); REGISTRY-MIRROR's project scope (13/13; the union RED on a removed row); the families registered | **met** — DOCTRINE_ENFORCEMENT ~11 KB, TOOLBOX ~3.2 KB; the next tool and doctrine fit |
| `2026-10-06` | `.2` | the three drifts measured (crates/app absent; the scaffold header; the 16,228-byte note); each corrected text checked against `ls crates/`, the CLI's subcommand match, `ls profiles/`; the map regenerated | **met** — the orientation sources state today's repository |
| `2026-10-06` | `.1` | the registry control vs the index census (22 of 31 rows completed); the CLOSURE rule that forbade obeying it; FRONTIER-SYNC extended (20/20; RED on the real pre-move index: 22 COMPLETED IN INDEX); the verbatim move; the register registered; the book's live includes | **met** — the index holds open trees only (4,053 B); completed trees have a gated home |

## Commit Log

`SEMULITH-LC-0031 (leaf LIVE-CONTAINMENT.4): retain whole closed reader records` — ten spans/nine units/checklist retained; index/query next.

`SEMULITH-LC-0030 (leaf LIVE-CONTAINMENT.4): enforce include integrity in public builds` — D65/D68 fixed; index/query expansion next.

`SEMULITH-LC-0029 (leaf LIVE-CONTAINMENT.4): qualify owned include sources and replay` — component complete/D66 fixed; D65 public integration next.

`SEMULITH-LC-0028 (leaf LIVE-CONTAINMENT.4): qualify actual include readers` — .4i2b3a assessment complete; D65 repair next.

`SEMULITH-LC-0027 (leaf LIVE-CONTAINMENT.4): validate task sources before progress claims` — D59/D64 fixed; .4i2b reader review next.

`SEMULITH-LC-0026 (leaf LIVE-CONTAINMENT.4): retain whole closed task units` — .4i2b2h complete; D59/D64 code repair next.

`SEMULITH-LC-0025 (leaf LIVE-CONTAINMENT.4): qualify task source and correct stale projections` — .4i2b2h next.

`SEMULITH-LC-0024 (leaf LIVE-CONTAINMENT.4): correct live composition progress` — D58/D60/D61 fixed; D59 qualification next.

`SEMULITH-LC-0023 (leaf LIVE-CONTAINMENT.4): collect closed graph inventory evidence` — .4i2a collection only; .4i2b transitive reader review next.

`SEMULITH-LC-0022 (leaf LIVE-CONTAINMENT.4): qualify containment inventory inputs` — .4i1 inputs and local integration contract; .4i2 graph inventory next.

`SEMULITH-LC-0021 (leaf LIVE-CONTAINMENT.4): apply reviewed task count authority` — .4h6c4 complete; count107, health64 debt; .4i full containment adoption next.

`SEMULITH-LC-0020 (leaf LIVE-CONTAINMENT.4): review separate six-activity count authority` — .4h6c3 complete; no cap change; .4h6c4 applies after fresh same33-ID/typed96 checks.

`SEMULITH-LC-0019 (leaf LIVE-CONTAINMENT.4): refuse unavailable or malformed registry policy` — .4h6c2 complete/D56–57 fixed; .4h6c3 separate capacity authority review next.

`SEMULITH-LC-0018 (leaf LIVE-CONTAINMENT.4): qualify remaining registry projections` — .4h6c1 complete/D56 confirmed; priority1 .4h6c2 repair before .4h6c3 authority.

`SEMULITH-LC-0017 (leaf LIVE-CONTAINMENT.4): correct the five-unit composition receipt` — .4h6b complete/D55 fixed; .4h6c separate capacity review next.

`SEMULITH-LC-0016 (leaf LIVE-CONTAINMENT.4): contain navigation before capacity authority` — .4h6a complete; .4h6b D55 correction next, .4h6c capacity review after.

`SEMULITH-LC-0015 (leaf LIVE-CONTAINMENT.4): correct the count receipt classification` — .4h5 complete/D51 fixed; .4h6 separate capacity review next.

`SEMULITH-LC-0014 (leaf LIVE-CONTAINMENT.4): refuse unavailable routing evidence` — .4h4 complete/D53–54 fixed; .4h5 D51 capacity review next.

`SEMULITH-LC-0013 (leaf LIVE-CONTAINMENT.4): refuse unmeasurable family inventories` — .4h3 complete/D52 fixed; .4h4 D51 capacity review next.

`SEMULITH-LC-0012 (leaf LIVE-CONTAINMENT.4): qualify capacity inputs before authority review` — .4h2 assessment complete; D52 repair precedes D51 capacity review.

`SEMULITH-LC-0011 (leaf LIVE-CONTAINMENT.4): contain duplicate decision-index summaries` — .4h1 complete; .4h2/D51 capacity review next.

`SEMULITH-LC-0010 (leaf LIVE-CONTAINMENT.4): adopt the local containment contract` — .4g complete; full inventory/checker/migrations and .4h capacity review remain.

`SEMULITH-LC-0009 (leaf LIVE-CONTAINMENT.4): make orientation describe its sources` — .4f complete; full adoption and capacity remedy remain.

`SEMULITH-LC-0008 (leaf LIVE-CONTAINMENT.4): publish temporary-control procedures in the book` — .4e complete.

`SEMULITH-LC-0007 (leaf LIVE-CONTAINMENT.4): keep temporary allocations on the repository volume` — .4d complete; full containment adoption remains.

`SEMULITH-LC-0006 (leaf LIVE-CONTAINMENT.4): seal closed P4 task history` — .4c complete; full adoption remains.

`SEMULITH-LC-0005 (leaf LIVE-CONTAINMENT.4): prepare finite task-history archive review`

`SEMULITH-LC-0004 (leaf LIVE-CONTAINMENT.4): seal the approved history archive with authenticated retrieval` — slice (a); full adoption remains.

| Leaf | Commit subject or reference | Notes |
| --- | --- | --- |
| `.3` | `SEMULITH-LC-0003 (leaf LIVE-CONTAINMENT.3): TOOLBOX and DOCTRINE_ENFORCEMENT partitioned behind bounded indexes — 76 tool rows and 35 doctrine rows moved verbatim, REGISTRY-MIRROR judges the family union` | both surfaces regain headroom; no row lost |
| `.2` | `SEMULITH-LC-0002 (leaf LIVE-CONTAINMENT.2): the stale orientation sources corrected — the knowledge map's subsystems, the workspace header, the README policy's measurements` | three drifts; the policy decision untouched |
| `.1` | `SEMULITH-LC-0001 (leaf LIVE-CONTAINMENT.1): the closed-tree register — completed trees leave the index (22 rows moved verbatim), FRONTIER-SYNC gates both files` | the control applied and enforced; the index 8,172 → 4,053 B |

## Changelog

- `2026-10-06`: `.3` done (`SEMULITH-LC-0003`) — TOOLBOX and DOCTRINE_ENFORCEMENT partitioned
  into family files behind bounded indexes; REGISTRY-MIRROR judges the doctrine families' union.
- `2026-10-06`: `.2` done (`SEMULITH-LC-0002`) — the orientation map names the real crates and
  subsystems; the scaffold header and the policy note's stale measurements corrected.
- `2026-10-06`: `.1` done (`SEMULITH-LC-0001`) — completed trees leave the index: 22 rows
  moved verbatim into `docs/TASK_TREE_CLOSED.md`, FRONTIER-SYNC gates both files.
- `2026-10-06`: Created after `SEMULITH-CA-0001` measured the stale orientation map and the
  three governance surfaces at their ceilings.
