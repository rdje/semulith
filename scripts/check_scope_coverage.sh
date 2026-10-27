#!/usr/bin/env bash
# scripts/check_scope_coverage.sh — shim (XTASK.6 slice 6p): the SCOPE-COVERAGE doctrine is now
# `cargo xtask check-scope-coverage [--self-test]` (xtask/src/check_scope_coverage.rs). The director's rule, mechanized
# (MODEL-METHOD.6): no model implementation for a profile while a category its DECLARED SCOPE requires is `missing`
# — every tracked materials/units.sexp read through the one record mapping, each unit's `requires` against the census
# beside the registry. The same verdict lines and exit statuses (0 ok, 1 the declared scope is uncovered, 2 refused).
# Kept because the project doctrine slot registers this path; a unit test holds it to this one command, and the
# DERIVED-COUNTS arm total counts the module's arms through it.
set -euo pipefail
cd "$(git rev-parse --show-toplevel)"
exec cargo xtask check-scope-coverage "$@"
