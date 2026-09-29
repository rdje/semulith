# The work-unit prefix is SEMULITH, never SEMILITH

- **Type:** `decision`
- **Date:** `2026-09-30`
- **Status:** `active`
- **Owner / source:** director ruling, 2026-09-30 ("it is SEMULITH and not SEMILITH … only
  SEMULITH and NOT SEMILITH"), after the spelling drift was surfaced the same day

## The fact / decision

Every work-unit id in a commit subject begins with the pinned project prefix `SEMULITH-`.
The spelling `SEMILITH-` — and any other — is refused by the `commit-msg` hook, with the
refusal naming `SEMULITH`.

## Why

The drift is measured, not hypothetical: 123 commits at ruling time carry both spellings
(`SEMILITH-PL` ×13, `SEMILITH-PS` ×8, `SEMILITH-MM` ×8, `SEMILITH-MB` ×8, `SEMILITH-SF` ×5,
`SEMILITH-MC` ×4, `SEMILITH-AC` ×3, …). Commit subjects are immutable history, so nothing
retroactive is fixable; a rule that is not enforced at the boundary loses to a typo every
time. The pin therefore lives where new subjects enter: `.githooks/commit-msg`. That hook is
a **neutral scaffold file** (`scripts/update_scaffold.sh` syncs it from the spine), and
carrying the pin upstream is unavailable by policy — other repositories are read-only. A
scaffold sync would revert the pin silently, so the project doctrine `COMMIT-PREFIX`
(`scripts/check_commit_prefix.sh`) probes the hook **behaviourally** on every commit: a silent
revert turns the very next commit RED, named. Same exposure, same shape as the repaired spine
defects ([[reference_upstream-spine-defects]], watched by SEAM-INTEGRITY).

## How to apply

- Write `SEMULITH-<AREA>-<NNNN>` in every commit subject. The hook refuses anything else;
  there is no override and no exception lane.
- If `COMMIT-PREFIX` goes RED naming a missing pin (typically after a scaffold sync), restore
  the pin in `.githooks/commit-msg` — the ruling stands; the sync is the accident.
- Never "fix" the misspelled history; it is the measurement that justified the pin.

Related: [[decision_push-cadence]] (the other boundary the hooks refuse rather than warn at).
