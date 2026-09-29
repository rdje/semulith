# CHANGELOG shard — SEMILITH-PL-0003 … SEMILITH-PL-0003

> Sharded from `CHANGELOG.md` when it crossed its 64 KiB ceiling (`doctrine/readme_routes.tsv`).
> Entries in a shard are **never edited after the shard** — git history is canonical.

## SEMILITH-PL-0003 (leaf P1-LAB.3) — architectural state, generated from the descriptor

- `semulith-core::state` exists, and it is generated: `scripts/gen_state.py` derives `state.rs` from `profiles/rv64i-lab-v0/state.sexp` through `dossier_sexp` (the single mapping owner), byte-deterministically, with the input's sha256 in the module header (OWN-03). The generator is deliberately narrow — it refuses, naming the construct, any descriptor shape it cannot emit (another profile, a non-64 width, an unmapped special register, a missing SEM-08 census). The 21st registered doctrine, `STATE-GEN` (`scripts/check_state_gen.sh`), re-runs its 6-arm self-test before judging and refuses drift with the regeneration command; fired RED against a hand-edited module before registration. The owner→mirror pair is registered in `doctrine/fact_ownership.tsv`.
- The state: 32 × 64-bit integer registers + pc, 264 bytes inline, no heap (RUST-03); x0 hardwired zero (write discarded, read yields 0); the three ISA-chapter-named roles (x1 return address, x2 stack pointer, x5 alternate link) emitted as alias views over the one storage — C02's "does writing one alias affect every other view" answered by 10 test suites; laboratory reset per REQ-D-ENTRY-STATE/OB-ENV-RESET (x1..x31 = 0, pc = environment-supplied entry); SEM-08's hidden-state census carried as data (7 candidates checked, none present).
- Verification: 22 test suites green (12 arithmetic + 10 state); `cargo clippy --all-targets --all-features -- -D warnings` clean; workspace still builds for `wasm32-unknown-unknown`; `make gate` green with the doctrine registered and both mirrors (DOCTRINE_ENFORCEMENT.md, the book's doctrines chapter) in sync.
- Lockstep: `LIVE_STATUS.md` re-derived (21 registered, 237 self-test arms; P1 3/12); the name list in the doctrines row completed (STATE-GEN added; SCOPE-COVERAGE, omitted when it landed, restored); `MEMORY.md`, `docs/TASK_TREE.md`, the book's P1 chapter, and this tree updated. The frontier moves to `.4` (environment boundary and fixtures).

