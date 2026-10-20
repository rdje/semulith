# <TREE-ID>: <Task Title>

## Metadata

- Tree ID: `<TREE-ID>`
- Status: `proposed`
- Roadmap lane: `<roadmap lane name>`
- Created: `YYYY-MM-DD`
- Owner: repo-local workflow

## Goal

State the exact outcome this top-level task must deliver.

## Non-Goals

- State what this task deliberately does not solve.

## Acceptance Criteria

- `<Tree-specific outcomes; apply the guide’s general completion criteria.>`

## Task Tree

- ID: `<TREE-ID>`
  Status: `active`
  Goal: `<top-level goal>`
  Children: `<TREE-ID>.1`

- ID: `<TREE-ID>.1`
  Status: `pending`
  Goal: `<first executable leaf>`
  Acceptance: `<what proves this leaf is done>`
  Verification: `pending`
  Commit: `pending`

## Current Frontier

| Order | Leaf | Status | Why next |
| --- | --- | --- | --- |
| 1 | `<TREE-ID>.1` | `pending` | `<reason>` |

## Decisions

- `YYYY-MM-DD`: `<decision and rationale>`

## Open Questions

- `<question, owner, and why it does or does not block the frontier>`

## Blockers

- None.

## Acceptance Checklist (leaf <TREE-ID>.1)

[Evidence requirements](../TASK_TREE_README.md#acceptance-checklist-required-for-any-leaf-that-lands-a-code-change).

- [ ] **REPRODUCE / ISSUE** — `<problem + observed output>`
- [ ] **ROOT CAUSE (WHY + WHERE)** — `<command/output + mechanism/location>`
- [ ] **FIX** — `<change>`
- [ ] **ADDRESSED (verified)** — `<measured before → after>`
- [ ] **NO REGRESSION** — `<checks + results>`
- [ ] **LOCKSTEP** — `<docs/contracts/index sync>`

## Verification Log

| Date | Leaf | Checks | Result |
| --- | --- | --- | --- |
| `YYYY-MM-DD` | `<TREE-ID>.1` | `pending` | `pending` |

## Commit Log

| Leaf | Commit subject or reference | Notes |
| --- | --- | --- |
| `<TREE-ID>.1` | `pending` | `pending` |

## Changelog

- `YYYY-MM-DD`: Created task tree.
