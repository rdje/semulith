# The interface findings report — DSP-REVIEW.7 (2026-10-01)

The tree's capstone: every candidate interface change the review produced, classified
and costed, routed to `P3-BREADTH` with its evidence attached. The routing method is the
tree's own `ROUTING EVIDENCE` section, chosen before the first finding existed:

1. the **manual locator** that states the target behaviour;
2. whether the current abstraction can express it — demonstrated **executably** (the
   `.6` synthetic fixture), not by reading type definitions;
3. whether the same limitation also fires for the **scalar profile** `rv64i-lab-v0` —
   if it does, the finding is a scalar/core defect, not a DSP finding.

⛔ **Scope discipline (`.8`'s arming).** A TI absence is never restated as a DSP absence,
and a TI requirement is never restated as a DSP requirement. Every finding below names
its family scope explicitly.

## The scalar controls (method leg 3, measured)

```
$ python3 scripts/gen_state.py --state profiles/rv64i-lab-v0/state.sexp \
    --arith crates/semulith-core/src/arith.rs --out /dev/null
gen_state: wrote /dev/null (14496 bytes)          # rc=0 — the real 64-bit state doc
                                                  # generates; the width refusal is
                                                  # nonstandard-width-specific
$ bash scripts/check_definition_gen.sh | tail -1
DEF-GEN: ok (crates/semulith-core/src/definition.rs matches the canonical definition, …)
$ bash docs/tasks/artifacts/dsp-review/synth/run_synth_probes.sh | tail -1
synth probes: 4 pass / 0 fail                     # the boundary is where the pins say
```

Plus the standing scalar evidence: `P2-SCALAR` closed with 642/642 live steps and the
interaction matrix green — the current step model has never failed the scalar profile.

## Classification classes

- **EXPRESSES** — the current abstraction covers it; the finding is semantics **data**,
  not interface work.
- **NEEDS-A-CHANGE** — expressible with named work; nothing refuses it today, but the
  interface does not yet carry the concept.
- **CANNOT-EXPRESS (refused by name)** — the pipeline refuses the shape today, and the
  refusal message itself names the work that lifts it.

## Findings

### F1 — nonstandard register widths — CANNOT-EXPRESS

- **What:** 24-bit registers (DSP56300's P/X/Y word width), 56-bit accumulators
  (DSP56300 A/B), 80-bit accumulators (SHARC MRF/MRB). The state generator refuses:
  `masked fixed-width storage for nonstandard widths is generator work
  (docs/ARCHITECTURE.md §4)`, rc 2 (probe `state.sexp`).
- **Locators:** DSP56300 §3.1 p. 3-1/3-3 (`A2:A1:A0`); SHARC §3 p. 3-13–3-15 (MR2 guard
  bits). See `2026-09-30-cross-vendor.md`.
- **ROUTING EVIDENCE:** locator above; executable demonstration = `.6` probe 1 (rc 2,
  pinned in `synth/README.md`); scalar reproduction = **does not fire** — the control
  above generates the scalar profile's 64-bit state with rc 0. Routed to
  `P3-BREADTH.5` (schema/generator functionality where justified).
- **Cost:** the generator names it — masked fixed-width storage. Medium, bounded to
  `gen_state.py` + the generated arith crate; no step-model change.

### F2 — register grouping with fill semantics — NEEDS-A-CHANGE

- **What:** TI 40-bit long results span an odd:even register pair with the odd
  register's upper 24 bits **zero-filled** ("Operations producing a long result
  zero-fill the 24 MSBs of the odd-numbered register", C64x §2.2 p. 26); 64-bit pairs
  (all three TI manuals); 128-bit quadruplets (C66x only).
  (`2026-09-30-widths-q1-q2.md`.)
- **ROUTING EVIDENCE:** locator above; **honest limit: no executable refusal was
  measured** — the `.6` suite did not probe grouping, so this is classified from the
  state document's shape (flat registers, no group/readout concept), not from a
  measured refusal; scalar reproduction = does not fire (RV64I has no register
  pairing). Routed to `P3-BREADTH.1`.
- **Cost:** the state schema gains register groups with a readout rule (the zero-fill
  is architecture, not convention). Medium. If `P3-BREADTH.3`'s real slice is not TI,
  this finding idles — grouping is TI-family-shaped in this corpus.

### F3 — multiple address spaces — CANNOT-EXPRESS

- **What:** DSP56300's P/X/Y spaces (24-bit word-addressed); SHARC's DM/PM (the address
  unit **varies by space**). The schema refuses: `undeclared field "memory_spaces"`,
  rc 1 (probe `state-spaces.sexp`). TI needs nothing here (one 32-bit byte-addressed
  space, `2026-09-30-addressing-q6-q8.md`) — this finding is the `.8` inversion's
  second half: the multi-space requirement belongs to the scalar-DSP families.
- **Locators:** `2026-09-30-cross-vendor.md` (the three unit shapes table).
- **ROUTING EVIDENCE:** locator above; executable demonstration = `.6` probe 2 (rc 1,
  pinned); scalar reproduction = does not fire (the scalar profile's single-space
  definitions validate today — the `DEF-GEN: ok` control above). Routed to
  `P3-BREADTH.5`; the address-unit-per-space question (bytes vs 24-bit words vs
  width-varies) is part of the same schema work, not a separate finding.
- **Cost:** schema field + the memory interface gains a space selector with a per-space
  unit. Large — touches every memory access's shape.

### F4 — the execute packet as the unit of progress — CANNOT-EXPRESS, TI-family-shaped

- **What:** ≤8 instructions per fetch packet, all operands read simultaneously at E1,
  one functional unit each — instruction-stepping miscomputes a two-store packet's
  joint outcome. The schema refuses: `undeclared field "packet"`, rc 1 (probe
  `packet.sexp`). (`2026-09-30-packets-q9-q11.md`.)
- **Locators:** C64x §3.7; the packet rules quoted in the artifact.
- **ROUTING EVIDENCE:** locator above; executable demonstration = `.6` probe 3 (rc 1,
  pinned); scalar reproduction = does not fire (RV64I retires each instruction as a
  unit; 642/642 live). **Scope: TI-family-shaped, measured** — DSP56300 and SHARC are
  scalar-issue (`.8`), so this finding constrains `P3-BREADTH.3`'s slice choice: a
  VLIW slice requires it, a scalar-DSP slice does not. Routed to `P3-BREADTH.1` with
  that condition attached.
- **Cost:** a packet-progress step model beside the instruction-progress one. Large —
  the single most expensive finding; the condition above exists so it is paid only
  for a target that needs it.

### F5 — delayed, visible writeback — CANNOT-EXPRESS, TI-family-shaped

- **What:** a load's result lands at cycle i+4 with the window architecturally visible
  — early reads are stale **by design**, unprotected, and interrupts land inside the
  window (in-E1 instructions complete through E5). The semantics schema refuses:
  `undeclared operator "delay"`, rc 1 (probe `delayed.sem.sexp`).
  (`2026-09-30-packets-q9-q11.md`.)
- **Locators:** C64x §3.7.4 (stale early read), the delay-slot tables in the artifact.
- **ROUTING EVIDENCE:** locator above; executable demonstration = `.6` probe 4 (rc 1,
  pinned); scalar reproduction = does not fire (the scalar census records "pending or
  partially committed effects: present false — every instruction completes or faults
  as a unit", `profiles/rv64i-lab-v0/state.sexp`). Same TI-family scope as F4.
  Routed to `P3-BREADTH.1` under the same condition.
- **Cost:** the `delay` operator + a **pending-writes window** in the architectural
  state (the census reopens — F6). Medium-large; cheaper than F4, required wherever
  F4 is.

### F6 — the state census reopens for every new profile — NEEDS-A-CHANGE

- **What:** the census method (`SEM-08`) exists and is proven (the scalar profile's
  census is why replay is honest), but each measured DSP carries state the scalar
  census answered "absent" for: accumulator extensions with readout semantics
  (DSP56300 A2/B2; SHARC MR2 guard bits, sign-extended on read); addressing-mode
  control registers (TI AMR; SHARC MODE1 carrying BR0/BR8); sticky flag state (TI
  CSR.SAT + SSR — both survive interrupts, TSR tables; SHARC STKYx/y); loop state (TI
  SPLOOP: the loop buffer, **two** hidden LBC registers, ILC with its 4-cycle
  load-to-use latency, RILC, TSR/ITSR/NTSR's SPLX bit; DSP56300's DO/REP state;
  SHARC's DO UNTIL loop stack); and, under F5, the pending-writes window.
- **Locators:** `2026-09-30-loops-q12-q14.md` (the SPLOOP census),
  `2026-09-30-rounding-saturation-q3-q5.md` (SAT/SSR survival),
  `2026-09-30-cross-vendor.md` (the extensions, MODE1, STKY).
- **ROUTING EVIDENCE:** locators above; executable demonstration = the scalar census
  itself (`profiles/rv64i-lab-v0/state.sexp` `hidden_state_census` — the method
  exists and runs); scalar reproduction = N/A by construction (this finding IS the
  census method applied wider, not a scalar defect). Routed to `P3-BREADTH.1`;
  `P3-BREADTH.2` is the natural home for the readout-semantics hooks (MR2's
  sign-extended read is exactly an "opaque semantic hook made explicit").
- **Cost:** per-profile census re-runs (cheap, method exists) + state fields as each
  profile demands (bounded by the profile). Medium.

## Non-findings (measured, then classified OUT of interface work)

- **NF1 — "DSPs need accumulator/guard state" as a universal.** False as stated: TI has
  no accumulator and no guard bits (measured absent, `.1`); DSP56300 and SHARC have
  both (`.8`). The interface consequence lands per-target through F6, never as a
  universal DSP state block.
- **NF2 — the per-instruction sticky-flag side effect.** SADD2 saturates but does NOT
  set the SAT bit (`.2`) — a per-instruction fact, i.e. semantics **data**. The step
  model already applies per-instruction effects; no interface change.
- **NF3 — the saturate/round ordering.** Multiply → accumulate → round-add →
  shift/saturate → narrow is per-instruction step-sequence data (`.2`). **EXPRESSES.**
- **NF4 — circular/bit-reversed addressing.** Address-generation semantics — data —
  with three measured alignment rules (TI align-to-size, restricted to A4–A7/B4–B7;
  DSP56300 2^k-aligned; SHARC arbitrary) and the AMR/MODE1 state landing through F6.
  **EXPRESSES** as semantics; no addressing-interface change.
- **NF5 — the SPLOOP drain asymmetry and MFENCE.** Interrupts drain the loop buffer,
  exceptions don't (C64x §7.13.3 p. 608); MFENCE is C66x-only (0 hits in two manuals,
  34 in C66x's). Both are per-instruction/per-exception semantics data + F6 census
  state, not interface shape.

## What the report does NOT say

- No finding claims DSP compatibility. The tree's non-goal stands; these are
  abstraction-shape findings with manual locators.
- F2's classification rests on the state document's shape, not a measured refusal —
  the only finding without an executable demonstration. If `P3-BREADTH.1` wants one,
  a grouping probe in the `synth/` suite is the honest way to get it.
- The recorded manual defects (seven in `.2`, nine further in `.8`, per the tree's
  Verification Log) stay unresolved upstream; none blocks a finding here.
