#!/usr/bin/env bash
# scripts/check_materials_bill.sh — shim (XTASK.6 slice 6am): the MATERIALS-BILL doctrine's driver is now
# `cargo xtask check-materials-bill [--self-test]` (xtask/src/check_materials_bill.rs). Every registered unit's book carries
# a materials bill whose identity tables are the generator's output (DRIFT otherwise) and whose prose states, for every
# material the unit's declared shape enumerates, what it does NOT supply; the driver's inline Python judge (over the pinned
# sexp, dossier_sexp and gen_model_book) runs verbatim through `python3 -` (not ported), the generator and the controls'
# inline edits are spawned as before. The same verdict lines and exit statuses (0 ok, 1 a finding, 2 refused). Kept
# because the project doctrine slot registers this path; a unit test holds it to this one command, and the
# DERIVED-COUNTS arm total counts the module's arms through it.
set -euo pipefail
cd "$(git rev-parse --show-toplevel)"
exec cargo xtask check-materials-bill "$@"
