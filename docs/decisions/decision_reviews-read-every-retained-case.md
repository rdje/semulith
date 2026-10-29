# The retained reviews read every reviewed capture; a state requirement's form coverage is vacuous; no feature rule applies to OB-XLEN

- **Type:** `decision`
- **Date:** `2026-10-29`
- **Status:** `active`
- **Owner / source:** `P4-SYSTEM.14` a43a-2f, `SEMULITH-P4-0326`; the workflow's decision under
  [`decision_four-rulings-delegated.md`](decision_four-rulings-delegated.md); continues
  [`decision_caller-names-the-case.md`](decision_caller-names-the-case.md) (the retained pointer lives in consumers no
  case pins), [`decision_state-capture-plan.md`](decision_state-capture-plan.md) (XLEN's address witnessed through the
  handler's read of `mtval`) and [`decision_ten-legs-satisfied-credit-separate.md`](decision_ten-legs-satisfied-credit-separate.md).
answers: How do the finite method and policy reviews read a second captured case, and how are the XLEN case's form-coverage and feature-rules legs decided?

## The fact / decision

1. **One row per reviewed capture.** `scripts/review_div_method.py` holds `RETAINED_CAPTURES`: per case, the
   declaration commit, the capture commit and the measured record's SHA256 and size, all reviewed historical facts.
   The M case's v4 keeps its named pins (177b43a1, 3c464095); the XLEN case's row is 5c2cde93, e32cc645 and
   `measured-experiment.sexp` 14,958 B `d39825b0…`. A case without a row (v2, v3: retained history) is `unsupported`
   and reads nothing. `scripts/review_div_policy.py` accepts exactly those cases, and `--every-retained` measures each
   in the row order, one line per case, exiting with the worst code; `PROFILE-CONSISTENCY`'s real run calls it.
2. **The boundary marker is the source's own.** A directed boundary fixture is an expectation step whose source cites
   a chapter table row (`Table`, M's Table 1) or carries a `(boundary: …)` tag (the XLEN guest's ten, a43a-2d). The tag
   occurs in no M expectation (`grep -c "(boundary"` = 0 for m-forms and v4), so M's twelve rows do not move.
3. **A state requirement naming no form is covered vacuously, and says so.** The form-coverage leg is satisfied when
   the requirement's `kind` is `state` and it names no instruction (REQ-D-XLEN: the register width and the address
   space); the leg's text reads "a state requirement names no form: coverage is vacuous, its 17 predeclared witnesses
   stand for it". Any other requirement naming no form stays pending.
4. **No feature rule applies to `OB-XLEN`.** The register width and the 64-bit address space touch no privilege,
   translation, atomic, floating-point, counter, fetch or environment rule. The access fault at 2^40 and the handler's
   `CSRRS` of `mtval` are the route that observes the address, not a claimed trap, CSR or protection behaviour: the
   fault's selection is REQ-D-FAULT-PRIORITY's, `mtval`'s presence REQ-D-CSR-SET's, the read REQ-GC-CSR-ACCESS's.

Measured (`target/p4-system-14/a43a-2f`): both cases `DIV-POLICY: satisfied — 10 of 10 legs satisfied`; v4 credited by
`CR-GC-M-2` (its table identical to the single-case run), the XLEN case uncredited. Before the change the XLEN case
measured 7 of 10, pending on exactly boundary-fixtures (0 rows), feature-rules (undeclared) and form-coverage (0 of 0).

## Why

- The reviews are consumers no manifest pins (a42av), so a row is added without lapsing a declaration, a capture or
  `CR-GC-M-2`; keeping v4's named constants keeps the method probe's synthetic copy re-pinning them unchanged.
- The policy credits declared observations only. A `state` requirement names no instruction, so "every form the
  requirement names" is the empty set; an empty set read as `pending` would block every state requirement forever,
  and read silently as `satisfied` would hide it — the leg states the vacuity and keeps the witnesses' count.
- A feature rule governs a check OF that feature. The XLEN case claims no trap behaviour: had the reference truncated
  `mtval`, the witness would diverge (the control models exactly that), but no trap, CSR or protection requirement is
  credited by it. The OB-GC-M disposition (a42aq) is the precedent for a `cpu-guarantee` obligation whose checks are
  the case's witnesses and its control.

## How to apply

- The next captured case (CSR-SET, SSTC) gets its own `RETAINED_CAPTURES` row in the unit that reviews it, and its
  obligation its own `FEATURE_DISPOSITIONS` row — those two are high risk and implementation-defined, so their feature
  rules (privilege/CSR/trap; counters/interrupts) DO apply and are met inside the program
  ([[decision_state-capture-plan]]); "none applies" is not their disposition.
- The probes hold the rows: `probe_div_method.py`'s real-tree arm requires one authenticated-count triple per row,
  `probe_div_policy.py`'s real-tree arm one expectation block per case; a new row without them fails.
- The XLEN credit (`CR-D-XLEN-1`, REQ-D-XLEN `implemented`) is the next unit; it cites this satisfied measurement.
