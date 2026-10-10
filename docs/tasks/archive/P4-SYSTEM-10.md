# P4-SYSTEM — evidence archive 10

Captured from 442a57da57fe4529febcb2a6641486240236c779 (P4-SYSTEM.13 c29e1).
Source docs/tasks/P4-SYSTEM.md: 124305 bytes, SHA256
45f985e70054d5d5fc5683dcc637a679e7fc14f2c7526b0830776e09f3ef57e8.

Five whole completed spans preserve 79234 original bytes in source order:
c26a–c29e0 designs/acceptance and complete original verification/commit/changelog
sections. Existing older history routes remain in their original context. The
active frontier, open c29e1/c29e plans, census and decisions stay in the live tree.
Historical "next" and "current" do not override current canonical/live records.

Extract after each BEGIN marker's newline and before the extra newline preceding
its END marker. Byte lengths and SHA256 authenticate every payload. Replace the
five new live history routes with these payloads, remove only new receipts and
restore c29e1's queued ownership to reconstruct the full committed source.
Earlier task archives and append-history shards remain immutable; caps stay fixed.

## designs

<!-- BEGIN designs bytes=44642 sha256=b8bfcc225edc2f4259db2a1bffced264a2c4edc52819d79873f31caa4696b09e -->
### `.13` c26a — preserve whole completed task receipts (completed, `SEMULITH-P4-0154`)

Owned on clean5eaef2a after complete workflow/census. Actual source123960 B,
SHA256 efd367b86309c45a53ddf736352135e18ea56171f1669d43c43941626c7fb4ac,
leaves7112 B below fixed131072 ceiling. Reviewed task/tree and route contracts,
archive8 byte-authenticated marker format, whole-source inverse and book workflow.
Finite spans from source: completed design-a15395/design-b17819, acceptance27509,
whole verification6581/commit5073/changelog9155 (older log rows retain context),
total81532 B. Archive8 is59436 B; combined140968 before wrappers cannot fit.
Create archive9 with six exact ordered payloads, source context/lengths/SHA256;
keep archive8 and all previous parts exact. No cap increase or sealed transition.

Keep live frontier/census/active ownership and route links. Before moving any
payload, capture source, spans, all original bytes and this ownership delta.
Inverse removes only new routes/receipts/ownership additions, replaces original
payloads in source order and must reconstruct exact committed5eaef2a bytes/hash.
Authenticate archive extraction separately and prove retained segments exact.
No runtime/input/registry/frozen/code changes, effective96/114 unchanged. Update
MEM/DEV/CHANGELOG/book/index; verify archive/new-file bounds, inverse, prior98
bindings/canonical/core/generated/frozen identity, focused gates/all six books/
hooks, commit/empty brief/clean actual census before c26b below.

### `.13` c26b — align push guidance and local self-tests (completed, `SEMULITH-P4-0155`)

Owned on clean f5739ec after workflow/census. Reproduced cadence help rc=1:
variable-only command contradicts actual pre-push record requirement. 13266aa
introduced guidance; ac07ff8 hardened enforcement without updating it. Fix only
recovery text to name director-approved approved_push.sh and explain variable
alone insufficient; never fabricate approval or push the project remote.
The live How-to-apply alias in decision_push-cadence still calls the CI exception
current. Primary fulfillment record says all three passed on76882c8 and approval
expired2026-10-08 (observed2026-10-09); correct that live pointer only.

Scoped public-tool review found two additional concrete defects, owned now:
(i) cadence/pre-push/approved-push --self-test use plain mktemp -d, so inherit
host TMPDIR (observed /var/folders/... outside repository volume). Baseline
runs are explicitly redirected to target/p4-system-13/c26b/caller-temp; no
outside data is created/deleted. Fix all three test-only allocators to derive
owner repo/target/push-selftest and ignore caller TMPDIR. Add path controls first
and see RED with a safe on-volume hostile caller temp; preserve success cleanup.
(ii) approved-push baseline is6 pass/1 fail: copied real ledger already has two
legitimate entries; "red suite left a ledger entry" falsely blames pre-existing
history. Real ledger unchanged. Replace borrowed ledger with a literal synthetic
prior approval and compare exact baseline bytes across the deliberately red
suite. Exercise a nonempty fixture and preserve append/record-push tests.
Baseline cadence11/0 and boundary14/0; all scratch cleaned under caller-temp.

Finite changes: three self-test scratch allocators/guards, cadence help + three
behavioral guidance controls, deterministic synthetic prior ledger and exact red-
suite no-write comparison, fulfilled-decision pointer, book/live/task receipts.
First guidance/path controls must fail old implementation; then repair and rerun
all three public self-tests without redirected host temp. Baseline production
cadence distance/verdict and complete normal pre_push/approved_push paths must
stay byte-exact. All CPU/registry/canonical/frozen/archive data and real approval
ledger unchanged. Preserve existing pending-reset/privilege/release ownership.

These three helper self-tests are not project-doctrine registry members; rg
census finds no CI/Makefile driver calls. Their local control totals may grow,
while DERIVED-COUNTS' registered total652 stays unchanged; do not invent credit.
Focused explicit tool tests, PUSH-RECORD, derived counts/bounds/frontier/reports/
freeze/schema/book/shards and all six books, hooks, commit/empty brief/clean
actual census. No Rust changes or real full-suite/push invocation required by
this help/test-only repair. Next c27 ATOMIC-MISALIGN, reviewed only after clean
commit; .14 retains statuses/experiments. Final scope is bounded to these fixes.

### `.13` c27 — observe atomic alignment before translation (completed, `SEMULITH-P4-0156`)

Owned on clean9a39f48 after full c26b workflow/actual census. Read roadmap P4,
frozen OB-ATOMIC-MISALIGN/REQ-D-ATOMIC-MISALIGN and dependencies, public LR/SC/AMO
execution/reservation/trap interfaces, registry/tests, atomics/v2/runtime/memory
book and source routes. Binding absent in current98 registry/effective96/114.
Frozen policy is LR cause5, SC/AMO cause7 before translation; status mirrors and
structured experiments remain .14, multicore/external events remain their owners.

Finite direct pair: POS48 aligned LR/SC programs (W/D × four aq/rl × M/S/U ×
rd0/7), two boundaries each; independent negative-word load sign extension and
low-width store bytes, reservation replacement then clear. NEG all22 atomic
forms × four aq/rl × every nonzero offset below width × five contexts × rd0/7 ×
invalid/valid prior reservation =8800 one-boundary cases. Contexts: bare M/S/U,
M fetch with MPRV-S/Sv39 invalid root, and MPRV-S noncanonical data address.
Expect cause5/7 with original VA/PC before any Walk/Load/Store, unchanged full
GPR/FPR/memory/reservation, all CSR owners except literal trap stack/time,
no retirement and exact two fetch parcels. Negative SC must trap even without
an eligible reservation. POS companion a-lrsc-pair; NEG a-lrsc-illegal and
 a-amo-overlap retain original comparison/bytes (illegal encodings are companion
coverage, not the direct alignment claim).

Scoped report review found an additional live-doc defect, owned/fix-now here:
gate.sexp's G-CONTRACT open statement still says23 remaining pairs and SSTC
repairs pending despite current96/114 and completed c13 work. git blame names
618b7d2e; generated GS repeats that stale canonical prose correctly. Replace
only this live open statement with the remaining-check/freeze owner and a pointer
to derived coverage, without another hand count. Add exact one-statement delta
to identity proof; every other canonical byte stays exact. No gate criterion,
verdict rule, frozen obligation or .14 status changes.

Derive literal words/state using independent author and pinned primary chapters
before writing runtime fixtures; source identity must authenticate offline.
Add named wrong public-table controls for cause/tval/PC/state/reservation/request/
memory corruption and actually disable an auditor to see RED, restore exact.
Temporarily change actual LR misalignment cause and bypass its alignment guard
under invalid Sv39, observe named RED and restore core exactly. Select new pair
in completeness test first and see missing binding RED before registration.
Keep prior98 entries/inputs/author/core/generated/frozen/archive exact; only this
runtime pair adds credit. Run focused checks then make check, all six books and
normal hooks; update GS/environment/book/live docs/task, explicit three acceptance
boxes/promotion, commit/empty brief/clean actual census before next pair. DEV
currently46003/49152 B: keep receipt bounded; contain before a later receipt if
needed, without weakening caps. No new doctrine or requirement-status change.

### `.13` c28a — retain bounded development receipts (completed, `SEMULITH-P4-0157`)

Owned on clean5daa7bb after full workflow/actual census. DEV_NOTES47951/49152 B
leaves1201 B. Source SHA2566d0ccb9383365685023d20543138f1e47735360257fe1fb9fe9560e91ecb70c3.
Read canonical sharder/manifest/freeze/bounds contracts and book task-tree
receipt protocol. Target30000 using published --head DEV_NOTES.md --max-bytes:
23 entries =16 kept +7 oldest moved, exact18245 B suffix, partition29706 B.
New shard0225 with wrappers; authenticate source/suffix/entry order and inverse
including any new footer/receipt removal. Earlier16 manifest rows/210 archived
logical shards/sealed object exact. Family currently17 files/173677 B, per-part
65536/family786432 fixed; live49152 unchanged. No runtime/profile/input changes,
registry100/effective98/114 unchanged. Update bounded live docs/book/task,
sharder controls, focused bounds/freeze/frontier/count/index/report/schema and
all six books/hooks; commit/empty brief/clean actual census before c28b.

### `.13` c28b — qualify the public AMO granule boundary (completed, `SEMULITH-P4-0158`)

Activated on clean a186409 after full containment workflow/actual census.
Read published adapter/trace parser/ELF assembler and independent author, tracked
Sail configuration/reference hash, A/machine primary clauses and memory/atomics
book. Initial finite diagnostic: a 13-boundary M program seeds rd=17, performs
AMOADD.W at0x80000101, then reads mcause/mtval and two aligned data doublewords.
Handler is the common following instruction, so trap vs completion is observed
by values independently of branch layout. Derive expectations before execution,
zero-pad the ELF's data cells, validate the exact baseline override, require
fresh successful/repeated traces. If it disagrees, test the granule parameter
through validated copies before changing any canonical input. No new credit.

Owned concrete evidence question found while reviewing c27's pinned A12.1.4:
optional misaligned-atomicity granule permits an AMO wholly within its granule.
The tracked Sail override has granule exponent4 (16 B) alongside amo AccessFault.
The historical matched a-lrsc-fault uses 0x800000fe (A-2), whose W access crosses
a 16-byte boundary; it does not distinguish contained-AMO behavior. No new
matched-reference claim was made for c27's8800 direct cases, but the frozen
reference-matched policy needs a public-boundary qualification before relying
on broader equivalence. Initial public reproduction CONFIRMED reference-configuration defect, priority
fix-now: validated tracked baseline, AMOADD.W at0x80000101 completes instead of
cause7. x5 changes17→0, mcause/mtval read0, aligned data read-back0x2a00; two
fresh13-row traces byte-identical, adapter DIVERGE at8. Laboratory expectation
was derived before either run. No production-core defect or new contract credit.
Public variant isolation rc=0: exponents0/1/2 validate and fault cause7 at the
contained W case;3/4 validate but complete/write. Public default/schema describe
the field as a granule exponent (schema integer0..12); baseline/no-granule public
ISA strings are identical. Thus AccessFault does not override the present MAG.
History859e5cc introduced the carried parameter at the privileged match; the A
experiment's boundary-crossing witness could not distinguish it. This is a local
matching-configuration defect, not an upstream Sail defect.

Repair scope owned before changes: change exactly scalar MAG exponent4→0 in
GC reference override, leaving vector/external/scalar/base-profile state and all
frozen declarations/guests exact. Add durable public diagnostic242 cases =22
forms × (W7/D15 offset cells), bare M, ordering bits clear, rd17 sentinel,13
boundaries each, aligned/contained/crossing with fresh repeated traces. Derive
all expectations first and retain a validated wrong-granule4 DIVERGE control.
Re-run original twelve A guests and public traces of the entire167-guest corpus
under both configurations, distinguishing output identity from laboratory
agreement. Update live references/book/task and generated GS only after final
profile edits; no new contract/doctrine credit or .14 experiment registration.
If any old guest changes, diagnose/own it before proceeding. Focused checks,
probe/adapter controls/books/hooks and exact field/input/registry identity before
commit/brief0/clean actual census. Qualification completed:242/3146 per repeat
AGREE, wrong-granule control DIVERGE at8, original11 A agreements/290 boundaries
and unchanged width-SC difference. All167 old traces identical before/after;
164 successful, three unchanged named counter/timer failures excluded. Existing
must-diverge-control card/INDEX gains the worked boundary counterexample; all
prior card bytes retained, family30/95032 B under fixed caps. No .14 status or
structured experiment credit. New adapter defect c28c below takes priority over
GC-FENCEI c28d. Focused checks/all six books rc=0; hooks at commit.

### `.13` c28c — keep post-budget reference faults from invalidating evidence (completed, `SEMULITH-P4-0159`)

Owned defect found in c28b's broader public regression, priority-next before
GC-FENCEI. Published adapter run dir-chase (cross_model=true) rc=2, duplicate
fetch delivery at step17 despite complete17-step guest prefix. Same pinned binary/
configuration/ELF with --inst-limit17 gives fresh rc=0, AGREE all17 declared rows.
Adapter requests instructions+2 and parses the whole result before judging its
budget; post-program run-off faults at PC0 repeat without instruction rows and
are mapped to the same next index, so valid in-budget evidence is refused.
Current public A/B raw traces:164 successful byte-identical pairs and three
unchanged process failures (mm-counters,w-notrap,w-timer; absent matched counter/
timer source). These failures earn no agreement/identity-as-success credit.
Twenty-five adapter refusals on successful raw traces include the same tail
shape; do not claim they are all repaired from the single initial reproduction.

Activated on clean0d49d27 after actual census rc=0/brief0. Read roadmap P4,
evidence/CPU boundary contracts, public runner/parser/offline controls, parcel
book and guest records. History75c79af introduced +2 with the adapter;190d16b
added the numeric-cause delivery spelling without changing budget. Initial
repair candidate: use the exact declared architectural-boundary limit, preserving
the entire strict parser/comparator. First measure all167 exact-limit public
runs (two fresh traces) and compare the observed25 tail-refusal set; include
required second-parcel delivery and mixed C. Add a runner-orchestration control
which rejects the old +2 invocation before any production change; retain every
existing missing/duplicate/malformed/failed/stale refusal and mutation control.

Exact-limit diagnostic rc=0: all167 fresh repeated pairs captured,24 of25
old tail refusals become AGREE;125 prior AGREE/14 DIVERGE unchanged. Three
counter/timer process failures remain. The last fault-fetch has an actual
cause1 delivery at boundary2 but adapter refuses: canonical historical insn
"the fetch at 0x40000000 — no word fetched" is not the later <fetch ...>
spelling. Confirmed second adapter vocabulary defect, fix-now within this same
bounded repair. Census of parsed167 expectations finds one historical word-less
spelling and four modern fetch-gap cells; keep exact legacy syntax recognized,
require real fetch-class event/empty writes, reject instruction rows there.
Do not rewrite frozen/canonical records to fit the adapter. Add legacy missing/
wrong-event/row controls first; no claim on unrecorded trap addresses/CSR state.
Raw census includes guest-no-device cross_model=false; normal run must still
refuse it, and its raw comparison earns no runner agreement credit. Root cause
predates current adapter:133e722 carries legacy record;75c79af only recognizes
new spelling. New exact-budget orchestration control is RED rc=1 on old code
(limit3 where declared1); same strict parser and other controls pass before it.

After c28b is committed/clean, audit actual trace/limit semantics and existing
parcel-delivery/negative/stale-trace contracts before choosing the smallest repair.
Own exact budget or bounded-prefix handling with permanent offline controls;
truncated required evidence, in-budget malformed/duplicate records, failed process
and stale output must still refuse. Re-run ordinary/mixed-C/witnessed-fetch-gap
live cases and all adapter controls; assess the whole observed25-tail-refusal
set. Keep intentional timer/counter and width-SC platform differences explicit.
Completed outcome: normal runner149 AGREE/4566 boundaries,14 unchanged
DIVERGE, three process failures plus disabled guest refused. All25 raw tail
cases assessed and now compare completely, including one excluded disabled case;
24 enabled repairs. Both new controls first RED1 then GREEN0; five old mutations
still RED1. Strict parser/core/author/frozen/registry exact; one live reference
prose delta declared. Atomic242 regression/focused/all six books rc=0; hooks next.
Promote existing shorter-trace card/INDEX under fixed caps, previous bytes retained.
No status/structured-experiment/contract credit. Next c28d GC-FENCEI,
SEMULITH-P4-0160, then remaining runtime pairs/freeze. .14 still owns records.

C28b promotes the worked counterexample into the existing must-diverge-control
card/INDEX (same question, no new family member); prior card bytes retained.
Knowledge family30 files/95032 B under fixed30/98304; no cap increase.


### `.13` c28d — observe FENCE.I visibility and ignored fields (completed, `SEMULITH-P4-0160`)

Activated on clean d892571 after brief0/actual census rc=0. Read roadmap P4,
frozen OB-GC-FENCEI/REQ-GC-FENCEI, canonical semantics/decode, existing contract
Execution registry/completeness tests, full state/FlatMemory/request interfaces,
ordering assumption and fence-i/memory book. Authenticate RVI-ZIFENCEI4.1 before
literal derivation; rely only on ISA and laboratory provider contracts/public
reference output, never a reference implementation claim.

Own direct finite field matrix: all4096 funct12 values, five rs1/rd pairs
(0/0,0/31,31/0,31/31,7/13), M/S/U =61440 boundaries. POS canonical zero fields;
NEG nonzero ignored fields execute rather than trap. Observe all GPR/FPR/26 CSR
owners, memory, PC/mode, exact requests/parcels/outcome, seeded reservation, full
TLB/cursor and active wait state. Instruction should cause only two parcel fetches,
PC+4 and one cycle/retirement. Preserve frozen semantics/input/registry records.

Add36 five-boundary programs: 32-bit vs C patched instruction, entry at0/2 mod4,
M/S/U and canonical FENCE.I/nonzero FENCE.I/no-fence coherent control. A halfword
store patches the future instruction, LHU reads it back, then its changed GPR
result proves the fetched bytes. Literal expectations/encodings independently
derived before running; store/readback/parcel extents must be exact. No claim on
arbitrary providers or legal stale pre-FENCE.I implementations. Existing ordering
provider auditor retains its own stale-response controls.

Missing binding must first fail real completeness test rc101. Add bad public
instruction tables for illegal ignored bits, architectural writes, extra requests,
trap, PC and reservation/TLB changes; corrupt each observation family including
wait. Wait entry is gated by the actual WFI word, not a public Sem node; an
actual temporary core condition admitting FENCE.I must fail the wait observation. Disable
the actual request auditor to prove a state-equivalent extra load is caught,
then restore exactly. Add only two registry Execution entries plus existing
fencei-selfmod/fault-selfmod/fencei-reserved companions after proof. Derive coverage,
full independent corpus, make check, focused gates/books; synchronized docs and
commit/brief0/actual census before next slice. Completed: independent literal
61440/36 derivation and direct witnesses rc=0,11 bad tables/16 corrupt captures
reject. Actual request/wait mutations RED101/restored exact; missing-binding
RED101 then two registry entries. Direct61620/123222/123294 requests, companions
17/34 =>pair61637/123256. Registry102/effective100/114; make check167/17/220.
Focused gates/all six books rc=0; hooks next. Next c28e below, then seven runtime
pairs/freeze. .14 still owns statuses/experiments.

### `.13` c29 — discriminate the A-extension execution contract (completed, `SEMULITH-P4-0162`)

Activated on clean bfd11bc after the completed workflow/actual census. Read
REQ-GC-ATOMICS, frozen OB-GC-ATOMICS and dependencies, A semantic forms,
evaluator/public reservation/translation interfaces, existing observers and
atomics book. Own new direct Execution pair plus named existing A guests.
Before executing the CPU, authenticate pinned A/Sv39 sources and derive literal
AMO vectors/words/expectations independently. Cover nine operations at W/D,
all ordering bits, M/S/U, x0 and source/destination aliases; LR/SC success/failure
with full retained-state and exact request/memory observations. Add direct
three-level AMO translation and unreadable/unwritable/A/D/page and physical
failure controls; never claim multicore atomicity from a one-hart request pair.

Require missing-binding RED, wrong public instruction tables and corrupted
captures to fail named observations, plus actual request-auditor/translation
mutations RED and exact restoration. Preserve frozen records, old registry,
core behavior, author/canonical guests and historical receipts. Update worked
book/environment/current coverage, regenerate reports after all profile edits,
run focused gates/make check/all six books, then commit/brief0/actual census.
.14 retains statuses and structured experiments. Follow-up c29a owns the
internal-dependency commentary encountered below before the next runtime pair.

Result: authenticated sources and independent12024 value/state boundaries/992
words before CPU;144 physical-failure plans observed separately. Missing-binding
RED101, then two Execution entries. Direct12168/24336/45840 requests, seven
companions198/396 =>pair12366/24732. Nine wrong tables/14 captures reject;
actual request auditor/Atomic→Load mutations RED101 and restored exact SHA.
make check rc0 Rust167/17/223. Initial scratch Trunc/Sext width-node misuse
corrected to scalar API before runtime RED credit. Registry104/effective102/114;
six remaining pairs/freeze. Core/author/frozen/old102 registry/archives exact.
Next c29a dependency-rationale replacement, then GC-COUNTERS. .14 retains records.

### `.13` c29a — replace obsolete atomic dependency assumptions (completed, `SEMULITH-P4-0163`)

Encountered in c29 interface review: reservation.rs names zalrsc_insts.sail's
internal cancellation/error sites; exec_rv64gc.rs SC commentary and atomics
book also assert internal cancellation behavior. Reproduce relevant completed,
failed and faulting LR/SC cases only through public CLI/declared profile,
then replace maintained explanatory assumptions and annotate relevant old
receipts without rewriting history. Never inspect dependency implementation.
Own source-comment/provenance effects and exact behavior verification separately
after c29 is clean. Local ISA/profile policy, not those assertions, grounds c29.

Activated on clean0bbfc64 after actual census rc=0/brief0. Relevant history:
1c554fc introduced the reservation commentary;495b4b8 ported the SC arm.
Read the declared reservation/deterministic policies, source-auth receipt and
current public adapter. Fresh-run all12 original A guests: require11 AGREE
pairs and separately repeat the known width-policy divergence; a wrong
surviving-SC result must DIVERGE through the same public interface. Replace
only comments/book rationale, including the over-broad specification-only
wording with explicit selected-profile policy. Annotate historical internal
quotations in a live route without editing sealed archive payloads. Prove
all non-comment Rust lines and entire profile/author/registry/frozen/generated/
archives byte-exact, run make check/focused/books/commit/brief0/actual census.
No new contract/status/experiment credit. c29b below follows before GC-COUNTERS.

Evidence-boundary annotation (`2026-10-10`, c29a): the preserved internal
reservation quotations in docs/tasks/archive/P4-SYSTEM-designs.md (A precondition7
and decision4) and docs/tasks/archive/P4-SYSTEM-2.md (.4 slice-c receipt/verification) are
historical observations, not maintained dependency assumptions. Current claims
use declared profile policy and public11/290 paired agreement, named width
DIVERGE22 and wrong surviving-SC DIVERGE39. Archived bytes remain exact.

Result: public.py rc=0; fresh11AGREE/290 pairs plus repeated named divergence,
wrong surviving-SC control rejects. Exact comment-deltas/non-comment Rust lines;
all entire dossiers/reports, generated/author/registry104/frozen/archives exact.
Independent167/5365/10524 unchanged. make check rc=0 Rust167/17/223; focused/
all six books rc=0, hooks next. Effective102/114 and LIVE652/49/P4 12/18 unchanged.
Commit/brief0/actual census, then c29b before GC-COUNTERS; .14 retains records.

### `.13` c29b — replace FP internal-reference rationale (completed, `SEMULITH-P4-0164`)

Encountered in the same scoped exec_rv64gc.rs review: FS-Off commentary names
fdext_control.sail:19 and register-write commentary cites Sail's internal wF.
These are maintained internal dependency assumptions under user §20. Own a
bounded comment/public-evidence repair after c29a is clean: read the relevant
FP-state ISA/profile/book contracts, exercise published FP interfaces and an
adversarial marker, replace those rationales, annotate related historical
receipts without modifying sealed payloads and prove behavior unchanged.
No dependency implementation inspection or pin changes. Priority next, then
GC-COUNTERS and remaining runtime pairs/freeze.

Activated on clean6385f2c after actual census rc=0/brief0. Read full relevant
FP-state clauses/semantics and floating-point book; finish any truncated reads
before changes. Encountered two book sentences asserting Dirty only on actual
value changes, while the current code marks Dirty on every f-register write.
Do not classify from prose alone: independently derive a same-value f-write
and read-only control, exercise public Sail and a temporary direct core test,
restore the direct fixture by SHA, then correct the measured book statement.
Own these diagnostics before any temporary code or artifact is written. Bind
the two comment repairs to pinned machine/F/D ISA and public FP guests plus
wrong expected marker. Preserve all non-comment code and every profile/source/
generated/registry/frozen/archive byte. make check/focused/books/commit workflow
required. c29c below owns additional encountered state-source prose; no feature
pivot or current contract credit.

Diagnosis (target/p4-system-13/c29b/diagnose.py rc=0): independent12-step
same-value f-write witness derived before CPU; temporary direct test observes
unchanged f1 but Dirty after FMV.D.X, and unchanged f1/Clean after FMV.X.D.
Direct file restored SHAab6cdb4698f469a38bbe6da6ca53d6560cfd20733ca232f2804c07577170017a.
Public witness AGREE12 twice identically; wrong Clean expectation DIVERGE10.
Initial diagnostic compared raw CSR storage with an architectural view;
corrected to public privilege::csr_read before credit. Thus the book's two
only-on-value-change sentences are stale, not an evaluator defect. Current
REQ-GC-F detail correction remains owned by c29c. Also replace the same book's
unattributed reference-backend assertion with the actual public-observation
limit; no backend implementation assumption is required for this evidence.

Result: independent/direct/public12 same-value witness and read-only control
confirm selected Dirty rule; wrong Clean expectation DIVERGE10. Public24/927
pairs agree. Exact comment-only code and measured book corrections; entire
profiles/author/generated/registry/frozen/archives unchanged. Historical FP
internal quotation in docs/tasks/archive/P4-SYSTEM-3.md (.7 slice-b Off-gate
receipt) is retained history, not a current dependency assumption. make check
rc=0 Rust167/17/223; focused/all six books rc=0, hooks next. Effective102/114
unchanged. Next c29b1 containment, c29c source prose, c29d book containment.

### `.13` c29b1 — keep development receipts below the fixed ceiling (completed, `SEMULITH-P4-0165`)

C29b receipt approaches the fixed49152B DEV ceiling. Before further units,
measure committed source/whole-entry suffix, use published shard_history.py
with existing target/caps, preserve old sealed rows and exact inverse bytes/
SHA, record a bounded receipt and worked provenance example. No cap increase
or feature deletion. Full focused/book/commit workflow, then c29c.

Activated on cleance3a53b after actual census rc=0/brief0. Read published
shard_history.py interface/partition contract, routes registry and the worked
task-tree book. Measured DEV46505/49152B and CHANGELOG56022/65536B; own
both heads' exact whole-entry suffix partitions (targets30000 and40000B)
before c29c's receipts. Capture committed source/hash/entry census and all
existing shard/manifest/archive hashes; require sharder self-test and dry runs,
then sequential published mutations and exact inverses/order. Append only
new manifest rows, retain all17 prior live rows/210 sealed shards. New head
receipts/navigation must be removable to reconstruct each source exactly.

Encountered book c28a paragraph still presents its then-next AMO question as
live; own a past-tense correction and route to the already completed public
qualification, plus the new measured two-head example. Preserve prior feature
examples and fixed caps. No source/code/profile/frozen/registry/history-payload
changes. Verify focused gates/all six books, commit/brief0/actual census before
c29c; c29d book containment remains queued before runtime features.


Result: prepare.py/partition.py rc=0; self-test12/0, dry-run identities exact.
DEV24=15+9, suffix17800B/shard022618033B; CHANGELOG97=59+38,
suffix16152B/shard022716389B. Inverses reconstruct committed ce3a53b source
DEV46505B/SHA92b5766fb8f41f3e563647aace6e20893e40bb8c02639e728dd1f841e84ca1f5
and CHANGELOG56022B/SHAb451f91d5f4ebb1cbb498fd3dc0166b3044c4af09031a8a23537aaaf967feb93.
Prior17 live rows/210sealed shards exact, append two rows; logical229. Fixed
caps and all core/author/canonical/generated/frozen/registry104 exact; effective
102/114 unchanged. Book AMO historical next question corrected/routed. Focused/
all six books rc=0; hooks next, then c29c after clean workflow/actual census.

### `.13` c29c — qualify state-source rationale and FP policy detail (completed, `SEMULITH-P4-0166`)

Encountered during c29b state reading: live state.sexp prose names internal
accrue_fflags, fdext_control.sail, Fcsr_RM_Illegal and dirty_fd_context. Its
reservation census also calls the selected trap-retention rule the exact
specification set. REQ-GC-F's source_semantics detail says Dirty only when
state actually changes, inconsistent with the current any-f-write rule if
c29b's diagnostic confirms it. Own measured correction of these explanatory
fields after c29b is clean. Preserve actual field/CSR/census/interface and all
frozen obligation bytes; use published gen_state/gen_definition routes and
prove only required source-provenance deltas in generated modules. Check
policy mirrors rather than assuming a frozen statement needs rewriting.
Read any relevant source/record/book dependencies before editing. Priority next,
then GC-COUNTERS and remaining pairs/freeze; containment before fixed caps
would be reached. No dependency implementation inspection or pin change.

Activated on clean4e40a60 after actual census rc=0/brief0. Read the exact
state CSR reset prose/census, current requirement and frozen statement,
privilege::csr_write/flag-accrual policy, c29b direct/public diagnosis and full
FP book. Published state generator pair uses state.sexp, core arith.rs and
state_rv64gc.rs; definition pair uses encoding.sexp/state.sexp and
definition_rv64gc.rs.
Before editing, capture exact proposed text deltas and state-source SHA; run
fresh public identical-write/FP evidence and compare with c29b raw traces.
Change only identified explanatory strings: remove four internal names,
qualify reservation trap retention as selected policy and clarify Dirty for
f-register/explicit FP-CSR writes versus flag accrual. Correct only
REQ-GC-F source_semantics detail after checking the unchanged non-exclusive
statement/frozen mirror. Preserve all field tables, owners, resets, census
presence, requirement associations and frozen bytes.

Both published --check commands must first refuse stale provenance, then
regenerate (never hand-edit outputs). Measure actual generated diff and prove
all executable structure exact. The first stricter hash-only assertion failed:
gen_state.py:801 deliberately carries each census `why` into read-only metadata.
The actual required delta is one state-source hash plus the two selected census
explanations in state_rv64gc.rs, and two hashes in definition_rv64gc.rs. Verify
those exact replacements, not a blanket metadata exclusion. Regenerate GS only after final
profile prose and update book/live receipts. make check, STATE-GEN/DEF-GEN/
SEMANTICS plus focused/all six books and full commit/brief0/actual census.
The scoped live-tree review also encounters a closed numeric-expectation
question retaining a reference-backend ancestry rationale. Own its replacement
here with the already measured exact-rational, hardware and public evidence;
sealed historical quotations stay intact. No new realized checks/status/experiment records. Next c29d book containment,
then GC-COUNTERS and six runtime pairs/freeze.


Completed: prepare/verify rc=0, fresh public24/927 pairs plus identical-write12
exact against c29b; statement/frozen mirror unchanged. Both provenance checks
RED rc=1, published generators rc=0. Exact generated state delta: one source
hash and two census explanations; definition delta: two hashes, all other
bytes exact. Old state SHA6f94e9cfa8fb8aa31daed162f37b22714db1512c6cd252063efcaa3d185a094c
→882483e090230562e4c932f0abd2095ab8b9819c7a4e0223be33069b3695d8e3.
Independent167/5365/10524 unchanged; registry104/effective102/114 unchanged.
make check rc=0 Rust167/17/223; normal STATE-GEN/DEF-GEN/SEMANTICS and
focused/all six books rc=0. Book/environment/GS agree; histories/canonical
inputs/author/frozen/LIVE exact except identified current prose/provenance.
Evidence target/p4-system-13/c29c. Hooks next, then c29d after clean workflow.

### `.13` c28e — remove the obsolete internal-reference rationale (completed, `SEMULITH-P4-0161`)

Activated on clean99369ab after actual census rc=0/brief0. Relevant history:
b5621de introduced the semantics commentary's internal-file quotation; current
book and old .6 Result repeat it. Read generator help and exact encoding/state/
output pair from DEF-GEN, public adapter/expectations and c28d authenticated ISA.
Own comment-only semantic-source edit, matching book replacement and historical
receipt annotation. First run six known fence.i/rewrite guests fresh via published
CLI and a wrong-marker expectation control, preserving pin/config. Before
regeneration require DEF-GEN RED on the provenance drift; parsed semantics must
stay exactly equal. Regenerate only through the existing owner, then prove the
module differs by the source SHA alone. No engine/reference internals or pin edit.
Completed: fresh public six pairs/29 boundaries AGREE rc=0; wrong marker43
DIVERGE at1 rc=1. Comment-only semantic edit, parsed forms exact; stale-provenance
check RED rc=1 before published regeneration. Module changes only old source SHA
048555ac8a792789fb534d37d05c0f099a658f822520689e214265ecd2afcd5c to new
91a6e728d1448d2f440a8672564c5912b6451ed105d87194429ded0f73b75164 twice.
Book replacement and old .6 receipt annotation complete the three identified
locations; no repository-wide audit claim. make check rc=0 Rust167/17/220;
focused/all six books rc=0; hooks next. Commit/brief0/census, then c29 GC-ATOMICS
(SEMULITH-P4-0162), with its own bounded plan before changes.

Encountered during c28d source review: maintained zifencei.sem.sexp commentary
names extensions/Zifencei/zifencei_insts.sail and the fence-i book describes the
reference's internal nop/decoded fields. User §20 requires published boundaries;
these explanatory assertions are no longer a basis for dependency assumptions.
The old .6 Result paragraph repeats the internal-source quote; annotate it with
the public-evidence replacement without rewriting the historical receipt.
Own bounded documentation/provenance repair after c28d is clean: replace them
with the observed public experiment/ISA latitude, preserve exact semantic forms,
regenerate affected provenance using published project tools and prove unchanged
instruction behavior/guest inputs/frozen obligations. No reference implementation
inspection or pin change. Priority-next before remaining runtime pairs; current
c28d derivation excludes these assertions and uses authenticated ISA/local provider.

### `.13` c29d — contain book execution history before further feature witnesses (completed, `SEMULITH-P4-0167`)

Current book family approaches fixed524288B total; six runtime pairs need new
worked feature examples. After c29c, census actual chapter/total bytes and
identify historical execution receipts already duplicated in canonical task
records. Preserve any removed payloads byte-for-byte under tracked repository
history with authenticated inverse/routes; retain every current behavior,
contract, interface, example and user instruction in the book. Replace only
historical verification detail with precise routes/bounded summaries, keeping
all feature documentation complete. Own a bounded source-specific design before
edits, preserve fixed chapter/family caps and gate counts, verify all six books
and exact inverses, commit clean before GC-COUNTERS. No broad rewrite or cap rise.

Activated on clean6addc98 after brief0/actual census rc=0. Source-specific
scope: C, floating-point, contract-v2 and contract-runtime chapters. Census
their actual paragraphs and select only dated execution/count/provenance
receipts; retain all current feature descriptions, worked inputs/results,
interfaces, user commands, limits and controls. If a historical paragraph mixes
receipt and behavior, retain the latter explicitly before removing the receipt.
Capture source bytes/SHA and exact old/new spans before changes. Put removed
payloads unchanged in one bounded task archive with source offsets, replacement
offsets, hashes and direct chapter routes. Reconstruct each full original from
the new chapter plus archived spans and authenticate byte/order/SHA equality.
No includes or relocated rendered content to bypass the book budget.
C29e below owns the separately encountered P0 ancestry rationale after this
containment commit is clean. Measure
the actual tracked book/task families including the new archive, keep all caps
fixed, regenerate the book index, run focused gates/all six books and complete
the commit/brief0/actual census workflow before selecting another slice.

Completed: prepare/apply/verify rc=0,45 exact spans across C20/FP4/v2 11/
runtime10. Chapter106679B→99976B; derived index saves55B more. Actual tracked
book51files/504796B, fixed524288B cap. Finite archive51848B SHA
945d134ef00c5b60e9be115992fc51fe43bd7d96d013f73aa0e306e0be9d85ca.
Its map/unchanged payloads reconstruct every source byte/order/SHA against6addc98;
corrupted payload, wrong offset and omitted-span controls reject. Every old
fenced example/command, table, link and heading retained; only new history
routes added. Other books/code/author/inputs/frozen/registry104/prior archives/
knowledge/LIVE exact; effective102/114 unchanged. Focused/all six books rc=0;
prior Rust167/17/223 applies. Evidence target/p4-system-13/c29d. Hooks next,
then c29d1 stdout byte-count fix, c29e public-evidence repair, GC-COUNTERS.

### `.13` c29d1 — report generated index bytes accurately (completed, `SEMULITH-P4-0168`)

Actual c29d regeneration prints23612 "bytes" while index.md contains24064
UTF-8 bytes. Root gen_book_index.py:178 uses len(content), a character count;
the written content and drift check are correct. Own a bounded stdout-only
repair after c29d is clean: read the generator/checker and book instructions,
measure actual output bytes in a same-volume scratch run, require the old
receipt to fail that assertion, then correct the byte count. Keep generated
index bytes/terms and check-mode behavior exact, use focused BOOK-INDEX and
normal docs/books/commit workflow. No new doctrine arm needed. Priority next,
then c29e and GC-COUNTERS; all c29d cap measurements use stat/encoded bytes.

Activated on clean71285e0 after brief0/actual census rc=0. Read full generator,
BOOK-INDEX control/check routes, and task-tree book receipt instructions. Own
only its success-message size expression: measure the written file with stat,
preserving render/write/check behavior and every output byte. First run the real
CLI to target-local output and reject its size claim against stat (RED), then
correct and prove byte-identical output, correct size/40 terms and quiet check.
Update the book's byte-measurement example and historical c29c/c29d next-action
tense. No new test arm; normal BOOK-INDEX controls plus focused/all six books.
Commit/brief0/actual census before c29e.

Completed: real CLI reports23612 bytes for24064-byte UTF-8 output; probe
RED rc=1. Exact one-expression correction len(content)→out.stat().st_size;
same-input probe GREEN rc=0,24064 bytes/40 terms. Output bytes identical SHA
ac9ff0d07fb058d99938111d5b9c56c89c4baa23e7ab89be408d5bce03f1575b;
quiet --check rc=0. Book byte-count example and historical next-action tense
corrected. All other code/author/canonical/generated/frozen/registry104/archive/
LIVE exact, effective102/114 unchanged. Focused/all six books rc=0, final
BOOK-INDEX/all six books rc=0 after prose spacing; previous Rust167/17/223
applies. Actual book51files/505485B, fixed caps unchanged. Evidence
 target/p4-system-13/c29d1. Hooks next; c29e after clean workflow/actual census.

### `.13` c29e0 — refuse failed or unauthenticated legacy reference runs (completed, `SEMULITH-P4-0169`)

Encountered in c29e prerequisite reading, after clean7e961c8/brief0/actual
census rc=0: run_smoke.py ignores both process return codes and does not remove
previous trace files. It also checks binary presence without authenticating the
existing candidate SHA pins. Own a bounded public-run lifecycle repair before
using this helper as fresh evidence. Read full runner, comparator protocol,
base expectation/config/candidate pins and existing guest-generation probe
integration. Reproduce the failed-process/stale-output false credit through
the real experiment with project-local stubs and cached valid public traces
before editing. No dependency implementation inspection or pin changes.

Require each published run to remove only its prior output, exit successfully
and produce a new nonempty trace; authenticate the two existing binary pins
before the command's comparisons. Refusal is exit2, distinct from a compared
disagreement (exit1). Preserve budgets, trace parsing, expectations, disabled
comparison rules and successful output bytes. Add meaningful offline stub
controls through one new GUEST-GEN arm, after the probe fails on the old
runner. Derive the actual arm total and synchronize LIVE rather than assuming
it. Fresh normal four-guest public smoke, repeated trace
identity and wrong-expectation control; focused/all six books and exact input/
registry/frozen identity. Update live/book receipts and commit clean before
c29e. The .14 knowledge/structured-record sweep already owns the broader
ancestry basis; record scoped routes there rather than duplicate that activity.

Completed: diagnosis.py rc=0 authenticates the actual binaries and proves
three exit7 processes reuse unchanged valid arithmetic traces while every check
prints PASS. Offline probe RED rc=1 on exact old source before repair and with
final controls. New runner requires existing pins, fresh nonempty output and
successful status; probe GREEN rc=0,16 controls/three defective modes rejected.
Public.py/compare-old.py/verify.py rc=0: four programs/34 boundaries,12successful
processes, four Sail repeats; all12 raw outputs and full stdout byte-identical
to isolated exact old source. Temporary wrong x1 expectation returns1, all12
processes successful. No input/pin/budget/parser/core/frozen/registry change;
effective102/114. GUEST148/0, derived653, focused/final BOOK-INDEX/all six books
rc=0; previous Rust167/17/223 applies. LIVE only652→653,6135B unchanged.
Evidence target/p4-system-13/c29e0. Commit then c29e1 containment before c29e.


<!-- END designs -->

## acceptance

<!-- BEGIN acceptance bytes=21861 sha256=93e6755d6f6918800fb4ef6d1c53f3e97cb69320dc108d6ac84ab00c03eb8fb0 -->
- [x] `.13` c29e0 — **ROOT CAUSE**: diagnosis.py rc=0 authenticates
  binary pins and records three actual exit7 calls with old traces unchanged;
  real arithmetic experiment prints all PASS. Runner ignored status, retained
  output and never authenticated pins. Exact old source captured/SHA checked.
- [x] `.13` c29e0 — **ADDRESSED**: offline old-runner RED rc=1 before
  repair and final probe against exact old source; GREEN rc=0 after guard/pin
  repair.16 controls plus ignored-status/stale-output/ignored-pin mutants reject.
  Lifecycle refusal2 distinct from compared failure1; book explains fresh credit.
- [x] `.13` c29e0 — **NO REGRESSION**: public.py/compare-old.py/verify.py
  rc=0: four guests/34 boundaries,12successful calls/four repeats; all12 raw
  files and full stdout equal isolated old source. Wrong x1 expectation rc=1
  with12successful calls. Exact command args/budgets/parser/core/canonical/frozen/
  history, registry104/effective102/114 unchanged. GUEST148/0, derived653;
  focused/final BOOK-INDEX/all six books rc=0; previous Rust167/17/223 applies.
  LIVE count only652→653,6135B under6144; fixed caps unchanged. C29e1 then c29e.
  promotion: declined (existing fresh-evidence discipline; permanent controls, real false-credit reproduction and book retain the repair).

- [x] `.13` c29d1 — **ROOT CAUSE**: probe.py before RED rc=1:
  reported23612=Python characters, actual UTF-8 file24064 bytes/40 terms.
  Root gen_book_index.py:178 uses len(content) in its success receipt; output
  content itself matches the canonical generated index exactly.
- [x] `.13` c29d1 — **ADDRESSED**: probe.py after GREEN rc=0,
  reports24064 bytes from written-file stat; verify.py rc=0 proves exactly
  one expression changed. Before/after/canonical output bytes identical SHA
  ac9ff0d07fb058d99938111d5b9c56c89c4baa23e7ab89be408d5bce03f1575b;
  quiet --check rc=0. Book captures the Unicode measurement and completed
  c29c/c29d receipt tense. No new test/doctrine arm or output-format change.
- [x] `.13` c29d1 — **NO REGRESSION**: verify.py rc=0: all other
  code/author/canonical/generated/frozen/registry104/history/LIVE exact;
  effective102/114 unchanged. Focused/all six books rc=0; final BOOK-INDEX
  and all six books rc=0 after prose spacing. Previous Rust167/17/223 applies;
  fixed caps unchanged, actual book51files/505485B. Next c29e public-evidence
  basis repair, then GC-COUNTERS and remaining six runtime pairs/freeze.
  promotion: declined (existing byte-measurement discipline; real Unicode CLI control and book retain the reporting diagnosis).

- [x] `.13` c29d — **ROOT CAUSE**: census.py/prepare.py rc=0:
  actual tracked book51files/511554B against524288B; four sources106679B.
  Source-specific review identifies45 historical receipt spans; source bytes/
  SHA and exact proposed changes captured before mutation. No feature cap rise.
- [x] `.13` c29d — **ADDRESSED**: archive-and-apply.py/verify.py rc=0:
  C32593→29216, FP14661→13909, v2 31527→30251, runtime27898→26600B;
  net6703B saved plus derived index55B. Finite51848B archive preserves all
  original spans/separators; four full source inverses authenticate byte/order/
  SHA. Corruption/wrong-offset/omitted-span controls refuse. Every old fenced
  example/command/table/link/heading remains; exact historical routes added.
- [x] `.13` c29d — **NO REGRESSION**: verify.py rc=0: all other
  books/code/author/canonical/frozen/registry104/prior archives/history/knowledge/
  LIVE exact, effective102/114 unchanged. Actual book51files/504796B and task
  family including new archive stay below unchanged caps. Focused/all six books
  rc=0; previous Rust167/17/223 applicable. Owned next c29d1 (false byte label),
  c29e (old internal ancestry), then remaining six runtime pairs/freeze.
  promotion: declined (established exact-payload containment; inverse map and byte-authenticated spans remain in the finite routed archive).

- [x] `.13` c29c — **ROOT CAUSE**: prepare.py rc=0 authenticates
  statement/frozen mirror and repeats public24/927 plus identical-write12
  byte-exact. State explanation names internals; F detail restricts Dirty
  unlike the diagnosed any-write rule. Both stale provenance checks rc=1.
- [x] `.13` c29c — **ADDRESSED**: verify.py/check-generated.py rc=0
  prove five exact state prose changes, one F-detail change and unchanged
  parsed structure. Generator hash-only assertion exposed intended census
  metadata emission; exact revised proof permits only one hash/two explanation
  strings in state and two hashes in definition. Book/environment/GS and live
  numeric-evidence rationale synchronized through published interfaces.
- [x] `.13` c29c — **NO REGRESSION**: verify.py rc=0: all other
  code/author/canonical/frozen/history/registry104/LIVE exact, independent
  corpus167/5365/10524 and effective102/114 unchanged. make check rc=0
  Rust167/17/223; STATE-GEN/DEF-GEN/SEMANTICS/focused/all six books rc=0.
  Fixed caps unchanged; .14 keeps statuses/experiments. Next c29d book
  containment before GC-COUNTERS and remaining runtime pairs/freeze.
  promotion: declined (established descriptor derivation; exact metadata/provenance proof and selected policy are retained in the book and task).

- [x] `.13` c29b1 — **ROOT CAUSE**: prepare.py rc=0 measures committed
  DEV46505/49152B and CHANGELOG56022/65536B; exact source SHA and24/97
  entries captured. Dry runs preserve heads/history; sharder self-test12/0
  rc=0. Current book's c28a AMO-next question is already resolved by c28b.
- [x] `.13` c29b1 — **ADDRESSED**: partition.py/verify.py rc=0:
  DEV15kept+9moved17800B, CHANGELOG59kept+38moved16152B; shards0226/
  0227 preserve whole payloads. Removing new receipts/navigation reconstructs
  both exact source bytes/order/SHA. Book worked inverse and past-tense repair.
- [x] `.13` c29b1 — **NO REGRESSION**: verify.py rc=0: prior17manifest
  rows/210sealed shards exact; exactly two appended rows, logical229. Explicit
  new-file census stays below fixed caps. Code/author/canonical/generated/
  frozen/registry104 exact; effective102/114 unchanged, previous Rust167/17/223
  applicable. Focused/all six books rc=0. LIVE652/49/P4 12/18 unchanged;
  next c29c source prose and F policy detail, then c29d book containment.
  promotion: declined (established exact-history partition protocol; source identities and inverse worked example remain in task-tree book).

- [x] `.13` c29b — **ROOT CAUSE**: diagnose.py rc=0 independently derives
  identical-value write, direct probe confirms Dirty/read-only Clean and restores
  source SHA. Public12 repeats AGREE, wrong Clean DIVERGE10. Source-auth rc=0
  confirms implementation-defined unchanged-write rule; old book claims stricter
  behavior and evaluator comments name internals (dd9bc1c history).
- [x] `.13` c29b — **ADDRESSED**: two comment deltas and measured book
  dirty-rule/backend-rationale replacements; exact non-comment code verify.py
  rc=0. Public24/927 pairs AGREE. Historical quotation annotated via live route;
  source-prose/F-detail follow-up owned c29c, containment c29b1/c29d scheduled.
- [x] `.13` c29b — **NO REGRESSION**: verify.py rc=0: entire profiles/
  reports/author/generated/registry104/frozen/archive/knowledge bytes exact;
  independent167/5365/10524 unchanged. make check rc=0 Rust167/17/223; focused/
  all six books rc=0. Effective102/114 and LIVE652/49/P4 12/18 unchanged; .14
  retains statuses/experiments. Next c29b1 exact DEV containment, then c29c.
  promotion: declined (established public-boundary discipline; worked FP book retains the identical-value and wrong-Clean evidence).

- [x] `.13` c29a — **ROOT CAUSE**: scoped history/text census rc=0 identifies
  1c554fc/495b4b8 internal reservation/error/reset rationales and the current
  atomics book repetition. Public.py rc=0:11AGREE/290 repeated, named width
  DIVERGE22 repeated, wrong surviving-SC expected1 DIVERGE39. Local policy,
  not dependency implementation assumptions, supports retained behavior.
- [x] `.13` c29a — **ADDRESSED**: exact declared comment replacements in
  reservation.rs/exec_rv64gc.rs and book; non-comment lines exact (verify.py
  rc=0). Historical internal quotations annotated through live routes, sealed
  payloads preserved. Failed-SC comment distinguishes explicit data from walk
  requests. No semantic-source/generator delta or new behavior.
- [x] `.13` c29a — **NO REGRESSION**: verify.py rc=0: entire profile/guest/
  report, author/generated/registry104/frozen/archive/knowledge bytes exact;
  independent167/5365/10524 corpus unchanged. make check rc=0 Rust167/17/223;
  focused/all six books rc=0. Effective102/114 and LIVE652/49/P4 12/18 unchanged.
  Next c29b FP rationale, then GC-COUNTERS. .14 owns statuses/experiments.
  promotion: declined (established public-boundary policy; worked atomics book retains the control and finite evidence limits).

- [x] `.13` c29 — **ROOT CAUSE**: completeness control rc=101 names missing
  CHK-GC-ATOMICS-POS. Authenticated A56889B/SHAafbd8def and Sv39186455B/
  SHAd5186efc; independent author/assembler rc=0 validates12024 boundaries and
  992 words before CPU. Original corpus alone lacks full request/state observer.
- [x] `.13` c29 — **ADDRESSED**: direct rc=0:12168 boundaries/24336 parcels/
  45840 requests; literal values/aliases/order/modes/LRSC plus six bad leaf and
  two physical refusal paths. Nine wrong tables/14 captures reject. Actual
  request/permission mutations RED101 then restored exact SHA; missing pair
  binds via two Execution entries. Seven companions198/396 =>pair12366/24732.
- [x] `.13` c29 — **NO REGRESSION**: verify.py rc=0: old102 registry entries,
  core/author/generated/canonical/frozen/archives exact; independent full167/
  5365/10524 corpus unchanged. Effective102/114, six pairs/freeze; Rust167/17/
  223, focused gates/all six books rc=0. LIVE652/49/P4 12/18 unchanged. .14 owns
  statuses/structured records. Next c29a obsolete internal rationale, owned
  priority-next; c29 excludes those assumptions.
  promotion: declined (established direct-observer discipline; worked atomics book and refusing controls retain diagnosis and finite limits).

- [x] `.13` c28e — **ROOT CAUSE**: scoped text/history census rc=0:
  b5621de introduced the internal-file quotation; maintained semantics/book and
  old .6 Result repeat it. User §20 requires public dependency boundaries.
  Fresh public six guests/29 boundaries AGREE rc=0, wrong marker43 DIVERGE
  at1 rc=1; ISA4.1 source already authenticated in c28d. These observations
  support execution of the named words/markers, not a dependency implementation.
- [x] `.13` c28e — **ADDRESSED**: parsed semantic forms exactly equal,
  scoped prose replacement and historical receipt annotation. Stale-provenance
  check RED rc=1, published generator rc=0. verify.py rc=0: generated module
  differs only by two occurrences of the source SHA048555ac→91a6e728.
  Current semantic/book explanations use public evidence; three known locations
  handled, no repository-wide census claim.
- [x] `.13` c28e — **NO REGRESSION**: verify.py rc=0: all canonical
  profile/guest/frozen/registry102/core evaluator/author/archives exact; only
  declared semantic commentary/generated SHA delta. Independent167/5365/10524
  corpus exact. make check rc=0 Rust167/17/220; DEF-GEN/SEMANTICS/focused/all
  six books rc=0; hooks next. Effective100/114 and LIVE652/49/P4 12/18 unchanged.
  Next c29 GC-ATOMICS; .14 owns statuses/experiments.
  promotion: declined (established public-boundary policy; worked visibility book retains scoped evidence and provenance limits).

- [x] `.13` c28d — **ROOT CAUSE**: completeness rc=101, missing
  CHK-GC-FENCEI-POS. Authenticated4.1 source32380 B/SHA4026de34713f4b898595eb4a17bb58176a0e2905196705a904d3d8fab4432a91
  permits coherent nop and requires ignored fields. Existing corpus alone is
  not the direct full-state/request observer. Initial diagnostic's source-label
  assertion corrected to existing full locator, no author change. Obsolete
  internal-reference rationale owned c28e; excluded from derivation.
- [x] `.13` c28d — **ADDRESSED**: independent61440 states/36 programs
  rc=0 before CPU execution; direct61620/123222/123294 requests rc=0. Full
  state/reservation/TLB cursor/wait and exact requests. Eleven bad tables/16
  corrupt captures reject. Actual request-disabled extra-Load admission and
  WFI condition admitting FENCE.I RED rc=101; both restored exact SHA. Two
  Execution entries bind canonical/nonzero/coherent controls plus companions17/34.
- [x] `.13` c28d — **NO REGRESSION**: verify.py rc=0: prior100 registry
  entries, core/author/generated/canonical/frozen/archives exact; independent
  full167/5365/10524 corpus unchanged. Pair61637/123256; effective100/114,
  seven runtime pairs/freeze. make check rc=0 Rust167/17/220; focused gates/all
  six books rc=0; hooks next. LIVE652/49/P4 12/18 unchanged; .14 statuses/
  experiments remain. Next c28e boundary-rationale cleanup before runtime pairs.
  promotion: declined (established direct-auditor discipline; worked visibility book and refusing controls retain diagnosis and finite limits).

- [x] `.13` c28c — **ROOT CAUSE**: public dir-chase rc=2 with complete17
  rows plus two post-budget fetch deliveries; exact17 AGREE. History75c79af
  introduced +2,190d16b retained it. Exact-limit167 diagnostic rc=0;24/25 tail
  refusals resolve, fault-fetch actual event refused due legacy syntax from
  133e722. Parsed census one legacy/four modern fetch-gap cells. New permanent
  budget control RED rc=1 (limit3 vs1), legacy control RED rc=1 (missing step0).
- [x] `.13` c28c — **ADDRESSED**: probe rc=0 with exact budget and
  exact legacy syntax; strict parser byte-identical. Five previous mutations
  rc=1. New duplicate/malformed/truncated/interior-gap/write-waiver controls
  refuse. Real runner census rc=0:149 AGREE/4566 boundaries with fresh identical
  pairs,14 unchanged differences, three named process failures and disabled
  guest refused. All25 raw tail cases compare completely; only24 enabled.
  Existing shorter-trace knowledge card/INDEX promoted with old bytes retained.
- [x] `.13` c28c — **NO REGRESSION**: verify.py rc=0; all125 prior
  agreements/14 differences preserved; pinned source/binary/config/core/author/
  frozen/registry100/archives exact. Prior112 base/348 GC canonical inputs exact
  except declared live reference prose. Independent167/5365/10524 corpus exact;
  atomic242/3146 paired regression rc=0. GUEST147/focused/all six books rc=0;
  hooks next. Effective98/114 and LIVE652/49/P4 12/18 unchanged, previous Rust
  167/17/217 applies. Next c28d GC-FENCEI; .14 statuses/experiments unchanged.

- [x] `.13` c28b — **ROOT CAUSE**: baseline public reproduction DIVERGE
  at8, repeated13 rows; old durable probe rc=2 on contained AMO. Scalar MAG4
  permits completion despite AccessFault; validated variants isolate parameter,
  history859e5cc carried it. Old800000fe witness crosses16 B and cannot
  distinguish. Primary A12.1.4/public schema0..12/ISA strings checked; no upstream
  or CPU defect. Separate post-budget adapter defect owned c28c priority-next.
- [x] `.13` c28b — **ADDRESSED**: public probe rc=0 after scalar4→0,
  242 cases/3146 boundaries per repetition, all22 forms/W7/D15 offset cells,
  fresh successful byte-identical pairs and literal PC/word/read-backs. Validated
  restored-MAG4 control DIVERGE at8 with rd0/cause0/tval0/data2a00. All
  expectations derived before execution. Existing knowledge card/INDEX promoted.
- [x] `.13` c28b — **NO REGRESSION**: verify.py rc=0: only declared
  scalar/reference-prose deltas;112 base/348 GC inputs, core/author/frozen/prior
  registry/archives exact otherwise. Independent corpus167/5365/10524 exact;
  original A11AGREE/290 plus named width-SC difference. All167 raw traces
  identical:164 successful and three unchanged counter/timer failures excluded.
  Adapter controls/focused gates/all six books rc=0; hooks next. Registry100/
  effective98/114 and LIVE652/49/P4 12/18 unchanged; previous Rust167/17/217.
  c28c owns all25 observed tail refusals before GC-FENCEI c28d.

- [x] `.13` c28a — **ROOT CAUSE**: census rc=0: DEV47951/49152 B,
 1201 B room; source SHA2566d0ccb9383365685023d20543138f1e47735360257fe1fb9fe9560e91ecb70c3.
  Prospective published target30000 partitions23 entries into16 kept/7 moved,
  exact18245 B suffix; family17 files/173677 B before new shard.
- [x] `.13` c28a — **ADDRESSED**: sharder rc=0,12 controls/0 fail;
  shard0225=18478 B, live partition29706 B. verify.py rc=0 removes only new
  receipt/footer, reconstructs exact committed47951 B/source SHA in original
  entry order. Suffix SHA2cd85b0620a097a68dcb3d4c33384949601b1b06c2e7fb94ba4f7fb207fa5852;
  shard SHA9917a51413d8946b9059b36bd489321ea33f11c45651f94e5e497039998ee33f.
- [x] `.13` c28a — **NO REGRESSION**: verify.py rc=0; earlier16 manifest
  rows/210 archived shards/sealed descriptor/object exact, all code/canonical/
  author/generated/frozen/prior archives exact, registry100/effective98/114.
  Explicit new-file/cap census; focused gates/all six books rc=0; hooks next.
  LIVE652 arms/49 chapters/P4 12/18 unchanged. No Rust changes; prior167/17/217.
  promotion: declined (established lossless partition; authenticated shard and worked task-tree book retain proof).
  Next c28b public AMO granule qualification, result pending; GC-FENCEI follows.

- [x] `.13` c27 — **ROOT CAUSE**: completeness test rc=101 on missing
  CHK-ATOMIC-MISALIGN-POS before registration. Authenticated A/machine sources
  and frozen contract choose LR5 vs SC/AMO7 before translation. Live gate owner
  note from618b7d2e still says23/SSTC pending although c13 closed; generated GS
  repeats that prose. Initial W-store expected request ignored explicit trunc32;
  inspected canonical Sem rule, corrected to low44332211 (bytes were correct).
- [x] `.13` c27 — **ADDRESSED**: independent literal derivation rc=0,
  176 words/8896 boundaries/17792 parcels; actual direct fixtures rc=0 with48
  aligned programs/8800 fault cases,17888 requests, listed state/reservation.
  Seven wrong effects/thirteen captures reject. Disabled request auditor and
  actual LR wrong-cause/bypassed-alignment controls rc=101, named CSR/extra-root-
  Walk failures; core/observer restored exactly. One stale gate open-note replaced
  with derived-coverage pointer; registry binds two Execution entries.
- [x] `.13` c27 — **NO REGRESSION**: verify.py rc=0: prior98 bindings,
  all112 base/348 GC canonical/guest inputs exact except one declared gate prose
  delta; core/author/generated/frozen/archives and all prior witnesses exact.
  Independent full167/5365/10524 corpus; companions63/126 =>pair8959/17918.
  make check rc=0 Rust167/17/217. Registry100/effective98/114; eight pairs/freeze.
  Focused gates/all six books rc=0; hooks next. LIVE unchanged652/49/P4 12/18.
  promotion: declined (direct refusing controls and worked memory book retain the policy, diagnosis and finite limits).
  Next c28a exact DEV sharding before c28b GC-FENCEI; .14 owns statuses/experiments.

- [x] `.13` c26b — **ROOT CAUSE**: baseline help rc=1 advertises obsolete
  variable-only command (13266aa vs ac07ff8 recorded act). Three allocators
  inherit host temp; controls on safe on-volume caller temp rc=1: cadence11/4,
  boundary14/1, act6/2. Baseline act6/1 misclassifies legitimate prior ledger
  entries as a new red-suite write. Live decision alias calls expired exception
  current; primary fulfillment says all three green on76882c8/expired Oct8.
- [x] `.13` c26b — **ADDRESSED**: explicit owner-derived test temp/nested
  TMPDIR, three guidance controls, recorded-act help, corrected live alias,
  synthetic prior ledger and exact no-write comparison. Hostile caller and
  direct alternate-cwd helpers15/0,15/0,8/0 rc=0; no fixture directories left.
- [x] `.13` c26b — **NO REGRESSION**: verify.py rc=0; normal pre-push/act
  exact and cadence production exact except declared help. Real approval ledger/
  fulfillment, CPU/canonical/98 registry/frozen/archive bytes exact; effective
  96/114 unchanged. Helper tests are unregistered; LIVE652 arms/49 chapters/
  P4 12/18 unchanged. Focused gates/all six books rc=0; hooks next. No real
  project push or exceptional approval.
  promotion: declined (established policy; public tests and provenance book retain the diagnosis and verification limits).

- [x] `.13` c26a — **ROOT CAUSE**: fixed task ceiling131072 B; current123960
  leaves7112 B. Census rc=0: six completed spans81532 B, archive8 already59436 B;
  combined140968 cannot fit even without wrappers. Original5eaef2a SHA256
  efd367b86309c45a53ddf736352135e18ea56171f1669d43c43941626c7fb4ac.
- [x] `.13` c26a — **ADDRESSED**: partition.py/verify.py rc=0. New archive9
  holds83418 B including81532 exact ordered payload bytes with six SHA/length
  markers. Live partition45205 B before new receipt. Extract each payload and
  remove only new routes/ownership to reconstruct exact123960 B committed
  source/hash. Earlier archive parts and retained source segments remain exact.
- [x] `.13` c26a — **NO REGRESSION**: verify.py rc=0: all prior code/canonical/
  author/98 registry entries/generated/frozen/archive bytes exact; effective
  96/114 unchanged, nine pairs/freeze. All task parts under fixed131072 B; new
  file census included explicitly. Book retains source/inverse worked example.
  Focused gates/all six books rc=0; hooks next. LIVE unchanged652 arms/49 chapters/P4 12/18.
  No Rust change; previous make check167/17/214 remains applicable. promotion:
  declined (established byte-preserving archive protocol; source and payload
  identities retained in archive9/tree/book). c26b owns stale push-help repair.


<!-- END acceptance -->

## verification

<!-- BEGIN verification bytes=4532 sha256=c89af5b364f5e0289fdb7bb54c0a29af3fa684b03d426c26bbc143e4c871a8c3 -->
## Verification Log

Prior rows: [archive/P4-SYSTEM-9.md](archive/P4-SYSTEM-9.md#verification).

| Date | Leaf | Checks | Result |
| --- | --- | --- | --- |
| `2026-10-10` | `.13` c29e0 | real stale-trace false PASS; offline RED1→GREEN0/16 controls/three bad lifecycles; public4/34/all12 old-source raw/stdout exact; wrong expected1; protected inputs/caps | effective102/114 unchanged; GUEST148/0/derived653; focused/final BOOK-INDEX/all six books rc=0; hooks next |
| `2026-10-10` | `.13` c29d1 | real CLI reporting RED1→GREEN0; exact single-expression delta; output SHA/40 terms/quiet check exact; protected inputs/caps | effective102/114 unchanged; focused/final BOOK-INDEX/all six books rc=0; hooks next |
| `2026-10-10` | `.13` c29d |45 exact spans/four full source inverses; corruption/offset/omission refused; all original code/commands/tables/links/headings retained; fixed family caps | book504796B; registry104/effective102/114 unchanged; focused/all six books rc=0; hooks next |
| `2026-10-10` | `.13` c29c | public24/927 plus identical-write12 exact; provenance RED1; exact five prose/one detail/three hashes/two metadata strings; full corpus and protected bytes | effective102/114 unchanged; Rust167/17/223; generators/SEMANTICS/focused/all six books rc=0; hooks next |
| `2026-10-10` | `.13` c29b1 | sharder12/0; two exact source inverses/order/SHA; prior17live/210sealed history exact; fixed new-file census/core/input identity | logical229 rows; effective102/114 unchanged; focused/all six books rc=0; hooks next |
| `2026-10-10` | `.13` c29b | independent/direct/public12; wrong Clean DIVERGE10; public24/927 repeated; exact comments/non-comment/input identity; full167 corpus | effective102/114 unchanged; Rust167/17/223; focused/all six books rc=0; hooks next |
| `2026-10-10` | `.13` c29a | public11/290 repeated; named width difference repeated; wrong SC DIVERGE39; exact comment/non-comment/dossier identity and full167 corpus | effective102/114 unchanged; Rust167/17/223; focused/all six books rc=0; hooks next |
| `2026-10-10` | `.13` c29 | independent12024/992 words; nine wrong tables/14 captures; request/permission/missing-binding RED101 restored; old102/core/inputs exact; full167 corpus | direct12168/24336/45840 requests, pair12366/24732; effective102/114; Rust167/17/223; focused/all six books rc0; hooks next |
| `2026-10-10` | `.13` c28e | public6/29 repeated, wrong marker DIVERGE1; semantic forms exact; provenance RED1 then two-SHA-only regeneration; profile/core/registry identity | effective100/114 unchanged; Rust167/17/220; DEF-GEN/SEMANTICS/focused/all six books rc=0; hooks next |
| `2026-10-10` | `.13` c28d | independent61440/36;11 bad tables/16 captures; request/wait/missing-binding RED101 restored; prior100/core/inputs exact; full167 corpus | direct61620/123222, pair61637/123256; effective100/114; Rust167/17/220; focused/all six books rc=0; hooks next |
| `2026-10-10` | `.13` c28c | budget/legacy RED1→GREEN0; five mutations reject;149AGREE/4566,14 prior differences, three failures/one disabled refused; atomic242 regression; strict parser/input/author/registry identity | effective98/114 unchanged; GUEST147/focused/all six books rc=0; hooks next |
| `2026-10-10` | `.13` c28b | public242/3146 repeated; restored granule DIVERGE; original A11AGREE/one named difference;164 successful old traces exact/three failures excluded; scalar/input/corpus/registry identity | effective98/114 unchanged; adapter controls/focused/all six books rc=0; hooks next |
| `2026-10-10` | `.13` c28a | sharder12/0; seven whole entries18245 B; exact47951 B source inverse/SHA; prior16 rows/sealed history/code/inputs exact; explicit caps | registry100/effective98/114 unchanged; focused/all six books rc=0; hooks next |
| `2026-10-10` | `.13` c27 | independent176 words/8896 states; seven wrong effects/thirteen captures; auditor/LR/missing-binding RED101 and restored; full167 corpus/core/prior98 exact except gate note | direct8896/17792, pair8959/17918; effective98/114; Rust167/17/217; focused/all six books rc=0; hooks next |
| `2026-10-10` | `.13` c26b | helper controls RED rc=1; hostile/direct15/0,15/0,8/0 rc=0; normal paths/real ledger/CPU/registry/frozen exact | effective96/114 and registered652 unchanged; focused/all six books rc=0; hooks next |
| `2026-10-10` | `.13` c26a | six payloads81532 B; exact source inverse123960 B/SHA; earlier parts/code/input/registry/frozen exact; explicit caps/new-file census | effective96/114 unchanged; focused/all six books rc=0; hooks next |


<!-- END verification -->

## commits

<!-- BEGIN commits bytes=2656 sha256=ee4902c09479ac89d0afad237f35fbcf51292b4682da355603af324e14b20eaa -->
## Commit Log

Prior rows: [archive/P4-SYSTEM-9.md](archive/P4-SYSTEM-9.md#commits).

| Leaf | Subject | Next |
| --- | --- | --- |
| `.13` c29e0 | `SEMULITH-P4-0169 (leaf P4-SYSTEM.13): refuse false scalar-reference credit` | c29e1 containment, c29e overview repair, then GC-COUNTERS |
| `.13` c29d1 | `SEMULITH-P4-0168 (leaf P4-SYSTEM.13): report generated index bytes accurately` | c29e public ancestry basis, then GC-COUNTERS |
| `.13` c29d | `SEMULITH-P4-0167 (leaf P4-SYSTEM.13): retain book verification history under fixed caps` | c29d1 byte-count receipt, c29e public ancestry basis, then GC-COUNTERS |
| `.13` c29c | `SEMULITH-P4-0166 (leaf P4-SYSTEM.13): align state-source rationale and FP policy detail` | c29d book containment, then GC-COUNTERS |
| `.13` c29b1 | `SEMULITH-P4-0165 (leaf P4-SYSTEM.13): retain exact history under fixed caps` | c29c source prose/F detail, then c29d book containment |
| `.13` c29b | `SEMULITH-P4-0164 (leaf P4-SYSTEM.13): ground FP-state claims in public evidence` | c29b1 DEV containment, c29c prose/provenance, c29d book containment |
| `.13` c29a | `SEMULITH-P4-0163 (leaf P4-SYSTEM.13): ground atomic rationale in public evidence` | c29b FP rationale, then GC-COUNTERS/six pairs/freeze |
| `.13` c29 | `SEMULITH-P4-0162 (leaf P4-SYSTEM.13): discriminate atomic execution and faults` | c29a public atomic rationale, then six runtime pairs/freeze |
| `.13` c28e | `SEMULITH-P4-0161 (leaf P4-SYSTEM.13): ground fence reference claims in public evidence` | c29 GC-ATOMICS, remaining runtime pairs/freeze |
| `.13` c28d | `SEMULITH-P4-0160 (leaf P4-SYSTEM.13): observe FENCE.I visibility and ignored fields` | c28e obsolete dependency rationale, then seven runtime pairs/freeze |
| `.13` c28c | `SEMULITH-P4-0159 (leaf P4-SYSTEM.13): bound public reference runs` | c28d GC-FENCEI, remaining runtime pairs/freeze |
| `.13` c28b | `SEMULITH-P4-0158 (leaf P4-SYSTEM.13): qualify the public AMO granule boundary` | c28c post-budget adapter repair, then GC-FENCEI c28d |
| `.13` c28a | `SEMULITH-P4-0157 (leaf P4-SYSTEM.13): retain bounded development receipts` | c28b public AMO granule qualification, then GC-FENCEI |
| `.13` c27 | `SEMULITH-P4-0156 (leaf P4-SYSTEM.13): observe atomic alignment before translation` | c28a DEV containment, c28b GC-FENCEI, remaining runtime pairs/freeze |
| `.13` c26b | `SEMULITH-P4-0155 (leaf P4-SYSTEM.13): align push guidance and local self-tests` | c27 ATOMIC-MISALIGN, remaining runtime pairs/freeze |
| `.13` c26a | `SEMULITH-P4-0154 (leaf P4-SYSTEM.13): preserve completed task receipts under fixed caps` | c26b stale exceptional-push help, then remaining runtime pairs |


<!-- END commits -->

## changelog

<!-- BEGIN changelog bytes=5543 sha256=ce570fdb3e3ba821ebb2b2b85e600e6caa619ae783d286d67114fb2eca86cc6c -->
## Changelog

- `2026-10-10`: `.13` c29e0 (SEMULITH-P4-0169): reject failed/stale/
  unauthenticated scalar reference evidence; real false PASS reproduced then
  offline16/three bad lifecycles discriminate. Public4/34/all12 raw/stdout exact,
  wrong expectation1; effective102/114 unchanged. Own c29e1 containment then c29e.

- `2026-10-10`: `.13` c29d1 (SEMULITH-P4-0168): written-file stat
  replaces character count in generator stdout; real Unicode RED1→GREEN0,
  exact output SHA/40 terms/quiet check. Book measurement and receipt tense
  synchronized; effective102/114 unchanged. C29e next after clean workflow.

- `2026-10-10`: `.13` c29d (SEMULITH-P4-0167): contain45 historical
  book receipt spans with exact full source inverses; all current code/commands/
  tables/links/headings retained. Finite51848B archive, book504796B under fixed
  caps,102/114 unchanged. Next owned c29d1 reporting fix and c29e ancestry repair.

- `2026-10-10`: `.13` c29c (SEMULITH-P4-0166): exact state prose/F
  detail repair, frozen statement preserved; provenance RED1 then published
  generation. Three source hashes/two census explanations only; public24/927
  and identical-write12 exact,102/114 unchanged. Book/environment/GS sync;
  c29d book containment next.

- `2026-10-10`: `.13` c29b1 (SEMULITH-P4-0165): whole DEV9 and
  CHANGELOG38 entry suffixes to frozen0226/0227; exact source inverses/order/
  SHA, old history preserved. Logical229, caps and102/114 unchanged. Book
  historical AMO question corrected and current c29c/c29d next actions retained.

- `2026-10-10`: `.13` c29b (SEMULITH-P4-0164): replace FP internal
  rationale and correct stale book dirty rule via independent/direct/public12,
  wrong Clean DIVERGE10, public24/927 pairs. Code comments only, inputs/frozen/
  registry exact,102/114 unchanged. C29b1/c29c/c29d own containment and source
  prose before remaining six runtime pairs/freeze.

- `2026-10-10`: `.13` c29a (SEMULITH-P4-0163): replace internal
  atomic source rationales with ISA/profile/public evidence.11AGREE/290 pairs,
  named width DIVERGE22 repeated; wrong SC code DIVERGE39. Comments only,
  non-comment code/dossiers/registry/frozen/archive bytes exact.102/114 unchanged;
  c29b owns encountered FP rationales before GC-COUNTERS.

- `2026-10-10`: `.13` c29 (SEMULITH-P4-0162): bind GC-ATOMICS with
  direct12168/24336/45840, pair12366/24732; literal arithmetic/aliases/LRSC,
  translated page/physical faults and full state. Independent12024/992 words,
  wrong tables/captures and actual request/permission controls refuse/restored.
  Registry104/effective102/114; c29a owns encountered internal rationale next.

- `2026-10-10`: `.13` c28e (SEMULITH-P4-0161): replace internal-source
  FENCE.I rationale with ISA/public observations, annotate old receipt. Six
  pairs/29 boundaries agree, wrong marker diverges. Semantic forms exact,
  only generated source SHA twice changes after provenance RED1. Coverage
  100/114 unchanged; c29 GC-ATOMICS next.

- `2026-10-10`: `.13` c28d (SEMULITH-P4-0160): bind GC-FENCEI
  field/mode and patched W/C visibility, full state/TLB cursor/wait/requests.
  Direct61620/123222, pair61637/123256; wrong tables/captures and actual
  request/wait controls reject/restored. Registry102/effective100/114; Rust220.
  c28e owns obsolete dependency rationale before remaining seven runtime pairs.

- `2026-10-10`: `.13` c28c (SEMULITH-P4-0159): exact public Sail
  budget/legacy fetch vocabulary; strict parser retained.149AGREE/4566 with
  fresh pairs,14 unchanged differences, three failures/one disabled refused.
  All25 raw tail cases assessed;24 enabled. New controls RED1→GREEN0, five
  prior mutations reject. Effective98/114 unchanged; c28d GC-FENCEI next.

- `2026-10-10`: `.13` c28b (SEMULITH-P4-0158): scalar MAG4→0;
  public242/3146 pairs and wrong-granule control. Prior164 successful traces
  identical/three named failures excluded; original A outcome unchanged. Exact
  core/inputs/registry100/effective98/114 otherwise; knowledge-card promotion.
  Own post-budget adapter refusal c28c before GC-FENCEI c28d.

- `2026-10-10`: `.13` c28a (SEMULITH-P4-0157): exact seven-entry DEV
  suffix18245 B to shard0225; source inverse47951 B/SHA, prior history exact,
  fixed caps and runtime100/effective98/114 unchanged. c28b owns public Sail
  contained-AMO granule qualification before GC-FENCEI; result pending.

- `2026-10-10`: `.13` c27 (SEMULITH-P4-0156): bind ATOMIC-MISALIGN with
  direct8896/17792 and full state/request/reservation observations; pair8959/17918.
  Wrong effects/captures and actual auditor/LR controls reject/restored; prior98/
  core/inputs exact except one repaired gate owner note. Effective98/114;
  c28a DEV containment before c28b GC-FENCEI; .14 statuses/experiments unchanged.

- `2026-10-10`: `.13` c26b (SEMULITH-P4-0155): recorded-act refusal help,
  fulfilled-exception pointer, on-volume helper fixtures and literal nonempty
  approval history with exact red-suite no-write control. Helpers15/0,15/0,8/0;
  real ledger/enforcement/CPU/registry/frozen exact, effective96/114 unchanged.
  Next c27 ATOMIC-MISALIGN after clean workflow/census.

- `2026-10-10`: `.13` c26a (SEMULITH-P4-0154): move six whole completed
  receipt spans81532 B to archive9; extract/authenticate and reconstruct exact
  source123960 B/SHA. Earlier archives/code/canonical/runtime/frozen exact;
  effective96/114 unchanged. c26b owns stale push guidance before runtime work.

Prior entries: [archive/P4-SYSTEM-9.md](archive/P4-SYSTEM-9.md#changelog).

<!-- END changelog -->
