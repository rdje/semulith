# DEV_NOTES shard — _(2026-09-30)_ … _(2026-09-30)_

> Sharded from `DEV_NOTES.md` when it crossed its 48 KiB ceiling (`doctrine/readme_routes.tsv`).
> Entries in a shard are **never edited after the shard** — git history is canonical.

## _(2026-09-30)_ — the ACT4 harness stands: I-add-00 three-way (P2-SCALAR.5, strand 2b)

The slice retired both toolchain risks by measurement before any fleet run: clang 21.1.8
(the docs name LLVM 22) assembled the suite's macro machinery with zero diagnostics, and
sail 0.14 (the cached README pins 0.13.1; the checked-in configs target 0.14.1) terminated
on the HTIF verdict under the laboratory override, printing `RVCP-SUMMARY: TEST SIGRUN`
itself. The design's observation adaptation works as recorded: semulith's new
`--trace-stores` (the crossing log surfaced, `mem[W,0xADDR] <- 0xVALUE`, width masked),
sail's `--trace-mem` (`mem[W,…]`), spike's commit log (`mem 0xADDR 0xVALUE` on the commit
line — a load's line carries no value, so the anchored two-group match can only take a
store). Signature extraction filters stores to `[begin_signature, end_signature)` from the
ELF's exported symbols; the verdict is the first HTIF pair (low 1|3, high 0), separated
from console bytes (high 0x01010000) by the high word — the self-test proves the channel
separation and the three RED arms (corrupted slot caught at its ordinal; shorter signature
≠ agreement; verdict-less trace refuses), 7/0. Result: I-add-00 — 513 signature slots
(512 sigupds + the final-offset word) agree semulith↔sail-derived AND spike↔sail; all
three verdicts pass. Semulith's budget is derived from sail's executed step count (4× +
10,000) because its halt is a store loop, unlike the references' native HTIF exit. No
model semantics changed; the smoke corpus is untouched.

Lesson: `promotion: declined` (the vocabulary spellings live in the harness's own comments
with the measurement citation; the RED controls enforce the rest).

## _(2026-09-30)_ — ACT4 acquired sparse; the strand-2 design measured against the fetch (P2-SCALAR.5, strand 2a)

The design doctrine is "measured first", so the design commit already carries the fetch: a blobless sparse clone (sparse to `tests/env` + `tests/rv64i/I` + `config`, pinned `e2216915…`) — 45 MB instead of the ~672 MB full tree, on the repository volume, untracked. Measured against the pinned headers, two planning-doc facts were stale: the README's sail pin (0.13.1) is superseded by the checked-in `sail.json` targeting the 0.14.1 schema, and the signature mechanism is HTIF-`tohost` in signature mode (`sail_macros.h` forcibly overrides the DUT's halt/console macros), not the old riscof signature-dump flow. The design's core decision follows from the measured mechanism: run the SIGNATURE-mode build on all three models, extract `[begin_signature, end_signature)` stores and the `tohost` verdict from each store trace — which is why the CLI learns to print the crossing log it already records (observability, not semantics). Byte-budget discipline: the live tree stood 1,226 B under its per-part ceiling, so `.4`'s design moved to the archive rather than the ceiling moving. Validation: `make gate` green (docs-only; the checker's new status value covered by its self-test).

Lesson: `promotion: declined` — the fetch recipe and census live in the leaf's strand-2 design where they bite.

