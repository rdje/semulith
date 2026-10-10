# P4.4 — Atomics and reservations

**Status:** Landed and closed (slices a–f, 2026-10-05)

The current A definition composes Zaamo and Zalrsc: nine AMOs plus LR/SC,
each at W and D widths, for 22 forms. The AMOs are ADD, SWAP, XOR, AND, OR,
signed MIN/MAX and unsigned MIN/MAX. Canonical encoding and semantic fragments
own their fields and effects; generated Rust executes those definitions. The
assembler accepts `.aq`, `.rl` and `.aqrl` suffixes and `(rs1)` addresses. All
four ordering encodings are exercised; at one hart they add no observable
cross-hart ordering outcome.

For an aligned mapped address in x6, memory word `0x80000005` and x9 = 42:

```asm
lr.w x5, (x6)
sc.w.aqrl x7, x9, (x6)
lw x8, x6, 0
```

LR returns `0xffffffff80000005`; the matching SC stores 42, returns x7 = 0,
and clears the reservation. Read-back gives x8 = 42. W operations use low 32 bits
and sign-extend returned old words; D retains all 64 bits. Register aliases must
use the original address/source, and x0 discards only its destination result.

The selected reservation is hart state `(physical address, width, valid)`.
A completed LR replaces it. A completed SC clears it on success or failure,
even at another address; traps preserve it. After alignment and permission checks, SC succeeds when valid,
physical address and width all match; otherwise it returns 1 without storing.
This laboratory chooses no spurious failure and exact-width matching. These
are declared profile policies within the architecture's permitted latitude;
public reference agreement does not make them universal ISA requirements.
Ordinary instructions do not provide external invalidation events here.

AMOs translate once with store/AMO permissions, then issue consecutive Load
and Store requests at the same physical address. The returned value precedes
the update. A failed SC may already have issued translation reads before its
reservation match; failure suppresses its data Store. A nonmatching SC still
issues a side-effect-free physical StorePermission check before retiring. Under the selected
misalignment policy, LR takes access-fault cause 5, SC/AMO cause 7, before
translation. A translated AMO page fault is cause 15 rather than load cause 13.
Precise traps preserve the old reservation and suppress destination writes.

The original twelve A guests cover successful pairs, no-LR/address/width/
replacement/intervening-SC failures, aliases, aq/rl combinations, translated
faults and a constrained loop. Fresh public Sail observations retain eleven
agreements and the named mixed-width SC divergence; the public-evidence section
below gives repeats and a wrong-expectation control. Independent literal
expectations and direct full-state/request observations remain separate evidence
legs. This one-hart, side-effect-free-memory environment establishes no
multicore indivisibility, device behavior or complete weak-memory exploration.

## Direct contract observations

P4.13 c29 binds OB-GC-ATOMICS to direct CPU execution and seven unchanged A
companions. The independent values come from the authenticated pinned RVI-A
12.1.2/12.1.4 page (56,889 bytes; SHA-256
`afbd8def7bdf64287ef51a9cb14dd654fba0f0cfeef63bccdfd47408f5b0dff2`)
and supervisor translation chapter (186,455 bytes; SHA-256
`d5186efc3ead1c1f693ac2b16aeccdcab95d990264f49b559252d2dc413a651a`).
The nine operations are ADD, SWAP, XOR, AND, OR, signed MIN/MAX and unsigned
MIN/MAX. Literal result tables are derived before CPU execution and checked
against the independent author, rather than copied from processor output.

Ten data pairs include zero, all ones, addition overflow, both signed endpoints,
complementary bit patterns, and two address/zero source controls. Each crosses
22 forms, W/D, four aq/rl combinations, M/S/U and rd=x0/x6/x7/x9, giving
10,560 successful boundaries. x6 is the address register and x9 the ordinary
source. Thus rd=rs1 and rd=rs2 cannot accidentally replace the original address
or source used by the instruction. The two extra source controls use rs2=rs1
and rs2=x0 for AMO/SC; LR always retains its required rs2=0 encoding. The
assembler independently verifies 992 distinct words, including every ordering
suffix. This is a finite matrix, not every register/value combination.

For example, at address 0x1080 let the original doubleword be
`0x1122334480000001` and rs2 be `0x8877665544332211`:

| Instruction | rd receives | Stored low-width value |
| --- | --- | --- |
| AMOADD.W | `0xffffffff80000001` | `0xc4332212` |
| AMOSWAP.W | `0xffffffff80000001` | `0x44332211` |
| AMOMIN.W | `0xffffffff80000001` | `0x80000001` |
| AMOMAX.W | `0xffffffff80000001` | `0x44332211` |
| AMOMINU.W | `0xffffffff80000001` | `0x44332211` |
| AMOMAXU.W | `0xffffffff80000001` | `0x80000001` |

All word operations leave the four adjacent upper bytes `44 33 22 11` intact.
AMOs return the original value even when rd aliases a source; rd=x0 suppresses
only the register write. The observed boundary is exactly two instruction
parcels, then Load followed by Store of the declared width at the same physical
address. The environment supplies raw bits; the CPU owns the operation and
word-result sign extension. There are no additional walk requests in Bare mode.

LR returns the original value and replaces the reservation with the accessed
physical address/width. Successful SC writes the source's low-width bytes,
returns zero and clears the reservation. Another 960 direct SC cells start with
a valid reservation at a different address: they return one, clear it and issue
no data Load/Store or memory write; each now makes a StorePermission request. The unchanged a-lrsc-mustfail guest also retains
its no-LR, width/address mismatch, replacement and intervening-SC history cases.
The dedicated reservation pair covers the histories below; deterministic SC
policy binding remains separate work.

The translated AMO fixture runs M-mode instruction fetch with MPRV/MPP=S data
access. VA 0x10000 maps to PA 0x5000 through these literal PTEs:

```
WalkAccess 0x2000 -> 0x0000000000000c01   (next table 0x3000)
WalkAccess 0x3000 -> 0x0000000000001001   (next table 0x4000)
WalkAccess 0x4080 -> 0x00000000000014c7   (R/W/A/D leaf at PA 0x5000)
Load       0x5000
Store      0x5000
```

All nine AMOs, both widths and all four ordering encodings run this successful
path (72 cells). The TLB receives the literal permission-bearing entry, while
all PTE bytes remain unchanged. Six bad leaf configurations—V=0, write-only,
read-only, A=0, D=0 and a U page with SUM clear—give 432 page-fault cells. They
stop after the three walk reads, deliver cause 15 with mtval=VA and mepc=the
instruction PC, and preserve rd/memory/reservation. An AMO cannot substitute
load-page-fault cause 13. Another 144 cells refuse either the physical Load or
Store; both deliver cause 7 with the virtual tval. A refused Store follows the
successful Load but changes no bytes or destination register.

Every boundary compares all GPRs/FPRs, 26 CSR owners, memory, PC/mode,
reservation including invalid retained fields, complete TLB/cursor, wait state,
exact requests, accepted parcels and execution outcome. Successful boundaries
advance mcycle 41→42, minstret 17→18 and PC by four; traps advance only mcycle.
The independent author checks 12,024 value/state boundaries and fetch/walk logs.
It omits explicit data-request logs and retained invalid reservation fields;
the direct observer owns those and the 144 physical-failure cases.

Nine deliberately wrong public instruction tables fail named observations:
a state-identical extra Load, skipped operation, missing Store, wrong operation,
missing word sign extension, extra CSR write, extra SC, TLB invalidation and
wrong next PC. Fourteen corrupt captures independently challenge the auditor.
Disabling the actual request predicate wrongly admits the extra Load and makes
the control RED. Changing the actual AMO translation kind to Load makes its
fault-kind witness RED. Both mutations are restored byte-for-byte before normal
checks. The completeness control first rejects an unregistered GC-ATOMICS pair.

The direct total is **12,168 boundaries, 24,336 parcels and 46,800 requests**.
The arith/minmax W/D, LR/SC pair, must-fail and Sv39 companion guests add
198 boundaries/396 parcels: the registered pair totals **12,366/24,732**.
The request pair witnesses this single-hart, side-effect-free-memory contract;
it proves no multicore indivisibility, weak-memory ordering or device behavior.


## Public evidence for the reservation policy

P4.13 c29a replaces old explanatory claims about the reference's internal
cancellation/error sites. The laboratory's reservation set, exact physical/width
matching, completed-SC invalidation and preservation on traps are selected
profile policies. Source comments now distinguish those choices from the ISA's
requirements. The failed-SC data-request rule does not erase translation reads:
WalkAccess requests may already have occurred before the reservation match.

All twelve original A guests run fresh through the pinned public binary and
unchanged validated override. Eleven guests agree over 290 boundaries, each
with two byte-identical traces. The twelfth, a-lrsc-mustfail, repeats its named
step-22 width-policy divergence: the reference succeeds on the .D SC after the
.W LR, whereas this profile requires equal widths. Two fresh divergence traces
are byte-identical too. Neither result licenses an inference about internal
reference functions or every possible reservation history.

The a-lrsc-fault guest is a concrete trap-retention witness: it reserves the
aligned word, attempts a misaligned SC, resumes through the handler, then
successfully stores42 with an aligned SC at boundary39 and reads42 at40.
Changing only the expected SC code to1 makes the fresh public comparison
DIVERGE at39. This control distinguishes the observed success from a comparator
that would accept either outcome. Existing unchanged must-fail/pair/loop guests
supply completed success/failure and constrained-loop observations; the declared
policy remains the authority for behavior outside these finite cells.

Historical internal-source quotations remain preserved as receipts in the task
archives, with a live evidence-boundary annotation in P4-SYSTEM.13 c29a. Current
matching claims use the public observations above. That repair changed no
instruction semantics, canonical guest, pin, frozen contract or registry entry;
its102/114 checkpoint is historical. See [contract v2](contract-v2.md#runtime-guarantee-witnesses)
for the current measure. Structured experiment registration remains
P4-SYSTEM.14's work.

## Reservation histories before binding

These histories began as an unbound prerequisite and now run in the dedicated
reservation pair. They check 60,640 boundaries: 56,448 normal steps and
4,192 fault steps. Seven histories exercise replacement by the latest LR,
wrong address/width, no LR, and clearing after both successful and failed SC.
Six more insert SW, SD, FSD, AMOADD, ADDI or FENCE before the SC, checking this
profile's selected preservation policy. Width, ordering, mode, destination/source
aliases and four data vectors vary. Distinct virtual addresses map to the same
or different physical addresses; repeated SC checks a cached translation.

For example, LR at A followed by LR at B replaces A's reservation. SC at A
returns1 and clears B's reservation, so a following SC at B also returns1.
If the first SC instead targets B, it stores and returns0; a repeated SC still
returns1. Trapping LR/SC cases preserve the prior reservation under the selected
laboratory policy, including its retained fields when invalid.

The direct observer compares every state owner, surrounding memory, exact
request sequence and retirement. The finite total includes 121,280 fetch parcels,
35,680 data requests,11,232 walk reads and20,736 permission checks:188,928
requests in all. Sixteen wrong instruction effects,
16 corrupt captures and23 disabled guards discriminate; paired outcomes catch
broken construction helpers even when expected state uses those same helpers.
The independent author checks every planned boundary and205 canonical words;
it does not observe explicit data requests or invalid retained reservation fields.
The qualified v2 replacement now binds both reservation checks. The
[current contract summary](contract-v2.md#runtime-guarantee-witnesses) owns
the realization measure; the dedicated SC policy pair still follows.

## Failed SC still checks physical permission

Cold `sc.w x7, x9, (x0)` to unmapped zero now takes cause7 with tval0,
without writing x7 or retiring. Previously it returned ordinary failure before
crossing the physical boundary. The pinned A12.1.2 requires memory permission
before SC retirement; fresh public Sail/Spike observations also take this trap.

After alignment and Store translation, a nonmatching SC issues
`StorePermission { width, addr: physical_address }`. `StorePermitted` allows
failure code1 and reservation clearing. A denied check traps with the original
VA and preserves the reservation. The check reads/writes no bytes and counts
no fetch. Matching SC uses Store's existing permission check. A malformed
permission answer is a typed provider violation, with no architectural trap.
For example, a mapped nonmatching SC can retire with1 even if a provider would
refuse an actual Store that was never issued. The experiment's `store` refusal
category covers both writes and permission checks; direct providers can
select their exact request kind.

The repair adds1,625full-state boundaries:1,152Bare and384translated permission
cases,80malformed answers,8provider-misalignment answers and the unissued-Store
control. The independent author cross-derives the1,536architectural permission
cells; contract-error answers are direct boundary evidence. Six new disabled
paths and all23prior guards discriminate and restore. Existing bound address,
width/region and every-kind event fixtures cover the added operation; frozen
v0/v1 remain unchanged. The reservation binding below includes all 1,536
architectural permission cases. The other 89 cases remain direct tests. Existing
environment pairs cover their declared boundary rules; these add no extra credit.

## Qualified reservation guarantee

The frozen `OB-RESERVATION` said invalidation was exactly the specification's
one-hart set. That wording overstated the authority of the selected policy.
`OB-GC-RESERVATION-V2` supersedes it without changing frozen v0/v1. The live
profile decision and requirement use the same qualified statement. V2 has
13 members; the replacement and its two executable bindings land together.

This laboratory chooses an exact physical address, byte width and validity bit.
Virtual aliases can pair when their physical address and width agree. Exact-width
matching, preserving the reservation across ordinary same-hart instructions,
and retaining it across traps are declared choices, rather than the ISA's only
permitted realization. The environment supplies no other-hart or device writes.

| Boundary | Selected reservation effect |
| --- | --- |
| Completed LR | Replace address/width and set valid |
| Completed SC, success or failure, at any address | Clear valid; retain address/width bookkeeping |
| LR/SC alignment, translation or physical access fault | Preserve prior valid/address/width and suppress destination writes |
| Ordinary instruction | Preserve the reservation; direct histories include SW, SD, FSD, AMOADD, ADDI and FENCE |
| Cold reset | Address=0, width=0, valid=false |

SC can complete only after alignment, Store translation and physical write
permission pass. `Reservation::matches` supplies the selected reservation
condition; a true result alone does not authorize a store or retirement.
The separate deterministic SC guarantee owns the no-spurious-failure choice.
The replacement selects this one-hart policy and does not claim multicore
behavior or every architecturally permitted reservation outcome.

`CHK-RESERVATION-POS` runs the 56,448 normal/history/alias boundaries above.
`CHK-RESERVATION-NEG` runs 4,192 fault boundaries plus the 1,536 architectural
permission cases, including their successful controls. The direct pair totals
**62,176 boundaries, 124,352 parcels, 35,680 data accesses, 12,384 walks and
22,272 permission checks: 194,688 requests**. The unchanged pair, must-fail and
trap-retention companion guests add 85 boundaries and 170 parcels.

The expectations still precede execution. The independently authored 60,640
history/fault boundaries and 1,536 permission cells retain their earlier
values and canonical-word derivations. Provider-contract errors and invalid
retained fields remain direct evidence outside that author's observations.
Sixteen wrong effects, 16 corrupt captures and 29 prior disabled guards still
discriminate. Two additional controls return an error from each registered
reservation witness; the registry test rejects both, confirming propagation.
Every source is restored before normal checks. The completeness test first
rejects the missing binding by name; its non-v0 selector is unchanged.

No CPU semantics, guest data or reference lineage changes here. The remaining
deterministic SC pair and final freeze keep the contract open; CPU acceptance
retains its separate evidence gates.

## Historical introduction and checkpoint receipt

The original six-slice timeline and c29a checkpoint paragraph remain verbatim
in `docs/tasks/archive/P4-SYSTEM-book-c33d.md`. Payload lengths/SHA256 and the
complete14,853-byte source inverse preserve their context. Current policies,
worked examples and public evidence remain above.
