# P4-SYSTEM — archive part 7

Completed receipts moved byte-verbatim from the active tree. Earlier parts
remain linked from [`P4-SYSTEM-6.md`](P4-SYSTEM-6.md).

## Completed designs

Slice b begins with a bounded **b1 state-inventory repair** (SEMULITH-P4-0106),
committed before the declarations/realizations. Own the stale pre-bind header,
mtime comment and census answer/consequence in state.sexp; regenerate its Rust
mirror through gen_state, prove executable definitions unchanged, run make check
and STATE-GEN, remove only the resolved .13 G-STATE opening, regenerate GS and
update the book. No snapshot implementation or new contract credit in b1.

b1 dependent-manifest repair (same owner): the first commit hook reproduced
DEF-GEN self-test 55 pass / 1 fail. Direct gen_definition --check reports only
the old state.sexp source pin in the definition module's OWN-03 manifest. The
state descriptor is an input to both generators; regenerate definition_rv64gc.rs
through its owner, assert everything except the two state-identity occurrences
byte-identical, and rerun make check plus DEF-GEN before retrying the commit.

**b2 registry evidence mechanism** (SEMULITH-P4-0107): scope-check support is a
prerequisite of declaring the scope replacements born realized. Introduce an
explicit guest/scope evidence type, preserve all existing guest bindings, and
realize only OB-GC-COMPOSITION's existing pair first. A tracked read-only Python
predicate checks parsed profile/encoding selection; its negative check mutates
copies (missing/extra extensions, wrong base/width and partial composition), and
normal Rust tests run both entries plus disabled-predicate controls. Unknown ids
refuse. No rewrite of frozen records, no new runtime guarantee, no freeze.
After this mechanism commits, extend scope realizations and then bind new v2
declarations with their actual evidence. This dependency ordering refines the
original bounded-unit plan; the final acceptance is unchanged.

**b3 structured scope pairs** (SEMULITH-P4-0108): own extension dependency
closure, privilege source revisions, CSR-name/storage/view inventory, no-PMP,
no-H and scope/composed-name equality. Validate canonical parsed declarations;
each negative case changes a fresh in-memory copy and must fail for its named
reason. Retain b2 controls and old guest bindings. Extend the normal registry
coverage guard, run make check and the gate/freeze controls; no new contract
record or freeze in this slice. Before appending notes beyond their fixed bound,
use shard_history.py on DEV_NOTES (and CHANGELOG if useful) under this same
slice's ownership, retain verbatim reconstruction and frozen shard manifest.

**b4 toolchain identity defect / ABI prerequisite** (SEMULITH-P4-0109): while
reviewing the ABI contract, build_c_guest.sh's public flow was found to probe
RISC-V capability and print versions but not enforce the compiler/linker versions
the pinned toolchain decision requires. Own reproduction through an on-volume
wrapper reporting another version while forwarding the installed tool, preserve
existing artifacts, and fix the script if the control confirms acceptance.
Priority: now, before crediting ABI/toolchain scope. Require explicit overrides
to refuse mismatched identities and validate selected tools before output writes;
retain successful pinned-tool builds and add permanent public-interface controls.
Read the guest-toolchain decision, script callers and its existing GUEST-GEN
coverage before editing. No install or off-repository write. This is a bounded
contract-enforcement repair within .13, not a roadmap pivot.
Include the ACT4 caller's duplicated discovery in this same repair: diagnose its
missing-candidate and shell-builtin lookup paths through public tool selection,
then use one pinned resolver for both callers. Own isolated, on-volume fake-tool
controls for rejection before output writes, explicit override refusal, backend
failure and successful selection, alongside a real pinned C build. No external
test-suite or submodule implementation inspection is needed.

**b5 remaining selection pairs** (SEMULITH-P4-0110): own ABI, SBI, RVWMO and
privileged-instruction scope predicates and their independent violating copies.
Validate LP64D/64-bit FP selection and the pinned psABI source; SBI 2.0's real
M-mode firmware route and source identity; one-hart RVWMO/A selection; and the
exact four privileged forms in both profile scope and resolved encoding.
These are scope selections, not evidence of an installed compiler in offline CI,
implemented firmware, Linux boot or exploration of every weak-memory outcome.
Retain all prior guest bindings and frozen records byte-exact. Run all new pairs
in normal Rust tests, then update GS/ENVIRONMENT/dossier/book and the live pointer.
Read canonical decisions, sources, state and the prior scope implementation first;
rehash the locally acquired psABI/SBI public artifacts before fixing their expected
identities. If unavailable, record the narrower declaration-only provenance honestly.

**c1 versioned current guarantees** (SEMULITH-P4-0111): replace frozen
OB-FP-DEFER with OB-GC-FP-QUALIFIED-V2, both historical route records with
OB-GC-DEFINITION-V2, and OB-FAULT-PRIORITY with OB-GC-FAULT-PRIORITY-V2.
Add three v2 members/four explicit supersessions without changing any frozen
record or membership. Bind six checks immediately: qualification/definition
selection predicates with independent negative copies, and existing priority
guests reviewed at instruction/expectation level. Scope predicates validate the
qualified backend identity and current generated route; FP numeric behavior
retains its distinct vector/guest evidence. Qualification and closing records,
Cargo pins, current composition, generated mirrors and public priority table
are the relevant sources. Repair stale current profile header/comments; retain
historical decision statements and requirement mirrors with explicit notes naming
their v2 replacement. No new decision-id mirror family or backend implementation
inspection. Run Rust, schema/freeze and owner generation checks; regenerate GS
only after final dossier edits. Expected effective census: 52 obligations/104
checks, 48 realized, v2 open; re-derive rather than hard-code acceptance.

**Capacity finding / c2 ownership** (SEMULITH-P4-0112): `wc -c` after c1's
three additions reports contract-obligations.sexp at 63,014 bytes against the
fixed 65,536-byte authored-part ceiling: 2,522 bytes remain before five complete
boundary assumptions. Priority: next, before adding them; never raise the cap.
Own a lossless version-partition of this catalogue and the minimal explicit
catalogue-include support needed by its real consumers. Census raw readers first
(record loader, freeze checker, registry tests and any others); use one expansion
owner, validate relative paths/cycles/missing parts, preserve every frozen record
byte and expanded order, and keep aggregate storage bounded without a duplicate
materialized catalogue. Treat this as a dedicated, fully checked slice; do not
mix the boundary declarations into the format migration. Review the existing
schema/loader contracts and book before choosing its final representation.
The consumer census finds dictionary readers already using records_sexp; raw
exceptions are CONTRACT-FREEZE, the Rust registry declaration test, legacy record
conversion, and gate-report scratch-copy controls. Select explicit
`include-obligations` forms with repository-root-relative paths, handled by one
record_catalog expansion owner; records_sexp delegates to it. Share validated
top-level token spans through sexp rather than line-matching directive-looking
prose. Keep root header/current v2 lines in place; move v0/v1 contiguous bytes to
two authored parts and assert expanded bytes equal the pre-partition catalogue.
Validate included records as well as directive shape, add part-schema routing,
flatten scratch copies through the owner, and let registry tests read the same
expanded stream at runtime. Exercise missing/cyclic/duplicate/escaping/malformed
includes, literal strings/comments, relocation and schema failures. Extend the
existing RECORD-SCHEMA controls; run focused checks and full CI at this format
milestone. No boundary record is added by c2 and G-CONTRACT credit stays 48/104.
Reader defect reproduced during that census: a valid top-level `(comment ...)`
plus a real obligation yields schema errors=[] but records_sexp.load refuses
"not a record form". Target receipt: c2/comment-reproduction.log. Impact: the
record reader rejects the one format's reserved annotations. Own and fix now in
c2 by skipping reserved top-level annotation forms in the record mapping path;
schema validation retains annotation-shape ownership. Add a permanent control.
Signoff defect discovered by `rg` of GS-REPORT.md line 32: its G-CONTRACT gap
still says four frozen statements require replacements, despite c1's explicit
supersessions. Root cause: the maintained open-axis statement in gate.sexp lines
25–26 was not updated; the report generator correctly copied it. Own and repair
now in c2 as a small review-surface correction: retain the real remaining five
boundary assumptions, unrealized checks and open freeze, without extra credit.
Regenerate GS through its owner after that canonical correction.

**c3 typed address-unit pair** (SEMULITH-P4-0113): the existing normal-suite
coverage guard requires every post-v0 record to be born realized. Retain it;
add the five assumptions one paired slice at a time, starting with physical
8-bit-byte addresses. Add OB-GC-ENV-ADDRESS-UNITS and its v2 membership, with a
named typed-boundary evidence variant and direct Rust fixture; no new check
credit from an unrelated guest or configuration predicate. Review env.rs,
FlatMemory/ScriptedEnv, exec_rv64gc translation and the generated state interface.
Positive evidence uses nonzero byte offsets above 32 bits, exact FlatMemory
responses/stores and a hand-scripted three-level Sv39 LB step: distinct VA/PA,
physical walk addresses, two parcel requests and a physical data request.
Negative providers deliberately scale a data address to word units, truncate a
walk address to 32 bits, or substitute a VA for a physical fetch. The same real
engine must report the exact typed ContractViolation::ResponseMismatch through
ModelError, with no delivered trap or destination write. Include a legitimate
access-failure control to preserve the target-failure distinction. Bind both
entries in the normal registry; update its exact coverage guard without weakening
post-v0 coverage. Preserve every old record/entry and frozen membership byte.
Read-only schema/freeze, Rust checks and gate controls are required; GS/book/live
docs must state 53 effective obligations/106 checks, 50 realized if re-derived.
Four assumptions remain afterward; v2 stays open. No production boundary behavior
or guest-observation vocabulary changes in this slice.

**c4a response-validation prerequisite** (SEMULITH-P4-0114): before declaring
widths/attributes, diagnose wrong response kinds and over-wide Load values through
the real GC boundary. The interface promises exact raw-width responses, and the
contract requires violating providers to use the typed violation family. Current
call-site census: word/parcel fetch, ordinary load/store, LR/SC/AMO and page-walk
reads in exec.rs, exec_rv64gc.rs and translation.rs. Generate an on-volume public
API probe, record before/after outcomes, then own any confirmed mismatch now.
If reproduced, put response validation in one env.rs owner: preserve legitimate
Target failures and valid answers, reject wrong success kinds and nonzero bits
above a requested Load width with named ContractViolation variants. Route every
CPU boundary crossing through it, including the legacy scalar path; do not copy
the validator into handlers or fixtures. Read core boundary/outcome tests and
standalone engine-probe consumers before changing interfaces. Add independent
request/response matrix, width-edge, real-engine and target-failure controls.
Keep existing enums' cases intact and add typed variants; no guest semantics,
valid traces, frozen records or check credit change. Retain 50/106 and v2 open;
width/attribute assumption with its direct registry pair follows in c4b. Run Rust,
focused fixture/generator/gate checks and full CI for the shared boundary change;
synchronize live docs and book, then commit this prerequisite separately.
Confirmed reproduction, target/p4-system-13/c4a/before.log:
wrong-kind -> Failed(InvalidDescription "environment answered a FetchParcel
with a non-parcel response"); over-wide-byte (Load 0x1ff for B) -> Executed,
x6=0xffffffffffffffff; legitimate AccessFault -> Executed, mcause=5.
Impact: malformed provider responses either enter the wrong model-error family
or silently pass as usable data. Root cause: handlers only match response kinds
locally and ordinary loads accept all u64 values without a shared width check.
Priority now, owned c4a; both defects must be fixed and the probe rerun before
claiming response-contract evidence. Existing valid provider behavior must stay
exact. The planned independent permanent controls will retain this reproduction.

Associated documentation drift found by rg: ENVIRONMENT's compressed-supply
paragraph still said 48 realized checks after c3 added its direct address pair;
the later address section and generated GS already report 50/106. Root cause:
c3's summary paragraph was not updated with the new registry pair. Owned/fixed
in c4a: correct that paragraph through its canonical document and regenerate GS.
The actual registry, records and credit are unchanged.

**c4b typed data-access pair** (SEMULITH-P4-0115): with c4a committed and
the tree clean, add OB-GC-ENV-DATA-ACCESS to open v2, born realized. Review
core env/request_checked, FlatMemory/ScriptedEnv, real GC load/store paths,
OB-ENDIAN/OB-ADDRESS-SPACE and this book's contract chapter. Declare B/H/W/D
raw data widths, little-endian executable main memory without MMIO, exact
whole-request success/failure and low-width stores; alignment-before-translation
remains the CPU's existing priority guarantee. Positive fixtures independently
pin byte arrays, raw values and low-width store neighbors for all widths; actual
hand-encoded loads/stores must use those requests. Probe aligned region-straddling
failures for every width and confirm no partial store or destination effect.
Negative providers supply over-wide B/H/W values and wrong success kinds to the
real engine, preserving typed violations and no delivered trap. A direct fixture
auditor compares exact expected response values, detects reversed-byte answers
and reports a distinct typed ResponseValueMismatch; CPU shape validation cannot
infer a provider's storage contents. This is finite provider evidence, not a
universal memory-content oracle. Reuse the shared shape validator, no duplicated
kind/width logic. Add BoundaryCheck variants and both registry entries, retain
all 50 prior entries/frozen records and the post-v0 guard (expected 52/108).
Run Rust, schema/freeze, direct positive/negative and disabled-auditor controls,
gate self-tests and books. Synchronize live docs/GS; three assumptions remain,
v2 stays open. No guest vocabulary, production memory map or cap change.
Initial registry test caught an incorrect fixture expectation: SB's request data
is 0x34 after the CPU narrows source 0x1234, not 0x1234. The generated store
effect and exec Store path explain the actual trace. Corrected the literal
negative expectation; added direct high-input-bit store checks so provider
truncation is independently tested rather than hidden by CPU operand narrowing.

**c5 typed event-delivery pair** (SEMULITH-P4-0116): c4b committed clean;
review interrupts/timekeeping, the step head, v1's source/time assumptions and
book interrupt/contract chapters. Declare event positioning separately from
source availability: this lab still supplies no external IRQ source, reservation
invalidation or host-time input. Pending/wake evaluation occurs at the step head
before any parcel request; one virtual tick follows each completed/trapping/
waiting boundary, never a memory callback. Add an explicit typed location guard
in env.rs, reusable by adapters: BetweenInstructions is permitted as a location
(not authority for a source), DuringRequest is EventDuringRequest. No event payload,
queue, source, guest observation or production scheduler is introduced. This
opt-in adapter guard cannot discover hidden mutation by arbitrary host code.
Positive direct fixtures execute a timer threshold between two ADDIs and a WFI
idle/wake sequence, checking literal counters, unfetched EPC and parcel counts.
Negative providers attempt delivery inside each request kind, must reach exact
typed violations through the real GC engine, and preserve PC/destination/trap
state. Disable the phase guard in a permanent control: the same negative fixture
must fail because the bad schedule escapes. Preserve all 52 prior entries and
frozen bytes; add one open-v2 assumption/pair and retain the post-v0 guard,
expected 54/110. Run Rust, schema/freeze, gate controls and books; synchronize
live docs/GS. Ordering/reset remain afterward; v2 stays open.

**c6 typed ordering pair** (SEMULITH-P4-0117): c5 committed clean. Reviewed
FlatMemory, ordinary/atomic request paths, FENCE/FENCE.I and the ordering/visibility
book chapters. Rehashed pinned RVWMO (121633 bytes, SHA-256
6126b0e31c33f3ff492308c14f264e9f86ae0d30dfeddaa6f834191c0ab37d91) and
Zifencei (32380 bytes, SHA-256
4026de34713f4b898595eb4a17bb58176a0e2905196705a904d3d8fab4432a91),
then read global/program order, load-value/atomicity/progress axioms and local
instruction visibility. Declare one-hart synchronous request order, latest
preceding stores and always-coherent fetch as this laboratory's selected RVWMO
realization, not exploration of all weak outcomes. No host buffering, concurrent
agent or delayed completion. Add one v2 assumption/pair born realized (56/112).
Positive direct fixtures use hand-encoded store/load/overlap/AMO ordering and
code rewrite with/without FENCE.I, with an independent exact conversation over
real memory and actual CPU steps. Negative providers acknowledge discarded
stores or serve a stale parcel cache; the independent fixture auditor reports
ResponseValueMismatch before a wrong result is consumed. Factor the existing
c4b value comparison into one fixture owner shared with c6, leaving production
shape validation unchanged. Disabled-value-auditor controls must lose every
negative fixture; valid fixtures must still pass. Preserve all 54 prior entries,
all frozen bytes and born-realized guard. Run Rust, schema/freeze, focused gate
controls and books; sync live docs/GS and commit. Cold reset remains afterward.
Initial disabled-auditor control reached the later AMO, whose store value
became 1 after the stale load; ScriptedEnv then correctly rejected its request
against the independent expected 0x1122aa45. This sibling check masked the
specific value-auditor bypass. Reduce the discarded-store observation to the
first two instructions (acknowledged store, bad load); keep the full five-step
conversation for positive ordering. The disabled value guard must then let the
bad load execute, without weakening request-order validation.

**c7b typed full-cold-reset pair** (SEMULITH-P4-0119): after c7a's prerequisite;
review state.sexp's full census/reset rows, generated state/reset API, CSR views,
TLB/reservation/wait public contracts, memory construction and book state inventory.
Add the final missing boundary assumption to open v2, born realized (58/114).
Cold reset reconstructs x/pc/mode, f-file, all 26 CSR owners and seven views,
memory/image, TLB including FIFO position, reservation and ACTIVE wait state.
Pin independent literal reset values from canonical rows: misa
0x800000000014112d, mstatus 0xa00000000, other raw CSR owners zero; computed
STIP is 1 at time=stimecmp=0, but enables are zero. Warm reset is not supported.
Positive fixture dirties every owner, calls the real state reset and reconstructs
memory, then validates each owner before executing a hand-encoded ADDI. Negative
fixtures retain one owner class, each CSR/register where meaningful, and a TLB
with invalid entries but nonzero FIFO cursor. A fixture-only cold-state auditor
returns typed ResetStateMismatch with a named component before the first fetch;
no production CPU reset behavior is changed. Disable that auditor in controls:
every bad reset must escape the negative fixture. Source/read receipts and exact
prior entries/frozen bytes retained. Run Rust, schema/freeze, gate controls/books
and full CI for completion of the boundary-assumption milestone. V2 remains open
for 28 runtime pairs; no freeze or CPU-SYSTEM closure until all checks pass.

c7b execution readiness: c7a committed as 8676d88, tree clean/message zero,
actual unsandboxed census handoff OK. Re-read pinned RVP-MACHINE 2.1.4 reset
paragraph, canonical CSR reset rows and generated reset/public state accessors,
Tlb/Reservation/HartState contracts, FlatMemory construction, registry/guards,
CPU_ENVIRONMENT and the privilege/interrupt/contract book sections. Own the
fixture-only ResetStateMismatch diagnostic with component and optional index.
Independently literal all raw CSR reset values and seven view values; never
use ArchitecturalState::zeroed_at as the expected-value oracle. Negative cases
cover each nonconstant integer, each FP/CSR owner, PC/mode, TLB content and
cursor-only retention, valid and cleared-but-retained reservation, wait, and
every image/outside-image byte. Each case must fail before fetch without target
effects; disabling the cold-state auditor must lose every case. Full CI at this
boundary-assumption milestone; frozen parts/prior registry entries byte-exact.
Canonical reset review also found mip's old statement "Nothing pending at reset"
contradicts its live computed STIP at time=stimecmp=0 (already reproduced in c7a).
Correct that prose to distinguish zero raw storage from computed pending state,
regenerate fingerprints and retain the actual reset values unchanged in c7b.
The seven-view witness respects FP access gating: cold FS=Off makes architectural
fcsr access illegal, while its internal composition is zero. Check that refusal
and composition, rather than changing FS or demanding a legal cold fcsr read.
Anchor the fixture's private-owner equality witnesses with literal field checks
in the owning core tests: default/new TLB entries and FIFO=0, reservation
address/width=0 and invalid. Comparing two constructors alone would not independently
pin those values if the shared constructor changed. No public API expansion.

**c7a supervisor interrupt-view prerequisite** (SEMULITH-P4-0118): reset
review found a suspicious omission in privilege.rs: csr_read masks sip/sie to
their declared fields but does not intersect mideleg; csr_write likewise needs
inspection before any change. The pinned RVP-MACHINE 2.1.1.9 explicitly makes
nondelegated sip/sie bits read-only zero. Supervisor artifact rehashed to
d5186efc3ead1c1f693ac2b16aeccdcab95d990264f49b559252d2dc413a651a;
machine delegation paragraph read from the pinned artifact. Own/reproduce now
through public CSR read/write and real instruction APIs before committing the
full cold-reset assumption. If confirmed, repair the shared CSR-view owner,
not per-instruction behavior or interrupt arbitration; preserve underlying mip/mie
and computed STIP behavior. Independently test delegation/read/write/clear/revoke
and source visibility, all three S bits and both M/S access modes. Existing
canonical state/semantics and independent expectation author must stay aligned;
inspect those owners before edits, update book/live docs and actual guest
expectations only from the corrected specified rule. No silent expectation
rewrites. Run Rust, focused generator/corpus checks and full CI for this
architectural behavior repair. This defect takes priority over c7b, is owned here,
and must be resolved and verified before reset evidence is claimed.

Confirmed through the public API before repair: `cargo build -p semulith-core`
and the on-volume `target/p4-system-13/c7/supervisor-view-probe.rs` give
undelegated sie/sip = 0x222/0x222; writes of zero erase mie and SSIP despite
mideleg=0 (mie=0, computed mip=0x220). Delegating 0x222 is the valid control.
RVP-MACHINE artifact SHA-256 reverified
b63fe33517fef2dabe53cdbc45b05d656bf808eebf83f0af5a4ab74549617fea.
Root cause: both shared architectural read/write paths omit the dynamic
delegation mask; the independent Python author repeats the omission. Correct
both owners, annotate canonical view rules and add separate read/write bypass
mutants for sip/sie to GUEST-GEN before claiming repaired evidence. Inspect all
existing sip/sie guest uses; update only specification-derived differences.
Contract credits remain 56/112 in this prerequisite.
Initial new controls exposed a second author defect in the same view owner:
sip read a separate zero-initialized dictionary slot rather than mip storage.
The existing guests did not observe that old value. Remove the fake view slots
and compute pending from the one mip owner. The first actual S-mode CSR fixture
instead took a legitimate higher-M interrupt before fetch: isolate view semantics
by clearing pending for sie instructions and clearing enables for sip instructions;
do not change arbitration to make a test execute.

No implementation-language, backend, board or observation-vocabulary expansion
is authorized by this plan. Static checks establish declared scope and its
consistency, not universal instruction correctness. Runtime checks retain their
finite corpus and boundary scope.

## Completed acceptance

`P4-SYSTEM.13` slice (c7b) (`2026-10-10`, `SEMULITH-P4-0119`):

- [x] **ROOT CAUSE** — git show 8676d88:profiles/rv64gc-lab-v0/contract.sexp:
  ten v2 members, full GC reset undeclared. Read pinned machine reset paragraph
  and canonical rows; public reset reconstructs 26 raw owners and hidden state.
  mip's "Nothing pending" prose contradicts computed STIP=1; distinguish raw
  storage/live view without changing reset values. Cold fcsr read is FS-gated.
- [x] **ADDRESSED** — cargo test -p semulith-verify contract_boundary_rv64gc:
  4 passed / 0 failed. Literal state/image checks precede actual ADDI; 128
  independently poisoned cases yield exact typed ResetStateMismatch, no fetch
  or target/state/memory effects. Disabled auditor loses every case. make check
  rc=0 includes the registry's positive/negative pair and literal private TLB/
  reservation cold-field tests. Empty FIFO=1 and cleared reservation discriminate.
- [x] **NO REGRESSION** — make check rc=0: 161 core / 17 DSP / 198 verify.
  PRIOR-EVIDENCE: all 56 old entries, root prefix, frozen parts/memberships
  byte-exact. RECORD-SCHEMA: ok (20 files); CONTRACT-FREEZE: 3 versions,
  0 findings; gate_report --self-test: 17 pass / 0 fail. Full make ci rc=0:
  all five legs green (check, gate, bench, smoke-bench, book).
- [x] **LOCKSTEP** — git diff --check rc=0; G-CONTRACT 58/114 with
  57 effective obligations, eleven open-v2 members. State/definition fingerprints,
  canonical reset prose, book, ENVIRONMENT, dossier, GS and live pointer sync.
  LIVE_STATUS reviewed unchanged: P4 12/18, 639 arms, 45 chapters. All five
  boundary pairs complete; 28 runtime pairs remain, then freeze. promotion:
  declined (canonical record, fixture/core controls and book retain it).

`P4-SYSTEM.13` slice (c7a) (`2026-10-09`, `SEMULITH-P4-0118`):

- [x] **ROOT CAUSE** — cargo build -p semulith-core; public CSR probe before:
  undelegated sie/sip=0x222, zero writes erase mie/SSIP. Rehash/read pinned
  RVP-MACHINE 2.1.1.9 (digest above); shared read/write paths miss mideleg.
  New author controls expose separate sip dictionary owner as a second defect.
- [x] **ADDRESSED** — cargo test -p semulith-core privilege::tests::interrupt_views:
  3 passed / 0 failed, eight masks in M/S and 192 real CSR instruction steps.
  Same public probe after: sie/sip=0, zero writes preserve mie/mip=0x222;
  delegated positive remains 0x222. python3 scripts/probe_gc_privilege_author.py
  rc=0: 42 historical records byte-identical and five mode-matrix guests / 140
  steps. Independent rule/owner corrections and five bypass mutations owned.
  The first S-mode fixture took a legitimate higher-M interrupt; isolate pending/
  enables in test setup, preserving arbitration. No instruction-specific fix.
- [x] **CONTROL DIAGNOSTIC** — make ci first run rc=2, GUEST-GEN 134/1:
  sip-owner mutant fails at the re-delegation control before its later mask-2
  read, but that chained assertion had no diagnostic. Split read assertions
  and name sip's owner/delegation failure at every read control. Keep the
  strict gate's reason check; rerun full CI rather than accept wrong-reason RED.
- [x] **NO REGRESSION** — make check rc=0: 160 core / 17 DSP / 197 verify,
  all existing guest records untouched. Frozen obligation records, memberships
  and registry entries unchanged. Initial GUEST-GEN overlaps initial author
  failure (134/1); final make ci rc=0, all five legs green; GUEST-GEN 135/0.
- [x] **LOCKSTEP** — git diff --check rc=0; canonical state/semantics,
  generated state/definition fingerprints, book and toolbox updated. LIVE_STATUS
  snapshot: P4 12/18, 45 chapters; arms 639 (+5, repository-derived). Contract
  56/112 unchanged, cold reset c7b and 28 runtime pairs remain; v2 open.
  promotion: declined (canonical rule, permanent controls and book retain it).

`P4-SYSTEM.13` slice (c6) (`2026-10-09`, `SEMULITH-P4-0117`):

- [x] **ROOT CAUSE** — git show 7bc9485:profiles/rv64gc-lab-v0/contract.sexp:
  nine v2 members, ordering not yet declared. Rehashed/read RVWMO and Zifencei
  pinned artifacts (digests in design above); reviewed request completion,
  overlap/AMO and coherent-fetch owners. Selected realization stays one-hart.
- [x] **ADDRESSED** — cargo test -p semulith-verify contract_checks_rv64gc:
  4 passed / 0 failed. New pair runs literal five-instruction store/load/overlap/
  AMO conversations for all aq/rl bits and two warmed-code rewrites. Three bad
  providers return exact typed value mismatches without wrong destination effects
  or target traps. cargo test -p semulith-verify contract_boundary_rv64gc:
  3 passed. Reduced bypass observation to first bad load after a sibling request
  guard initially caught its later AMO; disabled value auditing now loses all
  three cases without weakening request-order checks. Shared fixture value owner.
- [x] **NO REGRESSION** — make check rc=0: 157 core / 17 DSP / 197 verify.
  PRIOR-EVIDENCE: all 54 entries, frozen parts/memberships and old root prefix
  byte-exact. RECORD-SCHEMA: ok (20 files); CONTRACT-FREEZE: 3 versions,
  0 findings; gate_report --self-test: 17 pass / 0 fail; make book rc=0.
  Post-v0 born-realized guard retained, now 56 checks; no guest changes.
- [x] **LOCKSTEP** — G-CONTRACT: 56/112, 56 effective obligations,
  ten open-v2 members. Book/ENVIRONMENT/dossier/gate/GS and toolbox/live
  pointer synchronized. LIVE_STATUS reviewed unchanged: P4 12/18, 634 arms,
  45 chapters. Cold reset and 28 runtime pairs remain; v2/CPU-SYSTEM incomplete.
  promotion: declined (canonical assumption, focused controls and book retain it).

`P4-SYSTEM.13` slice (c5) (`2026-10-09`, `SEMULITH-P4-0116`):

- [x] **ROOT CAUSE** — git show 9ea649e:profiles/rv64gc-lab-v0/contract.sexp:
  eight v2 members, no event-positioning record. Reviewed v1's no-source/time
  rules, interrupt/timekeeping owners and step head before parcel requests.
  Source permission and delivery location remain separate; no event source added.
- [x] **ADDRESSED** — cargo test -p semulith-verify contract_checks_rv64gc:
  4 passed / 0 failed, including the new direct pair. Actual timer threshold
  between ADDIs and WFI/two idle boundaries/wake retain literal cycle/retire/fetch
  counts and unfetched EPC. Five in-request attempts produce exact typed
  EventDuringRequest errors with PC/mode/destination/trap/counters/memory intact.
  cargo test -p semulith-verify contract_boundary_rv64gc: 2 passed; disabled location guard loses
  all five negative cases. Opt-in limit explicitly retained.
- [x] **NO REGRESSION** — make check rc=0: 157 core / 17 DSP / 196 verify.
  PRIOR-EVIDENCE: all 52 entries, frozen parts/memberships and old root prefix
  byte-exact. RECORD-SCHEMA: ok (20 files); CONTRACT-FREEZE: 3 versions,
  0 findings; gate_report --self-test: 17 pass / 0 fail; make book rc=0.
  Post-v0 born-realized guard retained, now 54 checks; no guest changes.
- [x] **LOCKSTEP** — G-CONTRACT: 54/110, 55 effective obligations,
  nine open-v2 members. Book/ENVIRONMENT/dossier/gate/GS and toolbox/live
  pointer synchronized. LIVE_STATUS reviewed unchanged: P4 12/18, 634 arms,
  45 chapters. Ordering/reset remain; v2 and CPU-SYSTEM incomplete.
  promotion: declined (canonical assumption, guard, fixtures and book retain it).

`P4-SYSTEM.13` slice (c4b) (`2026-10-09`, `SEMULITH-P4-0115`):

- [x] **ROOT CAUSE** — git show f5d96bf:profiles/rv64gc-lab-v0/contract.sexp:
  seven v2 members, address units declared but no data-width/attribute
  assumption. Existing shared shape validator cannot infer stored byte content.
  Reviewed env, FlatMemory, store narrowing/translation and canonical priority.
  Initial registry test failed for the fixture's wrong SB data expectation;
  actual request data=52, not 4660. Corrected the literal; engine behavior valid.
- [x] **ADDRESSED** — make check rc=0: new pair runs through the normal
  registry. Literal B/H/W/D values and direct/CPU stores; executable bytes and
  eight whole-region failure cases preserve destination/memory. Twelve negative
  providers produce exact typed errors without target traps. Auditor valid-content
  control passes; disabling it lets reversed bytes execute, detected by the
  permanent test. CPU validation retains its shared shape-only owner.
- [x] **NO REGRESSION** — make check rc=0: 157 core / 17 DSP / 195 verify.
  PRIOR-EVIDENCE: all 50 entries, frozen parts/memberships and old root prefix
  byte-exact. RECORD-SCHEMA: ok (20 files); CONTRACT-FREEZE: 3 versions,
  0 findings. gate_report --self-test: 17 pass / 0 fail; make book rc=0.
  Post-v0 born-realized guard retained, now 52 checks; no guest expectations change.
- [x] **LOCKSTEP** — G-CONTRACT: 52/108, 54 effective obligations,
  eight open-v2 members. Book/ENVIRONMENT/dossier/gate/GS and toolbox/live
  pointer synchronized. LIVE_STATUS reviewed unchanged: P4 12/18, 634 arms,
  45 chapters. Three assumptions remain; v2/CPU-SYSTEM incomplete.
  promotion: declined (canonical assumption, direct fixtures and book retain it).

`P4-SYSTEM.13` slice (c4a) (`2026-10-09`, `SEMULITH-P4-0114`):

- [x] **ROOT CAUSE** — git show adf9218:crates/semulith-core/src/exec_rv64gc.rs:
  line 310 names
  the non-parcel InvalidDescription; lines 526/781/924 issue unchecked Loads.
  Public before.log: wrong FetchParcel answer became
  InvalidDescription; Load B 0x1ff executed with x6=all ones. AccessFault
  control delivered cause 5. Census: 12 raw CPU crossings; local kind matching
  and no raw-load-width validation explain both reproduced defects.
- [x] **ADDRESSED** — cargo test -p semulith-core env::tests: 8 passed,
  0 failed. Same after.log: WrongResponseKind and LoadValueOutOfWidth
  propagate through ModelError::ContractViolation; x6=0, mcause=0. Legitimate
  AccessFault keeps cause 5. One request_checked owner validates all crossings.
  Four permanent tests cover 25 kind combinations, independent width edges,
  exact error passthrough and actual GC/scalar/translation paths.
- [x] **NO REGRESSION** — make check rc=0: 157 core / 17 DSP / 194 verify.
  C engine probe: 18 passed / 0 failed, exact parcel/expansion checks passed.
  CONTRACT-FREEZE: 3 versions, 0 findings; DOSSIER-SCHEMA: 270 checked,
  2 named baseline skips; gate_report --self-test: 17 pass / 0 fail.
  First make ci refused checklist evidence signatures; corrected exact commands
  and results pass TASK-ACCEPTANCE. Final make ci rc=0: all five legs green
  (check, gate, bench, smoke-bench, book).
  No record, membership, registry entry or valid guest expectation changed.
- [x] **LOCKSTEP** — book/P1 context/ENVIRONMENT/dossier/GS, toolbox,
  DEV_NOTES/CHANGELOG and live resume pointer synchronized. G-CONTRACT stays
  50/106, v2 open; c4b owns data widths/attributes with its direct pair.
  LIVE_STATUS reviewed unchanged: P4 12/18, 634 arms, 45 chapters.
  promotion: declined (shared owner, permanent reproduction and book retain it).

`P4-SYSTEM.13` slice (c3) (`2026-10-09`, `SEMULITH-P4-0113`):

- [x] **ROOT CAUSE** — git show 460e4d8: catalog has no GC address-unit
  assumption; normal registry guard requires every post-v0 declaration realized.
  Read env/fixtures/interpreter/translation/state interfaces and boundary closure;
  data widths/events/ordering/reset retain distinct next-slice ownership.
- [x] **ADDRESSED** — cargo test contract_checks_rv64gc: 4 passed / 0 failed.
  One v2 record/pair, explicit Boundary evidence: full-width byte offsets/stores,
  exact six-request Sv39 LB, three deliberately distorted providers each matching
  typed ResponseMismatch through ModelError, no trap or destination effect.
  Legitimate walk access-failure response delivers cause 1 with VA mepc/mtval.
- [x] **NO REGRESSION** — make check rc=0 (153 core, 17 DSP, 194 verify);
  RECORD-SCHEMA: ok (20 files); CONTRACT-FREEZE: ok (3 versions, 0 findings);
  gate_report --self-test: 17 pass / 0 fail. REGISTRY: all 48 prior entries
  byte-exact; FROZEN PARTS: byte-identical to HEAD, old root prefix and frozen
  membership forms exact. make book rc=0. Post-v0 guard retained, now 50 checks.
- [x] **LOCKSTEP** — G-CONTRACT: 106 declared / 50 realized, 53 effective
  obligations. Book/ENVIRONMENT/dossier/gate/GS, toolbox and live pointer synced.
  LIVE_STATUS reviewed unchanged: P4 12/18, 634 registered arms, 45 chapters;
  CPU-SYSTEM incomplete, v2 open. Four boundary assumptions owned next.
  promotion: declined (canonical record, named direct fixture and book retain it).


`P4-SYSTEM.13` slice (c2) (`2026-10-09`, `SEMULITH-P4-0112`):

- [x] **ROOT CAUSE** — wc -c: catalog 63014/65536, only 2522 bytes before
  five complete boundary assumptions. Comment reproduction: schema errors=[],
  R.load refused "not a record form". Consumer census identifies raw freeze,
  conversion, declaration-test and scratch-copy paths; no dependency internals.
- [x] **ADDRESSED** — PARTITION: 63014 expanded bytes exactly preserved;
  58 records unchanged in order. Root/v0/v1: 9003/47168/7009 bytes, fixed caps.
  RECORD-CATALOG-CONTROLS: 31 pass / 0 fail; disabled expansion rc=1 with
  CONTROL-MISSED. Shared owner, original-source schema validation and exact
  frozen-line hashes; annotations map to no records, schema retains their shape.
- [x] **NO REGRESSION** — make check rc=0 (153 core, 17 DSP, 194 verify);
  RECORD-SCHEMA: ok (20 files); CONTRACT-FREEZE: ok (3 versions, 0 findings);
  gate_report --self-test: 17 pass / 0 fail. First make ci: Rust/project doctrines green; signoff box and Knowledge Map
  refused. Both owned doc fixes applied; final make ci rc=0: all legs green
  (check, gate, bench, smoke-bench, book). 58-record JSONL round-trip byte-exact.
- [x] **LOCKSTEP** — book/ENVIRONMENT/dossier, durable include decision, toolbox
  and live pointer synchronized. DERIVED-COUNTS --list: 634 self-test arms, 38
  doctrines, 45 chapters. P4 12/18; G-CONTRACT stays 48/104, v2 open.
  promotion: decision_obligation-catalog-parts and permanent probe retain it.


`P4-SYSTEM.13` slice (c1) (`2026-10-09`, `SEMULITH-P4-0111`):

- [x] **ROOT CAUSE** — git show 23f3e68 contract records: old FP condition,
  resolution/partial stages and no-breakpoint phrase still effective. Public
  RVP-MACHINE Table 7 distinguishes address triggers/environment break;
  c-breakpoint step 4 observes x7=3. Canonical Cargo pins and active qualification
  records confirm the completed backend choice; no dependency internals inspected.
- [x] **ADDRESSED** — three v2 members, four supersessions, six realized checks;
  GC-CONTRACT-SCOPE: CHK-GC-FP-QUALIFIED-V2-NEG holds (5 violating copies refused);
  CHK-GC-DEFINITION-V2-NEG holds (4 violating copies refused), both rc=0.
  Read-only owner generation checks all pass. Priority guests cover competing faults,
  FS-Off and both environment-break spellings. Profile current comments repaired;
  historical decision/requirement statements retained with replacement notes.
- [x] **NO REGRESSION** — make check rc=0 (153 core, 17 DSP, 194 verify);
  RECORD-SCHEMA: ok, 20 files; CONTRACT-FREEZE: ok, 0 findings; gate controls 17/17.
  All previous obligation bytes/frozen memberships and 42 registry entries exact.
  Books and tree/frontier/bounds pass. New census: 58 total, 52 effective, 104
  declared checks, 48 realized. No cap raised or frozen statement rewritten.
- [x] **LOCKSTEP** — GS 48/104, v2 open; ENVIRONMENT/dossier/book/tool catalog
  and live pointer synchronized. Catalog capacity measured 63,014/65,536 bytes;
  c2 owns partition next, before boundary assumptions. LIVE_STATUS unchanged:
  P4 12/18, 629 registered arms, CPU-SYSTEM incomplete eight axes.
  promotion: declined (versioned records, permanent checks and book retain it).

`P4-SYSTEM.13` slice (b5) (`2026-10-09`, `SEMULITH-P4-0110`):

- [x] **ROOT CAUSE** — git show 389b8d7 registry: 34 entries, seven scope
  pairs; ABI/SBI/RVWMO/privileged selection checks absent. Rehash public cache:
  psABI a8d06bdcaa82a6a4567a1904dc27ef1ca1043ebaa1f523558c927a9d72bc23d9;
  SBI 63084f54f382715efb340f46695d0e5cebd98965292d034d1b184b1abd3a682b.
- [x] **ADDRESSED** — GC-CONTRACT-SCOPE: all four new POS/NEG pairs hold;
  16 violating copies refused for specific reasons. All 34 prior entries
  byte-exact, six canonical documents unchanged. Static checks establish choices,
  not an installed compiler, firmware, Linux boot or complete weak-model exploration.
- [x] **NO REGRESSION** — make check rc=0 (core 153, DSP 17, verify 194);
  gate_report --self-test: 17 pass / 0 fail; CONTRACT-FREEZE: ok, 0 findings.
  All eleven scope pairs run and all 39 violating copies discriminate. Books and
  focused tree/frontier/bounds verified; no frozen byte or pin changed. First
  hook refused only GS source digest: stdout diff isolated it to the final dossier
  doc edits. Regenerated GS after those edits; GATE-REPORT focused recheck passes.
- [x] **LOCKSTEP** — generated GS 42/106 realized, v2 open. ENVIRONMENT's
  current summary and stale seven-gap row corrected to the five-topic census;
  dossier/book/tool catalog/live pointer synchronized. LIVE_STATUS reviewed:
  unchanged, P4 12/18, 629 registered arms, CPU-SYSTEM incomplete eight axes.
  promotion: declined (canonical decisions, predicates and book retain it).

`P4-SYSTEM.13` slice (b4) (`2026-10-09`, `SEMULITH-P4-0109`):

- [x] **ROOT CAUSE** — isolated public build reproduction: rc=0, clang/LLD
  99.0.0 accepted and ELF emitted. ACT4 public toolchain() with absent explicit
  compiler raised FileNotFoundError. Logs target/p4-system-13/b4/reproduction.log;
  no original guest artifact touched. Wrapper-root/relative override behavior
  retained and tested from another directory. Host `command` lookup happened to work;
  do not misclassify it as a reproduced host defect.
- [x] **ADDRESSED** — Toolchain probe: 20/20 controls passed. Shared resolver
  rejects wrong/missing explicit tools, validates identities before probe writes,
  cleans unique local probes and returns named refusals through both callers.
  ignore-version rc=1, CONTROL-MISSED for C wrong-clang/wrong-lld/suffix-version.
- [x] **NO REGRESSION** — real build rc=0, ELF before/after SHA-256
  f438ec2182ac57603c35e472942b7fa9de95cccc764bdf831c43288e7b50f437;
  ACT4 parser self-test 7 pass / 0 fail; focused GUEST-GEN and books verified.
  No Rust changed; no installation, off-repository write or suite inspection.
- [x] **LOCKSTEP** — owning decision amended, book/tool catalog and live resume
  pointer synchronized. Two GUEST-GEN arms: total 629, GUEST-GEN 130.
  Contract stays 34/106, v2 open; P4 12/18, CPU-SYSTEM incomplete eight axes.
  promotion: owning decision and book retain the enforcement repair.

`P4-SYSTEM.13` slice (b3) (`2026-10-09`, `SEMULITH-P4-0108`):

- [x] **ROOT CAUSE** — git show 0365bd8:crates/semulith-verify/src/contract_checks_rv64gc.rs
  realizes only one static scope pair. Six structured declarations still have
  no runnable pairs. Read their actual fields and rehash both public privilege
  pages; machine b63fe33517fef2dabe53cdbc45b05d656bf808eebf83f0af5a4ab74549617fea,
  supervisor d5186efc3ead1c1f693ac2b16aeccdcab95d990264f49b559252d2dc413a651a.
- [x] **ADDRESSED** — GC-CONTRACT-SCOPE: all six new POS/NEG pairs hold;
  17 isolated violating copies refused for exact reasons. Joint CSR omission,
  same-count wrong instruction name and valid-but-wrong digest discriminate.
  Existing b2 controls retained; all 20 old guest binding lists exact. Canonical
  input hashes unchanged by the checks. Scope evidence remains selection-only.
- [x] **NO REGRESSION** — make check rc=0 (core 153, DSP 17, verify 194);
  gate_report --self-test: 17 pass / 0 fail; CONTRACT-FREEZE: ok, 0 findings.
  SHARD-FREEZE: ok, 220 frozen rows, exact partition. Sharder reconstruction:
  notes 45=33+12 entries, changelog 86=75+11, byte/order exact. Books,
  tree/frontier/bounds pass; no cap raised or frozen record edited.
- [x] **LOCKSTEP** — GS 34/106 realized, v2 open; registry/coverage guard,
  ENVIRONMENT/dossier/book/tool catalog and live pointer synchronized. New
  immutable shards 0217/0218 preserve older notes/history. LIVE_STATUS reviewed,
  unchanged (P4 12/18, 45 chapters, CPU-SYSTEM incomplete on eight axes).
  promotion: declined (permanent predicates, records and v2 book retain it).

`P4-SYSTEM.13` slice (b2) (`2026-10-09`, `SEMULITH-P4-0107`):

- [x] **ROOT CAUSE** — git show d592759:crates/semulith-verify/src/contract_checks_rv64gc.rs
  binds evidence only through guests. OB-GC-COMPOSITION declares a selection,
  so an unrelated passing instruction run would not realize its POS/NEG pair.
  The slice-a census identified scope predicates as its proper evidence method.
- [x] **ADDRESSED** — GC-CONTRACT-SCOPE: CHK-GC-COMPOSITION-POS holds
  (parsed profile and complete composition); NEG holds (6 violating copies refused).
  Explicit guest/scope registry dispatch runs both. Ignoring profile/fragments
  each returns rc=1 CONTROL-MISSED; unknown id rc=2 UNKNOWN-CHECK. All 20 old
  id/obligation/guest lists compared exact before/after. No live check writes files.
- [x] **NO REGRESSION** — make check rc=0 (core 153, DSP 17, verify 194),
  all 167 guests and scope controls pass. gate_report --self-test: 17 pass / 0 fail;
  CONTRACT-FREEZE: ok, 3 versions / 0 findings. Books and focused tree/frontier/
  bounds pass. Frozen v0/v1 records/pins unchanged, no new runtime guarantee.
- [x] **LOCKSTEP** — GS regenerated: G-CONTRACT 22/106, v2 open; priority wording
  replacement now named among four open corrections. ENVIRONMENT, dossier, v2
  chapter, tool catalog, notes/changelog/live pointer synchronized. LIVE_STATUS
  reviewed, unchanged (P4 12/18, 45 chapters). CPU-SYSTEM incomplete, eight axes.
  promotion: declined (registry, permanent controls and v2 book retain it).

`P4-SYSTEM.13` slice (b1) (`2026-10-09`, `SEMULITH-P4-0106`):

- [x] **ROOT CAUSE** — git show d9eba37:profiles/rv64gc-lab-v0/state.sexp
  consequence listed the .2 snapshot, while generated fields include fregs,
  TLB, reservation and hart_state; translation::Tlb also carries a FIFO cursor.
  The old header still said staged/profile-resolution and external mtime.
- [x] **ADDRESSED** — STATE-GEN: ok, canonical descriptor and generated metadata
  agree. All twelve candidates and complete consequence re-answered, 26 storage
  owners distinguished from 33 CSR names; clock storage and reset/continuation
  distinction explicit. Executable-definition comparison before/after: identical,
  SHA-256 9617e2829fcf7bc425f196af17664cff744c258861ad710675cccf9b8c31f9c8.
  Definition regeneration differs only at two state-source hash occurrences;
  replacing that hash reconstructs the entire prior module exactly.
- [x] **NO REGRESSION** — make check rc=0 (core 153, DSP 17, verify 193),
  all 167 guests and cold re-execution pass. CONTRACT-FREEZE: ok, 3 versions,
  0 findings. STATE-GEN and DEF-GEN: ok after both owner regenerations;
  schema, books, tree/frontier/bounds pass. No executable
  behavior changed; frozen obligation text unchanged.
- [x] **LOCKSTEP** — remove only resolved .13 G-STATE opening, regenerate GS;
  G-STATE still incomplete for .14's requirement statuses, G-CONTRACT 20/106
  open. Dossier/book/live pointer updated. LIVE_STATUS reviewed, unchanged:
  P4 12/18, 45 chapters, CPU-SYSTEM incomplete. Serialization stays .16.
  promotion: declined (canonical descriptor and v2 book retain the inventory).

`P4-SYSTEM.13` slice (a) (`2026-10-09`, `SEMULITH-P4-0105`):

- [x] **ROOT CAUSE** — shared gate_report.contract_measure on the real records:
  55 total, 53 effective, 106 declared checks, 20 realized. Read every statement
  and current registry; table above accounts for all 53 ids exactly once. Pinned
  RVP-MACHINE hash b63fe33517fef2dabe53cdbc45b05d656bf808eebf83f0af5a4ab74549617fea
  matches its source pin; Table 7 and C.EBREAK fixture reproduce
  the additional priority-wording defect, owned for slice b.
- [x] **ADDRESSED** — complete per-record realization plan and five-item boundary
  closure recorded before implementation. Frozen records untouched, no check
  credit added. Static scope, runtime observations and typed boundary controls
  have separate explicit evidence requirements. CONTRACT-FREEZE: ok
  (1 versioned unit(s), 3 version(s), 0 finding(s)). State consequence repair owned.
- [x] **NO REGRESSION** — gate_report --self-test: 17 pass / 0 fail;
  CONTRACT-FREEZE ok, 3 versions / 0 findings. make book rc=0; TREE-CLAIMS,
  FRONTIER-SYNC and README-ROUTING-CLOSURE rc=0. Documentation-only slice.
- [x] **LOCKSTEP** — task/frontier, MEMORY, LIVE_STATUS, changelog, notes and v2
  book chapter synchronized. P4 stays 12/18; CPU-SYSTEM incomplete; 45 chapters.
  promotion: declined (versioned records and book retain the scope decisions).

`P4-SYSTEM.12` FINAL LEAF ACCEPTANCE (`2026-10-09`, `SEMULITH-P4-0104`):

- [x] **ROOT CAUSE** — git show 190d16b:profiles/rv64gc-lab-v0/encoding.sexp
  composes C with status complete. Read the .12 design and pinned RVI-C again at
  signoff: SHA-256 3f7e7d853d6e12e9d44c3d1bb488d1c312179a308d608182fb01db43a49d6aeb.
  Source expansions, reserved/hint rules, two-byte IALIGN and original ILEN are
  represented and checked; no scope inference from the GC name.
- [x] **ADDRESSED** — 37 forms lower to checked base rules; compiled operand,
  scatter, specificity and old-source pc+2 controls pass. Both page-edge guests
  pin no unnecessary second parcel and precise required-second-parcel fault.
  Requirement/contract/matrix and generated modules synchronized at 2611340.
  scripts/run_rv64gc_sail.py: 27 AGREE / 412 boundaries, all 37 forms in actual
  rows, exact repeat; the public timer probe owns the remaining platform limit.
  scripts/check_guest_gen.sh rc=0: 128 controls. This is finite C evidence,
  not full CPU-SYSTEM acceptance.
- [x] **NO REGRESSION** — make ci rc=0: check (core 153, DSP 17, verify 193),
  all doctrines, wasm bench, smoke-bench and all books. Final line: ci: all legs
  green (check, gate, bench, smoke-bench, book). Log target/p4-system-12/e2e/ci.log.
  All 167 guests pass; 139 historical parent PC/mode/write traces byte-identical;
  GUEST-GEN 128 controls and planted wrong expected value discriminate. No code
  change in this signoff. Closed live-head blocks archived byte-verbatim with
  complete reverse reconstruction asserted; fixed per-part/aggregate caps retained.
- [x] **LOCKSTEP** — .12 done, P4 12/18; .13 next, v2 open/20 of 106 checks
  realized. CPU-SYSTEM incomplete on eight axes. Current book/dossier/live pointer
  updated; .14 retains registry/book and black-box assumption-sweep ownership.
  promotion: declined (canonical declarations, permanent controls and C book retain it).


Active frontier: [`docs/tasks/P4-SYSTEM.md`](docs/tasks/P4-SYSTEM.md).


## Runtime designs

### `.13` c8 — privilege-mode runtime pair (`2026-10-10`, `SEMULITH-P4-0120`)

Own before changes: bind OB-PRIV-MODES's existing POS/NEG ids to the complete
13-guest P4.2 mode matrix. POS exercises CSR access, breakpoint/ECALL modes,
delegation and counter gates; NEG exercises S/U CSR refusal, return gates,
read-only writes, stimecmp, WFI and SFENCE.VMA permission. Whole guests can
contain both legal and refused cells; POS/NEG labels identify the witness focus.
Read all thirteen sources and the shared expectation/comparison owners before
binding. Retain the exact GPR-change, never-written and fetch-count rule: mode
and trap state are observed through ISA handler reads, not newly claimed direct
PC/mode comparisons. No universal mode-coverage, firmware or Linux claim.
Extend the required-binding regression guard without weakening post-v0 birth
realization. Preserve all 58 prior entries, all contract declarations and frozen
pins byte-for-byte. Expected census: 60/114; 27 runtime pairs then freeze remain.

This unit also owns routine DEV_NOTES pressure maintenance: use the existing
whole-entry sharder at a 32 KiB target, assert ordered byte reconstruction and
run SHARD-FREEZE. Fixed caps and sealed archive descriptors remain unchanged.
Run focused matrix/registry checks, make check, schema/freeze/gate controls,
books and commit hooks. Update canonical current counts, book and live pointer;
review LIVE_STATUS without fabricating milestone progress. Commit before c9.

### `.13` c9a — investigate inherited-global translation (`2026-10-10`, `SEMULITH-P4-0121`)

Priority prerequisite to OB-SV39 realization, owned before reproduction/changes.
Review found walk builds TlbEntry.global from the leaf alone, whereas the
independent author accumulates G along the traversal. Pinned supervisor artifact
rehashed d5186efc3ead1c1f693ac2b16aeccdcab95d990264f49b559252d2dc413a651a,
186455 bytes; read 11.1.3.1: non-leaf G makes subsequent mappings global.
This repository selects exact ASID/fence retention rather than over-fencing.
Potential impact: ASID changes re-walk instead of reusing inherited globals;
ASID-selective fences discard them and expose PTE changes prematurely under
the selected cache policy. Do not classify solely from source inspection.

Reproduce through public translate and actual SFENCE.VMA instructions with
hand-built PTEs; vary G at each of three levels, both ancestor levels together
and no-G control. Pin inherited cache hit/no walk across ASID/root changes,
both ASID-selective fence scopes, and subsequent full/address-only invalidation.
If confirmed, accumulate G in the single walk owner; preserve permissions,
fault priority and existing corpus observations. No author rewrite to fit CPU.
Require a pre-fix failing regression and green repair, ordinary translation and
full Rust tests, author cache controls, frozen-byte checks and full make ci.
Record root cause and finite policy scope in book/live docs; contract count
stays 60/114 in this prerequisite. Commit before c9b binding OB-SV39.
Also own the small current-doc correction: label c7b counts explicitly as
historical, so its 58/114 receipt cannot contradict the current 60/114 census.

c9a confirmed with independent literal PTEs and public calls on parent e4e657f:
`cargo test -p semulith-core global_from_any_walk_level_survives_asid_and_root_changes`
rc=101: mask 1 returns AccessFault cause 5/tval 0x402007 instead of
Physical 0x80004007. `cargo test -p semulith-core
actual_fences_retain_inherited_globals_only_for_asid_scopes` rc=101: root G,
ASID fence 0x12400073 leaves occupancy 0 instead of 1. Root cause is leaf-only
assignment of cached global flag. Accumulate G from every traversed PTE after
encoding checks; install only after existing permission/Svade checks succeed.
Eight root/middle/leaf G masks include nonglobal and all combinations; 32 actual
fence instructions cover both ASID-selective and both broad scopes. Keep the
independent author unchanged: its own inheritance mutant is already discriminated.

### `.13` c9b — Sv39 runtime pair (`2026-10-10`, `SEMULITH-P4-0122`)

Own before changes after c9a commits cleanly. Bind OB-SV39's two existing ids
to all fourteen translation guests: POS 4k/2m/1g, MPRV, cache/fence and
noncontiguous straddle; NEG canonical/invalid/reserved/superpage faults,
R/W/X and U/SUM/MXR permission, Svade and delegated faults. Read actual
sources (collapse repeated zero-word padding with counted runs), canonical
translation/CSR interfaces, all expectation observations and P4.3 book.
Re-derive each program's changes/fetch count with the independent parcel author
against the committed observations; preserve every input and old binding.
Use the existing corpus comparison rule, finite 1417-boundary evidence, no
universal Sv39/Linux claim. Extend required-binding guard; expect 62/114,
26 runtime pairs then freeze. Rust/focused registry, schema/freeze/gate controls,
books and hooks; update current counts while keeping old slice receipts historical.

Relevant historical audit: git log -S 'global: g,' identifies e839c1b,
P4-SYSTEM.3 slice d. Its diff introduced the leaf-only cached G assignment;
its message explicitly rejects over-fencing and tests leaf globals only.
c9a (7569fe2) now owns/fixes the missing ancestor case; archived historical
receipts remain unchanged. No other history audit is implied by this binding.

### `.13` c10 — Svade runtime pair (`2026-10-10`, `SEMULITH-P4-0123`)

Own before changes on clean 89a62a4. Read OB-SVADE/D-SVADE, state ADUE
exclusion, pinned supervisor A/D schemes, finish/cached permissions, original
programs/expectations and P4.3/v2 book. Bind POS to sv39-translate-4k/2m/1g
and NEG to sv39-svade. Preserve the existing full-width PTE read-back witnesses,
not merely fault causes: A=0 leaf 0x2000188f and D=0 leaf 0x2000184f at
steps 133/134; the three success guests read original PTEs at their final steps.
The D=0 load is legal (step 100), A=0 load faults 13 and D=0 store faults 15
(observed steps 94/107). Existing core step9 test also checks the whole byte
image unchanged. No new observation vocabulary or hardware-update claim.

Re-derive the four programs' changes/fetch counts independently and run focused
core Svade/registry plus make check, schema/freeze/gate controls/books/hooks.
All 62 prior entries and all contract/guest bytes stay exact. Extend required
bindings without weakening post-v0 guard; expected 64/114 with 25 runtime
pairs then freeze. Update current book/profile/live counts, qualify old counts
historically and commit before c11 IALIGN-16. No production behavior change.
Independence controls use in-memory author copies only: bypass A/D refusal,
and set A in a PTE while still returning the correct fault. The latter must
preserve fault observations and fail specifically at the later PTE read-back,
showing that the check observes absence of mutation as well as fault delivery.

c10 containment correction owned before edits: first commit attempt refused
README-ROUTING-CLOSURE because contract-v2.md reached 33700 > 32768 bytes.
Split the completed runtime-witness sections byte-verbatim into a linked P4.13
runtime chapter; retain index/navigation and update the chapter census through
its owner. Profiles family is 3144422 / 3145728 bytes: consolidate DOSSIER's
duplicated chronological contract progress into a current summary and pointers
to ENVIRONMENT, book and task receipts. Contract records and frozen inputs
remain exact. This is adopted routing/compaction within existing responsibilities,
not a cap increase or relocation of unbounded pressure. Measure all family axes,
run routing controls, books and retry hooks before completion. Preserve detailed
history in committed task/development/changelog records; do not erase receipts.
ENVIRONMENT's runtime progress likewise becomes a current exact binding table;
worked observations/controls remain in the new book chapter. Future profile
updates maintain current bindings rather than append duplicate slice histories.

### `.13` c11 — halfword instruction alignment (`2026-10-10`, `SEMULITH-P4-0124`)

Own before changes on clean c0507d0. Read frozen OB-IALIGN-16, RVI-C
27.1 (95631 B, pinned 3f7e7d85…49d6aeb), affected parcel fetch/SetPc
and independent author paths, four complete programs/expectations and C/runtime
book sections. POS binds c-links, c-page-end and sv39-straddle; NEG binds
c-page-straddle. Legal halfword links and a 32-bit instruction at page+0xffe
must execute. A compressed page-end instruction needs one parcel; a wider
instruction needs its second parcel. The refusal is instruction page fault 12,
not an alignment exception: mtval is the failed next-page parcel, mepc the
original halfword instruction. Existing changes/counts and never-written rule
remain the observation contract; no new trace-PC comparison or universal proof.

Independently replay all four budgets/observations and add in-memory alignment
and second-parcel fault controls if the actual vocabulary supports them. Bind
the two existing IDs, extend required coverage to 66, preserve all 64 prior
entries and contract/guest/author bytes. Run registry, make check, schema/freeze,
gate controls, routing and books. Update current profile table/counts and runtime
book; keep old slice counts historical. Expected 66/114, 24 runtime pairs then
freeze; c12 Zicntr next. Commit before advancing. If active task part pressure
requires it, move older completed receipts verbatim to new archive part 7 with
ordered reconstruction proof and current pointers; do not raise ceilings.

### `.13` c12 — base-counter inclusion (`2026-10-10`, `SEMULITH-P4-0125`)

Own before changes on clean 3be1785. Read OB-ZICNTR/D-ZICNTR, RVI-ZICNTR
6.1/6.1.1 (40747 B, pinned 8d619d6e…7f4fa81c), state counter owners/views,
public permission/timekeeping paths, mm-counters/mm-csr-ro-counters programs
and all observations, and privilege/interrupt/runtime books. Bind POS to
mm-counters and NEG to mm-csr-ro-counters. Rate/progress remain v1's declared
virtual-time contract; OB-GC-COUNTERS remains its own later pair. Existing exact
composition/CSR scope checks exclude Zihpm. Do not imply the guests alone
exercise S-mode time: the existing core counter permission fixture tests S
TIME's independent TM gate, and the independent author probe covers all three
counter gates in M/S/U. Run both supporting checks explicitly.

Independent replay must match both budgets/changes/parcels. Exercise existing
counter-enable and U-counter-enable refusing controls; add an in-memory
read-only-write bypass control against the actual sentinel guest if supported.
Preserve 66 prior entries and all frozen/guest/author inputs; required coverage
becomes 68. Focused registry, make check, schema/freeze, gate controls, routing,
books and hooks precede commit. Update current table/counts, book and pointer;
expected 68/114, 23 runtime pairs then freeze; c13 Sstc next.

Containment owned in this slice: active task part is 124649 B, leaving little
room for subsequent receipts. Move completed b1–c7a/c7b design blocks and old
c7b-through-a plus final .12 acceptance blocks byte-verbatim into new archive
part 7. Keep current execution plan/frontier/census and c8+ receipts live. Prove
ordered inverse reconstruction, link both blocks and prior archives, keep fixed
part/family caps and finite archive descriptors unchanged. Historical receipts
stay intact, and every ticked acceptance retains its original command/output.

### `.13` c16 — U-immediate sign extension and instruction PC (`2026-10-10`, `SEMULITH-P4-0133`)

Owned before edits on clean 8ef8419 after c15 hooks, brief clearing and actual
job census. Read OB-LUI-AUIPC/REQ-D-LUI-AUIPC/D-LUI-AUIPC and rehash/read
RVI-RV64I 3.1.2.1 (49,246 B, SHA256 6eadb316c2d535ccb87a7a6feb03ff54af6f4b5bbeb5c1a5102a02af81f13abd).
Review two canonical semantics rows, 20-bit/shifted widths, sign extension,
constant instruction PC and wrapping-add lowering, independent word author,
selected scope-alu/dir-chase/bound-arith source/expectations and current book.
POS uses scope-alu plus dir-chase; NEG bound-arith's signed/unsigned U-offset
edges. Independently replay all observations and demonstrate zero extension,
wrong shift, next-PC/extended-base-PC and nonwrapping addition alternatives
fail named steps. Whole legal programs; NEG is not a trap requirement.
Preserve all old registry/frozen/core/expectation/author data and assembled bytes;
require 78 registry entries, effective 76/114 (18 guest pairs), nineteen runtime
pairs/freeze. Focused make check, author/identity, schema/freeze/report/book gates.

Small encountered documentation defect owned here: both smoke-arith source
headers still name profile.toml and claim the assembler cannot read B/J formats.
Reproduce by reading lines 3–6 in both profiles; the active data is profile.sexp
and the assembler now supports B/J. History identifies b8d09f5 as the original
pre-completion comment and 133e722 as the unchanged GC copy. Correct only these
headers now; compare assembled old/new images and expected observations exactly.
No guest instruction or historical receipt is rewritten. Record the correction
in the worked book. Next OB-SHAMT after this bounded unit commits.

Hook dependency correction owned before dependent edits: PLATFORM-GEN refused
because the base smoke comment changes the rv64i dossier digest. Reproduction:
scripts/check_platform_gen.sh --self-test rc=1 names stale pin f24ca76d…8a74e
versus live 9f7cecb3…d784. This is the required pin propagation, not a changed
CPU or board capability. Deliberately rederive the pin through the shared digest
owner, then regenerate board artifacts, platform export and model-book materials.
Check that all generated semantic data are unchanged apart from the dossier pin
and provenance fingerprints. Re-run board/platform/material/report/schema gates
before the same c16 commit; do not pivot or bypass the hook.

### `.13` c15 — register ALU guarantees (`2026-10-10`, `SEMULITH-P4-0132`)

Owned before changes on clean 4beadff, after committed c14b checks/hooks and
actual job census. Read OB-ALU-REG and its requirement/decision; pinned
RVI-RV32I 1.1.4.2 (same 107630-B/3b20e92f…ad75ec snapshot rehashed at c14b).
Review seven semantic rows, wrapping Add/Sub and signed/unsigned comparison
lowering, pre-state GPR write discipline, scope-alu/bound-arith/bound-alias
sources and observations, integer author/probe, registry/tests and runtime book.

POS runs scope-alu and bound-arith for ADD/SUB/SLT/SLTU/XOR/OR/AND, signed
extremes, bitwise distinctions and ignored overflow. NEG runs bound-alias for
source/destination overlap, visible zero comparisons and hardwired x0 contexts.
Whole legal programs; NEG rejects semantic alternatives, not required traps.
Independently replay every observation/parcel, then demonstrate saturating
ADD/SUB, swapped signedness, wrong bitwise operators and premature aliased-source
clearing fail named steps. Existing integer-author controls remain the durable
proof route; slice-specific in-memory copies are diagnostics, no new semantics.

Preserve all 74 prior entries and all core/guest/author/canonical/frozen bytes.
Bind CHK-ALU-REG only after independent checks; require 76 registry bindings,
effective 74/114 (17 guest pairs), 20 remaining runtime pairs/freeze. Update
current book/ENV/dossier/GS and durable pointers/history. Focused make check,
registry/author/controls, schema/freeze/report and book gates precede commit;
no new mechanism warrants repeated full CI. Next OB-LUI-AUIPC.

### `.13` c14b — immediate ALU guarantees (`2026-10-10`, `SEMULITH-P4-0131`)

Owned before changes on clean 99b32e3, after gate-control commit/hooks and actual
job census. Read OB-ALU-IMM/REQ-D-ALU-IMM/D-ALU-IMM; rehash RVI-RV32I
107630 B to 3b20e92f067509535f95883832e84b32dbea43a29e1347b7925c374213ad75ec
and read 1.1.4.1. Review six canonical semantic rows, shared wrapping Add/bitwise/
comparison lowering, GPR writes, full scope-alu/bound-arith sources/expectations,
integer author/probe, registry comparison and runtime book before binding.

POS names scope-alu, covering ADDI/SLTI/SLTIU/XORI/ORI/ANDI with signed and
unsigned comparisons and visible zero overwrite. NEG names bound-arith for
ADDI wrap and extreme immediates/comparisons. Both are whole legal programs;
NEG rejects incorrect semantic alternatives, not an invented architectural
trap. Independently replay every write and parcel count before credit. Prove
zero-extended SLTIU/logical immediate, unsigned SLTI and saturating ADDI copies
fail meaningful observations, retaining initial-source words and budgets. Use
existing integer-author control as the durable refusing mechanism; finite
in-memory copies add slice-specific discrimination without production edits.

Preserve all 72 prior entries and all core/guest/author/canonical/frozen bytes.
Bind existing CHK-ALU-IMM IDs only after checks, extend declared registry coverage
to74/effective 72. Update current taxonomy (16 guest pairs), ENV/dossier/GS,
worked book values and live pointer/history/task receipts. Run focused registry,
independent author/control, make check, schema/freeze/report controls and books;
full CI only if findings warrant a milestone. Commit before next OB-ALU-REG;
expected 72/114, 21 runtime pairs and final freeze remain.

### `.13` c14a — contract-count controls without missing-id assumptions (`2026-10-10`, `SEMULITH-P4-0130`)

Owned before code changes on clean 834499b, after full CI/hooks and actual job
census. Scoped review: contract_measure, independent recount, _selftest fixtures,
GATE-REPORT wrapper, current runtime-book known finding and .13 completion plan.
Reproduction already RED: simulating valid CHK-ALU-IMM-POS registration makes
shared-id +1 arm expect114/72 but get114/71 (17/18). The measure is correct;
the test's example ceases to be missing when the next planned pair binds.

Repair only the oracle before c14b ALU credit. Always declare one reserved
synthetic check on an independently selected effective record in scratch
catalogs, then count it only when that unit names the exact registry pair.
Using a synthetic declaration avoids a live-unregistered-pair branch and its
full-coverage edge case. Actual catalog/forms/pins/registry and production
measure stay unchanged. No new CPU credit: 70/114 remains open.

Keep cross-unit non-credit and wrong-owner/shape/supersession controls. Add
permanent duplicate-registration and all-effective-checks-realized controls:
saturate a scratch registry from independently recounted pairs, then introduce
and bind the synthetic declaration. Coverage must still distinguish 114/114,
115/114 and 115/115 without pinning those live numbers. Run the former ALU
example already-bound scratch control and an over-credit/duplicate mutant RED
before increasing strict declared arm count from 18 to 20. Verify all generated
reports byte-identical, wrapper controls, book, live-doc bounds and hooks;
commit this bounded repair before c14b runtime binding. No Rust or profile
canonical data changes; ordinary focused checks suffice after prior full CI.

### `.13` c13b — observable S-mode timer witnesses (`2026-10-10`, `SEMULITH-P4-0129`)

Owned before changes on clean f769e91, after its full CI/hooks and actual job
census. Scoped review: pinned Sstc 12.1, supervisor 11.1.1.12, machine TM/STCE
clauses; OB-SSTC/D-SSTC, CSR permissions, timer progress, actual parcel engine,
registry/test dispatch, corpus comparison and current runtime/interrupt book.
No production semantics or canonical/guest/author input changes are needed.

Add a named Execution evidence kind distinct from provider-assumption Boundary.
Its Sstc POS runs i-timer/w-timer companions plus thirteen real S instructions:
program compare 16/read-back, observe pending 0, program 0/observe 32, program 32/
read-back/observe 0, then write/read-back 0x8000000000000020 from seeded x12
to exercise the full 64-bit compare field. Seed TM/STCE/delegation, leave interrupt enables clear;
nonzero values and sentinels make each read/write visible. Per-step audit all
GPRs, S mode/next PC, exact raw compare, time/retirement and two fetch parcels;
no M round trip can hide inside the fixed budget. NEG runs mm-stimecmp plus
three six-step literal cases: S missing TM, S missing STCE, U despite open gates.
CSRRW must trap before old-destination/compare/source effects; actual M handler
instructions read cause 2, offending word, original EPC and unchanged compare 101,
then continue with marker 42. Audit exact trap owners and full registers per step.

Extend independent counter-author probe with the same independently specified
literal witness sequences. Keep original production author and all historical
inputs exact. Reproduce forced-all-S-illegal author copy: old mm-stimecmp still
matches 35/70 but direct POS must fail visibly. Permanently test that disabled
TM/STCE causes POS refusal and opening a NEG gate is rejected. Observe controls
before registry credit. Disabled-witness control observed rc1 with explicit
terminal-control-missed reason before adding its one GUEST-GEN self-test arm;
normal counter probe verifies 31 new boundaries /62 parcels plus old 35/70 miss.
Registry companions use the existing shared corpus
comparison helper; never duplicate its observation rule. Bind existing CHK-SSTC
only after both direct checks and controls pass, extend declared coverage to 72
registry entries /70 effective checks, preserving earlier 70 entries byte-exact.

Update current taxonomy (one direct execution pair), dossier/env/GS, book worked
values and repaired-gap status, live pointer/history and task receipts. Preserve
all frozen forms/pins and guest/state/definition bytes. Focused author/core/
registry checks, schema/freeze/gate controls, make check and full CI (new evidence
mechanism milestone) precede commit; fixed caps stay unchanged. Then select the
next unbound effective runtime pair (22 remain), without freezing early.

Next-slice defect owned/scheduled in c14 before ALU binding: gate_report's
shared-id +1 control hard-codes CHK-ALU-IMM-POS as unregistered. A scratch
registry with that valid pair already bound makes only this arm fail (17/18):
actual114/71, expected114/72 because inserting a duplicate cannot add credit.
Reproduction: python3 in-memory gate_report self-test with the one synthetic
ALU entry, target/p4-system-13/c13b/next-alu-gate-control.log rc1. Production
measure is correct. Priority: blocking c14 before its first binding. Replace the
hard-coded pair with an independently selected effective unregistered pair;
add a control that repeats the experiment when the old example is already bound.
If no unregistered pair remains, use a deliberate synthetic declared fixture,
not a live-id assumption. Preserve cross-unit and duplicate-count discrimination.
This pending repair does not change the current70/114 result or c13b signoff.

### `.13` c13a2 — dynamic STIP fallback (`2026-10-10`, `SEMULITH-P4-0128`)

Own before changes on clean 7222cdc. Read pinned machine 2.1.1.9/2.1.1.18,
supervisor pending/compare clauses, computed/CSR legalization paths, real-state
interrupt-view fixtures, timekeeping, event/reset witnesses, independent author,
version records, registry/tests and current book. Machine text explicitly makes
STCE-clear pending behave as absent Sstc and then permits M software STIP writes.
Keep the 26 owners: raw mip holds software STIP; when STCE=1 expose unsigned
time>=stimecmp and ignore M writes to STIP. sip.STIP remains read-only and only
visible when delegated. Retain raw software STIP behind the enabled view as an
explicit laboratory choice where the pinned text imposes no transition storage
rule. No external source, counter reset change or hidden latch is introduced.

Before production edits, add focused real-state regressions and demonstrate RED
for cold pending=0, STCE-clear software set/clear, selected comparator transitions,
retained software state, delegated sip read-only behavior and all six actual CSR
forms (register operands can touch bit5; five-bit immediate operands cannot set
it). Each instruction case checks old destination, exact raw owner, mode/PC and
two fetch parcels. Repair computed overlay and conditional field legalization at
the shared CSR boundary, not individual instruction handlers. Update existing
interrupt-view/timekeeping and interrupts::timer-arrival fixtures to explicitly enable STCE where testing the
comparator, and reset expectations to cold zero. Enable event timer setup without
adding executed setup steps. Repair independent author from the same clauses;
extend its finite matrix and deliberate mutants, observe RED before adding gate
arms. Recheck all 167 guests and 42 owned records unchanged after c13a1.

Supersede frozen OB-GC-ENV-INTERRUPT-SOURCES with open-v2
OB-GC-ENV-INTERRUPT-SOURCES-V2 and a named direct boundary POS/NEG pair:
no external sources, explicit STCE-dependent software/comparator provenance,
read-only M sources and sip.STIP, retained raw policy and transitions. Fixtures
run real CSR instructions with literal independent witnesses, plus the existing
source guests. Negative witnesses reject forbidden pending writes, preserving
raw owners; no invented provider response violation is claimed for an ignored
architectural write. Existing historical registry entries remain tested; the new
pair replaces their effective credit, keeping 68/114. Update v2 event dependency
and reset statement, never frozen records/member pins. Require all 70 declared
bindings through this slice. Update state descriptions/field reset authority,
regenerate state and definition input-pin mirrors and GS, and document examples/limits before signoff.

The affected privilege/author FP-dirty comments still name Sail implementation
symbols/file locations. Remove those maintained internal assumptions while
editing these files; verify replacement rationale from pinned architectural FS
clauses. Broader dependency-assumption census remains .14's existing owned work.
Measure live-doc pressure: if DEV_NOTES cannot fit this receipt under its fixed
ceiling, move completed entries verbatim into the next governed archive part,
prove ordered inverse reconstruction and preserve links before adding the entry.
Gate-report self-tests reveal a separate owned oracle defect: they assume every
registry entry is effective, and that removing supersessions cannot restore
previously realized credit. Adding the first supersession of an already realized
record yields GREEN recount 114/70 versus correct 114/68 and nosup 128/70 versus
assumed 128/68 (15/17 controls). Production contract_measure correctly filters
effective pairs. Repair the independent self-test recount to intersect exact
non-superseded declared pairs with independently read registry pairs; derive the
nosup delta from realized superseded pairs. Add one synthetic supersession of a
currently realized record so this condition remains exercised after live changes,
observe its old-assumption mutant RED before registering the added arm. Keep
production measure/verdict unchanged. This is blocking self-test correctness,
fixed here before signoff rather than fitting its constants to 68/70.

Full CI exposes one additional stale comparator fixture: the compressed corpus
stager's independent c-irq blueprint still omits STCE and expects the old
17-boundary schedule. Its two GREEN staging arms fail hand checkpoint x7 after
the architectural repair (139/141). Own the blueprint repair here: prepend the
same explicit enable as the adopted source, increase deadline/budget by two,
advance handler/interrupt PCs by eight and retired count by two. Require the
independent generated blueprint body to match the adopted guest's assembled
bytes and all observations, while preserving all production guest records.
The stager's deterministic and observation/extent controls must all pass.

Run focused RED/GREEN regressions, author mutants, registry/schema/freeze/gates,
public CSR original reproduction (101 -> 0), corrected public Sail diagnostic,
make check and full make ci. Commit the architectural repair before c13b direct
S programming/refusal witnesses. No SSTC credit yet; cold STCE stays zero.

### `.13` c13a1 — explicit timer-source setup (`2026-10-10`, `SEMULITH-P4-0127`)

Own before changes on clean 618b7d2. Implement the first c13 prerequisite only:
prepare c-irq, env-irq-sources, i-prio, i-timer, mm-wfi, w-deleg, w-notrap,
w-sw and w-timer with two M-mode STCE setup instructions using unused x31.
Keep cold STCE=0 and mm-stimecmp unchanged. Declare each budget as old+2
before deriving. Shift finite compare deadlines by two ticks to retain the
same interrupt/wait schedule. Verify assembled body bytes except those declared
immediates, then independently derive all GPR changes and parcel requests before
any processor execution. Re-author stale source timing/address prose accurately;
w-timer's old mepc comment says 0x80000044 while its instruction/expectation is
0x8000002c (WFI+4); reproduce by assembly, correct to new WFI+4, and close here.

The old public timer diagnostic also leaves STCE clear, so its STIP=1
laboratory side is confounded by the known overlay defect. Repair it here with
explicit STCE setup and a read-back witness before interpreting the reference
limit. Re-derive a ten-boundary fixture and require actual menvcfg bit 63 from
Sail's public CSR read. Remove maintained plat_have_clint implementation naming;
use only public configuration, validation and traces. This is the same explicit
setup prerequisite, not a second direction. Own and close this evidence defect
before c13a1 signoff; retain historical receipts qualified by their old inputs.

The author's historical-owned set loses only env-irq-sources: 41 historical
captures stay exact; that guest becomes an explicitly budgeted fresh parcel
record. Keep --check-owned at 42 records (41 historical + one fresh), fresh
route headers and canonical write guards. Extend its existing extent/provenance
diagnostics with fresh-record/budget drift controls; observe each mutant RED
before registration. Preserve every other source/expectation and all contract
records/pins byte-exact. Measure profile containment before adoption. If necessary,
move duplicated protocol prose verbatim into a linked book part within fixed caps.

Regenerate the Rust guest mirror, replay all 167 guests and registry, run author
controls, fresh pinned Sail attempts for nine inputs (qualify public platform
limits), focused gates, make check and full make ci. Update current book/profile
counts (privilege matrix 483 boundaries), provenance, live docs and receipts.
Also correct the current ENVIRONMENT summary still saying 64 realized checks
against the already verified 68; no new credit. G-CONTRACT remains 68/114,
no production STIP repair or SSTC credit. Commit green
before c13a2. Verification/commit receipts follow in their canonical sections.

### `.13` c13 — supervisor timer programming (`2026-10-10`, `SEMULITH-P4-0126`)

Own before changes on clean 8d29fff. Review OB-SSTC/D-SSTC, pinned RVP-SSTC
12.1 and supervisor/machine stimecmp/STCE clauses, real CSR permission/computed
pending/timekeeping paths, complete mm-stimecmp/i-timer/w-timer observations
and interrupt/runtime book. Before credit, test a suspected terminal witness
hole: mm-stimecmp's legal S read at its last boundary returns zero, so both
success and an unexpected trap may produce no observed GPR change within budget.
Census all corpus stimecmp writes and counter/STCE setup; record actual outcome.

If confirmed, own the verification defect here and fix it before binding.
Add a named direct execution evidence kind distinct from provider-assumption
fixtures. Its Sstc positive check runs existing i-timer/w-timer guests plus an
actual S-mode CSR instruction sequence: nonzero compare programming/read-back,
cleared/reasserted/cleared delegated timer pending observations and continuation
markers must reject an unexpected trap. Negative check runs mm-stimecmp plus
literal S missing-TM/missing-STCE and U privilege refusals before destination/
compare effects, read back through M handler instructions. Initial state and
literal words/expected observations are specified independently of engine output.
Use real parcel fetch and interpreter; do not add production semantics.

Preserve prior 68 entries, all contract/guest/author bytes and frozen pins. Bind
existing CHK-SSTC IDs and extend coverage to 70 only once direct fixtures pass.
Independently replay old guests, demonstrate the suspected old witness miss and
new fixture discrimination, run timer permission/author controls, make check,
focused gates and full CI as the new evidence mechanism milestone. Update current
profile table/counts, book, live docs and task receipts, then commit. Expected
70/114, 22 runtime pairs then freeze; next base arithmetic pair after this slice.

#### c13 STCE pending-state investigation — owned before diagnostic

Re-reading pinned machine 2.1.1.18 additionally exposes a possible architectural
conflict: with menvcfg.STCE=0, STIP reverts as if Sstc were not implemented;
2.1.1.9 then makes mip.STIP software-writable. Current computed() ignores STCE
and state fields always compute STIP. Investigate through public CSR APIs with
stimecmp above time and STCE clear; do not classify as harmless laboratory
latitude or credit SSTC before resolving the source/contract conflict. If
confirmed, split this slice: commit the bounded diagnosis/design (no new credit),
then a separately owned c13a architectural prerequisite before c13b witnesses.
A repair must preserve frozen records by v2 supersession, synchronize current
state/author/guest inputs and fresh evidence, and pass full CI. Old receipts
remain historical; all affected timer observations must be re-earned, not fitted.

#### c13 confirmed verification defect — terminal zero timer read

Reproduction: execute an in-memory copy of derive_rv64gc_expectations with its
single `if not tm or not stce:` replaced by `if True:`. Replaying mm-stimecmp
still matches all 35 committed changes and 70 parcels, but boundary 34 traps
with cause 2, mepc=0x80000044, final mode M. Its zero-valued legal S read
produces no change, and the fixed budget stops before a handler observation.
Impact: this guest alone cannot discriminate S timer availability; do not bind
Sstc as an adequate positive witness. Production failure has not been observed.

Corpus census: rg stimecmp/menvcfg/mcounteren across all 167 source guests
finds only mm-stimecmp opens TM/STCE for timer access; it only reads stimecmp.
Timer writes in the other programs run in M. Existing core permission and
independent author matrix test gates, but no existing registered guest witnesses
S-mode compare programming/read-back. Own a direct registered execution fixture
in c13 now, with explicit nonzero values and handler-visible refusal cases.
Original guest/expectation records remain historical exact inputs; no need to
rewrite their scope or the observation contract. Priority: before SSTC credit.

#### c13 confirmed architectural defect and bounded repair order

Public-API diagnostic compiled against current semulith-core: cold state,
M mode, STCE=0, stimecmp=u64::MAX; csr_write(0x344,32) succeeds but
csr_read(0x344)&32 returns 0. Literal pinned fallback requires 32.
Executable target/p4-system-13/c13/stip_probe exits 101 with that assertion.
RVP-MACHINE 2.1.1.18 says STCE-clear STIP reverts as if Sstc absent;
2.1.1.9 makes mip.STIP software-writable in that case. Rehashed machine
271851 B b63fe335…17fea, supervisor 186455 B d5186efc…651a, Sstc
27429 B 30bea862…216e1. Root: computed() unconditionally overlays time>=compare
and computed-field writes always retain, while state.sexp declares that rule
unconditionally. git log -S locates introduction at 47badd2 (P4.2 d), confirmed
by its diff. Frozen v1 OB-GC-ENV-INTERRUPT-SOURCES repeats that assumption.

Priority: architectural prerequisite before any SSTC credit. Keep cold STCE=0;
do not change reset merely to preserve old observations. No external-source
expansion: software-writable STIP is hart software, not an injected device.
Bounded work, each green and committed before the next:

1. **c13a1 corpus preparation**: nine timer-source programs (c-irq,
   env-irq-sources, i-prio, i-timer, mm-wfi, w-deleg, w-notrap, w-sw,
   w-timer) explicitly enable STCE in M before using the comparator. Preserve
   mm-stimecmp's deliberately closed gates. Derive observations before engine
   execution; adjust authored timer thresholds for the added setup boundaries,
   preserve meaningful control flow and declare new provenance. Reconcile the
   historical author's owned-record protocol explicitly rather than copying
   capture headers to a new derivation. Regenerate guest mirrors, fresh public
   reference attempts where affected, current descriptions and full CI. Measure
   profile family pressure before adoption; if needed move duplicated ENVIRONMENT
   protocol prose verbatim to a linked book chapter within existing caps.
2. **c13a2 architecture/contract repair**: gate comparator overlay on STCE;
   STCE-clear mip.STIP is software-writable, sip.STIP remains read-only.
   Explicitly select retained raw software STIP across enabled comparator views,
   if permitted by the pinned text; test transitions and all CSR forms. Repair
   the independent author from the same clauses, direct cold/reset/event fixtures
   and current state narrative. Update the public timer-platform probe to enable
   STCE explicitly before deriving comparison-dependent reads (completed by c13a1).
   Supersede frozen v1 interrupt-source wording in
   open v2 with named realized checks; correct the open v2 reset description.
   Frozen records/pins and historical receipts stay byte-exact. Reproduce RED
   before/after public CSR/instruction regressions and full CI. Recheck every
   affected input and gate count, without awarding SSTC early.
3. **c13b Sstc witnesses**: registered direct execution pair, actual S compare
   programming/read-back/pending/continuation and illegal-before-effects cases,
   plus old guests. Explicitly demonstrate the terminal-zero control now fails.
   Only then bind CHK-SSTC and extend effective realization to 70/114.

This c13 commit is bounded diagnosis/design only: no production/guest/author
change, no new contract credit (68/114 remains). Director decision/access is not
needed to repair the pinned-rule mismatch; unresolved implementation facts are
re-verified during their owned slice. Promotion declined here: task, pending
book section and canonical gate opening retain both defects and exact schedule.



## Runtime acceptance

`P4-SYSTEM.13` slice (c16) (`2026-10-10`, `SEMULITH-P4-0133`):

- [x] **INDEPENDENT / CONTROLS** — python3 target/p4-system-13/c16/probe.py
  rc=0: three guests / 79 boundaries / 158 parcels exact; seven wrong alternatives
  fail intended scope step 3, bound step 29 or chase step 0. Integer author probe
  rc=0: 22 arithmetic/10 branch cases, 17 gaps/471 steps, 42 owned records exact.
- [x] **IDENTITY / RUST** — python3 target/p4-system-13/c16/identity.py rc=0:
  all 76 prior entries, author/core/frozen records exact; GC's other 347 inputs
  exact. Both corrected smoke headers preserve twelve instructions / 48 bytes;
  generated data bodies exact, only two source fingerprints regenerate.
  make check rc=0: Rust 167/17/201, fmt/clippy clean. Registry 78, effective 76/114.
- [x] **SCHEMA / REPORT / BOOK** — scripts/check_contract_freeze.sh rc=0:
  three versions/zero findings; scripts/check_dossier_schema.sh rc=0: 270/two
  named skips. scripts/check_gate_report.sh rc=0: five reports in sync;
  python3 scripts/gate_report.py --self-test rc=0: 20/0. make book rc=0:
  main/model books build; git diff --check rc=0. Nineteen runtime pairs/freeze
  remain, OB-SHAMT next. scripts/check_guest_gen.sh rc=0: both generated
  fixtures and governed mirror match, all 142 controls pass.
- [x] **DEPENDENT PIN CLOSURE** — scripts/check_platform_gen.sh --self-test
  initially rc=1 with named stale f24ca76d…8a74e pin. After shared-digest re-pin,
  scripts/check_platform_gen.sh rc=0 and --self-test 11/0; scripts/check_board_gen.sh
  rc=0: one board/seven outputs byte-exact. scripts/check_materials_bill.sh rc=0:
  all five books match. python3 target/p4-system-13/c16/board-identity.py rc=0:
  eight S-expression documents exact except dossier pin, map and four fragment
  bodies exact except displayed pin. Refreshed schema/report checks pass again.
  promotion: declined (canonical rules, counterexamples and worked runtime book retain the realization and header correction).

`P4-SYSTEM.13` slice (c15) (`2026-10-10`, `SEMULITH-P4-0132`):

- [x] **INDEPENDENT / CONTROLS** — python3 target/p4-system-13/c15/probe.py
  rc=0: three guests / 99 boundaries / 198 parcels exact. Eight alternatives
  fail intended steps: saturation 5/6, swapped comparison signedness 11/13,
  wrong AND/OR/XOR 5/6/7, premature aliased-source clearing 24.
  python3 scripts/probe_gc_integer_author.py rc=0: 22 arithmetic/10 branches,
  17 corpus gaps/471 steps and 42 owned records exact.
- [x] **IDENTITY / RUST** — python3 target/p4-system-13/c15/identity.py rc=0:
  348 canonical/guest files and four author/generated files exact; core unchanged,
  all 74 earlier entries exact. make check rc=0: Rust 167/17/201, fmt/clippy clean;
  registry 76, effective 74/114, twenty runtime pairs remain.
- [x] **SIGNOFF** — scripts/check_contract_freeze.sh rc=0: three versions/zero
  findings; scripts/check_dossier_schema.sh rc=0: 270/two named skips.
  scripts/check_gate_report.sh rc=0: five generated reports in sync;
  python3 scripts/gate_report.py --self-test rc=0: 20/0. make book rc=0:
  main/model books build; git diff --check rc=0. c15 complete; OB-LUI-AUIPC next.
  promotion: declined (exact bindings, counterexamples and worked runtime book retain the realization).

`P4-SYSTEM.13` slice (c14b) (`2026-10-10`, `SEMULITH-P4-0131`):

- [x] **INDEPENDENT / CONTROLS** — python3 target/p4-system-13/c14b/probe.py
  rc=0: two guests/62 boundaries/124 parcels exact; five wrong alternatives
  fail intended steps17/14/8/10/8 (SLTIU/SLTI/ANDI/XORI/ADDI saturation).
  python3 scripts/probe_gc_integer_author.py rc=0: 22 arithmetic/10 branches,
  17 corpus gaps/471 steps and 42 owned records exact; sign mutant rc1 with
  SLTIU sign extension reason. Negative binding rejects semantic countermodels,
  not invented traps for legal ALU instructions.
- [x] **IDENTITY / RUST** — python3 target/p4-system-13/c14b/identity.py rc=0:
  348 canonical/guest files+four author/generated files exact; core unchanged,
  all 72 previous entries exact. make check rc=0: Rust167/17/201, fmt/clippy clean;
  all 74 registry entries run. Gate-report --self-test 20/0 with actual ALU binding;
  effective114/72, 21 runtime pairs remain.
- [x] **SIGNOFF** — CONTRACT-FREEZE three versions/zero findings;
  DOSSIER-SCHEMA270/two named skips. scripts/check_gate_report.sh rc=0:
  five generated reports in sync. make book rc=0: main/model books build;
  diff check clean. c14b complete; OB-ALU-REG next after commit.
  promotion: declined (exact bindings, independent counterexamples and worked runtime book retain the realization).

`P4-SYSTEM.13` slice (c14a) (`2026-10-10`, `SEMULITH-P4-0130`):

- [x] **ROOT / REPAIR / RED** — python3 scripts/gate_report.py --self-test
  rc=0:20 pass/0 fail. Original simulated ALU binding failed17/18; now passes20/0.
  Duplicate-credit mutant rc1:19/20, specifically new duplicate-registration arm,
  observed before strict declared count20. Full-coverage fixture distinguishes
  complete, new unbound and newly bound check without live missing-id constants.
- [x] **SCOPE IDENTITY** — python3 target/p4-system-13/c14a/identity.py rc=0:
  production AST outside _selftest exact, all crates/profiles/author bytes exact,
  effective114/70 unchanged. No canonical/frozen record or actual registry edit.
- [x] **SIGNOFF** — scripts/check_gate_report.sh rc=0: five generated reports
  in sync; all20 Python controls pass. make book rc=0: main/model books built.
  DERIVED-COUNTS --self-test10/0; diff check clean. c14a complete; c14b next.
  promotion: declined (synthetic oracle, duplicate/full-coverage controls and runtime book retain the correction).

`P4-SYSTEM.13` slice (c13b) (`2026-10-10`, `SEMULITH-P4-0129`):

- [x] **DIRECT EXECUTION / CONTROLS** — cargo test -p semulith-verify
  contract_execution_rv64gc rc=0: three tests pass. POS thirteen S instructions
  /26 parcels includes full 64-bit compare read-back; NEG three six-step cases
  /36 parcels includes actual M-handler trap/unchanged-compare reads. All GPRs,
  mode/PC, compare, counters/fetches and NEG trap owners exact. Closed POS gates
  and opened NEG gate controls refuse at boundaries 2/1 respectively.
- [x] **INDEPENDENT / TERMINAL RED** — python3 scripts/probe_gc_counter_author.py
  rc=0: direct 31/62 exact; forced-S-illegal old guest 35/70 still matches but
  new POS refuses boundary 2. --disable-sstc-witness rc1 with explicit terminal
  control-missed reason observed before its GUEST-GEN arm registration. All 42
  owned records exact; production author unchanged.
- [x] **REGISTRY / IDENTITY** — cargo test -p semulith-verify
  contract_checks_rv64gc rc=0: four tests pass, all 72 entries run.
  python3 target/p4-system-13/c13b/identity.py rc=0: 348 profile canonical/guest
  files and four author/generated files exact; core unchanged; 70 prior entries
  exact; 114 declared/70 realized. python3 scripts/derive_gc_parcel_counts.py
  rc=0: 167 exact traces /5360 boundaries /10514 parcels, no input writes.
  python3 scripts/gate_report.py --self-test rc=0: 18 pass/0 fail.
- [x] **FINAL SIGNOFF** — make ci rc=0: all five legs green, Rust167/17/201,
  all doctrines and books green. CONTRACT-FREEZE three versions/zero findings;
  DOSSIER-SCHEMA270/two named skips. Current book/status sync reviewed;
  c13b complete, c14 gate-control repair and OB-ALU-IMM next after commit.
  promotion: declined (direct execution witnesses, discriminating control and worked runtime book retain the correction).

`P4-SYSTEM.13` slice (c13a2) (`2026-10-10`, `SEMULITH-P4-0128`):

- [x] **ARCHITECTURAL RED/GREEN** — cargo test -p semulith-core supervisor_timer:
  before repair four fail (rc101), after four pass (rc0), including 48 actual
  CSR instructions and exact old destination/raw source/parcel witnesses.
  Original public target/p4-system-13/c13a2/stip_probe rc0 replaces baseline101.
- [x] **AUTHOR / INPUTS** — python3 scripts/probe_gc_counter_author.py rc=0:
  eight literal STIP cases/retention and counter corpus117; four new mutants
  each rc1 before registration. Full independent corpus 167/5360/10514 and
  --check-owned42 exact. python3 target/p4-system-13/c13a2/identity.py rc=0:
  335 guest files, 52 frozen record lines, both frozen forms and 68 bindings
  exact; 114 declared / 68 effective realized. No SSTC credit.
- [x] **SOURCE CONTRACT / REPORT** — cargo test -p semulith-verify
  contract_checks_rv64gc rc=0: four tests pass, all70 registry entries run.
  Direct replacement source pair executes 27 boundaries / 54 parcels.
  python3 scripts/gate_report.py --self-test rc=0: 18 pass / 0 fail;
  unfiltered supersession mutant rc1: new arm and independent recount fail.
  Schema270/two skips; CONTRACT-FREEZE three versions/zero findings.
- [x] **CONTAINMENT / REVIEW** — python3 scripts/shard_history.py rc=0:
  21 completed entries moved to 15329-B shard-0220; exact ordered inverse
  SHA256 b2fc35ed2b74186ccd13b60fda26e891c7ad39f5ee81f7d99403785712bf8306
  matches prior committed notes. Caps unchanged. make check rc=0:
  Rust167/17/198, fmt/clippy clean. Corrected public Sail timer probe rc0:
  repeated traces, STCE read-back verified, qualified pending difference remains.
- [x] **STAGING REPAIR** — python3 scripts/stage_gc_c_corpus.py rc=0:
  28 guests / 37 forms / 431 boundaries / 712 parcels; --check rc0.
  Observation/extent mutants rc1 with precise record refusal. Independent
  assembly/record comparison reports adopted c-irq exact (19/32), preserving
  all production inputs; resolves the full-CI 139/141 staging failure.
- [x] **FINAL SIGNOFF** — make ci rc=0: all five legs green (check, gate,
  bench, smoke-bench, book), Rust167/17/198; all doctrines green. Book and
  current source/status sync reviewed. c13a2 complete; c13b next after commit.
  promotion: declined (versioned source contract, controls, history and worked runtime book retain the correction).

`P4-SYSTEM.13` slice (c13a1) (`2026-10-10`, `SEMULITH-P4-0127`):

- [x] **ROOT CAUSE / OWNERSHIP** — git show 618b7d2 timer sources:
  nine comparator programs omit STCE setup; cold STCE=0 is retained.
  Python assembly reproduces old w-timer WFI+4=0x8000002c and expectation
  x12=0x8000002c, contradicting source comment 0x80000044. The old public
  timer probe also omits STCE; its laboratory pending claim is confounded
  by c13's known production defect. Both documentation/evidence defects
  are owned here, alongside the existing preparation prerequisite.
- [x] **ADDRESSED / INDEPENDENT BEFORE ENGINE** — python3
  target/p4-system-13/c13a1/stage.py rc=0: nine programs, 281 boundaries / 524 parcels. Each budget old+2
  declared before deriving, body PCs old+8 and bytes exact except the eight
  declared deadline ADDIs (old+2). All body GPR changes match the exact
  address/counter/deadline transformation; actual request logs match counts.
  x31 unused before setup. Fresh route provenance carries no capture claim;
  nine source/record pairs 84576 -> 64696 B (19880 B saved). Current
  w-timer instret=13, time=17, mepc=0x80000034; two idle steps retained.
- [x] **AUTHOR / DISCRIMINATION** — python3 derive_rv64gc_expectations.py
  --check-owned: 42 byte-identical (41 historical + fresh env-irq-sources,
  fixed budget 13). probe_gc_owned_extent.py rc0: both branches refuse
  count/observation/comment/CRLF drift; repeat/write guards pass. Fresh-budget
  and fresh-word-route mutants each rc1 with env-irq-sources DRIFT before
  their two gate arms were registered. Provenance probe rc0; counter author
  30 mode gates / 117 corpus steps exact. Full independent parcel census:
  167 exact traces / 5360 boundaries / 10514 actual requests.
- [x] **PUBLIC REFERENCE EVIDENCE REPAIRED** — python3 probe_gc_sail_timer.py
  rc0: ten pre-derived boundaries, STCE read-back 0x8000000000000000 on
  both sides; Sail pending 0/0 versus laboratory 1/1, two identical traces.
  Removing enable makes its public read-back guard refuse. Nine fresh Sail
  attempts: w-sw AGREE (19 steps, two identical traces); six DIVERGE at
  c-irq 11 / env-irq-sources 12 / i-prio 26 / i-timer 5 / mm-wfi 11 /
  w-deleg 14. w-notrap and w-timer processes rc1 after illegal disabled
  time/instret reads and trap loops; old inputs reproduce rc1 too. Public
  configuration variants reject Zicntr without time source and CLINT without
  mapped region. Failed processes receive no credit. No submodule internals.
- [x] **NO REGRESSION / LOCKSTEP** — make ci rc0: check, gate, bench,
  smoke-bench and all books green (Rust core163 / DSP17 / verify198).
  First CI refused stale GS digest after Rust passed; regenerated before
  green rerun. Registry 4/0; schema 270 / two skips; freeze three versions /
  zero findings; gate controls 17/0. Python identity: 316 other guest files,
  four contract/version files and registry exact. GUEST-GEN 137 arms, project
  total 641; README routes profiles 3120707/3145728 B, fixed ceilings
  unchanged. git diff --check rc0. Current matrix 483 boundaries and
  summary 68 checks corrected; book/toolbox/profile/pointer synchronized.
  LIVE_STATUS now 641 arms; P4 12/18 and 46 chapters unchanged. No new
  contract credit: 68/114. Next c13a2 architecture/author/state/v2 repair.
  promotion: declined (tracked diagnostics, current protocol and worked runtime book retain the evidence and correction).

`P4-SYSTEM.13` slice (c13 diagnosis) (`2026-10-10`, `SEMULITH-P4-0126`):

- [x] **WITNESS ROOT CAUSE** — python3 in-memory author replay rc=0: forced S timer refusal still
  matches mm-stimecmp: 35 boundaries / 70 parcels; last step traps cause 2,
  mepc=0x80000044. Budget ends at a zero-valued read, with no distinguishing
  register change. Corpus source census in c13 decision records the scope.
- [x] **ARCHITECTURAL ROOT CAUSE** — rustc public csr_write/csr_read probe
  compiled against current core exits 101: STCE=0, stimecmp=MAX, write
  mip.STIP=1, observed 0 instead of required 32. Pinned machine 2.1.1.18/
  2.1.1.9 fallback clauses re-read; three artifact pins match. git log -S
  and git show 47badd2 locate unconditional computed overlay at P4.2 d.
  Frozen v1 source wording also identified, not rewritten.
- [x] **OWNED / SCHEDULED** — rg c13a1/c13a2/c13b in this tree reports
  all three owned stages: c13a1 nine-guest
  explicit-enable preparation, c13a2 dynamic STIP/author/state/v2 repair,
  and c13b registered direct S programming/refusal witnesses. Priority before
  any SSTC credit. Keep cold STCE=0; all behavior milestones require full CI.
  This bounded unit completes diagnosis/design, not either defect's closure.
- [x] **NO REGRESSION / LOCKSTEP** — Python identity: 340 contract/
  guest/author files byte-exact; git diff crates/scripts empty. Registry
  4 passed / 0 failed; DOSSIER-SCHEMA 270 / two skips; CONTRACT-FREEZE
  three versions / zero findings; gate controls 17 pass / 0 fail; books rc=0.
  G-CONTRACT unchanged 68/114; known limitation and next actions synchronized.
  LIVE_STATUS unchanged: P4 12/18, 639 arms, 46 chapters.
  promotion: declined (task, book and gate retain reproductions and repair ownership).

`P4-SYSTEM.13` slice (c12) (`2026-10-10`, `SEMULITH-P4-0125`):

- [x] **ROOT CAUSE** — git show 3be1785:crates/semulith-verify/src/contract_checks_rv64gc.rs:
  CHK-ZICNTR POS/NEG absent. RVI-ZICNTR rehash: 40747 B,
  8d619d6ef71d6cd87415342782aa615a0aff121a537342e4497658947f4fa81c.
  Read owners/views, full guest observations, permission/timekeeping paths
  and book. Exact profile/CSR scope already excludes Zihpm.
- [x] **ADDRESSED** — cargo test -p semulith-verify contract_checks_rv64gc:
  4 passed / 0 failed. POS mm-counters, NEG mm-csr-ro-counters.
  Independent replay 101 boundaries / 202 parcels exact. Existing author
  gate controls rc1 with counter mode enable gate; in-memory read-only
  bypass fails at step 9 (x5=9 instead of sentinel 7). Coverage now 68.
- [x] **NO REGRESSION** — make check rc=0: core 163 / DSP 17 /
  verify 198. Existing core counter_gating_mcounteren_then_scounteren:
  1 passed / 0 failed, including S TIME. Counter author: 30 mode gates,
  117 corpus steps and 42 owned records exact. 66 prior entries / 340
  contract/guest/author files exact. DOSSIER-SCHEMA 270 / two skips;
  freeze three versions / zero findings; gate controls 17/0; books rc=0.
- [x] **CONTAINMENT** — Python ordered inverse reconstruction exact:
  25612 B designs + 26817 B acceptance moved verbatim to archive part 7,
  52711 B; active owned head 126563 -> 74439 B before new receipts.
  SHA256 5b9c5f51506236994e0617d875990ed17e4712cf539b85f6de17042e580c3225.
  Both moved blocks also match committed 3be1785 bytes; old archives and
  all fixed ceilings/finite archive descriptors unchanged.
- [x] **LOCKSTEP** — git diff --check rc=0. Current table, book and
  pointer agree on 68/114, 23 pairs then freeze. LIVE_STATUS unchanged:
  P4 12/18, 639 arms, 46 chapters. .14 retains status/experiment ownership.
  promotion: declined — registry, canonical selection and runtime book
  retain evidence/limits; c13 Sstc next, v2 stays open.

`P4-SYSTEM.13` slice (c11) (`2026-10-10`, `SEMULITH-P4-0124`):

- [x] **ROOT CAUSE** — git show c0507d0:crates/semulith-verify/src/contract_checks_rv64gc.rs:
  frozen CHK-IALIGN-16 POS/NEG absent. RVI-C rehash: 95631 B,
  3f7e7d853d6e12e9d44c3d1bb488d1c312179a308d608182fb01db43a49d6aeb.
  Reviewed full meaningful source (zero padding counted), expected steps,
  parcel/SetPc paths and C/runtime book; no production defect found.
- [x] **ADDRESSED** — cargo test -p semulith-verify contract_checks_rv64gc:
  4 passed / 0 failed. POS c-links/c-page-end/sv39-straddle; NEG
  c-page-straddle. Independent replay: four programs, 165 boundaries,
  319 parcels, all changes/counts exact. In-memory four-byte parcel/PC,
  compressed over-fetch and wrong second-parcel tval controls fail at
  steps 0/3/45/46. Required coverage extends to 66 without weakening guards.
- [x] **NO REGRESSION** — make check rc=0: core 163 / DSP 17 /
  verify 198; Python identity: 64 prior bindings and 340 input files exact.
  DOSSIER-SCHEMA 270 validated, two declared skips; CONTRACT-FREEZE three
  versions / zero findings; gate_report --self-test 17 pass / 0 fail;
  make book rc=0. No production execution or expectation changes.
  First hook rejected a misplaced commit-log row in the verification table;
  restore its date prefix and move the new row to Commit Log. Recheck staged
  TABLE-ARITY-RATCHET before retry; no runtime changes needed.
- [x] **LOCKSTEP** — git diff --check rc=0. Profile table and book
  agree on 66/114, 24 pairs then freeze; .14 status/experiment ownership
  unchanged. LIVE_STATUS unchanged: P4 12/18, 639 arms, 46 chapters.
  promotion: declined — registry, immutable expectations and runtime book
  retain the finite observation/controls. c12 Zicntr next; v2 remains open.

`P4-SYSTEM.13` slice (c10) (`2026-10-10`, `SEMULITH-P4-0123`):

- [x] **ROOT CAUSE** — git show 89a62a4:crates/semulith-verify/src/contract_checks_rv64gc.rs:
  OB-SVADE's checks absent despite existing fault and full PTE witnesses.
  Read selected A/D scheme, ADUE exclusion and finish/cache permissions.
  A correct fault alone cannot establish the absence of a PTE update.
- [x] **ADDRESSED** — cargo test -p semulith-verify contract_checks_rv64gc:
  4 passed / 0 failed. Three success/PTE-read-back guests and sv39-svade
  run 434 boundaries / 868 parcels; independent replay exact. In-memory
  controls discriminate at step 90 (A/D bypass) and 133 (A write with correct
  fault causes). Whole PTE values 0x2000188f/0x2000184f remain observed.
- [x] **NO REGRESSION** — cargo test -p semulith-core
  step9_svade_faults_and_the_pte_is_byte_untouched: 1 passed / 0 failed.
  make check rc=0: core 163 / DSP 17 / verify 198. Python comparison:
  62 prior bindings and 340 contract/guest/author files byte-exact. Schema
  and freeze zero findings; gate controls 17/17; make book rc=0.
  First hook refused book part 33700 > 32768; runtime sections split with
  exact ordered reconstruction 28722+4978=33700. Routing rc=0 after fix;
  profile duplicate-progress compaction preserves detailed receipts and caps.
- [x] **LOCKSTEP** — git diff --check rc=0. G-CONTRACT 64/114 with
  25 runtime pairs then freeze; book/profile/live pointer synchronized,
  prior counts historical. LIVE_STATUS retains P4 12/18 and 639 arms;
  chapter count re-derived as 46, the only changed live metric. promotion: declined — registry, immutable expectations and
  book retain this realization. c11 IALIGN-16 next; v2 remains open.

`P4-SYSTEM.13` slice (c9b) (`2026-10-10`, `SEMULITH-P4-0122`):

- [x] **ROOT CAUSE** — git show 7569fe2:crates/semulith-verify/src/contract_checks_rv64gc.rs:
  OB-SV39's two frozen checks absent from registry; fourteen P4.3 guests
  already exist. Read translation/CSR paths, source programs with counted
  zero-word padding, expectations and book. Historical G defect owned/fixed
  separately at c9a; no old receipt rewritten.
- [x] **ADDRESSED** — cargo test -p semulith-verify contract_checks_rv64gc:
  4 passed / 0 failed. POS six translation/mode/cache/straddle guests; NEG
  eight fault/permission/Svade/delegation guests. Independent parcel author:
  14 programs, 1417 boundaries, all changes and 2832 fetch counts exact.
  Required-binding guard adds this pair; post-v0 realization guard retained.
- [x] **NO REGRESSION** — make check rc=0: core 163 / DSP 17 / verify 198.
  Python comparison: 60 prior registry entries and 339 contract/guest files
  byte-exact. Schema/freeze zero findings; gate controls 17 pass / 0 fail;
  make book rc=0. Focused checks appropriate for evidence bindings only.
- [x] **LOCKSTEP** — git diff --check rc=0. Book/profile/live pointer
  synchronized at G-CONTRACT 62/114; 26 runtime pairs then freeze remain.
  LIVE_STATUS unchanged: P4 12/18, 639 arms, 45 chapters. Finite comparison
  scope explicit. promotion: declined — bindings, canonical scope and book
  retain it; c10 OB-SVADE next, no premature version or CPU closure.

`P4-SYSTEM.13` slice (c9a) (`2026-10-10`, `SEMULITH-P4-0121`):

- [x] **ROOT CAUSE** — git show e4e657f:crates/semulith-core/src/translation.rs:
  global assigned only from leaf. Pinned supervisor 186455 B rehashed to
  d5186efc3ead1c1f693ac2b16aeccdcab95d990264f49b559252d2dc413a651a;
  read inheritance/fence rules. Both new cargo test regressions rc=101 on
  parent: wrong load access fault and premature actual ASID-fence invalidation.
- [x] **ADDRESSED** — cargo test -p semulith-core translation::tests:
  32 passed / 0 failed. Eight G masks and 32 actual fences discriminate
  inherited hits and exact retention/invalidation. Shared walk accumulates G;
  permission/fault/install owners unchanged. Cache author rc=0; its existing
  inheritance mutation rc=1 with intended non-leaf propagation assertion.
- [x] **NO REGRESSION** — make check rc=0: core 163 / DSP 17 / verify 198.
  make ci rc=0: all five legs green (check, gate, bench, smoke-bench, book).
  Python comparison: 342 contract/guest/author/registry files byte-exact;
  CONTRACT-FREEZE rc=0, three versions / zero findings. Logs under
  target/p4-system-13/c9a; no expectations fitted to the repair.
- [x] **LOCKSTEP** — git diff --check rc=0. Book/profile/live pointer
  record repaired selected-policy scope; c7b counts explicitly historical.
  LIVE_STATUS unchanged: P4 12/18, 639 arms, 45 chapters. G-CONTRACT 60/114
  and v2 open; c9b realization next. promotion: declined — implementation,
  permanent discriminating tests and book retain this local repair.

`P4-SYSTEM.13` slice (c8) (`2026-10-10`, `SEMULITH-P4-0120`):

- [x] **ROOT CAUSE** — git show e0f3dae:crates/semulith-verify/src/contract_checks_rv64gc.rs:
  no OB-PRIV-MODES binding despite the thirteen-guest P4.2 matrix. Read all
  program sources, expectation owner and shared comparison rule. Handler
  reads witness causes/EPC/status; no direct PC/mode comparison is claimed.
- [x] **ADDRESSED** — cargo test -p semulith-verify corpus_mode_matrix:
  1 passed / 0 failed; all 13 programs / 481 boundaries. Registry focused
  tests 4 passed / 0 failed, required-binding guard retains post-v0 birth
  realization and adds this old pair. POS legal-mode and NEG permission
  witnesses retain their original expected changes and refusal observations.
- [x] **NO REGRESSION** — make check rc=0: core 161 / DSP 17 / verify 198.
  Python byte comparison: all 58 prior entries and 339 contract/guest files
  exact. Schema/freeze zero findings, gate controls 17/17; make book rc=0.
  sharder completeness: 45 before = 35 kept + 10 moved, ordered bytes exact;
  SHARD-FREEZE rc=0. Fixed caps and sealed archive descriptors unchanged.
- [x] **LOCKSTEP** — git diff --check rc=0. G-CONTRACT 60/114;
  book/profile/live pointer synchronized; LIVE_STATUS reviewed unchanged
  (P4 12/18, 639 arms, 45 chapters). 27 runtime pairs then freeze remain;
  promotion: declined — exact bindings, canonical scope and book retain it.


## Runtime verification

| Date | Leaf | Checks | Result |
| --- | --- | --- | --- |
| `2026-10-10` | `.13` c16 | independent 79/158; seven mutants; smoke images 12/48 each; generated data exact; prior 76 bindings; Rust 167/17/201; report 20/0; schema/freeze/books; board pin/semantic identity/platform 11/0 | 76/114; OB-SHAMT next |
| `2026-10-10` | `.13` c15 | independent 99/198; eight countermodels; integer 22+10/471/42; identity 348+4+74; Rust 167/17/201; oracle 20/0; schema/freeze/books | 74/114; OB-LUI-AUIPC next |
| `2026-10-10` | `.13` c14b | independent62/124; five countermodels; integer22+10/471/42; identity348+4+72; Rust167/17/201; oracle20/0 | 72/114; OB-ALU-REG next |
| `2026-10-10` | `.13` c14a | original ALU-bound17/18 RED; corrected20/0; duplicate-credit mutant19/20; production AST/input identity | 70/114 unchanged; c14b OB-ALU-IMM next |
| `2026-10-10` | `.13` c13b | direct 3/0; registry 4/0; independent31/62 and terminal35/70 control; identity348+4+70; corpus 167/5360/10514; report 18/0; full CI all five legs green, Rust167/17/201, schema/freeze | 70/114; OB-ALU-IMM next |
| `2026-10-10` | `.13` c13a2 | core RED/GREEN4; author8 cases/four mutants; source27/54; identity335/52/68; public CSR0; Rust167/17/198; schema/freeze; gate18/0; lossless shard; full CI all five legs green | 68/114; c13b direct Sstc witnesses next |
| `2026-10-10` | `.13` c13a1 | independent nine-guest 281/524, full 167/5360/10514; 42 owned; two new RED controls; corrected public probe and nine attempts; identity; full CI rc0; registry/schema/freeze/gate controls | explicit setup ready; 68/114 unchanged; c13a2 next |
| `2026-10-10` | `.13` c13 diagnosis | forced S refusal missed by 35/70 terminal guest; public STCE-clear STIP regression rc101; pins/history; 340 inputs exact; registry 4/0; schema/freeze/gate 17/17/books | two defects owned before SSTC; 68/114 unchanged |
| `2026-10-10` | `.13` c12 | counter guests 101 boundaries / 202 parcels exact; three controls; core permission 1/0; author 30 mode gates; Rust 163/17/198; 66 entries + 340 inputs exact; lossless archive; focused gates/books | 68/114, v2 open |
| `2026-10-10` | `.13` c11 | four alignment programs / 165 boundaries / 319 parcels; four in-memory controls; prior 64 bindings + 340 inputs exact; Rust 163/17/198; schema/freeze/gate 17/17/books | 66/114, v2 open |
| `2026-10-10` | `.13` c10 | four Svade programs / 434 boundaries / 868 parcels; two controls incl. correct fault + bad PTE; core 1/0; Rust 163/17/198; prior 62 bindings + 340 files exact; focused gates/books | 64/114, v2 open |
| `2026-10-10` | `.13` c9b | 14 Sv39 guests / 1417 boundaries / 2832 parcels; independent author exact; prior 60 bindings + 339 files exact; Rust 163/17/198; schema/freeze/gate 17/17/books | 62/114, v2 open |
| `2026-10-10` | `.13` c9a | parent failures; eight G masks / 32 actual fences; translation 32/0; author + inheritance mutant; Rust 163/17/198; 342 files exact | make ci all five legs green; 60/114 unchanged |
| `2026-10-10` | `.13` c8 | 13 mode guests / 481 boundaries; prior 58 bindings + 339 files exact; Rust 161/17/198; schema/freeze/gate 17/17; shards/books | 60/114, v2 open |


## Runtime commits

| Leaf | Subject | Next |
| --- | --- | --- |
| `.13` c16 | `SEMULITH-P4-0133 (leaf P4-SYSTEM.13): realize signed U-immediates and instruction-address addition` | c17 OB-SHAMT |
| `.13` c15 | `SEMULITH-P4-0132 (leaf P4-SYSTEM.13): realize register ALU wrapping and operand overlap` | c16 OB-LUI-AUIPC |
| `.13` c14b | `SEMULITH-P4-0131 (leaf P4-SYSTEM.13): realize immediate ALU guarantees through boundary guests` | c15 OB-ALU-REG |
| `.13` c14a | `SEMULITH-P4-0130 (leaf P4-SYSTEM.13): remove missing-id assumptions from contract-count controls` | c14b OB-ALU-IMM |
| `.13` c13b | `SEMULITH-P4-0129 (leaf P4-SYSTEM.13): bind observable supervisor timer execution and refusals` | c14 OB-ALU-IMM, then remaining21 pairs and freeze |
| `.13` c13a2 | `SEMULITH-P4-0128 (leaf P4-SYSTEM.13): repair STCE-dependent pending and effective source evidence` | c13b direct S programming/refusal witnesses |
| `.13` c13a1 | `SEMULITH-P4-0127 (leaf P4-SYSTEM.13): prepare explicit STCE timer inputs and repair public evidence` | c13a2 dynamic STIP/author/state/v2 supersession, then direct Sstc witnesses |
| `.13` c13 diagnosis | `SEMULITH-P4-0126 (leaf P4-SYSTEM.13): own the STCE fallback defect and terminal timer witness gap` | c13a1 explicit timer enable, then architecture repair and Sstc witnesses |
| `.13` c12 | `SEMULITH-P4-0125 (leaf P4-SYSTEM.13): realize base-counter inclusion and read-only refusals` | c13 Sstc, then 22 runtime pairs |
| `.13` c11 | `SEMULITH-P4-0124 (leaf P4-SYSTEM.13): realize halfword alignment and precise parcel-fault checks` | c12 Zicntr, then 23 runtime pairs |
| `.13` c10 | `SEMULITH-P4-0123 (leaf P4-SYSTEM.13): realize Svade checks with fault and PTE-preservation witnesses` | c11 IALIGN-16, then 24 runtime pairs |
| `.13` c9b | `SEMULITH-P4-0122 (leaf P4-SYSTEM.13): realize Sv39 checks through the complete translation matrix` | c10 OB-SVADE, then 25 runtime pairs |
| `.13` c9a | `SEMULITH-P4-0121 (leaf P4-SYSTEM.13): preserve inherited-global mappings in the shared Sv39 walk` | c9b OB-SV39, then 26 runtime pairs |
| `.13` c8 | `SEMULITH-P4-0120 (leaf P4-SYSTEM.13): realize privilege-mode checks through the complete existing matrix` | c9 OB-SV39, then 26 runtime pairs |


## Runtime changelog

- `2026-10-10`: `.13` c16 (SEMULITH-P4-0133): U-immediates bind exact
  79/158 with seven sign/shift/PC/wrap alternatives caught. Correct stale smoke
  headers with exact assembled images; focused checks pass, 76/114 open.

- `2026-10-10`: `.13` c15 (SEMULITH-P4-0132): register ALU pair binds
  exact 99/198 with eight wrong alternatives caught, including overlapping sources.
  Prior inputs/bindings exact; focused checks pass, 74/114 open; OB-LUI-AUIPC next.

- `2026-10-10`: `.13` c14b (SEMULITH-P4-0131): immediate ALU pair
  binds exact62/124 corpus with five wrong semantic alternatives caught.
  Earlier inputs/bindings exact; Rust/gate oracle pass,72/114 open.

- `2026-10-10`: `.13` c14a (SEMULITH-P4-0130): shared-id oracle now
  synthetic, duplicate/full-coverage controls discriminate; actual production
  measure and70/114 unchanged. Next ALU binding no longer trips the old example.

- `2026-10-10`: `.13` c13b (SEMULITH-P4-0129): direct Execution pair
  closes terminal-zero SSTC coverage hole; S full-width programming/read-back
  and M-handler-visible refusals total31/62. Independent forced-trap and
  disabled-verifier controls discriminate; old inputs exact,70/114 open.

- `2026-10-10`: `.13` c13a2 (SEMULITH-P4-0128): dynamic STIP and source
  supersession repaired, raw retention explicit, direct27/54 and core48 cases.
  Independent author/controls and effective-report oracle repaired; old inputs
  and frozen records exact, 68/114 unchanged. Direct S witnesses next.

- `2026-10-10`: `.13` c13a1 (SEMULITH-P4-0127): explicit STCE setup
  in nine timer guests, fresh derivations/provenance and owned-record protocol;
  repair confounded public diagnostic with read-back. Full CI green; 68/114
  unchanged. Dynamic fallback and direct S witnesses remain next.

- `2026-10-10`: `.13` c13 diagnosis (SEMULITH-P4-0126): reproduce
  terminal-zero timer guest miss and public STCE-clear STIP write defect;
  root/history/pins checked. Own staged repair sequence before SSTC credit.
  No production/guest/author changes; 68/114 unchanged, defects remain open.

- `2026-10-10`: `.13` c12 (SEMULITH-P4-0125): bind base-counter
  inclusion/read-only refusal; independent 101-boundary replay exact, three
  controls discriminate; S TIME permission supporting test passes. 68/114.
  Earlier designs/acceptance archived verbatim with inverse reconstruction;
  fixed caps retained. Current table/book synchronized; c13 Sstc next.

- `2026-10-10`: `.13` c11 (SEMULITH-P4-0124): bind halfword control
  flow and translated page-edge successes/refusal; all four independent runs
  exact, four controls discriminate. 66/114; frozen/prior inputs preserved.
  Current book/profile bindings synchronized; c12 Zicntr next.

- `2026-10-10`: `.13` c10 (SEMULITH-P4-0123): bind Svade success/fault
  witnesses with full PTE read-backs. Independent replay and two controls
  discriminate even a PTE update with correct fault delivery. Prior bytes
  unchanged; focused checks/books pass, 64/114 and v2 open.

- `2026-10-10`: `.13` c9b (SEMULITH-P4-0122): bind Sv39 checks to
  all fourteen guests; independent 1417-boundary / 2832-parcel observations
  exact. Prior bytes unchanged; Rust/focused gates/books pass, 62/114 open.

- `2026-10-10`: `.13` c9a (SEMULITH-P4-0121): reproduced and repaired
  leaf-only G retention; eight path masks and 32 actual fence instructions
  discriminate. Independent author unchanged; full CI green, 60/114 unchanged.

- `2026-10-10`: `.13` c8 (SEMULITH-P4-0120): bind both privilege-mode
  checks to the full 13-guest matrix, 481 boundaries and unchanged comparison
  rule. Prior bytes exact; lossless DEV_NOTES shard 0219; 60/114, v2 open.


Active frontier: [`docs/tasks/P4-SYSTEM.md`](docs/tasks/P4-SYSTEM.md).
