# CHANGELOG shard — _(2026-09-14)_ … _(2026-09-14)_

> Sharded from `CHANGELOG.md` when it crossed its 64 KiB ceiling (`doctrine/readme_routes.tsv`).
> Entries in a shard are **never edited after the shard** — git history is canonical.

## _(2026-09-14)_ — a gate report that cannot tell a mention from an implementation

- Gate `G0` is run and reads **`incomplete`**: 66 declared checks, 0 implemented. The report is
  GENERATED from tracked inputs and gated for staleness, so `passed` is unreachable — the
  generator has no code path to it, and hand-editing the word fails the commit.
- ⛔ **The generator was wrong twice, both times inflating the verdict.** "How many checks are
  implemented?" first counted `EVIDENCE_POLICY.md` (grepping the id PATTERN across the tree — a
  document describing the naming convention), then counted `check_requirements.sh` (which tests
  the `-POS`/`-NEG` suffix while enforcing that ids exist — a gate about checks is not a check).
  Both said `1`; the truth is `0`. The measure is now exact: take the CONCRETE declared ids and
  ask which any tracked executable names. The failure direction is the lesson — an approximate
  measure of "is this done" drifts toward done.
- ⛔ The evidence policy's first draft stated class populations and got two wrong, by reading the
  profile's authority distribution instead of the requirements' category distribution — the exact
  non-mechanical mapping documented two leaves earlier, walked into by the person documenting it.
  Hand-typed populations were removed; the generated report derives them.
- ⭐ `incomplete` is the DELIVERABLE. A milestone whose job was to establish what evidence would
  be required cannot also have produced it. Saying so in the verdict, rather than in a footnote,
  is what stops the next milestone inheriting a claim nobody made.
- Promotion is explicitly declined in the owning leaf, with the reason.

