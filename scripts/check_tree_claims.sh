#!/usr/bin/env bash
# scripts/check_tree_claims.sh — shim (XTASK.6 slice 6aa): the TREE-CLAIMS doctrine's driver is now
# `cargo xtask check-tree-claims [--self-test]` (xtask/src/check_tree_claims.rs). A live document may state a tree fact
# — an active tree's leaf count, a frontier pointer, a leading progress ratio — only if the tree says the same; the
# driver's inline Python judge decides it over the shared task_source reader and runs verbatim through `python3 -` (not
# ported); the controls write the script's synthetic registry, live document and trees. The same verdict lines and exit
# statuses (0 ok, 1 a contradiction, 2 refused). Kept because the project doctrine slot registers this path; a unit test
# holds it to this one command, and the DERIVED-COUNTS arm total counts the module's arms through it.
set -euo pipefail
cd "$(git rev-parse --show-toplevel)"
exec cargo xtask check-tree-claims "$@"
