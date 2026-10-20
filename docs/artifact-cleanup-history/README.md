# Retained artifact-cleanup ledger

This finite terminal preserves the complete `ARTIFACT-CLEANUP` predecessor at
`839e9313d79105a079ac73e2259011c761c2d5ce` and its exact completed checklist/log suffix.
Every task node and current frontier stays in `docs/tasks/ARTIFACT-CLEANUP.md`.

Both originals remain directly readable as Markdown:

- [Complete predecessor](predecessor-b8c8f29c713329815ec51c72c0ddaa15a3cee4350ac474801218b760e4a42471.md): 76,937 bytes / 942 lines.
- [Completed ledger](ledger-2e841602eb6f3766f0c7ae8e841d4fa4d19b874ccf2e361fa53c287f965b6055.md): 38,046 bytes / 384 lines.

The ledger is also a suffix of the predecessor. These overlapping products
preserve different read paths; their byte totals are not disjoint source totals.
Unretained source bytes: zero. Neither snapshot describes mutable current state.

<!-- ANCHOR: usage -->
### Read the retained cleanup ledger

The current task graph remains in `docs/tasks/ARTIFACT-CLEANUP.md`. The completed
ledger and whole predecessor remain ordinary Markdown. Authenticate both before
reading or searching, from the repository root:

```sh
python3 scripts/artifact_task_history.py
python3 scripts/artifact_task_history.py --read ledger
python3 scripts/artifact_task_history.py --read predecessor
python3 scripts/artifact_task_history.py --read ledger | rg 'SEMULITH-AC-0071'
```

The reader checks the entire terminal and current pointer/graph before output.
It needs no Git, network, extraction, or generated cache. Each original can also
be opened directly through the retention page's links or read with `cat`.
<!-- ANCHOR_END: usage -->

Descriptor `object` locators are relative to the repository root. The separate
fixture-record `path` field keeps its record-relative contract. The retention
reader authenticates these objects through its own closed schema and digests.

Retention is project-owned and indefinite while these records are promised.
Keep the tracked files with ordinary and shallow clones. Corruption or missing
data refuses; restore the exact committed bytes, never replace a digest to bless
changed history. This four-file terminal is immutable and accepts no appends.
A future rollover needs its own owned finite transition. The earlier P4,
qualification and changelog terminals and all their bounds stay unchanged.

Authority: `ARTIFACT-CLEANUP.19`, the project-owned
`LIVE_DOCUMENT_SIZE_CONTAINMENT.md` task-ledger transition contract. The source
suffix begins at byte 38891, the first acceptance checklist.
Only completed checklist/log narrative moves; goals, nodes, children, decisions,
questions, blockers and the selected current frontier remain in the live tree.
New ledger text has independent raw-byte bounds, including embedded markup:
16 KiB health / 32 KiB ceiling; acceptance16, verification8, commits4 and
changelog4 KiB section ceilings. Warn at75% health; ordinary growth stops at90%
health until an owned rollover. This does not claim full containment adoption.
