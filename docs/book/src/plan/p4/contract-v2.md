# P4.13 — Completing the environment contract

**Status:** State inventory, scope pairs, three corrections and four typed boundary pairs landed; v2 remains open.

The complete instruction set now runs, including multiply/divide and compressed
instructions. Its contract still contains declarations inherited from earlier
stages. This work checks every effective obligation, fills the remaining boundary
assumptions, and realizes each declared check before freezing version 2.

The original census found 53 effective obligations and 106 checks. Three versioned
corrections replace four old records; four new boundary assumptions bring the
effective census to 56 obligations and 112 checks, with 56 checks running through
the unit's registry. A check will receive credit only when its actual
fixture runs: instruction guarantees use executable observations; a scope choice
such as the selected firmware ABI uses a predicate over the canonical documents
and a negative fixture that violates that predicate. Running an unrelated program
cannot establish a scope declaration.

Cold reset is the remaining boundary topic.
The scalar profile's assumptions cannot be
copied unchanged. For example, this processor can take interrupts, fetches exact
16-bit parcels, selects RVWMO, and resets floating-point, translation-cache,
reservation and wait state as well as integer registers and CSRs. Time, parcel
fetch and partial progress already have GC-specific records.

Version 2 now replaces the inherited definition stages and the earlier
floating-point qualification condition. It also corrects fault-priority language:
address triggers are absent, while EBREAK and C.EBREAK still raise environment-break
exceptions with cause 3. The pinned priority table distinguishes these cases.

Versioning preserves the record. Frozen version-0 and version-1 statements and
their hashes stay unchanged; version 2 names each replacement and why it replaces
the old statement. The complete per-obligation plan is in the active task tree's
`.13` census. Completion requires every effective check to run, the state census
to describe the actual complete state, and version 2 to be frozen. Until then,
G-CONTRACT and CPU-SYSTEM remain incomplete.

## Complete state inventory

The state census now describes the whole selected laboratory profile. Its twelve
candidates are answered, and its consequence names every state owner:

| State | What must be retained for exact continuation |
| --- | --- |
| Integer registers and control | x1–x31, PC and current privilege mode; x0 is constant |
| Floating point | f0–f31, each 64 bits |
| CSRs | 26 storage owners behind 33 named CSRs |
| Memory | The laboratory's main-memory bytes |
| Translation cache | Four TLB entries and the FIFO replacement position |
| Reservation | Physical address, width and validity |
| Waiting | ACTIVE or WAITING |

CSR aliases add no storage. For example, `time` and `cycle` view `mcycle`, and
`fcsr` combines `fflags` and `frm`. The virtual clock is already part of those
owners; this laboratory has no external timer or interrupt-controller state.
Cold reset constructs all owners anew. Exact continuation must also preserve
the current TLB replacement position, reservation and wait state: cold reset is
not a substitute for restoring them.

This correction changes the declared inventory and its generated metadata.
The definition module also records the updated state-source hash in its
provenance manifest. Storage, reset values, accessors and execution remain
byte-identical. Snapshot
and replay serialization still belong to P4.16; this inventory does not claim
that those features are implemented.

## Executable scope checks

The registry now distinguishes guest evidence from scope evidence. Its normal
Rust tests run every entry. The first scope pair checks the composition selection:
RV64I with 64-bit registers, the exact selected extension set, its nine encoding
fragments, and a complete composition.

The negative check first requires the real declarations to pass, then changes six
independent copies: remove C, add H, change XLEN, leave C unbound, change the base
fragment, or mark the composition partial. Each copy must fail for its specific
reason. Further controls deliberately disable each predicate family; the negative
check must then fail. Unknown check ids are refused. All copies stay in memory.

This adds two real checks without running an unrelated program as evidence of
selection. All twenty earlier guest bindings stay unchanged. The effective
contract reached 22 of 106 checks at that slice. The following structured
scope checks raise it to 34; version 2 remains open.

## Structured scope and identity

Six more scope pairs validate the extension dependencies, privilege-source
revision, CSR inventory, PMP and hypervisor exclusions, and equality between the
profile's instruction names and the resolved encoding. Their 17 violating copies
must each fail for a specific reason. Two examples show why a count or an agreement
between files is insufficient:

- Removing `fcsr` from both the profile and state lists leaves them agreeing, but
  violates the independently stated committed CSR selection.
- Replacing one C instruction name with an unknown name leaves the count intact,
  but violates equality with the composed encoding.

The privilege check also binds the declared version to exact source identities.
A different well-formed digest fails. The two public pages were rehashed when
these expectations were recorded; the ordinary scope check needs no artifact
cache and makes no fresh artifact-byte verification claim.

At b3, seven scope pairs plus the twenty existing guest checks realized 34 of
106 checks. These are selection and consistency checks. CSR field behavior and
instruction semantics retain their execution evidence; firmware is still future
work. Older notes and changelog entries were archived verbatim with exact
reconstruction, so their history remains available within the fixed size limits.

## Enforcing the guest toolchain

Before realizing the ABI scope, review found that the legacy C build printed
its tool versions without enforcing them. An isolated reproduction accepted
version-99 compiler and linker stand-ins. ACT4's duplicated discovery also crashed
when an explicit compiler was missing. Both callers now use the same resolver.

The resolver validates clang/LLD 21.1.8, Zig 0.16.0 when used as the linker driver,
and ACT4's LLVM 21.1.8 symbol reader. It checks these identities before writing a
backend probe. An explicit override that is missing, has the wrong version, or
cannot compile RV64I is refused; no fallback bypasses that override. For example:

```bash
bash scripts/build_c_guest.sh c-scope
SEMULITH_RISCV_CLANG=tools/clang bash scripts/build_c_guest.sh c-scope
```

The second command succeeds only when `tools/clang` exists and satisfies the
same pin and backend requirements. Probe files remain under the repository's
output directory and are cleaned on either outcome. Twenty isolated controls
cover both callers and refusal paths; disabling identity checking makes the
controls fail. The installed pinned tools still build the exact same C ELF.
That guest uses RV64I/LP64; the selected GC LP64D ABI still needs its own scope
checks, and firmware implementation remains later work.

## ABI, firmware, ordering and privileged scope

Four further pairs bring the effective contract to 42 of 106 realized checks.
They check selections, with a positive predicate and specific violating copies:

| Selection | What must hold | Example violation |
| --- | --- | --- |
| ABI | LP64D, 64-bit integer and FP state, D/F, declared compiler/target and exact psABI 1.0 identity | narrow the FP file while retaining LP64D |
| Firmware route | SBI 2.0 through real M-mode firmware into S mode, with no silent host substitution | replace the real-firmware requirement with host SBI |
| Memory model | RVWMO 2.0 with A at one hart; multicore retains its separate route | change the selected hart count to two |
| Privileged forms | MRET, SRET, WFI and SFENCE.VMA in the scope and resolved encoding | retain four names but replace one with HRET |

Sixteen violating copies must fail for their own reasons. The ABI and SBI source
artifacts were rehashed when the expected identities were recorded; ordinary
checks bind their declarations without requiring those cached files. All prior
registry entries remain byte-identical.

Scope evidence does not establish execution of an LP64D program, implemented
firmware, Linux boot or exploration of every weak-memory outcome. Those claims
retain their own work and evidence. Eleven scope pairs now run in the normal test
suite alongside the existing twenty guest checks. Remaining instruction and
boundary checks and the five assumptions still keep contract v2 open.

## Three current guarantees, four historical records

The effective contract now replaces the obsolete statements without rewriting
history. Frozen v0/v1 records and pins are unchanged. Profile decisions and their
requirement mirrors keep their historical statements, with notes identifying the
effective replacements; current profile comments describe the implemented state.

| Current v2 guarantee | What it replaces | What its checks run |
| --- | --- | --- |
| Qualified FP selection | pre-qualification FP condition | exact manifest/lock pins, model selection, active qualification records and numeric-independence limit; five violating copies |
| Complete generated definition | resolution stage and partial-composition checkpoint | complete route/scope plus the existing state, definition and guest generators in read-only check mode; four violating copies |
| Corrected fault priority | blanket absence of breakpoint exceptions | priority/FS-Off guests and both EBREAK spellings, with their actual trap observations |

For example, C.EBREAK delivers cause 3 with its own address in xepc and xtval.
Absent address-trigger support does not remove that exception. The pinned table
places address triggers and environment break in different rows, despite their
shared cause code. Data alignment retains the laboratory's choice before
translation, including the selected LR and SC/AMO access-fault codes.

The qualification check confirms the selected artifact and active evidence
records; numeric behavior retains its independent vectors and guest observations.
The generated-definition check calls the existing generators, so it verifies
fresh mirrors without implementing another generation rule.

Those six checks brought the effective census to 48 of 104 checks at c1. The
address-unit pair below brings it to 50 of 106. Version 2 stays open.

## Keeping the catalog bounded without rewriting history

The catalog reached 63,014 bytes against its fixed 65,536-byte authored-part cap.
It now retains the six current v2 records and explicitly includes two frozen
parts, in version order:

```lisp
(include-obligations (path "profiles/rv64gc-lab-v0/contract-v0.obligations.sexp"))
(include-obligations (path "profiles/rv64gc-lab-v0/contract-v1.obligations.sexp"))
```

Paths start at the repository root, so moving the checkout keeps them valid.
The v0 and v1 parts contain their original contiguous record bytes. At c2, expansion
reproduced all 63,014 pre-split bytes exactly, including order and blank lines;
all 58 record mappings and frozen pins were unchanged. At that split the root was
9,003 bytes, the v0 part 47,168 and the v1 part 7,009. No size ceiling was raised and no duplicate
materialized catalog is maintained.

`scripts/record_catalog.py` is the one expansion owner. The record loader, freeze
checker, conversion tools and Rust registry declaration test all use it. Only real
top-level forms expand: a directive inside a quoted statement or a comment remains
literal text. Missing parts, cycles, repeated parts, noncanonical paths and symlink
escapes refuse with named errors. The schema checks every original source, retaining
the part name in a refusal; existing duplicate-ID and reference checks then judge
the expanded records. Reserved `(comment "annotation")` forms survive in the source
but do not become records.

For a read-only view of the whole catalog, run:

```sh
python3 scripts/record_catalog.py profiles/rv64gc-lab-v0/contract-obligations.sexp --stdout
python3 scripts/probe_record_catalog.py
```

The probe has 31 controls, including relocation and malformed includes. Disabling
expansion makes it fail. RECORD-SCHEMA also plants invalid included fields and
duplicate IDs across distinct parts. Partitioning adds no contract-check credit.

## Physical byte addresses: a typed boundary pair

`OB-GC-ENV-ADDRESS-UNITS` states that requests carry unsigned 64-bit physical
addresses in 8-bit bytes. The CPU translates instruction and data VAs before
crossing the boundary; page-table reads already name physical addresses. Bare
translation preserves the address. A host pointer, word index or narrowed integer
cannot substitute for that declared address.

The positive check first addresses distinct bytes in a main-memory region above
32 bits, including a byte store that preserves its neighbors. It then runs the
real interpreter on a hand-encoded `LB x6, 0(x5)` under Sv39. The independent script
expects exactly these crossings:

| Request | Physical address | Supplied value |
| --- | --- | --- |
| Root PTE read | `0x1_0000_1000` | pointer to the next table |
| Level-1 PTE read | `0x1_0000_2010` | pointer to the last table |
| Leaf PTE read | `0x1_0000_3000` | executable/readable leaf at `0x1_0000_4000` |
| First instruction parcel | `0x1_0000_4000` | `0x8303` |
| Second instruction parcel | `0x1_0000_4002` | `0x0002` |
| Byte load | `0x1_0000_400b` | `0xee` |

The guest VA is `0x0040_0000`; x5 contains VA+11. The instruction produces
`x6 = 0xffff_ffff_ffff_ffee` and advances PC by four. All scripted requests are
consumed, so a missing or extra walk/fetch cannot silently pass.

Three negative providers distort one boundary address: divide the data address
by four, truncate the root-walk address to 32 bits, or use the guest VA for a
physical fetch. Each reaches the exact `ContractViolation::ResponseMismatch`
through `ModelError`, leaving PC, destination and trap CSRs untouched. A separate
legal access-failure response still delivers instruction access-fault cause 1,
with the guest VA in mepc/mtval. This distinguishes a broken provider from a
target exception.

The registry now has explicit `Evidence::Boundary` entries. Its normal tests run
both fixtures and retain the rule that every post-v0 declaration is born realized.
Frozen records and all earlier registry entries are unchanged. Four boundary
assumptions and the remaining execution pairs still need work; these finite
fixtures do not prove correctness for every possible address or environment.

## Checking success responses before consuming them

While preparing the data-access assumption, the public boundary probe found two
defects. A provider answering `FetchParcel` with `StoreDone` reached
`InvalidDescription`. A provider supplying `Load(0x1ff)` for an 8-bit load was
accepted, and the LB wrote all ones into its destination. Both responses break
the environment contract; neither should become usable instruction data.

`semulith_core::env::request_checked` now validates every CPU crossing in one
place: scalar word fetch/load/store, GC parcel fetch/load/store, LR/SC/AMO accesses
and implicit page-table reads. Providers still implement `Environment::request`.
CPU consumers call the checked entry point, which forwards exactly one unmodified
request and validates the answer before the interpreter consumes it.

| Request | Only valid success kind |
| --- | --- |
| `Fetch` | `Fetch(u32)` |
| `FetchParcel` | `FetchParcel(u16)` |
| `Load` | `Load(u64)` with no nonzero bits above the requested B/H/W/D width |
| `Store` | `StoreDone` |
| `WalkAccess` | `WalkAccess(u64)` |

A wrong kind returns `ContractViolation::WrongResponseKind`, retaining the
request and response. An over-wide load returns `LoadValueOutOfWidth`, retaining
the requested width and original value. The validator does not truncate the bad
answer into an apparently valid one. All 64 bits remain legal for a D-width load.
Sign or zero extension into XLEN still belongs to the instruction.

For example, `Load(0xff)` is a valid raw byte answer; `Load(0x100)` is a violation.
`Load(u64::MAX)` is valid for D and invalid for B/H/W. The original two probe cases
now reach `ModelError::ContractViolation`, with destination and trap state
untouched. The legitimate access-fault control still delivers load cause 5.

Four permanent core tests exercise all 25 request/response-kind combinations,
narrow-width edges, full-width values, unchanged target failures and existing
violations, and actual GC/scalar/translation paths. Normal guest observations
still pass. At c4a this repair added no contract-check credit: the census stayed
50 of 106 realized, with four boundary assumptions still to declare and realize.

## Data widths and physical memory attributes

`OB-GC-ENV-DATA-ACCESS` now supplies the data-width and memory-attribute assumption
with its own positive and negative registry fixtures. The physical map is
executable little-endian main memory without MMIO. Reads have no memory side
effects; a store writes its low requested bytes and preserves every other byte.
Each request completes as a whole or fails as a whole. The selected CPU alignment
check still precedes translation under the separate fault-priority guarantee.

The fixture begins with these independent bytes at address 0x1020:

```text
address:  1020 1021 1022 1023 1024 1025 1026 1027
byte:       88   77   66   55   44   33   22   11
```

| Width | Exact raw load | Bytes written by a store of 0xfedcba9876543210 |
| --- | --- | --- |
| B, 8 bits | 0x88 | 10 |
| H, 16 bits | 0x7788 | 10 32 |
| W, 32 bits | 0x55667788 | 10 32 54 76 |
| D, 64 bits | 0x1122334455667788 | 10 32 54 76 98 ba dc fe |

Hand-encoded LBU/LHU/LWU/LD and SB/SH/SW/SD consume those values through the real
engine. Direct store requests retain high source bits, independently checking
the provider's low-byte rule; CPU narrow stores already narrow their operands.
A parcel read observes the same bytes, and repeated reads preserve memory.

Eight region-edge cases refuse a load or store of every width. For B the address
is the first byte outside the region; H/W/D straddle its end. Causes 5/7 retain
the instruction in mepc and data address in mtval. The destination and entire
memory image stay unchanged, including the valid prefix of a refused store.

The negative pair runs twelve bad providers: wrong kinds for each of four loads
and stores, a first out-of-range raw B/H/W bit, and a reversed-byte D value.
Malformed shapes reach the shared validator. The reversed value fits 64 bits,
so a fixture-only auditor compares it with the independent byte witness and
returns `ResponseValueMismatch { request, expected, arrived }`. These failures
reach the typed model-error channel without a target trap or destination write.
A correct-content control passes; disabling the auditor makes the reversed-byte
negative fixture fail because the CPU executes the wrong value.

The CPU can validate response shape but cannot infer a provider's memory contents.
The content auditor establishes this finite fixture's behavior. It is not a
universal content check in ordinary execution. All prior entries and frozen
records remain exact. At c4b the census reached 54 effective obligations, 108 declared
checks and 52 realized checks; event delivery, ordering and reset remained open.

## Event delivery between steps

`OB-GC-ENV-EVENT-DELIVERY` states where input changes belong. The hart evaluates
eligible pending interrupts and WFI wake at the head of a step, before requesting
any instruction parcel. One virtual tick follows each completed, trapping or idle
step. A timer threshold reached by that tick is considered at the next head.
No memory callback splits an instruction by delivering an event.

Location permission and source permission are separate. The current laboratory
still supplies no external interrupt controller, reservation invalidation or
host-time input. An adapter can validate a proposed location before applying an
otherwise authorized input:

```rust
check_event_delivery(EventDeliveryPoint::BetweenInstructions) // Ok(())
check_event_delivery(EventDeliveryPoint::DuringRequest(request))
// Err(ContractViolation::EventDuringRequest { request })
```

The guard checks the location the adapter declares. It cannot discover arbitrary
hidden host mutation. There is no new event payload, queue or guest observation,
and normal instruction execution uses its existing pending/timekeeping owners.

The positive fixture arranges two ADDIs with the timer threshold at one tick:

| Step | Result | mcycle | minstret | Parcel requests so far |
| --- | --- | --- | --- | --- |
| 1 | x6 becomes 1; PC reaches 0x1004 and the timer becomes pending | 1 | 1 | 2 |
| 2 | Interrupt cause bit 63 plus code 5; mepc=0x1004, PC=0x1100; second ADDI unfetched | 2 | 1 | 2 |

A second arrangement executes WFI with threshold 3. WFI retires once, then two
idle steps move mcycle through 2 and 3 without fetch or retirement. The fourth
step wakes and delivers, with mepc at WFI's successor, mcycle=4 and minstret=1.
The only two parcel requests are WFI's original fetch.

The negative pair attempts delivery while answering each of Fetch, FetchParcel,
Load, Store and WalkAccess. Every real-engine path returns the exact typed
location violation, preserving PC, mode, destination, trap state, counters and
memory. Fetch uses the public legacy table seam over the same GC evaluator.
Disabling the location guard lets every bad schedule escape and makes each
negative fixture fail. At c5 these finite checks brought the effective census to
55 obligations, 110 declared checks and 54 realized checks.

## One-hart request order and coherent code

`OB-GC-ENV-ORDERING` declares the laboratory's sequential realization of RVWMO.
Requests complete synchronously in issued order. A load observes the latest
preceding store to each of its bytes; no host buffer, concurrent writer or delayed
completion intervenes. With one hart, consecutive AMO suboperations have no other
agent between them. This chooses a legal realization, while exploration of all
weaker outcomes and multicore retain their separate work.

The pinned RVWMO chapter defines global order, preserved program order and the
load-value, atomicity and progress constraints. Selecting the one-hart program
order and latest preceding stores meets those constraints here. The pinned
FENCE.I chapter separately orders preceding stores before later instruction
fetches. The laboratory's coherent reads provide immediate visibility even
without that synchronization, a stronger choice than the architectural minimum.
Both source artifacts were digest-verified when this pair was authored.

The positive fixture specifies a literal request/response conversation:

| Instruction | Required observation at data address 0x1040 |
| --- | --- |
| SW x6,0(x5) | Complete store of 0x11223344 |
| LWU x7,0(x5) | Read 0x11223344 |
| SB x8,1(x5) | Write 0xaa to byte 0x1041 only |
| LWU x9,0(x5) | Read overlapping result 0x1122aa44 |
| AMOADD.W x10,x11,(x5) | Read old 0x1122aa44, store 0x1122aa45, return old value |

All four aq/rl combinations run the same five-step conversation, with ten parcel
requests. An independent script owns request-order checks; the shared fixture
value auditor checks supplied values. It does not replace the ordinary CPU's
shape validator or infer arbitrary storage contents.

Two code-rewrite fixtures first execute ADDI x12,x0,1 to warm its address. They
rewind to a writer, patch that instruction to ADDI x12,x0,7, then reach it by normal
fallthrough, once directly and once through FENCE.I. Both finish with x12=7.
The warm step counts: three total retirements without the fence, four with it.

The negative provider either acknowledges a store without retaining it or serves
old instruction parcels after the patch. All three cases return exact typed
`ResponseValueMismatch` errors before a wrong destination write; no target trap
is delivered. Disabling value auditing loses each negative fixture. The
discarded-store control stops at its first bad load so a later AMO request check
cannot mask the value-auditor bypass.

All earlier registry entries and frozen records remain exact. The effective
census is 56 obligations, 112 declared checks and 56 realized checks. Full cold
reset and remaining instruction checks keep version 2 open.
