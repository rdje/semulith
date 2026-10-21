# Task-Tree Setup Guide

A task tree is a single markdown file under `docs/tasks/<TREE-ID>.md` that owns one
top-level task's recursive breakdown and its execution evidence.

## Create a tree

1. Copy [`tasks/TEMPLATE.md`](tasks/TEMPLATE.md) to `tasks/<TREE-ID>.md`.
2. Fill the metadata, goal, non-goals, and acceptance criteria.
3. Break the goal into leaves (`<TREE-ID>.1`, `<TREE-ID>.2`, …). A leaf is the smallest
   unit that can be finished, verified, and committed as one signoff-quality slice.
4. Set the **Current Frontier** table to the next executable leaf.
5. Register the tree in the Active Task Trees table in [`TASK_TREE.md`](TASK_TREE.md).

## Work a leaf

1. Move the leaf to `active`/`in_progress`.
2. Diagnose tools-first (`TOOLBOX.md`): pin WHY + WHERE before any code.
3. Implement only that leaf.
4. Record verification (before→after, the acceptance checklist from
   `DOCTRINE_ENFORCEMENT.md`) in the leaf's own record.
5. Commit via `COMMIT.md`; the record names the commit; move the leaf to `done`.
6. Update the frontier to the next leaf. One commit per leaf.

## Discover subtasks

When a leaf uncovers new work, add leaves with new direct numeric IDs
(`<TREE-ID>.2`, `<TREE-ID>.3`, …). Group related leaves under an activity heading
and list their IDs in its Children field. The progress readers accept direct
numeric IDs. Keep each committed slice safe; update its owning child list and frontier.

## When a tree completes

Mark it `done` in its own Metadata, move its index row — verbatim, status `done` — from
`TASK_TREE.md` to [`TASK_TREE_CLOSED.md`](TASK_TREE_CLOSED.md) (completed trees leave the
index; FRONTIER-SYNC refuses one left behind), ensure every leaf's evidence and commit is
recorded, and confirm the repo is clean before pivoting to another tree (the pivot rule).

<!-- ANCHOR: code-leaf-evidence -->
## Acceptance Checklist (required for any leaf that lands a CODE change)

Enforced by the `TASK-ACCEPTANCE` doctrine (`scripts/check_task_acceptance.sh`). The three boxes
below are **hard-gated**: each must be ticked **and** carry output from a tool you actually ran,
**inside that box's own bullet**. A tick is a claim; the pasted output is the artifact someone
else can re-run.

```markdown
- [ ] **ROOT CAUSE (WHY + WHERE)** — <the command you ran + its real output, naming the mechanism and the location>
- [ ] **ADDRESSED (verified)** — <measured before → after on the symptom>
- [ ] **NO REGRESSION** — <the suite/gate you re-ran + its result>
- [ ] **FIX** — <the minimal change made> *(not hard-gated)*
- [ ] **LOCKSTEP** — <docs / contracts / index updated, or N/A + reason> *(not hard-gated)*
- [ ] **REPRODUCE / ISSUE** — <the problem shown by a command and observed output> *(not hard-gated)*
```

⭐ The boxes above are the three legs of `docs/CLAIM_VERIFICATION.md` wearing this repository's
names: **ROOT CAUSE** is leg 1 (*re-derive* — does one command reproduce it from the source?),
**NO REGRESSION** carries leg 2 (*falsify* — what would make this false, and did the control
ever go RED?), and **LOCKSTEP** carries leg 3 (*durability* — is the producer tracked, and does
anything fail when the claim goes stale?). Two passes of the same question are one pass. If a
leg is missing, **name it in the box** — a claim with a named gap is usable; a claim with a
hidden gap is the defect.

⚠️ If none of the built-in evidence signatures fit your defect class, do **not** fake one and do
**not** quietly drop the box: declare your own tool's signature in `.doctrine/evidence_tokens.txt`
(see `.doctrine/README.md`). If you find yourself wanting to waive the gate instead, write the
waiver **and name the leaf that owns fixing the gate** — that is the `WAIVER-ROUTING` doctrine, and
an author hitting a gate's boundary is the highest-signal defect report the gate can receive.

## General completion criteria

- The behavior, documentation, or infrastructure outcome is implemented.
- Focused validation passes.
- Broader validation runs when the blast radius warrants it.
- Live docs and roadmap status are updated where project state changed.
- Each completed leaf is committed through `COMMIT.md`.

<!-- ANCHOR_END: code-leaf-evidence -->
