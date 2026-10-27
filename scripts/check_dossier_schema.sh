#!/usr/bin/env bash
# scripts/check_dossier_schema.sh — shim (XTASK.6 slice 6ao): the DOSSIER-SCHEMA doctrine's driver is now
# `cargo xtask check-dossier-schema [--self-test]` (xtask/src/check_dossier_schema.rs). Every tracked `profiles/*/*.sexp`
# whose basename (or suffix family) has a same-named `schema/*.sexp` validates against it through the one checker
# (`scripts/check_sexp_schema.py`); a document with no schema is skipped and counted BY NAME. The driver's inline Python
# sweep runs verbatim through `python3 -` (not ported); the controls' three probes are spawned as before. The same
# verdict lines and exit statuses (0 ok, 1 a violation, 2 refused). Kept because the project doctrine slot registers this
# path; a unit test holds it to this one command, and the DERIVED-COUNTS arm total counts the module's arms through it.
set -euo pipefail
cd "$(git rev-parse --show-toplevel)"
exec cargo xtask check-dossier-schema "$@"
