# The DOCTRINE_ENFORCEMENT.md ceiling is re-derived to 32 KiB for the 31st doctrine row

- **Type:** `decision`
- **Date:** `2026-10-02`
- **Status:** `active`
- **Owner / source:** `BOOK-APPARATUS.1`, applying the registry's own rule ("raising a ceiling
  needs a reviewed decision that the surface's contract expanded") with the director's
  approval — standing since `2026-10-01` ("ceiling raises: ask, they're approved",
  `decision_task-tree-per-part-growth`) and repeated `2026-10-02` ("if you need more headroom
  for some files, just ask and I will approve").

## The decision

`DOCTRINE_ENFORCEMENT.md`'s ceiling in `doctrine/readme_routes.tsv` is re-derived from
28,672 to **32,768 bytes** (28 KiB → 32 KiB). The measured state: 28,672 of 28,672 bytes at
HEAD with the 31st registered doctrine (`BOOK-INDEX`) owed a row by `REGISTRY-MIRROR`. At the
measured ~930 bytes per doctrine row, 32 KiB covers ~34 rows.

## Why this is the contract expanding, not the cap fitting content

The surface's contract IS the row count: one human-readable row per registered doctrine, and
doctrines register by design. The ceiling exists to bound prose bloat *per row* — and it did
its job: the `BOOK-INDEX` row was fitted to the per-row budget the sibling rows hold (~710
bytes, two trims) before the raise was asked for. This is the third re-derivation on the same
grounds (the 20th row, `SEMILITH-PL-0001`; the 25th, `SEMILITH-PS-0007`). No health target is
added (a doctrine row arrives, not a paragraph).
