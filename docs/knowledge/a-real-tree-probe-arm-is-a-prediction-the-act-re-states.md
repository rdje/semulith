# My profile change passed the focused set, then the gate refused PROFILE-CONSISTENCY — why?

**Because the gate's self-test reads the real tree, and your change moved what three of its arms
predict.** `scripts/check_profile_consistency.sh --self-test` fires every probe in `scripts/probe_*.py`
and compares each verdict line to a pinned expectation. Most arms run on fixtures and cannot see the
tree. Three kinds can, and a change to a profile's catalogue or evidence re-states them:

- **A real-tree arm.** `probe_requirement_status.py` (`test_real_tree_has_no_drift`) and
  `probe_div_policy.py` (`test_real_tree_measures_as_its_manifest_predicts`) derive the status table and
  the policy measurement from the repository and assert the manifest's prediction of it: how many cases
  are pending, which record credits which case, what the summary line says. They are predictions, not
  fixtures; the act that changes the tree re-predicts them from the measured tree, never loosens them.
- **A mutation arm whose count follows the tree.** `probe_matched_gpr_property.py` builds its fixture
  from the real `REQ-GC-M` record. Under the `derived-status` mutation (the module stops normalising
  the published status out of the semantic authority) the failure count was 2 while the record said
  `planned` and is 36 — every binding — once it says `implemented`. The pinned count lives in the
  `SOURCE_PROPERTY_CASES` table of the self-test; a status change re-states it.
- **A branch the tree has not exercised.** The policy probe's moved-pin branch had never run on the
  real tree. Once a credit record cites the case, a moved method input does more than invalidate the
  measurement: the credit's authentication walks the case's dependency manifest, so the record lapses
  and the gate line gains `FINDING credit … lapsed`, exit 1. Predict it from the code, then exercise it
  by moving one pinned input a byte and restoring it from the index.

The focused set (`cargo xtask focused`, 26 checks) does not include `PROFILE-CONSISTENCY`: the self-test
costs the pre-commit gate's fifty minutes. So the chain reports the three arms only after the gate has
run. Before launching a chain that touches `profiles/` or `evidence/`, run the probes directly, in both
modes, and the mutation arm whose count depends on the record:

```
python3 -B scripts/probe_requirement_status.py && python3 -B -O scripts/probe_requirement_status.py
python3 -B scripts/probe_div_policy.py && python3 -B -O scripts/probe_div_policy.py
python3 scripts/probe_matched_gpr_property.py --mutation derived-status | tail -1   # the count the table pins
```

## What happened

On 2026-10-26 the crediting act (`P4-SYSTEM.14` a42az) added `profiles/rv64gc-lab-v0/credits.sexp` and
recorded `REQ-GC-M` as `implemented`. All 26 focused checks were green; the pre-commit gate refused after
52 minutes with `PROFILE-CONSISTENCY: REFUSED — the check does not discriminate (self-test failed)` and
six MISS lines: the two real-tree arms in both modes, and `RED finite source property derived-status`
expecting 2 failures and seeing 36. The kept log (`target/profile-consistency-selftest.log`, copied to
target/p4-system-14/a42az/gate3/selftest-refusal.log) named every arm — the reason the log is kept
(`a-gate-that-discards-its-self-tests-output-cannot-be-diagnosed.md`). Each arm was re-predicted from the
measured tree; the moved-pin branch was exercised twice on the real tree (a method input, then the
policy pin), each restored and the index content, `.git/config` and HEAD verified unchanged.

## How to apply

- A real-tree arm is part of the act that moves the tree: re-predict it in the same commit, from the
  measured values, and say so in the arm's comment.
- A pinned count that depends on a record's field is a prediction too; name the dependence next to the
  pin so the next status change knows why the number moves.
- Read the kept self-test log first: the MISS lines name the arms; the tracebacks name the values.
