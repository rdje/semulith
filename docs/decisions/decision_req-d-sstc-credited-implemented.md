# `REQ-D-SSTC` is credited `implemented` on the SSTC case, signed by review under delegation

- **Type:** `decision`
- **Date:** `2026-11-05`
- **Status:** `active`
- **Owner / source:** `P4-SYSTEM.14` a43e-5, `SEMULITH-P4-0357`; the workflow under
  [`decision_four-rulings-delegated.md`](decision_four-rulings-delegated.md), carrying out the last step of
  [`decision_state-capture-plan.md`](decision_state-capture-plan.md) through the window of
  [`decision_sstc-delivery-needs-the-pinned-window.md`](decision_sstc-delivery-needs-the-pinned-window.md); the act and its rulings are
  [`decision_req-gc-m-credited-implemented.md`](decision_req-gc-m-credited-implemented.md)'s; the configuration is
  [`decision_reference-config-per-case.md`](decision_reference-config-per-case.md)'s, **raised to the director, who may overrule**.
answers: Who signs the SSTC credit, what does one finite case of 39 witnesses claim, and what does it not claim?

## The fact / decision

1. **Authority.** `CR-D-SSTC-1` in `profiles/rv64gc-lab-v0/credits.sexp` carries `authority review`: the capture plan's
   route for each of the four state requirements.
2. **Sufficiency.** One finite case, `rv64gc-sstc-v1`: 39 predeclared witnesses, a baseline, a byte-identical repeat, one
   control diverging at the predeclared witness (step 172, x11: 0 observed, 32 in the control's expectation), the configuration's
   effect retained (step 8). Its ten legs measure `satisfied` (`rv64gc-sstc-v1: DIV-POLICY: satisfied — 10 of 10 legs
   satisfied`), and that is sufficient for `implemented` and for nothing more: the M rulings' reading of the derivation.
3. **What it claims.** On these finite witnesses, and agreeing with the pinned reference on this configuration: `stimecmp`
   readable in M with both gates clear and holding all 64 bits; S refused with `mcounteren.TM` or `menvcfg.STCE` clear and U refused
   either way, `rd` kept each time; S reading the value M wrote and programming its own; `sip.STIP` following `time` against `stimecmp`,
   unsigned; delivery suppressed with STIE clear, with SIE clear in S, while delegated in M and with STCE clear; delivery from S, from U
   and to M when not delegated; one schedule, S reading `time` and adding 8, landing after 5 of 12 counted instructions; and writing a
   compare above `time` acknowledging it with no M-mode action.
4. **What it does not claim** (the record's `limitations`):

   | Not claimed | Why |
   | --- | --- |
   | a scheduled delivery's latency | The statement guarantees a changed comparison reaches STIP "eventually, but not necessarily immediately". The exact boundary is what both producers do on this configuration, at one tick per instruction. Only the delivery right after an explicit CSR write is normative: the conditions "must also be evaluated immediately following" it. |
   | `mtimecmp` or any M-mode timer | Not witnessed. |
   | `wfi`'s wake | No wait is scheduled in this case: `P4-SYSTEM.5`. |
   | the rate of `time` | The environment contract's (`P4-SYSTEM.5`, `P4-SYSTEM.9`). |
   | a CLINT or any device | It is the reference's source of time for this case, named by the case's overlay; the laboratory declares none. |

5. **The counter rule, read honestly.** The policy asks for "scheduled time/events, delivery boundaries and suppression cases". This is the
   first case to witness all three rather than to say why one does not apply: `FEATURE_DISPOSITIONS["OB-SSTC"]` names every one of the 39
   properties under its part, and the policy probe holds that set equal to the case's declaration, so a witness cannot go unread.
6. **The dependency stays planned, by the plan's order.** `REQ-D-PRIV-MODES` is `planned`; the derivation reads obligations, not dependencies.
7. **No dossier copy**, by the director's ruling ([`decision_dossier-copies-retire-at-the-next-window.md`](decision_dossier-copies-retire-at-the-next-window.md)):
   the record pins `evidence/rv64gc-sstc-v1/measured-experiment.sexp`, and `G-TRACE` lists the case, reading that file.

## Why

- This is what the window was opened for. Option B of [`decision_sstc-delivery-needs-the-pinned-window.md`](decision_sstc-delivery-needs-the-pinned-window.md) would have credited SSTC saying
  delivery was unwitnessed. Under A the case carries delivered interrupts as boundaries of their own, typed and checked: `G-STATE` closes on the requirement's purpose, not around it.
- The plan's first item had delivery and suppression stay corpus-judged, because the override has no timer source. [`decision_reference-config-per-case.md`](decision_reference-config-per-case.md)
  withdrew that on a measurement, and here both are witnessed.

## How to apply

- Any pin movement lapses this credit as it does the other four: the three pins and every input of the case's manifest.
- The retained overlay, effect record and effect trace are read by the policy review on every read. Moving one reads the leg
  pending, and a current credit over a pending measurement is a finding, so the gate fails: never edit them; a new configuration is a new case.
- A later interrupt case needs no format change: a boundary may fetch nothing exactly when its record declares an interrupt delivered there.
