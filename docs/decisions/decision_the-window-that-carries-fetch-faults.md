# A case learns to carry a fetch fault now, in one window with what else only a window can move

- **Type:** `decision`
- **Date:** `2026-11-06`
- **Status:** `active`, opened by `P4-SYSTEM.14` a49-0, `SEMULITH-P4-0367`, carried out from a49-1, `SEMULITH-P4-0368`
- **Owner / source:** the engineer's call under [`decision_findings-are-the-engineers-to-call.md`](decision_findings-are-the-engineers-to-call.md); it reverses option B of `decision_obligations-route.md`, "What the `defined` remainder found", and follows the reasoning of [`decision_sstc-delivery-needs-the-pinned-window.md`](decision_sstc-delivery-needs-the-pinned-window.md).
answers: Why open a pinned window now, what does it carry, what does it cost, and what did the clone prove?

## The fact

A case's step fetches a word of a length or is a delivery boundary. A fetch fault retires nothing and may read one parcel first, so it is neither (`matched_gpr_case.read_document`, `matched_gpr_comparison.compare_source_expectation`), and both files are among a case's pinned children. `SEMULITH-P4-0366` chose to witness around that, calling it "one sentence of one requirement". That was a claim, not a measurement:

| Measured | Result |
| --- | --- |
| Planned requirements whose statements state a fetch fault | 3: `REQ-GC-C`'s second-parcel report, `REQ-D-FAULT-PRIORITY`'s first adjacent pair, `REQ-GC-PARTIAL-PROGRESS`'s straddling fetch |
| Corpus guests with a fetch-fault step | 4: `c-page-end`, `c-page-straddle`, `it-prio-jump`, `sv39-perm-rwx` |
| Credits a later window would lapse | 19 now, 23 after Batch II-b, up to 47 |
| The adapter | Already reads a fetch fault: only the case tools refuse it |

So the wall recurs, and a window is coming anyway. A window's cost grows with each credit, so the cheapest moment is before Batch II-b is captured.

## The options

| | Cost | Result |
| --- | --- | --- |
| **A. Open it now** | 19 credits lapse until re-issued; three gated units | `REQ-GC-C`, `FAULT-PRIORITY` and `PARTIAL-PROGRESS` witness their faults; the wall is gone |
| B. Witness around it, as P4-0366 did | Three requirements credited with a named hole, or held back | The first row of the priority table goes unwitnessed |
| C. Wait for the next pinned movement | That window lapses 23 or more | The same work, later, for more |

**A.** It removes the wall, at its lowest price.

## What the window carries

A window is the only cheap time to move a pinned file, so it takes what else needs one, and no more:

1. **The fetch fault as a typed event.** A wordless boundary writes nothing; a delivered interrupt reads no parcel, and a fetch fault reads none or one. The adapter now also holds a fault's spelling to its cause, 12 or 1. A wait stays unsupported: Sail does not stall on `wfi`.
2. **`MAX_PROPERTIES` from 64 to 96.** `ATOMICS`, `F` and `D` met 64, and `F` and `D` dropped witnesses for it: FCLASS's other classes, FMIN with two NaNs. At 64 witnesses `d-forms`' `case.sexp` is 50,723 B of 65,536 B, so 96 fits; 128 would not. The prepared-input bound stays: dropping a sentinel that a changing value does not need makes the room.
3. **A statement-trace leg, the eleventh** (`EVIDENCE_POLICY.md`, pinned, so only now). Every clause of a requirement's statement must trace to declared properties or to a limit the case names. `decision_obligations-route.md` records why: first drafts covered every form, agreed with Sail on every step, and missed most of what the statements say, and the review could not see it. Annotation is not proof of semantics (EVD-06), but an omission can no longer pass silently. The 23 statements total 9,261 characters.
4. **Superseded captures leave the tree, and stay in history**, in a unit of their own once the new credits are current, so the old evidence is there until then. Each case costs every later gate about 9 to 20 seconds. Each directory that goes is listed with its last commit and digests, so that it can be read back with `git show`. Two stay: `rv64gc-signed-div-truncation-v2` and `rv64gc-m-forms-v3`, the tools' default case and their real fixture in 75 places and the book's worked example; moving those defaults is a churn with no gain.

**Not carried:** the prepared-input bound, a wait boundary, and any further tool change. A rider needs a measured need.

## Measured on a throwaway clone (a49-0)

`bash target/p4-system-14/a49-0/prototype.sh`, nothing touching the real tree (`prototype.txt`):

| Step | Result |
| --- | --- |
| The pinned edits | 8 files; `CREDIT-RECORDS: … 19 credit(s), 0 current, 19 lapsed`, the predicted cost exactly |
| 23 cases declared and captured | 19 re-issued and Batch II-b, `c-forms` with its faults back: 23 of 23 `capture rc=0`, in 42 s in all |
| Against the predecessors | **171 files byte-identical, 0 differ**: every trace, stdout stream, image and expectation of the 19 |
| The reviews | 23 of 23 `10 of 10 legs satisfied`; each control diverging at the same step as before |
| The three effects | `csr-set` step 34, `zicntr` step 6, `sstc` step 8, as before |
| Probes to re-state | 9 of the 12 run: 8 by their populations and predictions, and `DIV-CAPTURE-INPUTS` by the family's cap, which item 4 resolves |

**What it does not prove:** the statement-trace leg and the wider programs, written next, and rehearsed again before anything real moves.

## The units

| Unit | What it does |
| --- | --- |
| a49-0, `SEMULITH-P4-0367` | this record and the ruling; nothing moves |
| a49-1 | the window opens: pinned edits, the policy and its leg, the 19 credits retired by removal, 23 cases declared, the family's cap re-derived for its peak |
| a49-2 | each captured exactly once, and three effects retained |
| a49-3 | the reviews, 23 credits, `G-STATE` and `G-TRACE` restored |
| a49-4 | the 23 superseded directories left in the tree out, listed with their commits and digests |

**Between a49-1 and a49-3, `G-STATE` reads 0 of 4 and `G-TRACE` is open.** That is the cost, it is recoverable at each step, and it is what the numbers are for. Any trace of an unchanged guest that differs from its predecessor stops the window as a finding.

## What a49-1 found (2026-11-06)

**The trace paid for itself before it was committed.** Written clause by clause against the 23 statements, it found behaviour the ten legs had passed in two credited requirements, and one with no limit named (`policy-adequacy.md`, "The eleventh leg"). Each is witnessed or named now, and the cheapest moment to fix them was this one: all 19 were being re-issued anyway. `rv64gc-csr-access-v2` and `rv64gc-fencei-v2` therefore run new programs, the only two of the 19 whose traces will differ from their predecessors; `F` and `D` go to 90 and 93 witnesses, and all ten FCLASS classes, FMIN's NaN rules and the fused invalid rule are in.

**Two predecessors left early.** `csr-access.s` and `fencei-forms.s` changed in place, so `rv64gc-csr-access-v1` and `rv64gc-fencei-v1`, whose declarations pin the old bytes, read `refused` rather than `stale`. They left the tree at a49-1, recoverable from `82498e5e`, and a49-4 retires the other 23.

**Arms that named a real case.** The credit arms of `gate_report.py --self-test` and three tests of `test_gen_model_book.py` named real credited cases, so no window could hold them. They judge a stub now, and name none: authenticating a credit is `CREDIT-RECORDS`', and how a report reads one is theirs. That removes this cost from every later window. `probe_dossier_qualification.py`'s frozen credit now follows its mirror's policy, as its manifest already did.

**The family's cap, once more:** 50 cases, the peak, `decision_evidence-family-two-cases.md`'s tenth re-derivation.

**The rehearsal earned its place again.** On a throwaway clone of the staged tree, 23 of 23 captured in 40 s, and all 153 files compared with the 17 unchanged predecessors are byte-identical. It also found what the probes could not: `review_div_policy.py` still refused a case above 64 properties, after the tools moved to 96, and `F` and `D` are above it. That review imports no pinned tool, so it keeps its own constant, and a probe now holds the two equal. Nothing real had been captured.

## The captures (a49-2, 2026-11-06)

Each of the 23 once, 1.2 s to 1.6 s, each control where declared. **All 153 files compared with the 17 unchanged predecessors are byte-identical, every compared file of all 23 matches its rehearsal, and the three effect traces match their predecessors': no finding.** So the window's edits changed no behaviour of any unchanged guest, which is the question its stop condition asked.
