# P4.13 — Integer runtime contract witnesses

[Contract completion](contract-v2.md) tracks effective counts;
[system runtime witnesses](contract-runtime.md) retain privilege, translation and timers.
[memory runtime witnesses](contract-memory.md) cover extension, x0 loads and byte order.
[control transfer witnesses](contract-control.md) cover branches, jumps and direct JALR targets.

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
control also refuses.

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
valid register arithmetic.

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
recorded before either engine ran.

The previously surviving six-bit SRAW author fails only at new boundary 55.
The same public processor bad-table diagnostic also fails exactly there: its
all-ones result disagrees with the committed identity. The correct core corpus
passes. A durable hand-encoded author case uses garbage upper bits
0x1234567880000001 and count 96, requiring the same sign-extended low word.
Its isolated sraw-count mutation fails with the named five-bit-count reason
before a new GUEST-GEN control is registered.

SRLW step 51 keeps its correct expected value. Its explanation now names a
specific countermodel: widening the count in the present wide evaluator shifts
the low 32-bit logical input by 32 and produces zero. The old explanatory
0xffffffff80000000 was incorrect; no rule is asserted for every possible wrong
implementation. SRAW's arithmetic fill instead makes that erroneous shift all-ones.

The count-mask diagnostic also matched 56 declared Sail boundary rows with
two identical fresh traces. This is finite integer evidence, subject to the
reference/platform and FP-independence limits. Its provenance propagation and
dated corpus/contract counts are retained in the receipts below.

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
boundaries.

The durable probe's existing garbage-upper-word hand cases also distinguish both
rules. New sraw-width and sraiw-width controls were observed RED with their named
arithmetic-word reasons before registration.

The completed source-width program has 60 boundaries: 60 base word requests
or120 GC parcels. Pinned Sail matches its declared rows/change observations
and repeats identically; the base live smoke compares both Sail and Spike.
These finite observations close the source-width evidence gaps without
changing production rules; the standing reference/platform limits apply.

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

The selected observations and complete independent corpus agree. This is
finite evidence for these inputs; standing independence/platform limits apply.
Dated registry/corpus and pre-bind identity receipts remain below.

The scoped review also found incomplete requirement metadata: REQ-D-SHAMT's
statement names all twelve forms, while its base and GC insns fields omit
SLLW/SRLW/SRAW. The original base association commit added nine, and GC copied
that list. The aggregate extraction gate still sees the three forms through
WSUFFIX; it does not establish each requirement's association completeness.
The frozen statement and the twelve-form execution evidence above are correct.
The association repair below closes that metadata defect; implementation-status
and experiment work remains P4-SYSTEM.14.

c17e closes it by appending only SLLW/SRLW/SRAW associations in both requirement
catalogs. Every other requirement field, record and frozen obligation remains
exact. Two focused assertions query the canonical catalog owner and require
the complete twelve-form list, independently for the base and GC profiles.
Both were observed RED against the old nine-form catalogs, then GREEN after
the three additions; ordering is immaterial and duplicate associations are refused.
The aggregate extraction and mirror checks also pass with the repaired catalogs.

Requirement associations propagate through the base dossier pin into board
metadata, platform provenance and generated model/report outputs. This changes
metadata, not instruction behavior or observations; its exact propagation
receipt is preserved below.

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

Normal author/core observations agree. Negative fixtures are legal semantic
counterexamples, with no invented target traps. Standing finite-evidence,
reference and platform limits remain; dated progress receipts are below.

## XLEN: retain 64-bit registers and user addresses (c23b)

RV64I 3.1.1 widens the integer file and supported user address space to 64 bits.
Sv39 still requires bits 63–39 to equal bit 38. A 64-bit address representation
does not make every value canonical or mapped. The direct XLEN pair exercises
both canonical halves in U mode with Sv39 active, using ordinary laboratory RAM.

| Direct case | Virtual entry | Physical root PTE address | Data payload |
| --- | --- | --- | --- |
| POS, above 32 bits | 0x0000000100001000 | 0x80002020 | 0x0123456789abcdef |
| NEG, upper canonical half | 0xffffffff80001000 | 0x80002ff0 | 0xfedcba9876543210 |

Each fresh root at 0x80002000 contains exactly one valid 1 GiB user leaf:
PTE=0x200000df, with R/W/X/U/A/D set. The rest are zero. Both entries map their
program to PA=0x80001000; virtual data at entry+0x80 maps to PA=0x80001080.
The provider contains 16 KiB of executable little-endian RAM at 0x80000000.
No physical map or MMU width is added to the production profile.

Every writable GPR starts with an independently expected high-bit sentinel,
0x0123456700000000 plus its register number; x6 is replaced with the full virtual
data pointer. An attempted all-ones write to x0 must leave zero. Expected values
are established before these writes, so a narrow register file cannot supply
its own expectations through read-back. Four literal instruction words follow:

| Word | Instruction | Required observation |
| --- | --- | --- |
| 0x00030393 | ADDI x7,x6,0 | x7 retains the complete virtual pointer |
| 0x00033403 | LD x8,0(x6) | x8 receives all 64 payload bits |
| 0x00833423 | SD x8,8(x6) | Eight bytes at PA=0x80001088 receive the complete payload |
| 0x00000497 | AUIPC x9,0 | x9 receives the current virtual PC, entry+12 |

For example, the upper-half case produces x7=0xffffffff80001080,
x8=0xfedcba9876543210 and x9=0xffffffff8000100c. After every boundary the
observer checks all GPRs, exact virtual PC, U mode/UXL=64, trap state, cycle and
retirement, every physical request and the whole memory image. The only memory
change is the declared eight-byte store. Each case issues one cold WalkAccess,
eight FetchParcel requests, one D load and one D store: four boundaries/eight
parcels/eleven total requests. A/D were already set, so no PTE writes occur.
The two direct cases total **8 boundaries / 16 parcels / 22 requests**.

Seven isolated public table effects truncate one item to 32 bits: ADDI result,
LD address, SD address, LD value, SD value, AUIPC result or next PC. All fourteen
case/control combinations fail a named request or state observation. Truncated
virtual data addresses reach an invalid root entry; truncated values lose the
payload's upper half. Disabling the GPR audit lets the otherwise unused x7
truncation escape and makes the control test fail; restoring it passes.

The independent author confirms the literal words, canonical mappings, GPR/PC/U/
counter/memory values and fetch/walk logs. It does not log data boundary requests;
the public CPU observer separately checks those. The declaration test first
refused the missing binding. Unchanged companion guests are POS scope-alu
(31/62) and NEG bound-arith/sv39-fault-canonical (89/178). Including the direct
cases, the pair runs **128 boundaries / 256 parcels**. This is finite width evidence under the selected
translation and provider rules.



## Historical verification receipts

Further exact chronology and pre-bind identity receipts are preserved in
`docs/tasks/archive/P4-SYSTEM-book-c30b.md`, section `contract-integer`.
Current feature explanations, examples, controls and limits remain here.
