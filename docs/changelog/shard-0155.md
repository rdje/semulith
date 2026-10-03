# CHANGELOG shard — SEMULITH-P5-0003 … SEMULITH-BR-0020

> Sharded from `CHANGELOG.md` when it crossed its 64 KiB ceiling (`doctrine/readme_routes.tsv`).
> Entries in a shard are **never edited after the shard** — git history is canonical.

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

