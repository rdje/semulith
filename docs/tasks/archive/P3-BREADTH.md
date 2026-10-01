# P3-BREADTH — archived completed-leaf evidence (part 1)

The full, unedited acceptance checklists for the `done` leaves of the
[`P3-BREADTH`](../P3-BREADTH.md) tree (`.2`, `.4` slices 1–4, `.5` slices 1–2, and the
slice-gated `.1`'s two completed slices — the F2 probe and the F6 census leg), split out
on `2026-10-01` when the live file crossed its per-part ceiling — the ceiling was obeyed,
not raised, per the `docs/tasks/` precedent set by `SOT-FORMAT` and `P1-LAB`. The live
tree keeps the frontier, the decisions, the open questions, the blockers, every leaf's
goal/acceptance/result narrative, the newest completed slice's checklist (`.5` slice 3),
and both logs.

Archived sections, verbatim:

`P3-BREADTH.1`, slice 1 (`2026-10-01`, `SEMULITH-BR-0005`):

- [x] **ROOT CAUSE (WHY + WHERE)** — the findings report itself named the gap: F2 was
  "the only finding without an executable demonstration… If `P3-BREADTH.1` wants one, a
  grouping probe in the `synth/` suite is the honest way to get it"
  (`docs/tasks/artifacts/dsp-review/2026-10-01-interface-findings.md`, "What the report
  does NOT say"). Measured: `python3 scripts/check_sexp_schema.py
  docs/tasks/artifacts/dsp-review/synth/state-groups.sexp schema/state.sexp` →
  `REFUSED state-groups.sexp: construct "integer_registers": undeclared field
  "register_groups"`, rc 1 — exactly one refusal, the grouping shape.
- [x] **ADDRESSED (verified)** — probe 5 pinned in `run_synth_probes.sh`; the suite
  re-run: `synth probes: 5 pass / 0 fail` (was 4/0; the pin is the measured message).
- [x] **NO REGRESSION** — no code changed (probe fixture + docs only); the scalar
  regression re-run anyway per the leaf acceptance (`EVD-07`): `make check` → fmt clean,
  clippy `-D warnings` clean, 180/180 tests; `gen_state.py` on the real profile rc 0
  (14496 bytes); `check_definition_gen.sh` → `DEF-GEN: ok`;
  `gate_report.py rv64i-lab-v0 --gate G1` → verdict `passed`, re-derived.
- [x] **FIX** — `state-groups.sexp` (the real scalar state document plus one synthetic
  `register_groups` form, reduced to a single refusal), probe 5 in the runner, the synth
  README's table and count.
- [x] **LOCKSTEP** — tree (this file: leaf status, frontier, decision, logs),
  `LIVE_STATUS.md`, `docs/TASK_TREE.md`, `MEMORY.md`, `CHANGELOG.md`, `DEV_NOTES.md`,
  and the mdBook's P3 page (the synthetic-shapes list now names register grouping).

`P3-BREADTH.1`, F6 census leg (`2026-10-01`, `SEMULITH-BR-0013`):

- [x] **ROOT CAUSE (WHY + WHERE)** — F6 says the census reopens per new profile; `.4`
  delivered the exercised dsp56300-lab-v0 profile and pinned the load-bearing readouts
  (A1/B1 raw, A2/B2 sign-extended, accumulator-part destinations excluded) inside the
  crate's module docs and the measured 6/6 agreement — but no census record held them as
  one SEM-08 answer. WHERE the census lives, located mechanically (`grep -n
  hidden_state_census profiles/rv64i-lab-v0/state.sexp` → line 6): the scalar profile
  carries it as data in `state.sexp`'s `hidden_state_census`; this profile's `state.sexp`
  is deferred to `.5` (DOSSIER.md's deferral table), so the census lands as the measured
  record `.5` harvests.
- [x] **ADDRESSED (verified)** — the census record stands
  (`artifacts/p3-breadth/2026-10-01-dsp56300-state-census.md`): 14 candidates, each answered
  with locator and verdict, never by silence; the supported-observation surface defined from
  `references.sexp`'s comparison contract; surface completeness argued (no mutable cell
  outside the dump — slot 0 unwritable by the pre-incremented SP, P-low constant because
  subset v0 decodes no P-space write, the harness window excluded by the harness's own
  contract) and measured — the instruments re-run this leg:
  `python3 scripts/run_dsp56300_smoke.py` → `dsp56300 smoke: 6 agree / 0 fail` (51–64
  fields per case), `python3 scripts/compare_dumps.py --self-test` → `4 pass / 0 fail`,
  `cargo test -p semulith-dsp56300` → `test result: ok. 17 passed`.
- [x] **NO REGRESSION** — docs-only leg; `cargo test -p semulith-dsp56300` → 17/17 (the
  commit-level proof unchanged); `make gate` → `=== all doctrines green ===` with the census
  artifact present (the doc ceilings held: CHANGELOG.md/DEV_NOTES.md append heads within
  bounds after the event).
- [x] **FIX** — the census artifact; the DOSSIER's `state.sexp` deferral row now names the
  census as `.5`'s measured input.
- [x] **LOCKSTEP** — tree (this file: leaf record/status, frontier, checklist, logs),
  `LIVE_STATUS.md`, `docs/TASK_TREE.md`, `MEMORY.md`, `CHANGELOG.md`, `DEV_NOTES.md`,
  the profile DOSSIER; mdBook `plan/p3.md` (the census consequence stated).

`P3-BREADTH.5`, slice 1 (`2026-10-01`, `SEMULITH-BR-0014`):

- [x] **ROOT CAUSE (WHY + WHERE)** — the schema refused the DSP's measured state shapes
  (synth probe 2's pin: `python3 scripts/check_sexp_schema.py state-spaces.sexp
  schema/state.sexp` → `REFUSED … undeclared field "memory_spaces"`, rc 1), and two
  silent-path hazards sat between the schema and the generator:
  `dossier_sexp.state_to_doc` built the doc from named fields only (a declared
  `memory_spaces` would be DROPPED before the generator could refuse it — measured
  pre-change), and a missing `xlen` crashed with a KeyError traceback instead of a named
  Refusal. WHERE the constructs come from: the F6 census record
  (`artifacts/p3-breadth/2026-10-01-dsp56300-state-census.md`), candidates 1/2/4/6 + F1/F3.
- [x] **ADDRESSED (verified)** — the schema declares the constructs (each naming its case);
  the mapping owner carries them (round-trip data-equal on the rv64 document, re-derived:
  `state_to_doc(state_to_form(load_state(...))) == load_state(...)`); the generator refuses
  each by name — measured: `gen_state.py` on the spaces descriptor → rc 2, `memory_spaces
  declared`; the four new STATE-GEN self-test arms RED-prove the refusals
  (`check_state_gen.sh --self-test` → `10 pass / 0 fail`); synth probe 2 re-pinned
  (`run_synth_probes.sh` → `synth probes: 6 pass / 0 fail`: schema accepts rc 0
  `conforms`, generator refuses rc 2).
- [x] **NO REGRESSION** — `check_sexp_schema.py profiles/rv64i-lab-v0/state.sexp
  schema/state.sexp` → `ok`; `gen_state.py --check` → byte-identical (rc 0); the
  descriptor round-trip data-equal; `dossier_sexp.py --self-test` → `12 pass / 0 fail`;
  `make gate` → `=== all doctrines green ===` (DERIVED-COUNTS fired on the four new arms
  — re-derived 308 → 312 by the doctrine's own command, LIVE_STATUS.md updated; nothing
  else moved). No Rust changed (`make check` not owed; the dsp crate's 17/17 and the 6/6
  smoke were re-run this session for the census leg and stand unchanged).
- [x] **FIX** — `schema/state.sexp` (the constructs + the optional xlen/integer_registers),
  `scripts/dossier_sexp.py` (carry the new forms, xlen/integer_registers optional),
  `scripts/gen_state.py` (the named refusals + the xlen Refusal), `scripts/
  check_state_gen.sh` (four RED arms), the synth suite (probe 2 re-pinned two legs;
  `state-spaces.sexp` carries full `space` forms; README records the move).
- [x] **LOCKSTEP** — tree (this file: slice design + record, checklist, logs),
  `LIVE_STATUS.md` (arm count re-derived), `MEMORY.md`, `CHANGELOG.md`, `DEV_NOTES.md`,
  `DOCTRINE_ENFORCEMENT.md` (the STATE-GEN row names the new refusals), mdBook
  `plan/p1.md` (the refusal list grew) and `plan/p3.md`.

`P3-BREADTH.5`, slice 2 (`2026-10-01`, `SEMULITH-BR-0015`):

- [x] **ROOT CAUSE (WHY + WHERE)** — the scope taxonomy's scalar shape lived in exactly two
  closed places (`schema/profile.sexp`'s scope construct; `dossier_sexp._SCOPE_LISTS`,
  which refuses an undeclared field by name), and the DSP documents had nowhere honest to
  wait: landing them blind would attach four gates unmeasured. Measuring the attachment
  (untracked + intent-to-add placement) surfaced what no gate had ever checked —
  `scripts/check_profile_consistency.sh` on the DSP dossier → 7 findings: 3 UNEARNED
  OBTAINED (the candidate claimed `obtained` without binary/binary_sha256/injection) + 4
  UNKNOWN MODEL (independence pairs naming non-candidates).
- [x] **ADDRESSED (verified)** — schema generalized (each optional/added field names
  dsp56300-lab-v0 as its case); drafts validate:
  `python3 scripts/check_sexp_schema.py …/dsp56300-dossier/profile.sexp
  schema/profile.sexp` → `ok`, same for state.sexp → `ok`; both load through the mapping
  owner and round-trip data-equal (`profile round-trip: True`, `state round-trip: True`);
  the references.sexp defects fixed — re-run: `PROFILE-CONSISTENCY: ok (2 profile
  dossier(s) internally consistent)`; the schema fix re-verified:
  `check_sexp_schema.py profiles/rv64i-lab-v0/profile.sexp schema/profile.sexp` → `ok`
  (28 decisions, round-trip clean).
- [x] **NO REGRESSION** — `bash scripts/fetch_references.sh --verify-only
  dsp56300-lab-v0` → `ok`; `check_exercise_coverage.sh --self-test` → `8 pass / 0 fail`
  (the new comment arm); `check_sexp_schema.py --self-test` → `51 pass / 0 fail`;
  `dossier_sexp.py --self-test` → `12 pass / 0 fail`; rv64 documents re-validate and
  round-trip unchanged; `make gate` → `=== all doctrines green ===`.
- [x] **FIX** — `schema/profile.sexp`, `scripts/dossier_sexp.py` (`_SCOPE_LISTS`),
  `scripts/check_exercise_coverage.sh` (the comment skip + arm),
  `scripts/check_sexp_schema.py` (missing-input refusal + arm),
  `profiles/dsp56300-lab-v0/references.sexp` (the 7 findings), `profiles/rv64i-lab-v0/
  profile.sexp` (D-FENCE's notes merged), the two drafts under
  `docs/tasks/artifacts/p3-breadth/dsp56300-dossier/`.
- [x] **LOCKSTEP** — tree (this file: slice design + record, checklist, logs),
  `LIVE_STATUS.md`, `MEMORY.md`, `CHANGELOG.md`, `DEV_NOTES.md`, the profile DOSSIER
  (deferral rows now name the drafts + the measured attachment; the stale
  requirements-row wording fixed); mdBook `plan/p3.md`.

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
