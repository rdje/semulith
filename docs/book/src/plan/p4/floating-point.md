# P4.7 — Floating point

**Status:** Underway (slices a–b, c1–c4; 2026-10-06)

The P4 chapter's [floating-point condition](../p4.md#the-floating-point-condition) now has its
measurement. Slice (a)
re-measured the two candidates from the fetched artifacts (licenses,
provenance, capability), then probed both against each other and MPFR vectors —
63,752 cases, per op × 5 rounding modes × both widths. **rustc_apfloat is
QUALIFIED**: the arithmetic core (add/sub/mul/div/fma) is MPFR-exact, zero core
disagreements; the 612 value + 386 flag disagreements are named policy surfaces
fp.rs owns (NaN→int, fmin/fmax, NaN payloads) or two measured LLVM-vs-IEEE flag
deviations. softfloat fails the capability census (no rounding modes, no flags,
no FMA, no 64-bit conversions, no min/max) though MPFR-exact where it exists,
sqrt included. The dependency is pinned (`=0.2.3+llvm-462a31f5a5ab`),
wasm-proven. Slice (b) landed the FP state: the f0–f31 file (FLEN=64) declared
and census-gated; mstatus.FS now gates the FP CSRs in every mode (the
`fp_enabled()` hook awaits the binds' arms); fcsr's two-owner view composes —
the pre-slice engine read 0 and refused writes. Two FS=Off/fcsr guests;
103/103; the pre-slice corpus byte-identical. Slice (c), the F bind, executes in
six checkpoints. Its first, (c1), corrected slice (b) at root: `frm` had been
declared WARL one-of 0..4, retaining its old value on any other write — but the
chapter says FSRM writes "the three least-significant bits of integer register
rs1 into frm", and its rounding-mode table names 101–111 *dynamic reserved*
modes, a state frm can only reach by holding them. `frm` now stores any 3-bit
value; an instruction meeting a reserved mode (static 101/110, dynamic 101–111)
will raise illegal-instruction — the pinned revision weakened that mandate to
"reserved" but still calls it valid, and it is Sail's configured behaviour. The
guest pinning the old rule was re-derived spec-side first and caught the
unfixed engine (fcsr read `0x45` where the spec gives `0xE5`).
Checkpoint (c2) pinned the upstream F tables (`rv_f`, `rv64_f`: 26 + 4 forms) and
generated the repository's own `f.sexp` fragment from them. It owns two new operand
fields — `rs3`, the fused multiply-adds' third source, and `rm`, the rounding-mode
field — while `rd`/`rs1`/`rs2` stay the base's: which register *file* an operand
names is the instruction's meaning, so it will come from the semantics, not the
encoding table. The tables' thirteen pseudo-instructions (`fmv.s`, `frcsr`, …) are
not carried: they are spellings of real instructions, and guests write the real
form, as everywhere else in this repository.

Checkpoint (c3) taught the semantics language floating point. The shared rules are stated
once, as the meaning of the new operators: reading `(freg x)` sees the register file as it
was before the instruction; writing an f-register marks `mstatus.FS` Dirty; every
instruction whose rule touches floating-point state is illegal while FS is Off — judged
before it does anything, so an `flw` with FS Off raises illegal-instruction, never its
load's fault; arithmetic rounds once, keeps subnormals, returns the canonical NaN, and ORs
its exception flags into `fflags`. The thirty F rules then read like the chapter:

```text
fadd.s   (set (freg rd) (fbox 32 (fadd 32 (rounding (field rm))
                                   (funbox 32 (freg rs1)) (funbox 32 (freg rs2)))))
fmv.x.w  (set (reg rd) (sext 64 (bits 31 0 (freg rs1))))   ; a transfer: bits, no unboxing
```

`fbox`/`funbox` are NaN-boxing made visible (the D chapter's rule — a single lives in the
low half of a 64-bit register whose upper half is all ones). Because the rules say which
operands are f-registers, the assembler now derives its `f0..f31` spelling from them, and
refuses the wrong one by name. Nothing executes yet: the generated module grows the
floating-point vocabulary only at the bind.

Checkpoint (c4) landed the **model layer**, `fp.rs` — the one place the RISC-V rules meet
the arithmetic backend. It returns the canonical NaN for every NaN result, unpacks and packs
NaN-boxed singles, resolves the rounding mode, implements min/max, the compares and the
class mask directly in bits, converts a NaN to the integer maximum, applies the fused
multiply-add's ∞×0 rule — and computes the **square root** itself, because the backend has
none: an exact integer square root whose remainder says whether the result is exact.

Overflow and underflow are where it got interesting. IEEE 754 defines both on the result
"computed as though the exponent range were unbounded". `fp.rs` computes exactly that value —
the same operation at the same precision with a far wider exponent — and judges both flags
on it. Against a new spec-side reference (exact fractions, written from the standard and
checked against the computer's own IEEE hardware), three test vectors failed at one boundary:
a value just below the smallest normal number that rounds *up* to it is still an underflow,
and the backend did not say so. The slice-(a) qualification had missed it because its MPFR
oracle judged underflow the backend's way; the same oracle had also counted 72 false
overflows against the backend. Corrected, `fp.rs` agrees with both oracles on every one of
the 63,752 cases, and the qualification record carries a dated amendment. The test vectors
and their reference are tracked and gated (FP-VECTORS), and the reference is re-checked
against the hardware on every commit.

The same checkpoint fixed where the build gets its dependencies: the backend crate had been
resolved from a cache in the user's home directory, off the repository's volume; every cargo
command now reads it from `.app-data/vendor/` (`make vendor`).

Checkpoint (c5) wrote the **F test corpus** before the instructions are switched on: eleven
small guest programs — the floating-point unit switched off, NaN-boxing and the bit-exact
moves, every rounding mode (and the two reserved ones, which must trap), the five exception
flags, the fused multiply-adds, sign injection, minimum/maximum around ±0 and NaN, the
compares, the ten-way classification, the saturating conversions, and the rule that the
floating-point state becomes "dirty" only when something actually changes. Every expected
value is derived from the specification, never from the engine. Deriving the fused forms
showed the reference could only compute the first of the four (`(a×b)+c`); it now builds
all four from their signed terms as the chapter writes them, and is checked against a second,
independent construction on 464,000 cases. On an engine staged outside the tracked tree the
corpus passes 114 of 114, the 103 older programs run byte-identically, and all eleven new
ones fail on the previous engine — as they must.

Checkpoint (c6) is **the bind**: the profile now composes the F extension, and its 30
single-precision instructions execute in the tracked engine. With the floating-point unit
off, every one of them traps before it can touch anything; otherwise each rounded operation
takes its mode from the instruction or from `frm` (a reserved mode traps), its flags
accumulate in `fflags`, and the state is marked dirty only when something actually changed.
The instruction census grows from 88 to 118, matching the pinned upstream tables exactly,
and all 114 test programs pass — the 103 that existed before byte-for-byte unchanged.

Slice (d) brings in **double precision** the same way, in five checkpoints. The first pinned
the upstream D tables (32 instructions) and generated their definition fragment, which
declares that it needs F — D reuses F's register-file fields and the specification makes D
depend on F; a composition that tries D without F is refused by name. Because every
floating-point operation in the semantics language already takes its width as data, D needs
only one new operation: converting between single and double precision.

The second checkpoint wrote the 32 double-precision rules. Each is its single-precision
counterpart at width 64 — the specification itself defines them "analogously" — except the
two format conversions, which needed the language's one new operation. The assembler learns
which register file each D operand uses from those rules alone, and agrees with an
independent disassembler on all 32 instructions.

The third checkpoint added the conversion itself, and corrected the record. The backend's
qualification had listed a second flag defect: no "invalid" flag when a signaling NaN is
converted between formats. The fix was written — and the tests passed with it switched off.
Probed directly, the backend does raise the flag; every one of the 24 recorded cases came from
the reference oracle, which has no notion of a signaling NaN at all. The qualification record
now carries that correction: the backend has two genuine flag deviations, not three.

The fourth checkpoint wrote the double-precision test programs — eleven of them, each
expected value derived from the specification by the authoring model before any engine ran.
On an engine staged outside the tracked tree, all 125 programs pass; the 114 that existed
before run byte-for-byte unchanged, and every new one fails on the previous engine.

The fifth checkpoint is **the bind** for double precision: the profile composes D, and its
32 instructions execute in the tracked engine. The instruction census grows from 118 to 150,
matching the pinned upstream tables exactly, and all 125 test programs pass — the 114 that
existed before unchanged. Both floating-point extensions now run; what remains of this leaf is
broader numeric evidence, the structural comparison against the Sail reference, and the
leaf's own acceptance.
