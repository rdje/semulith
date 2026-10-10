# DEV_NOTES.md


## _(2026-10-10)_ — honor explicit counter-write precedence (P4-SYSTEM.13 c30a)

C30 prerequisite review encounters write-then-increment in timekeeping, root
e37e664. Authenticated Machine2.1.1.10/Zicsr5.1.1 say explicit writes replace
instruction-side updates. Real public-step tests RED rc=101: writing0 to either
owner leaves1; refusal control holds. Track/own before production repair.

Successful explicit CSR writes record per-frame counter flags. Boundary advance
skips only that owner's update, including unchanged writes; zero-source reads
still progress, refused writes never suppress the normal nonretiring trap step.
No persistent state added. Three suites GREEN rc=0:1776cases/3504boundaries/
7008parcels,48refused S/U writes, all six forms, source-field vs source-value,
full GPRs/aliases/read-back and exact requests. Actual no-op recorder RED101,
restored. First make check flags manual_is_multiple_of in fixture; corrected.
Final Rust170/17/223 with strict lint rc=0.

Two explanatory state strings qualify rebasing/history-based determinism;
STATE/DEF provenance RED1, published generation0, exactly three hashes only.
StateSHA cf460b3bfbfa31a2b95c748e70dd49badde1daa8e8fb815aa327823301419ac3.
Bounded author keeps refusing rebasing, only rationale corrected; independent
167/5365/10524 exact. GS digest only after environment sync; book worked example.

Public Sail's recorded Zicntr-disabled scope traps on owner write; initial4-step
probe hits duplicate deliveries after the trap, correctly refused. Bounded2
isolates that refusal. Temporary one-Boolean enable is publicly refused without
time source; no config/parser change. Spike initially lacks Zicntr under rv64gc;
explicit rv64gc_zicntr gives repeated4-step x7=41/x8=42, wrong42 discriminates.
This is a finite M observation, no full-profile or independence claim. Corrected
a scratch ELF IALIGN argument (bits16) before credit. Raw attempts retained.

Verify.py rc=0: frozen/guest/requirements/registry104/numerical state/history/
LIVE exact, effective102/114 unchanged; no binding credit. GUEST148/0, STATE/
DEF/SEMANTICS/focused/all six books rc=0. Scratch heading assertion/checker127
have no success credit; final published check names and book verified. Book
513368B/runtime29842B under fixed caps. Evidence target/p4-system-13/c30a.
Next c30 GC-COUNTERS; contain book/DEV before subsequent additions breach caps.
promotion: declined (architectural CSR precedence is already normative; permanent public-step controls and worked book example retain the diagnosed repair).

## _(2026-10-10)_ — ground reference overview in public evidence (P4-SYSTEM.13 c29e)

Root147de76 introduced source-tree counts/ancestry inferences into P0/P4/LIVE.
Read full chapters and actual schema/consistency/report consumers; these check
row/field presence and legal verdicts, not the truth of implementation ancestry.
Current overview now uses public artifacts/observations, explicit limitations
and independently derived expected values. Nine old spans6177B preserved in
finite17817B archive, SHA
d7df7f4fceaf2819fdc8def054c89c99c3ec16b268fd831653381c283ea30bb1.
Three full source inverses byte/order/SHA exact; corrupt/marker/omission reject.

Public.py/verify.py rc=0: authenticated scalar4/34/all12raw exact against
c29e0; FP24/927 pairs exact againstc29c. FP-VECTORS rc=0:230directed+3168
fixtures, hardware2131. Canonical base2experiments/6rows vsGC0/0 unchanged.
.14 already owns named decision/knowledge/canonical/closed .7 rationale sweep;
encountered acceptance reference added to its scope. No independence credit.
First row failed6144B cap before archive credit; restore only owned exact-source
replacements, shorten final row6131B (old6135). Status/counts unchanged.
Core/author/canonical/frozen/registry104/prior history exact; effective102/114.
Focused/all six books rc=0, previous Rust167/17/223 applies. Evidence
target/p4-system-13/c29e. Next c30 GC-COUNTERS after clean workflow/census.
promotion: declined (existing public-boundary/independent-expectation discipline; exact archive, current book and scheduled .14 sweep retain the scoped repair).

## _(2026-10-10)_ — contain completed task and development receipts (P4-SYSTEM.13 c29e1)

Source442a57d task124305B, only6767B below fixed131072. Five whole spans
79234B move to finite archive10/81004B, SHA
5e0f7eccbdd1f85707c66259ff78cb624b0b966894b97a2de074f4d73d9df310.
Live partition45649B; retained open plans/frontier/census/decisions exact.
Full inverse124305B/SHA45f985e70054d5d5fc5683dcc637a679e7fc14f2c7526b0830776e09f3ef57e8;
corruption/missing-marker/omitted-payload controls reject.

DEV36965B20entries exceeds36864 health target, still under49152 hard cap.
Published sharder self-test12/0 and dry-run preserve inputs. Four whole oldest
entries7098B to0228/7331B, SHA
9b2e8b4bc385edebf20688bb91c5b447919e24c9ba72973c7938b9d8e1a0fada.
Retained16/29867B plus suffix reconstructs exact source/order/SHA
48db9ec6872bf4c7b019286ddd63878ed56579b9f369231a494e0a97c6f01e76.
Prior19live rows/210sealed shards and task archives exact; logical230 rows.
No code/canonical/frozen/registry104/effective102/114/LIVE change or cap rise.
Book retains inverse example; focused/books in task. Evidence
target/p4-system-13/c29e1. Next c29e overview repair, then GC-COUNTERS.
promotion: declined (established whole-entry/exact-byte containment; source identities, inverse controls and book preserve the worked proof).

## _(2026-10-10)_ — refuse false scalar-reference credit (P4-SYSTEM.13 c29e0)

Root run_smoke.py ignores subprocess return codes and retains old output. It
also never authenticates its existing candidate pins. Diagnose.py rc=0 first
authenticates both actual binaries, then runs arithmetic with3successful calls.
Three exit7 stubs reuse those unchanged traces: the real experiment prints all
PASS and records no failure. Exact before source and trace hashes retained.

Add shared fresh-output/status guard and authenticate existing SHA pins before
comparison. Lifecycle refusal exits2; a compared discrepancy remains1. Budgets,
parsers, expected inputs, disabled comparison policy and successful bytes stay
exact. Offline probe RED1 on old runner; GREEN0 on repaired runner,16 controls
and3defective modes rejected. First mutant run hit an earlier cleanup assertion;
reorder fixtures so the stale-success mutant tests its intended credit path.
One new GUEST-GEN arm; derived count653 (38 doctrines/49 chapters/37 routes).

Public.py rc=0: four programs/34boundaries,12successful processes, four Sail
repeat pairs. Arithmetic raw traces equal the authenticated baseline. Temporary
wrong x1 expectation exits1. Initial scratch literal was not unique (x8 shares
it); select the full x1 write before credit. Final probe against exact old source
still RED1. Canonical inputs/frozen/registry104/effective102/114 unchanged.
Compare-old.py/verify.py rc=0: all12 raw files/full stdout equal isolated exact
old source; command args/constants/budgets/parsers/core/canonical/history exact.
GUEST148/0, focused/final BOOK-INDEX/all six books rc=0. LIVE only652→653,
6135B unchanged. No Rust change; prior167/17/223 applies. Evidence
target/p4-system-13/c29e0; c29e1 containment then c29e, broader sweep at .14.
promotion: declined (existing fresh-evidence/public-boundary discipline; permanent offline controls, real false-credit reproduction and book retain the repair).

## _(2026-10-10)_ — report generated index bytes accurately (P4-SYSTEM.13 c29d1)

Real CLI snapshot:23612 reported bytes vs24064 actual UTF-8 bytes,40 terms.
Probe RED rc=1. Root gen_book_index.py success message uses len(content), a
character count. Change only that expression to out.stat().st_size, measuring
the file actually written; render/write/check paths remain exact.

Same-input CLI GREEN rc=0 reports24064; before/after bytes identical SHA
ac9ff0d07fb058d99938111d5b9c56c89c4baa23e7ab89be408d5bce03f1575b.
Quiet --check rc=0. Book explains the measured Unicode difference and corrects
the c29b1 receipt's stale c29c/c29d-next tense. No new test/doctrine arm or
contract credit. Focused/all six books rc=0; final BOOK-INDEX/all six books
rc=0 after prose spacing. Previous Rust167/17/223 applies.
Evidence target/p4-system-13/c29d1. Next c29e public-ancestry repair, then
GC-COUNTERS and remaining runtime pairs/freeze.
promotion: declined (existing byte-measurement discipline; real Unicode CLI control and book retain the reporting diagnosis).

## _(2026-10-10)_ — retain book verification history under fixed caps (P4-SYSTEM.13 c29d)

Actual tracked book family starts51files/511554B (source-only census511245B
omits book.toml309B). Four chapter sources total106679B. Select45 exact
historical count/identity/provenance spans; preserve technical behavior when a
paragraph mixes it with a receipt. Current code/commands/tables/links/headings
remain exact; no include or relocated rendered content bypasses the cap.

Source-specific replacements save6703B. New finite task archive51848B, SHA
945d134ef00c5b60e9be115992fc51fe43bd7d96d013f73aa0e306e0be9d85ca,
contains original span bytes/separators and inverse map. Decode the tracked
map, remove exact footer, undo descending replacement offsets: every full
source returns byte/order/SHA-exact against6addc98. One-byte corruption, wrong
offset and omitted-span controls all reject without source mutation.

Book family504796B after derived index55B reduction; task family77files
including
new archive, below unchanged caps. All other books/code/author/canonical/frozen/
registry104/old archives/history/knowledge/LIVE exact, effective102/114 unchanged.
No Rust change; prior167/17/223 applies. Focused/all six books rc=0; evidence
target/p4-system-13/c29d. C29d1 owns generator stdout reporting characters
as bytes (len(content),23612 vs24064 actual); all cap/inverse measures above
use encoded/stat bytes. C29e owns encountered P0 internal-ancestry rationale
(root147de76) before GC-COUNTERS and remaining runtime pairs/freeze.
promotion: declined (established byte-preserving containment protocol; inverse map and exact payloads remain in the routed finite task archive).

## _(2026-10-10)_ — align state-source rationale and FP policy detail (P4-SYSTEM.13 c29c)

Fresh public24 FP pairs/927 boundaries and identical-write12 reproduce c29b
raw traces exactly before source edits. Current REQ-GC-F statement equals its
frozen OB-GC-F mirror: Dirty whenever values change is non-exclusive. Only
its explanatory detail incorrectly restricts Dirty to actual changes.

Five exact state prose deltas remove internal reference names, qualify LR/SC
trap retention as selected policy and describe any legal f/explicit FP-CSR
write versus changed-bit flag accrual. Correct only F source_semantics.detail;
all parsed state structure/other values and frozen bytes remain exact.
The scoped live-tree numeric question also replaces its backend ancestry
rationale with existing exact-rational/hardware/public evidence.
Both published stale-provenance checks RED rc=1, then generators rc=0.
The first hash-only assertion failed because gen_state.py:801 deliberately
emits census why metadata. Diagnose the exact diff: state module changes one
source hash plus precisely two read-only explanation strings; definition
changes two hashes. Revised exact replacements prove all other bytes unchanged.
Source SHA6f94e9cfa8fb8aa31daed162f37b22714db1512c6cd252063efcaa3d185a094c
→882483e090230562e4c932f0abd2095ab8b9819c7a4e0223be33069b3695d8e3.

Book/environment describe the same policy. GS regenerated after final profile
prose. Independent167/5365/10524, registry104/effective102/114 and frozen history
remain unchanged. make check rc=0 Rust167/17/223; normal generators/SEMANTICS
and focused/all six books rc=0; evidence under
target/p4-system-13/c29c. No behavior/status/experiment credit change. Next c29d
book containment, then GC-COUNTERS and remaining runtime pairs/freeze.
promotion: declined (established descriptor-to-inspection derivation; exact metadata/provenance proof and selected policy retained in the book and task).

## _(2026-10-10)_ — retain exact history under fixed caps (P4-SYSTEM.13 c29b1)

Committed ce3a53b heads: DEV46505B/24 entries, CHANGELOG56022B/97 entries.
Self-test12/0 and two dry runs rc=0 preserve all inputs. Published sequential
sharder targets30000/40000; DEV15kept+9moved17800B→shard0226(18033B),
CHANGELOG59kept+38moved16152B→shard0227(16389B). Actual numbering follows
both mutations; dry runs share the then-next0226. Remove only these new head
receipts/navigation, concatenate each retained prefix and exact archived
suffix: original bytes/order/SHA return. Full identities in task/book/partitions.

DEV source SHA92b5766fb8f41f3e563647aace6e20893e40bb8c02639e728dd1f841e84ca1f5;
CHANGELOG source SHAb451f91d5f4ebb1cbb498fd3dc0166b3044c4af09031a8a23537aaaf967feb93.
Prior17manifest rows/210sealed shards remain exact; append exactly two new
rows, logical229=19live+210sealed. Shards, family and live heads stay below
unchanged caps; prior code/canonical/author/generated/frozen/registry104 exact,
effective102/114 unchanged. Rust167/17/223 remains applicable; no Rust change.
Focused/all six books recorded in tree. Fix book's then-next AMO question to
past tense and route its completed public qualification. Next c29c source
rationale/F policy detail, then c29d book containment before runtime features.
promotion: declined (established byte-preserving partition discipline; source identities and inverse worked example retained in the task-tree book).

## _(2026-10-10)_ — ground FP-state claims in public evidence (P4-SYSTEM.13 c29b)

Scoped exec review found fdext_control.sail:19/wF implementation references.
FP book twice says Dirty only on actual value changes, unlike its own
write-Dirty operator paragraph/current evaluator. Source history dd9bc1c ported
those comments. Authenticated RVP-MACHINE2.1.1.6.7 explicitly permits Dirty on
unchanged f/fcsr writes; the laboratory selects every f-register write.

Diagnose.py rc=0: independent12-step same-value write before CPU; temporary
core probe observes identical f1 bits with FS Dirty after FMV.D.X, and Clean
after read-only FMV.X.D. Initial scratch comparison confused raw CSR owner
with computed architectural view; corrected to privilege::csr_read before
credit. Source restored SHAab6cdb46…170017a. Public12/24parcels AGREE twice;
wrong Clean expectation DIVERGE10. Existing24 FP guests/927 boundaries AGREE
in two identical traces each. Machine/F/D ISA and binary pins authenticated.

Two evaluator comment repairs, two book dirty-sentence corrections and a
reference-backend assumption replaced by scoped public-observation limits.
Exact declared text delta/all non-comment Rust lines preserved. Entire profiles/
reports/canonical/author/generated/registry104/frozen/archive bytes exact;
independent167/5365/10524 unchanged. make check rc=0 Rust167/17/223; focused/
all six books in tree. No policy/behavior or contract credit change (102/114).

C29b1 owns DEV sharding before source-prose/provenance c29c (additional state
internal names and stale F requirement detail). C29d owns bounded book history
containment before remaining runtime features; fixed ceilings stay unchanged.
Evidence: target/p4-system-13/c29b and worked floating-point book.
promotion: declined (existing published-interface policy; the identical-value/read-only/wrong-Clean controls and book retain the diagnosis).


## _(2026-10-10)_ — ground atomic rationale in public evidence (P4-SYSTEM.13 c29a)

Scoped history:1c554fc introduced reservation.rs internal Err/cancellation-site
claims;495b4b8 ported the SC evaluator commentary. Replace those explanations
and the reset-site aside with ISA/declared profile choices. Book no longer calls
trap preservation a universal specification invalidation rule. Clarify failed
SC explicit Load/Store exclusion separately from prior WalkAccess reads.
Only standalone Rust comments change, with exact declared text deltas and all
non-comment lines byte-identical. No semantic-source/generator changes needed.

Public.py rc=0: all12 original A guests fresh, pinned binary/unchanged override;
11AGREE/290boundaries in two identical traces each. Known a-lrsc-mustfail width
policy divergence at22 repeats in two identical traces; not agreement. Wrong
surviving-SC expected code1 gives DIVERGE39 in a fresh a-lrsc-fault run (actual
code0), retaining the subsequent read42 observation. No universal reference
reservation assertion or internal-source inspection. Historical raw quotes in
P4-SYSTEM-designs/P4-SYSTEM-2 stay byte-exact with a live annotation in the tree.

Entire dossiers/guests/reports, core code, author, generators, registry104 and
frozen/archive/knowledge/ledger bytes exact. Independent full167/5365/10524
corpus and effective102/114 unchanged. make check rc=0 Rust167/17/223; focused
checks/all six books in tree. Scoped review also encountered two FP internal
rationales, owned by priority-next c29b before GC-COUNTERS. Evidence in
target/p4-system-13/c29a and worked atomics book.
promotion: declined (established published-interface boundary; the public result/control and historical annotation retain the diagnosis and limits).


## _(2026-10-10)_ — discriminate atomic execution and faults (P4-SYSTEM.13 c29)

Missing-binding control selects GC-ATOMICS/count104 and fails rc101 for
CHK-GC-ATOMICS-POS before registration. Authenticate RVI-A56889B/SHAafbd8def
and supervisor186455B/SHAd5186efc; independent literal tables/assembler992
words/author12024 boundaries precede CPU execution. Initial scratch Sem
width-node construction corrected to published scalar Trunc/Sext API before
runtime control credit. Ten vectors ×11operations×W/D×aqrl×M/S/U×four rd patterns
=10560 successful cells; includes rd=rs1/rs2/x0 and two rs2 alias/zero controls.
Another960 SC address-mismatch cells return1/clear/no data requests.

Three-level MPRV AMO path: VA10000→PA5000, Walk2000/3000/4080 with PTEs
c01/1001/14c7. Nineops×two widths×four ordering cells:72 successes,432 page
faults (six leaf configurations),144 physical load/store refusals. Trap cause15
for pages/7 for physical failures, virtual tval, unchanged rd/memory/reservation.
Full GPR/FPR/26CSR/memory/reservation/TLB cursor/wait/PC/mode/outcome/request
observer; direct12168 boundaries/24336 parcels/45840 requests. Seven unchanged
companions198/396 give pair12366/24732. Author omits explicit data requests,
retained invalid fields and two-phase physical refusals; direct observer owns
these distinctions. No multicore proof from a one-hart request pair.

Nine wrong public tables and14 corrupt captures reject; request auditor off
admits state-identical extra Load (RED101), Atomic→Load translation gives
wrong page cause (RED101). Both actual sources restored by SHA before normal
checks. Registry104/effective102/114, six pairs/freeze remain. make check rc0:
167 core/17DSP/223 verifier; independent full167 corpus and focused/all six
books recorded in tree. Frozen/core/author/old102 registry/archives exact.

Encountered internal atomic cancellation/error-site rationales are owned by
priority-next c29a; c29 derives no dependency assumptions from them. All work
and measurements: target/p4-system-13/c29, tracked worked atomics book/tree.
promotion: declined (established direct-observer discipline; the worked atomic values, request paths and refusing controls retain the reusable evidence).

## _(2026-10-10)_ — ground fence reference claims in public evidence (P4-SYSTEM.13 c28e)

Scoped history/text census identifies b5621de's internal Sail-file quotation in
zifencei.sem.sexp, repeated by fence-i book/old .6 Result. User §20 requires
published boundaries. Replace maintained semantic/book rationale with authenticated
ISA/local coherence and public observations; annotate the historical receipt
without rewriting it. Three identified locations addressed; no repository-wide
internal-assumption audit is claimed. No dependency implementation was inspected.

Fresh public six guests/29 boundaries AGREE with two byte-identical traces each;
nonzero0011118f continues to x9=42. Wrong expected43 gives fresh DIVERGE at1,
rc1. This covers declared GPR changes/deliveries, not all ignored-field combinations.
Reference binary/config/pins exact; no new structured experiment/status credit.
Parsed semantic forms exactly equal. Stale generated provenance RED rc1; owner
regenerates the Rust module with only two source SHA replacements:
048555ac8a792789fb534d37d05c0f099a658f822520689e214265ecd2afcd5c →
91a6e728d1448d2f440a8672564c5912b6451ed105d87194429ded0f73b75164.
Every instruction/decode/effect token stays exact; no hand edit of generated code.

verify.py rc0: all profile/guest/frozen/registry102/evaluator/author/archive bytes
exact; independent167/5365/10524 corpus unchanged. make check rc0 Rust167/17/220;
DEF-GEN/SEMANTICS/focused/all six books rc0; hooks next. Effective100/114 and
LIVE652/49/P4 12/18 unchanged. Next c29 GC-ATOMICS SEMULITH-P4-0162, seven runtime
pairs/freeze; .14 statuses/experiments remain. promotion: declined (established
public-boundary policy; worked visibility book retains evidence/provenance limits).
Evidence: target/p4-system-13/c28e (fresh public/control, exact comment delta,
provenance RED, checks and identity proof).


## _(2026-10-10)_ — observe FENCE.I visibility and ignored fields (P4-SYSTEM.13 c28d)

Authenticated RVI-ZIFENCEI4.1,32380 B SHA4026de34713f4b898595eb4a17bb58176a0e2905196705a904d3d8fab4432a91.
Direct61440 field cells =4096 funct12×five rs1/rd pairs×M/S/U; POS3 canonical,
NEG61437 ignored-field words. Full GPR/FPR/26 CSR owners/memory/reservation/TLB
including FIFO cursor/Active wait/PC/mode/outcome/parcels/requests preserved.
Only PC+4/cycle+1/retired+1 and two parcel fetches.36 five-boundary SH/fence/LHU/
marker/patched-target programs cross W/C,0/2 mod4,M/S/U,canonical/nonzero/no-fence.
Word00200413 high-halfword0070 becomes00700413; C4409→441d, both x8=7.
The coherent no-fence subset and arbitrary-provider limits remain explicit.

Independent derivation first verifies all61440 states and36 program words/state/
fetch logs; direct61620/123222/123294 requests. Author omits72 SH/LHU requests;
CPU observer owns them and complete retained TLB/reservation fields. Three unchanged
companions17/34 give pair61637/123256. Initial diagnostic expected a shortened
source label; inspection found the existing full4.1/decision2/visibility locator,
retained verbatim and corrected the diagnostic (no producer change).

Eleven wrong public tables and16 corrupt captures reject, including cursor-only
TLB. Actual request auditor disabled admits state-equivalent extra Load, RED101;
actual WFI condition admitting FENCE.I fails wait state, RED101. Both restored
exact SHA. Wait entry has no public Sem node, so the actual core condition is
used instead of inventing one. Missing-binding completeness RED101, then two
Execution entries; prior100 entries exact. Registry102/effective100/114, seven
runtime pairs/freeze. make check rc0: Rust167/17/220. Independent full corpus
167/5365/10524; code/author/canonical/frozen/prior archives exact. Focused gates/
all six books rc0; hooks next. LIVE652/49/P4 12/18 unchanged.

Next c28e owns replacing obsolete Sail-internal explanatory assertions in the
semantics commentary/book (plus annotation of the old task receipt) with public
observations, preserving semantic forms/provenance. Current binding relies only
on authenticated ISA/local provider. .14 still owns statuses/experiments.
promotion: declined (existing direct-auditor discipline; worked visibility book and refusing controls retain the diagnosis and finite limits).
Evidence: target/p4-system-13/c28d (source auth, literal derivation, mutations,
missing-binding RED, direct/check logs, pair census and identity verification).


## _(2026-10-10)_ — bound public reference runs (P4-SYSTEM.13 c28c)

History75c79af introduced instructions+2;190d16b retained it while extending
interrupt vocabulary. Full dir-chase17-row prefix ends EBREAK, then two unclaimed
fetch-at-zero events map to duplicate boundary17. Public exact limit17 agrees.
Across167 fresh exact-limit pairs,24/25 previous tail refusals initially agree;
125 prior agreements/14 differences remain. Last fault-fetch has actual cause1
at boundary2 but legacy "the fetch at ... — no word fetched" is unrecognized.
Canonical133e722 record predates adapter; parsed corpus has one legacy/four modern
fetch-gap cells. No record is rewritten to fit the adapter.

Use exact declared limit; retain strict entire-trace parser byte-identically.
Recognize exact historical hexadecimal-address syntax alongside <fetch ...>,
requiring real fetch-class event/empty writes and rejecting instruction rows.
Offline orchestration control first RED rc1 (declared1 got3); legacy control
RED rc1 (actual event refused). Both GREEN rc0 after repair. Duplicate/malformed
events, truncated final row after interior gap, missing gap, bad legacy syntax
and attempted GPR-write waiver refuse. Five existing mutations remain RED rc1;
existing GUEST-GEN arm retains its success sentinel, no new arm/global count.

Normal live runner167:149AGREE/4566 declared boundaries with two fresh identical
traces;14 unchanged policy/platform differences; four refusals = three process
failures (mm-counters,w-notrap,w-timer) + cross_model=false guest-no-device.
Raw diagnostic includes that disabled guest, so its raw agreement is not runner
credit. All25 tail-shaped raw refusals now compare over complete declared data;
24 are enabled and repaired. Required C page-edge and terminal historical fetch
cases agree. Early targeted command used nonexistent c-jalr; corrected inventory
census uses actual names, no missing-file result counted as verification.
Public atomic regression242/3146 and wrong-granule control rc0. Finite GPR changes/
delivery presence only; event tval/PC/word/FP/memory/request checks not claimed.

verify.py rc0: strict parser/core/author/all previous inputs/frozen/registry100
exact except one live reference-scope prose delta; independent167/5365/10524;
effective98/114 unchanged. Focused gates/all six books rc0; hooks next. LIVE652/
49/P4 12/18 unchanged; no Rust edits, previous167/17/217 applies. Promote existing
shorter-trace knowledge card/INDEX, retain old bytes/fixed caps. Next c28d GC-FENCEI
SEMULITH-P4-0160, remaining runtime pairs/freeze; .14 statuses/experiments remain.
Evidence: target/p4-system-13/c28c (RED controls, exact raw/runner census, proof).


## _(2026-10-10)_ — qualify the public AMO granule boundary (P4-SYSTEM.13 c28b)

Confirmed local reference-configuration defect: scalar MAG exponent4 allows
contained AMOs despite amo=AccessFault. Historical a-lrsc-fault at800000fe crosses
16 B, so its agreement did not distinguish this case. Public two-fresh-trace
AMOADD.W at80000101 with rd17/data0 completes, writes rd0/data2a00, cause/tval0;
independent prior expectation faults7/tval80000101/preserves rd17/data0. History
859e5cc carried that parameter at privileged match. Validated exponent copies
0/1/2 fault this W case,3/4 complete; public schema0..12 and ISA strings checked.
No upstream or laboratory-core defect: the reference follows its supplied granule.

Change only scalar MAG4→0; vector/base override and frozen declarations exact.
New live public probe derives expectations first for242 cases (all22 atomic
forms, W7/D15 aligned/contained/crossing offsets, bare M, ordering clear). Each
13-row trace checks PC/word and declared GPR/CSR/data read-backs; each case has
two fresh successful byte-identical traces. Total3146 boundaries per repetition.
Validated restored-MAG4 control DIVERGEs at8 with actual completion read-backs;
old canonical config refuses rc2, corrected config rc0. Not a registered CI member
or new contract evidence. Missing/failed/incomplete/nonrepeat traces refuse.

Original A corpus11AGREE/290 boundaries plus same permitted width-SC difference.
All167 raw before/after/repeated traces identical;164 successful, three unchanged
process failures (mm-counters,w-notrap,w-timer) excluded from successful credit.
Whole-corpus identity is not CPU agreement. Broader run found owned adapter defect:
+2 steps produce duplicate post-program fetch delivery; dir-chase refuses rc2,
exact17 agrees. c28c priority-next before GC-FENCEI assesses all25 tail refusals
with permanent missing-evidence/parcel-gap controls. Matching limits stay explicit.

verify.py rc0: exact one scalar/one live matching-scope prose delta; all prior
canonical/core/author/frozen/registry/archive bytes exact. Independent corpus
167/5365/10524, registry100/effective98/114 unchanged. Adapter offline controls
rc0; focused gates/all six books rc0; hooks next. LIVE652/49/P4 12/18 unchanged;
no Rust changes, prior167/17/217 applies. Promote the worked counterexample into
existing must-diverge-control card/INDEX, retaining prior bytes under fixed caps.
Evidence: target/p4-system-13/c28b (live traces, variants, corpus, inverse proof).


## _(2026-10-10)_ — retain bounded development receipts (P4-SYSTEM.13 c28a)

DEV head47951/49152 B leaves1201 B. Published sharder target30000 moves seven
whole oldest entries18245 B into shard0225 (18478 B with wrapper), retaining
16 of23 entries/29706 B before this receipt. Inverse removes only this receipt/
new footer, then concatenates live prefix and exact frozen suffix to restore
committed5daa7bb47951 B SHA256
6d0ccb9383365685023d20543138f1e47735360257fe1fb9fe9560e91ecb70c3.
Suffix SHA2562cd85b0620a097a68dcb3d4c33384949601b1b06c2e7fb94ba4f7fb207fa5852;
shard SHA2569917a51413d8946b9059b36bd489321ea33f11c45651f94e5e497039998ee33f.
Earlier16 manifest rows/210 archived shards/object exact, fixed caps unchanged.
Sharder12/0 and inverse/identity rc=0. Code/inputs/registry100/effective98/114
exact; LIVE652 arms/49 chapters/P4 12/18 unchanged. Focused gates/all six books
rc=0; hooks next. c28b owns public Sail contained-vs-crossing AMO granule
qualification (tracked override exponent4; old matched AMO crosses boundary),
result pending/unclassified. GC-FENCEI follows. promotion: declined (established
lossless partition; authenticated shard and worked task-tree book retain proof).

## _(2026-10-10)_ — observe atomic alignment before translation (P4-SYSTEM.13 c27)

Authenticated RVI-A12.1.2/12.1.4 and machine exception table support frozen
LR cause5 vs SC/AMO7 policy. POS48 aligned W/D LR/SC programs cross ordering,
M/S/U and rd0/7; NEG8800 crosses all22 forms, every misaligned offset, five
bare/MPRV-S contexts, destinations and prior reservation validity. Full GPR/FPR/
26 CSR owners/memory/PC/mode/exact reservation and requests observed. Direct
8896/17792/17888 requests; unchanged companions63/126 give pair8959/17918.

Seven wrong public effects/thirteen corrupt captures reject. Actual request-
auditor disabled: extra-Load state-equivalent effect admitted, control RED101.
Actual LR cause4 and bypassed alignment each RED101 (CSR vs WalkAccess at2000);
core/observer restored exact. Missing-binding test RED101 before two entries.
Initial W-store expectation wrongly retained source high bits; a.sem.sexp's
explicit trunc32 explains the request, corrected to44332211; bytes were already
correct. Independent176 words/8896 states/fetch-walk logs match. Author omits
explicit data requests/retained invalid reservation fields; CPU observer owns
those checks. Full167/5365/10524 corpus exact. Prior98 entries,112 base/348 GC
inputs/core/author/generated/frozen/archives exact except one gate open-note.

That note from618b7d2e still said23 remaining pairs/SSTC fixes pending; GS
faithfully regenerated stale owner prose. Replace only that statement with
remaining-check/freeze ownership and a pointer to derived registry coverage.
All other canonical bytes exact. Registry100/effective98/114; Rust167/17/217.
LIVE652 arms/49 chapters/P4 12/18 unchanged; focused gates/all six books rc=0;
hooks next. Eight runtime pairs/freeze remain. Next c28a contains DEV head
under fixed cap before c28b GC-FENCEI. promotion: declined (direct refusing
controls and worked memory book retain policy, root cause and finite limits).

## _(2026-10-10)_ — align push guidance and local self-tests (P4-SYSTEM.13 c26b)

Cadence guidance from13266aa still advertised a variable-only push after
ac07ff8 required a committed approval. Enforcement was correct; change only
refusal help to name the director-approved recorded act. The decision's live
alias also called the fulfilled CI exception current; point to its completed
record/expiration, leaving that record and the real approval ledger exact.

All three helper self-tests used plain mktemp -d and inherited off-volume host
TMPDIR. Baselines were safely redirected on-volume; new path/help controls first
reject old code: cadence11/4, boundary14/1, act6/2 (each rc=1). Approval-act
baseline6/1 revealed a separate fixture defect: its borrowed real ledger already
had legitimate approvals, so the red-suite assertion falsely blamed old entries.
Use a literal nonempty synthetic ledger and compare its exact baseline bytes.

Derive owner-root/target/push-selftest for explicit allocators and nested Git/
toolchain TMPDIR. All three pass with a hostile on-volume caller temp and direct
from another working directory under the original environment:15/0,15/0,8/0,
rc=0. No synthetic directory residue. Local toolchain cache files stay on-volume.
verify.py rc=0: normal pre-push/approval-act paths and cadence distance/verdict/
dispatch exact except help; real ledger/fulfillment, CPU/inputs/registry/frozen/
archives exact; effective96/114 unchanged. The helper tests are not registered
CI/doctrine members; registered652 arms/49 chapters/P4 12/18 unchanged. No real
project push/approval act. Focused gates/all six books rc=0; hooks next.
promotion: declined (established push policy; repaired public tests and book
provenance example retain the failure mechanism and verified limits).

## _(2026-10-10)_ — preserve completed task receipts under fixed caps (P4-SYSTEM.13 c26a)

P4 tree123960/131072 B leaves7112 B. Six completed spans total81532 B; archive8
already59436 B, combined140968 cannot fit. Archive9 retains all payload bytes/
order/SHA markers in83418 B; live partition45205 B before new receipt. Inverse
extracts exact payloads, removes only new routes/ownership/receipts, restores
committed5eaef2a source123960 B SHA256
 efd367b86309c45a53ddf736352135e18ea56171f1669d43c43941626c7fb4ac.

partition.py/verify.py rc=0: all prior code/canonical/author/98 registry/generated/
frozen/archive bytes exact, effective96/114 unchanged; explicit new-file/cap
census and all kept segments exact. No Rust changes. Focused gates/all six books rc=0;
hooks next. LIVE unchanged652 arms/49 chapters/P4 12/18. promotion: declined
(established exact inverse; retained in archive9/tree and worked book example).

Own next c26b: cadence refusal still recommends approval-variable-only git push,
but pre-push correctly requires approved_push.sh's record (13266aa guidance vs
ac07ff8 recorded-act enforcement). Reproduced rc=1/contradictory public recovery
text. Fix guidance/behavioral controls next; no real push or approval fabrication.

Prior development notes: `docs/changelog/shard-0228.md`; earlier history via `docs/history/README.md`.
