# P3-BREADTH: stabilize only what has been demonstrated

## Metadata

- Tree ID: `P3-BREADTH`
- Status: `done` (`2026-10-01` — gate `BREADTH` RUN, verdict **`passed`**; `.1` stays
  `slice-gated` on the record, its conditional legs reopening by name)
- Roadmap lane: `ROADMAP.md` §6 → **P3 — Exercise breadth and stabilize only what is demonstrated**
- Gate: `BREADTH`
- Depends on: `P2-SCALAR` (gate `CPU-LAB`), `DSP-REVIEW`
- Unlocks: the **stable cross-architecture API** claim
- Created: `2026-09-13`
- Owner: repo-local workflow

## Goal

Turn `DSP-REVIEW`'s findings into actual interface changes, take a narrow real DSP slice **only
if** its evidence path can be demonstrated, and only then permit the claim that the public
abstraction is stable across architectures.

## Non-Goals

- No claim over unsupported families. A gate that makes an abstraction "general" by leaving
  families unmentioned has claimed them.
- No blocking of architecture-specific CPU progress. `P4-SYSTEM` proceeds in parallel; only the
  *stable general API* claim waits for this gate (`ROADMAP.md` §6).

## Acceptance Criteria — gate `BREADTH`

The stated real subset has evidence; the public abstraction supports the exercised cases;
unsupported families remain unclaimed.

## Task Tree

- ID: `P3-BREADTH.1` — **apply the interface findings**
  Status: `slice-gated` (executable-now scope done `2026-10-01`; the F6 census leg landed for
  dsp56300-lab-v0 `2026-10-01`; the remaining implementation legs — F2/F4/F5 — await a
  VLIW/TI slice decision)
  Goal: implement the abstraction changes `DSP-REVIEW.7` classified as required.
  Acceptance: every change traces to a numbered finding; scalar regression evidence for `rv64i-lab-v0` is preserved and re-run (`EVD-07`).
  Applied `2026-10-01`: the required-**unconditional** set measured **empty** — F2/F4/F5 are TI/VLIW-conditional, F6 fires per new profile (Decisions, `2026-10-01`). F2 gained its executable demonstration (synth probe 5: `undeclared field "register_groups"`, rc 1 — the report's named honest route); scalar regression re-run green (`make check` 180/180, gen_state rc 0, DEF-GEN ok, G1 `passed` re-derived).
  Lessons (slice 1): `promotion: declined (per-slice application of the report's own named remedy; the durable method — a finding without an executable demonstration gets a synth probe — lives in the findings report and the synth README where the next reader meets it)`.
  F6 census leg (`2026-10-01`, `SEMULITH-BR-0013`): the SEM-08 method re-run for the
  exercised dsp56300-lab-v0 profile — 14 candidates answered, never by silence: the
  accumulator-extension readout PRESENT and measured (A2/B2 sign-extended, A1/B1 raw —
  `.4`'s pinned readouts harvested), M0–M7/L/S/DO-stack/stale-slots PRESENT and declared,
  REP working state ABSENT beyond the declared LC, the pending-writes window (F5) ABSENT
  (scalar issue), CSRs/reservation/FP/vector/privilege ABSENT architecturally or by named
  exclusion. Consequence: **the canonical end-state dump IS the complete architectural
  state** for subset v0 — the surface-completeness argument (slot 0 unwritable, P-low
  constant, the harness window excluded by the harness's own contract) plus the measured
  6/6 agreement. Record:
  [`artifacts/p3-breadth/2026-10-01-dsp56300-state-census.md`](artifacts/p3-breadth/2026-10-01-dsp56300-state-census.md)
  — the measured input `.5`'s `state.sexp` cases (special-register census, F1 widths, F3
  spaces) harvest. The leaf stays `slice-gated`: F6 fires per new profile and F2/F4/F5 stay
  conditional on a VLIW/TI slice.
  Lessons (F6 leg): `promotion: declined (the census method was already durable — state.sexp's hidden_state_census and this record's re-run of it; the durable output is the measured answer "the dump is complete", recorded where .5 meets it)`.

- ID: `P3-BREADTH.2` — **opaque semantic hooks made explicit**
  Status: `done` (`2026-10-01`, `SEMULITH-BR-0006`)
  Goal: where a target needs behaviour the generic layer cannot express, the hook states its contract, its state, and which backends support it.
  Acceptance: no hook is a silent escape hatch; an unsupported construct is a **model-generation failure**, not a guessed translation (`docs/ARCHITECTURE.md` §2).
  The full-pipeline audit narrative (the census basis, the three designed seams, and the silent-extraction defect found and fixed) lives verbatim in [`archive/P3-BREADTH.md`](archive/P3-BREADTH.md). Result: no opaque hook exists (measured); the one live silent arm became a generation-time refusal (rc 2) plus a loud `ModelError`, with a RED self-test arm proving the refusal fires.

- ID: `P3-BREADTH.3` — **real DSP slice: evidence path first**
  Status: `done` (`2026-10-01` — slice 1 the survey, slice 2 the demonstration)
  Goal: demonstrate the evidence path for a candidate real DSP subset **before** implementing it.
  Acceptance: either a working path is demonstrated, or the work proceeds as a deliberately limited **experimental** claim that says so. `SRC-02`: a missing reference route prevents the associated evidence claim, not honest experimental work.
  The slice narratives (the oracle-availability survey — TI C6000 ABSENT, DSP56300 STRONG, SHARC PARTIAL — and the end-to-end evidence-path demonstration) live verbatim in [`archive/P3-BREADTH.md`](archive/P3-BREADTH.md). Result: the slice decision is DSP56300 (decided by the evidence path per RK08), and the path was EXERCISED here end-to-end — pinned, built, a micro guest assembled and run headless, the dump verified three independent ways.

- ID: `P3-BREADTH.4` — **the bounded real subset**
  Status: `done` (`2026-10-01` — slices 1–4: subset selected, dossier, the model crate,
  form-coverage completion + the guest corpus, all differentially AGREE)
  Goal: implement and evidence the narrow slice selected in `.3`.
  Acceptance: its claim names the exact subset; a source-reviewed experimental subset cannot inherit a differentially validated claim from another target (`docs/EVIDENCE_AND_GATES.md` §1).
  The full slice narratives (subset selection, dossier, the model crate, form-coverage + the guest corpus — with the five measured model corrections, each root-caused tools-first) live verbatim in [`archive/P3-BREADTH.md`](archive/P3-BREADTH.md). Result: subset v0 is form-complete and differentially agreed — six synthetic guests AGREE 6/6 over canonical end-state dumps (51–64 fields per case, `cyc` excluded by rule); the crate's 17 tests are the commit-level proof.

- ID: `P3-BREADTH.5` — **schema and generator functionality where justified**
  Status: `done` (`2026-10-01` — slices 1–3: the state schema learned the census's
  shapes, the profile schema's scope taxonomy generalized, the encoding case measured and
  deferred with named reopening conditions)
  Goal: extend the definition schema/generator only where an exercised target demonstrates the need.
  Acceptance: each extension names the target and case that required it.
  Slice 1 design (recorded before code, `2026-10-01`): **the state schema learns the
  census's shapes; the refusal boundary moves one layer down, measured.** The F6 census
  record (`artifacts/p3-breadth/2026-10-01-dsp56300-state-census.md`) is the content source;
  the exercising target is dsp56300-lab-v0 (6/6 AGREE).
  - `schema/state.sexp` gains optional constructs, each naming its case in the header:
    `register_family` (+ `parts` with per-part `readout` — census candidate 1, the A2/B2
    sign-extended readout; F1 masked widths), `memory_spaces` (F3 — the X/Y/P spaces),
    `hardware_stack` (census candidates 4/6 — 16×48-bit, pre-incremented SP, stale slots
    observable); `xlen` and `integer_registers` become OPTIONAL (case: dsp56300-lab-v0 has
    no XLEN concept and no x0-anchored integer file — forcing either would be a lie the
    schema exists to prevent). The "at least one register declaration" completeness check is
    stated as belonging to the consistency/generator layer, not the type schema.
  - `scripts/dossier_sexp.py` (the single mapping owner) learns to CARRY the new forms
    (parse + emit): measured pre-change, `state_to_doc` builds the doc from named fields
    only — a `memory_spaces` form would be silently DROPPED between the schema layer and
    the generator, the exact silent-path class `.2` eliminated for operands. After the
    change every declared form reaches the generator as data.
  - `scripts/gen_state.py` refuses each new construct by name (rc 2, naming the case and
    the work) — the refusal moves from the schema layer to the generator layer, never away;
    a missing `xlen` becomes a Refusal, not a KeyError traceback.
  - `scripts/check_state_gen.sh` gains the RED arms for the new refusals.
  - Synth probe 2 RE-PINS: `state-spaces.sexp` was pinned at the schema refusal
    `undeclared field "memory_spaces"` (rc 1); the schema now declares the shape, so the
    pin moves to `gen_state.py`'s refusal (rc 2). The suite's own contract covers this:
    "the day the pipeline genuinely supports a shape, its pin goes stale and the suite
    turns RED — measuring the boundary moving." The README records the move, dated, with
    the case.
  - **The DSP's `state.sexp` does NOT land in this slice.** Measured: PROFILE-CONSISTENCY
    iterates `profiles/*/profile.sexp` and reads `state.sexp` only when the profile exists
    (`check_profile_consistency.sh:71,98-99`), and STATE-GEN is rv64-hardcoded
    (`check_state_gen.sh:26`) — a `state.sexp` landed without `profile.sexp` would be a
    document no gate reads, an ungoverned claim. It lands with the scope-taxonomy slice,
    where PROFILE-CONSISTENCY's attachment (and its scalar-shaped arms) is measured.
  Slice 1 (`2026-10-01`, `SEMULITH-BR-0014`): the boundary MOVED, measured. The schema
  declares `register_family` (+ `parts`/`readout`), `memory_spaces`, `hardware_stack`,
  with `xlen`/`integer_registers` optional — each construct's comment names
  dsp56300-lab-v0 and its case. `dossier_sexp.state_to_doc`/`state_to_form` carry the new
  forms (the silent-drop path between schema and generator is closed — measured
  pre-change: the mapping built the doc from named fields only). `gen_state.py` refuses
  each by name (rc 2), and a missing `xlen` is a Refusal instead of a KeyError. Synth
  probe 2 did what the fixture exists to do — its pin went stale and the suite turned RED
  on the first run, then re-pinned one layer down (schema accepts rc 0; generator refuses
  `memory_spaces declared`, rc 2; 6/6). STATE-GEN's self-test grew four RED arms (10/10).
  rv64 regression: `state.sexp` re-validates against the extended schema, regeneration is
  byte-identical, the doc round-trip is data-equal.
  Lessons: `promotion: declined (the move-one-layer-down pattern is the synth fixture's own designed behaviour, already written in its README; the silent-drop close is the .2 lesson's second instance — the promoted record a-dead-justification-camouflages-a-silent-path already carries the generalizable shape)`.
  Slice 2 design (recorded before code, `2026-10-01`): **the profile schema's scope
  taxonomy generalizes; the DSP documents are DRAFTED as artifacts and their gate
  attachment is MEASURED — they land only when they can be governed.** Findings the design
  rests on, all measured this slice:
  - The gates' scope readers are already generic over group NAMES
    (`check_exercise_coverage.sh` skips count_*/authority/source and unions the rest;
    PROFILE-CONSISTENCY's `listed` counter sums list values) — the taxonomy's scalar shape
    lives in exactly two closed places: `schema/profile.sexp`'s scope construct and
    `dossier_sexp._SCOPE_LISTS` (which REFUSES an undeclared field by name). The honest
    minimal extension is per-case named optional fields, zero reader change — the readers'
    genericity is the original design intent confirmed.
  - PROFILE-CONSISTENCY's arms are presence-conditional (XLEN MISMATCH only when both
    sides carry xlen; REG COUNT only when the profile's state block declares
    integer_registers; PARTS DRIFT only when both part-counts exist), so the DSP documents
    pass it with no gate edit IF the schema lets them omit xlen / count_rv64i_additions /
    the integer-file scalars — each omission named by case (no XLEN concept; no RV64I
    base/additions split; registers are families).
  - The DSP documents land as `profiles/dsp56300-lab-v0/{profile,state}.sexp` in a LATER
    slice: landing attaches EXTRACTION, EXERCISE-COVERAGE and INTERACTION-MATRIX, whose
    contracts presume the rv64 evidence shape (encoding composition, per-step
    `*.expected.sexp` guests, the matrix) — their measured verdicts on the DSP unit are
    recorded in the slice record, and the landing slice is the one that can keep them
    green honestly (the encoding/evidence-shape machinery, or a named deferral with its
    owning leaf — WAIVER-ROUTING's shape). Until then the drafts live under
    `docs/tasks/artifacts/p3-breadth/dsp56300-dossier/`, schema-validated — measured
    content, not landed claims.
  Slice 2 (`2026-10-01`, `SEMULITH-BR-0015`): the taxonomy generalized and the attachment
  MEASURED. `schema/profile.sexp`: `xlen`, the state block's integer-file scalars and
  `count_rv64i_additions` are now optional; the scope gained the DSP's five group fields
  (moves/alu_core/multiplies/flow/loops) — no reader changed (the gates were already
  generic over group names). `dossier_sexp._SCOPE_LISTS` extended in the same commit (the
  two closed places the taxonomy lives). The drafts stand and validate
  (`artifacts/p3-breadth/dsp56300-dossier/{profile,state}.sexp` — 19-mnemonic scope,
  5 families + parts, 3 spaces, the stack, 12 special registers, the 14-candidate census
  as data; both load through the mapping owner and round-trip data-equal).
  **The attachment measurement** (drafts placed untracked + intent-to-add, gates run in
  their committed modes, then removed): PROFILE-CONSISTENCY GREEN on the DSP dossier
  (2 dossiers) — after it surfaced three REAL latent defects in the already-tracked
  `references.sexp`, fixed in this slice (§15): an `obtained` candidate missing
  `binary`/`binary_sha256`/`injection` (SRC-03's checkable-availability fields — supplied,
  digests measured) and four UNKNOWN MODEL pairs (the asm/emu legs and gearmulator
  registered as first-class candidates, the pairs re-labelled to candidate ids).
  EXERCISE-COVERAGE RED: NO COMPOSITION (no encoding.sexp), 19 UNRESOLVED FORM, no
  exercised set (the DSP's guests are checkpoint-compared `.a56`, not `*.expected.sexp`).
  EXTRACTION RED: INSUFFICIENT — no encoding.sexp. INTERACTION-MATRIX RED: NO MATRIX.
  Gate defect owned and fixed (§15): EXERCISE-COVERAGE's denominator counted a `(comment
  …)` inside scope as mnemonic prose (measured with the draft) — it now skips the reserved
  annotation head, with a GREEN self-test arm (8/8). Another latent defect owned and fixed:
  `profiles/rv64i-lab-v0/profile.sexp`'s D-FENCE carried two `note` fields against the
  schema's single-valued declaration — ungated drift, found by re-validating the corpus
  this slice; the notes merged. And `check_sexp_schema.py` tracebacks on a missing
  input file — now a clean rc-2 refusal with a RED arm (51/51).
  **Surfaced finding, owned and routed (§9/§15):** the dossier documents (profile, state,
  sources, references, encoding, interactions, …) are NOT schema-validated by any gate as
  a class — only RECORD-SCHEMA's record files are; the gates consume them through the
  strict mapping owner, which refuses undeclared fields but not facet violations, so the
  D-FENCE drift lived unseen. The owning slice is `.5`'s landing slice: the commit that
  lands the DSP documents adds the schema-validation leg for the dossier documents (the
  census for the gate: this slice's per-document re-validation).
  Lessons: `promotion: declined (the attach-then-measure method is this tree's own — .4 slice 2's gate census was the same move; the durable output is the measured attachment table, recorded here where the landing slice meets it)`.
  Slice 3 (`2026-10-01`, `SEMULITH-BR-0016`): the ENCODING case measured and
  dispositioned — `.5` closes; the dossier landing becomes leaf `.7`. The measurement,
  from the pinned sources: `gen_definition.py` refuses a second unit at three named walls
  — the profile scope (`a second unit is generator work, not a config knob`), the decode
  width (`emits a 32-bit decode table only`; the DSP fetches 24-bit words), and the
  semantics corpus (every declared instruction needs a `.sem.sexp`; the DSP's semantics
  are hand-written Rust in the sibling crate, not data). The semantics LANGUAGE is
  scalar-shaped, measured against `schema/semantics.sexp` (31 operators):
  `(load width signed? addr)` / `(store width addr value)` carry NO space parameter
  (F3's semantics face), state access is `reg`/`pc` only (no accumulator parts, no
  LA/LC/LF, no hardware stack, no SR flags as settable state), and there is no
  masked-width wrap or loop construct — the DSP's X/Y/P moves and do/rep machinery would
  be refused by name, the same class synth probe 4 pinned for `delay`. So the encoding
  generalization is a LANE (a DSP fragment family + 24-bit decode emission + the
  semantics-data re-expression + `Sem` enum variants), not an extension — and no current
  milestone consumes it: the sibling crate is the exercised, differentially agreed
  vehicle (`decision_dsp56300-lab-v0-subset`), and `decision_lane-consumption` descopes
  lanes no milestone consumes. **Decision: the encoding case is measured and DEFERRED**,
  reopening conditions named — a corpus extension beyond subset v0 (the parallel-move
  dual feed), a third unit arriving, or the landing leaf choosing the machinery route.
  `.5`'s acceptance is met: every landed extension (slices 1–2) names dsp56300-lab-v0 and
  its case; the one case measured and not built names its conditions. **The dossier
  landing is leaf `.7`**, owning the measured attachment table, the disposition choice
  (named deferrals vs evidence-shape machinery — the slice-2 record), and the surfaced
  schema-validation leg for the dossier documents.
  Lessons: `promotion: declined (the measurement is recorded where the next evaluator meets it — this leaf and .7's measured input)`.

- ID: `P3-BREADTH.6` — **the `BREADTH` gate report**
  Status: `done` (`2026-10-01` — slices 1–3: the DSP records, the unit registration +
  per-unit book, the report itself; gate `BREADTH` RUN, verdict **`passed`**)
  Goal: generate from pinned inputs; publish the capability report.
  Acceptance: families with no evidence are listed as **unclaimed**, explicitly.
  Slice plan (recorded before code, `2026-10-01`; reordered mid-flight, measured): three
  slices, each a governed landing —
  1 = the DSP's `requirements.sexp`/`contract-obligations.sexp` records (RECORD-SCHEMA
  attaches on landing with zero gate edits — the catalogues auto-discover);
  2 = the unit registration + per-unit book (`units.sexp` + the category-needs census +
  a book that builds; `gen_model_book.py` learns the sibling-crate shape — the measured
  blocker: it requires exactly one `encoding_source`, requires `encoding.sexp`, and reads
  `state["integer_registers"]`; each extension names the DSP case);
  3 = the BREADTH report itself (`gate_report.py` gains the cross-unit builder;
  `check_gate_report.sh` gains a repo-level leg; the report lives at
  `docs/BREADTH-REPORT.md` because this gate is cross-architecture, not a profile's).
  **The reorder, measured:** the report's claim list IS the unit registry (a family is
  claimed exactly by a registered unit), so a report generated before the registration
  reads "1 registered unit" and lists the DSP56300 family — whose evidence axis 1 just
  measured green — as UNCLAIMED. The capability report must be the leaf's capstone, not
  its middle slice.
  Slice 1 design (recorded before code, `2026-10-01`): **mirror the rv64i pattern exactly,
  at the DSP's size.** Seven decisions in `profile.sexp` ⇒ seven `REQ-D-*` requirements
  (COVERAGE: statements byte-identical), kinds/categories/risks assigned per record;
  seven `OB-*` cpu-guarantee mirrors (MIRROR: the statement restated verbatim; AUTHORITY:
  `defined` ⇒ `architecture`, the laboratory decisions ⇒ `laboratory`) plus six
  `OB-ENV-*` environment-assumptions carrying the laboratory's half of the contract
  (VIRTUAL-TIME — `cyc` never compared; ORDERING — scalar issue, the F5 window measured
  ABSENT; RESET — D-RESET-STATE's cold reset; FETCH-SUPPLY — one 24-bit P-space word per
  fetch; EVENT-DELIVERY — no asynchronous events in subset v0; PARTIAL-PROGRESS — each
  instruction completes or stops as a unit). Every `source_refs` cites `DSP56300FM` (the
  one pinned source; CITED). Contract id `dsp56300-lab-env-v0`. `implementation_status`
  stays `planned` — the sibling's convention: the record tracks the check fixtures, which
  no milestone has routed (the model's implementation is the crate's, measured elsewhere).
  Slice 1 (`2026-10-01`, `SEMULITH-BR-0019`): the DSP's records LAND, governed. Seven
  `REQ-D-*` requirements (statements byte-identical to the decisions; every `source_refs`
  cites `DSP56300FM` — CITED) and thirteen obligations: the seven `OB-*` mirrors
  (`defined` ⇒ `architecture`; the laboratory decisions ⇒ `laboratory`) plus six
  `OB-ENV-*` environment-assumptions (VIRTUAL-TIME — `cyc` never compared; ORDERING —
  scalar issue, the F5 window measured ABSENT; RESET; FETCH-SUPPLY — one 24-bit P-space
  word per fetch; EVENT-DELIVERY — no asynchronous events in subset v0;
  PARTIAL-PROGRESS — completes or stops as a unit), contract `dsp56300-lab-env-v0`, 26
  declared checks. RECORD-SCHEMA attached on landing with ZERO gate edits (auto-discovery
  measured: 10 record files green on the first run). FACT-OWNERSHIP gained the DSP's
  requirements/obligations rows — and its self-test fixture did what it exists to do: the
  GREEN fixture's pair glob follows the REAL corpus, so the landing turned it RED
  (`UNREGISTERED MIRROR PAIR` — the DSP's obligations pair unnamed in the fixture
  registry); re-pinned to the two-unit corpus (`__CHECKED__ 5 → 6`) with the reason in
  the check's comment — the same designed staleness the synth probes carry.
  Lessons: `promotion: declined (the fixture-repin-on-landing behaviour is the gate's own
  designed staleness, now recorded in the check's comment where the next landing meets it;
  the records' shape is RECORD-SCHEMA's rules applied, not a new method)`.
  Slice 2 (`2026-10-01`, `SEMULITH-BR-0020`): the unit REGISTERED, its book STANDING.
  `gen_model_book.py` learned the sibling-crate shape, each extension naming the DSP case:
  `emit_encoding` emits the declared-vehicle fragment when no `encoding_source` exists
  (the refusal stands without the declaration — applicability derives from the vehicle
  block, `decision_gate-applicability-by-declared-vehicle`); `emit_contracts` treats
  `encoding.sexp` as the ONE document a sibling-crate unit may lack (the row names the
  deferred lane), reads register families/spaces/stack when `integer_registers` is
  absent, and counts the `.a56` checkpoint corpus when no `*.expected.sexp` guests
  exist. rv64i regression measured byte-exact: every fragment differs ONLY in the
  generator-digest header line. `units.sexp` gained the DSP row (requires: the 14
  categories its scope needs — C17 in, C14 out against rv64i's set: reset is this unit's
  own decision, interrupts a named exclusion); the 24-row category-needs census landed
  with honest dispositions (8 covered, 6 partial, 3 missing-with-closing-routes, 4
  out-of-scope — the architecture never owed them, 3 deferred-to-board). The book
  `docs/models/dsp56300-lab-v0/` stands: the five-part arc in six chapters, the bill's
  12 sections each carrying its does-not-supply. Every attaching gate green on first
  full run: UNIT-BOOKS (2 units, both build), MATERIALS-BILL (12 materials, fragments
  match, every section negative), SCOPE-COVERAGE (2 units may code), FACT-OWNERSHIP (29
  kinds — the four fragment mirrors registered).
  Lessons: `promotion: declined (the applicability-from-declared-vehicle pattern is the
  .7 decision applied to a new consumer — the durable rule lives in
  decision_gate-applicability-by-declared-vehicle; the per-unit INTERNAL_CONTRACTS
  question was answered by keeping the constant and making the ROW honest, recorded here)`.
  Slice 3 (`2026-10-01`, `SEMULITH-BR-0021`): the BREADTH gate RUNS — verdict
  **`passed`**, published. `gate_report.py` gained the cross-unit builder
  (`--gate BREADTH`, no profile — the gate spans every registered unit), deriving the
  three roadmap axes from tracked files by concrete artifact name: axis 1 (the stated
  real subset has evidence) measures six anchors for dsp56300-lab-v0 — the declared
  scope + vehicle, the `.a56`+`.meta` corpus, the crate's 17 commit-level tests, the
  differential driver, the recorded comparison contract, the registered
  smoke-agreement mechanism — plus the scalar unit's GC record standing; axis 2 (the
  public abstraction supports the exercised cases) measures all nine constructs
  DECLARED in their schema AND CARRIED by the mapping owner, with the refusal boundary
  pinned by the five synthetic probes; axis 3 (unsupported families remain unclaimed)
  reads the claim list from the unit registry (2 units) and lists the surveyed
  families explicitly — TI C6000 (ABSENT for execution) and ADI SHARC (PARTIAL)
  unclaimed, everything else unclaimed by omission. EVD-08's shape holds: the
  generator has no code path to `passed` while an axis's anchors are absent. The
  report lives at `docs/BREADTH-REPORT.md` (a cross-architecture gate cannot be owned
  by a profile directory), and `check_gate_report.sh` gained the repo-level leg — the
  same regenerate-never-edit enforcement and the same three self-test controls (12/12;
  4 reports in sync). The report's own "what passed does NOT mean" bounds the claim:
  exercised cases only; no DSP56300 family compatibility; no RISC-V conformance
  upgrade; the slice-gated `.1` legs (F2/F4/F5) named. **The tree closes:** every
  leaf dispositioned — `.1` stays `slice-gated` on the record (its conditional legs
  reopen by name with a VLIW/TI slice decision), the gate's verdict is published, and
  the stable-API claim the tree guarded is permitted exactly where the report permits
  it.
  Lessons: `promotion: declined (the report's axes are the roadmap's gate text measured,
  not a new method; the repo-level-report placement rule is written in
  check_gate_report.sh's header where the next cross-architecture gate meets it)`.

- ID: `P3-BREADTH.7` — **land the dsp56300-lab-v0 dossier as governed documents**
  Status: `done` (`2026-10-01` — slices 1–3: the vehicle declaration + the gate legs, the
  DSP matrix + DOSSIER-SCHEMA + the FACT-OWNERSHIP pairing fix, the landing)
  Goal: move the schema-validated drafts (`docs/tasks/artifacts/p3-breadth/dsp56300-dossier/`)
  to `profiles/dsp56300-lab-v0/{profile,state}.sexp` with every attaching gate green
  honestly — never by landing a document no gate reads.
  Acceptance: `make gate` green with the documents landed; EXERCISE-COVERAGE, EXTRACTION
  and INTERACTION-MATRIX dispositioned BY NAME (the evidence-shape machinery or declared
  deferrals — the disposition choice is this leaf's design decision, made from the
  measured attachment table); the dossier schema-validation leg added (the surfaced gap:
  no gate schema-validates the dossier documents as a class — the D-FENCE drift lived
  unseen for it); the artifact copies removed when the governed documents land.
  Measured input: `.5` slice 2's attachment table (`2026-10-01`): PROFILE-CONSISTENCY
  green on the DSP dossier; EXERCISE-COVERAGE RED (NO COMPOSITION, 19 UNRESOLVED FORM, no
  exercised set — the DSP's guests are checkpoint-compared `.a56`, not
  `*.expected.sexp`); EXTRACTION RED (no encoding.sexp); INTERACTION-MATRIX RED (no
  interactions.sexp).
  Disposition (decided `2026-10-01`, director-delegated; full record
  `decision_gate-applicability-by-declared-vehicle`): **applicability derived from the
  declared vehicle + the unit's documents — no deferral machinery, no fiction
  machinery.** The unit declares `(vehicle (route sibling-crate) (comparison
  checkpoint-end-state))`; gates apply the contracts matching the declaration and refuse
  a declaration/documents mismatch (a stale declaration fails, never drifts).
  EXERCISE-COVERAGE gains the guest census both directions (declared scope vs the `.a56`
  corpus); EXTRACTION reports the sibling-crate route and applies the composition
  contract iff `encoding.sexp` exists; INTERACTION-MATRIX needs NO gate change — the DSP
  lands a real minimal matrix (6 axes, 21 cells, mechanism/degenerate dispositions; the
  closed mechanism registry gains two DSP entries, each naming its case). The dossier
  schema-validation gate is a new doctrine (the surfaced gap). Slices: 1 = the vehicle
  declaration + the EXTRACTION/EXERCISE-COVERAGE legs, measured against the drafts;
  2 = the DSP matrix + the schema-validation gate; 3 = the landing.
  The full slice narratives (the vehicle declaration + the two gate legs; the DSP matrix,
  DOSSIER-SCHEMA — the 30th doctrine — and the FACT-OWNERSHIP same-unit pairing fix; the
  landing) live verbatim in [`archive/P3-BREADTH.md`](archive/P3-BREADTH.md). Result: the
  three schema-validated documents landed in `profiles/dsp56300-lab-v0/` with every
  attaching gate green (EXERCISE-COVERAGE 19/19, EXTRACTION sibling-crate reported,
  INTERACTION-MATRIX 21 cells resolving, PROFILE-CONSISTENCY 2 dossiers, DOSSIER-SCHEMA
  62 validated / 2 skipped-by-name, FACT-OWNERSHIP 23 kinds); the DOSSIER's rows read
  present/deferred with owners. `.7` DONE.
  Lessons: `promotion: declined (the interlock lesson — derived counts measure the working tree, so co-developed slices land in one commit — is recorded here where the next batch meets it)`.
  Lessons: `promotion: declined (the landing mechanics are recorded in the leaf; the durable rule — never land a document no gate reads — was already the leaf's goal)`.

## Current Frontier

| Order | Leaf | Status | Why next |
| --- | --- | --- | --- |
| — | — | — | the tree is DONE: gate `BREADTH` RUN `2026-10-01`, verdict **`passed`** (`docs/BREADTH-REPORT.md`, GATE-REPORT-gated) |
| — | `P3-BREADTH.1` | `slice-gated` | executable-now scope done `2026-10-01`; the F6 census leg landed for dsp56300-lab-v0 (`SEMULITH-BR-0013`) — F6 refires per new profile; F2/F4/F5 (TI/VLIW) stay unbuilt, recorded — reopens by name with a VLIW/TI slice decision |

## Decisions

- `2026-09-13`: a stable general API **requires** this gate; architecture-specific CPU progress
  does not (`ROADMAP.md` §6).
- `2026-10-01` (`.1` applied): the findings' **unconditional** implementation set is empty,
  measured. F4/F5 carry the review's own condition — a VLIW slice in `.3` requires them, a
  scalar-DSP slice does not. F2's implementation idles unless the slice is TI (the review's
  routing note), and implementing grouping without an exercised target would be exactly the
  speculative generality this tree exists to refuse — `.5`'s acceptance requires each schema
  extension to name the target and case that required it. F6's method exists and is gated;
  its work is per-profile, so it fires when `.3`/`.4` bring one. What `.1` owed NOW was the
  evidence upgrade the report named: F2 was the one finding classified from a document's
  shape, not a measured refusal — synth probe 5 (`state-groups.sexp`, `undeclared field
  "register_groups"`, rc 1) makes it executable, and the scalar regression was re-run green
  (`EVD-07`: no code changed; `make check` 180/180 + the generation controls + the G1
  verdict re-derived). The implementation legs stay owned HERE — `.1` is `slice-gated`, not
  closed: choosing a VLIW or TI slice in `.3` reopens it by name.
- `2026-10-01` (`.3` slice 1): **the candidate real slice is DSP56300**, decided by the
  evidence path per `RK08`, not by manual convenience: it is the only measured family with
  a complete, license-clean route (MIT assembler roundtripped against the vendor assembler;
  MIT emulator silicon-validated by its authors with a canonical-state differential harness
  that IS this project's workflow). SHARC-2106x remains the PARTIAL alternative (MAME's
  BSD-3 core is real and scriptable, but no vendorable assembler exists and there is no
  second oracle); TI C6000 gets no real slice — no pinnable executor exists, so its findings
  (F2/F4/F5) stay conditional and TI-shaped exploration is the synthetic composed-DSP
  fixture's job, never a compatibility claim. Consequences named now: a scalar-DSP slice
  means F4/F5 stay unbuilt (recorded, not lost — a future VLIW target reopens `.1` by name),
  F2 idles, and `.5`'s F1/F3 generator work gains its exercising target.

- `2026-10-01` (`.4` slice 1): **the bounded subset is `dsp56300-lab-v0` subset v0**, selected
  against the reference's measured coverage (instruction-complete) and its documented gaps
  (LIMITATIONS bounds the claim axes: no modes, no stack extension, no verified peripheral
  interrupts, no timing). The subset is non-parallel moves (A2/B2 readout included), the
  immediate/register ALU core, signed `mpy`/`mac`, `nop/jmp/jsr/rts`, `do`/`enddo`/`rep`,
  linear addressing; the exclusions are each named with a reason, and the parallel-move
  dual-feed axis is deferred as the first named extension candidate. The vehicle is a new
  sibling crate (`crates/semulith-dsp56300`, EXPERIMENTAL, manual-derived and per-form
  cited): the pipeline refuses a second unit by name, that generator work is `.5`'s by this
  tree's own routing, and building it first would be the speculative generality P3 exists
  to refuse; a sibling crate also keeps the gated scalar model byte-untouched. The
  comparator is checkpoint-level canonical end-state equality (the difftest harness's own
  engine-agnostic contract), not the RISC-V per-step walk. Full record:
  `decision_dsp56300-lab-v0-subset`.

## Open Questions

- ~~Whether any real DSP oracle becomes available at all.~~ ANSWERED `2026-10-01` (`.3`):
  yes — DSP56300 has a complete license-clean path (STRONG), SHARC-2106x a partial one; only
  TI C6000 has none. And the path reproduces HERE: slice 2 pinned, built, assembled and ran
  a micro guest headless with the canonical dump verified three ways. No experimental-claim
  fallback was needed.

## Design Discussions

- `2026-10-01` (director, `[DBINP]`): **a DSP as composition, not monolith** — the measured
  per-axis menu, the composition rules as the research content, abstraction as
  simplification with validity bounds + composition laws + a named failure envelope, and
  the recursion of the abstraction. Recorded verbatim in
  [`archive/P3-BREADTH.md`](archive/P3-BREADTH.md) (split out `2026-10-01` for the per-part
  ceiling — **resume the exchange there**). The permanent bounds: every axis choice stays
  citable; the synthetic design is NEVER evidence about any real DSP; it claims no
  compatibility.

## Blockers

- ~~`P2-SCALAR` gate `CPU-LAB`; `DSP-REVIEW` findings.~~ Resolved `2026-10-01`: `DSP-REVIEW`
  closed 8/8 and routed six findings here (`SEMULITH-DR-0094`); `P2-SCALAR` closed with its
  release decision recorded. The tree is unblocked.

## Acceptance Checklist (filled per leaf at execution time)

`P3-BREADTH.1` slices (the F2 probe, the F6 census leg), `.2`, `.4` slices 1–2, `.4` slice 3, `.4` slice 4, `.5` slices 1–3, `.7` slices 1–3, `.6` slice 1 (completed `2026-10-01`): their full acceptance checklists live verbatim in [`archive/P3-BREADTH.md`](archive/P3-BREADTH.md) — split out when this file crossed its 64 KiB per-part ceiling (the `docs/tasks/` precedent; the ceiling was obeyed, not raised).

`P3-BREADTH.6`, slice 2 (`2026-10-01`, `SEMULITH-BR-0020`):

- [x] **ROOT CAUSE (WHY + WHERE)** — the unit registration was deferred to `.6` because
  UNIT-BOOKS requires a book that builds, and the book's generator refused the DSP
  shape at three measured walls — measured pre-change: `python3
  scripts/gen_model_book.py --check --profile-dir profiles/dsp56300-lab-v0 --book-dir
  docs/models/dsp56300-lab-v0` → `gen_model_book: REFUSED — … expected exactly one
  encoding_source record, found 0`, rc=2 (with `encoding.sexp` required and
  `state["integer_registers"]` assumed beside it). WHERE:
  `scripts/gen_model_book.py` (the sibling-crate shape), `materials/units.sexp` (the
  row), `materials/category-needs.sexp` (24 census rows),
  `docs/models/dsp56300-lab-v0/` (the book), `doctrine/fact_ownership.tsv` (the mirror
  rows).
- [x] **ADDRESSED (verified)** — rv64i regression byte-exact: `git diff` over the four
  regenerated fragments shows ONLY the generator-digest header line; the DSP gates on
  first full run: `bash scripts/check_unit_books.sh` → `ok (2 unit(s) — every
  registered unit has its book, and every book builds)`; `bash
  scripts/check_materials_bill.sh` → `ok (2 unit(s) …)` (12 DSP materials, every
  section carries its does-not-supply); `bash scripts/check_scope_coverage.sh` → `ok
  (2 unit(s) may code)`; `mdbook build docs/models/dsp56300-lab-v0` → rc 0.
- [x] **NO REGRESSION** — `bash scripts/check_doctrines.sh` → `=== all doctrines green
  ===` end-to-end with the registration landed; both catalogues validate
  (`check_sexp_schema.py` on `units.sexp` + `category-needs.sexp` → ok).
- [x] **FIX** — the generator's three sibling-crate extensions (each naming the DSP
  case; the refusals stand without the declared vehicle), the registry row (C17 in /
  C14 out against rv64i's requires set, the reason in the file's comment), the 24
  census rows (8 covered / 6 partial / 3 missing-with-closings / 4 out-of-scope / 3
  deferred-to-board), the six-chapter book, the four mirror rows.
- [x] **LOCKSTEP** — tree (slice record, checklist, logs, frontier), the DOSSIER (the
  registration row flips to present), `MEMORY.md`, `LIVE_STATUS.md`, `CHANGELOG.md`,
  `DEV_NOTES.md`; mdBook `models.md` (two units) + `plan/p3.md` (the registration);
  the `.6` slice-1 checklist archived verbatim (the per-part ceiling held).

`P3-BREADTH.6`, slice 3 (`2026-10-01`, `SEMULITH-BR-0021`):

- [x] **ROOT CAUSE (WHY + WHERE)** — the gate's report must be a function of pinned
  inputs (ROADMAP §P1; EVD-08), and it cannot be a profile's: the gate spans every
  registered unit, measured when the pre-registration generation read "1 registered
  unit" and listed the evidenced DSP family as unclaimed — the report had to be the
  capstone. WHERE: `scripts/gate_report.py` (the cross-unit builder),
  `scripts/check_gate_report.sh` (the repo-level leg), `docs/BREADTH-REPORT.md` (the
  published report).
- [x] **ADDRESSED (verified)** — `python3 scripts/gate_report.py --gate BREADTH` →
  wrote `docs/BREADTH-REPORT.md` (**Verdict: `passed`**, 5,789 B): axis 1 six anchors
  present, axis 2 nine constructs declared+carried, axis 3 two surveyed families
  unclaimed explicitly; `bash scripts/check_gate_report.sh --self-test` → `12 pass /
  0 fail`; `bash scripts/check_gate_report.sh` → `ok (4 generated report(s) in sync
  with their inputs)`.
- [x] **NO REGRESSION** — G0/G1/GC reports regenerate byte-identical (the same check's
  4-report census); `bash scripts/check_doctrines.sh` → `=== all doctrines green ===`.
- [x] **FIX** — the cross-unit builder (three axes measured from tracked files by
  concrete artifact name; no code path to `passed` over an absent anchor), the
  repo-level leg (same enforcement, same controls), the published report.
- [x] **LOCKSTEP** — tree (status done, slice record, checklist, logs, frontier),
  `docs/TASK_TREE.md` (the tree leaves the active index), `MEMORY.md`,
  `LIVE_STATUS.md` (P3 row → Done), `CHANGELOG.md`, `DEV_NOTES.md`; mdBook
  `plan/p3.md` (the gate verdict + the report).

## Verification Log

| Date | Leaf | Checks | Result |
| --- | --- | --- | --- |
| `2026-10-01` | `.6` slice 3 | `gate_report.py --gate BREADTH` → verdict `passed` (axis 1: six anchors; axis 2: nine constructs declared+carried; axis 3: TI C6000 + ADI SHARC unclaimed explicitly); GATE-REPORT self-test 12/12, 4 reports in sync; `make gate` → all doctrines green | **gate `BREADTH` RUN, verdict `passed`** — the capability report published at `docs/BREADTH-REPORT.md`; `.6` DONE 3/3; the tree closes |
| `2026-10-01` | `.6` slice 2 | rv64i fragments regenerated — `git diff` shows ONLY the generator-digest line; UNIT-BOOKS ok (2 units, both build); MATERIALS-BILL ok (12 DSP materials, every section negative); SCOPE-COVERAGE ok (2 units may code); units/category-needs schema-validate ok; `mdbook build` rc 0; `make gate` → all doctrines green | the dsp56300-lab-v0 unit is REGISTERED and its book STANDS — generator learned the sibling-crate shape, 24 census rows landed, four mirror rows registered |
| `2026-10-01` | `.6` slice 1 | both catalogues schema-validate ok; RECORD-SCHEMA ok (10 record files, zero gate edits on landing); FACT-OWNERSHIP ok (25 kinds), self-test 10/10 after the GREEN fixture's two-unit re-pin (RED before: `UNREGISTERED MIRROR PAIR`); `make gate` → all doctrines green | the DSP's requirements + contract-obligations records LAND governed: 7 requirements, 13 obligations, 26 declared checks, contract `dsp56300-lab-env-v0` |
| `2026-10-01` | `.7` slice 3 | the landing: every attaching gate green with the documents in place — EXERCISE-COVERAGE 19/19 (DSP) + 52/52 (rv64), EXTRACTION ok (2 units), INTERACTION-MATRIX ok (2 units, 21 DSP cells), PROFILE-CONSISTENCY ok (2 dossiers), DOSSIER-SCHEMA 62 validated / 2 skipped-by-name, FACT-OWNERSHIP ok (23 kinds), self-test 10/10 (two new census arms); `make gate` green | **the dsp56300-lab-v0 dossier is LANDED and governed**; `.7` DONE 3/3 |
| `2026-10-01` | `.7` slices 1–2 (one commit — the slices interlock through the working-tree derived counts) | drafts placed: EXERCISE-COVERAGE ok 19/19, EXTRACTION ok, PROFILE-CONSISTENCY ok (2), INTERACTION-MATRIX ok (2 units; the DSP's 21 cells resolve); DOSSIER-SCHEMA 64 validated / 2 skipped-by-name, self-test 3/3, historical RED firing on the pre-fix D-FENCE document; FACT-OWNERSHIP self-test 8/8; coverage/extraction self-tests 13/13, 5/5; `make gate` green (30 doctrines, 323 arms re-derived) | the vehicle declaration + the checkpoint/sibling-crate legs; the DSP matrix drafted; DOSSIER-SCHEMA registered; the FACT-OWNERSHIP cross-product fix (same-unit pairing) |
| `2026-10-01` | `.5` slice 3 | refusal census `grep -n Refusal scripts/gen_definition.py` (3 named walls); operator census of `schema/semantics.sexp` (31 operators; load/store carry no space parameter; state access `reg`/`pc` only); dsp crate re-verified (`run_dsp56300_smoke.py` 6/6, 17/17 tests); drafts re-validate ok; `make gate` green | the encoding case measured: a lane, not an extension — DEFERRED with named reopening conditions; `.5` DONE 3/3; the dossier landing is leaf `.7` |
| `2026-10-01` | `.5` slice 2 | drafts schema-validate + round-trip data-equal; PROFILE-CONSISTENCY ok (2 dossiers) after the references.sexp repairs; attachment measured: EXERCISE-COVERAGE RED (NO COMPOSITION + 19 UNRESOLVED + no exercised set), EXTRACTION RED (no encoding.sexp), INTERACTION-MATRIX RED (NO MATRIX); exercise-coverage self-test 8/8; check_sexp_schema self-test 51/51; rv64 profile.sexp re-validates ok; `fetch_references.sh --verify-only dsp56300-lab-v0` ok; `make gate` green | the scope taxonomy generalized (5 DSP group fields, xlen/part-counts optional; no reader changed); the documents DRAFTED as schema-valid artifacts, landing deferred to the slice that keeps the attaching gates green; 9 latent defects surfaced by the measurement, all fixed |
| `2026-10-01` | `.5` slice 1 | synth suite re-pinned → 6 pass / 0 fail (probe 2 two legs: schema accepts, generator refuses `memory_spaces declared` rc 2); `check_state_gen.sh --self-test` → 10 pass / 0 fail (four new RED arms); rv64 `state.sexp` re-validates ok; `gen_state.py --check` byte-identical; round-trip data-equal; `dossier_sexp --self-test` 12/12; `make gate` green (DERIVED-COUNTS re-derived 308→312) | the state schema learned the census's shapes (register_family+parts, memory_spaces, hardware_stack; xlen/integer_registers optional); the refusal boundary moved one layer down, measured; the silent-drop mapping path closed |
| `2026-10-01` | `.1` F6 census leg | census record: 14 candidates answered with locators; `run_dsp56300_smoke.py` re-run → 6 agree / 0 fail (51–64 fields/case); `compare_dumps.py --self-test` → 4 pass / 0 fail; `cargo test -p semulith-dsp56300` 17/17; `make gate` green | the SEM-08 census re-run for dsp56300-lab-v0: the canonical end-state dump measured as the COMPLETE architectural state for subset v0; the harvested input for `.5`'s `state.sexp` cases |
| `2026-10-01` | `.4` slice 4 | `run_dsp56300_smoke.py` 6 agree / 0 fail (51–64 fields/case); `cargo test -p semulith-dsp56300` 17/17; `make check` + `make gate` green | subset v0 form-complete and differentially agreed; five measured model corrections (RTS PC-only, short-imm A2 sign extension, A1/B1 raw reads, S on bus reads only, the 24-bit keep-mask); two boundary defects fixed (accumulator-part destinations stop by name; NOP citation 13-149 → 13-145) |
| `2026-10-01` | `.4` slice 3 | `cargo test -p semulith-dsp56300` 10/10; `compare_dumps.py --self-test` 4/0; `run_dsp56300_smoke.py` 1 agree / 0 fail (53 fields, byte-identical dump, cyc excluded); `make check` + `make gate` green | the model crate STANDS; the first differential case AGREES |
| `2026-10-01` | `.4` slice 2 | both ledgers schema-validated; `fetch_references.sh --verify-only dsp56300-lab-v0` → tarball MATCH; `fetch_sources.sh --verify-only dsp56300-lab-v0` → FM manual MATCH (byte-identical to the chipdoc cache, HTTP 200); rv64 flow re-verified identical; `make gate` green with the second profile present | dossier + ledger landed; the auto-discovering gates' treatment of a second profile measured (keyed on profile.sexp/encoding.sexp — attach later with no gate edit) |
| `2026-10-01` | `.4` slice 1 | reference coverage censused on the pinned source (the `Instruction` enum spans the full DSP56300 set); LIMITATIONS.md read in full and mapped to exclusions; the difftest README's comparison surface re-read (dump vocabulary, deviation windows, stack slots, `cyc` informational) | subset `dsp56300-lab-v0` v0 selected with every exclusion reasoned; vehicle decided (sibling crate, EXPERIMENTAL); decision record + selection artifact landed |
| `2026-10-01` | `.3` slice 1 | three parallel per-family web surveys over one enumerator (QEMU/MAME/gem5/GDB-sim/binutils/LLVM/vendor tooling/dedicated projects); the two load-bearing positives re-derived by direct fetch (mborgerson LICENSE = MIT, README = the difftest claim; MAME sharc.cpp = BSD-3, ADSP21060/62, full `state_add` export) | oracle availability measured: TI ABSENT, DSP56300 STRONG, SHARC PARTIAL; slice decision DSP56300 recorded |
| `2026-10-01` | `.3` slice 2 | pinned fetch (commit `c60aeedb`, tarball sha256 recorded), on-volume release build of `dsp56300-asm` + `difftest`; micro guest: asm rc 0 (22 words), difftest rc 0 (16 steps, canonical dump + `--dump-mem`); independent Python arithmetic reproduces `A=001f253d515280` exactly; `#$5`→`x1=050000` traced to DSP56300FM §3.4.1.3 | the evidence path DEMONSTRATED end-to-end; `.3` done |
| `2026-10-01` | `.2` | DEF-GEN self-test (9 arms, incl. the new unfielded-operand RED arm) + byte-compare; `make check` 180/180 + fmt + clippy; synth suite 5/5; `gen_fragments.py` regeneration byte-identical | `.2` done — no opaque hooks (census); the one silent arm eliminated at generation + runtime |
| `2026-10-01` | `.1` slice 1 | synth suite 5/5; `make check` 180/180 + fmt + clippy; gen_state rc 0; DEF-GEN ok; G1 `passed` re-derived | `.1` executable-now scope done; leaf `slice-gated` on `.3`'s slice decision |

## Commit Log

| Leaf | Commit subject or reference | Notes |
| --- | --- | --- |
| `.6` slice 3 | `SEMULITH-BR-0021 (leaf P3-BREADTH.6): gate BREADTH runs — verdict passed; the capability report published, generated and gated` | the cross-unit builder measures the three roadmap axes from tracked files; the repo-level leg enforces sync; TI C6000 + ADI SHARC unclaimed explicitly; the tree closes |
| `.6` slice 2 | `SEMULITH-BR-0020 (leaf P3-BREADTH.6): the second unit registered — the sibling-crate book generator, the census rows, the book; every attaching gate green` | gen_model_book learned the sibling-crate shape (rv64i fragments byte-stable modulo the generator digest); units.sexp + 24 category-needs rows; the six-chapter book builds; four mirror rows |
| `.6` slice 1 | `SEMULITH-BR-0019 (leaf P3-BREADTH.6): the DSP records land governed — 7 requirements, 13 obligations, 26 declared checks; RECORD-SCHEMA attaches with zero gate edits` | the catalogues mirror the rv64i pattern at the DSP's size; FACT-OWNERSHIP gains two rows and its GREEN fixture re-pins to the two-unit corpus (the designed staleness fired RED first) |
| `.7` slice 3 | `SEMULITH-BR-0018 (leaf P3-BREADTH.7): the dossier lands governed — profile/state/interactions in profiles/, the ownership rows, the census arms; every attaching gate green` | the three documents moved (rename lineage kept); five fact-ownership rows; DOSSIER rows read present/deferred with owners; `.7` DONE 3/3 |
| `.7` slices 1–2 | `SEMULITH-BR-0017 (leaf P3-BREADTH.7): the vehicle declaration, the DSP matrix, and the DOSSIER-SCHEMA gate — gates derive applicability; the cross-product pairing fixed` | decision_gate-applicability-by-declared-vehicle (deferral machinery rejected); the checkpoint + sibling-crate legs measured green against the drafts (19/19); interactions.sexp drafted (21 cells resolve); the 30th doctrine registered; fact kinds qualified per unit |
| `.5` slice 3 | `SEMULITH-BR-0016 (leaf P3-BREADTH.5): the encoding case measured — a lane, not an extension; .5 closes, the dossier landing is leaf .7` | gen_definition.py's three refusal walls + the semantics language's scalar operator set censused; deferral with named reopening conditions; `.7` owns the landing, the gate dispositions, and the schema-validation leg |
| `.5` slice 2 | `SEMULITH-BR-0015 (leaf P3-BREADTH.5): the scope taxonomy generalizes — the DSP dossier drafted, its gate attachment measured, nine latent defects fixed` | schema/profile.sexp optional fields + 5 DSP scope groups; _SCOPE_LISTS extended; drafts under artifacts/dsp56300-dossier; PROFILE-CONSISTENCY green on the DSP dossier after the references.sexp repairs; landing waits for the attaching gates |
| `.5` slice 1 | `SEMULITH-BR-0014 (leaf P3-BREADTH.5): the state schema learns the census's shapes — families+parts, spaces, the stack; the refusal moved one layer down` | schema declares register_family/memory_spaces/hardware_stack (xlen optional); the mapping owner carries them (silent drop closed); gen_state refuses by name; probe 2 re-pinned (suite turned RED first, by design); STATE-GEN 10 arms |
| `.1` F6 census leg | `SEMULITH-BR-0013 (leaf P3-BREADTH.1): the dsp56300-lab-v0 state census — 14 candidates answered, the dump measured complete; the input .5 harvests` | SEM-08 re-run for the exercised profile; A2/B2 readout + M/sticky/loop/stale-slot candidates declared and measured; F5 window + architectural absences answered; the leaf stays slice-gated (F6 refires per profile; F2/F4/F5 stay TI/VLIW-conditional) |
| `.4` slice 4 | `SEMULITH-BR-0012 (leaf P3-BREADTH.4): subset v0 form-complete — ALU core, jsr/rts, rep/enddo, (Rn) modes; the 6-guest corpus AGREEs` | five measured corrections via the differential campaign (RTS, A2 sign extension, A1/B1 raw reads, S locus, keep-mask); accumulator-part destinations refused at decode; NOP citation corrected (13-145) |
| `.4` slice 3 | `SEMULITH-BR-0011 (leaf P3-BREADTH.4): the model crate stands — the first differential case AGREEs over 53 fields` | machine/decode/exec/dump/lod + runner; compare_dumps.py (cyc skipped by rule) + the smoke driver; the U-bit extraction inversion owned; machine.rs naming per the FACT-OWNERSHIP convention |
| `.4` slice 1 | `SEMULITH-BR-0009 (leaf P3-BREADTH.4): the bounded subset selected — dsp56300-lab-v0 v0, sibling-crate vehicle, exclusions named` | coverage + LIMITATIONS censused; subset named exactly; checkpoint-level comparator shape measured; decision_dsp56300-lab-v0-subset |
| `.4` slice 2 | `SEMULITH-BR-0010 (leaf P3-BREADTH.4): the dossier stands — sources + references ledgers, generic source-tarball leg, the second-profile gate census` | FM manual pinned at NXP's locator (byte-identical to the chipdoc cache); dsp56300 candidate dossier with EVD-04 rows; fetch_references.sh generic leg (rv64 flow identical); no gate edit needed for a second profile |
| — (design discussion) | `SEMULITH-BR-0001 (leaf P3-BREADTH.1): the composable-DSP design discussion recorded — resume here` | the skeleton + the measured axis menu + composition rules + ISA-as-fabric; the lego framing; the permanent bounds |
| `.1` slice 1 | `SEMULITH-BR-0005 (leaf P3-BREADTH.1): F2 measured executably — synth probe 5; the unconditional set is empty, the leaf slice-gates on .3` | grouping probe pinned (rc 1, `register_groups`); scalar regression re-run green; F2/F4/F5/F6 implementation legs await the slice decision |
| `.2` | `SEMULITH-BR-0006 (leaf P3-BREADTH.2): the hook census — no opaque hooks; the one silent extraction arm is now a generation-time refusal` | full-pipeline audit; `exec.rs` silent skip → generator refusal rc 2 + loud `ModelError`; 4 stale justification sites swept; dead `_unused_build` removed; DEF-GEN RED arm added |
| `.3` slice 1 | `SEMULITH-BR-0007 (leaf P3-BREADTH.3): the oracle survey — DSP56300 chosen, evidence path first` | TI ABSENT / DSP56300 STRONG / SHARC PARTIAL, positives re-derived from primary sources; the slice decision recorded |
| `.3` slice 2 | `SEMULITH-BR-0008 (leaf P3-BREADTH.3): the evidence path exercised — pin, build, micro guest, verified dump; .3 done` | reference pinned (`c60aeedb`) and built on-volume; guest assembled + run headless; dump verified three independent ways (hand arithmetic, memory spaces, the manual's §3.4.1.3) |

## Changelog

- `2026-09-13`: Created from `ROADMAP.md` §P3 by `SEMULITH-TREES.2`.
- `2026-10-01`: Design discussion recorded (the composable-DSP model; `SEMULITH-BR-0001`);
  blockers cleared — `DSP-REVIEW` closed 8/8 (`SEMULITH-DR-0094`).
- `2026-10-01`: `.1` slice 1 (`SEMULITH-BR-0005`) — F2 gained its executable demonstration
  (synth probe 5); the unconditional-change set measured empty; `.1` is `slice-gated` on
  `.3`'s slice decision; frontier moves to `.2`.
- `2026-10-01`: `.2` done (`SEMULITH-BR-0006`) — the full-pipeline hook census found no
  opaque hooks and one live silent extraction arm (a stale-justification defect, owned and
  fixed per §15): the generator now refuses an operand naming no field (rc 2, with a RED
  self-test arm), the runtime arm is a loud `ModelError`, the dead whitelist and four
  stale comment sites are swept; the lesson promoted to `docs/knowledge/`. Frontier: `.3`.
- `2026-10-01`: `.3` slice 1 (`SEMULITH-BR-0007`) — the oracle survey: TI C6000 has no
  pinnable executor (ABSENT), DSP56300 has a complete MIT-licensed silicon-validated path
  (STRONG), SHARC-2106x a partial one (BSD-3 MAME core; assembler leg unbuilt). Slice
  decision: **DSP56300**; slice 2 demonstrates the path end-to-end (pin, build, run a
  micro guest) before `.4` implements anything.
- `2026-10-01`: `.3` slice 2 (`SEMULITH-BR-0008`) — the path exercised: the reference
  pinned and built on-volume, a synthetic micro guest assembled (rc 0) and run headless,
  the canonical dump verified three independent ways (exact accumulator arithmetic,
  X/Y-space memory deviations, the §3.4.1.3 immediate rule). **`.3` done** — the working
  path is demonstrated, no experimental fallback needed. Frontier: `.4` (the bounded
  subset, selected against the reference's measured coverage and gaps).
- `2026-10-01`: `.4` slice 1 (`SEMULITH-BR-0009`) — the bounded subset selected:
  `dsp56300-lab-v0` v0 (non-parallel moves incl. A2/B2 readout, the ALU core, signed
  `mpy`/`mac`, `nop/jmp/jsr/rts`, `do`/`enddo`/`rep`, linear addressing), every exclusion
  named with its reason against the reference's measured coverage and LIMITATIONS; the
  vehicle decided (sibling crate `semulith-dsp56300`, EXPERIMENTAL); the comparator is
  checkpoint-level canonical end-state equality. `.4` is `in-progress`; slice 2 is the
  profile dossier + the reference-ledger integration.
- `2026-10-01`: `.4` slice 2 (`SEMULITH-BR-0010`) — the dossier stands:
  `profiles/dsp56300-lab-v0/` with the FM manual pinned at NXP's own locator (byte-identical
  to the chipdoc cache), the dsp56300 reference candidate with its EVD-04 independence rows,
  and DOSSIER.md carrying the deferrals by name; `fetch_references.sh` gained a generic
  source-tarball leg (the rv64 flow re-verified identical). The second-profile gate census:
  the auto-discovering gates key on `profile.sexp`/`encoding.sexp` and attach later with no
  gate edit. Frontier: slice 3, the model crate.
  Addendum (same slice): the commit's pre-commit gate fired `OVER CEILING profiles/: 123
  files > 120` — the family bound was calibrated to exactly one profile. Resolved per the
  registry's own rule (a reviewed decision, not compaction): the bound re-derived to 2×
  (240 files / 1,146,880 B; per-part 32 KiB unchanged) in
  `decision_profiles-family-two-units`, with the compaction alternatives rejected on the
  record.
- `2026-10-01`: `.4` slice 3 (`SEMULITH-BR-0011`) — the model crate stands: manual-derived
  decode/semantics for the nine demo-path forms, the canonical-dump runner, the
  checkpoint comparator (`cyc` skipped by recorded rule), the smoke driver; the micro
  guest adopted; **AGREE over 53 fields** — the dump is byte-identical to the reference's.
  Owned findings: the FM's U-bit equation is an extraction inversion (the reference's SR
  is the arbiter); `machine.rs` naming per the FACT-OWNERSHIP generated-mirror
  convention. Frontier: slice 4 — form-coverage completion + the guest corpus.
- `2026-10-01`: `.4` slice 4 (`SEMULITH-BR-0012`) — subset v0 is FORM-COMPLETE: the
  register/immediate data-ALU core, ASR/LSR, JSR/RTS, ENDDO, REP #xxx/REP S, and the
  seven linear (Rn) modes, every mask FM-cited and assembler-cross-checked; five guests
  join `micro` — **6 agree / 0 fail**. The campaign caught five model defects (each
  root-caused tools-first: RTS pulls PC only; short immediates sign-extend into A2; A1/B1
  read raw — the limiter is whole-accumulator-only; S sets on accumulator bus reads only;
  the 24-bit keep-mask nibble-slip) and two boundary defects (accumulator-part move
  destinations now refuse at decode; the NOP citation corrected to 13-145). `.4` DONE;
  `.1`'s F6 census leg reopens per the exercised profile; `.5` gains its measured
  extension list. Ceiling bookkeeping: the commit's doc updates pushed CHANGELOG.md and
  DEV_NOTES.md over their append-history ceilings — sharded by `scripts/shard_history.py`
  (completeness printed exact: 52 = 51 + 1 and 36 = 35 + 1, order and bytes; shards
  0093/0094 manifested) and LIVE_STATUS.md trimmed to fit (6,123/6,144). The two shard
  events then fired the shard FAMILY's aggregate axis (396,259 > 393,216 — the axis the
  row's three count re-derivations told the next reader to watch): re-derived to 2× by
  reviewed decision `decision_changelog-family-aggregate-rederivation`, compaction
  alternatives rejected on the record; per-part and the hash-pinned partition unmoved.
- `2026-10-01`: `.1` F6 census leg (`SEMULITH-BR-0013`) — the SEM-08 census re-run for the
  exercised dsp56300-lab-v0 profile: 14 candidates answered with locators (the A2/B2
  sign-extended readout and A1/B1 raw reads harvested from `.4`'s pins; M0–M7 bounded at
  reset by typed stops; sticky L/S declared — S has no writer in subset v0; the DO stack and
  the stale popped slots inside the observation surface; REP's LC borrow transient; the F5
  pending-writes window ABSENT for scalar issue). Consequence measured: **the canonical
  end-state dump is the complete architectural state** for subset v0 — snapshot/replay
  reduces to the dump fields, the same honesty the scalar census bought on rv64i-lab-v0.
  The record is `.5`'s measured input for the `state.sexp` cases. `.1` stays `slice-gated`
  (F6 refires per profile; F2/F4/F5 stay TI/VLIW-conditional). Frontier: `.5`.
  Ceiling bookkeeping: this leg's CHANGELOG append fired the head's 64 KiB per-part bound —
  sharded by `scripts/shard_history.py` (completeness printed exact: 52 = 51 + 1, order and
  bytes; shard 0095 manifested), the designed pressure control, no bound moved.
- `2026-10-01`: `.5` slice 1 (`SEMULITH-BR-0014`) — the state schema learned the census's
  shapes: `register_family` (+ `parts` with per-part `readout`), `memory_spaces`,
  `hardware_stack`, with `xlen`/`integer_registers` optional — each construct names
  dsp56300-lab-v0 and its case (F1, F3, census candidates 1/4/6). The mapping owner
  (`dossier_sexp`) carries the new forms — the silent-drop path between schema and
  generator is closed — and `gen_state.py` refuses each by name (rc 2); a missing `xlen`
  is now a Refusal, not a KeyError. Synth probe 2 turned RED on the stale pin (the
  fixture's designed behaviour) and re-pinned one layer down: schema accepts, generator
  refuses. STATE-GEN self-test 10 arms; DERIVED-COUNTS re-derived 308→312. The DSP's
  `state.sexp` stays unlanded — without `profile.sexp` no gate would read it (measured);
  it lands with the scope-taxonomy slice. `.5` is `in_progress`.
  Ceiling bookkeeping: this slice's DEV_NOTES append fired that head's 48 KiB per-part
  bound — sharded by `scripts/shard_history.py` (completeness printed exact: 37 = 36 + 1,
  order and bytes; shard 0096 manifested); MEMORY.md trimmed to its cap (7,156/7,168);
  SEAM-INTEGRITY's acceptance-box regression caught one under-evidenced checklist box on
  the first pass — fixed with the probe's concrete command line, the gate doing its job.
- `2026-10-01`: `.5` slice 2 (`SEMULITH-BR-0015`) — the scope taxonomy generalized for the
  exercised DSP profile: `schema/profile.sexp` gained the five DSP group fields and made
  `xlen` / the integer-file scalars / `count_rv64i_additions` optional (each naming its
  case; no gate reader changed — they were already generic over group names);
  `_SCOPE_LISTS` extended in the same commit. The DSP's `profile.sexp`/`state.sexp` stand
  DRAFTED and schema-validated under `artifacts/p3-breadth/dsp56300-dossier/` (the census
  carried as data). The landing was measured, not guessed: PROFILE-CONSISTENCY passes the
  DSP dossier (after the measurement surfaced and this slice fixed seven latent
  references.sexp defects — an `obtained` candidate without binary/digest/injection, and
  four independence pairs naming non-candidates, repaired by registering the asm/emu legs
  and gearmulator as first-class candidates); EXERCISE-COVERAGE / EXTRACTION /
  INTERACTION-MATRIX go RED on a unit without encoding.sexp / interactions.sexp /
  per-step expectation guests — the landing slice owns them, plus the surfaced gap: no
  gate schema-validates the dossier documents as a class (the D-FENCE double-note drift,
  found and fixed here, lived unseen for that reason). Also fixed: EXERCISE-COVERAGE's
  denominator counted a `(comment …)` inside scope as mnemonics (now skipped, GREEN arm);
  `check_sexp_schema.py` tracebacks on a missing input (now rc 2, RED arm). Ceiling
  bookkeeping: the appends fired both heads' per-part bounds — shards 0097/0098 cut by the
  sharder (completeness exact: 53 = 52 + 1 and 37 = 36 + 1, order and bytes); this tree
  file crossed its 64 KiB per-part bound and was SPLIT per the `docs/tasks/` precedent
  (`.2`/`.4` checklists verbatim to `archive/P3-BREADTH.md`); MEMORY.md trimmed to cap;
  DERIVED-COUNTS re-derived 312 → 313 (one new shell arm; the python-side arm is outside
  the shell idiom's census); the D-FENCE change re-derived the GC report and the model
  book's internal-contracts fragment (both regenerated, never edited — the
  in-sync-at-HEAD check ran in a clean worktree first). The count ceiling then fired on
  the split itself (61 > 60): re-derived to 96 by reviewed decision
  `decision_task-tree-family-count-rederivation` (the partition lifecycle and the evidence
  archives are the designed file growth; per-part 64 KiB unmoved).
- `2026-10-01`: `.5` slice 3 (`SEMULITH-BR-0016`) — the encoding case MEASURED, not
  asserted: `gen_definition.py` refuses a second unit at three named walls (profile scope,
  the 32-bit decode table, the semantics corpus), and the semantics language is
  scalar-shaped (31 operators; load/store carry no space parameter; state access is
  `reg`/`pc` only) — the DSP's X/Y/P moves and do/rep machinery would refuse by name. The
  generalization is a lane no current milestone consumes; the sibling crate is the
  exercised, agreed vehicle. Decision: DEFERRED with named reopening conditions (a corpus
  extension, a third unit, or the landing leaf choosing the machinery route). **`.5` DONE
  3/3**; the dossier landing is new leaf `.7` (the measured attachment table is its
  input; it owns the gate-disposition choice and the dossier schema-validation leg).
  Bookkeeping: `.5` slices 1–2's checklists archived verbatim to `archive/P3-BREADTH.md`
  as the leaf closed, joined by the slice-gated `.1`'s two completed-slice checklists
  (the per-part ceiling held); the CHANGELOG append fired the head's bound again —
  shard 0099 (53 = 52 + 1, order and bytes exact).
- `2026-10-01`: `.7` slice 1 (`SEMULITH-BR-0017`) — the disposition DECIDED
  (director-delegated): `decision_gate-applicability-by-declared-vehicle` — gates derive
  per-unit applicability from the declared vehicle + the unit's documents; deferral
  machinery rejected (a weakening surface with no second user), fiction machinery
  rejected (evidence the claim never cites). Landed: the `vehicle` construct (schema +
  mapping owner), EXTRACTION's sibling-crate leg (contradiction = finding),
  EXERCISE-COVERAGE's checkpoint leg (the `.a56` guest census, both directions).
  Measured against the real drafts: **19/19 declared forms exercised**, EXTRACTION and
  PROFILE-CONSISTENCY green on the DSP dossier. rv64 byte-untouched in behavior (52/52).
  Bookkeeping: `.5` slice 3's checklist archived to keep the per-part ceiling.
  Slices 1–2 landed in ONE commit: the derived counts measure the working tree, so the
  co-developed halves could not pass the hook separately. Slice 2: the DSP
  `interactions.sexp` drafted (6 axes, 21 cells, mechanism/degenerate dispositions — the
  matrix gate needed NO change; the closed mechanism registry gained
  `dsp56300-smoke-agreement` and `dsp56300-typed-stop`); **DOSSIER-SCHEMA registered**
  (the 30th doctrine — dossier documents now schema-validate as a class; fired RED on the
  pre-fix D-FENCE document from git history before registration); FACT-OWNERSHIP's
  cross-product census fixed (same-unit pairing; the second unit had invented cross-unit
  pairs) and the registry's kinds qualified per unit. The `.4` slice narratives archived
  verbatim (the per-part ceiling held again).
- `2026-10-01`: `.7` slice 3 (`SEMULITH-BR-0018`) — **the dossier LANDS, governed**: the
  three schema-validated documents moved to `profiles/dsp56300-lab-v0/` (rename lineage
  kept; headers rewritten to the landed gate map), the DSP's five fact-ownership rows
  landed (`state (dsp56300-lab-v0)`'s profile mirror governed by PROFILE-CONSISTENCY),
  and the two post-landing census arms prove the second-unit pairing. Every attaching
  gate green with the documents in place (coverage 19/19, extraction, matrix — 21 cells,
  consistency, dossier-schema 62/2, ownership 23 kinds). `.7` DONE 3/3; the DOSSIER rows
  read present/deferred with owners (requirements + unit registration → `.6`). Frontier:
  `.6`, the BREADTH gate report. Bookkeeping: `.7` slice 1's checklist archived verbatim
  (the per-part held).
- `2026-10-01`: `.6` slice 1 (`SEMULITH-BR-0019`) — the DSP's records LAND governed:
  seven `REQ-D-*` requirements (statements byte-identical to the profile's decisions,
  every source citing `DSP56300FM`) and thirteen obligations (seven mirrors + six
  `OB-ENV-*` environment-assumptions: virtual-time, ordering, reset, fetch-supply,
  event-delivery, partial-progress), contract `dsp56300-lab-env-v0`, 26 declared checks.
  RECORD-SCHEMA attached on landing with zero gate edits (10 record files green first
  pass); FACT-OWNERSHIP gained the DSP's requirements/obligations rows, and its GREEN
  self-test fixture turned RED on the landing by design (the pair glob follows the real
  corpus) — re-pinned to the two-unit corpus (`__CHECKED__ 5 → 6`). Bookkeeping: the
  `.7` slice-3 checklist and the Design Discussions archived verbatim (the per-part
  ceiling held; the exchange's resume pointer stays in the tree). Frontier: slice 2 —
  the BREADTH report itself.
- `2026-10-01`: `.6` slice 2 (`SEMULITH-BR-0020`) — the unit REGISTERED, its book
  STANDING. `gen_model_book.py` learned the sibling-crate shape (three extensions, each
  naming the DSP case; the refusals stand without the declared vehicle; rv64i fragments
  byte-stable modulo the generator digest). `units.sexp` gained the DSP row (C17 in /
  C14 out against rv64i's requires set — reset is this unit's own decision, interrupts
  a named exclusion) and the 24-row category-needs census landed (8 covered / 6 partial
  / 3 missing-with-closings / 4 out-of-scope / 3 deferred-to-board). The six-chapter
  book builds; UNIT-BOOKS, MATERIALS-BILL, SCOPE-COVERAGE all green with 2 units; four
  fragment mirror rows registered. Frontier: slice 3 — the BREADTH report (the
  capability report is the capstone: the registry is now complete enough to read).
  Ceiling bookkeeping (same slice): the director ruled `2026-10-01` "allow increasing the
  size of task-trees" — the docs/tasks/ per-part bound rose to 128 KiB by reviewed
  decision `decision_task-tree-per-part-growth` (six forced archives in one day, two of
  them taxing ACTIVE narratives; the aggregate bound and the archive lifecycle are
  unchanged, and the director's stated invariant stands: a bound remains — a file must
  stay readable in one sitting, growth is never unbounded).
- `2026-10-01`: `.6` slice 3 (`SEMULITH-BR-0021`) — **gate `BREADTH` RUN, verdict
  `passed`.** The cross-unit builder measures the three roadmap axes from tracked
  files by concrete artifact name (axis 1: the subset's six evidence anchors; axis 2:
  nine abstraction constructs declared AND carried, the refusal boundary pinned; axis
  3: the registry as the complete claim list — TI C6000 and ADI SHARC unclaimed
  explicitly, everything else by omission), with no code path to `passed` over an
  absent anchor. The report publishes at `docs/BREADTH-REPORT.md`;
  `check_gate_report.sh` gained the repo-level leg (12/12 self-test; 4 reports in
  sync). `.6` DONE 3/3. **The tree closes** — `.1` stays `slice-gated` on the record,
  its conditional legs (F2/F4/F5) reopening by name with a VLIW/TI slice decision;
  the stable-API claim is permitted exactly where the report permits it: the
  exercised cases of the two registered units.
