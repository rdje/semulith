# `rv64i-lab-env-v0` — the environment contract for `rv64i-lab-v0`

- **Contract id:** `rv64i-lab-env-v0`  · **version:** `0` · **profile:** `rv64i-lab-v0`
- **Records:** [`contract-obligations.jsonl`](contract-obligations.jsonl) — 33 obligations
  (25 CPU guarantees, 8 environment assumptions), gated by `RECORD-SCHEMA`.

`docs/CPU_ENVIRONMENT.md` §1: *a CPU is validated under explicit environment assumptions, and the
laboratory must demonstrate that it satisfies them.* This file is those assumptions for the first
profile. It is a **conditional composition claim** — not a claim that the CPU is correct under
every possible environment response.

## The one rule that outranks the others

**Laboratory policy cannot override an architectural requirement.** Every obligation carries an
`authority` from the contract's four-value vocabulary, which is *not* the profile's three-value
one. The mapping is stated once, here, and applied mechanically:

| `profile.toml` authority | contract authority | meaning |
| --- | --- | --- |
| `architecture` | `architecture` | the ISA states it; nobody has latitude |
| `execution-environment` | `implementation-profile` | the ISA delegates it to the EEI; **we** chose |
| `laboratory` | `laboratory` | neither — a policy this harness adopts |
| — | `platform` | *unused*: this profile declares no devices |

⛔ The rule is **enforced**, not trusted: `RECORD-SCHEMA` refuses an obligation whose requirement
is architecturally `defined` but which claims any authority other than `architecture`. Mislabelling
an ISA rule as a harness choice is precisely how a defect becomes an unfalsifiable *"profile
difference"*, and that is the failure this profile's dossier warns about in its own header.

## Units and event boundaries, stated explicitly

`docs/CPU_ENVIRONMENT.md` §3 requires these five to be represented rather than assumed. Each is an
obligation record with machine-readable `parameters`:

| Obligation | What it pins |
| --- | --- |
| `OB-ENV-ADDRESS-UNITS` | 8-bit bytes; 64-bit addresses; arithmetic wraps modulo 2^64 |
| `OB-ENV-ACCESS-WIDTHS` | loads/stores of 8, 16, 32, 64 bits; fetch of 32 — any other width is a **contract violation**, not a service |
| `OB-ENV-VIRTUAL-TIME` | **no time source at all** — see below |
| `OB-ENV-EVENT-DELIVERY` | synchronous exceptions and requested traps only; **no asynchronous interrupt is deliverable** |
| `OB-ENV-ORDERING` | one hart, sequential, in-order; **no memory-ordering claim is made** |

### The two that are "none", and why that is a finding rather than an omission

**There is no virtual time.** This profile excludes `Zicntr`, `Zihpm` and every CSR, so no clock,
cycle counter or instruction counter is architecturally readable. The harness does count retired
instructions — that is how the smoke test bounds a run — but that counter is **not target-visible**
and may never be used to justify guest-observable behaviour. Recording "none" with its reason is
the point: a later profile that adds `Zicntr` reopens this obligation rather than inheriting it.

**There is no asynchronous event.** Not merely "none are configured": there is no interrupt
controller, no privileged mode and no CSR with which to enable, mask or report one, so the
contract has **no legal delivery point** to specify. `docs/CPU_ENVIRONMENT.md` §2's Interrupts row
is therefore out of scope by construction, not by choice.

## The boundary inventory, dispositioned

`docs/CPU_ENVIRONMENT.md` §2 lists ten boundary items. All ten are dispositioned here; an
undispositioned row is how a boundary silently leaves coverage.

| Boundary item | Disposition | Why |
| --- | --- | --- |
| Fetch | **in scope** — `OB-ENV-FETCH-SUPPLY` | 32-bit fetch from a declared executable region; no extraneous or side-effecting fetch |
| Data access | **in scope** — `OB-ENV-ACCESS-WIDTHS`, `OB-MISALIGN-DATA` | widths honoured; misaligned access raises `AlignmentException` and is exercised by `smoke-trap` |
| Translation/protection | **out of scope** | no privileged modes, no CSRs, no MMU/MPU; `profile.toml` declares `privilege_modes = []` |
| Interrupts | **out of scope** | no controller, no mode, no CSR — no legal delivery point exists to specify |
| Counter input | **out of scope** — see `OB-ENV-VIRTUAL-TIME` | `Zicntr`/`Zihpm` excluded; nothing architecturally readable |
| Reservations | **out of scope** | the `A` extension is absent; `state.json`'s census records the reservation set as one of seven hidden-state candidates, all absent |
| Reset | **in scope** — `OB-ENV-RESET` | cold reset only; entry state declared; no retained state to order |
| Waiting | **out of scope** | no `WFI` without privileged modes, and no timer or interrupt could wake one |
| Code visibility | **in scope** — `OB-CODE-VISIBILITY` | the model re-reads memory per fetch; ⚠️ **a legal implementation choice, not an architectural guarantee** — without `Zifencei` a caching reference is equally correct and will legitimately disagree |
| Partial progress | **in scope** — `OB-ENV-PARTIAL-PROGRESS` | every instruction in RV64I base completes or faults as a unit; no restartable suboperation exists |

Six of ten are out of scope, and each says *why* rather than simply being absent. That ratio is the
honest shape of a first profile: it is small on purpose, and the excluded rows are the ones a
Linux-capable profile (`P4-SYSTEM`) will have to reopen one at a time.

## Positive and negative fixtures

`docs/CPU_ENVIRONMENT.md` §4 asks for negative fixtures *"that must be reported as contract
violations rather than target exceptions"*. Every one of the 33 obligations therefore declares
both a `-POS` and a `-NEG` required check, and `RECORD-SCHEMA` refuses an obligation that declares
only positive ones — a contract with positive checks alone describes the cases that already work.

⚠️ **Stated plainly: the checks are declared, not implemented.** The 66 check ids name fixtures
that `P1-LAB` builds; nothing executes them today. What exists now is the obligation that they
must exist, which is what `EVD-03` means by declaring the required evidence *before* the
implementation that would be tempted to choose evidence it can easily produce.

## What is deliberately not here

No device, no board, no interrupt source, no timer, no translation. `docs/CPU_ENVIRONMENT.md` §5's
board composition gate — *for every CPU assumption, identify the board guarantee satisfying it* —
has nothing to match against yet, and that is `P5-BOARD`'s work. The eight assumptions above are
what a board will have to satisfy.
