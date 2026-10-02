# P4-SYSTEM: validate the processor Linux actually needs

## Metadata

- Tree ID: `P4-SYSTEM`
- Status: `active`
- Roadmap lane: `ROADMAP.md` §6 → **P4 — Validate the processor needed for Linux**
- Gate: `CPU-SYSTEM`
- Depends on: `P2-SCALAR` (gate `CPU-LAB`)
- Unlocks: the CPU release gate, and with it `P5-BOARD` and `MC-MULTICORE`
- Created: `2026-09-13`
- Owner: repo-local workflow

## Goal

Select and validate a Linux-capable profile — provisionally RV64GC with an explicitly chosen
privilege revision, M/S/U modes, Sv39 translation, implemented CSRs, interrupt acceptance,
counter behaviour, and stated firmware/toolchain requirements — as a **processor**, in the
laboratory, before any board exists.

## Non-Goals

- No board, no boot. Booting does not prove the CPU, and a CPU bug found during a later boot
  returns here and invalidates affected evidence (`docs/CPU_ENVIRONMENT.md` §5).
- No floating-point support until its backend passes qualification. There is **no silent
  native-float or FFI fallback** (`docs/ARCHITECTURE.md` §6, `RUST-01`).

## Acceptance Criteria — gate `CPU-SYSTEM`

The complete declared profile passes the processor gate, **including its environment contract**.
This gate authorises the planned next engineering stage: board implementation.

## Task Tree

- ID: `P4-SYSTEM.1` — **resolve the profile**
  Status: `pending`
  Goal: turn "provisionally RV64GC" into an exact selection with a resolved dependency closure — privilege revision, modes, translation scheme, CSR list, interrupt and counter behaviour, firmware and toolchain requirements.
  Acceptance: nothing is inferred from the letters `GC`; each element has a source locator (`SCP-01`, `SCP-02`).

- ID: `P4-SYSTEM.2` — **privilege and mode transitions**
  Status: `pending`
  Goal: M/S/U transitions, control-register permissions, trap interception, context state, mode-dependent decoding (catalog `C15`).
  Acceptance: the same instruction's behaviour is tested **in each supported mode**, not once.

- ID: `P4-SYSTEM.3` — **Sv39 translation and protection**
  Status: `pending`
  Goal: page-table format, walk ordering, permission checks, A/D update policy, ASIDs, translation invalidation, permitted walk side effects (catalog `C12`).
  Acceptance: permission failure produces the correct fault **and** the permitted page-table side effects; A/D policy is validated against the selected extensions and revision, not chosen as a knob.

- ID: `P4-SYSTEM.4` — **atomics and reservations**
  Status: `pending`
  Goal: atomic widths, reservation semantics, failed conditional stores, overlap and external-write cases (catalog `C16`, `docs/CPU_ENVIRONMENT.md` §2).
  Acceptance: single-core reservation behaviour is validated here; multicore memory-model work is `MC-MULTICORE`, not smuggled in.

- ID: `P4-SYSTEM.5` — **interrupts, counters and wait**
  Status: `pending`
  Goal: masks, priority, pending/active state, nesting, return; counter width, rate, wrap and mode gating; a halted core still receiving its wake event (catalog `C14`, `C17`).
  Acceptance: timer or interrupt wake occurs **without CPU retirement** — the laboratory must be able to make time pass while nothing executes.

- ID: `P4-SYSTEM.6` — **instruction visibility and fence semantics**
  Status: `pending`
  Goal: when newly written code must become executable, and when stale state may persist (catalog `C13`).
  Acceptance: rewrite-code fixtures with and without the architectural synchronization.

- ID: `P4-SYSTEM.7` — **floating-point backend qualification** *(task card `T011`)*
  Status: `pending`
  Goal: name a Rust candidate; pin the exact target policy for rounding modes, flags, result bits, conversions, NaN payloads and boxing; inventory ancestry (shared SoftFloat lineage, specialization, thread-local vs global status, exact compiler and features); run independent numeric fixtures.
  Acceptance: a decision record with **measured** correctness and performance evidence. If no candidate passes, implement the required subset in Rust and defer the capability. TestFloat's usual SoftFloat expected-value path is recorded as shared ancestry (`RK07`, `EVD-04`).
  ⛔ **Routed in from `P0-PROFILE.7` on `2026-09-14`, measured rather than anticipated:** the two reference models this project uses *both* vendor Berkeley SoftFloat, and **184 of the 199 `.c` files present in both copies are byte-identical** once the release-number comment is normalized (sail 3e / spike 3d; `f64_add.c` differs by one line). A Sail-versus-Spike floating-point comparison therefore executes **one implementation twice**. This leaf's ancestry inventory starts from that fact, and its independent numeric fixtures must derive expected values from something that does not descend from SoftFloat. See [`reference_softfloat-shared-ancestry`](../decisions/reference_softfloat-shared-ancestry.md).

- ID: `P4-SYSTEM.8` — **faults, restart and partial progress**
  Status: `pending`
  Goal: fault priority, suppressed effects, restart locations, partial commits under the new system features (`SEM-04`, `SEM-06`).
  Acceptance: a fault injected after the Nth suboperation leaves the architecturally required state.

- ID: `P4-SYSTEM.9` — **environment contract v1** — `G-CONTRACT`
  Status: `pending`
  Goal: extend the contract to cover translation inputs, interrupt sources, counter progress and reservation invalidation for this profile.
  Acceptance: every new assumption has a positive and a negative fixture; the contract is versioned, not edited in place.

- ID: `P4-SYSTEM.10` — **the `CPU-SYSTEM` gate report**
  Status: `pending`
  Goal: the full processor gate over the complete declared profile.
  Acceptance: reproducible from pinned inputs; fidelity reported per axis; missing checks read `incomplete`.

## Current Frontier

| Order | Leaf | Status | Why next |
| --- | --- | --- | --- |
| 1 | `P4-SYSTEM.1` | `pending` | every later leaf is scoped by the resolved profile |

## Decisions

- `2026-10-02` (design brief for `.1`, recorded before its execution; sources: the
  materials census — `materials/catalog.sexp`, the pinned snapshot measured on disk this
  day; the explore-agent census of the profile machinery, references dossier, and P4
  history; `ROADMAP.md` §P4/§P6; `docs/CPU_ENVIRONMENT.md` §2; the explore report is
  conversation-only, every load-bearing fact below re-measured by the signing engineer):
  **The measured pre-conditions.** (1) The pinned snapshot **carries the privileged
  chapters**: `.materials/riscv/pinned-v20260120/` holds `priv/` (24 pages —
  `machine.html`, `supervisor.html`, `priv-csrs.html`, `priv-insns.html`, `sstc.html`,
  `smepmp.html`, …) and `unpriv/` (46 pages — `m/a/f/d/c-st-ext.html`, `zicsr.html`,
  `zifencei.html`, `counters.html`, `rvwmo.html`, `naming.html`, `rv-32-64g.html`, …),
  every file digest-pinned by the tracked `SHA256SUMS`. This matches the catalog's
  "46 unprivileged + 24 privileged pages" claim and **contradicts the category census's
  closing notes** (C12/C14/C15 say the privileged volume is "absent from this
  unprivileged snapshot" — measured false today; the census predates the snapshot's
  current content; the rows' corrections land with the unit's category-needs
  dispositions at registration, and this brief is their measured basis). (2) The
  "wanted" support materials are already in the cache: `riscv-sbi-2.0.pdf`,
  `riscv-elf-psabi-1.0.pdf`, `riscv-brs-1.0.pdf` under `.materials/riscv/` —
  digest-verifiable, adoption = citing them. (3) The encoding corpus has exactly one
  extension fragment (`m.sexp`, generated from the pinned riscv-opcodes rv_m/rv64_m);
  rv_a/rv_f/rv_d/rv_c/zicsr… tables are NOT pinned — that re-pin belongs to the evidence
  leaves, not `.1`. (4) References: Sail 0.14 exposes the full extension/privileged
  config namespace (the matched override disables it today); Spike's default platform
  (Sv57, CLINT/PLIC/16550) is not matchable from its command line — the
  DIFF-PLATFORM-SPIKE lesson applies to any P4 matching; the SoftFloat shared ancestry
  (184/199 byte-identical) is already routed to `.7`. (5) The Rust bare-metal minimum is
  `riscv64imac` (`reference_what-running-real-rust-actually-requires`); the toolchain is
  clang/lld 21.1.8 (`decision_c-guest-routing-and-toolchain`).
  **The selection, decided** (the full per-element locator table is the execution's
  business; these are the design decisions it must evidence):
  1. **The unit is `rv64gc-lab-v0`.** Base RV64I + extensions **M, A, F, D, C, Zicsr,
     Zifencei**; privilege modes **M, S, U**; translation **Sv39**; harts 1 (multicore
     is MC-MULTICORE's, never smuggled); xlen 64, endianness little (the field is data
     since `P5-BOARD.6`). With C present, **IALIGN is 16** (ILEN stays 32) — a concrete
     consequence the resolution must state, with its locator. The revision is the
     pinned publication's (`v20260120`) with each chapter's own stated version measured
     from the page — the rv64i-lab-v0 versioning model, extended to the privileged
     chapters.
  2. **The closure is measured, not inferred from "GC".** G = IMAFD + Zicsr + Zifencei
     (`naming.html` / `rv-32-64g.html`); D implies F; F/D imply Zicsr (the FP CSRs);
     C's RV64 decomposition (Zca, and Zcd with D) — every implication cited from the
     pinned chapter that states it (SCP-02).
  3. **FP is IN the profile; its execution evidence is `.7`'s.** Linux's standard
     userspace ABI is lp64d (psABI — measured at execution), which requires D; the
     roadmap's provisional GC stands. The alternative (declare rv64imac now, FD later)
     is rejected: it would fork the profile identity at the .7 landing, and the
     honest-verdict machinery already carries declared-but-unevidenced scope as
     `incomplete`, never as a pass. The model implements no FP before `.7`'s backend
     qualification (the tree's non-goal, unchanged).
  4. **Interrupt/counter acceptance semantics are CPU-contract content** (the privileged
     interrupt model, `counters.html`, `sstc.html`); CLINT/PLIC are board-layer — the
     P4-profile board branch, not this tree (the P5-BOARD archive records the layering).
  5. **Firmware/toolchain requirements:** SBI 2.0 (cached, ratified) as the M-mode
     firmware contract the P6 route will execute (ROADMAP §P6: real firmware, never a
     host-modelled SBI silently); psABI 1.0 (cached) for the toolchain ABI; the
     toolchain stays clang/lld 21.1.8 with the rv64gc target. DT-SPEC/BRS stay `wanted`
     — P6's boot hardware description is not `.1`'s.
  6. **The citation rule extends, unchanged in kind:** the pinned snapshot's `priv/`
     pages are the citation authority for privileged content (same publication identity
     as the unprivileged pages); the PDFs stay reference-only (the numbering trap —
     `docs/knowledge/a-version-string-is-not-an-identity.md`). Each page's stated
     version is measured from the page, not presumed.
  7. **The output shape:** `profiles/rv64gc-lab-v0/` carries `profile.sexp` (the
     selection as data — the schema already supports every field needed, `extensions`
     and `privilege_modes` and the state block's `csrs` included), `sources.sexp` (the
     pinned pages, digests re-derived from the tracked SHA256SUMS), and `DOSSIER.md`
     (the resolution narrative: the per-element locator table, the closure, the
     rejected alternatives). **Unregistered** — registration day and its consequences
     (units.sexp, category-needs dispositions, the book) belong to a later leaf, the
     `.2`/`.11` precedent. Requirements/obligations/expectations catalogues arrive with
     the evidence leaves (`.2`+); `.1` ends with the selection complete and citable.
  **Not `.1`'s scope:** the extension encoding fragments and their riscv-opcodes re-pin;
  reference rv64gc matching (Sail config exists; Spike's platform problem is recorded);
  OpenSBI adoption; the P4-profile board branch; the CSR list's *semantics* (`.2`+);
  registration; the gate.

- `2026-09-13`: the default RISC-V Linux route runs compatible **M-mode firmware providing
  selected SBI services** before an S-mode kernel. A host-modelled SBI is a different contract
  and is never silently substituted (`ROADMAP.md` §P6) — which constrains what this profile
  must implement.

## Open Questions

- Exact privilege specification revision. Due before `.2` depends on it (`RK03`).
- Which Rust floating-point implementation, if any, qualifies. Due before `.7` completes; until
  then floating point is **not** part of the profile.
- What supplies an **independent** numeric expected value, given that both available reference
  models descend from the same SoftFloat source? Routed in from `P0-PROFILE.7` with its
  measurement; due before `.7` can call any numeric comparison independent.

## Blockers

- `P2-SCALAR` gate `CPU-LAB`.

## Acceptance Checklist (filled per leaf at execution time)

- [ ] **ROOT CAUSE (WHY + WHERE)** — <the command run and its real output>
- [ ] **ADDRESSED (verified)** — <measured before → after>
- [ ] **NO REGRESSION** — <the suite or gate re-run, and its result>
- [ ] **FIX** — <the change made>
- [ ] **LOCKSTEP** — <docs, contracts and indexes updated>

## Verification Log

| Date | Leaf | Checks | Result |
| --- | --- | --- | --- |
| — | — | not started | — |

## Commit Log

| Leaf | Commit subject or reference | Notes |
| --- | --- | --- |
| — | `SEMULITH-P4-0001 (tree P4-SYSTEM)` | the `.1` design brief: the pinned snapshot's privileged chapters measured present (24 priv + 46 unpriv pages); the selection decided (rv64gc-lab-v0, M/S/U, Sv39, IALIGN 16 with C, FP evidence at .7, SBI/psABI contracts); the output shape (unregistered unit dossier start) |

## Changelog

- `2026-09-13`: Created from `ROADMAP.md` §P4 and task card `T011` by `SEMULITH-TREES.2`.
- `2026-09-14`: received a routed finding from `P0-PROFILE.7` — Sail and Spike share Berkeley
  SoftFloat, 184 of 199 overlapping files byte-identical. `.7`'s ancestry inventory now starts
  from a measurement instead of a suspicion, and its "independent numeric fixtures" requirement
  has a concrete constraint to satisfy.
- `2026-10-02`: the `.1` design brief recorded (`SEMULITH-P4-0001`) and the tree
  activated. The measured pre-condition that shapes everything: the pinned v20260120
  snapshot CARRIES the privileged chapters (`priv/` — 24 pages, digest-pinned), so the
  privileged evidence base is citable today and the category census's "absent" phrasing
  is superseded. The selection decided: `rv64gc-lab-v0` — RV64I + M/A/F/D/C/Zicsr/
  Zifencei, M/S/U, Sv39, harts 1, IALIGN 16 with C; FP in the profile with its
  execution evidence gated on `.7`'s backend qualification; SBI 2.0 / psABI 1.0 (both
  already cached) as the firmware/toolchain contracts; the snapshot's `priv/` pages the
  citation authority, the PDFs reference-only. The output: the unit's profile.sexp +
  sources.sexp + DOSSIER.md, unregistered (the `.2`/`.11` precedent); catalogues arrive
  with the evidence leaves.
