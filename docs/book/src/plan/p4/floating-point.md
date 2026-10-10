# P4.7 — Floating point

**Status:** Landed and closed (slices a–b, c1–c6, d1–d5, e1–e3; 2026-10-06)

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


## Public FP-state observations

P4.13 c29b replaces internal-reference explanations with authenticated
RVP-MACHINE 2.1.1.6.7 and public instruction observations. FS Off requires an
illegal-instruction exception before the instruction accesses FP state. The
same chapter explicitly leaves Dirty-on-an-unchanged-write implementation
defined. This laboratory chooses Dirty on every f-register write, including a
write of the value already present. Every legal explicit write to fflags, frm
or fcsr also marks Dirty, including an unchanged value. Read-only moves preserve
Clean, while accrued flags mark Dirty when their stored bits change. Earlier book prose
incorrectly generalized the flag rule to every FP write; it is corrected above.

A twelve-instruction witness enables FP, writes1 to f1, sets FS Clean, writes
the same1 to f1 again, and reads mstatus and f1 through integer registers:

```
before identical FMV.D.X: mstatus = 0x0000000a00004000 (FS Clean, SD=0)
after  identical FMV.D.X: mstatus = 0x8000000a00006000 (FS Dirty, SD=1)
FMV.X.D read-back:        x12 = 1
```

The independent author derives these observations before CPU execution. A
separate direct core probe preserves f1's full bits and confirms Dirty after
the same-value write; its read-only FMV.X.D control preserves Clean. CSR storage
and architectural CSR views are distinguished: SD is computed by the public
CSR-read interface. The temporary diagnostic is removed and its source file
restored byte-for-byte before normal verification.

The public reference agrees on all12 boundaries in two byte-identical traces.
Changing only the expected post-write status to Clean is rejected at10.
All24 existing f-/d-/fp- guests also agree over927 boundaries, each in two fresh
identical traces. They include FS-Off, fcsr views, flag dirtiness and the numeric
families. These are finite observations of the published interface, without a
claim about the reference's internal functions or arithmetic backend.

The Machine/F/D pages are authenticated through their dossier source pins.
C29c corrects the
state descriptor and F requirement detail to state the same selected policy;
the current requirement statement and frozen obligation remain identical. The
statement promises Dirty whenever values change, without excluding unchanged
writes. Numerical contract realization and structured experiment registration
remain separate work.

The descriptor also supplies read-only census explanations in generated
inspection metadata. A prose change therefore requires published regeneration
and exact provenance/metadata checks. C29c changed one source hash and two
explanations in the state module, and two hashes in the definition; state
layout, CSR owners, resets, accessors and instructions stayed byte-identical.
Its stale-provenance refusals and complete source identities are retained
with the historical receipts below.



## Numeric instruction observations before F contract binding

The c32a witness drives **23 numeric F instructions** through the real
instruction decoder and executor. It reuses 1,504 single-precision rows from
the existing `FP-VECTORS`-governed text fixtures, excluding D's format
conversions. Expected bits and flags come from the exact-arithmetic reference;
the witness never calls the production FP backend to construct an expectation.
The shared fixture is included through a repository-relative path and remains
byte-checked by its existing generator and hardware controls.

Four fused forms use sign-adjusted inputs to retain the independent `a*b+c`
expected value. For example, the vector `(1+2^-23)*(1-2^-23)-1` is exactly
`-2^-46`, with no flags, under every rounding mode. FMADD uses addend `-1`;
FMSUB uses addend `+1`; FNMSUB negates the first multiplicand and uses
addend `-1`; FNMADD negates that multiplicand and uses addend `+1`. Each instruction still
rounds once. Wrong fused routing is rejected rather than accepted from a
matching operation name.

The expanded rows produce 3,104 static/dynamic settings. Rounded static
instructions run with `frm=7` to prove that their own valid rm overrides it;
dynamic instructions use each vector's mode. Unrounded operations also ignore
reserved frm. Across M/S/U, destinations 0/5/6/7/8/31 and initial flags 0/31,
**111,744 boundaries** preserve the literal full-state expectations and issue
exactly 223,488 fetch parcels. Destinations include all three FP source aliases;
f0 is writable, while an integer x0 destination discards only its result.
Word-sized integer conversion results are sign-extended to XLEN, including
unsigned conversion results whose bit 31 is set.

Every case starts FS Clean. An f-register write makes it Dirty; an integer
result preserves Clean when its accrued flags leave stored flags unchanged.
Flags remain sticky. All GPR/FPR values, raw CSR owners, PC/mode, reservation,
TLB entries/FIFO cursor, wait state, full memory, request sequence and extent
are compared. Twenty wrong effects/routes and sixteen corrupted captures
exercise the auditor; actual disabled observation, dynamic-rounding, boxing,
flag-accrual and Dirty paths must fail before byte restoration.

The independent instruction author agrees on the same numeric cases and the
original 167-guest corpus remains exact. The author and vector generator share
`specfp`; this agreement adds no new numeric lineage. These are finite numeric
instruction observations. The following c32b witnesses complete the F checks.


## Complete finite F contract witnesses

`CHK-GC-F-POS` and `CHK-GC-F-NEG` now run direct instruction witnesses and
tracked companion guests. The numeric matrix above remains unchanged. C32b
adds **92,088 positive boundaries** and **12,852 refusal/fault boundaries**;
together they observe all30 F forms over216,684 single-instruction boundaries.
This realizes the two F checks, taking effective G-CONTRACT to108/114. D,
reservation and deterministic SC remain, followed by final contract freeze.
Finite coverage does not mean an accepted processor profile.

The seven remaining forms preserve the distinctions that arithmetic tests
cannot establish:

| Operation | Worked observation |
| --- | --- |
| FLW | Memory word `0x7fa12345` becomes `0xffffffff7fa12345`; signaling payload unchanged, no flags, FS Dirty. |
| FSW | Register `0x123456787fa12345` stores exactly four bytes `45 23 a1 7f`; upper bits and neighboring bytes do not reach memory. FS stays Clean. |
| FMV.X.W | The same improperly boxed register yields integer `0x000000007fa12345`; raw low bits bypass computational unboxing. A negative low word sign-extends to XLEN. |
| FMV.W.X | Integer `0x123456787fa12345` becomes `0xffffffff7fa12345`; only the low word transfers, and FS becomes Dirty. |
| FSGNJ.S | Properly boxed signaling payload `0x7fa12345` with a negative second operand becomes `0xffa12345`; no NV flag. |
| FSGNJN.S / FSGNJX.S | Negate the second sign / XOR both signs while preserving the first operand's magnitude and NaN payload. |

Twelve low patterns cover all ten FP classes, with signed zeros, normals,
subnormals, infinities and quiet/signaling payloads. The three sign operations
cross both inputs, all four proper/improper-box layouts, M/S/U, six destination
choices and two initial flag sets:62,208 cases. An improperly boxed sign input
first becomes canonical qNaN; a properly boxed signaling input retains its bits.
Raw moves add2,592 cases over three upper patterns, including unboxed sources.
The integer x0 destination discards only its result; f0 remains writable.

FLW adds1,296 cases and FSW1,944, at offsets0/4/8. Exact W requests, store data,
full surrounding memory, preservation of Clean on a store, and all other state
are compared. FSW preserves the overlapping reservation: this laboratory's
selected policy changes it only through its own LR/SC. Seventy-two additional
same-value FLW/FMV.W.X controls prove that even an unchanged f-register write
makes FS Dirty. These start Clean and preserve the existing payload and flags.

Invalid-box numeric cases cover all19 F forms that read floating operands,
including each fused form and only operands that actually exist. Over12,456
cases, arithmetic produces boxed canonical qNaN; classification yields bit9;
FEQ yields0 without NV while FLT/FLE yield0 with NV. Min/max with one improper
input select the proper operand; two improper inputs yield canonical qNaN.
Conversions of the resulting qNaN saturate to the signed/unsigned maximum
with NV. An unsigned word result `0xffffffff` still sign-extends to XLEN.
Aliases, static/DYN rounding, sticky flags and Dirty-on-new-flags remain observed.

Another11,520 directed cases make rounding and range behavior explicit:

| Inputs / operation | Expected bits and flags |
| --- | --- |
| `1 + 2^-24` | RNE/RTZ/RDN:`0x3f800000`; RUP/RMM:`0x3f800001`; NX. The negative tie distinguishes RDN from RUP. |
| `0x00800000 * 0x3f7fffff` | RNE/RUP/RMM:`0x00800000`; RTZ/RDN:`0x007fffff`; UF+NX in every mode. |
| `0x00800000 * 0x3f7ffffe` | Exact largest subnormal:`0x007fffff`, no flags. |
| Fused `(1+2^-23)*(1-2^-23)-1` | Exactly `-2^-46` (`0xa8800000`), no flags; all four forms use the signed-term construction above. |
| Infinity, NaN or magnitude `2^64` converted to integer | Saturate by sign and destination range with NV; negative out-of-range unsigned inputs yield0. |

The UF boundary uses the selected IEEE rule: judge the rounded result as if
the exponent range were unbounded. Thus rounding to the smallest normal in
the destination format alone does not establish absence of underflow. The
literal expectations are re-derived with the independent exact-arithmetic
`specfp` reference. The instruction author and numeric generator share it;
their agreement adds no new numeric lineage.

The negative witness checks every F form with FS Off:30forms×M/S/U×six
register choices×two flag sets=1,080 cases. Loads/stores use an unmapped or
misaligned data address, yet only the two fetch parcels occur before cause2.
All17 rounded forms additionally cross19 reserved settings: static rm5/6
with every frm value, plus DYN with frm5/6/7. These11,628 cases trap with the
instruction word in mtval, instruction-start mepc, correct M privilege stack,
one cycle increment, no retirement and no instruction-owned writes.
Valid static rm ignoring reserved frm remains positive numeric evidence.
Ordinary memory faults add144 cases: cause4/6 before a data request for
misalignment, cause5/7 after exactly one W request at an unmapped address.
Faults retain FP state, flags, reservation, TLB cursor and memory.

Every expected state is constructed before execution. The comparator checks
all GPR/FPR values,26 raw CSR owners, PC/mode, reservation, TLB entries/FIFO
cursor, wait state, full memory, exact requests, fetch extent and outcome.
Twelve new wrong effects/routes complement the earlier20 numeric controls;
16 corrupted captures and16 actual disabled controls discriminate. Disabled
FS/rounding/boxing/width/sign/f0/trap-write/Dirty paths and observers must fail,
then source bytes are restored. The completed-check selector fails by the
missing F check name before the two registry entries are added. Prior108
entries and frozen/canonical inputs remain exact. Companion guests retain
their original expectations, and the original167-guest corpus remains exact.

## Historical verification receipts

Dated progress counts, pre-bind identity checks and exact provenance receipts
are preserved in `docs/tasks/archive/P4-SYSTEM-book-c29d.md`, section `floating-point`.
That record authenticates the original chapter and every removed span; all
current feature examples and commands remain here.
