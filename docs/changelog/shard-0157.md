# CHANGELOG shard — SEMULITH-BA-0001 … SEMULITH-AC-0056

> Sharded from `CHANGELOG.md` when it crossed its 64 KiB ceiling (`doctrine/readme_routes.tsv`).
> Entries in a shard are **never edited after the shard** — git history is canonical.

## SEMULITH-BA-0001 (leaf BOOK-APPARATUS.1) — the book's index: generated from the book's own text, gated against drift

- The director's `2026-10-02` apparatus directive audited against the real book: glossary
  present and unforkable (build-time `{{#include}}` of the canonical `docs/GLOSSARY.md`),
  two annexes present and on-policy — the **index was absent**. It lands derived, the only
  honest shape for a fact about a changing population: `scripts/gen_book_index.py` reads
  `SUMMARY.md` + the canonical glossary + the acronym table + every chapter's text;
  `docs/book/src/index.md` is what that derives (15,019 B, 40 terms).
- New project doctrine #31 **`BOOK-INDEX`** (`scripts/check_book_index.sh`): the index
  regenerates byte-exact or the commit fails — a hand-maintained index is a running total,
  and a running total is a memory of a measurement, not a measurement. Six self-test arms,
  fired RED before registration (DRIFT ×2, refusal-by-name ×2). Registered and mirrored
  (`DOCTRINE_ENFORCEMENT.md`, the book's doctrine chapter, `TOOLBOX.md`,
  `doctrine/fact_ownership.tsv`).
- The annex policy is stated in the book's introduction: chapters stay readable; what is too
  technical for the main line lives in an annex.
- The directive's second half became durable: `decision_mdbook-incremental-engaging` +
  `BOOK-APPARATUS.2` (the reading-experience audit). The TOC request was withdrawn by the
  director — the mdBook sidebar is the TOC; the contents page built for it was reverted.
- Defect fixed at root, not reported: the generator's printed term count was a fudge factor
  (read `47` against the real `40`); it now derives from the emitted rows.

## SEMULITH-MP-0001 (leaf MEMORY-POINTER.1) — MEMORY.md slimmed to the §6 next-action pointer

- The director's `2026-10-02` ruling executed: `MEMORY.md` exists solely to point at the next
  action, overwrite-only per `MEMORY_ARCHITECTURE.md` §6. Measured before: 34 lines / 7,031 B
  (97% of the hard cap; health 30 / 1,792). After: **29 lines / 1,865 B**.
- The audit verified every dropped line's durable home (trees, `docs/decisions/`,
  `docs/knowledge/`, TOOLBOX, git's submodule pin); exactly one ruling was dangling —
  `document EVERYTHING` (2026-10-01) — backfilled as `decision_document-everything`. The
  ruling itself is `decision_memory-next-action-pointer`.
- Gate lesson recorded: `TREE-CLAIMS` scans the `Active trees:` claim PER PHYSICAL LINE — the
  first slim draft wrapped the list and fired `MISSING ACTIVE`; the list stays on one line.

## SEMULITH-DS-0004 (tree DOC-SHARDING) — the append heads shard ahead of the next slice

- Trigger: `CHANGELOG.md` at 65,035 of 65,536 bytes (501 headroom) and `DEV_NOTES.md` at
  49,000 of 49,152 (152) with the next slice's entries already measured larger than the
  remaining room — the designed fire point, answered by sharding, never by raising the cap.
- `shard_history.py --max-bytes 63488`: 2 entries → `docs/changelog/shard-0113.md`,
  completeness `54 == 52 kept + 2 moved` order-and-bytes exact, head 65,035 → 62,570.
- `shard_history.py --head DEV_NOTES.md --max-bytes 46080`: 3 entries →
  `docs/changelog/shard-0114.md`, completeness `35 == 32 kept + 3 moved` exact, head
  49,000 → 45,633. Manifest 114 → 116 rows.

## SEMULITH-AC-0056 (tree ARTIFACT-CLEANUP) — the 2026-10-02 §8 cleanup: 105 incremental caches, 139 MB

- Time-triggered §8 run (the `2026-10-01` run was a full day old): 105 cargo
  incremental-cache `.bin` files deleted (139 MB), every one under a cargo
  `*/incremental/*` directory of `target/` (84 the project's own debug profile, 21
  wasm32) — exactly the enumerated safe scope; post-delete re-census 0; `target`
  4.0 G → 3.9 G; `.app-data` unchanged at 1.4 G.
- 0 stray `.bin`/`.log` in `target/release` / `target/debug/deps`; no
  `target/refs/*.log` present this run; the 7 cargo-home crate test fixtures kept
  by policy (inputs, not artifacts). `docs/ARTIFACT_CLEANUP.md` overwritten with
  the one-line record.

