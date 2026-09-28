# DEV_NOTES shard — _(2026-09-14)_ … _(2026-09-14)_

> Sharded from `DEV_NOTES.md` when it crossed its 48 KiB ceiling (`doctrine/readme_routes.tsv`).
> Entries in a shard are **never edited after the shard** — git history is canonical.

## _(2026-09-14)_ — explicit widths, and never regenerate over hand-derived work

- 52 of 52 RV64I instructions now have machine-checkable semantics, each citing the locator it came
  from. Before: 26 rules, all English prose, none executable.
- ⭐ **Widths are always explicit.** `(sext 64 (trunc 32 …))` says what it means; an implicit width
  is exactly where two models silently disagree, and `D-WSUFFIX` is one line once it is spelled.
- ⛔ **Generated and authored content must not share a file.** `rv64i.sexp` is regenerated whenever
  its upstream table moves; hand-derived semantics in the same file would be destroyed by a
  routine regeneration. Different provenance, different file — a rule worth carrying to any
  project that generates part of its source of truth.
- The language is 32 forms, each added because an instruction needed it, and the checker refuses
  the rest. A notation that quietly accepts an unknown operator produces a definition whose
  meaning nobody can state — worse than none, because it looks like one.
- ⚠️ `52 of 52` = well-formed, complete, cited. NOT correct. That distinction has to survive into
  the book, because the number invites the stronger reading.
- Promotion is explicitly declined in the owning leaf, with the reason.

