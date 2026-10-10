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

P4.13 c28a repeats the whole-entry proof for development notes. Source `5daa7bb`
holds 23 entries/47,951 bytes, only 1,201 bytes below the fixed 49,152-byte cap.
The published sharder targets 30,000 bytes: sixteen entries remain in 29,706
bytes; seven oldest entries move as an exact 18,245-byte suffix into shard 0225
(18,478 bytes including its wrapper). Remove only the new receipt/navigation
footer and concatenate the retained prefix and archived suffix to reconstruct
the source, SHA256
`6d0ccb9383365685023d20543138f1e47735360257fe1fb9fe9560e91ecb70c3`.
The earlier manifest rows and sealed history stay byte-exact, and no bound grows.
At that checkpoint the next evidence question was the public Sail override's
contained-versus-crossing AMO granule behavior. C28b subsequently qualified it;
the [memory chapter](../plan/p4/contract-memory.md) retains that result and its
wrong-granule control.



P4.13 c29b1 partitions two committed append-history heads from ce3a53b:

| Head | Source bytes/entries | Retained entries/bytes | Moved entries/payload bytes | New shard |
| --- | --- | --- | --- | --- |
| DEV_NOTES.md | 46,505 /24 | 15 /28,705 | 9 /17,800 | 0226 (18,033 bytes) |
| CHANGELOG.md | 56,022 /97 | 59 /39,870 | 38 /16,152 | 0227 (16,389 bytes) |

The published sharder targets30,000 and40,000 bytes respectively. Both dry runs
preserve the heads, manifest and prior history; the12-control self-test passes.
Actual mutations run sequentially, so numbering advances from0226 to0227.
Removing each new receipt/footer and concatenating its retained prefix with the
shard's payload reconstructs its exact original bytes and entry order:

- DEV source SHA256:
  `92b5766fb8f41f3e563647aace6e20893e40bb8c02639e728dd1f841e84ca1f5`.
- CHANGELOG source SHA256:
  `b451f91d5f4ebb1cbb498fd3dc0166b3044c4af09031a8a23537aaaf967feb93`.

The manifest gains only two rows. Its earlier17 rows and the210 sealed shards
remain exact, giving229 logical rows (19live+210sealed). Each new shard names
its source head and is frozen. Live/per-part/family ceilings stay fixed; current
feature examples remain in their own chapters. Code, profile inputs, frozen
contracts and registry bindings were unchanged. The subsequent c29c policy/
source-prose repair and c29d book containment are complete; their receipts
remain accessible through the task tree’s history routes.



### Preserve completed task receipts and live development history

P4.13 c29e1 starts from committed `442a57d`: the live task tree is 124,305
bytes under its fixed 131,072-byte ceiling. Five whole completed spans total
79,234 bytes: c26a–c29e0 designs and acceptance, plus the complete verification,
commit and changelog sections. [Archive 10](../../../tasks/archive/P4-SYSTEM-10.md)
retains every byte in source order, including earlier history routes. It is
81,004 bytes with wrappers. The live partition is 45,649 bytes before its new
receipt; the frontier, open plans, census and decisions remain live.

Extract the five marked payloads, authenticate their lengths and SHA256, replace
only the new routes and remove only the new ownership/receipt text: the complete
source reconstructs to 124,305 bytes, SHA256
`45f985e70054d5d5fc5683dcc637a679e7fc14f2c7526b0830776e09f3ef57e8`.
A corrupt payload, absent marker or omitted payload refuses authentication.
Earlier archives remain immutable.

The same unit uses the published sharder for `DEV_NOTES.md`: its 20 entries /
36,965 bytes partition into 16 retained entries /29,867 bytes and four oldest
entries /7,098 payload bytes. Shard 0228 is 7,331 bytes with its wrapper.
Concatenating the retained prefix and exact suffix reconstructs the source in
order, SHA256
`48db9ec6872bf4c7b019286ddd63878ed56579b9f369231a494e0a97c6f01e76`.
The earlier 19 manifest rows and 210 sealed shards remain exact: 230 logical
rows are now 20 live plus 210 sealed. No cap or CPU-contract credit changes;
current feature examples remain in their chapters.

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
