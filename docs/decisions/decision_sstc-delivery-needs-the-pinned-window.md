# SSTC's delivery witnesses need a typed event binding, which only a pinned window can add: open for the director

- **Type:** `decision`
- **Date:** `2026-11-05`
- **Status:** `active` (open: the director picks; the reversible default holds meanwhile)
- **Owner / source:** `P4-SYSTEM.14` a43d-3, `SEMULITH-P4-0347`; raised on the rule of [`decision_four-rulings-delegated.md`](decision_four-rulings-delegated.md) that an item changing a retained case goes to the director first, and read against item 4 of
  [`decision_dossier-copies-retire-at-the-next-window.md`](decision_dossier-copies-retire-at-the-next-window.md) ("It rides with the next pinned edit that is needed anyway").
answers: Why can the SSTC case not be written on the current tools, what would change that, what does each route cost, and what holds until the director picks?

## The fact

`sstc-timer.s` agrees on all three producers: the spec-side author writes 315 steps, the lab engine matches them (`every_guest_matches_its_expectations`), and the pinned Sail reads `AGREE 315 declared steps` on the case's configuration. Its case cannot be rendered, and the refusal is by design:

| Where | What it says |
| --- | --- |
| `schema/matched-case.sexp` | a `step` has an integer `word` and `length`; a delivered interrupt fetches nothing |
| `scripts/matched_gpr_case.py:190` | renders both, and fails on `None` |
| `scripts/matched_gpr_property.py:445` | `_reviewed_step` requires an integer for each |
| `scripts/matched_gpr_comparison.py:277`, `:295` | "declared event boundaries need typed event binding"; "unfetched boundaries need typed event binding" |

The book has said so since the first consumer: "any source boundary without a complete fetched instruction, need a later typed event binding" (`references.md`). `grep -c` in each of the four credited cases' manifests: 1 for all four files. So moving any of them lapses every credit. The deriver needs no change, and the Sail adapter already parses deliveries.

## The options

| | Cost | Result |
| --- | --- | --- |
| **A. Open the window** | About 6 units; the last, for two cases, took five units and 5.5 hours (`a43b-2a` … `a43b-2e`, 2026-11-02). All four credits lapse, G-STATE 3 of 4 → 0 of 4, until each case is re-captured once, byte-identical traces expected | SSTC with real delivery; G-STATE 4 of 4; the riders the director already ruled on (dossier copies retired, `contract_measure` moved out); every later interrupt, wait or fetch-fault case needs no further format change |
| **B. Credit SSTC without delivery** | 4 units, G-STATE 4 of 4 soon | The policy's rule asks "scheduled time/events, delivery boundaries and suppression cases", so the feature leg would have to say delivery is unwitnessed. The requirement's purpose stays corpus-judged. The next interrupt case hits the same wall with five credits to lapse |
| **C. A parallel chain of case tools** | Avoids the lapse | Forks the pinned tools permanently, two ways to read a case. Rejected |

## The recommendation

**A.** The window's cost grows with each credited case, and this edit is the one the ruling anticipated. Measured against the director's standard: it removes a recurring wall rather than working around it once.

## What holds meanwhile

- `sstc-timer.s` is in the corpus: useful on every route, and it binds nothing.
- The overlay and the case wait in target/p4-system-14/a43d-3 (`held/`, `draft/`), the case draft's 39 witnesses each already checked against the derivation.
- No credit moves and no pinned file is touched. Other open work continues.
