# DEV_NOTES shard — _(2026-09-30)_ … _(2026-09-30)_

> Sharded from `DEV_NOTES.md` when it crossed its 48 KiB ceiling (`doctrine/readme_routes.tsv`).
> Entries in a shard are **never edited after the shard** — git history is canonical.

## _(2026-09-30)_ — the routing answered, the toolchain measured: P2-SCALAR.5 unblocked (PS-0062)

The director delegated the two decisions `.5` was blocked on. Routing: the C guest lands in `P2-SCALAR.5` — the measured G0 precedent (the tree completes, the gate keeps the criterion visible every commit through GATE-REPORT, EVD-08 makes `passed` over a missing check mechanically unreachable); reopening P1-LAB would relocate bookkeeping, not evidence. Toolchain: measured, not installed — Apple clang 21.0.0 has NO RISC-V backend (the exact triple error is in the decision record); Homebrew `llvm@21` clang 21.1.8 compiled `-march=rv64i -mabi=lp64` to correct RV64I (objdump-verified); the keg ships no linker, and zig 0.16.0's bundled `ld.lld` (Homebrew LLD 21.1.8) does. Rejected: a system-wide GNU toolchain (multi-GB off-volume mutation for zero evidence gain) and routing clang's `-S` through the project's assembler (the criterion wants a genuinely compiled artifact). Recorded as `decision_c-guest-routing-and-toolchain`; `.5` blocked → active with the three-strand design before code. House-keeping under pressure: MEMORY.md's byte ceiling fired mid-commit (7217 > 7168) and was answered by demotion-grade trimming, never by raising the cap; KNOWLEDGE_MAP.md regenerated for the new record. Validation: `make gate` all green (docs-only commit).

Lesson: `promotion: declined` (recorded in the leaf) — the decision record IS the durable form.

