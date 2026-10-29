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

## Addendum (2026-10-29, `P4-SYSTEM.14` a44-2b): what the switch measured

- The declaration loader (`scripts/matched_gpr_case.py`) returns neutral data and the review maps it onto its
  own records; it imports no record type. The property probe executes a mutated copy of
  `matched_gpr_property.py` as a separate module, and a dataclass compares unequal across two class objects,
  so loader-built records would have shifted every one of its loss counts (measured: all 35 arms unchanged).
- A case's manifest children are its reviewed population counted, not a fixed 64: the declaration
  (`evidence/<case>/case.sexp`), its schema (`schema/matched-case.sexp`) and its reader join the 64, so 67
  for any case today. `matched_gpr_artifacts.MANIFEST_INPUTS` becomes a ceiling of 96 (a population above it
  is refused and is a re-derivation); `capture_div.py` requires the declaration among the pinned children,
  and the review requires the reviewed case to equal the one its pinned declaration bytes declare.
- Binding stays pure: a caller that selected the case passes it to `bind_source_property`, which then opens
  no file; the authority review takes the already-reviewed case, so its traced window still reads exactly
  the 13 current views.
- The switch is split so v4 pins the final code: a44-2b (the tools read the data, the tables removed, the
  censuses re-derived, `CR-GC-M-1` retired) and a44-2c (the checks still specific to the M source — the
  normative-source identity and publication in `review_div_capture.py`, the single obligation in
  `capture_div.py` — become checks against the catalogues, so a non-M case is accepted on its own authority).
