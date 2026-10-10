# P4.7 — Floating point

**Status:** Landed and closed (slices a–b, c1–c6, d1–d5, e1–e3; 2026-10-06)

The P4 [floating-point condition](../p4.md#the-floating-point-condition) has
its qualified implementation: single and double precision execute in the
experimental processor. This closes the P4.7 feature leaf; it does not accept
the CPU profile or close its separate contract and evidence gates. The F/D
contract witnesses and their current coverage are described below.

The selected arithmetic dependency is `rustc_apfloat`, pinned to
`=0.2.3+llvm-462a31f5a5ab` and verified for the wasm build. It supplies the
rounding modes, exception flags, fused multiply-add and integer conversions
that this profile needs. The recorded softfloat capability census did not meet
that contract, although the operations it offered agreed with MPFR. Backend
qualification and policy corrections are retained with the historical source
capture named below; agreement alone is not a claim of independent ancestry.
Every cargo invocation uses the project-local `.app-data/vendor/` store through
`.cargo/config.toml`; `make vendor` populates it on the repository volume.

The canonical state owns f0–f31 at FLEN=64 and fcsr's two-owner view, composed
from fflags and frm. Frm stores any three-bit value. A rounded instruction
uses its static rm or, for DYN, frm; this laboratory selects an illegal trap
for reserved modes. Pinned F §20.1.2 reserves static rm=5/6 and dynamic
frm=5/6/7 and explicitly permits the selected illegal-instruction behavior.
For example, rm=0 selects RNE regardless of frm; rm=7 with frm=3 selects RUP;
rm=5 or rm=7 with frm=7 traps. FP instructions and FP CSR accesses require FS enabled
in every privilege mode. The instruction gate runs before any instruction
effect, so an FS-Off FLW raises illegal-instruction before attempting its data
access. Every legal explicit f-register or FP-CSR write marks Dirty, even unchanged
values; flag accrual marks Dirty only when stored bits change. These are the
laboratory's selected policies under pinned Machine §2.1.1.6.7's latitude for
unchanged contents, rather than a requirement to copy a reference's default.
The public observations below
separately distinguish raw CSR storage from the computed SD view.

The profile composes30 real F forms and32 real D forms from pinned encoding
tables and its own canonical semantics. D requires F. The encoding fields rs3
and rm describe the third fused source and rounding selector; register-file
choice belongs to the semantics. The assembler derives f0..f31 operand spelling
from those rules and rejects the wrong register file. Upstream pseudo spellings
are not additional decoder instructions. The shared semantics read f-registers
from the instruction's prestate and state boxing and rounding explicitly:

```text
fadd.s   (set (freg rd) (fbox 32 (fadd 32 (rounding (field rm))
                                   (funbox 32 (freg rs1)) (funbox 32 (freg rs2)))))
fmv.x.w  (set (reg rd) (sext 64 (bits 31 0 (freg rs1))))   ; a transfer: bits, no unboxing
```

A single occupies the low32bits with every upper bit set. `fbox` creates that
representation; `funbox` treats any improper single box as canonical qNaN.
Transfers copy raw bits under their width rules, while computational narrow
operations check boxing. Double operations read the full64bits, so a boxed
single appears as a negative double qNaN. FCVT.S.D narrows with rounding and
writes a boxed single; FCVT.D.S unboxes its source and widens exactly. Even
exact numeric conversions still resolve their rounding selector under the
selected reserved-mode policy. The numeric and transfer examples below retain
these distinctions rather than inferring one from the other.

The model layer, `fp.rs`, owns the RISC-V policies around the backend: canonical
NaN results, NaN-to-integer saturation, min/max and comparison behavior,
classification and the fused infinity-times-zero invalid rule. It computes
square root with an exact integer square root and uses the remainder to decide
exactness. Overflow and underflow are judged at the same precision with an
unbounded exponent range; the wider-exponent calculation supplies that test.
Rounding to a normal destination value alone does not decide the underflow
flag. The directed boundary examples below make the selected rule concrete.

The qualification corrected its original MPFR overflow/underflow judgment and
withdrew a supposed signaling-NaN format-conversion backend defect: that backend
already raised NV, while the original MPFR oracle did not represent signaling
NaNs. The corrected record names two genuine flag deviations, not three. The generator
comment and three directed conversion labels now follow that correction; all
230 numeric rows and 3,168 fixture rows retain their exact bits and flags. This
history is evidence about the named measurements, not permission to infer
reference internals. The model's current conversion behavior is checked against
the independent exact-arithmetic rules and the instruction witnesses below.

`FP-VECTORS` regenerates230 directed vectors and3168 fixture rows byte-for-byte
from the spec-side exact-arithmetic reference and checks its RNE behavior against
host IEEE hardware. Numeric instruction witnesses reuse those governed rows;
the instruction author and generator share `specfp`, adding no numeric lineage.
The original floating-point guests also have public reference observations,
whose scope and controls are retained below. Exact overflow/underflow has a
measured cost: the recorded qualification found roughly three to seven times
the bare arithmetic backend's operation cost. That finite benchmark does not
promise a speed ratio on every host or input.

The original10576-byte introduction, including staged checkpoint counts,
qualification corrections, corpus derivation and bind/closure receipts, is
preserved byte-verbatim in `docs/tasks/archive/P4-SYSTEM-book-c33b0.md`. Its
inverse map reconstructs this entire source chapter at the named commit.
The executable semantic example, all links and the current public FP-state,
F witness and numeric D sections remain in this chapter.

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
This realized the two F checks, taking effective G-CONTRACT to108/114.
The D completion below advances that count; reservation/SC and freeze remain.
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


## Numeric D prerequisite before binding

C33a generalizes the private numeric fixture by explicit source and result
width. The shared module is now `floating.rs`, with F's remaining cases in
`floating/single.rs`; all216,684 F boundaries remain unchanged in effect.
C33a deliberately gave D no registry credit; the completion below now binds it.

The D matrix includes1,504 ordinary double rows and160 format-conversion rows
from the same governed numeric data. Both destination widths belong to D.
Four fused forms expand these to1,904 cases; static/DYN rounding yields3,424
settings. Across M/S/U, six destinations including all source aliases, and
flags0/31, **123,264 boundaries** require exactly246,528 fetch parcels.
D operands and results retain full64bits. FCVT.D.S unboxes its single input;
FCVT.S.D NaN-boxes its single result. Word integer results still sign-extend.

Two literal rows show the format distinction:

| Instruction/input | Expected result/flags |
| --- | --- |
| FCVT.S.D, RUP, `0xfff0000000000001` | Boxed canonical single `0xffffffff7fc00000`, NV: the source is a signaling double NaN. |
| FCVT.D.S, RMM, boxed `0x007fffff` | Double `0x380fffffc0000000`, no flags: widening the largest single subnormal is exact. |

Every rounded form resolves rm even where a legal mode cannot alter the
numeric result. Reserved-mode refusals, improperly boxed conversion inputs,
raw transfers/sign payloads and directed D rule cases belong to the completion
slice. Full state, memory, requests, sticky flags and selected Dirty behavior
use the same pre-execution comparator as F. Sixteen wrong numeric routes and
nine actual disabled controls must fail before source restoration. The
independent instruction author agrees on all new cases; it shares `specfp`
with the vector generator, adding no numeric lineage. The original167-guest
corpus remains exact. The following completion supplies the remaining D checks.

## Complete finite D contract witnesses

`CHK-GC-D-POS` and `CHK-GC-D-NEG` now bind all32 D forms with direct witnesses
and tracked companion guests. The numeric prerequisite remains123,264 positive
boundaries. Completion adds96,696 positive and14,292 refusal/fault boundaries:
**234,252 boundaries, 468,504 fetch parcels and2,844 data requests** in total.
Effective G-CONTRACT becomes110/114; reservation, deterministic SC and final
freeze remain open. These finite observations do not accept the CPU profile.

| Operation / input | Expected observation |
| --- | --- |
| FLD / FMV.D.X, `0x7ff0123456789abc` | Full64 signaling payload retained, no NV, FS Dirty even when destination bits were identical. |
| FSD, same payload | Eight bytes `bc 9a 78 56 34 12 f0 7f`; neighboring bytes and FS preserved. |
| FMV.X.D, `0xffffffff3f800000` | Exactly the same64bits, with no computational unboxing or word sign extension. |
| FSGNJ.D with negative second sign | First magnitude/payload retained, second sign copied. FSGNJN negates that sign; FSGNJX XORs both signs. No flags. |
| Boxed single `0xffffffff7fa12345` used by D arithmetic | A negative double quiet NaN; canonical D result, no signaling NV from its low single payload. |
| FCVT.D.S, proper boxed `0x7fa12345` | Canonical double `0x7ff8000000000000`, NV. Improper upper32bits instead supply canonical single qNaN, no NV. |
| `1 + 2^-53` | RNE/RTZ/RDN:`0x3ff0000000000000`; RUP/RMM:`0x3ff0000000000001`; NX. Negative tie distinguishes RDN/RUP. |
| `0x0010000000000000 * 0x3fefffffffffffff` | RNE/RUP/RMM:minimum normal; RTZ/RDN:largest subnormal; UF+NX in every mode under the unbounded-exponent rounding rule above. |
| Same minimum normal times `0x3feffffffffffffe` | Exact largest subnormal `0x000fffffffffffff`, no flags. |
| Fused `(1+2^-52)*(1-2^-52)-1` | Exact `-2^-104`, bits `0xb970000000000000`, no flags; all four signed-term forms. |

Sixteen raw64patterns cover all ten classes, signed NaN payloads, boxed singles
and an ordinary non-boxed double. Sign operations cross both operands:27,648
cases. Raw moves add1,152; loads1,728 and stores864 at offsets0/8/16 compare
exact D requests and32 surrounding bytes. Stores retain an overlapping
reservation under this selected one-hart policy. Same-value writes add72.
All matrices cross M/S/U, source aliases, x0/f0 and flags0/31. Another2,304
representative cases exercise every form with FS Initial and Dirty; Clean is
covered by the main matrices. x0 discards results; f0 remains writable.

Boxed-single-as-double observations add38,448 cases over all20 numeric forms
that read full-width FP operands and applicable operand positions. They retain
min/max one-NaN selection, classification bit9, FEQ versus FLT/FLE NV behavior,
integer saturation and sticky flags. FCVT.D.S adds12,960 proper/improper-box
cases. Directed ties, exact/tiny results, four fused forms and six signed
range/NaN inputs across four integer conversions add11,520 cases, including
all legal static/DYN rounding modes. Word integer results sign-extend.

Every D form refuses FS Off:1,152 cases. All19 rounded forms cross19 reserved
rm/frm settings:12,996 cases, including exact FCVT.D.W[U]/D.S. Unmapped or
misaligned data addresses establish FS gate priority: only fetch occurs before
cause2. Ordinary memory faults add144 cases, with cause4/6 before data access
or cause5/7 after one D request. Exact trap stack, nonretirement and suppression
of instruction-owned writes are compared with full state, requests and memory.

Fifteen new wrong transfer/sign/memory/format effects supplement16 numeric
wrong routes. Sixteen corrupted captures and18 actual disabled controls fail
before byte restoration. A proposed unused Bits-node mutation did not reach
the compiled sign operation; only the corrected masked-AND control is credited.
Missing-binding failure precedes the two entries; prior110 entries remain exact.
The independent instruction author agrees on all new and prior cases and the
167-guest corpus. It shares `specfp` with the numeric generator; agreement adds
no numeric lineage. Frozen records, numeric data and production core are exact.

## Historical verification receipts

Dated progress counts, pre-bind identity checks and exact provenance receipts
are preserved in `docs/tasks/archive/P4-SYSTEM-book-c29d.md`, section `floating-point`.
That record authenticates the original chapter and every removed span; all
current feature examples and commands remain here.
