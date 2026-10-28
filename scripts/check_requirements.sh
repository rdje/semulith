#!/usr/bin/env bash
# scripts/check_requirements.sh — shim (XTASK.6 slice 6ap): the RECORD-SCHEMA doctrine's driver is now
# `cargo xtask check-requirements [--self-test|--audit]` (xtask/src/check_requirements.rs). Every tracked record file —
# the JSONL delivery artifacts and the schema-layer catalogues — validates against its schema and carries the fifteen
# cross-checks (the driver's inline Python judge over the pinned validators and readers, run verbatim through `python3 -`,
# not ported); the JSONL track is re-derived by the workspace's own Rust checker (`cargo run -p semulith-cli --
# check-examples`), spawned as before; the controls' fixture programs and probes are spawned as before. The same verdict
# lines and exit statuses (0 ok, 1 a finding, 2 refused). Kept because the project doctrine slot registers this path; a
# unit test holds it to this one command, and the DERIVED-COUNTS arm total counts the module's arms through it.
set -euo pipefail
cd "$(git rev-parse --show-toplevel)"
exec cargo xtask check-requirements "$@"
