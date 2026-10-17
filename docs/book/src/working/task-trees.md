# Task-trees

**Create the owning task-tree leaf before any change.**
`TASK-TREE-OWNERSHIP` enforces ownership on every commit.

## What a leaf is

A leaf is one signoff-quality slice, finished, verified and committed together.
Its `docs/tasks/` tree holds goals/non-goals, acceptance, statuses/frontier,
decisions/questions, verification and commit logs.

Statuses: `proposed` → `pending` → `active`/`in_progress` → `done`.
Mark a stalled leaf `blocked` and name its blocker for the next reader.

## The acceptance checklist

A leaf that lands a code change carries six boxes, three of them **hard-gated** by
`TASK-ACCEPTANCE`:

| Box | Must contain | Hard-gated |
| --- | --- | --- |
| REPRODUCE / ISSUE | the problem, shown rather than asserted | no |
| **ROOT CAUSE (WHY + WHERE)** | the command run and its real output, naming mechanism and location | **yes** |
| FIX | the change, at the lowest-risk level that works | no |
| **ADDRESSED (verified)** | measured before → after on the symptom | **yes** |
| **NO REGRESSION** | the suite or gate re-run, and its result | **yes** |
| LOCKSTEP | live docs, contracts, and indexes updated in the same commit | no |

Evidence belongs **inside its ticked bullet**: unrelated leaves and tokens elsewhere
cannot supply it. The gate checks presence, not truth; re-run the cited command.

## The pivot rule

Before switching trees, finish/commit the leaf. Handoff-ready allows no modified/
untracked files except its task-tree, even when asked to pivot immediately.

Cleanup follows the same ownership and commit rule. Its latest record is
overwritten; censuses and retained-input checks stay in the recurring tree.
Diagnostic evidence and dependency inputs are retained.

{{#include ../../../ARTIFACT_CLEANUP.md:latest}}

## Orientation and the selected next action

`KNOWLEDGE_MAP.md` lists task files; open/closed indexes below own status.
`MEMORY.md` selects the next action. Source-pinned checks cover33 tasks,
59 decisions and29 lesson cards. Fresh current replay:

```sh
python3 scripts/qualify_orientation_indexes.py --working-code --require-clean --output target/live-containment/orientation-verified/source
```

D74/D75 fixed:22/0. Map failures refuse2, drift1; decision listings require real
links outside comments/fences. Unavailable reads refuse2; knowledge links are
independently checked. Scaffold retains all three repairs. Historical default17/11,
`--extended`21/14; finite controls.

The term index scans raw SUMMARY chapters/glossary/acronyms without expanding
includes. D73 read/write/launch refusals are fixed:

```sh
python3 scripts/qualify_book_index.py --working-code --require-clean --output target/live-containment/orientation-verified/index
```

### Decision navigation and the record it opens

Indexes route questions; records retain receipts/corrections. D55 fixes UART:
147+13 becomes151+9, total160 unchanged. D51 separates files from active work.
Authorized pooled107 files;108 breaches. Health64 is advisory; byte/part caps stay
fixed. Full classifications/derivations remain in the records:

```sh
cat docs/decisions/INDEX.md
cat docs/decisions/decision_task-tree-family-count-rederivation.md
cat docs/decisions/decision_profiles-family-five-units.md
cat docs/decisions/decision_task-family-six-activity-count.md
```

### Capacity evidence must be readable

Run 94 controls:

```sh
bash scripts/check_readme_routes.sh
bash scripts/check_readme_routes.sh --self-test
```

D52–57 validate NUL totals/parts, metrics, links, hints and README/registry reads.
Unavailable/diagnostic reads refuse2; breaches fail1; health is advisory.
Empty families/date-policy no-match remain valid; checked derived mirrors exempt.
Registry: UTF-8, nine tab fields, unique relative paths, limits0..9223372036854775807.
`00064` becomes64; `-1` refuses2. Sync retains the guards. D65 rejects missing/
ambiguous includes before expansion. Historical counts remain in retained book
source; finite checks grant neither atomic measurements nor capacity authority.
Graph/adoption remain open. Replay (fresh output):

```sh
python3 scripts/collect_containment_graph.py --revision 28920c6 \
  --output target/live-containment/graph-census/replay
```

## Local containment contract

Contract and frontier:

```sh
cat LIVE_DOCUMENT_SIZE_CONTAINMENT.md
cat docs/tasks/artifacts/live-containment/inventory-contract.md
```

{{#include ../../../../LIVE_DOCUMENT_SIZE_CONTAINMENT.md}}

## Every lane of the plan, and who owns it

Open trees, included live from `docs/TASK_TREE.md`:

{{#include ../../../TASK_TREE.md:trees}}

Closed rows move verbatim to `docs/TASK_TREE_CLOSED.md`, included below.
FRONTIER-SYNC requires one row per tree, in the index matching its status:

{{#include ../../../TASK_TREE_CLOSED.md:closed}}

Milestones quote `docs/EVIDENCE_AND_GATES.md`; leaves cite roadmap/card/rule/catalog
sources. Assess the work against those requirements.

The plan is the oracle; a citation is weaker than a test. No mechanical check
proves a tree still matches the roadmap.

## Keeping verification receipts bounded

Whole completed entries move to authenticated shards. Remove the new receipt/
footer; concatenate live prefix and archived suffix to restore exact bytes/order.
Earlier rows/seals, the48KiB ceiling and current worked examples stay fixed.
Complete c22a/c26a/c28a/c29b1/a42l1 receipts and source inverses are retained:

```sh
cat docs/tasks/artifacts/live-containment/include-source-integration.md
```

### Read task history

From the root, read live records with `cat docs/tasks/<TREE>.md`. Sealed
parts1–12 use the checked reader; choose the part, for example archive9:

```sh
python3 scripts/task_history_archive.py --read docs/tasks/archive/P4-SYSTEM-9.md
```

Ordinary P4 parts/receipts stay native. Two containment archives retain whole
closed units and LC0027's checklist; original headings link there:

```sh
cat docs/tasks/archive/P4-SYSTEM-13.md
cat docs/tasks/archive/P4-SYSTEM-14.md
cat docs/tasks/archive/P4-SYSTEM-15.md
cat docs/tasks/archive/P4-SYSTEM-16.md
cat docs/tasks/archive/P4-SYSTEM-17.md
cat docs/tasks/archive/P4-SYSTEM-18.md
cat docs/tasks/archive/P4-SYSTEM-19.md
cat docs/tasks/archive/LIVE-CONTAINMENT.md
cat docs/tasks/archive/LIVE-CONTAINMENT-readers.md
cat docs/tasks/archive/P4-SYSTEM-book-c30b.md
cat docs/tasks/archive/P4-SYSTEM-reference-c29e.md
cat docs/task-history/README.md
```

mdBook rewrites external Markdown links to absent HTML files. The post-include
resolver supplies record routes while preserving labels/examples/canonical files.

The publishing guard compares all HEAD archive Markdown and navigation files
with both staged and working bytes and Git modes:

```sh
python3 scripts/task_history_preservation.py
python3 scripts/probe_task_history_preservation.py
```

Preservation exits0, changes1, unavailable evidence2. Git/read/unsafe/malformed
failures refuse.43 controls run normally and with `python3 -O`. New files are
allowed; originals stay exact. This does not judge first publication or truth.
Correct in new records. The separate sealed reader owns12 files; future seals
need owned transitions.

Use a new owned output directory to test the full gate:

```sh
python3 scripts/task_archive_gate_probe.py --output target/p4-system-14/a42l2/replay
```

Exit0 means measurement completed; `gate_rc` is the verdict. The real views stay
exact. A42k's altered receipt passed; the publishing guard now rejects it(1).

### Preserve completed task receipts and live development history

Full c29e1/c33c task receipts remain above; archives stay immutable.

### Retain book history while keeping current explanations live

Full c30b/c33d book receipts remain above; current explanations/examples stay live.

### Measure stored bytes, including UTF-8

Measure `len(text.encode("utf-8"))` or the written file's `stat().st_size`,
not character count: `"é"` is one character but two UTF-8 bytes.
Use actual bytes for limits, space and inverses; the full c29d1 receipt remains above.

## Why this shape

After a crash, reset or harness change, the frontier names the next step and
the acceptance evidence lets a successor assess the completed work.

Complete privilege/FP receipts and source inverses remain here:

```sh
cat docs/tasks/artifacts/live-containment/include-source-validator.md
```

**Include validation** checks whole text, ASCII anchors and one-based lines
(`:2`, `::10`, `:2:`, `:2:10`) before expansion. Missing/ambiguous selections fail1;
unsupported/unsafe/unreadable inputs or spaces after # refuse2. Valid books stay
exact. Fences expand; nested paths follow selected included text. Cycles fail;
empty files/regions pass. CRLF becomes LF; bare CR/Unicode separators remain
inside physical lines. This qualifies source integrity, not prose truth.

All seven books validate before links by default. UNIT-BOOKS forces validation
even for scratch configurations, requires an execution witness and preserves
source refusal2. Missing files/anchors and duplicate anchors fail1. From root:

```sh
python3 scripts/probe_book_includes.py
python3 -O scripts/probe_book_includes.py
bash scripts/check_unit_books.sh
make book
```

Replay public/default qualification:

```sh
cat docs/tasks/artifacts/live-containment/include-source-integration.md
```

Count every tracked family member and owned addition, including `docs/book/book.toml`.
The retained integration receipt corrects its earlier Markdown-only omission.
Count, aggregate bytes and per-part bounds are separate checks.

### Preserve older live entries

SHARD-FREEZE preserves complete old DEV/CHANGELOG entries in both views. The
sharder may move whole oldest suffixes, keeping bytes/order. New corrections
precede originals. Staged old-count edits still refuse after worktree restoration;
failed Git reads refuse. Preservation does not establish historical truth.

```sh
bash scripts/check_changelog_shards.sh
python3 scripts/shard_history.py --head DEV_NOTES.md --max-bytes 42000 --dry-run
```

The first checks both views and the staged partition; the second previews a move.


### Executed page-heading navigation

LC0042 pins1226311: seven books/120 pages/1406 headings/589 entries. Independent
Python/DOM readers reconcile full labels/markup, targets, nesting, roles and active
parents. Nonpersistent WebKit executes scripts; strict Swift caches/temp stay on
volume. Four JS/HTTP witnesses, three producer omissions/fallback cause discriminate
normal/O.

```sh
python3 scripts/qualify_book_headings.py --output target/heading-replay
python3 scripts/qualify_book_headings.py --verify-record
python3 -O scripts/qualify_book_headings.py --self-test
```

Fresh captures exit0 when measured; D78 marks both Introduction and Index active.
Removing the fallback
fixes that page but breaks a unit index alias; LC0043 supplies the conditional repair.
`--require-clean` fails1 for this source. Record queries verify the full retained
metadata; nine damaged frames refuse. Replay needs pinned Git sources/producers
and the OS Swift/WebKit tools. Raw DOM/HTTP streams remain generated diagnostics.
Click/scroll/layout, search/resources, full graph/adoption and CPU stay unclaimed.

LC0043's `additional-js` integration selects an explicit chapter before heading
insertion; no direct match preserves the index alias. All120 current contracts
pass; supported main alias and three actual omissions discriminate normal/O.

```sh
python3 scripts/qualify_heading_repair.py --require-clean --output target/heading-fix
```

`--verify-record`/`--self-test` query the retained full source/current matrices;
seven damaged frames refuse. Immutable LC0042 remains one-defect evidence.
D79 remains open: one concurrent print replay lacked Mark; strict refusal held.
LC0044 owns delivery/dependency tracing; passing repeats do not close it.

## Reading sealed history

The query-first terminal retains210 older CH/DEV shards and their manifest
byte-exact in an immutable tracked object. Recent shards/live heads stay native.
This approved transition restored aggregate room when sharding could not.

```sh
python3 scripts/history_archive.py
python3 scripts/history_archive.py --read docs/changelog/shard-0001.md
```

Verify checks all identities; read prints the original. Both work in ordinary/
shallow clones without fetch/extraction. docs/history/archives.json pins source,
counts and content-addressed object; the SHA manifest authenticates every member.
Missing/changed inputs fail the unconditional freeze gate. Restore committed bytes.

The manifests remain one partition; sharding never reuses retired names.
Recheck the original P4/history terminals (222 originals) and six catalogues:

```sh
python3 scripts/qualify_query_consumers.py --working-code --require-clean --output target/query-repair-replay
```

Use a fresh path. All263 observations pass normal/O. Malformed deflate now
gives named refusal1 without stdout or traceback; removing its catch fails
qualification. Three consumer omissions/seven ledger controls still discriminate.
Immutable replay retains D76. Full containment adoption remains open.

### Reading closed P4 task histories

The director approved the12-file P4 seal on2026-10-10. Original paths retain
navigation pages and eight incoming anchors; the active graph stays native.

```sh
python3 scripts/task_history_archive.py
python3 scripts/task_history_archive.py --list
python3 scripts/task_history_archive.py --read docs/tasks/archive/P4-SYSTEM-12.md
python3 scripts/task_history_archive.py --read docs/tasks/archive/P4-SYSTEM-8.md | rg -n 'profile-progress'
bash scripts/check_task_history.sh
```

All12 originals authenticate before output, without Git/network/extraction;
shallow clones carry the object. Bounded metadata/decompression, plain members
and exact navigation refuse damaged/unsafe/excess content. Restore committed bytes.
The [front door](../../../task-history/README.md) gives tar/search/failure help;
`decision_task-history-seal-review.md` owns source/serialization.46 controls stay;
future captures need owned transitions.

### Reading closed qualification records

LC0041's delegated four-record seal retains book-index, graph/query, include/
navigation and orientation captures. Original paths preserve20 heading aliases/
retrieval commands. Current inventory/retention inputs stay native; caps stay fixed.

```sh
python3 scripts/qualification_history_archive.py
python3 scripts/qualification_history_archive.py --list
python3 scripts/qualification_history_archive.py --read docs/tasks/artifacts/live-containment/include-readers.md
python3 scripts/qualification_history_archive.py --read docs/book/src/working/task-trees.md
python3 scripts/qualification_history_preservation.py
python3 scripts/probe_qualification_history.py
```

Five originals retain497850 bytes/modes/Git identities from968bc010: four
records and this chapter's prior source. Archive/navigation authenticate before
output without Git/network/extraction; README is reader-bounded, publishing-frozen.
Tar/shallow clones retrieve originals. First publication verifies source tree/
originals/complete staged wiring; later both views freeze against HEAD. Unavailable
evidence refuses2; reader failure1 emits no original.32 tests run normal/O.
Restore committed bytes after damage/unsafe/excess refusal; correct in new records.
Replay still needs declared sources/producers/tools; Markdown retention promises
neither raw output nor toolchain availability. Graph/adoption/CPU remain open.
See `docs/qualification-history/README.md` for scope, tar and failure handling.

## Repository-volume temporary storage

{{#include ../../../decisions/reference_temporary-allocation-controls.md:controls}}
