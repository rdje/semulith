# Artifact maintenance tools

Bounded cleanup planning and historical procedure review. Part of the routed
`docs/toolbox/` family; `TOOLBOX.md` is its index. All controls use newly owned
on-volume fixtures. Historical receipts retain their original scope.

| Tool | Question | Invocation |
| --- | --- | --- |
| `scripts/artifact_task_history.py` · `scripts/artifact_task_history_preservation.py` · `scripts/probe_artifact_task_history.py` | are the cleanup predecessor/ledger directly readable, exact and safely published? | `python3 scripts/artifact_task_history.py [--read ledger \| --read predecessor] [--generation N]`; publishing accepts one generation per owned rollover and preserves both views and live history;45 tests normal/O in TASK-HISTORY; `python3 scripts/probe_artifact_task_history.py --list-mutations` lists20 omission controls; see `docs/artifact-cleanup-history/README.md` |
| `scripts/artifact_cleanup.py` | cache cohort? | `--help`; book task-trees |
| `scripts/probe_legacy_artifact_cleanup.py` | do the original helper bytes and observed debug/release behavior survive? | `python3 -B scripts/probe_legacy_artifact_cleanup.py`; five tests normal/O; source-pin omission loses one assertion/zero errors. Reader limited to8KiB, no symlink/foreign-volume/nested-Git walk; only fresh owned fixture caches removed. Passive fixture SHA authenticated before replay. |
| `scripts/check_artifact_cleanup.sh` | do planning and historical-source controls still discriminate? | `bash scripts/check_artifact_cleanup.sh --self-test`;128 outcomes: planner26 tests plus10 omissions per mode, legacy5 tests plus1 omission and journal26 tests plus10 omissions per mode; output provenance42 tests plus22 omissions per mode adds46 outcomes; bound Cargo23 tests/ten omissions per mode adds22; strict selection11 tests/five omissions per mode adds12. Default also requires tracked producers and passive fixture; no actual host census or project cleanup in CI. |
| `scripts/artifact_cleanup_journal.py` · `scripts/probe_artifact_cleanup_journal.py` | what observations survive an incomplete attempt? | `python3 -B scripts/artifact_cleanup_journal.py --workdir target/artifact-cleanup/NEW`; readonly inspection, no Git or cache unlink;26 tests normal/O plus10 individually failing omissions,22 outcomes; see shared usage below. |
| `scripts/artifact_output_provenance.py` · `scripts/probe_artifact_output_provenance.py` | which recorded outputs still match their bound producers and supplied current facts? | `python3 -B scripts/probe_artifact_output_provenance.py`;42 tests normal/O plus22 individually failing omissions,46 outcomes. Optional `--cargo-contract` reproduces the public dry-run container/input distinction without deletion. Versioned codec preserves v1 bytes; strict v2 matching binds runner/census sources. Census/observe/merge/publish record one bound build's new or changed-digest outputs and replace the ledger atomically under a non-blocking lock, previous ledger preserved on failure; matching tolerates ctime-only drift (rustc hard-link seeding) and nothing else. `--support-contract`/`--publication-contract` [`--revision REV`] report the interfaces and the current ledger. Strict selection .17 pending. |
| `scripts/artifact_cargo.py` · `scripts/probe_artifact_cargo.py` | do the actual C producers bind public Cargo outputs and join their children? | `python3 -B scripts/probe_artifact_cargo.py`;23 tests normal/O, ten guard omissions per mode,22 outcomes; actual cold copied Cargo build publishes v2 records and preserves a seeded unchanged input. Exact old output roots, bounded pipes/deadline and post-build source/manifest checks; `capture` surrounds the build with the output census and publishes through the recorder; a failed build records nothing and only retires rows whose files it removed; `run` stays bare. |
| `scripts/artifact_cleanup_selection.py` · `scripts/probe_artifact_cleanup_selection.py` | which planned candidates does the published ledger actually own? | `python3 -B scripts/artifact_cleanup_selection.py --select \| --inspect --workdir target/artifact-cleanup/NEW`;11 tests normal/O, five guard omissions per mode,12 outcomes. Re-censuses the plan, intersects its candidates with strict captured authority and exclusively publishes `selection.json` beside the plan; cache-named inputs stay unrecorded. Grants no deletion; .16 binds plan, selection and journal. |

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
{{#include ../../scripts/artifact_cargo.py:usage}}
{{#include ../../scripts/artifact_cleanup_selection.py:usage}}
<!-- ANCHOR_END: workflow -->
