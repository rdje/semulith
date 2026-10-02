# DOSSIER — `rv64gc-lab-v0` (development — the resolution stage)

The P4 profile, resolved: the **Linux-capable** processor this project validates next,
selected and recorded by `P4-SYSTEM.1` (design brief `2026-10-02`, executed
`2026-10-03` — [`docs/tasks/P4-SYSTEM.md`](../docs/tasks/P4-SYSTEM.md), Decisions).
Nothing here is inferred from the letters "GC": every element below carries its source
locator, and the dependency closure is measured against the pinned publication.

> **Claim scope.** This unit is a **profile resolution**: the selection is exact and
> citable, and the definition pipeline (encoding fragments, semantics, guests) has not
> started — the dossier declares the `profile-resolution` vehicle route
> (`D-RESOLUTION-ROUTE`) and the definition-pipeline gates refuse any
> definition-pipeline document beside the declaration. No model code exists for this
> unit, and nothing here is an execution result. F and D are in the profile, but the
> model implements no floating point until the backend passes qualification
> (`P4-SYSTEM.7`); the `CPU-SYSTEM` gate verdict will read `incomplete` until then.

## The selection, at a glance

| Element | Selection | Locator |
| --- | --- | --- |
| Base ISA | RV64I (version 2.1), XLEN 64, little-endian | `RVI-RV64I` §3.1 |
| Extensions | M 2.0, A 2.1, F 2.2, D 2.2, C 2.0, Zicntr 2.0, Zicsr 2.0, Zifencei 2.0; privileged: Sstc 1.0 | the chapters' own stated versions ([`sources.sexp`](sources.sexp)) |
| ISA string | `rv64imafdc_zicntr_zicsr_zifencei_sstc` (canonical order) | `RVI-NAMING` 36.1 |
| Privileged architecture | Machine-Level ISA 1.13 + Supervisor-Level ISA 1.13, under spec revision `v20260120` | `RVP-MACHINE` 2.1, `RVP-SUPERVISOR` 11.1 |
| Privilege modes | M, S, U (M-mode firmware, S-mode kernel, U-mode userspace); H excluded | `RVP-INTRO`; `D-PRIV-MODES`, `D-NO-H` |
| Translation | Sv39 (of Sv39/Sv48/Sv57 at SXLEN=64) | `RVP-SUPERVISOR` §11.1.3–§11.1.4; `D-SV39` |
| Alignment | IALIGN 16 with C; ILEN 32 | `RVI-C` 27.1; `D-IALIGN-16` |
| Counters | Zicntr `cycle`/`time`/`instret`; Zihpm not selected | `RVI-ZICNTR` 6.1; `D-ZICNTR` |
| S-mode timer | Sstc (`stimecmp`, `menvcfg.STCE`) | `RVP-SSTC` 12.1; `D-SSTC` |
| Memory model | RVWMO 2.0 (load-bearing already at one hart: the A extension's AMOs) | `RVI-RVWMO` 17.1; `D-RVWMO` |
| Privileged instructions | `mret`, `sret`, `wfi`, `sfence.vma` | `RVP-INSNS` 18.1; `D-PRIV-INSNS` |
| CSRs | the committed minimum of 33 (named in `profile.sexp`'s state block) | `D-CSR-SET` |
| PMP / hypervisor | both excluded at v0 (PMP is architecturally optional; no virtualization workload) | `RVP-MACHINE` §2.1.7; `D-NO-PMP`, `D-NO-H` |
| Toolchain ABI | LP64D (the standard RV64G ABI — requires D); clang/lld 21.1.8, `rv64gc` target | `RVI-PSABI` §2.4–§2.5; `D-ABI` |
| Firmware contract | SBI 2.0 — real M-mode firmware for the P6 route, never a silently substituted host-modelled SBI | `RVI-SBI`; `ROADMAP.md` §P6; `D-SBI` |
| Harts | 1 — multicore is `MC-MULTICORE`'s | `ROADMAP.md` §P4 |

## The dependency closure (measured, not inferred)

The acceptance is SCP-02's: the closure is resolved, every implication cited from the
pinned chapter that states it.

- **G = IMAFD + Zicsr + Zifencei** — `RVI-NAMING` 36.1: "an abbreviation 'G' to represent
  the 'IMAFDZicsr_Zifencei' base and extensions".
- **D depends on F** — `RVI-D` 21.1: "The D extension depends on the base
  single-precision instruction subset F."
- **F depends on Zicsr** — `RVI-F` 20.1: "The F extension depends on the 'Zicsr'
  extension for control and status register access" (the FP CSRs `fflags`/`frm`/`fcsr`).
- **C decomposes as Zca + Zcd** at RV64 with D — `RVI-ZC` 28.1.2: "C always implies Zca;
  C+F implies Zcf (RV32 only); C+D implies Zcd". With IALIGN=16, no
  instruction-address-misaligned exception arises from C's 16-bit forms (`RVI-C` 27.1).
- **Zicntr and Sstc are NOT in G** — both are named explicitly, with their own chapters
  (`RVI-ZICNTR` 6.1, `RVP-SSTC` 12.1): the supervisor-mode `time` read and the
  supervisor-programmable timer are what a Linux kernel actually uses; G alone does not
  supply them.

## Decisions with their own weight

- **FP is declared, not yet modelled** (`D-FP-DEFER`): the standard RV64G userspace ABI
  is LP64D (`RVI-PSABI` §2.4–§2.5: the hardware floating-point calling convention with
  ABI_FLEN=64), which requires D — so F and D are in the profile from day one, and the
  *model* implements none of it until `P4-SYSTEM.7` qualifies an FP backend. The
  alternative (resolve rv64imac now, add FD later) was weighed and rejected: it would
  fork the profile identity at the `.7` landing, and the honest-verdict machinery
  already carries declared-but-unevidenced scope as `incomplete`, never as a pass. And
  a Sail-versus-Spike FP comparison is **one implementation twice** (the SoftFloat
  shared ancestry, 184/199 files byte-identical) — `.7`'s fixtures must derive expected
  values from outside that lineage.
- **Sv39's precedent and its warning** (`D-SV39`): the pinned SoC manual's U54 implements
  Bare + Sv39 — and **raises page faults rather than setting PTE A/D bits**
  (`SIFIVE-FU540-C000` §4.7). The privileged architecture permits both behaviours; which
  one this model implements is `P4-SYSTEM.3`'s evidence-backed choice, recorded here as
  input, not decided by citation.
- **The privileged chapters were always in the pin.** The category census (2026-09-27)
  recorded the privileged volume as "absent from this unprivileged snapshot"; measured
  `2026-10-02`, the pinned snapshot carries `priv/` (24 pages) and `unpriv/` (46 pages),
  every cited row re-hashed against the tracked `SHA256SUMS`. The census rows'
  corrections land with this unit's category-needs dispositions at registration day.

## What this unit does NOT have yet

No `encoding.sexp`, no `state.sexp` census, no `guests/`, no `interactions.sexp`, no
reference dossier, no expectations — the definition pipeline starts at `P4-SYSTEM.2`.
No registration in `materials/units.sexp`, no book under `docs/models/` — registration
day is a later leaf (the `.2`/`.11` precedent: one coherent registration day with its
generator consequences). The environment contract (`rv64gc-lab-env-v0`) is **v0**: the
resolution's obligations only; `P4-SYSTEM.9` extends it to v1 (versioned, never edited
in place).

## Open questions

- **OQ-1 — license/terms recording.** SRC-01 requires the actual applicable terms
  recorded before relying on or shipping an artifact; the pinned artifacts are READ,
  not redistributed, and "shipping" is not reached. Owned here, due at the first
  release candidate of this profile (the rv64i-lab-v0 OQ-4 precedent).
- **OQ-2 — the A/D-update policy is open by design.** The pinned SoC precedent (U54)
  raises page faults instead of setting PTE A/D bits; the privileged architecture
  permits both. `P4-SYSTEM.3` decides this profile's policy against the selected
  extensions and revision — with evidence, not by citation of one implementation.
