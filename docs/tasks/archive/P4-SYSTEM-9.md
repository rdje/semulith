# P4-SYSTEM — evidence archive 9

Captured from 5eaef2ab7df03ac40db7e810564fed35d2331795 (P4-SYSTEM.13 c26a).
Source docs/tasks/P4-SYSTEM.md: 123960 bytes, SHA256
efd367b86309c45a53ddf736352135e18ea56171f1669d43c43941626c7fb4ac.

Six payloads preserve 81,532 original bytes in source order: completed c18–c25
designs/acceptance and the complete original verification/commit/changelog
sections, whose older rows retain their historical context. The active frontier,
census and current work stay in the live tree. Historical words such as "next"
and "current" do not override canonical records, registry, GS or live frontier.

Extract after each BEGIN marker's newline and before the extra newline preceding
its END marker. Declared byte lengths and SHA256 authenticate each payload.
The inverse replaces only the new live routes/receipts/ownership with these
original payloads and reconstructs the committed source exactly. Archive8 and
every earlier part remain unchanged; fixed caps do not grow.

## design-a

<!-- BEGIN design-a bytes=15395 sha256=e491dab6fec2ab2101f8f5fab718a16a7776d3451a69cf0ce8d72449e08aa3f3 -->
### `.13` c22b — JALR target masking, owned prerequisite and realization (`2026-10-10`)

Owned on clean a8b4e4c after hooks/empty brief/actual census. Scoped review finds
an inherited documentation defect in fault-jalr-mis.s and its expectation prose:
IALIGN=32 trap/no-link assertions contradict the GC expectation and actual final
state (PC2, cause0, x5=0x80000008). The two-boundary/four-parcel budget ends on
JALR; it does not fetch the target and may not discriminate clearing bit1 too.
Root source import133e722; 2611340 adds parcels but retains old derivations. The
initial census's dir-chain candidate contains no JALR; actual dir-chase must be
reviewed. Own both misleading notes and suspected witness gap now, before credit.

**c22b1 (`SEMULITH-P4-0148`)**: review frozen OB-JALR-LSB/REQ-D-JALR-LSB,
authenticated RV32I1.1.5.1/C alignment, affected source/expectation/generation and
book. Audit relevant file history; reproduce literal normal final state, census
all JALR guests, and public isolated base-JALR table clearing both bits across the
whole167 corpus. Investigate before classifying any survivor. Correct only GC
profile source/derivation prose (keep historical basename, formal writes/budgets/
images fixed); regenerate owned guest pins. Document proven finite gap and plan
independent target-state witnesses as priority-next c22b2. Preserve base input,
core/author/frozen/90 registry and88/114 credit. Run make check, GUEST-GEN,
independent full replay/identity, focused gates/books and hooks; commit clean.

Measured c22b1 result: isolated public base-JALR table masks with~3 instead of~1.
It still satisfies all167/5365/10524 old write/never-written/fetch observations;
fault-jalr-mis finalPC changes2→0 with identical link/cause/retirement. This proves
the missing target-state observation; production table is correct. Full source
census finds six base-JALR guests (dir-chase, fault-jalr-mis, fault-fetch,
guest-control, it-prio-jump, sv39-perm-rwx). Related IALIGN prose census identifies
three GC re-derivations, each with inherited false source/expectation claims:
fault-jal-mis, fault-jalr-mis, it-prio-jump (six input files). it-prio-jump's last
step is a target fetch fault, despite its copied JALR mnemonic. Own these same-
root annotation repairs in c22b1, preserve all images/numeric writes/budgets,
and inspect all relevant source histories. c22b2 target-state repair stays next.

The first focused gate exposed a related governor constraint: GUEST-GEN's
142/145 self-test arms pass, but the real-tree mirror and two dependent controls
refuse these corrected sources because check_gc_mirror.py permits only exact
source bytes. Own its repair here before modifying it: three explicit reviewed
owner/mirror SHA256 pairs, stale-pin rejection and independent identical assembled
(value/length/PC) images; all other sources remain byte-exact. Retain seven
expectation exceptions and independent write/parcel checks. Add pinned-source
positive/negative fixtures and isolated pin/image bypass controls under GUEST-GEN,
update actual arm mirrors, rerun focused gates and full CI because the governor
changes. No global comment exemption or gate waiver. This is the same annotation
prerequisite, not additional JALR credit; c22b2 remains next after a clean commit.

**c22b2 (`SEMULITH-P4-0149`, next)**: direct literal JALR requests/state cases
must distinguish bit0 masking after signed-immediate addition, bit1 retention,
carry/negative/wrap and aliased link source as applicable. Prove isolated bad
tables and disabled observer before two Execution bindings/declaration RED;
review evidence before finalizing finite cases. Only verified work may earn
90/114 (twelve runtime pairs/freeze). .14 retains statuses/experiments. Commit/
brief/clean/actual census after each subunit; no new core defect inferred yet.

### `.13` c22b2 — direct JALR target witnesses (`SEMULITH-P4-0149`)

Owned on clean 461c1a1 after empty brief/actual census. Reviewed frozen v0
OB-JALR-LSB, unchanged REQ-D-JALR-LSB (only base jalr), authenticated
RV32I1.1.5.1/C27.1, generated correct SetPc-before-link semantics, public
step_over/environment/state API, FlatMemory and ExecutionCheck/registry/test
interfaces. Integer book retains the all-167 wrong-mask survivor and root repair.

Implement only direct verification: three POS rows (even/odd source, +2047), ten
adversarial NEG rows (bit1, low-bit carry, odd immediate, -1, -2048, RV64 wrap,
high bits, rd=rs1, rd=x0, rs1=x0), and two next-boundary target-fetch faults
(target2 and40000002). Literal words/inputs/targets/linkpc+4 precede execution;
all GPRs, PC/mode/trap/counters, exact request sequence and memory are observed.
No target fetch occurs during JALR; fault cases explicitly add one refused parcel
at the next boundary. 15 cases/17 boundaries/32 actual parcel attempts, of which
POS3/6 and NEG14/26. Confirm literal encodings/values independently spec-side.

Exercise isolated public base-JALR effects: absent mask, clearing bit1 too,
masking source/immediate before addition, unsigned immediate, 32-bit target,
wrong link and link-before-aliased-source. Require named first differences, and
an actual disabled-PC-observer source mutation must fail then restore. Add the
obligation to the completed-selection test first: missing registry RED rc=101
before two Execution bindings with unchanged companion guests. Independently
replay all167/5365/10524 and preserve prior90 bindings, all112 base/348 GC input,
core/author/generated/frozen bytes. Only then earn registry92/effective90/114;
twelve runtime pairs/freeze remain. Update task/live/book/profile/report, make
check, focused gates/books, commit/clear brief/clean actual census; .14 retains
statuses/structured experiments/registration. No new processor implementation.

Control diagnosis before binding: normal 15-case witness passes, but the proposed
link-before-target bad table also passes alias (cargo test rc=101 only because
expect_err wrongly assumed otherwise). Root tools read Frame initialization and
Sem::Reg: all GPR reads use pre_regs captured before effects, so reordering alone
is semantically equivalent. Retain that as GREEN; explicitly substitute pc+4 as
the base when rd=rs1 to model the wrong new-link read, then require alias RED.
No CPU defect inferred from an equivalent mutation; source snapshot contract
preserved. Actual disabled-PC-observer control and full replay still required.

### `.13` c23 — bounded book then XLEN

c23a (`SEMULITH-P4-0150`) owns a lossless ordered-suffix move of immediate
transfers and both JALR sections from the 31,694 B integer chapter (1,074 B
remaining under 32,768 B cap) to a control-transfer chapter. Keep every witness
byte, inverse/hash proof, navigation/SUMMARY/index/GS pointers and chapter-count
mirror synchronized; no cap or runtime credit changes. Commit clean before
Execution owned on clean 167a196 after empty brief/actual census. Review SUMMARY,
index generator, profile ENV/GS fingerprints, runtime summary and fixed book
family caps. Original integer chapter 31,694 B SHA256
9beabe26eafc6b026ab8310cddf25f3ca97919ce5787e89536725a62149c7a7b;
control suffix 9,822 B SHA256
d1da14f93bf6f352739edd2a2e784cabd4f782481fb729bc67c2b1fc05b819c0.
Whitespace check first refused a blank separator at the retained EOF (rc=2).
Move that separator with the suffix; final inverse remains exact.
Use new plan/p4/contract-control.md, preserve the leading separator and every
suffix byte. Remove only new navigation/header for exact ordered inverse.
Include new file in explicit cap census; existing 50 files/460,097 B under fixed
80/524,288/32,768. Preserve all runtime, canonical and frozen bytes; 90/114
unchanged. Update LIVE chapter count48→49, regenerate index/GS, focused gates/
all books/hooks, commit/brief/clean actual census before c23b.

c23b (`SEMULITH-P4-0151`) scoped review/realization of OB-XLEN: literal 64-bit
register/address observations plus wrong-width controls, preserving the finite
Sv39 laboratory scope. Remaining runtime pairs and final freeze then follow.

### `.13` c23b — user integer/address width (`SEMULITH-P4-0151`)

Owned on clean 529f464 after empty brief/actual census. Read frozen OB-XLEN,
REQ-D-XLEN (state, no instruction association), 64-bit integer/PC descriptors,
public state/environment/execution and Sem table interfaces, existing arithmetic
and Sv39 canonical-fault guests, typed address-unit assumption and integer book.
Authenticated RV64I3.1.1 states 64-bit registers/user addresses; supervisor Sv39
requires bits63–39 equal bit38. Preserve the selected 39-bit canonical subset;
64-bit representation does not claim all 2^64 addresses map.

Implement a direct Execution pair: two four-instruction U/Sv39 programs at
VA0x0000000100001000 (POS) and VA0xffffffff80001000 (NEG), both translated to
PA0x80001000. Each fresh root0x80002000 has exactly one 1GiB user R/W/X A/D-set
leaf, literal PTE0x200000df at root+0x20 or root+0xff0. Other entries are zero.
ADDI x7,x6,0 retains full virtual data pointer, LD x8,0(x6) loads literal64-bit
payload, SD x8,8(x6) stores it whole, AUIPC x9,0 retains full current virtual PC.
Initialize every writable GPR with independent high-bit sentinel expectations;
observe all GPRs/x0, PC/U mode, trap/counters, whole memory and exact physical
request sequence (one cold walk, eight fetch parcels, one load and one store per
case). Two cases/eight boundaries/16 parcels/22 total requests; validate words,
PTEs, translations and observations independently spec-side before binding.

Seven isolated public table controls truncate ADDI result, LD address, SD address,
LD value, SD value, AUIPC result or next PC to32 bits; each must fail a named
observation. Actual disabled-GPR auditor must let the unused x7 truncation escape,
then restore. Declaration selects OB-XLEN first and must refuse missing binding
before two Execution entries; proposed unchanged companions POS scope-alu, NEG
bound-arith/sv39-fault-canonical subject to exact replay. Preserve prior92 entries,
all112 base/348 GC input/core/author/generated/frozen bytes. Only verified work
may earn registry94/effective92/114 (eleven runtime pairs/freeze). make check,
focused gates/all books/hooks, commit/brief/clean actual census; .14 retains
statuses/experiments. No CPU implementation, wider MMU or platform map change.

Pre-derived probe rc=0: all four literal words, both root PTE addresses/values,
canonical mappings, complete GPR/PC/U/counter/memory states and fetch/walk logs
match the independent author. The author logs only walk/fetch (nine entries per
case), not data requests; do not invent independent boundary credit for LD/SD.
The actual public CPU observer must separately judge all11 requests per case.

### `.13` c24 — implicit walk requests (completed, `SEMULITH-P4-0152`)

Owned on clean 0c49b15 after complete workflow. Reviewed OB-WALK-IMPLICIT,
REQ-D-WALK-IMPLICIT, public walk/finish/cache and CPU execution, typed boundary
fixture, existing translation tests, runtime/v2 book and roadmap P4. Existing
address-units fixture already executes a three-level CPU fetch/data walk; core
fault/cache tests and XLEN/LOAD-X0 direct walks also remain. This slice binds the
missing CPU-guarantee pair; it does not claim prior walk evidence was absent.

Finite direct plan: nine successful cases (Fetch/LD/SD × one/two/three levels),
two boundaries each; eleven single-boundary refusals (A-clear Fetch/LD/SD,
D-clear SD, invalid root/middle/leaf fetch, refused root/middle/leaf LD,
noncanonical LD). Exact literal PTE paths distinguish WalkAccess, FetchParcel
and explicit Load/Store. Observe all GPRs, PC/mode/trap/counters, whole memory,
ordered requests and same-page second-boundary cache hits. Svade/fault paths
must stop without data effects or any PTE writes. Pre-derive words, paths and
complete state with independent author; explicitly retain its no-data-log limit.

Seven corrupted-capture controls alter kind, count, address, fetch kind or PTE
bytes. Disable the actual request predicate and require its control to fail;
restore. Temporarily mutate the actual walker to use Load+D/Response::Load and
to write A before faulting: each must fail a named observation, then restore
all core bytes. Select declaration first, demonstrate missing-binding RED, then
bind two Execution entries and unchanged translation/injected-fault companions.
Preserve prior94 registry bindings,112 base/348 GC canonical inputs, author,
generated/frozen data and production core. Only verified work earns registry96/
effective94/114 (ten runtime pairs/freeze). make check, independent full corpus,
focused gates/all books/hooks, commit/empty brief/clean actual census. .14 owns
statuses/structured experiments. No CPU behavior or platform mapping change.

### `.13` c25 — FENCE ordering and field treatment (completed, `SEMULITH-P4-0153`)

Owned on clean c28d531 after workflow/census. Reviewed frozen OB-FENCE/REQ-D-
FENCE, generated mask707f/Nop and public CPU semantics, one-hart provider order,
canonical fault-fence/scope-alu and runtime/memory book. Authenticated RV32I
SHA3b20e92f... confirms section1.1.7: reserved configurations execute as FENCE,
TSO may strengthen to RW,RW; rs1/rd are ignored. Negative check means adversarial
accepted configurations, never an invented illegal trap.

Own small citation defect: author RULES["fence"] cites1.1.6 (Load/Store), while
actual Memory Ordering is1.1.7. Reproduce through execute(Hart(),0x0ff0000f)'s
source; impact future stock-derived provenance, not execution/numeric values.
Full relevant line history: introduced by022f557 (P4-0086), blame unchanged;
canonical fault-fence already cites correct1.1.7. Fix only this locator and prove
exact one-line source delta; all canonical/guest/generated/frozen data unchanged.

Finite CPU plan: every4096 fm/pred/succ configuration × three modes × five
rs1/rd pairs (0/0,0/31,31/0,31/31,7/13) =61440 one-boundary cases. POS ordinary
fm0 plus exactTSO with zero ignored fields (771); NEG remaining60669 all still
must retire. Observe all GPR/FPR/26 CSR owners except normal cycle/retirement,
PC/mode/wholememory and exactly two parcels; no extra data/fetch request.
Add three four-boundary LR.D/FENCE/SC.D/LD and three three-boundary translated
ADDI/FENCE/ADDI sequences for ordinary/TSO/reserved fields. Preserve reservation
and same-page translation through actual next instructions, not hidden readback.
Prederive all words/states and author fetch/walk logs, retaining no-data-log limit.
Direct total61461 boundaries/122922 parcels, subject to actual verification.

Ten isolated table controls: reject fm, reject ignored registers, GPR/FPR/CSR
write, memory Store, trap, wrongPC, consume reservation, flush translation. Each
must fail its named actual observation. Disable actual register predicate and
require bad-write control RED; restore. Select missing declaration first, then
bind two Execution entries (companions scope-alu/fault-fence). Preserve prior96
bindings/input/core and all author bytes except exactly fixed locator; only
verified work earns registry98/effective96/114, nine runtime pairs/freeze.
make check, independent full corpus, focused gates/all six books/hooks, commit/
brief/clean actual census. Keep book example in bounded memory chapter. Next
c26 containment before further receipts; .14 retains statuses/experiments.


<!-- END design-a -->

## design-b

<!-- BEGIN design-b bytes=17819 sha256=cde6acc1a2d376d5eb049acc33d967032fb02ad46885e1649000d71e90102e53 -->
### `.13` c22a — preserve whole development receipts under fixed caps (`2026-10-10`, `SEMULITH-P4-0147`)

Owned on clean 8f3376f after hooks/empty brief/actual census. DEV_NOTES is 47,462 B
under 49,152 B fixed ceiling, leaving 1,690 B for the next verification receipt.
Reviewed sharder, split_entries/inverse contract, sealed history reader, manifest
freeze checker, route cap, current task-tree book and latest seven older entries.
Dry-run rc=0 targets 32,768 B without changing the cap: 20 entries=13 kept+7 moved,
head 31,228 B, next shard 0224. This is lossless containment, not new CPU credit.

Own original SHA256/length, run existing sharder, retain all seven entry bytes/
order (including their old footer), and append a fresh live navigation footer.
Add this unit's bounded note and prove removing only new note/footer reconstructs
exact original from kept+shard entries. Old manifest prefix/sealed archive/files
must stay exact; append only one new frozen row. Keep all code/canonical/guest/
registry/frozen bytes unchanged, effective 88/114. Update task/resume/changelog
and mdBook with the actual preservation example. Verify inverse, no-op re-run,
prior 90 bindings/112 base+348 GC inputs, focused shards/bounds/frontier/counts/
freeze/reports/schema/index/all six books and hooks. Commit/brief/clean/actual
census before c22b JALR-LSB. .14 retains statuses/experiments.

### `.13` c21b — immediate control transfers (`2026-10-10`, `SEMULITH-P4-0146`)

Owned on clean 88230fb after hooks/empty brief/actual census. Review ROADMAP P4,
CPU_ENVIRONMENT, frozen OB-NO-DELAY-SLOTS/REQ-D-NO-DELAY-SLOTS (JAL/JALR and
six conditional branches), authenticated RV32I 1.1.5, SetPc/branch semantics and
public parcel step, independent parcel author, GC comparison/registry and
integer/runtime/v2 books. Existing guest-control/scope-branch/dir-cmp-branch
carry skipped register writes; c-branches/c-links add mixed-length integration.
Current 86/114, registry 88; canonical/frozen/production bytes must stay exact.

Before credit, independently derive all selected observations, never-written
markers and fetch counts. For each of the eight base forms and five C control
forms, use an isolated wrong driver that defers a taken transfer by one actual
instruction (the source instruction length governs sequential PC). A pending
transfer applies only after that slot; the control itself keeps its correct link.
Require a named visible difference; investigate any survivor before classification.
Reproduce base/C variants through the public CPU interface with a separate
pending-PC driver; preserve the production interpreter and author. Not-taken
branches remain ordinary fall-through, not an invented duplicate boundary.

Candidate POS guest-control/c-branches; NEG scope-branch/dir-cmp-branch/c-links,
if measured evidence supports every associated form. Extend declaration coverage
and observe missing-binding RED before two Guest entries. Run make check, normal
full independent 167/5365/10524, exact prior 88 registry/112 base+348 GC input/
core/author/generated/frozen identity, focused gates/books and hooks. Only then
record 88/114, thirteen runtime pairs/freeze. .14 retains statuses/experiments.
Commit/brief/clean/actual census before next bounded pair, containing live notes
first if the fixed cap leaves inadequate room.

### `.13` c21a — retain memory witnesses in a bounded chapter (`2026-10-10`, `SEMULITH-P4-0145`)

Owned on clean 2f45c52 after hooks/empty brief/actual job census. The integer
chapter is 32,287 B under a fixed 32,768 B per-part cap (481 B headroom); the
book family is 49 tracked files/448,559 B under 80 files/524,288 B, not a file-count
blocker. Review readme route, containment policy, SUMMARY/index generator,
integer/runtime/v2 book sections, profile pointers and live count derivation.

Move exactly the LOAD-EXT, LOAD-X0 and ENDIAN section suffix into a memory
runtime chapter. Preserve every section byte and ordered reconstruction of the
committed original; add only chapter title/navigation and current summary links.
Keep caps fixed. Update SUMMARY, generated index, profile pointer/report, live
chapter count and resume/task/notes. All canonical/guest/core/author/registry/
frozen data must stay byte-exact and effective 86/114 unchanged. Verify inverse
SHA256/length, prior 88 bindings/112 base+348 GC inputs, shards/bounds/frontier/
counts/freeze/reports/schema/main+five model books and hooks. No Rust changes;
focused document verification suffices. Commit/brief/clean/actual census before
c21b NO-DELAY-SLOTS. .14 retains requirement statuses/experiments.

### `.13` c20 — little-endian byte lanes (`2026-10-10`, `SEMULITH-P4-0144`)

Owned on clean 6ea2f6b after hooks/empty brief/actual job census. Review ROADMAP
P4, CPU_ENVIRONMENT, frozen OB-ENDIAN/REQ-D-ENDIAN and selected profile field,
authenticated RV32I 1.1.6, generic typed load/store path, FlatMemory read/write,
existing DataAccess literal/auditor witnesses, scope-mem/dir-ext-matrix sources
and expectations, registry/tests and integer/v2 books. Current 84/114, registry 86.

Little-endian is this EEI's choice, not the only RISC-V choice. Byte accesses
are invariant under byte order; multi-byte values place the least-significant
byte at the lowest address. Existing cross-width legal programs can prove the
selected rule without new production code. POS scope-mem, NEG dir-ext-matrix
if isolated controls discriminate all relevant lanes; do not rely only on a
same-width store/load round trip, where paired reversals could cancel.

Before binding, independently replay both and inspect literal byte/half/word/
double observations; reverse each LH/LHU/LW/LWU/LD read and SH/SW/SD store
separately, then both directions together. Require named differences, including
in the cross-width NEG program. Check byte-address invariance with all 256 byte
values and use the existing direct B/H/W/D provider tests as composition context.
Preserve all guest/canonical/author/core/generated/frozen data. Observe missing
binding RED after extending declaration coverage, then append exact two Guest
entries. make check, full independent 167/5365/10524, prior86 registry/input
identity, focused gates/books and hooks. Only measured evidence earns 86/114;
fourteen runtime pairs/freeze then remain. .14 retains statuses/experiments.
Commit/brief/clean/actual census before c21 bounded runtime pair.

### `.13` c19 — loads into x0 retain requests and faults (`2026-10-10`, `SEMULITH-P4-0143`)

Owned before edits on clean a76bdda after full CI, commit/hooks/brief/actual job
census. Read ROADMAP P4, CPU_ENVIRONMENT, frozen OB-LOAD-X0/REQ-D-LOAD-X0
(all seven forms), authenticated RV32I 1.1.6, load/set evaluator, typed request/
failure protocol, GC runner/registry and direct-execution infrastructure, existing
memory-boundary witnesses, base x0 crossing tests and GC success/fault guests.
Integer/runtime/v2 books provide review context. Effective 82/114, registry 84.

Measured evidence limit: base run/tests pins six dir-x0-writes load crossings;
GC runner compares writes/never-written/fetches and discards returned memory.
The success guest's empty register observations alone cannot distinguish an erased
load. Initial c19 isolated-author probe also leaves fault-ld-x0-fault writes
unchanged, contrary to the probe's assumption. Own this surprising fault-witness
gap now: trace the GC comparison and both fault fixtures, reproduce through the
public table interface/full corpus, and repair with the direct NEG trap/request
witness before credit. No processor defect is inferred. Preserve existing guest bytes and add a direct GC request observer,
without inventing side-effecting platform memory or duplicating CPU semantics.

Use literal LB/LH/LW/LBU/LHU/LWU/LD x0,0(x5) words. POS requires exactly one
width/address load request, unchanged GPRs/x0, PC+4, two parcels and retirement.
NEG requires load access fault for all seven, misalignment for five wider forms,
and Sv39 invalid-PTE load page fault for all seven with an explicit implicit walk.
Check original EPC/tval/cause, handler PC, no retirement and exact request lists.
Companion POS guests scope-mem/dir-x0-writes and NEG fault-ld-x0-fault/-mis
retain their corpus rule. A fixture log observes crossings, not a new I/O contract.

Before credit, prove fourteen independent public bad tables (each form erased or
duplicated) rejected by success witnesses, erased forms rejected by fault witness,
and enabled/disabled fault-injection controls discriminate. Extend declaration
coverage to 86 and observe missing-entry RED before adding Execution bindings.
Run focused tests then make check, independent full167/5365/10524, exact prior84
registry and112 base/348 GC inputs/production/author/generated/frozen identity,
focused reports/freeze/schema/counts/bounds/books and hooks. Only then record
84/114 (fifteen runtime pairs/freeze remain). .14 retains statuses/experiments.
Commit/brief/clean/actual census before c20 endian or next bounded runtime pair.

### `.13` c18b — independently realize load extension and store truncation (`2026-10-10`, `SEMULITH-P4-0141`)

Owned before edits on clean 6726658 after c18a hooks/brief/actual job census.
Reviewed ROADMAP P4, CPU_ENVIRONMENT, frozen OB-LOAD-EXT and owner/mirror
REQ-D-LOAD-EXT (all eleven associated forms), pinned RV64I 3.1.3/RV32I 1.1.6,
semantic load/store definitions, generic evaluator/environment access contracts,
existing core tests, GC runner/registry and scope-mem/bound-ext/dir-ext-matrix
sources/expectations. Integer/v2 book is the review surface. Current 80/114.

Before credit, derive selected whole-program observations independently and
prove the seven load/four store forms, signed edges, zero/ones and cross-width
lanes. POS scope-mem, NEG bound-ext plus dir-ext-matrix if their measured matrix
supports every clause. NEG means legal semantic counterexamples, not target traps.
Use isolated author copies for each signed/unsigned extension reversal, LD low-word
truncation, each narrow store's high-bit selection/overwide write/saturation and
SD low-word truncation. Each must fail a named committed observation; investigate
any survivor through full corpus and public interface before classification or
credit. Preserve all existing inputs, production rules, author and frozen records.

Only after discrimination, append the two registry bindings, extend declaration
coverage/count to 84, and observe the gate's missing-entry RED before registration.
Run make check, full independent 167-program comparison, exact prior 82 bindings/
112 base+348 GC inputs/production/generated/frozen identity, focused reports/freeze/
schema/counts/bounds/books and hooks. Update effective 82/114 (sixteen pairs/freeze
remain) only after actual evidence passes; .14 retains statuses/experiments.
Commit/brief/clean/actual census before priority-next c18c source identity repair,
then c19 LOAD-X0 or the next bounded runtime pair.

### `.13` c18c — source identity refusal on fetched citation route (`2026-10-10`, `SEMULITH-P4-0142`)

Owned at discovery during c18b, before any repair. Reproduction: sha256sum on
`target/sources/riscv-v20260120/{rv32,rv64}.html` differs from sources.sexp,
while `.materials/riscv/pinned-v20260120/unpriv/` matches exact pins. Byte diff
isolates a single Antora UI-version meta value on each page (same byte lengths);
architectural bodies unchanged. This explains the local mismatch but does not
make the fetched copies pinned artifacts. c18b must review the authenticated
cache copy before signoff and cannot claim the working copies match.

Actual defect: check_citations._work_dir prefers any existing fetched directory,
and published reads headings without checking source sha256. The quote checker
also resolves that route directly. Thus altered fetched pages can supply green
citation evidence under an exact-source ledger. Reproduce through public checks
and isolate both locator/quote readers before patching. Priority: immediately after
c18b commit, before the next runtime pair. Add discriminating altered-byte controls
and exact pin checks to shared routing/reader ownership as appropriate; refuse
mismatch clearly without repinning, bypass or silent fallback. Preserve cache and
frozen definitions, restore only provably project-owned fetched source copies from
verified local snapshot after comparing the full declared source set. Validate
locators/quotes, both route choices/refusals, focused doctrine counts and books.
This is evidence-reader integrity, not an architectural body or processor defect.

The follow-up also owns wrapper dispatch: SEMANTICS previously checked only
materials-cache availability, despite its fetched-or-cache message. Cache errors
could become an absence skip. Both wrappers must share presence-only dispatch;
partial/corrupt evidence is present and must reach an explicit identity refusal.
The locator tool's original "not a commit gate" docstring also predates its
SEMANTICS integration; correct that scoped interface description.

Implementation ownership reaffirmed on clean 9fa6d19 after c18b commit/hooks/
brief/actual census. Read both citation tools in full affected paths, shell
wrappers/controls, SEMANTICS cache dispatch, materials resolver/manifest contract,
source schemas, source/book/doctrine documentation and derived-count ownership.
Full declared fetched source census finds intro.html also differs by the same
UI meta value: all three base HTML pages, with no architecture-body change.

First capture both public readers returning green on the mismatched directory.
Add shared verified-source-path ownership: all snapshot readers require a regular
file and exact declared SHA256/byte length before reading it; declare non-snapshot
http_status=0 skips unchanged. Locator reader and default quote corpus must call
it, preserving the explicit synthetic --pages mode. Refuse mismatch clearly with
source/path/recovery instruction; never switch to another route silently. Catch
shared refusals in quote entrypoint. Cache dispatch must also judge a fetched-only
route, preserving named absence skip. Add independent RED controls for same-size
alteration, size mismatch, absent identity and quote-path integration as appropriate;
first see new controls fail on old readers. Existing controls keep their meanings,
fixtures gain actual hashes/lengths, all test scratch remains under target.

After observed refusal, compare all three fetched pages against verified snapshot
and save a diagnostic copy on-volume, then restore exactly those project-owned
HTML pages and rehash. Keep all pins, snapshot, normative bodies and contracts
unchanged. Validate fetched/default/cache/absence routes, both public readers,
Python controls, SEMANTICS and CITATION-QUOTES controls and doctrine count, focused
book/bounds/shards/frontier/reports/freeze/schema. Full CI is warranted for this
shared evidence boundary repair before next runtime credit. Update book/live/
resume/task/notes, commit, empty brief and clear actual jobs before c19 LOAD-X0.

### `.13` c18a — bound live history and correct its current pointer (`2026-10-10`, `SEMULITH-P4-0140`)

Owned before edits on clean d5519fb after c17f hooks/brief/actual job census.
Reviewed shard_history's whole-entry inverse, live route ceilings, archive
retrieval policy, closed c17 designs/acceptance/logs, full profile ENV boundaries,
canonical contract membership/effective interrupt source and runtime/integer/v2
book. DEV_NOTES 46093 B approaches fixed 49152; profiles family near 3 MiB;
archive 7 has no room. No cap change or compressed archive lifecycle transition.

Move oldest whole DEV entries through the sharder to next shard 0223, target
32768 B, preserving ordered byte reconstruction and existing manifest prefix.
Create archive 8 for completed c17a–f task designs/acceptance/verification/commits/
changelog and the profile's appended progress history (Scope evidence onward).
Keep each moved block byte-verbatim and all orders; record hashes/byte lengths,
prove inverse against the committed baseline, and link from the live task/profile.
Retain normative interface sections and a concise current pointer to generated
GS/registry and existing book chapters. Recheck aggregate/per-part fixed bounds.

Also own the scoped doc defect found during partition review: ENV's introduction
still says v2 has 11 members, 76 effective checks and the frozen v1 STIP rule,
while canonical v2 has 12 members (including interrupt-source replacement),
registry is 80/114 and STCE selects software/comparator STIP. Reproduce from
contract.sexp, effective records and contract_measure; trace the intro's edits.
Correct the effective source/id/selection; point duplicated live totals at their
canonical derived source to avoid another hand-count drift. Historical v1 text
stays explicitly historical and byte-exact. No production or frozen-record repair.
Full section review also finds the appended runtime table calling its old 76-check
view "current", and the v2 book introduction still saying 64 checks run. Own both
as the same duplicated-summary defect. Preserve the old profile table inside the
explicit historical archive, replace live counts by canonical/current-summary
pointers, and correct the book introduction before signoff.

Update book/live/resume/notes, rederive GS after final profile edits, run shard/
bounds/frontier/counts/freeze/reports/books and exact input/registry identity.
Prove both lossless historical partitions and the separately enumerated current
wording corrections. Commit/hooks/brief/clean/actual census, then c18b LOAD-EXT.

Completed c17a–f designs and diagnostic ownership are preserved byte-verbatim in
[archive/P4-SYSTEM-8.md](archive/P4-SYSTEM-8.md#c17-designs), together with their acceptance and logs.


<!-- END design-b -->

## acceptance

<!-- BEGIN acceptance bytes=27509 sha256=d28f7f7809682a3204e46ba8775c1592db6992b212fd3e0ce5ba35a7f55123ae -->
- [x] `.13` c25 — **ROOT CAUSE**: frozen FENCE pair unbound; authenticated
  RV32I1.1.7 requires accepted reserved configs and ignored fields. Author stock
  source incorrectly points at1.1.6; execute(Hart(),0x0ff0000f) rc=0 reproduces.
  Relevant line introduced022f557 and unchanged (git log -S/blame rc=0); canonical
  fault-fence already correct. Declaration missing CHK-FENCE-POS RED rc=101.
- [x] `.13` c25 — **ADDRESSED**: all61440 field/mode/representative-register
  cases plus six reservation/translation programs GREEN rc=0. Literal direct
  total61461/122922/122934 requests; pair61500/123000 with scope-alu/fault-fence.
  Observe all GPR/FPR/26 CSR owners/PC/mode/memory/exact requests. Ten wrong
  tables reject; actual disabled-GPR predicate RED rc=101 and restored. Initial
  mask-control reason diagnosis: public ReservedDecode advances cycle without
  retirement, so CSR counter predicate fails before outcome (read step_over
  branch, rc=0). Corrected named controls GREEN rc=0. Exact stock locator-only
  correction; reserved fence fields still execute, never invented illegal traps.
- [x] `.13` c25 — **NO REGRESSION**: make check rc=0, Rust167/17/214.
  Independent61440 words/full GPR/FPR/CSR/memory states plus six integration
  programs rc=0; author logs omit nine data requests, CPU observer owns them.
  verify.py rc=0: prior96 entries/112 base+348 GC inputs/core/generated/frozen
  bytes exact; scripts/author precisely locator-only delta. Full167/5365/10524
  unchanged. Registry98/effective96/114;13 scope/23 guest/6 boundary/6 execution
  pairs (raw registry includes two superseded guest entries). Nine runtime pairs/freeze remain.
  Focused gates/all six books rc=0; hooks next. LIVE unchanged652 arms/49 chapters/P4 12/18;
  .14 retains statuses/experiments. promotion: declined (finite matrix and
  mask-retirement/log limits retained in worked memory chapter/tree).

- [x] `.13` c24 — **ROOT CAUSE**: OB-WALK-IMPLICIT unbound, not absent walk
  evidence. Existing typed address fixture executes a three-level CPU path; core
  tests and prior direct walks remain. Authenticated source identity/algorithm
  review and independent20-case literal/state/memory/fetch-walk proof rc=0.
  Declaration selects pair then refuses missing CHK-WALK-IMPLICIT-POS, rc=101.
- [x] `.13` c24 — **ADDRESSED**: twenty direct CPU cases/29 boundaries/50
  parcels/104 requests check exact WalkAccess/FetchParcel/data order, three leaf
  sizes, second-boundary cache hits and eleven fault terminations/no PTE writes.
  Seven corrupted-capture controls GREEN rc=0; actual disabled-request predicate
  RED rc=101. Actual walker Load+D with matching response and write-A-before-
  fault mutants RED rc=101 at request predicate; all production bytes restored.
  State isolation rc=0: successful walk-as-Load paths retain exact memory/state
  with request predicate disabled. All-case state-only probe RED rc=101 at
  Denied(1): a Load bypasses the observer's Walk-only refusal. This limits the
  equivalence claim; production behavior is correct. Write-A with request guard
  disabled still memory-RED rc=101; request+memory guards disabled yields exact
  original trap/state GREEN rc=0. Restored make check rc=0.
  Unchanged companion188/376 POS+255/510 NEG, total pair472/936. State includes
  all GPR/PC/mode/status/satp/trap/counters and complete memory, not trace fields.
- [x] `.13` c24 — **NO REGRESSION**: make check rc=0, Rust167/17/212. verify.py
  rc=0: prior94 registry bindings,112 base/348 GC inputs/core/author/generated/
  frozen bytes exact; full independent167/5365/10524 unchanged. Effective94/114,
  registry96;13 scope/23 guest/6 boundary/5 execution pairs, ten runtime pairs/
  freeze. Focused gates/all six books rc=0. Hooks precede c25. LIVE unchanged652 arms/49 chapters/
  P4 12/18; .14 retains statuses/experiments. promotion: declined (finite request
  matrix and author data-log limit retained in runtime chapter/tree).

- [x] `.13` c23b — **ROOT CAUSE**: OB-XLEN declared/unbound. Authenticated
  RV64I3.1.1 fixes 64-bit registers/addresses; Sv39 canonical subset retained.
  Four words/two PTEs/mappings and independent GPR/PC/U/memory/fetch-walk proof
  rc=0. Declaration test selects XLEN and refuses missing CHK-XLEN-POS, rc=101.
  The author's log excludes data requests; actual CPU observer owns that evidence.

- [x] `.13` c23b — **ADDRESSED**: literal U/Sv39 programs at VA 0x100001000
  and 0xffffffff80001000 map to PA0x80001000. Independent high-bit expectations
  observe all GPR/PC/U/UXL/trap/counters/memory and 22 actual requests (8/16).
  Seven narrow public effects fail both cases (14 combinations); disabled-GPR
  source auditor lets unused x7 truncation escape (cargo test rc=101), restored
  witnesses rc=0. Two Execution entries plus exact companions yield 128/256.
  Book retains mappings, words and limits; no production map/MMU change.

- [x] `.13` c23b — **NO REGRESSION**: make check rc=0 (Rust 167/17/210).
  verify.py rc=0 proves prior 92 registry entries, all 112 base/348 GC canonical/
  guest inputs, core/author/generated/schema/doctrine/frozen bytes exact and
  full independent 167/5365/10524 unchanged. Registry 94/effective 92/114;
  thirteen scope/23 guest/six boundary/four execution pairs, eleven runtime
  pairs/freeze remain. Focused gates rc=0 (GUEST-GEN147, 226 frozen rows,
  fixed bounds, 33 frontiers, six derived claims, 40 index rows, frozen contracts,
  five fresh reports, schema270/two named skips); all six books rc=0. Whitespace
  rc=0. Hooks precede c24 WALK-IMPLICIT.
  LIVE_STATUS unchanged (652 arms,49 chapters,P4 12/18); .14 retains statuses/
  experiments. promotion: declined (finite width witnesses and author-log limits
  retained with worked examples in book/tree).

- [x] `.13` c23a — **ROOT CAUSE**: integer book is 31,694/32,768 B,
  leaving 1,074 B before XLEN and remaining runtime receipts. Ordered suffix
  census 9,822 B covers immediate transfers and both JALR sections; source hash
  9beabe26eafc6b026ab8310cddf25f3ca97919ce5787e89536725a62149c7a7b.
  verify.py rc=0 confirms source reconstruction and fixed caps; no cap increase.

- [x] `.13` c23a — **ADDRESSED**: exact suffix moved to contract-control.md,
  9,822 B SHA256 d1da14f93bf6f352739edd2a2e784cabd4f782481fb729bc67c2b1fc05b819c0.
  Remove only new link/header and concatenate prefix+suffix to restore all 31,694 B
  with original hash (verify.py rc=0). Integer/control 21,969/10,013 B. SUMMARY,
  index, v2 runtime summary, profile ENV/GS and resume follow the move.

- [x] `.13` c23a — **NO REGRESSION**: verify.py rc=0 proves all 92 registry/
  core/author/generated/schema/doctrine/frozen bytes and 112 base/348 GC canonical/
  guest inputs exact; effective 90/114 unchanged. Explicit new-file census 51
  under 80/524,288/32,768 fixed caps (51 files/460,743 B). No Rust code changed.
  Focused gates rc=0 (226 frozen rows, fixed routes, 33 frontiers, six derived
  claims, 40 index rows, frozen contracts/five fresh reports); all six books
  rc=0. Whitespace rc=0. Hooks precede c23b XLEN. LIVE_STATUS changes only chapters 48→49;
  doctrine 652 arms/P4 12/18 unchanged. .14 retains statuses/experiments.
  promotion: declined (existing bounded suffix protocol; exact evidence retained).

- [x] `.13` c22b2 — **ROOT CAUSE**: old all-167 GC observations admit
  base-JALR bit-1 erasure (c22b1 public reproduction rc=0). Declaration coverage
  now selects OB-JALR-LSB and refuses the missing binding, cargo test rc=101
  naming CHK-JALR-LSB-POS. Literal words/targets authenticated spec-side rc=0.
  Initial reordered-link control was equivalent; Frame pre_regs/Reg root read
  identifies why (initial witness test rc=101 from incorrect expect_err).

- [x] `.13` c22b2 — **ADDRESSED**: 15 direct literal cases/17 boundaries/
  32 actual parcels observe every GPR, target/link, mode/trap/counters, exact
  requests and memory. Eight bad public effects fail named observations; the
  reordered effect remains GREEN, explicit new-link alias effect RED. Actual
  disabled-PC observer lets bit-1 erasure escape, test rc=101; restored witness
  tests rc=0. Offline independent author matches all 15/17/32 (verify.py rc=0).
  Two Execution entries plus companion guests total53/103; book retains matrix.

- [x] `.13` c22b2 — **NO REGRESSION**: make check rc=0 (Rust167/17/208).
  verify.py rc=0 proves prior90 registry bindings, all112 base/348 GC canonical/
  guest inputs, core/author/generated/schema/doctrine/frozen bytes exact and
  full independent167/5365/10524 unchanged. Registry92/effective90/114;
  thirteen scope/23 guest/six boundary/three execution pairs, twelve runtime
  pairs/freeze remain. Focused gates rc=0 (GUEST-GEN147, 226 frozen shards,
  fixed bounds, 33 frontiers, six derived claims, 40 index rows, frozen contracts,
  five fresh reports, schema270/two named skips); all six books rc=0. Whitespace
  rc=0. Hooks precede c23a lossless book containment then c23b XLEN. LIVE_STATUS unchanged (652 arms,48 chapters,
  P4 12/18). .14 retains statuses/experiments. promotion: declined (finite
  target/request witnesses and equivalent-control diagnosis retained in book/tree).

- [x] `.13` c22b1 — **ROOT CAUSE**: mirror import133e722 retains base
  IALIGN=32 trap/no-link prose in six files despite GC numeric link writes;
  2611340 adds parcels only. Relevant histories audited through base roots
  a199ccf/25862a2. Literal normal final states reproduce. Public isolated base
  JALR `&~3` table still satisfies all 167/5365/10524 old observations while
  finalPC2→0 and target-fault EPC/tval40000002→40000000. Reproduction offline
  Cargo client (`target/p4-system-13/c22b1/engine/Cargo.toml`), rc=0. Full source
  census gives six JALR guests; initial dir-chain proposal was not a witness.
  GUEST-GEN initially refuses corrected source bytes (142/145 pass, rc=2).

- [x] `.13` c22b1 — **ADDRESSED**: authenticated RV32I1.1.5.1/C27.1
  guide six annotation repairs: legal halfword jumps/link writes, declared budgets,
  next target fetch fault and corrected final mnemonic. Historical names/base
  files preserved. Numeric writes/budgets/images exact; generated Rust changes
  only six input hashes (`python3 target/p4-system-13/c22b1/identity.py`, rc=0).
  Book retains three literal states and public survivor. Missing target witness
  owned priority-next c22b2 with direct state/bad-table/disabled-observer plan;
  no JALR credit added here. make check rc=0 (Rust 167/17/206). Three reviewed
  source pairs now require exact owner/mirror hashes and identical assembled
  images; stale exceptions, changed pins and changed images reject. Direct
  governor/self-test rc=0; isolated pin/image bypasses rc=1.

- [x] `.13` c22b1 — **NO REGRESSION**: 112 base files byte-exact;342 GC
  files byte-exact plus six metadata-only exceptions; all executable fixture
  arrays, 90 registry/core/author/definitions/schema/doctrine/frozen bytes exact.
  Normal independent 167/5365/10524 exact (same identity script rc=0). Registry 90,
  effective 88/114 unchanged; thirteen runtime pairs/freeze. GUEST-GEN rc=0
  (147/0 self-test); make ci rc=0 (check, all doctrines, bench, smoke-bench,
  main plus five model books). Whitespace rc=0; hooks precede c22b2. LIVE_STATUS changes only doctrine
  arms 650→652 (48 chapters / P4 12/18 unchanged); .14 retains statuses/experiments. promotion: declined (worked
  target-state distinction, retained source history and owned repair in book/tree).

- [x] `.13` c22a — **ROOT CAUSE**: measured DEV_NOTES 47,462 B under
  fixed 49,152 B cap (1,690 B room). Existing sharder dry-run rc=0 targets 32,768 B,
  predicts 20=13 retained+7 moved and head 31,228 B; preserve whole receipts before
  further feature work. `python3 scripts/shard_history.py --head DEV_NOTES.md
  --max-bytes 32768 --dry-run` reproduces the route and exact prospective partition.

- [x] `.13` c22a — **ADDRESSED**: existing sharder rc=0 moves seven oldest
  entries into shard 0224, suffix 16,234 B SHA256 0ad12ca063f04407f2aee04a06b2bec7a250050fc9135d5f8044f0bed7631af1.
  Remove only new c22a receipt/navigation footer and reconstruct original 47,462 B
  SHA256 8f3064fc70b5929072632f333171ba281d77a926a512013ae3d827f2a9277a46 from 13+7 entries,
  order/bytes exact (`python3 target/p4-system-13/c22a/verify.py`, rc=0).
  New live navigation retained; old footer remains verbatim in archived payload.
  Re-run is a no-op rc=0; manifest appends one row only (16 live+210 sealed=226).
  Caps unchanged; book explains the preservation example.

- [x] `.13` c22a — **NO REGRESSION**: prior 15 manifest rows/frozen shards
  and sealed history/index exact; authenticated archive 210 rows. All 90 bindings/
  core/author/generated/frozen/schema/doctrine and 112 base/348 GC canonical/guest
  inputs exact; effective 88/114 unchanged (same inverse/identity script rc=0).
  No Rust changes. Focused gates/books rc=0: 226 frozen rows, 37 fixed route
  caps, 33 frontiers, six derived claims, 40 index rows, three contract versions/
  zero findings, five fresh reports, 270 schema inputs/two named skips, main+five
  model books; whitespace rc=0. Hooks precede c22b JALR-LSB. LIVE_STATUS
  unchanged (650 arms, 48 chapters, P4 12/18); .14 retains statuses/experiments.
  promotion: declined (existing whole-entry policy; exact preservation proof
  retained here, in the live receipt and book example).

- [x] `.13` c21b — **ROOT CAUSE**: NO-DELAY-SLOTS remained declared/
  unbound. Authenticated RV32I 1.1.5 and canonical eight associations reviewed;
  declaration gate observed missing CHK-NO-DELAY-SLOTS-POS rc=101
  (`target/p4-system-13/c21b/registry-red.log`). Existing negative register writes
  distinguish delayed taken transfers; independently derived all five guests and
  normal corpus (`python3 target/p4-system-13/c21b/probe.py`, rc=0).

- [x] `.13` c21b — **ADDRESSED**: POS guest-control/c-branches, NEG
  scope-branch/dir-cmp-branch/c-links, all eight base and five C control forms
  over 63/111. Thirteen isolated author drivers defer a named taken transfer by
  one actual instruction, with correct links/lengths; every one fails. Separate
  public delayed-PC driver reproduces all thirteen first differences; normal
  driver retains writes/never-written/fetches (offline Cargo client
  `target/p4-system-13/c21b/engine/Cargo.toml`, rc=0). Book retains exact matrix.
  make check rc=0 (Rust 167/17/206) after exact two Guest entries.

- [x] `.13` c21b — **NO REGRESSION**: independent full 167/5365/10524 exact;
  all prior 88 registry entries and 112 base/348 GC canonical+guest inputs, core/
  author/definitions/generated/frozen bytes exact (`python3
  target/p4-system-13/c21b/identity.py`, rc=0). Registry 90, effective 88/114;
  taxonomy 13 scope/23 guest/6 boundary/2 execution pairs. Thirteen runtime pairs/
  freeze remain. Focused gates/books rc=0: 225 frozen rows, 37 fixed route caps,
  33 frontiers, six derived claims, three contract versions/zero findings, five
  fresh reports, 270 schema inputs/two named skips, main+five model books;
  whitespace rc=0. Hooks precede c22a live-note containment then c22b JALR-LSB. LIVE_STATUS unchanged (650 arms, 48 chapters, P4 12/18).
  .14 retains statuses/experiments. promotion: declined (worked control-flow
  matrix and finite evidence limits retained in the integer book/owning tree).

- [x] `.13` c21a — **ROOT CAUSE**: measured integer book 32,287 B under
  fixed 32,768 B part cap (481 B room). Family 49 tracked files/448,559 B under
  80/524,288, so a bounded split is available. Existing examples must remain
  reviewable before further feature work. Source hash/length verified with
  `python3 target/p4-system-13/c21a/verify.py`, rc=0.

- [x] `.13` c21a — **ADDRESSED**: move ordered LOAD-EXT/LOAD-X0/ENDIAN
  suffix, 10504 B SHA256 098a50b7a66bd45c39c91dbf5a73025e75f7720c16a2397a00ef61db9d241109,
  with section bytes/separator intact. Removing only new header/navigation
  reconstructs original 32,287 B SHA256 37589ade3b38e2065f8399cb7f475d74b0c2209636b33e836aa69a6629f64c28.
  Inverse proof rc=0 (`target/p4-system-13/c21a/verify.py`); chapter sizes
  21,872/10,782 B. SUMMARY/index/v2/profile links and live count follow; caps fixed.

- [x] `.13` c21a — **NO REGRESSION**: all prior 88 registry entries,
  core/author/generated/frozen/schema/doctrine bytes and 112 base/348 GC canonical/
  guest inputs exact; effective 86/114 unchanged (same verification rc=0).
  New file included in explicit cap census: 50 files/449,248 B under fixed
  80/524,288, each part ≤32,768 B. No Rust changes. Focused gates/books rc=0:
  225 frozen rows, 37 fixed route caps, 33 frontiers, six derived claims, index
  40 rows, three contract versions/zero findings, five fresh reports, 270 schema
  inputs/two named skips, main+five model books; whitespace rc=0. Hooks precede
  c21b NO-DELAY-SLOTS. LIVE_STATUS chapters 47→48; arms 650/P4 12/18 unchanged. .14 retains statuses/
  experiments. promotion: declined (exact preservation proof retained here/DEV;
  existing fixed containment policy governs the split).

- [x] `.13` c20 — **ROOT CAUSE**: ENDIAN remained declared/unbound. Gate
  observed missing CHK-ENDIAN-POS (`cargo test -p semulith-verify
  every_check_bound_through_the_scope_slice_is_realized`, rc=101). Authenticated
  RV32I 1.1.6 and canonical little selection reviewed; byte order is an EEI choice.
  Scope-mem's all-ones SH is symmetric under reversal, so its success observations
  alone are insufficient. Independent cross-width probe confirms the NEG matrix
  discriminates (`python3 target/p4-system-13/c20/probe.py`, rc=0).

- [x] `.13` c20 — **ADDRESSED**: bind scope-mem POS and dir-ext-matrix NEG,
  all eleven integer load/store forms over 64/128. Nine isolated author copies
  (five reads/three writes/both directions) fail NEG at named steps. Independent
  public H/W/D read/write/both provider variants also fail all nine; B variants
  leave both guests exact and all 256 public byte values preserve address/value
  (`target/p4-system-13/c20/engine/Cargo.toml`, offline Cargo run rc=0). Same-width
  round-trip symmetry cannot evade the cross-width witnesses. make check rc=0,
  Rust 167/17/206, after exact two registry entries.

- [x] `.13` c20 — **NO REGRESSION**: normal independent 167/5365/10524 exact;
  prior 86 bindings/112 base+348 GC canonical/guest inputs, core/definitions/
  author/generated/frozen bytes exact (`python3 target/p4-system-13/c20/identity.py`,
  rc=0). Registry 88, effective 86/114, fourteen runtime pairs/freeze remain;
  taxonomy 13 scope/22 guest/6 boundary/2 execution pairs. Focused gates/books
  rc=0: 225 frozen rows, 37 fixed route caps, 33 frontiers, six derived claims,
  three contract versions/zero findings, five fresh reports, 270 schema inputs/
  two named skips, main+five model books. Hooks precede c21a bounded book
  partition then c21b NO-DELAY-SLOTS. .14 retains
  statuses/experiments. LIVE_STATUS unchanged (650 arms, 47 chapters, P4 12/18).
  promotion: declined (worked lanes, symmetry controls and finite limits retained
  in the integer book and owning task).

- [x] `.13` c19 — **ROOT CAUSE**: old GC corpus rule lacks data-request/final
  trap observations. Initial probe's presumed fault discrimination was false;
  investigated before credit. Isolated author and independent public conditional
  x0-erasure table both satisfy all 167/5365/10524 old observations, but fault
  PC/cause/EPC/tval/retirement differ. Root mirror 133e722, original fixtures
  a199ccf, registry reuse 072b211; base-specific checks remain valid. No core bug.
  `python3 target/p4-system-13/c19/probe.py` and public offline Cargo client
  (`target/p4-system-13/c19/engine/Cargo.toml`), rc=0. Book retains exact states.

- [x] `.13` c19 — **ADDRESSED**: all seven literal encodings now require exact
  request sequences and trap/PC/GPR/mode/cycle/retirement/memory state. Direct
  success/access/alignment/page cases 26/52 plus companion 52/104 =78/156.
  Seven erased and seven duplicate public tables refuse; erasure fails all 19
  applicable fault cases. Disabled observer makes terminal control RED rc=101
  (`target/p4-system-13/c19/disable-observer.py`), restored exact; disabled
  access-fault injection refuses. Missing registry declaration first RED rc=101,
  then exact two Execution bindings. make check rc=0 (Rust 167/17/206).

- [x] `.13` c19 — **NO REGRESSION**: prior 84 bindings and 112 base/348 GC
  canonical/guest inputs, core/author/definitions/generated/frozen exact
  (`python3 target/p4-system-13/c19/identity.py`, rc=0). Registry 86, effective
  84/114; thirteen scope/twenty-one guest/six boundary/two execution pairs.
  Fifteen runtime pairs/freeze remain; .14 retains statuses/experiments. Focused
  gates/books rc=0: 225 frozen rows, 37 fixed route caps, 33 frontiers, six
  derived count claims, three contract versions/zero findings, five fresh reports,
  270 schema inputs/two named skips, main+five model books; whitespace rc=0.
  Hooks precede c20 ENDIAN. LIVE_STATUS unchanged (650 arms,
  47 chapters, P4 12/18). promotion: declined (worked literal matrix, root cause,
  public counterexample and evidence limits retained in integer book and task).

- [x] `.13` c18c — **ROOT CAUSE**: actual public locator/quote tools returned
  rc=0 on three mismatched fetched source hashes; exact diff is Antora metadata,
  all architectural bytes unchanged. Roots 32b72dbc/3afd2757/bf2070a7: neither
  final reader authenticated the preferred path. SEMANTICS checked only cache
  availability and swallowed route errors. New controls observed before patch:
  `python3 scripts/check_citations.py --self-test` rc=1, 15 pass/3 fail;
  `scripts/check_citation_quotes.sh --self-test` rc=1, 14 pass/1 fail, accepted
  altered default quote page. Reproduction/impact/ownership retained in c18c plan.

- [x] `.13` c18c — **ADDRESSED**: shared exact file/SHA256/byte-length
  verification and presence-only dispatch. Locator 21/0, quote 15/0, SEMANTICS 8/0
  (`python3 scripts/check_citations.py --self-test`,
  `scripts/check_citation_quotes.sh --self-test`,
  `scripts/check_semantics_corpus.sh --self-test`, rc=0 each). Actual bad pages
  refused by tools/wrappers rc=1/2/1/2, naming source and hash. Seven route cases
  discriminate (`python3 target/p4-system-13/c18c/routes.py`, rc=0). Authenticate
  snapshot 72/0, save old copies, verify metadata-only difference and restore
  exactly three fetched files/226648 B, unchanged pins. All new test paths local
  and relative. Knowledge card/index and book/toolbox/doctrine interfaces updated.

- [x] `.13` c18c — **NO REGRESSION**: all 84 registry/core/author/generated/
  frozen/canonical definitions and 112 base/348 GC inputs byte-exact; unchanged
  82/114 (`python3 target/p4-system-13/c18c/identity.py`, rc=0). Public locators
  resolve 10 semantic files/12 bindings; quote corpus 118 attributed/0 findings,
  88 unattributed, DS00002266B×2/LIMITATIONS×1 uncheckable. `make ci` rc=0, all five legs green: Rust 167/17/203, all doctrines, bench,
  smoke bench, main+five model books. Bounds/counts/reports/freeze/schema included
  in that gate; focused identities/controls/routes also rc=0. LIVE_STATUS only arms 649→650; chapters 47/P4 12/18 unchanged. Lesson
  promoted to existing source-identity card and index. Hooks/brief/clean/census
  precede c19 LOAD-X0; no registry or processor credit is added by this repair.

- [x] `.13` c18b — **ROOT CAUSE**: frozen LOAD-EXT's eleven instruction
  associations were declared but unbound. Reviewed authenticated RV64I 3.1.3 /
  RV32I 1.1.6, definitions/evaluator, runner and existing memory matrix. Literal
  8/16/32 sign-edge arithmetic and zero overwrite agree with committed values.
  Missing-entry reproduction: `cargo test -p semulith-verify every_check_bound_through_the_scope_slice_is_realized`,
  rc=101, OB-LOAD-EXT declares CHK-LOAD-EXT-POS with no registry entry.

- [x] `.13` c18b — **ADDRESSED**: POS scope-mem, NEG bound-ext/dir-ext-matrix, 111 boundaries/
  222 parcels and all eleven forms. Seventeen isolated author copies reject six
  extension reversals, LD/SD low-word truncation, three high-bit selections, three
  overwide stores and three saturating stores at named book observations.
  `python3 target/p4-system-13/c18b/probe.py` rc=0. Declaration gate first
  missing-entry RED (`cargo test -p semulith-verify every_check_bound_through_the_scope_slice_is_realized`,
  rc=101); registered exact two bindings, make check rc=0 (Rust 167/17/203).

- [x] `.13` c18b — **NO REGRESSION**: independent full 167/5365/10524 replay exact, all prior
  82 bindings and 112 base/348 GC input files/production/generated/frozen bytes
  exact (`python3 target/p4-system-13/c18b/identity.py`, rc=0). Registry 84,
  effective 82/114; sixteen runtime pairs/freeze remain. Focused gates/books and
  hooks precede priority-next c18c. Focused gates rc=0: 225 frozen rows, 37 route
  caps, 33 frontiers, five derived counts, three contract versions/zero findings,
  five fresh reports, 270 schema inputs/two skips, main+five model books.
  Source-pin mismatch root isolated to Antora
  metadata; authenticated cache hashes match and supplied review, reader defect
  owned immediately next. LIVE_STATUS unchanged (649 arms, 47 chapters, P4 12/18).
  promotion: declined (worked matrix/controls retained in integer book; separate evidence-reader integrity repair owned in c18c).

- [x] `.13` c18a — **ROOT CAUSE**: five completed task-history classes and eight
  whole DEV entries approached fixed caps; profile progress duplicated stale live
  claims (11 members/76 checks/v1 STIP) and book introduction said 64 checks.
  Canonical reproduction gives 12 v2 members, effective 80/114 and STCE selection.
  Blame roots e0f3daea/01154383/75c20ff0/c0507d02; no production defect.
  **ADDRESSED**: archive 8 retains all six payloads with exact lengths/SHA256;
  five task classes match committed d5519fb and all remaining segments keep order.
  DEV inverse 21=13+8 restores SHA0f5b1aae…2167f; owned task inverse restores
  SHA6dc33f90…bac7; profile history 22982 B SHA8702aa88…e184. Manifest prefix
  and sealed history exact; old summaries explicitly historical. Five reviewed
  normative-prefix corrections select v2 STIP and canonical/derived live pointers;
  current book examples retained. `python3 target/p4-system-13/c18a/verify.py`
  rc=0. **NO REGRESSION**: 112 base/348 GC canonical+guest inputs, all registry/
  core/author/scripts/frozen records exact; 80/114 unchanged. Focused shard,
  bounds, frontier, counts, freeze, reports and books rc=0: 225 frozen rows,
  37 fixed route caps, 33 frontiers, five derived counts, three frozen versions/
  zero findings, five fresh reports, 270 schema inputs/two named skips, main+five
  model books. Raw shard retains its source trailing blank separator; whitespace
  review excludes only that byte-proven file (all other changed files rc=0).
  Hooks precede the next slice. LIVE_STATUS unchanged (649 arms, 47 chapters, P4 12/18).
  promotion: declined (lossless authenticated payloads and existing containment/derived-source doctrine retain the proof).

Completed c17a–f acceptance is preserved byte-verbatim in
[archive/P4-SYSTEM-8.md](archive/P4-SYSTEM-8.md#c17-acceptance).

Completed c8–c16 acceptance are preserved byte-verbatim in
[`archive/P4-SYSTEM-7.md`](archive/P4-SYSTEM-7.md#runtime-acceptance).



<!-- END acceptance -->

## verification

<!-- BEGIN verification bytes=6581 sha256=d3a6146fa9e1bf265a712782b27536ba4352defa12f9d465eb93fc30008a8947 -->
## Verification Log

c17a–f receipts: [archive/P4-SYSTEM-8.md](archive/P4-SYSTEM-8.md#c17-verification).

| Date | Leaf | Checks | Result |
| --- | --- | --- | --- |
| `2026-10-10` | `.13` c25 |61440 field cases+six integration programs; ten wrong tables/disabled observer/missing binding; exact locator correction; independent/full167/prior96 identity; Rust167/17/214 | registry98/effective96/114; nine pairs/freeze; focused/all six books rc=0; hooks next |
| `2026-10-10` | `.13` c24 |20 actual CPU cases29/50/104; seven captures/disabled observer/two walker mutations; missing binding RED; independent literals/full167/prior94 identity; Rust167/17/212 | registry96/effective94/114; ten pairs/freeze; focused/all six books rc=0; hooks next |
| `2026-10-10` | `.13` c23b | two U/Sv39 width cases8/16/22; seven narrow effects fail both; disabled-GPR/missing-binding RED; literal author/full167/prior92 identity; Rust167/17/210 | registry94/effective92/114; eleven pairs/freeze; focused gates/all six books rc=0; hooks next |
| `2026-10-10` | `.13` c23a | 9,822 B suffix/inverse hashes exact; all runtime/input/frozen bytes exact; new-file cap census51 | registry92/effective90/114 unchanged; focused gates/all six books rc=0; hooks next |
| `2026-10-10` | `.13` c22b2 | 15 literal cases/17 boundaries/32 parcels; eight incorrect effects; reordered GREEN; disabled-PC and missing-binding RED; prior90/input/core bytes exact; independent full167; Rust167/17/208 | registry92/effective90/114; twelve pairs/freeze; focused gates/all six books rc=0; hooks next |
| `2026-10-10` | `.13` c22b1 | literal normal states; public base-JALR bit1 survivor across all 167; six annotation repairs; pinned image-identical source governor and two bypass REDs; executable arrays/prior bytes exact; Rust 167/17/206; full CI five legs green | effective 88/114 unchanged; direct c22b2 target witness next |
| `2026-10-10` | `.13` c22a | 20=13+7 ordered inverse/hash exact; old manifest/sealed bytes exact; one appended row; no-op; prior inputs/runtime exact; focused gates/books | effective 88/114 unchanged; 226 frozen rows; hooks before c22b |
| `2026-10-10` | `.13` c21b | 13 author/13 public delayed-PC controls; 63/111; declaration RED; Rust 167/17/206; full corpus/prior bytes exact | registry 90; effective 88/114; focused gates/books rc=0; hooks before c22a |
| `2026-10-10` | `.13` c21a | ordered suffix/inverse hashes exact; all prior registry/input/core/frozen bytes exact; navigation/counts; focused gates/books | effective 86/114 unchanged; book 48 chapters; hooks before c21b |
| `2026-10-10` | `.13` c20 | 9 author/9 public provider controls, 256 byte values; declaration RED; Rust 167/17/206; full corpus/prior bytes exact | registry 88; effective 86/114; focused gates/books rc=0; hooks before c21a |
| `2026-10-10` | `.13` c19 | 26 direct cases, 14 bad tables, all 19 erased fault cases; disabled observer RED; public full-corpus gap; Rust 167/17/206; prior bytes exact | registry 86; effective 84/114; focused gates/books rc=0; hooks before c20 |
| `2026-10-10` | `.13` c18c | new controls RED then21/15/8 green; actual hash refusals; seven routes;72-file snapshot/three-file restore; prior input/registry identity | make ci all five legs green; effective 82/114 unchanged; arms 650 |
| `2026-10-10` | `.13` c18b | 17 isolated countermodels; literal edges; declaration RED then Rust 167/17/203; author 167/5365/10524; prior bytes exact; focused gates/books | registry 84, effective 82/114; c18c source identity next |
| `2026-10-10` | `.13` c18a | six payloads and two inverse partitions exact; 112/348 input identity; shard/bounds/frontier/counts/freeze/reports/books | focused gates rc=0; effective 80/114 unchanged; hooks before c18b |
| `2026-10-10` | `.13` c7b | literal reset/view/image; 128 violations + disabled auditor; private cold fields; Rust 161/17/198; prior bytes exact; schema/freeze/gate 17/17 | make ci all five legs green; 58/114, boundary pairs complete |
| `2026-10-09` | `.13` c7a | public before/after; 3 Rust view controls / 192 CPU steps; author 42 exact; Rust 160/17/197; GUEST-GEN 135/0 | final make ci all five legs green; delegation/owner repaired; 56/112 unchanged |
| `2026-10-09` | `.13` c6 | Rust 157/17/197; literal order/overlap/AMO + 4 aq/rl; warmed rewrites; 3 violations + disabled auditor; old bytes exact; schema/freeze; gate 17/17; books | 56/112 realized, v2 open |
| `2026-10-09` | `.13` c5 | Rust 157/17/196; timer/head and WFI/idle/wake; 5 phase violations + disabled guard; old bytes exact; schema/freeze; gate 17/17; books | 54/110 realized, v2 open |
| `2026-10-09` | `.13` c4b | Rust 157/17/195; literal byte/width pairs; 12 negative cases; auditor disabled; old bytes exact; schema/freeze; gate 17/17; books | 52/108 realized, v2 open |
| `2026-10-09` | `.13` c4a | public before/after; 4 boundary controls; Rust 157/17/194; C engine 18; freeze/dossier; gate 17/17 | full make ci all five legs green; 50/106 unchanged |
| `2026-10-09` | `.13` c3 | exact typed Sv39/address fixtures; three provider violations; Rust; schema/freeze; gate 17/17; books | 50/106 realized, v2 open |
| `2026-10-09` | `.13` c2 | exact stream/mappings; 31 controls + mutant; Rust; schema/freeze; gate 17/17 | make ci all five legs green; 48/104 unchanged |
| `2026-10-09` | `.13` c1 | Rust; schema/freeze; three owner generators; nine violations; exact old bytes; gate 17/17; books | 48/104 realized, v2 open |
| `2026-10-09` | `.13` b5 | four scope pairs/16 violations; Rust; old-entry/input identity; gate 17/17; freeze/books | 42/106 realized, v2 open |
| `2026-10-09` | `.13` b4 | toolchain 20/20 and mutant; pinned C exact ELF; ACT4 7/7; GUEST-GEN 130; books | pins enforced, contract credit unchanged |
| `2026-10-09` | `.13` b3 | six scope pairs/17 violations; Rust; gate 17/17; freeze; exact bindings; shard reconstruction/freeze; books | 34/106 realized, v2 open |
| `2026-10-09` | `.13` b2 | make check; scope POS/NEG and disabled/unknown controls; exact old bindings; gate 17/17; freeze/books | 22/106 realized, v2 open |
| `2026-10-09` | `.13` b1 | make check; executable identity; state/schema/freeze; books and focused gates | complete state inventory; no behavior change |
| `2026-10-09` | `.13` a | full effective census; gate controls 17/17; freeze; books; tree/frontier/bounds | plan complete; declarations next |
| `2026-10-09` | `.12` FINAL | make ci all five legs; 37 forms/167 guests; prior traces exact; Sail 27 + one public-probed limit | met; .13 next |

Closed detailed rows: [`archive/P4-SYSTEM-6.md`](archive/P4-SYSTEM-6.md).


<!-- END verification -->

## commits

<!-- BEGIN commits bytes=5073 sha256=76b4d18485e0a903cbfd00c57a554faac300364404fd972a6ae9e13f54c7c67d -->
## Commit Log

c17a–f receipts: [archive/P4-SYSTEM-8.md](archive/P4-SYSTEM-8.md#c17-commits).

| Leaf | Subject | Next |
| --- | --- | --- |
| `.13` c25 | `SEMULITH-P4-0153 (leaf P4-SYSTEM.13): observe FENCE fields and preservation` | c26a receipt containment, then remaining pairs/freeze |
| `.13` c24 | `SEMULITH-P4-0152 (leaf P4-SYSTEM.13): observe implicit Sv39 requests and no-write faults` | c25 FENCE, then remaining pairs/freeze |
| `.13` c23b | `SEMULITH-P4-0151 (leaf P4-SYSTEM.13): retain 64-bit user registers and addresses` | c24 WALK-IMPLICIT, then remaining pairs/freeze |
| `.13` c23a | `SEMULITH-P4-0150 (leaf P4-SYSTEM.13): retain control-transfer witnesses in a bounded chapter` | c23b XLEN, then remaining pairs/freeze |
| `.13` c22b2 | `SEMULITH-P4-0149 (leaf P4-SYSTEM.13): observe JALR targets and links directly` | c23a bounded control-transfer book, then c23b XLEN |
| `.13` c22b1 | `SEMULITH-P4-0148 (leaf P4-SYSTEM.13): correct inherited GC alignment evidence and own target checks` | priority c22b2 direct JALR target-state pair |
| `.13` c22a | `SEMULITH-P4-0147 (leaf P4-SYSTEM.13): retain whole development receipts under fixed bounds` | c22b JALR-LSB, then remaining runtime pairs/freeze |
| `.13` c21b | `SEMULITH-P4-0146 (leaf P4-SYSTEM.13): realize immediate control-transfer observations` | c22a live-note containment, then c22b JALR-LSB |
| `.13` c21a | `SEMULITH-P4-0145 (leaf P4-SYSTEM.13): preserve memory witnesses in a bounded book chapter` | c21b NO-DELAY-SLOTS, then remaining runtime pairs/freeze |
| `.13` c20 | `SEMULITH-P4-0144 (leaf P4-SYSTEM.13): realize little-endian byte-lane observations` | c21a book partition, then c21b NO-DELAY-SLOTS |
| `.13` c19 | `SEMULITH-P4-0143 (leaf P4-SYSTEM.13): realize discarded-load requests and faults` | c20 ENDIAN, then remaining runtime pairs/freeze |
| `.13` c18c | `SEMULITH-P4-0142 (leaf P4-SYSTEM.13): authenticate citation source bytes before judging text` | c19 LOAD-X0, then remaining runtime pairs/freeze |
| `.13` c18b | `SEMULITH-P4-0141 (leaf P4-SYSTEM.13): realize load extension and low-bit stores` | priority c18c citation source identity, then c19 LOAD-X0 |
| `.13` c18a | `SEMULITH-P4-0140 (leaf P4-SYSTEM.13): retain bounded history and derive current contract summaries` | c18b OB-LOAD-EXT, then remaining runtime pairs |
| `.13` c7b | `SEMULITH-P4-0119 (leaf P4-SYSTEM.13): realize full cold reset with independent startup witnesses` | c8 OB-PRIV-MODES, then remaining runtime pairs |
| `.13` c7a | `SEMULITH-P4-0118 (leaf P4-SYSTEM.13): enforce delegation in supervisor interrupt CSR views` | c7b full cold reset, then 28 runtime pairs |
| `.13` c6 | `SEMULITH-P4-0117 (leaf P4-SYSTEM.13): realize one-hart ordering with independent conversations` | c7 full cold reset, then 28 runtime pairs |
| `.13` c5 | `SEMULITH-P4-0116 (leaf P4-SYSTEM.13): realize event positioning at explicit step boundaries` | c6 one-hart ordering, then cold reset |
| `.13` c4b | `SEMULITH-P4-0115 (leaf P4-SYSTEM.13): realize data-access assumptions with independent byte witnesses` | c5 event delivery, then ordering/reset |
| `.13` c4a | `SEMULITH-P4-0114 (leaf P4-SYSTEM.13): validate environment success responses before CPU consumption` | c4b data widths/attributes with direct pair |
| `.13` c3 | `SEMULITH-P4-0113 (leaf P4-SYSTEM.13): realize physical byte-address assumptions with typed boundary fixtures` | data widths/attributes, then three remaining assumptions |
| `.13` c2 | `SEMULITH-P4-0112 (leaf P4-SYSTEM.13): partition obligation catalogs without changing expanded records` | five boundary assumptions, then remaining runtime pairs |
| `.13` c1 | `SEMULITH-P4-0111 (leaf P4-SYSTEM.13): supersede obsolete stages and correct fault-priority wording` | lossless catalog partition, then five boundary assumptions |
| `.13` b5 | `SEMULITH-P4-0110 (leaf P4-SYSTEM.13): realize the remaining scope selections` | boundary assumptions, current replacements and runtime checks |
| `.13` b4 | `SEMULITH-P4-0109 (leaf P4-SYSTEM.13): enforce the pinned toolchain in both guest build paths` | remaining scope pairs and versioned declarations |
| `.13` b3 | `SEMULITH-P4-0108 (leaf P4-SYSTEM.13): realize six structured scope pairs and retain bounded history` | remaining scope dispositions and versioned declarations |
| `.13` b2 | `SEMULITH-P4-0107 (leaf P4-SYSTEM.13): run explicit scope evidence through the contract registry` | remaining scope checks, then versioned declarations with evidence |
| `.13` b1 | `SEMULITH-P4-0106 (leaf P4-SYSTEM.13): re-answer the complete state inventory without changing execution` | versioned declarations and check realization |
| `.13` a | `SEMULITH-P4-0105 (leaf P4-SYSTEM.13): census the effective contract and plan every check realization` | five boundary assumptions and v2 replacements |
| `.12` FINAL | `SEMULITH-P4-0104 (leaf P4-SYSTEM.12): close compressed-instruction acceptance after the complete local CI suite` | `.13` contract v2 completion/freeze |

Closed detailed rows: [`archive/P4-SYSTEM-6.md`](archive/P4-SYSTEM-6.md).


<!-- END commits -->

## changelog

<!-- BEGIN changelog bytes=9155 sha256=ff7603805c0ef5890ae2bad6696862874cb12f896bcfb1ea4774400e1e440ee9 -->
## Changelog

- `2026-10-10`: `.13` c25 (SEMULITH-P4-0153): bind FENCE field/no-effect
  observations and reservation/cache preservation, fix exact author source
  locator. Prior96/input/core/generated/frozen bytes exact; registry98/effective
  96/114, nine runtime pairs/freeze. c26a task containment follows workflow.

- `2026-10-10`: `.13` c24 (SEMULITH-P4-0152): bind direct implicit-walk
  request/no-write fault matrix with discriminating controls. Prior94/input/core/
  frozen bytes exact; registry96/effective94/114, ten runtime pairs/freeze.
  c25 FENCE follows complete commit workflow.

- `2026-10-10`: `.13` c23b (SEMULITH-P4-0151): realize XLEN with direct
  U/Sv39 high-address programs and fourteen narrow-effect refusals; actual disabled
  GPR-auditor/missing-binding RED. Prior input/runtime exact; registry94/effective
  92/114, eleven runtime pairs/freeze. c24 WALK-IMPLICIT follows clean workflow.

- `2026-10-10`: `.13` c23a (SEMULITH-P4-0150): move whole control-transfer
  suffix with exact inverse; all runtime/input/frozen bytes unchanged. Integer/
  control21,969/10,013 B, fixed caps unchanged. Book48→49, effective90/114.
  c23b XLEN follows hooks/brief/clean actual census.

- `2026-10-10`: `.13` c22b2 (SEMULITH-P4-0149): close direct JALR target
  witness gap with literal state/request cases and eight bad effects, including
  meaningful disabled-PC RED. Prior inputs/runtime exact; registry92/effective
  90/114, twelve pairs/freeze. Book containment before XLEN.

- `2026-10-10`: `.13` c22b1 (SEMULITH-P4-0148): correct six inherited
  GC IALIGN annotations, retain all images/numeric observations/budgets and base
  inputs. Public wrong base-JALR mask survives old full corpus; target-state
  repair owned priority-next c22b2. Effective88/114 unchanged; core correct.

- `2026-10-10`: `.13` c22a (SEMULITH-P4-0147): preserve whole older
  development receipts as 13 live+7 archived, byte/order inverse exact; fixed cap
  unchanged. Append one frozen row, preserve old/sealed history. Effective 88/114
  unchanged; c22b JALR-LSB follows hooks/brief/clean actual census.

- `2026-10-10`: `.13` c21b (SEMULITH-P4-0146): bind immediate control
  transfers after 13 author/13 public delayed-PC controls over 63/111. Base eight
  and C five forms discriminate; effective 88/114, prior bytes exact. c22a live-note
  containment then c22b JALR-LSB after hooks/brief/clean actual census.

- `2026-10-10`: `.13` c21a (SEMULITH-P4-0145): exact ordered suffix
  and inverse preserve all memory witness bytes in a bounded chapter; caps fixed.
  Current navigation/derived reports follow; chapters 48, effective 86/114 unchanged.
  c21b NO-DELAY-SLOTS follows hooks/brief/clean actual census.

- `2026-10-10`: `.13` c20 (SEMULITH-P4-0144): bind ENDIAN cross-width
  witnesses over 64/128 after nine author/nine public reversal controls; byte
  address invariance across 256 values exact. Effective86/114, all prior bytes exact.
  c21a fixed-cap integer book partition then c21b NO-DELAY-SLOTS after hooks.

- `2026-10-10`: `.13` c19 (SEMULITH-P4-0143): direct x0 request/trap
  witnesses close the old GC comparison gap, reproduced across all 167 guests
  through author and public tables. All seven forms discriminate before credit;
  84/114, prior bytes exact. c20 ENDIAN follows hooks/brief/clean census.

- `2026-10-10`: `.13` c18c (SEMULITH-P4-0142): close source-identity
  exposure in both citation readers and fetched/cache presence dispatch, with
  observed RED controls and actual hash refusals. Restore only three fetched pages
  from authenticated snapshot, pins/architecture bodies exact. Promote the lesson;
  effective82/114 unchanged, arms650. c19 LOAD-X0 follows full CI and commit.

- `2026-10-10`: `.13` c18b (SEMULITH-P4-0141): bind all eleven load/store
  extension forms over 111/222, with seventeen isolated countermodels rejected
  before credit. Exact prior registry/inputs/production/frozen identity; 82/114.
  Authenticated source cache supplied review; fetched-page identity refusal owned
  as priority-next c18c before the remaining runtime pairs.

- `2026-10-10`: `.13` c18a (SEMULITH-P4-0140): losslessly partition task/DEV/
  profile history under unchanged fixed caps; correct stale current membership/
  realization/interrupt summaries through canonical and derived sources. Exact
  input/registry/frozen identity; 80/114 unchanged. c18b load extension next.

c17a–f entries: [archive/P4-SYSTEM-8.md](archive/P4-SYSTEM-8.md#c17-changelog).

- `2026-10-10`: `.13` c7b (SEMULITH-P4-0119): full cold reset born
  realized with literal owner/view/image checks before actual ADDI. All 128
  typed bad resets and disabled auditing discriminate; private cold fields
  independently pinned. Respect FS=Off and correct raw/computed mip prose.
  Prior bytes exact; 58/114, all five boundary pairs complete and v2 open.

- `2026-10-09`: `.13` c7a (SEMULITH-P4-0118): confirmed missing delegation
  masks in shared supervisor CSR views and independent author; author also
  read a separate sip owner. Repaired and directly reproduced before/after;
  actual CSR instructions, all masks/M/S and five mutations discriminate.
  Existing guest records exact; contract credit unchanged. Cold reset c7b next.

- `2026-10-09`: `.13` c6 (SEMULITH-P4-0117): one-hart ordering born
  realized with exact store/load/overlap/AMO conversations and coherent warmed
  rewrites. Three typed bad-provider cases and disabled auditor discriminate;
  bypass observation avoids sibling-guard masking. Source pins rehashed, old
  entries/frozen bytes exact; 56/112, cold reset remains and v2 open.

- `2026-10-09`: `.13` c5 (SEMULITH-P4-0116): event positioning born
  realized; explicit location guard with no source authority, direct timer/head
  and WFI/idle/wake counts, five typed forbidden phases and disabled controls.
  Old entries/frozen bytes exact; 54/110, ordering/reset remain and v2 open.

- `2026-10-09`: `.13` c4b (SEMULITH-P4-0115): data widths/attributes
  born realized with literal byte witnesses, direct high-bit and actual CPU
  stores, eight whole failures and twelve typed bad answers. Content auditor's
  disabled control discriminates. Old entries/frozen bytes exact; 52/108,
  three assumptions remain and v2 stays open.

- `2026-10-09`: `.13` c4a (SEMULITH-P4-0114): reproduce and repair
  wrong-kind/over-wide success responses in one shared validator across all
  12 CPU crossings. Independent matrix/width and real-engine controls preserve
  legitimate target failures. No new credit; 50/106 remains open.

- `2026-10-09`: `.13` c3 (SEMULITH-P4-0113): physical byte-address
  assumption born realized; named direct boundary evidence, real Sv39 request
  script and three typed violations, separate target-failure control. Prior bytes
  exact; 50/106 realized, four assumptions remain, v2 open.

- `2026-10-09`: `.13` c2 (SEMULITH-P4-0112): lossless frozen-part
  partition, shared expansion/schema origins, annotation repair and 31 controls.
  Fixed caps, all old bytes/order/pins and 48/104 credit retained; full CI green.
  Stale canonical gate-gap description corrected through its owner.

- `2026-10-09`: `.13` c1 (SEMULITH-P4-0111): three current guarantees
  replace four old records, six checks realized; profile current comments repaired,
  historical mirrors/frozen bytes exact. 48/104 realized; c2 catalog partition next.
- `2026-10-09`: `.13` b5 (SEMULITH-P4-0110): four scope pairs and 16
  specific violating copies. psABI/SBI identities rehashed; prior entries exact.
  Eleven scope pairs/42 checks realized; v2 open, no later implementation claim.
- `2026-10-09`: `.13` b4 (SEMULITH-P4-0109): reproduced and repaired pin
  enforcement/ACT4 missing-path refusal. Shared resolver, 20 controls and mutant;
  real C ELF exact. Contract unchanged; registered arms 629.
- `2026-10-09`: `.13` b3 (SEMULITH-P4-0108): six structured scope pairs,
  17 violating copies, exact public privilege identities; 34/106 realized.
  Notes/history sharded losslessly into 0217/0218; fixed caps/freeze retained.
- `2026-10-09`: `.13` b2 (SEMULITH-P4-0107): explicit guest/scope evidence,
  composition pair and six violating copies. Disabled predicates/unknown id
  discriminate in normal tests; prior bindings exact. G-CONTRACT 22/106, open.
- `2026-10-09`: `.13` b1 (SEMULITH-P4-0106): complete state inventory and
  stale-header/time-source repair, generated metadata only. Executable definitions
  identical; make check passes. Resolved census opening, .14 status work retained.
- `2026-10-09`: `.13` a (SEMULITH-P4-0105): activate full 53-obligation census,
  five boundary topics and evidence-method plan. Additional priority wording
  defect reproduced against pinned public table, correction owned. No new credit.
- `2026-10-09`: `.12` CLOSED (SEMULITH-P4-0104): complete C composition and
  independently derived corpus/counts, matched Sail subset/public timer limit,
  all CI legs green. P4 12/18; .13 next. Closed live-head records moved verbatim
  to archive part 6, full reconstruction asserted; no ceiling raised.

Closed detailed entries: [`archive/P4-SYSTEM-6.md`](archive/P4-SYSTEM-6.md).

<!-- END changelog -->
