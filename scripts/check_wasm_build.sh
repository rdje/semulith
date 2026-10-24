#!/usr/bin/env bash
# scripts/check_wasm_build.sh — shim (XTASK.6 slice 6a): the PORT-WEB doctrine is now
# `cargo xtask check-wasm-build [--self-test]` (xtask/src/check_wasm_build.rs): the workspace must build
# for wasm32-unknown-unknown (decision_browser-wasm-target), with four self-test arms re-run before
# judging. The same verdict lines and exit statuses (0 ok, 1 fail, 2 refused). Kept because the
# project doctrine slot registers this path; a unit test holds it to this one command, and the
# DERIVED-COUNTS arm total counts the module's `tally.arm(` calls through it.
set -euo pipefail
cd "$(git rev-parse --show-toplevel)"
exec cargo xtask check-wasm-build "$@"
