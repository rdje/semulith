# Push approvals — the append-only record of pushes

Every exceptional push (below the 300-commit cadence, with the director's approval) leaves
one entry here, written by `scripts/approved_push.sh` as PART of the act — never afterwards
from memory (PUSH-DISCIPLINE.3). Cadence pushes leave no entry: nothing exceptional
happened.

⛔ APPEND-ONLY. Entries are never edited or removed; a correction is a new entry. The
`PUSH-RECORD` doctrine (`scripts/check_push_record.sh`) refuses any staged change to this
file that is not a pure append (HEAD's content must be a prefix of the new content), and
refuses an entry missing a required field.

Entry shape (one `## SEMULITH-PUSH-NNNN — <timestamp>` block per act):

- **Approved by:** the director — the approval is theirs; the variable only carried it
- **Reason:** the reason they gave, verbatim
- **Range:** `<upstream>..<HEAD>` — the commits this push carried (derived from git, never typed)
- **Suite:** `make ci` green at the recorded HEAD before the record was written

## SEMULITH-PUSH-0001 — 2026-10-08T17:19:08+0200

- **Approved by:** the director
- **Reason:** pushes needed to fix GitHub CI are exceptional hence accepted
- **Range:** origin/main..5cd7ab65e192639c06b08e1189310097d2f27984 — 20 commit(s) since the last push, plus this record commit
- **Suite:** `make ci` green at 5cd7ab65e192639c06b08e1189310097d2f27984 before this record was written

## SEMULITH-PUSH-0002 — 2026-10-08T17:55:23+0200

- **Approved by:** the director
- **Reason:** pushes needed to fix GitHub CI are exceptional hence accepted
- **Range:** origin/main..1f25d4871fe73fc6e078f2f13fd78fa2ff7f6a25 — 3 commit(s) since the last push, plus this record commit
- **Suite:** `make ci` green at 1f25d4871fe73fc6e078f2f13fd78fa2ff7f6a25 before this record was written

## SEMULITH-PUSH-0003 — 2026-10-28T19:19:26+0100

- **Approved by:** the director
- **Reason:** director 2026-10-28: 'ok' to pushing the fix for the hosted doctrines failure on b917d1ba (ARTIFACT-COHORT on Linux, run 40713852259) once the gated commit lands
- **Range:** origin/main..62e807a71ecc698566b91021ea55ecb9f4e91960 — 7 commit(s) since the last push, plus this record commit
- **Suite:** `make ci` green at 62e807a71ecc698566b91021ea55ecb9f4e91960 before this record was written

## SEMULITH-PUSH-0004 — 2026-10-28T21:04:40+0100

- **Approved by:** the director
- **Reason:** director 2026-10-28: 'right now I need the GitHub CI to go green' - push the UNIT-BOOKS refusal diagnostic so the hosted doctrines run names what missed (run 40746652030 refused with no detail after a runner image change)
- **Range:** origin/main..300ffbf41d7c3d2fdd1936342ae5f277c5cba9be — 5 commit(s) since the last push, plus this record commit
- **Suite:** `make ci` green at 300ffbf41d7c3d2fdd1936342ae5f277c5cba9be before this record was written

## SEMULITH-PUSH-0005 — 2026-10-28T23:20:26+0100

- **Approved by:** the director
- **Reason:** director 2026-10-28: 'right now I need the GitHub CI to go green' - push the fix for the hosted UNIT-BOOKS refusal (a probe counted Python 3.12's pathlib calls; run 40763391753)
- **Range:** origin/main..48473252390a6852359dae96e89170d4a5ff957a — 2 commit(s) since the last push, plus this record commit
- **Suite:** `make ci` green at 48473252390a6852359dae96e89170d4a5ff957a before this record was written
