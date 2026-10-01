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

- ID: `P5-BOARD.8` — **the network-connected board's documentation, researched**
  Status: `done` (`2026-10-01`, `SEMULITH-P5-0002` — the requests are filed and the
  channel's pickup measured)
  Goal: turn the `2026-10-01` design discussion (boards that touch the world) into a
  measured documentation position BEFORE `.1` picks a board: what the corpus already
  holds, and acquisition requests for the rest through the chipdoc channel.
  Acceptance: `materials/requests.sexp` parses with the one reader; chipdoc's poller
  (read-only) sees exactly the new request ids; nothing the corpus already holds is
  re-requested; every request names its consumer (`.1`'s board choice).
  Not blocked by the CPU release gate: documentation research is an input to `.1`, not
  the milestone's execution.
  Result (`2026-10-01`): the corpus survey (the snapshotted feed, corpus `92a73b6`)
  measured the holdings — a complete register-level Ethernet MAC+PHY contract
  (TI-DP83816), ESP32/C3/S3 register maps (SVD-ESPRESSIF), the SiFive FU540/FU740 manuals
  and HiFive board docs, the TI AM335x TRM (on-SoC CPSW Ethernet) — and chipdoc's own
  note that no standalone Cadence GEM / Synopsys DesignWare GMAC spec is public. Ten
  requests filed (`materials/requests.sexp`): three wired NIC/MAC datasheets with QEMU
  model precedents (LAN9118, Intel 82540EM/e1000, RTL8139), three LTE modem AT manuals
  (Quectel EC25, SIMCom SIM7600, u-blox SARA-R4), the WiFi-module command surface
  (Espressif ESP-AT), two register-documented embedded radios for the true-RFIC leg
  (Nordic nRF52840, Microchip AT86RF233), and one honest probe — Atheros AR9271
  (ath9k_htc) register-level docs, expected absent, the negative to be recorded.
  Pickup measured: `poll_semulith_gaps.py` (chipdoc, run read-only) reports exactly the
  ten new ids, exit 1. Fulfilment is chipdoc-side and asynchronous; each request's
  status flips when the feed mirrors it. The channel's filing mechanics are now recorded
  semulith-side: `docs/knowledge/the-chipdoc-request-channel.md` — they had lived only in
  the corpus-side manual, and a session re-derived them the hard way once.

- ID: `P5-BOARD.9` — **reconcile the chipdoc answers: adopt, mark, record**
  Status: `done` (`2026-10-01`, `SEMULITH-P5-0003`)
  Goal: consume the answers the channel delivered for `.8`'s ten requests — adopt the
  five fulfilled materials into `materials/catalog.sexp` (digests verified into the
  cache), mark every request `resolved`/`blocked` with its evidence, and bring the
  semulith-side channel record up to the updated protocol (CHANNEL.md §0.3/§0.5 —
  answers arrive per-request in `catalog/responses.sexp`; our statuses stay `open`
  until WE flip them, which is expected, not silence).
  Acceptance: every fulfilled artifact's sha256 verifies from the cache
  (`scripts/materials.py --verify`); every request carries its answer and its
  evidence; the knowledge card carries the answer path end-to-end; the measured
  negatives are recorded as RESULTS (a blocked answer is an answer — `.1` plans
  around them), never re-filed without a new route.
  Not milestone execution: this is channel hygiene on `.8`'s inputs, ahead of `.1`.
  Result (`2026-10-01`): the channel verified live first —
  `build_responses.py --report` → 5 fulfilled / 5 blocked, exit 0 (every open request
  answered). The five fulfilled adopted as catalog materials (`MICROCHIP-LAN9118`,
  `UBLOX-SARA-R4-AT`, `ESPRESSIF-ESP-AT`, `NORDIC-NRF52840-PS`,
  `MICROCHIP-AT86RF233`), fetched into `.materials/network/` with every sha256
  re-verified (`materials --verify: 52 verified / 0 unresolved`); the corpus pin
  re-derived to `c4ad8a2` (5696 files / 293 PDFs, the same census). All ten requests
  carry their answer: five `resolved`, five `blocked` — each blocked answer a MEASURED
  NEGATIVE with its consequence named (the LAN9118 dossier is the wired-NIC primary;
  SARA-R4 the cellular AT primary; the AR9271 probe's negative IS its answer — no
  public register-level WiFi baseband documentation exists). The knowledge cards
  carry the full ask→answer loop (`the-chipdoc-request-channel.md` refreshed with the
  §0.3/§0.5 answer path; `the-chipdoc-channel.md` updated and cross-linked, its
  measured history kept). Consequence for `.1`: the board's network device now has
  FIVE sourced candidates (wired NIC, LTE modem, WiFi module, two true RFICs) plus
  five measured negatives that close the alternatives.

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

`P5-BOARD.9` (`2026-10-01`, `SEMULITH-P5-0003`):

- [x] **ROOT CAUSE (WHY + WHERE)** — CHANNEL.md §0.3/§0.5 (re-read `2026-10-01`) closed
  the answer path per-request after the second incident: chipdoc answered all ten
  `.8` requests (`542a14b`), and semulith still saw ten `open` — because only WE flip
  our own file. Verified live before any edit: `SEMULITH_ROOT=<repo> python3
  <corpus>/scripts/build_responses.py --report` → 5 fulfilled / 5 blocked, exit 0.
  WHERE: `materials/catalog.sexp` (five adopted records + the corpus re-pin),
  `materials/requests.sexp` (ten answers), the two knowledge cards.
- [x] **ADDRESSED (verified)** — `SEMULITH_CHIPDOC_ROOT=<corpus> python3
  scripts/materials.py --fetch <the five ids>` → all five `sha256 verified` into
  `.materials/network/`; `scripts/materials.py --verify` → `materials --verify: 52
  verified / 0 unresolved`, rc=0; the corpus census re-derived at `c4ad8a2` (5696
  files / 293 PDFs); every request now carries `(status resolved|blocked)` + its
  `(answer …)` with the evidence verbatim from `catalog/responses.sexp`.
- [x] **NO REGRESSION** — `bash scripts/check_doctrines.sh` → `=== all doctrines
  green ===`; `mdbook build docs/book` rc 0 (no book surface touches the channel).
- [x] **FIX** — the five catalog records + the re-pin, the ten answers, the two
  knowledge cards (+ INDEX hooks), this tree's `.9`.
- [x] **LOCKSTEP** — tree (leaf + checklist + logs), `MEMORY.md` (next action was
  this reconciliation — now `.1`), `CHANGELOG.md`, `DEV_NOTES.md`,
  `docs/knowledge/INDEX.md`.

`P5-BOARD.8` (`2026-10-01`, `SEMULITH-P5-0002`):

- [x] **ROOT CAUSE (WHY + WHERE)** — the `2026-10-01` design discussion needs measured
  documentation positions before `.1` can pick a network-connected board; and the
  channel's filing mechanics lived only corpus-side (`CHANNEL.md`), so a session had to
  re-derive them — a durable-memory gap on semulith's side. WHERE the corpus stands:
  `grep -io … .semulith-data/chipdoc/catalog/semulith-proposals.sexp` measured the
  holdings (DP83816, ESP32 SVDs, FU540/FU740, AM335x; the GEM/GMAC negative already on
  record).
- [x] **ADDRESSED (verified)** — `materials/requests.sexp` filed (10 requests, each
  naming `.1` as consumer); parses with the one reader (`sexp.read_file` → 10 forms);
  chipdoc's poller run READ-ONLY — `SEMULITH_ROOT=<repo> python3
  <corpus>/scripts/poll_semulith_gaps.py` → `NEW REQUESTS (10) [source=requests]`,
  rc=1 — exactly the ten new ids. The knowledge card
  `docs/knowledge/the-chipdoc-request-channel.md` (+ INDEX row) closes the memory gap.
- [x] **NO REGRESSION** — `make gate` → `=== all doctrines green ===` (the new
  `materials/requests.sexp` is in-family for SOURCE-FORMAT and parses with the one
  reader); no existing request/gap touched.
- [x] **FIX** — `materials/requests.sexp` (new), the knowledge card, this tree's `.8`.
- [x] **LOCKSTEP** — tree (leaf + checklist + logs), `MEMORY.md` (the channel card named),
  `CHANGELOG.md`, `DEV_NOTES.md`, `docs/knowledge/INDEX.md`; mdBook: the channel is
  internal plumbing — the book's materials chapter does not list it, no drift.

## Verification Log

| Date | Leaf | Checks | Result |
| --- | --- | --- | --- |
| `2026-10-01` | `.9` | `build_responses.py --report` → 5 fulfilled / 5 blocked, exit 0; `materials.py --fetch` → all five sha256-verified into `.materials/network/`; `materials.py --verify` → 52/0; corpus census at `c4ad8a2` (5696/293); `make gate` green | the ten answers reconciled: five materials adopted, ten requests marked (5 resolved / 5 measured-negative blocked); the knowledge cards carry the ask→answer loop |
| `2026-10-01` | `.8` | `sexp.read_file` → 10 forms (the one reader); `poll_semulith_gaps.py` read-only → NEW REQUESTS (10), rc 1; `make gate` green | ten acquisition requests filed and seen by the channel; the filing mechanics recorded semulith-side (knowledge card) |

## Commit Log

| Leaf | Commit subject or reference | Notes |
| --- | --- | --- |
| `.9` | `SEMULITH-P5-0003 (leaf P5-BOARD.9): the chipdoc answers reconciled — five materials adopted and digest-verified, ten requests marked, the answer path recorded` | 5 fulfilled adopted (LAN9118, SARA-R4, ESP-AT, nRF52840, AT86RF233); 5 measured negatives recorded with consequences; corpus re-pinned c4ad8a2; the knowledge cards carry §0.3/§0.5 |
| `.8` | `SEMULITH-P5-0002 (leaf P5-BOARD.8): the network-connected board's documentation researched — corpus surveyed, ten requests filed, the channel measured` | DP83816/ESP32-SVD/FU540/FU740/AM335x already held; LAN9118/e1000/RTL8139, three LTE AT manuals, ESP-AT, nRF52840, AT86RF233, and the AR9271 probe requested; the poller sees exactly the ten |
| — | `pending` | `pending` |

## Changelog

- `2026-09-13`: Created from `ROADMAP.md` §P5 by `SEMULITH-TREES.3`.
- `2026-10-01`: Design discussion recorded (boards that touch the world;
  `SEMULITH-P5-0001`). `.8` done (`SEMULITH-P5-0002`): the documentation research — the
  corpus's holdings surveyed from the snapshotted feed, ten acquisition requests filed
  through `materials/requests.sexp` (the preferred channel), pickup measured with
  chipdoc's poller (read-only, exactly the ten new ids), and the channel's filing
  mechanics recorded as a knowledge card so no session re-derives them.
- `2026-10-01`: `.9` done (`SEMULITH-P5-0003`): the channel's answers consumed —
  verified live first (`build_responses.py --report`, 5/5, exit 0), the five fulfilled
  adopted as catalog materials with every digest re-verified at fetch (52/0), all ten
  requests marked (five `resolved`, five `blocked` — each blocked a measured negative
  with its consequence named, never to be re-filed without a new route), the corpus
  re-pinned `c4ad8a2`, and the knowledge cards brought up to the §0.3/§0.5 answer
  path. `.1` inherits five sourced network-device candidates plus five measured
  negatives closing the alternatives.
