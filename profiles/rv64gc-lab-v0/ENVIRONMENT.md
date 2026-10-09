# `rv64gc-lab-env` — the environment contract for `rv64gc-lab-v0`

Contract ids: `rv64gc-lab-env-v0`, `rv64gc-lab-env-v1` (extends v0), and
`rv64gc-lab-env-v2` (open, extends v1).
The records live one per line in [`contract-obligations.sexp`](contract-obligations.sexp)
and its explicitly included [v0](contract-v0.obligations.sexp) and
[v1](contract-v1.obligations.sexp) parts; which
records make up which version is [`contract.sexp`](contract.sexp) (schema `schema/contract.sexp`),
judged by **CONTRACT-FREEZE** (`scripts/check_contract_freeze.sh`): every record belongs to
exactly one version, and a frozen version's records are pinned by sha256 — a statement that turns
out wrong is **superseded by a later version, never rewritten**. Written at `P4-SYSTEM.9` (`2026-10-06`), updated through `.13` c5 (`2026-10-09`).

`scripts/record_catalog.py` expands repository-root-relative includes in order.
The c2 split reconstructed the original 63,014 bytes exactly, preserving its 58
records and frozen hashes. Subsequent additions live in the root. Schema validation judges every source part before
cross-record checks. This containment change adds no contract credit. See
`docs/decisions/decision_obligation-catalog-parts.md` for the include contract.

## The versions

| Version | Status | Members | What it is |
| --- | --- | --- | --- |
| v0 | frozen | 46 | everything `P4-SYSTEM.1`–`.8` declared — every one a CPU guarantee, the 13 rv64i base mirrors among them |
| v1 | frozen at `.9`'s close | 6 (+ v0's, minus 2 superseded) | the four environment assumptions below, and two corrections |
| v2 | open; `.13` owns completion/freeze | 9 (+ inherited v1, minus 4 superseded) | M, C, parcel supply, qualified FP, current route, fault priority, physical byte addresses, data access and event positioning; two boundary assumptions remain |

## The boundary inventory, dispositioned (`docs/CPU_ENVIRONMENT.md` §2)

| Boundary item | Disposition | Where |
| --- | --- | --- |
| Translation | **in scope** | `OB-GC-ENV-TRANSLATION-INPUTS` (v1); `OB-SV39`, `OB-SVADE`, `OB-WALK-IMPLICIT` (v0) |
| Interrupts | **in scope — none supplied** | `OB-GC-ENV-INTERRUPT-SOURCES` (v1): no CLINT, no PLIC; STIP the hart's own comparison |
| Counter input | **in scope** | `OB-GC-ENV-VIRTUAL-TIME` (v1): the time supply is the virtual-time domain |
| Reservations | **in scope — no external event** | `OB-GC-ENV-RESERVATION-EVENTS` (v1); `OB-RESERVATION`, `OB-SC-DETERMINISTIC` (v0) |
| Waiting | **in scope** | `OB-GC-PRIV-INSNS-V1` (v1): a legal wfi enters the wait; the wake needs no retirement |
| Partial progress | **in scope** | `OB-GC-PARTIAL-PROGRESS` (v0, `.8`): every instruction completes or faults as a unit |
| Fetch | **in scope — 16-bit parcels** | `OB-GC-ENV-FETCH-SUPPLY` (v2): exact requested executable bytes or a declared access failure; no extraneous fetch or side effect |
| Address units | **in scope — physical 8-bit bytes** | `OB-GC-ENV-ADDRESS-UNITS` (v2): full unsigned 64-bit addresses; translated instruction/data accesses and physical PTE reads; direct typed pair |
| Data widths/attributes | **in scope — B/H/W/D, little-endian main memory** | `OB-GC-ENV-DATA-ACCESS` (v2): whole responses, low-width stores, executable bytes, no MMIO; direct typed pair |
| Event delivery | **in scope — between steps** | `OB-GC-ENV-EVENT-DELIVERY` (v2): pending/wake before fetch; typed guard rejects in-request attempts; no external source added |
| Reset, ordering | **remaining named gaps** | Two GC-specific assumptions await `.13`; time/fetch/partial progress and code visibility already have GC dispositions |

## The four v1 assumptions — and what would make each false

| Assumption | It is false if … |
| --- | --- |
| `OB-GC-ENV-TRANSLATION-INPUTS` — page-table walk reads are their own request kind, answered from the memory the hart's stores write; the environment never writes a PTE; a refused walk read is the original access's access fault | a walk read returned anything but the stored bytes, or the environment wrote a PTE |
| `OB-GC-ENV-INTERRUPT-SOURCES` — v1 supplies no source: MSIP/MTIP/MEIP read 0 and cannot be written; STIP is the hart's `time >= stimecmp`; SSIP/SEIP are software's | a pending bit became 1 without the hart's comparison or a software write of a software-writable bit |
| `OB-GC-ENV-VIRTUAL-TIME` — one tick per step boundary, retired, trapping or halted alike; instret on retirement only; no host time | time stood still while the hart waited, moved with host time, or instret counted a trap or a halted step |
| `OB-GC-ENV-RESERVATION-EVENTS` — no external invalidation at one hart; a constrained LR/SC loop's first SC succeeds | a reservation vanished without the hart's own LR or SC, or a constrained loop's first SC failed |

## Open v2: compressed execution and parcel supply

`OB-GC-C` states the 37 compressed forms' expansions, compact registers and signed/scaled
immediates, mixed two/four-byte PCs, C.JALR's old-source target and pc+2 link, hints,
breakpoint/reserved/FS-Off outcomes, LR/SC preservation and precise straddling faults.
`OB-GC-ENV-FETCH-SUPPLY` states the environment's narrower role: answer each physical
`FetchParcel` with exactly sixteen executable bits or a declared failure, without extra
requests or side effects. CPU decode chooses whether the second parcel is needed.

The count is actual physical parcel requests, including refused ones. Translation faults
before a request add zero. For example, `c-page-end` executes C.NOP at a page's last
halfword without reading the next page; `c-page-straddle` faults on the second parcel
of a 32-bit instruction at that address, reporting the second parcel VA and original
instruction EPC before effects. Both issue 101 requests, at 52 versus 51 boundaries.

The registry realizes `CHK-GC-C-POS` / `-NEG` over all 28 new C guests and
`CHK-GC-ENV-FETCH-SUPPLY-POS` / `-NEG` over page-end/link and straddle/fetch-fault
fixtures. Across the full registry, including thirteen scope pairs and the
three direct boundary pairs, 54 checks are realized in the effective contract;
the remaining declared checks keep G-CONTRACT incomplete. Frozen v0/v1 text and
pins are unchanged. V2 stays open until `.13` completes and freezes it.

## Supersessions (v1 corrects v0 without rewriting it)

| v0 record (frozen) | Superseded by | Why |
| --- | --- | --- |
| `OB-GC-PRIV-INSNS` | `OB-GC-PRIV-INSNS-V1` | v0 called wfi and sfence.vma's invalidation no-ops; the wait state (`.5`) and the TLB (`.3`) made both wrong |
| `OB-ECALL-EBREAK` (rv64i mirror) | `OB-GC-ECALL-EBREAK-V1` | the mirror says no privileged modes and a harness report that stops; here the trap is delivered to a handler |

The requirement mirrors of the two superseded records still carry v0's text — they mirror the
frozen v0 obligations; the contract is where v1 corrects them.

## Positive and negative fixtures

Every v1 check, `.8`'s partial-progress pair, the M/C/fetch pairs, and the
thirteen scope pairs and c1's priority pair are **realized**: the registry
`crates/semulith-verify/src/contract_checks_rv64gc.rs` binds each check id to tracked guests, and
its tests run the guest entries under the corpus's comparison rule. Scope entries run
`python3 scripts/check_gc_contract_scope.py --check CHECK-ID` over parsed canonical
declarations and violating in-memory copies. The tests refuse a missing check among
the pairs bound so far; G-CONTRACT continues to count all remaining missing pairs. A positive fixture exercises the assumption holding; a negative one exercises what would
falsify it (a refused walk read, a software write that must not take, a counter that must not
move, an SC that must fail for the hart's own reasons).

| Check | Guests |
| --- | --- |
| `CHK-GC-ENV-TRANSLATION-INPUTS-POS` / `-NEG` | sv39-translate-4k, sv39-svade / inj-walk-l2, inj-walk-l1, inj-walk-l0 |
| `CHK-GC-ENV-INTERRUPT-SOURCES-POS` / `-NEG` | i-timer, w-sw / env-irq-sources |
| `CHK-GC-ENV-VIRTUAL-TIME-POS` / `-NEG` | mm-counters, i-timer / w-timer |
| `CHK-GC-ENV-RESERVATION-EVENTS-POS` / `-NEG` | a-lrsc-loop, a-lrsc-pair / a-lrsc-mustfail |
| `CHK-GC-PRIV-INSNS-V1-POS` / `-NEG` | mm-wfi, w-timer, sv39-tlb-fence / mm-csr-legality-u, w-notrap |
| `CHK-GC-ECALL-EBREAK-V1-POS` / `-NEG` | mm-ecall-modes, mm-ebreak / mm-ecall-deleg |
| `CHK-GC-PARTIAL-PROGRESS-POS` / `-NEG` | inj-carrier, inj-atomics, inj-fp, prio-sv39 / mm-csr-ro-write, inj-walk-l2 |

## What is deliberately not here

- **Interrupt sources a platform supplies** (a CLINT's MTIP/MSIP, a PLIC's MEIP): a later contract
  version, the board's (`P5-BOARD`) — v1's environment supplies none.
- **External reservation invalidation** (another hart, a device): `MC-MULTICORE`, as "a new
  contract version; the single-core contract is not edited in place".
- **The G-CONTRACT verdict**: `P4-SYSTEM.10`'s gate report.

## Scope evidence (P4-SYSTEM.13 b2)

OB-GC-COMPOSITION's existing POS/NEG pair now runs a static predicate. It checks
RV64I/XLEN=64, the exact selected extensions, the nine encoding fragments and
complete composition. Six independent copies violate missing C, extra H, XLEN,
unbound C, fragment base and completeness respectively; each must fail for its
own reason. Disabled-profile/disabled-fragment controls fail the negative check,
and an unknown id refuses. No live file is changed by a check. This establishes
the declared selection, not instruction execution or universal conformance.
The 20 existing guest bindings remain exact. At b2, G-CONTRACT reached 22/106, v2 open.

## Structured scope evidence (P4-SYSTEM.13 b3)

At b3, seven scope pairs run through the registry. Six new predicates add 17
violating copies; with composition's six, 23 specific violations are rejected.
These checks validate declarations and their internal consistency. They do not
execute CSR field semantics, validate external firmware or prove an ISA.

| Obligation | What the scope predicate checks | Negative copies |
| --- | --- | --- |
| OB-EXT-CLOSURE | D requires F, F requires Zicsr; RV64+D C selects its Zcd memory forms | remove F/Zicsr or C.FLD |
| OB-PRIV-REVISION | v20260120 and Machine/Supervisor 1.13 with exact declared page identities | publication, each chapter revision, valid but different hash |
| OB-CSR-SET | exact committed CSR names, unique addresses, seven views and their owners | shorten both lists, change time's owner, duplicate an address |
| OB-NO-PMP | explicit exclusion and no PMP CSR selection | introduce pmpcfg0 or declare inclusion |
| OB-NO-H | extension/mode/CSR selection and explicit exclusion | select H, introduce hstatus, declare inclusion |
| OB-SCOPE-CENSUS | enumeration count/uniqueness and equality with resolved encoding names | wrong total, same-count wrong name |

Privilege artifacts were rehashed when the expected identities were recorded;
normal scope checks bind the declarations to those identities without requiring
the untracked artifact cache. Artifact-byte verification is the citation check's
separate role. The scope-name check reuses the extraction owner's resolution.
At b3, G-CONTRACT reached 34/106; v2 remains open.

## Remaining scope evidence (P4-SYSTEM.13 b5)

Four more pairs realize the remaining selection records. Their predicates validate
the declarations below and require 16 independently changed copies to fail for
specific reasons. Eleven scope pairs now realize 22 checks; with the twenty guest
checks, G-CONTRACT is 42/106. Version 2 remains open.

| Obligation | Selection validated | Negative copies |
| --- | --- | --- |
| OB-ABI | LP64D, ELFCLASS64/double float ABI, ABI_FLEN=64, pinned clang/lld target, D/F and 32×64 FP state, psABI 1.0 source identity | soft-float ABI, wrong toolchain pin, absent D, narrow FP file, different source hash |
| OB-SBI | SBI 2.0 route through real M-mode firmware into S mode, explicit refusal of silent host substitution, source identity | older SBI, host substitution, no M mode, different source hash |
| OB-RVWMO | RVWMO 2.0 selected with A at one hart; multicore work retains its own route | substituted model, extra hart, absent A, wrong chapter revision |
| OB-PRIV-INSNS | exact MRET/SRET/WFI/SFENCE.VMA scope and their resolved encodings | same-count wrong form, missing encoding, altered decision |

The psABI/SBI artifacts were rehashed when recording the expected identities;
ordinary checks compare declarations without requiring the artifact cache or
installed toolchain. These are selection checks: they do not execute a compiled
LP64D program, supply firmware, boot Linux, or explore every RVWMO outcome.
Instruction behavior retains its separate execution evidence. All 34 prior
registry entries, including every guest binding, remain byte-identical.

## Current guarantees replace frozen stages (P4-SYSTEM.13 c1)

Version 2 adds three current guarantees and explicitly supersedes four v0 records.
Every old record line and frozen version membership remains byte-identical. The
historical profile decisions and requirement mirrors retain their text, with notes
pointing to the effective replacements. Current profile comments describe the
implemented F/D support and complete generated-definition route.

| Frozen record | Effective v2 replacement | Evidence |
| --- | --- | --- |
| OB-FP-DEFER | OB-GC-FP-QUALIFIED-V2 | exact manifest/artifact pins, model selection, active qualification/closing records and shared numeric ancestry; five violating copies |
| OB-RESOLUTION-ROUTE, OB-ROUTE-FLIP | OB-GC-DEFINITION-V2 | complete generated route/scope and all three owner generators' read-only drift checks; four violating copies |
| OB-FAULT-PRIORITY | OB-GC-FAULT-PRIORITY-V2 | priority guests, FS-Off cases, EBREAK and C.EBREAK observations |

Address triggers are absent because Sdtrig is absent. Environment-break
exceptions remain: EBREAK and C.EBREAK deliver cause 3, with the instruction's
start in xepc and xtval. The same cause code does not mean the same priority-table
row. Ordinary data alignment is checked before translation; atomics retain their
selected access-fault causes at that point. Executable fixtures cover the named
cases, without claiming every possible fault combination.

Qualification scope binds rustc_apfloat's exact artifact behind the model layer
and the active evidence records. It preserves the independence limit: Sail and
Spike share their numeric implementation. Numeric and instruction guarantees keep
their own vector/guest evidence. The generated-route check delegates to existing
state/definition/guest generators, adding no second generation implementation.

At c1 the effective census was 52 obligations, 104 checks and 48 realized checks.
The address-unit pair below brings it to 53 obligations, 106 checks and 50 realized:
thirteen scope pairs, eleven guest pairs and one direct boundary pair. Four boundary
assumptions and remaining execution checks still keep v2 open.

## Physical byte addresses (P4-SYSTEM.13 c3)

`OB-GC-ENV-ADDRESS-UNITS` requires full unsigned 64-bit physical addresses in
8-bit bytes for parcels, data and page-table reads. Sv39 instruction/data VAs
are translated by the CPU before the request; Bare addresses pass unchanged.
The environment substitutes neither host pointers nor word indices nor VAs.

`contract_boundary_rv64gc.rs` checks distinct byte offsets and stores above 32
bits, then executes a hand-scripted Sv39 LB: guest VA 0x00400000 maps to physical
0x100004000, with physical PTE reads and exactly two requested instruction parcels.
Three deliberately distorted providers (data word index, truncated walk address,
virtual fetch address) must return exact typed ResponseMismatch violations through
ModelError, with PC/destination/trap state unchanged. A legitimate walk access
failure instead delivers cause 1 with the guest VA in mepc/mtval. Both entries run
in the normal registry suite; all earlier entries and frozen bytes remain exact.
This is finite boundary evidence, not proof over every address or provider.


## Shared success-response validation (P4-SYSTEM.13 c4a)

All CPU requests pass through env::request_checked before their answers are
consumed. Wrong kinds and Load values wider than the requested B/H/W width are
typed contract violations; D permits the full u64 range. Valid values, legitimate
target failures and existing violations pass unchanged. This repairs the observed
wrong-family and silently accepted over-wide responses without adding contract
credit. Four core controls include the exact real-engine reproduction. The c4b section
below supplies the explicit data-width/physical-attribute assumption and pair.

## Data widths and physical memory attributes (P4-SYSTEM.13 c4b)

OB-GC-ENV-DATA-ACCESS supplies exact B/H/W/D raw values and whole-request
responses from executable little-endian main memory, without MMIO. Stores write
only the low requested bytes; failed stores write none. The CPU's selected
alignment-before-translation rule remains OB-GC-FAULT-PRIORITY-V2.

The direct pair uses literal bytes, values and instruction words for all four
widths. Direct high-input-bit stores independently test the provider's low-byte
behavior; actual CPU stores also test their narrowed requests. Eight region-edge
load/store failures deliver causes 5/7, preserve the destination and all memory,
and retain the original instruction/address in mepc/mtval. Twelve negative
cases cover eight wrong-kind answers, three over-wide raw loads and one
reversed-byte answer. They remain typed violations without trap/destination effects.

ResponseValueMismatch is emitted by a fixture-only content auditor with an
independent byte witness; ordinary CPU validation checks kinds/widths and cannot
infer memory contents. A valid-content control passes, while disabling the auditor
makes the reversed-byte negative fixture fail. This is finite provider evidence.
All 50 prior registry entries and frozen parts/memberships remain byte-exact.
At c4b the effective census reached 54 obligations / 108 checks, 52 realized:
thirteen scope pairs, eleven guest pairs and two typed boundary pairs.

## Event positioning (P4-SYSTEM.13 c5)

OB-GC-ENV-EVENT-DELIVERY separates delivery location from source permission.
The hart evaluates pending interrupts and WFI wake at the step head before fetch;
virtual time advances once per completed/trapping/waiting boundary. This still
supplies no external IRQs, reservation invalidations or host-time input.

Adapters can call env::check_event_delivery before applying an event. A declared
BetweenInstructions location passes; DuringRequest(request) returns the typed
EventDuringRequest violation. This opt-in guard does not detect arbitrary hidden
host mutation, and introduces no event queue or payload into the CPU runner.
The direct positive pair observes an ADDI reaching the timer threshold followed
by an unfetched-PC interrupt, then WFI and two idle steps followed by timer wake.
Literal cycle/retirement/parcel counts distinguish those boundaries.
Five deliberately in-request attempts reach exact typed errors through the real
GC engine, including its legacy word-table seam. PC, mode, destination, trap
state, counters and memory stay unchanged. Disabling the guard loses every
negative case. All 52 earlier registry entries and frozen bytes remain exact.
Current census: 55 effective obligations / 110 checks, 54 realized; thirteen scope
pairs, eleven guest pairs and three typed boundary pairs. Ordering/reset remain;
v2 is open.
