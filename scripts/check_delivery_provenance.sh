#!/usr/bin/env bash
# scripts/check_delivery_provenance.sh — shim (XTASK.6 slice 6c): the DELIVERY-PROVENANCE doctrine is
# now `cargo xtask check-delivery-provenance [--self-test]` (xtask/src/check_delivery_provenance.rs).
# Every row of a delivered package's MANIFEST.sha256 carries exactly one disposition in its
# dispositions.tsv; frozen-in-place and relocated rows have their hash re-derived, live rows must
# exist, and an undeclared row or an orphan disposition is a breach. The same verdict lines and exit
# statuses (0 ok, 1 a package no longer matches, 2 refused). Kept because the project doctrine slot
# registers this path; a unit test holds it to these commands, and the DERIVED-COUNTS arm total
# counts the module's arms through it.
set -euo pipefail
ROOT="$(git rev-parse --show-toplevel)" || exit 2; cd "$ROOT"
# All scratch, including child-tool defaults, stays on the repository volume.
mkdir -p "$ROOT/target/tmp" || exit 2
export TMPDIR="$ROOT/target/tmp"
exec cargo xtask check-delivery-provenance "$@"
