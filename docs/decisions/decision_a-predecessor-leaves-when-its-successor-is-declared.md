# Slice f: one batch, and each predecessor leaves in the unit that declares its successor

- **Type:** `decision`
- **Date:** `2026-11-14`
- **Status:** `active`
- **Owner / source:** `P4-SYSTEM.20` slice f's brief, `SEMULITH-P4-0413`; the open item "how the 46 credits are re-issued in bulk; slice f measures the act per batch" of [`decision_the-next-window-is-version-1.md`](decision_the-next-window-is-version-1.md). The engineer's call under [`decision_findings-are-the-engineers-to-call.md`](decision_findings-are-the-engineers-to-call.md).
answers: How does slice f capture the 42 cases again and re-issue their credits, in what order, under which ids and contract, and what does the order cost?

## What was measured

Two throwaway clones of `438ca348`; the real tree was only read (`target/p4-system-20/f-brief`: `prototype.sh`, `retire_first.sh`, `credit.py`, their `.txt` outputs). In each, the 42 cases naming `rv64gc-lab-env-v3` were re-declared under new ids, each with its id one on, its authority read fresh, its prepared pins re-derived, and its overlay and declared alternative renamed with it. Each was then captured once through `scripts/capture_guarded.py`, its retained effect and walk measured again, and its credit re-issued.

| | Clone 1: predecessors kept until the credits are current (the a49 order) | Clone 2: each predecessor removed in the declaring commit |
| --- | --- | --- |
| Cases at the peak | 86 | 44 (45 with the exception below) |
| Evidence files at the peak | 1,893, against the family's ceiling of 1,101 | 381 at the declaration, 969 after the captures |
| `requirement_status.py` | refuses: `more than 64 evidence cases` | `ok` at every step |
| Captures | 42 of 42 `capture rc=0`, 127 s | 42 of 42 `capture rc=0`, 125 s |
| Full policy review (`--every-retained`) | 100.7 s | 49.7 s |
| After the credits | 46 current, 46 implemented, 2 not applicable; report `incomplete`, 3 of 10 open | the same |

**Behaviour did not move.** In both clones the comparison of all 42 × 22 files with the predecessors finds 506 byte-identical. That covers every trace, stdout, guest image and expectation, the three stderr streams once the trace path that names the case is renamed, and the two reference configurations that already selected slice d's key. The other 418 differ by design: the case file, the three declarations, the three receipts and the two results name the new id (378), and 40 reference configurations carry slice d's key. All 12 retained configuration effects, the ten predicted stale since slice d among them, give traces byte-identical to their predecessors'. Both raw walk traces are byte-identical too. Clone 2 read each predecessor back from the commit before its removal.

**At the report:** with the 42 re-credited, `G-STATE`, `G-TRACE` and `G-OBLIGATIONS` close. `G-REGRESSION`, `G-PORTABILITY` and `G-RELEASE` stay open, and those are slices g and h.

## What measuring found

1. **The peak is what costs.** Kept until the new credits are current, the window holds 86 cases. That breaks two bounds: the evidence family's 1,101 files, which the a49-1 addendum called "the last re-derivation the route needs", and `MAX_CASES = 64` in `scripts/requirement_status.py`, which refuses the whole derivation. Every evidence-walking check also runs at twice its cost for four gated units.
2. **Retiring first is lossless now.** a49 kept its predecessors until the new credits were current, before `retired-cases.md` existed. Since a49-4 each retired directory is listed with its last commit, Git tree and measured digest, and `test_every_retired_case_reads_back_from_history` reads every row back on every run. No credit, report or pinned input reads a predecessor: their credits left at slice a, and `G-TRACE` is open and owned. So a predecessor can leave in the commit that declares its successor, and its bytes stay addressable.
3. **A retired row's holder goes stale when the holder retires.** The test requires each row's "Holds it now" case in the tree. All 25 of the page's rows name a holder this window retires, and the test refused each of them in clone 2.
4. **Two tools default to a retiring case.** `scripts/review_div_method.py` (`RETAINED_CASE_ID`) and `scripts/review_div_policy.py` (`CASE_ID`) name `rv64gc-m-forms-v7`, a captured case the method review reads. Every commit passes the gate, so that case can leave only once its successor is captured. 52 tracked files outside `evidence/` and the records name an old id. The two defaults are the only ones that need a captured case. The fixture reads of the others (a guest, an overlay) are of files a declared successor already holds.
5. **No tool holds a case's contract label to `contract.sexp`.** Census: `git grep -n '\.contract_id\b' -- scripts xtask crates` finds two lines, both in probes. `scripts/matched_gpr_case.py` renders the label, `scripts/matched_gpr_property.py` maps it, and the other `["contract_id"]` reads are of obligation records. The binding that matters is the obligation's semantic digest, which the authority leg authenticates.
6. **The credit catalogue is nearly full.** With all 46 back, `credits.sexp` reaches 63,891 B of its 65,536 B (`DOCUMENT_BYTES`). That leaves room for fewer than two records, and a 47th credit is refused loudly.
7. **A defect in a tool slice f runs.** `scripts/measure_walk_trace.py` reports a failed engine run as `REFUSED: the engine process failed: rc=101` and drops its stderr. In clone 1 that was cargo refusing to build without `.app-data/vendor`, which exits 101 like a panic. The message could not tell the two apart.

## The call

1. **One batch of 42.** The act takes about two minutes of captures. Batches would repeat the declare, capture and credit units, and their probe re-statements, once per batch. Batches of six under the cap would take seven rounds.
2. **Each predecessor leaves in the unit that declares its successor,** listed on `retired-cases.md` from history in the same commit. The one exception is `rv64gc-m-forms-v7`, the review tools' default, which leaves when its successor is captured. The peak is 45 cases, so no family bound moves and the a49-1 addendum's claim stays true. Rejected: the a49 order (two bounds re-derived, four gated units at twice the check cost) and batches under the cap.
3. **Ids one on, contract version 4.** All 42 new ids are unused in history and on the retired list. Each case names `rv64gc-lab-env-v4`, version `4`, the contract in effect when it is declared. Not carried: a check of the label, for which nothing measured shows a need (finding 5).
4. **Three units, features 3 to 5:**
   - **f1:** the 42 declared. 41 predecessors and the 43 reference files named for them leave, listed. The 25 stale holders are re-pointed. The probes' fixtures move to the declared successors, and their real-tree predictions are re-stated: the retained-effect and retained-capture tables hold none until f2. The walk tool's refusal carries the process's last stderr line (finding 7). Rehearsed on a clone before anything is committed.
   - **f2:** each case captured exactly once through the tracked guard and compared with its predecessor, read from history. The 12 effects and the walk are measured again, and `STALE_SINCE_SLICE_D` retires with the cases it named. **Stop condition:** any trace, stdout, guest image or expectation that differs from its predecessor stops the window as a finding.
   - **f3:** the 42 credits re-issued from their last text, `a88b01a0`. Each keeps its limitations, takes the next id, and pins its new case's records and the policy. Their requirements read implemented, the `G-TRACE` rows name the new cases, and the three open items they close leave the manifest. The two defaults move to `rv64gc-m-forms-v8`, and `rv64gc-m-forms-v7` leaves, listed. The catalogue's header is rewritten to the population it now holds.

## What f1 found (2026-11-14, `SEMULITH-P4-0414`)

1. **A correction to finding 4: two predecessors wait, not one.** `scripts/probe_config_effect.py`'s stand-in reference replays
   `rv64gc-csr-set-v3`'s `baseline.trace`, a captured file its successor holds only after f2. The brief's census looked for module
   defaults naming a retiring case, and that read is a fixture's, not a default's. Re-taken over every probe as reads of a
   captured slot from a real case, it finds that one besides the defaults' case. So f1 retires 40, `rv64gc-csr-set-v3` leaves
   with `rv64gc-m-forms-v7` in f3, and the window peaks at 46 cases. No bound moves.
2. **The unit book had drifted since slice a.** `method-adequacy.md`, `policy-adequacy.md`, `requirement-status.md` and
   `references.md` showed version 0's outputs as current, and a census command printed different counts by then (182 and 19,
   not 180 and 21). f1 marks each page as version 0's measurement and moves the three commands that run read-only to
   successors. f3 measures the rest again under the successors.

## What this does not settle

- The 47th credit (finding 6). The catalogue holds the 46. Before a further requirement is credited, its bound must be re-derived or the catalogue split, by the leaf that declares that requirement. The refusal is loud, so it cannot pass silently.
- The hosted run of slice g. A push stays the director's.

## How to apply

- Re-derive on any clone: `bash target/p4-system-20/f-brief/retire_first.sh` from the repository root. It writes only inside its clone.
- A later window that re-captures every case follows this order: a family holding N cases needs room for N plus the defaults that wait, not 2N.
