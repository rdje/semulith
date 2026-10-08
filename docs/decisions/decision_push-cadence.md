# Push cadence: every 300 commits, and an exception is the director's to grant

- **Type:** `decision`
- **Date:** `2026-09-14`
- **Status:** `active`
- **Owner / source:** director instruction, `2026-09-14`

## What is being decided

> *"Set the push cadence to every 300 commits. Exceptional push happen from time to time, but they
> shall require my approval."* — director

- **Cadence: 300 commits since the last push.**
- **Below cadence, a push is exceptional and requires the director's approval.**

## Why a push is governed differently from a commit

A commit is local and reversible. Reword it, drop it, rebase it — nothing outside this disk ever
knew. A push sends bytes to a server that may keep, cache, mirror or index them regardless of what
happens here afterwards. The acts differ in kind, and until this decision the repository governed
them identically: `grep -i push COMMIT.md` returned nothing, and no `pre-push` hook existed.

## What the mechanism actually guards against

⛔ **An agent deciding, reasonably and on its own, that this particular push is fine.** That is the
failure mode this exists to prevent, and it is not a hypothetical one — an assistant asked to
"finish up" has every incentive to treat pushing as tidying. So:

- the `pre-push` hook **refuses**, it does not warn, because a warning at an outward-facing
  boundary is read after the bytes have left;
- approval is carried by `SEMULITH_PUSH_APPROVED='<reason>'`, and the reason is echoed into the
  permitting message so the exception is auditable rather than indistinguishable from routine;
- **the director grants the exception; the variable only carries it.** An agent setting that
  variable from its own judgement has defeated the rule, not satisfied it.

⚠️ A human with `--no-verify` can always proceed. The gate is not a lock; it makes the act
deliberate and visible instead of accidental.

## The accepted exposure, stated rather than discovered later

At the time of this decision **45 commits exist only on one disk**, and cadence 300 means they stay
there for a long while. That is the director's call, made with the exposure on the record. It is
written here so it remains a decision someone made rather than an oversight nobody revisited.

## How to apply

- **Routine work:** commit per `COMMIT.md`, do not push, do not ask about pushing.
- **Reached 300?** `scripts/check_push_cadence.sh --status` says so, and the push is permitted.
- **Need an earlier push?** Say why, and let the director decide. If they approve, pass their reason
  through `scripts/approved_push.sh '<their reason>'` per COMMIT.md: full local CI,
  committed approval ledger, then the guarded push. The original variable-only mechanism
  described above has since been hardened; the variable alone is insufficient.
- **Current recovery exception:** [[decision_ci-recovery-push-approval]] records the
  director's approval for the pushes needed to repair the current GitHub CI failures.
  Do not ask again within that scope; ordinary cadence resumes after all three workflows pass.
- **The number lives in `scripts/check_push_cadence.sh` and nowhere else.** `COMMIT.md` restates it
  and that script's self-test checks the two agree — the same no-duplicated-fact rule the canonical
  definition uses.

Related: [[decision_public-repository-no-confidential-content]], [[decision_delivery-provenance-is-frozen]].
