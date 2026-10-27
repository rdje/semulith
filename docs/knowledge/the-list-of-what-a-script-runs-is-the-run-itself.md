# I want every command a self-test runs, to run them in parallel first — can I read them off the script?

**No. Read them off the run.** A regular expression over the script's text finds the commands as they
are *written*: the explicit `python3 "$ROOT/scripts/probe_x.py" --mutation m` lines. It cannot follow
what the script *computes* — an array set inside a loop (`for mode in normal optimized; do
mode_python=(python3); [ … ] && mode_python+=(-O)`), a flag read from a variable, a mutation list
built from another command's output. The list that is exact by construction is the one the run
produces about itself: run the self-test once with the command shadowed by a function that only
writes down its argv, then run that list in parallel, then run the self-test for real with the
function answering from the record.

## What happened

On 2026-10-27 (`XTASK.8` slice c) PROFILE-CONSISTENCY's self-test — 1114 probe invocations, 2730 s
of its 2746 s serial wall — was to prefetch its invocations in parallel. The first prefetch
enumerated them from the script's source with two regular expressions and read the mode arrays
from their definitions (`name=(python3 …)`). It found 533 distinct argv and all of them valid. The
instrumented serial run then recorded what actually ran: 1114 distinct argv. The 625 missed were the
array-driven loops the regex could not follow (the arrays gain `-O` inside the loop, not at their
definition), and 44 of the 533 it did find never run at all (a base read from a definition the loop
overrides). Every missed shape would have run live — slower, never wrong — so the gate stayed
right; it would have stayed slow.

## How to catch it, and what to do

- **Enumerate by recording, not by reading.** A shadow function with the command's name, in force
  inside the self-test only, that appends its argv to a file and returns 0 for the commands of
  interest (and runs everything else live) lists exactly what the self-test does today, and
  tomorrow after someone adds an arm. Nothing to keep in step with the script's text.
- **Compare the two lists before trusting either.** The instrumented run's argv against the
  enumerator's output (`comm -23`, `comm -13`): the misses AND the phantoms are the finding.
- **Keep the answer exact and the fallback live.** The record is keyed by the argv itself (joined by
  U+001F, `/` as U+001E — a file name bash builds by expansion alone, no process per lookup); an
  exact match is answered, anything else runs live, and the verdict is still the self-test's own
  `score` over the bytes — a tampered record is a MISS, not a pass (`control_shadow.sh`).

Evidence: `docs/tasks/XTASK.md` `XTASK.8` slice c; target/xtask/xt0017 (observed-argv.txt 1114 probe argv vs
enumerated-argv.txt 533, missed-argv.txt 625 probe argv, phantom-argv.txt 44; control_shadow.out).
