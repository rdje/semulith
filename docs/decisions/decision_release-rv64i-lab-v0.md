# The rv64i-lab-v0 release decision: an EXPERIMENTAL release of the versioned evidence artifact, not an accepted profile

- **Type:** `decision`
- **Date:** `2026-09-30`
- **Status:** `active`
- **Owner / source:** `P2-SCALAR.9` (`G-RELEASE`), applying `docs/EVIDENCE_AND_GATES.md`
  §7 and the gate series to the measured state; the route for the portability axis is
  `decision_release-route-x86-64-leg` (director, same day).

## The decision

`rv64i-lab-v0` version 0 is released as a **versioned experimental evidence artifact** —
the dossier plus its measured evidence package, digest-pinned in the CPU-LAB report —
and is explicitly **NOT an accepted/validated CPU profile**. The name is the decision:
"experimental release v0", not "acceptance".

## Why (the measured axes, 2026-09-30)

- **Green axes, measured:** G-INTERACTIONS (21/21 cells, gated), G-REGRESSION (the
  corpus 642/642 three-way, the ACT4 campaign 51/51 recorded, the mutation suite
  commit-gated), G-PORTABILITY (`passed` — four legs green; the x86-64 leg under Rosetta
  2 translation with the byte-identical manifest, the bare-metal CI leg landing at the
  next approved push), G-REPLAY (bundles + mid-execution snapshots, commit-gated),
  G-TRACE (commit-gated).
- **Open axes, measured:** G-CONTRACT (72 declared obligation checks, 0 implemented —
  the G0 probe, re-derived) and G-OBLIGATIONS (28 requirements measured
  `implementation_status: planned`, 1 research `partial`). The obligations axis cannot
  read complete on the record's own terms, so EVD-08 forbids `passed` and the profile
  stays experimental. No waiver exists for this and none was adopted.
- **What "accepted" would require:** the obligation fixtures implemented (the declared
  72 checks), the requirements' statuses re-derived as implemented where the evidence
  supports it, and the bare-metal x86-64 CI leg green. All three are future leaves,
  named here so the next evaluator never re-derives the gap list from memory.

## What the artifact is and is not

- **Is:** the complete, reproducible laboratory record for the first RV64I profile — the
  dossier, the corpus, the external campaign record, the gate reports — content-digested
  in `profiles/rv64i-lab-v0/GC-REPORT.md` and re-derivable from pinned inputs.
- **Is not:** a conformance claim, a validated-CPU claim, or evidence for any other
  profile or host beyond the recorded ones. "Supports RV64I" appears nowhere.
