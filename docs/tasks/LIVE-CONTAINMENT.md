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
- Not the append-history families (`CHANGELOG.md`, `DEV_NOTES.md`): their shard transition
  exists and works (`DOC-SHARDING`).

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
  Status: `pending`
  Goal: `TOOLBOX.md` (20,478 / 20,480 B) and `DOCTRINE_ENFORCEMENT.md` (32,669 / 32,768 B) —
  both "one row per" normative tables — are partitioned behind a bounded index (the book's
  `partitioned` precedent), so the next tool or doctrine can be registered.
  Acceptance: both below their health targets; REGISTRY-MIRROR, MEMORY-ARCH and
  README-ROUTING-CLOSURE green; no row lost (an enumerated before/after census).
  Verification: pending
  Commit: pending

- ID: `LIVE-CONTAINMENT.4` — **adopt the live-document containment doctrine**
  Status: `proposed`
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
| 1 | `LIVE-CONTAINMENT.3` | `pending` | the next registered tool or doctrine cannot fit; due before `P4-SYSTEM.7` slice (c5) |
| 2 | `LIVE-CONTAINMENT.4` | `proposed` | the README policy's own trigger has fired (CHANGELOG/DEV_NOTES shards, the P4 tree archive, the book partition — 2026-10-06 alone) |

## Decisions

- `2026-10-06` (measured before opening): the drifts were found while registering
  `CITATION-QUOTES` (`SEMULITH-CA-0001`) — the Knowledge Map's subsystem paragraph names
  `crates/app/` (`ls crates/` → `semulith-cli semulith-core semulith-dsp56300
  semulith-verify`; no `app`), and three governance surfaces finished that commit within
  0.1–0.3 % of their ceilings after their new rows were tightened to fit. Tightening wording
  to pass a cap is the guide's named anti-pattern; this tree owns the real answer.

## Open Questions

- Does `.3` adopt the full checker package (`live-document-size/` in the donor) or map its
  contracts onto the existing README-ROUTING-CLOSURE registry? Measured at `.3`.

## Blockers

- None.

## Acceptance Checklist (required for any leaf that lands a CODE change)

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


## Verification Log

| Date | Leaf | Checks | Result |
| --- | --- | --- | --- |
| `2026-10-06` | `.2` | the three drifts measured (crates/app absent; the scaffold header; the 16,228-byte note); each corrected text checked against `ls crates/`, the CLI's subcommand match, `ls profiles/`; the map regenerated | **met** — the orientation sources state today's repository |
| `2026-10-06` | `.1` | the registry control vs the index census (22 of 31 rows completed); the CLOSURE rule that forbade obeying it; FRONTIER-SYNC extended (20/20; RED on the real pre-move index: 22 COMPLETED IN INDEX); the verbatim move; the register registered; the book's live includes | **met** — the index holds open trees only (4,053 B); completed trees have a gated home |

## Commit Log

| Leaf | Commit subject or reference | Notes |
| --- | --- | --- |
| `.2` | `SEMULITH-LC-0002 (leaf LIVE-CONTAINMENT.2): the stale orientation sources corrected — the knowledge map's subsystems, the workspace header, the README policy's measurements` | three drifts; the policy decision untouched |
| `.1` | `SEMULITH-LC-0001 (leaf LIVE-CONTAINMENT.1): the closed-tree register — completed trees leave the index (22 rows moved verbatim), FRONTIER-SYNC gates both files` | the control applied and enforced; the index 8,172 → 4,053 B |

## Changelog

- `2026-10-06`: `.2` done (`SEMULITH-LC-0002`) — the orientation map names the real crates and
  subsystems; the scaffold header and the policy note's stale measurements corrected.
- `2026-10-06`: `.1` done (`SEMULITH-LC-0001`) — completed trees leave the index: 22 rows
  moved verbatim into `docs/TASK_TREE_CLOSED.md`, FRONTIER-SYNC gates both files.
- `2026-10-06`: Created after `SEMULITH-CA-0001` measured the stale orientation map and the
  three governance surfaces at their ceilings.
