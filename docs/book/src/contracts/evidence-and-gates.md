# Evidence, traceability and gates

> **Orientation.** This is the contract that decides what the project is allowed to say.
>
> Three ideas carry it. First, **evidence is a structured claim**, not a grade: it names the
> property and profile it addresses, how it was obtained, its exact inputs, its results, its
> independence, and its limitations. There is deliberately no universal letter score, because a
> differential test over one arithmetic case and a source-reviewed global invariant answer
> different obligations and averaging them destroys both.
>
> Second, **the graph is many-to-many and machine-checked**. Requirements, semantic symbols,
> generated artifacts, generator steps, tests, comparators, source artifacts, reference builds
> and evidence results are nodes; `implements`, `depends_on`, `generated_from`, `exercises`,
> `expects_from` and `supports` are edges. The invariants in §3 are the ones worth reading
> twice — particularly *no untested included requirement is silently reclassified as an
> exclusion*.
>
> Third, **change impact is conservative by default**. Uncertain influence broadens the
> selection rather than narrowing it, and a shared change — arithmetic, decode, memory
> contract, event scheduling, build features, reference adapters, comparison masks — defaults
> to the whole affected profile.
>
> §6, *Testing the validator*, is the part most projects skip. A comparator that hides a
> semantic error passes every test in the suite it is hiding it from.

{{#include ../../../EVIDENCE_AND_GATES.md}}
