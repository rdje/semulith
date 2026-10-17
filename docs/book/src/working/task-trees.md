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

The evidence must sit **inside the ticked box's own bullet**. That is not a formatting
preference: scoping it per-box closes two measured leakage paths — a co-staged unrelated leaf
supplying the signature, and a token matched anywhere else in the file.

> **Stated limit.** The gate proves a box was ticked and that tool-shaped output sits in it. It
> cannot prove the output is true. A tick is presence; the un-fakeable leg is re-running the
> cited command.

## The pivot rule

Do not pivot to a different tree while the repository is dirty. Handoff-ready means clean: no
modified or untracked work except the task-tree file itself. Finish the leaf, get clean, then
switch — even when asked to switch immediately.

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

D74/D75 fixed:22 observations/0 wrong verdicts. Map input/generator/comparison
failures refuse2; drift fails1. Decision listings require table links outside
comments/fences. Unavailable reads refuse2. Knowledge links are independently
checked. Scaffold sync retains all three repairs. Historical default17/11;
`--extended` 21/14. These are finite controls.

The term index scans raw SUMMARY chapters and glossary terms/acronyms;
includes stay unexpanded. D73 read/write/launch refusals are fixed:

```sh
python3 scripts/qualify_book_index.py --working-code --require-clean --output target/live-containment/orientation-verified/index
```

### Decision navigation and the record it opens

Indexes keep dated questions; records retain receipts/corrections.
D55 corrects the partial UART subtotal: 147 + 13 becomes 151 + 9; total 160 stands.
D51 distinguishes files from active work. A separate review authorizes107 pooled
files;108 breaches. Health64 remains warning debt; byte/part caps stay fixed.
Full classifications and derivations remain in the records:

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

A milestone quotes its acceptance gate from `docs/EVIDENCE_AND_GATES.md`.
Each leaf cites its roadmap section, task card, rule ID or catalog entry;
readers assess the leaf against that source.

The plan is the oracle; a citation is weaker than a test. No mechanical check
proves a tree still matches the roadmap.

## Keeping verification receipts bounded

Completed development notes move as whole entries into authenticated history
shards. Remove the new live receipt/footer and concatenate the retained live
prefix and archived suffix to reconstruct the original bytes and entry order.
The manifest gains rows; earlier rows and sealed history remain immutable.
The 48 KiB ceiling stays fixed; current worked feature examples stay in the book.
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

Ordinary P4 parts and named receipts remain native Markdown. Two containment
archives retain whole closed units, including LC0027's checklist. Original task
headings link to them:

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

These instructions stay in the book because mdBook rewrites external Markdown
links to HTML files that it does not generate. The build resolver runs after
includes, preserving labels, examples and canonical source files.

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

**Include source validation.** Whole text, ASCII anchors and one-based
line selections (`:2`, `::10`, `:2:`, `:2:10`) are checked before expansion.
Missing/ambiguous selections fail1; unsupported/unsafe/unreadable inputs refuse2.
Valid input returns the same book. Spaces after # refuse2. Fences expand;
nested includes follow selected text relative to the included file. Cycles fail;
empty files and empty named regions are valid. CRLF becomes LF; bare CR/Unicode
separators stay inside physical lines. This checks source integrity, not prose truth.

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

Measure every tracked family member, including `docs/book/book.toml`, plus
explicitly owned untracked additions. A Markdown-only census once omitted that
configuration and overstated room. Count, aggregate bytes and per-part bounds
are separate checks. The retained integration record owns the corrected receipt.

### Preserve older live entries

SHARD-FREEZE also compares complete old DEV/CHANGELOG entries in the staged and
working views. Whole oldest suffixes may move through the published sharder;
bytes/order stay exact. New corrections precede old records. Editing an older
count refuses even if the working file is restored after staging. Failed Git
reads refuse; preservation does not prove old claims true.

```sh
bash scripts/check_changelog_shards.sh
python3 scripts/shard_history.py --head DEV_NOTES.md --max-bytes 42000 --dry-run
```

The first checks both views and the staged partition; the second previews a move.


### Executed page-heading navigation

LC0042 pins source1226311: seven books/120 HTML pages,1406 heading rows and589
navigation entries. Independent Python/DOM readers reconcile labels, full inline
markup, targets, nesting, page roles and active-parent bindings. Nonpersistent
WebKit executes the generated scripts; Swift compiles with warnings as errors,
module caches/temp stay on volume. Four JS/HTTP witnesses, three real producer
omissions and an index-fallback cause control discriminate normal/O.

```sh
python3 scripts/qualify_book_headings.py --output target/heading-replay
python3 scripts/qualify_book_headings.py --verify-record
python3 -O scripts/qualify_book_headings.py --self-test
```

Use a fresh output. Capture exits0 when measured; source D78 leaves one wrong
contract: Index marks both Introduction and Index active. Removing the fallback
fixes that page but breaks a unit index alias; LC0043 owns the conditional repair.
`--require-clean` fails1 for this source. Record queries verify the full retained
metadata; nine damaged frames refuse. Replay needs pinned Git sources/producers
and the OS Swift/WebKit tools. Raw DOM/HTTP streams remain generated diagnostics.
Click/scroll/layout, search/resources, full graph/adoption and CPU stay unclaimed.

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

Before output, all12 originals authenticate without Git/network/extraction;
shallow clones carry the object. Bounded metadata/decompression, plain members
and exact navigation fail closed on damaged/unsafe/excess content. Restore
committed bytes. The [front door](../../../task-history/README.md) gives
tar/search/failure instructions; `decision_task-history-seal-review.md` retains
the source manifest/serialization. Original46 controls stay; future captures
need owned transitions.

### Reading closed qualification records

LC0041 applies the director's standing archive delegation to four completed
qualification records: book-index consumer, graph/query census, include/navigation
readers and orientation indexes. Their original paths preserve all20 heading
aliases and give retrieval commands. The current inventory contract and live
retention inputs remain native. Existing capacities stay fixed.

```sh
python3 scripts/qualification_history_archive.py
python3 scripts/qualification_history_archive.py --list
python3 scripts/qualification_history_archive.py --read docs/tasks/artifacts/live-containment/include-readers.md
python3 scripts/qualification_history_archive.py --read docs/book/src/working/task-trees.md
python3 scripts/qualification_history_preservation.py
python3 scripts/probe_qualification_history.py
```

Five originals retain497850 bytes/modes/Git identities from968bc010: four
records plus this chapter's whole prior unexpanded source; its successor stays
live. Archive data/navigation authenticate before output, without Git/network/
extraction. README content is bounded by the reader and frozen by publishing.
Tar retrieves originals; shallow clones carry the object. First
publication checks the source tree, originals and complete staged data/wiring.
Later both views freeze against HEAD. Unavailable evidence refuses2; the reader
refuses1 without original output.32 tests run normal/O. Damaged/unsafe/excess
content fails closed; restore committed bytes. Corrections use new records.
Historical replay still needs its declared sources/producers/tools; retained
Markdown adds no raw-output or toolchain promise. Graph/adoption/CPU stay open.
See `docs/qualification-history/README.md` for scope, tar and failure handling.

## Repository-volume temporary storage

{{#include ../../../decisions/reference_temporary-allocation-controls.md:controls}}
