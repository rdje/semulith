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
