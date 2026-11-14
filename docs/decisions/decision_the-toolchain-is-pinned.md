# The Rust toolchain is pinned to one exact release, locally and in every workflow

- **Type:** `decision`
- **Date:** `2026-11-14`
- **Status:** `active`
- **Owner / source:** `XTASK.19` slice b, `SEMULITH-XTASK-0098` (evidence target/xtask/xt0098). Found by the approved push `SEMULITH-PUSH-0007`: hosted runs `43633628211` (`rust`) and `43633628199` (`portability`) failed on `aa93d858` while `make ci` had passed twice on this host. The engineer's call under [`decision_findings-are-the-engineers-to-call.md`](decision_findings-are-the-engineers-to-call.md).
answers: Which Rust release do local and hosted builds use, why that one, and how does it change?

## What was measured

- `rust-toolchain.toml` named `channel = "stable"`, and all three workflows installed and selected `stable`. So each hosted run took that day's release, while this host's `stable` is 1.95.0 (`rustc 1.95.0 (59807616e 2026-04-14)`).
- It broke twice. On 2026-10-08, 1.99's clippy failed a revision that had passed locally on 1.95 (`CI-RECOVERY.1` fixed the lints, not the float). On 2026-11-14, 1.100.0 (released 2026-11-09) did it again: its clippy flagged four index loops (`XTASK.19` slice a), and its cargo moved integration-test executables under `target/debug/build/<package>/<hash>/out/`. Ten tests that located the CLI binary from their own path failed on the native leg (slice a2).
- With slices a and a2, the workspace passes clippy and every test on 1.100.0 as well as on 1.95.0.

## The decision

1. **One exact release: 1.95.0.** `rust-toolchain.toml` names `channel = "1.95.0"`. Every workflow step that installs or selects Rust names `1.95.0`: `RUSTUP_TOOLCHAIN=1.95.0` and `rustup toolchain install 1.95.0`. Local and hosted builds then judge with the same compiler and the same clippy.
2. **Why 1.95.0 and not the newest release.** It is the exact build (`59807616e`) behind every local gate, the version-0 release evidence and the recorded portability rows (`profiles/*/portability.sexp` name it). Pinning it changes nothing this host measures. A newer release changes lints and tool behaviour, which is what this leaf found, so moving to one is a unit of its own.
3. **The Miri leg keeps its own pin.** `scripts/check_portability.sh --print-toolchain` prints its dated nightly, and the workflow installs `"$toolchain"` assigned from that command.
4. **`TOOLCHAIN-PIN` holds it on every commit.** The check refuses a channel name or a partial version (`1.95`) in `rust-toolchain.toml`. It refuses a workflow step that selects a channel, a different release, or a variable not assigned from the Miri printer. Its self-test judges ten frozen fixtures.

## How to apply

- **Moving to a newer release** is its own unit with its own record. Install the release on-volume (`RUSTUP_HOME=.app-data/rustup-ci rustup toolchain install <release> --profile minimal --component clippy,rustfmt`), run `cargo clippy --all-targets --all-features -- -D warnings` and `cargo test --all` on it, and fix what it finds. Then change `rust-toolchain.toml` and every workflow in the same commit (`TOOLCHAIN-PIN` refuses a half-done bump), re-record anything that names the compiler, and run `make ci` before the push.
- **A new workflow** names the pinned release, or takes its toolchain from a printer `TOOLCHAIN-PIN` knows.
- **A fresh clone** gets 1.95.0 from rustup on its first cargo command; the targets a leg needs (`wasm32-unknown-unknown` for `PORT-WEB`, `x86_64-apple-darwin` for the Rosetta leg) are added as that leg's own hint says.
