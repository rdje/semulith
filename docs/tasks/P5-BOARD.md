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

- ID: `P5-BOARD.2` — **device dossiers, first device: the SiFive UART (`sifive-uart-lab-v0`)**
  Status: `done` (`2026-10-02`, `SEMULITH-P5-0007`)
  Goal: the UART's dossier — sources, requirements, state, reset, access semantics, side
  effects, and independently sourced expected results (catalog `C19`) — under
  `profiles/sifive-uart-lab-v0/`, reusing the CPU's dossier machinery. (Split
  `2026-10-02`: one device per leaf — `.2` the UART, `.10` the LAN9118; the original
  `.2` covered both. Device order decided at the `.2` design brief: the UART first.)
  Acceptance: devices reuse the CPU's dossier and gate machinery; they are not a lower
  tier (`docs/EVIDENCE_AND_GATES.md` §8).
  Result (`2026-10-02`): the dossier landed — 8 files: `DOSSIER.md`, `sources.sexp`
  (the §13 pin, digest re-verified from the cache), `requirements.sexp` (19 records:
  13 `defined` + 6 `unspecified` — the datasheet's measured silences are requirements of
  non-commitment), `contract-obligations.sexp` (19 obligations, contract
  `sifive-uart-v0` v0, the schema's new third direction `device-guarantee`),
  `state.sexp` (7 registers + 2 FIFOs + the earned hidden-state census: the model
  carries the registers and the FIFOs' contents/occupancies, and nothing else MMIO can
  reach), `profile.sexp` (19 decisions mirroring the requirements verbatim), and
  `expectations/` (3 documents: reset, tx-fifo, rx-watermark — datasheet-derived
  register-read expectations recorded before any model exists, EVD-05's shape at the
  device layer). The machinery was generalized **by declaration, not exemption**
  (`decision_device-applicability-by-declared-vehicle`): `schema/profile.sexp`'s
  processor-only fields went optional (the xlen precedent), the scope gained
  `mmio_registers`, `vehicle` gained `device-model`/`register-expectations`,
  `schema/expectations.sexp`'s `entry`/`instructions` went optional, and
  `scripts/dossier_sexp.py` moved in the same breath; EXTRACTION / EXERCISE-COVERAGE /
  INTERACTION-MATRIX derive device applicability from the declaration with
  contradiction = RED in both directions; PROFILE-CONSISTENCY needed no conditional
  (measured by a new GREEN device-shaped self-test arm); a device-guarantee discharges a
  CPU assumption by construction in `discharge_assumptions.py`, pinned by a new GREEN
  arm. **Measured in execution, fixed at root:** (1) §13.8's watermark bits carry a
  strict-inequality RAISED and a strict-inequality CLEARED condition and the manual never
  says level vs hold — the `==` boundary and pre-first-condition values are undetermined
  (`REQ-D-UART-WM-MODE`); the expectations pin a watermark bit only when its raised
  condition holds under every reading, and the dossier's first-draft "level conditions"
  claim was corrected before it ossified. (2) The dossier's `REQ-U-*` id prefix collided
  with RECORD-SCHEMA's mechanical decision→requirement mapping (`D-X` → `REQ-D-X`) — the
  prefix was private convention, the mapping is the contract; renamed, and the prose now
  names the records by their `unspecified` category instead. (3) Two gate-level defects
  fixed in review: INTERACTION-MATRIX counted the device n/a note as a "cell" (cell
  counts now count indented cell lines), and EXTRACTION's device leg demanded a reset per
  state element — the FIFOs' resets are now recorded AS DATA ("unspecified", sourced to
  the measured silence) rather than weakening the every-element-a-reset contract.
  FACT-OWNERSHIP re-pinned: 6 registry rows for the unit, the self-test fixtures re-pinned
  to three units (`__CHECKED__ 6→7`, `2→3`). The gate machinery edits were drafted by a
  subagent that died mid-task (usage limit); every diff was re-read and every gate re-run
  by the signing engineer before acceptance. Registration (`materials/units.sexp`, the
  `kind` edit, the book, the materials bill) is `.11`'s — the dossier is fully gated
  unregistered; what registration adds waits with its owner named.

- ID: `P5-BOARD.3` — **generated maps and hardware description**
  Status: `pending`
  Goal: address maps, wiring and hardware-description data generated from the canonical board definition (`OWN-05`).
  Acceptance: no handwritten duplicate map anywhere; generated artifacts carry their fingerprints and CI detects drift.
  Note (`2026-10-02`): the board-unit registration `.1` routed here moved to `.11` —
  one registration day for all three units, not two partial ones (Decisions, `.2`
  design brief).

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

- ID: `P5-BOARD.10` — **device dossiers, second device: the LAN9118 (`lan9118-lab-v0`)**
  Status: `pending`
  Goal: the NIC's dossier — sources, requirements, state, reset, access semantics, side
  effects, and independently sourced expected results (catalog `C19`) — under
  `profiles/lan9118-lab-v0/`, inheriting the device-dossier shape `.2` hardens.
  Acceptance: identical to `.2` — the full dossier and gate machinery, no lower tier
  (`docs/EVIDENCE_AND_GATES.md` §8).

- ID: `P5-BOARD.11` — **registration day: the three units register**
  Status: `pending`
  Goal: register `netboard-lab-v0`, `sifive-uart-lab-v0` and `lan9118-lab-v0` in
  `materials/units.sexp` — one registration day: the `schema/units.sexp` `kind` edit
  (the schema sanctions a `(values …)` edit "the day a real unit needs one"), the
  materials-bill generator's generalization beyond processor-shaped units (its
  INTERNAL_CONTRACTS census is processor-shaped, measured `2026-10-02`), the three
  per-unit books under `docs/models/<unit-id>/` (UNIT-BOOKS), the category-needs rows
  (SCOPE-COVERAGE), and the rest of the registration-day consequences `.1` censused
  (BREADTH-report prose among them).
  Routing note (`2026-10-02`, from the `.2` machinery design): the materials-bill
  generator's two `sibling-crate` conditionals in `scripts/gen_model_book.py` (~:136 and
  ~:212-213) must extend to the `device-model` route — declared by the device units'
  `vehicle` blocks — or the device book refuses; and its INTERNAL_CONTRACTS census is
  processor-shaped (`encoding.sexp`, `guests/`, `interactions.sexp`), needing the same
  kind-conditional generalization. Both are `.11`'s, one generator adaptation.
  Acceptance: every registered unit passes UNIT-BOOKS, MATERIALS-BILL, SCOPE-COVERAGE
  and RECORD-SCHEMA rules 10–11 — registration is one coherent day, not three partial
  ones.

## Current Frontier

| Order | Leaf | Status | Why next |
| --- | --- | --- | --- |
| 1 | `P5-BOARD.10` | `pending` | the LAN9118 dossier inherits the device shape `.2` hardened — the director's headline device |
| 2 | `P5-BOARD.11` | `pending` | registration day: the three units register together — one generator generalization, one `kind` edit |

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
- `2026-10-02` (design brief for `.2`, recorded before its execution; sources: the `.1`
  machinery census, the dossier-machinery map re-derived this day, the schema corpus):
  **the device-order Open Question is answered — the UART goes first.** The SiFive UART
  is the simplest contract on the board (7 datasheet registers, two 8-entry FIFOs, no
  DMA, one access width), so the device-dossier machinery is exercised end-to-end on the
  smallest device; the LAN9118 (`.10`) inherits the hardened shape. **Tree restructure,
  recorded:** the original `.2` (both devices' dossiers) splits — one device per leaf,
  `.2` the UART and `.10` the NIC, so each dossier lands as one safe-slice commit; `.11`
  is registration day (below). **Registration routing amended:** `.1` routed board-unit
  registration to `.3`; it consolidates into `.11` — ONE registration day for all three
  units (board + both devices). Reason: registration day carries the `schema/units.sexp`
  `kind` edit and the materials-bill generator's generalization (its INTERNAL_CONTRACTS
  census — `encoding.sexp`, `guests/`, `interactions.sexp` — is processor-shaped, so both
  board-shaped and device-shaped units need the same kind-conditional machinery); two
  registration days would split one generator adaptation across two leaves. `.1`'s
  routing note stays as recorded; this entry is the amendment.
  **The `.2` machinery census (measured `2026-10-02`):**
  - *Schema edits the UART dossier needs* (each the sanctioned "(values …) edit the day a
    real unit needs one" shape, each fired before landing): `schema/profile.sexp` is
    processor-shaped — `architecture`, `base`, `chapter_version`, `spec_revision`,
    `harts`, `ilen`, `ialign`, `extensions`, `privilege_modes` are mandatory, and a UART
    cannot honestly fill them (the P3-BREADTH.5 xlen precedent: forcing a field that does
    not apply records a lie, so the field goes optional); its `scope` table needs a
    device shape (PROFILE-CONSISTENCY refuses a profile.sexp with no scope census).
    `schema/contract-obligations.sexp` `direction` admits only
    `environment-assumption | cpu-guarantee` — a device guarantee needs the third value.
    `schema/requirements.sexp` needs NO edit (`kind` already admits `device` and
    `composition`); `authority` already admits `platform`.
  - *Registration is NOT `.2`'s* (the `.1` precedent: a content leaf does not register;
    registration-day consequences are `.11`'s). The gates that attach automatically the
    day the documents land — DOSSIER-SCHEMA (basename pairs), RECORD-SCHEMA (the
    requirements/obligations cross-checks, including CITED against the unit's own
    `sources.sexp`, MIRROR, AUTHORITY), PROFILE-CONSISTENCY (`profiles/*/profile.sexp`)
    — are glob-driven, so an unregistered dossier is still fully checked; what
    registration adds (UNIT-BOOKS, MATERIALS-BILL, SCOPE-COVERAGE, rules 10–11) waits
    for `.11` with its owner named, the WAIVER-ROUTING shape.
  - *`state.sexp`:* the schema was generalized by P3-BREADTH.5 (`register_family`,
    `memory_spaces`, the census; `xlen`/`integer_registers` optional) and can express
    device state; `scripts/gen_state.py` is rv64i-only BY CONSTRUCTION (STATE-GEN
    hardcodes the one profile), so a device `state.sexp` is decided by DOSSIER-SCHEMA +
    PROFILE-CONSISTENCY and is never fed to the generator.
  - *Expected results, independently sourced (C19):* the UART's expected results are
    datasheet-sourced register-read expectations (reset values, status/FIFO-watermark
    behaviour after defined stimuli), not an implementation's output. The dossier-machinery
    route is the `.expected.sexp` family (DOSSIER-SCHEMA maps it to
    `schema/expectations.sexp`); whether that schema is probe-shaped (pc/register steps)
    is measured at execution, and a generalization — if needed — is the same sanctioned
    schema-edit shape, recorded with the leaf.
  - *Contract and authority mapping:* the device gets its own contract id
    (`sifive-uart-v0` v0) so `.4`'s `discharge_assumptions.py` consumes device
    guarantees by id — the board definition's `satisfies` fields name them. The
    datasheet is the device's architecture authority: a datasheet-`defined` requirement
    maps to `authority architecture` (RECORD-SCHEMA rule 7); the instance address, the
    backend and the unconnected-interrupt declaration are `laboratory`/`platform`.
  - *The `profiles/` family:* the fourth unit directory re-derives the bound 3× → 4× by
    the standing arithmetic (per-unit 120 files / 573,440 B; per-part 32,768 B unchanged
    — the bound that bites), with a decision record like
    `decision_profiles-family-three-units.md`; `.10` re-derives 4× → 5× the same way.
  - *Not `.2`'s scope:* the device MODEL (Rust) — the dossier is the documents the model
    route consumes; implementation follows the model route, and firmware probes (`.5`)
    stay gated on the CPU's acceptance trajectory regardless.
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
- ~~Which device gets a dossier first in `.2` — the UART (simpler contract) or the NIC (the
  director's headline)?~~ **Answered `2026-10-02`** (Decisions, `.2` design brief): the
  **UART first** — the simplest contract on the board (7 registers, two 8-entry FIFOs, no
  DMA, one access width) exercises the device-dossier machinery end-to-end on the smallest
  device; the NIC (`.10`) inherits the hardened shape. The original `.2` split: `.2` the
  UART, `.10` the LAN9118, `.11` registration day.

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

`P5-BOARD.2` (`2026-10-02`, `SEMULITH-P5-0007`):

- [x] **REPRODUCE / ISSUE** — the board's two devices had no dossiers: `board.sexp`
  declared the unit ids with `.2` as their owner, and no `profiles/sifive-uart-lab-v0/`
  existed. Measured pre-conditions the leaf changed: `grep -c -i 16550` had already
  corrected the UART kind (`.1`); the schema census measured `direction` admitting only
  `environment-assumption | cpu-guarantee` and `profile.sexp` demanding processor-shaped
  fields a UART cannot honestly fill; `scripts/check_interaction_matrix.py` demanded a
  matrix per profile-bearing unit with no honest cell resolution available at dossier
  time.
- [x] **ROOT CAUSE (WHY + WHERE)** — the gates attach by glob the day documents land, so a
  device dossier without the applicability machinery would either fail instruction-shaped
  gates or bypass them — the lower tier the leaf's acceptance forbids. WHY the machinery
  route: the P3-BREADTH.7 vehicle declaration is the existing applicability key; the
  device extends it. WHERE, censused before editing:

  ```
  $ grep -ln 'profiles/\*' scripts/check_*.sh scripts/*.py | sort
  scripts/check_dossier_schema.sh
  scripts/check_exercise_coverage.sh
  scripts/check_extraction.sh
  scripts/check_fact_ownership.sh
  scripts/check_gate_report.sh
  scripts/check_interaction_matrix.sh
  scripts/check_requirements.sh
  scripts/check_semantics_corpus.sh
  scripts/check_unit_composition.sh
  $ grep -A2 'name direction' schema/contract-obligations.sexp
  (field (name direction) (type symbol) (values environment-assumption)
         (values cpu-guarantee))            # no device direction existed
  ```

  The edit surface: the three profile-glob gates (`check_exercise_coverage.sh`,
  `check_extraction.{py,sh}`, `check_interaction_matrix.{py,sh}`), the three schemas
  (`profile`, `expectations`, `contract-obligations`), the mapping owner
  (`dossier_sexp.py` `_SCOPE_LISTS` + expectations round-trip),
  `discharge_assumptions.py` (discharge by construction), `check_profile_consistency.sh`
  (no conditional needed — measured), FACT-OWNERSHIP (registry + self-test fixtures glob
  the real corpus).
- [x] **FIX** — the 8-file dossier under `profiles/sifive-uart-lab-v0/` (every fact read
  against the digest-verified pinned PDF, `sha256 5fa68a67…cab79c` re-derived from the
  cache); the three schema widenings with named cases; the gate branches with new
  self-test arms (EXERCISE-COVERAGE +4, EXTRACTION +4, INTERACTION-MATRIX +2,
  PROFILE-CONSISTENCY +2, discharge +1, dossier_sexp +2, FACT-OWNERSHIP re-pinned);
  6 FACT-OWNERSHIP registry rows; the `profiles/` 4× re-derivation record.
- [x] **ADDRESSED (verified)** — every dossier document validates, and the device unit is
  decided by declaration:

  ```
  $ python3 scripts/check_sexp_schema.py profiles/sifive-uart-lab-v0/profile.sexp schema/profile.sexp
  check_sexp_schema: ok — profiles/sifive-uart-lab-v0/profile.sexp conforms to profile.sexp
  $ bash scripts/check_extraction.sh
  EXTRACTION: ok (3 unit(s) sufficient — P1-LAB may cite this)
  $ bash scripts/check_interaction_matrix.sh
    profiles/sifive-uart-lab-v0: device-model route declared — the matrix attaches with the probe corpus (P5-BOARD.5)
    profiles/sifive-uart-lab-v0: 0 cells declared, every disposition resolves
  $ shasum -a 256 .materials/sifive/fu540-c000-v1p5.pdf
  5fa68a677ca4bc9fc81456840834eb4fa72874a2bd72a76c33f6709f3ecab79c  .materials/sifive/fu540-c000-v1p5.pdf
  ```

  The cross-checks hold (CITED/MIRROR/COVERAGE/AUTHORITY green over the 19/19/19
  requirement/obligation/decision mirrors — one fact, three surfaces, one wording);
  EXERCISE-COVERAGE `3 profile(s)`, PROFILE-CONSISTENCY `3 profile dossier(s) internally
  consistent`. The measured findings fixed in execution (watermark mode gap, the
  id-prefix collision, the cell-count and FIFO-reset defects) are recorded with the leaf.
- [x] **NO REGRESSION** — every edited check's self-test: EXERCISE-COVERAGE 17/0,
  EXTRACTION 9/0, INTERACTION-MATRIX 14/0, PROFILE-CONSISTENCY 41/0,
  discharge_assumptions 7/0, dossier_sexp 14/0, FACT-OWNERSHIP 10/0; the corpus
  re-validates under the widened schemas (all pre-existing `profiles/*/*.sexp` pairs
  re-checked ok); `bash scripts/check_doctrines.sh` → `=== all doctrines green ===`;
  `mdbook build docs/book` rc 0; `gen_book_index.py --check` rc 0. No Rust surface
  touched.
- [x] **LOCKSTEP** — tree (leaf + frontier + checklist + logs), `MEMORY.md` (next action
  `.10`), `CHANGELOG.md`, `LIVE_STATUS.md` (P5 row + the 341-arm count),
  `docs/TASK_TREE.md`, `docs/decisions/INDEX.md` (+2 records), KNOWLEDGE_MAP regenerated,
  mdBook `plan/p5-p7.md` (the device-dossier section).

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
| `2026-10-02` | `.2` | `check_sexp_schema.py` ok on all 7 dossier .sexp files; EXTRACTION `3 unit(s) sufficient`; EXERCISE-COVERAGE `3 profile(s)`; INTERACTION-MATRIX `device-model route declared … 0 cells`; PROFILE-CONSISTENCY `3 profile dossier(s)`; self-tests: 17/0, 9/0, 14/0, 41/0, 7/0, 14/0, 10/0; `check_fact_ownership.sh` ok (37 fact kinds); `make gate` green; `mdbook build` rc 0; `gen_book_index.py --check` rc 0 | the first device dossier landed fully gated; the machinery generalized by declaration (`device-model`/`register-expectations`); the watermark mode gap measured and recorded (`REQ-D-UART-WM-MODE`); registration routed to `.11` |
| `2026-10-02` | `.1` | `check_sexp_schema.py` (definition vs `schema/board.sexp`; the schema vs `schema/schema.sexp`) → ok; every pin re-derived from its source (GC-REPORT digest, the two catalog sha256s, the FU540/LAN9118 PDFs, the harness DEFAULT_BASE/SIZE); the 16550 census: 0 occurrences in the pinned FU540 v1p5; `make gate` green; `mdbook build docs/book` rc 0 | `netboard-lab-v0` specified: the canonical board definition pins versions, not names; the two absences declared as data with their obligations; the 16550 defect corrected at its records; registration routed to `.3` |
| `2026-10-01` | `.9` | `build_responses.py --report` → 5 fulfilled / 5 blocked, exit 0; `materials.py --fetch` → all five sha256-verified into `.materials/network/`; `materials.py --verify` → 52/0; corpus census at `c4ad8a2` (5696/293); `make gate` green | the ten answers reconciled: five materials adopted, ten requests marked (5 resolved / 5 measured-negative blocked); the knowledge cards carry the ask→answer loop |
| `2026-10-01` | `.8` | `sexp.read_file` → 10 forms (the one reader); `poll_semulith_gaps.py` read-only → NEW REQUESTS (10), rc 1; `make gate` green | ten acquisition requests filed and seen by the channel; the filing mechanics recorded semulith-side (knowledge card) |

## Commit Log

| Leaf | Commit subject or reference | Notes |
| --- | --- | --- |
| `.2` | `SEMULITH-P5-0007 (leaf P5-BOARD.2): the first device dossier — sifive-uart-lab-v0 fully gated; the machinery generalized by declaration, and the watermark mode gap measured` | 8 dossier files (19/19/19 mirrored records, 3 expectation documents); three schema widenings with named cases; five gates extended with self-test arms; FACT-OWNERSHIP re-pinned to three units; profiles/ bound re-derived 4× |
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
- `2026-10-02`: the `.2` design brief recorded (`SEMULITH-P5-0006`). Device order
  answered: the UART first (the simplest contract exercises the machinery; the NIC
  inherits it). Tree restructured — the original two-device `.2` splits into `.2` (the
  UART dossier) and `.10` (the LAN9118 dossier), one device per leaf; `.11` is
  registration day: all three units (board + both devices) register together, amending
  `.1`'s `.3` routing so the `kind` edit and the materials-bill generator's
  generalization land once, coherently. The `.2` machinery census (schema edits for
  `profile.sexp` and `contract-obligations.sexp`, the auto-attaching gates, STATE-GEN's
  non-attachment, the expectations route, the 4× `profiles/` re-derivation) is in
  Decisions. Frontier: `.2` — the UART dossier.
- `2026-10-02`: `.2` done (`SEMULITH-P5-0007`) — the first device dossier landed, fully
  gated. `profiles/sifive-uart-lab-v0/` carries 8 documents: the §13-pinned source, 19
  requirements (13 defined + 6 measured silences), 19 mirrored obligations under the new
  `device-guarantee` direction (contract `sifive-uart-v0` v0), the state document with
  its earned census, 19 verbatim decision mirrors, and 3 datasheet-derived expectation
  documents recorded before any model exists. The machinery generalized by declaration
  (`vehicle (route device-model) (comparison register-expectations)`;
  `decision_device-applicability-by-declared-vehicle`): EXTRACTION / EXERCISE-COVERAGE /
  INTERACTION-MATRIX derive device applicability with contradiction = RED; PROFILE-
  CONSISTENCY needed no conditional (measured); a device-guarantee discharges by
  construction, pinned. Measured in execution and fixed at root: the §13.8 watermark
  level-vs-hold gap (`REQ-D-UART-WM-MODE` — expectations pin a bit only when its raised
  condition holds under every reading), the `REQ-U-` id prefix colliding with
  RECORD-SCHEMA's mechanical decision→requirement mapping (renamed), the
  interaction-matrix note counted as a cell, and the FIFO resets recorded as
  "unspecified" data rather than weakening the every-element-a-reset contract.
  FACT-OWNERSHIP re-pinned to three units; the `profiles/` bound re-derived 4×
  (`decision_profiles-family-four-units`). Frontier: `.10` — the LAN9118 dossier.
