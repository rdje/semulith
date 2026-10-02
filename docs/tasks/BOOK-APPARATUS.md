# BOOK-APPARATUS: the project book carries a glossary, annexes, and an index

## Metadata

- Tree ID: `BOOK-APPARATUS`
- Status: `done` (`2026-10-02` — both leaves complete)
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
  Status: `done` (`2026-10-02`, `SEMULITH-BA-0002`)
  Goal: apply `decision_mdbook-incremental-engaging` (director, `2026-10-02`) to the existing
  chapters: every chapter builds only on what earlier chapters established, motivation comes
  before mechanism, a term is introduced before it is leaned on, and what is too technical for
  the main line lives in an annex. Audit first (a per-chapter disposition recorded here), then
  revise what the audit flags — one measured pass, not a taste-driven rewrite.
  Acceptance: every chapter has a recorded disposition (`kept` / `revised`, each revised one
  naming what violated the record and the fix); the book builds; the index regenerates clean.
  Verification: `2026-10-02` — all in the Verification Log below.
  Result (`2026-10-02`): the audit ran as six parallel read-only chapter reviews against the
  decision's four operationalized criteria (incremental build-up; motivation before mechanism;
  layered density; both-audiences engagement), every flagged item re-verified against the
  repository by the signing engineer before any edit. 29 main-line chapters audited (the annexes, glossary and index are the apparatus itself):
  **16 kept, 13 revised** — and the audit's sharpest yield was **factual drift**, not style:
  the book had gone stale against the repository in a dozen places (the audit class the
  decision's "every new or revised chapter is reviewed" rule exists to catch). Three of the
  flagged documents proved **frozen-in-place** (the doctrine refused their staged edits by
  name — measured, then reverted): their corrections landed in the live orientation
  chapters, and the leaf records the tension honestly — a frozen v0.2 record rendered into
  a live book will drift again; the orientation note is the containment, unfreezing is a
  provenance decision above this leaf's authority.

  **Per-chapter dispositions** (each revised chapter: what violated, and the fix):

  | Chapter | Disposition | What violated → the fix |
  | --- | --- | --- |
  | `introduction.md` | kept | — |
  | `claim-scope.md` | revised | drift: "three-crate" → four (measured `crates/`); the same page said CPU-LAB "HAS run … incomplete" and "has not run" → the gate ran, verdict `incomplete`, stated once; the corpus was 40 programs/"forty-one" → 48 assembled + 1 compiled = 49 (measured: 49 `.expected.sexp`) |
  | `status.md` | kept | the include is live by construction; the staleness it rendered was LIVE_STATUS.md's, fixed there ("1 unit today" → 5) |
  | `models.md` | kept | — (the five-unit update landed with P5-BOARD.11) |
  | `models/the-information-a-unit-demands.md` | revised | criterion 1: findings F3/F6 leaned on with no source named → each names `docs/tasks/DSP-REVIEW.md`; CLINT unexpanded → glossed; drift: "the two units this project has actually built" → the device units and the board are named as registered (their per-category demand is their dossiers' own) |
  | `plan/overview.md` | revised | criterion 4: the "closes exactly what it says" sentence was stated twice in three lines → the first instance dropped, the punchline kept |
  | `plan/p0.md` | revised | drift: the contract quoted 33 obligations/66 checks where the regenerated G0-REPORT reads 36/72 — the quote contradicted the tracked report it claims to quote → updated, with the growth since P0 noted in the narrative |
  | `plan/p1.md` | revised | drift: G1 "verdict today is incomplete … owned by P2-SCALAR.5" → P2-SCALAR.5 landed; now the at-first-run verdict plus the closure (G1 `passed` 2026-09-30); "forty guests, 492 steps" → 48/642; criterion 1: the P3-BREADTH.5 forward reference now names its chapter |
  | `plan/p2.md` | kept | — (verified: every count matches the P2 records) |
  | `plan/p3.md` | revised | criterion 3: one list item had accreted ~68 lines of dated leaf-by-leaf update chain — a campaign log in the main line → collapsed to a final-state paragraph keeping the two measured incidents (the five naive-FM divergences; the seven latent references.sexp defects) and pointing at the tree for the blow-by-blow |
  | `plan/p4.md` | kept | — |
  | `plan/p5-p7.md` | revised | drift: registration day `.11` framed as future → done `2026-10-02`, `.3`/`.4` named as the remaining pre-gate work; criterion 2: P7's cold mechanism open → one why-sentence ("validated parts, not a computer") |
  | `plan/multicore.md` | kept | — |
  | `contracts/method.md` | kept | — |
  | `contracts/rules.md` | kept | — |
  | `contracts/architecture.md` | revised | drift in the included doc: 26/34/26 → 28/36/28 records (measured against `profiles/rv64i-lab-v0/`); the ` ```mermaid ` block rendered as raw source in the book (no preprocessor) → a text-rendered flow, no new dependency |
  | `contracts/cpu-environment.md` | kept | — |
  | `contracts/evidence-and-gates.md` | kept | — |
  | `contracts/archogen.md` | revised | the same raw-mermaid defect — but the included doc is FROZEN (the doctrine named it `DRIFTED (frozen-in-place)` when an edit was staged) → the source stands; the orientation carries the flow in one sentence |
  | `contracts/information-catalog.md` | kept | — |
  | `contracts/risks.md` | revised | drift in the included register's current-state column — and the register is FROZEN (the doctrine refused the staged edit by name) → the source stands as the v0.2 record; the orientation now date-scopes it and routes the reader to the live status chapter (the four stale rows named there) |
  | `contracts/sources.md` | revised | drift in the included v0.2 record ("proposals, not created packages"; "no … repository … reserved") — the record is FROZEN → the source stands; the orientation carries the dated correction (the crates exist; only crates.io/domain/trademark remain unreserved) |
  | `contracts/review-disposition.md` | kept | — (a frozen, dated record; staleness is its nature) |
  | `data/overview.md` | revised | criterion 2: cold mechanism open → one why-sentence first ("a claim must be data a checker can refuse") |
  | `data/worked-example.md` | kept | — |
  | `working/task-trees.md` | kept | — |
  | `working/claim-verification.md` | kept | — |
  | `working/doctrines.md` | revised | the embedded `--list` capture (25/9/27/122) silently contradicted the live re-derived values (33/31/33/345) in the chapter teaching that carried constants drift → date-stamped as the registration-day capture (`2026-09-14`, measured from git history) — regenerating it would have falsified the incident narrative |
  | `working/provenance.md` | kept | — |

  Borderline-but-defensible items the audit reported and the pass deliberately did NOT
  touch (measured, not taste-driven): task-leaf IDs before the task-trees chapter
  (self-describing), MMU/CSR/Sv39 unexpanded (named as selection items, not leaned on),
  the archogen F/M external IDs (references into an external document), and the
  registry-mirror tables in `working/doctrines.md` (REGISTRY-MIRROR mandates them — they
  cannot move to an annex).

## Current Frontier

| Order | Leaf | Status | Why next |
| --- | --- | --- | --- |
| — | — | — | 2/2 leaves complete — the tree closes (the apparatus exists and the first audit pass landed); further passes are new leaves the day the director's record grows |

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

`BOOK-APPARATUS.2` (`2026-10-02`, `SEMULITH-BA-0002`):

- [x] **REPRODUCE / ISSUE** — the chapters predate the director's `2026-10-02`
  reading-experience record; the audit measured them against it. The measured
  pre-condition sample (each later verified at its line): `ls crates/` → four crates
  against `claim-scope.md`'s "three-crate"; `grep -c "^(obligation"
  profiles/rv64i-lab-v0/contract-obligations.sexp` → 36 against `p0.md`'s quoted 33;
  `G1-REPORT.md` reads `passed` against `p1.md`'s "verdict today is `incomplete`".
- [x] **ROOT CAUSE (WHY + WHERE)** — two classes, honestly separated. WHY the drift
  class: the book's prose carries repository facts by hand, and the repository moved
  (registration day, G1's closure, the contract's growth) — exactly the failure
  DERIVED-COUNTS was founded on, in chapters no derived-counts enumerator covers.
  WHERE: twelve files, each flagged by the audit and re-verified before editing
  (`git show`-class verification: `grep -c "(decision "` miscounts the rv64i
  profile.sexp's inline forms — the real count is 28, verified by enumerating the ids).
  WHY the style class: three chapters violated the record's own criteria (a duplicated
  sentence, a cold open, a 68-line accreted list item) — measured against the decision,
  not taste.
- [x] **FIX** — the thirteen revised chapters (the disposition table in the leaf records
  what violated and the fix, per chapter), plus LIVE_STATUS.md's stale unit count found
  via `status.md`'s include. No criterion-1 glossary additions: the borderline
  terminology items were measured defensible (self-glossing first uses), recorded as
  such in the leaf.
- [x] **ADDRESSED (verified)** — the acceptance's three legs:

  ```
  $ mdbook build docs/book          → rc 0
  $ python3 scripts/gen_book_index.py
  gen_book_index: wrote docs/book/src/index.md (15259 bytes, 40 indexed terms)
  $ python3 scripts/gen_book_index.py --check → rc 0 (regenerates clean)
  $ bash scripts/check_doctrines.sh → === all doctrines green ===
  ```

  Every chapter carries its disposition in the leaf's table (16 kept / 13 revised).
- [x] **NO REGRESSION** — `bash scripts/check_doctrines.sh` → `=== all doctrines green
  ===`; `gen_book_index.py --check` rc 0; the two mermaid→text replacements render as
  diagrams in the standalone docs and as readable flows in the book (no new dependency
  — mdbook-mermaid was deliberately not added: an unsanctioned dependency is worse than
  a plainer diagram).
- [x] **LOCKSTEP** — tree (leaf + dispositions + checklist + logs + the tree closes),
  `MEMORY.md` (next action), `CHANGELOG.md`, `DEV_NOTES.md` (the audit-method note),
  `LIVE_STATUS.md`, `docs/TASK_TREE.md` (BOOK-APPARATUS done), KNOWLEDGE_MAP
  regenerated. The lesson: promotion: declined (the audit method is the decision record's own consequence clause; the drift fixes are per-slice history).

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
| `2026-10-02` | `.2` | six parallel read-only chapter audits against the decision's four criteria; every flag re-verified at its line before editing (`ls crates/`, `grep -c` on the contract, the G1/G0 reports, git history for the capture date); `mdbook build docs/book` rc 0; `gen_book_index.py` regenerated (15259 B, 40 terms) and `--check` rc 0; `check_doctrines.sh` all green | 29 main-line chapters audited, 16 kept / 13 revised — the yield was factual drift (twelve stale facts, each fixed and verified) plus three genuine style violations; the tree closes |
| `2026-10-02` | `.1` | `gen_book_index.py` → wrote index.md (15019 B, 40 terms); `mdbook build docs/book` rc 0; `check_book_index.sh` → ok; `--self-test` 6/6 (RED arms fired before registration); `check_doctrines.sh` all green | the index exists, is generated, and is gated; the annex policy is stated in the book's introduction; glossary/annexes verified present and on-policy |

## Commit Log

| Leaf | Commit subject or reference | Notes |
| --- | --- | --- |
| `.2` | `SEMULITH-BA-0002 (leaf BOOK-APPARATUS.2): the reading-experience audit — 29 main-line chapters, 16 kept / 13 revised; the yield was factual drift` | six-chapter-group parallel audit against decision_mdbook-incremental-engaging; every flag re-verified before editing; twelve stale facts fixed (claim-scope/p0/p1/p5-p7/architecture/risks/sources/live-status), three style violations (overview duplication, p3's accreted chain, p7's cold open), two raw-mermaid blocks rendered as text flows, the doctrines.md capture date-stamped |
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
- `2026-10-02`: `.2` done (`SEMULITH-BA-0002`) — the first reading-experience audit pass. Six
  parallel chapter-group audits against the decision's four criteria; every flagged item
  re-verified against the repository before any edit. 29 main-line chapters: 16 kept, 13
  revised — and the yield was **factual drift** more than style: twelve places where the book
  had gone stale against the repository (the crate count, the guest corpus counts, the
  contract's 33/66 → 36/72, G1's verdict, registration day, the units count, the risks
  register's current-state column, the naming record's reservation claims, the doctrines
  chapter's undated capture), each fixed at its line with the measurement recorded; plus three
  genuine record violations (a duplicated sentence in the gates overview, plan/p3's 68-line
  accreted update chain collapsed to its final state with the incidents kept, P7's cold open),
  and two mermaid blocks that rendered as raw source replaced by text flows (no new
  dependency). The book builds; the index regenerates clean; the tree closes (2/2).
