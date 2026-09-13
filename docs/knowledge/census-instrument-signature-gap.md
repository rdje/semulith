# My census evidence was rejected by the acceptance gate — is my evidence weak, or the gate?

**Answer: check whether the two doctrines agree on what an instrument is, before rewriting
your evidence.** In this spine they did not. `GAP-CLAIM-CENSUS` *instructs* an author to
enumerate with `git grep … | wc -l`; `TASK-ACCEPTANCE`'s default signature family does not
recognise either command, so the evidence one doctrine asks for is evidence the other refuses.

## Evidence

```
$ grep -o "git (ls-files[^|]*|[^)]*)" scripts/check_task_acceptance.sh | head -1
git (ls-files|log -S|log --all -S|rev-list|fsck|reflog|diff-tree|merge-base|cat-file|show )

$ grep -n "git grep" scripts/check_gap_claims.sh | head -2
60:CENSUS_RE='git grep|grep -r|grep -c|grep -l|…|wc -l|sort -u|uniq -c|…'
99:    echo "         git grep -n '<symbol>' -- src scripts | wc -l   # -> 0"
```

`git grep` and `wc -l` appear in the census gate's accepted list **and in its own printed
hint**, and in neither the acceptance gate's default list nor its documentation.

## What to do about it

Use the sanctioned seam, not a waiver and not weaker evidence: declare the real instrument
signature in `.doctrine/evidence_tokens.txt`. That file exists precisely so a project adapts a
neutral check without forking it — editing the check to hardcode your tool names is what turns
a portable standard into someone else's workflow.

⛔ **Do not "fix" this by pasting a different command that happens to match.** That produces a
leaf whose evidence is chosen for the grep rather than for the question, which is the failure
mode the gate exists to prevent.

## It happened three times, and the third fix was different

| # | The refused evidence | The patch |
| --- | --- | --- |
| 1 | `git grep -lE … \| wc -l` — a census the sibling gate recommends | declared `git grep` and `wc` |
| 2 | `README-ROUTING-CLOSURE: ok (24 governed destination(s))` — a new project doctrine's own verdict line | replaced the **enumerated list of doctrine names** with the *shape* every gate prints |
| 3 | `grep -ci reset rv32.txt rv64.txt` — a plain enumeration over a pinned specification | replaced `git grep` with **any** `grep` invocation, aligning with the census gate's own accepted list |

The first two patches were additions; each held until the next new thing existed. Only the
third and second kind of fix — *match the shape, not the instance* — stopped the pattern. ⭐ **A
list that must be edited whenever a sibling file changes is a list that will be stale.** If you
find yourself declaring a token for the third time, the declaration is the wrong shape.

After each widening the gate was fired RED on a prose-only box (`rc=1`) to prove it still
discriminates. Widening a gate's acceptance is exactly the change that can make it vacuous, and
"it still looks strict" is not a measurement.

## Why this generalises

Two gates written at different times share no vocabulary unless something forces them to. A
signature family that does not fit the real corpus is a gate authors learn to waive — and a
waiver is itself the highest-signal bug report a gate can receive (`WAIVER-ROUTING`). When you
hit a boundary, the first question is not *"how do I get past this?"* but *"which of these two
rules is wrong, and who owns fixing it?"* Here the local answer is a declared token; the
upstream answer is a `bedrock` change, and it belongs to whoever maintains that template.
