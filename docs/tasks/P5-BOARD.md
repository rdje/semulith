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
  Status: `done` (`2026-10-02`, `SEMULITH-P5-0017`)
  Goal: for **every** CPU assumption, name the board or device guarantee that satisfies it, or reject the composition. Reset wiring, memory attributes, source priorities, counter units, time progress, access side effects, reservation invalidations, instruction visibility (`docs/CPU_ENVIRONMENT.md` §5, `ENV-02`).
  Acceptance: an unmatched assumption is a **rejection**, not a note. The laboratory's interface tests are re-run against the board provider where meaningful.
  Result (`2026-10-02`): the composition is **ACCEPTED**, and the verdict is decided, not
  narrated — the **BOARD-VERDICT** doctrine (33rd project doctrine,
  `scripts/board_verdict.py` + `scripts/check_board_verdict.sh`, self-test 6/6 with every
  RED arm asserting its reason on copies of the real board) re-decides three legs on
  every commit: the discharge over the composed catalogues (8/8), every `satisfies` edge
  resolved to a discharged assumption (3/3), and every board-deferred device obligation
  bound to exactly one decision `answers` edge (4/4). The machinery: the four deferred
  obligations (`OB-NIC-STRAP-RESETS` joined the three `.10` pre-wired records — the strap
  VALUES are `.4`-owned) carry the marker param `composition_disposition "required"`;
  `schema/board.sexp`'s `decision` gained the optional `answers` edge; the dispositions
  mirror into `hardware.sexp` (schema + generator, symmetric with the absence mirroring)
  so the model route consumes them as data. **The four dispositions, decided:**
  `D-BOARD-NIC-STRAPS` (D32 tied high — 32-bit native mode, EEDIO has no pull so the tie
  is explicit; SPEED_SEL unwired → its internal pull-up latches 1: 100 Mbps + AN
  enabled), `D-BOARD-NIC-TIME-FROZEN` (FREE_RUN reads its reset value forever, GPT_CNT
  never advances, INT_DEAS never runs — constant values carry no time information),
  `D-BOARD-NIC-LINK-SCENE` (static-complete at 100BASE-TX FD from before the guest's
  first access — the `D-BOARD-RESET` precedent the reset expectations already use for
  READY/EPC_BSY; BSR reads `0x782D`), `D-BOARD-NIC-PIN-TIEOFFS` (all pin reads 0).
  **Measured in execution, fixed at root (§15):** the board's eth0 declared 16-bit
  accesses from §1.10's summary sentence, but §3.6 makes the bus widths MODE-EXCLUSIVE —
  with D32 strapped, a 16-bit access has no datasheet-defined behaviour
  (`REQ-D-NIC-WIDTH`): the declaration narrowed to 32 (board.sexp, the generated maps
  regenerated), the NIC dossier's pairing-latch census entry flipped to `present false`
  with the new reason, the NIC DOSSIER corrected. The authored verdict landed as
  `profiles/netboard-lab-v0/COMPOSITION-VERDICT.md` (the per-assumption table with every
  aspect of the goal enumerated — source priorities/counter units/reservation
  invalidations recorded as not-arising with their reasons, never skipped; the
  `OB-PLATFORM` note stating why the discharge edges alone would be materially
  misleading), included as the board book's verdict chapter (one owner, two readers).
  The NIC expectations re-pinned what the verdict determines: `hw_cfg` → `0x00050004`,
  `free_run` → `0x00000000` (frozen), `phy_basic_status` → `0x782D` (the completed
  scene). **MODEL-COMPOSE's open question answered for this board shape:** no operator
  beyond union + discharge is needed — the declared edges close the gap. The
  interface-test leg: the laboratory's boundary and fixture suites re-run (`make check`,
  `run_smoke` — green), covering the RAM half the board preserves at the same base/size;
  the MMIO halves attach with the device models (the model route; probes are `.5`'s),
  named in the verdict document. DERIVED-COUNTS fired as designed (32→33 doctrines,
  359→365 arms, re-derived in `LIVE_STATUS.md`); FACT-OWNERSHIP gained no rows (the
  verdict document is authored narrative — the DOSSIER.md precedent; the disposition
  mirrors ride the existing `board-map` rows). The DEV_NOTES lesson: promotion declined
  (the finding's durability is the verdict + the doctrine; the measure-against-the-
  source discipline already has its knowledge cards).

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

- ID: `P5-BOARD.12` — **derived members of bounded families: the right instrument**
  Status: `done` (`2026-10-02`, `SEMULITH-P5-0015`)
  Goal: the routes-registry per-part byte ceiling applies to AUTHORED content;
  regeneration-gated derived members are exempt as a CHECKED property — registered in
  `doctrine/fact_ownership.tsv` as a mirror whose governor is a regeneration doctrine
  (the closed set) — never as a declaration. The ruling:
  [`decision_derived-members-of-bounded-families`](../../docs/decisions/decision_derived-members-of-bounded-families.md),
  director-delegated `2026-10-02` (the `.3` finding was surfaced; the director assigned
  the decision to the signing engineer, SOTA/signoff-grade).
  Acceptance: an authored over-ceiling part still fails by name; a derived over-ceiling
  part registered with a regeneration governor passes; a non-regeneration governor
  (e.g. RECORD-SCHEMA) never exempts; the `profiles/` authored per-part returns to
  65,536 with the composed catalogues exempt; `decision_profiles-family-composed-units`
  marked superseded in part. Aggregates untouched.
  Routing note (`2026-10-02`): created from the `.3` surfaced finding — composed
  catalogues multiply record bytes with composition depth, and the interim reviewed
  raise (64 → 128 KiB, one day old) taxed a property derived files cannot have. The
  board's composition work owns the fix; P7's soc/computer compositions inherit it.
  Result (`2026-10-02`): the two-tier per-part rule landed in
  `scripts/check_readme_routes.sh`. The closed regeneration-doctrine set (STATE-GEN,
  DEF-GEN, GUEST-GEN, BOARD-GEN, GATE-REPORT, MATERIALS-BILL, BOOK-INDEX) lives in the
  check, each member asserted registered in the project driver (a set/driver
  disagreement REFUSES — the exemption can never silently widen); `derived_exempt`
  resolves the exemption from `doctrine/fact_ownership.tsv` (mirror + regen governor),
  the one already completeness-checked registry — no second declaration surface. The
  per-part loop now judges EVERY over-ceiling member (it previously inspected only the
  single biggest): exempt members are reported as proof (`derived: <path> …`), the
  rest fail by name. Self-test 12 → **17 arms** (GREEN the real-corpus-shaped
  exemption with the proof line; RED a validation governor keeps the authored ceiling;
  RED no exemption by adjacency; GREEN/RED the set/driver agreement), 17/17. On the
  real corpus the rule discriminates exactly as ruled: the two composed catalogues
  (104,372 B / 94,027 B) exempt with proof printed, the NIC's authored 60,112 B
  catalogue silently under the restored **65,536** authored per-part (0.92×) — the
  day-old 128 KiB interim raise reverted, `decision_profiles-family-composed-units`
  superseded in part. **Measured in execution, fixed at root:** the two regen-set arms
  were first written under a new `armregen` helper — an idiom DERIVED-COUNTS'
  enumerator does not count (it knows `arm "` and `score`), so 2 of the 17 arms were
  invisible to the arm total; caught by the enumerator's own drift verdict (357 ≠ 359)
  and fixed by folding the probe command into `arm`'s optional `[cmd...]` form — one
  counted idiom, the enumerator untouched. The lesson PROMOTED to
  `docs/knowledge/a-byte-ceiling-applies-to-authored-content.md` (+ INDEX): the
  instrument must match the failure mode.

## Current Frontier

| Order | Leaf | Status | Why next |
| --- | --- | --- | --- |
| 1 | `P5-BOARD.6` | `pending` | the platform capability manifest: the read-only derived export of the accepted processor/device/board profile and its boot contract for archogen's compatibility checker (OWN-06 — derived, never handwritten); the composition verdict (`.4`) is landed and the dispositions are data in `hardware.sexp`, so the manifest's inputs are all on disk |

## Decisions

- `2026-09-13` … `2026-10-02` (the `.1`, `.2`, `.10`, `.11` design briefs and the `.1` execution amendments): archived to [`archive/P5-BOARD.md`](archive/P5-BOARD.md) (per-part ceiling — moved there on `2026-10-02` at leaf `.4`; recorded before code, kept verbatim).

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
- `2026-10-02` (the `.12` ruling, director-delegated; recorded before its execution;
  sources: the `.3` measured finding, the routes-registry gate's own code, the
  FACT-OWNERSHIP registry's completeness contract):
  **The instrument must match the failure mode.** The `.3` composed catalogues fired
  the authored per-part byte ceiling and forced a reviewed raise one day after the
  previous one; the director delegated the policy question to the signing engineer
  ("yours to decision and act upon … SOTA, SIGNOFF and PRODUCTION-GRADE"). The ruling,
  recorded in full in `decision_derived-members-of-bounded-families.md`: the per-part
  byte ceiling's founding failure mode is silent accretion in hand-maintained files —
  a property a regeneration-gated derived file CANNOT have (every byte is re-derived
  on every commit; its size is a pure function of already-bounded inputs; its real
  risks are governed by other gates). So the ceiling goes two-tier: it applies to
  every family member NOT registered in `doctrine/fact_ownership.tsv` as a mirror
  with a regeneration-doctrine governor (the closed set: STATE-GEN, DEF-GEN,
  GUEST-GEN, BOARD-GEN, GATE-REPORT, MATERIALS-BILL, BOOK-INDEX); the exemption is a
  CHECKED property (the registry is the one already completeness-checked declaration —
  no second surface, and an authored file cannot smuggle under it because nothing
  regenerates it), never a declaration. The discriminating line measured against the
  live corpus: the NIC's authored 60,112 B catalogue (governor RECORD-SCHEMA) keeps
  the authored ceiling at 0.92×; the board's composed 104,372 B catalogue (governor
  BOARD-GEN) is exempt. Aggregates still apply to derived members (population
  surprises are census-level). Consequences: the `profiles/` authored per-part returns
  to 65,536; `decision_profiles-family-composed-units` is superseded in part (its
  measurement stands; its raise was the right interim); the per-depth raise ceremony
  never recurs; a governor removed from the doctrine registry makes its exempt files
  ceiling-liable the same commit. **Design alternatives weighed and rejected:** (a)
  keep raising per-part per composition level — reviews a number, proves nothing
  about the derivation; (b) a `derived` lifecycle class on the routes registry — the
  registry is per-row and `profiles/` mixes authored + derived members in one
  directory, so the granularity is wrong and a second declaration surface would drift
  against fact_ownership.tsv; (c) fingerprint-header detection — the composed
  catalogues are record-format files that cannot carry headers. The closed regen set
  grows the day a new regeneration doctrine is registered, with that doctrine's leaf.
- `2026-10-02` (design brief for `.4`, recorded before its execution; sources: the composed
  catalogues on disk (`.3`), the four pre-wired composition records in
  `profiles/lan9118-lab-v0/`, `docs/CPU_ENVIRONMENT.md` §5, ENV-02, the discharge machinery
  (`MODEL-COMPOSE.3`), and the pinned LAN9118 artifact re-read for the strap semantics —
  §1.10, §3.6, Table 2-2, Table 2-4, Notes 5-1/5-3/5-4, §5.5.13):
  **The verdict's shape: a mechanical core, re-decided on every commit, plus an authored
  analysis.** Measured pre-conditions: `discharge_assumptions.py` over both the three parts
  and the composed unit discharges 8/8 today — but that is the obligation-graph half. The
  discharge edges of the two platform-dependent assumptions land on `OB-PLATFORM`, the
  LABORATORY platform guarantee ("declares exactly one region … and NO devices"), scoped to
  `rv64i-lab-v0` by `profile_ids`. On the board their content is re-established by the
  board's declared absences (the `satisfies` edges `.1` pre-wired) plus the device
  dispositions below — that re-establishment IS the composition verdict, and it needs a
  re-runner (the MODEL-COMPOSE.4 lesson: a capability without a re-runner regresses
  silently). **There are FOUR composition records, not three** — beyond TIME-SOURCES /
  PHY-LINK / GPIO-PINS, `OB-NIC-STRAP-RESETS` (authority `architecture`): the strap VALUES
  are the board's composition choice, `.4`-owned.
  **The four dispositions, decided** (each lands as a board.sexp `decision` carrying a new
  optional `answers` edge — the sanctioned schema-edit shape — and is mirrored into
  `hardware.sexp` as a `(disposition …)`, symmetric with the absence/`satisfies` mirroring,
  so the model route consumes them as data):
  1. `D-BOARD-NIC-STRAPS` answers `OB-NIC-STRAP-RESETS`: **D32/nD16 tied HIGH** (32-bit
     native mode — §3.6: "the native environment for the LAN9118 … no special requirements";
     the 64-bit host's natural width; EEDIO has no internal pull per Table 2-4, so this is
     an explicit board tie, declared) and **SPEED_SEL left unwired** → its internal pull-up
     (Table 2-3: `I (PU)`) latches 1 (Table 2-2: 100 Mbps + auto-negotiation ENABLED).
     Consequences: `HW_CFG` = `0x00050004`; PHY 0 bits 13/12 = 1/1; PHY 4 = `0x01E1`;
     PHY 31's HCDSPEED default = 100HD pre-negotiation.
  2. `D-BOARD-NIC-TIME-FROZEN` answers `OB-NIC-TIME-SOURCES`: **frozen.** `FREE_RUN` reads
     its reset value 0 forever; `GPT_CNT` never advances (a `TIMER_EN` write still loads
     `GPT_LOAD` — a guest-visible, datasheet-defined, deterministic state change — but the
     count never decrements, so `GPT_INT` never sets); `INT_DEAS` never runs (the interrupt
     line is unconnected, `INT_EN` resets 0 — no deassertion interval ever starts). Constant
     or guest-written-static values carry no time information; the harness's
     retired-instruction count never becomes target-visible. The deviation from wall-clock
     faithfulness is deliberate and recorded as data: a polled driver never needs the
     counters, and a guest busy-waiting on one hanging is exactly why the disposition must
     not be prose.
  3. `D-BOARD-NIC-LINK-SCENE` answers `OB-NIC-PHY-LINK`: the replay's declared link scene
     is **static and complete** — the recorded trace's wire is up at 100BASE-TX full-duplex,
     auto-negotiation complete, from before the guest's first access. The reasoning is the
     reset expectations' own precedent (`D-BOARD-RESET`: the board's cold reset completes
     before any guest access exists — the same discipline that already pins READY and
     EPC_BSY post-transient): the wire-domain transients complete before any guest read, so
     every guest-observable read sees the completed scene — BSR = `0x782D` (the `0x7809`
     reset composition with Link Status + Auto-Negotiate Complete; the latch-low Link bit
     never trips, the scene never fails), PHY 17 ENERGYON = 1 (already its reset), PHY 31
     Autodone = 1 and HCDSPEED = `110b` (§5.5.13: 100BASE-TX FD), PHY 5 = `0x01E1` (the
     declared partner scene). Note 3-11's wait-for-link succeeds at the first read.
  4. `D-BOARD-NIC-PIN-TIEOFFS` answers `OB-NIC-GPIO-PINS`: no GPIO/LED/EEPROM pins are
     wired; every pin-readable value is tied off at **0** — `GPIODn` reads 0, and the
     `EEPR_EN`-muxed MII monitor signals read 0.
  **Measured composition defect found in the brief, fixed with the leaf (§15):**
  board.sexp's eth0 declares `access-widths 16 32` citing §1.10's summary sentence — but
  §3.6 makes the widths MODE-EXCLUSIVE (the strap selects the bus width; 16-bit pairing is
  16-bit-mode operation), so with D32 strapped a 16-bit access has no datasheet-defined
  behaviour (`REQ-D-NIC-WIDTH`). The declaration narrows to **32 only**; the NIC dossier's
  pairing-latch census entry (justified by the old declaration) flips to `present false`
  with the new reason, and `state.sexp`'s census answer/consequence + the NIC DOSSIER are
  corrected in the same pass. The datasheet-facing records (`REQ-D-NIC-HBI`,
  `REQ-D-NIC-WIDTH`, `WORD_SWAP`) stay — they describe the device across both modes; the
  strap narrowing is the board's composition choice, exactly the layering the dossier
  designed for.
  **The per-assumption verdict (the leaf goal's enumeration):** RESET ← the board's cold-only
  reset block (`satisfies`) + both dossiers' POR/nRESET semantics; ADDRESS-UNITS ← 64-bit
  byte space, regions resolved in hardware.sexp, off-map = AccessFault (harness rule,
  unchanged); ACCESS-WIDTHS ← the per-device declared widths (32 UART, 32 NIC), anything
  else a board-reported contract violation (`D-BOARD-ACCESS-POLICY`), misalignment stopped
  by the CPU first (`OB-MISALIGN-DATA`); VIRTUAL-TIME (counter units, time progress) ← no
  timer device (`satisfies`) + the frozen NIC counters (disposition 2) + the UART carries
  no counter (`div` is a programmed divisor latch, not a counting register) + the CPU
  profile's CSR exclusion (the same digest-pinned unit); EVENT-DELIVERY (source priorities)
  ← no interrupt controller (`satisfies`) + both IRQ lines unconnected-and-declared — no
  sources exist, so no priority question arises; device status bits still set per datasheet
  (MMIO-visible, polled); ORDERING ← one hart, sequential, PIO devices with no DMA add no
  concurrency; FETCH-SUPPLY (instruction visibility) ← fetch from RAM only (every MMIO
  region non-executable, generator-refused otherwise), no extraneous fetch, no caches
  anywhere — stores and fetches hit the same RAM, coherent by construction;
  PARTIAL-PROGRESS (reservation invalidations) ← the profile's encoding is rv64i only: no
  A extension, no LR/SC, so no reservations exist to invalidate, and device side effects
  complete at the access. **MODEL-COMPOSE's open question answered for this board shape:**
  no operator beyond union + discharge is needed — the declared `satisfies`/`answers` edges
  close the gap the open question anticipated; recorded in the verdict document.
  **The machinery:** (a) the four obligations gain `(param (name composition_disposition)
  (value (str "required")))` — the machine-readable "the board must answer this"; (b)
  `schema/board.sexp`'s `decision` gains optional `answers` (`^OB-[A-Z0-9-]+$`, repeated,
  unique); `schema/hardware.sexp` gains `(disposition …)` (repeated-optional) and
  `gen_board.py` mirrors it; (c) the **BOARD-VERDICT doctrine**
  (`scripts/board_verdict.py` + `scripts/check_board_verdict.sh`): per tracked board —
  schema-validate board.sexp, discharge the composed unit, every `satisfies` edge resolves
  to a discharged environment-assumption, every marked obligation is answered by exactly
  one decision `answers`, every `answers` names a marked obligation — ACCEPTED prints every
  edge; any leg failing is a REJECTION by name, never a note (the leaf's acceptance).
  Self-test arms RED each leg on copies of the real board; registered + mirrored +
  DERIVED-COUNTS re-derived. (d) `profiles/netboard-lab-v0/COMPOSITION-VERDICT.md` — the
  authored verdict: the per-assumption table, §5's aspects checklist (reset wiring, memory
  attributes, source priorities, counter units, time progress, access side effects,
  reservation invalidations, instruction visibility), the four dispositions, the
  OB-PLATFORM note, the interface-test leg, the non-claims; the board book's evidence
  chapter includes it (one owner, two readers); the DOSSIER's status row flips;
  `gen_model_book.py`'s board census prose updated. (e) The NIC expectations re-pin what
  the verdict determines: `hw_cfg` → `0x00050004`, `free_run` → `0x00000000` (frozen),
  `phy_basic_status` → `0x782D` (the completed scene), the header comment corrected.
  **The interface-test leg (the leaf's second acceptance):** the laboratory's boundary and
  fixture suites re-run (`make check` + smoke) — their board-meaningful half is the RAM
  region the board preserves at the same base/size; the MMIO halves attach with the device
  models (the model route; probes are `.5`'s), named, never silently skipped.
  **FACT-OWNERSHIP:** no new rows — the verdict document is authored narrative (the
  DOSSIER.md precedent, covered by the internal-contracts census), its mechanical core
  re-decided by BOARD-VERDICT on every commit; the disposition mirrors into hardware.sexp
  ride the existing `board-map` rows.
  **Not `.4`'s scope:** the device models (Rust — the model route), probes (`.5`), the
  capability manifest (`.6`), the BOARD gate report (`.7`).

- `2026-10-02` (design brief for `.6`, recorded before its execution; sources:
  `docs/ARCHOGEN_INTEGRATION.md` §2/§3, `RULES.md` OWN-06, the `gen_board.py` idiom, the
  dossier mapping owner (`scripts/dossier_sexp.py`), the obligation-parameter census, the
  GC-REPORT digest rule (`scripts/gate_report.py`), and the director's same-day reminder:
  archogen is actively being developed and is far from functional):
  **The consumer-absence boundary, stated first.** archogen has no functional eADL
  interface today (§1: "no eADL grammar, typed API, or archogen implementation was
  supplied"; the director re-confirmed `2026-10-02`). So `.6` builds the Semulith-owned
  side of the export boundary ONLY: a versioned, schema-gated, regeneration-gated
  manifest whose correctness legs on our side are derivation freshness, schema
  conformance, and §3 content coverage. The compatibility checker is archogen's and does
  not exist; nothing here may claim "archogen accepts this", and the manifest's
  non-claims say so. The real-interface inspection stays with `AG-OS.1` (proposed). No
  eADL parser, matcher or scheduler in Semulith (§2) and no archogen dependency — the
  manifest is consumable by ANY checker that reads the schema.
  **The §3 content census (measured this day).** §3's six bullets against tracked data:
  (1) CPU identity/profile — DATA in `profiles/rv64i-lab-v0/profile.sexp` via the mapping
  owner: id, version, architecture, base RV64I, chapter_version 2.1, spec_revision
  v20260120, harts 1, xlen 64, ilen 32, ialign 32, privilege_modes `["M"]`, extensions
  `[]` (measured: `dossier_sexp.load_profile` returns all); **endianness is prose-only**
  (REQ-D-ENDIAN / OB-ENDIAN carry the decision, never the value). (2) Memory map /
  devices / widths / interrupts / timers — DATA in board.sexp (regions, device pins with
  material/revision/sha256, access-widths, interrupt unconnected, absences with
  `satisfies`). (3) Boot contract — PARTIAL: the reset block is data; the image format
  (ELF PT_LOAD), argument convention (none), firmware services (none), ABI constraint and
  hardware-description format are NOT DECLARED as data anywhere (measured: the
  schema/board.sexp construct census — board, processor, device, backend, memory-map,
  region, reset, timers, interrupt-controller, serial-console, decision — has no boot
  construct; the ELF loading lives in `crates/semulith-cli` source). (4) Counter/time,
  events, ordering — DATA: the obligation parameters (`OB-ENV-VIRTUAL-TIME` pins
  `time_source "none"`, `csr_readable_time false`, `mmio_readable_time false`;
  `OB-ENV-EVENT-DELIVERY` pins synchronous yes / asynchronous no / controller none;
  `OB-ENV-ORDERING` pins harts 1, sequential in-order, `memory_model_claim "none"`);
  timing fidelity (functional-only, no WCET) is NOT declared. (5) Test-control —
  PARTIAL: the backends and cold reset are board data; the execution budget, trace
  selection and snapshot/resume are CLI capabilities (`semulith run --steps`,
  `--trace-stores`, `snapshot`/`resume`), not tracked data. (6) Versions / dependencies /
  fingerprints / limitations — DATA (the board's pins and `(status experimental)`).
  **The gap census (GAP-CLAIM-CENSUS):** no platform export exists — `ls
  scripts/gen_platform.py scripts/check_platform_gen.sh schema/platform.sexp` all absent;
  `grep manifest doctrine/fact_ownership.tsv` finds only the composition-manifest rows.
  **Measured integrity finding, logged and owned (§15), fixed with this leaf:** the
  board's `dossier-sha256` pin is DISPLAY-ONLY today — `gen_model_book.py` renders it and
  nothing re-derives it (census: two consumers, both display); the digest covers every
  tracked dossier file except `*-REPORT.md` (measured in `gate_report.py`), so a
  profile.sexp edit would silently stale the pin. `.6`'s generator makes the pin
  load-bearing: it re-derives the digest by gate_report's rule (imported — one code path)
  and REFUSES a stale pin.
  **The design, decided.**
  1. **board.sexp gains `(boot …)` and `(test-control …)` blocks** (schema/board.sexp —
     the sanctioned schema-edit shape; §2's table makes the platform package the boot
     contract's owner). `boot`: image format (ELF, PT_LOAD segments), load region (names
     a declared executable RAM region — the generator refuses a dangler), entry (the
     image's entry address, citing `OB-ENV-RESET`), register state (x1..x31 zeroed,
     citing `D-ENTRY-STATE`), argument convention (none), firmware services (none —
     ECALL/EBREAK are typed harness traps, `REQ-D-ECALL-EBREAK`), ABI (freestanding — no
     environment ABI), hardware-description (hardware.sexp, the board's internal
     generated data — NOT a device tree; P6 pins its own format). `test-control`:
     console capture (the console device's host-console backend), completion/failure
     signalling (the typed outcome vocabulary — RequestedTrap / Exception / ModelError /
     UndefinedCase), reset (cold only), input injection (the recorded backends),
     execution budget (the runner's step budget), trace selection (step trace + store
     trace), snapshots (snapshot/resume records). The runner capabilities are the
     platform package's DECLARATION, evidenced by the CLI's own suites — the manifest
     says so; it does not evidence them itself.
  2. **`schema/platform.sexp`** — the export's contract; DOSSIER-SCHEMA pairs
     `profiles/*/platform.sexp` by basename, automatically. Every facility carries an
     explicit presence marker (`offered` / `absent-by-contract` / `limited`) with its
     evidence edge — §3's "required versus optional facilities are explicit", answered
     from the offering side.
  3. **`scripts/gen_platform.py`** — the one generator; boards discovered BY DECLARATION
     (the gen_board idiom). Inputs: board.sexp (read through gen_board's
     `read_board`/`check_consistency` — imported, never re-implemented), the pinned
     processor unit's profile.sexp (through `dossier_sexp`, the mapping owner), and the
     composed contract-obligations.sexp (BOARD-GEN-gated; the platform-level obligation
     parameters). The OWN-03 fingerprint header names ALL canonical inputs (the
     gate_report multi-input idiom). Refusals BY NAME: a stale dossier pin (the finding
     above), a missing unit directory or profile.sexp, a schema failure, a boot/test-
     control claim contradicting the wiring (console capture without a host-console
     backend; injection without a recorded backend; a load region that is not declared,
     executable RAM). `--check` re-derives byte-exact and refuses drift.
  4. **`scripts/check_platform_gen.sh` — the PLATFORM-GEN doctrine** (the 34th project
     doctrine): freshness with self-test RED arms asserting the reason (a hand-edited
     platform.sexp → DRIFT; a board.sexp edit leaving a stale export; a stale dossier
     pin; a contradicting claim), registered in `scripts/check_doctrines.project.sh`,
     mirrored in `DOCTRINE_ENFORCEMENT.md` + `docs/book/src/working/doctrines.md`;
     `REGEN_GOVERNORS` in `check_readme_routes.sh` gains PLATFORM-GEN per the `.12`
     ruling ("the closed regen set grows the day a new regeneration doctrine is
     registered, with that doctrine's leaf"); DERIVED-COUNTS re-derived, never
     incremented.
  5. **Endianness gets its machine-readable owner**: profile.sexp gains
     `(endianness little)` (schema/profile.sexp edit — the `.11` sanctioned-edit
     precedent). The cascade is measured and lands in the same commit: the GC-REPORT
     digest changes (GATE-REPORT regenerates GC-REPORT.md), board.sexp's pin updates,
     and the new pin verification is what turns any future drift into a refusal.
  6. **The export's shape** mirrors §3's six bullets: processor identity + ISA facts;
     memory map; devices with pins; absences; dispositions; boot contract; time/events/
     ordering; test-control; versions/fingerprints (the header + pins); limitations
     (EXPERIMENTAL, conditional on the CPU's acceptance trajectory; no timers, no
     interrupts, 32-bit MMIO only, PIO no DMA, polled drivers); non-claims (a compatible
     manifest proves neither OS correctness nor manifest-implementation match — §3's own
     sentence; no archogen consumer exists today).
  7. **FACT-OWNERSHIP rows** (exact set settled at execution against the gate's verdict):
     `platform-export (netboard-lab-v0)` owner board.sexp → mirror platform.sexp,
     governor PLATFORM-GEN; the profile-facts and obligation-parameter restatements
     registered with their true owners (profile.sexp; the CPU's contract-obligations via
     the composed catalogue), never left ungoverned.
  8. **Docs:** the board book gains the platform-export chapter (one owner, two readers —
     the generated file included); `docs/book/src/plan/p5-p7.md` gains the `.6` section;
     ARCHOGEN_INTEGRATION §3 updated (the "future versioned manifest" now exists for
     netboard-lab-v0, with the consumer-absence stated); TOOLBOX.md gains the tool row;
     the doctrine mirrors; KNOWLEDGE-MAP and the book index regenerated; the live docs in
     the same commit.
  **Not `.6`'s scope:** the probes (`.5`), the `BOARD` gate report (`.7` — its "a
  compatible manifest is recorded as not proving…" acceptance is the report's, the
  manifest carries the non-claims as data), the device models in Rust, any eADL-side
  artifact, P6's pinned boot hardware-description format.

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

`P5-BOARD.4` (`2026-10-02`, `SEMULITH-P5-0017`):

- [x] **REPRODUCE / ISSUE** — the composition's mechanical core was green but the verdict
  did not exist: nothing re-decided it, four device records deferred values to the board
  with no binding, and a board declaration contradicted the datasheet. Measured
  pre-conditions:

  ```
  $ python3 scripts/discharge_assumptions.py profiles/netboard-lab-v0
  … all 8 environment-assumption(s) discharged by named guarantee(s) — the composition holds
  # … but the platform-dependent edges land on OB-PLATFORM, the LABORATORY guarantee
  #   ("declares … NO devices") — formally true, materially misleading on a board
  $ grep -c 'composition_disposition' profiles/lan9118-lab-v0/contract-obligations.sexp
  0            # the four deferred records were prose-only — nothing could check the binding
  $ git ls-files scripts | grep -c 'board_verdict'
  0            # no re-runner: the verdict would regress silently (MODEL-COMPOSE.4's lesson)
  $ grep -A2 'access-widths' profiles/netboard-lab-v0/board.sexp | head -2
  (access-widths 16)   # ← measured false for the strapped mode: §3.6 makes the bus widths
  (access-widths 32)   #    mode-exclusive; with D32 a 16-bit access is datasheet-undefined
  ```

- [x] **ROOT CAUSE (WHY + WHERE)** — WHY: a composition verdict that lives in prose is a
  claim without legs; the device dossier's four deferrals (STRAP-RESETS joined the three
  `.10` records — the strap VALUES are the board's choice) had no machine-readable marker,
  so no gate could refuse a board that ignored them; and `.1`'s 16-bit declaration read
  §1.10's summary sentence without §3.6's mode exclusivity. WHERE: the new
  `scripts/board_verdict.py` + `scripts/check_board_verdict.sh`; `schema/board.sexp`
  (decision `answers`), `schema/hardware.sexp` (`disposition`) + `scripts/gen_board.py`
  (the mirror); `profiles/lan9118-lab-v0/contract-obligations.sexp` (the marker param);
  `profiles/netboard-lab-v0/board.sexp` (the dispositions + the width narrowing);
  the registry + mirrors (`scripts/check_doctrines.project.sh`,
  `DOCTRINE_ENFORCEMENT.md`, `docs/book/src/working/doctrines.md`).
- [x] **FIX** — the BOARD-VERDICT doctrine (33rd): discharge + satisfies-resolution +
  disposition-binding per tracked board, every refusal named; the four dispositions as
  board.sexp decisions with `answers`, mirrored into hardware.sexp; the marker param on
  the four obligations; eth0 narrowed to 32-bit and the NIC dossier's pairing-latch
  census flipped with the new reason; `COMPOSITION-VERDICT.md` (the per-assumption
  table, the §5 aspects, the OB-PLATFORM note, the interface-test leg, the non-claims)
  included as the board book's verdict chapter; the expectations re-pinned
  (`hw_cfg 0x00050004`, `free_run 0` frozen, `phy_basic_status 0x782D`).
- [x] **ADDRESSED (verified)** — the acceptance: every assumption matched, an unmatched
  one a rejection BY NAME:

  ```
  $ bash scripts/check_board_verdict.sh
  BOARD-VERDICT: ok (1 board(s) — every CPU assumption discharged, every satisfies edge
  resolved, every composition disposition bound)
  $ bash scripts/check_board_verdict.sh --self-test
  BOARD-VERDICT --self-test: 6 pass / 0 fail
  #   REDs: UNANSWERED COMPOSITION OBLIGATION 'OB-NIC-STRAP-RESETS'; ANSWERS NOTHING;
  #   ANSWERED TWICE; SATISFIES EDGE 'OB-ENV-GHOST'; DANGLING DEP (the acceptance's
  #   unmatched assumption, armed by removing a guarantee from the composed catalogue)
  $ python3 scripts/board_verdict.py profiles/netboard-lab-v0 | tail -6
    D-BOARD-NIC-STRAPS answers OB-NIC-STRAP-RESETS
    D-BOARD-NIC-TIME-FROZEN answers OB-NIC-TIME-SOURCES
    D-BOARD-NIC-LINK-SCENE answers OB-NIC-PHY-LINK
    D-BOARD-NIC-PIN-TIEOFFS answers OB-NIC-GPIO-PINS
    all 8 environment-assumption(s) discharged, 3 satisfies edge(s) resolve, 4 composition
    disposition(s) bind — the composition holds
  $ grep -c '(disposition ' profiles/netboard-lab-v0/hardware.sexp
  4            # the model route consumes the dispositions as data
  $ grep -c '0x782D' docs/models/netboard-lab-v0/book/the-verdict.html
  1            # the verdict chapter includes the ONE authored verdict — verified in HTML
  ```

  The interface-test leg: `make check` (fmt + clippy -D warnings + all tests) green;
  `python3 scripts/run_smoke.py` → `run_smoke: ok` — the laboratory's boundary and
  fixture suites re-run, covering the RAM half the board preserves at the same
  base/size; the MMIO halves attach with the device models (the model route; probes are
  `.5`'s), named in the verdict document.
- [x] **NO REGRESSION** — RECORD-SCHEMA `16 record file(s)` after the marker-param edit;
  BOARD-GEN `byte-exact` (self-test 9/9) after the hardware.sexp disposition mirror;
  MATERIALS-BILL 5/5 after the board-census prose update (the two processor books'
  fragments byte-identical modulo the embedded generator hash — measured by the same
  filtered diff as `.11`; the NIC fragment's input fingerprint updated for the dossier
  edit, the machinery working as designed); UNIT-BOOKS 5/5; `make gate` →
  `=== all doctrines green ===` (DERIVED-COUNTS re-derived 32→33 doctrines, 359→365
  arms in `LIVE_STATUS.md`); `mdbook build docs/book` rc 0; `gen_book_index.py --check`
  rc 0. No Rust surface touched. The per-part ceiling firing on the tree file itself was
  handled by the house's own instrument: the older completed leaves' design briefs and
  checklists archived verbatim to `docs/tasks/archive/P5-BOARD.md` with pointers — the
  split, not a raise (the `archive/P2-SCALAR*` precedent).
- [x] **LOCKSTEP** — tree (leaf + frontier + checklist + logs; the archive split),
  `MEMORY.md` (next action `.6`), `CHANGELOG.md`, `DEV_NOTES.md` (the 16-bit lesson;
  promotion declined), `LIVE_STATUS.md` (P5 row + re-derived counts),
  `docs/TASK_TREE.md`, the doctrine mirrors, the board DOSSIER (status + claim scope),
  the board book (the verdict chapter, methodology, gaps, materials), the NIC dossier
  (DOSSIER, state.sexp census, expectations), mdBook `plan/p5-p7.md` (the `.4` section)
  + `models/the-information-a-unit-demands.md`, KNOWLEDGE_MAP regenerated,
  `gen_book_index.py` regenerated.

`P5-BOARD.12` (`2026-10-02`, `SEMULITH-P5-0015`):

- [x] **REPRODUCE / ISSUE** — the `.3` composed catalogues forced a per-part raise one
  day after the previous one, and the `.3` finding (surfaced, director-delegated)
  named the cause: the ceiling taxed a property derived files cannot have. Measured
  pre-condition, the interim state this leaf replaced:

  ```
  $ grep -n "131072" doctrine/readme_routes.tsv | tail -1
  …the per-part 128 KiB decision_profiles-family-composed-units (2026-10-02)	590	2450000	600	2867200	131072
  $ bash scripts/check_readme_routes.sh --self-test
  README-ROUTING-CLOSURE --self-test: 12 pass / 0 fail   # no two-tier arms existed
  ```

- [x] **ROOT CAUSE (WHY + WHERE)** — the per-part ceiling's founding failure mode is
  silent accretion in hand-maintained files (the gate's own comment: "an aggregate
  bound alone permits one member to become the monolith"); a regeneration-gated file
  cannot accrete silently, so the instrument did not match the failure mode. WHERE:
  the per-part block in `verify_routes` (`scripts/check_readme_routes.sh` — which
  also inspected only the single biggest member, so a second over-ceiling file was
  never even reported), the closed regen set and the set/driver assertion (same
  file), the routes-registry row (`doctrine/readme_routes.tsv`), the doctrine prose
  mirrors (`DOCTRINE_ENFORCEMENT.md`, `docs/book/src/working/doctrines.md`).
- [x] **FIX** — the two-tier rule: `derived_exempt` resolves the exemption from
  `doctrine/fact_ownership.tsv` (mirror + regeneration governor); the closed
  `REGEN_GOVERNORS` set with `regen_set_registered` refusing set/driver drift; the
  per-part loop judging EVERY over-ceiling member (exempt → reported as proof, else
  failed by name); the registry row back to 65,536 with the ruling comment; the
  composed-units record superseded in part; the lesson promoted to
  `docs/knowledge/a-byte-ceiling-applies-to-authored-content.md` (+ INDEX).
- [x] **ADDRESSED (verified)** — the acceptance, run:

  ```
  $ bash scripts/check_readme_routes.sh --self-test
  README-ROUTING-CLOSURE --self-test: 17 pass / 0 fail
  $ bash scripts/check_readme_routes.sh
  README-ROUTING-CLOSURE: ok (33 governed destination(s))
    derived: profiles/netboard-lab-v0/contract-obligations.sexp (104372 bytes > 65536 authored per-part) is regeneration-gated — exempt (decision_derived-members-of-bounded-families)
    derived: profiles/netboard-lab-v0/requirements.sexp (94027 bytes > 65536 authored per-part) is regeneration-gated — exempt (decision_derived-members-of-bounded-families)
  $ wc -c profiles/lan9118-lab-v0/contract-obligations.sexp
  60112   # the authored catalogue: under the restored 65,536 authored ceiling (0.92x), not exempt
  $ grep -c "131072" doctrine/readme_routes.tsv
  0       # the day-old interim raise is gone
  ```

- [x] **NO REGRESSION** — the pre-edit self-test arms all still pass (12 carried + 5
  new = 17/17, every RED asserting the reason); the authored-fail path is armed RED
  on fixtures (validation governor, adjacency) since the real corpus's authored
  members are all under the ceiling; `make gate` → `=== all doctrines green ===`
  (DERIVED-COUNTS after the enumerator re-derived 354 → 359 arms in
  `LIVE_STATUS.md`); `mdbook build docs/book` rc 0; `gen_book_index.py --check` rc 0.
  No Rust surface touched.
- [x] **LOCKSTEP** — tree (leaf + frontier + checklist + logs), `MEMORY.md` (active
  trees line), `CHANGELOG.md`, `DEV_NOTES.md` (lesson PROMOTED to the knowledge card
  + INDEX), `LIVE_STATUS.md` (P5 row + arm total), `docs/TASK_TREE.md`,
  `docs/decisions/INDEX.md` (the ruling row; the composed-units row marked
  superseded in part), the doctrine prose mirrors, KNOWLEDGE_MAP regenerated.

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
  Archived to [`archive/P5-BOARD.md`](archive/P5-BOARD.md) (per-part ceiling — moved
  there on `2026-10-02` at leaf `.4`; the filled checklist is kept verbatim).

`P5-BOARD.10` (`2026-10-02`, `SEMULITH-P5-0009`):
  Archived to [`archive/P5-BOARD.md`](archive/P5-BOARD.md) (per-part ceiling — moved
  there on `2026-10-02` at leaf `.4`; the filled checklist is kept verbatim).

`P5-BOARD.2` (`2026-10-02`, `SEMULITH-P5-0007`):
  Archived to [`archive/P5-BOARD.md`](archive/P5-BOARD.md) (per-part ceiling — moved
  there on `2026-10-02` at leaf `.4`; the filled checklist is kept verbatim).

`P5-BOARD.1` (`2026-10-02`, `SEMULITH-P5-0005`):
  Archived to [`archive/P5-BOARD.md`](archive/P5-BOARD.md) (per-part ceiling — moved
  there on `2026-10-02` at leaf `.4`; the filled checklist is kept verbatim).

`P5-BOARD.9` (`2026-10-01`, `SEMULITH-P5-0003`):
  Archived to [`archive/P5-BOARD.md`](archive/P5-BOARD.md) (per-part ceiling — moved
  there on `2026-10-02` at leaf `.4`; the filled checklist is kept verbatim).

`P5-BOARD.8` (`2026-10-01`, `SEMULITH-P5-0002`):
  Archived to [`archive/P5-BOARD.md`](archive/P5-BOARD.md) (per-part ceiling — moved
  there on `2026-10-02` at leaf `.4`; the filled checklist is kept verbatim).

## Verification Log

| Date | Leaf | Checks | Result |
| --- | --- | --- |
| `2026-10-02` | `.4` | `discharge_assumptions.py` over the composed unit 8/8 (pre-condition); BOARD-VERDICT real run green + self-test 6/6 (REDs: unanswered/ghost/double-bound dispositions, ghost satisfies edge, guarantee removed → DANGLING DEP); 4 dispositions in hardware.sexp; the verdict include verified in the built HTML; `make check` + `run_smoke` green (the interface-test leg); RECORD-SCHEMA 16 files; BOARD-GEN byte-exact 9/9; MATERIALS-BILL 5/5 (processor fragments byte-identical modulo generator hash); UNIT-BOOKS 5/5; `make gate` green (DERIVED-COUNTS re-derived 32→33 doctrines, 359→365 arms); `mdbook build` rc 0; `gen_book_index.py --check` rc 0 | the composition verdict: ACCEPTED and re-decided on every commit — 8/8 discharged, 3/3 satisfies edges resolved, 4/4 dispositions bound (straps, frozen time sources, static-complete link scene, pin tie-offs); the 16-bit declaration measured false against §3.6 and narrowed; the tree file's own per-part ceiling firing handled by the archive split |
| `2026-10-02` | `.12` | README-ROUTING-CLOSURE self-test 12 → 17 arms, 17/0 (GREEN the real-corpus-shaped exemption + proof line; RED validation governor keeps the ceiling; RED no exemption by adjacency; GREEN/RED set/driver agreement); the real run: 33 destinations ok, both composed catalogues exempt with proof printed, the NIC's authored 60,112 B under the restored 65,536; `make gate` green (DERIVED-COUNTS 354 → 359 re-derived); `mdbook build` rc 0; `gen_book_index.py --check` rc 0 | the two-tier per-part rule landed: authored content keeps the ceiling, regeneration-gated derived members are exempt as a checked property via FACT-OWNERSHIP; the day-old interim raise reverted, the lesson promoted to a knowledge card |
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
| `.4` | `SEMULITH-P5-0017 (leaf P5-BOARD.4): the composition verdict — ACCEPTED, decided on every commit by BOARD-VERDICT; four dispositions as data; the 16-bit declaration measured false and narrowed` | board_verdict.py + check_board_verdict.sh (33rd doctrine, self-test 6/6); the marker param on 4 obligations; decision answers + hardware disposition mirror; the four dispositions decided (D32 high / SPEED_SEL pull-up, frozen counters, static-complete 100FDX scene, pin tie-offs 0); eth0 narrowed to 32-bit (§3.6 mode exclusivity), the pairing-latch census flipped; COMPOSITION-VERDICT.md + the book's verdict chapter; expectations re-pinned; the tree file archived-split at the per-part ceiling |
| — | `SEMULITH-P5-0016 (tree P5-BOARD)` | the `.4` design brief: the verdict's shape (mechanical core + authored analysis + a re-runner), four composition records not three, the OB-PLATFORM subtlety, MODEL-COMPOSE's open question answered for this board shape |
| `.12` | `SEMULITH-P5-0015 (leaf P5-BOARD.12): the two-tier per-part ceiling — authored content bounded, regeneration-gated derived members exempt as a checked property` | check_readme_routes.sh: closed REGEN_GOVERNORS set + set/driver assertion (refuses on drift), derived_exempt via fact_ownership.tsv, per-part loop judges every over-ceiling member; self-test 12 → 17 arms; profiles/ authored per-part back to 65,536; the lesson promoted to a knowledge card |
| — | `SEMULITH-P5-0014 (tree P5-BOARD)` | the `.12` ruling, director-delegated: the instrument must match the failure mode; decision_derived-members-of-bounded-families recorded; the day-old 128 KiB interim raise named for reversion; three alternatives rejected |
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
- `2026-10-02`: the `.12` ruling recorded (`SEMULITH-P5-0014`) — director-delegated
  ("yours to decision and act upon … SOTA, SIGNOFF and PRODUCTION-GRADE"): the
  per-part byte ceiling's founding failure mode (silent accretion in hand-maintained
  files) cannot occur in regeneration-gated derived files, so the instrument goes
  two-tier — authored members keep the ceiling, derived members are governed by their
  regeneration doctrine, exempt as a CHECKED property via the FACT-OWNERSHIP registry
  (closed regen set), never as a declaration. `decision_derived-members-of-bounded-
  families.md` carries the full ruling; `decision_profiles-family-composed-units.md`
  is superseded in part (its measurement stands; the day-old 128 KiB raise was the
  right interim). Three alternatives weighed and rejected (per-level raises, a
  lifecycle class, fingerprint-header detection). Frontier: `.12` execution — the
  two-tier gate, the registry row, the self-tests.
- `2026-10-02`: `.12` done (`SEMULITH-P5-0015`) — the two-tier per-part ceiling landed.
  `check_readme_routes.sh` carries the closed regeneration-doctrine set with a
  set/driver agreement assertion (drift refuses — the exemption can never silently
  widen), and `derived_exempt` resolves the exemption from the FACT-OWNERSHIP registry
  (mirror + regeneration governor — the one completeness-checked declaration; no second
  surface). The per-part loop now judges EVERY over-ceiling member (it previously
  inspected only the biggest): exempt members are reported as proof, the rest fail by
  name. Self-test 12 → 17 arms (17/0). On the real corpus the rule discriminates as
  ruled: both composed catalogues exempt with proof printed, the NIC's authored
  catalogue under the restored 65,536 authored ceiling; the day-old 128 KiB interim
  raise reverted (`decision_profiles-family-composed-units` superseded in part). The
  lesson PROMOTED: `docs/knowledge/a-byte-ceiling-applies-to-authored-content.md` —
  the instrument must match the failure mode. Frontier: `.4` — the composition
  verdict.
- `2026-10-02`: the `.4` design brief recorded (`SEMULITH-P5-0016`). The verdict's shape:
  the mechanical discharge (green today, 8/8 — but its platform-dependent edges land on
  `OB-PLATFORM`, the laboratory guarantee) re-established on the board by the declared
  `satisfies` edges plus FOUR composition dispositions, decided: D32 strapped (32-bit
  native mode — and a measured defect fixed with the leaf: eth0's declared 16-bit width is
  mode-exclusive per §3.6 and drops), SPEED_SEL unwired to its pull-up, the NIC time
  sources frozen, the replay link scene static-complete at 100BASE-TX FD, the pin reads
  tied off at 0. The machinery: a `composition_disposition` marker param, an `answers`
  edge on board decisions, the dispositions mirrored into hardware.sexp, and the
  BOARD-VERDICT doctrine re-deciding the verdict on every commit — an unmatched assumption
  is a rejection by name, never a note. MODEL-COMPOSE's open question (an operator beyond
  union + discharge?) answered for this board shape: none needed. Frontier: `.4`
  execution.
- `2026-10-02`: `.4` done (`SEMULITH-P5-0017`) — the composition verdict: **ACCEPTED**,
  and decided on every commit by the 33rd doctrine, BOARD-VERDICT (`board_verdict.py` +
  `check_board_verdict.sh`, self-test 6/6 with every RED asserting its reason): 8/8
  assumptions discharged, 3/3 `satisfies` edges resolved, 4/4 board-deferred obligations
  bound to exactly one decision `answers` edge — an unmatched assumption or a dangling
  edge is a rejection by name. The machinery: the `composition_disposition "required"`
  marker (`OB-NIC-STRAP-RESETS` joined the three `.10` records), the `answers` edge on
  board decisions, the dispositions mirrored into `hardware.sexp`. The dispositions
  decided: D32 tied high + SPEED_SEL at its pull-up; the NIC time sources frozen; the
  replay link scene static-complete at 100BASE-TX FD (BSR `0x782D`); pin reads tied off
  at 0. Measured in execution, fixed at root: eth0's declared 16-bit width is
  mode-exclusive per §3.6 — narrowed to 32, the pairing-latch census flipped; the
  expectations re-pinned where the verdict determines values. The authored verdict
  (`COMPOSITION-VERDICT.md` + the board book's verdict chapter) carries the
  per-assumption table, the `OB-PLATFORM` note, and the interface-test leg
  (`make check` + smoke green — the RAM half; the MMIO halves attach with the device
  models, named). DERIVED-COUNTS re-derived (33 doctrines, 365 arms). The tree file
  itself crossed the per-part ceiling at this leaf — handled by the house's own
  instrument: the older completed leaves' design briefs and checklists archived verbatim
  to `docs/tasks/archive/P5-BOARD.md` (the split, not a raise). Frontier: `.6` — the
  platform capability manifest.
