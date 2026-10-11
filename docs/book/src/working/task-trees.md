# Task-trees

**Nothing changes in this repository without a task-tree leaf that owns the change, created
before the change is made.** It is the binding rule, and `TASK-TREE-OWNERSHIP` enforces it on
every commit.

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

`KNOWLEDGE_MAP.md` lists every task-tree file, including completed and proposed
trees. Its generated inventory is not an active-work roster. The status-aware
open and closed indexes below own that distinction. `MEMORY.md` selects one
next action; measurements and completed receipts stay in their owning trees.
Read the current revision from Git:

```sh
git log -1 --format='%H %s'
cat MEMORY.md
cat KNOWLEDGE_MAP.md
```

### Decision navigation and the record it opens

The decision index is a bounded navigation view. Dated topic labels and reader
questions point to the complete records, which own the rationale and historical
measurements. Shortening duplicate summaries preserves those records and links;
it does not authorize changing a limit. For example, read the index and the
per-tree size ruling:

```sh
cat docs/decisions/INDEX.md
cat docs/decisions/decision_task-tree-per-part-growth.md
```

### Capacity evidence must be readable

Run the route guard and its failure controls:

```sh
bash scripts/check_readme_routes.sh
bash scripts/check_readme_routes.sh --self-test
```

D52–54 fixes check file counts, README links, emitted hints and provider reads.
A successful, stderr-free NUL inventory supplies validated totals and part sizes.
Unavailable inputs refuse2 without green; a measured ceiling breach returns1.
An empty tracked family is valid; health warnings do not block and checked
regeneration-gated mirrors keep their exemption. README date and literal policy
counts accept legitimate no-match1, but refuse failed or diagnostic reads.
Scaffold sync retains the local README guard and helper; review replacements
explicitly. Working-file measurements over tracked membership are not atomic
snapshots or authority to raise limits. Full neutral containment adoption remains
LIVE-CONTAINMENT.4.

## Local containment contract

The following is the complete locally owned contract. Its adoption note separates
this exact import from the inventory, checker and migration work still owned by
LIVE-CONTAINMENT.4. Existing controls and ceilings remain in force.

```sh
cat LIVE_DOCUMENT_SIZE_CONTAINMENT.md
```

{{#include ../../../../LIVE_DOCUMENT_SIZE_CONTAINMENT.md}}

## Every lane of the plan, and who owns it

Included live from `docs/TASK_TREE.md`, so this map cannot drift from the index the repository
maintains — the OPEN trees:

{{#include ../../../TASK_TREE.md:trees}}

A tree that completes leaves the index and keeps its row, verbatim, in the closed-tree register
(`docs/TASK_TREE_CLOSED.md`, included live too); FRONTIER-SYNC gates both files, so every tree
has exactly one row, by its status:

{{#include ../../../TASK_TREE_CLOSED.md:closed}}

A milestone tree's **acceptance criteria are its gate** — quoted from
`docs/EVIDENCE_AND_GATES.md`, not restated, because a restated gate is a second owner. Its
leaves each cite the roadmap section, task card, rule ID or catalog entry they derive from, so
a reader refutes a leaf by reading one paragraph rather than by trusting the tree.

⚠️ That citation is the strongest control available for a prose-to-structure conversion, and it
is weaker than a test. The honest statement is: the plan is the oracle for these trees, and
nothing mechanically proves a tree still matches it.

## Keeping verification receipts bounded

Completed development notes move as whole entries into authenticated history
shards; their contents are retained, not summarized away. P4.13 c22a moved seven
older entries from a 47,462-byte live head, leaving thirteen entries / 31,228 bytes
before the new receipt. Removing only that new receipt and navigation footer,
then concatenating the live prefix and archived suffix, reconstructs the original
bytes and entry order exactly. The owning task records source/suffix SHA256 and
lengths. The frozen manifest gains one row; earlier rows and sealed history remain
unchanged. The 48 KiB live ceiling stays fixed, and the book retains the worked
feature examples independently of the session notes.

The complete P4.13 c26a/c28a book receipts remain in ordinary archive14;
read them through the commands below. Current partition rules remain above.

The whole P4.13 c29b1 append-history receipt is retained in
[archive 13](#read-task-history).

P4.14 a42l1 retains four completed workflow designs and three whole book
receipt spans in ordinary part19. Complete source inverses preserve each byte;
active a42/a42l and current explanations stay live. Read the records below.

### Read task history

From the root, read live records with `cat docs/tasks/<TREE>.md`. Sealed
parts1–12 use the checked reader; choose the part, for example archive9:

```sh
python3 scripts/task_history_archive.py --read docs/tasks/archive/P4-SYSTEM-9.md
```

Ordinary part13 and named book receipts remain directly readable Markdown:

```sh
cat docs/tasks/archive/P4-SYSTEM-13.md
cat docs/tasks/archive/P4-SYSTEM-14.md
cat docs/tasks/archive/P4-SYSTEM-15.md
cat docs/tasks/archive/P4-SYSTEM-16.md
cat docs/tasks/archive/P4-SYSTEM-17.md
cat docs/tasks/archive/P4-SYSTEM-18.md
cat docs/tasks/archive/P4-SYSTEM-19.md
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

The complete c29e1/c33c task and DEV partition receipts are retained in
ordinary part19. They include source identities and all inverse/control
measurements. Earlier archives remain immutable.

### Retain book history while keeping current explanations live

Ordinary part19 retains the complete c30b/c33d book and DEV partition
receipts, including source identities and measured inverses. Current
feature explanations and examples remain in their chapters.

### Measure stored bytes, including UTF-8

Size claims use encoded file bytes. At the c29d1 diagnostic, the index generator
reported 23,612 "bytes" for a file containing 24,064 bytes: it had counted Python
characters, which omit UTF-8's extra bytes for non-ASCII text. The generator now
reports the written file's `stat().st_size`. Its output bytes and 40 indexed terms
are unchanged, and `--check` still succeeds quietly. The byte-count assertion
fails on the old message and passes after the reporting-only correction.
Containment and inverse proofs measure actual bytes throughout; a character
count cannot establish available space under a byte cap.


## Why this shape

A session can be lost at any moment: a crash, a context reset, a change of tool, a change of
model. The tree is the layer that makes that survivable — its frontier row *is* the next step,
and the acceptance checklist is why a successor can trust the previous step without repeating
it.

A later privilege-timeline containment applies the same complete-source inverse
at one span. Its map in `docs/tasks/archive/P4-SYSTEM-book-c32b0.md` records
source `21a997f`, 14,486 bytes and SHA-256
`bc97a1b69d515c5a9b0af2dd9022084bac7c08e8dc8955720e2901756595382f`.
Check the retained chapter's proposed digest, replace the exact replacement at
the recorded byte offset with the marked original 8,436-byte payload, then
verify the entire restored source against that commit. Corruption, a missing
marker or an omitted payload must refuse. Current features and CSR examples
stay in the book; historical checkpoint counts stay in the immutable archive.

The FP timeline provides another full-source inverse:
`docs/tasks/archive/P4-SYSTEM-book-c33b0.md` authenticates source `07e14ae`,
24,259 bytes, SHA-256
`ef2fd2d2d8395dbbf848d6b6a37b914c3b6d4499b60812d98db507edd8ad0db1`.
Verify proposed chapter bytes/SHA, replace the mapped span with the marked
10,576-byte original introduction, then verify the entire restored chapter
against Git. Its semantic code fence and current feature/witness sections
remain in the book. Damaged payloads or missing markers cannot receive credit.

Containment measurements count every tracked family member, including
`docs/book/book.toml`. A Markdown-only scratch census omitted its309bytes and
reported extra room that the production routing guard did not grant. At the
measured revision the full51-member book was523133bytes, leaving1155 under
524288. Use `git ls-files` plus explicitly owned untracked additions for the
same-volume byte census; keep file count, aggregate bytes and per-part caps
as separate checks. The corrected planning receipt and inverse retain the
measurement's source and scope.

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

The live and archived manifests form one logical partition. Moving a row into the
archive keeps its digest and predecessor identity; it does not delete history. The
gate checks heading uniqueness across both live heads and the complete archive, and
the sharder includes retired filenames when allocating its next number. Thirty-one
positive/negative controls guard these checks. This finite terminal has one object,
a bounded descriptor and a retrieval front door; a later seal needs its own verified
capture and transition. Full containment-doctrine adoption remains owned by
LIVE-CONTAINMENT.4.


### Reading closed P4 task histories

The director approved the12-file task-history seal on2026-10-10. The base P4
archive and parts2–12 retain every original byte in a tracked375,029-byte object,
with12 navigation pages at their former paths and eight incoming section anchors.
The active18-node graph and current evidence leaf remain directly readable.
Historical links lead to a navigation page that gives the original identity and
read command; the page discloses that the historical body is in the archive.

```sh
python3 scripts/task_history_archive.py
python3 scripts/task_history_archive.py --list
python3 scripts/task_history_archive.py --read docs/tasks/archive/P4-SYSTEM-12.md
python3 scripts/task_history_archive.py --read docs/tasks/archive/P4-SYSTEM-8.md | rg -n 'profile-progress'
bash scripts/check_task_history.sh
```

Verification authenticates the whole terminal before printing any requested
original. All12 originals (1,144,703bytes/15,055lines) and the original manifest
are retained. The reader uses Python's standard library without Git, network or
extraction; ordinary/shallow clones carry the tracked object. Ordinary tar also
retrieves every original exactly. The descriptor is immutable and independently
pinned, with bounded metadata, decompression and regular members. Missing,
corrupt, extra, unsafe or oversized content and changed navigation fail closed.
Restore the exact committed bytes on failure.46 permanent controls run under
TASK-HISTORY, including relocated no-Git retrieval and malicious archive cases.

The [terminal front door](../../../task-history/README.md) gives tar commands,
search, retention and failure handling. The exact manifest and reproducible
serialization remain in `docs/decisions/decision_task-history-seal-review.md`.
The twelve navigation pages total7,040bytes; this transition releases1,137,663B
from the existing task-family aggregate. Existing incoming link targets
remain unchanged, and no earlier ceiling changes. The three-file terminal has a fixed387,317B bound derived
from its immutable object plus bounded metadata. Nothing appends to it; a future
capture needs its own owned, verified transition. Full containment adoption
remains open under LIVE-CONTAINMENT.4. Archival grants no CPU acceptance credit.

## Repository-volume temporary storage

{{#include ../../../decisions/reference_temporary-allocation-controls.md:controls}}
