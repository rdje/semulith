#!/usr/bin/env bash
# scripts/check_push_record.sh — shim (XTASK.6 slice 6e): the PUSH-RECORD doctrine is now
# `cargo xtask check-push-record [--self-test]` (xtask/src/check_push_record.rs). The approval ledger
# docs/push-approvals.md is append-only (a staged change keeps HEAD's content a prefix) and every
# `## SEMULITH-PUSH-NNNN — <timestamp>` entry carries Approved by, Reason, Range and Suite, ids
# sequential from 0001. The same verdict lines and exit statuses (0 ok, 1 rewritten or misshapen,
# 2 refused). Kept because the project doctrine slot registers this path; a unit test holds it to
# this one command, and the DERIVED-COUNTS arm total counts the module's arms through it.
set -euo pipefail
cd "$(git rev-parse --show-toplevel)"
exec cargo xtask check-push-record "$@"
