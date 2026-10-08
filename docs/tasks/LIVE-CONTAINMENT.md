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
| 1 | `LIVE-CONTAINMENT.4` | `active` | finite archive sealed; full inventory, neutral doctrine and checker adoption remain |

## Decisions

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
