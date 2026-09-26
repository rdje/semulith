# The director named a priority action — when does it run?

**Immediately after context recovery, before any standing housekeeping.** A session's startup
has two kinds of obligations: standing ones (cleanup cadences, record-keeping) that recur every
session regardless, and pointed ones, where the director has said *"do X"*. The pointed kind
wins, and it wins because the standing kind is designed to be interruptible — cleanup can wait
24 hours; an adopted fix or a named decision cannot.

## What happened

`2026-09-26`. The director's first message of the session: *"update LINKEDSPEC submodule since
they fixed and pushed the bugs you reported."* The session instead ran the §8 artifact cleanup
first — defensibly, on the reading that a startup obligation is a startup obligation — and the
director had to say twice, including *"I urge you … that's important"*, before the pin moved.

Nothing was corrupted by the ordering: the cleanup touched only cargo caches and no earlier step
had read the reader. But the cost was real anyway — the director's attention spent re-prioritising
work they had already prioritised once, and a session that was visibly doing something other than
what it had just been told to do.

## The rule

> When the director names an action, it is the first work after the minimum context needed to act
> safely. Standing cadences queue behind it.

"Minimum context" is genuinely small: the bootstrap files, the resume pointer, the named target's
own records, git state. It is not the whole startup checklist — the rest of the checklist
continues *after* the named action lands, because the named action is itself usually the thing
the rest of the checklist would have surfaced as next.

Corollaries that keep the rule honest:

- **Urgency never skips safety.** "Update the submodule" still means verify-then-commit; the
  minimum context exists so the fast path is the safe path.
- **A named action preempts a batch, not the pivot rule.** The repo must still be clean before
  switching trees — speed never overrides handoff integrity.
- **If the named action and a gate collide** (the gate red, the action blocked), the blocker is
  named to the director immediately, not worked around silently.

Related: [[re-derivable-vs-cited-evidence]] (why the pin update wanted a re-run, not a changelog),
[[a-parse-without-error-is-not-a-faithful-read]].
