# One definition, one book

Every modelled unit has its own mdBook beside this one, under `docs/models/<unit-id>/` —
the `decision_one-definition-one-book` rule: the unit of modelling is the unit of
documentation. A unit's book is where a reviewer reads **how that unit went from pinned
documents to a running model**: its complete materials bill (generated from the pinned
dossier, gated so a digest cannot rot), what the materials do not contain, the method, the
references and what their agreement is worth, and the evidence with the honest gate
verdict.

Today two units exist:

- **`rv64i-lab-v0`** (kind: processor) — `docs/models/rv64i-lab-v0/`. Build it with
  `mdbook build docs/models/rv64i-lab-v0`, or build every book with `make book`.
- **`dsp56300-lab-v0`** (kind: processor) — `docs/models/dsp56300-lab-v0/`. The bounded,
  EXPERIMENTAL DSP56300 subset: a sibling-crate model, checkpoint-compared against the
  pinned reference — and the unit that pushed the public abstraction past its
  scalar-CPU assumptions (`P3-BREADTH`).

The wiring is a gate, not a habit: the `UNIT-BOOKS` doctrine
(`scripts/check_unit_books.sh`) enumerates the registered units from
`materials/units.sexp` — the one registration place — and fails the commit if a unit lacks
its book, if a book does not build, or if a book under `docs/models/` belongs to no
registered unit. Adding a profile without its book fails the gate.
