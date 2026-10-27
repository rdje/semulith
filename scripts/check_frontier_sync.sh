#!/usr/bin/env bash
# scripts/check_frontier_sync.sh — shim (XTASK.6 slice 6ab): the FRONTIER-SYNC doctrine's driver is now
# `cargo xtask check-frontier-sync [--self-test]` (xtask/src/check_frontier_sync.rs). The task-tree index and the
# closed-tree register must mirror the trees they index — status, frontier leaf, every count in a cell, one row per tree;
# the driver's inline Python judge decides it over the shared task_source reader and runs verbatim through `python3 -`
# (not ported); the controls write the script's synthetic trees, index and register. The same verdict lines and exit
# statuses (0 ok, 1 the index drifts, 2 refused). Kept because the project doctrine slot registers this path; a unit test
# holds it to this one command, and the DERIVED-COUNTS arm total counts the module's arms through it.
set -euo pipefail
cd "$(git rev-parse --show-toplevel)"
exec cargo xtask check-frontier-sync "$@"
