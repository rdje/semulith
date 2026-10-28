# The director's rulings of 2026-10-28: the five recommendations granted, the next push granted

- **Type:** `decision`
- **Date:** `2026-10-28`
- **Status:** `active`
- **Owner / source:** the director, 2026-10-28, on the five recommendations of the session's status report:
  "I grant all your recommendations"; "Your recommendations better be sota, signoff and production-grade";
  "next push granted". Authority `director` (not a delegation).
answers: What did the director rule on 2026-10-28, to what standard, and which leaf executes each ruling?

## The fact / decision

| # | Ruling | Record | Executed by |
| --- | --- | --- | --- |
| 1 | Case declarations move to data; both retained cases re-captured once | [`decision_case-declarations-as-data.md`](decision_case-declarations-as-data.md) | `P4-SYSTEM.14` (slice a44 first) |
| 2 | `XTASK` closes with its 13 remaining scripts in shell | [`decision_xtask-closes-with-shell-remainder.md`](decision_xtask-closes-with-shell-remainder.md) | `XTASK.4`, then the tree's close |
| 3 | The next push is granted | this record | the next push (a cadence push: 359 commits since 76882c8c, cadence 300) |
| 4 | Orphan incremental sessions: whole sessions, record-anchored (option C); other trees' leftover build directories removed | [`decision_orphan-sessions-record-anchored.md`](decision_orphan-sessions-record-anchored.md) | `ARTIFACT-CLEANUP.29` |
| 5 | The doctrine controls: a probe exception refuses; live-data controls judge frozen copies | [`decision_doctrine-controls-refuse-and-freeze.md`](decision_doctrine-controls-refuse-and-freeze.md) | `XTASK` (the three doctrines' open questions) |

## Why

Each item had waited on the director with its options measured and written down in its leaf. The standard
is the 2026-10-26 delegation's: "sota, signoff and production-grade" — every ruling is executed by a leaf
under the gated commit, with its controls fired RED where a control exists, and nothing in a ruling is
read as wider than its words.

## How to apply

- Ruling 1 was recommended as "one re-capture of the M case"; measured while recording it, both retained
  cases pin the two declaration scripts (`evidence/rv64gc-m-forms-v3` and
  `evidence/rv64gc-signed-div-truncation-v2`), so it costs two re-captures. Recorded as measured; the
  director is told.
- Ruling 1 does not reach the ZICNTR program: it waits for a pinned reference that implements Zicntr (the
  `.14` a43d-1 addendum), a reference re-pin no option addressed. It stays open, raised to the director.
- Ruling 3 covers the next push only; later pushes follow the 300-commit cadence or a new approval.
