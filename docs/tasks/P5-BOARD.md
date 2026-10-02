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
  Status: `done` (`2026-10-02`, `SEMULITH-P5-0013`)
  Goal: address maps, wiring and hardware-description data generated from the canonical board definition (`OWN-05`).
  Acceptance: no handwritten duplicate map anywhere; generated artifacts carry their fingerprints and CI detects drift.
  Note (`2026-10-02`): the board-unit registration `.1` routed here moved to `.11` —
  one registration day for all three units, not two partial ones (Decisions, `.2`
  design brief).
  Result (`2026-10-02`): the maps are generated and drift-gated. `scripts/gen_board.py`
  discovers boards by declaration (`profiles/*/board.sexp`) and emits seven artifacts
  per board from board.sexp alone: `composition.sexp` (the manifest — the part list
  derived from the pins), the four composed catalogues (99 requirements, 107
  obligations, 5 sources, the rv64i encoding — materialized by
  `compose_units.compose_resolved`, a factorization of `compose` so the manifest-file
  path and the generator path share the ONE materialization code path; the refactor
  measured byte-identical on the real parts and self-test 9/9), `hardware.sexp` (the
  hardware description under the new `schema/hardware.sexp`: regions resolved with
  computed ends, the device↔region↔widths↔interrupt↔backend wiring, the console, the
  reset, the absences with their `satisfies` edges), and `map.md` (the human-readable
  map — the DOSSIER links it, the board book includes it: one owner, two readers,
  the include verified in the built HTML). Every artifact carries the OWN-03
  fingerprint header (canonical-input + generator sha256, repo-relative paths). The
  freshness proof `compose_units.py` deferred to the first tracked board landed as
  the **BOARD-GEN doctrine** (`scripts/check_board_gen.sh`, registered, mirrored):
  `--check` re-derives all seven and refuses DRIFT by name; the generator refuses an
  inconsistent definition by name (overlap, mmio window without device or device
  without window, executable mmio, ghost console) — self-test 9/9 with every RED arm
  asserting the reason. **The one handwritten duplicate map died**: the census found
  exactly one (the DOSSIER.md table, 3 rows); it is replaced by the generated map,
  the prose kept as decision narrative citing `D-BOARD-MEMORY-MAP`. FACT-OWNERSHIP
  gained 8 rows (the two measured corpus pairs — `obligations (netboard-lab-v0)` with
  RECORD-SCHEMA, `encodings (netboard-lab-v0)` with BOARD-GEN — plus the derivation
  rows with owner board.sexp, governor BOARD-GEN; 54 kinds total) and the fixture
  re-pinned to five units (`__CHECKED__ 8→9`, self-test 10/10). **Two measured
  findings, recorded at root:** (1) the brief's register-surface containment check is
  NOT implementable — the device dossiers carry register offsets in prose with
  datasheet citations, never as machine-readable data (measured in both `state.sexp`
  documents and the expectations); the generator's refusals are scoped to what
  board.sexp itself proves, and machine-readable offsets arrive with the device
  models, where the check belongs. (2) The DOSSIER's status table was stale post-
  `.11` (device dossiers and registration still marked absent/deferred) — the
  defect the brief logged; fixed with this leaf. (3) The `profiles/` per-part bound
  bit a second time — the first DERIVED member class: the composed
  `contract-obligations.sexp` (104,372 B) exceeds 64 KiB; handled by the standing
  reviewed-raise rule (`decision_profiles-family-composed-units`: 65,536 → 131,072
  at 0.80×, aggregates unmoved at 167 files / 1,051,283 B = 0.28×/0.37× of 5×).
  DERIVED-COUNTS fired as designed (31→32 doctrines, 345→354 arms, re-derived in
  `LIVE_STATUS.md`). The composed catalogues on disk are `.4`'s pre-staged input:
  the board directory is now an ordinary composed unit, checked by the unchanged
  tools.

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
  Status: `done` (`2026-10-02`, `SEMULITH-P5-0009`)
  Goal: the NIC's dossier — sources, requirements, state, reset, access semantics, side
  effects, and independently sourced expected results (catalog `C19`) — under
  `profiles/lan9118-lab-v0/`, inheriting the device-dossier shape `.2` hardens.
  Acceptance: identical to `.2` — the full dossier and gate machinery, no lower tier
  (`docs/EVIDENCE_AND_GATES.md` §8).
  Result (`2026-10-02`): the dossier landed — 9 files: `DOSSIER.md`, `sources.sexp`
  (the DS00002266B pin, digest re-verified from the cache), `requirements.sexp` (52
  records: 46 `defined` + 1 `reserved` + 1 `unspecified` + 4 `implementation-defined` —
  the datasheet's measured silences and strap/board deferrals are requirements of
  non-commitment), `contract-obligations.sexp` (52 obligations, contract `lan9118-v0`
  v0, direction `device-guarantee`; `laboratory` authority for exactly the three
  composition dispositions), `state.sexp` (24 direct CSRs + 12 indexed MAC CSRs + 13
  doubly-indexed PHY registers + 4 FIFO families + the earned hidden-state census: the
  model carries the registers, the FIFOs' contents/occupancies, the TX command-parser
  state and the 16-bit pairing latch — and nothing else MMIO can reach; the MIL FIFOs
  are not host-visible by the datasheet's own words), `profile.sexp` (52 verbatim
  decision mirrors — generated from requirements.sexp mechanically, so drift is
  impossible by construction AND refused by gate), and `expectations/` (3 documents:
  cold-reset reads, the exact TDFREE free-space accounting with TX_ON = 0, the
  recorded-trace RX path with pop/PEEK and the underrun → RXE discipline). **No
  machinery edit was needed** — `.2`'s by-declaration generalization covered the NIC;
  the mechanical re-pins were FACT-OWNERSHIP (+6 registry rows; self-test fixtures
  `__CHECKED__ 7→8` and `3→4`, comments updated) and the `profiles/` 4× → 5×
  re-derivation (`decision_profiles-family-five-units`) — where **the per-part bound
  bit for the first time**: the NIC's mirrored catalogues exceed 32 KiB
  (contract-obligations 60,112 B), so the per-part doubled to 64 KiB, reviewed and
  recorded. **Measured in execution, recorded at root:** (1) the two `pdftotext` modes
  DISAGREE on Table 5-1's Default column (two-column layout scrambles row pairing) —
  every reset value taken from each register's own section and cross-checked
  arithmetically (TDFREE `1200h` = Table 5-3's 4608 B at the TX_FIF_SZ = 5 default);
  (2) §3.11's SRST/PHY-reset completion times render as "2 s"/"100 s" in the PDF's OWN
  text layer (hexdump-verified: a symbol-font µ mis-mapped to ASCII s by the producer,
  not an extraction drop), contradicted by §5.3.13's clean "100us" and §3.11.4's own
  100 ms bound — the dossier pins only the cleanly stated figures (first drafted as
  "µs, confirmed by extraction", measured false, corrected before landing);
  (3) PHY ID2's model/revision nibbles are blank in the datasheet — only bits [15:10]
  pin (`REQ-D-NIC-PHY-ID`); (4) ADDRH/ADDRL carry Table 5-6 defaults AND §5.4.2/§5.4.3's
  "undefined until loaded" — both recorded, nothing pinned at reset
  (`REQ-D-NIC-MAC-ADDR`); (5) unlike the UART, FIFO occupancy at reset IS pinned empty
  here — by the INF registers' stated resets (`REQ-D-NIC-FIFO-INF`). The design brief's
  sharpest finding stands as the dossier's composition records: the guest-readable time
  sources (`REQ-D-NIC-TIME-SOURCES`), the wire-domain PHY link scene under replay
  (`REQ-D-NIC-PHY-LINK`), the pin tie-offs (`REQ-D-NIC-GPIO-PINS`) — all pre-wired to
  `.4`. Registration stays `.11`'s (all three units together).

- ID: `P5-BOARD.11` — **registration day: the three units register**
  Status: `done` (`2026-10-02`, `SEMULITH-P5-0011`)
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
  Result (`2026-10-02`): registration day landed as one coherent commit. The three
  units register in `materials/units.sexp` (`netboard-lab-v0` kind `board`/layer
  `board`; the two devices kind `device`/layer `device`), the schema edits landed as
  the sanctioned "(values …) edit the day a real unit needs one" (`schema/units.sexp`
  kind +board/+device; the shared layer taxonomy +device in both `units` and
  `category-needs` schemas). **The generator/gate generalization is route-keyed, one
  generator + one gate** (`gen_model_book.py` `unit_shape`/`shape_contracts` derive the
  shape from the DECLARATION — `board.sexp` present for the board, the vehicle route
  otherwise — never from a guess; `check_materials_bill.sh`'s COMPLETENESS half keys on
  the same function): the board's pinned-specifications fragment enumerates the
  composition pins from board.sexp, the device fragments carry the route-honest "no
  encoding space / no reference candidates" content, the internal-contracts census is
  per-shape (device: `expectations/` is the corpus; board: `board.sexp`+`DOSSIER.md`),
  and the two processor books' fragments regenerated byte-identical but for the
  embedded generator hash (measured: `diff` minus the Generator line — empty). New
  self-test arms pin both new shapes (MATERIALS-BILL 11/11: GREEN device, GREEN board,
  RED missing-section each). **The three books landed** under `docs/models/<unit-id>/`
  (devices: introduction/materials/gaps/methodology/evidence — no compiled-guest
  chapter, probes are `.5`'s; the board: the composition narrative as the method
  chapter, no evidence chapter until `.4` — deliberate). **The category-needs census**
  carries 72 rows (24 per unit): the devices' covered set (C01/C02/C10/C11/C14/C17/
  C19/C22/C23 + the NIC's C09 sequencing disciplines) names the pinned datasheets;
  the board's declared absences are `out-of-scope` WITH their contract reasons (never
  owed, not missing) and its composition categories `partial` (the device halves rest
  on the pinned datasheets; the composition is authored, gated definition data — no
  catalog material could evidence it, and `covered` demands one). **Measured and
  corrected at execution:** the BREADTH report is DERIVED (GATE-REPORT) — its "2
  registered units" prose was the generator's hardcoded string, fixed at the generator
  (the count now derives; the abstraction sentence keys on processor units) and the
  report regenerated (`5 registered units`, verdict still `passed`); the project book's
  `models.md` "Today two units exist" updated to five with the arc-adaptation note.
  FACT-OWNERSHIP gained the book-side mirrors (46 fact kinds). DERIVED-COUNTS fired on
  the self-test-arm total (341 → 345, re-derived by the enumerator, never incremented).
  The gates: UNIT-BOOKS 5/5 books build, MATERIALS-BILL 5/5 (every fragment matches,
  every section carries its does-not-supply), SCOPE-COVERAGE `5 unit(s) may code`,
  RECORD-SCHEMA 14 record files. The DEV_NOTES lesson: promotion: declined (derive-from-declaration already has its decision records — decision_device-applicability-by-declared-vehicle, decision_gate-applicability-by-declared-vehicle — and regenerate-vs-edit is a standing house rule).

## Current Frontier

| Order | Leaf | Status | Why next |
| --- | --- | --- | --- |
| 1 | `P5-BOARD.4` | `pending` | the gate's core obligation: the composition verdict — every CPU assumption matched against a board/device guarantee or rejected; the composed catalogues are on disk (`.3`), the devices' composition records (TIME-SOURCES/PHY-LINK/GPIO-PINS, the strap values) are pre-wired to it |

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
- `2026-10-02` (design brief for `.10`, recorded before its execution; sources: the pinned
  `MICROCHIP-LAN9118` artifact — sha256 `72fe68f2…91bf6ee` re-verified from the cache —
  read in full for the register contract: §1.10, §3.6–§3.13, chapter 5 whole, via
  `pdftotext -raw`; the `.2` hardened machinery; the board definition):
  **the NIC dossier needs NO machinery edit.** `.2`'s generalization by declaration
  (`decision_device-applicability-by-declared-vehicle` — `vehicle (route device-model)
  (comparison register-expectations)`) already covers the NIC: schemas, gates and
  `dossier_sexp.py` are device-shaped, and the auto-attaching gates (DOSSIER-SCHEMA,
  RECORD-SCHEMA, PROFILE-CONSISTENCY, EXTRACTION's device leg, EXERCISE-COVERAGE,
  INTERACTION-MATRIX) decide an unregistered device dossier fully. What `.10` adds is
  content plus the mechanical re-pins: FACT-OWNERSHIP registry +6 rows and self-test
  fixture re-pins (`__CHECKED__ 7→8`, `3→4` — the fixtures glob the real corpus), and the
  `profiles/` bound re-derives 4× → 5× by the standing arithmetic with a
  `decision_profiles-family-five-units` record. One measured extraction hazard, recorded:
  `pdftotext`'s `-layout` and `-raw` renderings DISAGREE on Table 5-1's Default column
  (the two-column page layout scrambles row pairing); every reset value in the dossier is
  therefore taken from each register's own §5.3.x/§5.4.x/§5.5.x section, with the
  whole-register arithmetic cross-checked (e.g. TX_FIFO_INF.TDFREE = 1200h = 4608 B =
  Table 5-3's TX data FIFO size at the TX_FIF_SZ = 5 default — the two independent
  statements agree).
  **The datasheet census (measured `2026-10-02`):**
  - *The register surface:* four host-accessible FIFOs (RX data, RX status, TX data, TX
    status — §5.2) behind aliased ports: RX data at 04h–1Ch (8 DWORD aliases,
    destructive reads only), TX data at 20h–3Ch (write-only), the status FIFOs at 40h/48h
    (destructive pops) with non-destructive PEEKs at 44h/4Ch; 24 named direct CSRs at
    50h–B4h; RESERVED slots at 60h, 94h and B8h–FCh (§5.1: reads "a random value can
    be returned", writes "may cause system failure"); 12 MAC CSRs indexed through
    MAC_CSR_CMD/DATA (A4h/A8h, Table 5-6); 13 PHY registers indexed one level deeper
    through MII_ACC/MII_DATA (PHY address 00001b, Table 5-8). The board's 256-byte
    window spans exactly the direct map (`D-BOARD-MEMORY-MAP`).
  - *Scope decision:* `profile.sexp`'s scope census counts the direct host-bus surface —
    4 FIFO port groups + 24 named CSRs = **28** — with the indexed MAC CSR and PHY
    spaces carried in `state.sexp` (MMIO-reachable state through one and two levels of
    indirection) and their own requirements. RESERVED slots are absences, covered by the
    off-map requirement, not scope members (the `.2` precedent: a Reserved field is a
    measured silence, not a register).
  - *The reset architecture:* five reset sources (Table 3-10: POR, nRESET, SRST,
    PHY_RST, PHY reg 0.15); the board's cold-only reset (`D-BOARD-RESET`) maps to
    POR/nRESET semantics — the full reset, NASR bits included. Stated resets are
    concrete: ID_REV = `0118_0001h`, BYTE_TEST = `87654321h`, INT_STS/INT_EN = 0,
    FIFO_INT = `48000000h`, RX_CFG/TX_CFG/RX_DP_CTL/PMT_CTRL/GPIO_CFG = 0,
    HW_CFG = `0005_0000` with bit 2 = the D32/nD16 **strap value** (RO — a board
    composition choice the datasheet deliberately does not pin), TX_FIFO_INF.TDFREE =
    `1200h`, GPT_CFG/GPT_CNT = `0000FFFFh`, WORD_SWAP = 0 (NASR), MAC_CR =
    `00040000h`, ADDRH = `0000FFFFh` / ADDRL = `FFFFFFFFh` "undefined until loaded
    from the EEPROM" (§5.4.2/§5.4.3), the remaining MAC CSRs = 0. Two measured
    post-reset transients: E2P_CMD.EPC_BSY reads 1 until the EEPROM auto-load attempt
    completes (§5.3.23's note), and "the LAN9118 must always be read at least once after
    power-up, reset, or upon return from a power-saving state or write operations will
    not function" (§5.3.9 and §5.3.13 notes).
  - *No EEPROM on this board* (`board.sexp` declares none): the auto-load finds no `A5h`
    marker at address 00h, so it ends initialization, "MAC Address Loaded" stays clear,
    and ADDRL/ADDRH are the host's to program (§3.9.1) — the datasheet's own defined
    path for an absent EEPROM, not a gap.
  - *The no-DMA shape confirmed:* §1.10 — programmed I/O only over an SRAM-like slave
    interface, 32-bit and 16-bit bus transfers, internally all 32-bit; every device effect
    reaches the guest through its own MMIO accesses, exactly the shape the CPU
    contract's eight assumptions tolerate (the `.1` brief). The interrupt pin is
    unconnected and declared so (`D-BOARD-NO-TIMER-IRQ`); INT_STS/INT_EN/IRQ_CFG stay
    MMIO-visible state — status bits set regardless of the unconnected pin (§5.3.4).
  **The sharpest measured finding — the NIC carries guest-readable TIME SOURCES, and
  the CPU contract excludes all of them.** FREE_RUN (9Ch) is a free-running 25 MHz
  32-bit counter, RO, that "will run regardless of the power management states D0, D1 or
  D2" (§5.3.18); GPT_CNT (90h) reads a 16-bit timer counting down at 100 µs resolution
  (§3.8); IRQ_CFG's INT_DEAS runs a 10 µs-granularity deassertion interval with an
  MMIO-visible status bit (§5.3.2). `OB-ENV-VIRTUAL-TIME` excludes every guest-reachable
  time source — no CSR counter AND no memory-mapped one — so a faithful wall-clock
  implementation of FREE_RUN/GPT_CNT would falsify the composition from INSIDE a
  device, exactly as a CLINT would from beside one (the `.1` brief's sharpest edge). The
  dossier records the datasheet facts as defined requirements AND records the tension as
  a high-risk requirement: the deterministic discipline that already pins RX delivery to
  the guest's own polling (the `.1` brief) extends to the counters — the model may not
  wire them to wall-clock, and the harness's retired-instruction count must never become
  target-visible through them; the exact frozen/deterministic disposition is `.4`'s
  composition verdict, pre-wired here so it cannot be missed. The board choice stands:
  the counters are disposable (a polled driver never needs them), their formats are
  datasheet-defined, and every alternative NIC carries the same class of state.
  **Contract id and prefixes:** contract `lan9118-v0` v0; record ids `REQ-D-NIC-*` /
  `D-NIC-*` / `OB-NIC-*` / `CHK-NIC-*-POS/-NEG` (the `.2` RECORD-SCHEMA prefix
  discipline: `D-X` ↔ `REQ-D-X` mechanically).
  **Expected results (C19), three documents mirroring `.2`'s shape:** cold-reset register
  reads (the stated resets above, with the HW_CFG strap bit and the EPC_BSY transient
  recorded under the datasheet's own conditions); the TX-FIFO free-space accounting
  (§3.12.5's usage rules give exact TDFREE arithmetic with TX_ON = 0 — no wire needed);
  the RX replay path (a recorded frame's RX status word format, §3.13.3, and the FIFO
  port pop/PEEK semantics, §5.2). A value pins only where the datasheet determines it.
  **Not `.10`'s scope:** the device model (Rust) — the dossier is the documents the model
  route consumes; registration stays `.11`'s (one registration day, all three units).
- `2026-10-02` (design brief for `.11`, recorded before its execution; sources: the `.2`
  routing note, the machinery census below measured this day against the live scripts and
  schemas):
  **Registration day's design, decided.** The three units register together in
  `materials/units.sexp`: `netboard-lab-v0` (kind `board`, layer `board`),
  `sifive-uart-lab-v0` and `lan9118-lab-v0` (kind `device`, layer `device`).
  **Schema edits** (each the sanctioned "(values …) edit the day a real unit needs one",
  each fired before landing): `schema/units.sexp` `kind` admits only `processor` — gains
  `board` and `device`; its `layer` (and `schema/category-needs.sexp`'s, the shared
  taxonomy) gains `device` — a device is not the board layer; it is the board's
  constituent, and the dossier family's measured unit kinds are now three.
  **The generator generalization, measured in detail** (`scripts/gen_model_book.py`):
  the `.2` routing note named the two `sibling-crate` conditionals (~:136, ~:212-213) and
  the processor-shaped INTERNAL_CONTRACTS census; the full read measures MORE: the
  emitters load `references.sexp` (absent from both device dossiers AND the board — the
  board dossier is `board.sexp` + `DOSSIER.md`, with no `profile.sexp` at all, so
  `_vehicle_route` reads None there), and `emit_contracts` reads `interactions.sexp`,
  globs `guests/`, and reports "declared instruction forms" — all processor-shaped.
  The gate side needs the same: MATERIALS-BILL's COMPLETENESS half loads
  `references.sexp` per unit and would report CANNOT JUDGE for all three new units.
  **The adaptation is route-keyed, one generator + one gate:** the unit's shape derives
  from its DECLARATION (vehicle route `device-model` for the devices; `board.sexp`
  present for the board — never from a guess), the INTERNAL_CONTRACTS census becomes
  per-route (device: profile/state/requirements/contract-obligations/`expectations/`;
  board: `board.sexp` + `DOSSIER.md`), the four fragment names stay uniform with
  route-honest content (a device's encoding-tables.md: "no encoding space — a device has
  no instruction encodings; its register map is the contract"; reference-models.md: "no
  reference candidates pinned — the evidence shape is datasheet-derived register-read
  expectations"), and the gate's required-material enumeration follows the same route
  key. New self-test arms pin the device and board shapes GREEN (a route the generator
  cannot emit stays a refusal).
  **The books** (`docs/models/<unit-id>/`, UNIT-BOOKS — presence + build + reverse
  registration are the gate; the chapter arc is MODEL-BOOKS' authorship convention,
  adapted honestly per kind): the device books carry introduction / the materials bill /
  the gaps chapter / the methodology (the device route: datasheet → dossier → the model
  route) / the evidence chapter (the expectations route — no compiled-guest chapter: a
  device has no guest corpus, and probes are `.5`'s); the board book carries
  introduction / the materials bill / gaps / the composition narrative (the board's
  method IS composition) — evidence lands with `.4`'s verdict. Prose dominates; the
  teaching test applies (MODEL-BOOKS' standing criteria 4–6).
  **category-needs rows** (SCOPE-COVERAGE refuses a required category with no row;
  LAYERS refuses a reasonless `missing`; the dsp56300 precedent carries a full census
  per unit): each device unit declares `requires` for the categories its dossier
  demonstrably carries — C02 (state census), C19 (device register semantics), C22 (the
  measured silences ARE C22 records), C23 (the pinned-source provenance) — each
  dispositioned `covered` against the datasheet material at layer `device`, with C21
  (the wire/backends) dispositioned against the board's declared backend data and the
  rest `out-of-scope`; the board unit's rows disposition the board-layer categories the
  board definition actually carries (C19 covered by board.sexp's pins, C17/C14 the
  declared absences with their reasons — the absences are the design's sharpest edge,
  recorded as data, never silent). Exact row sets measured at execution against the
  live census file.
  **FACT-OWNERSHIP**: registration adds the book-side mirrors to the units' rows (the
  dsp56300 pattern: `pinned-sources` mirrors the generated `pinned-specifications.md`,
  `internal-contracts` row per unit) — the fixture re-pins follow the measured corpus.
  **The BREADTH-report prose** (docs/BREADTH-REPORT.md) and any "every registered unit"
  phrasing elsewhere get re-read against the five-unit registry and corrected where
  measured stale — drift correction is part of registration day, per `.1`'s census.
  **Not `.11`'s scope:** the composition verdict (`.4`), generated maps (`.3`), probes
  (`.5`) — registration makes the units reviewable; it does not advance their evidence.
- `2026-10-02` (design brief for `.3`, recorded before its execution; sources: the `.1`
  machinery census naming `.3` the owner of `compose_units.py`'s tracked-board freshness
  gate, the DOSSIER's status row, and the probes measured this day against the live
  gates):
  **The scope, censused.** `.3` carries three obligations: (1) the address maps, wiring
  and hardware-description data GENERATED from `profiles/netboard-lab-v0/board.sexp`
  (the leaf goal, OWN-05); (2) the freshness proof for a TRACKED board —
  `compose_units.py`'s docstring defers it explicitly to the first tracked board
  ("manifest → derived bytes, the gen_fragments precedent"); (3) the acceptance: no
  handwritten duplicate map anywhere — measured: exactly ONE exists, the DOSSIER.md
  memory-map table (3 rows). The addresses elsewhere are dated narrative (DEV_NOTES,
  the knowledge card, the plan chapter's leaf reports) citing `D-BOARD-MEMORY-MAP`,
  never a second map.
  **Measured pre-conditions (this day; probe removed after measurement, tree clean
  before this brief).** A probe manifest composing the three real parts through
  `compose_units.py` succeeds: 99 requirements, 107 obligations, 5 sources, the
  encoding derived from rv64i-lab-v0. With the derived catalogues placed in
  `profiles/netboard-lab-v0/` (the compose docstring's own shape: "the ordinary gates
  cover it wherever it lives because it is ordinary corpus"), every profile-glob gate
  ran GREEN unchanged: RECORD-SCHEMA (14 → 16 record files), DOSSIER-SCHEMA (83),
  UNIT-COMPOSITION, PROFILE-CONSISTENCY, EXTRACTION, EXERCISE-COVERAGE,
  INTERACTION-MATRIX, SEMANTICS, GATE-REPORT, MATERIALS-BILL, SCOPE-COVERAGE,
  UNIT-BOOKS. **The one gate that fires is FACT-OWNERSHIP, exactly as designed:** the
  merged corpus adds two restatement pairs the registry does not name — the same-unit
  pair `netboard contract-obligations ← netboard requirements` and the cross-family
  restater `netboard encoding.sexp ← definitions/`. Registration, not weakening, is
  the fix (below).
  **The design, decided.**
  1. **`scripts/gen_board.py` — the one generator.** Boards are discovered BY
     DECLARATION (`profiles/*/board.sexp` glob — the `unit_shape` idiom, never a
     hardcoded id). Per board, from board.sexp alone: `composition.sexp` (the manifest —
     the part list derived from the processor + device unit pins, never a handwritten
     duplicate of them); the four composed catalogues (`requirements` /
     `contract-obligations` / `sources` / `encoding`) materialized by
     `compose_units.compose` — the ONE code path, imported, never re-implemented —
     into the board's own directory; `hardware.sexp` (the hardware description: every
     region resolved to machine integers with its computed end; the wiring — device ↔
     region ↔ access-widths ↔ interrupt-state ↔ backend; the serial console; the
     reset; the declared absences with their `satisfies` edges); and `map.md` (the
     human-readable map, hex-rendered). Every generated artifact carries the OWN-03
     fingerprint header (canonical-input sha256 + generator sha256); `--check`
     re-derives in memory and refuses drift, naming the artifact. The generator
     REFUSES, by name: a region overlap; an MMIO region naming no device (or a device
     no region); a device region that does not contain its device unit's declared
     register surface (the offsets in the unit's `state.sexp`, measured at execution)
     — a wiring inconsistency is a refusal, never a generated map with a hole.
  2. **`schema/hardware.sexp`** — the generated artifact's contract (DOSSIER-SCHEMA
     then validates it by basename; the consumers — `.4`'s verdict, the model route,
     P6's boot contract — read a shape with a governor). It is NOT P6's device tree:
     P6 pins its own hardware-description format; this is the board's internal
     generated data.
  3. **`scripts/check_board_gen.sh` — the `BOARD-GEN` doctrine.** The freshness proof
     the compose docstring defers: re-derive every artifact and byte-compare, with a
     `--self-test` whose RED arms assert the reason (a hand-edited hardware.sexp; a
     hand-edited composed catalogue; a board.sexp edit leaving stale artifacts; a
     hand-edited manifest), registered in `scripts/check_doctrines.project.sh` and
     mirrored in `DOCTRINE_ENFORCEMENT.md` + `docs/book/src/working/doctrines.md`
     (REGISTRY-MIRROR).
  4. **The one handwritten duplicate map dies.** DOSSIER.md's memory-map table is
     replaced by a link to the generated `map.md` (the acceptance: no handwritten
     duplicate map anywhere); the board book gains the generated map as a chapter
     including the ONE generated file (mdBook `{{#include}}`, UNIT-BOOKS verifies the
     build) — one owner, two readers.
  5. **FACT-OWNERSHIP registrations** (the measured pairs, plus the derivation rows):
     `obligations (netboard-lab-v0)` (owner the merged requirements, mirror the merged
     obligations, RECORD-SCHEMA — the per-unit idiom); `encodings (netboard-lab-v0)`
     (owner `definitions/riscv/`, mirror the merged encoding, BOARD-GEN); the composed
     catalogues and the generated map/hardware rows with owner `board.sexp`, governor
     BOARD-GEN. The self-test fixture re-pins to five units (`__CHECKED__ 8→9`, the
     GREEN fixture registry gains the netboard row, the comment extended) — the re-pin
     lineage (two→three at `.2`, three→four at `.10`) continues to four→five.
  6. **The DOSSIER's stale status rows, logged as a defect.** The dossier-status table
     still reads "device unit dossiers: absent, owned" and "registration: deferred,
     owned" — both landed (`.2`/`.10`/`.11`) and the table was not re-read on
     registration day. Logged here (§15: finding it creates the obligation); fixed
     with this leaf, the composition-manifest row flipping to present at the same time.
  7. **The mechanical re-derivations:** DERIVED-COUNTS (doctrine count and
     self-test-arm total, re-derived by the enumerator, never incremented); the
     KNOWLEDGE-MAP regenerated; `docs/book/src/plan/p5-p7.md` gains the `.3` section;
     `models.md` and `LIVE_STATUS.md` re-read against the new surface.
  **Not `.3`'s scope:** the composition verdict (`.4` — the composed catalogues on disk
  are its input, pre-staged here), the device models in Rust (the model route),
  firmware probes (`.5`), the capability manifest (`.6`), P6's pinned boot
  hardware-description. `gen_model_book.py`'s `BOARD_CONTRACTS` census stays
  `board.sexp + DOSSIER.md`: the census enumerates the dossier's AUTHORED contracts;
  the generated set is governed by BOARD-GEN and reviewed in the book's map chapter,
  not billed as materials.

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

`P5-BOARD.3` (`2026-10-02`, `SEMULITH-P5-0013`):

- [x] **REPRODUCE / ISSUE** — the board definition existed, but every map downstream of
  it was prose, and the freshness proof was unowned: `profiles/netboard-lab-v0/`
  held only `board.sexp` + `DOSSIER.md`, the DOSSIER carried a handwritten map table
  (the leaf acceptance's one duplicate), and `compose_units.py`'s docstring deferred
  the tracked-board freshness gate to this leaf. Measured pre-conditions:

  ```
  $ ls profiles/netboard-lab-v0/
  DOSSIER.md	board.sexp
  $ python3 scripts/compose_units.py target/board-probe/manifest.sexp target/board-probe/out
  composed unit 'netboard-lab-v0': 99 requirement(s), 107 obligation(s), 5 source(s); encoding derived from …/profiles/rv64i-lab-v0
  $ bash scripts/check_fact_ownership.sh   # with the probe catalogues in place
  FACT-OWNERSHIP: REFUSED — the check does not discriminate (self-test failed).
  # → the two new corpus restatement pairs, exactly as the gate is designed to catch
  ```

- [x] **ROOT CAUSE (WHY + WHERE)** — OWN-05 requires the maps generated from the one
  definition; no generator consumed board.sexp, so the map existed only as prose
  (which drifts) and the composition manifest/catalogues existed only in scratch.
  WHY the fixture re-pin and not a gate edit: the merged corpus's two new
  restatement pairs are genuine restatements — registration, never weakening. WHERE:
  `scripts/gen_board.py` + `schema/hardware.sexp` + `scripts/check_board_gen.sh`
  (new); `scripts/compose_units.py` (`compose_resolved` factorization);
  `doctrine/fact_ownership.tsv` (+8 rows); `scripts/check_fact_ownership.sh`
  (fixture re-pin); `profiles/netboard-lab-v0/DOSSIER.md` (the duplicate table);
  `docs/models/netboard-lab-v0/` (the map chapter); the doctrine mirrors.
- [x] **FIX** — the generator (boards discovered by declaration; seven artifacts;
  consistency refusals named), the schema, the BOARD-GEN doctrine (self-test 9/9,
  every RED arm asserting the reason), the factorized one-code-path compose (probe
  byte-identical to the pre-refactor output), the generated corpus in place, the
  DOSSIER's table replaced by the generated map, the FACT-OWNERSHIP rows, the
  mirrors. The stale DOSSIER status rows (the brief's logged defect) fixed in the
  same pass.
- [x] **ADDRESSED (verified)** — the acceptance: no handwritten duplicate map, and
  every generated artifact fingerprinted with drift gated:

  ```
  $ python3 scripts/gen_board.py
  …/profiles/netboard-lab-v0: 7 artifact(s) generated from …/board.sexp
  $ bash scripts/check_board_gen.sh
  BOARD-GEN: ok (1 board(s) — manifest, composed catalogues, hardware description and map all byte-exact functions of the canonical definition)
  $ bash scripts/check_board_gen.sh --self-test
  BOARD-GEN --self-test: 9 pass / 0 fail
  $ python3 scripts/check_sexp_schema.py profiles/netboard-lab-v0/hardware.sexp schema/hardware.sexp
  check_sexp_schema: ok — profiles/netboard-lab-v0/hardware.sexp conforms to hardware.sexp
  $ grep -c "0x1001_0000" docs/models/netboard-lab-v0/book/the-map.html
  1          # the book chapter includes the ONE generated map — verified in the built HTML
  $ grep -c "^| \`ram0\`" profiles/netboard-lab-v0/DOSSIER.md
  0          # the handwritten duplicate table is gone
  $ bash scripts/check_fact_ownership.sh
  FACT-OWNERSHIP: ok (54 fact kind(s): one owner each, every mirror governed)
  $ bash scripts/check_requirements.sh
  RECORD-SCHEMA: ok (16 record file(s) validate and agree with their profile; …)
  ```

- [x] **NO REGRESSION** — the composed corpus is ordinary corpus under the unchanged
  gates (DOSSIER-SCHEMA 83 files, UNIT-COMPOSITION, PROFILE-CONSISTENCY, EXTRACTION,
  EXERCISE-COVERAGE, INTERACTION-MATRIX, SEMANTICS, GATE-REPORT, MATERIALS-BILL,
  SCOPE-COVERAGE all green with it in place — measured before landing);
  `compose_units --self-test` 9/9 after the factorization; `make gate` →
  `=== all doctrines green ===` (DERIVED-COUNTS after the enumerator re-derived
  31→32 doctrines and 345→354 arms in `LIVE_STATUS.md`); `mdbook build docs/book`
  rc 0; all 5 unit books build (UNIT-BOOKS); `gen_book_index.py --check` rc 0.
  No Rust surface touched.
- [x] **LOCKSTEP** — tree (leaf + frontier + checklist + logs), `MEMORY.md` (next
  action `.4`), `CHANGELOG.md`, `DEV_NOTES.md` (the offset-format finding; promotion
  declined — the by-declaration measurement discipline has its decision records),
  `LIVE_STATUS.md` (P5 row + re-derived counts), `docs/TASK_TREE.md`,
  `doctrine/fact_ownership.tsv`, the doctrine mirrors (`DOCTRINE_ENFORCEMENT.md` +
  `docs/book/src/working/doctrines.md`), `profiles/netboard-lab-v0/DOSSIER.md`,
  the board book (the map chapter, gaps), mdBook `plan/p5-p7.md` (the `.3` section),
  KNOWLEDGE_MAP regenerated.

`P5-BOARD.11` (`2026-10-02`, `SEMULITH-P5-0011`):

- [x] **REPRODUCE / ISSUE** — three gated dossiers existed unregistered:
  `materials/units.sexp` held two units, `schema/units.sexp`'s `kind` admitted only
  `processor`, and the registration-day gates could not have passed — measured:
  `grep -c "^(unit " materials/units.sexp` → 2; `gen_model_book.py --check --unit
  sifive-uart-lab-v0` → REFUSED (no `references.sexp`); MATERIALS-BILL's COMPLETENESS
  loaded `references.sexp` per unit (CANNOT JUDGE for all three new dossiers).
- [x] **ROOT CAUSE (WHY + WHERE)** — the registry machinery was processor-shaped by
  construction ("nothing is pre-built for kinds that have never been exercised" —
  MODEL-METHOD.2), so registration day is the day the kinds are exercised. WHERE,
  censused at the design brief and verified in execution: the two schema value lists
  (`schema/units.sexp` kind + layer, `schema/category-needs.sexp` layer), the one
  generator (`scripts/gen_model_book.py` — `unit_shape`/`shape_contracts` + the
  route-keyed emitters), the one gate (`scripts/check_materials_bill.sh` —
  COMPLETENESS keyed on the same shape function), the registry + census
  (`materials/units.sexp`, `materials/category-needs.sexp`), the three books
  (`docs/models/<unit-id>/`), the FACT-OWNERSHIP book-side mirrors, and the derived
  prose (BREADTH-REPORT via its generator; `docs/book/src/models.md`).
- [x] **FIX** — the schema edits, the route-keyed generator + gate (shape derived from
  the DECLARATION, never a guess; an undeclared absence stays a refusal), the three
  registrations, 72 census rows, the three authored books with generated fragments,
  the mirror rows, the generator-side BREADTH fix + regeneration, the models.md
  update.
- [x] **ADDRESSED (verified)** — the acceptance's four gates over five units:

  ```
  $ bash scripts/check_unit_books.sh
  UNIT-BOOKS: ok (5 unit(s) — every registered unit has its book, and every book builds)
  $ bash scripts/check_materials_bill.sh
  MATERIALS-BILL: ok (5 unit(s) — generated tables match the pinned data; every material states what it does not supply)
  $ bash scripts/check_scope_coverage.sh
  SCOPE-COVERAGE: ok (5 unit(s) may code — every required category covered)
  $ bash scripts/check_requirements.sh
  RECORD-SCHEMA: ok (14 record file(s) validate and agree with their profile; …)
  $ bash scripts/check_materials_bill.sh --self-test
  MATERIALS-BILL --self-test: 11 pass / 0 fail
  ```

  No regression on the processor shapes: the two processor books' regenerated
  fragments differ from their committed predecessors ONLY in the embedded generator
  hash (measured: `diff` with the Generator line filtered — empty for all four
  fragments); the BREADTH verdict stays `passed` with the counts derived
  (`GATE-REPORT: ok (4 generated report(s) in sync with their inputs)`).
- [x] **NO REGRESSION** — `make gate` → `=== all doctrines green ===` (including
  DERIVED-COUNTS after the arm total was re-derived 341 → 345 by the enumerator);
  `mdbook build docs/book` rc 0; `gen_book_index.py --check` rc 0; each new unit book
  `mdbook build` rc 0 (UNIT-BOOKS builds them). No Rust surface touched.
- [x] **LOCKSTEP** — tree (leaf + frontier + checklist + logs), `MEMORY.md` (next
  action), `CHANGELOG.md`, `DEV_NOTES.md` (lesson declined — the derive-from-
  declaration pattern already has its decision record), `LIVE_STATUS.md` (P5 row +
  the arm total), `docs/TASK_TREE.md`, KNOWLEDGE_MAP regenerated, mdBook
  `models.md` + regenerated index; `docs/BREADTH-REPORT.md` via its generator.

`P5-BOARD.10` (`2026-10-02`, `SEMULITH-P5-0009`):

- [x] **REPRODUCE / ISSUE** — the board's second device had no dossier: `board.sexp`
  declared the unit id `lan9118-lab-v0` with `.10` as its owner (named `.2` at `.1`,
  renumbered at the `.2` split), and no `profiles/lan9118-lab-v0/` existed. Measured
  pre-conditions the leaf changed: `git ls-files profiles/` counted four unit
  directories; the FACT-OWNERSHIP fixtures globbed three; `readme_routes.tsv`'s
  per-part bound stood at 32,768 — below the NIC dossier's measured file sizes.
- [x] **ROOT CAUSE (WHY + WHERE)** — the dossier is the contract the model route
  consumes; without it the NIC is a name in a board definition. WHY no machinery edit:
  measured at the design brief — the gates attach by glob and derive device
  applicability from the `vehicle` declaration (`.2`'s generalization), so content plus
  mechanical re-pins is the whole leaf. WHERE the content came from: the pinned
  artifact read in full for the register contract, with the two measured extraction
  hazards handled at root (the Table 5-1 default-column disagreement → per-register
  sections are the authority; the §3.11 µ-glyph defect → verified against the PDF's own
  text-layer bytes, only cleanly stated figures pinned):

  ```
  $ pdftotext -raw .materials/network/lan9118.pdf target/lan9118-raw.txt && wc -l target/lan9118-raw.txt
  4906 target/lan9118-raw.txt
  $ grep -c "87654321" target/lan9118.txt && grep -c "87654321" target/lan9118-raw.txt
  2   # -layout: one in the text AND one MISPAIRED in Table 5-1's default column
  2   # -raw: the same two — but the two modes pair the defaults to different registers
  $ pdftotext -f 32 -l 32 -raw .materials/network/lan9118.pdf - | grep -a "approximately 2" | hexdump -C | head -1
  00000000  61 70 70 72 6f 78 69 6d  61 74 65 6c 79 20 32 20  |approximately 2 |
  # … 20 73 — a plain ASCII 's': the µ mis-mapping is the producer's text layer,
  # not the extractor (§5.3.13's clean "100us" for the same PHY reset confirms it)
  ```

- [x] **FIX** — the 9-file dossier under `profiles/lan9118-lab-v0/` (every fact read
  against the digest-verified pinned PDF, `sha256 72fe68f2…91bf6ee` re-derived from the
  cache); the obligation/decision mirrors GENERATED from requirements.sexp
  (`target/gen_nic_mirrors.py` — drift impossible by construction, refused by gate
  regardless); 6 FACT-OWNERSHIP registry rows; the self-test fixture re-pins; the
  `profiles/` 5× re-derivation with the first per-part raise, recorded in
  `decision_profiles-family-five-units.md` (+ INDEX).
- [x] **ADDRESSED (verified)** — every dossier document validates, and the device unit
  is decided by declaration:

  ```
  $ for each dossier .sexp: python3 scripts/check_sexp_schema.py <file> schema/<basename>.sexp
  check_sexp_schema: ok — all 6 dossier documents + 3 expectation documents conform
  $ python3 scripts/check_extraction.py profiles/lan9118-lab-v0
  device-model route declared (28 scope registers; resets everywhere; obligations checked both ways)
  $ bash scripts/check_requirements.sh
  RECORD-SCHEMA: ok (14 record file(s) validate and agree with their profile; …)
  $ bash scripts/check_fact_ownership.sh
  FACT-OWNERSHIP: ok (43 fact kind(s): one owner each, every mirror governed)
  $ shasum -a 256 .materials/network/lan9118.pdf
  72fe68f241b5bc91a861cff98a877ae907339d396e64394b0f5daa2c391bf6ee  .materials/network/lan9118.pdf
  ```

  The cross-checks hold (CITED/MIRROR/COVERAGE/AUTHORITY green over the 52/52/52
  requirement/obligation/decision mirrors); PROFILE-CONSISTENCY `4 profile dossier(s)
  internally consistent`; EXERCISE-COVERAGE and INTERACTION-MATRIX derive the
  device-model route for the fifth unit after staging (git-mode discovery). The
  measured findings fixed in execution (the Table 5-1 extraction hazard, the §3.11
  text-layer defect, the blank PHY ID2 nibbles, the ADDRH/ADDRL tension, the pinned
  FIFO occupancy) are recorded with the leaf.
- [x] **NO REGRESSION** — every edited check's self-test passes inside its gate run
  (FACT-OWNERSHIP refuses to judge when its self-test fails — it judged); the corpus
  re-validates (DOSSIER-SCHEMA 75 files ok, 2 declared skips); `make gate` →
  `=== all doctrines green ===`; `mdbook build docs/book` rc 0;
  `gen_book_index.py --check` rc 0. No Rust surface touched.
- [x] **LOCKSTEP** — tree (leaf + frontier + checklist + logs), `MEMORY.md` (next action
  `.11`), `CHANGELOG.md`, `DEV_NOTES.md` (the extraction-hazard lesson PROMOTED to
  `docs/knowledge/a-pdf-text-layer-is-not-the-page.md` + INDEX), `LIVE_STATUS.md` (P5
  row), `docs/TASK_TREE.md`, `docs/decisions/INDEX.md` (+1 record), KNOWLEDGE_MAP
  regenerated, mdBook `plan/p5-p7.md` (the second device-dossier section).

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
| `2026-10-02` | `.3` | `gen_board.py` → 7 artifacts; BOARD-GEN `1 board(s) … byte-exact` (self-test 9/9, REDs: hand-edited hardware/catalogue/manifest, moved definition, overlap, ghost device); `check_sexp_schema.py` ok on hardware.sexp and composition.sexp; RECORD-SCHEMA `16 record file(s)`; FACT-OWNERSHIP `54 fact kind(s)` (self-test 10/10, fixture re-pinned 9); DOSSIER-SCHEMA 83 files; UNIT-BOOKS 5/5 (the map include verified in the built HTML); DERIVED-COUNTS re-derived 31→32 doctrines, 345→354 arms; `make gate` green; `mdbook build` rc 0; `gen_book_index.py --check` rc 0 | the maps are generated and drift-gated: one generator, seven artifacts, the BOARD-GEN freshness proof the compose docstring deferred; the one handwritten duplicate map replaced; the composed catalogues pre-staged as `.4`'s input |
| `2026-10-02` | `.11` | pre-fix generator re-run from `de46377` → `REFUSED — references.sexp: the pinned document is missing` (the measured pre-condition); UNIT-BOOKS `5 unit(s)`; MATERIALS-BILL `5 unit(s)` (self-test 11/0 with the new device/board arms); SCOPE-COVERAGE `5 unit(s) may code`; RECORD-SCHEMA 14 files; GATE-REPORT `4 generated report(s) in sync`; DERIVED-COUNTS arm total re-derived 341→345; `make gate` green; all 5 unit books + the project book build; `gen_book_index.py --check` rc 0 | registration day landed as one coherent day: three units registered (kind board/device, layer +device), the generator + gate route-keyed by declaration, three books authored, 72 census rows, the BREADTH prose fixed at its generator |
| `2026-10-02` | `.10` | `check_sexp_schema.py` ok on all 6 dossier .sexp files + 3 expectation documents; EXTRACTION `device-model route declared (28 scope registers; resets everywhere; obligations checked both ways)`; RECORD-SCHEMA `14 record file(s)`; PROFILE-CONSISTENCY `4 profile dossier(s)`; FACT-OWNERSHIP `43 fact kind(s)` (self-test re-pinned 8/4); `make gate` green; `mdbook build` rc 0; `gen_book_index.py --check` rc 0 | the second device dossier landed fully gated with NO machinery edit; the `profiles/` per-part bound bit for the first time (32→64 KiB, recorded); the §3.11 text-layer defect and the Table 5-1 extraction hazard measured and handled; the time-source/link-scene/pin-tie-off composition tensions pre-wired to `.4` |
| `2026-10-02` | `.2` | `check_sexp_schema.py` ok on all 7 dossier .sexp files; EXTRACTION `3 unit(s) sufficient`; EXERCISE-COVERAGE `3 profile(s)`; INTERACTION-MATRIX `device-model route declared … 0 cells`; PROFILE-CONSISTENCY `3 profile dossier(s)`; self-tests: 17/0, 9/0, 14/0, 41/0, 7/0, 14/0, 10/0; `check_fact_ownership.sh` ok (37 fact kinds); `make gate` green; `mdbook build` rc 0; `gen_book_index.py --check` rc 0 | the first device dossier landed fully gated; the machinery generalized by declaration (`device-model`/`register-expectations`); the watermark mode gap measured and recorded (`REQ-D-UART-WM-MODE`); registration routed to `.11` |
| `2026-10-02` | `.1` | `check_sexp_schema.py` (definition vs `schema/board.sexp`; the schema vs `schema/schema.sexp`) → ok; every pin re-derived from its source (GC-REPORT digest, the two catalog sha256s, the FU540/LAN9118 PDFs, the harness DEFAULT_BASE/SIZE); the 16550 census: 0 occurrences in the pinned FU540 v1p5; `make gate` green; `mdbook build docs/book` rc 0 | `netboard-lab-v0` specified: the canonical board definition pins versions, not names; the two absences declared as data with their obligations; the 16550 defect corrected at its records; registration routed to `.3` |
| `2026-10-01` | `.9` | `build_responses.py --report` → 5 fulfilled / 5 blocked, exit 0; `materials.py --fetch` → all five sha256-verified into `.materials/network/`; `materials.py --verify` → 52/0; corpus census at `c4ad8a2` (5696/293); `make gate` green | the ten answers reconciled: five materials adopted, ten requests marked (5 resolved / 5 measured-negative blocked); the knowledge cards carry the ask→answer loop |
| `2026-10-01` | `.8` | `sexp.read_file` → 10 forms (the one reader); `poll_semulith_gaps.py` read-only → NEW REQUESTS (10), rc 1; `make gate` green | ten acquisition requests filed and seen by the channel; the filing mechanics recorded semulith-side (knowledge card) |

## Commit Log

| Leaf | Commit subject or reference | Notes |
| --- | --- | --- |
| `.3` | `SEMULITH-P5-0013 (leaf P5-BOARD.3): the generated maps — one generator, seven artifacts, the BOARD-GEN freshness gate; the duplicate map measured and replaced` | gen_board.py (boards discovered by declaration) emits the manifest, 4 composed catalogues (compose_units.compose_resolved — one code path), hardware.sexp (new schema) and map.md; BOARD-GEN registered (self-test 9/9); FACT-OWNERSHIP +8 rows (54 kinds), fixture re-pinned to five units; the DOSSIER's duplicate table and stale status rows fixed; DERIVED-COUNTS re-derived (32 doctrines, 354 arms) |
| `.11` | `SEMULITH-P5-0011 (leaf P5-BOARD.11): registration day — the three units register; the materials-bill machinery goes route-keyed by declaration` | schema/units.sexp kind +board/+device, layer +device (shared taxonomy); gen_model_book.py unit_shape/shape_contracts + route-keyed emitters; check_materials_bill.sh COMPLETENESS keyed on the same shape (+4 self-test arms); 3 registrations, 72 census rows, 3 books (authored chapters + generated fragments), FACT-OWNERSHIP book-side mirrors (46 kinds); BREADTH prose fixed at the generator and regenerated (5 units, verdict passed) |
| — | `SEMULITH-P5-0010 (tree P5-BOARD)` | the `.11` design brief: registration day's design decided; the generator generalization measured in full (references.sexp absent from all three new dossiers; MATERIALS-BILL's COMPLETENESS would CANNOT JUDGE) |
| `.10` | `SEMULITH-P5-0009 (leaf P5-BOARD.10): the second device dossier — lan9118-lab-v0 fully gated with no machinery edit; the per-part bound bites; the time sources found` | 9 dossier files (52/52/52 mirrored records, 3 expectation documents); FACT-OWNERSHIP re-pinned to four units; profiles/ bound re-derived 5× with the first per-part raise (32→64 KiB); the §3.11 text-layer defect measured (hexdump) and only cleanly stated figures pinned |
| — | `SEMULITH-P5-0008 (tree P5-BOARD)` | the `.10` design brief: the datasheet census, the scope decision (28 direct registers), no machinery edit, the guest-readable time sources finding |
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
- `2026-10-02`: the `.10` design brief recorded (`SEMULITH-P5-0008`). The pinned LAN9118
  artifact read in full for the register contract: no machinery edit needed (`.2`'s
  generalization by declaration covers the NIC); the census measured — 4 FIFO port
  groups + 24 direct CSRs + 12 indexed MAC CSRs + 13 PHY registers, five reset sources,
  the stated resets cross-checked per-register after the two `pdftotext` modes were
  caught disagreeing on Table 5-1's default column, the no-EEPROM auto-load path, the
  PIO-only shape confirmed. The sharpest finding: the NIC carries guest-readable time
  sources (FREE_RUN, GPT_CNT, INT_DEAS) that `OB-ENV-VIRTUAL-TIME` excludes — recorded
  as a high-risk requirement pre-wiring `.4`'s composition verdict. Scope decision: 28
  direct host-bus registers. Frontier: `.10` execution — the LAN9118 dossier lands.
- `2026-10-02`: `.10` done (`SEMULITH-P5-0009`) — the second device dossier landed, fully
  gated, with NO machinery edit (`.2`'s by-declaration generalization covered the NIC).
  `profiles/lan9118-lab-v0/` carries 9 documents: the DS00002266B-pinned source
  (digest re-verified), 52 requirements (46 defined + the reserved/unspecified/
  implementation-defined silences and deferrals), 52 mirrored obligations (contract
  `lan9118-v0` v0), the state document (49 registers across three indexing levels + 4
  FIFO families + the earned census — the TX command-parser state and the 16-bit
  pairing latch join the registers and FIFOs), 52 mechanically generated decision
  mirrors, and 3 datasheet-derived expectation documents. Measured in execution and
  recorded at root: the `pdftotext` Table 5-1 default-column disagreement (per-register
  sections are the authority), the PDF's own text layer mis-mapping §3.11's µ (hexdump-
  verified; only cleanly stated figures pinned), the blank PHY ID2 nibbles, the
  ADDRH/ADDRL defaults-vs-undefined tension, FIFO occupancy pinned empty by the INF
  resets (the UART contrast). The `profiles/` per-part bound bit for the first time —
  32→64 KiB, reviewed and recorded (`decision_profiles-family-five-units`);
  FACT-OWNERSHIP re-pinned to four units. Frontier: `.11` — registration day.
- `2026-10-02`: the `.11` design brief recorded (`SEMULITH-P5-0010`). Registration day's
  design decided: the three units register together (`netboard-lab-v0` board/board, the
  two devices device/device); the schema edits measured (`schema/units.sexp` kind
  +board/+device, the shared layer taxonomy +device); the generator generalization
  measured in FULL against the live code — beyond the `.2` routing note's two
  conditionals, the emitters load `references.sexp` (absent from all three new dossiers)
  and `emit_contracts` reads `interactions.sexp`/`guests/`/instruction-form prose, and
  MATERIALS-BILL's COMPLETENESS half would report CANNOT JUDGE — so the adaptation is
  route-keyed in ONE generator and ONE gate, with honest per-route fragment content and
  new GREEN self-test arms; the books' arc adapts per kind (no compiled-guest chapter
  for devices; the board's method chapter is composition); category-needs rows follow
  the dsp56300 full-census precedent with the devices' covered set measured (C02/C19/
  C22/C23 covered by the datasheets at layer device, C21 against the board's backend
  declaration); FACT-OWNERSHIP gains the book-side mirrors; stale "every registered
  unit" prose is re-read and corrected. Frontier: `.11` execution — the registrations,
  the books, the gates.
- `2026-10-02`: `.11` done (`SEMULITH-P5-0011`) — registration day, one coherent commit.
  The three units register (`netboard-lab-v0` board/board; the devices device/device —
  `schema/units.sexp` kind +board/+device, the shared layer taxonomy +device). The
  materials-bill machinery is route-keyed by DECLARATION (`unit_shape`: board.sexp
  present → board; the vehicle route otherwise): `gen_model_book.py`'s emitters carry
  route-honest content (the board's pin table from board.sexp; the devices' honest
  no-encoding/no-reference fragments; the per-shape internal-contracts census) and
  `check_materials_bill.sh`'s COMPLETENESS keys on the same function — with 4 new
  self-test arms (11/11). The two processor books' fragments regenerated
  byte-identical modulo the embedded generator hash (measured). Three books landed
  under `docs/models/`; the category-needs census carries 72 rows (the devices'
  covered sets name their datasheets; the board's absences are `out-of-scope` WITH
  their contract reasons, its composition categories `partial`); FACT-OWNERSHIP
  carries the book-side mirrors (46 kinds). Measured and corrected at execution: the
  BREADTH report's stale "2 registered units" prose was the GENERATOR's hardcoded
  string — fixed at the generator, regenerated (5 units, verdict `passed`);
  `models.md` updated to five units; DERIVED-COUNTS' arm total re-derived 341→345.
  Frontier: `.3` — generated maps and the hardware description.
- `2026-10-02`: the `.3` design brief recorded (`SEMULITH-P5-0012`). The scope censused:
  generated maps/wiring/hardware-description from `board.sexp` (OWN-05), the
  tracked-board freshness proof `compose_units.py` defers to the first tracked board,
  and exactly one handwritten duplicate map measured (the DOSSIER.md table). Probed
  before designing: the three parts compose (99 requirements / 107 obligations / 5
  sources, encoding from rv64i), and the composed catalogues in the board directory
  pass every profile-glob gate unchanged except FACT-OWNERSHIP, which fires on exactly
  the two new restatement pairs — registration, not weakening, is the recorded fix.
  The design: one generator (`gen_board.py`, boards discovered by declaration),
  `schema/hardware.sexp`, the `BOARD-GEN` doctrine with self-test, the duplicate map
  replaced by the generated `map.md` (one owner, two readers: DOSSIER link + book
  chapter), the FACT-OWNERSHIP rows + fixture re-pin to five units, the DOSSIER's
  stale status rows logged as a defect and fixed with the leaf. Frontier: `.3`
  execution — the generator, the gate, the generated corpus.
- `2026-10-02`: `.3` done (`SEMULITH-P5-0013`) — the maps are generated and drift-gated.
  `scripts/gen_board.py` (boards discovered by declaration) emits the seven artifacts
  from `board.sexp` alone: the composition manifest, the four composed catalogues (99
  requirements / 107 obligations / 5 sources / the rv64i encoding, materialized by the
  factorized `compose_units.compose_resolved` — one code path, the refactor measured
  byte-identical), `hardware.sexp` under its new schema, and `map.md`. The freshness
  proof `compose_units.py` deferred to the first tracked board landed as the BOARD-GEN
  doctrine (self-test 9/9, every RED arm asserting the reason; the generator refuses an
  inconsistent definition by name). The census found exactly one handwritten duplicate
  map (the DOSSIER's table) — replaced by the generated map (one owner, two readers:
  the DOSSIER links it, the book includes it). FACT-OWNERSHIP +8 rows (54 kinds), the
  fixture re-pinned to five units; DERIVED-COUNTS re-derived (32 doctrines, 354 arms).
  Measured and recorded at root: the brief's register-surface containment check is not
  implementable (device dossiers carry offsets in prose, never as data — the generator's
  refusals are scoped to what board.sexp proves; machine-readable offsets arrive with
  the device models); the DOSSIER's post-`.11` stale status rows (the brief's logged
  defect) fixed. Frontier: `.4` — the composition verdict, its input now on disk.
