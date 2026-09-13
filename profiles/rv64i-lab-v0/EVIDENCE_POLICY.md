# Evidence policy for `rv64i-lab-v0` — what each obligation class must be shown by

- **Declared:** `2026-09-14`, by `P0-PROFILE.9`, **before** any model implementation exists.
- **Rule:** `EVD-03` — the kind of evidence an obligation requires is declared in advance,
  because an implementation that chooses its own evidence afterwards chooses whatever it can most
  easily produce. `crates/` still holds the scaffold's placeholder `main.rs`; nothing here has
  been shaped by what a model can currently do, because there is no model.

## The classes, and what closes each

An obligation's class comes from its requirement's `source_semantics.category`, which is already
recorded per record and gated by `RECORD-SCHEMA`. There are five classes in this profile.

⛔ **No class population is counted here.** The first draft of this file stated them and got two
wrong, by reading the profile's *authority* distribution (14 `architecture` / 8
`execution-environment`) instead of the requirements' *category* distribution (13 `defined` / 10
`implementation-defined`) — which is precisely the non-mechanical mapping this profile documents,
walked into by the person documenting it. Counts belong in the **generated** report
([`G0-REPORT.md`](G0-REPORT.md)), which derives them; this file states the rules.

### `defined` — the specification states it

**Required:** directed fixtures whose expected values are derived from the pinned specification
text, **plus** differential agreement with at least one reference model on those fixtures.

⛔ **Model agreement is not sufficient on its own, and never becomes sufficient by adding models.**
Where two comparators share the relevant semantic code, their agreement is one opinion — the
independence inventory records which pairs those are, and for floating point the answer is
already *shared* (184 of 199 files byte-identical). For an integer obligation in this profile no
sharing has been found, which is recorded as `no-evidence-of-sharing` and is deliberately weaker
than `not-shared`.

**Not accepted:** a model's own output as the expected value; agreement between a model and a test
suite that derives its expectations from that model.

### `implementation-defined` — the specification delegates to the EEI

**Required:** the profile's choice stated with its source locator, **and** one of —
(a) the reference configured to the same choice, with the configuration pinned and its effect
demonstrated by a control that changes the observation; or
(b) the difference enumerated as a profile difference, with the reference's choice recorded.

⭐ The control in (a) is the load-bearing half. `P0-PROFILE.6` established the pattern: flipping
the misaligned-access policy, with the same binary and nothing else changed, produced a real first
divergence. Without such a control, "the reference is configured to match" is an assertion about a
file rather than a statement about behaviour.

**Not accepted:** a disagreement recorded as a defect. A reference that chose differently under a
delegated choice is a **profile difference**, and filing it as a defect is how it stops being
looked at.

### `unspecified` — the specification declines to say

**Required:** evidence that the model can **report the case as unspecified**, not evidence that it
produces a particular value. The laboratory policy's outcome is also recorded, but the outcome is
not the obligation — the reportability is.

**Not accepted:** differential agreement. Two implementations agreeing on an unspecified case
tells you they made the same choice, which the specification permits either way.

### `reserved` — the encoding is reserved in this revision

**Required:** the behaviour of **each** reference model enumerated separately, and every
disagreement classified. `D-SHIFTW-RESERVED` is the live instance: this revision marks
`SLLIW`/`SRLIW`/`SRAIW` with `imm[5] != 0` as reserved, where an earlier revision defined them to
raise an illegal-instruction exception, so a model built against the older text may legitimately
trap where this one need not.

**Not accepted:** a single model's behaviour taken as the answer. Disagreement here is *expected*
and is the finding, not a failure.

### environment assumptions — what the harness must supply

**Required:** a **positive and a negative** fixture per obligation, exercised at the interface
**independently of the CPU instruction handler** (`docs/CPU_ENVIRONMENT.md` §4.1), with the
negative case reported as a **contract violation** rather than as a target exception.

⭐ Negative fixtures are not symmetry for its own sake. `P0-PROFILE.8` measured the difference: a
jump that fails to skip writes a register nobody was watching, and a checker inspecting only the
registers it expects to change cannot see it. The negative observation caught exactly that.

## What no class accepts

- **A number with no producer.** Every recorded result names the command that made it.
- **A run that has not been reproduced.** Reproduction is byte-identical re-execution, recorded.
- **A green result from an instrument never seen RED.** Every gate here ships controls that were
  observed failing for the stated reason before the gate was trusted.
- **"Passed" with a required check missing.** `EVD-08`: the report reads `incomplete` instead.

## The honest shape of this policy today

⛔ **66 checks are declared and 0 are implemented.** That is not a flaw in the policy; it is the
policy working. The declaration exists so that `P1-LAB` and `P2-SCALAR` build fixtures against a
standard fixed before them, rather than discovering after the fact that the available evidence
happens to be the required evidence. Until those fixtures exist, gate `G0` cannot read `passed`
and the report says so in its verdict rather than in a footnote.
