# I made the producer refuse a case it must not plan, and now a retained capture reads `refused` instead of `stale` — why?

**A consumer that detects staleness by regenerating loses it the moment the producer refuses to regenerate.** The
finite method review (`scripts/review_div_method.py`) decided `stale` indirectly: it asked the producer to prepare the
case again and found the first retained declaration whose bytes differ from the regeneration. `P4-SYSTEM.14` a43b-2b
made the producer refuse any case whose control declares no id and statement (`scripts/capture_div.py`, D1), which is
every case declared before it. Measured on the real tree, before the repair:

```text
review_div_method.py --case rv64gc-m-forms-v4  → refused: case rv64gc-m-forms-v4 declares no control id/statement …
review_div_policy.py --every-retained          → blocked (exit 1): a refused finite method is a finding
```

The captures were stale — the slice moved four inputs both manifests pin — but the review never reached the comparison
that would have said so, and the director's 2026-10-22 ruling ("a stale method invalidates, it does not lock") turned
into a red gate. The probe that caught it was the method probe's real-tree arm, which predicts each case's outcome from
its own manifest, not from the tree.

## The repair

Regeneration was only the *means*; the definition of stale is "a pinned input moved" (a42as). When the producer refuses
to prepare a retained case, the review measures that directly, with authenticated reads only: the measured record (its
pin is the review's own row), the dependency manifest through the record's `dependency-manifest` pin, then the pins of
the declaration's route — the case file, its schema — in order; the first that moved stops the review `stale`, naming
it, and a refusal with nothing moved stands. A walk over every pinned input was ruled out by measurement: one is 97,811
bytes, above the review's 64 KiB snapshot bound.

## How to apply

- Before adding a refusal to a producer, list the consumers that call it to *compare*, not to *create* (`grep -rn
  'prepare_capture' scripts/`): each one's verdict for history changes from "differs" to "refused".
- Probes that plan in runtime copies need the copy to satisfy the new rule (`probe_div_command.declare_control`);
  probes that plan the real tree's history must now assert the refusal by name.
- Keep the fallback's seam (`stale-route`) and its synthetic arm: strip the fields from a copy, expect `stale` naming
  the case file; patch a refusal with nothing moved, expect `refused`.

Evidence: `docs/tasks/P4-SYSTEM.md` a43b-2b; `decision_stale-method-invalidates-not-locks.md`.
