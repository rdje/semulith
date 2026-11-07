# A requirement with nothing to run closes on a selection's record, a credit with no case

- **Type:** `decision`
- **Date:** `2026-11-07`
- **Status:** `active`
- **Owner / source:** `P4-SYSTEM.14` a51-11, `SEMULITH-P4-0389`; the workflow under [`decision_findings-are-the-engineers-to-call.md`](decision_findings-are-the-engineers-to-call.md), carrying out track 4 of [`decision_the-seventeen-called.md`](decision_the-seventeen-called.md).
answers: How can a requirement with no behaviour of its own reach `implemented`, and what keeps such a credit honest?

## The fact / decision

`REQ-D-ABI`, `REQ-D-FP-DEFER`, `REQ-D-ROUTE-FLIP` and `REQ-D-SCOPE-CENSUS` state what the laboratory selected and how it stays true. Their behaviour is each extension's own credit, so a case would add nothing.

1. **The shape.** A credit names a case or a selection, never both. A selection has no receipt. Its `measured` pin is its record, `profiles/<profile>/selections/<SEL-id>.selection.sexp`, and the catalogue's schema refuses nothing else: `credit_records.py` refuses a credit naming both or neither.
2. **Declared before anything runs.** A `kind record` disposition in `dispositions.sexp` states the argument and each fact with the value the statement expects. `scripts/selections.py --record` refuses to run without one, and refuses to take a second record.
3. **What a record retains.** Each fact as read. Each named check's output, run twice and compared. The identity of every input it read. Its limitations. That is what the policy's "Records, controls and currentness" asks of a credited disposition.
4. **What a read does.** It reads every fact again and holds it to the declaration and to the record. It holds the required checks to the retained runs, and the statement's clauses to the facts, as the trace holds a case's properties. A read starts no process: the named checks and drift gates run in every commit's gate on their own.
5. **A fact is compared, not a file's bytes.** A `Cargo.lock` that moves some other package does not lapse the backend's credit. One that moves the backend does. The record and the policy are still pinned by bytes.

## What measuring found first

- **The controls already exist.** `scripts/check_gc_contract_scope.py` has named positive and negative checks for all four, and the Rust contract registry runs them in the ordinary test suite. The negative ones refuse 5, 5, 4 and 2 violating copies. So a record runs those, and this adds no second checker.
- **They do not read everything the statements say.** The ABI check reads the declaration and the state, and no object anyone compiled. The backend check confirms `fp.rs` exists, not that nothing else uses the backend. The census check never compares with `rv64i-lab-v0`, though the statement says "the same enumeration and source". Each is a fact a record reads, at a51-12.

## How to apply

- A new selection is a new record and a new credit. When a fact moves on purpose, delete the record and its credit in the same commit, and take a new one.
- This is for what is selected and has no behaviour of its own. A requirement with behaviour to compare needs a case: a record cannot stand in for one.
