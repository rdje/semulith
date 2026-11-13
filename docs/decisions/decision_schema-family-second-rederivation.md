# The `schema/` file ceiling re-derived a second time: one schema per catalogue, 32 to 48

- **Type:** `decision`
- **Date:** `2026-11-14`
- **Status:** `active`
- **Owner / source:** `P4-SYSTEM.20` slice a, `SEMULITH-P4-0403`: `bash scripts/check_readme_routes.sh` printed `OVER CEILING schema/: 33 files > 32` when `schema/identity.sexp` joined, the release identity that left `profile.sexp` ([`decision_the-next-window-is-version-1.md`](decision_the-next-window-is-version-1.md), item 7). The engineer's call under [`decision_findings-are-the-engineers-to-call.md`](decision_findings-are-the-engineers-to-call.md).
answers: Why did the schema family's file ceiling move again, to what, and when does it move next?

## What was measured

At staging, `git ls-files schema | wc -l` gives 33 files and `git ls-files schema | xargs cat | wc -c` gives 160,204 B; the largest member is still `semantics.sexp` at 28,465 B. Since the first re-derivation ([`decision_schema-and-decisions-families-rederivation.md`](decision_schema-and-decisions-families-rederivation.md), 2026-10-23, at 25 files), `git log --diff-filter=A --since=2026-10-22 -- schema/` lists eight additions on seven days: `credits` (10-23), `workload` (10-27), `matched-case` (10-28), `overlay` (11-03), `config-effect` (11-04), `statement-trace` and `alternative` (11-06), `dispositions` (11-07), then `identity` (11-14). Each is the schema of one new catalogue or source-of-truth file, which is the schema layer's design (`SOT-FORMAT.1`).

## The re-derived bounds

| Row | Column | Was | Now | At staging |
| --- | --- | --- | --- | --- |
| `schema/` | `ceiling_lines` (files) | 32 | **48** | 33: 0.69× |
| `schema/` | `health_lines` (files) | 27 | **42** | below: warns again six schemas before the ceiling |
| `schema/` | `health_bytes` / `ceiling_bytes` | 262,144 / 524,288 | unchanged | 160,204: 0.61× / 0.31× |
| `schema/` | `ceiling_part_bytes` | 65,536 | unchanged | 28,465: 0.43× |

The health line keeps the standing ratio of its ceiling (0.875). Fifteen more schemas fit, about six weeks at the measured rate of one every 2.6 days.

## Why, and what was not changed

- The file count is the only bound the family reaches; bytes and the largest member stand at a third and under half of theirs. A count ceiling that fires on the designed addition, with the health line reached two weeks before (the 27th file, `matched-case`, on 2026-10-28), is the miscalibration the first record named.
- No schema joins unseen: RECORD-SCHEMA's token inventory states the file count (`LIVE_SCHEMAS` in `scripts/probe_schema_token_facets.py`, 33 now) and refuses a mismatch, and DOSSIER-SCHEMA validates every profile document against its same-named schema.

## How to apply

- `doctrine/readme_routes.tsv` row `schema/` carries the bounds above; `check_readme_routes.sh` enforces them on every commit.
- The next crossing is a new measurement and a new record, not an edit to this one.
