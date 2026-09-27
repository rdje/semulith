# CHANGELOG shard — _(2026-09-14)_ … _(2026-09-14)_

> Sharded from `CHANGELOG.md` when it crossed its 64 KiB ceiling (`doctrine/readme_routes.tsv`).
> Entries in a shard are **never edited after the shard** — git history is canonical.

## _(2026-09-14)_ — the pinned spec has no encodings, and a shorter trace is not agreement

- ⛔ **The specification we pinned does not contain instruction encodings.** Census over all six
  artifacts: `grep -cE '[01]{7}'` -> 0 every time; the format diagrams are images (31 in the
  RV32I chapter). The SEMANTICS are all present in prose, which is the half expected values need,
  so encodings were pinned separately from `riscv-opcodes` and recorded as a *different*
  provenance. That source is upstream of both models, so encoding agreement is not independent
  evidence — only semantic agreement is, and that is what the experiment tests.
- ⭐ Unplanned corroboration: the encoding table holds exactly 52 instructions for this extension
  set, and `P0-PROFILE.1` enumerated exactly 52 by hand from the prose without it. Symmetric
  difference: none. Two independent routes to the same closed set.
- ⛔ **The comparator reported a false pass and running it is what found that.** Walking only the
  overlapping prefix, it printed `AGREE over 2 aligned step(s)` for a run where one model trapped
  and the other stopped. The prefixes agreed; the observation did not. Promoted:
  [`docs/knowledge/a-shorter-trace-is-not-agreement.md`](docs/knowledge/a-shorter-trace-is-not-agreement.md).
- ⭐ **Two models agreeing means nothing until the agreement is shown to be doing work.** Flipping
  one configuration key — the misaligned policy — with the same binary produced a real first
  divergence. That control is why "matched profile" is now a measurement. The project gate now
  refuses an experiment record that claims agreement without naming such a control.
- 🔎 `docs/tasks/` crossed its advisory health target (214,002 B against 196,608). Not a ceiling
  (393,216 aggregate, 65,536 per part) and nothing is breached, but `P0-PROFILE.md` is at 49,521 B
  — 76% of the per-part ceiling — because completed-leaf evidence accumulates in-tree by design.
  The mechanism intended for this is archive compaction, and no tree has needed it yet.

