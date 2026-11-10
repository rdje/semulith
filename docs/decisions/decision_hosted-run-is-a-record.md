# The hosted run is a record the tree can re-read, and an accepted release needs it

- **Type:** `decision`
- **Date:** `2026-11-10`
- **Status:** `active`
- **Owner / source:** `P4-SYSTEM.18` slice b, `SEMULITH-P4-0396`; the engineer's call under [`decision_findings-are-the-engineers-to-call.md`](decision_findings-are-the-engineers-to-call.md).
answers: Where is the native x86-64 leg's evidence kept once the hosting service drops a run's logs, and what did recording it find?

## What was measured

Run 42418631491 of the `portability` workflow ran on commit `12347bc5`, the push the director allowed on 2026-11-07 as an exception.

| Host | Architecture | `cargo test --all` | `rv64gc-lab-v0` manifest | `rv64i-lab-v0` manifest |
| --- | --- | --- | --- | --- |
| `ubuntu-latest` | x86_64, native | 519 passed, 0 failed | `0aaf081f…` over 210 guests | `3fbc498e…` over 49 guests |
| `macos-latest` | arm64, native | 519 passed, 0 failed | `0aaf081f…` over 210 guests | `3fbc498e…` over 49 guests |

Each unit's two manifests are byte-identical. Miri passed 178 tests natively and 178 on big-endian powerpc64. The runners built with rustc 1.99.1 and this host recorded with 1.95.0, and `rv64gc-lab-v0`'s digest is the same on all three.

## The decision

1. **A hosted run is recorded by a tool, from the run's own files.** `scripts/hosted_matrix.py` fetches the run's description, job logs and artifacts, judges them, and writes `profiles/<unit>/hosted-matrix.sexp`. Nothing in the record is typed. The service keeps a run's files for a limited time, and the record is what stays.
2. **The record is tied to the tree before it is written.** The run's commit and this tree must hold the same engine, definitions and guests. Both hosts must give the digest this host recorded, over exactly the guests the tree tracks. One host must be x86_64 and the other AArch64.
3. **`gate.sexp` names it as a second `x86-64` row, with what it covers.** The report then lists the native leg beside the translated one, and the row stops being evidence when the engine, the definitions or the guests move ([`decision_recorded-evidence-states-what-it-covers.md`](decision_recorded-evidence-states-what-it-covers.md)).
4. **An `accepted` release decision needs the hosted row verified.** The axis alone does not ask for it: with the hosted record damaged, `G-PORTABILITY` still read green on the Rosetta row. That is the standing route, in which Rosetta carries the leg between pushes ([`decision_release-route-x86-64-leg.md`](decision_release-route-x86-64-leg.md)). `docs/EVIDENCE_AND_GATES.md` §7 asks for native fixtures, so `P4-SYSTEM.18` slice c holds the decision to the hosted row.

## What recording found

- **`rv64i-lab-v0`'s portability record is stale.** It states `0670a01b…` over 49 guests, recorded 2026-09-30. Both hosted hosts give `3fbc498e…` over the same 49. Its inputs moved after the record: 8 commits touch its guest source, the last on 2026-10-10, and 63 touch the engine, the last on 2026-10-24. The tool refuses to record that unit. Its report reads the axis green from the record's verdict alone, the defect slice a fixed for `rv64gc-lab-v0`. No claim of `rv64gc-lab-v0`'s report reads the scalar unit's records, so the release decision does not wait on it. `P4-SYSTEM.19` owns the repair.
- **The local record's "519 suites" were 519 tests, in 14 suites.** The record writer summed tests and called them suites. It is corrected. Run over slice a's retained logs, it gives the tracked record again but for the date, the kernel version and those four lines, which are now the record's.

## How to apply

- After a push whose `portability` run is green: `--fetch`, `--verify`, `--record`, add the printed row to the unit's `gate.sexp`, and regenerate the report, in one commit.
- After a local re-measure moves a row's covers, the hosted row reads as no evidence until the next hosted run. That is intended.
- Run `bash scripts/check_portability.sh --self-test` before a record act: it runs the tool's 40 controls.
