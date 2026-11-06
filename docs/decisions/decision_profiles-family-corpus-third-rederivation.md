# The `profiles/` byte ceiling re-derived a third time, once for the rest of the route

- **Type:** `decision`
- **Date:** `2026-11-06`
- **Status:** `active`
- **Owner / source:** `P4-SYSTEM.14` a49-2, `SEMULITH-P4-0369`: `bash scripts/check_readme_routes.sh` printed `OVER CEILING profiles/: 4254076 aggregate bytes > 4194304`. The engineer's call under [`decision_findings-are-the-engineers-to-call.md`](decision_findings-are-the-engineers-to-call.md); precedent: [`decision_profiles-family-corpus-second-rederivation.md`](decision_profiles-family-corpus-second-rederivation.md).
answers: Why did the profiles family's byte ceiling move again, to what, and for how long?

## The measurement

| Axis | Measured |
| --- | --- |
| Aggregate | 4,254,076 B, over by 59,772 B |
| Files | 630 of a ceiling of 800, unchanged |
| The window's own peak | 118,103 B of overlays and effects a49-4 retires with their cases |
| A corpus program and its expectation | 22,896 B to 94,222 B: `csr-access` to `d-forms` |
| Requirements still to case | 24 at most: 7 with a switch, and 17 ending at a ruling, several of which need no program |

So the peak alone is not the cause. Retiring it leaves 4,135,973 B, and the next batch would cross the ceiling again.

## The decision

The aggregate goes to **6,291,456** B (6 MiB), health **5,505,024** B, 87.5%. Worst case for the route is 24 programs at 70 KiB each, about 1.7 MB, which ends near 5.8 MB. **One raise for the rest of `G-OBLIGATIONS`, not one per batch**, as `decision_evidence-family-two-cases.md` did for its count at a46-2.

## How to apply

- `doctrine/readme_routes.tsv`'s `profiles/` row carries the bounds above; the file count and the per-part bound stay.
- A crossing before `G-OBLIGATIONS` closes means a program far larger than these, which is itself a finding: read it before raising anything.
