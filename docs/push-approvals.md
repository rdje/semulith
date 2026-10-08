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
