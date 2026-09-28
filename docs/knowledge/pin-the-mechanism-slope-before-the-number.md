# My measurement says "1.4 allocations per step" — is that signoff-grade?

Not until the mechanism producing the number is pinned, exactly, by a gate that fails when
the mechanism changes. A measured figure with no pin is a memory of a measurement: it goes
stale the day the code changes, and nobody notices because nothing recomputes it.

Two moves make a count signoff-grade:

1. **Separate the slope from the intercept before attributing anything.** Run the workload
   for N steps and for 2N steps and difference the counts — a per-step allocation is the
   slope, setup cost is the intercept. An attribution argued from code reading ("this Vec
   is the only allocation on the path") is a hypothesis; the slope proves it. In the
   founding case (`P1-LAB.13`), the untraced interpreter path pinned at exactly 1
   allocation per step with zero intercept — the operand Vec — while the traced path's
   figure only made sense once a second mechanism was found: the observation diff compares
   VALUES, so a write that changes nothing allocates nothing, and workloads that settle
   into fixed points (loops computing the same values every iteration) allocate far less
   than one Vec per step. The naive model said ~2/step; the truth was 1.2 — the measured
   number was right and the mental model was wrong.
2. **Count per thread, not per process, when the suite runs in parallel.** A
   process-global counter inside a parallel test binary counts every sibling test's
   allocations; exact pins are impossible. A thread-local counter makes the pin exact
   (`semulith-verify::bench::alloc` carries both scopes — the single-threaded CLI sees
   them agree by construction).

And fire every pin RED before trusting it: perturb the pinned constant, watch the suite
fail naming the true value, restore. A pin that has never failed is a hope, not a gate
(`self-test-arms-that-never-ran.md` is the same lesson for harness arms).

Provenance: `P1-LAB.13` (2026-09-29) — the `.11` performance baseline's allocation figures
were reported-but-unpinned until the slope/intercept probes and the four exact pin suites
landed.
