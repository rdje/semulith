# A stale finite method invalidates the retained case; it does not lock the tree

- **Type:** `decision`
- **Date:** `2026-10-22`
- **Status:** `active`
- **Owner / source:** `P4-SYSTEM.14` a42as, `SEMULITH-P4-0287`; the director's ruling of 2026-10-22
  ("let's follow your recommendation") on the four options raised after a42ar;
  `profiles/rv64gc-lab-v0/EVIDENCE_POLICY.md` "Records, controls and currentness": "Relevant source,
  definition, primitive, adapter, expectation, mask, configuration or build changes invalidate
  dependent evidence." Precedents:
  [`decision_policy-legs-measured-two-pending.md`](decision_policy-legs-measured-two-pending.md)
  (the expected author is a pinned input) and
  [`decision_sail-gpr-comparison-method.md`](decision_sail-gpr-comparison-method.md).
answers: What happens to the gate when one of the retained case's pinned inputs changes, and why is that an invalidation rather than a refusal?

## The fact / decision

The retained case `rv64gc-signed-div-truncation-v2` pins 64 inputs and 4 principals: 35 scripts
(every `matched_gpr_*.py`, `capture_div.py`, the expected author, the shared readers), all 20
`definitions/riscv/*.sexp`, six `profiles/rv64gc-lab-v0` files, four schemas and the guest.
Measured on 2026-10-21: no commit since the capture (c91d08f, 2026-10-19) touched a pinned path,
but 67 of the 68 had commits in the previous 30 days, and the next units — the property binding,
the v3 declaration, P4-SYSTEM.15 to .18 — must edit several. Until a42as,
`scripts/review_div_policy.py` reported a `stale` finite method as `blocked` with exit 1, so
PROFILE-CONSISTENCY refused every commit; and because the finite method's probe and the command
probe asserted the curated capture current on a copy of the tree, the gate's own self-test refused
as well (measured: 32 of 1,086 arms miss after one appended comment line on
`scripts/matched_gpr_property.py`; `target/p4-system-14/a42as/stale-selftest.log`).

The decision, in the policy's own words: a changed pinned input **invalidates** the dependent
evidence. That is a status of the evidence, not a lock on the tree.

1. `scripts/review_div_policy.py` reports a `stale` finite method as the `invalidated` disposition
   with exit 0, naming the first moved declaration in `invalidated_by` and in the summary line; the
   legs that depend on the method (`matched-reference-comparison`, `currentness`) stay pending.
   Exit 1 is kept for a receipt that still claims `qualification` and for a `refused`,
   `unavailable` or `unsupported` method (`blocked`). Nothing is credited; the next capture
   supersedes the invalidated case.
2. The finite method's probe runs its deep arms against a synthetic current retained case built
   once per run from the live modules and the prepared inputs — current declarations, three
   synthetic processes, the measured experiment persisted, the copy's method pinned to it — so
   every seam stays reachable whether or not the curated capture is current. One arm reads the
   curated capture on the real tree and predicts its outcome from the dependency manifest:
   `satisfied` while every pin is current; `stale`, naming the first moved declaration and
   charging one allowance, once a pin moved.
3. The command probe's two real-tree arms predict the same way: with a moved pin the regenerated
   manifest differs from the tracked one in exactly the moved inputs, the tracked declaration pins
   report `mismatch`, and the offline evaluation refuses the current inventory.
4. The requirement status derivation is untouched: an invalidated case credits nothing, so
   `REQ-GC-M` keeps deriving `planned`.

## Why

Four options were weighed. Keeping the block and re-capturing after every pinned edit costs two
commits per edit and forbids any intermediate state. An add-only discipline (parallel modules,
about 1,700 duplicated lines) still leaves the definition and profile edits refused. Narrowing the
pin set is itself an edit to the pinned policy. The chosen reading changes no pin and no evidence:
the measurement says `invalidated` and names what moved, which is exactly what the policy's
currentness rule asks the project to know. The gate keeps refusing what it must — a qualification
claim over an invalidated case, a tampered or unreadable record, a receipt relabelled by hand —
because those are findings about integrity, not about currency.

The self-test consequence is the part that was not visible in the ruling: a probe that asserts the
curated capture current on a copy of the tree is a second lock. Building the deep arms on a
synthetic current capture keeps every RED arm discriminating during the window between a pinned
edit and the capture that supersedes the case; the real-tree arms stay, but they assert the state
the manifest predicts instead of a frozen tree.

## How to apply

- Editing a pinned path is allowed and expected. Run `python3 -B scripts/review_div_policy.py`
  and read `invalidated by …` as the first thing the next capture must re-pin.
- A receipt is never relabelled: the fresh capture is the only way back from `invalidated`.
- When a new case becomes the reviewed one, `scripts/review_div_method.py`'s curated pins change
  with it; the probes need no edit, because their deep arms never depended on the curated bytes.
- A gate that reads the real tree asserts what an independent reading predicts, never that the
  tree has not moved.
