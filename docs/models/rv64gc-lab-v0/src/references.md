# References and comparison limits

The generated [reference table](materials.md#reference-candidates) identifies each
candidate and its recorded matching scope. `references.sexp` is canonical;
`reference/sail-rv64gc-lab-v0.override.sexp` declares the public configuration.
Adapters and author scripts are tracked project tools. Dependency interaction uses
published configuration, builds, APIs and outputs; source access grants no license
to infer a submodule's internal implementation or ancestry.

## What the earlier comparisons mean

Earlier privilege, Sv39, atomic, interrupt/wake, FENCE.I, FP, fault, M and C runs
are historical finite observations. They name agreement, architectural latitude
and platform differences separately. The live adapter compares declared GPR changes
and witnessed delivery gaps. It does not infer complete PC, instruction-word, FP,
memory, CSR or request equality from the same text output.

For example, the compressed timer guest differs at the boundary where the
laboratory delivers STI and the matched reference proceeds with C.ADDI. Public
configuration and fresh public traces identify an unmatched timer source.
That result is not a compressed arithmetic defect and is not acceptance for
Sstc timing. Likewise disabled reference Zicntr and absent injected physical
refusal regions leave those observations unmatched.

A deliberately wrong C.LI result must diverge through a fresh reference run.
An adapter that accepts a failed producer, stale trace or changed expected value
is itself a defect, even if the reference program normally succeeds. Controls
must exercise the actual execution/comparison path and then prove restoration.

## Independence has a denominator too

No current claim authenticates Sail/Spike implementation ancestry. Agreement is
useful on named inputs, but it does not establish independent numeric derivation.
The spec-side author and engine can share opcode tables or arithmetic producers;
record those common inputs and do not count two wrappers as two methods.

For an FP requirement, a source-derived exact arithmetic fixture can provide a
second method when its producer and scope are explicit. A Sail GPR-only trace
cannot by itself qualify FP result bits/flags. For translation, a separately
specified request-path expectation can expose a walk or fault-order defect that
a final handler register masks. The policy requires methods to address the same
property, with their controls and limitations recorded.

## What comes next

The earlier comparisons are prose in the canonical reference dossier. Structured
experiment, control and independence records, fresh repeated execution and
adequacy/status checks remain .14 obligations. The [policy](policy.md) was declared
after implementation and is prospective; this book does not backdate it. Candidate
availability, a successful book build and a complete contract registry do not
advance requirement status or close G-TRACE.
