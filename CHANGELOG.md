# CHANGELOG.md

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

## SEMULITH-PS-0077 (leaf P2-SCALAR.8) — the portability matrix: three legs green, the honest `incomplete`

- `scripts/check_portability.sh` runs the four legs and ends with the honest verdict:
  native aarch64 green (the commit gate's run + the digest manifest over the 49 guests'
  `demo --json` fingerprints — the contract the second host must reproduce
  byte-identically), Miri green 65/65 interpreted, cross-endian green 65/65 on
  big-endian powerpc64 under Miri — and the mandatory x86-64 leg measured UNAVAILABLE
  (Rosetta absent), so the verdict is `incomplete` and the profile stays experimental.
  Recorded, never waived (EVIDENCE_AND_GATES.md §7's own clause).
- The record: `profiles/rv64i-lab-v0/portability.sexp` (baseline.sexp's plain-atom
  shape). The verdict logic carries 6 self-test arms (6/0); the instrument is NOT a
  commit gate (nightly + host-measuring).
- Two authoring REDs, both measured: `grep -q` under `pipefail` SIGPIPEd cargo and read
  every leg red against a green reality (capture-then-read now); a script edited
  mid-run broke its own parse (bash reads incrementally — restart, never edit in
  flight). One drift caught and owned: the model book's bench-arm count had gone stale
  (44 → 53) across two leaves.

## SEMULITH-PS-0076 (leaf P2-SCALAR.8, design) — the portability matrix: availability measured first

- Measured, not assumed: x86-64 is UNAVAILABLE on this host (`arch -x86_64` → `Bad CPU
  type in executable`, Rosetta absent; no qemu user-mode runner) — the mandatory leg
  reads UNMET, recorded not waived; the profile stays experimental per the acceptance.
- Miri measured present and green: 65/65 core suites interpreted natively AND 65/65 on
  `powerpc64-unknown-linux-gnu` (big-endian) — the cross-endian leg holds. The one
  `unsafe` island (bench's counting allocator) excluded by name.
- The design: `scripts/check_portability.sh` (four legs, honest `incomplete` verdict,
  not a commit gate) + `portability.sexp` in `baseline.sexp`'s plain-atom shape.

## SEMULITH-PS-0075 (leaf P2-SCALAR.7) — mid-execution snapshots: replay proven for the implemented boundaries

- `semulith-verify::snapshot` + the CLI pair `snapshot`/`resume`: the record carries the
  definition-identity pins (the bundle's own pin check, extracted and shared), the region,
  entry, step index, the register file + pc, and the memory sparse-encoded and digested.
  The completeness claim is the pinned hidden-state census: registers + pc + memory is ALL
  the pending state this profile has — anything more is not offered (the acceptance's
  second arm).
- The proof: every tracked guest split at three points (early/middle/penultimate), resumed
  through the JSON round-trip, continuations identical — steps AND crossing logs. RED
  arms: corrupted run (digest), foreign definition (pin), incoherent/overrunning/partial
  records — each refused by name. 175 → 180 verify suites.
- One in-flight RED, the author's test arithmetic: the sparse encoding splits at zero
  bytes (the first run is one byte), so the overrun tamper needed one-past-the-end.
- CLI measured end-to-end: `dir-memwalk.elf` snapshotted at step 13 resumes the copy loop
  exactly (24 continuation steps, stop Trap).

## SEMULITH-PS-0074 (leaf P2-SCALAR.7, design) — mid-execution snapshots, designed on the pinned census

- The design's pending-state census is not new work but the pinned dossier's own:
  `state.sexp`'s hidden-state census measured all seven candidates absent, so a complete
  snapshot for this profile is exactly registers + pc + memory — anything more is "not
  offered at all", the acceptance's second arm.
- The mechanism: a `Snapshot` record (definition-identity pins, region, entry, step k,
  the register file + pc, sparse-encoded memory), JSON via the crate's own reader; the
  proof suite runs every guest's continuation twice (snapshot+continue vs
  restore+continue) with RED arms on corrupted/foreign snapshots; the CLI mirrors
  bundle/replay (`snapshot`/`resume`).

## SEMULITH-MM-0073 (leaf MODEL-METHOD.14) — the encoding re-sourcing probe: adopt-in-principle, measured

- The probe (untracked `target/materials/mm14_probe.py` over the pinned PDF's text
  layer): Chapter 36's listings carry every field as selectable text; ADD reconstructs
  end-to-end identical to the incumbent fragment; the full sweep measures **52/52
  opcodes extracted, zero value conflicts, 37/52 fully reconstructed by the naive
  parser** — the 15 remainders are parser-ordering gaps (page-local alignment), each
  caught by the incumbent comparison, which is the verification control.
- Decision recorded (`decision_encoding-resourcing-probe`): adopt-in-principle; the
  re-source is a later reviewed leaf (`.8` owns the encoding), triggered when the
  encoding is next touched or a second unit reuses the fragment. The re-sourced
  provenance would shrink the shared-with-spike ancestry leg.
- **The tree CLOSES 17/17.** Closure sweep found `.15`/`.17`'s Status fields stale
  (`active` with Results landed) — drift corrected.
- `MODEL-METHOD` leaves the active index; `P2-SCALAR.7` (snapshot/replay) is next.

## SEMULITH-PS-0072 (leaf P2-SCALAR.6) — the minimized divergence is retained; the leaf is DONE

- `min-fencei` — one word (`0x0000100F`) — reproduces the corpus's one model-vs-references
  divergence (`DIFF-FENCEI-EXECUTED`): the policy trap at step 0, the expected-divergence
  protocol green against EACH reference, the references agreeing over their full length
  (the nop, then the measured run-off-the-end illegal word). 175 verify suites; the
  matrix's F×E cell gains the guest; the difference record names the retained case
  (`references.sexp` at 32,765/32,768 — the note written to fit, the ceiling unmoved).
- No discrepancy was closed by widening a mask or editing an expectation (EVD-05/AI-05):
  the census found none tempting either. The seven non-model differences stay
  dispositioned with citations.

## SEMULITH-PS-0071 (leaf P2-SCALAR.6, design) — the discrepancy census: exactly one divergence to minimize

- Every recorded difference dispositioned with its citation (harness ×2, trace
  vocabulary, sub-granularity observable, the corrected platform-configuration defect,
  the board-layer difference, one reference-vs-reference mask) across all four corpora
  (48 guests / 642 steps, ACT4 51/51, the offline differential, the mutation suite):
  **one genuine model-vs-references divergence exists — `DIFF-FENCEI-EXECUTED`**.
- The minimization design: `it-fencei`'s three words reduce to ONE (`0x0000100F` alone) —
  the policy trap at step 0, the references nop and run off the end into the measured
  illegal zero word. Retained as `min-fencei` (expect_divergence at_step 0). The reducer
  is deliberately not the tool (it minimizes against mutations, not reference
  differences).

## SEMULITH-PS-0070 (leaf P2-SCALAR.5, strand 3) — the directed sequences; the leaf is DONE

- Eight directed guests from the measured census, every expectation derived before any
  run: `dir-runoff` (semulith's first run off a program's end — the zero word's policy
  trap, three-way identical), `dir-chase` (load→use as ADDRESS: the pointer chase and the
  jump through memory — the idiom that existed nowhere), `dir-ext-matrix` (the
  cross-width sign-extend matrix at the sign edges), `dir-selfmod-fence` (the patch
  visible through `fence rw,rw` — probed on all three models before authoring),
  `dir-cmp-branch` (all four senses on fresh predicates), `dir-memwalk` (the load+store
  loop), `dir-chain` (14 varied serial links), `dir-x0-writes` (every unpinned producer
  to x0). **150 new aligned steps, all three-way — 642/642 over 48 assembled guests**,
  byte-identical reproduction; the matrix's cells assigned (orphan rule green); the
  census pins the 55 new data crossings; 174 verify suites.
- Two authoring REDs caught by the offline differential, never a model defect:
  `dir-ext-matrix`'s data cell sat inside the code its stores patched (moved past the
  code end); one hand-typed constant re-derived.
- The census's defect is fixed and closed: `c-scope.c`'s comment overclaimed its
  constant-folded ELF (no jump table exists in the artifact) — the comment and the model
  book's chapter corrected, and the promised idiom became `dir-chase`'s measured guest.
- **`.5` is done** — all three strands landed: the compiled C guest (G1 `passed`), the
  ACT4 campaign (51/51, recorded and gated), the directed sequences. The frontier moves
  to `.6` (discrepancy reduction).

## SEMULITH-PS-0069 (leaf P2-SCALAR.5, strand 3 design) — directed sequences: the gaps measured, the design recorded

- The strand-3 design stands on a measured census (tracked corpus + the `c-scope.elf`
  disassembly + the ACT4 testplan): eight genuine gaps, each with its citation — semulith
  never running off a program's end, load→use-as-address (the jump-table idiom exists
  NOWHERE, not even in the compiled guest), the cross-width sign-extend matrix,
  store→fence→execute, compare→branch, the load+store loop, 12-deep varied chains, and
  the unpinned x0 producers.
- Two probes measured the uncertain behaviors before any guest exists (`run_probes_p25s3.py`):
  run-off-the-end traps illegal-instruction (0x02/tval 0) identically on all three models,
  and a self-modifying store stays visible through `fence rw,rw` on all three.
- One defect found by the census and logged: `c-scope.c`'s comment overclaims its ELF
  (constant folding removed the switch's indirect jump) — correction scheduled in-strand,
  the promised jump table becoming a real guest (`dir-chase`).
- Ceiling bookkeeping: `.4`'s checklist joined the archive (per-part ceiling obeyed).

## SEMULITH-PS-0068 (leaf P2-SCALAR.5, strand 2c) — the ACT4 RV64I campaign: 51/51, three-way, recorded and gated

- The full pinned suite ran green on the first fleet run: **51/51 test files, every HTIF
  verdict pass on all three models, every signature agreeing slot-for-slot — semulith vs
  the Sail-derived expectations AND spike vs sail (the control pair), 17,017 slots in
  sum.** The slot census reconciles exactly against the static sigupd counts (dead-path
  branch instances, store read-back slots, the final-offset word — all measured).
  `I-fence-00` (reserved-`fm`, `fence.tso`, HINTs) passes: DEFECT-A's inversion has
  external-suite confirmation.
- The record: `profiles/rv64i-lab-v0/act4.sexp`, emitted by the runner's `--record` from
  measured rows (never hand-typed), behind the new `schema/act4.sexp` family.
  RECORD-SCHEMA gained rule 13 (CAMPAIGN): every carried count re-derives from the rows
  and the verdict vocabulary is closed — five new self-test RED arms, 39/0.
- The EVD-04 framing is on the record: external tests with Sail-derived expectations —
  one semantics answering twice by construction; the value is that somebody else chose
  the tests. The model book's evidence chapter and materials section carry the campaign;
  the claim-scope page's "no ACT suite" row is corrected.
- Ceilings re-derived per the design's reviewed expansion: `profiles/` 100 files /
  427,926 B (ceiling 104, bytes unchanged at 0.83×), `schema/` 17 files.

## SEMULITH-PS-0067 (leaf P2-SCALAR.5, strand 2b) — the ACT4 harness: one test end-to-end three-way

- `semulith run` learned `--trace-stores`: the runner's crossing log (already recorded
  per step) is surfaced as `mem[W,0xADDR] <- 0xVALUE` lines — an observability option;
  the interpreter and the semantics data are untouched.
- The laboratory's DUT-side ACT4 pieces stand (`profiles/rv64i-lab-v0/act4/`):
  `rvtest_config.h` (the minimal measured define set — `UDB_MXLEN 64` alone; every
  privileged/FP path compiles out), `rvmodel_macros.h` (the check_defines-required
  names; the interrupt macros documented inert — no I-suite test executes them),
  `link.ld` (the lab's declared memory map, identical to the matched sail override).
- `scripts/fetch_act4.sh` is the reproducible acquisition route (pin-verified, refuses
  a drifted clone, census 51 files / 18,092 sigupds).
- `scripts/run_act4_campaign.py` builds and runs `I-add-00` end-to-end three-way: both
  toolchain risks retired by measurement (clang 21.1.8 assembles the suite clean; sail
  0.14's HTIF terminates under the lab override), all verdicts pass, the 513-slot
  signature agrees semulith↔sail-derived AND spike↔sail. The harness carries RED/GREEN
  controls (self-test 7/0).

## SEMULITH-PS-0066 (leaf P2-SCALAR.5, strand 2a) — ACT4 acquired sparse; strand-2 design recorded before code

- The pinned suite's generated half landed as a blobless sparse clone at `e2216915…`
  under `target/refs/riscv-arch-test/` (untracked: `tests/env` + `tests/rv64i/I` +
  `config`, 45 MB of the ~672 MB tree) — measured: 51 RV64I test files, 18,092
  `RVTEST_SIGUPD`s, 14,820 testcases.
- Strand-2 design recorded before code: signature-mode build; the CLI learns a store
  trace from the runner's crossing log; Sail-derived expectations per `EVD-04`, spike
  the control pair; DUT-side `rvtest_config.h` / `rvmodel_macros.h` / `link.ld` under
  `profiles/rv64i-lab-v0/act4/`; three slices.
- Acquisition facts synced: `references.sexp` (act4 → `acquired (sparse partial)` + pin;
  PROFILE-CONSISTENCY's vocabulary extended), the catalogue note, both books. Per-part
  ceiling obeyed: `.4`'s design moved to the tree archive (live file was 64,310/65,536).

## SEMULITH-PS-0065 (leaf P2-SCALAR.5) — the compiled guest, written into the model book

- New model-book chapter `compiled-guest.md` (between references and evidence): what a
  guest is and the shared-mind weakness of hand-written assembly; the self-checking
  design and why per-step expectations stay with the assembly corpus; the measured
  toolchain; all three in-flight defects as the teaching record (the C-UB shift, the
  visible-change vocabulary, GATE-REPORT's verdict-assuming arm); what it proved and
  what it did not. Linked from the evidence chapter. Book builds; gate green.

## SEMULITH-PS-0063 (leaf P2-SCALAR.5, strand 1) — the compiled C guest retires three-way; G1 reads `passed`

- `guests/c-scope.c` is the first COMPILED guest: a self-checking freestanding C tour of
  the declared scope (64/32-bit ALU, every load/store width, branches and a counted loop,
  real calls through the argument registers and an indirect jump, variable shifts),
  compiled by the pinned toolchain (`scripts/build_c_guest.sh` — clang 21.1.8 with the
  RISC-V backend plus `ld.lld` 21.1.8, both probed, refused by name if absent, nothing
  installed) and retiring under first-divergence comparison against sail-riscv AND spike:
  **129/129 aligned steps, byte-identical reproduction**.
- Two in-flight REDs, both authoring-side, never a model defect: the guest's own
  self-check caught `w32 << 33` (UB in C — clang deleted the rest of the program; proven
  by bisect, the `-fno-strict-aliasing` control innocent), and the three-way comparison
  surfaced a comparator gap the hand-written corpus never exercised — the references log
  no-change writes (`li a0, 0`), semulith's declared visible-change vocabulary does not.
  The comparator now reduces every trace to the declared vocabulary (`_visible_changes`
  in `align`, +2 self-test arms, 19/0).
- `gate_report.py`'s criterion 6 gained its met branch — **G1's verdict is `passed`**, the
  same instrument that said `incomplete` while the C path was missing. The report names
  the guest, the build script and the decision record; the toolchain versions keep their
  ONE owner (the decision record + the script's refusals).
- Lockstep: the smoke's `.c` path (build → budget run → `e_entry` from the ELF header),
  LIVE_STATUS (P1 `passed`), MEMORY, both books, P1-LAB's metadata, the model book.
  `make gate` all green; the full smoke 221 PASS / 0 FAIL.

## SEMULITH-PS-0062 (leaf P2-SCALAR.5) — the routing answered, the toolchain measured: .5 unblocked, design before code

- Director delegation `2026-09-30`: the C-guest routing and toolchain call is the
  engineer's. Recorded in `decision_c-guest-routing-and-toolchain`: the C guest lands in
  `P2-SCALAR.5` (the G0 precedent — the tree completes, the gate keeps criterion 6
  visible every commit, `EVD-08` forbids `passed` over a missing check); `P1-LAB` stays
  `done`.
- The toolchain was measured, not installed: Apple clang has no RISC-V backend (exact
  error recorded); Homebrew `llvm@21` clang 21.1.8 compiles RV64I correctly
  (objdump-verified); zig 0.16.0's bundled `ld.lld` 21.1.8 links.
- `.5` blocked → active; the three-strand design recorded before code (strand 1: the C
  guest; strand 2: the ACT4 generated suite; strand 3: directed sequences). Docs-only
  commit; `make gate` green.

