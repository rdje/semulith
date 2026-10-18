# DOSSIER — `rv64gc-lab-v0` (development — complete instruction composition)

The P4 profile, resolved: the **Linux-capable** processor this project validates next,
selected and recorded by `P4-SYSTEM.1` (design brief `2026-10-02`, executed
`2026-10-03` — [`docs/tasks/P4-SYSTEM.md`](../../docs/tasks/P4-SYSTEM.md), Decisions).
Nothing here is inferred from the letters "GC": every element below carries its source
locator, and the dependency closure is measured against the pinned publication.

> **Claim scope.** This `generated-definition` unit executes its complete
> instruction composition: RV64I, M/A/F/D/C, Zicsr, Zicntr and Zifencei, with the
> declared privileged machinery. The scope is 200 spellings (197 instructions and
> three counter pseudos); all are exercised by the 167-guest directed corpus.
> F/D use the qualified Rust backend (`P4-SYSTEM.7`); C bound at `.12` slice e2c.
> This is finite laboratory evidence. The generated [CPU-SYSTEM report](GS-REPORT.md)
> owns the current acceptance verdict. Instruction composition and realized
> environment checks do not close evidence, regression, portability or
> release obligations. Resolution-era declarations below retain their history;
> effective membership and supersessions are defined in contract.sexp.

## The selection, at a glance

| Element | Selection | Locator |
| --- | --- | --- |
| Base ISA | RV64I (version 2.1), XLEN 64, little-endian | `RVI-RV64I` §3.1 |
| Extensions | M 2.0, A 2.1, F 2.2, D 2.2, C 2.0, Zicntr 2.0, Zicsr 2.0, Zifencei 2.0; privileged: Sstc 1.0, Svade (defined inline in `RVP-SUPERVISOR` 1.13, no separate chapter) | the chapters' own stated versions ([`sources.sexp`](sources.sexp)) |
| ISA string | `rv64imafdc_zicntr_zicsr_zifencei_sstc_svade` (canonical order; `svade` appended at P4-SYSTEM.3 slice a) | `RVI-NAMING` 36.1; `D-SVADE` |
| Privileged architecture | Machine-Level ISA 1.13 + Supervisor-Level ISA 1.13, under spec revision `v20260120` | `RVP-MACHINE` 2.1, `RVP-SUPERVISOR` 11.1 |
| Privilege modes | M, S, U (M-mode firmware, S-mode kernel, U-mode userspace); H excluded | `RVP-INTRO`; `D-PRIV-MODES`, `D-NO-H` |
| Translation | Sv39 (of Sv39/Sv48/Sv57 at SXLEN=64); Svade for A/D (page fault, never a hardware PTE update; Svadu not selected) | `RVP-SUPERVISOR` §11.1.3–§11.1.4, §11.1.10; `D-SV39`, `D-SVADE` |
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

- **FP qualification preceded implementation** (historical `D-FP-DEFER`): the
  standard RV64G userspace ABI is LP64D (`RVI-PSABI` §2.4–§2.5), requiring D.
  The initial resolution included F/D and deferred their implementation until
  `P4-SYSTEM.7` qualified `rustc_apfloat` with independent exact-rational fixtures.
  F and D now execute through that backend. Resolving rv64imac first was rejected
  because it would fork the profile identity. Comparator implementation ancestry
  has not been authenticated through public evidence. Sail/Spike agreement is
  finite evidence on the declared observations, with no numeric independence
  credit. The original unsupported rationale is retained in the model book's
  historical capture, not used as a current assumption.
- **Sv39's precedent and its warning** (`D-SV39`): the pinned SoC manual's U54 implements
  Bare + Sv39 — and **raises page faults rather than setting PTE A/D bits**
  (`SIFIVE-FU540-C000` §4.7). The privileged architecture permits both behaviours; which
  one this model implements is `P4-SYSTEM.3`'s evidence-backed choice, recorded here as
  input, not decided by citation.
- **The privileged chapters were always in the pin.** The category census (2026-09-27)
  recorded the privileged volume as "absent from this unprivileged snapshot"; measured
  `2026-10-02`, the pinned snapshot carries `priv/` (24 pages) and `unpriv/` (46 pages),
  every cited row re-hashed against the tracked `SHA256SUMS`. The census rows'
  corrections are recorded with this unit's category-needs dispositions at registration day.

## Current implementation and remaining acceptance

The unit owns its encoding/semantic composition, state census, expectations,
interaction matrix and pinned reference dossier. Registration, the complete category
census and the dedicated book are recorded in materials/units.sexp,
materials/category-needs.sexp and docs/models/rv64gc-lab-v0/. The book distinguishes
acquired facts, implementation and evidence acceptance. Historical matched results
remain finite observations; structured experiments and requirement-status derivation
remain .14 work. CPU-SYSTEM acceptance has not been reached.

Contract membership and realization are derived in [GS-REPORT.md](GS-REPORT.md).
The latest v2 is frozen; supersessions preserve earlier frozen text and pins.
The [C chapter](docs/book/src/plan/p4/c.md) records its binding and finite matched
comparison. The full [verification policy](EVIDENCE_POLICY.md) is prospective after
implementation: earlier successful runs are not automatically requalified.

## Open questions

- **OQ-1 — license/terms recording.** SRC-01 requires the actual applicable terms
  recorded before relying on or shipping an artifact. One retained DIV statement
  has a scoped CC-BY4.0 decision in `materials/RVI_M_RETENTION.md`; the full fetched
  artifacts remain unredistributed and other terms open. Owned here, due at the first
  release candidate of this profile (the rv64i-lab-v0 OQ-4 precedent).
- **OQ-2 — CLOSED (`2026-10-03`, P4-SYSTEM.3 slice a, D-SVADE): the profile implements
  Svade.** A translation needing an A or D PTE update raises a page fault instead of
  performing the hardware update. The three evidence legs: (i) the pinned revision
  defines exactly two A/D schemes and names the page-fault one Svade
  (RVP-SUPERVISOR §11.1.3.1, §11.1.10); (ii) the pinned SoC precedent the Sv39 choice
  already cites implements exactly that scheme — "does not automatically set the A and
  D bits … Instead, the U54 MMU will raise a page fault" (FU540 §4.7); (iii) the
  laboratory's observe-through-the-ISA discipline (P4-SYSTEM.2 decision 6) can evidence
  a page fault (scause/stval via csrr) but cannot evidence an implicit PTE write, so the
  hardware-update default would price a new observation vocabulary to test a side
  effect the laboratory need not produce. Svadu is NOT selected: menvcfg's ADUE stays
  WPRI. The Sail matched override's `Svade` flag is `true` (the resolution-era reference flip
  measured no verdict change in that earlier corpus).

## Complete state and current contract

The canonical census accounts for x/PC/mode, the FP file, 26 CSR owners behind
33 names, main memory, four TLB entries plus FIFO position, reservation and
ACTIVE/WAITING state. Time is stored in mcycle; views add no independent storage.
Requirement statuses remain .14's work. P4.16 provides bounded laboratory JSON
snapshot/resume and model-aware replay bundles, including all census owners; reduction stays open.
Two named full-table fault controls exercise the text demo; the complete mutation
campaign remains .15 work.

The effective contract and executable registry are complete at the .13 checkpoint;
[GS-REPORT.md](GS-REPORT.md) derives their current denominator and realization.
Frozen v0/v1/v2 text, membership and pins remain unchanged. Shared catalog/schema/
freeze owners judge the same records. V2 supersedes the earlier FP condition,
definition stages, blanket no-breakpoint wording and v1 STIP comparator assumption.
STCE-clear software pending and direct S-mode programming/refusal witnesses are
bound through direct Execution evidence with their original guest companions.

| Current evidence | Canonical detail |
| --- | --- |
| Physical addresses, data widths/attributes, event positioning, ordering, cold reset | Five direct typed pairs plus the STCE source pair in ENVIRONMENT.md and the contract book |
| Success-response shape validation | Shared CPU boundary validator; target failures remain target exceptions |
| Value/phase/startup auditing | Independent fixture controls; adapters cannot detect hidden host mutation or grant interrupt-source authority |
| Privilege modes, Sv39, Svade, IALIGN-16, Zicntr, immediate/register ALU, U-immediates | Exact guest bindings in ENVIRONMENT.md; worked observations and controls in the runtime book |
| Inherited-global cache repair | G accumulates along the walk; actual ASID/root/fence regressions; independent author unchanged |

The boundary fixtures distinguish provider violations from target exceptions.
Ordering selects a sequential one-hart RVWMO realization, not all weak outcomes.
Reset includes retained cache/reservation/wait owners; cold fcsr is internally
zero but FS-gated, and computed pending state differs from raw mip storage.
All evidence retains its finite scope; no firmware or Linux acceptance is claimed.
STCE-clear software STIP and the SSTC contract witness are repaired. Direct
S programming/read-back and handler-visible refusals reject the forced-S-trap
defect that the unchanged terminal zero-read guest alone still misses.

Review [the contract book](docs/book/src/plan/p4/contract-v2.md) and
[runtime witnesses](docs/book/src/plan/p4/contract-runtime.md) for examples.
Detailed slice history lives in docs/tasks/P4-SYSTEM.md, DEV_NOTES.md and CHANGELOG.md;
this dossier maintains the current state rather than duplicate progress histories.
