# The command accepted my flag — did the branch that ran actually honour it?

**Not necessarily.** A command that parses an option up front and then dispatches on something
else (a profile, a mode, a format) honours the option only on the branches that were written
with it. A branch added later, or a branch that returns early, accepts the flag and does
nothing — no error, no warning, a run that looks complete.

## What happened

On 2026-10-26 (`P4-SYSTEM.15` slice a) the ACT4 campaign runner was pointed at the rv64gc model
for the first time: `semulith run <elf> --profile=rv64gc-lab-v0 --steps=N --trace-stores`. The
run returned 0 with a 32,902-line trace and not one store line. The CLI parsed `--trace-stores`
for every profile, but the GC profile's branch returned from the command before the block that
writes the store trace — written for rv64i, never reached for rv64gc. Nothing in the CLI said so.

What caught it was the consumer's refusal, by design: the campaign's extractor refuses an empty
store trace (`no store crossings parsed — an unparseable trace is never an empty match`) instead
of reading it as "no stores". A tolerant extractor would have compared an empty signature against
Sail's and reported a mismatch for the wrong reason, or, worse, a shorter signature as agreement.

## How to catch it, and what to do

- **Measure every option on every branch that accepts it.** The cheapest measurement is the one
  that found this: run the same input through both branches with the flag and compare the
  outputs (here, the same ELF on both models: 17,018 identical store lines once fixed).
- **A consumer refuses an empty observation.** An extractor that reads nothing must say so;
  "no stores" and "the flag did nothing" are indistinguishable to a tolerant reader.
- **Thread the option into the branch, do not test for it after the branch.** The fix passed
  `trace_stores` into the GC run and recorded stores at the environment boundary through a
  recording environment — the same pattern the GC run loop already used to count fetches.

Evidence: `docs/tasks/P4-SYSTEM.md` `.15` slice a; target/p4-system-15/a (gc-run.out, smoke-rv64gc.log,
gc-stores.txt vs i-stores.txt).
