#!/usr/bin/env bash
# scripts/check_unit_books.sh — shim (XTASK.6 slice 6z): the UNIT-BOOKS doctrine's driver is now
# `cargo xtask check-unit-books [--self-test]` (xtask/src/check_unit_books.rs). Every registered unit owns a model book
# that builds with mdbook, is catalogued with its kind, includes only what exists and whose rendered hyperlinks resolve —
# scripts/unit_books.py, the pinned Python judge, decides it over a fresh bundle and is spawned as this driver spawned it
# (not ported); its two probes run as the script ran them. The same verdict lines and exit statuses (0 ok, 1 a defect,
# 2 refused). Kept because the project doctrine slot registers this path; a unit test holds it to this one command, and
# the DERIVED-COUNTS arm total counts the module's arms through it.
set -euo pipefail
cd "$(git rev-parse --show-toplevel)"
exec cargo xtask check-unit-books "$@"
