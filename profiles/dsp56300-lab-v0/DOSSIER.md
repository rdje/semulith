# DOSSIER — `dsp56300-lab-v0` (EXPERIMENTAL)

A bounded, experimental Motorola DSP56300 subset — the second unit in this repository and the
first non-scalar-CPU one. Selected by `P3-BREADTH.4` slice 1 against the reference's measured
coverage and documented gaps; the full selection record is
[`docs/tasks/artifacts/p3-breadth/2026-10-01-subset-selection.md`](../docs/tasks/artifacts/p3-breadth/2026-10-01-subset-selection.md)
and the durable decision is
[`docs/decisions/decision_dsp56300-lab-v0-subset.md`](../docs/decisions/decision_dsp56300-lab-v0-subset.md).

> **Claim scope.** No DSP compatibility is claimed. When `P3-BREADTH.4` completes, the claim
> is functional canonical-end-state agreement with the pinned reference on the declared guest
> corpus for the named subset — never a DSP56300 family compatibility claim, and nothing
> inherited from `rv64i-lab-v0`'s evidence.

## The subset (v0)

Non-parallel moves including the A2/B2 accumulator-extension readout; the immediate/register
data-ALU core (`add/sub/cmp/and/or/eor`, `asl/asr/lsr`); signed `mpy`/`mac`;
`nop/jmp/jsr/rts`; `do`/`enddo`/`rep`; linear addressing only. Excluded by name, each with
its reason in the selection record: parallel moves (the dual-feed axis — first named
extension candidate), the condition-code branch family, rounding/iterative multiplies,
bit-field ops, modulo/reverse-carry addressing, interrupts and traps, operating modes,
stack extension, peripherals, and all timing (`cyc` is never compared).

## Dossier status

| Document | Status |
| --- | --- |
| `sources.sexp` | present — the family manual (DSP56300FM Rev. 5) pinned at NXP's own locator; re-derive `scripts/fetch_sources.sh dsp56300-lab-v0` |
| `references.sexp` | present — `mborgerson/dsp56300@c60aeedb` obtained (tarball + on-volume build), the path-demonstration experiment and the independence inventory recorded; re-derive `scripts/fetch_references.sh dsp56300-lab-v0` |
| `profile.sexp` | **drafted** — the scope taxonomy generalized for this unit (`P3-BREADTH.5` slice 2): the document stands schema-validated at [`docs/tasks/artifacts/p3-breadth/dsp56300-dossier/profile.sexp`](../docs/tasks/artifacts/p3-breadth/dsp56300-dossier/profile.sexp). Landing is leaf `P3-BREADTH.7`: the measured attachment (slice 2) shows EXTRACTION / EXERCISE-COVERAGE / INTERACTION-MATRIX go RED on a unit without `encoding.sexp` / `interactions.sexp` / per-step expectation guests — `.7` owns their disposition. PROFILE-CONSISTENCY already passes this dossier |
| `state.sexp` | **drafted** — the schema constructs landed in `P3-BREADTH.5` slice 1; the document stands schema-validated at [`docs/tasks/artifacts/p3-breadth/dsp56300-dossier/state.sexp`](../docs/tasks/artifacts/p3-breadth/dsp56300-dossier/state.sexp), carrying the F6 census as data (5 register families + parts, 3 spaces, the hardware stack, 12 special registers, 14 candidates). Lands with `profile.sexp` in leaf `P3-BREADTH.7` |
| `encoding.sexp` | **deferred** — the encoding/definition generalization was measured in `P3-BREADTH.5` slice 3 and deferred with named reopening conditions (a lane, not an extension: 24-bit decode emission, a DSP fragment family, semantics as data); the sibling crate is the exercised, agreed vehicle |
| `requirements.sexp` / `contract-obligations.sexp` | **deferred** — the model slice closed with the crate's per-form FM citations; the records land with the dossier documents in leaf `P3-BREADTH.7` (the earlier wording said "with the model slice" — that slice closed without them; corrected `2026-10-01`) |
| unit registration (`materials/units.sexp`) + per-unit book | land with the model slice — `UNIT-BOOKS` requires a book that builds, and the book's evidence chapter needs the model's measured evidence |
| `guests/` | present — `micro.a56` + `micro.meta` (the `.3` demo guest adopted); the corpus grows with slice 4's form coverage |
| the model | **present, EXPERIMENTAL** — `crates/semulith-dsp56300` (slice 3): nine FM-cited forms, the canonical-dump runner, and the first differential agreement (53 fields, `scripts/run_dsp56300_smoke.py` — not a commit gate; the crate's unit tests are the commit-level proof) |

The deferrals are recorded, not gaps to be read as oversight: each names its owning leaf.

## Open items

- **Exact-toolchain policy for the reference build** — the upstream pins Rust 1.98.1; the
  demonstrated build ran under the host's 1.98.0 (satisfies the crate's `rust-version`
  floor) to keep the rustup store off-volume. Recorded as an `attempt` row in
  `references.sexp`; resolve before the reference becomes evidence-bearing.
- The profile's guests, expectations, and the checkpoint-level comparator all land with the
  model slice; the comparison contract (canonical dump, deviation windows, `steps` compared,
  `cyc` never) is fixed in `references.sexp`'s `trace_granularity`.
