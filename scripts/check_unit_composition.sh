#!/usr/bin/env bash
# scripts/check_unit_composition.sh — shim (XTASK.6 slice 6n): the UNIT-COMPOSITION doctrine is now
# `cargo xtask check-unit-composition [--self-test]` (xtask/src/check_unit_composition.rs). Every tracked
# profiles/*/encoding.sexp is decided through the one disjointness judge — validated against its schema, resolved through
# the one composition resolver, its union judged for collisions, duplicate names and pseudo problems, its slots declared
# partial or not. The same verdict lines and exit statuses (0 ok, 1 a unit's composition does not hold, 2 refused). Kept
# because the project doctrine slot registers this path; a unit test holds it to this one command, and the DERIVED-COUNTS
# arm total counts the module's arms through it.
set -euo pipefail
cd "$(git rev-parse --show-toplevel)"
exec cargo xtask check-unit-composition "$@"
