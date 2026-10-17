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

D52–57 check NUL inventory totals/parts, metrics, links, hints and README/registry reads.
Read failures/diagnostics return 2; breaches return 1; health is advisory.
Empty families and date/policy no-match (1) are valid; checked derived mirrors
stay exempt. Sync retains that guard/helper.

Registry: UTF-8, nine tab-separated fields, unique normalized relative paths,
limits 0..9223372036854775807. `00064` becomes 64; `-1` returns 2.
Validated rows supply routes/caps/count. D56's seven unchecked
consumers are removed; three reader faults return 2 normal/O. D57's five
malformed fixtures change 0→2. All 26 new controls fail under 17 omissions.
Checks are finite; measurements are not atomic or capacity authority.
At `cad73f3`:54 candidates;49 includes match93 chapters.
D65 repair: UNIT-BOOKS rejects missing/ambiguous includes before expansion.
Graph/full adoption open. Replay (fresh output):

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

⚠️ That citation is the strongest control available for a prose-to-structure conversion, and it
is weaker than a test. The honest statement is: the plan is the oracle for these trees, and
nothing mechanically proves a tree still matches it.

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

The first exits0 for exact preservation,1 for changed records,2 when it cannot
judge. Failed Git reads, malformed responses, unsafe paths and unavailable
inputs refuse. The second runs43 controls; `python3 -O` runs the same controls
with optimization. New files may be added. This checks preservation, not first
publication or historical truth; corrections belong in new records. The sealed
reader still owns only its original12 files; a future seal needs its own transition.

Use a new owned output directory to test the full gate:

```sh
python3 scripts/task_archive_gate_probe.py --output target/p4-system-14/a42l2/replay
```

Exit0 marks a completed measurement; `gate_rc` is the gate verdict.
The real index/worktree must stay exact. A42k's altered receipt passed
before the publishing guard. A42l2's same staged edit is rejected (`gate_rc=1`).

### Preserve completed task receipts and live development history

Read the complete c29e1/c33c receipts in the retained record above.
Earlier archives remain immutable.

### Retain book history while keeping current explanations live

The retained record preserves the complete c30b/c33d receipt and source route.
Current feature explanations and examples remain in their chapters.

### Measure stored bytes, including UTF-8

Measure `len(text.encode("utf-8"))` or the written file's `stat().st_size`,
not character count: `"é"` is one character but two UTF-8 bytes.
Limits, available-space calculations and inverses use actual bytes.
The retained record above includes the complete c29d1 diagnostic receipt.

## Why this shape

A session can be lost at any moment: a crash, a context reset, a change of tool, a change of
model. The tree is the layer that makes that survivable — its frontier row *is* the next step,
and the acceptance checklist is why a successor can trust the previous step without repeating
it.

The complete privilege/FP timeline-containment receipts and inverse instructions
are retained with the include-validator evidence:

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

## Reading sealed history

Older changelog and development-note shards now have a query-first archive terminal.
The 210 older shards and their manifest retain every byte, but use a tracked immutable
compressed object instead of individual Markdown files. Recent shards and both live
heads remain directly readable. This approved transition restores the live collection's
headroom; sharding alone had left its aggregate at the limit.

```sh
python3 scripts/history_archive.py
python3 scripts/history_archive.py --read docs/changelog/shard-0001.md
```

The first command verifies all identities; the second prints the original shard.
Both work in an ordinary shallow clone without fetching history or extracting files.
The descriptor in docs/history/archives.json names the exact source capture, source
counts and content-addressed object. The archive's SHA manifest authenticates each
member. A missing object, changed descriptor or bad member fails the same unconditional
freeze gate used locally and in CI. Restore the committed bytes when that happens.

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
