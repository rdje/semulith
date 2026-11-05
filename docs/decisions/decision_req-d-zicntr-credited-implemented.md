# `REQ-D-ZICNTR` is credited `implemented` on the ZICNTR case, signed by review under delegation

- **Type:** `decision`
- **Date:** `2026-11-05`
- **Status:** `active`
- **Owner / source:** `P4-SYSTEM.14` a43c-5, `SEMULITH-P4-0345`; the workflow under
  [`decision_four-rulings-delegated.md`](decision_four-rulings-delegated.md), carrying out item 1 (iii) of
  [`decision_state-capture-plan.md`](decision_state-capture-plan.md); the act and its rulings are
  [`decision_req-gc-m-credited-implemented.md`](decision_req-gc-m-credited-implemented.md)'s; the configuration is
  [`decision_reference-config-per-case.md`](decision_reference-config-per-case.md)'s, **raised to the director, who may overrule**.
answers: Who signs the ZICNTR credit, what does one finite case of 44 witnesses claim, and what does it not claim?

## The fact / decision

1. **Authority.** `CR-D-ZICNTR-1` in `profiles/rv64gc-lab-v0/credits.sexp` carries `authority review`: the capture plan's
   route for each of the four state requirements.
2. **Sufficiency.** One finite case, `rv64gc-zicntr-v1`: 44 predeclared witnesses, a baseline, a byte-identical repeat, one
   control diverging at the predeclared witness (step 109, x21: 21 observed, 102 in the control's expectation), the configuration's
   effect retained (step 6). Its ten legs measure `satisfied` (`rv64gc-zicntr-v1: DIV-POLICY: satisfied — 10 of 10 legs
   satisfied`), and that is sufficient for `implemented` and for nothing more: the M rulings' reading of the derivation.
3. **What it claims.** On these finite witnesses, and agreeing with the pinned reference on this configuration: `cycle`, `time`
   and `instret` and the machine views `mcycle` and `minstret` read in M; each read gated by its own bit of `mcounteren` and
   `scounteren` in S and U; the counters read-only, five write attempts refused with `rd` kept; `instret` moving by what retired, and
   a trap retiring nothing. The requirement and obligation are an inclusion: "The Zicntr base counters (cycle, time, instret) are included".
4. **What it does not claim** (the record's `limitations`):

   | Not claimed | Why |
   | --- | --- |
   | a write through `mcycle` or `minstret` | The spec-side deriver refuses it, and the laboratory's `time` is a view of `mcycle` (`state.sexp`) where the reference's comes from its CLINT, so a write would separate them. Someone must model that before it can be witnessed. |
   | Zihpm's absence | The deriver's vocabulary is the 33. "Zihpm (hardware performance monitors) is not selected" stays a statement of the selection. |
   | rate and progress semantics | The requirement gives them to the environment contract (`P4-SYSTEM.5`, `P4-SYSTEM.9`). The values agree at these boundaries on this configuration, one tick per instruction, which claims no rate. |
   | a CLINT or any device | It is the reference's source of time for this case; the laboratory declares none. |
   | timer delivery | No interrupt or wait is scheduled in this case: `REQ-D-SSTC`. |

5. **The counter rule, read honestly.** The policy's rule asks for "scheduled time/events, delivery boundaries and suppression cases".
   The schedule here is the step boundary itself, a guest count and never host time. The suppression is the trap that retires nothing.
   Nothing is delivered, because nothing is scheduled to be, and the disposition says so rather than stretching the rule (`review_div_policy.py`, `FEATURE_DISPOSITIONS`).
6. **The dependency stays planned, by the plan's order.** The requirement's dependency `REQ-D-PRIV-MODES` is `planned`; the
   derivation reads obligations, not dependencies.
7. **No dossier copy**, by the director's ruling ([`decision_dossier-copies-retire-at-the-next-window.md`](decision_dossier-copies-retire-at-the-next-window.md)):
   `G-TRACE`'s table does not list this case, and the record pins `evidence/rv64gc-zicntr-v1/measured-experiment.sexp`.

## Why

- The route, the vocabulary and the order are the plan's; this is its third step for its third case, and no tool had to change.
- The plan's first item had `cycle` and `time` values stay corpus-judged. [`decision_reference-config-per-case.md`](decision_reference-config-per-case.md) withdrew that on a measurement, and here they
  agree at every read, so the case witnesses the values on this configuration and still claims no rate.

## How to apply

- Any pin movement lapses this credit as it does the other three: the three pins and every input of the case's manifest.
- The retained overlay, effect record and effect trace are read by the policy review on every read. Moving one reads the leg
  pending, and a current credit over a pending measurement is a finding, so the gate fails: never edit them; a new configuration is a new case.
- SSTC (a43d) follows the same way, with delivery and suppression the counter rule's parts it must actually witness.

## Retirement (2026-11-05, `P4-SYSTEM.14` a43e-1)

`CR-D-ZICNTR-1` was retired by removal in the commit that opens the window for SSTC ([`decision_sstc-delivery-needs-the-pinned-window.md`](decision_sstc-delivery-needs-the-pinned-window.md)): the typed event binding moved four inputs the case's manifest pins (`schema/matched-case.sexp`, `scripts/matched_gpr_case.py`, `scripts/matched_gpr_comparison.py`, `scripts/matched_gpr_property.py`), and the measure's move a fifth and sixth, so the review reads `invalidated`, 8 of 10 legs. In the same commit `REQ-D-ZICNTR` records `planned` and the catalogue file leaves with its last records (`REQUIREMENT-STATUS: … 47 planned, 1 not-applicable; 8 case(s), 0 credited, 0 declared, 0 of 0 credit record(s) current; 0 drift`). The rulings above stand for the re-credit: the case is re-captured once as `rv64gc-zicntr-v2` and credited through the same act (a43e-5).
