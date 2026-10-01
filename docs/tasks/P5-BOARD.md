# P5-BOARD: model one board, and prove it satisfies the accepted CPU contract

## Metadata

- Tree ID: `P5-BOARD`
- Status: `proposed`
- Roadmap lane: `ROADMAP.md` §6 → **P5 — Model one board in Rust**
- Gate: `BOARD`
- Depends on: the CPU release gate (`P4-SYSTEM` → `CPU-SYSTEM`), or a separately accepted smaller profile
- Unlocks: `P6-LINUX`, `AG-OS`
- Created: `2026-09-13`
- Owner: repo-local workflow

## Goal

A minimal virtual platform — memory, reset, timers, interrupt controllers, serial console —
whose devices carry the same dossier, requirement-link and evidence machinery as the CPU, and
which **demonstrably satisfies every assumption** in the accepted CPU/environment contract.

## Non-Goals

- No Linux. Booting is `P6-LINUX`; firmware probes here are device evidence, not a boot claim.
- No device invented to make something work. A device without a source is a device without
  expected results.

## Acceptance Criteria — gate `BOARD`

Devices and composition pass their applicable gates; small firmware probes pass; **no silently
incompatible CPU/environment assumption remains**.

## Task Tree

- ID: `P5-BOARD.1` — **platform specification**
  Status: `pending`
  Goal: documented memory map, reset behaviour, timers, interrupt controller, serial console; the canonical board definition composing **exact** processor and device versions (`OWN-05`).
  Acceptance: the board profile pins versions, not names.

- ID: `P5-BOARD.2` — **device dossiers**
  Status: `pending`
  Goal: per device — sources, requirements, state, reset, access semantics, side effects, and independently sourced expected results (catalog `C19`).
  Acceptance: devices reuse the CPU's dossier and gate machinery; they are not a lower tier (`docs/EVIDENCE_AND_GATES.md` §8).

- ID: `P5-BOARD.3` — **generated maps and hardware description**
  Status: `pending`
  Goal: address maps, wiring and hardware-description data generated from the canonical board definition (`OWN-05`).
  Acceptance: no handwritten duplicate map anywhere; generated artifacts carry their fingerprints and CI detects drift.

- ID: `P5-BOARD.4` — **composition against the CPU contract** — the gate's core obligation
  Status: `pending`
  Goal: for **every** CPU assumption, name the board or device guarantee that satisfies it, or reject the composition. Reset wiring, memory attributes, source priorities, counter units, time progress, access side effects, reservation invalidations, instruction visibility (`docs/CPU_ENVIRONMENT.md` §5, `ENV-02`).
  Acceptance: an unmatched assumption is a **rejection**, not a note. The laboratory's interface tests are re-run against the board provider where meaningful.

- ID: `P5-BOARD.5` — **firmware probes**
  Status: `pending`
  Goal: small firmware that finds and interacts with the devices it expects (catalog `C19`).
  Acceptance: a probe failure is classified as a CPU, contract, device or composition issue with an explicit owner — never as an unattributed emulator bug.

- ID: `P5-BOARD.6` — **platform capability manifest**
  Status: `pending`
  Goal: the read-only derived export of the accepted processor/device/board profile and its boot contract, for archogen's compatibility checker (`docs/ARCHOGEN_INTEGRATION.md` §3).
  Acceptance: derived, never handwritten; eADL imports facts rather than becoming a second hardware implementation (`OWN-06`).

- ID: `P5-BOARD.7` — **the `BOARD` gate report**
  Status: `pending`
  Goal: generate from pinned inputs.
  Acceptance: a compatible manifest is recorded as **not** proving the OS correct, nor that the manifest matches the implementation.

## Current Frontier

| Order | Leaf | Status | Why next |
| --- | --- | --- | --- |
| 1 | `P5-BOARD.1` | `pending` | the composition check needs a specified platform to check |

## Decisions

- `2026-09-13`: a **smaller separately accepted CPU profile** may support an earlier board
  branch for archogen, before the richer Linux profile exists. The CPU-first rule still applies:
  the profile must already have passed a CPU gate (`ROADMAP.md` §P5).

## Open Questions

- Which board? Driven by the first real workload — an archogen OS or the Linux route — and
  decided before `.1`, not during it (`RK12`).

## Design Discussions

- `2026-10-01` (director, ideas exchange — recorded to resume later; no pivot, no leaf scope
  changed): **boards that touch the world.** The director's brief: every board SEMULITH
  models shall have a network connection — maybe an RFIC chip model, i.e. any component
  letting the model's CPUs interact with reality outside the model and use the host's
  network (wifi); ideally the model's memory is accessible from the host. The director
  explicitly invited pushback and grading ("some might be feasible, others out of reach or
  totally nuts").
  **The engineer's assessment, recorded:**
  - *NIC + host networking: feasible, precedented, right-sized.* The device model is an
    ordinary bus device (registers + DMA + interrupt) — `.2`'s device-dossier machinery
    covers it unchanged. The design-critical split is the BACKEND: a recorded-trace replay
    backend (deterministic, evidence-grade, re-runnable in a fresh clone) versus a live
    host-socket backend (laboratory play). QEMU's SLiRP-style user-mode NAT shows the live
    shape is unprivileged and portable; TAP/L2 is real frames but needs host privileges and
    is macOS-hostile (vmnet), so it is the later, named extension. The live backend must
    sit at the `Environment` boundary (`crates/semulith-core/src/env.rs` — the sanctioned
    plug point) and may never enter a deterministic evidence claim; the recorded backend is
    the evidence leg. Guest→host networking is a CAPABILITY the harness declares — typed
    and auditable, the contract/obligations machinery's native shape.
  - *RFIC model: feasible as a device; the blocker is documentation, not modeling.* WiFi
    baseband register maps are mostly NDA; radios with public register documentation exist
    (e.g. the nRF52 BLE radio's public Product Spec; IEEE 802.15.4 parts like the
    AT86RF233). A synthetic RFIC with a declared contract is always possible and never a
    compatibility claim — the same discipline as `synth24`. Renode (802.15.4/BLE medium
    models with Wireshark bridges) is the existence proof that simulators do radios.
  - *Host access to the model's memory: feasible, cheap, and already half-built.* The
    canonical-dump/snapshot machinery plus the bench `Observer` are the spine; a live
    inspector (GDB-stub-style or a memory socket) is LAB-BENCH-shaped. Note:
    `LAB-BENCH.2` is feedback-gated — this message is relevant feedback for it.
  - *Consequence for `.1`'s open question:* "which board" gains a candidate criterion —
    prefer a board whose network device has PUBLIC register documentation, so the device
    dossier has sources (the tree's own non-goal: no device without a source).
  **Resume here when P5 opens; nothing in P3-BREADTH's frontier changes.**

## Blockers

- The CPU release gate.

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
| — | `pending` | `pending` |

## Changelog

- `2026-09-13`: Created from `ROADMAP.md` §P5 by `SEMULITH-TREES.3`.
