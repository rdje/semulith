# The calls on the engineer's own findings are the engineer's, to the director's standard

- **Type:** `decision`
- **Date:** `2026-11-06`
- **Status:** `active`
- **Owner / source:** the director, 2026-11-06, answering the findings surfaced with `SEMULITH-P4-0366`: "All the decisions or calls about your findings shall be yours to make but they got to be sota, signoff, production-grade, and serve the SEMULITH roadmap, goals and objectives long-term."
answers: Who makes the call on a finding the engineer surfaces, to what standard, and what stays the director's?

## The fact / decision

1. **A finding's call is the engineer's.** It is made, recorded in `docs/decisions/` with its measurements, carried out under a task leaf and the normal gate, and reported. It is not left "raised to the director, who may overrule".
2. **The standard is the director's:** sota, signoff, production-grade, serving the roadmap, goals and objectives long-term ([`decision_four-rulings-delegated.md`](decision_four-rulings-delegated.md) set the same standard for its four items).
3. **This widens that record's rule** that an item changing a retained case goes to the director first. Such an item, when it comes from a finding, is now the engineer's too.
4. **It reaches the 17 requirements `decision_obligations-route.md` ends at a ruling.** They are findings of that record: each is called with a measured proposal when its turn comes, and reported.
5. **What stays the director's:** the approval a push needs (`scripts/approved_push.sh`). This ruling says nothing about it.

## Why

A surfaced finding left waiting on the director costs a day and adds nothing the measurements do not already say. The first call under this ruling shows the discipline it asks for: `SEMULITH-P4-0366` had kept a fetch fault out of a case on the claim that it was "one sentence of one requirement". Measured, it is three of the planned requirements, so the call was reversed the same day ([`decision_the-window-that-carries-fetch-faults.md`](decision_the-window-that-carries-fetch-faults.md)).

## How to apply

- Measure before calling, and weigh what the choice costs on its next ten uses.
- A call changing a retained case still goes through a clone first, and every retained capture stays reachable.
- Report the call and its reason at the end of the reply; do not ask for it to be confirmed.
