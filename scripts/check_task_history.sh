#!/usr/bin/env bash
# scripts/check_task_history.sh — shim (XTASK.6 slice 6ac): the TASK-HISTORY doctrine's driver is now
# `cargo xtask check-task-history [--self-test]` (xtask/src/check_task_history.rs). The task family's sealed history —
# the archive terminal and its descriptor against HEAD's, the navigation stubs, the qualification and cleanup histories,
# the links into retained narrative — is judged by the Python judges the driver ran, run as it ran them (not ported); the
# controls are its fifty-two probe runs. The same output and exit statuses (each judge's own; 2 refused). Kept because the
# project doctrine slot registers this path; a unit test holds it to this one command, and the DERIVED-COUNTS arm total
# counts the module's arms through it.
set -euo pipefail
cd "$(git rev-parse --show-toplevel)"
exec cargo xtask check-task-history "$@"
