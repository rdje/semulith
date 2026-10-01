# BOOK-APPARATUS: the project book carries a glossary, annexes, and an index

## Metadata

- Tree ID: `BOOK-APPARATUS`
- Status: `active`
- Roadmap lane: cross-cutting — the mdBook is the project's review surface (session-directive §7;
  `README.md` routes `docs/book/` as "the reviewable narrative surface")
- Gate: none of its own beyond the doctrine it registers (`BOOK-INDEX`)
- Created: `2026-10-02`
- Owner: repo-local workflow

## Goal

The director's directive (`2026-10-02`): keep the roadmap, the codebase, and the mdBook in
lockstep — and make sure the book has a **glossary**, **annexes**, and an **index**, where the
annexes hold what is too technical to reasonably put in a normal chapter. Deliver the missing
apparatus in the house style: derived where derivable, gated so it cannot rot, and recorded so
the policy survives the session.

## Non-Goals

- No re-organization of existing chapters into/out of annexes — the two current annexes already
  match the directive's definition (assembler internals; the step-by-step first-model build). A
  content audit of "what else is too technical" is a separate, larger judgement, not this slice.
- No generated back-of-book index for the per-unit model books (`docs/models/*`) — the directive
  names the project book; the unit books have their own governed structure (`MATERIALS-BILL`).

## Acceptance Criteria

1. The book's `SUMMARY.md` offers a Glossary, an Annexes section, and an Index, and
   `mdbook build docs/book` passes.
2. The index is **generated** from the book's own text and the canonical glossary, and a
   registered doctrine (`BOOK-INDEX`) refuses drift — a hand-maintained index would be a running
   total, not a measurement.
3. The annex policy (too technical for a normal chapter → annex) is stated in the book itself.
4. The new gate ships a `--self-test` whose RED arms were observed failing before registration,
   and every mirror (`DOCTRINE_ENFORCEMENT.md`, `docs/book/src/working/doctrines.md`,
   `TOOLBOX.md`) is updated in the same commit.

## Task Tree

- ID: `BOOK-APPARATUS`
  Status: `active`
  Goal: the project book carries a governed glossary, annexes, and index
  Children: `BOOK-APPARATUS.1`, `BOOK-APPARATUS.2`

- ID: `BOOK-APPARATUS.1` — **the index, generated and gated; the annex policy stated**
  Status: `done` (`2026-10-02`)
  Goal: survey the existing apparatus (glossary: `docs/book/src/glossary.md` includes the
  canonical `docs/GLOSSARY.md` verbatim — in sync by construction; annexes: two chapters that
  already match the directive's definition; index: ABSENT — the measured gap); build
  `scripts/gen_book_index.py` + `scripts/check_book_index.sh`; generate
  `docs/book/src/index.md`; state the annex policy in the book; register and mirror the gate.
  Acceptance: `mdbook build docs/book` passes with all three apparatus entries; the gate is
  green, registered, mirrored, and its RED arms were fired before registration; `make gate`
  green.
  Verification: `2026-10-02` — all in the Verification Log below.
  Commit: `pending`
  `promotion: declined (per-slice history; the durable halves are the BOOK-INDEX doctrine row
  and decision_mdbook-incremental-engaging, both retrievable already).`

- ID: `BOOK-APPARATUS.2` — **the reading-experience audit pass**
  Status: `pending`
  Goal: apply `decision_mdbook-incremental-engaging` (director, `2026-10-02`) to the existing
  chapters: every chapter builds only on what earlier chapters established, motivation comes
  before mechanism, a term is introduced before it is leaned on, and what is too technical for
  the main line lives in an annex. Audit first (a per-chapter disposition recorded here), then
  revise what the audit flags — one measured pass, not a taste-driven rewrite.
  Acceptance: every chapter has a recorded disposition (`kept` / `revised`, each revised one
  naming what violated the record and the fix); the book builds; the index regenerates clean.
  Verification: `pending`
  Commit: `pending`

## Current Frontier

| Order | Leaf | Status | Why next |
| --- | --- | --- | --- |
| 1 | `BOOK-APPARATUS.2` | `pending` | `.1` closed the measured gap (the index); `.2` applies the director's reading-experience record to the chapters that predate it |

## Decisions

- `2026-10-02`: the index is **derived, never handwritten**. A curated index is a fact about the
  book's text maintained by memory — the same failure `DERIVED-COUNTS` was founded on (a running
  total is a memory of a measurement, not a measurement). The generator reads `SUMMARY.md` (the
  chapter set and its order), `docs/GLOSSARY.md` and the acronym table (the term set), and the
  chapter texts (the occurrence set); the gate re-derives and refuses drift.
- `2026-10-02`: index granularity is the **chapter**, not the section. Chapter-level "discussed
  in" links are stable against section renames and honest about what the generator can vouch for.
- `2026-10-02` (director): the book **builds up incrementally and keeps both audiences
  reading** — not too dry for students/newcomers, not too slow or boring for experts. Recorded
  durably as `decision_mdbook-incremental-engaging`; `.2` owns the first audit pass.
- `2026-10-02` (director): the TOC request was **withdrawn** on confirmation that mdBook renders
  a table of contents from `SUMMARY.md` (the sidebar, present in every build). A separate
  in-book contents page was built, shown, and reverted as redundant — the sidebar is the TOC.

## Open Questions

- Do the per-unit model books want the same apparatus? Deferred — the directive names the
  project book; if the answer becomes yes, a new leaf generalizes the generator.

## Blockers

- None.

## Acceptance Checklist (filled per leaf at execution time)

`BOOK-APPARATUS.1` (`2026-10-02`):

- [x] **ROOT CAUSE (WHY + WHERE)** — the director's `2026-10-02` apparatus directive against the
  measured state: the glossary exists and cannot fork (`docs/book/src/glossary.md` splices the
  canonical `docs/GLOSSARY.md` at build time via `{{#include}}`), two annexes exist and match
  the directive's definition, and the **index is absent** — `grep -ci index
  docs/book/src/SUMMARY.md` → `0`. WHERE: no generator, no gate, no `index.md`, and no
  stated annex policy — a book whose only apparatus was prose someone remembered to keep.
- [x] **ADDRESSED (verified)** — before → after, measured:

  ```
  $ python3 scripts/gen_book_index.py
    gen_book_index: wrote docs/book/src/index.md (15019 bytes, 40 indexed terms)
  $ mdbook build docs/book                     -> INFO HTML book written …  rc 0
  $ bash scripts/check_book_index.sh           -> BOOK-INDEX: ok (… 40 table rows)
  ```

- [x] **NO REGRESSION** — the enforcer re-run after staging; the new gate's self-test fired
  RED **before** registration (6 arms, each asserting the reason as well as the verdict —
  hand-edit DRIFT, stale-behind-chapter-edit DRIFT, missing chapter and missing SUMMARY
  refused by name):

  ```
  $ bash scripts/check_book_index.sh --self-test   -> BOOK-INDEX --self-test: 6 pass / 0 fail
  $ bash scripts/check_doctrines.sh                -> === all doctrines green ===
  ```

  A defect the build itself exposed was fixed at root, not reported: the generator's own
  printed term count read `47` against the real `40` (a fudge-factor count, not a
  measurement) — corrected to derive the count from the emitted rows and re-verified.

- [x] **FIX** — `scripts/gen_book_index.py` (generator; refuses by name what it cannot emit),
  `scripts/check_book_index.sh` (the `BOOK-INDEX` gate), `docs/book/src/index.md` (generated),
  `SUMMARY.md` + `introduction.md` (the index entry and the stated annex policy), registration
  in `scripts/check_doctrines.project.sh`, mirrors in `DOCTRINE_ENFORCEMENT.md` /
  `docs/book/src/working/doctrines.md` / `TOOLBOX.md`, the owner→mirror row in
  `doctrine/fact_ownership.tsv`.
- [x] **LOCKSTEP** — tree (leaf + checklist + logs), `docs/TASK_TREE.md` row,
  `LIVE_STATUS.md` (31 doctrines / 329 arms / 33 chapters — re-derived, not incremented),
  `CHANGELOG.md`, `DEV_NOTES.md`, `MEMORY.md`; `docs/decisions/` gained
  `decision_mdbook-incremental-engaging` (+ INDEX row) for the second half of the directive.
  `promotion: declined (per-slice history; the durable halves are the BOOK-INDEX doctrine row
  and decision_mdbook-incremental-engaging, both retrievable already).`

## Verification Log

| Date | Leaf | Checks | Result |
| --- | --- | --- | --- |
| `2026-10-02` | `.1` | `gen_book_index.py` → wrote index.md (15019 B, 40 terms); `mdbook build docs/book` rc 0; `check_book_index.sh` → ok; `--self-test` 6/6 (RED arms fired before registration); `check_doctrines.sh` all green | the index exists, is generated, and is gated; the annex policy is stated in the book's introduction; glossary/annexes verified present and on-policy |

## Commit Log

| Leaf | Commit subject or reference | Notes |
| --- | --- | --- |
| `.1` | `SEMULITH-BA-0001 (leaf BOOK-APPARATUS.1): the book's index — generated from the book's own text, gated against drift; the annex policy stated` | generator + BOOK-INDEX gate (6 self-test arms, fired RED before registration); index.md; SUMMARY + introduction; registration + all mirrors + fact-ownership row |

## Changelog

- `2026-10-02`: Created from the director's `2026-10-02` directive (glossary, annexes, index —
  annexes for what is too technical for a normal chapter). Survey measured: glossary present and
  in sync by construction (`{{#include ../../GLOSSARY.md}}`), two annexes present and on-policy,
  the index absent — `.1` owns closing that gap.
- `2026-10-02`: `.1` done: the index lands generated and gated (`BOOK-INDEX`, the 31st project
  doctrine). Mid-leaf the directive grew twice and both halves were recorded: the
  reading-experience direction → `decision_mdbook-incremental-engaging` + `.2`; the TOC request
  → withdrawn by the director (the mdBook sidebar IS the TOC; the built contents page was
  reverted as redundant).
