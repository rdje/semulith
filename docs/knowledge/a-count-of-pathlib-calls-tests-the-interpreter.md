# The hosted doctrines run refused UNIT-BOOKS on inputs that had passed the run before — what changed?

**The interpreter, not the code.** `scripts/probe_book_includes.py`'s
`test_another_volume_and_changed_input_refuse` patched `Path.stat` to report a foreign device for an include target and
asserted the target was stat'ed exactly once (`assertEqual(calls, 1)`; a sibling assertion counted `Path.lstat` calls,
`== 2`). How many pathlib calls reach `Path.stat` is pathlib's own business: on Python 3.11 and 3.12, `is_symlink()`,
`exists()` and `stat()` each route there, so `book_paths.source_path`'s three checks made 3 calls; on 3.14 only `stat()`
does, so 1. The runner's `python3` is 3.12, this host's 3.14: the probe passed here and failed there (`AssertionError: 3 != 1`,
run 40763391753, 2026-10-28) — and the run before it had passed with the same inputs.

## What happened

The first hosted refusal said only `UNIT-BOOKS: REFUSED — the check does not discriminate (self-test failed)`: every
driver printed a self-test miss only in a verbose run. `XTASK.12` gave all 29 drivers a quiet report path, the next hosted
run named the test and the line, and the failure reproduced exactly under a local Python 3.12 (and 3.11), never under 3.14.

## How to catch it, and what to do

- **Assert the property, not the route.** The behaviour the test guards is "a source on another volume is refused, for
  that reason, before it is ever opened": assert the refusal's reason and spy on the read (`os.open`), and keep
  `calls >= 1` to prove the patch was consulted. A call count pins one interpreter's internals.
- **Run the suite under the runner's Python before a push** when a probe patches standard-library methods: here a
  `python3` shim to 3.12 on PATH reproduced the hosted failure and then cleared the whole gate (13 checks green).
- **A refusal that does not name what missed is undiagnosable from a log**; print the misses on the quiet path.

Evidence: target/xtask/xt0071 (the 3.11, 3.12 and 3.14 runs, the RED with the volume refusal removed, gate-py312.log);
`docs/tasks/XTASK.md` `XTASK.12` slice c.
