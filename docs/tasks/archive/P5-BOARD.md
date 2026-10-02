# P5-BOARD — archived completed-leaf design briefs and acceptance checklists

The recorded-before-execution design briefs and the filled acceptance checklists of the
older completed leaves of the [`P5-BOARD`](../P5-BOARD.md) tree, split from
`P5-BOARD.md` on `2026-10-02` when the tree file crossed the per-part ceiling
(131,072 B) at leaf `.4`. The ceiling was obeyed by the split, not raised — the
`docs/tasks/` precedent (`archive/P2-SCALAR.md`, `archive/P2-SCALAR-designs.md`).
Archived verbatim; the live tree keeps the recent leaves and a pointer here.

## Archived Decisions entries (2026-09-13; the `.1`, `.2`, `.10`, `.11` design briefs; the `.1` execution amendments)

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


## Archived Acceptance Checklists (leaves `.11`, `.10`, `.2`, `.1`, `.9`, `.8`)

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

