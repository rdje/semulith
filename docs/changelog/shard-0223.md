# DEV_NOTES shard — _(2026-10-10)_ … _(2026-10-10)_

> Sharded from `DEV_NOTES.md` under its 48 KiB ceiling (`doctrine/readme_routes.tsv`).
> Entries in a shard are **never edited after the shard** — git history is canonical.

## _(2026-10-10)_ — Sstc review exposes a terminal witness hole and STCE fallback defect (P4-SYSTEM.13 c13)

Before binding SSTC, an in-memory author copy forces every S stimecmp access
illegal. mm-stimecmp still matches all 35 changes / 70 parcels; final boundary
34 traps cause 2, EPC=0x80000044, but its zero read would also change nothing.
The existing budget stops before a handler read. No production failure follows
from this diagnostic alone: it establishes the guest's observation gap.

Pinned RVP-MACHINE 2.1.1.18 additionally requires STCE=0 to restore non-Sstc
STIP behavior; 2.1.1.9 then makes mip.STIP software-writable in M. A public CSR
probe on current core sets stimecmp=MAX while STCE=0, writes mip=32 and reads
mip&32: actual 0, required 32, rc101. computed() always overlays the comparator;
computed-field writes ignore proposed STIP. git log -S and 47badd2's diff locate
introduction at P4.2 d. Frozen v1's interrupt-source assumption repeats it.
Machine/supervisor/Sstc artifacts rehashed to all three pinned digests.

Own both repairs before SSTC credit. Keep cold STCE=0: prepare nine comparator
programs with explicit enable instructions and fresh independent observations,
including threshold/step changes and honest provenance. Then repair dynamic
STIP source/writability, author/state/reset/event fixtures and open-v2
supersession. Only then add direct S-mode compare programming/read-back and
handler-visible refusals to the registry. Full CI at behavior milestones.
Profile pressure must be measured before adoption; duplicated ENVIRONMENT
protocol prose can move verbatim to a linked book part within existing caps.
This commit is diagnosis/design only; production/guest/author inputs unchanged,
G-CONTRACT remains 68/114, 23 runtime pairs then freeze. LIVE_STATUS unchanged
(P4 12/18, 639 arms, 46 chapters). Promotion declined: owning task, explicit
canonical gate opening and runtime book retain reproductions and schedule.


## _(2026-10-10)_ — counter inclusion retains separate progress and access contracts (P4-SYSTEM.13 c12)

OB-ZICNTR binds mm-counters / mm-csr-ro-counters. Rate and progress
remain v1's declared virtual-time contract; OB-GC-COUNTERS remains its own
later pair. Exact selection excludes Zihpm; three counter spellings are CSRRS
specializations. Initial M reads are 0/1/2; S/U cycle retries read 25/51 after
separate enable gates. The guest does not read S TIME: existing core permission
fixture covers its TM gate (1/0), and independent author checks all three
counters in thirty counter/timer mode cases with source fields pinned.

Both guests independently match 101 boundaries / 202 parcels. Existing total-
and U-counter gate mutants rc1 with the intended assertion. In-memory read-only
write-as-read control first clobbers x5 at step 9 (9 instead of sentinel 7).
The real six refusals preserve destinations, including rd=x0 write semantics;
subsequent reads give cycle=45 and instret=40. Input sources remain unchanged.
Registry 4/0, make check 163/17/198, schema/freeze, gate 17/17 and books pass.
66 prior bindings / 340 inputs exact. G-CONTRACT 68/114; 23 pairs then freeze.
LIVE_STATUS unchanged (P4 12/18, 639 arms, 46 chapters). Promotion declined:
registry, exact selection and runtime book retain finite evidence and limits.

Active task head was 124649 B before ownership. Move completed early designs
(25612 B) and acceptance (26817 B) verbatim to archive part 7 (52711 B).
Ordered inverse reconstruction of the owned pre-move 126563 B head is exact,
SHA256 5b9c5f51506236994e0617d875990ed17e4712cf539b85f6de17042e580c3225.
Both moved blocks also match the prior commit. New head 74439 B before receipt;
frontier/census/current plans remain live, old archives/ceilings unchanged.


## _(2026-10-10)_ — halfword alignment includes precise parcel refusal (P4-SYSTEM.13 c11)

Bind OB-IALIGN-16 POS to c-links/c-page-end/sv39-straddle, NEG to
c-page-straddle. Rehash/read RVI-C 27.1 and review actual fetch/target paths.
C.JALR saves pc+2 and reaches 0x8000000e; translated ADDI at page+0xffe
executes across noncontiguous physical pages. C.NOP at that offset retires
before the following fetch faults; the wider instruction faults on its second
parcel before effects. Cause 12 is a page fault, not an alignment exception.
Straddle handler reads mtval=0x80001000, mepc=0x80000ffe.

Independent replay exactly reproduces four programs / 165 boundaries /
319 physical parcels. In-memory author controls enforce four-byte parcel
alignment (fails step 0), four-byte PC alignment (c-links step 3), unnecessary
compressed over-fetch (page-end 45), and instruction-start tval for the second
parcel (straddle 46). Four controls discriminate without rewriting source.
All 64 prior registry entries and 340 contract/guest/author files byte-exact.
Registry 4/0; make check 163 core / 17 DSP / 198 verify; schema/freeze,
gate controls 17/17 and books pass. 66/114, 24 pairs then freeze remain.
LIVE_STATUS unchanged: P4 12/18, 639 arms, 46 chapters. Promotion declined:
registry, immutable expectations and runtime book retain finite evidence/limits.


## _(2026-10-10)_ — correct faults alone do not establish Svade preservation (P4-SYSTEM.13 c10)

Bind OB-SVADE POS to the three leaf-size programs, NEG to sv39-svade.
Read frozen decision/record, menvcfg's WPRI 62:0 exclusion of ADUE, pinned
supervisor A/D schemes, finish/cache permissions and original observations.
The three successes read original PTEs in x17 at steps 110/98/88. The negative
guest observes A=0 load cause 13 (step 94), legal D=0 load value 0x42424242
(step 100), D=0 store cause 15 (107), then complete PTEs 0x2000188f and
0x2000184f at 133/134. Existing core step9 test compares full byte images.

Independent replay agrees for four programs / 434 boundaries / 868 parcels.
Two author copies run only in memory. Replace permits_translation's A/D refusal
condition with False: first mismatch at step 90. Separately inject
self.write(pte_addr, 8, pte | 0x40) before the walk's permission-failure return.
The fault causes at 94/107 remain correct; first mismatch is precisely step 133,
x17=0x200018cf instead of 0x2000188f. This control establishes that the later
read-back discriminates an implicit PTE update even with correct trap delivery.
Source files are never rewritten. Normal author/CPU observations remain intact.

All 62 prior bindings and 340 contract/guest/author files byte-exact. Focused
core Svade 1/0, registry 4/0 and make check 163 core / 17 DSP / 198 verify;
schema/freeze, gate controls 17/17 and books pass. G-CONTRACT 64/114, 25 pairs
then freeze remain. LIVE_STATUS keeps P4 12/18 and 639 arms; its derived chapter count is now 46.
Promotion declined: registry, immutable expectation values and book retain it.

The first commit hook refused contract-v2.md at 33,700 > 32,768 bytes.
Move the runtime sections byte-verbatim into contract-runtime.md: 28,722-byte
prefix + 4,978-byte suffix reconstructs the original exactly. Link both chapters,
register the new navigation entry and derive the chapter census (46). Consolidate
DOSSIER/ENVIRONMENT's repeated progress histories into current summaries/bindings;
worked examples remain in the book, full receipts in task/notes/changelog.
Profiles family falls from 3,144,422 to 3,138,746 bytes before final staging;
no contract/guest/author input or fixed ceiling changes. Routing and books pass.
Future profile changes update the current binding table rather than append history.

## _(2026-10-10)_ — bind Sv39 without rewriting its witnesses (P4-SYSTEM.13 c9b)

After the inherited-global repair, bind OB-SV39 to all fourteen P4.3 programs.
POS covers 4k/2m/1g leaves, MPRV, TLB/fences and noncontiguous straddle; NEG
covers canonical/invalid/reserved/superpage faults, permissions, Svade and
delegation. Read meaningful source including counted zero-word padding, actual
translation/CSR paths and expected observations. Matrix totals 1,417 boundaries
and 2,832 physical parcel requests; handler reads and changes retain the existing
comparison rule. No direct PC/mode, universal translation or Linux claim.

The independent diagnostic imports dossier_sexp.load_expectations,
riscv_asm.Assembler and derive_rv64gc_expectations.derive_parcel_guest. For each
of the fourteen sv39-*.s files it uses the declared instruction budget, compares
all step.writes with the committed write dictionaries and counts 'fetch' records
in hart.log against declared fetches. Every program agrees exactly; no inputs
written. Existing author controls and c9a's before/after regressions discriminate.

All sixty prior bindings and 339 contract/guest files byte-exact. Registry tests
4/0 and make check 163 core / 17 DSP / 198 verify; schema/freeze, gate controls
17/17 and books pass. G-CONTRACT 62/114, 26 runtime pairs then freeze remain.
LIVE_STATUS unchanged (P4 12/18, 639 arms, 45 chapters). Historical audit locates
leaf-only G introduction at e839c1b, repaired in 7569fe2; old receipts unchanged.
Promotion declined: exact registry, canonical scope and book retain this binding.

## _(2026-10-10)_ — inherited global mappings belong to the walk path (P4-SYSTEM.13 c9a)

Sv39 contract review found CPU walk caching leaf G only, while the independent
spec author accumulated G correctly. Rehash/read pinned supervisor artifact:
186,455 B, d5186efc3ead1c1f693ac2b16aeccdcab95d990264f49b559252d2dc413a651a,
11.1.3.1 non-leaf G inheritance and 11.1.2.1 fence scopes. The profile selects
exact retention rather than ISA over-fence latitude. Public translate regression
on e4e657f fails rc101: root-only G yields load access fault 5 instead of cached
PA after ASID/root switch. Actual SFENCE.VMA 0x12400073 regression fails rc101:
occupancy 0 instead of retained 1. This is a selected-policy defect, not a claim
that every ISA hart must retain every global entry.

Accumulate G from each traversed PTE after encoding checks; existing finish
permissions/Svade and successful-install discipline unchanged. Eight G masks
cover both ancestors and leaf, plus nonglobal and every combination. Switch to
an inaccessible root/other ASID to distinguish real cache hit from re-walk;
switch back also verifies no root-triggered flush. Thirty-two actual CPU fences
exercise both ASID scopes and both broad scopes after a PPN rewrite, checking
retained/refreshed PA and exact walk counts. Both tests fail before and pass after.

Focused translation 32/0 and make check 163 core / 17 DSP / 198 verify pass.
Independent cache author passes unchanged; its inheritance mutant fails rc1
with the intended non-leaf propagation assertion. Full make ci all five legs
green. Mark c7b census prose historical to avoid contradictory current counts. Contract,
registry and guest inputs are unchanged; G-CONTRACT remains 60/114, v2 open.
LIVE_STATUS unchanged: P4 12/18, 639 arms, 45 chapters. Promotion declined:
production rule, permanent discriminating regressions and book retain it.

## _(2026-10-10)_ — realize privilege modes through existing ISA observations (P4-SYSTEM.13 c8)

The frozen privilege-mode guarantee lacked bindings despite thirteen P4.2 guests
already running in the ordinary corpus. Read all programs, expectation owners,
registry and shared comparison rule. Bind its existing POS/NEG ids to all thirteen
programs: five focus on operations/mode exceptions/delegation/counters; eight on
permission refusals and return/interception gates. Whole programs contain both
legal and refused cells. All 481 declared boundaries execute; causes, EPC and
status are observed through handler CSR reads, never a newly claimed direct
trace PC/mode comparison. ECALL's x7 causes are 11/9/8 at steps 8/28/53;
S/U CSR refusal observes cause 2 at steps 11/10. No universal mode or Linux claim.

The required-binding guard now includes this old v0 pair; post-v0 birth-realized
coverage stays intact. All 58 prior registry entries and 339 contract/guest files
are byte-exact. make check 161 core / 17 DSP / 198 verify, focused matrix and
registry, schema/freeze, gate controls and books pass. Current 60/114, 27 runtime
pairs then freeze remain. LIVE_STATUS reviewed unchanged (P4 12/18, 639 arms,
45 book chapters). Promotion declined: bindings, canonical scope and book retain it.

DEV_NOTES was 48,051 bytes against its 49,152-byte cap. The adopted sharder
moves ten oldest whole entries to shard-0219; 45 before = 35 kept + 10 moved,
ordered bytes exact, head 32,112 bytes before this note. SHARD-FREEZE passes;
sealed archive descriptors and every fixed ceiling remain unchanged.

## _(2026-10-10)_ — full cold reset needs every owner before fetch (P4-SYSTEM.13 c7b)

Read pinned RVP-MACHINE 2.1.4 and all canonical reset rows, public state/reset,
TLB/reservation/wait contracts and memory construction. Add OB-GC-ENV-RESET
born realized, with a fixture-only startup auditor returning ResetStateMismatch
and its component/index. Positive dirties all owners, calls actual reset and
reconstructs memory; literal CSR/view/image witnesses precede actual ADDI.
No generated fresh-state value is used as the register/CSR expectation oracle.

128 cases poison every nonconstant x, f and raw CSR owner; PC/mode, TLB
content/cursor, reservation valid or cleared with retained fields, WAITING and
every image/outside-image byte. Each exact typed failure occurs before fetch
and preserves the whole poisoned state/memory. Disabling startup auditing
loses every case. Empty TLB occupancy alone misses FIFO=1; full Eq includes it.
Core private-field tests independently pin constructor entries/FIFO and
reservation address/width/validity, avoiding circular constructor agreement.

Cold fcsr composes zero but FS=Off makes architectural reads illegal; respect
that gate rather than enable FP to get a value. mip's old "Nothing pending"
reset prose contradicted its computed STIP=1; distinguish raw zero storage
from the live overlay. Reset values/implementation unchanged; fingerprints
regenerated. Cold SIP=0 because mideleg=0. No warm reset, host mutation
detection or snapshot implementation is claimed.

make check: 161 core / 17 DSP / 198 verify; schema 20 files, freeze 3 versions
zero findings and gate controls 17/17 pass. All 56 prior registry entries, root
prefix and frozen parts/memberships byte-exact. Full make ci all five legs green. Census
57 effective obligations / 114 checks, 58 realized; 28 runtime pairs keep v2
open. Promotion declined: canonical record, fixture/core controls and book retain it.

