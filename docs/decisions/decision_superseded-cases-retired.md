# The superseded cases leave the tree, listed, and their list reads back from history

- **Type:** `decision`
- **Date:** `2026-11-06`
- **Status:** `active`
- **Owner / source:** `P4-SYSTEM.14` a49-4, `SEMULITH-P4-0371`; the last unit of [`decision_the-window-that-carries-fetch-faults.md`](decision_the-window-that-carries-fetch-faults.md), the engineer's call under [`decision_findings-are-the-engineers-to-call.md`](decision_findings-are-the-engineers-to-call.md).
answers: Which case directories left, why was that safe, which two stayed, how does the repository know nothing was lost, and does the family's cap move?

## The fact / decision

1. **What left.** 23 superseded case directories, 3,700,566 B in 506 files, and the 16 overlay and effect files named for them, 118,103 B. Two more had left at a49-1, when their guests changed in place. `docs/models/rv64gc-lab-v0/src/retired-cases.md` lists all 25 and all 16.
2. **Why that was safe.** No credit, report or pinned input read any of them: `python3 -B scripts/credit_records.py --profile rv64gc-lab-v0` reads `23 credit(s), 23 current, 0 lapsed` before and after, and the status still derives 23 `implemented`, 24 `planned`, 1 `not-applicable`. The order was the window's: nothing was deleted until the new credits were current.
3. **What stayed.** `rv64gc-signed-div-truncation-v2` and `rv64gc-m-forms-v3` credit nothing either. `scripts/matched_gpr_property.py`, which every case's manifest pins, names them as `CASE_ID` and `M_FORMS_CASE_ID`, so removing them would lapse every credit for no gain. They can leave at the next window that has to move that file anyway. This is not a reason to open one.
4. **How nothing is lost.** The page holds, per case, the last commit, the directory's Git tree and the measured record's sha256, and, per file, the last commit and sha256. `test_every_retired_case_reads_back_from_history` in `scripts/probe_div_capture_inputs.py` reads every row back from history on every run, and holds each listed directory and file absent from the tree. A copy without full history skips it and says so: `git rev-parse --is-shallow-repository`. CI's doctrine job fetches at depth 0, so it judges.
5. **The cap does not move.** 551 files of 1101, 25 cases of 50. The record that set it said this would hold for the rest of the route, and the route's remaining cases fit it. Re-deriving it downward now would only force an upward re-derivation at the next window, so it stands until a measurement says otherwise.

## Why

Each directory cost a pass of every doctrine that walks `evidence/`, and the gate had reached 28.7 minutes at 48 cases, against a tripwire of one minute per added case. Retained history in the tree also misled: a reader of `evidence/` saw 48 cases and could not tell which 23 mattered, and the book's own examples kept naming cases the review had stopped reading.

Git already keeps these bytes, addressed by content. What it does not keep is the knowledge that they matter, or which commit holds them, so the list and its check are the part worth adding. A Git tree id covers all 22 files of a directory with one value, so a row is short and a single flipped byte in any file fails it.

## How to apply

- To read a retired case: `git show <last commit>:evidence/<case>/<file>`. The page shows it worked through.
- To retire another: add its row before removing it, from history, with the same columns. The test counts the rows, so a row added or dropped moves its count in the same commit.
- A page that says what was measured on a retired case stays as it is: that is a record of what ran. A command the book offers to run must name a case in the tree.
