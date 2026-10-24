#!/usr/bin/env bash
# scripts/check_rustdoc.sh — shim (XTASK.6 slice 6d): the API-DOCS doctrine is now
# `cargo xtask check-rustdoc [--self-test]` (xtask/src/check_rustdoc.rs). The workspace's rustdoc builds
# offline with broken and private intra-doc links and invalid HTML tags denied, each defect named by
# file, line and lint; undocumented public items are a ratchet against doctrine/undocumented_items.tsv
# (decision_rust-native-tooling, trees RUSTDOC and XTASK). The same verdict lines and exit statuses
# (0 ok, 1 fail, 2 refused). Kept because the project doctrine slot registers this path; a unit test
# holds it to this one command, and the DERIVED-COUNTS arm total counts the module's arms through it.
set -euo pipefail
cd "$(git rev-parse --show-toplevel)"
exec cargo xtask check-rustdoc "$@"
