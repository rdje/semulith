# ROADMAP-V3: make the north star reachable — re-sequence, consume, resolve

## Metadata

- Tree ID: `ROADMAP-V3`
- Status: `done`
- Roadmap lane: the plan itself — `ROADMAP.md`
- Gate: none (the plan; consumed by every milestone gate downstream)
- Consumed by: the v0.4 revision at P1 first-slice completion (`decision_lane-consumption`)
- Depends on: director delegation `2026-09-27` — *"the decision is yours to make but it got
  to be sota, signoff and production-grade"*
- Unlocks: `P1-LAB` start conditions; the v0.4 revision boundary
- Created: `2026-09-27`
- Owner: repo-local workflow

## Goal

Close the gap between the milestone chain and the work actually executing. P0 closed, then
~24 consecutive work units landed in cross-cutting lanes while every milestone tree sat at
`proposed` — nothing in the plan governed that sequencing. This tree ships the fix as
`ROADMAP.md` v0.3: named start conditions for P1, a consumption rule for cross-cutting lanes,
the execution-authority contradiction resolved before P1 meets it, and P1's gate sharpened to
the star-facing proof (a *compiled* guest program under first-divergence comparison, with the
first book increment alongside).

## Non-Goals

- No change to milestone scope or gates P2–P7; multicore and DSP lanes untouched.
- No weakening of evidence or doctrine discipline — nothing above pivots the repository.
- No full-text preservation of v0.2 inside the repo: the house pattern for v0.1, plus
  `docs/provenance/planning-package-v0.2/MANIFEST.sha256` and git history, carry superseded
  versions byte-exact.

## Task Tree

- ID: `ROADMAP-V3.1` — **the execution authority: the semantics data executes**
  Status: `done`
  Goal: resolve the ARCHITECTURE.md §1.1-vs-§2 contradiction (semantics as data vs canonical
  Rust handlers) before P1 codes against either.
  Acceptance: a decision record states that P1 interprets the semantics data directly, that
  compiled/IR handlers enter only as generated, fingerprinted artifacts behind an
  observational-equivalence regression, names the Sail interpreter-first precedent and the
  revisit conditions; INDEX row added; MEMORY-ARCH doctrine green.

- ID: `ROADMAP-V3.2` — **every lane names the milestone that consumes it**
  Status: `done`
  Goal: convert the roadmap's warning sentence ("evidence tooling … does not become an
  unrelated research product") into an operational rule with a first application over the
  current lanes.
  Acceptance: decision record states the rule (consumer + latest consumption point in tree
  Metadata; no-consumer lanes descoped at revision; new lanes need a named consumer), lists
  the current lanes' consumers, and names the optional mechanical census gate as
  director-pending; INDEX row added.

- ID: `ROADMAP-V3.3` — **ROADMAP v0.3: the star gets a start condition**
  Status: `done`
  Goal: supersede v0.2 (house pattern: manifest + git carry the bytes) with the adopted
  package: P1 start condition (`SOT-FORMAT.2` + `MODEL-METHOD.10`), the lane-consumption rule
  in §1, the execution-authority row in the decision table, P1 deliverables/G1 sharpened
  (compiled freestanding guest, C-toolchain note, first book increment, `MODEL-METHOD.10`
  named as entry input), and the v0.4 trigger at P1 first-slice completion.
  Acceptance: byte ceiling 24,576 respected; v0.2 recoverable byte-exact; LIVE_STATUS
  re-derived counts corrected (the `3/10` format a gate cannot see); enforcer green.

## Current Frontier

| Order | Leaf | Status | Why next |
| --- | --- | --- | --- |
| — | — | — | the tree is complete (3/3 leaves done); its consumer is the v0.4 revision at P1 first-slice completion |

## Acceptance Checklist (leaf ROADMAP-V3.2)

- [x] **ROOT CAUSE (WHY + WHERE)** — leg 1. WHERE: the gap between the milestone chain and
  the work executing on it, counted rather than asserted:

  ```
  $ git log --format='%H %s' -1 -- docs/tasks/P0-PROFILE.md docs/tasks/P1-LAB.md docs/tasks/P2-SCALAR.md docs/tasks/P3-BREADTH.md docs/tasks/P4-SYSTEM.md docs/tasks/P5-BOARD.md docs/tasks/P6-LINUX.md docs/tasks/P7-COMPUTER.md docs/tasks/AG-OS.md docs/tasks/MC-MULTICORE.md docs/tasks/DSP-REVIEW.md
  74b081097ef0b3e04786f049006571d8cceed9a6 SEMULITH-P0-0031 (leaf P0-PROFILE.10): the profile was matched on its ISA and not its platform
  $ git log --oneline 74b0810..HEAD | wc -l
  27
  ```

  27 commits since any milestone tree was last touched — and that touch was P0 closure, not
  P1 progress. WHY severe: an unexamined default ("finish the infrastructure first") was
  spending the project's entire velocity on lanes the dependency graph never schedules against
  the star.
- [x] **ADDRESSED (verified)** — leg 2. `docs/decisions/decision_lane-consumption.md` states
  the rule (Metadata declares `Consumed by:` + latest consumption point; no-consumer lanes are
  descoped at the revision; new lanes name a consumer at proposal), applies it to all seven
  current lanes in a table, and marks the mechanical census gate as director-pending rather
  than registering it unilaterally. Existence and shape derived:

  ```
  $ grep -c '^  | ' docs/decisions/decision_lane-consumption.md
  9
  $ grep -n 'Mechanical arm' docs/decisions/decision_lane-consumption.md | head -1
  9:- **Mechanical arm:** a census gate over tree Metadata is **proposed, not yet registered**;
  ```
- [x] **NO REGRESSION** — leg 3. No source file touched; `bash scripts/check_doctrines.sh`
  reports `=== all doctrines green ===` at commit time; the schema and reader instruments
  stay green (`16 pass / 0 fail`, `18 pass / 0 fail` — same runs as leaf `.1`).
- [x] **FIX** — the decision record above; INDEX row added; `MEMORY.md` names the pending
  census gate so the proposal is not lost.
- [x] **LOCKSTEP** — `docs/decisions/INDEX.md`, this tree, `docs/TASK_TREE.md` count,
  `MEMORY.md`, `CHANGELOG.md` — one commit.

## Decisions

| Date | Decision | Rationale |
| --- | --- | --- |
| `2026-09-27` | The semantics data is the execution authority; interpreter first, compiler only as a generated, equivalence-regressed derivative | director delegation, "sota, signoff and production-grade"; record `decision_interpreter-before-compiler` |
| `2026-09-27` | Every cross-cutting lane names its consuming milestone; no-consumer lanes are descoped at the next roadmap revision | closes the sequencing vacuum measured after P0; record `decision_lane-consumption` |

## Blockers

- None.

## Acceptance Checklist (leaf ROADMAP-V3.1)

- [x] **ROOT CAUSE (WHY + WHERE)** — leg 1. WHERE: one rule set, two declared owners, side by
  side in the same contract:

  ```
  $ grep -n 'Semantics are data\|canonical Rust semantic functions' docs/ARCHITECTURE.md
  40:- **Semantics are data, cited.** `definitions/riscv/rv64i.sem.sexp` expresses each instruction's
  96:| Reference interpreter | Generated dispatch plus canonical Rust semantic functions | The functions own behavior; this backend is not an external oracle |
  ```

  and ROADMAP.md §1: *"Initial representation: Structured encoding/state/profile data plus typed
  Rust semantic functions."* WHY severe, not cosmetic: whichever of the two P1 codes against,
  the other silently becomes a second authority for the same rules — the exact failure OWN-01
  (one owned implementation per semantic rule) exists to prevent.
- [x] **ADDRESSED (verified)** — leg 2. `docs/decisions/decision_interpreter-before-compiler.md`
  decides: P1 evaluates the semantics data directly (definitional interpreter over the declared
  32 forms); compiled handlers enter only as generated, fingerprinted artifacts behind an
  observational-equivalence regression; the pinned Sail reference named as the interpreter-first
  precedent; revisit conditions stated. Existence and shape derived, not assumed:

  ```
  $ ls docs/decisions/decision_interpreter-before-compiler.md && grep -c '^## ' docs/decisions/decision_interpreter-before-compiler.md
  docs/decisions/decision_interpreter-before-compiler.md
  3
  ```
- [x] **NO REGRESSION** — leg 3. No source file touched; the instruments around the decision
  stay green:

  ```
  $ python3 scripts/check_sexp_schema.py --self-test | tail -1
  check_sexp_schema --self-test: 16 pass / 0 fail
  $ python3 scripts/sexp.py --self-test | tail -1
  sexp --self-test: 18 pass / 0 fail
  ```

  and `bash scripts/check_doctrines.sh` reports `=== all doctrines green ===` at commit time.
- [x] **FIX** — the decision record above; INDEX row added; no source file modified.
- [x] **LOCKSTEP** — `docs/decisions/INDEX.md`, this tree, `docs/TASK_TREE.md` row, `MEMORY.md`
  pointer, `CHANGELOG.md` entry — staged together, verified by `git status --short` naming
  exactly these paths plus the record.

## Acceptance Checklist (leaf ROADMAP-V3.3)

- [x] **ROOT CAUSE (WHY + WHERE)** — leg 1. WHERE: the three gaps in the plan itself, each
  named where v0.2 left it: (a) P1 had no start condition — `git show 4b2fbb1:ROADMAP.md`
  (the tree before this leaf) is the v0.2 text, and
  `git show 4b2fbb1:ROADMAP.md | grep -c 'Start condition'` prints `0`; (b) no sequencing rule for
  cross-cutting lanes (the §1 consumption rule's absence, counted in leaf `.2`); (c) two
  unreconciled execution authorities (leaf `.1`'s grep — `docs/ARCHITECTURE.md:40` vs `:96`).
  WHY severe: the star was unreachable not because any milestone was wrong, but because
  nothing in the plan decided when the first one could start.
- [x] **ADDRESSED (verified)** — leg 2. `ROADMAP.md` is v0.3: the start condition lives in the
  P1 section, the consumption rule and the execution-authority table row in §1, the sharpened
  G1 and the v0.4 trigger in §6/§7 — and both decision records are cited from the plan:

  ```
  $ grep -ci 'start condition' ROADMAP.md
  2
  $ grep -c 'decision_lane-consumption\|decision_interpreter-before-compiler' ROADMAP.md
  2
  $ wc -c < ROADMAP.md
  24065
  ```

  24,065 bytes against the 24,576 registry ceiling, and v0.2 stays recoverable byte-exact:
  `docs/provenance/planning-package-v0.2/MANIFEST.sha256` still carries its delivered hash and
  `scripts/check_delivery_provenance.sh` reports `3 live row(s) declared` with no breach.
- [x] **NO REGRESSION** — leg 3. `LIVE_STATUS.md`'s ungated count corrected while under review:
  the `MODEL-METHOD` row read `3/10` (a spelling no gate re-derives; the tree is at 6 of 13)
  and now states `6 of 13` in the gated form. `bash scripts/check_doctrines.sh` reports
  `=== all doctrines green ===` at commit time.
- [x] **FIX** — the v0.3 rewrite (this commit) plus the LIVE_STATUS correction and the
  `MEMORY.md` pointer; no source file modified.
- [x] **LOCKSTEP** — `ROADMAP.md`, this tree, `docs/TASK_TREE.md` row, `MEMORY.md`, `CHANGELOG.md`,
  `LIVE_STATUS.md`, `DEV_NOTES.md` — one commit.

## Routing evidence

- `2026-09-27`: while adopting `.3`, measured a status anomaly in `SOT-FORMAT.10` — its
  acceptance checklist is fully ticked and its commit (`SEMILITH-SF-0056`) is recorded, yet the
  leaf's `Status:` line reads `active`, so every derived count counts it not-done. WHERE:
  `docs/tasks/SOT-FORMAT.md`, leaf `.10` Status field. Routed to `SOT-FORMAT.2`'s lockstep
  (the next leaf that legitimately opens that tree's file). Reproduces outside the family:
  yes — the class is general (any leaf can tick boxes while its Status line lags, and no
  standing check compares the two); the durable fix is the proposed LEAF-CLOSURE census
  (director-pending, announced `2026-09-27`), which would refuse exactly this shape at
  commit time.

## Verification Log

| Date | Leaf | Checks | Result |
| --- | --- | --- | --- |
| `2026-09-27` | `ROADMAP-V3.1` | `bash scripts/check_doctrines.sh` | all doctrines green (pre-staging) |
| `2026-09-27` | `ROADMAP-V3.2` | `bash scripts/check_doctrines.sh` | `=== all doctrines green ===` at commit time |
| `2026-09-27` | `ROADMAP-V3.2` | vacuum re-derived: `git log --oneline 74b0810..HEAD \| wc -l` | `27` commits since any milestone tree was touched |
| `2026-09-27` | `ROADMAP-V3.3` | `wc -c < ROADMAP.md` | `24065` ≤ `24576` ceiling; delivery-provenance `3 live row(s) declared` |
| `2026-09-27` | `ROADMAP-V3.3` | `bash scripts/check_doctrines.sh` | `=== all doctrines green ===` at commit time |

## Commit Log

| Leaf | Commit subject or reference | Notes |
| --- | --- | --- |
| `ROADMAP-V3.1` | `SEMULITH-RM-0057 (leaf ROADMAP-V3.1): the semantics data is the execution authority` | decision record + tree registered |
| `ROADMAP-V3.2` | `SEMILITH-RM-0058 (leaf ROADMAP-V3.2): every lane names the milestone that consumes it` | decision record + INDEX row; census gate proposed to the director, not registered |
| `ROADMAP-V3.3` | `SEMILITH-RM-0059 (leaf ROADMAP-V3.3): ROADMAP v0.3 — the star gets a start condition` | v0.3 supersedes v0.2; LIVE_STATUS `6 of 13` correction; tree complete 3/3 |

## Changelog

- `2026-09-27`: Created under director delegation; the reachability package adopted as v0.3.
