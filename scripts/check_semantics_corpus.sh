#!/usr/bin/env bash
# scripts/check_semantics_corpus.sh — shim (XTASK.6 slice 6ah): the SEMANTICS doctrine's driver is now
# `cargo xtask check-semantics-corpus [--self-test]` (xtask/src/check_semantics_corpus.rs). Every semantics document
# pairs with the fragment beside it and checks against it (scripts/check_semantics.py, spawned as this driver spawned
# it), every unit's composed fragments refine without a silent redefinition, and the citations arm judges the tracked
# corpus or names its skip; the encoding documents are read through the harness's own reader. The same verdict lines
# and exit statuses (0 ok, 1 the corpus does not hold, 2 refused). Kept because the project doctrine slot registers this
# path; a unit test holds it to this one command, and the DERIVED-COUNTS arm total counts the module's arms through it.
set -euo pipefail
cd "$(git rev-parse --show-toplevel)"
exec cargo xtask check-semantics-corpus "$@"
