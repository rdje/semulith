# VERIFIED — consumer confirmation for LS-003

**To the LinkedSpec maintainer.** This is the reply to the three first-consumer papercuts
reported in this directory — it travels in the same envelope as the report it answers.

## What you shipped

The integration guide at pin `a8d34c84595d46c24cd1820d5fc0414261706412` remedies all three
observations (the `BACKEND-INTEGRATION-GUIDES` and `CONSUMER-REPORT-DELIVERY` work): a dedicated
*"Applications with a Cargo workspace"* section before any build step; an explicit prerequisite
chain at the top of *"Parse Lispish files in your application"* for readers who arrive there
directly; and the *"Keep preparation and build products local"* section prescribing the
maintained wrapper and application-owned storage. The guide even carries our measured cost of
the recursive-checkout mistake (about 1.7 GB across 30 submodules) as a warning to the next
consumer — thank you for turning one consumer's stumble into everyone's guardrail.

## What we re-ran

Not a script — documentation. The verification is the pin update of `2026-09-26`, which walked
the new guide section by section and exercised each remedy in order: workspace exclusion
(applied, builds no longer stop with the workspace-membership error), the prerequisite chain
(storage, RGX bootstrap, metadata, then build — no step failed), and the maintained wrapper
(`run_cargo_local.sh`, with the bootstrap's exit status checked rather than its progress
banner, per the guide's own warning). The transcript is
[`evidence/verified-a8d34c845.txt`](evidence/verified-a8d34c845.txt); the pin this verification
ran against is the record's `verified-against` `a8d34c84595d46c24cd1820d5fc0414261706412`.

## What it unblocks

Nothing structural on our side — this was a documentation issue, and its cost was measured in
failed first attempts. The next consumer's won't be.

No residue, no follow-up owed; LS-003 is closed with thanks.
