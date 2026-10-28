#!/usr/bin/env bash
# scripts/check_readme_routes.sh — shim (XTASK.6 slice 6at): the README-ROUTING-CLOSURE doctrine's driver is now
# `cargo xtask check-readme-routes [--self-test]` (xtask/src/check_readme_routes.rs). Every relative destination the
# landing page links to and every path-shaped destination the README guard emits in its failure guidance is governed
# by a row of doctrine/readme_routes.tsv; every governed destination exists with a known class; ceilings block,
# health targets report, a family's per-part ceiling exempts only a regeneration-gated mirror; the registry owns the
# landing page's caps. The three Python readers run verbatim through `python3 -` (not ported); wc, the README guard and
# the hint pipeline are spawned as before. The same verdict lines and exit statuses (0 ok, 1 a breach, 2 refused).
# Kept because the project doctrine slot registers this path; a unit test holds it to these commands, and the
# DERIVED-COUNTS arm total counts the module's arms through it.
set -euo pipefail
ROOT="$(git rev-parse --show-toplevel)" || exit 2; cd "$ROOT"
# All scratch, including child-tool defaults, stays on the repository volume.
mkdir -p "$ROOT/target/tmp" || exit 2
export TMPDIR="$ROOT/target/tmp"
exec cargo xtask check-readme-routes "$@"
