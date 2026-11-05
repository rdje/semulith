# SSTC's delivery witnesses need a typed event binding, which only a pinned window can add: A, opened 2026-11-05

- **Type:** `decision`
- **Date:** `2026-11-05`
- **Status:** `active` (the director delegated the pick on 2026-11-05, "Pick yourself."; **A** was picked and is being carried out from a43e-1, `SEMULITH-P4-0351`)
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
| **A. Open the window** | About 5 units, proved on a clone (below); the last, for two cases, took five units and 5.5 hours (`a43b-2a` … `a43b-2e`, 2026-11-02). All four credits lapse, G-STATE 3 of 4 → 0 of 4, until each case is re-captured once, byte-identical traces expected | SSTC with real delivery; G-STATE 4 of 4; the riders the director already ruled on (dossier copies retired, `contract_measure` moved out); every later interrupt case needs no further format change, and editing a report never lapses evidence again |
| **B. Credit SSTC without delivery** | 4 units, G-STATE 4 of 4 soon | The policy's rule asks "scheduled time/events, delivery boundaries and suppression cases", so the feature leg would have to say delivery is unwitnessed. The requirement's purpose stays corpus-judged. The next interrupt case hits the same wall with five credits to lapse |
| **C. A parallel chain of case tools** | Avoids the lapse | Forks the pinned tools permanently, two ways to read a case. Rejected |

## The recommendation

**A.** The window's cost grows with each credited case, and this edit is the one the ruling anticipated. Measured against the director's standard: it removes a recurring wall rather than working around it once.

## Measured on a throwaway clone (2026-11-05, a43e-0)

`target/p4-system-14/a43e/prototype.sh` re-creates this from a fresh clone, and nothing it does touches the real tree (`prototype.txt`, `pinned-edits.patch`):

| Step | Result |
| --- | --- |
| The binding, four pinned files | 15 changed lines: `word` and `length` optional; a boundary may fetch nothing exactly when its record declares an interrupt delivered there, and it then writes nothing; every other unfetched boundary stays unsupported |
| The rider, `contract_measure` out | 2 functions and 2 patterns move to `scripts/effective_contract.py`; `gate_report.py` runs after the move; `experiment_verification.py` and `review_div_capture.py`'s reviewed module list take one line each |
| The manifest after both | 67 children, **no report or book generator** |
| SSTC declared, captured | `AGREE`, `AGREE`, the control `DIVERGE step 172 (csrrs x11, sip, x0): Sail {'x11': 0}, expectations {'x11': 32}`; traces byte-identical, 26,417 B; all nine findings matched or satisfied |
| Its effect | `step 8 (rdtime x5): Sail {}, expectations {'x5': 8}` |
| The reviews | method `satisfied`, 88 files; `DIV-POLICY: satisfied — 10 of 10 legs satisfied` |
| The four credits | `4 credit(s), 0 current, 4 lapsed`: the predicted cost, exactly |
| Probes to re-state | three: the derivation probe's "declared events are unsupported" arm, which the binding narrows on purpose, and two case-population lists |

**What it does not prove:** the four re-captures' traces byte-identical to their predecessors. They should be, since none of their steps is a delivery and their guests and configurations do not move, as a43b-2d's were; a difference would be a finding. The prototype's `OB-SSTC` feature disposition is a placeholder.

**The window, then, in four or five units:** (1) the pinned edits, the riders, the deriver's placeholder (a43b-c2) and the four stale requirement statements with `profile.sexp`'s decisions and a contract version that mirrors them (`decision_requirements-bound-to-the-effective-contract.md`, measured 2026-11-05), one commit, the credits retired by removal; (2) `rv64gc-m-forms-v6`, `rv64gc-xlen-forms-v3`, `rv64gc-csr-set-v2`, `rv64gc-zicntr-v2` and `rv64gc-sstc-v1` declared, the family re-derived; (3) the five captured once each on a quiet host, with the three effects; (4) the reviews, the five credits, G-STATE 4 of 4 and `G-TRACE` listing every credited case.

## The pick (2026-11-05)

Asked to pick among A, B and C, the director answered: "Pick yourself." I picked **A**, for the reasons above: it removes the wall instead of working around it, and it costs least now, with four credits to lapse rather than five. The delegation is the authority; the director can overrule it, and the lapse is recoverable at each step, because every retained capture stays in place and a re-capture is a new case.

| Unit | What it does |
| --- | --- |
| a43e-1, `SEMULITH-P4-0351` | the binding, the measure's move, the four credits retired by removal, the dossier copies and `G-TRACE`'s rows out |
| a43e-2 | the deriver's placeholder (a43b-c2), the four stale statements with `profile.sexp`'s decisions and a contract version that mirrors them |
| a43e-3 | five cases declared: `rv64gc-m-forms-v6`, `rv64gc-xlen-forms-v3`, `rv64gc-csr-set-v2`, `rv64gc-zicntr-v2`, `rv64gc-sstc-v1` |
| a43e-4 | each captured exactly once on a quiet host, and the effects of the three on their own configuration |
| a43e-5 | the reviews read them, five credits, `REQ-D-SSTC` `implemented`, `G-STATE` 4 of 4, `gate_report.py` reading each credited record from `evidence/` |

**What a43e-1 found that the prototype did not.** Eight probes moved, not the three predicted: the prototype counted the ones that fail on the binding, and did not run the two that read the measure's module (`probe_gate_runtime_root.py`, which lost all six tests, and `probe_contract_ancestry.py`, whose seam targets the guard that moved) or the three that predict the real tree's credits. And its check accepted a half-fetched boundary on a row declaring a delivery, a step with a length and no word, because it asked whether either field was missing. The real check asks for both, on both arms.

## What holds meanwhile

(Written before the pick; history since a43e-1, except that `sstc-timer.s` still binds nothing until a43e-3.)

- `sstc-timer.s` is in the corpus: useful on every route, and it binds nothing.
- The overlay and the case wait in target/p4-system-14/a43d-3 (`held/`, `draft/`), the case draft's 39 witnesses each already checked against the derivation. A prototype run found one thing the draft could not: the control's witness row must cite the requirement's own source for the policy's first leg, so `sstc-timer.s` cites `RVP-SSTC §12.1` there since a43e-0.
- No credit moves and no pinned file is touched. Other open work continues.
