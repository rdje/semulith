#!/usr/bin/env bash
# scripts/check_derived_counts.sh — shim (XTASK.6 slice 6ae): the DERIVED-COUNTS doctrine is now
# `cargo xtask check-derived-counts [--self-test|--list]` (xtask/src/check_derived_counts.rs). A live document may state
# a repository count only as the number the repository re-derives today — the routed destinations, the registered project
# doctrines, the book chapters, the self-test arms (bash `arm "`/`score "` lines and a shim module's `tally.arm(`/
# `tally.score(` lines), the open upstream issues; the claims table, the enumerators (run as the script ran them) and the
# shell's own `grep -E` extraction are the script's. The same verdict lines and exit statuses (0 ok, 1 a count drifts,
# 2 refused). Kept because the project doctrine slot registers this path; a unit test holds it to this one command, and
# the arm total counts the module's arms through it.
set -euo pipefail
cd "$(git rev-parse --show-toplevel)"
exec cargo xtask check-derived-counts "$@"
