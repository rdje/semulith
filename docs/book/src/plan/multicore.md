# Multicore and optimization

Both of these are separated from the main line for the same reason: they are the two places
where an emulator most easily acquires a capability it cannot justify.

## Multicore is a CPU milestone, not a threading change

It never arrives by adding host threads. It first extends and revalidates the CPU and
environment contract for the memory model, atomicity, reservations, event delivery, and
progress. SMP Linux is a later *integration test*, not the evidence.

A deterministic sequentially consistent execution mode is a legitimate initial design **if its
produced executions satisfy the selected architecture**. What it is not is coverage: producing
only legal behaviour and exploring all allowed weak behaviour are different claims, and the
second needs its own exploration method, checker, and corpus.

Broader weak-memory exploration uses a separately selected existing operational or axiomatic
checker with a pinned litmus corpus. Do **not** build a research-grade memory-model checker as
an incidental emulator feature.

## Optimization keeps the reference

Profile-guided optimization and JIT work retain the reference interpreter and the
observational-equivalence regression path. Measured performance limitations may justify earlier
optimization — they never justify a skipped CPU gate or altered semantics.

The asymmetry is deliberate: a slow correct model is an inconvenience, a fast model whose
semantics drifted is a defect generator that produces confident wrong answers for everything
built on top of it.
