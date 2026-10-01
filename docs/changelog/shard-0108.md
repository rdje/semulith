# DEV_NOTES shard — _(2026-09-30)_ … _(2026-09-30)_

> Sharded from `DEV_NOTES.md` when it crossed its 48 KiB ceiling (`doctrine/readme_routes.tsv`).
> Entries in a shard are **never edited after the shard** — git history is canonical.

## _(2026-09-30)_ — the discrepancy census: one divergence exists (P2-SCALAR.6 design)

Discrepancy reduction opened with the measurement its acceptance implies: enumerate every
recorded difference and every campaign result before minimizing anything. Eight
`references.sexp` difference records dispositioned with citations — two harness, one
trace-vocabulary, one sub-granularity observable, one corrected configuration defect
(pinned by guest-no-device), one board-layer (stated precondition, not a model defect),
one reference-vs-reference (sail's 56-bit tval mask; spike AND semulith agree) — leaving
exactly one model-vs-references behavioral divergence: DIFF-FENCEI-EXECUTED, the
legitimate UNSPECIFIED case. The minimization is one word (0x0000100F alone reproduces
it: policy trap at step 0; both references nop and run off the end into the measured
illegal zero word, staying each other's control). The reducer stays out of scope by
design: it minimizes against MUTANT divergences, not reference differences.

## _(2026-09-30)_ — the directed guests land; P2-SCALAR.5 done (PS-0070)

The eight guests from the measured census landed with the full wiring (gen_guests tuple +
regenerated guests.rs, one run/tests.rs suite each, the mutation census's 55 pinned
crossings, the smoke tuple, matrix cells chosen by the axis each guest genuinely
exercises). The offline differential earned its keep twice, both authoring-side:
dir-ext-matrix's first draft put its data cell at entry+0x60 — INSIDE the 0x8C code
region — so the zeroing stores patched the remaining instructions and the run stopped at
25 of 35 steps (D-CODE-VISIBILITY working as declared, against the author); moved to
0xA0, census addresses with it. dir-x0-writes' step-0 auipc constant was hand-typed
0x8000000080000000; re-derived. And the generated-fixture discipline bit once: guests.rs
must be REGENERATED after an expectation edit — a stale fixture replays the old words
(the two "persistent" failures were exactly that, not model behavior). The live smoke ran
all 48 guests three-way green: 642/642 aligned steps (+150), every run reproducing. One
documentary defect closed (c-scope.c's overclaim; the jump-table idiom is now a measured
guest). Validation: 174/174 verify suites; smoke 262 PASS / 0 FAIL; coverage 52/52;
matrix self-test 12/0; comparator 19/0; bench 52 arms after the wasm rebuild
(smoke-bench reads the built artifact — `make ci` builds before running; a bare
smoke-bench on a stale module reads the old guest set, measured); `make gate` green;
both books render.

Lesson: `promotion: declined` (the regenerate-after-edit rule is enforced by the
differential itself — stale fixtures fail loudly, measured this strand).

