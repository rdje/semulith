# An identity proof needs a must-diverge control — identical failure output compares byte-identical

**Short answer:** a byte-level identity proof ("the pre-change corpus runs identical on the
old and new engine") is only as strong as its answer to one question: *can this harness
tell different apart at all?* If both runs fail the same way — the same usage error, the
same crash, the same empty trace — the comparison reports byte-identical over garbage.
The control that sees it is a case that MUST diverge: run the change's own new fixtures
against the old engine, where the new behavior provably does not exist. If they compare
identical, the harness is broken, not the identity.

Measured at P4-SYSTEM.7 slice (b) (2026-10-06): the slice's identity harness ran 101
pre-slice guests through two CLI builds and printed "101 byte-identical, 0 diverge" —
while every one of the 202 invocations had failed with the same usage-error text (the
driver passed `--profile NAME`; the CLI parses `--profile=NAME` only). The must-diverge
control — the slice's two new guests, which trap on the new engine's FS gate and cannot
trap on the parent — reported "IDENTICAL", and the contradiction named the harness bug
in one line. Fixed, the proof measured 5,491 trace lines cmp-clean and both control
guests diverging as required.

## The pattern that works

- Every identity/equivalence proof carries a case that must NOT be identical — the new
  behavior's own fixtures against the old engine is the natural one — and the control's
  verdict is reported beside the identity count, never assumed.
- Include the exit status (and stderr, where it carries the verdict) in what is compared;
  stdout alone lets a failing runner's empty output agree with itself.
- A usage-error or crash text that is identical on both sides is a harness property, not
  evidence about the engines — the control is how you learn it happened.

## Evidence

- The slice-(b) harness and its two runs live in the leaf's verification record
  (`docs/tasks/P4-SYSTEM.md`, `.7` slice (b)'s checklist: the ADDRESSED box's RED line).
- The sibling shape — agreement over a truncated prefix — is
  [`a-shorter-trace-is-not-agreement.md`](a-shorter-trace-is-not-agreement.md); this card
  is the same lesson one level up: agreement over identical FAILURES.
