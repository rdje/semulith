# CHANGELOG shard — _(2026-09-14)_ … _(2026-09-14)_

> Sharded from `CHANGELOG.md` when it crossed its 64 KiB ceiling (`doctrine/readme_routes.tsv`).
> Entries in a shard are **never edited after the shard** — git history is canonical.

## _(2026-09-14)_ — a running total is a memory of a measurement, not a measurement

- ⛔ Two derived counts were committed WRONG in a single session, both as running totals:
  `24 destinations governed` against a 25-row registry, and `107 self-test arms` against 112. The
  method was identical each time — take the written number, add your delta, write the sum back —
  and nothing recomputed either. Gated by `DERIVED-COUNTS`, which re-derives each from the
  population it summarises and prints the enumerator alongside the value.
- ⭐ The new gate caught its own registration: adding it made the project hold 9 doctrines where
  the page said 8, and the commit was blocked until the number was re-derived rather than bumped.
- ⛔ Its first cut was wrong in the *dangerous* direction. `sed -nE "s/.*([0-9]+) widgets.*/\1/p"`
  is greedy: on `12 widgets` the leading `.*` eats the `1` and the capture is `2`. A stale count
  could have matched a wrong extraction and read as correct. Found by a GREEN arm going red.
  Extraction is now off the front of a `grep -o` match, and a pattern not beginning with its
  number group is refused.
- The `TASK-ACCEPTANCE` recipient-tree boundary is **documented, not relaxed**. Requiring only one
  staged leaf to pass would reopen the co-staged-leaf hole that box-scoping exists to close, so a
  routed annotation lands as its own doc-only commit instead. The lesson's promotion is
  explicitly declined in the owning leaf, with the reason.

