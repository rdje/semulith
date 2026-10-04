# CHANGELOG shard — SEMULITH-BA-0002 … SEMULITH-BA-0002

> Sharded from `CHANGELOG.md` when it crossed its 64 KiB ceiling (`doctrine/readme_routes.tsv`).
> Entries in a shard are **never edited after the shard** — git history is canonical.

## SEMULITH-BA-0002 (leaf BOOK-APPARATUS.2) — the reading-experience audit pass: 29 main-line chapters, 16 kept / 13 revised; the yield was factual drift

- The first audit pass over the project book against
  [`decision_mdbook-incremental-engaging`](docs/decisions/decision_mdbook-incremental-engaging.md):
  six parallel chapter-group audits (the decision's four criteria operationalized), every
  flagged item re-verified against the repository before any edit. The per-chapter
  dispositions are recorded in [`docs/tasks/BOOK-APPARATUS.md`](docs/tasks/BOOK-APPARATUS.md).
- **Twelve stale facts fixed at their lines** (each measured): `claim-scope.md` (four crates,
  not three; the CPU-LAB self-contradiction; the 48+1-program corpus, not forty-one),
  `plan/p0.md` (the contract is 36 obligations / 72 checks — the quote now matches the
  regenerated G0-REPORT it claims to quote), `plan/p1.md` (G1 reads `passed` since
  2026-09-30; 48 guests / 642 steps), `plan/p5-p7.md` (registration day is done),
  `docs/ARCHITECTURE.md` (28/36/28 records), `docs/RISKS_AND_DECISIONS.md` §2 (four
  current-state rows updated with measured states and dates — the column whose point is
  tracking change), `docs/SOURCES_AND_NAMING.md` (the crates exist; the reservation claim
  narrowed), `LIVE_STATUS.md` ("1 unit today" → 5).
- **Three record violations revised**: the gates overview's duplicated sentence dropped;
  `plan/p3.md`'s 68-line leaf-by-leaf update chain collapsed to a final-state paragraph
  (both measured incidents kept; the tree carries the blow-by-blow); P7's cold mechanism
  open gained its why-sentence. Terminology pointers added where a concept was leaned on
  without introduction (F3/F6 → `docs/tasks/DSP-REVIEW.md`; CLINT glossed; the P3 forward
  reference named).
- **Two ` ```mermaid ` blocks rendered as raw source in the book** (no preprocessor) —
  replaced by text-rendered flows; `mdbook-mermaid` deliberately NOT added (an
  unsanctioned dependency is worse than a plainer diagram).
- The book builds; the index regenerates clean (`gen_book_index.py --check` rc 0);
  `make gate` green. The BOOK-APPARATUS tree closes (2/2).

