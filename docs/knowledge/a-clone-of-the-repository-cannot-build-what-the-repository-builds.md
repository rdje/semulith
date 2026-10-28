# A clone of the repository cannot build what the repository builds

**The crates the workspace builds against are not in the tree.** `.cargo/config.toml` replaces the `crates-io`
source with `directory = ".app-data/vendor"`, and `.gitignore` ignores `/.app-data`: the vendored crates live in an
untracked directory beside the checkout. A `git clone` of the repository — the shape every scratch fixture of the
`XTASK.6` port measurements takes — carries the config and not the directory, so any offline `cargo` run inside
the clone fails before compiling anything: `failed to read root of directory source: <clone>/.app-data/vendor`.

## What happened

Measured on 2026-10-27 in the `XTASK.6` slice 6aq fixtures (`target/xtask/xt0052/red/`): the `GUEST-GEN` driver's
self-test runs `scripts/probe_c_guest_image.py`, which builds a temporary crate on `semulith-core` offline. In three
clone states the probe failed on both sides — the bash driver and its Rust port — with the same cargo error; both
drivers refused (`REFUSED — the check does not discriminate`, exit 2) and printed the self-test log's tail, and the
two tails differed only in the random names of the temporary crate directories. A symlink to the repository's
`.app-data` does not help: the artifact-cleanup boundary the probe's capture runs under refuses it by design
(`Boundary('.app-data', 'symlink')` — an owned directory must be a real directory on the same volume). Copying
`.app-data/vendor` (20 MB) and `.app-data/cargo-home` (165 MB) into the clone as real directories is what lets the
controls run there: the clone then passes, and an edited tracked fixture fails by name. The `vendor/` directory at
the top of the tree — a submodule, the LinkedSpec checkout — is a different thing and does nothing for cargo.

## Why it matters

A refusal in a fixture is a claim about the thing under test only when the fixture is the thing. Here the refusal
was the environment's: a measurement that compared a port against its script inside bare clones would have read a
missing directory as "both refuse identically" and passed — the one state (the real tree) where the controls run
would never have been exercised. The rule for every clone-based fixture of a check that runs cargo: copy
`.app-data/vendor` and `.app-data/cargo-home` in as real directories first, then measure; and when both sides refuse, read the refusal before counting it as agreement.
