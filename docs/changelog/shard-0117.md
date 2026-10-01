# DEV_NOTES shard — _(2026-09-30)_ … _(2026-09-30)_

> Sharded from `DEV_NOTES.md` when it crossed its 48 KiB ceiling (`doctrine/readme_routes.tsv`).
> Entries in a shard are **never edited after the shard** — git history is canonical.

## _(2026-09-30)_ — the Rosetta proof: the x86-64 leg green under translation (P2-SCALAR.9, slice b)

The leg's two halves were measured separately: the fixtures cross-compiled for
x86_64-apple-darwin and ran green under Rosetta (cargo test --target, rc=0), and the
agreement contract — the digest manifest — matched the aarch64 recording byte-for-byte
(0670a01b…5bb52; the demo --json fingerprints are architecture-independent by
construction: addresses and values, no host bytes). The instrument's verdict strings
gained annotations ("green (Rosetta translation; …)"), so the ladder's normalization
learned prefix matching — a one-line fix with the self-test re-run. The record's verdict
moved incomplete → passed with the nuance preserved: the bare-metal leg is the CI
matrix's ubuntu job, landing at the next approved push; Rosetta expires fall 2027 and is
the bridge only. Also owned: slice (a)'s LOCKSTEP claimed a plan/p2.md line that commit
never carried — the .9 book section lands with (b) and the miss is on the record.

Lesson: `promotion: declined` (the normalization fix is measured by the self-test).

