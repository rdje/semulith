# P4.7 — Floating point

**Status:** Underway (slices a–b, c1–c3; 2026-10-06)

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
