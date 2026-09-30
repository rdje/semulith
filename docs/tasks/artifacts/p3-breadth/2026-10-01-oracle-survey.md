# The real-DSP oracle survey — P3-BREADTH.3, slice 1 (2026-10-01)

The leaf's acceptance demands the evidence path be demonstrated BEFORE a real DSP subset is
implemented, and `SRC-02` makes a missing reference route prevent the evidence claim. So the
first question is empirical: for each family `DSP-REVIEW` measured, does a runnable, pinnable,
license-clean reference route exist at all?

**Method (the census behind every absence claim below).** Three parallel web surveys, one per
family, each instructed to check the same enumerator: QEMU's supported-targets document, MAME's
`src/devices/cpu/` listing, gem5's `src/arch` listing, GDB's `sim/` directory, binutils'
`bfd/config.bfd` / LLVM's target list, dedicated open-source emulator projects, and the vendor
toolchain's current status — each with a URL per claim, "unverified" where a search could not
decide. The two load-bearing positive claims were then re-derived here against primary sources
(`docs/CLAIM_VERIFICATION.md` — a survey report is one leg; the fetch is the other):

- `https://raw.githubusercontent.com/mborgerson/dsp56300/main/README.md` — fetched
  `2026-10-01`: the crate table (`dsp56300-core` decoder, `-asm`, `-disasm`, `-emu` JIT,
  `-emu-ffi`), the silicon-validated difftest ("corpus programs are run on the emulator and on
  silicon, and the resulting state dumps are compared word for word"), the a56 examples.
- `https://raw.githubusercontent.com/mborgerson/dsp56300/main/LICENSE` — fetched `2026-10-01`:
  **MIT**, © 2026 Matt Borgerson.
- `https://raw.githubusercontent.com/mamedev/mame/master/src/devices/cpu/sharc/sharc.cpp` —
  fetched `2026-10-01`: `// license:BSD-3-Clause`, "Analog Devices ADSP-2106x SHARC emulator
  v3.0", `DEFINE_DEVICE_TYPE(ADSP21062 …)` / `(ADSP21060 …)`, the full register export via
  `state_add` (PC, MODE1/2, ASTAT, STKY, MRF/MRB, I/M/L/B 0–15, …), interpreter + DRC, and the
  visible gaps (unimplemented IOP registers `emu_fatalerror`; counter-loops of length 1/2
  stubbed).

## Per-family verdicts

### TI C6000 (C64x/C64x+/C66x) — ABSENT for execution

| Leg | Status | Evidence |
| --- | --- | --- |
| Runnable OSS reference | **none exists** | QEMU target list: no C6x ([qemu.org targets](https://www.qemu.org/docs/master/system/targets.html)); MAME `src/devices/cpu`: tms320c1x/c2x/c3x/c5x/c82, tms57002 — no c6x; gem5 `src/arch`: arm/mips/power/riscv/sparc/x86 only; GDB `sim/`: no tic6x (GDB has tic6x *debug* support only) |
| Vendor simulator | discontinued, proprietary | TI removed ALL simulators from CCSv6 (2014) — "Texas Instruments is moving away from providing simulators" ([E2E](https://e2e.ti.com/support/tools/code-composer-studio-group/ccs/f/code-composer-studio-forum/332756/)); CCSv5.5 survives as legacy proprietary |
| Toolchain | strong for ≤ C674x | GNU binutils `tc-tic6x.c` + GCC `config/c6x/`, both upstream and maintained into 2026; **no C66x** in either (C66x: TI CGT 8.5.0 LTS only, free but proprietary) |
| Machine-readable encodings | partial | binutils `opcodes/tic6x-dis.c` tables (GPL-3.0+); Capstone TMS320C64x module (BSD-3) — C64x only; no neutral opcode DB |

The sail-riscv/spike pattern **cannot be replicated** for C6000: there is nothing to pin.

### Motorola/NXP DSP56300 — STRONG

| Leg | Status | Evidence |
| --- | --- | --- |
| Runnable OSS reference | **yes** | [`mborgerson/dsp56300`](https://github.com/mborgerson/dsp56300) — MIT (verified above), active (crates published 2026-09), core-complete, headless CLI + library, Cranelift JIT; **silicon-validated**: its `tools/difftest` compares full canonical state (pc sr omr la lc sp ssh ssl ep sz sc vba, x0 x1 y0 y1 a0..b2, r0–r7 n0–n7 m0–m7, stack slots, X/Y/P memory deviations) word-for-word against real MCPX silicon and Motorola's `sim56300`; known gaps enumerated in `docs/LIMITATIONS.md` (SA/SC/DM mode bits, stack extension, instruction cache, pipeline interlocks unmodelled) |
| Second implementation | yes, GPL-3.0 | [`dsp56300/dsp56300`](https://github.com/dsp56300/dsp56300) + [`dsp56300/gearmulator`](https://github.com/dsp56300/gearmulator) ("The Usual Suspects") — runs real commercial firmware (Virus, Nord Lead…); no published differential harness; GPL-3.0 (the MIT toolkit is the pinnable one) |
| Vendor simulator | proprietary, obsolete | Motorola Suite56 `sim56300` — runs under wine (the MIT repo's `simdrv.py` drives it), but NXP no longer supports or distributes it; usable as a third opinion, never pinnable |
| Toolchain | **yes, MIT** | `dsp56300-asm` in the same repo — roundtrip-tested exhaustively against Motorola's official `asm56300` v6.3.15 across the full encoding space; Alfred Arnold's AS (GPL) also covers DSP56300. binutils/LLVM: no target (verified upstream) |
| Machine-readable encodings | partial | the decoder tables in `dsp56300-core` (MIT, Rust — directly consumable); no neutral opcode DB |

### ADI SHARC (ADSP-2106x) — PARTIAL

| Leg | Status | Evidence |
| --- | --- | --- |
| Runnable OSS reference | **yes** | MAME `src/devices/cpu/sharc/` — BSD-3-Clause (verified above), very actively maintained (commits into 2026-09), ADSP21060/21062, interpreter + DRC + disassembler, ROM-less `adsp21060` machine (boots with only external memory — a ready differential host), every register exported for per-step dumps; arcade-validated, NOT hardware-validated against a SHARC test suite |
| Toolchain | friction on every path | `sergev/g21k` carries AD's own 21k assembler under GPL (1990s AD/FSF agreement) but is 32-bit-era C needing porting; `mikewolak/sharc_asm` is complete but under a personal/educational-use-only license — **not vendorable**; no binutils/LLVM/Capstone support |
| Machine-readable encodings | partial | mineable from MAME's BSD-3 opcode tables; no declarative DB |
| Beyond 2106x | absent | no open emulator for 21160/213xx/214xx/TigerSHARC found (unverified absence — vendor/clone listings only) |

## The slice decision

**The candidate real slice is DSP56300.** The tree's own rule decides it — the slice is
"resolved by whether an evidence path can be demonstrated — not by which manual is easiest to
read" (`DSP-REVIEW`'s Open Questions, `RK08`), and DSP56300 is the only family whose evidence
path is complete AND license-clean end-to-end: an MIT assembler whose encodings were
exhaustively roundtripped against the vendor assembler, and an MIT emulator whose validation
harness is exactly this project's workflow (assemble → execute → compare full architectural
state per checkpoint), already silicon-sealed by its authors.

The choice also fits the findings' conditioning (`DSP-REVIEW.7`'s routing): a scalar-DSP slice
**activates** F1 (24-bit words, 56-bit accumulators — `.5`'s generator work), F3 (P/X/Y spaces
with 24-bit word addressing — `.5`), and F6 (the census reopens: A2/B2 extension readout
semantics, DO/REP state — `.1`/`.2`); it does **not** require F4/F5 (scalar issue, no packets)
and leaves F2 idle (no register pairing in this family). SHARC stays the documented PARTIAL
alternative (its assembler leg is unbuilt). TI C6000 gets **no real slice** — there is no
oracle to pin; its findings stay conditional, and TI-shaped exploration belongs to the
synthetic composed-DSP fixture (this tree's Design Discussions), never to a compatibility
claim.

## What this survey does NOT say

- No DSP compatibility is claimed or implied; this document measures ORACLE AVAILABILITY.
- The DSP56300 reference's silicon validation is **its authors'** proof artifact — Semulith
  has not re-run a hardware capture (it needs MCPX silicon this project does not have). Under
  `EVD-04` its ancestry is recorded honestly: the JIT emitter was early-differential-tested
  against the xemu/XQEMU DSP56300 core (ARAnyM/Hatari DSP56001 lineage), then validated against
  silicon and the official simulator — so `sim56300` and the sealed corpus are the stronger
  legs, and both are external to Semulith.
- The reference's documented gaps (pipeline interlocks, cache, SA/SC/DM modes, stack
  extension) bound the evidence to **functional architectural state** — no timing claim can
  ride this path.
- An "unverified absence" above means exactly that: the named enumerator returned nothing,
  which is evidence of absence for the enumerated set, not a theorem about the internet.
