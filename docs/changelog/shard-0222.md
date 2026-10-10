# DEV_NOTES shard — _(2026-10-09)_ … _(2026-10-09)_

> Sharded from `DEV_NOTES.md` under its 48 KiB ceiling (`doctrine/readme_routes.tsv`).
> Entries in a shard are **never edited after the shard** — git history is canonical.

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

