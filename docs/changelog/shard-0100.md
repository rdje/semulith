# CHANGELOG shard — SEMILITH-MB-0008 … SEMILITH-MB-0008

> Sharded from `CHANGELOG.md` when it crossed its 64 KiB ceiling (`doctrine/readme_routes.tsv`).
> Entries in a shard are **never edited after the shard** — git history is canonical.

## SEMILITH-MB-0008 (leaf MODEL-BOOKS.6) — the wiring; MODEL-BOOKS closes (8/8)

- `make book` now builds the project book AND every model book (the Makefile's `book`
  target loops `docs/models/*/book.toml`; measured: two books, one command).
- Routing: the project book gains "The models" (`docs/book/src/models.md` — one
  definition, one book; 31 chapters) and README.md's Layout table gains the governed
  `docs/models/` row (69/85 lines, 3,947/4,864 B — inside both caps).
- The 27th doctrine `UNIT-BOOKS` (`scripts/check_unit_books.sh`): every registered unit
  (`materials/units.sexp` — the one registration place) has its own mdBook and it builds;
  a unit without a book (NO BOOK), a book missing its skeleton or failing to build
  (INCOMPLETE BOOK / BOOK DOES NOT BUILD), or a book no unit registers (ORPHAN BOOK) fails
  by name. Fired RED against the real corpus before registration (`NO BOOK rv64i-lab-v0`,
  named, with the book moved aside); self-test 7/0; mirrored per the registry rules.
  Measured in flight: mdbook tolerates a SUMMARY naming a missing chapter (draft +
  warning), so the build arm's broken fixture is a malformed `book.toml` — recorded in
  the gate's header.
- **The tree closes**: all seven acceptance criteria met — (1) every registered unit has
  a book and UNIT-BOOKS says so; (2) the materials list complete, generated, gated (`.1`);
  (3) the methodology follows one rule end to end (`.3`); (4) `make book` builds every
  book and the project book routes (`.6`); (5) prose dominates; (6) the teaching test —
  mistakes in — (every chapter); (7) real-compiled-code ability stated with its limits
  from the extension set (`.5`).
- `make gate` all green (27 doctrines, 287 arms — DERIVED-COUNTS re-derives);
  `check_materials_bill.sh [--self-test]` ok / 7-0; both books render.

