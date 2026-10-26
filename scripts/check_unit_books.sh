#!/usr/bin/env bash
# scripts/check_unit_books.sh — UNIT-BOOKS (project doctrine).
#
# UNIT-BOOKS: shared registry mapping, relative owned source paths, exact catalogue,
# no orphan books, validated include sources before expansion, and fresh builds.
# Mandatory execution witnesses and typed source refusals prevent skipped checks.
# Every rendered local hyperlink path/HTML fragment (including print) must resolve.
# Remote availability and semantic/chapter completeness are separate claims.
# Scratch outputs and self-test fixtures stay under target/ and are removed.
# Exit 0 = checked; 1 = defect; 2 = cannot judge/refused input. No network.
set -uo pipefail
ROOT="$(git rev-parse --show-toplevel)"; cd "$ROOT"

command -v python3 >/dev/null 2>&1 || {
  echo "UNIT-BOOKS: REFUSED — python3 is not on PATH; this check cannot judge." >&2; exit 2; }
command -v mdbook >/dev/null 2>&1 || {
  echo "UNIT-BOOKS: REFUSED — mdbook is not on PATH; this check cannot judge." >&2
  echo "  Install it with: cargo install mdbook" >&2; exit 2; }

check_books() { python3 scripts/unit_books.py "$1"; }

self_test() {
  SELFTEST_TMP() { local d="$ROOT/target/doctrine-selftest"; mkdir -p "$d"; mktemp -d "$d/XXXXXX"; }
  local t pass=0 fail=0 out rc
  t="$(SELFTEST_TMP)" && [ -n "$t" ] && [ -d "$t" ] || { echo "UNIT-BOOKS self-test: cannot create a scratch directory under target/doctrine-selftest" >&2; return 1; }

  argc() {
    [ "$2" -eq "$1" ] && return 0
    fail=$((fail+1))
    printf 'UNIT-BOOKS self-test HARNESS: %s() got %s argument(s), expected %s — a missing `;` before `arm` swallows it\n' "$3" "$2" "$1" >&2
    return 1
  }
  arm() {
    argc 3 "$#" arm || return
    out="$(check_books "$t" 2>&1)"; rc=$?
    if [ "$rc" != "$2" ]; then
      fail=$((fail+1)); printf 'UNIT-BOOKS self-test MISS: %s expected rc=%s got rc=%s\n%s\n' "$1" "$2" "$rc" "$out" >&2
    elif ! printf '%s' "$out" | grep -qF "$3"; then
      fail=$((fail+1)); printf 'UNIT-BOOKS self-test MISS: %s right verdict, wrong reason (no %s)\n%s\n' "$1" "$3" "$out" >&2
    else pass=$((pass+1)); fi
  }

  # A scratch corpus: one registered unit with a minimal building book.
  registry() { mkdir -p "$t/materials"; printf '%s\n' "$1" > "$t/materials/units.sexp"; }
  book() { # $1 = book dir name under docs/models
    mkdir -p "$t/docs/models/$1/src"
    printf '[book]\ntitle = "%s"\nsrc = "src"\n' "$1" > "$t/docs/models/$1/book.toml"
    printf '# Summary\n\n[Intro](intro.md)\n' > "$t/docs/models/$1/src/SUMMARY.md"
    printf '# Intro\n' > "$t/docs/models/$1/src/intro.md"
  }

  arm "REFUSE no registry at all" 2 "REFUSED"

  registry '(unit (id "u1") (kind processor) (layer processor) (book "docs/models/u1"))'
  arm "RED   a unit whose book does not exist" 1 "NO BOOK u1"

  mkdir -p "$t/docs/book/src"
  printf '[book]\ntitle = "project"\nsrc = "src"\n' > "$t/docs/book/book.toml"
  printf '# Summary\n\n[Models](models.md)\n' > "$t/docs/book/src/SUMMARY.md"
  printf '# Models\n\n- **`u1`** (kind: processor)\n' > "$t/docs/book/src/models.md"
  book u1
  arm "GREEN a registered unit with a building book" 0 "__CHECKED__ 1"

  book stray
  arm "RED   a book no unit registers" 1 "ORPHAN BOOK"
  rm -rf "$t/docs/models/stray"

  rm "$t/docs/models/u1/src/SUMMARY.md"
  arm "RED   a book without its SUMMARY" 1 "INCOMPLETE BOOK u1"
  printf '# Summary\n\n[Intro](intro.md)\n' > "$t/docs/models/u1/src/SUMMARY.md"

  printf 'not toml at all [[[\n' > "$t/docs/models/u1/book.toml"
  arm "RED   a book that does not build (a malformed book.toml)" 1 "BOOK DOES NOT BUILD u1"
  printf '[book]\ntitle = "u1"\nsrc = "src"\n' > "$t/docs/models/u1/book.toml"

  printf '# Models\n' > "$t/docs/book/src/models.md"
  arm "RED   missing registered catalogue entry" 1 "MODEL-CATALOGUE missing u1"
  printf '# Models\n\n- **`u1`** (kind: board)\n' > "$t/docs/book/src/models.md"
  arm "RED   wrong catalogue kind" 1 "MODEL-CATALOGUE kind u1"
  printf '# Models\n\n- **`u1`** (kind: processor)\n' > "$t/docs/book/src/models.md"

  # Source integrity is independent of the final rendered hyperlink census.
  printf '// ANCHOR: selected\ncontract\n// ANCHOR_END: selected\n' > "$t/docs/book/src/fragment.txt"
  cp "$t/docs/book/src/fragment.txt" "$t/docs/models/u1/src/fragment.txt"
  printf '# Models\n\n- **`u1`** (kind: processor)\n\n{{#include absent.txt}}\n' > "$t/docs/book/src/models.md"
  arm "RED   project include file missing" 1 "DEFECT"
  printf '# Models\n\n- **`u1`** (kind: processor)\n\n{{#include fragment.txt:absent}}\n' > "$t/docs/book/src/models.md"
  arm "RED   project include anchor missing" 1 "DEFECT"
  cat "$t/docs/book/src/fragment.txt" >> "$t/docs/book/src/fragment.txt.duplicate"
  cat "$t/docs/book/src/fragment.txt" >> "$t/docs/book/src/fragment.txt.duplicate"
  mv "$t/docs/book/src/fragment.txt.duplicate" "$t/docs/book/src/fragment.txt"
  printf '# Models\n\n- **`u1`** (kind: processor)\n\n{{#include fragment.txt:selected}}\n' > "$t/docs/book/src/models.md"
  arm "RED   project include anchor duplicate" 1 "DEFECT"
  printf '# Models\n\n- **`u1`** (kind: processor)\n' > "$t/docs/book/src/models.md"
  printf '# Intro\n\n{{#include absent.txt}}\n' > "$t/docs/models/u1/src/intro.md"
  arm "RED   unit include file missing" 1 "DEFECT"
  printf '# Intro\n\n{{#include fragment.txt:absent}}\n' > "$t/docs/models/u1/src/intro.md"
  arm "RED   unit include anchor missing" 1 "DEFECT"
  cp "$t/docs/book/src/fragment.txt" "$t/docs/models/u1/src/fragment.txt"
  printf '# Intro\n\n{{#include fragment.txt:selected}}\n' > "$t/docs/models/u1/src/intro.md"
  arm "RED   unit include anchor duplicate" 1 "DEFECT"

  printf '# Intro\n\n[Missing](missing.md)\n' > "$t/docs/models/u1/src/intro.md"
  arm "RED   rendered local path is absent" 1 "BOOK-LINK missing-path"
  printf '# Intro\n\n[Missing](intro.md#absent)\n' > "$t/docs/models/u1/src/intro.md"
  arm "RED   rendered HTML anchor is absent" 1 "BOOK-LINK missing-anchor"
  printf '# Intro\n' > "$t/docs/models/u1/src/intro.md"

  registry "(unit (id \"u1\") (kind processor) (layer processor) (book \"$t/docs/models/u1\"))"
  arm "REFUSE absolute registry book path before build" 2 "UNSAFE BOOK PATH"

  registry ''
  arm "REFUSE an empty registry" 2 "registry is empty"

  out="$(python3 scripts/probe_unit_books.py 2>&1)"; rc=$?
  if [ "$rc" -eq 0 ]; then pass=$((pass+1)); else
    fail=$((fail+1)); printf 'UNIT-BOOKS probe failed\n%s\n' "$out" >&2
  fi
  out="$(python3 -O scripts/probe_unit_books.py 2>&1)"; rc=$?
  if [ "$rc" -eq 0 ]; then pass=$((pass+1)); else
    fail=$((fail+1)); printf 'UNIT-BOOKS optimized probe failed\n%s\n' "$out" >&2
  fi
  out="$(python3 scripts/probe_book_navigation.py 2>&1)"; rc=$?
  if [ "$rc" -eq 0 ]; then pass=$((pass+1)); else
    fail=$((fail+1)); printf 'UNIT-BOOKS navigation probe failed\n%s\n' "$out" >&2
  fi
  out="$(python3 -O scripts/probe_book_navigation.py 2>&1)"; rc=$?
  if [ "$rc" -eq 0 ]; then pass=$((pass+1)); else
    fail=$((fail+1)); printf 'UNIT-BOOKS optimized navigation probe failed\n%s\n' "$out" >&2
  fi
  rm -rf "$t"
  printf 'UNIT-BOOKS --self-test: %d pass / %d fail\n' "$pass" "$fail"
  [ "$fail" -eq 0 ]
}

[ "${1:-}" = "--self-test" ] && { self_test; exit $?; }

self_test >/dev/null 2>&1 || {
  echo "UNIT-BOOKS: REFUSED — the check does not discriminate (self-test failed)." >&2; exit 2; }

out="$(check_books "$ROOT")"; rc=$?
count="$(printf '%s' "$out" | sed -n 's/^__CHECKED__ //p')"
body="$(printf '%s' "$out" | grep -v '^__\(CHECKED\|LINKS\)__ ' || true)"
if [ "$rc" -eq 2 ]; then
  { echo "UNIT-BOOKS: REFUSED — the unit corpus could not be read."
    printf '%s\n' "$body" | sed 's/^/  /'; } >&2
  exit 2
fi
if [ "$rc" -ne 0 ]; then
  { echo "UNIT-BOOKS: catalogue, source, build or rendered-navigation defect."
    printf '%s\n' "$body" | sed 's/^/  /'
    echo "  Inspect the named source and fresh bundle verdict; stale output cannot qualify."; } >&2
  exit 1
fi
links="$(printf '%s' "$out" | sed -n 's/^__LINKS__ //p')"
printf 'UNIT-BOOKS: ok (%s units + project book; catalogue and %s rendered hyperlinks checked in fresh bundle)\n' "${count:-0}" "${links:-0}"
exit 0
