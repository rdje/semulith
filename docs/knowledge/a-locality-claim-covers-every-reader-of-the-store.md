# A locality claim covers every reader of the store — not the command that filled it

**Short answer:** "the dependency cache is on-volume" is a claim about every command that
READS dependencies, not the one that downloaded them. Find the mechanism that routes ALL of
them — for cargo, `.cargo/config.toml` (an environment variable set for one command routes
one command) — and prove it by asking the tool where it resolved from, before and after.

Measured at P4-SYSTEM.7 slice (c4) part 1 (2026-10-06): slice (a) fetched the workspace's
first registry dependency with `CARGO_HOME=.app-data/cargo-home` and recorded the cache as
on-volume. Every later `make check` and wasm build ran with no `CARGO_HOME`, so cargo
resolved `rustc_apfloat` from the shared `~/.cargo` — `cargo metadata` printed the
user-home path. Nothing failed: the build was correct, just off-volume, which is why no gate
saw it.

## The pattern that works

- Route by configuration every invocation reads (`.cargo/config.toml` source replacement),
  not by an environment variable someone has to remember.
- Make the absent store a LOUD failure (a directory source that does not exist stops the
  build) — a silent fall-back to the network or a shared cache re-creates the defect.
- Prove it with the tool's own answer (`cargo metadata`'s `manifest_path`) and a control
  with the routing removed; leave a shared global cache alone — stop consulting it.

## Evidence

- `docs/tasks/P4-SYSTEM.md` — the `2026-10-06` slice (c4) part 1 decision and checklist.
- `.cargo/config.toml`, the Makefile's `vendor` target.
