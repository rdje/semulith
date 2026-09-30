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
  Status: `in-progress` (slice 1 done `2026-10-01`: the oracle survey + the slice decision)
  Goal: demonstrate the evidence path for a candidate real DSP subset **before** implementing it.
  Acceptance: either a working path is demonstrated, or the work proceeds as a deliberately limited **experimental** claim that says so. `SRC-02`: a missing reference route prevents the associated evidence claim, not honest experimental work.
  Slice 1 (`2026-10-01`, `SEMULITH-BR-0007`): the oracle-availability survey
  ([`artifacts/p3-breadth/2026-10-01-oracle-survey.md`](artifacts/p3-breadth/2026-10-01-oracle-survey.md))
  — TI C6000 ABSENT for execution (no OSS executor anywhere; the vendor simulator was
  discontinued in 2014), DSP56300 STRONG (MIT assembler + MIT silicon-validated emulator
  with a ready differential harness), SHARC ADSP-2106x PARTIAL (BSD-3 MAME core, but the
  assembler leg is unbuilt and no second oracle exists). Both load-bearing positives
  re-derived against primary sources. **Slice decision: DSP56300** (Decisions, `2026-10-01`).
  Slice 2 (next): demonstrate the path end-to-end WITHOUT a Semulith DSP model — pin and
  build the reference on-volume, assemble a micro guest, execute it headless, dump the
  canonical state. Only then does `.4` implement the bounded subset.
  Lessons: `promotion: declined (the survey is dated evidence living where the next evaluator meets it; its durable output is the slice decision, recorded in this tree's Decisions)`.

- ID: `P3-BREADTH.4` — **the bounded real subset**
  Status: `pending`
  Goal: implement and evidence the narrow slice selected in `.3`.
  Acceptance: its claim names the exact subset; a source-reviewed experimental subset cannot inherit a differentially validated claim from another target (`docs/EVIDENCE_AND_GATES.md` §1).

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
| 1 | `P3-BREADTH.3` | `pending` | the slice decision is now the pivotal leaf: it unblocks `.1`'s gated legs (VLIW ⇒ F4+F5; TI ⇒ F2), `.4`, and F6's per-profile census work — and it starts from the evidence path, per its acceptance |
| — | `P3-BREADTH.1` | `slice-gated` | the executable-now scope landed `2026-10-01`; F2's implementation and F4/F5 resume when `.3` names the slice (VLIW ⇒ F4+F5; TI ⇒ F2); F6 resumes per new profile |

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

## Open Questions

- ~~Whether any real DSP oracle becomes available at all.~~ ANSWERED `2026-10-01` (`.3`
  slice 1): yes — DSP56300 has a complete license-clean path (STRONG), SHARC-2106x a partial
  one; only TI C6000 has none. What remains open until `.3` slice 2 demonstrates it: whether
  the DSP56300 path reproduces HERE (pinned, on-volume, headless) as measured, not surveyed.
  If the demonstration fails, `.4` ships an explicitly experimental claim and the `BREADTH`
  gate states that limit rather than hiding it.

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

## Verification Log

| Date | Leaf | Checks | Result |
| --- | --- | --- | --- |
| `2026-10-01` | `.3` slice 1 | three parallel per-family web surveys over one enumerator (QEMU/MAME/gem5/GDB-sim/binutils/LLVM/vendor tooling/dedicated projects); the two load-bearing positives re-derived by direct fetch (mborgerson LICENSE = MIT, README = the difftest claim; MAME sharc.cpp = BSD-3, ADSP21060/62, full `state_add` export) | oracle availability measured: TI ABSENT, DSP56300 STRONG, SHARC PARTIAL; slice decision DSP56300 recorded |
| `2026-10-01` | `.2` | DEF-GEN self-test (9 arms, incl. the new unfielded-operand RED arm) + byte-compare; `make check` 180/180 + fmt + clippy; synth suite 5/5; `gen_fragments.py` regeneration byte-identical | `.2` done — no opaque hooks (census); the one silent arm eliminated at generation + runtime |
| `2026-10-01` | `.1` slice 1 | synth suite 5/5; `make check` 180/180 + fmt + clippy; gen_state rc 0; DEF-GEN ok; G1 `passed` re-derived | `.1` executable-now scope done; leaf `slice-gated` on `.3`'s slice decision |

## Commit Log

| Leaf | Commit subject or reference | Notes |
| --- | --- | --- |
| — (design discussion) | `SEMULITH-BR-0001 (leaf P3-BREADTH.1): the composable-DSP design discussion recorded — resume here` | the skeleton + the measured axis menu + composition rules + ISA-as-fabric; the lego framing; the permanent bounds |
| `.1` slice 1 | `SEMULITH-BR-0005 (leaf P3-BREADTH.1): F2 measured executably — synth probe 5; the unconditional set is empty, the leaf slice-gates on .3` | grouping probe pinned (rc 1, `register_groups`); scalar regression re-run green; F2/F4/F5/F6 implementation legs await the slice decision |
| `.2` | `SEMULITH-BR-0006 (leaf P3-BREADTH.2): the hook census — no opaque hooks; the one silent extraction arm is now a generation-time refusal` | full-pipeline audit; `exec.rs` silent skip → generator refusal rc 2 + loud `ModelError`; 4 stale justification sites swept; dead `_unused_build` removed; DEF-GEN RED arm added |
| `.3` slice 1 | `SEMULITH-BR-0007 (leaf P3-BREADTH.3): the oracle survey — DSP56300 chosen, evidence path first` | TI ABSENT / DSP56300 STRONG / SHARC PARTIAL, positives re-derived from primary sources; the slice decision recorded |

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
