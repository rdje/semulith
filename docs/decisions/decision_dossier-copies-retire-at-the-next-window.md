# Credited cases' measured records leave the dossier at the next pinned window; until then a new case is credited without a copy

- **Type:** `decision`
- **Date:** `2026-11-04`
- **Status:** `active`
- **Owner / source:** the director, 2026-11-04, on the option raised at `P4-SYSTEM.14` a43b-3h (a43b-c3; recorded at a43c-3, `SEMULITH-P4-0343`): "Let's do as you recommended it. All I want is
  your decisions and actions to be sota, signoff and production-grade." and "And they shall serve the project long-term."; amends step (iii) of
  [`decision_state-capture-plan.md`](decision_state-capture-plan.md) and answers item 6 of
  [`decision_req-d-csr-set-credited-implemented.md`](decision_req-d-csr-set-credited-implemented.md).
answers: Where does a credited case's measured record live, what does G-TRACE list until that moves, and what must the next pinned window do about it?

## The fact

The dossier, `profiles/rv64gc-lab-v0/references.sexp`, holds a form-for-form copy of each credited case's measured record, and `G-TRACE` lists those copies. It stopped scaling at the third case:

| Measured 2026-11-04 | Bytes |
| --- | --- |
| `references.sexp`, with the M and XLEN copies | 50,323 |
| CSR-SET's measured record | 27,346 |
| Together | 77,669 |
| The per-file ceiling for an authored file in `profiles/` | 65,536 |

Every retained case's manifest pins `scripts/gate_report.py` and `scripts/dossier_sexp.py` (`grep -c`, 1 each, in all three), so reading the records from anywhere else moves a pinned input and lapses every credit. The
report generator is pinned for one reason: `scripts/experiment_verification.py:39`, `from gate_report import contract_measure`, the only import that puts it in a retained experiment's module closure.

## The decision

1. **Until the next pinned window, a new case is credited without a copy and without a `G-TRACE` row**: CSR-SET already, ZICNTR and SSTC the same way. The ceiling stays 65,536 B. The status is unaffected: it derives from the credit
   record, which pins `evidence/<case>/measured-experiment.sexp`, and the method review validates that graph on every read. `G-TRACE` stays green on its two records.
2. **The next pinned window retires the copies.** `gate_report.py` reads a credited case's measured record from `evidence/`, its one owner, and `G-TRACE` lists every credited case. That removes about 32 KB of duplication and the mirror check it needs.
3. **The same window takes the report generator out of the experiments' inputs.** `contract_measure` moves to a small module of its own, so `experiment_verification.py` no longer imports `gate_report.py` and no later manifest pins it. Editing a report should never lapse evidence; this removes that whole class of lapse rather than paying for it once.
4. **No window is opened for this alone.** It retires every credit until the cases are re-captured and re-credited, and the a43b-2 window took five units. It rides with the next pinned edit that is needed anyway; a43b-c2, the deriver's placeholder, waits for the same window.

## Why

- One owner per fact. A mirror of retained bytes adds a check and no evidence, and raising a ceiling to hold more of it would pay the ceiling's cost to keep a duplicate.
- The cost of a window grows with each credited case, so the decision to move the generator out belongs to the first window that can, not to a later one.
- It claims less meanwhile and forecloses nothing: the gate report lists fewer experiments, and every status stays true.

## How to apply

- `scripts/probe_dossier_qualification.py` holds the dossier to its two records, so adding a copy, or the retirement, re-states that arm.
- A credit for ZICNTR or SSTC names this record in its decision, and the gate report's `G-TRACE` table is read as "the records in the dossier", not "every credited case", until the window.
- The window's design measures before it moves: re-derive the manifests' module closure with `contract_measure` moved, and confirm no other report or book generator is in it.
- Its re-captures should be byte-identical to their predecessors, as a43b-2d's were; a difference is a finding, not a retry.

## Carried out (2026-11-05, `P4-SYSTEM.14` a43e-1)

This is the window ([`decision_sstc-delivery-needs-the-pinned-window.md`](decision_sstc-delivery-needs-the-pinned-window.md)). Item 3 is done: `contract_measure` lives in `scripts/effective_contract.py`, and `experiment_verification.py` imports it from there, so the next manifests pin no report or book generator. Item 2's first half is done: the two copies left `references.sexp` (50,323 B → 18,392 B) and `G-TRACE` lists nothing while no credit is current. Its second half, `gate_report.py` reading each credited record from `evidence/`, lands with the re-credits at a43e-5.

## Finished (2026-11-05, `P4-SYSTEM.14` a43e-5)

Item 2's second half landed with the re-credits. `gate_report.py` takes `G-TRACE`'s experiments from every current credit of the unit, each case's record staying in `evidence/`: a lapsed credit is no evidence, with no copy to fall back on. The ruling's other half is now mechanical: a credited case with no `G-TRACE` row keeps the axis open and names the case. Both fired RED, each guard omitted in memory (`target/p4-system-14/a43e-5/check/gate-report-red.txt`). `G-TRACE` lists all five.
