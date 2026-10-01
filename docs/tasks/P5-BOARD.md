# P5-BOARD: model one board, and prove it satisfies the accepted CPU contract

## Metadata

- Tree ID: `P5-BOARD`
- Status: `active`
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
  Status: `done` (`2026-10-02`, `SEMULITH-P5-0005`)
  Goal: documented memory map, reset behaviour, timers, interrupt controller, serial console; the canonical board definition composing **exact** processor and device versions (`OWN-05`).
  Acceptance: the board profile pins versions, not names.
  Result (`2026-10-02`): the board is **`netboard-lab-v0`** — the id finalized in the
  units-registry idiom. The canonical definition is
  [`profiles/netboard-lab-v0/board.sexp`](../../profiles/netboard-lab-v0/board.sexp),
  gated by the new [`schema/board.sexp`](../../schema/board.sexp) (the first non-processor
  source-of-truth schema; DOSSIER-SCHEMA pairs them by basename), narrated by
  [`profiles/netboard-lab-v0/DOSSIER.md`](../../profiles/netboard-lab-v0/DOSSIER.md).
  Every pin is a version, not a name: the processor by unit id + version `0` + the
  GATE-REPORT-gated dossier content digest; each device by its datasheet's material id +
  revision + sha256. The memory map (2 GiB RAM at the harness's existing base, the UART at
  the sourced FU540 instance address, the NIC in a 256-byte window spanning the datasheet's
  direct register map), cold-only reset, the serial console, and the two declared absences
  (timers, interrupt controller — each carrying its reason and the obligation it satisfies)
  are DATA, with `satisfies` fields pre-wiring `.4`'s composition verdict. **One measured
  defect found and fixed in execution:** the design brief's "16550-compatible UART" label
  is false against the pinned source — a `pdftotext` census of `SIFIVE-FU540-C000` v1p5
  finds zero occurrences of "16550"; the manual's §13 UART is the SiFive UART
  (txdata/rxdata/txctrl/rxctrl/ie/ip/div, 32-bit-aligned). The source pin was the intent,
  so the board adopts the SiFive UART and the label is corrected in
  `materials/catalog.sexp` and recorded in `D-BOARD-UART-KIND`. **Scope routing recorded:**
  unit registration (`materials/units.sexp`), the `kind` edit in `schema/units.sexp`, and
  the per-unit book land with the leaf that materializes the composed board unit (`.3`) —
  the registry admits a new kind "the day a real unit needs one", and registration day
  carries UNIT-BOOKS/MATERIALS-BILL/generator consequences that are `.3`'s, not a
  specification's. The `profiles/` family's third unit directory triggered the standing
  re-derivation: 3× bound, `decision_profiles-family-three-units`.

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
| 1 | `P5-BOARD.2` | `pending` | the platform is specified; the devices need dossiers before anything composes — and `.2` decides which device goes first (Open Questions) |

## Decisions

- `2026-09-13`: a **smaller separately accepted CPU profile** may support an earlier board
  branch for archogen, before the richer Linux profile exists. The CPU-first rule still applies:
  the profile must already have passed a CPU gate (`ROADMAP.md` §P5).
- `2026-10-02` (design brief for `.1`, recorded before its execution; sources: the `.8`/`.9`
  reconciled corpus, the CPU contract, the machinery census below):
  **the board question is answered.** Open Question "which board" closes: the first board
  composes `rv64i-lab-v0` v0 (the EXPERIMENTAL release — the board inherits that status and
  must say so) with exactly two devices, both digest-pinned in `materials/catalog.sexp`:
  a **16550-compatible UART** (serial console; source `SIFIVE-FU540-C000` v1p5) and a
  **LAN9118 wired NIC** (source `MICROCHIP-LAN9118` DS00002266B; PIO host bus — no bus-master
  DMA, so every device effect reaches the guest through its own MMIO accesses, exactly the
  shape the CPU contract's eight assumptions tolerate). The director's `2026-10-01` brief —
  every board touches the world — is satisfied by the NIC from board v0.
  **Timers and interrupt controllers are ABSENT by contract, and that is the design's sharpest
  edge:** `OB-ENV-VIRTUAL-TIME` and `OB-ENV-EVENT-DELIVERY` are *environment assumptions* the
  board must satisfy (ENV-02), so a CLINT/PLIC would not be a feature but a composition
  REJECTION (`.4`'s verdict, `scripts/discharge_assumptions.py` — already built and
  self-tested). Both devices' interrupt lines are **unconnected and declared so**; drivers
  poll. The board spec dispositions every `ROADMAP.md` §P5 element — memory ✓, reset ✓ (cold
  only, `OB-ENV-RESET`), serial console ✓, timers/IRQ controllers ✗-by-contract, deferred to
  the P4-profile board branch where the CPU contract has counter/interrupt assumptions to
  satisfy instead.
  **The network backend is the recorded-trace replay leg** (deterministic, evidence-grade;
  the `.8` design discussion's split): without a time source, RX delivery is pinned to the
  guest's own polling — the device holds the next recorded packet and offers it when polled,
  so the harness's retired-instruction count never becomes target-visible
  (`OB-ENV-VIRTUAL-TIME`'s second half). TX goes to a recording sink. A live host-socket
  backend stays laboratory play at the `Environment` boundary, never inside an evidence claim.
  **Machinery `.1` must touch** (censused `2026-10-02`): `schema/units.sexp` `kind` admits only
  `processor` — a `board` value is a declared-by-edit extension ("the day a real unit needs
  one"); the `profiles/` family's 240-file ceiling is at its 2-unit budget — a third unit
  directory fires README-ROUTING-CLOSURE and needs a reviewed re-derivation (director-approved
  in principle `2026-10-02`); `scripts/compose_units.py` materializes boards from a
  `(composition …)` manifest but its tracked-board freshness gate is explicitly deferred to
  the first tracked board (`.3` owns it); no memory-map/reset/device fields exist in any
  schema — the board-definition document and its schema are `.1`'s to design (house shape:
  one S-expression source of truth, schema in `schema/`, generated mirrors gated, dossier
  under `profiles/<board-id>/`); `gate_report.py --gate BOARD` is `.7`'s, with the
  `BREADTH`/`--gate` precedent mapped.
  **Version pins, not names** (the leaf's acceptance): processor = unit id + version `0` +
  the dossier content digest in `profiles/rv64i-lab-v0/GC-REPORT.md` (GATE-REPORT-gated);
  devices = their datasheets' material id + revision + sha256; device UNIT dossiers land in
  `.2` — where a device unit does not yet exist, the board definition declares the id and
  names `.2` as its owner (the WAIVER-ROUTING shape, honesty with an owner).
- `2026-10-02` (`.1` execution amendments, recorded with the leaf):
  **CORRECTION — the "16550-compatible UART" label was measured false.** A `pdftotext`
  census of the pinned `SIFIVE-FU540-C000` v1p5 artifact finds zero occurrences of
  "16550"; the manual's §13 UART is the **SiFive UART** (txdata/rxdata/txctrl/rxctrl/ie/
  ip/div, 8-entry FIFOs, naturally aligned 32-bit accesses). The source pin — not the
  label — was the brief's intent, so `netboard-lab-v0` adopts the SiFive UART; the label
  is corrected in `materials/catalog.sexp` (the `SIFIVE-FU540-C000` supplies text) and
  the board definition carries the correction as `D-BOARD-UART-KIND`. Spike's
  `ns16550@10000000` (in `profiles/rv64i-lab-v0/references.sexp`) is the reference's own
  device tree, factual, and untouched. The brief's lines above stay as recorded — this
  note is the correction, per the house pattern (a defect is corrected with evidence,
  not edited out of history).
  **Registration routing:** unit registration in `materials/units.sexp`, the
  `(values board)` edit in `schema/units.sexp`, and the per-unit book land with `.3` —
  the leaf that materializes the composed board unit. Registration day carries the
  UNIT-BOOKS / MATERIALS-BILL / book-generator / BREADTH-report-prose consequences
  (censused in `.1` execution); a specification leaf does not register.
  **The `profiles/` bound re-derived to 3×** (`decision_profiles-family-three-units`):
  142 files / ~565 KiB measured at staging — nothing fired; the family's contract
  expanded to three units and the standing arithmetic followed.

## Open Questions

- ~~Which board?~~ **Answered `2026-10-02`** (Decisions, design brief; id finalized at `.1`
  execution): **`netboard-lab-v0`** — rv64i-lab-v0 v0 + the SiFive UART + LAN9118, no
  timer/IRQ controller by contract.
- Which device gets a dossier first in `.2` — the UART (simpler contract) or the NIC (the
  director's headline)? Decided at `.2`, not blocking `.1`.

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

- ~~The CPU release gate.~~ Resolved for `.1`–`.4` (`2026-10-02`): `ROADMAP.md` §P5 — *"contract
  design starts now; board execution still follows CPU validation."* The platform specification
  (`.1`), device dossiers (`.2`), generated maps (`.3`) and the composition verdict (`.4`) are
  contract design over an already-gated CPU contract (`rv64i-lab-v0` passed G1 `2026-09-30`);
  the board inherits the CPU's EXPERIMENTAL status and every board claim must read as
  conditional on it. Firmware probes (`.5`) and the `BOARD` gate verdict (`.7`) stay gated on
  the CPU's own acceptance trajectory — the composition can never outrank its processor.

## Acceptance Checklist (filled per leaf at execution time)

`P5-BOARD.1` (`2026-10-02`, `SEMULITH-P5-0005`):

- [x] **ROOT CAUSE (WHY + WHERE)** — the composition check (`.4`) needs a specified
  platform to check, and no memory-map/reset/device fields existed in any schema: the
  board-definition document and its schema were `.1`'s to design (the recorded machinery
  census). Measured before designing: a search of `schema/` finds no memory-map, reset
  or device construct (census: 17 schema files, none board-shaped), and the brief's
  UART label failed its source check — `grep -c -i 16550 target/fu540.txt` (the
  `pdftotext` rendering of the pinned artifact) → 0.
  WHERE: `schema/board.sexp` (new), `profiles/netboard-lab-v0/board.sexp` +
  `DOSSIER.md` (new), `materials/catalog.sexp` (the 16550 correction),
  `doctrine/readme_routes.tsv` + `docs/decisions/decision_profiles-family-three-units.md`
  (the third unit directory), `doctrine/fact_ownership.tsv` (the new fact kind).
- [x] **ADDRESSED (verified)** — `python3 scripts/check_sexp_schema.py
  profiles/netboard-lab-v0/board.sexp schema/board.sexp` → ok; the schema validates under
  the schema language (`schema/board.sexp` against `schema/schema.sexp`) → ok. Every pin
  verified against its source before being written: the dossier digest read from
  `profiles/rv64i-lab-v0/GC-REPORT.md`; both device sha256s read from
  `materials/catalog.sexp`; the UART's kind/register model/widths measured from the
  pinned FU540 PDF (§13, Table 58/59 — and the 16550 defect measured: zero occurrences);
  the NIC's widths and map span measured from the pinned LAN9118 PDF (§1.10, Table 5-1);
  the RAM base/size read from `crates/semulith-cli/src/main.rs` (DEFAULT_BASE/SIZE).
- [x] **NO REGRESSION** — the focused gates: DOSSIER-SCHEMA (the new basename pair),
  RECORD-SCHEMA, FACT-OWNERSHIP (the new fact kind), README-ROUTING-CLOSURE (the 3×
  re-derivation), DERIVED-COUNTS, UNIT-BOOKS, MATERIALS-BILL, then `make gate` → all
  green; `mdbook build docs/book` rc 0. No Rust surface touched.
- [x] **FIX** — the schema, the definition, the dossier, the catalog correction, the
  ceiling re-derivation + decision record (+ INDEX), the fact-ownership row, this tree's
  `.1`, the book's P5 chapter.
- [x] **LOCKSTEP** — tree (leaf + frontier + decisions + checklist + logs), `MEMORY.md`
  (next action `.2`), `CHANGELOG.md`, `DEV_NOTES.md`, `LIVE_STATUS.md` (P5 row),
  `docs/decisions/INDEX.md`, mdBook `plan/p5-p7.md`.

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
| `2026-10-02` | `.1` | `check_sexp_schema.py` (definition vs `schema/board.sexp`; the schema vs `schema/schema.sexp`) → ok; every pin re-derived from its source (GC-REPORT digest, the two catalog sha256s, the FU540/LAN9118 PDFs, the harness DEFAULT_BASE/SIZE); the 16550 census: 0 occurrences in the pinned FU540 v1p5; `make gate` green; `mdbook build docs/book` rc 0 | `netboard-lab-v0` specified: the canonical board definition pins versions, not names; the two absences declared as data with their obligations; the 16550 defect corrected at its records; registration routed to `.3` |
| `2026-10-01` | `.9` | `build_responses.py --report` → 5 fulfilled / 5 blocked, exit 0; `materials.py --fetch` → all five sha256-verified into `.materials/network/`; `materials.py --verify` → 52/0; corpus census at `c4ad8a2` (5696/293); `make gate` green | the ten answers reconciled: five materials adopted, ten requests marked (5 resolved / 5 measured-negative blocked); the knowledge cards carry the ask→answer loop |
| `2026-10-01` | `.8` | `sexp.read_file` → 10 forms (the one reader); `poll_semulith_gaps.py` read-only → NEW REQUESTS (10), rc 1; `make gate` green | ten acquisition requests filed and seen by the channel; the filing mechanics recorded semulith-side (knowledge card) |

## Commit Log

| Leaf | Commit subject or reference | Notes |
| --- | --- | --- |
| `.1` | `SEMULITH-P5-0005 (leaf P5-BOARD.1): the platform specified — netboard-lab-v0's canonical board definition pins versions, not names; the 16550 label measured false and corrected` | `schema/board.sexp` designed (the first non-processor SoT schema); the definition + DOSSIER land under `profiles/netboard-lab-v0/`; timers/IRQ absent-by-contract as data with `satisfies` pre-wiring `.4`; profiles/ bound re-derived 3×; registration routed to `.3` |
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
- `2026-10-02`: the `.1` design brief recorded (`SEMULITH-P5-0004`): the board question
  answered — rv64i-lab-v0 v0 + 16550 UART (`SIFIVE-FU540-C000`) + LAN9118
  (`MICROCHIP-LAN9118`), timers/IRQ controllers absent BY CONTRACT (ENV-02; a CLINT/PLIC
  would be a composition rejection, not a feature), recorded-trace replay RX backend,
  polled drivers, IRQ lines unconnected-and-declared. The machinery census for `.1`
  (units kind edit, profiles/ ceiling, composition freshness gate, board schema to
  design) and the version-pin shape are in Decisions; the CPU-release-gate blocker is
  resolved for `.1`–`.4` as contract design per `ROADMAP.md` §P5.
- `2026-10-02`: `.1` done (`SEMULITH-P5-0005`) — the platform specified. The board is
  `netboard-lab-v0`: `profiles/netboard-lab-v0/board.sexp` under the new
  `schema/board.sexp`, every pin a version (unit id + version + GATE-REPORT-gated
  dossier digest; material id + revision + sha256), the memory map / cold reset /
  serial console / declared timer-and-IRQ absences all data with `satisfies`
  pre-wiring `.4`. One measured defect fixed in execution: the brief's
  "16550-compatible UART" label was false against the pinned source (zero "16550"
  occurrences in FU540-C000 v1p5); the SiFive UART (§13) is the adopted device, the
  catalog's supplies text corrected, the correction recorded as `D-BOARD-UART-KIND`.
  Registration (`materials/units.sexp`, the `kind` edit, the book) routed to `.3`;
  the `profiles/` bound re-derived to 3× (`decision_profiles-family-three-units`).
  Frontier: `.2` — device dossiers.
