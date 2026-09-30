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
  Status: `pending`
  Goal: where a target needs behaviour the generic layer cannot express, the hook states its contract, its state, and which backends support it.
  Acceptance: no hook is a silent escape hatch; an unsupported construct is a **model-generation failure**, not a guessed translation (`docs/ARCHITECTURE.md` §2).

- ID: `P3-BREADTH.3` — **real DSP slice: evidence path first**
  Status: `pending`
  Goal: demonstrate the evidence path for a candidate real DSP subset **before** implementing it.
  Acceptance: either a working path is demonstrated, or the work proceeds as a deliberately limited **experimental** claim that says so. `SRC-02`: a missing reference route prevents the associated evidence claim, not honest experimental work.

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
| 1 | `P3-BREADTH.2` | `pending` | the hook audit is executable now: no target is needed to verify that an unsupported construct is a named generation failure, never a guessed translation; the synth suite already pins five such refusals |
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

## Open Questions

- Whether any real DSP oracle becomes available at all. If none does, `.4` ships an explicitly
  experimental claim and the `BREADTH` gate states that limit rather than hiding it.

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

## Verification Log

| Date | Leaf | Checks | Result |
| --- | --- | --- | --- |
| `2026-10-01` | `.1` slice 1 | synth suite 5/5; `make check` 180/180 + fmt + clippy; gen_state rc 0; DEF-GEN ok; G1 `passed` re-derived | `.1` executable-now scope done; leaf `slice-gated` on `.3`'s slice decision |

## Commit Log

| Leaf | Commit subject or reference | Notes |
| --- | --- | --- |
| — (design discussion) | `SEMULITH-BR-0001 (leaf P3-BREADTH.1): the composable-DSP design discussion recorded — resume here` | the skeleton + the measured axis menu + composition rules + ISA-as-fabric; the lego framing; the permanent bounds |
| `.1` slice 1 | `SEMULITH-BR-0005 (leaf P3-BREADTH.1): F2 measured executably — synth probe 5; the unconditional set is empty, the leaf slice-gates on .3` | grouping probe pinned (rc 1, `register_groups`); scalar regression re-run green; F2/F4/F5/F6 implementation legs await the slice decision |

## Changelog

- `2026-09-13`: Created from `ROADMAP.md` §P3 by `SEMULITH-TREES.2`.
- `2026-10-01`: Design discussion recorded (the composable-DSP model; `SEMULITH-BR-0001`);
  blockers cleared — `DSP-REVIEW` closed 8/8 (`SEMULITH-DR-0094`).
- `2026-10-01`: `.1` slice 1 (`SEMULITH-BR-0005`) — F2 gained its executable demonstration
  (synth probe 5); the unconditional-change set measured empty; `.1` is `slice-gated` on
  `.3`'s slice decision; frontier moves to `.2`.
