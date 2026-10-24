#!/usr/bin/env bash
# scripts/check_commit_prefix.sh — shim (XTASK.6 slice 6b): the COMMIT-PREFIX doctrine is now
# `cargo xtask check-commit-prefix [--self-test]` (xtask/src/check_commit_prefix.rs). It runs
# .githooks/commit-msg on a SEMILITH- and a SEMULITH- subject and judges what the hook does: the
# misspelling refused naming SEMULITH, the pinned prefix accepted (director ruling 2026-09-30,
# decision_work-unit-prefix-semulith). The same verdict lines and exit statuses (0 ok, 1 the hook
# does not pin, 2 refused). Kept because the project doctrine slot registers this path; a unit
# test holds it to this one command, and the DERIVED-COUNTS arm total counts the module's arms.
set -euo pipefail
cd "$(git rev-parse --show-toplevel)"
exec cargo xtask check-commit-prefix "$@"
