# My gate's self-test says `N pass / 0 fail` — how do I know N is all the arms I wrote?

**You don't, unless you count.** A self-test reports the arms it *ran*. Nothing in the report
distinguishes "every arm passed" from "most arms never executed and the survivors passed".

## What happened

`scripts/check_frontier_sync.sh` was written with fourteen control arms. Its first run printed:

```
FRONTIER-SYNC --self-test: 4 pass / 0 fail
```

Green, `rc=0`, and judging almost nothing. Ten arms had been written in the shape

```bash
  index active '`.1` — first'                 arm "RED   index names another leaf"  1 "FRONTIER DRIFT"
```

Two shell commands on one physical line with no `;` between them. Bash does not see two
commands there — it sees one call to `index` with six arguments. `index()` reads `$1` and `$2`
and ignores the rest, so `arm` and its three arguments were **discarded in silence**. No syntax
error, no unbound variable, no nonzero exit. Adding the separator turned `4 pass / 0 fail`
into `13 pass / 1 fail` — and that single failure was real (two opposite drift directions were
sharing one message, so one of them could never be distinguished). That is the second half of
the point: the skipped arms were not decoration, and the green report had been concealing a
genuine defect in the gate as well as in its own coverage. Two further arms were added while
fixing it, which is why the file now holds sixteen.

## How to catch it

Count the arms you wrote and compare that number to the number the self-test reports. It is one
subtraction and it is the only check that catches this class:

```
$ grep -c '  arm "' scripts/check_frontier_sync.sh
16
$ scripts/check_frontier_sync.sh --self-test
FRONTIER-SYNC --self-test: 16 pass / 0 fail
```

`16` written, `16` accounted for (14 RED + 2 GREEN) — they agree. At the moment of the defect
the same two commands read `14` and `4 pass / 0 fail`. **Ten arms, gone, and the report said
`0 fail`.** That difference is the entire signal: a mismatch means arms are being skipped,
whatever the pass count says.

## Why it generalizes

This is the repository's own founding failure class in a new costume. `DEV_NOTES.md`
(`2026-09-04`) records *"a green gate that judges nothing is the class a template must not
ship"*, and `TOOLBOX.md` states it as a rule: **a gate that has never been observed RED is not
known to work.** The subtlety here is that the rule is usually applied to the *gate* and this
was the *self-test* — the instrument that certifies the gate. One level up, the same question
applies, and nothing was asking it.

The shell-specific trigger is worth carrying separately: **a function that ignores its extra
arguments will swallow a whole command silently.** Any `f() { use "$1" "$2"; }` turns a missing
`;` into deleted code rather than into an error. Writing `local` parameters or a
`[ $# -eq 2 ] || return 2` guard in a test helper converts that silence into a failure.

## A sibling failure — a GREEN control that masks the finding (2026-10-06, P4-SYSTEM.9 slice d)

CONTRACT-FREEZE ran its controls BEFORE judging (the project's convention), and its GREEN arm
copied the LIVE contract files. With a frozen record edited, the GREEN arm failed, the self-test
failed, and the gate printed "REFUSED — the check does not discriminate" instead of naming the
edited record: the finding hid behind a harness message. A failing verdict needs no proof that the
check discriminates — only a passing one does. The fix: judge first, exit 1 with the findings;
run the controls only to certify a PASS.

- Audit any check whose GREEN control reads the live tree: a broken tree must surface as the
  finding, not as "does not discriminate".

## A third failure — a control pinned to the live data (2026-10-06, P4-SYSTEM.11 slice b)

The gate report's controls built scratch copies of the REAL unit and asserted its numbers as
they stood ("100 effective checks, 14 realized"). They were right for one leaf. The contract's
first legitimate growth turned them red, and through GATE-REPORT's self-test they would have
refused every later commit, for a change that was correct. A control over live data must
assert what the check DOES — a delta from a baseline measured at run time (+1 realized for an
added entry; −1 for a misregistered one), or agreement with an independent recount — never
today's totals.

- When writing a control, ask: would a correct change to the data turn this red?

Related: [[census-instrument-signature-gap]], [[re-derivable-vs-cited-evidence]].
