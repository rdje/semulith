# `REQ-D-XLEN` is credited `implemented` on the XLEN case, signed by review under delegation — the first `state` requirement

- **Type:** `decision`
- **Date:** `2026-10-29`
- **Status:** `active`
- **Owner / source:** `P4-SYSTEM.14` a43a-3, `SEMULITH-P4-0327`; the workflow under
  [`decision_four-rulings-delegated.md`](decision_four-rulings-delegated.md), carrying out item 1 (iii) of
  [`decision_state-capture-plan.md`](decision_state-capture-plan.md); the act and its rulings are
  [`decision_req-gc-m-credited-implemented.md`](decision_req-gc-m-credited-implemented.md)'s; the measurement is
  [`decision_reviews-read-every-retained-case.md`](decision_reviews-read-every-retained-case.md)'s.
answers: Who signs the XLEN credit, is one finite case of seventeen witnesses enough for `implemented`, and what do the case's retained M words claim?

## The fact / decision

1. **Authority.** `CR-D-XLEN-1` in `profiles/rv64gc-lab-v0/credits.sexp` carries `authority review`: the workflow's
   review under the director's delegation of 2026-10-26, as `CR-GC-M-2` does.
2. **Sufficiency.** One finite case — `rv64gc-xlen-forms-v1`, 17 predeclared witnesses (bit 63 and the 2^64 wrap, the
   shift amounts, RV64 LUI, the `*W` family, and the 64-bit address reported whole through `mtval`), a baseline, a
   byte-identical repeat, one control diverging at the predeclared witness (step 24, x31: 2^40 observed, 0 in the
   control's expectation) — whose ten policy legs measure `satisfied` (`rv64gc-xlen-forms-v1: DIV-POLICY: satisfied —
   10 of 10 legs satisfied`, a43a-2f) is sufficient for `implemented`, and for nothing more: the M rulings' reading of
   the derivation ("every effective obligation credited through a current record") and of the policy's legs.
3. **The retained M words claim nothing.** Three strings in the retained bytes are the producers' fixed M text, not this
   case's: the receipt's limitation "not all M or CPU acceptance" (`retain_div_capture.py`, fixed for later receipts at
   a43a-2e), and the measured record's `control` prose "wrong quotient must diverge" with its control-run id
   `wrong-quotient` (`scripts/capture_div.py`, which both captures' manifests pin). Retained bytes are never rewritten,
   and a record's prose and verdict words grant nothing (`credit_records.dossier_qualification`); the control-run's
   `reason` states the actual control. The record's `limitations` name all three.
4. **The act** (one commit): the record; `implementation_status implemented` on `REQ-D-XLEN`; the dossier copy of the
   case's measured record in `references.sexp` and its `G-TRACE` evidence row in `gate.sexp`; the GS report and the
   model book regenerated. The derivation must report 46 `planned`, 2 `implemented`, 2 credited, 0 drift; G-STATE
   `1 of 4 state requirements implemented`.

## Why

- The route, the vocabulary and the order are the state-capture plan's; this is its third step for its first case.
  The XLEN requirement is `defined` and low risk: the policy asks no second method and no feature rule applies
  (the reviews' decision, item 4).
- Generalizing `capture_div.py`'s two literals inside this act would move an input both captures' manifests pin:
  `CR-GC-M-2` and this record would lapse in the commit meant to credit — so the fix is its own window, scheduled before
  the next case (see How to apply).

## How to apply

- The fix is scheduled (2026-10-29, the director's question): the window that opens CSR-SET makes `capture_div.py`'s
  control prose and control-run id the case's own and re-captures this case once, before any further case is declared
  ([`decision_producer-debt-paid-before-the-next-case.md`](decision_producer-debt-paid-before-the-next-case.md)); the
  cell vocabulary is not widened.
- Any pin movement lapses this credit as it does `CR-GC-M-2` (the three pins and every input of the case's manifest);
  the status falls back to `planned` and the gate fails.
