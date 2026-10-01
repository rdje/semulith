# The dsp56300-lab-v0 state census — P3-BREADTH.1, the F6 leg (2026-10-01)

F6 (`docs/tasks/artifacts/dsp-review/2026-10-01-interface-findings.md`) is the finding that
the state census reopens for every new profile: the census method (`SEM-08`, RULES.md) is
proven on the scalar profile, but each measured DSP carries state that census answered
"absent" for — accumulator extensions with readout semantics, addressing-mode control,
sticky flags, loop state. `.4` delivered the exercised `dsp56300-lab-v0` profile and pinned
the load-bearing readouts along the way; this leg re-runs the method and harvests them. The
per-profile `state.sexp` that would carry this census as generated data is `.5`'s named
schema case (special registers beyond `pc`, nonstandard widths, memory spaces); this record
is its measured input.

## The method, re-run

The census question (SEM-08, catalog C02): **is there any state, not declared, that can
influence a future supported observation?** Answered per candidate, with the reason and the
locator, never by silence — the scalar census's shape
(`profiles/rv64i-lab-v0/state.sexp`'s `hidden_state_census`).

The **supported observation** for this profile is fixed by the comparison contract
(`profiles/dsp56300-lab-v0/references.sexp`'s `trace_granularity`, the reference harness's
own engine-agnostic shape): the canonical end-state dump per case — `steps`, the 46 register
lines (`pc sr omr la lc sp ssh ssl ep sz sc vba x0 x1 y0 y1 a0 a1 a2 b0 b1 b2 r0–r7 n0–n7
m0–m7`), deviation-encoded X/Y/P memory windows, and the 15 hardware-stack slots; `cyc` is
excluded by recorded rule (timing is never compared).

The **declared state** is exactly that surface: `crates/semulith-dsp56300/src/machine.rs`
carries "every field the reference harness's canonical dump names, nothing more".

**Surface completeness, argued before the candidates:** the machine has no mutable cell
outside the surface. Hardware-stack slot 0 is unwritable by construction (SP pre-increments,
FM §5.4.3); P $0000–$07BF holds the loaded program and subset v0 decodes no P-space write,
so it is constant and equal to the image (only the harness's $07C0–$07FF window is
compared); the harness-private X window $0400–$04FF is excluded by the harness's own
contract on both engines. Every other cell is dumped and compared. The six-guest corpus
AGREEs 6/6 over 51–64 fields per case against the pinned reference
(`scripts/run_dsp56300_smoke.py`) — the empirical half of the argument.

## The candidates

F6's named DSP classes, then the scalar census's seven re-asked for this target.

| # | Candidate | Verdict | Why — with the locator |
| --- | --- | --- | --- |
| 1 | **Accumulator extensions with readout semantics (A2/B2)** — F6's named case | **PRESENT, declared and measured** | A2/B2 read as the sign-extended extension byte (FM §3.4.1.2; `a2`/`b2` ride in the surface and agree on all six guests). A1/B1 read **raw** — the shifter/limiter sits on the whole-accumulator read path only (measured, alu guest: `move a1,x:` with A2=0, A1=$FE00FF stores $FE00FF and L stays clear; `.4` slice 4 finding (c) — the FM's limiting prose over-applies here). Writes: `move #xx,A/B` sign-extends the 8-bit fraction through A2 (measured, shift guest — finding (b); the FM 13-113 prose "the remaining bits are zeroed" is falsified for A2); data-ALU results write the full 56 bits; ASL/ASR are 56-bit; LSR is a 24-bit op leaving the extension byte untouched (FM 13-95). Accumulator-part move **destinations** are outside subset v0 — a typed decode stop by name, never a guessed write. |
| 2 | **Addressing-mode control (M0–M7)** | **PRESENT, declared and bounded** | Reset `$FFFFFF` = linear (the reference's reset dump agrees). Subset v0 decodes no write to any Mn (AGU registers as move-bus ends are typed stops), so in subset v0 they are constant at reset; any Mn ≠ `$FFFFFF` at an (Rn) access stops by name (`effective_addr` — modulo/reverse-carry is the named exclusion, never a guessed wrap). |
| 3 | **Sticky flag state (SR's L and S)** | **PRESENT, declared** | L is sticky: set when V sets, never cleared by a data-ALU op (FM Table 5-1; `set_v` in `exec.rs`). S is sticky with **no writer in subset v0**: it sets on whole-accumulator XDB/YDB bus reads, which subset v0 does not decode — measured (finding (d): an ASR of a negative accumulator does NOT set S; S never moves from reset across all six guests). Both ride in the dumped `sr` line. |
| 4 | **Loop state (DO: LA/LC/LF + the stacked levels)** | **PRESENT, declared** | LA, LC and LF (SR bit 15) are in the surface; the stacked loop context (prior LA/LC, then PC/SR) lives on the hardware stack — dumped slots 1–15. DO pushes two levels and sets LF; the end-of-pass rule decrements LC and loops (SSH → PC) or unwinds (LF from SSL's bit 15, then LA/LC restored — FM §13 DO / ENDDO 13-67). Measured: micro's `do #4` and the corpus 6/6. |
| 5 | **REP working state** | **ABSENT beyond the declared LC** | REP's borrow of LC is restored before the instruction retires (LC → TEMP, count → LC, …, TEMP → LC inside one step, `exec.rs` `rep`) — nothing pending crosses an instruction boundary. Measured: the rep guest, 64 fields AGREE, with LC back at its pre-REP value at case end. |
| 6 | **Stale popped stack slots** | **PRESENT, declared** | Pop does not clear the slot; popped SSH/SSL content persists and IS observable — the dump compares slots 1–15 deviation-encoded, and the jsr guest agrees byte-for-byte with the reference's stale slots. Hidden from the programmer, inside the observation surface, so declared here rather than discovered later. |
| 7 | Control/status registers beyond the declared set (interrupt, peripheral) | **ABSENT by exclusion** | Interrupts/traps/peripherals/operating modes are named subset exclusions (the reference's own LIMITATIONS §3.6 unverifies peripheral interrupts upstream). EP/SZ/SC/VBA exist but have no writer in subset v0; they ride at reset and are dumped. |
| 8 | Reservation / atomicity state | **ABSENT architecturally** | The DSP56300 instruction set has no load-reserved/store-conditional mechanism (FM §13 has none); subset v0's moves complete as a unit. |
| 9 | Floating-point state | **ABSENT architecturally** | The data ALU is integer/fractional only (FM §3); no FP registers or status exist to hide. |
| 10 | Vector state | **ABSENT architecturally** | No vector unit exists in the family. |
| 11 | Privilege / trap state | **ABSENT by exclusion** | No privilege modes; no exception model in subset v0 — a fault is a typed `ModelStop` to the harness, never an in-model trap. |
| 12 | Instruction-fetch cache state | **ABSENT architecturally** | The DSP56300 fetches program RAM directly; the reference implements cache ops as NOPs (LIMITATIONS §1.4/§3.2) and the model re-reads P on every fetch. Same reasoning shape as the scalar census's D-CODE-VISIBILITY note, one step stronger: here the architecture itself carries no cache. |
| 13 | **Pending / partially committed effects** (F5's delayed-writeback window) | **ABSENT** | Scalar issue; every subset-v0 instruction completes or stops as a unit — no multi-cycle visible writeback window exists to model. Measured: the 6/6 end-state agreement. This is the scalar census's seventh candidate re-asked, with the same answer and a new arbiter. |
| 14 | Stack-extension state (the X-space extended stack) | **ABSENT by exclusion** | Stack extension is excluded upstream (LIMITATIONS §2.1) and in subset v0 — a 16th-level push is a typed `StackOverflow` stop, never a spill. |

## The consequence

For subset v0 under its named exclusions, **the canonical end-state dump is the complete
architectural state**: every cell that can influence a future supported observation is in
the comparison surface, and the census measured nothing hidden. Snapshot/replay of this
profile reduces to the dump fields — the same honesty the scalar census bought replay on
`rv64i-lab-v0`, now earned for a target whose state the scalar census could not have
expressed (a 56-bit accumulator with a sign-extended extension readout, a hardware stack
whose stale slots are observable, three memory spaces).

This census is the harvested input for `.5`'s named cases: the special-register census (what
the state schema's `special_registers` must learn to carry), F1 (masked widths — 24-bit
registers, 56-bit accumulators, the 8-bit extension), F3 (the three memory spaces with their
bounded windows), and the scope taxonomy (the exclusions above are the profile's scope).

## Honest bounds

- **This census answers for subset v0 only.** Every named exclusion reopens its row:
  parallel moves add no state but change the observation surface; interrupts add pending
  state (candidate 11); modulo/reverse-carry turns candidate 2 live; stack extension turns
  candidate 14 live.
- **Nested DO is exercised at one level** (micro's `do #4`); the two-level stack machinery
  is agreed through the jsr depth, not through nested loops. A nested-loop guest is a named
  corpus extension candidate.
- **`cyc` is never an observation** (excluded by recorded rule); no timing state is censused
  because no timing claim exists.
