#!/usr/bin/env bash
# scripts/check_book_index.sh — shim (XTASK.6 slice 6t): the BOOK-INDEX doctrine's driver is now
# `cargo xtask check-book-index [--self-test]` (xtask/src/check_book_index.rs). docs/book/src/index.md is GENERATED from
# the book's own text by scripts/gen_book_index.py (BOOK-APPARATUS.1; OWN-03); the check regenerates it in memory through
# the generator, spawned as this driver spawned it (not ported), and refuses the day the committed file stops
# byte-matching — status 1 with the generator's named DRIFT line is the FAIL, every other failure stays a refusal. The
# same verdict lines and exit statuses (0 ok, 1 out of sync, 2 refused). Kept because the project doctrine slot
# registers this path; a unit test holds it to this one command, and the DERIVED-COUNTS arm total counts the module's
# arms through it.
set -euo pipefail
cd "$(git rev-parse --show-toplevel)"
exec cargo xtask check-book-index "$@"
