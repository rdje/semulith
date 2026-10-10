# Sealed P4 task history

This finite terminal retains the 12 closed P4 task histories captured at
`47cb4365b6b0ec38b76ac7863e3ad39eb82e3b1c`: the base archive and parts 2–12,
through completed P4.13. The director approved the browsing change on 2026-10-10.
The active tree remains at `docs/tasks/P4-SYSTEM.md`. Former historical paths
remain as navigation pages, including the eight incoming section anchors.

From the repository root:

```sh
python3 scripts/task_history_archive.py
python3 scripts/task_history_archive.py --list
python3 scripts/task_history_archive.py --read docs/tasks/archive/P4-SYSTEM-12.md
bash scripts/check_task_history.sh
```

The reader authenticates the entire terminal and all navigation pages before
writing any original bytes to stdout. It uses only Python's standard library,
without Git, network access or extraction to disk. Ordinary and shallow clones
retain the tracked object. A corrupt/missing object, descriptor or navigation
page fails closed. Restore the exact committed bytes; changing a digest to
bless changed history is refused by the immutable descriptor pin and gate.

`descriptor.json` binds the capture, approval, counts, object and manifest
identities, and preserved anchors. The 375,029-byte gzip/USTAR object under
`sealed/` contains 1,144,703 original bytes / 15,055 lines in 12 files, plus
the original 2,418-byte manifest. Its manifest member keeps the reviewed logical
name `docs/history/task-history-manifest.json`; it is not a live file or a
dependency on the separate changelog terminal.

Ordinary tar can retrieve originals independently of the checked reader:

```sh
tar -xOf docs/task-history/sealed/892f5c98fb8567392fea2b0a615baab3bd2aa4a38768517e0f3c7b418887242d.tar.gz docs/tasks/archive/P4-SYSTEM-12.md
```

The checked reader adds whole-terminal, member identity and navigation checks.
For a filename search use `--list`; for text search pipe an authenticated
`--read` to `rg`. Archived cross-links name other logical originals; retrieve
those with the same command. Existing Markdown links lead to the navigation
page, where the read command and original identity are visible.

Retention is project-owned and indefinite while these histories are promised.
This is one immutable object, one descriptor and this bounded front door.
Nothing appends here. A future seal needs its own task-owned, verified transition;
the existing changelog terminal and all earlier ceilings remain unchanged.
The capture manifest and reproducible serialization recipe are recorded in
`docs/decisions/decision_task-history-seal-review.md`. Full live-document
containment adoption remains owned by `LIVE-CONTAINMENT.4`.
