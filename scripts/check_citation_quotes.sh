#!/usr/bin/env bash
# scripts/check_citation_quotes.sh — shim (XTASK.6 slice 6r): the CITATION-QUOTES doctrine's driver is now
# `cargo xtask check-citation-quotes [--self-test]` (xtask/src/check_citation_quotes.rs). Every quoted phrase a tracked
# .sexp or live .md attributes to a pinned section must occur IN that section — scripts/check_citation_quotes.py, the
# pinned Python tool, decides it and is spawned exactly as this driver spawned it (not ported); the driver's two inline
# Python controls (source availability, altered-bytes identity) run verbatim. The same verdict lines, the NAMED SKIP
# without the pinned pages, and the same exit statuses (0 ok or skip, 1 a quote is not in its section, 2 refused).
# Kept because the project doctrine slot registers this path; a unit test holds it to this one command, and the
# DERIVED-COUNTS arm total counts the module's arms through it.
set -euo pipefail
cd "$(git rev-parse --show-toplevel)"
exec cargo xtask check-citation-quotes "$@"
