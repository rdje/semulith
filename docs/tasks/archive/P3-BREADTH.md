# P3-BREADTH — archived completed-leaf evidence (part 1)

The full, unedited acceptance checklists for the `done` leaves of the
[`P3-BREADTH`](../P3-BREADTH.md) tree (`.2` and `.4` slices 1–4), split out on
`2026-10-01` when the live file crossed its per-part ceiling — the ceiling was obeyed,
not raised, per the `docs/tasks/` precedent set by `SOT-FORMAT` and `P1-LAB`. The live
tree keeps the frontier, the decisions, the open questions, the blockers, every leaf's
goal/acceptance/result narrative, the active leaves' checklists (`.1`, `.5`), and both
logs.

Archived sections, verbatim:

`P3-BREADTH.2` (`2026-10-01`, `SEMULITH-BR-0006`):

- [x] **ROOT CAUSE (WHY + WHERE)** — the audit censused every generator and reader error
  path plus the runtime dispatch (method recorded in the leaf's Census paragraph). The one
  silent escape hatch: `crates/semulith-core/src/exec.rs`'s `extract_operands` `_` arm —
  `let Some(f) = field(name) else { continue; }` skipped an operand naming no field, under
  a comment whose premise `P2-SCALAR.1` had falsified. Pre-fix, no generation-time check
  existed: `grep -n "names no field" scripts/gen_definition.py` had 0 hits (post-fix:
  `scripts/gen_definition.py:352` is the refusal). WHERE the contract lives:
  `docs/ARCHITECTURE.md` §2 — "an unsupported construct is a model-generation failure,
  not a guessed translation" — enforced for operands only by a test ratchet whose own
  whitelist comment was equally stale (`schema/fragment.sexp` accepts any symbol).
- [x] **ADDRESSED (verified)** — before → after, measured through the new DEF-GEN
  self-test RED arm (an `add` clone declaring operand `rs9`, which names no field):
  before, generation emitted a module without protest and extraction skipped `rs9`;
  after, `gen_definition.py` exits rc 2 with
  `add: operand 'rs9' names no field — extraction for it would be silent; declare the
  field or drop the operand`, and the full self-test prints `9 pass / 0 fail`
  (the arm included). The runtime arm now returns
  `ModelError::InvalidDescription` instead of skipping.
- [x] **NO REGRESSION** — `bash scripts/check_definition_gen.sh` → `DEF-GEN: ok` (self-test
  9 arms incl. the new RED arm, then byte-compare); `make check` → fmt clean, clippy
  `-D warnings` clean, 180/180 tests; synth suite 5/5; `gen_fragments.py` re-run against
  the pinned upstream regenerates both fragments BYTE-IDENTICAL (the dead-code removal
  changed no output — `git status` clean under `definitions/`).
- [x] **FIX** — `gen_definition.py` (the operand-names-a-field refusal + the stale emitted
  docstring corrected), `exec.rs` (the silent `continue` → loud `ModelError`),
  `definition/tests.rs` (the ratchet strict: whitelist deleted), `exec/tests.rs` (the
  word-builder panics on an unfielded operand instead of emitting a wrong word),
  `gen_fragments.py` (dead `HEADER`+`_unused_build` removed), `check_definition_gen.sh`
  (the RED arm), `definition.rs` regenerated (docstring only — tables byte-identical).
- [x] **LOCKSTEP** — tree (leaf status/census/defect, frontier, checklist, logs),
  `LIVE_STATUS.md`, `docs/TASK_TREE.md`, `MEMORY.md`, `CHANGELOG.md`, `DEV_NOTES.md`;
  the lesson PROMOTED to `docs/knowledge/a-dead-justification-camouflages-a-silent-path.md`
  (+ INDEX row). mdBook: no page documents the extraction internals — no drift.

`P3-BREADTH.4`, slices 1–2 (`2026-10-01`, `SEMULITH-BR-0009` / `SEMULITH-BR-0010`):

- [x] **ROOT CAUSE (WHY + WHERE)** — `.3` demonstrated the path but selected nothing: the
  leaf acceptance requires the claim to name the exact subset, and `.3` left the ledger
  integration ("`profiles/<dsp>/references.sexp` driving `fetch_references.sh`") explicitly
  to `.4`. WHERE the bounds come from, measured: the pinned reference's `Instruction` enum
  (commit `c60aeedb`, tarball sha256
  `46b0e3e532e774859ee59b861901ac53b94a31ca5c924c61f8f32b26d6b308c9` — coverage complete, so
  the bound is honest implementability), its `docs/LIMITATIONS.md`
  (each gap → a named exclusion), and its `tools/difftest/README.md` (the checkpoint-level
  comparison contract). WHERE the dossier integrates: `scripts/fetch_references.sh`
  processed candidates only by hardcoded id (sail-riscv/spike/qemu) — a dsp56300 ledger
  would have verified nothing while printing `ok`.
- [x] **ADDRESSED (verified)** — the selection artifact names subset v0 and every
  exclusion's reason; `profiles/dsp56300-lab-v0/` stands and VALIDATES:
  `python3 scripts/check_sexp_schema.py profiles/dsp56300-lab-v0/references.sexp
  schema/references.sexp` → `ok`; same for `sources.sexp` → `ok`;
  `bash scripts/fetch_references.sh --verify-only dsp56300-lab-v0` →
  `MATCH dsp56300 source tarball … ok (dsp56300-lab-v0)`;
  `bash scripts/fetch_sources.sh --verify-only dsp56300-lab-v0` →
  `MATCH DSP56300FM.pdf b2e8e346…`, rc 0.
- [x] **NO REGRESSION** — the rv64 reference flow re-verified byte-behaviour-identical after
  the script change: `bash scripts/fetch_references.sh --verify-only rv64i-lab-v0` →
  `MATCH owned fragments agree…`, `MATCH matched-profile ISA string rv64i_zvl32b`,
  `ok (rv64i-lab-v0)`; the generic leg's discriminator (asset + source_commit +
  asset_sha256) matches no rv64 candidate. `make gate` → `=== all doctrines green ===`
  with the new dossier present (the second-profile census: no gate edit needed — measured,
  recorded in the leaf). No Rust changed (`make check` not owed; the script is bash+python,
  exercised directly above).
- [x] **FIX** — the selection artifact, `decision_dsp56300-lab-v0-subset` (+ INDEX),
  `profiles/dsp56300-lab-v0/{DOSSIER.md,sources.sexp,references.sexp}`,
  `scripts/fetch_references.sh`'s generic source-tarball leg.
- [x] **LOCKSTEP** — tree (leaf slices, frontier, checklist, logs), `LIVE_STATUS.md`,
  `docs/TASK_TREE.md`, `MEMORY.md`, `CHANGELOG.md`, `DEV_NOTES.md`, the decisions INDEX;
  mdBook: `plan/p3.md` updated at slice 1 (slice 2 is dossier plumbing the book's P3 page
  already covers as "in progress" — no new drift).

`P3-BREADTH.4`, slice 3 (`2026-10-01`, `SEMULITH-BR-0011`):

- [x] **ROOT CAUSE (WHY + WHERE)** — slices 1–2 selected and dossiered the subset, but no
  model existed to evidence. WHERE the risk concentrated: the CCR rules (FM Table 5-1's
  extraction carries an inverted U-bit equation — its own prose says "set if the two MSBs
  are identical"; the reference's `sr c00310` is the arbiter), the DO loop's stack
  discipline (FM §13, push LA/LC then PC/SR, exit restoring LA/LC and LF alone), and the
  A2 readout (FM §3.4.1.2: the extension byte sign-extended through bit 7). Every decode
  mask was derived from the FM's opcode figures and cross-checked against the pinned
  assembler's words (`target/dsp56300-demo/micro.lod`, e.g. `$44F400` = move #imm24,x0).
- [x] **ADDRESSED (verified)** — the crate's 10 unit tests carry manual-derived
  expectations (EVD-05, derived before the model ran — the `.3` record's three-way
  verification): `cargo test -p semulith-dsp56300` → `test result: ok. 10 passed`;
  `python3 scripts/compare_dumps.py --self-test` → `4 pass / 0 fail`;
  `python3 scripts/run_dsp56300_smoke.py` →
  `AGREE micro: AGREE over 53 fields for case 'micro' (skipped by rule: cyc)`,
  `dsp56300 smoke: 1 agree / 0 fail` — the Semulith dump is byte-identical to the
  reference's (`diff` of the two dumps empty apart from the excluded `cyc` line).
- [x] **NO REGRESSION** — `make check` → fmt clean, clippy `-D warnings` clean, all tests
  green (180 rv64 + 65 + 10 new dsp + the rest — the scalar model byte-untouched);
  `make gate` → `=== all doctrines green ===` (after the FACT-OWNERSHIP convention
  collision was resolved by the `state.rs` → `machine.rs` rename — the generated-mirror
  naming convention is the gate's premise, not a dodge);
  `python3 scripts/run_dsp56300_smoke.py` re-run after the rename → still `1 agree / 0 fail`.
- [x] **FIX** — `crates/semulith-dsp56300/` (new crate: machine, decode, exec, dump, lod,
  runner), `scripts/compare_dumps.py` + `scripts/run_dsp56300_smoke.py`,
  `profiles/dsp56300-lab-v0/guests/{micro.a56,micro.meta}`.
- [x] **LOCKSTEP** — tree (leaf slice, frontier, checklist, logs), `LIVE_STATUS.md`,
  `docs/TASK_TREE.md`, `MEMORY.md`, `CHANGELOG.md`, `DEV_NOTES.md`, the profile DOSSIER;
  mdBook `plan/p3.md` (the first differential agreement).

`P3-BREADTH.4`, slice 4 (`2026-10-01`, `SEMULITH-BR-0012`):

- [x] **ROOT CAUSE (WHY + WHERE)** — slices 1–3 left the subset at nine demo-path forms;
  the leaf's acceptance requires the NAMED subset (ALU core, jsr/rts, rep, the (Rn)
  modes) exercised and agreed. WHERE the risk concentrated, measured by the first smoke
  run — `python3 scripts/run_dsp56300_smoke.py` printed `dsp56300 smoke: 2 agree /
  4 fail`, rc=1: the accumulator readout/writeback paths (the A1 limiter locus,
  the short-immediate A2 sign extension, the 24-bit ops' keep-mask), the RTS stack
  contract, and the S-bit's trigger — exactly the seams where FM prose and silicon can
  part. Each failure's root cause is named in the slice record above, (a)–(e), with the
  arbiter (the pinned reference's observed end-state) and the FM page for each.
- [x] **ADDRESSED (verified)** — `python3 scripts/run_dsp56300_smoke.py` → `6 agree /
  0 fail` (micro 53, alu 51, shift 51, rn 53, rep 64, jsr 54 fields; `cyc` skipped by
  rule); `cargo test -p semulith-dsp56300` → 17/17 (the five new exec tests carry
  hand-derived end-states — values derived from the FM figures BEFORE the model run,
  matching the agreed dumps; the decode test pins 40+ assembler-emitted probe words).
- [x] **NO REGRESSION** — `make check` → fmt clean, clippy `-D warnings` clean, all
  workspace tests green (the scalar model byte-untouched); `make gate` →
  `=== all doctrines green ===`; the micro guest (slice 3's case) still AGREEs.
- [x] **FIX** — `crates/semulith-dsp56300/src/{decode,exec}.rs` (the new forms + the five
  measured corrections + the two boundary fixes), `profiles/dsp56300-lab-v0/guests/`
  (five new guests + metas, the rep guest's `#>` fix).
- [x] **LOCKSTEP** — tree (this file: leaf status/slice record, frontier, checklist,
  logs), `LIVE_STATUS.md`, `docs/TASK_TREE.md`, `MEMORY.md`, `CHANGELOG.md`,
  `DEV_NOTES.md`; mdBook `plan/p3.md` (the subset is form-complete, 6/6 AGREE).
