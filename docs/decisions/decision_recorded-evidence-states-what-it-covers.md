# A recorded evidence row states what it covers, and stops being evidence when that moves

- **Type:** `decision`
- **Date:** `2026-11-07`
- **Status:** `active`
- **Owner / source:** `P4-SYSTEM.18` slice a, `SEMULITH-P4-0393`; the workflow under [`decision_findings-are-the-engineers-to-call.md`](decision_findings-are-the-engineers-to-call.md).
answers: What says a recorded verdict still stands for the tree, and what did measuring that find before a release decision?

## What measuring found

`G-PORTABILITY` read green on `portability.sexp`, recorded 2026-10-27 over 168 guests. The tree holds 210, so 42 guests had never been in its manifest. `scripts/gate_report.py` read only the record's verdict, so nothing could say it had aged.

| Recorded evidence | Recorded | Its inputs last moved | Reading |
| --- | --- | --- | --- |
| `portability.sexp` | 2026-10-27 | guests 2026-11-07 | **stale by 42 guests** |
| `act4.sexp` | 2026-10-27 | engine 2026-10-24 | current |
| `workload.sexp` | 2026-10-27 | engine 2026-10-24 | current |

The risk was low, because `crates/semulith-core/src` and `definitions` have no commit since the record, and the reference binaries' pins have not moved. But a verdict should not rest on a green row that nothing ties to the tree.

## The decision

1. **Each row with a recorded verdict states what it covers:** `(covers (path …) (sha256 …))`, a file or every tracked file below a directory, as `python3 -B scripts/gate_report.py --covers PATH` prints it. A row that states nothing, or one whose path has moved, is not evidence, and its axis reads `incomplete` by name.
2. **The covers:** the engine and the definitions for all five rows, plus the ACT pieces, the workload sources or the guest fixture, as each row's run read them. So a later engine change opens these axes until they are re-measured. That is intended: the policy says relevant source changes invalidate dependent evidence.
3. **Portability is re-measured.** All four legs over the 210 guests: `cargo test --all` 519 tests on arm64 and under Rosetta (written "suites" until 2026-11-10; they are tests, in 14 suites), manifest `0aaf081f…` byte-identical on both, Miri and big-endian powerpc64 green.

## What this does not settle

- **The hosted matrix has not seen these 210 guests.** Its last run was 40713852362 on `b917d1ba`, over 171. [`decision_release-route-x86-64-leg.md`](decision_release-route-x86-64-leg.md) makes it the x86-64 leg's permanent home and Rosetta the local bridge, so a release decision should have a hosted run on this tree. That needs a push, and a push below the cadence is the director's to approve. **Settled 2026-11-10:** the director allowed the push, and run 42418631491 is recorded ([`decision_hosted-run-is-a-record.md`](decision_hosted-run-is-a-record.md)).
- Nothing here records a release.

## How to apply

- After a re-measure, update its rows with `--covers` in the same commit as the new record.
- A new recorded row states its covers from its first commit.
