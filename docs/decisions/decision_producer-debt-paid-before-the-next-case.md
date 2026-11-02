# The producers' first-case literals are removed in one planned lapse that opens CSR-SET — before a third case freezes them

- **Type:** `decision`
- **Date:** `2026-10-29`
- **Status:** `active`
- **Owner / source:** the director's question of 2026-10-29 ("which decision would you make here that is sota, signoff
  and production-grade that would help SEMULITH going forward?") on the leaked M wording found at `P4-SYSTEM.14`
  a43a-3; decided by the workflow under [`decision_four-rulings-delegated.md`](decision_four-rulings-delegated.md).
  Supersedes the open-ended "waits for the next unavoidable re-capture" of
  [`decision_req-d-xlen-credited-implemented.md`](decision_req-d-xlen-credited-implemented.md) by naming that capture.
answers: When and how are the M literals in the pinned producers (the control prose and control-run id) removed, and what does it cost?

## The fact / decision

1. **Not deferred indefinitely, not paid for prose alone: paid at CSR-SET, before its declaration.** The window
   `a43b-2` opens the CSR-SET program; no further case is declared on the current producers.
2. **The window, in order** (the a44 pattern: a44-2b … a44-5):
   - *Pinned edits, one commit.* The control's id and statement become case declarations: `schema/matched-case.sexp`'s
     control form gains them, `scripts/matched_gpr_case.py` reads them, `scripts/capture_div.py` emits them, and no
     first-case literal remains in what the producers write (the knowledge card's audit run over every emitted string).
     In the same commit, the high-risk predeclaration vocabulary CSR-SET needs — its second method and adversarial case
     (`decision_state-capture-plan.md` item 2; the policy review's `risk-method` leg has no declaration vocabulary for it
     yet) — so the pinned schema moves once. `CR-GC-M-2` and `CR-D-XLEN-1` lapse there and are retired by removal in that
     commit, `REQ-GC-M` and `REQ-D-XLEN` record `planned`, their dossier copies and `G-TRACE` rows leave.
   - *A guard.* The capture-input probe asserts that each planned record's control id and statement equal its
     declaration's, so a hard-coded literal cannot return.
   - *Re-capture once each.* `rv64gc-m-forms-v5` and `rv64gc-xlen-forms-v2` declared (v4 and xlen-v1 stay history) and
     captured once on a quiet host; their traces must be byte-identical to v4's and xlen-v1's (the reproduction check,
     as a44-4 did for v3 → v4). The evidence family's bounds are re-derived for the two new directories.
   - *Close.* The reviews' `RETAINED_CAPTURES` rows, `CR-GC-M-3` and `CR-D-XLEN-2` through the same crediting act, the
     statuses, dossier copies and `G-TRACE` rows. Then CSR-SET is declared on the clean producers.
3. **Not widened:** `schema/matched-case.sexp`'s cell vocabulary. `form:<mnemonic>` carries CSR-SET's reads, and no
   consumer reads a cell beyond its pattern (`matched_gpr_case.py` alone).

## Why

- Every capture pins `capture_div.py`, so the cost of the fix grows with each case captured on it: two cases now is the
  least it will ever cost. Waiting freezes "wrong quotient must diverge" into CSR-SET's and SSTC's records too — a
  false control statement in retained evidence that a sign-off reviewer reads, and a caveat in every credit.
- The lapse is not extra: CSR-SET is high risk, and its second method and adversarial case must be predeclared in the
  case declaration the capture pins — the schema moves at CSR-SET whatever is decided here. One window pays both.
- A lapse is honest and bounded: the statuses fall back to `planned` and the gate shows it until the re-credit; the
  traces' byte identity proves the re-capture changed only what was declared.

## How to apply

- Plan the window's pinned edits before the first of them (a44-1's design pattern): every pinned file it moves, every
  probe and count that moves with it, the order, and the capture script for a quiet host.
- A literal the audit finds after this window is fixed in the next window that moves a pinned producer, and named in
  the credits of any case captured meanwhile.

## Designed (`P4-SYSTEM.14` a43b-2a, `2026-11-02`, `SEMULITH-P4-0328`)

The full design is the a43b-2a record in `docs/tasks/P4-SYSTEM.md`; its binding choices:

- **The control's `id` and `statement` are optional in `schema/matched-case.sexp` and required by the producer.** The four
  retained declarations are bytes that cannot gain fields; `capture_div.py` refuses by name to plan a case without them.
  One schema, not a `-v2` beside it.
- **CSR-SET's vocabulary is two optional case forms**, `second_method` (one of the policy's four named methods, at least two
  producers, their common inputs, what is independently derived) and `adversarial` (the properties witnessing the failure
  mode). For high or critical risk the `risk-method` leg holds only when the producers are the measured graph's, with
  pairwise distinct versions; every pair of them is a recorded producer pair whose shared inputs intersect to the declared
  common inputs; the independence text earns no credit beyond the pair's recorded assessment; and every adversarial
  property is a declared property of a capture whose baseline agrees.
- **Order:** a43b-2b the one pinned-edit commit (both credits retired, 48 / 0); a43b-2c v5 and xlen-v2 declared (the family
  89 → 133 files); a43b-2d each captured once, traces byte-identical; a43b-2e both re-credited (46 / 2); then a43b-3.

## Implemented (`P4-SYSTEM.14` a43b-2b, `2026-11-02`)

The pinned edit landed as designed, with four refinements the implementation measured (the a43b-2b record):

- **Copies declare the control.** Between the edit and the v5/xlen-v2 declarations no case in the tree can be planned,
  so the probes that plan in runtime copies write a control into the copy (`probe_div_command.declare_control`: the
  historical words for the M-family cases); the real tree's history is asserted refused by name.
- **Stale without regeneration.** The method review detected `stale` by regenerating; history the producer refuses
  read `refused` (a red gate). On a refused preparation it now re-checks the declaration route's pins on the capture's
  own manifest, read through the measured record — v4 and xlen-v1 read `invalidated by schema/matched-case.sexp`
  (knowledge card `a-producer-refusal-hides-staleness-detected-by-regeneration.md`).
- **Condition 4 is a check, not only a report:** a producer pair recorded `shared` refuses the second method; a
  declaration at low or medium risk is judged by all five conditions.
- **The guard lives where planning lives:** the command probe, which plans in copies, holds the literal guard
  (unique-token control, prose only from the case file or the reviewed neutral set); the case probe's
  retained-record agreement (`probe_matched_gpr_case.py`) holds each declared control id and statement equal to its
  planned record, from a43b-2c, the first declarations carrying them.

## Closed (`P4-SYSTEM.14` a43b-2e, `2026-11-02`)

The window ran a43b-2a … a43b-2e in one day: designed; one pinned-edit commit (both credits retired, 48 / 0); v5 and
xlen-v2 declared, their predeclarations differing from their predecessors' only in what was declared; each captured once,
traces byte-identical; both re-credited (`CR-GC-M-3`, `CR-D-XLEN-2`; 46 / 2; G-TRACE green). No first-case literal remains
in what the producers write, the command probe guards against its return, and CSR-SET's second-method vocabulary waits
in the schema for its case (a43b-3).
