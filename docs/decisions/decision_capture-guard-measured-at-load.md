# The capture guard's load limit is 32, because it was measured

- **Type:** `decision`
- **Date:** `2026-11-06`
- **Status:** `active`
- **Owner / source:** `P4-SYSTEM.14` a50-3, `SEMULITH-P4-0374`; revises the guard of [`decision_sstc-delivery-needs-the-pinned-window.md`](decision_sstc-delivery-needs-the-pinned-window.md); the call is the engineer's under [`decision_findings-are-the-engineers-to-call.md`](decision_findings-are-the-engineers-to-call.md).
answers: What did the capture guard's load limit protect, what was measured, and what holds now?

## The fact / decision

1. **The limit moves from 8 to 32.** Before each case the 1-minute load must be below 32 and 50 of 50 children must spawn and reap the collector's way. The guard's other holds stay: a clean tree, frozen paths unmoved, declarations equal to their regeneration, the preflight ready, no retry, and ten minutes at most before stopping with nothing spent.
2. **What forced the question.** The seven's captures waited 2 h 20 min on 2026-11-06 while sibling projects held the host, at load 10 to 47 whenever the guard sampled it. The work itself takes ten seconds.
3. **What was measured,** on a throwaway clone of the declaration commit, so no case id was spent (`target/p4-system-14/a50-3/load-rehearsal/`):

   | Measure | Result |
   | --- | --- |
   | Captures of the seven, 30 rounds | 210 |
   | Load while they ran | 14.94 to 72.99, median 18.94; 199 at or above 16, 27 at or above 24, 26 at or above 32 |
   | Non-zero exits; `Operation not permitted` mentions | 0; 0 |
   | Seconds per capture | 1.43 to 12.86, median 1.75, beside `PROCESS_SECONDS = 30` for each of its three processes |
   | Upper bound on the refusal rate, 95% | 1.4% per capture |

4. **The real captures then ran under the new limit:** load 21.00 to 25.65, 1.2 s to 1.4 s each, `rc=0` each, and all 77 compared files byte-identical to a rehearsal made earlier on another clone.

## Why

- **A refused capture costs little and misleads nobody.** The failure this guards against is a refusal, never a false success. The case stays recoverable as a new case with a new declaration commit, and since [`decision_superseded-cases-retired.md`](decision_superseded-cases-retired.md) a spent directory can leave the tree with its history listed. Against that, the wait had no bound.
- **32, not 73.** 184 of the 210 ran below 32 and 26 above it, so the limit keeps a margin inside the measured range. One gate's self-test arm also missed at about load 35 at a50-2, unattributed.
- **The spawn probe stays,** because it measures the operation directly, where load is only a proxy.

## What this does not claim

- 0 of 210 bounds the refusal rate. It does not make the rate zero, and the call site of the load-sensitive refusal is still unidentified (`target/p4-system-14/collector-race/FINDING.md`).
- The rehearsal's per-round digest covered `verification.json`, which carries process ids, so it cannot show the 210 rounds byte-identical. What shows bytes unmoved is narrower: three further runs of `rv64gc-priv-modes-v1` with 21 of 22 files identical and `verification.json` differing in process ids only, and the seven's real captures against their rehearsal.

## How to apply

- If a capture refuses, read its `capture.err`, trace it as `FINDING.md` says, never retry, and declare a new case.
- A load above the limit still holds for ten minutes at most and spends nothing. Re-run the guard, which skips any case already holding `verification.json`.
- **The guard is scratch, and that is a gap.** Every capture since a43e-4 used a copy of it under `target/`, which git does not track, so a lost `target/` would lose the procedure. `a50-c2` moves it to a tracked script before the next capture.
