# DEV_NOTES.md

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

## _(2026-10-09)_ — complete the effective contract without copying obsolete assumptions (P4-SYSTEM.13 a)

The shared gate measure reports 55 records / 53 effective / 106 checks / 20
realized. A complete per-record census separates scope predicates from executable
guarantees. Five remaining scalar boundary topics need GC-specific records; time,
fetch and partial progress already have GC dispositions. The pinned priority
table distinguishes address triggers from environment break; the frozen blanket
no-breakpoint phrase contradicts C.EBREAK cause 3. Own its supersession alongside
the qualification and pipeline-stage corrections. No engine change or premature
check credit. Promotion declined in the leaf; versioned records/book retain it.

## _(2026-10-09)_ — C signoff retains its limits and retrieval path (P4-SYSTEM.12 e2e)

The named full make ci passes every leg on the completed C implementation: core
153, DSP 17, verify 193; doctrine/wasm/bench-smoke/books green. Leaf acceptance
covers its declarations, compiled controls, independently authored corpus and
precise fault restart, with the measured Sail timer limit retained. Close .12,
P4 12/18, then complete/realize v2 at .13. Move 100,163 B of closed live-head
sections verbatim into archive part 6; reverse every replacement and assert the
full original file reconstructed. Archive remains within 131,072 B; the active
head becomes about 34 KB. No code change. Promotion declined in the leaf.

## _(2026-10-09)_ — distinguish an adapter gap from timer supply (P4-SYSTEM.12 e2d)

All 37 C forms occur in actual Sail rows: 27 guests / 412 boundaries agree twice.
The parcel author's numeric interrupt annotation was absent from the legacy adapter;
a witnessed event reproduced the refusal. Accept both exact spellings with the same
cause/event requirement, retain missing/wrong-event and row controls, and mutate the
new support away. c-irq still differs at 9 because the public reference supplies no
STIP in the zero-stimecmp probe. Its seven-boundary diagnostic and config variants
are tracked, with exact fresh repeats; no source inspection or fitted expectations.
A wrong C.LI expectation fails a fresh run at 0. GUEST-GEN 128/128, 627 registered
arms. Current reference prose drops implementation assumptions; .14 owns the wider
maintained-knowledge sweep. Promotion declined in the leaf.

## _(2026-10-09)_ — the C bind changes only independently declared extents (P4-SYSTEM.12 e2c)

The staged 28 C programs/records land exact alongside the complete composition,
200-form scope, v2 C/fetch records, registry and matrix. All 139 older sources and
non-count record bytes remain exact; their PC/mode/write traces match the saved
parent CLI byte-for-byte. Five public-CLI C traces distinguish the parent. Fetch
counts total 9,770 actual parcels, derived before adoption, not blindly doubled.
The ignored manifest's fingerprint closure changed after author prerequisites;
re-derivation kept all guest rows identical before adoption.

Integration exposed omitted C scope grammar/mapping and part sums, omitted
expansion semantics, and a stale-exception control failing for a copied wrong
observation. Repair each owner, delegate expansion validation to SEM, and require
the control's actual refusal. Three registered arms, including all 17 Python contract controls; total 626. make check passes all 167;
registry 20/106, v2 open, CPU-SYSTEM 8/10 axes open. Current resolution-era dossier
and P4 overview claims corrected; historical frozen records retained for .13.
A full gate with exported GIT_INDEX_FILE was invalid: nested Git controls replaced
that disposable index. Real index digest remained exact; use normal staged hooks
for the full gate. A final registry census corrected the draft's assumed registration:
RV64GC remains unregistered, with its dedicated book now explicitly owned by .14. Promotion declined in the leaf.

## _(2026-10-09)_ — historical text and new extent have separate derivations (P4-SYSTEM.12 e2b)

A C-composed snapshot rejects the 42 historical captures after only their parcel
counts migrate. Keep the word-derived text, independently compare parcel writes and
actual requests, then transform only the count. The helper is shared by author and
mirror. Default canonical word writes refuse; explicit parcel writes keep their new
route provenance. Four mutants discriminate. The unstaged cold test correctly found
the new helper missing from git ls-files; a temporary index includes pending inputs
without changing the real index. Promotion declined in the leaf.

## _(2026-10-09)_ — count migration is narrower than a mirror waiver (P4-SYSTEM.12 e2a)

The prior governor refuses staged parcel extents as full-byte drift. Its replacement
selects C through the shared assembler, independently checks every supplied trace and
request extent, and transforms only the owner's direct fetches field. Strings, nested
fields, comments and CRLF remain bytes to compare. The seven historical exceptions
must still differ after normalization. Four weakened-check mutants fail; the unbound
production route remains 91 exact / seven declared. Promotion declined in the leaf.

## _(2026-10-09)_ — stage C observations before executing the model (P4-SYSTEM.12 e1d2)

The tracked producer declares 28 programs and budgets covering 37 compressed forms.
The independent author derives 429 boundaries / 708 parcels; hand checkpoints pin
signed/scaled limits, word overflow, aliases, hints, D memory, pc+2 links, IRQ return,
LR/SC, reserved/FS-Off traps and ILEN=32 bits. Adapt the public Sv39 guest's next leaf
to non-executable: final-halfword C.NOP succeeds, a required second parcel faults;
both runs issue 101 requests but take 52 versus 51 boundaries. New expectations
validate, repeat exactly and reject observation/extent or saved-budget corruption.
Production files stay exact. Promotion declined in the leaf.

## _(2026-10-09)_ — count actual requests before migrating extent (P4-SYSTEM.12 e1d1)

All 139 historical traces match the independent parcel author at 4,913 declared
boundaries. Actual request logs total 9,770, versus 4,888 prior word requests;
five guests differ from blind doubling because of runoff or fetch faults. The
tracked census stages a deterministic fingerprinted manifest, rejects changed
observations/extent and detects a damaged saved count. Production records stay
exact until the bind. Promotion declined in the leaf.

## _(2026-10-09)_ — recurring cleanup (ARTIFACT-CLEANUP.4)

Census, tracked/symlink exclusions and exact deletion remove 249 incremental bins /
861,367,249 B; residue zero. Evidence and inputs retained. Actual process census
clear. Promotion declined in the leaf.

## _(2026-10-09)_ — filenames do not carry capture history (P4-SYSTEM.12 e1d0)

emit's fallback stamped generic/C outputs as the FP corpus. Historical headers now
require a canonical owned word input; new outputs name the actual author/route.
No chronology is invented. Generic, borrowed-name, C/schema and parcel controls
pass; four mutants fail, 42 owned records exact. Promotion declined in the leaf.

## _(2026-10-09)_ — recover hosted proof and preserve its clocks (CI-RECOVERY.4 f)

The crash left this receipt staged. Rust, doctrines and all portability legs pass
at 76882c8 after the cold CSR fixture fix; the exact-SHA artifacts confirm native
and endian each pass 153/153. The scoped push approval is fulfilled. First run's reported
1294-second durations differ from GitHub's 771/779-second step spans: Miri's default
isolation simulates clocks. Preserve raw receipts, use external time for elapsed
comparisons, and leave isolation unchanged. Promotion recorded in the timing reference.
The sandbox's census is invalid because ps is denied. The actual census finds Kimi
with two read-only AGENTS.md handles; the director authorizes closure. SIGTERM stops
the app and five helpers, zero survivors; the actual census then reports handoff: OK.
CI-RECOVERY closes 4/4; P4 staging is the next action, left for the resumed session.

## _(2026-10-08)_ — warm reference data masked an incomplete fixture (CI-RECOVERY.4 e)

A tracked-only snapshot reproduces the parcel probe's mtvec failure: its temporary
unit omitted state/profile metadata and used the local CSR CSV fallback. Copy the
unit owners; use 0xf11 for the intentionally unmodeled mvendorid case. --cold runs
the public probe from a temporary tracked-only snapshot, with local temp/bytecode
stores and no external reference data. Missing metadata and external-name controls
both fail by their CSR diagnosis; native 104/104 passes. All 42 owned records and
the 176 legacy observations remain exact. Promotion declined in the receipt.

## _(2026-10-08)_ — a refused self-test must expose its cause (CI-RECOVERY.4 d)

The repaired hosted doctrine job provisions mdBook, then refuses GUEST-GEN. Its
wrapper discards self-test output. Local controls pass 103/103 on Python 3.14 and
3.11, so that does not identify the hosted root. Keep a target-local log, bounded
failure tail and failure-only artifact. Forced interpreter failure stays rc=2 and
retains its sentinel; no oracle or self-test change. Actual hosted cause remains open.
Promotion declined in the receipt.

## _(2026-10-08)_ — approval act completed (CI-RECOVERY.4 c)

Both full local suites passed; SEMULITH-PUSH-0001 pushed in f4364bc. Three hosted
run IDs are in the tree. Running checks remain unverified; no new code in this receipt.

## _(2026-10-08)_ — CI repair has bounded push authority (CI-RECOVERY.4 b)

The director approves necessary recovery pushes without another question until
GitHub CI passes. Record the scope and all-three-green expiry in a decision and
COMMIT/book; preserve the full-CI/ledger act and ordinary cadence afterward.
This grants no Kimi closure/exemption. No hook or cadence code changes.

## _(2026-10-08)_ — record the handoff reader without inventing authority (CI-RECOVERY.4 a)

The actual process census refuses Kimi Code PID 1292. Targeted lsof identifies two
read-only AGENTS.md descriptors, with no other repository handles for that PID.
The census counts any repository handle, so this result is expected under its
contract. No project verification job remains. Own closure/exemption with .4;
only the director may sanction a process, and another editor is not ours to kill.
Exceptional push approval is separately pending. Promotion declined in the receipt.

## _(2026-10-08)_ — confirm the repaired pipeline before publication (CI-RECOVERY.3 b)

Immutable-script native and powerpc64 Miri runs each execute all 153 core tests, zero
failures/ignored, about 22 minutes each. Full local CI then passes on Rust 1.99 with
the pinned book tool: check, gate, bench, smoke-bench and book all green. Code bytes
match the verified snapshot. These close the local repair, while .4 retains hosted
verification and the exceptional push approval boundary. Historical measurements and
the invalidated earlier run are not substituted for this evidence.

## _(2026-10-08)_ — cold portability paths and truthful verdicts (CI-RECOVERY.3 a)

Cold single legs lacked their output directory and Linux queried a macOS-only nightly.
Common local stores and one dated pin repair both. Local Miri setup also exposed workspace
membership and missing toolchain dependencies: exclude target workspaces, synchronize both
locked manifests through public Cargo vendor, and set separate explicit Miri sysroots.
Decorated Rosetta red was ignored by the full verdict; decorated green failed its selector.
Count prefixes/unknown failures, compare current native output, and refuse failed digests.
Controls 9+15 pass; immutable-snapshot native Miri 153/153 passes. Endian confirmation is
pending. An earlier run edited mid-flight is invalid evidence and was stopped. Failure tails
and log-only CI artifacts preserve diagnosis. Promotion declined in the owning receipt.

## _(2026-10-08)_ — a mandatory book gate needs a provisioned tool (CI-RECOVERY.2)

The clean doctrine runner had no mdBook. The installer pins official 0.5.4 release
identities, verifies before extraction, and installs under .app-data/ci-tools; target/
holds the cache. The workflow adds its bin directory to GITHUB_PATH before the gate.
Rustup/Cargo/temp locations also derive from the repository, with self-update disabled.
Cold PATH reproduces the old refusal; the new native tool builds all five model books,
7/7 controls pass and corrupt cache is refused before binary replacement. Linux asset
identity/layout verified; actual Linux execution stays with hosted verification in .4.
Public stable/wasm provisioning succeeds locally. Promotion declined in the leaf.

## _(2026-10-08)_ — reproduce the hosted toolchain (CI-RECOVERY.1)

GitHub Rust 1.99 denied a lint unseen by local 1.95. Exact-toolchain reproduction also
found three SHA constant-chunk lints. Replaced the identity map with unwrap_or; used
array chunks for SHA words, full blocks and padding, preserving the remainder and
making compression accept exactly 64 bytes. No lint suppression or result change.
Rust 1.99 make check passes; 259 deterministic inputs match Python hashlib. Existing
benchmark 14/14 and SHA 2/2 suites also pass under 1.95. Project-local tools/cache/temp
live in .app-data/target; no shared toolchain writes. Promotion declined in the leaf.
These local results do not establish hosted CI green; workflow repairs remain next.

## _(2026-10-08)_ — a bounded history head needs an archive terminal (LIVE-CONTAINMENT.4 a)

The live shard family had 2,114 B left while the next whole-record cut needed 2,377 B
before metadata. Sharding controlled file size but retained the aggregate scaling term.
The director approved sealing 210 older shards with their exact manifest. The tracked
284,500-byte object preserves 211 members, 781,740 source bytes and 9,639 lines. Copy,
verify every member, retire only exact duplicates: no byte of historical content lost.

The bounded descriptor/reader authenticates objects, manifest and every member. The
freeze gate compares predecessor rows against the logical live/archive union and keeps
committed descriptors immutable; heading/location uniqueness covers both. The sharder
uses archived filenames when allocating numbers. Gate temporaries now use target/.
The finite three-file terminal is registered; no existing cap moves. A future seal
needs a separate finite capture/transition. Full doctrine adoption remains in .4.

- Validation: SHARD-FREEZE 31/31 (old 14 + positive/16 negative archive controls),
  sharder 12/12; actual 210-source reconstruction exact, zero retired-file residue.
  Read/check works without Git history; controlled corruption/unsafe/oversized/duplicate
  data and changed committed descriptors refuse. Complete logical partition passes.
- Promotion: declined — descriptor schema and permanent controls encode the lesson.
  CI-RECOVERY owns three hosted failures plus the Linux cross-endian toolchain defect;
  local pre-push green had not established hosted CI green. Repairs precede C staging.

## _(2026-10-08)_ — independent translation cache (P4-SYSTEM.12 e1c1)

Hart.walk always rewalked PTEs while SFENCE emitted flush prose. Added the selected
four-slot FIFO cache from state.sexp and pinned supervisor rules: 4-KiB keys, 16-bit
ASIDs, inherited globals, cached leaf/A/D bits and live permission checks. Legal fences
select register identity; illegal fences have no cache effect. Failed translations
never install. Direct permission fixtures now fence explicit PTE edits.

- Validation: parent ff75610 RED; 13 mutations RED; GUEST-GEN 103/103. Census 139/139
  architectural traces exact, zero refusals; 120/121 prior word texts exact, only the
  known incorrect unadopted cache guest corrected. All 42 owned records byte-exact.
  Production records/counts unchanged. Full evidence: docs/tasks/P4-SYSTEM.md e1c1.
- Promotion: declined — permanent hand fixtures and RED controls retain this lesson.
  Archive-family pressure is routed to LIVE-CONTAINMENT.4 before further appends.

## _(2026-10-08)_ — a zero operand value is not register x0 (P4-SYSTEM.12 e1c0)

SFENCE used values to choose scope, losing x0 register identity. Three evaluator tests
fail on c413dd3; history e839c1b introduced the value-only API. Nonzero registers holding
zero must select page/ASID zero, retaining other entries and globals under the declared
no-over-fence policy. The old fixture also encoded wrong registers and refilled in M.

The semantic effect now carries values and identity flags; None is x0, Some(0) a real
zero selection. Corrected raw words and armed the S refill with an occupancy assertion.
Four stale gate mutations now replace exactly one parsed effect; obsolete arity refuses.
Full root/history and verification: docs/tasks/P4-SYSTEM.md e1c0 and the Sv39 book.

- Validation: parent 0/3 then green; two selector mutations RED; translation 29/29;
  make check (153 core, 17 DSP, 193 verify), DEF-GEN 56/56 and books green. Scalar
  definition changes only two generator digests. Corpus/profile/counts unchanged.
- Promotion: declined — permanent regressions, typed API and arity gate retain the lesson.
  Independent author cache is next. New summaries kept bounded after archive pressure.

## _(2026-10-08)_ — CSR vocabulary and quoted annotations (P4-SYSTEM.12 e1b2)

The remaining three parcel refusals were mcounteren's missing address and a source
annotation containing quotes. Registered mcounteren/scounteren/menvcfg, legalized the
selected CY/TM/IR and STCE fields, retained WPRI and ignored unimplemented HPM fields.
S stimecmp read/write needs both mcounteren.TM and menvcfg.STCE before own effects;
M bypass and U address privilege remain intact. Counter accessibility changes no value
or progression. Writable counter rebasing remains an explicit bounded-author refusal.

records_sexp.quote_string exposes the existing canonical escape table. Its form renderer
and the expectation emitter share it, so quotes, backslashes, control characters and
Unicode round-trip for program, instruction, derivation and source. Removed the parcel
annotation refusal; historical word routing is unchanged. No engine trace provides values.

- Validation: masks/WPRI/alias, 30 counter/timer mode gates, read/write unit discipline,
  annotation/all-field literal round-trips, non-string refusal and emitted schema. Eight
  mutations and parent f099905 fail; three formerly refused guests match 117 steps.
  GUEST-GEN 89/89. All 121 prior word texts and 42 owned records byte-identical.
- Census: 138/139 architectural traces exact, zero vocabulary refusals; sv39-tlb-fence
  steps 191/192/195 remain the owned cache-policy disagreement. Fix e1c before staging
  C/counts. Production images/records/counts unchanged. Completed e1b1 receipt archived
  verbatim; DEV_NOTES crosses its fixed ceiling and shards with byte/order proof.
- Promotion: declined — permanent mode/string fixtures and eight RED controls retain
  this bounded-author lesson; the cache's schedule and reproduction are in the tree.

## _(2026-10-08)_ — author vocabulary is distinct from illegal instructions (P4-SYSTEM.12 e1b1)

Seventeen pre-bind refusals named valid integer operations whose computations or stock
prose were missing from the independent author. Added comparisons/XORI, XLEN and word
shifts, signed/unsigned branches and narrow load/store rules from the pinned chapters.
SLTIU sign-extends its immediate before the unsigned comparison; W shifts mask counts
to five bits, operate on the low word and sign-extend the result. Branch offsets remain
byte-relative and may target a two-mod-four address in this profile.

Reserved W shift bits are independently known. ReservedInstruction names that outcome
before effects, and the parcel route alone delivers the declared raw-word diagnostic.
Generic unknown valid vocabulary remains a Refusal. The older XORI/LBU negative controls
now use the real unmodeled mvendorid CSR, so extending coverage does not drop that guard.

- Validation: 22 hand arithmetic/alias/x0 cases, ten branch cases, narrow memory
  sign/width/alignment and three reserved raw words. Eight mutations and parent c70693d
  fail; 17 formerly refused guests match 471 architectural steps. GUEST-GEN 80/80.
- Regression: 105 prior historical word texts and 42 owned records byte-identical;
  16 new word outputs not adopted/written. All 139 parcel guests: 135 exact, one owned
  cached-translation disagreement, three named CSR/directive refusals. Record hashes
  unchanged. e1b2 owns the remaining vocabulary, e1c the cache, before count adoption.
- Containment: e1a receipt and closed .11 design/split moved verbatim to archive part 5;
  reconstruction asserted, fixed ceilings preserved. Promotion: declined — hand fixtures
  and eight mutation controls retain the lesson; remaining gaps are scheduled in the tree.

## _(2026-10-08)_ — accepted privilege paths needed independent guards (P4-SYSTEM.12 e1a)

The pre-bind census ran all 139 historical guests with their already-declared budgets.
It found 113 exact architectural traces, four disagreements and 22 named refusals. Three
of those disagreements came from missing author rules: misa had no fixed reset/read-only
field handling; satp/SFENCE ignored TVM; SRET ignored U/TSR legality. Existing known CSR
privilege failures raised model Refusal instead of the architectural illegal instruction.
The task owns every disagreement/refusal before adoption: privilege here, vocabulary next,
and the declared cached-translation policy after that. No engine trace supplies counts.

misa now fixes RV64 plus A/C/D/F/I/M/S/U, matching the independently selected laboratory
policy. Writes ignore its read-only fields without making its RW address illegal. Known
CSR access faults and xRET/SFENCE legality deliver original bits before own side effects.
M-mode ignores S interception; legal returns retain the existing mode-stack rules.

- Validation: fixed reset/ignored writes/alias, CSR unit discipline, MRET lower modes,
  SRET U/TSR, SFENCE U/TVM, satp read/write TVM, M bypass and legal controls. Nine mutations
  fail behaviorally; parent 132506f RED. Five mode-matrix guests match 140 architectural
  steps, including two previously refused CSR-permission guests. GUEST-GEN 71/71.
- Regression: all 97 prior historical-route texts and 42 owned records exact; eight extra
  historical-route outputs are not adopted or written. Full parcel census now 118 exact,
  one cache disagreement (sv39-tlb-fence) and 20 named vocabulary refusals, all owned.
  Production unit/images/records unchanged. Cache repair is scheduled before C counts.
- Promotion: declined — permanent mode/field fixtures and nine behavioral controls retain
  this author lesson; the full-census findings and immediate schedule live in the tree.

## _(2026-10-08)_ — source length is not a guest budget (P4-SYSTEM.12 d3d2)

The independent author has an explicit parcel route, selected by --parcels --steps N.
It loads exact sized units, fetches current memory each step, and keys directives by
byte PC. The declared 1..10000 boundary budget governs source run-off, faults, pending
interrupt delivery and halted ticks; source end comments cannot shorten it. Refused
fetches count, failed translations do not, and delivery/wait boundaries never retire.
A store patch is visible to the next fetch, including a compressed unit in a word store.
Known reserved C/wider-prefix bits follow the laboratory diagnostic; unknown valid
vocabulary still refuses. All requested derivations finish before any record is written.

- Validation: hand mixed image/PC/writes/annotations, repeated spellings, source run-off,
  upper-parcel refusal, full ILEN diagnostics, code patch, pending-before-fetch, halted
  ticks, retirement and bounded-budget/refused-batch controls. Eight mutations RED;
  parent 740efda RED (API absent). GUEST-GEN 61/61; 97 prior texts and 42 refusals exact;
  all 42 owned records exact. Newly emitted documents validate against the schema.
- Five already-owned gaps repaired on the new route using budgets declared first:
  dir-runoff 3 steps/5 parcels, fault-fetch 3/5, it-prio-jump 4/7, sv39-straddle 52/104,
  sv39-perm-rwx 114/226. All 176 committed architectural observations match. Parcel
  counts are independently derived and differ from the old word-request convention;
  old records stay untouched until the C bind changes their declared extent together.
- Promotion: declined — permanent byte/budget/visibility fixtures and eight mutations
  retain this bounded authoring lesson. Next: staged corpus/count derivation, then bind.

## _(2026-10-08)_ — independent parcel fetch needs a correct walk (P4-SYSTEM.12 d3d1)

The author now fetches from memory under the selected C/ILEN=32 profile. Each required
parcel walks first, then issues exactly two bytes. Refused physical requests count;
translation failures issue none. A second-parcel fault keeps the instruction start in
EPC and the failed virtual address in tval. Wider prefixes retain all ILEN bits, while a
compressed parcel at a region/page end leaves its neighbor untouched. Unwritten in-region
bytes remain zero. Fetch does not tick time or retirement; guest boundaries own those.

Four existing walk defects were reproduced before repair: canonical sign validation
ignored bit 38, reserved high PTE bits passed, a bottom-level pointer raised author Refusal,
and M-mode data skipped MPRV/MPP translation. The corrected Svade walk also rejects reserved
non-leaf U/A/D while retaining RSW/G, and applies permissions to effective data privilege.
Odd-PC fetch fixtures exposed a fifth defect: exception/interrupt delivery assigned EPC
without clearing bit zero. M/S delivery now masks that bit while retaining bit one.

- Validation: pure hand-parcel/PTE fixtures, both canonical signs, all ten reserved high
  bits and four access kinds, non-leaf levels, MPRV/SUM/U, exact request/refusal schedules,
  translated straddles, starting EPC/failing VA, M/S/interrupt EPC, and no walk writes.
  Parent f8f213c is RED; nine mutations fail for their intended behavioral reasons.
  GUEST-GEN 52/52; complete before/after census 97/97 exact, 42 refused unchanged;
  all 42 owned records exact. No historical observations overwritten. Old guest route
  remains word-based until d3d2 explicitly integrates byte execution and declared budgets.
- Promotion: declined — the independent component, permanent fixtures and nine mutation
  controls retain the local fetch/walk lesson. Completed receipts archived verbatim.

## _(2026-10-08)_ — a wider prefix still needs ILEN diagnostic bits (P4-SYSTEM.12 d3d0)

The C evaluator stopped after its first parcel when the lowest five bits were all ones.
That identifies a wider instruction, but the nonzero illegal-instruction diagnostic must
contain min(actual length, ILEN, MXLEN) bits; ILEN=32 here. An all-ones 32-bit instruction
was reported as 0xffff, and a second-parcel fault was suppressed. Only true compressed
prefixes now finish after one parcel. Wider prefixes read two, preserving all ILEN bits
without requesting a third. The diagnosis came while deriving the independent author fetch.

- Validation: three new cases (all-ones/other prefix bits, upper access refusal, translated
  second-page fault) fail on b48201c and the short-ILEN mutation; repaired C probe 18/18.
  DEF-GEN 55/55; make check green. Production C remains unbound; old records unchanged.
- Containment: the sharder now states the governed ceiling without claiming it was
  crossed; lower targets are allowed. Header checks fail on the old wording (10/2),
  then pass on the corrected producer (12/0). Only the new shard is regenerated.
- Promotion: declined — permanent probes and mutation retain the fetch lesson; the
  sharder's header tests retain its reporting repair. Independent walker/fetch follows.

## _(2026-10-08)_ — independent C rules keep lengths and original bits (P4-SYSTEM.12 d3c)

The author lacked C decoding and five base shapes needed by compressed instructions.
A separate spec_c.py reconstructs fields and base words from the pinned chapter and its
three public SVG listings, without reading engine/assembler mappings. execute_c passes
length 2 and original parcel bits to the existing spec-side base rules; normal word callers
retain length 4. C.JALR reads old rs1 even when it links into that same register. Missing
SRAI, ADDIW, ADDW/SUBW and JALR rules use fixed-bit guards; W results truncate/sign-extend.
Reserved parcels and FS-Off traps retain the original 16-bit tval. FP loads dirty FS;
read-only stores retain the declared Precise state. The unused ADDIW locator is repaired.

- Validation: 37 expansion/effect cases, 22 limits, 79 one-hot immediate bits, 11 reserved
  parcels, 10 hints, two branch outcomes, link aliasing, memory/FP and word-overflow checks.
  One-hot cases catch a bit permutation that all-ones limits miss. Six mutations RED;
  GUEST-GEN 42/42; 42 owned records exact. All 91 older emitted texts remain exact.
  New JALR vocabulary emits six other guests; three show the already-owned source-end/fetch
  gaps. Their names and immediate d3d repair schedule live in the tree. No record overwritten.
- Promotion: declined — the independent component, permanent probe and six mutation controls
  retain this bounded lesson. Guest parcel fetching/budgets and production binding follow.

## _(2026-10-08)_ — absence is not a no-write instruction (P4-SYSTEM.12 d3b)

The scratch comparator skipped any absent row whose expected writes were empty and ignored
process status. A failed process with an empty trace could agree with an ordinary nop.
The tracked adapter requires every ordinary row and successful fresh output. A declared
interrupt or fetch-delivery gap instead needs its matching numbered trace event; unknown,
malformed, duplicate and orphan records refuse. Exact assembler bytes pass through the
tracked ELF writer's public API, removing the scratch compiler-path assumptions. The binary
is digest-checked against the dossier and the override comes from the existing conversion
owner. Two executions must produce byte-identical traces. Comparison remains declared GPR
change-observations, not unrecorded state.

- Validation: four behavioral absence mutations RED; GUEST-GEN 35/35. All 95 cached corpus
  traces audited: 79 from AGREE-claimed cells pass the new comparator (nine interrupt and
  one fetch-page-fault event gaps, no ordinary gaps); sixteen named not-matches unchanged.
  Cached process statuses are unavailable. Fresh M 4/4 verifies status and 99 observations,
  with repeat traces identical. A temporary mixed C image verifies five hand-derived pcs,
  words and writes, including a word at 2-mod-4 and a trailing parcel; repeats identical.
- Promotion: declined — the permanent adapter, offline probe and mutation controls retain
  this local lesson. Wider experimental policy remains owned by P4-SYSTEM.14.

