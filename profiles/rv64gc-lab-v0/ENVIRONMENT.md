# `rv64gc-lab-env` — the environment contract for `rv64gc-lab-v0`

Contract ids: `rv64gc-lab-env-v0`, `rv64gc-lab-env-v1` (extends v0), and
`rv64gc-lab-env-v2` (open, extends v1).
The records live one per line in [`contract-obligations.sexp`](contract-obligations.sexp)
and its explicitly included [v0](contract-v0.obligations.sexp) and
[v1](contract-v1.obligations.sexp) parts; which
records make up which version is [`contract.sexp`](contract.sexp) (schema `schema/contract.sexp`),
judged by **CONTRACT-FREEZE** (`scripts/check_contract_freeze.sh`): every record belongs to
exactly one version, and a frozen version's records are pinned by sha256 — a statement that turns
out wrong is **superseded by a later version, never rewritten**.

`scripts/record_catalog.py` expands repository-root-relative includes in order.
The c2 split reconstructed the original 63,014 bytes exactly, preserving its 58
records and frozen hashes. Subsequent additions live in the root. Schema validation judges every source part before
cross-record checks. This containment change adds no contract credit. See
`docs/decisions/decision_obligation-catalog-parts.md` for the include contract.

OB-LOAD-X0 uses direct request and trap-state witnesses for all seven load forms;
the legacy GC register/fetch comparison alone cannot distinguish a skipped x0
load. OB-ENDIAN binds cross-width byte-lane observations that discriminate even
paired read/write reversal, while byte accesses remain invariant. Worked cases
and mutation controls: `docs/book/src/plan/p4/contract-memory.md`.

NO-DELAY-SLOTS binds skipped-write and fall-through observations for all eight
base branch/jump forms, with mixed-length C integration. Worked controls:
`docs/book/src/plan/p4/contract-control.md`.

JALR-LSB binds literal target/link/request witnesses, including signed-immediate
addition, bit-1 retention, RV64 wrap, aliases and next-boundary target faults.
The old register/fetch corpus comparison alone admits bit-1 erasure; direct PC
observation rejects it. Worked matrix: `docs/book/src/plan/p4/contract-control.md`.

XLEN binds direct full-width GPR/data/PC observations in U mode at two canonical
Sv39 addresses with high bits set. Seven 32-bit truncation controls fail in both
programs. Worked mappings and limits: `docs/book/src/plan/p4/contract-integer.md`.

WALK-IMPLICIT binds literal one/two/three-level CPU request paths, same-page
hits and fault termination with unchanged PTEs. Worked paths and controls:
`docs/book/src/plan/p4/contract-runtime.md#implicit-sv39-reads-have-their-own-request-kind`.

FENCE binds all fm/pred/succ configurations across modes with representative
ignored register fields, plus reservation/cache preservation. Reserved fence
fields execute normally. Worked matrix: `docs/book/src/plan/p4/contract-memory.md`.

ATOMIC-MISALIGN binds both widths, every atomic form and ordering bits, with
full trap/request/state and prior-reservation observations. LR uses cause5;
SC/AMO cause7 before data translation. Aligned LR/SC controls and worked limits:
`docs/book/src/plan/p4/contract-memory.md`.

GC-FENCEI binds all4096 funct12 values/five register pairs/M/S/U, preserving
full state and exact requests. Halfword patches of 16-/32-bit targets at0/2 mod4
remain visible with standard/nonzero FENCE.I and under the coherent no-fence
control. Worked programs and controls: `docs/book/src/plan/p4/fence-i.md`.

GC-ATOMICS binds literal nine-operation W/D values, LR/SC success/failure,
ordering encodings, representative source/destination aliases and exact
state/request effects. Three-level translated AMOs and page/physical failures
retain their store/AMO fault kinds. Worked values, paths and finite limits:
`docs/book/src/plan/p4/atomics.md#direct-contract-observations`.

Explicit instruction writes to mcycle/minstret replace their own implicit
boundary update, including unchanged writes (RVI-ZICSR5.1.1/RVP-MACHINE2.1.1.10).
The other counter follows its ordinary rule; refused writes retire nothing and
advance cycle/time. Writing mcycle re-bases the domain, so determinism is from
initial state and instruction/boundary history. Worked values/reference limits:
`docs/book/src/plan/p4/contract-runtime.md#writable-counters-explicit-writes-replace-their-own-increment`.

The selected FP dirtiness policy marks Dirty on every legal f-register or
explicit fflags/frm/fcsr write, including unchanged values. Flag accrual marks
Dirty when stored flag bits change. RVP-MACHINE 2.1.1.6.7 permits the unchanged-
write choice; public identical-write and read-only observations are documented
in `docs/book/src/plan/p4/floating-point.md#public-fp-state-observations`.

The matched Sail override sets scalar misaligned-atomicity granule exponent0.
A 16-byte granule permits contained AMOs despite AccessFault, so that former
setting did not match the unconditional laboratory alignment rule. Public
qualification: `scripts/probe_gc_sail_atomic_align.py`; worked evidence/limits:
`docs/book/src/plan/p4/contract-memory.md`.

The public Sail runner requests exactly each declared boundary budget and still
requires every ordinary row or witnessed delivery gap. Its historical word-less
fetch spelling is supported without rewriting expectations. Worked observations,
negative controls and platform limits: `docs/book/src/plan/p4/c.md`.

## The versions

| Version | Status | Members | What it is |
| --- | --- | --- | --- |
| v0 | frozen | 46 | everything `P4-SYSTEM.1`–`.8` declared — every one a CPU guarantee, the 13 rv64i base mirrors among them |
| v1 | frozen at `.9`'s close | 6 (+ v0's, minus 2 superseded) | the four environment assumptions below, and two corrections |
| v2 | open; `.13` owns completion/freeze | canonical membership in `contract.sexp`; inherits v1 | M, C, parcel supply, qualified FP, current route, fault priority, physical byte addresses, data access, event positioning, ordering, full cold reset and STCE-selected interrupt sources |

## The boundary inventory, dispositioned (`docs/CPU_ENVIRONMENT.md` §2)

| Boundary item | Disposition | Where |
| --- | --- | --- |
| Translation | **in scope** | `OB-GC-ENV-TRANSLATION-INPUTS` (v1); `OB-SV39`, `OB-SVADE`, `OB-WALK-IMPLICIT` (v0) |
| Interrupts | **in scope — no external source** | `OB-GC-ENV-INTERRUPT-SOURCES-V2` (v2): no CLINT/PLIC; STCE=0 selects software STIP, STCE=1 the hart's comparator; raw software pending is retained behind that view |
| Counter input | **in scope** | `OB-GC-ENV-VIRTUAL-TIME` (v1): the time supply is the virtual-time domain |
| Reservations | **in scope — no external event** | `OB-GC-ENV-RESERVATION-EVENTS` (v1); `OB-RESERVATION`, `OB-SC-DETERMINISTIC` (v0) |
| Waiting | **in scope** | `OB-GC-PRIV-INSNS-V1` (v1): a legal wfi enters the wait; the wake needs no retirement |
| Partial progress | **in scope** | `OB-GC-PARTIAL-PROGRESS` (v0, `.8`): every instruction completes or faults as a unit |
| Fetch | **in scope — 16-bit parcels** | `OB-GC-ENV-FETCH-SUPPLY` (v2): exact requested executable bytes or a declared access failure; no extraneous fetch or side effect |
| Address units | **in scope — physical 8-bit bytes** | `OB-GC-ENV-ADDRESS-UNITS` (v2): full unsigned 64-bit addresses; translated instruction/data accesses and physical PTE reads; direct typed pair |
| Data widths/attributes | **in scope — B/H/W/D, little-endian main memory** | `OB-GC-ENV-DATA-ACCESS` (v2): whole responses, low-width stores, executable bytes, no MMIO; direct typed pair |
| Event delivery | **in scope — between steps** | `OB-GC-ENV-EVENT-DELIVERY` (v2): pending/wake before fetch; typed guard rejects in-request attempts; no external source added |
| Ordering | **in scope — synchronous one-hart realization** | `OB-GC-ENV-ORDERING` (v2): latest preceding stores, consecutive AMO suboperations, coherent parcels; direct typed pair, no exhaustive weak-outcome claim |
| Reset | **in scope — full cold state** | `OB-GC-ENV-RESET` (v2): complete owner/view and image witnesses before fetch; no warm reset |

## The four frozen v1 assumptions — historical statements

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
fixtures. Across the full registry, [GS-REPORT.md](GS-REPORT.md) derives the
effective realization census from the canonical catalog and registered checks.
Remaining unbound checks keep G-CONTRACT incomplete. Frozen v0/v1 text and
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
`crates/semulith-verify/src/contract_checks_rv64gc.rs` binds exact check/obligation
pairs to guest, static-scope, typed-boundary or direct-execution evidence. Tests
run every selected leg; guests retain the corpus comparison rule, and Execution
entries also run their direct observers and named companions. Scope entries run
`python3 scripts/check_gc_contract_scope.py --check CHECK-ID` over parsed canonical
declarations and violating in-memory copies. The tests refuse a missing check among
the pairs bound so far; G-CONTRACT continues to count all remaining missing pairs. A positive fixture exercises the assumption holding; a negative one exercises what would
falsify it (a refused walk read, a software write that must not take, a counter that must not
move, an SC that must fail for the hart's own reasons).

The table below retains frozen-v1 and partial-progress fixture bindings. The
effective registry and GS report include subsequent additions and superseding
pairs, including v2's direct interrupt-source check.

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

## Current evidence and history

The canonical membership is `profiles/rv64gc-lab-v0/contract.sexp`; the executable
registry is `crates/semulith-verify/src/contract_checks_rv64gc.rs`.
[GS-REPORT.md](GS-REPORT.md) derives effective coverage from those inputs.
The [runtime](docs/book/src/plan/p4/contract-runtime.md) and
[integer](docs/book/src/plan/p4/contract-integer.md) and
[control transfer](docs/book/src/plan/p4/contract-control.md) and
[memory](docs/book/src/plan/p4/contract-memory.md) chapters retain examples,
controls and finite comparison limits.

Earlier progress sections are preserved byte-verbatim in
[profile history](docs/tasks/archive/P4-SYSTEM-8.md#profile-progress), with their
source context and hashes. Historical self-descriptions do not override the
current contract, report or executable registry.

Before CSR-access binding, c31a repairs unsupported satp.MODE writes: after
permission checks, the entire write is ignored, including ASID/PPN. The supported
set remains Bare/Sv39; valid field writes and the existing TLB policy remain.
Core and independent-author controls plus finite public M-mode read-back support
the repair. The Sv39 book section gives the example and limits; no binding credit.

C33a adds the D numeric prerequisite:25forms/123264boundaries/246528parcels,
including both format conversions. The shared private fixture preserves all
F observations. Independent author agrees; shared specfp adds no lineage.
D transfers/signs/boxing/refusals and bindings remain; registry110/effective
108/114 unchanged. The FP book gives literal narrowing/widening examples.

GC-F binds203832positive/12852refusal-fault boundaries across all30forms:
numeric111744, transfer/sign/boxing/directed92088, FS-Off1080,
reserved-rounding11628 and ordinary memory faults144. Full state, exact
parcels/W requests and surrounding memory precede expected comparisons.
Payload transfers, improper-box computational qNaNs, same-value Dirty,
sticky flags and selected reservation preservation have literal examples
in the FP book. Twelve new wrong effects and16actual disabled controls
discriminate. Prior108entries/frozen inputs remain exact; now registry110,
effective108/114. Independent author agrees; its shared specfp origin adds
no numeric lineage. D/reservation/SC and final freeze remain open.

GC-CSR-ACCESS binds4480legal/8480refused single boundaries across six forms,
M/S/U, aliases, source-field/value suppression and15selected CSR contexts.
Full state/memory/exact requests are compared; refusal preserves destination
and owners before M trap delivery. Actual disabled permissions/suppression/
observers discriminate. An extra same-CSR read on rd0 swaps is dynamically
indistinguishable for these side-effect-free CSRs; a separate published-table
inspection rejects that branch. The privilege book explains this limit and
worked examples. Independent author12096cases agree;864unknown CSR cases are
named vocabulary refusals, not author trap evidence. Frozen records unchanged.

GC-COUNTERS now binds direct Execution witnesses: 4032 legal and2880 gated
single-boundary reads across M/S/U, all enable masks, three views, three destination
choices and four counter pairs. Full state, memory, requests and retirement are
observed; named wrong effects, corrupted captures and disabled observers/gates
must fail. The runtime chapter gives worked values and finite limits. Existing
counter companions retain their original expectations; no frozen record changes.

The integer chapter also covers load/store extension: scope-mem's pattern and
bound-ext/dir-ext-matrix's signed edges and wider read-backs distinguish correct
load extension and low-bit stores from seventeen isolated wrong alternatives.
All earlier inputs and frozen declarations remain exact; GS derives the updated
realization count. Source review uses the authenticated local snapshot; the
fetched-page identity refusal is enforced by P4-SYSTEM.13 c18c: locator and quote
readers verify exact source hashes/lengths before using a page. Restored fetched
copies match the unchanged pins; only absent evidence permits a named skip.
