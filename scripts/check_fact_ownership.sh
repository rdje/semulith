#!/usr/bin/env bash
# scripts/check_fact_ownership.sh — shim (XTASK.6 slice 6h): the FACT-OWNERSHIP doctrine (MODEL-METHOD.7) is
# now `cargo xtask check-fact-ownership [--self-test]` (xtask/src/check_fact_ownership.rs). The registry
# doctrine/fact_ownership.tsv holds — exactly one owner per fact kind, owners exist, every mirror names a
# governor, every governor is a registered project doctrine — and the corpus's enumerated restatement pairs
# are all named in it. The same verdict lines and exit statuses (0 ok, 1 breached, 2 refused). Kept because
# the project doctrine slot registers this path; a unit test holds it to this one command, and the
# DERIVED-COUNTS arm total counts the module's arms through it.
set -euo pipefail
cd "$(git rev-parse --show-toplevel)"
exec cargo xtask check-fact-ownership "$@"
