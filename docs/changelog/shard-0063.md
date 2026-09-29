# CHANGELOG shard — SEMILITH-PL-0001 … SEMILITH-PL-0001

> Sharded from `CHANGELOG.md` when it crossed its 64 KiB ceiling (`doctrine/readme_routes.tsv`).
> Entries in a shard are **never edited after the shard** — git history is canonical.

## SEMILITH-PL-0001 (leaf P1-LAB.1, PORT-WEB.1) — the laboratory gets its three crates, and the browser target gets its gate

- `P1-LAB.1`: `crates/app` (the `semulith` placeholder) replaced by the three laboratory crates, wired per `docs/ARCHITECTURE.md` §4 — `semulith-core` depends on nothing (`Cargo.lock` carries no dependencies block for it), `semulith-verify` holds the fixtures home and depends on core only, `semulith-cli` (binary name `semulith`, ROADMAP.md §8) calls both. `make check` green at `-D warnings`; `cargo tree` shows the one-directional edges.
- `PORT-WEB.1` (same commit, as its acceptance requires): the workspace builds for `wasm32-unknown-unknown` from the first slice, enforced by the 20th registered doctrine, `scripts/check_wasm_build.sh` — it refuses with install instructions when the rustup target is absent, re-runs its 4-arm self-test before every judgement, and was fired RED against the real workspace (a `std::os::unix` import in `semulith-core`, refused naming `lib.rs:13`) before registration. CI's doctrines workflow now installs the Wasm target. No host-only API exists yet; the build itself is the standing proof.
- Docs in lockstep: mirrors in `DOCTRINE_ENFORCEMENT.md`, the book's doctrines chapter, `TOOLBOX.md`; `LIVE_STATUS.md` re-derived (20 registered, 231 self-test arms; P1 In Progress, 1/12) with a stale MODEL-METHOD row corrected; the book's P1 chapter now states the crates exist and build for host and Wasm. Fixed in passing: a layer-A typo (`sexr_file` → `sexpr_file`); the `DOCTRINE_ENFORCEMENT.md` ceiling re-derived 20 → 24 KiB in the routes registry (the 20th doctrine row is the surface's contract expanding, the same grounds as the TOOLBOX raise). Both append heads sharded again the day they were sharded — the pressure valve working as designed; the `docs/changelog/` file-count ceiling re-derived 20 → 40 in the same commit (the family now carries shards for two append heads — the derivation is recorded in the registry).

Validation: `make gate` green (20 doctrines); `make check` green (fmt + clippy -D warnings + 5 test suites); `bash scripts/check_wasm_build.sh --self-test` → 4 pass / 0 fail.

