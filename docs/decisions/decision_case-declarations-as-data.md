# Case declarations move to data; the credited M case is re-captured once

- **Type:** `decision`
- **Date:** `2026-10-28`
- **Status:** `active`
- **Owner / source:** the director, 2026-10-28 (option B of the P4-0306 finding;
  [`decision_director-rulings-2026-10-28.md`](decision_director-rulings-2026-10-28.md)). Authority `director`.
answers: How does a new matched case get declared without lapsing the credit that rests on a retained capture?

## The fact / decision

A matched case's declaration — its properties (today the `_CASES` table of `scripts/matched_gpr_property.py`)
and its input pins (today `CURATED_INPUTS` of `scripts/capture_div.py`) — moves out of the scripts into data,
one file per case under `evidence/<case>/` read by the tools. Both retained cases pin both scripts in their
dependency manifests; the credited M case is re-captured once under the new manifest, as `v4`. The signed-DIV
case's capture has been `invalidated` since 2026-10-22 and credits nothing, so it stays a historical capture
(corrected in a44-1: this record first said both were re-captured). From then on a new case adds data only and
touches no pinned file. The design: `docs/tasks/P4-SYSTEM.md` `.14` a44-1.

## Why

The P4-0306 finding: declaring the XLEN case the way the M case was declared edits two pinned scripts, which
lapses `CR-GC-M-1` and drops REQ-GC-M to `planned`. Option A would redefine what a retained capture pins;
option C would repeat a lapse and re-credit for every new case. B pays the cost once and removes the cause.

## How to apply

- The re-captures are measurements, not edits: each new capture must reproduce its predecessor's verdicts
  (every property, every witness) with the manifest change as the only declared difference, and the credit
  record is re-issued against the new capture through the crediting act — never carried by hand.
- The tools read the case file and refuse a case that has none; the old in-script tables are removed, not
  kept beside the data (one definition).
- Executed by `P4-SYSTEM.14`, slice a44 first; the XLEN, CSR-SET and SSTC declarations follow as data.
  The ZICNTR program is not covered (it needs a reference with Zicntr).
