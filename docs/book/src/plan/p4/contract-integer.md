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
rule is correct; the defect is missing corpus discrimination. Priority-next c17b
will add this pre-derived boundary witness to both mirrored profiles, preserve
every old observation, and repair the SRLW counterexample's explanatory arithmetic.
Then c17c may register the shift pair after independent controls. Until that
repair is verified, the defect remains open and G-CONTRACT stays 76/114.
