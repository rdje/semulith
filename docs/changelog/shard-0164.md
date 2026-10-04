# DEV_NOTES shard — _(2026-10-02)_ … _(2026-10-02)_

> Sharded from `DEV_NOTES.md` when it crossed its 48 KiB ceiling (`doctrine/readme_routes.tsv`).
> Entries in a shard are **never edited after the shard** — git history is canonical.

## _(2026-10-02)_ — a freshness gate deferred to "the first tracked board" lands exactly once (P5-BOARD.3)

`compose_units.py` shipped with its freshness proof explicitly deferred — "lands with
the first tracked board" — and P5-BOARD.3 was that board. The shape that landed: one
generator (`gen_board.py`, boards discovered by declaration, never a hardcoded id),
seven artifacts per board, and the BOARD-GEN doctrine re-deriving all seven on every
commit. The compose factorization is the part worth remembering: `compose()` took a
manifest FILE, which pins part resolution to the manifest's location — useless inside a
generator that derives the manifest itself and must compose in scratch. The fix was not
a second materialization path but `compose_resolved(comp_id, part_dirs, out_dir)` — the
manifest-file entry point and the generator both land on it (the refactor measured
byte-identical on the real parts, self-test 9/9).

Two measurements did the design's real work. The FACT-OWNERSHIP probe: placing the
composed catalogues in the board directory tripped the gate's self-test on EXACTLY the
two new restatement pairs — the gate refusing to judge an unregistered corpus is the
registry doing its job; registration (8 rows), not weakening, was the fix. And the
design brief's register-surface containment check turned out NOT implementable: the
device dossiers carry register offsets in prose with datasheet citations (measured in
both `state.sexp` documents and the expectations), never as machine-readable data — so
the generator's refusals are scoped to what board.sexp itself proves (overlap, window ↔
device resolution, executable-mmio, ghost console), and machine-readable offsets arrive
with the device models, where the check belongs. A brief line that says "measured at
execution" is a promise; the honest outcome can be "the data is not there".

Lesson: `promotion: declined` (recorded in the leaf) — derive-from-declaration and
measure-before-design already carry their decision records
(`decision_device-applicability-by-declared-vehicle`, `decision_gate-applicability-by-
declared-vehicle`); the compose factorization is recorded with the leaf and in
`compose_units.py`'s own docstring.

