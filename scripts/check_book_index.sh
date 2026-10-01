#!/usr/bin/env bash
# scripts/check_book_index.sh — BOOK-INDEX (project doctrine).
#
# `docs/book/src/index.md` is GENERATED from the book's own text by
# `scripts/gen_book_index.py` (BOOK-APPARATUS.1; OWN-03: generated artifacts are changed by
# regeneration, never by direct editing, and identify their canonical input). This check
# regenerates the index in memory and refuses the day it stops byte-matching the committed
# file — a hand-edited or stale index is a running total, and a running total is a memory of
# a measurement, not a measurement (DERIVED-COUNTS' founding failure).
#
# ⭐ WHAT THIS ACTUALLY PROTECTS: not the index's looks — the DERIVATION. The book's text is
# the authority; the index is its mirror. The pair is registered in doctrine/fact_ownership.tsv.
#
# ⚠️ HONEST LIMIT: it proves the index is still the function of the book's text. It says
# nothing about whether the CHAPTERS are true — that is the contracts' own review surface.
# Chapter-level "discussed in" granularity is deliberate (BOOK-APPARATUS decision 2026-10-02):
# the index vouches for chapter presence, never for section anchors.
#
# CONTRACT: exit code is the verdict; explains on stderr; deterministic; read-only; no network.
#   --self-test   run the RED/GREEN controls and exit.
set -uo pipefail
ROOT="$(git rev-parse --show-toplevel)"; cd "$ROOT"

command -v python3 >/dev/null 2>&1 || {
  echo "BOOK-INDEX: REFUSED — python3 is not on PATH; this check cannot judge." >&2; exit 2; }

BOOK="docs/book"
GLOSSARY="docs/GLOSSARY.md"
OUT="docs/book/src/index.md"

# ── self-test ────────────────────────────────────────────────────────────────────────────────
SELFTEST_TMP() { local d="$ROOT/target/doctrine-selftest"; mkdir -p "$d"; mktemp -d "$d/XXXXXX"; }

self_test() {
  local t pass=0 fail=0 out rc
  t="$(SELFTEST_TMP)"

  # ⛔ STRICT ARITY (docs/knowledge/self-test-arms-that-never-ran.md): a missing `;` before
  # an arm call swallows it silently; the guard makes that a loud failure.
  argc() {
    [ "$2" -eq "$1" ] && return 0
    fail=$((fail+1))
    printf 'BOOK-INDEX self-test HARNESS: %s() got %s argument(s), expected %s — a missing `;` before `arm` swallows it\n' \
      "$3" "$2" "$1" >&2
    return 1
  }
  arm() { # arm <name> <rc> <expected-rc> <output> <reason substring; empty = expect no output>
    argc 5 "$#" arm || return
    if [ -z "$5" ]; then
      if [ "$2" = "$3" ] && [ -z "$4" ]; then
        pass=$((pass+1)); return
      fi
      fail=$((fail+1))
      printf 'BOOK-INDEX self-test MISS: %s — expected rc=%s and no output, got rc=%s\n%s\n' \
        "$1" "$3" "$2" "$4" >&2
      return
    fi
    if [ "$2" = "$3" ] && printf '%s' "$4" | grep -qF "$5"; then
      pass=$((pass+1))
    else
      fail=$((fail+1))
      printf 'BOOK-INDEX self-test MISS: %s — expected rc=%s (reason: %s), got rc=%s\n%s\n' \
        "$1" "$3" "$5" "$2" "$4" >&2
    fi
  }

  cp -R "$BOOK" "$t/book"; cp "$GLOSSARY" "$t/GLOSSARY.md"

  # GREEN: the generator emits an index from the real book.
  out="$(python3 scripts/gen_book_index.py --book "$t/book" --glossary "$t/GLOSSARY.md" \
        --out "$t/index.md" 2>&1)"; rc=$?
  arm "GREEN the generator emits an index from the real book" "$rc" 0 "$out" "wrote"

  # GREEN: the drift check passes on a faithful regeneration.
  out="$(python3 scripts/gen_book_index.py --check --book "$t/book" --glossary "$t/GLOSSARY.md" \
        --out "$t/index.md" 2>&1)"; rc=$?
  arm "GREEN a faithful regeneration is judged in sync" "$rc" 0 "$out" ""

  # RED: a hand-edit of the generated index is detected, named, and refused.
  printf '\na hand edit\n' >> "$t/index.md"
  out="$(python3 scripts/gen_book_index.py --check --book "$t/book" --glossary "$t/GLOSSARY.md" \
        --out "$t/index.md" 2>&1)"; rc=$?
  arm "RED a hand-edited index is refused, naming DRIFT" "$rc" 1 "$out" "DRIFT"

  # RED: a book edit the index must reflect (every chapter's text removed) regenerates to
  #    different bytes — a stale index is refused, naming DRIFT.
  find "$t/book/src" -name '*.md' ! -name 'SUMMARY.md' ! -name 'glossary.md' ! -name 'index.md' \
    -exec sh -c ': > "$1"' _ {} \;
  out="$(python3 scripts/gen_book_index.py --check --book "$t/book" --glossary "$t/GLOSSARY.md" \
        --out "$t/index.md" 2>&1)"; rc=$?
  arm "RED a stale index behind edited chapters is refused, naming DRIFT" "$rc" 1 "$out" "DRIFT"

  # RED: a SUMMARY naming a missing chapter is refused BY NAME — new book structure is
  #    generator work, never silently skipped.
  rm "$t/book/src/claim-scope.md"
  out="$(python3 scripts/gen_book_index.py --check --book "$t/book" --glossary "$t/GLOSSARY.md" \
        --out "$t/index.md" 2>&1)"; rc=$?
  arm "RED a SUMMARY naming a missing chapter is refused by name" "$rc" 2 "$out" "claim-scope.md"

  # RED: a book without its SUMMARY is refused — the chapter set is undeclared, and an
  #    index over an undeclared population is a guess.
  rm "$t/book/src/SUMMARY.md"
  out="$(python3 scripts/gen_book_index.py --check --book "$t/book" --glossary "$t/GLOSSARY.md" \
        --out "$t/index.md" 2>&1)"; rc=$?
  arm "RED a missing SUMMARY.md is refused, naming it" "$rc" 2 "$out" "SUMMARY.md"

  rm -rf "$t"
  printf 'BOOK-INDEX --self-test: %d pass / %d fail\n' "$pass" "$fail"
  [ "$fail" -eq 0 ]
}

if [ "${1:-}" = "--self-test" ]; then
  self_test
  exit $?
fi

# Re-run the controls before judging: a check that no longer discriminates must refuse,
# not pass (the project-doctrine contract in scripts/check_doctrines.project.sh).
self_test >/dev/null 2>&1 || {
  echo "BOOK-INDEX: REFUSED — the check does not discriminate (self-test failed)." >&2
  exit 2; }

[ -f "$BOOK/src/SUMMARY.md" ] || { echo "BOOK-INDEX: ok (no project book yet)"; exit 0; }

out="$(python3 scripts/gen_book_index.py --check --book "$BOOK" --glossary "$GLOSSARY" \
      --out "$OUT" 2>&1)" || {
  printf '%s\n' "$out" >&2
  printf 'BOOK-INDEX: FAIL — %s is out of sync with the book. Regenerate — never edit:\n  python3 scripts/gen_book_index.py\n' \
    "$OUT" >&2
  exit 1
}
terms="$(grep -c '^| ' "$OUT")"
printf 'BOOK-INDEX: ok (%s matches the book, %s table rows)\n' "$OUT" "$((terms - 2))"
exit 0
