#!/usr/bin/env bash
# scripts/check_artifact_cleanup.sh — shim (XTASK.6 slice 6af): the ARTIFACT-COHORT doctrine's driver is now
# `cargo xtask check-artifact-cleanup [--self-test]` (xtask/src/check_artifact_cleanup.rs). The recurring cleanup's
# instrument and controls must keep discriminating — every probe suite green and every mutation caught, plain and
# optimized — and stay tracked; the probes run as this driver ran them (not ported); no real cleanup runs. The same lines
# and exit statuses (0 ok, 2 refused). Kept because the project doctrine slot registers this path; a unit test holds it to
# this one command, and the DERIVED-COUNTS arm total counts the module's scorings through it.
set -euo pipefail
cd "$(git rev-parse --show-toplevel)"
exec cargo xtask check-artifact-cleanup "$@"
