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
| 1 | `LIVE-CONTAINMENT.4` | `active` | .4i2b transitive reader/index/query/generated-expansion review |

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

## .4h — revision-pinned task-capacity review (active)

D51 remains priority2 and owned here. Before selecting a count remedy, retain
the historical receipt and derive typed source inventories at6622177 and the
current committed boundary; distinguish task instances, template, archives and
artifacts. Six real task instances were added. A proposed increase requires a
new separate reviewed authority proving that expansion, not calendar growth.
Current decision-family pressure is a prerequisite, not permission to widen it.
Children: .4h1/LC-0011 index containment, .4h2/LC-0012 input assessment,
.4h3/LC-0013 inventory repair and .4h4/LC-0014 remaining-read repair are
complete; .4h5/LC-0015 completes D51; .4h6a/LC-0016 contains navigation,
.4h6b/LC-0017 completes D55; .4h6c1/LC-0018 confirms D56. Immediate next
.4h6c2/LC-0019 completes D56/D57; .4h6c3/LC-0020 reviews authority;
.4h6c4/LC-0021 applies it after fresh preconditions; .4i full adoption next.

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

Status: complete; input qualification only, full graph/adoption pending. Owned on clean3615547 after normal hooks, exact8-file postcheck,
brief0/untracked, unrestricted handoff0 and full COMMIT report. Read the full
local doctrine, source adoption guide and published neutral checker contract.
The external source is read-only (fsmgen HEAD21f4d3d); its ordinary package tree
is not a submodule. Complete local imported body remains20208B/SHA0be4823e,
including its six-byte separator; heading-only comparison is20202B and is not
the complete imported-body measurement. No source-policy drift observed.

Own target/live-containment/inventory-contract, fresh immutable HEAD census
and real HEAD/index/all1408 identities, checked complete source/path and existing
39-route declarations, local mapping of existing dimensions/classes/verifiers
against the published checker schema, and a bounded durable contract under
docs/tasks/artifacts/live-containment/, including its read-only source replay
qualifier and deliberate malformed-input controls. This is preparatory code,
not an integrated containment gate; own scripts/qualify_containment_inventory_inputs.py,
its toolbox discovery row and acceptance. Place executable discipline under the
existing scripts/ classification, rather than expanding the gate's path policy.
Separate complete source membership from
semantic graph coverage: no claim of complete surface/route/field adoption in
this preparatory slice. Keep authority/utility/lifecycle choices open until their
actual consumers are reviewed; no mechanical extension/date-based classification.

Own a concrete .4i2 discovery/coverage procedure: reader and emitted author
routes, transitive includes/index/query expansion, generated views, exact terminals,
opaque Gitlinks, candidate exclusions with reasons, and finite control-plane
bounds. Review published checker execution/proof-token/staged-input contracts
without importing donor paths, thresholds, owners or debt. Do not yet copy or
integrate checker implementation, migrate content, alter limits or inspect
submodule internals. Published integration contracts only for Gitlinks.

Own source/protected bytes/modes/Gitlink and whole-history inverses, necessary
whole-oldest CH/DEV rollover, real receipt/digest refusals, bounded book frontier/
pointer/owner synchronization, focused/seven books/rendered/literal checks,
normal hooks/exact postcheck/brief0/unrestricted host0. Existing registry count107,
health64 warning debt, canonical records, archived histories, CPU and profiles
remain exact. .4i2 follows COMMIT; all later adoption children stay pending.
promotion: declined (local preparatory contract and source replay are task artifacts, not new cross-cutting authority).


Implementation: inventory-contract.md specifies the source boundary, local
schema/classification gaps and separately owned .4i2–8 procedure. Tracked
qualify_containment_inventory_inputs.py replays immutable1408 identities/39 destinations;12 named
refusal controls pass normal/O. Registry/count107/health64 debt and imported
policy body unchanged. Complete graph/field coverage, lifecycle choices,
neutral-checker import and integration are not claimed by this slice.

- [x] **REPRODUCE / ISSUE** — existing39 routed destinations are a finite
  starting set; complete semantic graph coverage remains pending, not inferred.
- [x] **FIX** — locally owned bounded contract and read-only source qualifier;
  complete graph/utility/fields/debt/checker activities have separate owners.
- [x] **ROOT CAUSE** — `python3 scripts/qualify_containment_inventory_inputs.py`
  rc=0 normal/O: complete source1408/39 declarations pinned; existing declarations
  are inputs, with semantic graph coverage explicitly pending LC.4i2.
- [x] **ADDRESSED** — `python3 target/live-containment/inventory-contract/verify.py`
  rc=0 normal/O: complete source/protected/book/task/history inverses;
  local contract and read-only qualifier align, no capacity or lifecycle change.
- [x] **NO REGRESSION** — `bash target/live-containment/inventory-contract/focused.sh`
  rc=0: focused12/sharder12/seven books; rendered normal+print and five
  literal reads. All prior whole entries/modes/seals, LIVE/CPU remain exact.
- [x] **LOCKSTEP** — bounded book/pointer/task/artifacts/toolbox agree: closed
  inputs qualified; full adoption remains .4i. Normal COMMIT and postcheck close
  this unit before .4i2 complete graph inventory begins.

Final evidence: whole DEV3178B→0291/3411B,
SHA840f48217ca358f7fbee42f5e9f2b54f930f327db729bf7da5e19f9398349132;
105 prior entries and full source/order preserved. Combined guards refuse real
original/moved/published receipt edits with updated digests. Immutable normal/O
censuses,1400 protected regular files/Gitlink exact. Focused12/sharder12/seven
books and3244 fresh/actual links pass; complete navigation teaching, expanded
policy and five literal decision/contract reads verified normal/O. Render
instrument first compared an include token with expanded prose; trace pins that
mismatch, then correct only the instrument and rerun. No product render defect.
Book grows1B to524282; every other canonical/profile/CPU/registry input exact.
Normal staged acceptance/seam, hooks and exact postcheck/brief0/host0 required.

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

### .4i2b1 / SEMULITH-LC-0024 — correct composition progress and count discrimination

Status: complete; D58/D60/D61 fixed and verified; normal COMMIT/postcheck required before D59 and remaining .4i2b reader review. Owned on
clean9706ecb after normal hooks, exact10-file postcheck, brief0/untracked,
unrestricted handoff0 and full COMMIT report. Reproduction: LIVE_STATUS.md's
Composition row reports In Progress/2/6; MODEL-COMPOSE metadata, six leaf
statuses, frontier and closed register report done/6/6 on 2026-09-27. Impact:
the authoritative live review surface understates completed composition work.
Confirmed guard gap: actual public check returns0 on the stale bare ratio;
all12 old controls pass. Complete four-live-file candidate census also exposes
source/parser and semantic-binding preconditions, owned priority1 .4i2b2 below.
Use the existing explicit A-of-B-leaves grammar for this repair, and qualify
its actual refusal rather than widening an ambiguous parser. Historical
receipts and task source stay exact.

D61 confirmed/priority1 same-unit repair: actual status.html and print.html
render12 of21 Foundation rows as literal pipe prose, including composition.
Two blank lines end the only declared table; subsequent row groups have no
header/separator. table-before-v2.json enumerates all12 missing actual rows.
Join exactly those two breaks; own full rendered21-row reconciliation normal/O.
The initial row instrument also inserted spaces around inline code, giving
one extra false missing label; preserve it and the corrected cell-text census.
No table cell content is changed by this structural repair.

D60 confirmed in the first copied omission: removing the A_OF_B loop leaves
all12 old controls green and the actual wrong-done same-total row accepted0.
The initial diagnostic expected refusal and stopped; retain that failure and
raw streams. Own this priority1 same-unit discriminator repair: add one
same-total/wrong-completed count arm, preserving all12 prior arms. This makes
the copied omission refuse2 through the public self-check. Qualify normal/O
before/after; derived arm count changes only after the arm actually exists.

Own target/live-containment/composition-progress diagnostics and qualified
before/after evidence; existing scripts/check_tree_claims.sh actual public
positive/refusal and copied omission controls plus the D60 self-test arm;
truthful live composition row, doctrine
scope/limits and bounded mdBook explanation, including regenerated
docs/book/src/index.md from the public generator after chapter changes. Review the six completed leaves,
composition contract/public tools and current book before writing the new row.
No processor qualification or conformance claim follows tree closure. Preserve
existing controls, history exclusion and nearest-tree binding. Qualify guard
omissions and real source/HEAD/index/mode/Gitlink preservation normal/O.
Own whole-oldest CH/DEV rollover where required, full history/protected/book
inverses, focused checks/seven books/rendered teaching/literal examples, normal
COMMIT and exact postcheck/brief0/unrestricted host0. No cap, lifecycle, canonical
record, archived history or CPU change. Remaining .4i2b follows clean COMMIT.
promotion: declined (local stale projection and parser repair, not new policy authority).

- [x] **REPRODUCE / ISSUE** — `python3 target/live-containment/composition-progress/assess.py`
  rc=0: actual public0 on stale2/6; six completed leaves and four live files pinned.
- [x] **ROOT CAUSE** — `python3 target/live-containment/composition-progress/qualify-before-v2.py`
  rc=0 normal/O: explicit stale1; original bare0 and copied count-loop omission0.
  Existing12 arms lack same-total/wrong-done discrimination (D60).
- [x] **FIX** — live Done/6 of 6 leaves; one discriminator added; book and
  doctrine state exact syntax/source limits and D59 priority1 ownership.
- [x] **ADDRESSED** — `python3 target/live-containment/composition-progress/check-evidence.py`
  rc=0 normal/O: seven public cases/mode; D60 copied omission0 to2/no stdout.
  `python3 target/live-containment/composition-progress/rendered.py` rc=0 normal/O:
  D61 twelve missing Foundation rows become all21 exact normal/print cells.
- [x] **NO REGRESSION** — `python3 target/live-containment/composition-progress/verify.py`
  rc=0 normal/O:106 prior entries,1404 protected regular files/Gitlink and
  complete source/book/task/guard/doctrine/live/history inverses.
  `bash target/live-containment/composition-progress/focused.sh` rc=0:
  focused12/sharder12/seven books; final make book and3244 actual links pass.
- [x] **LOCKSTEP** — live Done/6 of6 explicit leaves and derived1519 arms;
  book shows the corrected row, all Foundation cells and syntax/source limits.
  Pointer/frontier/owner schedule D59 next, then transitive reader review.

Final qualification: source9706ecb/1414 identities. All12 prior controls and
production guard source reconstruct exactly after removing the one new arm;
13 pass normal/O. Explicit stale2 of6 rejects1; corrected6 of6 passes0;
wrong-done and wrong-total reject1; later non-task ratio and history exclusion
pass0. Bare ratio remains outside current grammar, explicitly owned D59.
Copied count-loop omission passed0 before and refuses2 after through the public
self-check. Real HEAD/index/member identities remain exact across both batches.
D61 joins exactly two Foundation table breaks without changing cells; all21
rows reconcile against actual normal/print HTML. Initial inline/emphasis
instrument mismatches are retained and corrected from rendered cell evidence.
Generated index re-derives byte-exact; source wording calls a task-tree link,
not an oracle reference. The initial generated diff was reviewed before this
wording choice. Book grows58B within its unchanged bound to524259.
Whole CH706B→0293/943B/SHAe902f608386b3c2c2e8b3b8d36e0e3d28f5970236f68de8967fb0a50b37f56a2;
DEV5150B→0294/5383B/SHAa0ae173134b1d53855480fe9d3bd5adeae988d2f98a2b88e8568f76fcd4e3530.
106 prior entries/source/order/seals exact; actual old/moved/published receipt
edits plus updated digests are jointly refused.1404 protected files/Gitlink,
normal/O complete inverses, focused12/sharder12/seven books/3244 links and
literal13-control example pass. Count107/health64 debt, all caps, canonical
records, other milestones/CPU remain exact. Normal staged acceptance/seam/hooks,
exact11-file postcheck, brief0/untracked and unrestricted host0 close this unit.

### .4i2b2 — priority1 D59 source parser and bare-ratio coverage

Status: active, decomposed; .4i2b2a qualifies source/consumer defects first;
.4i2b2b repairs them in lockstep before remaining reader review.
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
No full generic Markdown coverage claim. Until this closes, explicit
A-of-B-leaves is the supported progress grammar for repaired projections.

#### .4i2b2a / SEMULITH-LC-0025 — qualify source and progress-reader boundaries

Status: complete; qualification/projection repair only. Normal COMMIT required. Owned on clean5bdaa14 after normal hooks, exact11-file
postcheck, brief0/untracked, unrestricted handoff0 and full COMMIT report.
Own target/live-containment/task-claim-inputs and a durable source-read-only
qualifier under scripts/. Pin complete immutable1416-member source and real
HEAD/index/member/mode/Gitlink state. Independently decode all33 task roots'
direct IDs/statuses, the one explicit archived whole-leaf declaration, and
exact root metadata/frontier/closed-register claims; preserve archive bodies.
Qualify explicit backtick/bold status spellings and conditional slice-gated
semantics without equating it with done. Validate the declared archived range
against actual immutable archived IDs/statuses, not the summary alone.

Run actual public TREE-CLAIMS and FRONTIER-SYNC, then isolated public truth/
falsehood cases for bold statuses, archived leaves, same-total done drift,
leading versus later ratios and punctuated closed-register claims. Derive
claims from actual source, classify only measured defects, log reproduction/
impact/priority and schedule each repair .4i2b2b before broader graph work.
Keep source/consumer code repair separate; correct proven stale live and closed
progress projections here after public qualification. No registry count, cap,
canonical record, archived body or lifecycle change in this unit. Qualify failed/malformed/duplicate/missing
inputs and copied omissions normal/O; preserve real state across every run.
Own bounded receipt/toolbox/book teaching, necessary whole-entry CH/DEV rollover,
full history/protected/source inverses, focused/seven-book/rendered/literal
checks, normal COMMIT/exact postcheck/brief0/unrestricted host0. If the task's
part limit approaches, separately own a whole closed-unit migration rather
than growing its cap. Full adoption and CPU qualification remain pending.
promotion: declined (local source assessment and producer are task artifacts, not new policy authority).

- [x] **REPRODUCE / ISSUE** — `python3 target/live-containment/task-claim-inputs/public.py`
  rc=0 normal/O:12 cases/mode; actual TREE/FRONTIER0, typed source differs.
- [x] **ROOT CAUSE** — `python3 scripts/qualify_task_claim_inputs.py` rc=0
  normal/O:33 roots/34 source pins/205 numeric declarations;14 refusals.
  Public bold/archive1, unknown0 and punctuated false count0 locate D59/D64.
- [x] **FIX** — D62/D63 live/closed projections corrected; durable qualifier/
  receipt/toolbox/book and separate D59/D64 repair owner after part containment.
- [x] **ADDRESSED** — `python3 target/live-containment/task-claim-inputs/check-evidence.py`
  rc=0 normal/O:205 IDs/34 pins,14 controls/12 public cases per mode; real state exact.
- [x] **NO REGRESSION** — `python3 target/live-containment/task-claim-inputs/verify.py`
  rc=0 normal/O:106 old entries/1406 protected/Gitlink/full inverses;
  `bash target/live-containment/task-claim-inputs/focused.sh` rc=0;12 checks,
  sharder12/seven books/3242 links/rendered/literal source replay pass.
- [x] **LOCKSTEP** — D62/D63 corrected; source tasks/archives/guard1519/caps/CPU
  exact. .4i2b2h part containment precedes D59/D64 code repair.

Source qualification: immutable5bdaa14/1416 identities, wire603ef1a2;
33 roots/34 exact source pins. Direct192 IDs plus13 actually checked archived
MODEL-METHOD IDs yield205:164 done,36 pending,2 proposed,2 active,1 slice-gated.
MODEL-METHOD19/19 differs from live18/18 (D62, priority1 this unit);
P3-BREADTH6/7 plus the conditional leaf differs from live/closed8/8 (D63,
priority1 this unit). P4 13/18 is correct; its bold status decoding is D59.
Actual public TREE/FRONTIER baselines0 normal/O, with real1416 plus owned
producer exact. Twelve cases/mode qualify bold/archive false breaches1,
unknown-status false greens0, bare/later ratios0, explicit false count1, and
D64 punctuated false closed count0 versus plain false1. D64 priority1 repair
is owned .4i2b2b; its parser requires a closing parenthesis immediately after
complete. Qualification is finite, not universal source/Markdown coverage.

#### .4i2b2h — whole closed-unit part containment before code repair

Status: complete; SEMULITH-LC-0026. Owned before mutation on clean3f08060.
Move only the contiguous eleven whole closed units .4h1–.4h6c4 (LC0011–21)
into new ordinary docs/tasks/archive/LIVE-CONTAINMENT.md. The source root is
130973B/SHA5e623c50110b7642b8b2c941f0874f7ab9d96fde4f3763c51fae7cafbbbd1fad;
selected span47486B/684LF/SHAf9f6070cd0f063126dc3753744c08e726ded2574bbdae4c1e4062934d82ed53f.
No source span byte, ordering or historical pending statement is rewritten.

Acceptance: archive copy verified before removal; complete root inverse;
retain all eleven original heading lines/anchors as links to full records;
normal mdbook before/after qualifies actual heading IDs and rendered links.
Check whole normal/print book teaching, literal ordinary read, complete old
CH/DEV entry inverses and published archive/mode preservation. Protect every
other tracked identity and opaque Gitlink; normal hooks/postcheck/brief0 and
host handoff must pass. Existing caps, count107/health64 debt and finite sealed
P4 capture stay fixed. This is ordinary partitioning, not a new seal.

The first HTML whole-file equality check found only a changed shared search-
index filename after shortening the live chapter. Preserve that raw diff;
compare complete article bytes and qualify each generated resource separately.
The selected684 lines have zero literal candidates for ](, includes, HTML
anchors/images, reference-definition prefixes, angle HTTP links and ./ paths;
that scoped scan is not a generic Markdown completeness claim.

Verification: verify.py/rendered.py/history.py rc=0 normal/O; full source,
root/book/pointer inverses,1413 protected files/modes/Gitlink and106 old history
entries exact. All eleven public mdbook heading identities and direct links
agree; complete archived article unchanged. Archive48178B/SHA
d2965e92cdf4401b7bfa7ceb839d4f29e99c6b642840f61c8360b8b4d9438762.
Two original receipt, two moved-receipt+digest and one published-receipt+digest
controls refuse jointly. CH1725B/two entries→0297/1962B/SHA
53df48d73e1a4ada66d500f46b9a3496365c1ad2047038adb06c1ae372f8fa17;
DEV2424B/one→0298/2657B/SHA
55f87049678d5226312ab8028392c0094eda2a1833f8d038ac42671ba4b2243d.
Focused12/sharder12/seven books/3242 links, complete normal/print reader teaching
and11 literal ordinary reads pass. Book gains43B→524205B; generated index stays
exact. Task family100≤107; aggregate within3145728, health64 debt unchanged.
The verifier's initial predicted book delta41B was corrected to actual43B;
retain failed output, source/book inverse and fresh generator checks qualify it.
Normal commit hooks/postcheck/brief0/host handoff complete the unit. D59/D64
code repair is next after clean COMMIT. No processor/MCU/DSP/board behavior changes.

#### .4i2b2b — repair qualified task source and mirrored progress

Status: complete; SEMULITH-LC-0027. Owned on cleanca9f0c8 after LC0026
normal hooks, exact nine-file postcheck, brief0 and host handoff0. Repair D59
and D64 through one explicit task-source reader used by both public guards:
known backtick/bold statuses, checked whole archived ranges, uniqueness and
unavailable/malformed source refusal2. Preserve the original control blocks.
Add only a leading progress ratio immediately after a known tree reference,
optionally separated by a dash or opening parenthesis; later instruction or
observation ratios remain outside that grammar. Bind each count to its own
nearest preceding tree. FRONTIER-SYNC must check parenthesized completed
counts followed by semicolon/comma annotations as well as closing parentheses.
Qualify actual source205 declarations, both public interfaces, source failures,
finite positive/negative/omission controls normal/O and unchanged history.
No universal Markdown, full graph or processor qualification claim.

Implemented: shared scripts/task_source.py reads regular UTF-8 sources once,
known backtick/bold statuses, unique declared IDs/statuses and explicit whole
archived ranges with actual completed/disjoint populations. Missing/malformed/
unavailable inputs refuse2; no summary-only archive completion. Archive paths
are normalized relative locators, with regular files/directory components;
no symlink traversal. Source metadata is checked when declared; legacy numeric
fixtures without a Tree ID retain filename binding. The source grammar covers
numeric declarations, not every heading-based nested activity.

Seventeen new source controls per consumer plus eight leading-ratio/four
annotated-count controls retain every original13/20 control. Current38/41 pass
normal/O. All recognized counts in an index cell are checked, including a
second false count after a truthful first. Ratios immediately after separate
known tree references bind independently; later instruction/observation ratios
remain excluded. Both actual public baselines0 and the same12 isolated cases/
mode agree with desired verdicts. Eleven actual predicate omissions produce38
consumer/mode discriminators (named selftest1 and default2). Eight actual root/
archive read failures each inject once, refuse2/no stdout after selftests pass.
Separate immutable LC0025 decoder agrees on33 roots/34 sources/205 declarations:164 done,
36 pending,2 proposed,2 active,1 conditional. The old guard/control inverses
are complete. Only these two imports use the new reader; neither is in the
scaffold updater's published NEUTRAL copy list; the module is project-owned.

Book proposals exceeding the unchanged aggregate cap were refused before
writing book bytes. Final teaching retains the historical command and adds both
live commands. The index generator initially found a29B Oracle/reference link
from the generic word reference; precise known-tree-ID wording removes that
lexical false topic hit. Regeneration now agrees byte-for-byte; no index edit.
D59/D64 are repaired. Full source/guard/control/book/tool/doctrine/task/pointer
inverses,1411 protected files/modes and opaque Gitlink,105 old history entries
and earlier archives/seals are exact normal/O. DEV2622B/one whole entry→0299/
2855B/SHAed596ff1cf24c437d3a293a9d4e540734f90f6141e2a1ccaff5389b85259bfce;
CH remains unsharded. Two old receipt, one moved-receipt+digest and one
published-receipt+digest controls refuse jointly. Focused12/sharder12/seven
books/3242 actual links,21 normal/print Foundation rows, complete current
explanation and three literal commands pass. Scaffold24 controls normal/O
pass. Re-derived1565 arms; all other LIVE bytes and milestones stay exact.
Book +67B→524272B, generated index exact, fixed caps unchanged.
The separate decoder shares the explicit source grammar; this is structural
reconciliation and finite discrimination, not independent semantic/oracle proof.
Normal hooks/postcheck/brief0 and host handoff complete this unit; next is
.4i2b transitive reader/index/query/generated-expansion review. Full graph/
adoption and processor qualification remain open.

Qualified code SHA256 (same bytes used by public/omission/read-fault runs):
- scripts/task_source.py:817c110bafb8da93c67e8367d54f09b81dd97fed0e95807d71964c5050d7bdf3
- scripts/check_tree_claims.sh:7db60abdcee6c7d031cc562d6091fcf8734c3d19ab743c0e92997ff6d9bfafc3
- scripts/check_frontier_sync.sh:6838534c65ff95c6d5b1b6e64e4c7ea6cea42e6b44a60c6776dea2c1acd2ffd2
Eleven copied omissions: bold alternative, known-status membership, duplicate
ID, unique status, archive population/completion/overlap, directory lstat,
leading-ratio loop, annotated-count lookahead and every-count loop. Eight
shared-reader omissions exercise both consumers; three loop/lookahead
omissions exercise their own consumer, all normal/O:19 per mode,38 total.
Each copied selftest fails1 with its named control; default refuses2. The durable
38/41 controls remain embedded in the two public scripts. Final inverse checks
caught two scratch defects: colliding governance.md capture basenames and an
unanchored frontier phrase repeated in the completion receipt. Read the two
separate immutable Git objects and anchor the whole frontier row; complete
scoped row/source inverses now pass normal/O. No project source was affected. Raw diagnostic copies
and outputs are under target/live-containment/task-source-repair; historical
retention/replay of those ignored aids is not promised. Correct independently proven
stale live/index projections without changing task source to fit a mirror.
Preserve archive immutability, source failure refusals, original controls and
non-task ratios; add discriminator/omission controls normal/O. Reconcile book,
registry-derived arms, task/pointer/frontier and normal COMMIT. Do not infer
universal Markdown or full graph coverage from these finite supported forms.

### .4i2a / SEMULITH-LC-0023 — collect closed graph inventory evidence

Status: complete; collection evidence only, semantic graph closure pending. Owned on clean28920c6 after normal hooks, exact10-file postcheck,
brief0/untracked, unrestricted handoff0 and complete COMMIT report. Fresh checked
recursive source has1411 identities,462 Markdown files and one opaque Gitlink;
source wire SHAaa328d6df30bb2b39d1491c348e88e4a666934f4db51d43d633d9571942351a2.
Existing book_navigation.py is explicitly a limited resolver, not a general
Markdown parser. Actual seven-book HTML link verification is available through
unit_books.py. Do not mistake either for complete source-graph coverage.

Own target/live-containment/graph-census, a durable source-read-only evidence collector
under scripts/, its toolbox row and bounded graph-census receipt artifact.
Qualify complete immutable source/member identities and blob reads; account for
all tracked members without opening Gitlink implementation. Inventory literal
mdBook include candidates with exact source offsets/markers, and actual rendered
local/remote/fragment links from freshly verified seven books, including print.
Pin source inputs and rendered outputs; independently reconcile the complete
output file/link population with the existing rendered verifier. Record source
Markdown outside registered book source directories and every unresolved candidate
explicitly for .4i2b, rather than silently excluding it or inventing a lifecycle.
Outside a book's source directory does not mean absent from its expanded pages.
Keep syntactic include candidates distinct from proven actual expansion.
The collector may invoke the documented mdbook build interface into a fresh
owned target directory; snapshot all source/index inputs across the build.
Inventory anchor hyperlinks separately from rendered resource candidates;
the existing verifier's hyperlink count is not resource-route coverage.

This child is collection evidence, not a generic CommonMark parser, final route
registry, utility decision or complete graph/adoption verdict. Source-only
references, read commands, generated/index/query routes, public emitted author
hints, exact terminal obligations and exclusions remain separately owned.
Do not import the neutral checker, migrate content, raise any bound, extend
sealed captures or introduce external project-owned stores.

Own deliberate failed/partial/diagnostic read and omitted member/output/link
controls normal/O; source/program/real HEAD/index/protected/mode/Gitlink pins;
whole prior CH/DEV history inverses and real damaged receipt/digest refusals;
bounded book/frontier/pointer/owner synchronization, focused/seven-book/rendered
checks and normal COMMIT/postcheck/brief0/unrestricted host0. Registry/count107,
health64 warning debt, canonical/CPU/profiles and archives remain exact.
promotion: declined (local collection evidence and its producer are owned task artifacts, not new policy authority).


Implementation: scripts/collect_containment_graph.py retains a complete source
and fresh seven-book evidence bundle. graph-census.md names the measured source,
working-view distinction, replay/refusals and exact pending review obligations.
First census:1411 identities/462 Markdown/53 include candidates;120 HTML pages/
3244 anchor occurrences (2006 fragment,1176 local,62 remote),2076 separate
resource candidates and338 paths outside book source directories. No final
semantic route/lifecycle/coverage claim.22 finite controls pass normal/O.

- [x] **REPRODUCE / ISSUE** — complete source/member and actual rendered evidence
  are inputs to .4i2; a limited link resolver cannot choose semantic routes.
- [x] **ROOT CAUSE** — `python3 target/live-containment/graph-census/check-evidence.py`
  rc=0 normal/O; source28920c6 census1411/462 and fresh seven-book120/3244
  distinguish immutable source, actual working render and pending candidates.
- [x] **FIX** — tracked collector/receipt/toolbox discovery and bounded book replay;
  .4i2b-d explicitly own transitive reader, emitted author and terminal closure.
- [x] **ADDRESSED** — `python3 target/live-containment/graph-census/verify.py`
  rc=0 normal/O: complete independent source census, actual normal/O
  collection, read/program/state/output pins, source/book/task/history inverses.
- [x] **NO REGRESSION** — `bash target/live-containment/graph-census/focused.sh`
  rc=0: focused12/sharder12/seven books/rendered/literal examples;
  every prior whole history entry, protected file/mode/Gitlink and seal exact.
- [x] **LOCKSTEP** — book/pointer/owner/artifact/toolbox agree: collection evidence
  only; .4i2b review next. Registry/caps/count107/health64 debt/LIVE/CPU unchanged.
  Normal COMMIT/postcheck/brief0/unrestricted handoff close before next child.

Final qualification: normal/O full census bytes identical, SHA
89aa869394874856c27e4416a86002a86db889e0a5092678f22e452e4c01f732.
Independent complete source1411 identities, byte-position/include/Git-grep
population and all120 per-page ordered href lists agree.22 controls plus one
copied resource append omission discriminate; three actual public CLI cases/
mode refuse2/no stdout, with real1411+three additions and old bundle exact.
All ten measured proposal bodies/modes and exact index retained against their
recorded pins before closing the task record; historical render replay is not
promised.1403 other regular files/Gitlink exact. Whole CH1190B/two entries→0292/
1427B/SHAe8249f4db35c375da0032bbd3864b8e5e99d3e4072fd0d14b1347d5f49e51c71
preserves106 prior entries; real receipt/digest refusals and full inverses pass.
Focused12/sharder12/seven books/3244 fresh+actual links, normal+print teaching
and five literal decision/contract reads pass normal/O. Book shrinks81B; every
bound and canonical/CPU/profile/seal remains fixed. Collector literal replay,
normal staged acceptance/seam/hooks/post/brief0/unrestricted host close COMMIT.

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

## Acceptance Checklist (current code unit — LIVE-CONTAINMENT.4i2b2b)

- [x] **ROOT CAUSE** — LC0025 public.py rc=0 measured D59 bold/archive
  false breaches1 and unknown-status false greens0; D64 annotated false count0.
  LC0024 source/public census rc=0 measured the stale bare progress ratio0.
  Duplicated source parsers accepted only backticks; closed regex required an
  immediate closing parenthesis. Source205 declarations/34 pins reconcile.
- [x] **ADDRESSED** — TREE-CLAIMS --self-test:38 pass /0 fail;
  FRONTIER-SYNC --self-test:41 pass /0 fail, normal/O. Same12 public cases/mode
  now return desired0/1/2; eleven actual predicate omissions across38 consumer/
  mode cases give named selftest1/default2. Eight actual read-fault cases
  refuse2/no stdout, exactly one injection each; default selftests passed.
- [x] **NO REGRESSION** — focused12/sharder12/seven books rc=0;
  rendered.py rc=0 normal/O:3242 links,21 complete Foundation table rows and
  three literal commands pass. verify.py/history.py/check-source.py rc=0:
  whole inverses,105 old entries/1411 protected files/modes/Gitlink exact.
  Scaffold24 normal/O pass; Rust/profile/canonical/frozen/archive scope exact.
  promotion: declined (the shared explicit reader and both guarded consumers
  own the repair; no new cross-cutting policy or general Markdown claim).

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
