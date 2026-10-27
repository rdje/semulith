#!/usr/bin/env bash
# scripts/check_contract_freeze.sh — shim (XTASK.6 slice 6aj): the CONTRACT-FREEZE doctrine's driver is now
# `cargo xtask check-contract-freeze [--self-test]` (xtask/src/check_contract_freeze.rs). A unit's contract versions own
# their obligation records exactly — members with records of their version, frozen members matching their pins,
# extensions chaining without gaps or cycles, supersessions naming inherited records; the driver's inline Python judge
# (over the pinned record_catalog and sexp) runs verbatim through `python3 -` (not ported); the controls take the real
# contract and apply the script's edits. The same verdict lines and exit statuses (0 ok, 1 a finding, 2 refused). Kept
# because the project doctrine slot registers this path; a unit test holds it to this one command, and the
# DERIVED-COUNTS arm total counts the module's arms through it.
set -euo pipefail
cd "$(git rev-parse --show-toplevel)"
exec cargo xtask check-contract-freeze "$@"
