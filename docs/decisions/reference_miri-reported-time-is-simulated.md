---
answers:
  - Why does Miri's reported test duration differ from GitHub step wall time?
  - Which clock should be used for elapsed-time comparisons of Miri runs?
---

# Miri's reported test duration uses interpreted time

- **Type:** `reference`
- **Date:** `2026-10-08`
- **Status:** `active`
- **Owner / source:** CI-RECOVERY.4; hosted artifacts/timestamps and published Miri documentation

## The measured discrepancy

Run 37800113741 at f4364bc completes both interpreted core suites, 153 passed and
zero failed/ignored each. Its artifact reports 1294.44 seconds for native and
1294.07 for powerpc64. GitHub's corresponding step timestamps span 771 and 779
seconds, including setup. Each suite executes all 153 tests; the durations come
from different clock domains.

The [published Miri contract](https://github.com/rust-lang/miri#readme) states that
default isolation replaces host clocks with deterministic implementations. Our
runner supplies no isolation-disabling flag, and the Cargo configuration supplies
none. This explains why interpreted harness durations are unsuitable as external
wall-time measurements.

## How to apply

- Preserve test counts and reported durations exactly, identifying their clock.
- Measure elapsed job time from external timestamps; benchmark performance with
  the normal benchmark instruments.
- The earlier DEV_NOTES description of these roughly 1294-second reports as
  about 22 minutes is reported interpreter time, not a wall-time claim. Do not
  use it to compare hosts' speed.
- Keep isolation enabled for the existing verification; no test setting changes.

Evidence: https://github.com/rdje/semulith/actions/runs/37800113741.
Regenerable local artifacts: target/ci-recovery/hosted-miri-1/miri.log and cross.log.
