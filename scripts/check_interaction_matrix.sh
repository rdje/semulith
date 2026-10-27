#!/usr/bin/env bash
# scripts/check_interaction_matrix.sh — shim (XTASK.6 slice 6y): the INTERACTION-MATRIX doctrine's driver is now
# `cargo xtask check-interaction-matrix [--self-test]` (xtask/src/check_interaction_matrix.rs). Every tracked unit's
# declared interaction matrix must cover every derived cell, resolve every disposition and name every tracked guest —
# scripts/check_interaction_matrix.py, the pinned Python judge, decides each unit and is spawned as this driver spawned it
# (not ported); the controls write the script's synthetic unit. The same verdict lines and exit statuses (0 ok, 1 the
# matrix does not hold, 2 refused). Kept because the project doctrine slot registers this path; a unit test holds it to
# this one command, and the DERIVED-COUNTS arm total counts the module's arms through it.
set -euo pipefail
cd "$(git rev-parse --show-toplevel)"
exec cargo xtask check-interaction-matrix "$@"
