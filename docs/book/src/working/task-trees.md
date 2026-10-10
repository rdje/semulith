# Task-trees

**Nothing changes in this repository without a task-tree leaf that owns the change, created
before the change is made.** It is the binding rule, and `TASK-TREE-OWNERSHIP` enforces it on
every commit.

## What a leaf is

The smallest unit that can be finished, verified, and committed as one signoff-quality slice.
A tree file under `docs/tasks/` carries the goal, the non-goals, the acceptance criteria, the
leaves with their statuses, the current frontier, the decisions, the open questions, the
verification log, and the commit log.

Statuses run `proposed` → `pending` → `active`/`in_progress` → `done`. A stalled leaf is marked
`blocked` with the blocker named, never left `active` — the difference is what a reader six
weeks later needs.

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

P4.13 c26a applies the same discipline to the task tree itself. At 123,960 bytes,
the live tree had 7,112 bytes of room under its fixed 131,072-byte part ceiling.
Six completed spans totaled 81,532 bytes; archive 8 already held 59,436, so those
payloads could not fit there. [Archive 9](../../../tasks/archive/P4-SYSTEM-9.md)
retains all six payloads in source order with individual byte lengths and SHA256
markers, including older log rows in their original context. It is 83,418 bytes
with wrappers; the live partition is 45,205 bytes before the new receipt.

The verification extracts each marked payload, removes only new live routing,
ownership and receipt text, and reconstructs the committed source from 5eaef2a:
123,960 bytes, SHA256
`efd367b86309c45a53ddf736352135e18ea56171f1669d43c43941626c7fb4ac`.
Earlier archive parts and all retained source segments are byte-exact. The
frontier, census and next action stay live; feature examples remain in their
book chapters. Neither the task-family nor per-part cap grows, and this move
adds no CPU-contract credit.

## Why this shape

A session can be lost at any moment: a crash, a context reset, a change of tool, a change of
model. The tree is the layer that makes that survivable — its frontier row *is* the next step,
and the acceptance checklist is why a successor can trust the previous step without repeating
it.
