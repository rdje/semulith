# P4.13 — Memory runtime contract witnesses

[Contract completion](contract-v2.md) tracks effective counts;
[integer runtime witnesses](contract-integer.md) retain arithmetic and shifts;
[system runtime witnesses](contract-runtime.md) cover privilege, translation and timers.

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

## FENCE accepts future fields and preserves one-hart state

OB-FENCE binds a direct CPU Execution pair at P4.13 c25. RVI-RV32I 1.1.7
requires base implementations to treat reserved fence configurations as ordinary
FENCE and to ignore rs1/rd. FENCE.TSO has fm=8, pred=RW and succ=RW; implementing
it as the stronger FENCE RW,RW is permitted. With this laboratory's one hart,
no external devices and synchronous instruction execution, all these forms
retire without an observable fence effect. Ordinary counter/PC advance still
occurs. The NEG check exercises adversarial accepted encodings; it does not
invent an illegal-instruction expectation for reserved fence fields.

The field matrix crosses all 4,096 fm/pred/succ configurations with M, S and U
and five rs1/rd pairs: 0/0, 0/31, 31/0, 31/31 and 7/13. That is 61,440 actual
CPU boundaries, each fetching exactly two 16-bit parcels. The word is packed as
config<<20 | rs1<<15 | rd<<7 | 0x0f and independently checked by the assembler.
These are all twelve-bit fence configurations with representative register
pairs, rather than all 32×32 register combinations.

POS selects the 256 fm=0 configurations and exact FENCE.TSO with rs1=rd=0,
in all three modes: 771 boundaries. NEG runs the remaining 60,669 cases.
Every case compares all 32 integer registers, all 32 floating-point registers,
26 CSR owners, PC, mode and the complete memory image. CSR expectations begin
from seeded state before CPU execution; only mcycle/minstret advance. High-bit
GPR and FPR sentinels, scratch/trap CSR values, fflags=0x15, frm=3 and FS=Dirty
make unwanted writes visible. Counters start at 41/17 and must become 42/18;
PC advances from 0x1000 to 0x1004. The only boundary requests are parcels at
0x1000 and 0x1002; no explicit memory request is added by FENCE.

Three literal forms also run inside each integration sequence:

| Form | Word | Meaning |
| --- | --- | --- |
| Ordinary | 0x0ff0000f | fm=0, pred=succ=15, rs1=rd=0 |
| TSO | 0x8330000f | fm=8, pred=succ=RW, rs1=rd=0 |
| Reserved/ignored fields | 0xffff8f8f | fm=pred=succ=15, rs1=rd=31 |

LR.D x7,(x6); FENCE; SC.D x8,x9,(x6); LD x10,0(x6) executes in M with
x6=0x1080. LR reads 0x1122334455667788. FENCE must preserve its reservation;
SC writes 0x8877665544332211 and reports x8=0; LD reads that value into x10.
Each four-boundary program has eight parcels and exactly three data requests
(Load, Store, Load). All state and bytes are checked after each boundary,
including unchanged memory immediately after the fence.

ADDI x7,0,1; FENCE; ADDI x8,0,2 executes in S at VA 0x1000. Satp
0x8000000000080002 selects root PA 0x80002000, whose PTE 0x200000cf maps a
1 GiB S leaf to PA 0x80001000. The first ADDI performs one WalkAccess and two
parcels. FENCE and the next ADDI reuse that same-page mapping without another
walk. Each three-boundary program has six parcels and seven requests. This
observes translation preservation through subsequent execution rather than
reading hidden cache fields.

The direct pair totals 61,461 boundaries, 122,922 parcels and 122,934 requests.
Unchanged scope-alu (31/62) and fault-fence (8/16) companions bring the pair to
61,500 boundaries/123,000 parcels. The old fault-fence program already cites
the correct reserved-field rule. The independent author's stock FENCE locator
had instead pointed at 1.1.6, Load and Store Instructions, since its promotion
in commit 022f557. The one-line correction now points at 1.1.7, Memory Ordering
Instructions; no canonical guest text, value, word or generated fixture changes.

Ten isolated instruction-table controls reject restrictive fm/register masks,
GPR/FPR/CSR writes, a Store, trap delivery, a skipped PC, consumption of the
reservation and translation-cache invalidation. Restrictive masks return
ReservedDecode and do not retire, so the counter expectation detects them.
The reservation consumer fails when the later SC omits its required Store;
the cache invalidator fails when the final ADDI issues an extra WalkAccess.
Disabling the actual GPR predicate makes the bad-write control fail, confirming
that the observation is needed. The production table/core are unchanged.

Independent specification-side replay verifies every matrix word and complete
state/memory result, plus all six integration programs and their fetch/walk
logs. Its log omits the nine LR/SC/LD data requests, which the direct CPU
observer checks separately. These checks establish the selected one-hart
behavior and field treatment. They do not exercise multiple-hart ordering,
external devices, all register-pair combinations or every atomic/cache policy.

## Atomic misalignment wins before data translation

OB-ATOMIC-MISALIGN now binds a direct Execution pair at P4.13 c27. RVI-A
12.1.2/12.1.4 offer address-misaligned or access-fault exceptions. This frozen
laboratory contract selects access fault before translation. RVP-MACHINE's
exception table assigns LR to the load family: cause **5**. SC and all nine
AMOs use the store/AMO family: cause **7**. This is the selected profile choice;
it does not make every other permitted implementation choose the same cause.

The aligned control runs 48 LR/SC programs: W/D × four aq/rl combinations ×
M/S/U × destination x0/x7. Both instructions use the selected destination.
All 96 boundaries compare the full register files, 26 CSR owners, PC, mode,
complete memory, exact reservation state and request sequence. A prior valid
reservation at a different address is replaced by LR, then cleared by SC.

For x6=0x1080 and x9=0x8877665544332211, the initial eight data bytes encode
0x1122334480000001. Representative programs have these results:

| Program, with ordering bits clear | LR destination | SC destination | Final eight-byte cell |
| --- | --- | --- | --- |
| LR.W x7,(x6); SC.W x7,x9,(x6) | 0xffffffff80000001 | 0 | 0x1122334444332211 |
| LR.D x7,(x6); SC.D x7,x9,(x6) | 0x1122334480000001 | 0 | 0x8877665544332211 |
| Same pairs with rd=x0 | x0 remains zero | x0 remains zero | same stored bytes |

The W instructions sign-extend the loaded word and store only the low four
bytes, preserving neighboring bytes. The declared SC.W semantic expression
truncates rs2 before issuing its Store: the observer expects data=0x44332211,
while SC.D supplies the complete 64-bit value. Every successful program requests
two parcels then a Load, followed by two parcels then a Store. Counters advance
41/17 → 42/18 → 43/19 and PC advances 0x1000 → 0x1004 → 0x1008.

The negative matrix executes **8,800** one-boundary cases. It crosses all 22
legal atomic forms with four aq/rl settings, each nonzero offset below the
access width (1–3 for W, 1–7 for D), destinations x0/x7, invalid/valid prior
reservations and five contexts:

| Context | Why alignment must still decide first |
| --- | --- |
| Bare M, S and U | Natural alignment is required in each mode |
| M fetch, MPRV-S data, Sv39 with a zero root PTE | A translation attempt would read the root and raise a page fault |
| Same MPRV-S setup with noncanonical data VA 0x4000001080+offset | A canonicality check would otherwise raise a page fault |

The translated contexts use satp=0x8000000000000002, root PA=0x2000. Instruction
fetch remains physical in M. Each misaligned instruction must request exactly
FetchParcel(0x1000) and FetchParcel(0x1002), with no WalkAccess, Load or Store.
The trap records the original instruction PC and full data VA. It retires
nothing, advances mcycle once and preserves all GPRs, FPRs, memory and the exact
prior reservation. A misaligned SC traps even when no reservation could succeed;
it must not quietly return the ordinary failed-SC code 1.

For example, LR.D x7,(x6), word 0x100333af, with x6=0x1081 in the invalid-root
context delivers mcause=5, mepc=0x1000 and mtval=0x1081 to M at PC 0x1100.
Mstatus changes from 0xa00026808 to 0xa00027880: MIE is saved in MPIE and MPP
records the originating M mode. Mcycle/minstret become 42/17. The root PTE and
all other memory stay unchanged. A zero destination still takes that trap.
SC.D at the same address instead delivers cause 7, preserving the reservation.

The direct pair totals 8,896 boundaries, 17,792 parcels and 17,888 requests.
Unchanged companions a-lrsc-pair (14/28), a-lrsc-illegal (33/66) and a-amo-overlap
(16/32) bring the pair to 8,959 boundaries/17,918 parcels. The illegal-encoding
companion covers decode refusals; the direct matrix contains legal atomic words
with misaligned addresses. These are separate claims.

Seven wrong public instruction effects fail cause, trap-value, GPR, CSR,
extra-Load and reservation observations. Thirteen corrupted captures exercise
every auditor family, including unexpected Walk/Load/Store requests, memory,
FPR, PC/mode and parcel/outcome changes. Disabling the actual request predicate
makes the extra-Load control fail: its remaining architectural state matches.
Changing the actual LR cause to 4 fails the CSR comparison. Bypassing its
alignment guard issues a root WalkAccess at 0x2000 and fails the request comparison.
All temporary mutations are restored exactly; production semantics stay unchanged.

Independent specification-side derivation checks all 176 matrix words against
the assembler and verifies the listed state/memory results and fetch/walk logs.
Its log omits explicit data requests and models a cleared reservation as absent,
without retained invalid fields. The direct CPU observer owns those stronger
observations. This finite evidence establishes the selected alignment policy;
it does not close the separate atomic arithmetic, reservation-policy or
multicore obligations. Those retain their own checks.

## Matching the reference's atomicity granule

The c27 source review exposed a configuration mismatch that the original A
experiment could not distinguish. RVI-A 12.1.4 permits an optional misaligned-
atomicity granule. An AMO contained within that granule need not fault. The Sail
override carried scalar granule exponent 4 (16 bytes) alongside amo=AccessFault,
introduced at 859e5cc's privileged match. The old a-lrsc-fault AMO uses address
0x800000fe: its four-byte access crosses a 16-byte boundary and therefore traps
under either configuration. Agreement on that address did not establish the
unconditional alignment rule.

A new literal program initializes its data bytes and seeds x5=17, then executes
AMOADD.W x5,x6,(x2) with x2=0x80000101 and x6=42. Its following instructions read
mcause, mtval and the two aligned doublewords containing the data. Those
instructions are also the trap handler, so both outcomes reach the same read-backs.
Expectations are derived before the reference runs.

| Observation | Laboratory and corrected override | Former 16-byte granule |
| --- | --- | --- |
| AMO destination x5 | stays 17 | becomes 0, the old memory value |
| mcause / mtval | 7 / 0x80000101 | 0 / 0 |
| Aligned data read-back at 0x80000100 | 0 | 0x2a00 |

Two fresh traces reproduce the wrong completion exactly. Validated public
configuration copies isolate the setting: exponent 0 restores the fault;
exponents 3 and 4 permit this contained word AMO. The public schema allows
integer exponents 0–12, and the public ISA string is identical before/after.
The tracked override now changes exactly the scalar exponent 4→0. The vector
parameter, instruction selection and frozen laboratory obligations stay unchanged.
This repairs a local matching configuration; Sail correctly implemented its
previously supplied granule.

Run the durable public qualification with the acquired pinned binary:

```bash
python3 scripts/probe_gc_sail_atomic_align.py
```

It checks 242 cases over all 22 atomic forms, W/D, ordering bits clear and bare
M mode. Each width has one aligned address, every contained misaligned offset,
and every misaligned offset crossing the next 16-byte boundary: seven W cells
and fifteen D cells per operation. Each 13-boundary program verifies literal
instruction PCs/words, declared GPR changes and CSR/data read-backs. There are
3,146 boundaries per repetition, with two fresh byte-identical traces per case.
A validated copy restoring the 16-byte granule must reproduce the specific
AMOADD.W completion and diverge at boundary 8. Missing, failed, incomplete or
non-repeating traces refuse. Outputs stay below the repository's target directory.
This live diagnostic requires the reference binary; it is not an offline CI
member and adds no registered doctrine or CPU-contract credit.

All original twelve A guests were re-run: eleven agree over 290 declared
boundaries with repeated traces; a-lrsc-mustfail retains the permitted width-SC
policy difference at step 22. The broader before/after run captures instruction,
GPR/FPR/CSR, memory, walk/cache and exception/interrupt traces. All 164 successful
old-guest traces are byte-identical across configurations and repetitions. Three
old runs retain the same process failures: mm-counters, w-notrap and w-timer
reach a trap loop without the matched counter/timer source. They are explicit
limits and earn no successful-trace credit. These observations are reference
configuration regression evidence, not agreement of every guest with the CPU.

The broad run also found a separate adapter defect: its two extra steps can run
off a completed program and produce repeated fetch faults. It then refuses the
entire trace for duplicate delivery, even when the declared prefix is complete.
The public dir-chase adapter refuses at step 17; the same binary/configuration/
ELF with its exact 17-step budget agrees. P4.13 c28c owns the bounded repair and
its missing-evidence/parcel-gap controls before the next runtime binding.
Structured experiment records and requirement statuses remain P4.14's work.
