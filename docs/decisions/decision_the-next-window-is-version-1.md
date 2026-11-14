# The next pinned window is rv64gc-lab-v0 version 1: what each item lapses, and the label that should not

- **Type:** `decision`
- **Date:** `2026-11-10`
- **Status:** `active`
- **Owner / source:** `P4-SYSTEM.20`'s design brief, `SEMULITH-P4-0401`; the engineer's call under [`decision_findings-are-the-engineers-to-call.md`](decision_findings-are-the-engineers-to-call.md).
answers: What does the next pinned window lapse, item by item, what must it carry, and what does version 1's release need that version 0's did not?

## What was measured

On a throwaway clone of `ea848a5b`, one byte edit per item, then `scripts/credit_records.py --profile rv64gc-lab-v0` and the CPU-SYSTEM report; the real tree was not touched. Re-derive on any clone: append one comment line to the file, `git add` it, and run `python3 -B scripts/credit_records.py --profile rv64gc-lab-v0`.

| Item | File it edits | Credits lapsed | Report |
| --- | --- | --- | --- |
| the expectations author's legalization, and its vocabulary | `scripts/derive_rv64gc_expectations.py` | 42 of 46 | `G-TRACE`, `G-RELEASE` open |
| `medeleg` narrowed to `0xb3ff` | `state.sexp` | 42 of 46 | `G-TRACE`, `G-RELEASE` open |
| `misaligned_amo AccessFault` | the profile override | 0 | `G-RELEASE` open |
| `profile.sexp`'s status and stale comment | `profile.sexp` | 42 of 46 | `G-TRACE`, `G-RELEASE` open |
| device regions: `OB-GC-ENV-DATA-ACCESS` superseded | `contract-obligations.sexp`, `contract.sexp` | 0 | `G-RELEASE` open |
| (a hazard, not an item) | `EVIDENCE_POLICY.md` | 46 of 46 | `G-TRACE`, `G-RELEASE` open |

The 42 are every case-backed credit; the four with nothing to run stand. Two more facts complete the table:

- **The state table moves the engine.** `crates/semulith-core/src/definition_rv64gc.rs` pins `state.sexp` by digest, and `state_rv64gc.rs` is generated from it. Narrowing `medeleg` regenerates both, so every recorded row that covers `crates/semulith-core/src` lapses: rv64gc's ACT4, workload and three portability rows and its hosted row, and the scalar unit's ACT4, portability and hosted rows, because the engine is shared.
- **The override and the contract lapse no credit.** Credit verification reads each case's retained `reference-config.json`; the override is read only to prepare a new case, by the smoke runs and by probes. No requirement, credit or case names `OB-GC-ENV-DATA-ACCESS`, and only the registry realizes its two checks.

## What measuring found

1. **The version label sits in a file every case pins.** `profile.sexp` carries `(version "0")` and `(status "development")`, and every case pins its bytes. So a new version number lapses all 42 case credits even when no behaviour moved. A contract-only version 1 would cost a full re-capture for one string. That is a label lapsing evidence about behaviour.
2. **During the window the live report cannot verify version 0.** The first pinned input that moves opens `G-TRACE`, and the first dossier file that moves breaks the decision's digest. Version 0's acceptance stays verifiable at the commit that recorded it, `194437d6`.
3. **Version 1's acceptance needs a hosted run on its engine.** The native x86-64 leg is a hosted record, and narrowing `medeleg` moves the engine it covers. On 2026-11-10 the tree stood 10 commits past the last push, against a cadence of 300. So the hosted run is either an exceptional push, which is the director's to approve, or it waits for the cadence.

Slice a's brief (2026-11-13, `SEMULITH-P4-0402`) measured two more, on a clone of `ca562be1`:

4. **A lapsed credit is a finding the gate refuses, so no slice can leave one behind.** One comment line appended to `profile.sexp` gives `REQUIREMENT-STATUS: drift or finding (rv64gc-lab-v0: … 42 planned, 4 implemented …; 4 of 46 credit record(s) current; 42 drift, 42 finding(s))`, rc=1, and PROFILE-CONSISTENCY runs that derivation on every commit (`xtask/src/check_profile_consistency.rs`). This is the design: "a moved pin lapses the credit, the status falls back, the recorded status drifts, the gate fails" ([`decision_credit-is-a-catalogue-record.md`](decision_credit-is-a-catalogue-record.md)). So "slices a to f leave `G-TRACE` open" holds only if the slice that moves a pin also retires what it lapses. The precedent is the fetch-fault window: a49-1 retired its 19 credits by removal, and no requirement read implemented until a49-3 re-credited them ([`decision_the-window-that-carries-fetch-faults.md`](decision_the-window-that-carries-fetch-faults.md)). Measured on the same clone: with the 42 lapsed records removed and their 42 requirements recorded `planned`, the derivation reads `ok … 4 of 4 credit record(s) current; 0 drift, 0 finding(s)`, the DIV review exits 0, and the CPU-SYSTEM report reads `incomplete` with `G-STATE`, `G-TRACE`, `G-OBLIGATIONS` and `G-RELEASE` open, each **unowned** until the manifest declares its `open` item.
5. **The release identity is a file of its own, in every profile.** Three of the five profiles (`dsp56300-lab-v0`, `lan9118-lab-v0`, `sifive-uart-lab-v0`) have no `gate.sexp`, and all five carry `(version …)` and `(status …)` in `profile.sexp` under one shared spec (`scripts/dossier_sexp.py`, pinned by 44 cases). A `gate.sexp` form would leave the label in two places. Nothing reads the profile's `status`; `scripts/gate_report.py` reads its `version` at three sites. No recorded row covers `profile.sexp` or a whole profile directory, so the recorded rows do not lapse. Only `rv64i-lab-v0`'s dossier digest is pinned, by the netboard's `board.sexp`, so that one re-pin follows.

## The decision

1. **The window is version 1, one coherent set.** It carries every item above. Every engine move lands before slice g, so the recorded rows are re-measured once and one push serves both units.
2. **First, the label leaves the pinned file.** The window's first slice moves the version and status out of `profile.sexp` into a release identity no case pins, and the report and schema read them from there. That costs the one lapse the window pays anyway, and after it a version that moves no behaviour lapses no case credit.
3. **The claim pages name the commit before the window's first pinned move.** README, `claim-scope.md`, LIVE_STATUS and the unit book say that version 0 is accepted as verified at `194437d6`, so nothing reads as a live claim the live report has stopped checking.
4. **The order:**
   - **a.** The release identity out of `profile.sexp`; the claim pages name `194437d6`.
   - **b.** The author's legalization and vocabulary, and the probe that holds the author to the engine.
   - **c.** The state table's `medeleg`; the engine moves.
   - **d.** The override's `misaligned_amo`.
   - **e.** The device-region supersession and its realized checks.
   - **f.** The 42 cases captured again and their credits re-issued, in batches.
   - **g.** The recorded rows re-measured for both units, and the hosted run.
   - **h.** Version 1's release decision.

   Slices a to f leave `G-TRACE` open, and that is expected. Each slice's own brief measures what it moves, and a slice that lapses a credit retires it in the same commit (item 6).
5. **The device-region item asks the CPU for a guarantee too.** An MMIO region is safe only if the hart reads it exactly as often as the program does: no speculative read, no repeated read, and no fetch from it. Slice e states that guarantee next to the assumption and realizes both checks. Whether MTIP and MEIP sources come in the same version, for timers and an interrupt controller, slice e measures against what P6's firmware needs.

6. **Slice a retires the 42 credits it lapses, by removal, and records their requirements `planned`, in the same commit.** Version 0's 46 credits stand at `194437d6` and stay recoverable there; slice f re-issues them against the new captures. Rejected: re-capturing in every slice that moves a pin (all 42 cases in each of slices a, b and c), a disposition that tolerates a lapse (it removes the teeth the credit record was given), and one commit for slices a to f.
7. **`identity.sexp` in every profile directory, `(identity (unit …) (version …) (status …))` under `schema/identity.sexp`,** with `status` one of `development` and `experimental`. `profile.sexp` and its spec lose both fields; the report reads the identity and refuses one whose unit is not the profile. `rv64gc-lab-v0`'s identity is version `1`, `development`: the live dossier is version 1's window, and version 0 is the dossier at `194437d6`. The manifest declares the four open axes, each owned by this leaf.

8. **Slice d found what the override's move lapses (2026-11-14, `SEMULITH-P4-0409`):** no credit, as measured, but 10 of the 12 retained configuration effects, whose comparison side is the override or an alternative over it. A retained effect is never re-measured under its name, so they stay, predicted stale until slice f captures their cases again; likewise the five retained cases whose prepared configuration a probe compares with today's, which now differ by exactly that key.

## What this does not settle

- How the 46 credits are re-issued in bulk. Slice f measures the act per batch. Measured by slice f's brief (2026-11-14, `SEMULITH-P4-0413`): one batch of 42, each predecessor retired in the unit that declares its successor, so the window peaks at 45 cases and no family bound moves ([`decision_a-predecessor-leaves-when-its-successor-is-declared.md`](decision_a-predecessor-leaves-when-its-successor-is-declared.md)).
- The push. When slice g needs the hosted run, the director is asked in one plain sentence; nothing here approves it.

## How to apply

- `EVIDENCE_POLICY.md` stays untouched in the window: editing it lapses all 46 credits.
- Each slice's record states what it lapsed and what it re-issued.
- `P5-BOARD.13` waits on slice h, the version that admits device regions ([`decision_a-board-needs-a-contract-that-admits-devices.md`](decision_a-board-needs-a-contract-that-admits-devices.md)).
