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
