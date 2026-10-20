# Artifact maintenance tools

Bounded cleanup planning and historical procedure review. Part of the routed
`docs/toolbox/` family; `TOOLBOX.md` is its index. All controls use newly owned
on-volume fixtures. Historical receipts retain their original scope.

| Tool | Question | Invocation |
| --- | --- | --- |
| `scripts/artifact_task_history.py` · `scripts/artifact_task_history_preservation.py` · `scripts/probe_artifact_task_history.py` | are the cleanup predecessor/ledger directly readable, exact and safely published? | `python3 scripts/artifact_task_history.py [--read ledger \| --read predecessor]`; publishing preserves both views and live history;40 tests normal/O in TASK-HISTORY; `python3 scripts/probe_artifact_task_history.py --list-mutations` lists18 omission controls; see `docs/artifact-cleanup-history/README.md` |
| `scripts/artifact_cleanup.py` | cache cohort? | `--help`; book task-trees |
| `scripts/probe_legacy_artifact_cleanup.py` | do the original helper bytes and observed debug/release behavior survive? | `python3 -B scripts/probe_legacy_artifact_cleanup.py`; five tests normal/O; source-pin omission loses one assertion/zero errors. Reader limited to8KiB, no symlink/foreign-volume/nested-Git walk; only fresh owned fixture caches removed. Passive fixture SHA authenticated before replay. |
| `scripts/check_artifact_cleanup.sh` | do planning and historical-source controls still discriminate? | `bash scripts/check_artifact_cleanup.sh --self-test`;76 outcomes: planner26 tests plus10 omissions per mode, legacy5 tests plus1 omission and journal26 tests plus10 omissions per mode; output provenance25 tests plus13 omissions per mode adds28 outcomes. Default also requires tracked producers and passive fixture; no actual host census or project cleanup in CI. |
| `scripts/artifact_cleanup_journal.py` · `scripts/probe_artifact_cleanup_journal.py` | what observations survive an incomplete attempt? | `python3 -B scripts/artifact_cleanup_journal.py --workdir target/artifact-cleanup/NEW`; readonly inspection, no Git or cache unlink;26 tests normal/O plus10 individually failing omissions,22 outcomes; see shared usage below. |
| `scripts/artifact_output_provenance.py` · `scripts/probe_artifact_output_provenance.py` | which recorded outputs still match their bound producers and supplied current facts? | `python3 -B scripts/probe_artifact_output_provenance.py`;25 tests normal/O plus13 individually failing omissions,28 outcomes. Optional `--cargo-contract` reproduces the public dry-run container/input distinction without deletion. Read-only codec/anchored source matching; producer/planner integration pending .17. |

The passive input is `scripts/fixtures/artifact_cleanup_0067.py.txt`, the
byte-exact5,815B source from the AC0067 event. The release reproduction demonstrates
the old missing-receipt defect; it does not rerun that historical event or grant
execution provenance to the later tool. Original source and new behavior remain
separately identified. Supported deletion is pending `ARTIFACT-CLEANUP.14`.

## Cleanup and attempt inspection

<!-- ANCHOR: workflow -->
Cleanup follows ownership/commit rules: overwrite its latest record; keep
censuses/retained-input checks in its tree and retain evidence/dependencies.

{{#include ../ARTIFACT_CLEANUP.md:latest}}

{{#include ../../scripts/artifact_cleanup.py:usage}}

{{#include ../../scripts/artifact_cleanup_journal.py:usage}}

{{#include ../../scripts/artifact_output_provenance.py:usage}}
<!-- ANCHOR_END: workflow -->
