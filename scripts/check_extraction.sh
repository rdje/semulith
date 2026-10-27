#!/usr/bin/env bash
# scripts/check_extraction.sh — shim (XTASK.6 slice 6q): the EXTRACTION doctrine's driver is now
# `cargo xtask check-extraction [--self-test]` (xtask/src/check_extraction.rs). MODEL-METHOD.10 as a verdict: every
# tracked unit (profiles/*/profile.sexp) is judged by the pinned Python judge, scripts/check_extraction.py, spawned
# exactly as this driver spawned it — the judge is not ported; the self-test's record fixtures are written through the
# Rust record mapping. The same verdict lines and exit statuses (0 ok, 1 a definition is not sufficient, 2 refused).
# Kept because the project doctrine slot registers this path; a unit test holds it to this one command, and the
# DERIVED-COUNTS arm total counts the module's arms through it.
set -euo pipefail
cd "$(git rev-parse --show-toplevel)"
exec cargo xtask check-extraction "$@"
