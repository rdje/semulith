# CHANGELOG shard — SEMULITH-PD-0051 … SEMULITH-PD-0051

> Sharded from `CHANGELOG.md` when it crossed its 64 KiB ceiling (`doctrine/readme_routes.tsv`).
> Entries in a shard are **never edited after the shard** — git history is canonical.

## SEMULITH-PD-0051 (leaf PUSH-DISCIPLINE.3) — the approval record; PUSH-DISCIPLINE closes (3/3)

- An exceptional push is now an auditable ACT: `scripts/approved_push.sh '<the director's
  reason>'` runs `make ci` green FIRST (a red suite refuses and writes nothing), appends
  the entry to the tracked append-only ledger `docs/push-approvals.md` and commits it as
  its OWN commit (`SEMULITH-PUSH-NNNN: push approved — <reason>` — the only way the record
  travels in the pushed history), then pushes with the approval variable set — and the
  pre-push boundary re-verifies all three: cadence, suite, record.
- The ledger entry carries: the sequential id, the act's timestamp, the director as
  approver, the reason verbatim, the derived range (`<upstream>..<work-head>`, N commits —
  never typed), and the suite line. Cadence pushes leave no entry.
- `PUSH-RECORD` (#28, `scripts/check_push_record.sh`) enforces it: a staged change must
  keep HEAD's content a PREFIX of the new content (history is never rewritten), and every
  entry carries who/when/why/range with sequential ids — self-test 6/0; fired RED against
  the real corpus before registration (a malformed entry → `MISSING FIELD`, named).
- ⭐ The design's fixpoint defect — "the entry covers HEAD" is impossible, since the
  record commit advances HEAD — was caught by MEASUREMENT, not review: the end-to-end
  self-test's scratch push first ran with NO hooks installed (the defective check never
  ran); with the shim, the real boundary fired. The honest semantics: the entry names the
  WORK head; the record commit rides on top; the hook verifies the chain (self-test
  9/0 → 14/0 with the five approval-path arms).
- COMMIT.md names the act (the variable alone no longer suffices); the ledger has its
  routes-registry row. The tree closes 3/3 — all four Acceptance Criteria met.
- `make ci` green; `make gate` all green (28 doctrines / 297 arms). No push was attempted
  at any point; CHANGELOG.md / DEV_NOTES.md shard at their thresholds.

