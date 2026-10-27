#!/usr/bin/env bash
# scripts/check_exercise_coverage.sh — shim (XTASK.6 slice 6k): the EXERCISE-COVERAGE doctrine is now
# `cargo xtask check-exercise-coverage [--self-test]` (xtask/src/check_exercise_coverage.rs). Every form a profile
# declares in its [scope] is executed by a tracked guest (coverage with its denominator; a count_total that
# contradicts its enumeration is a DENOMINATOR LIE), the composition closes through the one resolver (SCP-02), and
# the checkpoint, device-model and profile-resolution routes keep their declared legs. The same verdict lines and
# exit statuses (0 ok, 1 a declared form unexercised or a contradiction, 2 refused). Kept because the project
# doctrine slot registers this path; a unit test holds it to this one command, and the DERIVED-COUNTS arm total
# counts the module's arms through it.
set -euo pipefail
cd "$(git rev-parse --show-toplevel)"
exec cargo xtask check-exercise-coverage "$@"
