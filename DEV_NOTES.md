# DEV_NOTES.md

## _(2026-10-10)_ — bind immediate ALU arithmetic and counterexamples (P4-SYSTEM.13 c14b)

Rehash/read the pinned RV32I 1.1.4.1 clauses; six authored semantic rows match
sign extension, wrapping arithmetic, signed/unsigned comparison and logical
operations. POS names scope-alu, NEG bound-arith; both whole legal programs.
Their 31+31 boundaries /62+62 parcels independently match every committed GPR
change. Scope steps 8/9/10 read ANDI/ORI/XORI values 0xffffffff80000000,
0xffffffff800007ff and 0x7fffffff; step 16 observes the visible 1-to-0 unsigned result,
step 17 proves SLTIU sign-extends -1 before unsigned comparison. Boundary step 8
wraps INT64_MIN + -1 to 0x7fffffffffffffff; steps 9/10 cover -2048/+2047.

Five in-memory author alternatives fail exact observations: zero-extended SLTIU
at scope step 17, unsigned SLTI at step 14, zero-extended ANDI/XORI at steps 8/10, saturating ADDI at
bound step 8. Existing integer-author sign mutant refuses; normal 22 arithmetic/10
branch cases and 17 corpus gaps/471 steps pass, plus 42 owned records exact.
The new binding changes no instruction, expectation, canonical record, author
or core semantics. Identity: 348 profile files+four author/generated files and 72
prior entries exact. Registry: 74, effective 72/114:13 scope,16 guest,6 direct
assumption,1 execution pair. Gate oracle 20/0 passes with actual ALU registered.
make check passes Rust 167/17/201 and fmt/clippy. Focused schema270/two skips,
freeze3/zero findings, five report freshness checks and books pass. Hooks precede
commit; no new mechanism warrants repeated full CI.
Next OB-ALU-REG; 21 runtime pairs/freeze remain. Promotion declined: exact guest
bindings, original expected observations and worked runtime book retain it.


## _(2026-10-10)_ — contract-count controls survive complete registration (P4-SYSTEM.13 c14a)

The shared-id self-test hard-coded CHK-ALU-IMM-POS as unregistered. Simulating
its valid registration produced 17/18 controls: inserting it again cannot earn
another check, so actual 114/71 correctly disagreed with expected 114/72.
The production measure was right; fix the test before the planned ALU binding.
Scratch catalogs now add one reserved check to an independently selected
effective record. It earns credit only through that unit's exact registry pair;
an undeclared or unbound copy earns none, and a unit without a registry gets none.
New duplicate and full-coverage controls require no real check to stay missing.
The full fixture realizes every effective pair, then independently distinguishes
a new unbound declaration and its binding. Duplicate-credit mutant fails 19/20;
all 20 corrected controls and the formerly failing ALU-bound fixture pass.
Production AST outside _selftest, all crates/profile/author bytes and 70/114 stay
exact. The report wrapper verifies all generated reports; no new CPU credit.
No Rust change; report wrapper verifies five reports, all20 controls pass,
make book succeeds and derived-count controls10/0. Commit hooks precede c14b. Next
c14b OB-ALU-IMM. Promotion declined: live oracle controls and runtime book retain
this correction and its future full-coverage edge case.


## _(2026-10-10)_ — observable supervisor timer programming (P4-SYSTEM.13 c13b)

The terminal-zero guest defect is closed for SSTC contract coverage by direct
Execution evidence, separate from provider-assumption Boundary and static Scope.
Registry tests run the new architectural witness plus companion guests using
one existing corpus comparison helper. POS retains i-timer/w-timer; NEG retains
mm-stimecmp. No production semantics or old input changes are introduced.

POS executes thirteen S instructions /26 parcels with TM/STCE/delegation seeded
and interrupt enables clear. It programs compare 16, reads16 and pending 0,
programs 0 and reads pending 32, programs 32/read-back/cleared pending, then writes
and reads 0x8000000000000020 to retain the full 64-bit compare value. Sentinels
make zero reads visible. Each boundary checks all 32 GPRs, S mode/next PC, raw
compare, time/retirement and fetch count; no M round trip hides inside the budget.
NEG has three six-step cases: S missing TM, S missing STCE, U despite open gates.
CSRRW must deliver cause2 before source/destination/compare effects. Actual M
handler reads cause2, offending word 0x14d29373, EPC 0x1000 and unchanged compare 101,
then writes marker42. Trap owners and all GPRs/mode/PC/counters/fetches are exact;
first step does not retire. Direct pair totals 31 boundaries /62 parcels.

Independent counter-author replay agrees with all literal values. Its scratch
forced-all-S-illegal copy still matches old mm-stimecmp's 35/70, ending unexpectedly
in M, but the new POS refuses at boundary 2. Disabling that positive verifier
fails with a terminal-control-missed reason before its new GUEST-GEN arm is
registered. Real-engine tests reject POS with either gate closed, and reject
NEG with opened permission. Three direct tests and four registry tests pass.
GUEST-GEN142, registered shell arms646. Full make ci passes all five legs; Rust167/17/201, all doctrines/books green.

Identity: 348 profile canonical/guest files and four author/generated files exact,
core entirely unchanged, all 70 prior registry entries exact. Full independent
corpus remains 167/5360/10514 and --check-owned 42 exact. Schema/freeze/gate owners
retain their authority; report controls 18/0. Registry now 72 including historical
superseded checks, effective 70/114:13 scope,15 guest,6 direct assumption,1 direct
execution pair. Twenty-two runtime pairs and freeze remain. Next OB-ALU-IMM;
CPU-SYSTEM/firmware/Linux acceptance is not implied.
Promotion declined: the live execution mechanism, refusing control and worked
runtime book retain the lesson with its exact old/new witness behavior.


## _(2026-10-10)_ — STCE selects software or comparator STIP (P4-SYSTEM.13 c13a2)

Pinned Machine 2.1.1.18 makes STCE-clear STIP behave as absent Sstc;
2.1.1.9 then permits M software writes. The old unconditional comparator
introduced in 47badd2 discarded those writes and made cold pending one.
Repair the shared CSR field selection/legalization: cold STCE=0 reads raw
mip.STIP=0; M sets/clears it. STCE=1 selects unsigned time>=stimecmp and
ignores STIP writes. sip.STIP stays read-only/delegated. Retaining software
STIP behind the comparator is an explicit lab choice; no hidden owner is added.
Four core regressions fail before repair and pass after, including 48 actual
CSR instructions across all six forms, raw states and compare/source choices.
Existing comparator-only interrupt/time/event fixtures now enable STCE explicitly;
cold reset expectations become zero. State and definition input pins regenerate.
Affected FP-dirty comments now cite pinned conservative tracking permission,
removing implementation-specific dependency assumptions without changing FP.

The independent author follows the same clauses. Eight literal source/write
cases plus retention pass; four new source/write/retention mutants each fail
before registration. GUEST-GEN141; registered shell arms645. All 167 guests
remain independently exact at 5360 boundaries / 10514 parcels, all 42 owned
records exact. Original public CSR reproduction changes rc101 to rc0. Corrected
public Sail diagnostic still reports its qualified STCE-enabled platform gap.

Open v2 supersedes the frozen interrupt-source assumption, with a direct
POS/NEG pair executing 27 instructions / 54 parcels. Literal observations
cover source selection/transitions, forbidden M pending writes, retained raw
STIP and read-only delegated sip in M/S; every step checks all GPRs, mode/PC,
raw owner and parcel count. Ignored architectural writes are not invented
provider violations. Old bindings still run, but superseded credit is removed:
70 registry entries, 57 effective obligations / 114 checks / 68 realized.
No SSTC credit yet: c13b must repair the old terminal-zero witness hole.

Gate-report self-tests exposed an oracle defect: every registry entry was
assumed effective. Recount now independently intersects effective declared
pairs and registry pairs; dropping supersessions restores old credit. A new
synthetic realized-record supersession control catches the disabled filter;
mutant 16 pass / 2 fail, corrected 18/0. Production measure remains unchanged.

Identity proof: 335 guest files (334 source/record files plus run order), all
52 frozen record lines and both frozen forms exact; 68 earlier bindings exact.
DEV_NOTES containment moves 21 completed entries verbatim to shard-0220,
15329 B. Inverse reconstruction SHA256 b2fc35ed2b74186ccd13b60fda26e891c7ad39f5ee81f7d99403785712bf8306
matches committed head; fixed caps unchanged. Focused make check passes
Rust167/17/198; schema270/two named skips, freeze3/zero findings.
Full CI first exposed a stale compressed staging blueprint: c-irq still lacked
STCE, so both GREEN staging arms failed x7 (139/141). Repair its independent
setup/deadline/budget/PC checkpoints to the adopted input, not the processor.
Staging now gives 28 guests / 37 forms / 431 boundaries / 712 parcels; repeat
is byte-exact, both corrupted record controls refuse. Its c-irq body and complete
semantic record equal the adopted guest (19/32). All production inputs stay exact.
Full make ci passes all five legs (check, gate, bench, smoke-bench, book);
Rust167/17/198, all doctrines green and both book families build.
Promotion declined: explicit contract/history and worked runtime book retain
these corrections and controls.


## _(2026-10-10)_ — explicit comparator setup preserves timer schedules (P4-SYSTEM.13 c13a1)

Nine timer-source guests now enable STCE in M with LUI x31,0x80000 and CSRRS
menvcfg; x31 was unused. Independent derivation preceded processor execution.
Budgets increase by two, bodies move eight bytes and finite deadlines increase
by two ticks. All body instruction bytes except declared deadline immediates
and all GPR observations under that exact transformation agree. The nine inputs
span 281 boundaries / 524 parcels; full corpus 167 / 5360 / 10514. mm-stimecmp
and 316 other guest files, all four contract/version files and registry stay exact.
Removing stale inline chronology while providing fresh route provenance saves
19880 B across the nine source/record pairs; fixed family ceilings need no change.
The w-timer comment's old mepc=0x80000044 was wrong: assembly and observation
both give old WFI+4=0x8000002c, now 0x80000034. Handler instret/time now 13/17.

Historical author ownership is explicit: 41 captures stay exact; env-irq-sources
is a fresh parcel record with fixed author budget 13. --check-owned still checks
42 inputs. Both branches refuse count/write/comment/line-ending drift; new
wrong-budget and word-route mutants fail before their two GUEST-GEN registrations.

Fresh public Sail attempts: w-sw agrees (19 steps, two identical traces); six
inputs diverge at declared timer/wait observations, and w-notrap/w-timer processes
refuse rc1 after disabled counter reads and trap loops. Old inputs reproduce the
process refusals. The older timer diagnostic left STCE clear and therefore
confounded its laboratory result with the known overlay defect. Repaired here:
ten boundaries, explicit enable and bit-63 read-back on both independent sides.
It still observes Sail STIP=0 at both reads, versus laboratory 1; traces repeat
exactly. Removing enable makes its read-back guard refuse. Public config rejects
Zicntr without a time source and CLINT without a region. No submodule internals
are used; remove the maintained implementation-specific symbol from the book.

First full CI passed Rust 163/17/198 but refused a stale GS digest; regenerate
before final CI. Final make ci passes all five legs; Rust 163/17/198, registry
4/0, schema270/two skips, freeze3/zero findings and gate controls17/0.
Current docs also correct an old 64-check summary to verified 68.
No architectural fallback repair or new contract credit in this prerequisite.
Next c13a2 dynamic STIP/author/state/v2 supersession, then c13b direct S witnesses.
Promotion declined: the current owned-record protocol and worked timer example
are maintained in tracked author diagnostics and the runtime book.


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

## _(2026-10-09)_ — delegated supervisor CSR views are read-only zero otherwise (P4-SYSTEM.13 c7a)

Cold-reset review found shared CSR reads/writes missing mideleg's dynamic
view mask. Rehash/read RVP-MACHINE 2.1.1.9 (machine artifact SHA-256
b63fe33517fef2dabe53cdbc45b05d656bf808eebf83f0af5a4ab74549617fea):
nondelegated sip/sie bits must be read-only zero. The same public API probe
before repair exposed 0x222 in both views and erased mie/SSIP on zero writes.
After repair it exposes zero, preserves mie/mip=0x222, and the delegated
positive control still reads 0x222. One shared dynamic mask applies after
computed fields on read and preserves hidden owner bits on legalized write.
Interrupt arbitration, WFI wake and the M owners keep their specified rules.

The independent author's new controls also found sip reading a fake separate
dictionary owner; remove those view slots and overlay timer state on sole mip.
Canonical state/semantics prose and regenerated fingerprints carry the rule.
Three Rust tests exercise eight delegation masks in M/S, clear/set/revoke,
readonly SEIP/STIP and 192 actual CPU CSR steps across all six forms/views.
The initial S-mode instruction fixture correctly took a higher-M interrupt:
isolate view tests by disarming pending for sie, disabling enables for sip.
Five independent author mutations distinguish both read masks, write masks
and sip ownership. The first GUEST-GEN run overlapped the initial failing
author control (134/1); rerun against the corrected owner in full CI.
The first full CI instead caught the sip-owner mutant at an unnamed chained
re-delegation assertion. Split/named those assertions; all five mutations now
fail with their exact reason. Final GUEST-GEN 135/0; make ci all five legs green.

make check passes 160 core / 17 DSP / 197 verify. The public before/after probe
discriminates; author checks preserve 42 historical records byte-exact, and
all committed guests still match. No guest/contract record rewrite or added
credit: 56/112 remains open. Cold reset follows as c7b. Full CI receipt is in
the owning leaf. No knowledge promotion: canonical rule, tests and book retain it.

## _(2026-10-09)_ — ordering evidence needs an independent conversation (P4-SYSTEM.13 c6)

Rehash/read pinned RVWMO and Zifencei: program/global order, load-value/atomicity/
progress constraints and local fetch synchronization support this selected
sequential one-hart/coherent realization, without exhaustive weak-outcome claims.
One v2 assumption/pair runs literal SW/LWU/overlap/AMO requests for all aq/rl bits,
then warmed-code rewrites with/without FENCE.I. ScriptedEnv owns request order;
factor c4b's response-value comparison into one shared fixture owner.
Acknowledged discarded stores and stale parcels reach exact typed value errors
without wrong destination effects/traps. Disabled auditing loses all three cases.
Initially the bad load reached a later AMO whose changed store value was caught
by request matching. Stop that bypass control at its first bad load, retaining
the complete five-step positive conversation and all independent request checks.
This distinguishes the specific auditor from a sibling guard masking its bypass.
make check: 157 core / 17 DSP / 197 verify; schema/freeze, gate 17/17 and books
pass. All prior entries/frozen bytes remain exact; 56/112, cold reset remains, v2 open.
Promotion declined in leaf: canonical assumption, focused controls and book retain it.

## _(2026-10-09)_ — event location is distinct from source authority (P4-SYSTEM.13 c5)

The source/time v1 assumptions did not declare delivery positioning. Add one
open-v2 assumption/pair: head evaluation before fetch and a tick per step
boundary, with the current no-external-source/no-host-time choices retained.
env::check_event_delivery accepts a declared BetweenInstructions location and
returns typed EventDuringRequest otherwise. This opt-in adapter guard cannot
discover hidden host mutation and introduces no event payload or queue.
Direct fixtures observe an ADDI reaching a timer threshold then delivery before
the next fetch, plus WFI/two idle boundaries/timer wake with one retirement.
Five forbidden in-request attempts use actual GC paths, including its public
legacy word-table seam; mode, PC, destination, trap state, counters and memory
remain unchanged. Disabling the guard loses every negative case.
make check: 157 core / 17 DSP / 196 verify. Credit 54/110, 55 effective
obligations; ordering/reset and remaining runtime checks keep v2 open.
Promotion declined in leaf: canonical assumption, guard, fixtures and book retain it.

## _(2026-10-09)_ — data attributes need both byte and shape witnesses (P4-SYSTEM.13 c4b)

Add one open-v2 data-access assumption with a named direct registry pair.
Independent bytes/values/encodings check all four widths, executable little-endian
main memory, low-byte stores and eight load/store region-edge failures without
partial effects. Direct stores retain high input bits: the initial negative
fixture expected full SB input 0x1234 but the CPU correctly narrows it to 0x34.
Correct that literal expectation and test provider narrowing independently.
Twelve negative cases reject wrong kinds, over-wide loads and reversed D bytes.
Only the fixture's independent content witness can detect valid-width wrong
bytes; ResponseValueMismatch retains request/expected/arrived. The CPU's shared
shape validator is unchanged. Valid-content control passes; disabling the auditor
lets the bad load execute and makes the negative fixture fail.
make check: 157 core / 17 DSP / 195 verify. All 50 prior entries, frozen
parts/memberships and old root prefix remain byte-exact. Credit becomes 52/108,
54 effective obligations; event delivery, ordering and reset remain. V2 open.
Promotion declined in leaf: canonical assumption, direct fixtures and book retain it.

## _(2026-10-09)_ — reject malformed answers before consuming them (P4-SYSTEM.13 c4a)

The public GC probe supplied StoreDone to FetchParcel and a 9-bit 0x1ff answer to
an 8-bit Load: the former became InvalidDescription, the latter executed and wrote
all ones. A legitimate AccessFault control delivered cause 5. Handlers matched
kinds locally and accepted every u64 Load value; no shared response validator.
One env::request_checked now owns kind/raw-width validation across all 12 CPU
crossings, including scalar, parcel, walk and LR/SC/AMO paths. WrongResponseKind
retains the request/answer; LoadValueOutOfWidth retains width/value. Correct
responses, existing violations and Target failures pass unchanged, with no silent
truncation. Re-running the same probe yields typed ContractViolation failures,
x6=0 and mcause=0 for both malformed cases; the target-failure control keeps 5.
Four permanent tests cover the 25 kind combinations, width edges/full D range,
error passthrough and actual GC/scalar/translation paths. make check passes:
157 core / 17 DSP / 194 verify. Full make ci passes all five legs. The first
run refused checklist command signatures; exact invocations/results repaired the
signoff and the final run passed. A stale ENVIRONMENT summary said 48 after c3's
pair; corrected it to the measured 50 and regenerated GS through its owner.
No new record/registry entry or credit: 50/106 stays open; c4b owns data attributes.
Promotion declined in leaf: shared owner, permanent reproduction and book retain it.

## _(2026-10-09)_ — address units need a real boundary witness (P4-SYSTEM.13 c3)

Retain the normal guard requiring every post-v0 declaration to be born realized;
add the five remaining assumptions one paired slice at a time. The first pins
unsigned 64-bit physical addresses in 8-bit bytes. Evidence::Boundary runs a
named direct Rust fixture, rather than attributing an unrelated guest to it.
Hand-selected FlatMemory offsets/stores above 32 bits and a scripted Sv39 LB
observe actual byte offsets, physical walk/data/fetch addresses and two parcels.
Three provider adapters distort data to word indices, truncate a walk to 32 bits
or substitute a fetch VA; the real engine preserves exact typed ResponseMismatch
errors without a delivered trap or destination effect. A legal walk access fault
still delivers cause 1, so target failure and contract violation stay separate.
All 48 prior entries, root prefix, frozen parts and memberships remain byte-exact.
make check and schema/freeze pass; gate controls 17/17. Census: 53 effective
obligations, 106 checks, 50 realized. Four assumptions and remaining runtime pairs
keep v2 open; production boundary behavior/guest vocabulary unchanged.
Promotion declined in leaf: canonical record, direct fixture and book retain it.

## _(2026-10-09)_ — partition frozen catalogs through one reader (P4-SYSTEM.13 c2)

The obligation source had only 2,522 bytes left under its fixed 65,536-byte cap.
Move contiguous v0/v1 bytes into explicit root-relative parts; the expansion owner
reconstructs all 63,014 old bytes and 58 record mappings exactly. Root/parts are
9,003 / 47,168 / 7,009 bytes; no duplicate catalog or raised ceiling. Freeze,
conversion, registry declaration tests and scratch mutation copies share expansion.
Schema validation retains every source origin, then existing ID/reference rules
judge the expanded records. A schema-valid top-level comment previously failed
record mapping; annotations now add no records and retain schema ownership.
The canonical reader owns validated token spans, shared with expectation editing.
31 isolated controls include relocation, multiline literal directives, path/cycle
refusals and symlink loops; disabling expansion turns the same suite RED.
RECORD-SCHEMA has 48 controls (+5), registered total re-derived as 634. make check
passes; gate controls 17/17 and freeze pass. Full make ci passes all five legs. Its first run passed Rust/project checks
but refused a pending checklist box and stale Knowledge Map; both repaired
before the final green run. Correct the stale canonical G-CONTRACT gap statement too: c1
already supplies its four supersessions; the generator was copying obsolete text.
Promotion: decision_obligation-catalog-parts, permanent controls and book retain it.

## _(2026-10-09)_ — supersede the stage without rewriting its historical mirrors (P4-SYSTEM.13 c1)

Three v2 guarantees replace four obsolete v0 statements: qualified FP selection,
current generated definition, and fault priority distinguishing address triggers
from environment break. All old obligation bytes and frozen membership forms stay
exact. Current profile comments are repaired; historical decision statements and
requirement mirrors retain explicit replacement notes. Two scope pairs check pins,
active qualification records and existing owner generators; nine violating copies.
The priority pair runs reviewed competing-fault/FS-Off and EBREAK fixtures.
make check passes; effective census 52/104, 48 realized. Catalog size is 63,014 of
65,536 bytes: c2 owns lossless partition before five assumptions, with no cap rise.
Promotion declined in leaf: versioned records, permanent checks and book retain it.

## _(2026-10-09)_ — selection evidence keeps later implementation claims open (P4-SYSTEM.13 b5)

Realize ABI/SBI/RVWMO/privileged scope as predicates over decisions, state, source
identities and resolved encodings. Sixteen violating copies include narrow FP,
host firmware substitution, an extra hart and a same-count wrong privileged form.
Rehash cached psABI 1.0/SBI 2.0 public artifacts before fixing expected identities;
ordinary checks compare declarations without a cache or toolchain dependency.
Keep every prior registry entry byte-exact. Eleven scope pairs plus twenty guest
checks realize 42/106, with firmware/LP64D execution/Linux boot still unclaimed.
Regenerate GS after the final dossier-doc edit: its source digest covers those
documents too. The hook caught only that stale digest; regenerate through its owner.
Promotion declined in leaf: predicates, canonical decisions and book retain it.

## _(2026-10-09)_ — a printed version is not an enforced pin (P4-SYSTEM.13 b4)

A copied public C-build flow accepted fake clang/LLD 99.0.0 and emitted an ELF.
ACT4's duplicate resolver raised FileNotFoundError for a missing explicit compiler.
One resolver now validates exact identities before any probe output, refuses bad
explicit overrides, uses portable executable lookup and cleans unique on-volume
backend probes. Both callers use it; the C flags/link arguments are unchanged.
Twenty isolated controls exercise both callers, backend refusal, version query
failure, symbol-reader identity and PATH/Zig discovery. Disabling identity checking
fails three controls. The real C ELF SHA-256 remains f438ec2182ac57603c35e472942b7fa9de95cccc764bdf831c43288e7b50f437.
Promotion: amended the owning toolchain decision and book; no duplicate note needed.

## _(2026-10-09)_ — check identity and set equality rather than two agreeing omissions (P4-SYSTEM.13 b3)

Six structured scope pairs join composition: closure, privilege revision, CSR
selection/views, no PMP/H, and scope-to-resolved-name equality. Rehash the two
public privilege pages before fixing their expected identities; a different valid
hash is refused. Seventeen negative copies include removing fcsr from both
input lists and changing a C name while retaining its count. Every registry entry
runs; old guest bindings remain exact. Shard 12 older note entries and 11 older
changelog entries through the existing lossless sharder, preserving reconstruction
and frozen manifest. Promotion declined in leaf: predicates, records and book retain it.

## _(2026-10-09)_ — scope checks need their own executable evidence (P4-SYSTEM.13 b2)

The guest-only registry could not truthfully realize selection obligations with
unrelated executions. Add explicit guest/scope evidence and run scope ids through
a read-only parsed-declaration predicate. Composition POS validates the canonical
selection; NEG requires six violating copies to fail for precise reasons. Normal
Rust tests also disable each predicate family and refuse an unknown id. Preserve
all 20 prior guest bindings exactly; G-CONTRACT advances to 22/106 while v2 stays
open. Promotion declined in the leaf: registry, permanent controls and book retain it.

## _(2026-10-09)_ — state inventory distinguishes cold reset from exact continuation (P4-SYSTEM.13 b1)

The old consequence omitted the FP file, TLB, reservation and wait bit, and
counted CSR names rather than storage owners. Read the generated state fields and
TLB cursor, then re-answer the canonical descriptor. Time is the mcycle domain,
with no separate CLINT storage. Regeneration changes only source identity and
census prose; all executable definitions remain byte-identical. The commit hook
also caught the dependent definition manifest: regenerate its two state-source
pins, assert every other byte identical. make check
passes; remove only the resolved census opening. Serialization remains .16.
Promotion declined in the leaf: canonical descriptor and v2 book retain it.

