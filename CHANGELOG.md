# CHANGELOG.md

## SEMULITH-MCU-0002 (leaf MCU-DOCS.2) — the channel's twelve answers reconciled: the MCU documentation set acquired and digest-verified

- Verified live first: `build_responses.py --report` → **12 fulfilled / 0 blocked**, exit 0.
  The routes, measured by the channel: the Cortex-M TRMs from Arm's documentation-service
  API; FE310 from the SiFive CDN; MSP430 direct from ti.com; i.MX RT / SAM D21 / STM32 from
  Wayback captures of the official URLs (the live URLs 404/403/reset automated clients —
  measured routes, recorded in the answers' evidence); the three M-profile ARMs and the
  RP2040 datasheet already held corpus-side.
- Twelve materials adopted into `materials/catalog.sexp` (the three M-profile ARMs, three
  Cortex-M TRMs, FE310, i.MX RT1050 RM, MSP430FR59xx UG, SAM D21, STM32 RM0394 + PM0214)
  and fetched into `.materials/mcu/` with every sha256 re-verified — `materials --verify:
  64 verified / 0 unresolved` (52 at P5-BOARD.9 + the twelve). The corpus re-pinned
  `c4ad8a2` → `3dc4e62` (302 PDFs; 293 at the prior pin). All twelve requests marked
  `resolved` with their evidence.
- **Measured defect, fixed at root:** the `.1` survey measured the corpus's
  semulith-facing proposals feed only — the RP2040 datasheet was already adopted in our
  own catalog since 2026-09-14 (same sha256, cached), so one request was redundant from
  filing. No duplicate record adopted; the survey knowledge card gained the three-layer
  "already held" rule (tracked catalog + fetch cache + corpus tree, not just the feed).
  The tree closes (2/2).

## SEMULITH-MCU-0001 (leaf MCU-DOCS.1) — the MCU documentation set surveyed and requested through the chipdoc channel

- The director's `2026-10-02` steer (ARMs carry full MCU documentations; other vendors
  too — ask chipdoc) executed as documentation research, ahead of any MCU milestone
  (none owns MCU modeling yet — stated, not hidden). New tree:
  [`MCU-DOCS`](docs/tasks/MCU-DOCS.md).
- The survey measured the LIVE corpus feed (corpus `c4ad8a2` working tree, read-only):
  held — ESP32/C3/S3 and RP2040/RP2350 SVD register maps, the nRF52840 PS, the AM335x
  TRM (a Cortex-A8 SoC, not an MCU), the Arm PrimeCell/AMBA/GIC set (Cortex-A class);
  absent — every Arm M-profile architecture manual, every Cortex-M TRM, every vendor
  MCU datasheet/RM beyond the held trio.
- Twelve requests filed in `materials/requests.sexp` (the preferred channel): the three
  M-profile ARMs (v6-M/v7-M/v8-M), three Cortex-M TRMs (M0+/M3/M4), and six vendor
  documents (RP2040 datasheet, STM32 RM + PM0214, SiFive FE310, i.MX RT1050 RM, SAM
  D21, MSP430FR59xx). Pickup measured: the poller (read-only) reports exactly the
  twelve new ids, rc 1. One authoring defect (a heredoc paren over-close) caught by the
  one reader before landing — parse gates work.
- Fulfilment is chipdoc-side and asynchronous; a `MCU-DOCS.2` reconciles the answers
  when they arrive (the `P5-BOARD.9` pattern).

## SEMULITH-BA-0002 (leaf BOOK-APPARATUS.2) — the reading-experience audit pass: 29 main-line chapters, 16 kept / 13 revised; the yield was factual drift

- The first audit pass over the project book against
  [`decision_mdbook-incremental-engaging`](docs/decisions/decision_mdbook-incremental-engaging.md):
  six parallel chapter-group audits (the decision's four criteria operationalized), every
  flagged item re-verified against the repository before any edit. The per-chapter
  dispositions are recorded in [`docs/tasks/BOOK-APPARATUS.md`](docs/tasks/BOOK-APPARATUS.md).
- **Twelve stale facts fixed at their lines** (each measured): `claim-scope.md` (four crates,
  not three; the CPU-LAB self-contradiction; the 48+1-program corpus, not forty-one),
  `plan/p0.md` (the contract is 36 obligations / 72 checks — the quote now matches the
  regenerated G0-REPORT it claims to quote), `plan/p1.md` (G1 reads `passed` since
  2026-09-30; 48 guests / 642 steps), `plan/p5-p7.md` (registration day is done),
  `docs/ARCHITECTURE.md` (28/36/28 records), `docs/RISKS_AND_DECISIONS.md` §2 (four
  current-state rows updated with measured states and dates — the column whose point is
  tracking change), `docs/SOURCES_AND_NAMING.md` (the crates exist; the reservation claim
  narrowed), `LIVE_STATUS.md` ("1 unit today" → 5).
- **Three record violations revised**: the gates overview's duplicated sentence dropped;
  `plan/p3.md`'s 68-line leaf-by-leaf update chain collapsed to a final-state paragraph
  (both measured incidents kept; the tree carries the blow-by-blow); P7's cold mechanism
  open gained its why-sentence. Terminology pointers added where a concept was leaned on
  without introduction (F3/F6 → `docs/tasks/DSP-REVIEW.md`; CLINT glossed; the P3 forward
  reference named).
- **Two ` ```mermaid ` blocks rendered as raw source in the book** (no preprocessor) —
  replaced by text-rendered flows; `mdbook-mermaid` deliberately NOT added (an
  unsanctioned dependency is worse than a plainer diagram).
- The book builds; the index regenerates clean (`gen_book_index.py --check` rc 0);
  `make gate` green. The BOOK-APPARATUS tree closes (2/2).

## SEMULITH-P5-0011 (leaf P5-BOARD.11) — registration day: the three units register; the materials-bill machinery goes route-keyed by declaration

- `materials/units.sexp` now registers five units: `netboard-lab-v0` (kind `board`),
  `sifive-uart-lab-v0` and `lan9118-lab-v0` (kind `device`) beside the two processors —
  the schema's sanctioned "(values …) edit the day a real unit needs one":
  `schema/units.sexp` kind +board/+device, the shared layer taxonomy +device.
- The materials-bill machinery is **route-keyed by declaration**
  (`gen_model_book.unit_shape`: `board.sexp` present → board; the profile's vehicle
  route otherwise — never a guess): per-shape internal-contracts censuses (devices carry
  `expectations/`, the board carries `board.sexp`+`DOSSIER.md`), route-honest fragment
  content (a device has no encoding space and pins no reference models — the fragments
  say so), and `check_materials_bill.sh`'s COMPLETENESS keyed on the same shape. The
  pre-fix refusal was re-run from the parent commit and measured (`REFUSED —
  references.sexp: the pinned document is missing`); the two processor books' fragments
  regenerated byte-identical modulo the embedded generator hash. Four new self-test
  arms pin the device and board shapes (MATERIALS-BILL 11/11).
- The three per-unit books land under `docs/models/<unit-id>/` — authored chapters
  (devices: introduction / materials bill / gaps / methodology / evidence; the board:
  the composition narrative as its method, no evidence chapter until `.4`) with the
  generated fragments; UNIT-BOOKS 5/5 build, MATERIALS-BILL 5/5 (every material states
  what it does not supply), SCOPE-COVERAGE `5 unit(s) may code` over the 72 new census
  rows (the board's absences are `out-of-scope` WITH their contract reasons — never
  `missing`).
- Measured and corrected at execution: the BREADTH report's stale "2 registered units"
  prose was the **generator's** hardcoded string — fixed at `gate_report.py` (the count
  and the processor-units claim now derive), the report regenerated (5 units, verdict
  still `passed`); the project book's `models.md` updated to five units;
  DERIVED-COUNTS' self-test-arm total re-derived 341→345 by its enumerator.
- FACT-OWNERSHIP carries the book-side mirrors (46 fact kinds). The P5 frontier is
  `.3` (generated maps) then `.4` (the composition verdict — the devices' composition
  records are pre-wired to it).

## SEMULITH-P5-0009 (leaf P5-BOARD.10) — the second device dossier: `lan9118-lab-v0`, fully gated with no machinery edit; the per-part bound bites

- The LAN9118 NIC dossier lands under
  [`profiles/lan9118-lab-v0/`](profiles/lan9118-lab-v0/DOSSIER.md): the DS00002266B-pinned
  source (digest re-verified from the materials cache), 52 requirements (46 defined + the
  reserved/unspecified/implementation-defined silences and deferrals), 52 mirrored
  obligations (contract `lan9118-v0` v0, `device-guarantee`), the state document (49
  registers across three indexing levels + 4 FIFO families + the earned hidden-state
  census — the model additionally carries the TX command-parser state and the 16-bit
  pairing latch), 52 verbatim decision mirrors (generated from requirements.sexp
  mechanically — drift impossible by construction, refused by gate regardless), and 3
  datasheet-derived expectation documents (cold-reset reads; exact TX free-space
  accounting; the recorded-trace RX path) recorded **before any model exists**.
- **No machinery edit**: `.2`'s generalization by declaration covered the NIC — the
  gates attach by glob and derive device applicability from the `vehicle` declaration.
  The mechanical re-pins: FACT-OWNERSHIP +6 registry rows and fixture re-pins
  (`7→8`, `3→4`); the `profiles/` bound re-derived 4× → 5×
  ([`decision_profiles-family-five-units`](docs/decisions/decision_profiles-family-five-units.md))
  — where the **per-part bound bit for the first time** (32→64 KiB; the mirror
  discipline on a 52-record contract puts the largest catalogue at 60,112 B).
- Measured in execution, recorded at root: the two `pdftotext` modes disagree on
  Table 5-1's Default column (per-register sections are the authority, arithmetic
  cross-checks agree); §3.11's reset completion times render as `2 s`/`100 s` in the
  PDF's **own text layer** (hexdump-verified µ mis-mapping — only cleanly stated figures
  pinned); PHY ID2's model/revision nibbles are blank in the datasheet; ADDRH/ADDRL's
  Table 5-6 defaults sit beside §5.4.2's "undefined until loaded" — both recorded,
  nothing guessed. The lesson is promoted:
  [`a-pdf-text-layer-is-not-the-page`](docs/knowledge/a-pdf-text-layer-is-not-the-page.md).
- The design brief's sharpest finding is now contract data: the NIC's guest-readable
  time sources (`REQ-D-NIC-TIME-SOURCES`), the wire-domain PHY link scene under replay
  (`REQ-D-NIC-PHY-LINK`) and the pin tie-offs (`REQ-D-NIC-GPIO-PINS`) pre-wire
  `P5-BOARD.4`'s composition verdict. Registration day (`.11`) is next.

## SEMULITH-P5-0007 (leaf P5-BOARD.2) — the first device dossier: `sifive-uart-lab-v0`, fully gated; the machinery generalized by declaration

- The SiFive UART dossier lands under
  [`profiles/sifive-uart-lab-v0/`](profiles/sifive-uart-lab-v0/DOSSIER.md): the §13-pinned
  source (digest re-verified from the materials cache), 19 requirements (13 defined + 6
  measured silences — Reserved bits, X-marked resets, FIFO reset, off-map/non-32-bit
  accesses, the watermark mode), 19 mirrored obligations under contract `sifive-uart-v0`
  v0 with the schema's new third direction `device-guarantee`, the state document with
  its earned hidden-state census (registers + FIFO contents/occupancies, nothing else
  MMIO-visible), 19 verbatim decision mirrors, and 3 datasheet-derived register-read
  expectation documents recorded **before any model exists**.
- The dossier machinery generalized **by declaration, not exemption**
  ([`decision_device-applicability-by-declared-vehicle`](docs/decisions/decision_device-applicability-by-declared-vehicle.md)):
  `vehicle (route device-model) (comparison register-expectations)`; `profile.sexp`'s
  processor-only fields optional; `mmio_registers` scope; `expectations.sexp`
  entry/instructions optional; EXTRACTION / EXERCISE-COVERAGE / INTERACTION-MATRIX derive
  device applicability with contradiction = RED; a device-guarantee discharges a CPU
  assumption by construction (pinned GREEN arm); PROFILE-CONSISTENCY needed no
  conditional (measured by a new self-test arm).
- Measured in execution, fixed at root: the §13.8 watermark bits' level-vs-hold gap
  (`REQ-D-UART-WM-MODE` — expectations pin a bit only when its raised condition holds
  under every reading); the `REQ-U-` id prefix colliding with RECORD-SCHEMA's mechanical
  decision→requirement mapping (renamed); the interaction-matrix n/a note counted as a
  cell (fixed); FIFO resets recorded as "unspecified" data rather than weakening the
  every-element-a-reset contract.
- FACT-OWNERSHIP re-pinned to three units (registry + fixtures); the `profiles/` bound
  re-derived 4× ([`decision_profiles-family-four-units`](docs/decisions/decision_profiles-family-four-units.md)).
  Registration of all three units consolidates into `.11`; the LAN9118 dossier is `.10`.
- Validation: all dossier documents schema-validate; the three profile-glob gates decide
  the device by declaration; every edited check's self-test green (17/9/14/41/7/14/10
  arms, 0 fail); `make gate` all doctrines green; the mdBook builds.

## SEMULITH-PKG-0017 (leaf SEMULITH-PKG.9) — the policy note's provenance triple now re-derives from the note

- Session-start policy check (§14/§17/§18), measured live: `README_POLICY.md`'s neutral
  body is byte-identical to the originating project's current revision (no unadopted
  upstream change), and `docs/CLAIM_VERIFICATION.md`'s recorded source SHA-256
  (`9f99df25…6046bd`) matches the pgen source exactly. Nothing to re-adopt.
- One defect found and fixed: the policy adoption note's recorded SHA-256 / line / byte
  triple did not state its digest span, so it failed to reproduce as written (the measured
  span trims leading blank lines and the `---` separator). The note now states the span;
  the re-deriving command lives in task leaf `SEMULITH-PKG.9`; the recorded
  `77a1e934…c0182d6eefec` / `159 / 8,279` reproduces exactly.
- `SEMULITH-PKG` complete (9/9). Validation: `scripts/check_doctrines.sh` all green.

## SEMULITH-P5-0005 (leaf P5-BOARD.1) — the platform specified: `netboard-lab-v0` pins versions, not names; the 16550 label measured false and corrected

- The first board's canonical definition lands: [`profiles/netboard-lab-v0/board.sexp`](profiles/netboard-lab-v0/board.sexp)
  under the new [`schema/board.sexp`](schema/board.sexp) — the first non-processor
  source-of-truth schema (DOSSIER-SCHEMA pairs them by basename) — narrated by
  [`profiles/netboard-lab-v0/DOSSIER.md`](profiles/netboard-lab-v0/DOSSIER.md).
- Every pin is a version, never a name (OWN-05, the leaf's acceptance): the processor by
  unit id + version `0` + the GATE-REPORT-gated dossier content digest; each device by its
  datasheet's material id + revision + sha256. The memory map (2 GiB RAM at the harness's
  existing base, the UART at the sourced FU540 instance address, the NIC in the datasheet's
  256-byte direct-register span), cold-only reset, and the serial console are data.
- Timers and interrupt controllers are **absent by contract** — declared as data with their
  reasons and the obligations they satisfy (`OB-ENV-VIRTUAL-TIME`, `OB-ENV-EVENT-DELIVERY`);
  a CLINT/PLIC would be a composition rejection, not a feature. `satisfies` fields pre-wire
  `.4`'s composition verdict. Both devices' interrupt lines unconnected-and-declared;
  drivers poll. The NIC backend is recorded-trace replay RX / recording-sink TX.
- **Measured defect, found and fixed in execution:** the design brief's "16550-compatible
  UART" label is false against the pinned source — zero occurrences of "16550" in
  FU540-C000 v1p5 (`pdftotext` census); §13 documents the SiFive UART. The source pin was
  the intent: the board adopts the SiFive UART, `materials/catalog.sexp`'s supplies text is
  corrected, and the correction is recorded as `D-BOARD-UART-KIND`.
- Scope routing: board-unit registration (`materials/units.sexp`, the `kind` edit, the
  per-unit book) lands with `.3` — registration day carries the UNIT-BOOKS /
  MATERIALS-BILL / generator consequences, which are not a specification's to bear.
- The `profiles/` family's third unit directory: the bound re-derived to 3× by the standing
  arithmetic ([`docs/decisions/decision_profiles-family-three-units.md`](docs/decisions/decision_profiles-family-three-units.md));
  the board-definition fact kind registered in `doctrine/fact_ownership.tsv`.
- Validation: both schema validations ok; every pin re-derived from its source artifact;
  `make gate` green; `mdbook build docs/book` rc 0.

## SEMULITH-BA-0001 (leaf BOOK-APPARATUS.1) — the book's index: generated from the book's own text, gated against drift

- The director's `2026-10-02` apparatus directive audited against the real book: glossary
  present and unforkable (build-time `{{#include}}` of the canonical `docs/GLOSSARY.md`),
  two annexes present and on-policy — the **index was absent**. It lands derived, the only
  honest shape for a fact about a changing population: `scripts/gen_book_index.py` reads
  `SUMMARY.md` + the canonical glossary + the acronym table + every chapter's text;
  `docs/book/src/index.md` is what that derives (15,019 B, 40 terms).
- New project doctrine #31 **`BOOK-INDEX`** (`scripts/check_book_index.sh`): the index
  regenerates byte-exact or the commit fails — a hand-maintained index is a running total,
  and a running total is a memory of a measurement, not a measurement. Six self-test arms,
  fired RED before registration (DRIFT ×2, refusal-by-name ×2). Registered and mirrored
  (`DOCTRINE_ENFORCEMENT.md`, the book's doctrine chapter, `TOOLBOX.md`,
  `doctrine/fact_ownership.tsv`).
- The annex policy is stated in the book's introduction: chapters stay readable; what is too
  technical for the main line lives in an annex.
- The directive's second half became durable: `decision_mdbook-incremental-engaging` +
  `BOOK-APPARATUS.2` (the reading-experience audit). The TOC request was withdrawn by the
  director — the mdBook sidebar is the TOC; the contents page built for it was reverted.
- Defect fixed at root, not reported: the generator's printed term count was a fudge factor
  (read `47` against the real `40`); it now derives from the emitted rows.

## SEMULITH-MP-0001 (leaf MEMORY-POINTER.1) — MEMORY.md slimmed to the §6 next-action pointer

- The director's `2026-10-02` ruling executed: `MEMORY.md` exists solely to point at the next
  action, overwrite-only per `MEMORY_ARCHITECTURE.md` §6. Measured before: 34 lines / 7,031 B
  (97% of the hard cap; health 30 / 1,792). After: **29 lines / 1,865 B**.
- The audit verified every dropped line's durable home (trees, `docs/decisions/`,
  `docs/knowledge/`, TOOLBOX, git's submodule pin); exactly one ruling was dangling —
  `document EVERYTHING` (2026-10-01) — backfilled as `decision_document-everything`. The
  ruling itself is `decision_memory-next-action-pointer`.
- Gate lesson recorded: `TREE-CLAIMS` scans the `Active trees:` claim PER PHYSICAL LINE — the
  first slim draft wrapped the list and fired `MISSING ACTIVE`; the list stays on one line.

## SEMULITH-DS-0004 (tree DOC-SHARDING) — the append heads shard ahead of the next slice

- Trigger: `CHANGELOG.md` at 65,035 of 65,536 bytes (501 headroom) and `DEV_NOTES.md` at
  49,000 of 49,152 (152) with the next slice's entries already measured larger than the
  remaining room — the designed fire point, answered by sharding, never by raising the cap.
- `shard_history.py --max-bytes 63488`: 2 entries → `docs/changelog/shard-0113.md`,
  completeness `54 == 52 kept + 2 moved` order-and-bytes exact, head 65,035 → 62,570.
- `shard_history.py --head DEV_NOTES.md --max-bytes 46080`: 3 entries →
  `docs/changelog/shard-0114.md`, completeness `35 == 32 kept + 3 moved` exact, head
  49,000 → 45,633. Manifest 114 → 116 rows.

## SEMULITH-AC-0056 (tree ARTIFACT-CLEANUP) — the 2026-10-02 §8 cleanup: 105 incremental caches, 139 MB

- Time-triggered §8 run (the `2026-10-01` run was a full day old): 105 cargo
  incremental-cache `.bin` files deleted (139 MB), every one under a cargo
  `*/incremental/*` directory of `target/` (84 the project's own debug profile, 21
  wasm32) — exactly the enumerated safe scope; post-delete re-census 0; `target`
  4.0 G → 3.9 G; `.app-data` unchanged at 1.4 G.
- 0 stray `.bin`/`.log` in `target/release` / `target/debug/deps`; no
  `target/refs/*.log` present this run; the 7 cargo-home crate test fixtures kept
  by policy (inputs, not artifacts). `docs/ARTIFACT_CLEANUP.md` overwritten with
  the one-line record.

## SEMULITH-P5-0003 (leaf P5-BOARD.9) — the chipdoc answers reconciled: five adopted, five measured negatives

- Verified live first: `build_responses.py --report` → 5 fulfilled / 5 blocked, exit 0
  (every open request answered — the second incident's gap, closed by CHANNEL.md
  §0.3/§0.5, re-read `2026-10-01`).
- The five fulfilled adopted as catalog materials — `MICROCHIP-LAN9118` (the wired-NIC
  primary), `UBLOX-SARA-R4-AT` (the cellular AT primary), `ESPRESSIF-ESP-AT`,
  `NORDIC-NRF52840-PS`, `MICROCHIP-AT86RF233` (the two true RFICs) — fetched into
  `.materials/network/`, every sha256 re-verified (`materials --verify: 52/0`); the
  corpus re-pinned `c4ad8a2` (5696 files / 293 PDFs, the same census).
- All ten requests marked: five `resolved`, five `blocked` — each blocked a MEASURED
  NEGATIVE with its consequence named (e1000/RTL8139 → LAN9118 is primary; EC25/
  SIM7600 → SARA-R4 is primary; the AR9271 probe's negative IS its answer: no public
  register-level WiFi baseband documentation exists). Never re-filed without a new
  route. `P5-BOARD.1` inherits five sourced candidates plus five closed alternatives.
- The knowledge cards carry the ask→answer loop end-to-end
  (`the-chipdoc-request-channel.md` refreshed with the §0.3/§0.5 answer path;
  `the-chipdoc-channel.md` updated and cross-linked).

## SEMULITH-BR-0021 (leaf P3-BREADTH.6) — gate BREADTH runs: verdict passed; the capability report published

- `scripts/gate_report.py` gained the cross-unit builder (`--gate BREADTH`): the three
  roadmap axes measured from tracked files by concrete artifact name — axis 1 the
  subset's six evidence anchors (declared scope + vehicle, the `.a56` corpus, 17
  crate tests, the driver, the comparison contract, the registered mechanism), axis 2
  nine abstraction constructs DECLARED in their schema AND CARRIED by the mapping
  owner with the refusal boundary pinned (5 synth probes), axis 3 the registry as the
  complete claim list — **TI C6000 and ADI SHARC unclaimed explicitly**, everything
  else by omission. No code path to `passed` over an absent anchor (EVD-08).
- The report publishes at `docs/BREADTH-REPORT.md` — a cross-architecture gate cannot
  be owned by a profile directory — and `check_gate_report.sh` gained the repo-level
  leg: same regenerate-never-edit enforcement, same controls (self-test 12/12; 4
  reports in sync, G0/G1/GC byte-identical).
- `P3-BREADTH` **CLOSED 8/8** — the stable-API claim is permitted exactly where the
  report permits it (the exercised cases of the two registered units); `.1` stays
  `slice-gated` on the record, its TI/VLIW legs reopening by name.

## SEMULITH-BR-0020 (leaf P3-BREADTH.6) — the second unit registered; its book stands; the per-part ceiling rises by ruling

- `materials/units.sexp` gained `dsp56300-lab-v0` (the second unit; C17 in / C14 out
  against rv64i's requires set — reset is this unit's own decision, interrupts a named
  exclusion) and the 24-row category-needs census landed (8 covered / 6 partial /
  3 missing-with-closings / 4 out-of-scope / 3 deferred-to-board).
- `scripts/gen_model_book.py` learned the sibling-crate shape — three extensions, each
  naming the DSP case (the declared-vehicle encoding fragment; `encoding.sexp` as the
  one document a sibling-crate unit may lack, its row naming the deferred lane; register
  families / spaces / the `.a56` census where the rv64 shapes are absent). rv64i
  regression byte-exact: only the generator-digest header line moved.
- The book `docs/models/dsp56300-lab-v0/` stands (six chapters, the bill's 12 sections
  each with its does-not-supply); UNIT-BOOKS, MATERIALS-BILL and SCOPE-COVERAGE all
  green with 2 units; four fragment mirror rows registered (FACT-OWNERSHIP 29 kinds).
- **Director ruling (`2026-10-01`): task-tree growth is ALLOWED** — the docs/tasks/
  per-part bound rose to 128 KiB (`decision_task-tree-per-part-growth`) after six forced
  archive operations in one day taxed active slices; the aggregate bound and the archive
  lifecycle are unchanged, and a bound remains — a file stays readable in one sitting.

## SEMULITH-BR-0019 (leaf P3-BREADTH.6) — the DSP's contract records land governed; the fixture noticed

- `profiles/dsp56300-lab-v0/` gained `requirements.sexp` (seven records, statements
  byte-identical to the profile's decisions) and `contract-obligations.sexp` (thirteen
  obligations — seven mirrors plus six environment-assumptions; contract
  `dsp56300-lab-env-v0`; 26 declared checks). RECORD-SCHEMA attached on landing with zero
  gate edits (auto-discovery; 10 record files green on the first pass); FACT-OWNERSHIP
  gained the DSP's two registry rows.
- FACT-OWNERSHIP's GREEN self-test fixture went RED on the landing BY DESIGN — its pair
  glob follows the real corpus, and the fixture registry still named a one-unit world
  (`UNREGISTERED MIRROR PAIR`). Re-pinned to the two-unit corpus (`__CHECKED__ 5 → 6`),
  the reason recorded in the check's comment.
- Validation: both catalogues schema-validate; RECORD-SCHEMA, FACT-OWNERSHIP (25 kinds,
  self-test 10/10) and `make gate` all green; the rv64i catalogues byte-untouched. The
  DOSSIER's records row reads present; `.6` continues with slice 2 (the BREADTH report).

## SEMULITH-P5-0002 (leaf P5-BOARD.8) — the network-connected board's documentation researched; ten requests filed, the channel measured

- The `2026-10-01` design discussion (boards that touch the world) turned into a measured
  documentation position ahead of `P5-BOARD.1`'s board choice. The corpus survey (the
  snapshotted chipdoc feed, corpus `92a73b6`) measured the holdings: a complete
  register-level Ethernet MAC+PHY contract (TI-DP83816), ESP32/C3/S3 register maps, the
  SiFive FU540/FU740 manuals and HiFive board docs, the TI AM335x TRM — and the recorded
  negative: no standalone Cadence GEM / DesignWare GMAC spec is public.
- Ten acquisition requests filed in `materials/requests.sexp` (the preferred channel),
  each naming its consumer: wired NICs with QEMU precedents (LAN9118, Intel 82540EM,
  RTL8139), three LTE modem AT manuals (Quectel EC25, SIMCom SIM7600, u-blox SARA-R4),
  the WiFi-module command surface (ESP-AT), two register-documented radios for the
  true-RFIC leg (nRF52840, AT86RF233), and one honest probe (AR9271 register docs,
  expected absent). Pickup measured: chipdoc's poller (run read-only) reports exactly
  the ten new ids, rc 1.
- The channel's filing mechanics are now recorded semulith-side as a knowledge card
  (`docs/knowledge/the-chipdoc-request-channel.md` + INDEX) — they had lived only in the
  corpus-side manual, and a session re-derived them the hard way once.

## SEMULITH-BR-0018 (leaf P3-BREADTH.7) — the dsp56300-lab-v0 dossier lands, governed

- The three schema-validated documents moved from
  `docs/tasks/artifacts/p3-breadth/dsp56300-dossier/` to `profiles/dsp56300-lab-v0/`
  (rename lineage kept; headers rewritten from "NOT LANDED" to the landed gate map):
  `profile.sexp` (the subset decisions + the vehicle declaration), `state.sexp` (the F6
  census as data), `interactions.sexp` (6 axes, 21 cells).
- Every attaching gate green WITH the documents landed: EXERCISE-COVERAGE (19/19 DSP,
  52/52 rv64), EXTRACTION (sibling-crate route reported), INTERACTION-MATRIX (2 units —
  the DSP's 21 cells re-derived and resolved), PROFILE-CONSISTENCY (2 dossiers),
  DOSSIER-SCHEMA (62 validated, 2 skipped by name), FACT-OWNERSHIP (23 kinds — the DSP's
  five rows landed; the two post-landing census arms prove same-unit pairing, 10/10).
- The DOSSIER's rows now read present/deferred with owners; the stale "lands with the
  model slice" wording for requirements and unit registration re-routed to
  `P3-BREADTH.6`. `.7` DONE 3/3; the frontier is `.6`, the BREADTH gate report.
- Bookkeeping: `.7` slice 1's checklist archived verbatim (the 64 KiB per-part held).

## SEMULITH-BR-0017 (leaf P3-BREADTH.7) — the vehicle declaration, the DSP matrix, and the DOSSIER-SCHEMA gate

- The `.7` disposition, decided (director-delegated) and recorded in
  `decision_gate-applicability-by-declared-vehicle`: gates derive per-unit applicability
  from a declared `(vehicle (route …) (comparison …))` plus the unit's documents.
  Deferral machinery rejected (a weakening surface built for one unit); the full
  evidence-shape fiction rejected (artifacts the claim never cites). A declaration
  contradicting the documents is a finding — a stale declaration fails, never drifts.
- `schema/profile.sexp` gains the optional `vehicle` block (closed enums:
  `generated-definition|sibling-crate`, `per-step-trace|checkpoint-end-state`);
  `dossier_sexp` carries it both directions. EXTRACTION's sibling-crate leg reports the
  route by name and refuses a contradicted declaration; EXERCISE-COVERAGE's checkpoint
  leg runs the `.a56` guest census BOTH directions (UNEXERCISED / UNDECLARED EXERCISE)
  and makes the composition leg n/a exactly while no `encoding.sexp` exists.
- The DSP's `interactions.sexp` stands drafted (6 axes — progress, stop, loop, stack,
  alias, state; 21 cells, mechanism/degenerate dispositions): measured with the drafts
  placed — `21 cells declared, every disposition resolves`, the gate ok on 2 units. The
  closed mechanism registry gained `dsp56300-smoke-agreement` and `dsp56300-typed-stop`,
  each naming its case.
- **DOSSIER-SCHEMA registered (the 30th doctrine)**: every tracked dossier document with
  a same-named (or family) schema validates through the one checker — 64 validated, 2
  skipped by name; fired RED before registration against the pre-fix D-FENCE document
  recovered from git history (the exact drift class it exists to catch).
- FACT-OWNERSHIP's second-unit fix: the corpus census enumerated restatement pairs as a
  cross product — exact with one unit, inventing cross-unit pairs with two. Now same-unit
  pairing for `profiles/*/` patterns and registry-nominated cross-family pairs with a
  restater-participation census; fact kinds qualified per unit. Self-test 8/8 unchanged
  (the single-unit regression control).
- Measured against the real DSP drafts: **EXERCISE-COVERAGE ok — 19/19 declared forms
  exercised**; EXTRACTION ok (sibling-crate route named); PROFILE-CONSISTENCY ok (2
  dossiers). rv64 behavior byte-untouched (52/52; self-tests 13/13, 5/5). Slices 1–2
  share this commit: the derived counts measure the working tree, so the co-developed
  halves could not pass the hook separately. Bookkeeping: `.5` slice-3's checklist and
  `.4`'s slice narratives archived verbatim; shards 0100/0101 (completeness exact);
  DERIVED-COUNTS re-derived to 30 doctrines / 323 arms.

## SEMULITH-BR-0016 (leaf P3-BREADTH.5) — the encoding case measured; .5 closes, the landing is leaf .7

- The encoding/definition generalization was MEASURED, not asserted: `gen_definition.py`
  refuses a second unit at three named walls (the profile scope, the 32-bit-only decode
  table — the DSP fetches 24-bit words, and the semantics corpus — the DSP's semantics
  are hand-written Rust, not data), and the semantics language is scalar-shaped (31
  operators censused in `schema/semantics.sexp`: load/store carry no space parameter,
  state access is `reg`/`pc` only, no masked-width wrap, no loop construct — the DSP's
  X/Y/P moves and do/rep machinery would refuse by name).
- Decision: the generalization is a LANE, not an extension, and no current milestone
  consumes it (`decision_lane-consumption`; the sibling crate is the exercised,
  differentially agreed vehicle) — DEFERRED with named reopening conditions: a corpus
  extension beyond subset v0, a third unit, or the landing leaf choosing the machinery
  route. **`P3-BREADTH.5` DONE 3/3** — every landed extension names dsp56300-lab-v0 and
  its case; the one case measured and not built names its conditions.
- The dossier landing is new leaf `P3-BREADTH.7`: it owns the measured attachment table
  (PROFILE-CONSISTENCY green; the three evidence-shape gates RED on rv64-shaped
  presumptions), the disposition choice (named deferrals vs machinery), and the surfaced
  dossier schema-validation leg. The DOSSIER's deferral rows name it.
- Bookkeeping: `.5` slices 1–2's checklists archived verbatim to
  `docs/tasks/archive/P3-BREADTH.md` as the leaf closed — the 64 KiB per-part ceiling
  held.

## SEMULITH-BR-0015 (leaf P3-BREADTH.5) — the scope taxonomy generalizes; the DSP dossier drafted, attachment measured

- `schema/profile.sexp`: the DSP's five scope groups (moves/alu_core/multiplies/flow/loops)
  as named optional fields; `xlen`, the integer-file scalars and `count_rv64i_additions`
  optional — each naming dsp56300-lab-v0 as its case. No gate reader changed: they were
  already generic over group names. `dossier_sexp._SCOPE_LISTS` extended alongside (the
  two closed places the taxonomy lives).
- The DSP's `profile.sexp`/`state.sexp` stand DRAFTED and schema-validated under
  `docs/tasks/artifacts/p3-breadth/dsp56300-dossier/` — the 19-mnemonic subset scope, five
  register families with parts and readouts, three memory spaces, the hardware stack,
  twelve special registers, and the 14-candidate census carried as data; both load through
  the mapping owner and round-trip data-equal.
- The landing was MEASURED (untracked + intent-to-add placement, gates run in their
  committed modes): PROFILE-CONSISTENCY passes the DSP dossier — after the measurement
  surfaced seven latent `references.sexp` defects no gate had been checking, all fixed
  (an `obtained` candidate without binary/digest/injection; four independence pairs naming
  non-candidates — the asm/emu legs and gearmulator are now first-class candidates).
  EXERCISE-COVERAGE, EXTRACTION and INTERACTION-MATRIX go RED on a unit without
  `encoding.sexp`/`interactions.sexp`/per-step expectation guests — the landing slice owns
  them, so the documents wait under artifacts/.
- More latent defects owned and fixed (§15): EXERCISE-COVERAGE counted a `(comment …)`
  inside scope as mnemonics (skipped now, GREEN arm, 8/8); rv64's own `profile.sexp`
  carried two notes on D-FENCE against the schema's single-valued declaration (merged);
  `check_sexp_schema.py` tracebacks on a missing input (clean rc-2 refusal, RED arm,
  51/51). Surfaced and routed: no gate schema-validates the dossier documents as a class —
  the landing slice adds that leg.

## SEMULITH-BR-0014 (leaf P3-BREADTH.5) — the state schema learns the census's shapes

- `schema/state.sexp` declares `register_family` (with `parts` and per-part `readout`),
  `memory_spaces`, and `hardware_stack`; `xlen`/`integer_registers` become optional. Every
  construct names its exercising target and case: dsp56300-lab-v0, F1 masked widths, F3
  memory spaces, the census's special-register/stack candidates — the content source is
  the F6 census record.
- The mapping owner (`dossier_sexp`) now CARRIES the new forms end to end: pre-change it
  built the state doc from named fields only, so a declared `memory_spaces` would have
  been silently dropped between the schema and the generator (the `.2` silent-path class).
  `gen_state.py` refuses each declared construct by name (rc 2), and a missing `xlen` is
  a named Refusal instead of a KeyError traceback.
- Synth probe 2 did what the fixture exists to do: its pin went stale, the suite turned
  RED, and the pin moved one layer down — the schema now accepts `memory_spaces` (rc 0)
  while the generator refuses it by name (rc 2). Suite 6/6; STATE-GEN self-test grew four
  RED arms (10/10); the rv64 descriptor re-validates and regenerates byte-identical.
- The DSP's own `state.sexp` deliberately does NOT land yet: without `profile.sexp` no
  gate would read it (measured — PROFILE-CONSISTENCY iterates `profiles/*/profile.sexp`),
  so it lands with the scope-taxonomy slice where its gate attachment is measured.

## SEMULITH-BR-0013 (leaf P3-BREADTH.1) — the dsp56300-lab-v0 state census; the dump is complete

- The SEM-08 hidden-state census re-ran for the exercised DSP profile (F6's per-profile
  leg): 14 candidates answered with locators, never by silence — the record is
  `docs/tasks/artifacts/p3-breadth/2026-10-01-dsp56300-state-census.md`.
- PRESENT and declared: the A2/B2 sign-extended extension readout and A1/B1 raw reads
  (`.4`'s pins harvested), M0–M7 bounded at reset by typed stops, sticky L/S (S has no
  writer in subset v0), the DO loop's stacked levels, the observable stale popped stack
  slots. ABSENT: REP working state beyond the declared LC (restored before the
  instruction retires), the F5 pending-writes window (scalar issue), reservation/FP/vector
  state (none exist in the family), and the interrupt/mode/stack-extension state (named
  exclusions, each reopening its census row).
- Consequence: for subset v0 under its named exclusions, the canonical end-state dump is
  the COMPLETE architectural state — surface completeness argued (stack slot 0 unwritable,
  P-low constant, the harness window excluded by the harness's own contract) and measured
  (the 6/6 agreement re-run this leg). The record is `.5`'s measured input for the
  `state.sexp` cases; the DOSSIER's deferral row names it. `P3-BREADTH.1` stays
  slice-gated (F6 refires per profile; F2/F4/F5 stay TI/VLIW-conditional); the frontier
  moves to `.5`.

## SEMULITH-BR-0012 (leaf P3-BREADTH.4) — subset v0 form-complete; the 6-guest corpus AGREEs

- `crates/semulith-dsp56300` decode+exec gained the whole subset: the register/immediate
  data-ALU core (add/sub/cmp/and/or/eor, all three source shapes), ASR/LSR, JSR/RTS,
  ENDDO, REP #xxx/REP S, and the seven linear (Rn) addressing modes — every mask
  FM-cited (page-footer cites) and cross-checked against the pinned assembler's probe
  words, which the decode tests pin.
- Guests `alu`, `shift`, `rn`, `rep`, `jsr` join `micro`: **6 agree / 0 fail** over the
  canonical end-state dumps (51–64 fields per case, `cyc` excluded by rule); the crate's
  17 unit tests carry hand-derived end-states (EVD-05).
- The differential campaign caught five model defects, each root-caused tools-first:
  RTS pulls PC only (FM 13-168 — SR stays, pinned by the jsr guest); MOVE #xx to an
  accumulator sign-extends into A2 (the FM's "remaining bits zeroed" prose falsified);
  A1/B1 memory reads are RAW (the shifter/limiter sits on the whole-accumulator path
  only); S sets on accumulator bus reads, never on ALU results; and a keep-mask
  nibble-slip zeroed A2 on the 24-bit ops. Two boundary defects fixed on the spot:
  accumulator-part move destinations now refuse at decode (a latent panic), and the NOP
  citation corrected to 13-145 (the FM's §13 TOC numbers pages differently from the
  printed footers). `P3-BREADTH.4` DONE 4/4.

## SEMULITH-MM-0075 (leaf MODEL-METHOD.19) — the demand chapter is a live chapter

- Director ruling (`2026-10-01`): *The information a unit demands* is a WIP by design —
  a live chapter that is re-derived, not just re-read, as each new CPU/DSP/board is
  modelled: prospective sections become measured, classes split or merge with what is
  measured, and every claim keeps citing a measured instance. The chapter header now
  states that rule (no hand-kept date — LIVE-DOC-CURRENCY). `MODEL-METHOD` DONE 19/19.

## SEMULITH-MM-0074 (leaf MODEL-METHOD.18) — the information a unit demands, per kind

- New mdBook chapter, *The information a unit demands — CPU, DSP, board* (The models
  section): per unit kind, the precise set of load-bearing information a faithful model
  needs and what each absence prevents — on the spine "prevents-the-model vs
  prevents-the-claim" (plus the quieter third: prevents-the-bound, the census never
  taken). CPU: 9 measured classes; DSP: the CPU set plus 6, each earned by a measured
  bite (the `x1=050000` readout surprise, the `memory_spaces` refusal, the U-bit
  extraction inversion); board: 5 prospective classes, marked derived-not-measured.
  Every class maps to the information catalogue's categories without restating them.
- The chapter closes on the recursion the P3 design discussions predicted: CPU = base
  set, DSP = base + scalar-breaking axes, board = base + composition. Book builds;
  chapter count re-derived 31 → 32; `MODEL-METHOD` is DONE 18/18.

## SEMULITH-BR-0011 (leaf P3-BREADTH.4) — the model crate stands; the first differential case AGREEs

- `crates/semulith-dsp56300` (lib + runner): the full canonical register set + 16-level
  hardware stack + three bounded memory windows (`machine.rs` — named per the
  FACT-OWNERSHIP generated-mirror convention), FM-cited decode for the nine demo-path
  forms, semantics with the FM Table 5-1 CCR rules and the DO loop machinery, the
  canonical-dump emitter (NO `cyc` line — timing is never emitted), the `.lod`/`.meta`
  dialects with fill headers refused by name; every out-of-subset word is a typed
  `ModelStop`.
- `scripts/compare_dumps.py` — the checkpoint-level comparator (field-exact; a missing
  key is a mismatch; `cyc` skipped by recorded rule; 4-arm self-test) and
  `scripts/run_dsp56300_smoke.py` — the campaign driver (not a commit gate; refuses
  unbuilt references).
- **The micro guest AGREES over 53 fields** (registers + X/Y deviations + stack slots) —
  the Semulith dump is byte-identical to the reference's. The 10 unit tests carry
  manual-derived expectations (EVD-05); `make check` + `make gate` green.
- Owned findings (§15): the FM's U-bit equation is an extraction INVERSION of its own
  prose (the reference's `sr c00310` is the arbiter — XNOR, recorded in `exec.rs`).

## SEMULITH-BR-0010 (leaf P3-BREADTH.4) — the dsp56300-lab-v0 dossier stands

- `profiles/dsp56300-lab-v0/`: `sources.sexp` pins DSP56300FM Rev. 5 at NXP's own locator —
  the fresh fetch returned byte-identical bytes to the chipdoc-cached copy (two acquisition
  routes, one artifact, verified); `references.sexp` records the `dsp56300` candidate
  (tarball pin, on-volume build note, the path-demonstration experiment, and the EVD-04
  independence rows: assembler and emulator share one project — the independent legs are
  upstream's asm56300 roundtrip and its silicon corpus; gearmulator not-examined);
  `DOSSIER.md` carries the deferrals by name (`profile.sexp`/`state.sexp`/`encoding.sexp` →
  `.5` named schema cases; requirements, unit registration, the per-unit book → the model
  slice).
- `scripts/fetch_references.sh` gained a GENERIC source-tarball leg (discriminator asset +
  source_commit + asset_sha256 — unreachable by the rv64 ledger, whose verify-only flow
  re-ran byte-behaviour-identical); `fetch_references.sh --verify-only dsp56300-lab-v0` →
  tarball MATCH.
- **The second-profile gate census (measured):** every auto-discovering gate keys on
  `profiles/*/profile.sexp` or `profiles/*/encoding.sexp`, so the deliberately partial
  dossier is invisible until those land — then the gates attach with NO gate edit.
  `make gate` green with the dossier present.

## SEMULITH-BR-0009 (leaf P3-BREADTH.4) — the bounded subset selected: `dsp56300-lab-v0` v0

- The reference's coverage censused on the pinned source (its decoder spans the full
  DSP56300 set) and its LIMITATIONS read in full — so the subset is bounded by honest
  implementability and the reference's own gaps, not by coverage. The comparison surface
  measured: checkpoint-level canonical end-state (registers, deviation-encoded X/Y windows,
  15 hardware stack slots; `steps` compared, `cyc` never) — a new comparator shape.
- **Subset v0:** non-parallel moves including the A2/B2 extension readout, the
  immediate/register data-ALU core, signed `mpy`/`mac`, `nop/jmp/jsr/rts`, `do`/`enddo`/`rep`,
  linear addressing only. Every exclusion named with its reason — parallel moves (the
  dual-feed axis) deferred as the first named extension candidate; interrupts, modes, stack
  extension and timing excluded on the reference's documented gaps.
- **Vehicle decided:** a new sibling crate `crates/semulith-dsp56300` (manual-derived,
  per-form-cited, EXPERIMENTAL); the generator/schema generalization stays `.5`'s work with
  this exercised target as its justification. Record:
  `docs/tasks/artifacts/p3-breadth/2026-10-01-subset-selection.md`; decision:
  `decision_dsp56300-lab-v0-subset`. Gaps surfaced and routed: the profile schema's scope
  taxonomy is scalar-named (→ `.5`); the auto-discovering gates' treatment of a second
  partial profile is the dossier slice's first measurement.

## SEMULITH-BR-0008 (leaf P3-BREADTH.3) — the evidence path exercised; `.3` done

- Reference pinned (commit `c60aeedb`, tarball sha256 recorded, `target/refs/` discipline)
  and release-built on-volume; a synthetic micro guest (24-bit immediates, mpy+mac into the
  56-bit accumulator, X/Y-space stores, a zero-overhead do loop) assembled (rc 0) and run
  headless — canonical-state dump, rc 0.
- Verified three independent ways: hand arithmetic reproduces A=001f253d515280 exactly;
  `--dump-mem` shows the X/Y stores landing right; the one surprise (`#$5` → `x1=050000`)
  traced to DSP56300FM §3.4.1.3. No Semulith DSP model exists — the claim is about the
  PATH. Artifact: `docs/tasks/artifacts/p3-breadth/2026-10-01-evidence-path-demo.md`.

## SEMULITH-BR-0007 (leaf P3-BREADTH.3) — the oracle survey: DSP56300 chosen, evidence path first

- Per-family oracle census (QEMU/MAME/gem5/GDB-sim/binutils/LLVM/vendor tooling/dedicated
  projects, one URL per claim): **TI C6000 ABSENT** for execution (no open-source executor;
  the vendor simulator was discontinued in 2014 and survives only as legacy proprietary);
  **DSP56300 STRONG** (mborgerson/dsp56300: MIT assembler roundtripped against the vendor
  assembler + MIT Cranelift emulator silicon-validated with a canonical-state differential
  harness); **SHARC ADSP-2106x PARTIAL** (MAME's BSD-3 core is real and scriptable, but no
  vendorable assembler exists and there is no second oracle).
- Both load-bearing positives re-derived against primary sources (the MIT LICENSE, the
  README's silicon-difftest claim, MAME's sharc.cpp header and register export).
- **Slice decision: DSP56300** — the only complete, license-clean evidence path (RK08: the
  slice is chosen by demonstrable evidence, not manual convenience). A scalar-DSP slice
  activates F1/F3 (`.5`) and F6 (census), leaves F4/F5 unbuilt and F2 idle — recorded, not
  lost. Slice 2 demonstrates the path end-to-end before `.4` implements anything.

## SEMULITH-BR-0006 (leaf P3-BREADTH.2) — the hook census: no opaque hooks; the one silent extraction arm is now a generation-time refusal

- Full-pipeline audit against `docs/ARCHITECTURE.md` §2 ("an unsupported construct is a
  model-generation failure, not a guessed translation"): every generator and shared
  definition reader refuses by name with rc ≠ 0; the runtime dispatch is a closed `Sem`
  enum with no catch-all; no feature flags or callback tables exist. Three designed seams
  are typed contracts, not escape hatches: the `Environment` boundary trait, the mutation
  seam `step_over`, the bench `Observer`.
- Defect found, owned, fixed (§15): `exec.rs`'s operand extraction silently skipped an
  operand naming no field, under a comment whose premise `P2-SCALAR.1` had falsified
  (FENCE's `fm`/`pred`/`succ` have field ranges since). `gen_definition.py` now refuses
  it (rc 2, naming instruction and operand — with a new DEF-GEN self-test RED arm);
  the runtime arm is a loud `ModelError`; the test ratchet lost its dead whitelist;
  four stale justification sites swept; `gen_fragments.py`'s dead `_unused_build` removed.
- Verified: DEF-GEN ok (9 self-test arms + byte-compare); `make check` 180/180 + fmt +
  clippy; synth suite 5/5; fragment regeneration byte-identical. Lesson promoted to
  `docs/knowledge/a-dead-justification-camouflages-a-silent-path.md`.

## SEMULITH-AC-0055 (tree ARTIFACT-CLEANUP) — the 2026-10-01 §8 cleanup: 96 incremental caches, 248 MB

- Time-triggered run (the `2026-09-30` run was a full day old). Pre-delete census: 96
  cargo incremental `.bin` files / 248 MB, all under `*/incremental/*` (48
  `target/debug`, 18 x86_64, 12 wasm32, 9+9 the two miri profiles); 0 stray
  `.bin`/`.log` in the enumerated locations; no `target/refs/*.log` present; the 7
  cargo-home crate-source fixtures kept by policy (inputs, not artifacts).
- Post-delete re-census: 0 incremental `.bin`; `target` 3.7 G → 3.5 G, `.app-data`
  unchanged at 1.4 G. `docs/ARTIFACT_CLEANUP.md` overwritten with the one-line record.

## SEMULITH-BR-0005 (leaf P3-BREADTH.1) — F2 measured executably; the unconditional-change set is empty; `.1` slice-gates on `.3`

- Finding F2 (register grouping with fill semantics, TI C64x §2.2) was the one
  `DSP-REVIEW.7` finding classified from a document's shape, not a measured refusal.
  The report named the honest route and `.1` took it: synth probe 5
  (`state-groups.sexp` — the real scalar state document plus one synthetic
  `register_groups` form) refuses by name, `undeclared field "register_groups"`, rc 1;
  the synth suite is now 5/5.
- The findings' required-**unconditional** implementation set measured **empty**: F4/F5
  are conditional on a VLIW slice, F2's implementation idles unless the slice is TI
  (implementing grouping with no exercised target would be the speculative generality
  this tree exists to refuse), F6 fires per new profile. `.1` is `slice-gated` — not
  closed: `.3` naming a VLIW or TI slice reopens it by name. Frontier moves to `.2`.
- Scalar regression evidence preserved and re-run (`EVD-07`; no code changed):
  `make check` 180/180 + fmt + clippy clean; gen_state rc 0; DEF-GEN ok; the G1 gate
  verdict `passed` re-derived.

## SEMULITH-BR-0001 (leaf P3-BREADTH.1) — the composable-DSP design discussion, recorded for resumption

- The director's `[DBINP]` exchange recorded in the `P3-BREADTH` tree's new Design
  Discussions section: a DSP as composition — the fixed skeleton of problems, the measured
  per-axis menu of vendor-citable choices, the composition rules that make a selection
  coherent, and the ISA as the fabric moving data between the chosen parts ("lego into a
  coherent, functional whole"). Resume point for the hypothetical high-end DSP as this
  tree's ultimate stress fixture; the permanent bounds carried (citable per-axis; never
  evidence about a real DSP).
- The tree's blockers cleared on record: `DSP-REVIEW` closed 8/8 (`SEMULITH-DR-0094`).

## SEMULITH-DR-0094 (leaf DSP-REVIEW.7) — the interface findings report: six findings routed, the tree closed 8/8

- The tree's capstone: every candidate interface change classified and costed, routed to
  `P3-BREADTH` with per-finding `ROUTING EVIDENCE` (manual locator + executable
  demonstration + the scalar-profile reproduction check — the method the tree
  pre-committed to before the first finding existed).
- Three CANNOT-EXPRESS findings, each refused by name and pinned by the `.6` synth
  suite: **F1** nonstandard widths (24/56/80-bit; rc 2) and **F3** multiple address
  spaces (rc 1) route to `P3-BREADTH.5`; **F4** the execute packet and **F5** the
  delayed visible writeback (both rc 1) route to `.1` **with the `.8` scope condition**
  — TI-family-shaped, so a scalar-DSP slice does not need them.
- Three NEEDS-A-CHANGE findings: **F2** register grouping with fill semantics (TI's
  40-bit odd:even zero-fill; the one finding without a measured refusal — recorded as
  its honest limit) and **F6** the per-profile state census reopenings (accumulator
  extensions, AMR/MODE1, sticky flags, loop state, the pending-writes window).
- Five measured non-findings classified OUT of interface work (the per-instruction SAT
  side effect, the saturate/round ordering, circular/bit-reversed addressing, the
  SPLOOP drain asymmetry, MFENCE — semantics data + census state, not interface shape).
- The scalar controls measured: the real 64-bit state document generates rc 0,
  `DEF-GEN: ok`, the synth suite 4/0 — **no finding reproduces on `rv64i-lab-v0`**;
  nothing routed belongs to `P2-SCALAR`. Evidence:
  `docs/tasks/artifacts/dsp-review/2026-10-01-interface-findings.md`.

## SEMULITH-DR-0093 (leaf DSP-REVIEW.8) — the cross-vendor contrast: TI's absences are TI's, measured

- The review's first three leaves measured three TI manuals only, and its interim facts
  ("no accumulator", "no guard bits", "no bit-reversed addressing") risked reading as DSP
  properties. The two channel-answered manuals (`SEMULITH-DR-0092`) measured the contrast:
  **the inversion is real, twice over** — DSP56300 carries two 56-bit A/B accumulators
  with 8-bit extension registers (A2/B2, §3.1) and SHARC carries 80-bit MRF/MRB
  accumulators that name the guard bits outright (§3); bit-reversed addressing exists in
  both (DSP56300 reverse-carry modifier §4.5.2; SHARC BR0/BR8 §6).
- Three address-unit shapes (TI byte / DSP56300 24-bit word in P/X/Y / SHARC
  width-varies-by-space word), three circular-buffer alignment rules (align-to-size /
  2^k-aligned / arbitrary), three loop models (SPLOOP / DO+REP / DO UNTIL loop stack).
- SHARC's five-stage **interlocked** pipeline is the printed negation of TI's
  "eliminating pipeline interlocks" — the `.4` break (execute-packet progress, delayed
  visible writeback) re-scopes: it is **TI-family-shaped, not DSP-shaped**.
- Every contrast carries both vendors' locators; nine further manual defects recorded
  unresolved. Evidence: `docs/tasks/artifacts/dsp-review/2026-09-30-cross-vendor.md`.

## SEMULITH-DR-0091 (leaf DSP-REVIEW.6) — the synthetic stress fixture: the boundary pinned, not assumed

- `synth24` (24-bit registers, a second address space, a packet construct, a delayed
  effect) pushed through the REAL pipeline — every shape measured refused BY NAME, and
  the refusals are the pins: the width (`gen_state.py`: "masked fixed-width storage for
  nonstandard widths is generator work", rc 2), the space (`undeclared field
  "memory_spaces"`), the packet (`undeclared field "packet"`), the delayed effect
  (`undeclared operator "delay"`). Each probe descriptor reduced until its ONLY refusal
  is the shape under test.
- The tracked fixture `docs/tasks/artifacts/dsp-review/synth/` carries the SYNTHETIC
  banner everywhere and the citation ban verbatim; the suite is green (4/4) exactly
  while the boundary stands pinned — a shape becoming supported turns it RED, by design.
  This is `.4`'s break made executable: packets and delayed effects refuse at the
  schema layer today, so `.7`'s report can say WHERE the work lives.
- The two vendor gaps were answered same-day (chipdoc's 2026-09-30 DSP batch:
  DSP56300, full SHARC family, TigerSHARC, Blackfin, DSP56800E, DSP48E2) — adoption
  follows; the channel contract recorded as knowledge card `the-chipdoc-channel`.

## SEMULITH-DR-0090 (leaf DSP-REVIEW.5) — loops, repeats, interrupts: the SPLOOP census

- SPLOOP is C64x+-and-later only (measured by the compatibility fields); the loop state
  is fully enumerated (the loop buffer, the hidden LBC ×2, ILC with its 4-cycle load
  latency, RILC, the SPLX bit). Interrupts DRAIN to a stage boundary (short loops are
  not interruptible — the rule has its formula); exceptions do NOT drain (the buffer
  goes idle immediately); restart refills the buffer by re-executing SPLOOP under
  modified rules, the ISR's saves named (ITSR/NTSR, ILC, RILC).
- The acceptance's SEM-04 framing measured: per-instruction completion holds across
  interrupts (E1-entered completes through E5; annulled packets leave no state); the
  persistent loop progress is exactly ILC + the refill — and `.4`'s packet/window break
  stands beside it. Multi-access: LDDW/STDW/LDNDW, ≤2 accesses/cycle; load-multiple and
  non-temporal measured absent; MFENCE is C66x-only, its violated restrictions
  undefined-by-omission.
- Evidence: docs/tasks/artifacts/dsp-review/2026-09-30-loops-q12-q14.md.

## SEMULITH-DR-0089 (leaf DSP-REVIEW.4) — the predicted break, measured — twice

- The scalar step model breaks, measured: (1) the execute PACKET is the unit of progress
  (≤8 instructions, all operands read simultaneously at E1); (2) writeback is delayed and
  visible (load at i+4, no interlocks, early reads stale by design) with interrupts
  landing INSIDE the window (the manual's own LDW/ADD example computes incorrectly).
  `OB-ENV-PARTIAL-PROGRESS` is true for RV64I and false for C6000 — recorded so
  P3-BREADTH never inherits it silently.
- The census consequence: a DSP profile reopens the hidden-state census by its own rule
  (the pending-writes window + packet state). The §3.7.2/§3.8.2 contradiction recorded in
  both forms, C66x's resolved form beside them.
- Evidence: docs/tasks/artifacts/dsp-review/2026-09-30-packets-q9-q11.md.

## SEMULITH-DR-0088 (leaf DSP-REVIEW.3) — addressing and address spaces: units byte-compatible, the seams named

- The acceptance's exact check — units, not just widths: byte-addressed on BOTH sides,
  one 32-bit numbering (no word-addressed space exists — measured). The five seams that
  do NOT fit the flat lab shape, each measured with locators: the 32-bit space; two L1
  spaces with a program-only fetch port (D-FETCH-MAP is scalar-lab-shaped); fetch-packet
  alignment; the AMR control register (the lab has no CSR surface); circular addressing
  restricted to A4–A7/B4–B7. Measured absent: bit-reversed addressing (BITR is a data
  op), strided modes (0 hits ×3). A second core-version split pinned (the circular
  nonalignment floor). Four more manual defects recorded unresolved.
- Includes the gap filing's changelog (SEMULITH-DR-0087 carried none — folded here):
  GAP-DSP56K-FAMILY-MANUAL and GAP-ADI-SHARC-PRM filed through the two-way channel; the
  C55x want dissolved on measurement (already catalogued).
- Evidence: docs/tasks/artifacts/dsp-review/2026-09-30-addressing-q6-q8.md.

## SEMULITH-DR-0086 (leaf DSP-REVIEW.2) — rounding, saturation, sticky flags: the defined step sequences

- The ordering measured as the manuals' own step sequences (multiply → accumulate →
  round-add → shift/saturate → narrow; CMPYR1/DDOTPH2R/QSMPY32R1/DOTPNRSU2 quoted with
  locators) — the leaf's acceptance, never "a saturating add".
- Saturation is in-instruction AND per-lane AND an explicit transfer (SAT); the
  sticky-flag side effect is per-instruction DATA (SADD2 saturates but does not set SAT —
  printed in its own entry). CSR.SAT/SSR survive interrupts (the TSR tables prove it);
  the context-switch restore ORDER is documented; SAT sets one cycle after the result —
  the delayed-effect shape, routed as `.4`'s input.
- **Seven manual defects/ambiguities recorded, none resolved by intuition** (the CMPYR1
  typo in two manuals, the prose-vs-C ordering contradiction, the missing saturation
  clause, the core-version intermediate-width split…). Evidence:
  docs/tasks/artifacts/dsp-review/2026-09-30-rounding-saturation-q3-q5.md.

## SEMULITH-DR-0085 (leaf DSP-REVIEW.1) — widths and accumulator semantics, measured across the three TI manuals

- The first DSP review leaf: Q1/Q2 of the catalog's DSP questions answered from the
  catalogued C64x/C66x/C674x manuals by text extraction — every fact quoted with its
  printed page and section. Headlines: NO accumulator and NO guard bits anywhere
  (measured absent, the searches named); 40-bit "long" values in odd:even register pairs
  with a zero-fill rule (all three), 64-bit pairs (all three), 128-bit quadruplets (C66x
  only); Q-notation nearly absent (Q31 exactly once); scaling instruction-encoded (the
  S-family's <<1+saturate) — and the `s`-bit trap measured (it's the A/B side-select).
- The first classification for `.7`: register GROUPING with a width+fill rule is the one
  candidate abstraction change; no accumulator/guard state is needed for these targets.
  Evidence: docs/tasks/artifacts/dsp-review/2026-09-30-widths-q1-q2.md.
- The tree's stale G1 blocker repaired; the tree is active; LIVE_STATUS's P2 row (stale
  at 8/9 from a mid-flight script abort) corrected to Done 9/9.

## SEMULITH-PS-0084 (leaf P2-SCALAR.9, slice c) — the CPU-LAB report stands; the tree CLOSES 9/9

- `gate_report.py` gained `build_cpulab`: the full processor-gate series per axis
  (SCP-05 — never rolled up; "supports RV64I" appears nowhere), every probe static over
  tracked artifacts (byte-stable in a fresh clone), the dossier content digest as the
  versioned artifact's identity. The generated `GC-REPORT.md` reads **`incomplete`**,
  naming the measured open axes: G-CONTRACT (0/72 obligation checks implemented) and
  G-OBLIGATIONS (28 requirements `planned`, 1 `partial`). Green with their measurements:
  G-TRACE, G-INTERACTIONS (21/21), G-REGRESSION (ACT4 51/51 + the corpus + the mutation
  suite), G-PORTABILITY (`passed` under the bridge), G-REPLAY (bundles + snapshots).
- The named release decision (`decision_release-rv64i-lab-v0`): **rv64i-lab-v0 v0 is an
  EXPERIMENTAL release of the versioned evidence artifact — NOT an accepted profile**;
  the closing conditions are named (the 72 fixtures, the status re-derivation, the
  bare-metal CI leg).
- One defect fixed in flight: the G0 generator's hardcoded "No CPU model exists" — prose
  written at P0, stale since the interpreter landed; the limitation now reads true, and
  GATE-REPORT holds all three generated reports in sync. MEMORY.md's active-trees count
  had drifted at 6/9 across two commits — corrected at closure.

## SEMULITH-PS-0082 (leaf P2-SCALAR.9, slice b) — the Rosetta proof: the x86-64 leg green, `portability: passed`

- The director's Rosetta install landed (VLC's Intel build triggered it); re-measured
  live: `arch -x86_64` prints `x86_64`. The instrument's x86-64 leg learned the bridge
  path: cross-compile `x86_64-apple-darwin`, run under translation, and compare the
  digest manifest against the aarch64 recording — **byte-identical** (`0670a01b…`).
- The full four-leg run reads **passed** (native green, x86-64 green under translation,
  Miri green, cross-endian green); `portability.sexp` re-measured to `passed`, with the
  translation-vs-bare-metal nuance and the fall-2027 horizon on the record.
- Slice (a)'s checklist claimed a `plan/p2.md` line that commit did not carry — the
  drift is recorded and the `.9` book section lands with this commit instead.

## SEMULITH-PS-0081 (leaf P2-SCALAR.9, slice a) — the CI two-host matrix wired; Rosetta measured LIVE

- `.github/workflows/portability.yml`: the host matrix (`ubuntu-latest` x86-64 +
  `macos-latest` aarch64) each running the native leg and uploading the digest manifest;
  the Miri + cross-endian job on x86-64 (nightly provisioned by the workflow); the
  `agree` job byte-comparing both manifests. The instrument gained `--leg` /
  `--emit-manifest` selectors (native-leg manifest measured reproducing the `.8`
  recording byte-identically, `0670a01b…`).
- **Rosetta measured LIVE** mid-slice: the director's install (VLC's Intel build
  triggered it) — `arch -x86_64` now prints `x86_64`, the probe binary runs. The bridge
  is up; slice (b) runs the leg through it next.
- CI evidence lands at the next approved push — the cadence governs.

## SEMULITH-PS-0080 (leaf P2-SCALAR.9, design) — the CPU-LAB release: three slices designed

- (a) The CI two-host matrix: a new `portability.yml` workflow (`ubuntu-latest` x86-64 +
  `macos-latest` aarch64 + a Miri job + the manifest-agreement job); the instrument gains
  `--leg`/`--emit-manifest` selectors. CI evidence lands at the next approved push.
- (b) The Rosetta-local proof when the director's reinstall lands (measured inert today:
  payload in the cryptex, daemon off).
- (c) The release report — measured first: G-CONTRACT's obligation-check implementation
  state decides whether the honest decision can read "accepted" even with portability
  green.
- Ceiling obeyed again: the `.8` checklist archived at the `.9` design commit.

## SEMULITH-PS-0079 (leaf P2-SCALAR.9) — the release route decided; Rosetta measured inert pending reinstall

- The director answered the release fork: CI two-host matrix (permanent home of the
  mandatory x86-64 leg: `ubuntu-latest` + `macos-latest`, the digest manifest the
  byte-exact contract) + Rosetta-local proof (the bridge) — recorded in
  `decision_release-route-x86-64-leg`. No narrower host policy.
- Measured refinement of the `.8` record: Rosetta on this host is PRESENT BUT INERT —
  binaries at `/usr/libexec/rosetta/`, the x86-64 dyld cache in the Rosetta cryptex, the
  oahd daemon not running, `arch -x86_64` failing (`Bad CPU type in executable`);
  activation is the director's admin act (a reinstall is coming). The horizon is on the
  record: Apple phases Rosetta out fall 2027 — nothing may be built on the bridge.

