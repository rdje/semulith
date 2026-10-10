# Withdrawn policy and gate prose — P4-SYSTEM.14 a8

Historical bytes from `e3a5a72627239ec96d879168559ccdb86c8afc7e`, captured by
SEMULITH-P4-0199. Preserve the complete original scalar policy, the report's old
presence label, and the superseded gate-open statements. The scalar declaration's
original timing and category requirements remain historical facts; its internal
ancestry assertions and mutable current count are withdrawn as current evidence.
The maintained files distinguish prospective GC requalification from past runs.
No implementation ancestry, requirement status or release credit is added.

## Reconstruction map

Authenticate the corrected source's length/SHA and its replacement spans, then
replace spans in descending byte-offset order with the historical payloads.
A zero-length replacement inserts the removed span. Payload lengths exclude
framing; authenticate the full reconstructed original. The corrected revision
is the named work-unit commit, so later edits cannot alter this capture's identity.

```json
{
  "base": "e3a5a72627239ec96d879168559ccdb86c8afc7e",
  "work_unit": "SEMULITH-P4-0199",
  "sources": [
    {
      "path": "profiles/rv64i-lab-v0/EVIDENCE_POLICY.md",
      "old_bytes": 5817,
      "old_sha256": "d0c32d272ecdf4b372aad80cbe3c1a9ceed356968a6106db3e12351caf5bea83",
      "new_bytes": 5699,
      "new_sha256": "8a4dbb655a57391e962165c22fa49299944377a4b343c5a62f6dfb6517e52d66",
      "changes": [
        {
          "tag": "f1-1",
          "start": 0,
          "old_bytes": 5817,
          "old_sha256": "d0c32d272ecdf4b372aad80cbe3c1a9ceed356968a6106db3e12351caf5bea83",
          "new_bytes": 5699,
          "new_sha256": "8a4dbb655a57391e962165c22fa49299944377a4b343c5a62f6dfb6517e52d66",
          "label": "complete scalar policy before correction"
        }
      ]
    },
    {
      "path": "scripts/gate_report.py",
      "old_bytes": 87559,
      "old_sha256": "0c3679091e21755e07ba5fea74fa4a6521fbf35fe058084d4f1b44e0c392e8d4",
      "new_bytes": 87556,
      "new_sha256": "9766675304eddd6c004dfb2a5418908e1beee7346a7c61dc122f5bbc468f5d8f",
      "changes": [
        {
          "tag": "f2-1",
          "start": 50054,
          "old_bytes": 116,
          "old_sha256": "d14c12cef72a38a4db9ff844d3ee58d8aa33bf06d7c0c75829e6b8f1746d57c7",
          "new_bytes": 113,
          "new_sha256": "4474b777ed7232ea494401b745fb62fb95b244b049a32c9abc736481e8c8ac53",
          "label": "GS presence label"
        }
      ]
    },
    {
      "path": "profiles/rv64gc-lab-v0/gate.sexp",
      "old_bytes": 4033,
      "old_sha256": "0d8478609e6e8633a96e74789151979ef1cc21c23010d4f645e0808b42003045",
      "new_bytes": 3735,
      "new_sha256": "83687aeffc4e1ea81cf269c41a3188626b63c2fd0c4a6df5edea5cb244d029cf",
      "changes": [
        {
          "tag": "f3-1",
          "start": 2279,
          "old_bytes": 495,
          "old_sha256": "220822b101a87e37691a5b4d127afdc56334d13dfeb0db17db3c80e8f192927b",
          "new_bytes": 0,
          "new_sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
          "label": "resolved contract open item"
        },
        {
          "tag": "f3-2",
          "start": 2757,
          "old_bytes": 146,
          "old_sha256": "0a98fe9799ad3c22a33599d54320a14eaf8a7510bf9367976aa68ac5669c4c89",
          "new_bytes": 343,
          "new_sha256": "2c9e5f8fab53526d77ebbe40ea439642fc968191df3fab295f34f7408c9bff17",
          "label": "obligations policy open item"
        }
      ]
    }
  ]
}
```

## f1-1 — historical payload

<!-- BEGIN:f1-1 -->
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

<!-- END:f1-1 -->

## f2-1 — historical payload

<!-- BEGIN:f2-1 -->
                             + f"; predeclared policy (`EVIDENCE_POLICY.md`): {'present' if policy else 'absent'}",

<!-- END:f2-1 -->

## f3-1 — historical payload

<!-- BEGIN:f3-1 -->
(open (axis G-CONTRACT) (owner "P4-SYSTEM.13")
  (statement "P4-SYSTEM.13 owns realization of the remaining effective runtime pairs and the final v2 freeze. The G-CONTRACT criterion derives coverage from the executable registry; the active task tree and runtime book chapters retain completed witnesses and the next slice. Version 2 stays open until every effective check passes and its membership is frozen. P4-SYSTEM.14 retains requirement-status mirrors and structured experiment records."))

<!-- END:f3-1 -->

## f3-2 — historical payload

<!-- BEGIN:f3-2 -->
Every requirement reads planned; no predeclared verification policy exists for this unit; REQ-D-ECALL-EBREAK (an rv64i mirror) is partial on OQ-5.
<!-- END:f3-2 -->
