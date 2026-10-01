# The bounded subset, selected — P3-BREADTH.4, slice 1 (2026-10-01)

`.3` demonstrated the evidence path; this slice selects the exact subset `.4` will implement
and evidence, measured against the reference's coverage and its documented gaps. The claim
discipline is the leaf's own acceptance: the claim names the exact subset, and nothing
inherits a differentially validated claim from another target (`docs/EVIDENCE_AND_GATES.md`
§1).

## The reference's measured coverage (the census behind the bounds)

- **Instruction coverage: complete.** The pinned `mborgerson/dsp56300@c60aeedb` core decodes
  the full DSP56300 instruction set — the `Instruction` enum
  (`target/refs/dsp56300-src/crates/core/src/lib.rs:1163`) spans the parallel-move ALU group,
  the immediate ALU forms, shifts, the multiply family (MPY/MAC/MPYR/MACR/DMAC/MPY_SU/MAC_SU),
  the whole branch/bit-field family (Bcc/Bra/Bsr/Jcc/Jsr/Jclr/Jset/Brclr/Brset/Bsclr/Bsset/
  Bchg/Bclr/Bset/Btst), the loop machinery (DO/DOR/ENDDO/REP), CLB/MERGE/EXTRACT/EXTRACTU/
  INSERT, DIV/NORM/NORMF, MOVEC/MOVEM/MOVEP, LRA/LUA, and the system instructions. The
  subset is therefore bounded by what Semulith can honestly implement and evidence, not by
  reference coverage.
- **The documented gaps bound the claim axes** (`target/refs/dsp56300-src/docs/LIMITATIONS.md`,
  read in full): SA/SC/DM mode bits are stored but never affect execution (§1.1–1.3 — so no
  16-bit-arithmetic or double-precision-multiply behaviour can be evidenced down this path);
  stack extension is unimplemented (§2.1); the instruction cache and cache ops are NOPs
  (§1.4/§3.2); pipeline interlocks are unmodelled and cycle counts are base-table values only
  (§3.1/§4 — the `cyc` dump field is informational, never a claim); peripheral interrupt
  sources and fast-vector stack-error shapes are unverified against hardware (§3.6);
  STOP/WAIT are not distinguished (§3.5); RESET and DEBUG are NOPs (§3.3–3.4).
- **The comparison surface is checkpoint-level canonical state**, engine-agnostic by the
  harness's own contract ("anything that can produce the canonical dump format can be
  compared", `target/refs/dsp56300-src/tools/difftest/README.md`): per case — `steps`, `pc
  sr omr la lc sp ssh ssl ep sz sc vba`, `x0 x1 y0 y1 a0 a1 a2 b0 b1 b2`, `r0–r7 n0–n7
  m0–m7`, `cyc` (informational); with `--dump-mem`, deviation-encoded X/Y/P windows
  (X:$0000–$0BFF minus the harness window $0400–$04FF, Y:$0000–$07FF, P:$07C0–$07FF); with
  `--dump-stack`, the 15 hardware stack slots deviation-encoded against the seed. Dirty-state
  affine fills make wrong-address reads diverge instantly. This is a per-CASE end-state
  comparison, not the per-instruction commit walk the RISC-V references produce — the
  comparator `.4` builds is a new, simpler shape (field-exact end-state equality over the
  declared vocabulary; `steps` compared, `cyc` never).

## The selected subset — unit `dsp56300-lab-v0`, subset v0

Instruction classes (assembler-level forms; the implementation slice enumerates every form
with its DSP56300FM citation — the pinned manual is `NXP-DSP56300-FAMILY-MANUAL` in
`materials/catalog.sexp`):

1. **Moves** — short (8-bit) and long (24-bit) immediates to the data-ALU and address
   registers; register-to-register moves within the dumped register set; X-space and Y-space
   moves in both directions over absolute addresses and the `(Rn)`, `(Rn)+`, `(Rn)-` forms;
   accumulator reads and writes **including A2/B2** (the extension-byte readout — F6's named
   case, already exercised by the `.3` demo guest).
2. **Data ALU** — `add`, `sub`, `cmp`, `and`, `or`, `eor` (register and immediate forms);
   `asl`, `asr`, `lsr` (single-bit and multi-bit forms).
3. **Multiply-accumulate** — `mpy` and `mac`, signed, with the fractional ×2 convention and
   the 56-bit A2:A1:A0 result.
4. **Program control** — `nop`, `jmp`, `jsr`, `rts`.
5. **Zero-overhead looping** — `do` (immediate and register count forms, nested within the
   hardware stack's depth) with `enddo`; `rep` (immediate and register forms).
6. **Addressing: linear only** — M registers are compared (they are in the dump) but held at
   their reset values; no modulo or reverse-carry arithmetic is claimed in v0.

State the subset touches (all inside the comparison vocabulary): the full dumped register
list above, the hardware stack (bounded depth, no extension), X and Y data memory, and P
memory as the fetched program image only (no P-space data writes in v0).

## Exclusions — each named with its reason

| Excluded | Why |
| --- | --- |
| Parallel moves (the ALU + dual X/Y feed in one word) | bounded scope; the dual-operand-feed axis (the skeleton's defining DSP shape) stays **unexercised in v0** — recorded as the first named extension candidate, not silently absent |
| The condition-code family (`bcc/jcc/bscc/tcc`, the `jclr/jset/brclr/brset/bsclr/bsset` bit-test branches) | bounded scope; the SR CCR bits are still written by the ALU ops and compared in every dump |
| Rounding/iterative multiply (`mpyr/macr/dmac/div/norm/normf`, `mpy_su/mac_su`) | bounded scope |
| Bit-field and bit-manipulation ops (`bchg/bclr/bset/btst`, `clb/merge/extract/extractu/insert`, `vsl`, `inc/dec`, `lra/lua`) | bounded scope |
| Modulo and reverse-carry addressing | NF4 classifies these as expressible semantics **data** needing no interface work; excluded to keep v0 bounded — a named extension candidate |
| Interrupts, traps, exceptions, illegal-instruction delivery | the reference's peripheral-interrupt and fast-vector shapes are **unverified** (LIMITATIONS §3.6); a v0 guest hitting one is a typed model stop, never a claim |
| `stop`/`wait`/`reset`/`debug` | unmodelled or NOP upstream (LIMITATIONS §3.3–3.5) |
| Cache ops (`pflush` …) | NOPs upstream (§1.4/§3.2) |
| Stack extension (SEN/EP spill) | unimplemented upstream (§2.1); stack overflow in v0 is a typed stop |
| SA/SC/DM mode behaviours | stored-but-inert upstream (§1.1–1.3); v0 runs in reset default mode only |
| `movep` / peripherals | outside the core-state comparison surface |
| Timing | `cyc` is informational (§3.1/§4); `steps` is the compared counter — **no cycle claim ever rides this path** |

## The implementation vehicle (decided)

A new crate, `crates/semulith-dsp56300`: decode and semantics derived from the pinned family
manual, every form cited, the model labelled **EXPERIMENTAL** exactly as `rv64i-lab-v0`'s
release decision labels its v0 (`decision_release-rv64i-lab-v0`). Reasons:

- The existing pipeline refuses a second unit by name (`gen_state.py`'s "a second unit is
  generator work"; `gen_definition.py`'s hardcoded profile) — that generator work is
  **`.5`'s**, and this tree already routed it there: `.5`'s extensions must each name "the
  target and case that required it", which is exactly what an exercised `dsp56300-lab-v0`
  provides. Implementing the generator generalization first would invert the tree's order
  and build abstraction ahead of its exercising target — the speculative generality P3
  exists to refuse.
- A sibling crate keeps the gated scalar model byte-untouched (no regression surface for
  `rv64i-lab-v0`'s 180-test suite and its gates) and keeps the DSP model's claim honestly
  separable.
- The generated-artifact boundary (`docs/ARCHITECTURE.md` §2) is not violated: there is no
  generated DSP56300 table to duplicate; whether the DSP decode becomes generated fragments
  (the MIT decoder tables and the FM manual as candidate sources, ancestry recorded per
  EVD-04) is `.5`'s reviewed decision, with this crate as the measured input.

The differential harness: a Semulith-side runner emitting the canonical difftest dump
verbatim (same field names, same deviation encoding against the same init/fill), the
reference driven exactly as `.3` slice 2 drove it, and a checkpoint-level comparator —
field-exact equality over the declared vocabulary, `steps` compared, `cyc` ignored, a
shorter or missing field a failing verdict. Guest expectations are manual-derived before any
model runs (EVD-05). The ancestry record (EVD-04): assembler and emulator share one upstream
project; the assembler's independent leg is upstream's exhaustive roundtrip against
Motorola's `asm56300`; the emulator's is upstream's silicon-sealed corpus — both are
upstream proof artifacts, not Semulith re-derivations, and are recorded as such.

## The claim shape (what `.4` may say when done)

> `dsp56300-lab-v0` subset v0 is an **experimental** Semulith model of the named instruction
> classes, differentially validated against `mborgerson/dsp56300@c60aeedb` on the declared
> guest corpus over canonical architectural end-state (registers, bounded X/Y memory
> windows, hardware stack slots) — **functional agreement only**: no timing, no operating
> modes, no interrupts, no parallel moves, no modulo addressing. It is not a compatibility
> claim over the DSP56300 family, and it inherits nothing from `rv64i-lab-v0`'s evidence.

## Gaps this selection surfaced (owned, routed)

- **The profile schema's `scope` enumeration is scalar-named** (`schema/profile.sexp`'s
  `base_u_type`, `rv64_loads`, …): a validating `profile.sexp` for `dsp56300-lab-v0` needs
  a scope taxonomy that names DSP categories. Routed to `.5` as a named case (target:
  `dsp56300-lab-v0`; case: the profile dossier's scope section). `.4`'s dossier slice
  carries what validates today (`sources.sexp`, `references.sexp`, requirements/obligations,
  guest expectations) and records the profile description in prose until the schema catches
  up — the same honest pattern as the `memory_spaces` refusal (F3).
- **Auto-discovering gates iterate `profiles/*/`** (EXTRACTION, PROFILE-CONSISTENCY, …): the
  dossier slice must measure how each treats a second, deliberately partial profile before
  landing, and disposition each (satisfy, or extend the gate with the reason recorded).
