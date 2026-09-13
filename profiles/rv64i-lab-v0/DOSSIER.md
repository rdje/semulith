# `rv64i-lab-v0` — profile dossier

The first experiment's development profile. **Development, not accepted**: no evidence is
attached to anything here, no gate has been run, and `SCP-01` requires a support claim to
identify a versioned profile, an environment contract, an observation contract *and* the
applicable specification revisions — this dossier is the first of those four.

Machine-readable form: [`profile.toml`](profile.toml) and [`state.json`](state.json). Pinned
sources: [`sources.toml`](sources.toml). All are gated — `PROFILE-CONSISTENCY` re-derives the
declared counts from the enumeration, refuses a decision that carries no authority or no
source, requires `state.json` to agree with `profile.toml`, and refuses an empty `hidden_state`
list that carries no census.

## What this profile is

| | |
| --- | --- |
| Architecture | RISC-V, base **RV64I**, chapter version 2.1 |
| Specification revision | `v20260120` |
| XLEN / ILEN / IALIGN | 64 / 32 / 32 |
| Extensions | **none** — no C, M, A, F, D, Zicsr, Zifencei |
| Privilege modes | **none modelled** — unprivileged base ISA only |
| Harts | 1 |
| Endianness | little (an execution-environment choice) |
| Instruction scope | 40 base + 12 RV64I additions = **52**, enumerated in `profile.toml` |

Selecting RV64I is **not** a claim that the laboratory constitutes a fully specified privileged
processor. It is the smallest scope in which real scalar machinery can be validated at 64 bits
without a 32-bit detour.

## The three authorities, and why the distinction is load-bearing

Every decision in `profile.toml` carries one:

- **`architecture`** — the specification states it. We have no choice. *(12 decisions)*
- **`execution-environment`** — the specification explicitly delegates it to the EEI, and this
  profile chose. *(6 decisions)*
- **`laboratory`** — neither: a policy this harness adopts over a case the architecture leaves
  `UNSPECIFIED`, or a boundary the harness itself imposes. *(2 decisions)*

⛔ A `laboratory` decision can never override an `architecture` one. And where a laboratory
policy resolves an `UNSPECIFIED` case, the model must still be able to report that the case
*was* unspecified — because a reference model that chose differently is not wrong, and a
differential test that flags it has found a profile difference, not a defect (`SEM-07`).

The specification is explicit about what `UNSPECIFIED` means: *"a behavior or value that is
intentionally unconstrained… open to extensions, platform standards, or implementations"*
(`RVI-INTRO`, *UNSPECIFIED Behaviors and Values*). That is a different thing from a gap in our
research, and `docs/INFORMATION_CATALOG.md` §6 keeps the two apart deliberately.

## The decisions worth reading before writing any code

**Two reporting points that deliberately disagree.** An `instruction-address-misaligned`
exception on a taken branch or jump is reported **on the branch or jump**, not on the target
(`RVI-RV32I` §1.1.5.2). An instruction **access-fault** on the target of that same jump is
reported **on the target**, not on the jump (`RVI-RV32I` §1.1.5). A model that gets one of
these backwards is right about the fault and wrong about where it happened — and a final-state
checksum will never notice.

**A not-taken branch raises nothing.** No `instruction-address-misaligned` exception is
generated for a conditional branch that is not taken, even when its target is misaligned
(`RVI-RV32I` §1.1.5.2). This is a suppressed-effect case in the sense of `SEM-06`.

**`SLLIW`/`SRLIW`/`SRAIW` with `imm[5] != 0` are RESERVED, not illegal.** The specification
records that they *previously* raised an illegal-instruction exception and that marking them
reserved is a backwards-compatible change (`RVI-RV64I` §3.1.2.1). Under this profile's
`D-RESERVED-DECODE` policy they raise illegal-instruction anyway — but the model must record
*why*: a laboratory choice over an `UNSPECIFIED` case, not an architectural requirement. A
reference built against the older text agrees for the wrong reason, and one built against a
platform that permits reserved encodings disagrees for a legitimate one. See OQ-2.

**A load into `x0` still faults.** *"Loads with a destination of x0 must still raise any
exceptions and cause any other side effects even though the load value is discarded"*
(`RVI-RV32I` §1.1.6). The obvious optimisation — skip a load whose result is discarded — is
architecturally wrong.

**HINTs must not trap.** Every code point in the RV64I HINT table (`RVI-RV64I` §3.1.4, Table 1)
executes as a no-op. `SLLI x0, x0, 0x1f` and `SRAI x0, x0, 7` are *standard* HINTs in this
revision — the semihosting entry and exit markers — having previously been custom HINTs.

**`ECALL` and `EBREAK` are requested traps, not model failures.** They cause a *precise
requested trap to the supporting execution environment* (`RVI-RV32I` §1.1.8; `RVI-INTRO`,
*Requested Trap*). With no privileged mode in this profile there is no guest handler, so both
are reported to the harness as a typed environment-trap outcome. This is precisely why
`TargetEvent` and `ModelError` must be different types: *"the guest asked the environment for
something"* is not *"the model cannot do this"* (`SEM-01`, `SEM-02`).

**The address space is circular.** *"memory address computations done by the hardware ignore
overflow and instead wrap around modulo 2^XLEN"* (`RVI-INTRO`, *Memory*). Host pointer
arithmetic does not behave this way, which is precisely the class `SEM-05` exists for: host
pointers do not supply guest semantics.

**Code visibility is a laboratory choice, and a reference that disagrees is not wrong.** Without
the Zifencei extension — absent from this profile — the base ISA permits a hart to cache
fetchable bytes and never re-read main memory (`RVI-INTRO`, *Memory*). This model re-reads on
every fetch, which is legal, but a guest may not rely on it and a caching reference model is
equally legal. The comparator must report such a divergence as a **profile difference**, not a
defect. This is catalog `C13`, and it is the kind of case a final-state checksum never surfaces.

**No ordering claim.** `FENCE` is decoded and must not trap; with one hart, no external devices
and an in-order model it has no observable effect. `FENCE.TSO` (fm=1000, pred=RW, succ=RW) is
accepted and implemented as `FENCE RW,RW`, which the specification states is correct
(`RVI-RV32I` §1.1.7, Table 3). RVWMO is **out of scope** until `MC-MULTICORE`, and this profile
claims nothing about memory ordering.

## Open questions

Each has an owner and a due point. None blocks writing `profile.toml`; all block the `G0` gate.

| ID | Question | Owner | Due |
| --- | --- | --- | --- |
| **OQ-1** | Does archogen's `rt-static-up-v1` need machine-mode features this profile excludes? `docs/ARCHOGEN_INTEGRATION.md` §6 warns against promising that unprivileged RV64I alone suffices. | `AG-OS` / this leaf on re-open | before `P1-LAB.1` fixes the crate boundary |
| **OQ-2** | Which reference models treat `SLLIW` `imm[5]!=0` as reserved versus illegal, and how is the difference reported rather than counted as a mismatch? | `P0-PROFILE.5`/`.6` | `G0` |
| **OQ-3** | Is `D-MISALIGN-DATA`'s contained-trap choice expressible in the selected reference's configuration, or must it be normalized at the comparator? A normalization needs a source-grounded justification (`EVD-05`). | `P0-PROFILE.6` | `G0` |
| **OQ-4** | What are the actual applicable terms for the specification artifacts, and does anything here get redistributed? Nothing is committed today; `SRC-01` requires the terms before it is. **Partly answered by `.5`:** the *reference models'* terms are now recorded (BSD-2-Clause, BSD-3-Clause, GPL-2.0-only, Apache-2.0) and none is redistributed. The *specification* artifacts' terms remain open. | `P0-PROFILE.5` (models, done) / `.9` (specification) | before any artifact is shipped |
| **OQ-5** | Is `pc` after an `ECALL`/`EBREAK` requested trap defined by this harness, or left to the harness contract? The base ISA gives no answer without a privileged mode. | `P0-PROFILE.4` | `G0` |

## The state inventory, and why "no hidden state" is a checked claim

[`state.json`](state.json) records 32 integer registers of 64 bits (`x0` hardwired to zero) and
`pc`, and then does the part that matters: it **enumerates seven candidates for hidden state and
shows each absent** — CSRs, the reservation set, floating-point registers and `fcsr`, vector
state, privilege and trap state, instruction-fetch cache state, and pending or partially
committed effects. An empty list with no census is an unearned claim, and the gate refuses one.

Two entries in that census are worth reading. *Instruction-fetch cache state* is absent only
because of `D-CODE-VISIBILITY`: a caching implementation would have hidden state there and would
still be architecturally legal. And *pending effects* are absent because no instruction in RV64I
base is a multi-step or restartable suboperation — which is exactly what makes this a good first
experiment, since snapshot and replay reduce to the register file, `pc` and memory. **Every
extension added later reopens this census.**

Register **ABI names are software convention, not architecture.** Only the three roles the ISA
chapter itself names — `x1` return address, `x5` alternate link, `x2` stack pointer — are
recorded, with authority `software-convention`. The rest belong to the calling-convention
document, which has not been fetched, so they are absent rather than assumed
(`docs/INFORMATION_CATALOG.md` §6, *Instruction semantics versus ABI*).

Reset values for `x1..x31` are a **laboratory** declaration, and that was measured rather than
assumed: the string `reset` appears **0 times** in the RV32I chapter and **0 times** in the
RV64I chapter. The unprivileged specification says the EEI defines the initial state of the
program (`RVI-INTRO`), and this harness's choice of zero is not something a guest may rely on
elsewhere.

## The reference models, and what having three of them does not mean

[`references.toml`](references.toml) is the candidate dossier. Three models were obtained and
run on this host, and one test corpus was located but deliberately not acquired:

| Candidate | Status | Matched to this profile by | Reports itself as |
| --- | --- | --- | --- |
| **Sail RISC-V 0.14** | obtained (prebuilt `Mac-arm64` binary) | [`reference/sail-rv64i-lab-v0.override.json`](reference/sail-rv64i-lab-v0.override.json) | `rv64i_zvl32b` |
| **Spike 1.1.1-dev** | obtained (source build, commit `1e05ddac`) | `--isa=rv64i --priv=m` | `rv64i` |
| **QEMU 11.1.1** | obtained (pre-existing host toolchain, read-only) | `-cpu rv64i` | *(no ISA string emitted)* |
| **ACT (`act4`)** | reachable, not acquired | — | — |

⛔ **Three models is not three opinions.** ACT computes its expected results with a *configured
Sail model*, so agreement between ACT and candidate 1 is one semantics answering twice. Spike
and QEMU are plausibly independent of Sail and of each other — *plausibly*, which is not a
finding. `EVD-04` requires shared ancestry to be **examined per subsystem**, and
`P0-PROFILE.7` owns that. The `lineage` field on every candidate is the input to that leaf, and
the gate refuses a candidate that omits it, because an unasked independence question reads
exactly like an answered one.

⛔ **And none of them is usable yet.** `docs/EVIDENCE_AND_GATES.md` §5 makes a real matched-profile
experiment the condition for calling a reference usable, and that is `P0-PROFILE.6`. What `.5`
establishes is narrower and worth stating exactly: *we have these binaries, this is which ones
they are, and each can be configured to something close to this profile.*

### Two differences that are already known, before any instruction has been run

**The Sail model cannot be configured to exactly `extensions = []`.** Driven down from its
default `rv64imafdcbvh_…` (96 supported extensions) it reaches `rv64i_zvl32b` — the base plus a
vestigial minimum vector-length class that survives because the model always instantiates a
`VLEN` even with the vector unit `Disabled`. No vector instruction decodes, so the difference is
believed benign; it is recorded rather than rounded away, because `G0` asks for differences to
be *enumerated*, not assumed absent.

**The Sail model will not tell us what configuration it actually ran with.**
`--print-default-config` ignores `--config-override`; the two dumps are byte-identical. So the
effective configuration is recorded as *(release 0.14 default) + (the tracked override)*, and
**that merge is ours, not the model's report of itself.** The one self-description the model does
emit is `--print-isa-string`, which is why `rv64i_zvl32b` is pinned and re-derived by
`scripts/fetch_references.sh`. `P0-PROFILE.6` must not treat our merge as the model's own word.

### What the acquisition attempt cost, versus what it was expected to cost

The task-tree budgeted this leaf on building Sail from source through an OCaml/opam toolchain.
That turned out not to be necessary: release 0.14 publishes a native binary for this host's exact
architecture. The attempt that *did* fail is recorded too — the host package manager's `sail`
formula is a WordPress deployment tool for DigitalOcean, an exact name collision with the Sail
ISA language. Recording "Sail is available from the package manager" would have been false in
precisely the way `SRC-03` exists to prevent.

## What is deliberately absent

No `requirements.jsonl` (leaf `.3`), no environment contract
(leaf `.4`), no reference dossier (leaf `.5`), and no evidence of any kind. The `G0` gate is
`incomplete` and will read `incomplete` until `P0-PROFILE.9`.
