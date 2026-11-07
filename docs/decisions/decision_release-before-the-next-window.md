# The release decision comes before the next pinned window, and names what that window will carry

- **Type:** `decision`
- **Date:** `2026-11-07`
- **Status:** `active`
- **Owner / source:** `P4-SYSTEM.18`, `SEMULITH-P4-0394`; the engineer's call under [`decision_findings-are-the-engineers-to-call.md`](decision_findings-are-the-engineers-to-call.md), whose note of 2026-11-07 leaves it there.
answers: Should the next pinned window run before or after `rv64gc-lab-v0`'s release decision, and what does that decision still need?

## The question

[`decision_csr-write-three-producers.md`](decision_csr-write-three-producers.md) lists what the next pinned window carries. Its fixes include a real defect in the pinned expectations author. Should a profile be accepted with that list still open?

## What was measured

| Item | Does it change what a credit claims? | Evidence |
| --- | --- | --- |
| The author legalizes `medeleg`, `mtvec` and `stvec` by the table | No. No retained expectation reaches the defect, and it fails safe, as a divergence | 164 guests' writes: 11 `medeleg`, 81 `mtvec` and `stvec`, all inside both masks and MODE 0 |
| The table's `medeleg` narrows to `0xb3ff` | No. The engine's wider mask is legal, and no case writes the bits that differ | The specification lets an implementation choose. The two declarations disagree, which is untidy, not wrong |
| The override's `misaligned_amo AccessFault` | No. Both cases that need it carry it in an overlay | `decision_seven-with-a-switch.md` |
| A probe holding the author to the engine | No. It keeps the class closed | Tooling |
| The author's vocabulary | No. It narrows two named limits, `hstatus` and `pmpcfg0` | `decision_the-seventeen-called.md` |

The window costs 42 case credits lapsing and re-issued. Narrowing the table moves the engine, so `act4.sexp`, `workload.sexp` and `portability.sexp` stop being evidence until each is re-measured, as `decision_recorded-evidence-states-what-it-covers.md` now requires.

## The call

**Release first, then the window, as its own version.**

1. No item changes a claim any credit makes, so nothing accepted would be false.
2. Each item goes into the decision's capability limits by name, so nothing is hidden.
3. `P5-BOARD` and `AG-OS` wait on this gate, and the window's cost does not grow while they run: a board adds no credits to this profile.

Closing the list first would have cost about a day of gated units.

## What the release decision still needs

1. **A hosted matrix run on this tree.** [`decision_release-route-x86-64-leg.md`](decision_release-route-x86-64-leg.md) makes it the x86-64 leg's permanent home. Its last run covered 171 guests, and the tree holds 210. **This needs a push below the 300-commit cadence.** The director allowed it on 2026-11-07, as an exception. The act is `scripts/approved_push.sh`, and `docs/push-approvals.md` records it.
2. **The named decision** (`P4-SYSTEM.18` slice c), recorded in `gate.sexp` as `G-RELEASE`'s evidence, with the versioned artifact digest-pinned. `accepted` only on `passed`, and it never exceeds the report.

## The capability limits it will name

- Finite evidence on named inputs: agreement with the pinned reference, on the declared observations, and no more. Each credit's own limits stand.
- One hart. No board, no boot and no multicore or weak-memory exploration.
- Past the reference, and uncredited: `wfi`'s stall and the fetches it withholds, and faults injected at a chosen suboperation. A reader who holds those clauses must be witnessed reads `REQ-GC-PRIV-INSNS` and `REQ-GC-PARTIAL-PROGRESS` as `partial`.
- The ABI statement holds for what the pinned compiler builds. The retained assembly guests and the ACT suites are tagged soft-float on purpose, because they make no calls across the ABI.
- Everything on the next window's list.
