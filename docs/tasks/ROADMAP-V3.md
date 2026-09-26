# ROADMAP-V3: make the north star reachable — re-sequence, consume, resolve

## Metadata

- Tree ID: `ROADMAP-V3`
- Status: `active`
- Roadmap lane: the plan itself — `ROADMAP.md`
- Gate: none (the plan; consumed by every milestone gate downstream)
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
  Status: `pending`
  Goal: convert the roadmap's warning sentence ("evidence tooling … does not become an
  unrelated research product") into an operational rule with a first application over the
  current lanes.
  Acceptance: decision record states the rule (consumer + latest consumption point in tree
  Metadata; no-consumer lanes descoped at revision; new lanes need a named consumer), lists
  the current lanes' consumers, and names the optional mechanical census gate as
  director-pending; INDEX row added.

- ID: `ROADMAP-V3.3` — **ROADMAP v0.3: the star gets a start condition**
  Status: `pending`
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
| 1 | `ROADMAP-V3.2` | `pending` | the consumption rule is a stated precondition of the v0.3 text |
| 2 | `ROADMAP-V3.3` | `pending` | the revision folds both records in |

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

## Verification Log

| Date | Leaf | Checks | Result |
| --- | --- | --- | --- |
| `2026-09-27` | `ROADMAP-V3.1` | `bash scripts/check_doctrines.sh` | all doctrines green (pre-staging) |

## Commit Log

| Leaf | Commit subject or reference | Notes |
| --- | --- | --- |
| `ROADMAP-V3.1` | `SEMULITH-RM-0057 (leaf ROADMAP-V3.1): the semantics data is the execution authority` | decision record + tree registered |

## Changelog

- `2026-09-27`: Created under director delegation; the reachability package adopted as v0.3.
