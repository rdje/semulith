# Two Miri runs reported `finished in 7251.82s` to the hundredth — how long did they take?

**About fifty minutes each; the number is not a duration on this machine at all.** Under Miri's default
isolation the interpreted program has no access to the host clock: `Instant::now()` reads a deterministic
*virtual* clock that advances with the work executed, so the test harness running *inside* the interpreter
prints the same "finished in" for the same code on every run, on any host, however loaded. The figure is a
property of the program, not of the session. A duration read inside the interpreter is the interpreter's time;
wall time is measured outside it — by the caller's clock, or by the mtimes of what the run wrote.

## What happened

On 2026-10-27 (`P4-SYSTEM.17` slice a) the first clean Miri leg over `semulith-core` printed `173 passed …
finished in 7251.82s`, and I reported "Miri takes about two hours per leg" against the rv64i record's "about
three minutes". The recording run then printed the same `7251.82s` for its native Miri leg and `7249.37s`
for the big-endian powerpc64 leg (a different target executes slightly different code, so the virtual count
differs a little). The run's own files told the real story: the Miri leg's target directory was created at
08:19:32 and its log last written at 09:09:12 (2980 s); the cross-endian log closed at 09:59:14 (3002 s);
the whole four-leg run took 6227 s. The doc-tests' `finished in 0.16s` / `0.30s` *did* differ between runs —
rustdoc's harness runs natively and spawns each doc-test under Miri, so that figure is wall time.

## How to catch it, and what to do

- **Two timings identical to the hundredth are not a coincidence; they are a clock that is not a clock.**
  Any measurement that reproduces exactly across independent runs is deterministic by construction — find
  out what it counts before quoting it as a duration.
- **Measure a leg from outside the process under test.** `date +%s` around the invocation, or the mtimes of
  the files the leg writes (the record block of `scripts/check_portability.sh` could carry per-leg wall
  seconds from the caller's clock; today the figures live in the leaf and this card).
- **Harness output under an interpreter, emulator or sandbox inherits that layer's time.** Miri (isolation),
  Wasm runtimes, deterministic simulators and record/replay tools all present a controlled clock; the
  message text looks like the native harness's and means something else.

Evidence: `profiles/rv64gc-lab-v0/portability.sexp`; target/portability/{miri,cross}.log (`finished in`
lines 225) and the directory mtimes under target/portability/miri-target/nightly-2026-09-13; target/
p4-system-17/a/miri-clean.log line 183 (the first run's identical figure); `docs/tasks/P4-SYSTEM.md` `.17` slice a.
