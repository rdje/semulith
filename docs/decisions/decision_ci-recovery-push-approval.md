# CI recovery pushes are approved until the repaired GitHub workflows pass

- **Type:** `decision`
- **Date:** `2026-10-08`
- **Status:** `fulfilled` — all three hosted workflows passed on the repaired pushed revision
- **Owner / source:** director instruction, `2026-10-08`; owned by CI-RECOVERY.4

## The decision

> pushes needed to fix GitHub CI are exceptional hence accepted, you should do them without asking, but once the GitHub CI pass then you need to resume honoring the push cadence as defined.

The director has approved the exceptional pushes needed for the current CI recovery.
Do not request approval again within that scope. The approval expires when the rust,
doctrines and portability workflows all succeed on the repaired pushed revision;
subsequent work returns to the ordinary push cadence.

## Why

Local repairs and their verification are committed, but the failing hosted workflows
cannot be verified without pushing the repaired revision. CI-RECOVERY.4 owns the
hosted obligation and any further repair revealed by those runs. The director grants
this bounded exception rather than changing the cadence or weakening its boundary.

## How to apply

1. Complete and commit each necessary repair with its focused checks and live/book docs.
2. Run `scripts/approved_push.sh 'pushes needed to fix GitHub CI are exceptional hence accepted'`.
   That verbatim clause supplies the director's reason; the act runs full local CI,
   commits the approval ledger and pushes through the normal hook. Never bypass it.
3. Observe all three workflows on the exact pushed SHA. Own and repair new failures,
   then repeat the authorized act as necessary while this recovery remains open.
4. Record all three successful hosted run URLs and SHA, retire this authorization and
   return to the ordinary cadence. A partial green run or a local pass does not expire it.

The approved history archive and prior local work ride in the current fast-forward
range; their presence does not extend this approval to unrelated future pushes.
No authority to terminate Kimi Code or sanction its process is granted here.

Related: [[decision_push-cadence]]. Workflow: `COMMIT.md`.

## Fulfillment — observed after crash recovery, 2026-10-09

`gh run list --commit 76882c8c710db3163fed31ffec583a8c1eed49bc` reports
`completed` / `success` for all three workflows on that exact repaired pushed SHA:

- [Rust](https://github.com/rdje/semulith/actions/runs/37805020620).
- [Doctrines](https://github.com/rdje/semulith/actions/runs/37805020628).
- [Portability](https://github.com/rdje/semulith/actions/runs/37805020582), including
  both native hosts, manifest agreement and both 153-test interpreted targets.

Portability completed at `2026-10-08T16:28:37Z`; the approval expired when the
last workflow passed. Ordinary cadence now applies, including to the local recovery
receipt. No further push is made under this authorization.
