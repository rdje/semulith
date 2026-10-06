# The FP backend is rustc_apfloat 0.2.3+llvm-462a31f5a5ab — qualified by measurement, with the model layer owning the named deviations

- **Type:** `decision`
- **Date:** `2026-10-06`
- **Status:** `active`
- **Owner / source:** measured by `P4-SYSTEM.7` slice (a) (the backend qualification) —
  `target/p4-system-7/` (scratch: `probe/` the comparison+timing harness, `mpfr/vec_gen.c`
  the MPFR vector generator, `candidates/` the extracted crates)

## The fact / decision

`rustc_apfloat 0.2.3+llvm-462a31f5a5ab` (crates.io, updated 2025-06-11) is the floating-point
backend for the rv64gc model's F/D work, pinned with `=0.2.3+llvm-462a31f5a5ab`. The model
layer (`fp.rs`, `P4-SYSTEM.7` slice (b)) owns the RISC-V target policy AND the measured
LLVM-vs-IEEE deviations listed below — the crate is arithmetic machinery, not policy.

## Why — the measurements (all reproducible from the scratch harness)

**The candidate landscape, re-measured** (the census's web claims re-verified against the
fetched artifacts): exactly two pure-Rust, wasm-compiling, non-SoftFloat candidates exist.
- `rustc_apfloat 0.2.3+llvm-462a31f5a5ab`: license **Apache-2.0 WITH LLVM-exception**
  (LICENSE.txt measured in the extracted crate; LICENSE-DETAILS.md records the port's
  provenance: LLVM's APFloat/APInt at llvm-project commit `f3598e8f`, the version string's
  `+llvm-462a31f5a5ab` pinning the source commit). `#![forbid(unsafe_code)]`, `#![no_std]`,
  no global state, pure-value API (status rides every result — no thread-local or global
  status anywhere).
- `softfloat 1.0.0` (koute, updated 2023-11-03): license **MIT OR Apache-2.0**
  (LICENSE-MIT/LICENSE-APACHE measured). Forked from `const_soft_float` — the musl-libc
  math lineage, NOT Berkeley SoftFloat (EVD-04-clean). `#![no_std]`, `const`, with
  localized `unsafe { core::mem::transmute }` in the bits conversions. The census's
  "TestFloat-verified upstream" claim is UNVERIFIED — the crate's own documents carry no
  such statement (recorded, not counted).
- The negatives re-confirmed from crates.io metadata: `softfloat-sys` 0.1.4 is "Rust
  bindings for Berkeley SoftFloat 3" (C FFI, fails RUST-01); `softfloat-wrapper` 0.3.4 is
  its wrapper (same); `softfloat-pure` does not resolve on crates.io (moot).
- Native host floats fail ARCH §6 on capability (no per-op rounding control, no flag
  access, NaN-payload nondeterminism on wasm32) — never probed, by the brief's own words.

**Capability surface (measured from the extracted sources):**

| requirement (ARCHITECTURE.md §6) | rustc_apfloat | softfloat |
| --- | --- | --- |
| the 5 IEEE rounding modes | ✓ (all five, per-op) | ✗ nearest-even only — no mode parameter in the API |
| exception flags | ✓ Status bitflags on every result (StatusAnd) | ✗ (flag mentions are comments only: "Not Asserted") |
| add/sub/mul/div | ✓ `*_r(round)` | ✓ (RNE) |
| FMA | ✓ `mul_add_r` | ✗ (no fma anywhere in the crate) |
| sqrt | ✗ (the port never carried opSqrt — lib.rs:235's doc mentions it, unported) | ✓ (measured MPFR-exact) |
| compares / min / max | ✓ partial_cmp / min / max | ✓ cmp / ✗ min / ✗ max |
| conversions f32↔f64 | ✓ `FloatConvert::convert_r(round)` | ✓ (RNE) |
| int conversions | ✓ to/from i128/u128 with rounding + is_exact (any width ≤128) | ✗ 64-bit ints — i32/u32 only |
| NaN payloads / signaling | ✓ qnan/snan payload, is_signaling, quieted-with-payload | ✓ payload kept, sign cleared |
| formats | f16/f32/f64/x87/quad | f32/f64 |

**Correctness against MPFR** (63,752 cases: directed classes — ±0, subnormals, NaNs with
payloads, infinities, rounding-boundary ties, the 2^53/2^63/2^64 conversion edges — plus
seeded xorshift64* streams; per op × 5 modes × f32/f64):

- the arithmetic core (add/sub/mul/div/fma VALUES, all modes, both widths): **ZERO
  disagreements**.
- flags: two measured LLVM-vs-IEEE deviations, both model-layer work, never defects to
  hide: (i) `opOverflow` fires only when the result is ±inf — `overflow_result` in
  ieee.rs returns INEXACT-only for the TowardZero/TowardNegative clamp and the below-tie
  nearest cases never reach it (362 measured cases: APFloat NX where IEEE's magnitude rule
  wants OFNX — fp.rs computes OF itself: |exact| > max-finite, via the wider-format
  re-evaluation); (ii) an sNaN through a format conversion gets no NV flag (24 cases —
  fp.rs detects is_signaling on fcvt).
- the model-layer policy gaps (fp.rs-owned, measured): NaN→int conversion VALUE (APFloat
  returns 0 with INVALID_OP; RISC-V wants the target's max with NV — 340 cases; note
  +inf/−inf saturate to max/min + INVALID_OP exactly as RISC-V wants); fmin/fmax's
  signed-zero pair (APFloat returns +0 for min(+0,−0); RISC-V §20.1.1 wants −0/+0 by sign)
  and both-NaN canonical (APFloat returns the RHS NaN's payload; RISC-V wants canonical) —
  240 cases; NaN payload scaling on format conversion (APFloat widens/narrows payloads per
  LLVM; RISC-V's canonical NaN on any NaN result — 32 cases).
- sqrt: absent from APFloat (1,440 corpus cases unprobed there) — fp.rs owns sqrt; its
  correctness bar is MPFR + the measured-clean softfloat sqrt (see below).
- `softfloat` vs MPFR on its covered set (4,416 cases: add/sub/mul/div/sqrt at RNE): 68
  disagreements, ALL one family — softfloat clears the propagated NaN's SIGN bit
  (IEEE-unspecified; APFloat preserves it). Its arithmetic core is MPFR-exact where it
  exists — INCLUDING sqrt. The apfloat↔softfloat cross-check: the same 68, nothing else.

**Timing on this host** (release, 2M-iteration loops): apfloat f64 add 10.1 / mul 10.5 /
div 40.7 ns/op, f32 add 8.9 / mul 10.4 / div 15.6, fma 15.7, f2u64 3.5, u2f64 5.4;
softfloat f64 add 3.2 / mul 2.3 / div 5.1 / sqrt 44.1. APFloat's 3–5× premium over
softfloat on the arithmetic core is the StatusAnd/generality cost — acceptable for a
laboratory model (the tracked bench refuses rv64gc by name; this is the scratch evidence
ARCH §6 asks for).

**The independence argument** (the brief's decision 2, stated once): three lineages, none
Berkeley — LLVM APFloat (the port), musl-libc (koute's softfloat), MPFR (GNU 4.2.2, the
system Homebrew library via the scratch `vec_gen.c`). Sail/Spike FP agreement is one
opinion (EVD-04 — [[reference_softfloat-shared-ancestry]]); the closing Sail matched
experiment (slice (e)) is an ENCODING/STATE match, never numeric independence.

**The MPFR path, recorded**: no CLI/gmpy2/mpmath on this host — the system Homebrew
libmpfr 4.2.2 (`/opt/homebrew/lib/libmpfr.6.dylib` + `mpfr.h`) driven by a scratch C
generator (`target/p4-system-7/mpfr/vec_gen.c`). MPFR semantics measured and handled:
MPFR_RNDNA is documented DON'T-USE (RNDA behavior for the arithmetic ops — RMM goes
through `mpfr_round_nearest_away`); MPFR's own OF/UF flags are exponent-range-shaped
(useless for f32/f64 targets — OF/UF computed spec-side against a 2100-bit exact shadow);
MPFR canonicalizes NaN results (payloads dropped — NaN results are computed spec-side with
the IEEE quieting rule); MPFR's NAN flag is "result is NaN", not IEEE's NV (NV computed
spec-side: sNaN operands + the genuine invalids).

**The pinned target policy fp.rs serves** (pre-condition 4's list, measured against the
backend): canonical NaN `0x7fc00000` / `0x7ff8000000000000` on every NaN result;
NaN-boxing (upper bits all-1s; an unboxed input reads as the n-bit canonical NaN);
opStatus→NV/DZ/OF/UF/NX with the two deviations patched (OF by the magnitude rule; NV on
sNaN conversions); dyn/frm resolution with rm 101/110 reserved → illegal; FMA ∞×0 → NV;
fmin/fmax NaN rules (canonical on both-NaN, the non-NaN operand otherwise, the
signed-zero pair by sign); NaN→int → max + NV; subnormal passthrough (no FTZ).

**wasm proof (PORT-WEB)**: the scratch probe project (both candidates as path deps) builds
clean for `wasm32-unknown-unknown`.

## How to apply

- FP work on this profile uses `rustc_apfloat` through `fp.rs` ONLY — never the crate
  directly from an evaluator arm, never softfloat, never host floats.
- fp.rs implements, with the measurements above as its spec: the OF predicate (magnitude
  rule), the sNaN-on-conversion NV, the NaN→int value map (max + NV), the fmin/fmax
  signed-zero and canonical-NaN rules, the canonical NaN on every NaN result, the boxing,
  and **sqrt** (the one operation the backend lacks — derived spec-side, falsified against
  MPFR + the measured-clean softfloat sqrt).
- The crate's dependency lands pinned (`=0.2.3+llvm-462a31f5a5ab`); a version bump
  re-runs the scratch qualification (`probe run` regenerates the tables above).
- The fallback stays named (decision 1 of the `.7` brief): had neither candidate passed,
  the subset would be implemented in Rust and the capability deferred.
