# DEV_NOTES shard — _(2026-09-30)_ … _(2026-09-30)_

> Sharded from `DEV_NOTES.md` when it crossed its 48 KiB ceiling (`doctrine/readme_routes.tsv`).
> Entries in a shard are **never edited after the shard** — git history is canonical.

## _(2026-09-30)_ — the CI two-host matrix; Rosetta comes live mid-slice (P2-SCALAR.9, slice a)

The matrix is a third workflow rather than edits to rust.yml/doctrines.yml: those own
check and enforce; portability owns host-matrix evidence with its own provisioning
(nightly + miri + the BE target on the x86-64 job). The agreement mechanism is the `.8`
contract: both hosts emit the digest manifest (`demo --json` per guest, sha256-chained),
the `agree` job diffs them byte-exactly. The instrument's `--leg` selector makes each CI
job run exactly its leg; the four-leg verdict stays the full-run form. Measured locally:
native leg + manifest emission green, digest byte-identical to the `.8` recording; the
workflow mirrors the existing two (no tabs, three jobs) — CI proof lands at the next
approved push. Mid-slice the director's Rosetta install landed (via VLC's Intel build):
re-measured live (`arch -x86_64` → `x86_64`, the probe binary runs). One trap re-armed
and avoided: editing a running shell script — the restructuring was done quiescent this
time.

Lesson: `promotion: declined` (the workflow's shape is the record).

## _(2026-09-30)_ — the release route decision and the Rosetta measurement (P2-SCALAR.9 opens)

The director picked the two-route answer to the .9 fork: CI matrix permanent + Rosetta
bridge. The measurement that shaped it: Rosetta on macOS 27.0 is present-but-inert —
/usr/libexec/rosetta/ holds oahd/translate_tool/runtime, the x86-64 dyld cache sits in
the Rosetta cryptex (/System/Volumes/Preboot/Cryptexes/Rosetta/…), but the daemon is off
and exec fails (Bad CPU type; translate_tool wants the legacy cache path). External
corroboration for the symptom: the missing dyld_shared_cache_x86_64 is the documented
signature of an unprovisioned Rosetta, and on Tahoe the classic install flag misbehaves
(Jamf field report) — the activation path is recorded in the decision record. The
director's horizon fact (Rosetta phase-out fall 2027) is what makes "bridge, never
foundation" explicit on the record.

Lesson: `promotion: declined` (the decision record IS the durable form).

## _(2026-09-30)_ — the portability matrix and the honest incomplete (P2-SCALAR.8)

The leaf's substance was measurement: Rosetta absent (arch -x86_64 → Bad CPU type in
executable), no qemu user-mode x86-64 runner, Miri present on nightly (809936eac6), the
powerpc64 BE target provisioned. The instrument's first live run reported ALL legs red
against a green reality — the pipefail + grep -q defect (grep -q exits on first match,
cargo dies by SIGPIPE, pipefail reports the pipe's death as the leg's verdict); fixed by
capture-then-read, the pattern now named in the script's comment. A second authoring slip:
editing the script while a run was in flight — bash reads scripts incrementally and hit
the shifted bytes; the honest rerun was clean. The verdict ladder (passed / incomplete /
failed) carries 6 self-test arms. The record is plain-atom portability.sexp, and .9's
release report is the gate that must carry the x86-64 leg's absence. Drift owned: the
model book's bench-arm count went stale across two leaves (44 → 53); fixed, and the fix
is noted here because the book is the review surface.

Lesson: `promotion: declined` (the SIGPIPE rule lives in the instrument's comment; the
self-test enforces the verdict ladder).

