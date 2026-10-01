# P3-BREADTH: stabilize only what has been demonstrated

## Metadata

- Tree ID: `P3-BREADTH`
- Status: `active`
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
  Status: `slice-gated` (executable-now scope done `2026-10-01`; the implementation legs await `.3`'s slice decision)
  Goal: implement the abstraction changes `DSP-REVIEW.7` classified as required.
  Acceptance: every change traces to a numbered finding; scalar regression evidence for `rv64i-lab-v0` is preserved and re-run (`EVD-07`).
  Applied `2026-10-01`: the required-**unconditional** set measured **empty** — F2/F4/F5 are TI/VLIW-conditional, F6 fires per new profile (Decisions, `2026-10-01`). F2 gained its executable demonstration (synth probe 5: `undeclared field "register_groups"`, rc 1 — the report's named honest route); scalar regression re-run green (`make check` 180/180, gen_state rc 0, DEF-GEN ok, G1 `passed` re-derived).
  Lessons: `promotion: declined (per-slice application of the report's own named remedy; the durable method — a finding without an executable demonstration gets a synth probe — lives in the findings report and the synth README where the next reader meets it)`.

- ID: `P3-BREADTH.2` — **opaque semantic hooks made explicit**
  Status: `done` (`2026-10-01`, `SEMULITH-BR-0006`)
  Goal: where a target needs behaviour the generic layer cannot express, the hook states its contract, its state, and which backends support it.
  Acceptance: no hook is a silent escape hatch; an unsupported construct is a **model-generation failure**, not a guessed translation (`docs/ARCHITECTURE.md` §2).
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

- ID: `P3-BREADTH.3` — **real DSP slice: evidence path first**
  Status: `done` (`2026-10-01` — slice 1 the survey, slice 2 the demonstration)
  Goal: demonstrate the evidence path for a candidate real DSP subset **before** implementing it.
  Acceptance: either a working path is demonstrated, or the work proceeds as a deliberately limited **experimental** claim that says so. `SRC-02`: a missing reference route prevents the associated evidence claim, not honest experimental work.
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

- ID: `P3-BREADTH.4` — **the bounded real subset**
  Status: `in-progress` (slices 1–3 done `2026-10-01`; slice 4 is form-coverage completion)
  Goal: implement and evidence the narrow slice selected in `.3`.
  Acceptance: its claim names the exact subset; a source-reviewed experimental subset cannot inherit a differentially validated claim from another target (`docs/EVIDENCE_AND_GATES.md` §1).
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

- ID: `P3-BREADTH.5` — **schema and generator functionality where justified**
  Status: `pending`
  Goal: extend the definition schema/generator only where an exercised target demonstrates the need.
  Acceptance: each extension names the target and case that required it.

- ID: `P3-BREADTH.6` — **the `BREADTH` gate report**
  Status: `pending`
  Goal: generate from pinned inputs; publish the capability report.
  Acceptance: families with no evidence are listed as **unclaimed**, explicitly.

## Current Frontier

| Order | Leaf | Status | Why next |
| --- | --- | --- | --- |
| 1 | `P3-BREADTH.4` | `in-progress` | slices 1–3 done (subset selected; dossier; the model crate STANDS — first differential case AGREEs over 53 fields); slice 4 is form-coverage completion (ALU core, jsr/rts, rep, (Rn) modes) + the guest corpus |
| — | `P3-BREADTH.1` | `slice-gated` | the executable-now scope landed `2026-10-01`; the DSP56300 slice (`.3`) resolves part of the gating — F6's census reopens per the new profile in `.4`; F4/F5 (VLIW) and F2 (TI grouping) stay unbuilt, recorded |

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

- `2026-10-01` (director, `[DBINP]` — recorded to resume the exchange later; no pivot, no
  leaf scope changed): **a DSP as composition, not monolith.** The exchange that closed
  `DSP-REVIEW` produced a working model of what a DSP *is*: a fixed skeleton of problems —
  the MAC as the atom; accumulation headroom; the dual operand feed; specialized addressing
  (circular, bit-reversed); zero-overhead looping; saturating arithmetic with sticky flags;
  determinism as the organizing contract — plus a **measured per-axis menu of choices**
  (accumulator: none / 56-bit+8-ext / 80-bit guard; address unit: byte / 24-bit word /
  per-space width; spaces: 1 / 2 / 3; issue: VLIW packet / scalar interlocked / scalar+REP;
  saturation locus: per-instruction / mode bits / explicit transfer; circular alignment:
  to-size / 2^k / arbitrary; sticky flags: CSR.SAT+SSR / STKY; loop machinery; interrupt
  interaction), each axis choice citable to the vendor that actually made it
  (`docs/tasks/artifacts/dsp-review/2026-10-01-interface-findings.md`).
  The director's framing: building a DSP is **composing lego into a coherent, functional
  whole** — choose one option per axis, then find the **composition rules** that make the
  choices fit together (accumulator width ⇒ readout semantics; addressing mode ⇒ alignment
  rule; loop model ⇒ interrupt rules; issue model ⇒ the state census), then design the ISA
  as the fabric that moves data between the chosen parts. **Resume here:** the hypothetical
  high-end DSP — a coherent menu selection + its composition rules + its ISA + its manual —
  as this tree's ultimate stress fixture, the positive counterpart to `synth24`'s refusals
  (where `synth24` measured what the pipeline *refuses*, the composed DSP would exercise
  what it must come to *express*). Bounds carried from the review, permanent: every choice
  stays citable per-axis; the synthetic design is NEVER evidence about any real DSP; it
  claims no compatibility.
  **The director's refinement (same exchange): the key idea is abstraction.** The menu of
  axes is an abstraction OF the measured manuals; the composed DSP is the dual operation —
  instantiating a coherent point from the abstraction. If the abstraction can generate a
  coherent point in the design space, it can probably host a real one; that is the
  strongest test an abstraction gets — not "does it cover case X" but "does it compose".
  The carried warning (same exchange): an abstraction's value is what it makes ILLEGAL —
  a universal step relation "expresses" everything and constrains nothing. So the
  exercise's real output is the boundary map (which axis choices the abstraction refuses,
  and whether each refusal is named work or an accident), and the composition rules —
  the coupling graph between axes — are the actual research content, because an
  abstraction that treats coupled axes as independent generates incoherent processors.
  **The director's grounding (same exchange): abstraction means to SIMPLIFY the view of a
  problem** — as R, C and L are simplifications of real physical phenomena that, composed
  by rules, yield working circuits; as RTL is a simplification of the real design problem.
  Same idea, another level, another domain: the axis menu simplifies five vendors' manuals
  into composable components; the composition rules are the Kirchhoff laws of the domain.
  The analogy carries its own engineering requirements: the lumped R/C/L model works
  because it ships with (a) stated VALIDITY BOUNDS (dimensions ≪ wavelength), (b)
  COMPOSITION LAWS (KVL/KCL), and (c) a KNOWN FAILURE ENVELOPE (parasitics, distributed
  effects — the model tells you where it breaks). This tree's equivalents: (a) the claim
  discipline (unsupported families stay unclaimed), (b) the composition rules — the work,
  (c) the named-refusal map (`synth24`'s pins) and the honest limits. An abstraction is
  judged by what it can afford to forget; R/C/L forget Maxwell's equations, the axis menu
  forgets implementation detail, and both keep exactly what composition needs.
  **The director's closing remark (same exchange): the abstraction is RECURSIVE** — each
  axis can itself be abstracted further, simplified further, if need be. The menu is not
  a fixed depth: "accumulator" can refine into width × readout × extension semantics,
  "issue model" into packet formation × writeback visibility × interrupt interaction,
  each sub-axis still citable to the manuals that carry it. The R/C/L grounding holds at
  every level — each refinement keeps its own validity bounds, composition laws, and
  failure envelope. Depth is chosen by need (an exercised target demands it), never by
  completeness for its own sake.

## Blockers

- ~~`P2-SCALAR` gate `CPU-LAB`; `DSP-REVIEW` findings.~~ Resolved `2026-10-01`: `DSP-REVIEW`
  closed 8/8 and routed six findings here (`SEMULITH-DR-0094`); `P2-SCALAR` closed with its
  release decision recorded. The tree is unblocked.

## Acceptance Checklist (filled per leaf at execution time)

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

## Verification Log

| Date | Leaf | Checks | Result |
| --- | --- | --- | --- |
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
