# The `docs/decisions/` aggregate doubled a third time, and the next firing archives instead

- **Type:** `decision`
- **Date:** `2026-11-06`
- **Status:** `active`
- **Owner / source:** `P4-SYSTEM.14` a49-1, `SEMULITH-P4-0368`: `bash scripts/check_readme_routes.sh` printed `OVER CEILING docs/decisions/: 524499 aggregate bytes > 524288` on the record of [`decision_the-window-that-carries-fetch-faults.md`](decision_the-window-that-carries-fetch-faults.md). The engineer's call under [`decision_findings-are-the-engineers-to-call.md`](decision_findings-are-the-engineers-to-call.md); precedents: [`decision_decisions-family-aggregate-rederivation.md`](decision_decisions-family-aggregate-rederivation.md), [`decision_decisions-family-second-rederivation.md`](decision_decisions-family-second-rederivation.md), [`decision_schema-and-decisions-families-rederivation.md`](decision_schema-and-decisions-families-rederivation.md).
answers: Why did the decisions family's aggregate ceiling move again, to what, and what must the next firing do instead?

## The measurement

| Axis | Measured | Ceiling |
| --- | --- | --- |
| Files | 110 | 160, unchanged |
| Largest part, `INDEX.md` | 26,326 B | 32,768 B, unchanged |
| Aggregate | 524,499 B | 524,288 B: over by 211 B |
| Growth | 323,698 B to 524,499 B in the 14 days since 2026-10-23, about 14 KiB a day | |
| Records marked `closed` | 3, 20,501 B | |

## The decision

1. **The aggregate goes to 1,048,576 B, health 917,504 B**, the same 87.5% as before. Trimming a sentence would buy minutes, and each record is what `CLAUDE.md` asks for: only 3 are closed, so there is nothing to shed honestly.
2. **The next firing does not double.** At this rate it is about five weeks away. A family that only grows needs an archive part, as `docs/tasks/` has: closed and superseded records moved verbatim, each leaving a pointer and its `INDEX.md` row.
3. **Not done here:** a pinned window is open, and a move touches links many records hold.

## How to apply

- `doctrine/readme_routes.tsv`'s `docs/decisions/` row carries the bounds above.
- The next crossing is an archive unit with its own record, not another doubling.
