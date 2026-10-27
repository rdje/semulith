#!/usr/bin/env bash
# scripts/check_changelog_shards.sh — shim (XTASK.6 slice 6ad): the SHARD-FREEZE doctrine's driver is now
# `cargo xtask check-changelog-shards [--self-test]` (xtask/src/check_changelog_shards.rs). The sharded history — the
# shards, their manifest, the two live heads, the archive descriptor — is frozen: scripts/check_history_partition.py judges
# the partition against the committed manifest and descriptor taken through `git show`, scripts/history_predecessor.py the
# chain; both run as this driver ran them (not ported); the controls write the script's synthetic shards and run its probe
# mutations. The same verdict lines and exit statuses (0 ok, 1 thawed or rewritten, 2 refused). Kept because the project
# doctrine slot registers this path; a unit test holds it to this one command, and the DERIVED-COUNTS arm total counts the
# module's arms through it.
set -euo pipefail
cd "$(git rev-parse --show-toplevel)"
exec cargo xtask check-changelog-shards "$@"
