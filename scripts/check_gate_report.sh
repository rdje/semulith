#!/usr/bin/env bash
# scripts/check_gate_report.sh — shim (XTASK.6 slice 6al): the GATE-REPORT doctrine's driver is now
# `cargo xtask check-gate-report [--self-test]` (xtask/src/check_gate_report.rs). Every tracked gate report —
# `profiles/<id>/G?-REPORT.md` and the repo-level cross-architecture report — must still be the function of its inputs
# that `scripts/gate_report.py` computes (a hand-edited report is how a project comes to hold a verdict nothing produced);
# the generator, its own `--self-test` and the runtime-root probe are spawned as before (not ported); the controls run
# against the real reports. The same verdict lines and exit statuses (0 ok, 1 stale, 2 refused). Kept because the project
# doctrine slot registers this path; a unit test holds it to this one command, and the DERIVED-COUNTS arm total counts
# the module's arms through it.
set -euo pipefail
cd "$(git rev-parse --show-toplevel)"
exec cargo xtask check-gate-report "$@"
