# P4.13 — Integer runtime contract witnesses

[Contract completion](contract-v2.md) tracks effective counts;
[system runtime witnesses](contract-runtime.md) retain privilege, translation and timers.

## Immediate ALU semantics through existing boundary programs

At c14b, CHK-ALU-IMM-POS runs scope-alu and NEG runs bound-arith. Both are
whole legal programs; NEG rejects incorrect semantic alternatives such as
saturation or wrong signedness, rather than requiring a trap for valid ALU
instructions. All six forms are exercised: ADDI, SLTI, SLTIU, XORI, ORI and ANDI.
Their shared twelve-bit immediate sign-extends before the operation. ADDI wraps
modulo 2^64; SLTI compares signed, while SLTIU treats the sign-extended immediate
as unsigned. These clauses are pinned at RVI-RV32I 1.1.4.1.

Each guest spans 31 boundaries /62 parcel requests; all committed GPR changes,
never-written registers and fetch counts use the existing corpus rule. Independent
replay agrees with the entire 62/124 pair. Representative zero-based steps:

| Guest/step | Operation | Observed value |
| --- | --- | --- |
| scope-alu, step 8 | ANDI x9,x4,-1, x4=0xffffffff80000000 | x9=0xffffffff80000000 |
| scope-alu, step 9 | ORI x10,x4,2047 | x10=0xffffffff800007ff |
| scope-alu, step 10 | XORI x11,x4,-1 | x11=0x000000007fffffff |
| scope-alu, step 14 | SLTI x14,x4,1 | x14=1 |
| scope-alu, step 16 | SLTIU x15,x4,1 | x15=0, visibly overwriting 1 |
| scope-alu, step 17 | SLTIU x16,x4,-1 | x16=1 |
| bound-arith, step 8 | ADDI x7,INT64_MIN,-1 | x7=0x7fffffffffffffff |
| bound-arith, steps 9/10 | ADDI with -2048 /2047 | x8=0xfffffffffffff800 /x9=0x7ff |

Five in-memory author copies are deliberately wrong. Zero-extended SLTIU fails
scope-alu, step 17; unsigned SLTI fails at step 14; zero-extended ANDI fails at step 8; zero-extended XORI
fails at step 10; saturating ADDI fails bound-arith, step 8. The existing integer-author sign
control also refuses. No source, expectation, frozen record, production author
or processor semantics changes. All 72 prior registry entries remain exact.
The repaired gate oracle passes with the ALU pair now actually registered.

At c14b, G-CONTRACT reached **72/114**: thirteen scope pairs, sixteen guest pairs,
six direct assumption pairs and one direct execution pair. The registry has 74
entries including two historical superseded bindings. Twenty-one runtime pairs
and final freeze remain; no universal execution or firmware acceptance is claimed.

## Register ALU wrapping, signedness and overlapping operands

At c15, CHK-ALU-REG-POS runs scope-alu and bound-arith; NEG runs bound-alias.
These whole legal programs cover ADD, SUB, SLT, SLTU, XOR, OR and AND. Overflow
is ignored: ADD/SUB retain the low 64 bits. SLT compares signed values; SLTU
compares unsigned. Logical forms operate bitwise. Both sources are read from
the pre-state before the destination is written, including rd=rs1=rs2.
Pinned RVI-RV32I 1.1.4.2 supplies these rules; shifts have their own contract pair.

Independent replay matches every committed observation: scope-alu 31/62,
bound-arith 31/62 and bound-alias 37/74 (99 boundaries  / 198 parcels total).
Selected zero-based observations make the differences visible:

| Guest/step | Operation or operands | Value |
| --- | --- | --- |
| scope-alu, steps 5/6/7 | AND/OR/XOR of 0x654 and 0x470 | 0x450 / 0x674 / 0x224 |
| scope-alu, step 11 | Signed SLT of -1 and 1620 | x12=1 |
| scope-alu, step 13 | Unsigned SLTU of the same bits | x13=0, overwriting 1 |
| bound-arith, step 5 | INT64_MAX +1 | x3=0x8000000000000000 |
| bound-arith, step 6 | INT64_MIN -1 | x5=0x7fffffffffffffff |
| bound-alias, step 24 | ADD x20,x20,x20 with x20=5 | x20=10 |
| bound-alias, steps 26/28 | SUB/SLT with identical sources | x21=0 / x22=0, both visible overwrites |

Eight deliberately incorrect author copies fail exact steps: saturation at
bound-arith steps 5/6; swapped comparison signedness at scope-alu steps 11/13; wrong AND/OR/XOR
operators at scope-alu steps 5/6/7; cleared aliased ADD sources at bound-alias step 24. The
existing integer-author controls and full normal corpus comparison retain their
authority. NEG rejects these semantic alternatives, not a required trap for
valid register arithmetic. All 74 earlier registry entries and every old input
remain exact; no processor or production-author semantics changes.

At c15, G-CONTRACT reached **74/114**: thirteen scope pairs, seventeen guest pairs,
six direct assumption pairs and one direct execution pair. The registry keeps 76
entries, including two superseded historical checks. Twenty runtime pairs and
final freeze remain; CPU-SYSTEM stays open.

## U-immediates use a signed offset and the instruction address

CHK-LUI-AUIPC-POS runs scope-alu and dir-chase; NEG runs bound-arith. These
legal programs distinguish the exact RV64I 3.1.2.1 rules: LUI forms a 32-bit
value with twelve low zero bits, then sign-extends it to 64 bits. AUIPC forms
that same signed offset and adds it to its own instruction address, wrapping
the address sum at 64 bits. It does not sign-extend the instruction address.
The pinned 49,246-byte RV64I chapter was rehashed and read before registration.

Independent replay matches all 79 boundaries / 158 parcels and observations.
Selected zero-based steps show why truncating or advancing the PC is observable:

| Guest/step | Computation | Result |
| --- | --- | --- |
| scope-alu, 3 | LUI 0x80000 | x4=0xffffffff80000000 |
| bound-arith, 28 | LUI 0x7ffff | x22=0x7ffff000 |
| bound-arith, 29 | AUIPC at 0x80000074, signed offset 0xffffffff80000000 | x23=0x74 |
| bound-arith, 30 | AUIPC at 0x80000078, offset 0x7ffff000 | x24=0xfffff078 |
| dir-chase, 0/4/7 | AUIPC offset zero | x1=0x80000000, x2=0x80000010, x3=0x8000001c |

Seven in-memory wrong author copies fail intended observations: LUI zero
extension or missing shift at scope step 3; AUIPC zero extension, missing shift
or unsigned saturation at bound step 29; next-PC or sign-extended base-PC at
chase step 0. The whole programs and their intermediate observations matter.
NEG rejects wrong legal arithmetic, not a required architectural exception.
The existing independent integer probe remains green; no production rule or
expected value changes. Both smoke-arith headers now name profile.sexp and the
assembler's implemented B/J support; each still assembles to the same twelve
instructions / 48 bytes. Generated guest data is exact, with only those source
fingerprint comments regenerated. That base-profile comment also changes the dossier
digest: the commit hook refused the stale board processor pin. The pin was deliberately
rederived through the shared digest owner, then board/platform artifacts and model-book
materials regenerated. Their semantic data, map and text stay exact except that identity
pin and provenance fingerprints. Frozen records and all 76 earlier entries stay exact.

Current G-CONTRACT is **76/114**: thirteen scope pairs, eighteen guest pairs,
six direct assumption pairs and one direct execution pair. There are 78 registry
entries including two superseded historical checks. Nineteen runtime pairs and
final freeze remain; CPU-SYSTEM stays open.

## SRAW count-mask coverage hole before registration

Before CHK-SHAMT is registered, an isolated wrong SRAW rule using rs2[5:0]
instead of rs2[4:0] still matches all 167 guests / 5,360 boundaries / 10,514
parcels in an independent author copy. The public processor step_over seam
confirms the miss across all three SRAW-bearing programs / 104 boundaries.
Only SRAW's count mask changes; the production core and all inputs stay exact.

The reason is concrete: scope-alu uses count 20, whose low-five and low-six
readings agree. bound-shiftw uses -1: shifting the negative low word by either
31 or 63 produces all sign bits. The third SRAW writes x0. The existing sweeps
exercise immediate SRAIW, so they do not discriminate SRAW's register-count mask.

A literal public-interface witness already distinguishes the rules:

| Input / instruction | Correct five-bit count | Incorrect six-bit count |
| --- | --- | --- |
| x8=0xffffffff80000001, x10=96; SRAW x16,x8,x10 (0x40a4583b) | count 0; x16=0xffffffff80000001 | count 32; x16=0xffffffffffffffff |

The independent author and public core agree on both outcomes. The production
rule is correct; the defect was missing corpus discrimination. c17b's verified
repair below adds the pre-derived boundary witness and corrects the SRLW
counterexample's explanatory arithmetic. G-CONTRACT stays 76/114 until c17d
registers the shift pair after source-width repair and its independent controls.

## Repair: SRAW independently discriminates the count mask

At c17b, both bound-shiftw programs append SRAW x16,x8,x10 at address
0x800000dc, after all 55 original instructions. Its literal word is 0x40a4583b.
The existing x8=0xffffffff80000001 and x10=96 make rs2[4:0]=0: low32 remains
0x80000001, sign-extended to x16=0xffffffff80000001. That expected value was
recorded before either engine ran. The independent author matches every old
observation and the new boundary; all old instruction bytes and positions remain.
The base program now takes 56 word requests; the GC program takes 112 parcels.

The previously surviving six-bit SRAW author fails only at new boundary 55.
The same public processor bad-table diagnostic also fails exactly there: its
all-ones result disagrees with the committed identity. The correct core corpus
passes. A durable hand-encoded author case uses garbage upper bits
0x1234567880000001 and count 96, requiring the same sign-extended low word.
Its isolated sraw-count mutation fails with the named five-bit-count reason
before a new GUEST-GEN control is registered. The ordinary probe now has 23
arithmetic/10 branch cases, 17 corpus gaps / 472 steps and 42 owned records exact.
GUEST-GEN has 143 controls; the registered doctrine total becomes 647.

SRLW step 51 keeps its correct expected value. Its explanation now names a
specific countermodel: widening the count in the present wide evaluator shifts
the low 32-bit logical input by 32 and produces zero. The old explanatory
0xffffffff80000000 was incorrect; no rule is asserted for every possible wrong
implementation. SRAW's arithmetic fill instead makes that erroneous shift all-ones.

The full independent GC corpus matches 167 guests / 5,361 boundaries / 10,516
parcels. Pinned Sail 0.14 agrees on all 56 declared boundary-program rows and
change observations, with two fresh traces byte-identical. This is finite integer
evidence; the standing reference/platform and FP-independence limits still apply.
Only the selected guest data, diagnostic control and their provenance change.
The base dossier digest and dependent board/platform/model-book pins are rederived;
all other generated guest/board semantics and all 78 registry entries stay exact.
The SRAW count-mask coverage and SRLW explanation defects are closed. Contract
credit stays 76/114; nineteen runtime pairs and freeze remain.

<a id="open-evidence-gap-arithmetic-w-source-width"></a>

## Arithmetic-W source width: diagnosis and repair

The adjacent c17b review found a separate missing discriminator. Replacing only
SRAW's or SRAIW's pre-shift 32-bit source truncation with a 64-bit read still
matches the entire 167-guest corpus. Public processor bad tables also match all
105 boundaries of the three affected programs. All 38 arithmetic-W source
occurrences already contain sign-extended 32-bit values; arithmetic right shift
therefore gives the same answer at both widths. The new count-96 witness uses
count zero, so it does not exercise this distinction either.

| Input / instruction | Correct 32-bit source | Incorrect 64-bit source |
| --- | --- | --- |
| x8=0x0000000080000001, x10=1; SRAW x16,x8,x10 (0x40a4583b) | x16=0xffffffffc0000000 | x16=0x0000000040000000 |
| x8=0x0000000080000001; SRAIW x16,x8,1 (0x4014581b) | x16=0xffffffffc0000000 | x16=0x0000000040000000 |

Both public literal experiments confirm these outcomes. The production rules
already truncate correctly. At c17b this corpus evidence defect remained OPEN,
owned priority-next by c17c before shift/word-result registration. Its verified
repair follows.

c17c appends four instructions after the current 56, in both profiles. The
expected words and values were recorded before either engine executed:

| Boundary / address | Instruction / word | Derived write |
| --- | --- | --- |
| 56 / 0x800000e0 | AND x17,x8,x12 / 0x00c478b3 | x17=0x0000000080000001; x12's zero upper word clears x8's sign extension |
| 57 / 0x800000e4 | ADDI x18,x0,1 / 0x00100913 | x18=1 |
| 58 / 0x800000e8 | SRAW x19,x17,x18 / 0x4128d9bb | x19=0xffffffffc0000000 |
| 59 / 0x800000ec | SRAIW x20,x17,1 / 0x4018da1b | x20=0xffffffffc0000000 |

The arithmetic low word is -2147483647. Shifting it right by one rounds down to
-1073741824, whose word is 0xc0000000; sign extension supplies the required
64-bit value. The wrong full-width read instead sees positive 2147483649 and
yields 0x40000000. Each isolated bad author now disagrees only at its new boundary
(58 for SRAW, 59 for SRAIW); public engine bad tables first fail at those same
boundaries. All 56 prior positions, bytes, expectations and observations stay exact.

The durable probe's existing garbage-upper-word hand cases also distinguish both
rules. New sraw-width and sraiw-width controls were observed RED with their named
arithmetic-word reasons before registration. The probe retains 23 arithmetic/10
branch cases and 42 owned records, with 17 corpus gaps / 476 steps. GUEST-GEN
now has 145 controls, and the doctrine total becomes 649.

The correct engine passes the full corpus. The independent author matches all
167 guests / 5,365 boundaries / 10,524 parcels. Pinned Sail agrees on the changed
60-step program's declared rows/change observations and repeats byte-identically;
the base live smoke also compares it against both Sail and Spike. The base budget
is 60 word requests, the GC budget 120 parcels. These source-width evidence defects
are closed; production rules and all 78 registry entries remain unchanged.
G-CONTRACT stays 76/114 with nineteen runtime pairs and freeze remaining. c17d
may now register SHAMT after its independent mask controls. The finite-reference
and platform limits above continue to apply.

## Shift-count domains: all twelve forms

c17d binds CHK-SHAMT-POS to scope-alu and CHK-SHAMT-NEG to bound-shift plus
bound-shiftw: 180 boundaries / 360 parcels. These are legal architectural
instructions. The negative evidence distinguishes wrong count rules through
register observations, without inventing traps for legal shift amounts.

RV64I 3.1.2.1–2 specifies six immediate count bits for SLLI/SRLI/SRAI and the
low six rs2 bits for SLL/SRL/SRA. Word-immediate forms read five count bits;
SLLW/SRLW/SRAW read rs2[4:0]. Twelve independent author copies each change only
one mnemonic's count expression. Every copy is rejected before registry credit:

| Form | Deliberately wrong count | First mismatch |
| --- | --- | --- |
| SLLI | five bits | bound-shift 1 |
| SRLI | five bits | bound-shift 35 |
| SRAI | five bits | bound-shift 73 |
| SLL | low five rs2 bits | bound-shift 87 |
| SRL | low five rs2 bits | bound-shiftw 49 |
| SRA | low five rs2 bits | bound-shift 88 |
| SLLIW | four bits | bound-shiftw 46 |
| SRLIW | four bits | scope-alu 28 |
| SRAIW | four bits | scope-alu 29 |
| SLLW | low six rs2 bits | scope-alu 25 |
| SRLW | low six rs2 bits | bound-shiftw 51 |
| SRAW | low six rs2 bits | bound-shiftw 55 |

For example, SRLI by 32 gives 0x0000000080000000 from
0x8000000000000001; the five-bit copy reads zero and preserves the whole input.
The paired register SRL/SRLW at count 96 deliberately reads 32 versus zero.
SRL gives 0x00000000ffffffff; SRLW preserves the low word and sign-extends it to
0xffffffff80000001. SRAW's separate count-96 witness prevents arithmetic fill
from hiding the mask error: zero count preserves that signed word, while the
six-bit copy produces all ones. The subsequent source-width witnesses remain
exact and continue to distinguish pre-shift truncation independently.

The correct engine and author match all selected observations and the complete
167 / 5,365 / 10,524 corpus. All canonical inputs, guest data, production author,
core, frozen records and prior 78 bindings remain exact. Registry entries become
80; effective G-CONTRACT becomes **78/114**: thirteen scope pairs, nineteen guest
pairs, six boundary pairs and one direct-execution pair. Eighteen runtime pairs
and final freeze remain. This credit is finite evidence for these inputs; the
standing independence/platform limits still apply.

The scoped review also found incomplete requirement metadata: REQ-D-SHAMT's
statement names all twelve forms, while its base and GC insns fields omit
SLLW/SRLW/SRAW. The original base association commit added nine, and GC copied
that list. The aggregate extraction gate still sees the three forms through
WSUFFIX; it does not establish each requirement's association completeness.
The frozen statement and the twelve-form execution evidence above are correct.
At c17d this metadata defect was OPEN and owned priority-next by c17e, before
word-result registration. Implementation-status/experiment work stays .14.

c17e closes it by appending only SLLW/SRLW/SRAW associations in both requirement
catalogs. Every other requirement field, record and frozen obligation remains
exact. Two focused assertions query the canonical catalog owner and require
the complete twelve-form list, independently for the base and GC profiles.
Both were observed RED against the old nine-form catalogs, then GREEN after
the three additions; ordering is immaterial and duplicate associations are refused.
The aggregate extraction and mirror checks also pass with the repaired catalogs.

The change propagates through the base dossier pin into the composed board's
requirement metadata, platform provenance and model/report outputs. It adds no
instruction or observation and changes no runtime behavior. All guest data,
production rules, frozen records and 80 registry entries stay exact; effective
G-CONTRACT remains 78/114. c17f now reviews all nine word-result forms before
binding WSUFFIX. Eighteen runtime pairs and final freeze remain.

## Signed word results: truncation, extension and wrapping

c17f binds WSUFFIX POS to scope-alu plus bound-arith, NEG to bound-shiftw.
Together the fixtures cover all nine RV64I forms named by REQ-D-WSUFFIX:
ADDIW, SLLIW, SRLIW, SRAIW, ADDW, SUBW, SLLW, SRLW and SRAW. The unique
footprint is 122 boundaries / 244 parcels. M's five word forms retain their
separate existing M witnesses. The source-width repairs above are prerequisites
to this registration, and every observation remains unchanged.

The selected rule operates on the low word, retains its low 32-bit result and
sign-extends bit 31 to 64 bits. Overflow is ignored. For example:

| Witness | Required result | What the wrong rule would do |
| --- | --- | --- |
| ADDIW on x10=0xdeadb7ef7fffffff, immediate 1 (bound-arith 17) | x12=0xffffffff80000000 | Zero-extension gives 0x0000000080000000; saturation gives 0x000000007fffffff |
| ADDW on the same low-word overflow (bound-arith 19) | x14=0xffffffff80000000 | Signed saturation clamps to 0x7fffffff |
| SUBW at signed INT32_MIN minus 1620 (scope-alu 24) | x23=0x000000007ffff9ac | Signed saturation instead gives 0xffffffff80000000 |
| SRLIW by zero on low32 0x80000001 (bound-shiftw 34) | x20=0xffffffff80000001 | Word result still needs sign extension, even for a logical shift by zero |
| SRAW/SRAIW on zero-extended 0x80000001 by one (bound-shiftw 58/59) | 0xffffffffc0000000 | A full-width source read gives 0x40000000 |

Sixteen isolated author copies fail named observations before credit. Nine
copies zero-extend only one named word result; four read the full 64-bit source
before right shift; three saturate only the named signed 32-bit add/subtract.
Shared result finishes keep every other mnemonic's expression unchanged.

| Deliberately wrong rule | First mismatch |
| --- | --- |
| ADDIW zero result extension | bound-arith 17 |
| SLLIW zero result extension | bound-shiftw 41 |
| SRLIW zero result extension | bound-shiftw 34 |
| SRAIW zero result extension | scope-alu 29 |
| ADDW zero result extension | scope-alu 23 |
| SUBW zero result extension | bound-arith 20 |
| SLLW zero result extension | bound-shiftw 53 |
| SRLW zero result extension | bound-shiftw 51 |
| SRAW zero result extension | scope-alu 27 |
| SRLIW full-width source | scope-alu 28 |
| SRAIW full-width source | bound-shiftw 59 |
| SRLW full-width source | scope-alu 26 |
| SRAW full-width source | bound-shiftw 58 |
| ADDIW signed saturation | bound-arith 17 |
| ADDW signed saturation | bound-arith 19 |
| SUBW signed saturation | scope-alu 24 |

The right-shift source width matters because upper bits can enter the retained
word or change arithmetic fill. For addition/subtraction and left shift, reading
upper bits before an otherwise correct final low32 truncation is observationally
equivalent: those operations' low 32 result bits depend only on the low input
bits. Such equivalent rewrites are not classified as faulty countermodels.

The normal author/core matches all selected observations and the full
167 / 5,365 / 10,524 corpus. Canonical inputs, generated data, production rules,
frozen records and all prior 80 bindings remain exact. Registry entries become
82; effective G-CONTRACT becomes **80/114**: thirteen scope, twenty guest, six
boundary and one direct-execution pairs. Seventeen runtime pairs and freeze
remain. Negative fixtures are legal semantic counterexamples, with no invented
target traps. Standing finite-evidence/reference/platform limits remain.

## Load extension follows the read width; stores keep the low source bits

At c18b, CHK-LOAD-EXT-POS runs scope-mem (29 boundaries/58 parcels), and NEG
runs bound-ext (47/94) plus dir-ext-matrix (35/70). Together their 111/222
observations exercise LB/LH/LW, LBU/LHU/LWU, LD and SB/SH/SW/SD. RV64I 3.1.3
requires sign extension for the first three loads, zero extension for their
unsigned counterparts, and a full 64-bit LD result. Each store writes only the
low 8/16/32/64 bits of rs2. The authenticated local snapshot matches the source
ledger's exact RV64I/RV32I hashes; RV32I 1.1.6 supplies the inherited rules.

The read width determines the sign bit, independently of the earlier store's
width. For example, storing the byte 0x80 into an explicitly zeroed eight-byte
cell gives LB=0xffffffffffffff80, but LH/LW/LD=0x80. Storing 0x8000 gives
LB at byte offset 1 the negative byte result, LH=0xffffffffffff8000 and
LW/LD=0x8000. The matrix repeats this reasoning through the high halfword of
0x80000000 and high word of 0x8000000000000000. All accesses are naturally
aligned, and the cell is explicitly cleared between widths.

Selected zero-based bound-ext steps pin both sides of each sign edge:

| Width | Positive signed load | Negative signed load | Unsigned load of the same sign edge |
| --- | --- | --- | --- |
| 8 | step 23: 0x7f | step 24: 0xffffffffffffff80 | step 25: 0x80 |
| 16 | step 28: 0x7fff | step 29: 0xffffffffffff8000 | step 30: 0x8000 |
| 32 | step 33: 0x7fffffff | step 34: 0xffffffff80000000 | step 35: 0x80000000 |

Each width also reads all ones through signed/unsigned forms. At steps 39/40,
a pre-write of -1 makes the subsequent zero-byte LB observable. Store truncation
is checked by wider read-back: scope-mem's narrow stores of -1 yield LD results
0xff, 0xffff and 0xffffffff at steps 22/24/26, leaving the higher lanes zero.
Its SW of 0x80fff7f080fff7f0 yields LD=0x80fff7f0 at step 28, while the full
SD/LD pair preserves 0x80fff7f080fff7f0 at step 18. Non-clamping inputs
in bound-ext distinguish truncation from saturation: SB of 0x180 yields 0x80;
SH/SW of 0xffffffffffff8000 yield 0x8000/0xffff8000.

Seventeen isolated spec-side copies are deliberately wrong; each fails a named
committed observation before registry credit:

| Wrong rule | First discriminating observation |
| --- | --- |
| Zero extension for LB/LH/LW | scope-mem steps 12/14/16 |
| Sign extension for LBU/LHU/LWU | scope-mem steps 13/15/17 |
| LD truncated to low 32 bits | scope-mem step 18 |
| SB/SH/SW choose high source bits | bound-ext steps 23/28/33 |
| SB/SH/SW write eight bytes | scope-mem LD steps 22/24/26 |
| SB/SH/SW saturate instead of truncating | bound-ext steps 42/44; scope-mem step 28 |
| SD truncated to low 32 source bits | scope-mem LWU step 17 |

The declaration test first fails with CHK-LOAD-EXT-POS missing, then passes when
both exact bindings are registered. Normal independent replay matches the entire
167-program corpus, 5,365 boundaries/10,524 parcels. All earlier 82 bindings,
canonical and guest inputs, generated data, production rules/author and frozen
records remain exact. Registry entries become 84, effective G-CONTRACT **82/114**:
thirteen scope, twenty-one guest, six boundary and one direct-execution pairs.
Sixteen runtime pairs and freeze remain. These finite, legal counterexamples do
not require target traps and do not establish untested memory-system behavior.
Address faults, x0 side effects and the selected endian policy retain their own
contract obligations.

Source review also exposed a separate evidence-reader defect: the fetched HTML
copies differed only in Antora metadata, while the readers accepted mismatched
pins. The authenticated snapshot was used here. c18c repairs both readers with
shared exact-hash/length refusal and restores only the three fetched pages from
the verified snapshot; all pins and architecture text stay unchanged.


## Loads into x0 still execute (P4.13 c19)

RV32I 1.1.6 requires a load whose destination is x0 to raise exceptions and
cause other side effects even though its value is discarded. OB-LOAD-X0 now
uses direct execution witnesses for every associated form, with the older guests
as companions. The instructions are literal encodings of LB/LH/LW/LBU/LHU/LWU/LD
x0,0(x5), executed through the public table interface. An environment wrapper logs
actual requests; it implements no instruction semantics.

| Case | Forms | Required data boundary | Architectural result |
| --- | --- | --- | --- |
| Aligned success at 0x1080 | all seven | exactly one Load with the form's width/address | PC 0x1004; one retired instruction |
| Environment access refusal at 0x1080 | all seven | exactly one Load, answered AccessFault | cause 5, EPC 0x1000, tval 0x1080, PC 0x1100; no retirement |
| Misaligned address 0x1081 | LH/LW/LHU/LWU/LD | no data request | cause 4, EPC 0x1000, tval 0x1081, PC 0x1100; no retirement |
| Sv39 invalid root PTE | all seven | exactly one implicit WalkAccess at 0x2000; no Load | cause 13, EPC 0x1000, tval 0x1080, PC 0x1100; no retirement |

Every case also requires two fetch parcels, one cycle boundary, unchanged GPRs
(including x0 and a nonzero sentinel in each other register), unchanged memory
and M mode after the step. The page-fault case uses MPRV/MPP=S for the data access;
the instruction fetch remains bare M mode. These are 26 direct boundaries / 52
parcels. Companion scope-mem and dir-x0-writes contribute 47/94; the two
fault-ld-x0 guests contribute 5/10, giving 78/156 in total.

The companions alone cannot establish this guarantee. Investigation found that
the GC corpus comparison checks register changes, never-written registers and
fetch counts, but not the final trap state or data requests. An isolated author
that skips loads only when rd=0 still matches all 167 programs, 5,365 boundaries
and 10,524 parcels. A separate client reproduces this through the public CPU
interface with a conditional bad table. Both fault guests still satisfy their
old observations, although their architectural outcomes differ:

| Guest | Correct final state | Incorrect skipped-load state |
| --- | --- | --- |
| fault-ld-x0-fault | cause 5, EPC 0x80000004, tval 0x40000000, PC 0, retired 1; one Load | cause/EPC/tval 0, PC 0x80000008, retired 2; no Load |
| fault-ld-x0-mis | cause 4, EPC 0x80000008, tval 0x80000402, PC 0, retired 2; no Load | cause/EPC/tval 0, PC 0x8000000c, retired 3; no Load |

This is a missing observation in the old GC witness, not a processor defect.
The inherited base-profile tests separately inspect load crossings and faults;
the GC mirror's shared comparison did not inherit those assertions. The new
negative witness explicitly checks all three fault cases for each applicable
form. Erasing any form fails; duplicating any form fails the success request log.
Disabling the request comparison first makes the erased-load control fail its
own expected-refusal assertion. Disabling access-fault injection is also rejected.
The declaration test first fails on the missing LOAD-X0 binding before either
execution entry is registered.

Normal Rust checks pass 167 core / 17 DSP / 206 verify tests. Independent normal
replay and all prior 84 bindings, 112 base / 348 GC canonical and guest inputs,
production rules, author, generated data and frozen records remain exact.
Registry entries become 86; effective G-CONTRACT is **84/114**: thirteen scope,
twenty-one guest, six boundary and two direct-execution pairs. Fifteen runtime
pairs and final freeze remain. Request logs prove the access occurs; they do not
add a device or claim unimplemented MMIO behavior. Byte-order selection and other
remaining obligations retain their own witnesses.


## Selected little-endian byte order (P4.13 c20)

OB-ENDIAN records an EEI choice. RV32I 1.1.6 permits either byte order and
requires byte-address invariance; this profile selects little-endian. The pinned
107,630-byte chapter was authenticated before review. CHK-ENDIAN-POS now runs
scope-mem and NEG runs dir-ext-matrix: 64 boundaries / 128 parcels covering all
seven integer loads and four stores. NEG means a wrong order produces different
legal observations, not that a big-endian RISC-V system must trap.

The matrix stores one sign bit and reads different widths and byte addresses:

| Stored value/width | Bytes at increasing addresses | Selected observations (zero-based steps) |
| --- | --- | --- |
| 0x80 / SB | 80 00 00 00 00 00 00 00 | LB=-128 at 5; LBU=0x80 at 6; LH=0x80 at 7; LD=0x80 at 9 |
| 0x8000 / SH | 00 80 00 00 00 00 00 00 | LB at offset 0 is 0 at 13; LB at offset 1 is -128 at 14; LHU=0x8000 at 15 |
| 0x80000000 / SW | 00 00 00 80 00 00 00 00 | LB at offset 3 is -128 at 22; LH at offset 2 is -32768 at 23; LWU=0x80000000 at 24 |
| 0x8000000000000000 / SD | 00 00 00 00 00 00 00 80 | high-byte/halfword reads retain their prior values at 30/31; high LW=-2147483648 at 32; LD=0x8000000000000000 at 33 |

Nine isolated author copies reverse each LH/LHU/LW/LWU/LD read, each SH/SW/SD
write, or both directions together. The NEG matrix rejects all nine, first at
steps 7/15/8/24/9, 13/22/30, and 7 respectively. Reversing SH alone survives
scope-mem because its halfword store is all ones; the cross-width matrix removes
that symmetry. SW reversal is caught later in scope-mem at step 28. A matching
store/load reversal cannot hide behind a same-width round trip here.

A separate public-interface client reverses H/W/D provider reads, writes and
both together: all nine variants fail the NEG observations. Byte reversal changes
neither selected guest, and all 256 byte values retain their exact address/value
through the public provider interface. Existing direct data-access witnesses also
pin literal B/H/W/D values, low-width stores, neighboring bytes and a typed
refusal for a reversed valid-width response. The normal CPU trusts conforming
provider content; the independent fixture auditor detects incorrect content.

The declaration check first fails on the missing ENDIAN binding, then passes.
Normal Rust checks and independent full 167/5365/10524 replay pass. All prior 86
bindings and canonical/guest/core/author/generated/frozen data remain exact.
At c20, registry entries reach 88, effective G-CONTRACT **86/114**: thirteen scope,
twenty-two guest, six boundary and two direct-execution pairs. Fourteen runtime
pairs/freeze remain. This is evidence for the selected ordinary-memory byte
order; it does not add selectable big-endian execution or a device model.
