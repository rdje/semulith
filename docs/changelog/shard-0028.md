# CHANGELOG shard — SEMULITH-PD-0046 … SEMULITH-PD-0046

> Sharded from `CHANGELOG.md` when it crossed its 64 KiB ceiling (`doctrine/readme_routes.tsv`).
> Entries in a shard are **never edited after the shard** — git history is canonical.

## SEMULITH-PD-0046 (leaf PUSH-DISCIPLINE.1) — the push boundary gets a gate that refuses

**Director instruction, `2026-09-14`:** *"Set the push cadence to every 300 commits. Exceptional
push happen from time to time, but they shall require my approval."*

**Measured before writing anything, and the finding is an absence:**

```
$ grep -ci push COMMIT.md          ->  0     the normative commit workflow never mentions pushing
$ ls .githooks/                    ->  commit-msg  pre-commit     (no pre-push)
$ git rev-list --count origin/main..HEAD  ->  45
```

45 commits had exactly one governance rule between them and a server: a human remembering. The
policy was not being broken — it did not exist.

**Why a push is governed differently from a commit.** A commit is local and reversible: reword it,
drop it, rebase it, and nothing outside this disk ever knew. A push sends bytes to a server that
may keep, cache, mirror or index them regardless of what happens here afterwards.

⛔ **And the specific failure this guards against is an agent's.** An assistant asked to "finish
up" will naturally read pushing as tidying, and will reach — reasonably, on its own — the judgement
that this particular push is surely fine. So the hook **refuses rather than warns** (a warning at
an outward-facing boundary is read after the bytes have left), and **the director grants the
exception while the variable only carries it**:

```
$ bash scripts/check_push_cadence.sh --status ; echo $?
PUSH-CADENCE: REFUSED — 45 commits since the last push; the cadence is 300 …
  Two ways forward, and only two:
    1. Wait. The cadence is 300 commits; this is 45.
    2. Ask the director. … SEMULITH_PUSH_APPROVED='<the director's reason>' git push
  ⛔ An agent may not supply this on its own judgement.
1
```

**11 arms, each in a throwaway repository with a real upstream** — a gate about
distance-from-upstream cannot be tested without one. Three were fired RED first and failed: two
because the refusal message wrapped across a newline so a literal match missed it, and one because
`COMMIT.md` did not yet state the cadence — the no-duplicated-fact arm doing its job before the
fact existed.

⛔ The instrument refuses on `DETACHED`, `NO-UPSTREAM` and `NOT-A-REPO` rather than printing a
distance it cannot know. "0 commits ahead" for a detached HEAD is a lie that *permits* a push.

**The accepted exposure is on the record, not discovered later.** 45 commits exist only on one
disk and cadence 300 means they stay there a long while. `decision_push-cadence` states that
plainly, so it remains a decision someone made rather than an oversight nobody revisited.

New tree `PUSH-DISCIPLINE` (3 leaves). `.2` is next and is Policy 16's unenforced half: full CI
runs before a push, and nothing enforces it — the pre-commit hook covers only the "selected checks
for ordinary commits" side.

