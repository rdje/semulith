# DEV_NOTES shard — _(2026-09-27)_ … _(2026-09-27)_

> Sharded from `DEV_NOTES.md` when it crossed its 48 KiB ceiling (`doctrine/readme_routes.tsv`).
> Entries in a shard are **never edited after the shard** — git history is canonical.

## _(2026-09-27)_ — target arithmetic primitives, and the width-sensitivity trap (P1-LAB.2)

Implementation: `semulith-core::arith`, one function per semantics-data operation, contracts written to SEM-03 (width/signedness/intermediate precision/truncation/exceptional behavior per function), source links as doc comments naming requirement ids + pinned locators. The first code content in the workspace. Validation: 12 test suites — boundary at XLEN, 8-bit-exhaustive against different-host-width references (multiply-as-shift, De Morgan), 100k-draw word-op sweep; clippy -D warnings clean; gate green. Design notes, kept: (1) the exhaustive layer caught the signed-op width-sensitivity trap on its first run — `slt`/`sar` compared against an `i8` reference without embedding the signed view at XLEN; the primitives were right, the test was wrong, and the trap is now a knowledge card. (2) Unmasked shift amounts panic via `debug_assert` rather than silently wrapping — a decoder bug must not produce a plausible-looking wrong result; the masking rule lives in `shamt64`/`shamt32` next to the REQ-D-SHAMT citation. (3) `implementation_status` on the requirements stays `planned` until the interpreter can exercise instruction-level obligations — do not inflate status to match enthusiasm.

Lessons: promoted to `docs/knowledge/reduced-width-verification-of-signed-ops.md` (the width-sensitivity rule and the per-operation table).

## _(2026-09-27)_ — the laboratory crates and the Wasm gate (P1-LAB.1, PORT-WEB.1)

Root cause: the crate boundary was a `docs/ARCHITECTURE.md` §4 table with no crates behind it, and the browser target was a decision with no instrument. Implementation: three crates with one-directional edges (`cli → {core, verify}`, `verify → core`, `core →` nothing — the wiring IS the deliverable at `.1`; behaviour stays with its owning leaf); `scripts/check_wasm_build.sh` registered as the `PORT-WEB` doctrine — preflight refuses when the rustup target is absent (exit 2), the 4-arm self-test re-runs before every judgement, the verdict is a plain `cargo build --workspace --target wasm32-unknown-unknown`. Validation: `make check` green (5 suites, 0 warnings at `-D warnings`); self-test 4 pass / 0 fail; fired RED on a real `std::os::unix` import (rc=1, naming `lib.rs:13`); `make gate` green after registration. Design notes, kept: (1) the self-test caught my own first cut — bin crates want `src/main.rs`, not `src/bin.rs`, and cargo fails builds with rc=101, not 1; a control never run RED is not known to work. (2) Scratch builds pass `--target-dir` inside the temp dir — the measured family defect is self-test state leaking into the real run through environment variables.

Lessons: declined here (both notes are recorded in the PORT-WEB.1 leaf checklist).

## _(2026-09-27)_ — the sanctioned watcher is a ruling, not a false positive (ARTIFACT-CLEANUP.2)

The director ruled CHIPDOC's ChipdocWatcher stays, and the census stopped crying wolf the
honest way: the exemption is a RULING in data (doctrine/sanctioned_processes.tsv), not a
vocabulary in detection — the pattern-free census is untouched, and only director-ruled
standing processes skip it. Design note worth keeping: a detection list and an exemption list
are different shapes of the same text file; the difference is WHO adds a row and WHY (an agent
proposes, the director disposes, the ruling is quoted). Verified both directions: handoff OK
with PID 36462 alive; the row absent -> the same process flags.

Lessons: declined here (the propose-vs-dispose discipline is stated in the registry header).

