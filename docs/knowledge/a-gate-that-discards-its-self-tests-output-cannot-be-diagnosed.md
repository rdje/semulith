# The gate refused with "the check does not discriminate" — which self-test arm missed?

**Short answer:** before 2026-10-23 nobody could say, because `scripts/check_profile_consistency.sh`
ran its self-test as `self_test >/dev/null 2>&1` and kept only the verdict. A self-test that can
refuse a commit must keep its own output: the gate now writes the complete self-test output to
`target/profile-consistency-selftest.log` and prints the `self-test MISS` lines on REFUSED. Read the
log; the arm, its expected and actual exit codes and the probe's output are there.

## The founding measurements

- 2026-10-21 (`P4-SYSTEM.14` a42ar): the second commit attempt was refused after 2 h 10 min in the
  hook — `PROFILE-CONSISTENCY: REFUSED — the check does not discriminate (self-test failed).` and
  nothing else. The self-test then passed twice from the shell (1086 arms, about 35 min each) and the
  five time-budgeted probes passed under a 12-thread CPU burn. Cause not identified.
- 2026-10-23 (a42ax): the same refusal after 2 h 55 min in the hook, with two other repositories'
  gates loading the machine (load average 8–12 on 12 cores). The focused set had been 26 of 26
  green and every probe the arms run had passed in both interpreter modes minutes before. Again
  the MISS line was gone with the `/dev/null`. The children's wall times under the same load used
  at most 7 % of their budgets (`target/p4-system-14/a42ax/children-timing-loaded.log`), so a
  timeout was not the explanation either; the arm's name was the one fact that would have settled
  it, and the gate had thrown it away.

## The rule

- A check that runs a self-test and refuses on its failure keeps the self-test's output in a file
  under `target/` and prints the lines that name the missing arm. The verdict alone is a "trust me"
  about the gate's own grammar, and it cannot be reproduced from a shell whose environment and load
  differ from the hook's.
- When a refusal names no arm, the first action is to make the next one name it, not to rerun and
  hope. Two silent refusals cost two reruns of a two-hour gate and left the cause open.
- The same self-tests must clean up their fixtures: `scripts/check_citations.py --self-test` had
  left 19 directories under `target/doctrine-selftest` on every run — 5,494 directories, 87 MB, by
  the same day — a leak no cleanup act governs because the fixtures are not recorded outputs. Every
  fixture a self-test creates is removed when it ends, and the summary line counts what it removed.

## Related

`a-fixture-must-have-the-real-records-shape.md` (a green self-test proves consistency with its
author, not with the tree). Owner: `P4-SYSTEM.14` a42ax, `SEMULITH-P4-0292`; evidence
`target/p4-system-14/a42ax/` (commit.log, selftest.log, children-timing-loaded.log, citations-leak.log).
