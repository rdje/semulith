# `rv64i-lab-v0` — profile dossier

The first experiment's development profile. **Development, not accepted**: no evidence is
attached to anything here, no gate has been run, and `SCP-01` requires a support claim to
identify a versioned profile, an environment contract, an observation contract *and* the
applicable specification revisions — this dossier is the first of those four.

Machine-readable form: [`profile.toml`](profile.toml). Pinned sources:
[`sources.toml`](sources.toml). Both are gated — `PROFILE-CONSISTENCY` re-derives the declared
counts from the enumeration and refuses a decision that carries no authority or no source.

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
| **OQ-4** | What are the actual applicable terms for the specification artifacts, and does anything here get redistributed? Nothing is committed today; `SRC-01` requires the terms before it is. | `P0-PROFILE.5` | before any artifact is shipped |
| **OQ-5** | Is `pc` after an `ECALL`/`EBREAK` requested trap defined by this harness, or left to the harness contract? The base ISA gives no answer without a privileged mode. | `P0-PROFILE.4` | `G0` |

## What is deliberately absent

No `state.json` (leaf `.2`), no `requirements.jsonl` (leaf `.3`), no environment contract
(leaf `.4`), no reference dossier (leaf `.5`), and no evidence of any kind. The `G0` gate is
`incomplete` and will read `incomplete` until `P0-PROFILE.9`.
