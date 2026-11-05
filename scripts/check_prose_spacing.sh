#!/usr/bin/env bash
# scripts/check_prose_spacing.sh — shim: the PROSE-SPACING doctrine's driver is `cargo xtask check-prose-spacing [--self-test]`
# (xtask/src/check_prose_spacing.rs). The same verdict lines and exit statuses (0 ok, 1 a finding, 2 refused). Kept because the
# project doctrine slot registers this path.
set -euo pipefail
cd "$(git rev-parse --show-toplevel)"
exec cargo xtask check-prose-spacing "$@"
