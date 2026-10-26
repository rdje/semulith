#!/usr/bin/env bash
# scripts/check_registry_mirror.sh — shim (XTASK.6 slice 6i): the REGISTRY-MIRROR doctrine is now
# `cargo xtask check-registry-mirror [--self-test]` (xtask/src/check_registry_mirror.rs). DOCTRINE_ENFORCEMENT.md
# and the mdBook chapter docs/book/src/working/doctrines.md list exactly the doctrines the two registries
# register (coverage, no phantom row, the right section, every registered check present and executable, the
# "<N> checks run today" sentence true), and the docs/doctrines/ family union is a project-scoped mirror. The
# same verdict lines and exit statuses (0 ok, 1 a document no longer mirrors the registry, 2 refused). Kept
# because the project doctrine slot registers this path; a unit test holds it to this one command, and the
# DERIVED-COUNTS arm total counts the module's arms through it.
set -euo pipefail
cd "$(git rev-parse --show-toplevel)"
exec cargo xtask check-registry-mirror "$@"
