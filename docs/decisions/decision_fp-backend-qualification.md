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

> **Amended `2026-10-06` (`P4-SYSTEM.7` slice (c4))** — see "Amendment" at the end: the
> model layer landed at slice (c4), not (b); the overflow count below is 290, not 362 (72 were
> the oracle's false overflows); a THIRD deviation exists (underflow), invisible to this
> record's oracle because the oracle shared it; the manifest pin is expressed `=0.2.3`.
>
> **Amended again `2026-10-06` (`P4-SYSTEM.7` slice (d3))** — see the second amendment at
> the end: deviation (ii) below is WITHDRAWN. Its 24 cases were the MPFR oracle's silence
> (MPFR has no signaling NaN), not the backend's: the backend raises NV for a signaling NaN
> through a format conversion. The backend's genuine flag deviations are TWO — overflow on a
> directed-mode clamp (290) and underflow at the smallest-normal boundary.

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

## Amendment — `2026-10-06`, `P4-SYSTEM.7` slice (c4): the oracle shared two of the backend's conventions

Writing the model layer against a SECOND spec-side oracle — `scripts/specfp.py`, exact
rationals written from the pinned chapters and IEEE 754-2008 (checked against the host's
hardware IEEE in RNE) — exposed two rule defects in this record's MPFR generator
(`target/p4-system-7/mpfr/vec_gen.c`) and one deviation they had hidden:

- **Overflow.** The generator flagged OF when the EXACT magnitude exceeded the largest finite.
  IEEE 754-2008 §7.4 judges "what would have been the rounded floating-point result were the
  exponent range unbounded": MAX+1 in RTZ rounds back to MAX and is NO overflow (Berkeley
  SoftFloat's RISC-V roundPack agrees — `sig + roundIncrement` at full precision). Re-run with
  the corrected rule, 72 of the 362 "deviation (i)" cases were the oracle's false overflows and
  the backend was right; the genuine deviation (i) is **290 cases**, the total flag
  disagreements **314** (290 + the 24 of deviation (ii)), not 386.
- **Underflow — deviation (iii), new.** The generator flagged UF when the DELIVERED result was
  subnormal — the backend's own convention — so the two agreed by construction. RISC-V
  specifies tininess AFTER rounding (RVI-F §20.1.4), which §7.5 defines on the
  unbounded-exponent rounded result: 2^-126·(1−2^-24) is tiny, and when it rounds (RNE, RUP,
  RMM) up to the smallest normal the result is still an UNDERFLOW (tiny and inexact) — the
  backend raises none (measured; SoftFloat's RISC-V specialization, `init_detectTininess` =
  after rounding, raises it). The slice-(a) corpus never contained that boundary.
- **The model layer computes both flags from one exact value**: the same operation in a
  backend format with the SAME precision and a 15-bit exponent (`fp.rs`'s `WideSingleS` /
  `WideDoubleS`) — rounding there IS rounding with an unbounded exponent. OF = that value
  finite and beyond the largest finite; UF = that value tiny and the delivered result inexact.
- **Re-qualification of the model layer** (scratch: `target/p4-system-7/fpcheck/`): over the
  same 63,752-case corpus, `fp.rs` disagrees with the corrected MPFR oracle on **0 of 51,840**
  comparable cases (canonical-NaN transform; compares excluded — the generator's compare-NV
  logic is not a reference) and with the exact-rational reference on **0 of 63,480**; a
  one-line corruption is caught by both (the RED control). The tracked proof is the 176
  spec-side unit vectors (`crates/semulith-core/src/fp/tests/vectors.rs`, gated by
  FP-VECTORS), which include the underflow boundary.
- **The pin, expressed honestly.** Cargo ignores build metadata in a version REQUIREMENT (it
  warned on every build); the manifest now reads `=0.2.3`, and the exact artifact
  `0.2.3+llvm-462a31f5a5ab` is pinned by `Cargo.lock`'s version string and checksum, verified
  against the on-volume vendored copy (`.cargo/config.toml`, slice (c4) part 1).

The lesson is the record's own subject, one level down: a second lineage is not a second
opinion when its DERIVATION shares the first one's convention — the oracle's rule text has to
be checked against the specification's sentence, not against the thing it judges
([[decision_claim-verification-adopted]]; `docs/knowledge/an-oracle-can-share-the-convention-it-judges.md`).

## Amendment — `2026-10-06`, `P4-SYSTEM.7` slice (d3): deviation (ii) was the oracle's

Writing `fp.rs`'s format conversion (`f2f`, FCVT.S.D/FCVT.D.S) to "patch deviation (ii)", the
model layer's vectors passed with the patch BYPASSED — so the patch was dead, and the backend
was measured directly instead of trusted to the record:

```
rustc_apfloat 0.2.3, convert_r (the slice-(a) probe's own call, target/p4-system-7/probe):
  d->s 0x7ff4000000000000 (sNaN): status INVALID_OP     d->s 0x7ff8000000000001 (qNaN): 0
  s->d 0x7fa00000         (sNaN): status INVALID_OP     s->d 0x7fc00001         (qNaN): 0
$ grep -cE "FLAGS (f32_64|f64_32) .*apfloat NV, mpfr -" probe/run.corrected.txt → 24
$ grep -E "FLAGS (f32_64|f64_32)" probe/run.corrected.txt | grep -v "apfloat NV, mpfr -"
  → the 4 RTZ/RDN/RUP clamp rows of deviation (i) (apfloat NX, mpfr OFNX) — nothing else
```

Every one of the 24 disagreements is **backend NV, oracle none**. The MPFR generator reads a
binary NaN through `mpfr_set_flt`/`mpfr_set_d` into MPFR's single NaN kind — it has no
signaling NaN, so it cannot raise invalid for one — and the record read the oracle's silence
as the backend's omission. IEEE 754-2008 §7.2 makes an operation on a signaling NaN invalid;
the backend is right. **Consequences:** the genuine backend flag deviations are two — (i)
overflow on a directed-mode clamp, 290 cases (the 4 conversion clamps among them), and (iii)
underflow at the smallest-normal boundary; of the 314 flag disagreements, 24 are this
record's oracle. `fp.rs::convert` relies on the backend's `INVALID_OP` (the result
canonicalized by the common tail), and its 54 spec-side conversion vectors — signaling NaNs
both ways among them — pass on the backend's own status. The text above is kept verbatim as
the record of what was believed; this amendment is the correction.

It is the c4 lesson a third time, in its starkest form: an oracle cannot disagree about a
case it cannot represent, and the disagreement it reports there belongs to the oracle.

