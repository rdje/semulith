# My second case's retained record says "wrong quotient" — where did the first case's words come from, and how do I catch them before a capture freezes them?

**A producer generalized from its first case keeps that case's literals.** `P4-SYSTEM.14` a44 moved every case-specific
fact of a matched case — properties, witnesses, the control's property and reason — out of the producers and into
`evidence/<case>/case.sexp`. It did not move the string literals the producers *emit*, because with one case they
read correctly. The XLEN case, the first non-M case, was declared and captured through the generalized producers and
froze three M phrases into retained bytes:

| Literal | Where it is emitted | Where it froze | Cost of fixing it |
| --- | --- | --- | --- |
| "…, not all M or CPU acceptance" | `scripts/retain_div_capture.py` (receipt limitations) | `verification.json` | none: unpinned, fixed for later receipts at a43a-2e |
| "Predeclared target: wrong quotient must diverge." | `scripts/capture_div.py:337` (`control` prose) | planned and measured records | a lapse: both captures' manifests pin `capture_div.py` |
| `wrong-quotient` | `scripts/capture_div.py:330` (control-run id) | planned and measured records | the same lapse |

None of them changes a verdict: the record's prose and verdict words grant nothing, and the control-run's `reason`
(from `case.sexp`) states the real control. But they are false statements in retained evidence, a credit must name
them (`CR-D-XLEN-1`'s limitations), and every later case copies them until the producer changes.

## How to catch it

Before the declaration commit of the first case of a new kind, audit what the producers write, not what they read:

```bash
grep -n -i '"[^"]*\(quotient\|divi\|m-forms\|M case\|REQ-GC-M\)[^"]*"' scripts/capture_div.py scripts/retain_div_capture.py \
  scripts/matched_gpr_case.py scripts/matched_gpr_property.py
grep -o 'quotient\|wrong-[a-z]*' evidence/<new-case>/planned-experiment.sexp
```

Every string in the planned record that is not copied from `case.sexp` and names the first case's subject is a leak.
The planned record exists at the declaration commit, before the capture: that is the last moment it costs nothing.

## When it is found after the capture

Retained bytes are never rewritten. Name the literal in the credit's limitations, then fix the producer before the
next case is declared: every capture pins the producer, so each case captured on it adds a re-capture to the fix. Batch
the fix with any pinned change the next case needs anyway, in one planned lapse window, and re-capture the existing
cases once (their traces byte-identical). This one was paid at `P4-SYSTEM.14` a43b-2b: the control's id and statement
are fields of each case's declaration, the producer refuses a case without them, and the audit above is mechanical —
`scripts/probe_div_command.py` plans a declaration whose control id and statement are unique tokens and requires every
prose string of the planned record to come from the case file or the producer's reviewed neutral set (`NEUTRAL_PROSE`,
five strings); restoring either literal fails it by name (seams `control-id-literal`, `control-statement-literal`).
A new neutral sentence in the producer fails it too, until it is reviewed into the set. Evidence: `decision_producer-debt-paid-before-the-next-case.md`,
`decision_req-d-xlen-credited-implemented.md`; `docs/tasks/P4-SYSTEM.md` a43a-2e, a43a-3 and a43b-2b.
