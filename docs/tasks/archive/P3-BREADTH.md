# P3-BREADTH — archived completed-leaf evidence (part 1)

The full, unedited acceptance checklists for the `done` leaves of the
[`P3-BREADTH`](../P3-BREADTH.md) tree (`.2`, `.4` slices 1–4, `.5` slices 1–3, and the
slice-gated `.1`'s two completed slices — the F2 probe and the F6 census leg), split out
on `2026-10-01` when the live file crossed its per-part ceiling — the ceiling was obeyed,
not raised, per the `docs/tasks/` precedent set by `SOT-FORMAT` and `P1-LAB`. The live
tree keeps the frontier, the decisions, the open questions, the blockers, every leaf's
goal/acceptance/result narrative, the active leaf's checklist (`P3-BREADTH.7`),
and both logs.

Archived sections, verbatim:

`P3-BREADTH.5`, slice 3 (`2026-10-01`, `SEMULITH-BR-0016`):

- [x] **ROOT CAUSE (WHY + WHERE)** — `.5`'s last named case was the encoding/definition
  route, deferred by `.4`'s vehicle decision; what it would cost was asserted, never
  measured. WHERE measured: `grep -n 'Refusal' scripts/gen_definition.py` (the profile
  scope at line 322, the 32-bit decode table at line 326, the semantics corpus at lines
  148/210) and the operator census of `schema/semantics.sexp` (31 operators;
  `(load width signed? addr)`/`(store width addr value)` carry no space parameter, state
  access is `reg`/`pc` only — the DSP's X/Y/P moves and do/rep machinery would refuse by
  name, the class synth probe 4 pinned for `delay`).
- [x] **ADDRESSED (verified)** — the measurement is recorded in the leaf (slice 3 above):
  the encoding generalization is a lane, not an extension, and no current milestone
  consumes it (`decision_lane-consumption`); the sibling crate is the exercised,
  differentially agreed vehicle (`run_dsp56300_smoke.py` 6/6, `cargo test -p
  semulith-dsp56300` 17/17 — both re-verified green this leg, unchanged since `.4`).
  The deferral's reopening conditions are named in the leaf; the landing is leaf `.7`
  with its measured input table.
- [x] **NO REGRESSION** — docs-only slice (the tree, the DOSSIER rows, the live docs):
  `make gate` → `=== all doctrines green ===`; the drafts still validate
  (`check_sexp_schema.py` on both → `ok`, re-run).
- [x] **FIX** — the tree (`.5` closed 3/3; `.7` added with its acceptance and measured
  input), the DOSSIER deferral rows re-routed to `.7`.
- [x] **LOCKSTEP** — tree, `docs/TASK_TREE.md`, `MEMORY.md`, `LIVE_STATUS.md`,
  `CHANGELOG.md`, `DEV_NOTES.md`, the DOSSIER; mdBook `plan/p3.md` (the encoding case's
  disposition stated).

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

## `.4` — the slice narratives (verbatim), archived the same day

  Slice 1 (`2026-10-01`, `SEMULITH-BR-0009`): the subset SELECTED against the reference's
  measured coverage and gaps — unit `dsp56300-lab-v0` subset v0: non-parallel moves incl.
  the A2/B2 extension readout (F6's named case), the immediate/register data-ALU core,
  signed `mpy`/`mac`, `nop/jmp/jsr/rts`, `do`/`enddo`/`rep`, linear addressing only; every
  exclusion named with its reason (parallel moves — the dual-feed axis — deferred as the
  first named extension candidate; interrupts/modes/stack-extension/timing excluded on the
  reference's own LIMITATIONS). The comparison surface measured: checkpoint-level canonical
  end-state (registers + deviation-encoded X/Y windows + 15 stack slots; `steps` compared,
  `cyc` never) — a new, simpler comparator shape than the RISC-V per-step walk. Vehicle
  DECIDED: sibling crate `crates/semulith-dsp56300`, manual-derived decode/semantics with
  per-form citations, EXPERIMENTAL label; generator/schema generalization stays `.5`'s.
  Record: [`artifacts/p3-breadth/2026-10-01-subset-selection.md`](artifacts/p3-breadth/2026-10-01-subset-selection.md);
  decision: `decision_dsp56300-lab-v0-subset`. Gaps surfaced, owned, routed: the profile
  schema's scope taxonomy is scalar-named (→ `.5` named case); the auto-discovering gates'
  treatment of a second partial profile must be measured by the dossier slice.
  Slice 2 (`2026-10-01`, `SEMULITH-BR-0010`): the dossier + the reference ledger —
  `profiles/dsp56300-lab-v0/` stands with `sources.sexp` (DSP56300FM Rev. 5 pinned at NXP's
  own locator; the fresh fetch returned byte-identical bytes to the chipdoc-cached copy —
  two acquisition routes, one artifact, verified), `references.sexp` (the `dsp56300`
  candidate: tarball pin + build note + the path-demonstration experiment + the EVD-04
  independence rows — asm/emu share one project, gearmulator not-examined), and `DOSSIER.md`
  carrying the deferrals by name (`profile.sexp`/`state.sexp`/`encoding.sexp` → `.5` named
  schema cases; requirements, unit registration and the per-unit book → the model slice).
  `scripts/fetch_references.sh` gained a GENERIC source-tarball leg (discriminator: asset +
  source_commit + asset_sha256 — unreachable by the rv64 ledger, whose flow re-verified
  byte-behaviour-identical). **The gate census, measured:** every auto-discovering gate keys
  on `profiles/*/profile.sexp` or `profiles/*/encoding.sexp` (EXTRACTION, EXERCISE-COVERAGE,
  INTERACTION-MATRIX, PROFILE-CONSISTENCY, UNIT-COMPOSITION, SEMANTICS corpus) — the new
  directory is invisible to them until the schema-deferred documents land, then they attach
  with NO gate edit; GATE-REPORT iterates directories but only checks existing reports;
  FACT-OWNERSHIP's enumerated mirrors are untouched. Full `make gate` green with the
  dossier present. Lessons: `promotion: declined (the census is recorded where the next
  profile meets it — this leaf and DOSSIER.md's deferral table; the durable output is the
  measured answer "no gate edit needed", not a reusable method)`.
  Slice 3 is the model crate: `crates/semulith-dsp56300` — manual-derived decode + semantics
  for subset v0, the canonical-dump runner, and the checkpoint comparator.
  Slice 3 (`2026-10-01`, `SEMULITH-BR-0011`): the crate STANDS and the first differential
  case AGREES. `crates/semulith-dsp56300` (lib + runner bin): `machine.rs` (the full
  canonical register set, the 16-level hardware stack, the three bounded memory windows),
  `decode.rs` (the nine demo-path forms, every mask FM-cited), `exec.rs` (semantics + the
  FM Table 5-1 CCR rules + the DO loop machinery), `dump.rs` (the canonical dump,
  byte-compatible vocabulary, NO `cyc` line — timing is never emitted), `lod.rs` (the
  `.lod`/`.meta` dialects; fill headers refused by name), all outside-subset words typed
  `ModelStop`s. `scripts/compare_dumps.py` — the checkpoint comparator (field-exact, a
  missing key is a mismatch, `cyc` skipped by recorded rule; 4-arm self-test).
  `scripts/run_dsp56300_smoke.py` — the campaign driver (NOT a commit gate, same
  discipline as the RISC-V smoke; refuses unbuilt references). The micro guest adopted
  into `profiles/dsp56300-lab-v0/guests/`. **Verdict: AGREE over 53 fields** (registers +
  X/Y deviations + stack slots), `cyc` skipped — byte-identical to the reference's dump.
  Two findings owned on the spot (§15): (a) the FM's U-bit equation is an extraction
  INVERSION of its own prose ("identical" → XNOR; the reference's `sr c00310` is the
  arbiter and agrees with the prose) — recorded in `exec.rs`'s module docs; (b) the
  repo's FACT-OWNERSHIP convention reserves `crates/*/src/state.rs` for GENERATED state
  mirrors — the crate's hand-written state module is `machine.rs` until `.5` generates
  it. Lessons: `promotion: declined (the slice's durable outputs — the crate, the
  comparator, the measured inversion — live where the next evaluator meets them)`.
  Slice 4 is form-coverage completion: the ALU core (add/sub/cmp/and/or/eor, asr/lsr),
  jsr/rts, rep, the (Rn) addressing modes, and the guest corpus that exercises them.
  Slice 4 (`2026-10-01`, `SEMULITH-BR-0012`): the subset is FORM-COMPLETE and the corpus
  AGREEs 6/6. Decode gained the register/immediate data-ALU core (`0JJJd_kkk` /
  `01JJd_kkk` + the `$01408_`/`$0140C_` immediate classes), ASR/LSR, JSR/RTS, ENDDO,
  REP #xxx/REP S, and the seven linear (Rn) modes — every mask FM-cited and cross-checked
  against the pinned assembler's probe words (pinned in `decode.rs`'s tests). Guests
  `alu`, `shift`, `rn`, `rep`, `jsr` join `micro`: **`6 agree / 0 fail`** over the
  canonical end-state dumps (51–64 fields per case, `cyc` excluded by rule). The
  differential campaign caught and fixed five model defects, each traced tools-first
  (§15): (a) RTS pulled SR — the FM (13-168) pulls PC only, measured; (b) MOVE #xx to an
  accumulator zeroed A2 — the reference sign-extends through it (the FM's "remaining bits
  zeroed" prose falsified for A2); (c) A1/B1 memory reads ran my limiter — measured: the
  shifter/limiter sits on the whole-accumulator read path only, A1/B1 read raw (the FM's
  limiting prose over-applied by me, corrected by measurement); (d) S was set per ALU
  result — measured: S sets only on whole-accumulator bus reads, a path subset v0 does
  not decode; (e) a nibble-slip mask zeroed A2 on the 24-bit ops. Two latent boundary
  defects owned and fixed on the spot: accumulator-PART move destinations now stop by
  name at decode instead of panicking in `bus_write`, and the NOP citation (13-149 →
  13-145; the FM's own §13 TOC numbers pages differently from the printed footers, a
  measured FM-internal discrepancy). Guest-side defect owned: `move #$000002,x1`
  assembles to the SHORT form (x1 = $020000, not 2) — `#>` forces the long form; the
  typed `OutOfWindow` stop caught the runaway. The reference's emit source was consulted
  to LOCATE the limiter mechanism (TOOLBOX); the evidence is the dump agreement (EVD-04
  unchanged: asm/emu share one project, the claim stays EXPERIMENTAL). Named subset
  boundaries, all typed stops: register–register moves, accumulator-part move
  destinations, AGU registers as move-bus ends, modulo/reverse-carry (Mn ≠ $FFFFFF
  refuses by name), REP of two-word/control instructions (the FM's own A.3.8), REP at
  LA/LA-1, DO #0, REP S from non-word registers, multi-bit shifts.
  Lessons: `promotion: declined (the four measured rules live in exec.rs's module header where the next reader meets them; three were my over-applications of correct FM prose, one a genuine prose falsification — the arbiter discipline is already EVD-04/RK08)`.

## `.3` — the slice narratives (verbatim), archived the same day

  Slice 1 (`2026-10-01`, `SEMULITH-BR-0007`): the oracle-availability survey
  ([`artifacts/p3-breadth/2026-10-01-oracle-survey.md`](artifacts/p3-breadth/2026-10-01-oracle-survey.md))
  — TI C6000 ABSENT for execution (no OSS executor anywhere; the vendor simulator was
  discontinued in 2014), DSP56300 STRONG (MIT assembler + MIT silicon-validated emulator
  with a ready differential harness), SHARC ADSP-2106x PARTIAL (BSD-3 MAME core, but the
  assembler leg is unbuilt and no second oracle exists). Both load-bearing positives
  re-derived against primary sources. **Slice decision: DSP56300** (Decisions, `2026-10-01`).
  Slice 2 (`2026-10-01`): the path EXERCISED end-to-end, no Semulith DSP model involved —
  the reference pinned (commit `c60aeedb`, tarball sha256 `46b0e3e5…`, `target/refs/`
  discipline), built on-volume, a synthetic micro guest assembled (rc 0) and executed
  headless with a full canonical-state dump; verified three independent ways (hand
  arithmetic reproduces the 56-bit accumulator exactly; `--dump-mem` shows the X/Y-space
  stores landing right; the one surprising value — `#$5` → `x1=050000` — traced to
  DSP56300FM §3.4.1.3, matching the manual). Record:
  [`artifacts/p3-breadth/2026-10-01-evidence-path-demo.md`](artifacts/p3-breadth/2026-10-01-evidence-path-demo.md).
  The acceptance's working path is DEMONSTRATED; no experimental-claim fallback needed.
  Defect owned (§15, surfaced by this slice's build): the reference build grew the
  on-volume cargo store, and FIXTURE-FINGERPRINT — which scans the raw tree for JSON
  records — choked on a dependency's deliberately malformed parser fixture
  (`chumsky-0.13.0/examples/sample.json`, UNPARSEABLE). The gate's own rule covers OUR
  records; `.app-data` is a cache of other projects' sources, the `vendor/` exclusion's
  exact class — added to the exclusion list with the reason recorded in the file.
  Lessons: `promotion: declined (the survey and the demonstration are dated evidence living where the next evaluator meets them; their durable outputs — the slice decision and the demonstrated path — are recorded in this tree's Decisions and Verification Log)`.

## `.2` — the hook-census narrative (verbatim), archived the same day

  Census (`2026-10-01`, full-pipeline audit): **no opaque hook exists.** Census basis
  (GAP-CLAIM-CENSUS): every Rust-emitting generator (`gen_definition.py`, `gen_state.py`,
  `gen_guests.py`) and every shared definition reader (`riscv_asm.py`, `dossier_sexp.py`,
  `check_semantics.py`, `check_sexp_schema.py`) was read along its error paths — all refuse
  by name with rc ≠ 0 (the `Refusal` pattern); the runtime dispatch is a closed `Sem` enum
  with no catch-all (a new variant fails COMPILATION in every consumer); the workspace
  carries no feature flags, no callback tables, no per-target hand-written semantics. Three
  DESIGNED seams exist, already typed contracts rather than escape hatches: the
  `Environment` boundary trait (`env.rs` — ARCHITECTURE §3's sanctioned plug point; it can
  only answer typed failures, never alter instruction behaviour), the mutation seam
  `step_over` (`P1-LAB.9`'s detector fixture: same evaluator, mutated data), and the bench
  `Observer` (a measurement sink that cannot affect execution).
  Defect found, owned, FIXED (§15): `exec.rs`'s operand extraction had a live SILENT arm —
  an operand naming no field was skipped, justified by a comment whose premise `P2-SCALAR.1`
  had falsified (FENCE's `fm`/`pred`/`succ` carry field ranges since). Fix: the generator
  now REFUSES an unfielded operand by name (rc 2 — ARCHITECTURE §2's rule made mechanical,
  with a RED self-test arm proving the refusal fires); the runtime arm is a loud
  `ModelError`; the test ratchet lost its dead whitelist; four stale justification sites
  swept; `gen_fragments.py`'s dead `_unused_build`+`HEADER` (naming a nonexistent
  `gen_encoding.py`) removed. Repro (pre-fix): an insn declaring operand `rs9` generated
  without protest and extracted nothing for it; post-fix the generation refuses, naming
  `rs9`. Future target-driven hooks (F6's readout semantics, e.g. a sign-extended
  accumulator-extension read) land with the profile that demands them — `.1`'s gating.
  Lessons: promoted → `docs/knowledge/a-dead-justification-camouflages-a-silent-path.md`.
