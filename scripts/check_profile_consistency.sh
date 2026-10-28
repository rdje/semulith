#!/usr/bin/env bash
# scripts/check_profile_consistency.sh — shim (XTASK.6 slice 6ar): the PROFILE-CONSISTENCY doctrine's driver is now
# `cargo xtask check-profile-consistency [--self-test|--csr-cross <profile-dir> <state>]`
# (xtask/src/check_profile_consistency.rs). Every profile dossier is judged by the driver's inline Python (over the pinned
# dossier reader and verification modules), run verbatim through `python3 -` (not ported); the retained-statement
# verifiers, the status derivation, the policy review and the probe suites are spawned as before, the probes through the
# XTASK.8 prefetch (recorded, run in parallel by scripts/doctrine_prefetch.py, answered from the record;
# PROFILE_CONSISTENCY_PREFETCH=0 restores the live run); the quiet run keeps the controls' output in
# target/profile-consistency-selftest.log. The same verdict lines and exit statuses (0 ok, 1 a finding, 2 refused). Kept
# because the project doctrine slot registers this path; a unit test holds it to this one command, and the
# DERIVED-COUNTS arm total counts the module's arms and scores through it.
set -euo pipefail
cd "$(git rev-parse --show-toplevel)"
exec cargo xtask check-profile-consistency "$@"
