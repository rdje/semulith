# P4.13 — Runtime contract witnesses

[Contract completion](contract-v2.md) tracks the effective count and freeze.

## Privilege-mode guarantees through the existing matrix

At .13 c8, OB-PRIV-MODES bound both checks to the complete
thirteen-guest P4.2 matrix, totaling 483 declared execution boundaries. This
reuses specification-derived expectations without changing instructions or
expected results.

The positive group runs mm-csr-rw, mm-ebreak, mm-ecall-modes, mm-ecall-deleg
and mm-counters. The negative group runs mm-csr-legality-s/u, mm-mret,
mm-readonly, mm-stimecmp, mm-wfi, mm-sfence and mm-sret. These are whole
programs with legal setup and both legal/refused cells; the labels describe
which behavior each group witnesses.

For a concrete mode observation, mm-ecall-modes reads mcause into x7:
M-mode ECALL yields 11 at step 8, S-mode yields 9 at step 28, and U-mode
yields 8 at step 53 (steps start at zero). The S/U CSR-legality programs
observe illegal-instruction cause 2 at steps 11/10. Other cells read trap
EPC/status and exercise delegation, return and counter/timer gates.

The shared comparison rule checks exact register changes at each step,
never-written registers and physical fetch counts. Mode and trap state are
observed through instructions and handler reads; this does not introduce a
direct comparison of trace PC/mode fields. Finite matrix evidence does not
prove every possible mode-dependent execution or Linux capability.


## Sv39 prerequisite: inherited global translations

Before binding OB-SV39, review exposed a mismatch between the CPU walk and
its selected cache policy. The CPU remembered only leaf G; an ancestor's G
was lost. Literal PTE regressions reproduced an access fault after an ASID/root
change and premature invalidation by an actual ASID-selective SFENCE.VMA.
The walker now accumulates G along the path. Root/middle/leaf combinations,
no-G controls and all four actual fence scopes discriminate the repair.

The independent expectation author already inherited G correctly and remains
unchanged. This fixes the declared retention policy rather than broadening the
ISA claim.


## Sv39 runtime checks

After the inherited-global prerequisite, OB-SV39's two checks now execute
all fourteen P4.3 translation programs. The positive group covers 4 KiB,
2 MiB and 1 GiB leaves, MPRV's effective mode, stale/fenced mappings and
an instruction straddling noncontiguous physical pages. The negative group
covers noncanonical addresses, invalid/reserved PTEs, misaligned superpages,
R/W/X and U/SUM/MXR permissions, Svade faults and delegated fault delivery.
ENVIRONMENT.md lists every binding.

For example, sv39-perm-rwx reads page-fault causes 15, 13 and 12 into x7
at steps 94, 101 and 109: store, load and instruction faults respectively.
The canonical-address guest reads cause 13 at step 51 and the original
address through mtval. Register changes, expected absent writes, handler
reads and continuation markers retain the existing comparison vocabulary.

The matrix spans 1,417 execution boundaries and 2,832 physical parcel
requests. Re-executing the independent parcel author reproduces every
committed register-change sequence and fetch count exactly. Neither the
programs nor their expectations changed. This is finite translation evidence,
not universal Sv39 or Linux acceptance.


## Svade: fault delivery and unchanged PTEs

OB-SVADE now runs its own positive and negative checks. The three successful
translation programs cover 4 KiB, 2 MiB and 1 GiB leaves and read back each
original 64-bit PTE after translation. The negative program, sv39-svade,
observes A=0 and D=0 behavior separately:

| Step | Result |
| --- | --- |
| 94 | A=0 load: x7 observes page-fault cause 13 |
| 100 | D=0 load: x14 receives 0x42424242 |
| 107 | D=0 store: x7 observes page-fault cause 15 |
| 133 | A=0 PTE read-back: x17 remains 0x2000188f |
| 134 | D=0 PTE read-back: x18 remains 0x2000184f |

A correct trap alone would miss an unintended PTE update. An in-memory control
sets A while still delivering the expected fault: its trap observations agree,
but step 133 reads 0x200018cf and fails. Disabling A/D refusal instead fails
at the first load. The normal independent author agrees with all four programs,
434 boundaries and 868 parcels; the existing core test also compares the whole
byte image across both faults. Guest inputs and production behavior are unchanged.

These witnesses retain the existing ISA observation vocabulary and finite scope.
The selected policy faults instead of updating A/D; Svadu is excluded.


## IALIGN-16: legal halfwords and required parcels

OB-IALIGN-16 binds c-links, c-page-end and sv39-straddle positively, and
c-page-straddle negatively. With C, both 16-bit and 32-bit instructions may
start at an address congruent to two modulo four. The instruction-length limit
remains 32 bits. These four programs use 165 boundaries and 319 parcel requests.

In c-links, C.JALR targets 0x8000000e and saves 0x8000000a, its pc+2 link;
the subroutine writes x10=1 and returns through that halfword link. In
sv39-straddle, a 32-bit ADDI starts at 0x80000ffe across noncontiguous physical
pages and writes x21=42 at step 44. The next instruction writes x22=7.

The two page-edge programs distinguish instruction length and fault timing:

| Program | Page-end result | Handler observations |
| --- | --- | --- |
| c-page-end | C.NOP executes at step 44; next instruction fetch faults at 45 | cause 12; mtval and mepc both 0x80001000 |
| c-page-straddle | Required second parcel faults at step 44 before instruction effects | cause 12; mtval 0x80001000, mepc 0x80000ffe |

The negative witness is an instruction page fault, not an alignment exception.
A successful first parcel cannot authorize skipping the second one. Conversely,
a compressed instruction must not fetch an unnecessary second parcel.

The independent author reproduces every committed register change and request
count. Four in-memory controls fail: enforcing four-byte parcel alignment (step
0), enforcing four-byte PC alignment (c-links step 3), over-fetching compressed
instructions (page-end step 45), and substituting the instruction start for the
failed parcel's trap value (straddle step 46). No source or expectation changes.
The existing comparison also checks never-written registers; direct trace PC/mode
comparison is not added. This is finite evidence for the selected contract.


## Zicntr: included counters and read-only refusals

OB-ZICNTR binds mm-counters positively and mm-csr-ro-counters negatively.
Zicntr adds the cycle, time and instret counter views beyond the G abbreviation;
Zihpm is excluded by the exact profile/CSR scope checks. The three assembler
spellings are read-only CSRRS specializations, not three new instruction encodings.
Counter rate and progress retain the existing virtual-time contract.

In mm-counters, the initial M-mode reads observe cycle=0, time=1 and instret=2.
The zero cycle read causes no register change. A gated S-mode cycle read delivers
cause 2; enabling mcounteren.CY permits x8=25 at step 25. In U, scounteren.CY
must also be enabled before x13=51 at step 51. The program's S-mode cells read
cycle; the existing core permission test separately checks S TIME's TM gate.
The independent author's existing mode matrix checks all three counters in M/S/U.

The negative guest attempts six writes to the read-only counter views through
register/immediate forms, including CSRRW with rd=x0. Every refusal preserves
its destination sentinel. Later legal zero-source reads observe cycle=45 and
instret=40 at steps 45/46; the differing counts retain the declared rule that
trapping instructions do not retire. The handler reads cause 2 and the final
refused instruction bits through ordinary GPR observations.

Independent replay reproduces both programs, 101 boundaries and 202 parcels.
Existing counter-enable and U-enable controls fail the mode-gate assertion.
An in-memory control replaces a forbidden write with a successful read: step 9
clobbers x5 with 9 instead of preserving its sentinel 7, and fails. No guest,
expectation or author source is rewritten. This pair is finite inclusion/refusal
evidence; OB-GC-COUNTERS remains a separate later binding. Firmware and Linux
acceptance are still open.


## Writable counters: explicit writes replace their own increment

The selected counters are 64-bit. Ordinary boundaries advance `mcycle` once;
retired instructions advance `minstret` once. RVI-ZICSR 5.1.1 and RVP-MACHINE
2.1.1.10 require an exception to that implicit update: **an explicit instruction
write takes precedence**, including a write that leaves the stored value
unchanged. The following read observes the written value before its own update.

For example, starting from the reset retirement count:

```text
addi     x6, x0, 41       # retires: minstret becomes 1
csrrw    x0, minstret, x6 # explicit write commits 41, replacing this increment
rdinstret x7             # x7 = 41; after retirement minstret becomes 42
rdinstret x8             # x8 = 42; after retirement minstret becomes 43
```

Writing `mcycle` similarly re-bases the shared cycle/time domain. The other
counter follows its ordinary rule: a successful `mcycle` write still retires,
and a successful `minstret` write still advances cycle/time. This remains
deterministic from the initial state and instruction/boundary history; the step
index alone cannot determine a domain that guest software can re-base.

CSRRS/CSRRC and their immediate forms suppress a write only when their source
**field** is zero. A nonzero register source containing zero still performs an
explicit write and therefore replaces the increment, even if no bit changes.
CSRRW/CSRRWI always write, including zero sources and `rd=x0`. Refused writes
perform no counter write: the trap boundary advances cycle/time and retires
nothing.

P4.13 c30a reproduced the old defect through the public engine: writing zero
to either owner left one after the same instruction. The repair records only
successful explicit writes in the current execution frame and suppresses that
owner's implicit update. These flags are discarded at the end of the boundary;
there is no new architectural state or snapshot requirement. Fixture setup
outside an instruction still precedes the next ordinary boundary increment.

Three suites cover both owners and all six CSR forms, zero/nonzero source
fields, unchanged/zero/high/wrapping values, destination suppression and aliases,
full GPR preservation, the next read and exact parcel requests. They include
1,776 cases /3,504 boundaries /7,008 parcels; 48 cases are refused S/U writes.
Both owner suites fail on the old engine and with the actual write recorder
disabled, then pass after restoration. The independent corpus author continues
to refuse writable-counter rebasing explicitly; these literal tests do not
silently extend its supported scope.

An authenticated public Spike run with explicit `rv64gc_zicntr` observes x7=41
and x8=42 in the four-instruction example twice, with identical raw logs. That
is a finite M-mode observation, not a full-profile match or independence claim.
The tracked Sail configuration explicitly disables Zicntr: it traps on the
owner write. Enabling only Zicntr in a temporary override is refused by its
public validator because no time source is configured. Those platform limits
remain explicit; the comparator is not weakened to turn the refusal into
agreement. This prerequisite repair adds no GC-COUNTERS registry credit.

## Explicit comparator setup before fallback repair

The nine timer-source programs now enable menvcfg.STCE in M before relying on
stimecmp. Cold STCE remains zero. Two four-byte instructions use unused x31:

```asm
lui x31, 0x80000       # RV64 sign extension sets bit 63
csrrs x0, menvcfg, x31 # select comparator-driven STIP; other bits are WPRI
```

Every body instruction moves eight bytes. Finite deadlines move two ticks, so
interrupts and halted spans retain their relative schedules. The independent
parcel author derives all new observations before processor execution; every
body write agrees with the declared address/counter/deadline transformation.
The nine inputs total 281 boundaries and 524 actual parcel requests.

| Guest | Boundaries | Parcels | New finite compare deadlines |
| --- | ---: | ---: | --- |
| c-irq | 19 | 32 | 11 |
| env-irq-sources | 13 | 26 | maximum, then 0 |
| i-prio | 65 | 124 | reset comparison at 0, then disarm |
| i-timer | 28 | 54 | 10 |
| mm-wfi | 63 | 118 | 13 and 27 |
| w-deleg | 28 | 52 | 15 |
| w-notrap | 21 | 36 | 10 and 16 |
| w-sw | 19 | 38 | disarmed above the observed time range |
| w-timer | 25 | 44 | 15 |

For w-timer, WFI retires at boundary 12, boundaries 13–14 remain halted, and
boundary 15 delivers STI without fetching or retiring. The handler reads
instret=13 at boundary 16 and time=17 at boundary 17. It then observes cause
0x8000000000000005 and mepc=0x80000034, the WFI continuation. The earlier
source comment's 0x80000044 was incorrect: its old assembled continuation and
observation were 0x8000002c. The added setup moves that continuation by eight.

Fresh records name the actual parcel route without inheriting capture chronology.
`--check-owned` now checks 41 unchanged historical captures and the fresh
13-boundary env-irq-sources record. Its budget is fixed in the author, never
read from the expected output. Wrong-budget and word-route controls fail; both
historical and fresh records reject count, observation, comment and line-ending
drift. mm-stimecmp's deliberately closed gates remain unchanged.

Fresh pinned Sail attempts agree on w-sw (19 boundaries, two identical traces).
Six inputs diverge: c-irq at 11, env-irq-sources at 12, i-prio at 26,
i-timer at 5, mm-wfi at 11 and w-deleg at 14. The trace witnesses absent
comparator pending or continued execution instead of declared delivery/wait.
w-notrap and w-timer processes refuse (rc1): their time/instret reads trap with
Zicntr disabled and enter trap loops. Old inputs reproduce those refusals.
The public timer diagnostic now enables STCE and reads back bit 63 on both
sides before comparing pending state (ten boundaries, repeat traces identical).
Its old seven-boundary STCE-clear result was confounded by the overlay defect
and cannot alone establish a reference cause. Public configuration validation
still rejects Zicntr without a time source and
CLINT without a mapped region. These are qualified reference-platform limits;
failed processes are never counted as agreement. Structured experiments remain
P4-SYSTEM.14's work.

## Sstc prerequisites: two discovered defects

Review found two issues before the Sstc pair could bind. c13a2 and c13b
repair them below, preserving the diagnostic evidence.
First, mm-stimecmp ends with a legal zero-valued S-mode read. Forcing every
S-mode stimecmp access to trap still matches all 35 GPR-change observations
and 70 parcel requests. Its last boundary instead traps with cause 2 and
mepc=0x80000044, but the budget ends before a handler read. A terminal absence
of a register change cannot establish that access succeeded.

Second, before c13a2 the implementation always computed STIP from time >= stimecmp, even
with menvcfg.STCE clear. The pinned machine chapter 2.1.1.18 requires STIP's
non-Sstc behavior when STCE=0; section 2.1.1.9 then permits M-mode software
to write mip.STIP. A public CSR diagnostic starts in M with STCE=0 and
stimecmp=UINT64_MAX, writes mip=32, then reads mip & 32. On baseline 618b7d2 the model
returned 0; the pinned fallback requires 32. This is a processor defect, beyond
the terminal-observation gap. The unconditional overlay originated at P4.2 d.
The frozen v1 interrupt-source wording also assumes the comparison unconditionally.

The architectural prerequisite is repaired by c13a2, after c13a1's explicit
setup. c13b closes the contract witness hole with direct S-mode programming and
refusal cases. Repairing interrupt pending alone granted no SSTC credit. Frozen
records and old receipts stay intact.

## STCE-dependent pending and the v2 source contract

Cold STCE=0 now exposes raw software mip.STIP=0. In M, software can set and
clear this bit independently of time/stimecmp. Setting STCE selects the unsigned
comparison instead, makes mip.STIP read-only, and retains the raw software bit
behind that view. Clearing STCE exposes the retained bit. This retention is an
explicit laboratory choice: the pinned rule selects behavior without specifying
transition storage. Existing mip storage owns it; no hidden latch is added.

| STCE | Raw software STIP | time >= stimecmp | Read mip.STIP | M write to STIP |
| ---: | ---: | ---: | ---: | --- |
| 0 | 0 | either | 0 | set or clear software storage |
| 0 | 1 | either | 1 | set or clear software storage |
| 1 | either | false | 0 | ignored, software storage retained |
| 1 | either | true | 1 | ignored, software storage retained |

sip.STIP remains read-only in both cases and is visible only when delegated.
MSIP/MTIP/MEIP remain zero and unwritable: no platform source is supplied.
For example, with STCE=0 and compare=MAX, writing mip=32 and reading it returns
32. Enabling STCE then reads zero; writing mip=0 leaves raw software STIP=1.
Disabling STCE reads 32 again. Software can then clear it with a legal M write.

Open v2 supersedes OB-GC-ENV-INTERRUPT-SOURCES with
OB-GC-ENV-INTERRUPT-SOURCES-V2. The event record refers to that source rule;
the cold-reset record now states pending zero. The frozen v1 statement remains
historical exact text. The registry retains its old checks as historical test
bindings and adds the replacement's direct POS/NEG pair. The effective census
stays 57 obligations / 114 checks, 68 realized: thirteen scope pairs, fifteen
guest pairs and six direct assumption pairs. Twelve v2 members remain open.
Coverage counts only registered checks whose records remain effective. The
report's independent recount and synthetic realized-record supersession control
verify this distinction; removing that filter fails both controls.

The new POS executes thirteen literal instructions (26 parcels): software
set/read/clear, explicit comparator enable/read-back, compare=0 assertion,
disable/recovered zero and a visible continuation marker. NEG executes fourteen
instructions (28 parcels) across all-one M pending writes, enabled-comparator
write refusal/retention, and read-only delegated sip in M/S under both STCE
settings. Every instruction checks all GPRs, exact raw mip, mode, PC and parcel
count. Sentinels distinguish zero reads from unexpected traps. An ignored
architectural write is expected CPU behavior, never a typed provider violation.
Historical source guests continue to run through their earlier registry entries.

Four new core regressions first failed on the old processor; after repair they
pass, including 48 actual instruction cases over all six CSR forms, two raw
software states, both compare conditions and both STCE settings. Five-bit CSR
immediates cannot set bit 5; their other pending writes still obey the selected
mask. The independent author tests eight literal source/write combinations and
retention; four deliberate source/write/retention mutations each fail. All 167
guest observations and 42 owned records remain exact. The original public CSR
reproduction changes from rc101 to rc0; the corrected public Sail diagnostic
still reports its qualified comparator-platform difference with STCE verified.

The direct S-mode witnesses below earn the SSTC pair; neither prerequisite
repair nor this pair establishes firmware/Linux capability.


## Observable S-mode timer programming and refusals

At c13b, CHK-SSTC-POS/NEG bind a named **Execution** evidence pair, distinct
from provider-assumption Boundary fixtures and static Scope checks. The normal
registry test runs each direct witness and its companion guests through the
existing corpus comparison rule. POS companions are i-timer and w-timer; NEG
retains mm-stimecmp. Original guests, expectations and frozen records are exact.
The new direct sequences use values fixed before processor runs, with independent
replay through the specification-side counter-author probe.

The positive fixture starts in S with mcounteren.TM=1, menvcfg.STCE=1 and
mideleg.STIP=1. Interrupt enables remain clear, so pending can be read without
interrupt delivery. Compare/time start at zero; x6 through x11 and x13 start at 0x55.
x12 supplies the literal full-width compare value 0x8000000000000020.
Each row is one actual 32-bit instruction fetched as two parcels:

| Boundary | Instruction | Destination observation | Compare after |
| --- | --- | --- | --- |
| 1 | ADDI x5,x0,16 | x5=16 | 0 |
| 2 | CSRRW x6,stimecmp,x5 | x6=0 (old compare) | 16 |
| 3 | CSRRS x7,stimecmp,x0 | x7=16 | 16 |
| 4 | CSRRS x8,sip,x0 | x8=0 (timer not pending) | 16 |
| 5 | ADDI x5,x0,0 | x5=0 | 16 |
| 6 | CSRRW x0,stimecmp,x5 | none | 0 |
| 7 | CSRRS x9,sip,x0 | x9=32 (timer pending) | 0 |
| 8 | ADDI x5,x0,32 | x5=32 | 0 |
| 9 | CSRRW x0,stimecmp,x5 | none | 32 |
| 10 | CSRRS x10,stimecmp,x0 | x10=32 | 32 |
| 11 | CSRRS x11,sip,x0 | x11=0 (timer cleared) | 32 |
| 12 | CSRRW x0,stimecmp,x12 | none | 0x8000000000000020 |
| 13 | CSRRS x13,stimecmp,x0 | x13=0x8000000000000020 | 0x8000000000000020 |

Every boundary checks all 32 GPRs, S mode, exact next PC, raw compare, time,
retirement and fetch count. After thirteen boundaries, time=instret=13 and the
fixture has made 26 parcel requests. Full-width S write/read-back retains bit63. These observations establish actual S
programming/read-back and continuation without an M round trip. The selected
laboratory immediately reflects comparator changes; the architectural source
allows eventual reflection and possible spurious interrupts. This finite fixture
does not require every platform to share the laboratory's exact latency.

The negative fixture has three cases: S with TM clear and STCE set; S with TM
set and STCE clear; U with both gates set. Each starts with compare=101,
x5=33 and destination x6=0x55, then executes CSRRW x6,stimecmp,x5 (0x14d29373).
The instruction must deliver cause2 before changing source, destination or
compare. Actual M-handler instructions then read mcause=2, mtval=0x14d29373,
mepc=0x1000 and stimecmp=101, followed by ADDI x11,x0,42. Every step checks
all GPRs, M mode/PC, compare, time/retirement, parcel count and the three trap
owners. Each case spans six boundaries / twelve parcels; the first does not
retire, leaving five retired instructions. Direct POS+NEG total 31/62.

The forced-all-S-access-illegal author copy still matches mm-stimecmp's old
35 changes / 70 parcels, ending in M at the unexpected final trap. The new
positive witness rejects that same defect model at boundary2. Disabling the
positive verifier makes the terminal control fail explicitly; its RED arm is
registered only after that failure is observed. Real-engine controls also reject
unexpected traps when either permission gate is cleared, and reject a NEG case
when its gate is opened and the write succeeds. The original observation rule is
preserved; additional direct evidence closes the coverage hole.

The registry self-test creates its synthetic declaration only in scratch
data and measures its own registration, so real ALU registration cannot break
its assumptions. Controls reject duplicate credit and distinguish full
effective coverage from a newly missing check. A duplicate-counting mutant
fails. This gate repair grants no CPU credit.


## Integer runtime witnesses

Immediate/register ALU and U-immediate evidence now lives in the
[integer runtime chapter](contract-integer.md), preserving its worked values and controls.

## Immediate ALU semantics through existing boundary programs

[Read the preserved section](contract-integer.md#immediate-alu-semantics-through-existing-boundary-programs).

## Register ALU wrapping, signedness and overlapping operands

[Read the preserved section](contract-integer.md#register-alu-wrapping-signedness-and-overlapping-operands).

## U-immediates use a signed offset and the instruction address

[Read the preserved section](contract-integer.md#u-immediates-use-a-signed-offset-and-the-instruction-address).

## Implicit Sv39 reads have their own request kind

OB-WALK-IMPLICIT binds a direct CPU Execution pair at P4.13 c24. The
laboratory spells every page-table read as WalkAccess, an implicit physical
8-byte read. Instruction fetch remains FetchParcel; an explicit LD or SD
remains Load or Store after translation. RVP-SUPERVISOR 11.1.3.2 supplies the
walk algorithm, and Sv39 selects three levels with eight-byte PTEs. Svade
raises a page fault when A, or D for a write, needs setting. The laboratory
permits no implicit PTE writes.

Earlier evidence remains: the typed address-units fixture already runs a
three-level CPU fetch/data path, core translation tests cover faults and cache
rules, and XLEN/LOAD-X0 have direct walk observations. This pair adds a finite,
explicit request-and-state matrix to the CPU guarantee's registry binding.

All cases use a fresh 64 KiB memory image at PA 0x80000000, satp
0x8000000000080002 and zero unlisted PTEs. Pointer PTEs have only V;
leaf flags 0xcf set V/R/W/X/A/D and clear U/G. Literal paths are:

| Leaf size | Physical PTE addresses, in order | PTE values, in order |
| --- | --- | --- |
| 1 GiB | 0x80002000 | 0x200000cf |
| 2 MiB | 0x80002000, 0x80003008 | 0x20000c01, 0x200000cf |
| 4 KiB | 0x80002000, 0x80003008, 0x80004008 | 0x20000c01, 0x20001001, 0x200004cf |

Nine successful cases cross each path with instruction fetch, LD and SD. Fetch
runs in S at VA 0x1000 for the 1 GiB leaf or 0x201000 for the smaller leaves;
all map to PA 0x80001000. Two ADDIs write x7=1 then x8=2. The first parcel
causes one walk; the second parcel and the next instruction reuse the same-page
translation. Each case has four FetchParcel requests plus its one, two or three
WalkAccess requests.

Data cases fetch in M at PA 0x80000000 with MPRV=1/MPP=S, so only data
translation uses Sv39. The corresponding virtual data address ends in 0x1080
and maps to PA 0x80001080. Two LDs read 0x0123456789abcdef from that address.
Two SDs write 0x8877665544332211 there and 0x1122334455667788 eight bytes later.
The first explicit access walks; the second hits the same 4 KiB cache entry.
Each case has four FetchParcel requests, two explicit data requests and the
literal walk prefix. Fetch parcels precede the data walk; translated instruction
fetch walks before its parcels. Exact request order distinguishes these paths.

Eleven fault cases stop at the attempted access:

| Refusal | Cases | Required observation |
| --- | --- | --- |
| Leaf A=0 | Fetch, LD, SD at depth three | Causes 12/13/15; three walk reads, no translated fetch/data request |
| Leaf D=0 | SD at depth three | Cause 15; three walk reads, no Store |
| Invalid PTE | Fetch at root, middle or leaf | Cause 12; exactly one, two or three walk reads, no parcel |
| Refused walk read | LD at root, middle or leaf | Cause 5, original virtual data address in mtval; no Load |
| Noncanonical VA 0x4000000000 | LD | Cause 13 before any walk or data request |

Data-fault cases still fetch their instruction's two M-mode parcels. Every fault
enters M at handler 0x80000100, records the original instruction PC in mepc,
consumes one cycle and retires nothing. GPRs and the complete memory image stay
unchanged. In particular A/D remain clear: no implicit write is hidden behind
the right trap. Successes check complete GPR/PC/mode/status/satp/trap/counter
state after each boundary and permit only the two planned explicit stores.

The direct matrix totals 20 cases, 29 boundaries, 50 parcels and 104 requests
(66 successful-path, 38 fault-path requests). POS companions sv39-translate-1g
and sv39-translate-2m retain 188 boundaries/376 parcels; NEG inj-walk-l2/l1/l0
retain 255/510. The combined pair totals 472/936. Its seven corrupted-capture
controls change walk kind/count/address, introduce a PTE Store, disguise a
fetch as a data read, or change a faulting PTE's A byte. All are refused.
Disabling the real request predicate makes its control fail. Temporary actual
walker mutations also fail: using Load+D with a matching Load response keeps
the PTE value but changes the request kind; writing A before delivering the
same Svade fault adds a forbidden Store. With the request predicate disabled,
the successful Load-disguised paths retain exact state and memory. This equivalence
does not extend to a provider refusing only WalkAccess: the disguised Load bypasses
that refusal, which a whole-matrix state-only probe correctly rejects. For write-A,
disabling only request judgment still rejects changed memory; disabling both
request and memory judgment leaves the exact original trap/state green. Thus the
extra write is detected even when its trap report is right. Production walker
and observer bytes are restored.

Independent specification-side derivation checks literal instruction words,
PTE mappings, full GPR/PC/mode/trap/counter/memory results and fetch/walk logs
for all 20 cases. Its log omits explicit data requests; the direct CPU observer
checks those separately. These finite cases do not exhaust page-table shapes,
permissions, ASIDs, cache eviction, speculative alternatives or all access-fault
kinds. They verify the selected laboratory's concrete request contract and
same-page cache behavior without changing Sv39 or its frozen declarations.

## Historical verification receipts

Dated progress counts, pre-bind identity checks and exact provenance receipts
are preserved in `docs/tasks/archive/P4-SYSTEM-book-c29d.md`, section `contract-runtime`.
That record authenticates the original chapter and every removed span; all
current feature examples and commands remain here.
