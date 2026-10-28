#!/usr/bin/env bash
# scripts/check_seam_integrity.sh — shim (XTASK.6 slice 6au): the SEAM-INTEGRITY doctrine's driver is now
# `cargo xtask check-seam-integrity [--self-test]` (xtask/src/check_seam_integrity.rs). The `.doctrine/` seams that fix
# defects in the neutral spine checks are judged by their BEHAVIOUR over the repository's own history: still consumed
# (R1), every current tracked acceptance box still accepted (R2), no prose classified as code (R3), every behaviour
# family classified as code (R4), the census and acceptance vocabularies agreeing (R5). The owner's effective rules are
# asked of scripts/check_task_acceptance.sh; the box scoper (awk) and every pattern test (grep -E) are spawned as before.
# The same verdict lines and exit statuses (0 ok, 1 a breach, 2 refused). Kept because the project doctrine slot
# registers this path; a unit test holds it to these commands, and the DERIVED-COUNTS arm total counts the module's
# scores through it.
set -euo pipefail
ROOT="$(git rev-parse --show-toplevel)" || exit 2; cd "$ROOT"
# All scratch, including child-tool defaults, stays on the repository volume.
mkdir -p "$ROOT/target/tmp" || exit 2
export TMPDIR="$ROOT/target/tmp"
exec cargo xtask check-seam-integrity "$@"
