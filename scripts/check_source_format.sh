#!/usr/bin/env bash
# scripts/check_source_format.sh — shim (XTASK.6 slice 6ag): the SOURCE-FORMAT doctrine is now
# `cargo xtask check-source-format [--self-test]` (xtask/src/check_source_format.rs). Every source of truth under
# definitions/ schema/ profiles/ materials/ is an S-expression or it is refused — a retired-format file, a .sexp the one
# reader cannot parse, a corpus without a .sexp; the harness's own reader (sexp.rs, measured equal to the pinned
# scripts/sexp.py) parses the corpus, and the shared reader's refusal probe runs as this driver ran it. The same verdict
# lines and exit statuses (0 ok, 1 a source outside the format, 2 refused). Kept because the project doctrine slot
# registers this path; a unit test holds it to this one command, and the DERIVED-COUNTS arm total counts the module's
# arms and scorings through it.
set -euo pipefail
cd "$(git rev-parse --show-toplevel)"
exec cargo xtask check-source-format "$@"
