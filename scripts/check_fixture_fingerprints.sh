#!/usr/bin/env bash
# scripts/check_fixture_fingerprints.sh — shim (XTASK.6 slice 6g): the FIXTURE-FINGERPRINT doctrine is now
# `cargo xtask check-fixture-fingerprints [--self-test]` (xtask/src/check_fixture_fingerprints.rs). In every
# tracked JSON/JSONL record, an object carrying both `path` and `sha256` names a file that exists, resolved
# against the record's directory, whose content hashes to that value (docs/CLAIM_VERIFICATION.md §5B); not
# covered, deliberately: docs/provenance/** (DELIVERY-PROVENANCE), vendor/, .app-data/, .git, target. The same
# verdict lines and exit statuses (0 ok, 1 a pin no longer describes the tree, 2 refused). Kept because the
# project doctrine slot registers this path; a unit test holds it to this one command, and the DERIVED-COUNTS
# arm total counts the module's arms through it.
set -euo pipefail
cd "$(git rev-parse --show-toplevel)"
exec cargo xtask check-fixture-fingerprints "$@"
