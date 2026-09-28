# DEV_NOTES shard — _(2026-09-27)_ … _(2026-09-27)_

> Sharded from `DEV_NOTES.md` when it crossed its 48 KiB ceiling (`doctrine/readme_routes.tsv`).
> Entries in a shard are **never edited after the shard** — git history is canonical.

## _(2026-09-27)_ — the star gets a start condition (ROADMAP v0.3)

- ⭐ **A plan that cannot say when its first milestone starts is not yet a plan.** The vacuum
  was measured, not argued: `27` commits since any milestone tree was touched, that touch being
  P0 closure. The fix is not "work faster" — it is to make the sequencing *derivable*: P1's
  start condition (`SOT-FORMAT.2` + `MODEL-METHOD.10`) is now named in the plan itself, and
  every cross-cutting lane must name its consuming milestone (`decision_lane-consumption`).
- ⭐ **Contradictions between contract documents are defects with owners, not interpretations to
  code around.** ARCHITECTURE.md §1.1 (semantics are data) and §2 (canonical Rust handlers)
  disagreed; P1 would have met that ambiguity on day one and picked silently. Recorded and
  resolved in `decision_interpreter-before-compiler`: the data executes; compiled handlers are
  derived artifacts behind an equivalence regression.
- Counts in live documents drift by spelling: `LIVE_STATUS.md` carried `MODEL-METHOD 3/10`
  (stale: 6 of 13) because the gated pattern only matches "of/leaves" phrasing — a count in a
  non-gated spelling is a memory of a measurement. (Fix proposal D3 announced to the director;
  the check extension is pending approval.)

