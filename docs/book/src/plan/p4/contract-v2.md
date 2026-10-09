# P4.13 — Completing the environment contract

**Status:** Census and complete state inventory landed; version 2 remains open.

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

## Complete state inventory

The state census now describes the whole selected laboratory profile. Its twelve
candidates are answered, and its consequence names every state owner:

| State | What must be retained for exact continuation |
| --- | --- |
| Integer registers and control | x1–x31, PC and current privilege mode; x0 is constant |
| Floating point | f0–f31, each 64 bits |
| CSRs | 26 storage owners behind 33 named CSRs |
| Memory | The laboratory's main-memory bytes |
| Translation cache | Four TLB entries and the FIFO replacement position |
| Reservation | Physical address, width and validity |
| Waiting | ACTIVE or WAITING |

CSR aliases add no storage. For example, `time` and `cycle` view `mcycle`, and
`fcsr` combines `fflags` and `frm`. The virtual clock is already part of those
owners; this laboratory has no external timer or interrupt-controller state.
Cold reset constructs all owners anew. Exact continuation must also preserve
the current TLB replacement position, reservation and wait state: cold reset is
not a substitute for restoring them.

This correction changes the declared inventory and its generated metadata.
The definition module also records the updated state-source hash in its
provenance manifest. Storage, reset values, accessors and execution remain
byte-identical. Snapshot
and replay serialization still belong to P4.16; this inventory does not claim
that those features are implemented.
