# Retained artifact-cleanup ledger

This finite terminal preserves each complete `ARTIFACT-CLEANUP` predecessor and its
exact completed checklist/log suffix, one generation per owned rollover. Every task
node and the current frontier stay in `docs/tasks/ARTIFACT-CLEANUP.md`.

All originals remain directly readable as Markdown:

- Generation 1 (`839e9313d79105a079ac73e2259011c761c2d5ce`, `ARTIFACT-CLEANUP.19`):
  [predecessor](predecessor-b8c8f29c713329815ec51c72c0ddaa15a3cee4350ac474801218b760e4a42471.md) 76,937 bytes / 942 lines;
  [ledger](ledger-2e841602eb6f3766f0c7ae8e841d4fa4d19b874ccf2e361fa53c287f965b6055.md) 38,046 bytes / 384 lines.
- Generation 2 (`b18971eeea61fdcce6f428693916f4f00b145ba6`, `ARTIFACT-CLEANUP.23`):
  [predecessor](predecessor-ec938336682f4bb4443d57838d45d431dc330a1dabd5ad011cd64f7117d04aa4.md) 58,246 bytes / 826 lines;
  [ledger](ledger-db1260a6fa02df38fe81d6368cb4f7ba544e8cc67ac339dd8dbf4509383f9a63.md) 13,433 bytes / 186 lines.

Each ledger is a suffix of its predecessor; from the second generation on it begins
with the previous generation's pointer, so the chain stays navigable. Overlapping
products preserve different read paths; their byte totals are not disjoint source
totals. Unretained source bytes: zero. No snapshot describes mutable current state.

<!-- ANCHOR: usage -->
### Read the retained cleanup ledger

The current task graph remains in `docs/tasks/ARTIFACT-CLEANUP.md`. Every completed
ledger and whole predecessor remain ordinary Markdown. Authenticate the whole chain
before reading or searching, from the repository root:

```sh
python3 scripts/artifact_task_history.py
python3 scripts/artifact_task_history.py --read ledger
python3 scripts/artifact_task_history.py --read predecessor --generation 1
python3 scripts/artifact_task_history.py --read ledger | rg 'SEMULITH-AC-0076'
```

`--read` defaults to the latest generation; `--generation N` selects an earlier one.
The reader checks the entire terminal, the generation chain and the current
pointer/graph before output. It needs no Git, network, extraction or generated cache.
Each original can also be opened through this page's links or read with `cat`.
<!-- ANCHOR_END: usage -->

Descriptor `object` locators are relative to the repository root. The retention
reader authenticates these objects through its own closed schema and digests. A
generation's retained entry re-derives the descriptor it superseded byte-exactly;
that digest is the `predecessor_pointer` of the next generation.

Retention is project-owned and indefinite while these records are promised. Keep
the tracked files with ordinary and shallow clones. Corruption or missing data
refuses; restore the exact committed bytes, never replace a digest to bless changed
history. Published generations are immutable. A rollover adds exactly one
generation through its own owned transition, which the publisher verifies against
HEAD; nothing else may change the terminal.

Authority: `ARTIFACT-CLEANUP.19` (generation 1) and `ARTIFACT-CLEANUP.23`
(generation 2), under the project-owned `LIVE_DOCUMENT_SIZE_CONTAINMENT.md`
task-ledger transition contract. Only completed checklist/log narrative moves;
goals, nodes, children, decisions, questions, blockers and the selected frontier
remain in the live tree. New ledger text has independent raw-byte bounds,
including embedded markup: 16 KiB health / 32 KiB ceiling; acceptance16,
verification8, commits4 and changelog4 KiB section ceilings. Warn at75% health;
ordinary growth stops at90% health until an owned rollover.
