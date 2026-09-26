# Every cross-cutting lane names the milestone that consumes it

- **Type:** `decision`
- **Date:** `2026-09-27`
- **Status:** `active`
- **Owner / source:** agent decision under director delegation `2026-09-27` — *"the decision
  is yours to make but it got to be sota, signoff and production-grade"* — adopted with
  `ROADMAP-V3` and folded into `ROADMAP.md` v0.3
- **Mechanical arm:** a census gate over tree Metadata is **proposed, not yet registered**;
  the director asked to be told of new governance before it is tasked, so until approved the
  census runs by hand at each roadmap revision

## The fact / decision

Every cross-cutting (non-milestone) task tree declares, in its Metadata, **the milestone its
work is consumed by and the point by which it must be consumed**. A lane without a named
consumer at a roadmap revision is **descoped or closed** at that revision. Proposing a new
cross-cutting lane requires naming its consumer at proposal time.

## Why

The measured failure this closes: P0 finished, then ~24 consecutive work units landed in
infrastructure lanes while every milestone tree (`P1-LAB` … `P7-COMPUTER`) sat at `proposed`
with its first leaf untouched. The milestone dependency graph is silent on cross-cutting
lanes, so *"finish the infrastructure first"* became the default sequencing — an assumption
never examined because nothing in the plan made it examinable. The roadmap already carried
the warning sentence — *"Evidence tooling supports both; it does not become an unrelated
research product"* — but a warning without an operational rule is a hope, not a control.

The rule is the standard portfolio test for enabling work, stated for this project's
vocabulary: an investment that cannot name what it unblocks, and roughly by when, is
indistinguishable from an end in itself. Stated with the same honesty in the other
direction: a lane whose consumer arrives *earlier* than declared is fine — the rule binds the
**absence** of a consumer, not the calendar, and a consumption point is a planning anchor
that revisions may move, not a cliff.

## How to apply

- Tree Metadata gains a `Consumed by:` line — milestone (or standing-hygiene class) plus the
  latest consumption point — at tree creation; the lane-consumption census (manual until the
  mechanical gate is approved) lists every active lane's consumer at each roadmap revision.
- **First application, `2026-09-27`:**
  | Lane | Consumed by | Latest point |
  | --- | --- | --- |
  | `SOT-FORMAT` | the generator engine's read path; P3+ record merge | v0.4 revision |
  | `MODEL-METHOD` | `P1-LAB` — its extraction contract is a P1 entry input | P1 start |
  | `MODEL-COMPOSE` | P3 / board assumption-guarantee discharge | P3 start |
  | `MODEL-BOOKS` | P1's first book increment (dual mandate) | P1 first slice |
  | `UPSTREAM-TRACK` | standing hygiene — the reported-defect index | bounded by its tree |
  | `PUSH-DISCIPLINE` | standing hygiene — the push boundary | bounded by its tree |
  | `ARTIFACT-CLEANUP` | §8 recurring housekeeping | time-triggered |
- **Governance clause:** at each roadmap revision, any active lane with no `Consumed by`
  declaration, or whose declared consumer no longer exists, is descoped or closed in that
  revision's text — recorded, not silently dropped.

Related: [[decision_interpreter-before-compiler]], [[decision_one-definition-one-book]],
[[decision_task-tree-family-bound]].
