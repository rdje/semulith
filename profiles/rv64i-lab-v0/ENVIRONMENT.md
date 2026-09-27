# `rv64i-lab-env-v0` — the environment contract for `rv64i-lab-v0`

- **Contract id:** `rv64i-lab-env-v0`  · **version:** `0` · **profile:** `rv64i-lab-v0`
- **Records:** [`contract-obligations.sexp`](contract-obligations.sexp) — 34 obligations
  (26 CPU guarantees, 8 environment assumptions), gated by `RECORD-SCHEMA` behind the schema layer
  (`SOT-FORMAT.3`).

`docs/CPU_ENVIRONMENT.md` §1: *a CPU is validated under explicit environment assumptions, and the
laboratory must demonstrate that it satisfies them.* This file is those assumptions for the first
profile. It is a **conditional composition claim** — not a claim that the CPU is correct under
every possible environment response.

## The one rule that outranks the others

**Laboratory policy cannot override an architectural requirement.** Every obligation carries an
`authority` from the contract's four-value vocabulary, which is *not* the profile's three-value
one. The mapping is stated once, here, and applied mechanically:

| `profile.sexp` authority | contract authority | meaning |
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
| `OB-ENV-VIRTUAL-TIME` | **no time source at all**: no CSR-readable counter **and** no device — see below |
| `OB-ENV-EVENT-DELIVERY` | synchronous exceptions and requested traps only; **no asynchronous interrupt is deliverable** |
| `OB-ENV-ORDERING` | one hart, sequential, in-order; **no memory-ordering claim is made** |

### The two that are "none", and why that is a finding rather than an omission

**There is no virtual time — and the reason has two halves, because one is not enough.** This
profile excludes `Zicntr`, `Zihpm` and every CSR, so no counter is architecturally readable. That
was once the whole argument, and it was **wrong**: a core-local interruptor exposes `mtime` as
ordinary MMIO, which a plain load reaches with no CSR instruction at all. Measured on the
then-matched reference, a guest read `0x0200_BFF8` and got an advancing value (2, then 3). The
second half is therefore the load-bearing one — the laboratory platform declares **no device**, so
there is no memory-mapped time register either. Excluding instructions does not exclude
capabilities; excluding devices does.

**There is no asynchronous event**, because the laboratory platform declares no interrupt
controller and no machine software, timer or external source. ⛔ The earlier wording justified this
by "no privileged mode and no CSR", and both halves were false: a RISC-V hart is **always** in at
least machine mode — every reference trace line in this repository reads `[M]` — and its trap
state exists whether or not `Zicsr` is present, since `Zicsr` supplies the *instructions* that
reach CSRs, not the CSRs. An absence has to be a **platform** property to be real.

## The boundary inventory, dispositioned

`docs/CPU_ENVIRONMENT.md` §2 lists ten boundary items. All ten are dispositioned here; an
undispositioned row is how a boundary silently leaves coverage.

| Boundary item | Disposition | Why |
| --- | --- | --- |
| Fetch | **in scope** — `OB-ENV-FETCH-SUPPLY` | 32-bit fetch from a declared executable region; no extraneous or side-effecting fetch |
| Data access | **in scope** — `OB-ENV-ACCESS-WIDTHS`, `OB-MISALIGN-DATA` | widths honoured; misaligned access raises `AlignmentException` and is exercised by `smoke-trap` |
| Translation/protection | **out of scope** | no MMU/MPU and no supervisor/user mode; `profile.sexp` declares `(privilege_modes "M")` — machine mode only, which is the minimum a hart can have |
| Interrupts | **out of scope** | the laboratory platform declares **no controller and no source**. ⚠️ Not "no mode, no CSR": those were the wrong reasons, and `P0-PROFILE.10` corrected them |
| Counter input | **out of scope** — see `OB-ENV-VIRTUAL-TIME` | `Zicntr`/`Zihpm` excluded **and** no device exposes a counter as MMIO. Both halves are required |
| Reservations | **out of scope** | the `A` extension is absent; `state.sexp`'s census records the reservation set as one of seven hidden-state candidates, all absent |
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

## A matched profile is matched on its platform too

⛔ **This contract once described an environment the reference did not provide.** The matched-profile
override configured the *instruction set* — `--print-isa-string` read `rv64i_zvl32b`, which is
correct and answers a narrower question than "is this matched". Underneath it the reference kept a
device-bearing default platform: a core-local interruptor, an interrupt generator, and two I/O
regions. `P0-PROFILE.10` configured the platform, corrected every claim that had rested on the
unconfigured one, and left behind a negative fixture (`guests/guest-no-device.s`) that fails the
run if a device becomes reachable again.

⚠️ **And the repair does not reach every reference — because the difference is a LAYER one.**
Spike ships a CPU *and a small board*: an interruptor, a platform interrupt controller and a UART,
not separable from its command line. A processor model owns none of those. So what
`DIFF-PLATFORM-SPIKE` measures is **how much board each reference drags in**, and the consequence
is stated exactly: any guest touching `0x1000` or `0x0200_0000..0x11ff_ffff` behaves differently on
the two references. The three original guests touch neither — a **stated precondition**, not luck.

⛔ **This is the boundary that keeps a processor model a processor model.** A UART, an interrupt
controller or an interconnect belongs to a board / SoC / ASIC model — `P5-BOARD` — and this
contract's job at that line is to state what the CPU **assumes**, so a board can later be checked
against it (`docs/CPU_ENVIRONMENT.md` §5). Every device named anywhere in this profile appears in
exactly one role: something a reference brings that we exclude. None is modelled here, and none
should be.
