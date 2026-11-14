#!/usr/bin/env bash
# scripts/check_toolchain_pin.sh — shim (XTASK.19 slice b): the TOOLCHAIN-PIN doctrine is
# `cargo xtask check-toolchain-pin [--self-test]` (xtask/src/check_toolchain_pin.rs). rust-toolchain.toml names
# one exact Rust release and every workflow step that installs or selects Rust names the same one, so local and
# hosted builds judge with the same compiler and clippy (decision_the-toolchain-is-pinned). Exit 0 ok, 1 a
# floating or mismatched toolchain, 2 refused. Kept because the project doctrine slot registers this path; a unit
# test holds it to this one command, and the DERIVED-COUNTS arm total counts the module's arms through it.
set -euo pipefail
cd "$(git rev-parse --show-toplevel)"
exec cargo xtask check-toolchain-pin "$@"
