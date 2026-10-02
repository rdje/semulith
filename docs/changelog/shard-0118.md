# CHANGELOG shard — SEMULITH-PS-0069 … SEMULITH-PS-0066

> Sharded from `CHANGELOG.md` when it crossed its 64 KiB ceiling (`doctrine/readme_routes.tsv`).
> Entries in a shard are **never edited after the shard** — git history is canonical.

## SEMULITH-PS-0069 (leaf P2-SCALAR.5, strand 3 design) — directed sequences: the gaps measured, the design recorded

- The strand-3 design stands on a measured census (tracked corpus + the `c-scope.elf`
  disassembly + the ACT4 testplan): eight genuine gaps, each with its citation — semulith
  never running off a program's end, load→use-as-address (the jump-table idiom exists
  NOWHERE, not even in the compiled guest), the cross-width sign-extend matrix,
  store→fence→execute, compare→branch, the load+store loop, 12-deep varied chains, and
  the unpinned x0 producers.
- Two probes measured the uncertain behaviors before any guest exists (`run_probes_p25s3.py`):
  run-off-the-end traps illegal-instruction (0x02/tval 0) identically on all three models,
  and a self-modifying store stays visible through `fence rw,rw` on all three.
- One defect found by the census and logged: `c-scope.c`'s comment overclaims its ELF
  (constant folding removed the switch's indirect jump) — correction scheduled in-strand,
  the promised jump table becoming a real guest (`dir-chase`).
- Ceiling bookkeeping: `.4`'s checklist joined the archive (per-part ceiling obeyed).

## SEMULITH-PS-0068 (leaf P2-SCALAR.5, strand 2c) — the ACT4 RV64I campaign: 51/51, three-way, recorded and gated

- The full pinned suite ran green on the first fleet run: **51/51 test files, every HTIF
  verdict pass on all three models, every signature agreeing slot-for-slot — semulith vs
  the Sail-derived expectations AND spike vs sail (the control pair), 17,017 slots in
  sum.** The slot census reconciles exactly against the static sigupd counts (dead-path
  branch instances, store read-back slots, the final-offset word — all measured).
  `I-fence-00` (reserved-`fm`, `fence.tso`, HINTs) passes: DEFECT-A's inversion has
  external-suite confirmation.
- The record: `profiles/rv64i-lab-v0/act4.sexp`, emitted by the runner's `--record` from
  measured rows (never hand-typed), behind the new `schema/act4.sexp` family.
  RECORD-SCHEMA gained rule 13 (CAMPAIGN): every carried count re-derives from the rows
  and the verdict vocabulary is closed — five new self-test RED arms, 39/0.
- The EVD-04 framing is on the record: external tests with Sail-derived expectations —
  one semantics answering twice by construction; the value is that somebody else chose
  the tests. The model book's evidence chapter and materials section carry the campaign;
  the claim-scope page's "no ACT suite" row is corrected.
- Ceilings re-derived per the design's reviewed expansion: `profiles/` 100 files /
  427,926 B (ceiling 104, bytes unchanged at 0.83×), `schema/` 17 files.

## SEMULITH-PS-0067 (leaf P2-SCALAR.5, strand 2b) — the ACT4 harness: one test end-to-end three-way

- `semulith run` learned `--trace-stores`: the runner's crossing log (already recorded
  per step) is surfaced as `mem[W,0xADDR] <- 0xVALUE` lines — an observability option;
  the interpreter and the semantics data are untouched.
- The laboratory's DUT-side ACT4 pieces stand (`profiles/rv64i-lab-v0/act4/`):
  `rvtest_config.h` (the minimal measured define set — `UDB_MXLEN 64` alone; every
  privileged/FP path compiles out), `rvmodel_macros.h` (the check_defines-required
  names; the interrupt macros documented inert — no I-suite test executes them),
  `link.ld` (the lab's declared memory map, identical to the matched sail override).
- `scripts/fetch_act4.sh` is the reproducible acquisition route (pin-verified, refuses
  a drifted clone, census 51 files / 18,092 sigupds).
- `scripts/run_act4_campaign.py` builds and runs `I-add-00` end-to-end three-way: both
  toolchain risks retired by measurement (clang 21.1.8 assembles the suite clean; sail
  0.14's HTIF terminates under the lab override), all verdicts pass, the 513-slot
  signature agrees semulith↔sail-derived AND spike↔sail. The harness carries RED/GREEN
  controls (self-test 7/0).

## SEMULITH-PS-0066 (leaf P2-SCALAR.5, strand 2a) — ACT4 acquired sparse; strand-2 design recorded before code

- The pinned suite's generated half landed as a blobless sparse clone at `e2216915…`
  under `target/refs/riscv-arch-test/` (untracked: `tests/env` + `tests/rv64i/I` +
  `config`, 45 MB of the ~672 MB tree) — measured: 51 RV64I test files, 18,092
  `RVTEST_SIGUPD`s, 14,820 testcases.
- Strand-2 design recorded before code: signature-mode build; the CLI learns a store
  trace from the runner's crossing log; Sail-derived expectations per `EVD-04`, spike
  the control pair; DUT-side `rvtest_config.h` / `rvmodel_macros.h` / `link.ld` under
  `profiles/rv64i-lab-v0/act4/`; three slices.
- Acquisition facts synced: `references.sexp` (act4 → `acquired (sparse partial)` + pin;
  PROFILE-CONSISTENCY's vocabulary extended), the catalogue note, both books. Per-part
  ceiling obeyed: `.4`'s design moved to the tree archive (live file was 64,310/65,536).

