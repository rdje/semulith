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
