# From sources to checked behavior

The traceable chain is source → selected decision → requirement → versioned
obligation → named positive/negative checks → executable producer and exact
observations → structured verdict. A generated table or successful test occupies
one place in that chain; it cannot stand for the entire chain.

## Scope before code

The registry's repeated `requires` fields are all read, in declared order. A
missing C07 after a covered C01 must refuse just as a missing first category does.
Registration's negative control exposed the old first-field-only reader; the
shared mapping and scope-gate tests now reject that blind spot. All existing
unit declarations are preserved, and the full six-unit required census passes.

## A fetch-boundary example

With C selected, fetch begins with a two-byte parcel. A compressed instruction at
a page end needs no next-page parcel; a 32-bit instruction beginning at the same
halfword needs the second parcel and can fault there. Check the requested addresses,
lengths and order, start PC saved on the trap, and fault address. A decoder returning
the right final instruction after an extra read is still wrong for this contract.
The page-end C guests and direct fetch observers separate that failure from a
wrong compressed expansion. The P4 C/fault chapters retain worked observations.

## A CSR example

A CSR instruction's source **field** controls write suppression; a nonzero source
register containing zero does not make the instruction the same as a zero source
field. `rd=x0` suppresses a destination write and, for appropriate forms, the CSR
read. Privilege and read-only checks must precede forbidden side effects. Observe
CSR owner, destination, trap state and requests; mutate a suppression/gate or an
observer to show the checker notices. Identical final values can hide an extra
side-effect-free read, so a separately declared inspection rule is needed for that
claim. Finite dynamic indistinguishability is a limit, not an invitation to assert
that a read never happened.

## A failed-SC example

Create or omit a reservation, translate the target, and independently select
physical permission. A nonmatching reservation does not authorize bypassing the
permission check. Distinguish completed failure code1 from a store-access trap;
observe destination/reservation preservation on the fault and exact request kinds.
A test that checks only memory unchanged accepts both behaviors and misses the
permission defect. The atomics chapter retains the repair and discriminating
controls through the public CPU/environment interface.

## Reproduce the document and scope checks

Run from the repository root with project-local tool caches and scratch paths:

```bash
python3 scripts/gen_model_book.py --unit rv64gc-lab-v0 --check
bash scripts/check_scope_coverage.sh
bash scripts/check_materials_bill.sh
bash scripts/check_contract_freeze.sh
bash scripts/check_gate_report.sh
mdbook build docs/models/rv64gc-lab-v0
```

For a deliberate stale-table diagnostic, edit only a disposable on-volume copy
and point `gen_model_book.py --profile-dir profiles/rv64gc-lab-v0 --book-dir COPY
--check` at it. It must refuse drift. Restore or regenerate from the canonical
inputs; never repin sources to accept a modified generated table. MATERIALS-BILL
also has self-tests for missing sections, absent limits and catalogue disclosure.

To assess executable behavior, `make check` runs strict Rust lint and tests;
`make ci` additionally runs all doctrines, benchmark legs and every book. This
registration milestone runs that complete suite, but it does not manufacture
missing external, replay, host or release evidence records. Future .14 qualification
must declare comparison scope and controls before executing its fresh runs.
