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

## Retirement (2026-11-02, `P4-SYSTEM.14` a43b-2b)

`CR-D-XLEN-1` was retired by removal in the one pinned-edit commit of the planned lapse that opens CSR-SET
([`decision_producer-debt-paid-before-the-next-case.md`](decision_producer-debt-paid-before-the-next-case.md)): the
slice moved four inputs the case's manifest pins (`schema/matched-case.sexp`, `scripts/capture_div.py`,
`scripts/matched_gpr_case.py`, `scripts/matched_gpr_property.py`; measured: `credit CR-D-XLEN-1 names this case but
lapsed: manifest input schema/matched-case.sexp …`), and a lapsed record is a finding. In the same commit `REQ-D-XLEN`
records `planned`, the dossier copy and the `G-TRACE` row leave, and the catalogue file leaves with its last records
(`REQUIREMENT-STATUS: … 48 planned; 4 case(s), 0 credited, 0 declared, 0 of 0 credit record(s) current; 0 drift`). The
rulings above stand for the re-credit: the case re-captured once as `rv64gc-xlen-forms-v2`, its control declared
(`truncated-address`), is credited by `CR-D-XLEN-2` through the same act (a43b-2e).

## Second issue (2026-11-02, `P4-SYSTEM.14` a43b-2e)

`CR-D-XLEN-2` credits `REQ-D-XLEN` through `rv64gc-xlen-forms-v2` by the same act and on the rulings above: the case
re-captured once with its control declared (`truncated-address`, "Predeclared target: the address truncated to 32 bits must
diverge."), every trace and stdout byte-identical to xlen-v1's (a43b-2d). Pinned: the measured record (14,979 B,
`3e536d08…`), the receipt (7,064 B, `fbbfb66f…`), the policy; authority `review`; ten legs; **three** limitations, not
four: the two that named the producer's M text — the receipt's "not all M or CPU acceptance" and the record's control
prose and control-run id — no longer describe the evidence (the receipt names `REQ-D-XLEN`; the record carries the case's
own control). That removal is what the planned lapse was for. Measured: `rv64gc-xlen-forms-v2: DIV-POLICY: satisfied — 10
of 10 legs satisfied; credited by CR-D-XLEN-2`.

## Retirement (2026-11-05, `P4-SYSTEM.14` a43e-1)

`CR-D-XLEN-2` was retired by removal in the commit that opens the window for SSTC ([`decision_sstc-delivery-needs-the-pinned-window.md`](decision_sstc-delivery-needs-the-pinned-window.md)): the typed event binding moved four inputs the case's manifest pins (`schema/matched-case.sexp`, `scripts/matched_gpr_case.py`, `scripts/matched_gpr_comparison.py`, `scripts/matched_gpr_property.py`), and the measure's move a fifth and sixth, so the review reads `invalidated`, 8 of 10 legs. In the same commit `REQ-D-XLEN` records `planned` and the catalogue file leaves with its last records (`REQUIREMENT-STATUS: … 47 planned, 1 not-applicable; 8 case(s), 0 credited, 0 declared, 0 of 0 credit record(s) current; 0 drift`). The rulings above stand for the re-credit: the case is re-captured once as `rv64gc-xlen-forms-v3` and credited through the same act (a43e-5).

## Re-credited (2026-11-05, `P4-SYSTEM.14` a43e-5)

The window closed ([`decision_sstc-delivery-needs-the-pinned-window.md`](decision_sstc-delivery-needs-the-pinned-window.md)). `rv64gc-xlen-forms-v2` was re-captured once as `rv64gc-xlen-forms-v3`, its traces byte-identical to its predecessor's (a43e-4), and `CR-D-XLEN-3` credits it by the same act, on the same rulings and with the same limitations as `CR-D-XLEN-2`. Its ten legs measure `satisfied`. Read this record's claims against `CR-D-XLEN-3` from here on, and `rv64gc-xlen-forms-v2` as history. No dossier copy: `G-TRACE` reads the measured record from `evidence/`.
