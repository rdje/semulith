# P4-SYSTEM.13 c33b0 — historical FP implementation introduction

Finite immutable capture from source commit `07e14ae916cb9eddff66540f5e811589020c1ca3`, SEMULITH-P4-0181.
The original introduction remains byte-verbatim, in original order. The book
retains its executable example and current feature/policy descriptions.

Reconstruct the entire source chapter by verifying proposed bytes/SHA, replacing
exactly the replacement at offset with the marked original payload, then checking
source bytes/SHA and the named Git source. Offsets and lengths count bytes.
No later payload is appended here.

## Inverse map

```json
{
  "source": "docs/book/src/plan/p4/floating-point.md",
  "commit": "07e14ae916cb9eddff66540f5e811589020c1ca3",
  "source_bytes": 24259,
  "source_sha256": "ef2fd2d2d8395dbbf848d6b6a37b914c3b6d4499b60812d98db507edd8ad0db1",
  "proposed_bytes": 19145,
  "proposed_sha256": "e3a76b5f4225b2ead424d9534fb8c072fe01300f140fbf9f0c8f5f4e6db91e44",
  "offset": 112,
  "payload_bytes": 10576,
  "payload_sha256": "29beaf6cd8a28885c2fcae86a94f0e8641dc867b4a072b089ad1aba2eb252dab",
  "replacement": "The P4 [floating-point condition](../p4.md#the-floating-point-condition) has\nits qualified implementation: single and double precision execute in the\nexperimental processor. This closes the P4.7 feature leaf; it does not accept\nthe CPU profile or close its separate contract and evidence gates. The F/D\ncontract witnesses and their current coverage are described below.\n\nThe selected arithmetic dependency is `rustc_apfloat`, pinned to\n`=0.2.3+llvm-462a31f5a5ab` and verified for the wasm build. It supplies the\nrounding modes, exception flags, fused multiply-add and integer conversions\nthat this profile needs. The recorded softfloat capability census did not meet\nthat contract, although the operations it offered agreed with MPFR. Backend\nqualification and policy corrections are retained with the historical source\ncapture named below; agreement alone is not a claim of independent ancestry.\nEvery cargo invocation uses the project-local `.app-data/vendor/` store through\n`.cargo/config.toml`; `make vendor` populates it on the repository volume.\n\nThe canonical state owns f0–f31 at FLEN=64 and fcsr's two-owner view, composed\nfrom fflags and frm. Frm stores any three-bit value. A rounded instruction\nuses its static rm or, for DYN, frm; this laboratory selects an illegal trap\nfor reserved modes. FP instructions and FP CSR accesses require FS enabled\nin every privilege mode. The instruction gate runs before any instruction\neffect, so an FS-Off FLW raises illegal-instruction before attempting its data\naccess. Every f-register write marks Dirty, even unchanged values; flag accrual\nmarks Dirty only when stored bits change. The public observations below\nseparately distinguish raw CSR storage from the computed SD view.\n\nThe profile composes30 real F forms and32 real D forms from pinned encoding\ntables and its own canonical semantics. D requires F. The encoding fields rs3\nand rm describe the third fused source and rounding selector; register-file\nchoice belongs to the semantics. The assembler derives f0..f31 operand spelling\nfrom those rules and rejects the wrong register file. Upstream pseudo spellings\nare not additional decoder instructions. The shared semantics read f-registers\nfrom the instruction's prestate and state boxing and rounding explicitly:\n\n```text\nfadd.s   (set (freg rd) (fbox 32 (fadd 32 (rounding (field rm))\n                                   (funbox 32 (freg rs1)) (funbox 32 (freg rs2)))))\nfmv.x.w  (set (reg rd) (sext 64 (bits 31 0 (freg rs1))))   ; a transfer: bits, no unboxing\n```\n\nA single occupies the low32bits with every upper bit set. `fbox` creates that\nrepresentation; `funbox` treats any improper single box as canonical qNaN.\nTransfers copy raw bits under their width rules, while computational narrow\noperations check boxing. Double operations read the full64bits, so a boxed\nsingle appears as a negative double qNaN. FCVT.S.D narrows with rounding and\nwrites a boxed single; FCVT.D.S unboxes its source and widens exactly. Even\nexact numeric conversions still resolve their rounding selector under the\nselected reserved-mode policy. The numeric and transfer examples below retain\nthese distinctions rather than inferring one from the other.\n\nThe model layer, `fp.rs`, owns the RISC-V policies around the backend: canonical\nNaN results, NaN-to-integer saturation, min/max and comparison behavior,\nclassification and the fused infinity-times-zero invalid rule. It computes\nsquare root with an exact integer square root and uses the remainder to decide\nexactness. Overflow and underflow are judged at the same precision with an\nunbounded exponent range; the wider-exponent calculation supplies that test.\nRounding to a normal destination value alone does not decide the underflow\nflag. The directed boundary examples below make the selected rule concrete.\n\nThe qualification corrected its original MPFR overflow/underflow judgment and\nwithdrew a supposed signaling-NaN format-conversion backend defect: that backend\nalready raised NV, while the original MPFR oracle did not represent signaling\nNaNs. The corrected record names two genuine flag deviations, not three. This\nhistory is evidence about the named measurements, not permission to infer\nreference internals. The model's current conversion behavior is checked against\nthe independent exact-arithmetic rules and the instruction witnesses below.\n\n`FP-VECTORS` regenerates230 directed vectors and3168 fixture rows byte-for-byte\nfrom the spec-side exact-arithmetic reference and checks its RNE behavior against\nhost IEEE hardware. Numeric instruction witnesses reuse those governed rows;\nthe instruction author and generator share `specfp`, adding no numeric lineage.\nThe original floating-point guests also have public reference observations,\nwhose scope and controls are retained below. Exact overflow/underflow has a\nmeasured cost: the recorded qualification found roughly three to seven times\nthe bare arithmetic backend's operation cost. That finite benchmark does not\npromise a speed ratio on every host or input.\n\nThe original10576-byte introduction, including staged checkpoint counts,\nqualification corrections, corpus derivation and bind/closure receipts, is\npreserved byte-verbatim in `docs/tasks/archive/P4-SYSTEM-book-c33b0.md`. Its\ninverse map reconstructs this entire source chapter at the named commit.\nThe executable semantic example, all links and the current public FP-state,\nF witness and numeric D sections remain in this chapter.\n\n"
}
```

## Original introduction

<!-- c33b0 original introduction -->
````text
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
compares, the ten-way classification, the saturating conversions, and the selected
dirty rule: every f-register write marks Dirty, while accrued flags mark Dirty
when their stored bits change. Every expected
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
accumulate in `fflags`, every f-register write marks Dirty, and flag accrual marks
Dirty when it changes the stored flags.
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

Eleven double-precision programs were authored from the specification
before any processor-engine run.

The profile composes D, and all 32 double-precision forms execute in the
tracked engine alongside F. Both extensions are part of the processor.

Slice (e) gathers the leaf's closing evidence. Its first checkpoint ran all 24 floating-point
test programs on the Sail reference model: every one agrees with its specification-derived
expectations, step for step (927 steps). This public comparison measures the named
decode, gating, boxing, value and flag observations. The next checkpoint supplies
independent numeric evidence; no reference-backend implementation assumption is needed.

The second checkpoint made the numeric evidence broad and permanent: 3,168 generated test
cases — every floating-point operation, in both widths and all five rounding modes, with
operands chosen to hit the awkward classes (zeros, subnormals, infinities, NaNs, values at
the range edges) — each checked against the exact-arithmetic reference on every build. It
also measured the cost of exactness: computing overflow and underflow exactly makes each
rounded operation roughly three to seven times slower than the bare arithmetic library.

**The leaf is closed (2026-10-06).** The qualification record now ends with the evidence its
acceptance asked for: correctness measured three ways — thousands of specification-derived
cases checked on every build, zero disagreements across the original 63,752-case corpus, and
all floating-point programs agreeing with the Sail reference — and the measured cost of the
model layer. Single and double precision are part of the processor.


````
