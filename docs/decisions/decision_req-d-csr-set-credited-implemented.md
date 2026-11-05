# `REQ-D-CSR-SET` is credited `implemented` on the CSR-SET case, signed by review under delegation — the first `implementation-defined` requirement

- **Type:** `decision`
- **Date:** `2026-11-04`
- **Status:** `active`
- **Owner / source:** `P4-SYSTEM.14` a43b-3h, `SEMULITH-P4-0340`; the workflow under
  [`decision_four-rulings-delegated.md`](decision_four-rulings-delegated.md), carrying out item 1 (iii) of
  [`decision_state-capture-plan.md`](decision_state-capture-plan.md); the act and its rulings are
  [`decision_req-gc-m-credited-implemented.md`](decision_req-gc-m-credited-implemented.md)'s; the configuration is
  [`decision_reference-config-per-case.md`](decision_reference-config-per-case.md)'s, **raised to the director, who may overrule**.
answers: Who signs the CSR-SET credit, what does one finite case of 53 witnesses claim, what does it not claim, and why is its measured record not copied into the dossier?

## The fact / decision

1. **Authority.** `CR-D-CSR-SET-1` in `profiles/rv64gc-lab-v0/credits.sexp` carries `authority review`: the capture plan's
   route for each of the four state requirements ("reviewed, credited (`authority review` under the 2026-10-26 delegation)").
2. **Sufficiency.** One finite case, `rv64gc-csr-set-v1`: 53 predeclared witnesses, a baseline, a byte-identical repeat, one
   control diverging at the predeclared witness (step 130, x28: 5 observed, 9 in the control's expectation), the configuration's
   effect retained (step 34). Its ten legs measure `satisfied` (`rv64gc-csr-set-v1: DIV-POLICY: satisfied — 10 of 10 legs
   satisfied`, a43b-3g), and that is sufficient for `implemented` and for nothing more: the M rulings' reading of the derivation.
3. **What it claims.** The committed 33 are implemented and agree with the pinned reference on this configuration, the aliases
   hold, and a refused access commits nothing in M, S and U, on these finite witnesses. Requirement and obligation are a
   membership: "The implemented CSR set is the committed minimum of 33".
4. **What it does not claim** (the record's `limitations`):

   | Not claimed | Why |
   | --- | --- |
   | `mip`'s value directly | The case's CLINT holds `mip.MTIP`, so `mip` is read with `rd` = x0 and its bits are witnessed through `sip`. |
   | a CLINT or any device | The device is the reference's source of time for this case; the laboratory declares none. |
   | a non-member address trapping | The spec-side deriver's vocabulary is the 33, and it is a pinned input (the plan's addendum). The negative side is the refused write and the privilege-refused access. |
   | field semantics, counter rates, timer delivery, numerics | `P4-SYSTEM.2`, `REQ-D-ZICNTR`, `REQ-D-SSTC`, the F and D cases. |

5. **The dependencies stay planned, by the plan's order.** The requirement's `dependencies` name `REQ-D-PRIV-MODES`,
   `REQ-D-ZICNTR` and `REQ-D-SSTC`, all `planned`; the derivation reads obligations, not dependencies, and the plan's item 4
   orders CSR-SET before ZICNTR and SSTC. The credit says so: it is membership, and it does not stand for their semantics.
6. **The dossier copy is left out; the director ruled on 2026-11-04** ([`decision_dossier-copies-retire-at-the-next-window.md`](decision_dossier-copies-retire-at-the-next-window.md)). The plan's step (iii) records each case's measured
   record in `references.sexp`, and the M and XLEN cases' are there. CSR-SET's does not fit:

   | | Bytes |
   | --- | --- |
   | `references.sexp` today | 50,323 |
   | CSR-SET's measured record | 27,346 |
   | Together | 77,669 |
   | The per-part ceiling for an authored file in `profiles/` | 65,536 |

   Splitting the file or reading the record from `evidence/` needs a change to `scripts/gate_report.py` or `scripts/dossier_sexp.py`,
   and every credited case's manifest pins both, so either change lapses all three credits. The ceiling is a team decision
   (`doctrine/readme_routes.tsv`: "PER-PART STAYS 65,536"). So this act leaves the copy and its `G-TRACE` row out, which claims
   less and forecloses nothing: the derivation credits through the record, `evidence/<case>/measured-experiment.sexp` owns the
   bytes and the record pins them, the method review validates the same graph on every read, and `G-TRACE` stays green on the
   other two records. `G-TRACE`'s table simply does not list this case until the question is answered.

## Why

- The route, the vocabulary and the order are the plan's; this is its third step for its second case.
- Crediting the requirement and holding back only the mirror keeps the status true: the status is derived from a record, and a
  missing mirror changes no evidence.

## How to apply

- Any pin movement lapses this credit as it does the other two: the three pins and every input of the case's manifest.
- The retained overlay, effect record and effect trace are read by the policy review on every read. Moving one reads the leg
  pending, and a current credit over a pending measurement is a finding, so the gate fails: never edit them; a new configuration is a new case.
- The question (a43b-c3) is answered: the copy stays out until the next pinned window, which retires all the copies ([`decision_dossier-copies-retire-at-the-next-window.md`](decision_dossier-copies-retire-at-the-next-window.md)).

## Retirement (2026-11-05, `P4-SYSTEM.14` a43e-1)

`CR-D-CSR-SET-1` was retired by removal in the commit that opens the window for SSTC ([`decision_sstc-delivery-needs-the-pinned-window.md`](decision_sstc-delivery-needs-the-pinned-window.md)): the typed event binding moved four inputs the case's manifest pins (`schema/matched-case.sexp`, `scripts/matched_gpr_case.py`, `scripts/matched_gpr_comparison.py`, `scripts/matched_gpr_property.py`), and the measure's move a fifth and sixth, so the review reads `invalidated`, 8 of 10 legs. In the same commit `REQ-D-CSR-SET` records `planned` and the catalogue file leaves with its last records (`REQUIREMENT-STATUS: … 47 planned, 1 not-applicable; 8 case(s), 0 credited, 0 declared, 0 of 0 credit record(s) current; 0 drift`). The rulings above stand for the re-credit: the case is re-captured once as `rv64gc-csr-set-v2` and credited through the same act (a43e-5).

## Re-credited (2026-11-05, `P4-SYSTEM.14` a43e-5)

The window closed ([`decision_sstc-delivery-needs-the-pinned-window.md`](decision_sstc-delivery-needs-the-pinned-window.md)). `rv64gc-csr-set-v1` was re-captured once as `rv64gc-csr-set-v2`, its traces byte-identical to its predecessor's (a43e-4), and `CR-D-CSR-SET-2` credits it by the same act, on the same rulings and with the same limitations as `CR-D-CSR-SET-1`. Its ten legs measure `satisfied`. Read this record's claims against `CR-D-CSR-SET-2` from here on, and `rv64gc-csr-set-v1` as history. No dossier copy: `G-TRACE` reads the measured record from `evidence/`.
