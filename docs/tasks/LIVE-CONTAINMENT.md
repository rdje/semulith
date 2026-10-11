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
| 1 | `LIVE-CONTAINMENT.4` | `active` | D52 repaired; .4h4 D51 capacity review, then full inventory and checker adoption |

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
.4h3/LC-0013 inventory-read repair is complete; .4h4 D51 review is next.

### .4h1 / SEMULITH-LC-0011 — contain duplicated decision-index summaries

Status: complete. Owned on clean42dd68f after exact10-file commit verification,
brief0/untracked and unrestricted handoff0, before edits or scratch writes.
The decisions family is60files/261604B under262144B (540B room); INDEX.md is
16379/16384B (5B room). Do not add an authority record into that pressure or
raise either cap. Four task-family and one changelog-family index rows duplicate rationale and historical
numbers in their linked canonical records; all five records have been read in
full. Compare every removed clause with its authority before demotion and
retain D51's source-classification correction for .4h2; no unique detail may be
removed or a faulty authority hidden. Leave the D51-affected count record's row
exact until .4h2 repairs its authority. Replace only the other five navigation rows
with dated topic labels and reader questions, retaining targets/types/order,
all other index bytes, all canonical records and the complete membership set.

Own target/live-containment/decision-index, immutable source/row/authority
mapping, complete index inverse, source-clause checks, focused checks and seven
books. Update the existing book's navigation teaching with a worked read example;
retain all other book bytes. Own necessary whole-oldest CH/DEV rollover before
new receipts, full-source/head reconstruction, earlier seals/manifest prefix,
real receipt+digest refusal controls, protected file/mode/Gitlink proof and COMMIT.
Existing caps, CPU/canonical/qualification and LIVE stay exact. Full containment
inventory/checker remains LC.4; no new decision or count raise in this slice.
promotion: declined (canonical records already own the demoted details).

- [x] **ROOT CAUSE** — `python3 target/live-containment/decision-index/verify.py`
  rc=0: source INDEX16379/16384B; family261604/262144B. Five old summaries
  repeat15 located clauses in complete linked records; D51's row is excluded.
- [x] **ADDRESSED** — verify.py normal/O rc=0: INDEX15656B,723B freed;
  complete index/book inverses, every target/type/order and all five source
  identities exact. Decision family260881B; no cap or canonical-record change.
- [x] **NO REGRESSION** — history.py/verify.py/rendered.py normal/O and
  focused.sh rc=0: all101 prior entries/complete heads/seals retained; genuine
  head/moved/published receipt+digest controls refuse jointly. Focused12/
  sharder12/seven books/3238 links, complete normal+print teaching/two literal
  examples and1387 protected regular files/Gitlink exact; LIVE/CPU unchanged.
- [x] **LOCKSTEP** — current navigation/book/pointer/frontier and this owner
  agree. Whole DEV6957B→0280 (7190B SHA b0df3588) and CH1398B→0281
  (1635B SHA4e913b3d); manifest prefix exact,73live+210sealed283logical.
  Source EOF blank runs retained; only0280:100/0281:27 whitespace notices,
  complete inverses prove the runs. COMMIT precedes .4h2/D51 capacity review.

### .4h2 / SEMULITH-LC-0012 — qualify capacity inputs before authority review

Status: assessment complete; D52 fixed/verified by .4h3 below. Owned on clean85fe189 after exact9-file commit verification,
brief0/untracked and unrestricted handoff0, before edits or scratch writes.
Read the route checker's family listing/count/aggregate/per-part paths and all
relevant count/size decisions. Qualify successful and failed inventory reads
through the public checker CLI before relying on its boundary results. Source
inspection shows three pipeline consumers of family_files; status propagation
needs an actual controlled test, not an inferred verdict. Own
target/live-containment/capacity-inputs, a narrowly scoped Git facade delegating
all other real reads, project-local scratch/cleanup, literal CLI invocations,
status/stdout/stderr receipts and before/after real HEAD/index/tracked-file proof.
Do not change any ceiling, authority record, canonical input or checker behavior
before classifying this diagnostic. If it accepts a failed/partial inventory,
log/own that defect with root cause and priority, complete this finite assessment
and repair it in the next owned slice before the count decision. Otherwise own
the revision-pinned expansion/boundary review on clean committed state.
Sync the actual result and reproduction in the book/live owner, preserve whole
prior history and other files/modes/Gitlink, run focused/book checks and COMMIT.
D51 remains .4h's priority2 correction; full containment inventory/checker
adoption remains .4. No count raise is authorized by this assessment slice.
promotion: declined (a measured publishing-boundary assessment; repair owns controls).


D52 reproduction and ownership (2026-10-11, priority1): at85fe189 the literal
`bash scripts/check_readme_routes.sh` returns0 and prints
`README-ROUTING-CLOSURE: ok (39 governed destination(s))` when a PATH-selected
Git facade fails exactly `git -C <runtime-root> ls-files -- docs/tasks/`.
The facade delegates every other invocation to the real Git executable. Case1
prints `capacity controlled inventory failure` to stderr and exits73 with no
stdout. Case2 prints `docs/tasks/P4-SYSTEM.md` plus LF to stdout, writes
`capacity controlled partial inventory` to stderr and exits0. Baseline delegates
normally: status0, empty stderr and the same green banner. Each case intercepts
three listings. Both failed/partial cases are falsely green; this assessment
does not claim the entire doctrine enforcer accepts a globally failing Git.

Root cause: family_files feeds unchecked count/aggregate/per-part pipelines in
verify_routes; their read failures do not set bad. stderr is diagnostic only,
and the aggregate cat suppresses read errors. A capacity decision cannot use
this result as proof of a complete measured family. .4h3 owns repair and
permanent failed/partial/read controls next, before any D51 count remedy.

Evidence: target/live-containment/capacity-inputs/assess.py and result.json;
per-case stdout/stderr/trace, immutable before.json/after.json. Before/after
HEAD85fe189, index SHA and all1397 tracked byte/mode/Gitlink identities match.
The controlled checker SHA is
`e0b023586154ec4545763abf61b0c874b170ef73aa183c1f4671490c735033dc`; facade SHA and complete receipt digests are in result.json.
All scratch is project-local; no checker, ceiling, authority or index changed.

### .4h3 / SEMULITH-LC-0013 — refuse unmeasurable family inventories

Status: complete; D52 fixed/verified. Owned on clean403595f after exact6-file postcheck, brief0,
unrestricted handoff0 and the complete COMMIT report. D52 priority1 blocks D51
capacity review. Repair only the existing route checker's family measurement:
one successful, stderr-free NUL Git inventory, validated unique family-relative
paths and regular project-local members, then one measured size table for all
three ceilings. Failed/diagnostic/malformed listings or member measurements refuse
with status2 and no green banner. Preserve ordinary health/ceiling verdicts,
derived-member exemptions, all original17 controls, current ceilings, authority
records, sealed and ordinary archives, and CPU/qualification state.

Own target/live-containment/capacity-repair, source/checker inverses, independent
Git-facade CLI controls, new permanent boundary/failure controls, normal/O runs,
complete history/head/protected-mode/Gitlink checks, focused checks/seven books
and any whole-oldest rollover needed before receipts. Sync tool/doctrine/book
descriptions and the generated keyword index, derived arm count, LIVE's actual
repair status and resume pointer.
No new neutral checker or limit decision in this slice. After verified COMMIT,
resume D51 capacity review; full containment inventory/adoption remains LC.4.
promotion: declined (the existing route checker and permanent controls own the repair).


- [x] **REPRODUCE / ISSUE** — LC-0012's public CLI receipts on85fe189
  falsely return0 for failed73 and partial-with-stderr listings; owning .4h2
  retains the selective facade recipe and pinned checker/source identities.
- [x] **ROOT CAUSE** — `python3 target/live-containment/capacity-inputs/assess.py`
  rc=0 on85fe189: all three cases return0, three listings each, unchanged
  real HEAD/index/all1397 identities. Unchecked family_files pipelines discard
  inventory failures and never set verify_routes' bad verdict.
- [x] **FIX** — family_measure validates one NUL listing and member sizes;
  every family bound consumes that table. Failed metadata/listing reads refuse2.
- [x] **ADDRESSED** — capacity-repair/assess.py rc=0 normal/O: public
  baseline0, failed73→2 and partial+stderr→2; one listing each, no failed-run
  stdout/green banner. Real HEAD/index/all1397 tracked identities stay exact.
- [x] **NO REGRESSION** — focused.sh/history.py/checker-inverse.py/rendered.py
  rc=0: original17 plus15 controls,32/0 normal/O; nine omission variants
  discriminate normal/O. Complete checker/book/task/head inverses,101 prior
  entries and1383 protected regular files/Gitlink exact. Focused12/sharder12/
  seven books/3242 links; full normal+print teaching and two literal commands
  pass. Existing ceilings, authorities, archive bodies and CPU state exact.
- [x] **LOCKSTEP** — tool/driver/doctrine/book/index/pointer agree; derived
  arms1456 and LIVE routing closure Done reflect the verified repair. CH two
  whole oldest entries1382B→0282/1619B/SHA03abd6f7;74live+210sealed284logical,
  old manifest prefix exact. D51 capacity review next; full adoption remains .4.


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
