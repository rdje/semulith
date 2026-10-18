# DEV_NOTES.md

## _(2026-10-18)_ — full-profile detector controls before GC reduction (P4-SYSTEM.16)

P4-0251 begins after5c42e3a/brief0/host0, with only the explicitly queued task
note dirty. Native demo --profile=rv64gc-lab-v0 --guest=guest-control with
--mutate=zext-addi refuses2 before; --json instead returns0/plain text. The
latter is a real machine-readable-success defect: the common parser consumes
the flag but the GC route ignores its boolean. Own and fix it in this slice.

Add model_rv64gc::Model with Production, ZextAddi and JalNoLink. Rebuild only
the selected canonical GC effect spine, retaining the entire generated table
and all row metadata, including compressed expansion effects. This never uses
scalar-only tables or a second evaluator. OnceLock caches each control table;
only three small static Sem nodes for the ADDI spine are allocated once, while
JAL reuses its existing transfer effect. Unexpected source shapes refuse by
name. They are deliberately wrong controls, not accepted ISA implementations.
The full P4.15 mutation campaign is still pending; do not credit its gate kind.

The common runner accepts an explicit full-GC table. Production still passes
INSNS; the existing loop changes only step to step_over with that parameter.
New named APIs preserve the same typed fault regions. Every167 guest compares
production trace/fetch/complete final CPU state/memory through both API paths.
Selected controls fail at guest-control boundaries1/x1 and7/x5, anchored in the
spec-derived expected writes. Metadata/pointer checks preserve all untouched
rows and repeat-call cache identity; malformed effect shapes and unknown names
refuse. C-links remains identical under these 32-bit-form controls.

The text demo names each selected model and displays both observations at the
first differing paired boundary. Unknown controls refuse2; detectable wrong
results exit1. A GC --json request now refuses2 with an explicit unsupported
structured-report message and no stdout; scalar JSON remains valid. Default
production output is compared byte-exact to the pre-change native output.
GC bundles still record production only; model-aware records and reduction
follow in .16. Book examples state that intentionally wrong demos exit1 and
unaffected guests may agree. No CPU acceptance or regression-campaign claim.

Strict lint first rejects three nested pattern matches; flatten them into
explicit match patterns/guards, retaining the same shape refusals. No allow
attribute or lint policy changes. Own necessary whole-history rollover before
new prose: CH78=72+6/5453B into0337; DEV17=14+3/7207B into0338, with exact order
and bytes and old manifest prefix. Sharder self-test12/0. Evidence and final
scope/old-loop/default-output proofs: target/p4-system-16/controls. Rust/wasm,
focused publication and book checks precede normal COMMIT. LIVE_STATUS stays
P4 In Progress13/18, replay3/4, CPU-SYSTEM incomplete; board10/12 unchanged.
The history gate correctly refuses intent-added shards with the old staged
manifest. Stage the complete verified partition before judging that view.
New shard terminal blank lines are exact old payload bytes; preserve them.
The whitespace probe reports only those two shard endings; source/docs checks
exclude these two verbatim artifacts explicitly. No frozen payload is trimmed. Focused13, Rust/wasm, seven books and normal/O
scope checks pass:1487 protected files/95 old head entries, exact legacy loop
with explicit table, byte-exact default demo and four rendered guide views.

The first full hook exposes the isolated C-image crate's explicit dependency
closure: it copies run_rv64gc but omits its new Model module. The positive
case cannot compile, and the wrong-offset arm fails for that unrelated reason;
GUEST-GEN correctly refuses326pass/2fail. Add the unchanged production Model
module to that fixture and its root declarations. Its test module is an explicit
empty fixture because this crate runs only its own image tests; the complete
control-model suite remains compiled/executed in the workspace. Preserve both
original C-image tests, expected data and the exact wrong-offset mutation.
This is dependency-closure repair, not acceptance of a compile error as evidence.
Reading the affected C chapter also finds its current-scope sentence still
calling v2 open after .13 froze it and still referring to remaining contract
work after G-CONTRACT passed. Correct both current-status phrases against the
contract/gate; historical receipts and all contract members remain exact.
Direct image positive normal/O exits0, wrong-offset normal/O exits1 with the
same mixed-step0-write reason, and padding exits1 at exact-image verification.
The complete GUEST-GEN self-test returns328/0 after repair. Scope normal/O now
protects1485 files/95 old entries; final book and publication checks follow.

## _(2026-10-18)_ — complete RV64GC replay records (P4-SYSTEM.16)

P4-0250 starts from clean1cf0673, brief0/untracked and a green host census.
The actual GC bundle CLI refuses2 before. Add the fs-free BundleRv64gc API
and explicit-profile bundle/replay routes. Input is a complete snapshot; its
CPU, memory, typed fault regions and runtime/definition/lock identity travel
with an explicit flat-memory/no-external-events policy. CLI recording selects
tracked production guests from reset; API recording also supports checkpoints.
Producer-source pins bind the replay machinery and string encoder. These are
reproducibility identities, not an external author's authenticity signature.

Compare incoming PC, resulting mode and ordered GPR changes at their first
absolute boundary, then independently compare boundary count, model-error and
fetch receipts and SHA256 of the complete canonical final checkpoint. Aggregate
receipts do not pretend to locate the first instruction responsible. Identical
model-error reproduction is successful replay, not a correct CPU verdict.
Keep reduction/nonproduction GC mutation models out of this slice. Bounds:
10000 continuation boundaries, existing64MiB memory, 145MiB JSON, depth12,
2000000 structural punctuation and4096B model-error text; fail before parsing
or execution at the applicable boundary. Artifact limits are not exact RAM caps.

Review also finds both snapshot writers interpolate digest text unescaped.
Permanent Cargo tests reproduce runtime and memory quote/control-character
serialization failures independently (1pass/2fail before), then pass3/0 after
using the existing JSON string encoder. Restore continues refusing both foreign
identities. The earlier manual rlib probe could not link; its output is not a
behavior witness. Include the encoder source in the conservative runtime pins.
No valid digest bytes or scalar replay behavior change. CLI tests retain the
actual scalar catalogue/default route as well as four GC system cases.

Own necessary bounded retention in the product slice: all four complete a21
reader-unit spans (3766B) move into the existing mutable reader record. Preserve
its121386B old prefix and every published archive. Source offsets/digests plus
unique root stubs yield the exact131036B owner inverse; four independently
damaged payloads refuse. Root127897B/retention128023B before new growth stay
under the existing131072B ceilings. Preserve the original root heading and
link the full retained decision/acceptance/verification/commit bytes. No capacity
raise, new task file, canonical record or qualification change.

Evidence: target/p4-system-16/replay. All167 corpus bundles round-trip/replay;
mid-execution/empty continuations and changed PC/mode/GPR/length/fetch/error/final
receipts discriminate, as do missing/foreign/invalid inputs and step bounds.
Four real CLI cases cover atomics, wait/timer, translation and floating point;
usage/malformed2, changed/refused1, identical0. G-REPLAY gains only the bundle
kind (3/4); CPU-SYSTEM remains incomplete, P4 remains13/18 and .14 stays open.
The first manifest used kind bundle; the gate refused it by name. Correct to
the existing required kind replay-bundle without changing the gate. Focused
publication, Rust/wasm and book checks precede the normal COMMIT. The route
gate catches the new LIVE row6B over its fixed cap; concise current wording
fits. Correct the print probe to require the gate table in its actual GC book
owner; both main-book guide views remain explicitly checked. Focused13, make check,
wasm, seven books and source/inverse checks pass normal/O:1479 protected
files,93 whole old head entries,4 retained spans/4 damaged refusals. The first
commit hook rejects the abbreviated ADDRESSED bullet. Cancel that owned Git
parent/eight descendants, verify process residue0, add the actual Cargo command
and rc=0 to the bullet, then rerun acceptance and normal hooks.

## _(2026-10-17)_ — RV64GC checkpoints resume the complete laboratory state (P4-SYSTEM.16)

The director identifies delivery stagnation and requests product implementation.
At cb39c69 the latest40subjects are all LC/AC, while CPU13/18 and board10/12
remain unchanged. After clean2a97c46/brief0/host0, choose the independent .16
snapshot capability ahead of remaining .14 qualification machinery. The latter
stays owned/open; actual correctness/review blockers retain priority. Record the
risk, scheduling correction and successful480-observation/155525-packet user
capture in LIVE-CONTAINMENT. No authorization or further terminal command is
needed. The capture's pending Git parent was held/resumed to keep its full
source/index/HEAD window stable; its result/working-after and PCAP SHA survive.

Before: the actual `cargo run -p semulith-cli -- snapshot --profile=rv64gc-lab-v0`
returns2 with the named unsupported-state refusal. Implement .16a as a complete
CLI/library vertical slice: JSON checkpoint, structural/identity validation,
state restoration and the continuation driver. The generated state's existing
raw accessors remain the register/CSR owners. Add fixed-size TLB slot/cursor
and reservation tuple inspection/restoration to their own core modules. Preserve
invalidated slots and cleared-but-retained reservation metadata. The common GC
corpus runner also drives checkpoint prefixes and continuations. The existing
CLI run path stays byte-exact and supplies the integration-test comparison;
trace mode is explicitly the resulting mode.
The scalar snapshot parser shares only its decoded-value helper; old JSON stays
byte-compatible. No handwritten instruction semantics or generated-state edit.

The new format retains all SEM-08 owners and typed laboratory refusal regions.
Compiled definition pins plus hashes of selected runtime/state/environment/reader
sources and Cargo.lock reject changed execution machinery. A OnceLock caches the
runtime hash without filesystem access, preserving the wasm build boundary.
Memory is bounded to64MiB, total boundaries to1000000; fixed4KiB chunks bound
sparse overhead. JSON bytes/depth/structural tokens are bounded before parsing;
ELF input is bounded before reading beyond65MiB. These are artifact scopes, not
exact RAM ceilings. Resume continues the recorded cold-started execution at its
step index; frozen cold-reset/environment contracts remain unchanged.

Eight API controls include all167guests/501 JSON continuations, exact final CPU/
memory state and fetch totals, observable reservation/wait omissions, retained
TLB slots/FIFO and a real warm-versus-cold page-walk request witness, corrupted/
foreign/missing-state records, bounds and zero/final checkpoints. CLI integration
covers four actual system ELF cases and an independently encoded compressed
sequence at entry0x80000002. Strict clippy caught an unnecessary cast and Copy
clone in the draft; both are corrected and the complete Rust checks rerun.

Declare only the snapshot kind in gate.sexp and regenerate GS-REPORT: replay
kinds1/4→2/4; seven axes remain open, CPU-SYSTEM incomplete, P4 total13/18.
Architecture owns the commands/state/limits contract; both main and GC unit books
include it, and the main overview states current replay scope. Focused gates,
seven books, full Rust checks and normal COMMIT qualify the product slice.
No feature/reference independence or processor release is inferred from replay
agreement. Bundle/reduction implementation is the next .16 slice; .14 evidence,
other CPU gates and board/MCU/DSP expansion remain separately scheduled.

## _(2026-10-17)_ — due cleanup preserves terminal capture evidence (ARTIFACT-CLEANUP.8)

After clean cb39c69/brief0/normal hooks, census finds18 disposable incremental
caches/77596894B and14220retained files/131741041B. Reuse the .7 safe-cohort
helper with only its owned scratch path changed. Whole-cohort preflight and
per-path size/device/inode/mtime/SHA checks precede unlink. Skip four nested
Git roots, symlinks and other volumes; preserve all inputs and diagnostics,
including the original failed and corrected native preparation outputs. Four
changed identity/totals cases refuse normal/O; both complete positive preflights
pass. An early pre-delete census catches our still-running check child and
correctly blocks deletion; all checks join before a repeated green census.

Actual deletion completes2026-10-17T22:50:22Z:18saved paths absent, immediate
selected residue0, retained count/bytes/SHA exact; no release/deps stray files.
Six C-engine caches/46660990B and twelve C-guest-image caches/30935904B removed.
Later gate builds may regenerate caches; the receipt describes this event.
The original LC0047 app handles are no longer observed by the host census after
cb39c69. Record the release witness in its owning tree; no app action, exemption
or claim about application internals. Policy source hashes still match the
reviewed package and exact imported claim-verification body. Overwrite only
the latest receipt, already included by the book; original teaching/source,
prior history/modes/Gitlinks and fixed limits stay exact. Focused13/seven books,
normal/print receipt and inverse verification plus normal COMMIT qualify the
housekeeping. LIVE_STATUS unchanged; next terminal D79 capture/causal analysis.

## _(2026-10-17)_ — select the reviewed terminal mdBook before preparation (LIVE-CONTAINMENT.4i2b5b2r.d2v)

The user's packet-20261017T222353Z-1bef02 stops at the frozen public mdBook
version guard before sudo. It has working-before/compiler records but neither
version stdout nor failure.json: the initial preparation was outside the failure
recorder. Census finds project/Homebrew0.5.4 and user Cargo0.5.2. The original
terminal resolution was not recorded, so its exact executable is unknown.
Cargo-first PATH independently reproduces the same refusal with stdout0.5.2.

The capture entrypoint now runs the existing install_ci_mdbook.sh, which checks
the pinned release archive checksum and installs only under .app-data/ci-tools.
Validate owned cache/binary paths against links, Git boundaries and other volumes
before setup; retain setup stdout/stderr/status, exact version response and
selected binary SHA. Only that invocation's PATH receives the local bin prefix.
Keep the original exact0.5.4 guard and all old forensic producers byte-exact.
Check the selected binary identity again after the workload. Move compilation,
version/calibration and immutable preparation inside the failure recorder.
No shell profile, global mdBook, permission or sudo policy is changed.

All33 controls pass normal/O: original24 remain, plus old-first selection through
the actual frozen guard, wrong/stderr/nonzero version, failed installer, missing/
symlink binary and early setup/compiler failure persistence. Controls use an
isolated unprivileged installer; the real checksum installer is verified by the
native check. Cargo-first --check-preparation rc=0 rebuilds fixed inputs, runs
WebKit calibration and closes four servers with no sudo. Selected binary SHA
49f163c7a5a9d0a4fc9cacf34bd0b96b11801458effddb1b7e951377af909d8e.
Raw evidence: target/live-containment/capture-version and packet-20261017T223050Z-6ac03d.

Retain whole closed LC0044/45/47 task spans from4c14bf7 byte-exact in the existing
reader-records-retention.md LC0048 phase, preserving headings/pointers and fixed
caps. Two oldest whole DEV entries move to0335; prior head/shard bytes and order
remain recoverable. The book's canonical include explains automatic version
selection, logs and why this failure cannot ask for a password. Focused gates,
seven books, source/history/retention verification and normal COMMIT qualify
this repair. D79 remains priority1/open pending terminal capture/causal analysis;
D80 follows. LC0047 app disposition and due cleanup remain separately owned.

## _(2026-10-17)_ — application disposition blocks handoff (LIVE-CONTAINMENT.4i2b5b2r.d2)

After dafb073, the actual host handoff census returns1 for Kimi Code PID5950.
Scoped lsof -Ffan shows only AGENTS.md, read-only fds84/87. Read handles count
under the published detector; this observation is not a detector/code defect.
doctrine/sanctioned_processes.tsv reserves exemptions to the director. Closing
another app could disrupt work, so no termination or exemption is authorized.
LC0047 owns release/director disposition before clean handoff, priority2. The
capture tool and D79 causal evidence stay unchanged and ready for terminal use.

## _(2026-10-17)_ — one terminal command for scoped packet evidence (LIVE-CONTAINMENT.4i2b5b2r.d2)

The director requests a single terminal tool for the blocked D79 packet leg.
capture_book_dependencies.py prepares immutable LC0044 inputs through existing
public helpers, calibrates nonpersistent WebKit and reserves all four origins
before one sudo tcpdump starts. Only that system binary gains privilege; Python,
builds, journals, packet file descriptors and browser workers stay user-owned.
The IPv4 TCP filter requires both endpoints127.0.0.1 and a reserved owned port;
96-byte snapshots,200000 packets and600seconds bound capture. Native startup
acknowledgement precedes replay. Source/current phases each run two servers with
two workers. SIGINT/TERM/HUP unwinds cleanup; pending pages cancel, active pages
join, sudo relays the stop signal to tcpdump, and the child is waited. A stopped
capture, missing/drop counters, out-of-scope/truncated pcap or changed source
refuses rather than reporting complete evidence. Raw journals survive refusal.

Normal/O controls use real unprivileged substitute children and an independent
offline system tcpdump oracle: malformed scope/pcap, missing ports, counter/drop
faults, authentication denial, startup/deadline, interruption, pending cancellation
and whole observation streaming. They do not claim actual privileged capture.
The real native preparation path initially exposed a tmp-name collision with the
frozen builder. Use environment-tmp for caller defaults, preserving the builder's
own tmp allocation. --check-preparation validates the corrected actual public path
and four server closures without sudo. Initial sandbox WebKit refusal is separated
from the host-native check; no browser diagnostic is suppressed or blessed.

Existing tracers/producers/retained captures remain unchanged. The book includes
the toolbox's bounded capture contract, preserving its previous D79 paragraph
byte-exact in that canonical anchor. The draft duplicate exceeded the book
aggregate; inclusion restores room without raising a cap. The contract explains
the sole user command and generated paths. No permission changes, new decision
file, capacity increase or acceptance claim. D79 remains open until the user's
authorized terminal capture and causal analysis; passing repeats cannot close it.
Six whole oldest CH entries roll to0334 with exact byte/order reconstruction;
focused gates/seven books and normal COMMIT qualify tool delivery only.

## _(2026-10-17)_ — persistent dependency forensics and explicit evidence blocker (LIVE-CONTAINMENT.4i2b5b2r.d)

LC0044 owns the diagnostic gap after D79's missing-Mark print refusal. Pin current
f3c5e81/1485 identities and reproduction5c72864/1481 separately. Public mdBook0.5.4
rebuilds all345 fixed output identities exactly from the original source plus the
two-file D78 overlay. Frozen Q/R/Swift/reader/helper bytes and Gitlink remain exact.
The new owned tracer streams linked received/response/written/failure records and
page observations even when native/DOM/qualification refuses. Every handler has
bounded reads and shutdown joins all workers; process/source/index snapshots stay
stable. Separate normal/O processes with two workers each reproduce four-adapter
source-before-fixed workloads. Nonpersistent WebKit/strict Swift6 and execution
witnesses retain their actual boundaries and on-volume data locality.

The first window-load observer misses descendant resource loads: DOM's document
parent is null for load events. Use document capture and independent declaration/
load-or-error membership. An actual omitted-document-listener control refuses2
with intact journals. The source URL oracle also initially ignored base href=/
on404 pages; corrected static/browser base reconciliation makes those actual
resource failures observable rather than unjudgeable. All seven 404 assets route
outside their book under shared serving, a verified D80 priority1 owned by LC0046.

Six real controls pass normally/optimized, plus three mutation/type boundaries:
positive; Mark404; Mark200empty; Mark+book404; omitted load observer; absent native
adapter. Receipt/delivery/observation streams reconcile fully even on refusal.
Mark-only failures keep1917 highlighted nodes/155 spans/97 copy buttons. Combined
denial removes all enhancements and reproduces the entire original failed heading
witness. This is a sufficient symptom mechanism, not proof of original cause.

Four selected normal/O queue5/32 comparisons retain960 complete source/fixed
heading witnesses and all verdict/check/script/error/global/enhancement rows.
Full per-path delivery/status/byte/count footprints reconcile every event. Final
profiles expose only seven D80 cases each. An earlier optimized queue5 assembler
trace loses ten assets before application receipt: two styles and eight scripts
emit resource-error, globals/late enhancements absent; other styles/fonts arrive.
Full selected failure forensics and page-linked delivery rows are retained. Later
passing queue5/32 repeats do not close D79 or establish a listen-backlog cause.
OS TCP counters all report0 including observed traffic, so cannot attribute loss.
A strictly owned lo0 port/two-packet/96-byte tcpdump probe is denied opening BPF;
no packet/other-app traffic was captured. Immediate LC0045 is blocked on approved
read-only capture of the tracer's own ports, without global permission changes.

The native reader-retention record preserves its whole29198B prefix and5729B
closed LC0043 unit before a bounded live pointer is used. Bounded XZ references
restore all selected full witnesses from immutable LC0043 bases, with complete
source/current/probe verdicts, selected failures/access evidence, producer bytes
and old/new book/task seams. Both actual collector source versions are retained;
the sole difference is an unused posixpath import, verified by execution AST.
Current code passes permanent native controls normal/O; seven damaged evidence
frames refuse. Whole projected data equals the capture-derived projection. Raw
ordered HTTP/non-script successful-load order/resource timings/DOM remain generated
diagnostics with profile/journal identities, not a new raw-output archive promise.
Pinned Git/producers are required with lazy fetch disabled. No resource-completeness,
concurrent-load, original-cause, full graph/adoption or processor acceptance claim.

Book/toolbox/live pointers and exact earlier history/source/modes stay aligned.
Focused checks/seven books and the full staged reverse patch precede normal COMMIT.
Existing caps and LIVE1578/39/40/49 remain fixed. No new decision file is needed:
finite evidence, the exact access blocker and D80 repair have native canonical
owners. This slice delivers verified forensics; D79 remains explicitly open.

## _(2026-10-17)_ — authored-index context repair and scoped replay (LIVE-CONTAINMENT.4i2b5b2r)

D78's source5c72864/1481 identities still marks Introduction and authored Index
active together. The generated public fallback assumes root index is an alias.
The owned additional-js hook runs after sidebar creation, before DOMContentLoaded
inserts heading links. It normalizes query/fragment, directory index and .html;
a unique explicit chapter wins. No unique match preserves the existing alias/
auxiliary state. No mdBook/Gitlink internals or pins, URLs, bodies or model-book
configurations change. Public renderer configuration and actual generated outputs
establish the integration; the asset stays under theme/ with content hashing.

Final complete normal/O captures use strict Swift6/nonpersistent OS WebKit and
public mdBook0.5.4. Each source120-page matrix has only D78; each current120-page
matrix passes, retaining1408 headings/590 entries, all labels/inline ASTs/targets/
nesting/roles/active parents/titles and107 source pins. Static inversion removes
one exact script tag from51 main HTML files and reconstructs all original bytes;
293 other original outputs remain exact, with one new byte-exact owned asset.
All six model aliases pass. A supported main SUMMARY without authored Index
exercises the guard directly. Actual active-class, alias-guard and integration-
configuration omissions execute0 and fail qualification1. Four JS/HTTP witnesses
still distinguish execution from exit0. Every process/server is waited/closed.

One final optimized replay at four concurrent adapters refused print.html:
ready=true/native0/empty stderr, ReferenceError missing global Mark. Final normal
passes; the successful final optimized replay runs alone with at most two adapters.
D79 remains open and priority1, immediate LC0044 before search. Sixteen traced
print repeats deliver the complete17320B Mark resource200 and see Mark=function;
module/exports/define stay undefined. Passing repeats do not explain the original
failure. The existing helper returns HTTP observations only on successful page
assessment, so original delivery cannot be reconstructed. That verified forensic
gap and the unresolved dependency load have a dedicated next owner. No error is
suppressed; no resource-completeness or concurrent-load correctness claim is made.

The native validator record keeps its whole14406B prefix and the entire7063B
closed LC0042 task span, including calibration/ownership/acceptance text, before
the live root becomes a705B pointer. Full old/new book/task seams are retained.
Source/current and normal/optimized metadata use exact replacement references;
source rows and navigation oracles reconstruct before complete inverse comparison.
The bounded XZ frame preserves all retained page/header/nav/input/check/manifest
rows; seven outer/inner corruptions refuse normally and optimized. Codec changes
precede fresh final producer execution; older captures remain diagnostic. Queries
require pinned Git objects/producers with lazy fetch disabled. Raw DOM/HTTP streams
and omitted-bundle tables remain diagnostics with fingerprints/request footprints.

All old history entries/order and terminal bytes, protected source/modes, existing
limits, focused checks/seven books and the complete staged reverse patch are checked
before normal COMMIT. Book/current tools/live pointer agree; generated index is
regenerated and unchanged. LIVE1578/39/40/49 and CPU/MCU/DSP/board acceptance stay
unchanged. Click/scroll/layout, search/resources, full graph/adoption remain open.
The finite repair/retention and next D79 investigation have native canonical owners;
no new decision file or capacity increase is needed.

## _(2026-10-17)_ — executed heading-navigation qualification (LIVE-CONTAINMENT.4i2b5b2)

LC0042 pins1226311/1477 identities, one opaque Gitlink. Immutable public builds
produce344 files across seven books; SUMMARY/config/chapter oracle107 inputs
defines93 chapters, six index aliases and seven each print/toc/404 pages. All120
HTML pages execute through public nonpersistent WKWebView. Independent Python
HTML parsing and DOM serialization retain1406 full source/runtime headings and
589 navigation entries, labels/inline ASTs, target uniqueness, nesting, roles,
title, chapter context and actual active-parent binding. An observational script
is injected by the owned numeric-loopback server; generated bytes stay exact.

Calibration first refused Chrome155 graphics/display/allocator diagnostics.
Blank probes repeat them before project input; Edge shares Chromium ancestry,
so its agreement is not an independent engine oracle. Direct public CoreVideo
accepts actual display1 but rejects synthetic2000; the installed call path is
not traced, so virtual/native display mismatch remains an inference. Further
graphics-mailbox errors remain unblessed. Required external OS tools are read
only; profiles/module caches/temp/output stay on volume. A loopback resolver
omission produced exit0/empty DOM; an explicit HTTP witness prevents recurrence.
The public WebKit adapter uses nonpersistent website data and no personal profile.
Swift6.4/driver1.168.6 strict Swift6/warnings-as-errors compilation succeeds with
empty diagnostics. WebKit22625.1.29.11.28 on macOS27.0.1/26A434 produces empty
stderr. Positive delayed-JS/HTTP witnesses pass; script-omitted/blank pages exit0
but fail execution qualification. Every process/server is waited and closed.

Both complete normal/O captures show one wrong contract: D78, authored Index
marks both Introduction and Index active. Public generated connectedCallback
applies its first-link root-index fallback despite an explicit Index match.
Removing that branch corrects authored Index but breaks the unit first-chapter
alias. Immediate priority1 LC0043 owns a conditional public-integration repair;
six aliases must survive. Three real copied omissions (heading insertion, h2
selection, inline-label copy) complete native execution0 and fail independent
qualification1. The fourth cause control demonstrates both sides of D78.

Full normal/optimized metadata,107 inputs, every page/header/nav/check,344-file
baseline manifest, toolchain/calibrations and omission outcomes are retained in
the native integration record after its exact46333B prefix. Bounded XZ/base64
references authenticate the immutable source census and whole LC0040 predecessor
manifest; optimized replacements reconstruct the complete second view. The old
task-tree book teaching survives as exact old/new source seams, all shell commands
remain live. Nine outer/inner corruptions refuse normal/O, including re-hashed
member/source/type/trailing-data changes. Decoder assertions are unconditional.
Queries require pinned Git objects/producers, disabling lazy fetch; raw DOM/HTTP
streams and alternate bundle tables are generated diagnostics with retained
fingerprints/request footprints. No no-Git replay or complete resource claim.

Whole old history entries/order, published terminal bytes, source/modes, seven
books, focused checks and staged full-patch inverse precede normal COMMIT. Existing
caps remain fixed; live progress1578 arms/39 doctrines/40 routes/49 chapters stays
unchanged. Click/scroll/layout/search/resources, full graph/adoption and every
processor/board acceptance claim remain open. No new decision file is needed:
the finite assessment and scheduled defect have canonical native ownership.

## _(2026-10-17)_ — finite lossless qualification-history transition (LIVE-CONTAINMENT.4i2b5b1h)

LC0041 begins at968bc010/1469 identities, one opaque Gitlink. The107-file task
family had3145560B/168B spare; book51/524256B/32B spare. Classification selects
four completed source-pinned measurements: book-index consumer, graph/query
census, include/navigation readers and orientation indexes. Keep maintained
inventory/retention inputs, integration/validator teaching and task claims native.
The director's standing “do whatever you see fit regarding the task history or
archive” delegates the finite selection; it does not name this cohort or grant
an overflow sink. The owning tree and terminal record the local decision. No
existing seal, live task root or ordinary P4 archive joins this capture.

Copy/verify/use/retire preserves five originals497850B/3647LF: four records and
the whole16672B prior unexpanded task-tree book chapter. Independent immutable
Git source bytes/modes, full-tree identity, Python reader and ordinary tar verify
before retirement. All20 native mdBook heading IDs become navigation aliases;
481178B originals become5016B stubs,476162B released. The separate192354B object
plus bounded descriptor8192B/front door4096B gives a204642B terminal, exactly
three files. All original bytes/order, Git OIDs/modes and SHA identities remain.
Whole prior book source is queryable; current teaching/commands stay live while
duplicated historical receipt prose is compacted. All existing caps stay fixed.

The reader authenticates archive data/navigation before output, bounds metadata
and decompression, rejects unsafe/nonregular/duplicate/noncanonical tar members,
and verifies source SHA/GitOID/byte/LF identities. No-follow file-descriptor reads
check stable dev/inode/mode/size/mtime/ctime; no Git/network/extraction. README
content is reader-bounded and publishing-frozen; changed bounded prose still
retrieves exact originals but fails publishing. A separate
publishing guard authenticates immutable source provenance at first publication
and requires complete staged data/wiring once any transition change is staged.
Later it preserves the whole published terminal/navigation in both index and
working views, requiring no old source in shallow clones. Git API calls disable
lazy fetch themselves. Failed/unavailable evidence refuses. Corrections use new
records; retained Markdown adds no producer/toolchain/raw-output replay promise.

Initial full CI identified a metadata integration conflict: generic JSON
path/sha256 pairs denote live record-relative files. The new historical schema
now uses original_path, retaining the same five original/stub bytes through
reserialization and the same independent source/publishing verification. No
fingerprint-checker exclusion or changed original pin. The task receipt also
names the actual command/rc required by the evidence-signature gate.

All32 tests pass normal/O; all5 Python/tar retrievals agree in relocated no-Git
fixtures, without extraction or writes. Six actual isolated guard omissions turn
refusal into acceptance: staged preservation, working preservation, source-tree
provenance, original source mode/bytes, descriptor pin and navigation identity.
The initial omission selector missed computed reason strings; AST traversal now
finds their literal prefix and requires one unique statement before compiling the
owned copy. No production file was changed by those controls. The original46
retrieval arms and two43-test ordinary publishing wrappers remain; two new32-test
wrappers yield50 TASK-HISTORY arms. Re-derived global1578/40 routes;39 doctrines
and49 book chapters remain. Source/history/mode/book/cap/staged inverses, focused
checks and full milestone CI precede normal COMMIT. Heading/search/resources,
full graph/adoption and every processor/board acceptance claim remain open.

## _(2026-10-16)_ — generated chapter contents qualification (LIVE-CONTAINMENT.4i2b5b1)

LC0040 separates authored chapter contents from dynamic page-heading navigation,
search and resource loading. Source718bbd9 authenticates1466 identities; copied
regular blobs/modes verify before and after, Gitlink opaque. Seven source SUMMARYs
use a closed plain-label grammar: root parts, unnumbered root links and four-space
nested numbered lists. An independent source walker reconstructs all93 chapters/
seven parts with labels, relative paths, parent names, depth and numbering. Full
captured metadata agrees before/after navigation, and both generated chapter-TOC
forms agree:toc.html iframe and the toc JavaScript's literal initial contents.
This does not claim browser execution or generic Markdown semantics. All344
original/captured outputs match every byte normal/O. Canonical107 source inputs
are seven summaries/configs plus93 chapter files; all330 other output candidates
remain explicitly open. Dynamic page-heading insertion is a separate next leg.

Three actual supported SUMMARY changes remove, rename or unnest a chapter in
isolated source copies. Native public builds succeed0; complete original metadata
and both TOC forms differ, qualification1. They are configuration/input controls,
not mdBook defects. Restore only each owned changed SUMMARY and reauthenticate
its entire original source/mode population afterward. All raw captures, native
streams and full output manifests remain generated on-volume diagnostics.

Initial zlib and shared-JSON encodings exceeded the remaining fixed task-family
budget. The final tracked codec retains complete TOC metadata, reconstructs all
107 source pins from authenticated immutable Git indices, and inherits the closed
344-file baseline from published LC0038 plus exact changed members. Exclusions
retain all330 members/order by baseline indices. Whole metadata and old book seams
round-trip exactly; all originally qualified producer function ASTs stay unchanged.
Use standard-library XZ preset6 with explicit8MiB dictionary; XZ decoder memory is capped
at64MiB; metadata/reconstruction at524288B, authenticates all streams and rejects
trailing data. Six corrupted captures refuse normally and optimized. Protocol
bodies and omission manifests keep fingerprints, not new retention promises.
Missing pinned source/producers refuse without fetching; no archive seal or raised
cap. Full prior24876B artifact prefix and book teaching retained. Source/history/
mode/cap/staged inverses, focused12/sharder12/seven books and rendered/literal checks
qualify before normal COMMIT. No Rust/LIVE/CPU acceptance or full-adoption change.
Own task-family byte containment next before heading/search work continues.

## _(2026-10-16)_ — public navigation depth refusal (LIVE-CONTAINMENT.4i2b5ar)

D77 is the observed copy.deepcopy(book) RecursionError in the public navigation
API. Catch that runtime depth failure at preprocess and translate it into the
existing NavigationRefused type. Main already emits the named refusal2, zero
stdout, no traceback. No invented depth cap or recursion-limit change; depth20
and every valid source/rendered byte remain unchanged. Permanent new test
constructs1200 nested nodes iteratively and builds CLI JSON without recursively
encoding the fixture. Explicit normal/-O children clear inherited PYTHONOPTIMIZE.
Before repair27 tests/two CLI failures and one API error normal/O; after27/0.
All26 original method ASTs remain exact; no new shell arm or LIVE count change.

The tracked qualifier's --working-code overlays only consumer/probe bytes/modes
on the authenticated1459-identity source data. It authenticates the original
copy first, then explicit working expectations on all baseline/route-omission
fixtures. Code pins distinguish source Git provenance from working fingerprints.
Immutable16/1 stays measurable normal/O; current16/0. Whole93 chapters/344 files,
54 source and110 rendered rewrites,3240 hyperlinks/exclusions agree independently.
Three original actual route omissions remain; removing only the new catch restores
D77/qualification1, while all other15 public cases stay correct. Permanent probe
is27 tests in working copies and unchanged26 on immutable replay.

Retain the full106266B published include-readers prefix. Four complete metadata
matrices reconstruct losslessly from the prior capture via explicit mixed-key
patches and added working fields, including full new omission observations.
Whole protocol bodies keep original canonical fingerprints; generated raw bodies
are diagnostics, not a new retention promise. Retain the complete prior book seam
before current teaching. Complete source/history/mode/prefix/cap/staged inverses,
focused12/sharder12/seven books and normal/print/literal checks qualify before
normal COMMIT. No Rust/LIVE/processor/full-adoption change. Next generated
TOC/search LC0040, then resources; full graph/adoption remains owned by LC.4.

## _(2026-10-16)_ — recurring cleanup preserves qualification evidence (ARTIFACT-CLEANUP.7)

Latest cleanup2026-10-11T18:24:49Z is over24h old. Start clean d3d2904 after
LC0038 hooks/exact post/brief0/unrestricted host census. Reuse the standing
safe-cohort tool on target/.app-data: no symlink/nested-Git/foreign-device
traversal, select only untracked known incremental Cargo outputs. Save every
relative path/device/inode/mtime/size/SHA and all retained byte/SHA identities.
Complete cohort preflight, then recheck each candidate immediately before unlink.
Actual unrestricted pre-delete census reports handoff: OK/no project job.
Changed candidate SHA and totals refuse before deletion normal/O.

Measured event2026-10-16T21:24:43.629148+00:00:18caches/77596881B removed;
C-engine6/46660983B and C-guest-image12/30935898B. Immediate selected residue0;
all10701retained files/131474223B byte/hash-exact. Release/deps strays0, four
nested Git roots skipped. Keep all diagnostic/reference logs, qualification
captures, source fixtures and unknown inputs. Later gates may rewrite logs or
regenerate caches; the receipt describes this immediate event. Latest single
record reaches normal/print through the existing include; no book source growth.
External README/containment package unchanged from reviewed21f4d3d; claim source
still9f99df25. Complete original task/index/history inverses, unrelated source
identities/modes/Gitlink, fixed caps, focused12/sharder12/seven books and exact
rendered receipt qualify before normal COMMIT. CPU/LIVE/full adoption unchanged;
next LC0039 D77 repair. Scratch remains project-local target/artifact-cleanup-0064.

## _(2026-10-12)_ — qualify actual book navigation (LIVE-CONTAINMENT.4i2b5a)

LC0038 separates actual owned navigation from later generated TOC/search and
resource review. Source213f818 authenticates1459 identities; all1458 regular
blobs/modes are copied/verified, Gitlink opaque. Public mdBook0.5.4 builds seven
books in original, captured-consumer and pass-through-navigation bundles per
mode. Original/captured344-file manifests and every byte agree. Captured before/
after protocol books contain93 complete chapters; only54 declared destinations
change, all other text/examples/labels/metadata exact. Independent quoted-anchor
HTML spans plus declared route contracts transform the whole bare bundle into
the actual bundle:110 rewrites/12 files, all3240 hyperlinks and3130 explicit
exclusions. All non-HTML assets remain byte-equal. The project index is authored;
six model index aliases are first authenticated against their original chapter.

Actual Path.open reads are complete units.sexp bytes/digest/order: project0,
RV64I1,DSP1,netboard5,UART2,NIC2,RV64GC41. Task/history destinations are statted,
not body-read; module import/stat operations are outside byte-read trace claims.
Sixteen real public cases preserve supports0/unsupported1 and named refusal2.
One injected registry-open fault fires once. D77 alone fails: depth20 nested
Chapter/sub_items passes0, depth1200 triggers copy.deepcopy RecursionError/
traceback1/no stdout. Main catches ValueError/OSError/TypeError, not this depth
failure. LC0039 owns priority1 repair immediately next. Actual copied task/
history/sibling route omissions each execute all seven captured books0, then
fail whole expected-book qualification1; original26 controls pass normal/O.

Preparation errors were corrected from actual evidence: project authored index
is not an alias, and registry reads use Path.open rather than read_text. Neither
is a source defect. Final normal/O clean selectors return1 with D77 only.
The complete17280B published prefix and prior book seam are retained. Inline
zlib/base64 encodes complete bounded metadata rows/manifests/exclusions/cases/
reads losslessly, with47 optimized runtime overrides. Whole protocol bodies
have canonical byte/SHA fingerprints and pinned-source public replay; raw bodies
and build logs are generated diagnostics, not an archive-retention promise.
A bounded standard-library decoder authenticates compressed and metadata
identities. Source-context/log hashes vary with runtime fixture/time; this is
explicit, not silently normalized. Whole history/source/mode/inverse/cap and
focused/seven-book/rendered/literal checks qualify before normal COMMIT.
No existing consumer, archive, capacity, processor or full-adoption change.

