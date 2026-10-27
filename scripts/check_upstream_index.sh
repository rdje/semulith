#!/usr/bin/env bash
# scripts/check_upstream_index.sh — shim (XTASK.6 slice 6ai): the UPSTREAM-INDEX doctrine's driver is now
# `cargo xtask check-upstream-index [--self-test]` (xtask/src/check_upstream_index.rs). Every upstream issue record is
# the authority its two indices and its REPORT.md mirror — states and severities from the vocabularies, a verified state
# earned by a pin and a captured re-run, blocks entries naming leaves a tree declares, nothing pointing outside its
# subtree; the driver's inline Python judge runs verbatim through `python3 -` (not ported). The same lines and exit
# statuses (0 ok, else the judge's own). Kept because the project doctrine slot registers this path; a unit test holds
# it to this one command, and the DERIVED-COUNTS arm total counts the module's arms through it.
set -euo pipefail
ROOT="$(git rev-parse --show-toplevel)" || exit 2; cd "$ROOT"
# All scratch, including child-tool defaults, stays on the repository volume.
mkdir -p "$ROOT/target/tmp" || exit 2
export TMPDIR="$ROOT/target/tmp"
exec cargo xtask check-upstream-index "$@"
