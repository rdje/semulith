# CHANGELOG shard — SEMULITH-SF-0051 … SEMULITH-AC-0050

> Sharded from `CHANGELOG.md` when it crossed its 64 KiB ceiling (`doctrine/readme_routes.tsv`).
> Entries in a shard are **never edited after the shard** — git history is canonical.

## SEMULITH-SF-0051 (leaf SOT-FORMAT.9) — the pin moves, the readers agree, the loop closes

Director instruction `2026-09-26`: upstream fixed and pushed the reported bugs, so the LinkedSpec
pin advances `ad290bdb4` → `a8d34c845` (`origin/main` tip, ~120 commits). The update followed the
guide's own flow — fetch, check out the reviewed revision, re-verify, THEN commit the pointer.
RGX stays at `8763a0e6` on both pins (bootstrap: "already generated", a no-op); the consumer
rebuilt in 20.39 s.

**LS-001 is `verified`, not just `fixed-upstream`.** Our self-contained reproduction re-ran
against the new binary and grammar: `8 matched / 0 differed` (was 4/4), and both readers now
agree on **all five** tracked `.sexp` files, including the 43-form catalogue that had read as 6.
The issue record, both index mirrors and the REPORT carry the `verified-against` pin the
UPSTREAM-INDEX gate requires.

**The fix moved the disagreement one layer down, and that layer is enumerated, not hidden.**
The corpus census found exactly four residue atoms in `materials/catalog.sexp`: two
quoted-numeric strings (`"20260911"`, `"1992"` — Lispish discards quote-kind, LS-002) and two
escape-retained strings (`\"` kept verbatim — the guide documents this). Both are CLASS families
in `compare_readers.py` now: each is anchored to exact byte meaning (`sexp._atom(A) == B`
exactly; decoding B with sexp.py's own escape table reproduces A exactly), with 9 new self-test
arms (4 GREEN classification, 5 RED masking) and a fired RED proof — the pre-fix grammar still
makes the comparator report the original 43-vs-6 defect, rc=1. "Agree" still means same structure.

**Named departure, one.** The guide now prescribes copying the consumer source into the
application's crate; semulith builds the vendored example workspace in place (virtual root
manifest has no package to own it) — recorded in the tree, to revisit when the engine adopts the
reader. Upstream's document grammar (SExprDocumentV1, tagged kinds) is the durable answer to both
CLASS families when that day comes.

## SEMULITH-AC-0050 (leaf ARTIFACT-CLEANUP.1) — the first §8 cleanup, measured and recorded

Session-directive §8 requires an artifact cleanup roughly every 24 h, tracked in
`docs/ARTIFACT_CLEANUP.md`. The file did not exist — the "no file → clean this session" trigger
fired — so the cleanup owns a task-tree now, the same as any other change.

**Census before deleting anything** — 22 `.bin` under `target/`, 18 under `.app-data/target/`,
all of them cargo incremental caches in the directive's enumerated scope; 7 crate **source**
fixtures under `.app-data/cargo-home/` (inputs, not artifacts — kept); 13 reference-run logs
under `target/refs/` (kept: evidence trails, 1.3 MB, outside the enumerated cargo dirs).

**Measured, not asserted:** 40 files / 341 MB deleted (`.app-data` 1.4 G → 1.1 G); zero after;
`git status` shows only the intended tracked files. The record is overwrite-only — one date and
one line per run, so the file can never become the changelog it exists to prevent — and it is a
governed live surface from its first commit (registered in `doctrine/readme_routes.tsv`).

