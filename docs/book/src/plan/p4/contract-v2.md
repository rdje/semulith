# P4.13 — Completing the environment contract

**Status:** Census and execution plan landed; version 2 remains open.

The complete instruction set now runs, including multiply/divide and compressed
instructions. Its contract still contains declarations inherited from earlier
stages. This work checks every effective obligation, fills the remaining boundary
assumptions, and realizes each declared check before freezing version 2.

The census finds 53 effective obligations and 106 checks. Twenty checks currently
run through the unit's registry. A check will receive credit only when its actual
fixture runs: instruction guarantees use executable observations; a scope choice
such as the selected firmware ABI uses a predicate over the canonical documents
and a negative fixture that violates that predicate. Running an unrelated program
cannot establish a scope declaration.

Five boundary topics remain: address units, access widths and memory attributes,
event delivery, ordering, and reset. The scalar profile's assumptions cannot be
copied unchanged. For example, this processor can take interrupts, fetches exact
16-bit parcels, selects RVWMO, and resets floating-point, translation-cache,
reservation and wait state as well as integer registers and CSRs. Time, parcel
fetch and partial progress already have GC-specific records.

Some inherited statements need replacements. Two describe obsolete definition
stages; another describes the earlier floating-point qualification condition.
The fault-priority statement also needs more precise language: address triggers
are absent, while EBREAK and C.EBREAK still raise environment-break exceptions
with cause 3. The pinned priority table distinguishes these cases.

Versioning preserves the record. Frozen version-0 and version-1 statements and
their hashes stay unchanged; version 2 names each replacement and why it replaces
the old statement. The complete per-obligation plan is in the active task tree's
`.13` census. Completion requires every effective check to run, the state census
to describe the actual complete state, and version 2 to be frozen. Until then,
G-CONTRACT and CPU-SYSTEM remain incomplete.
