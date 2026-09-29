#!/usr/bin/env bash
# scripts/check_unit_books.sh — UNIT-BOOKS (project doctrine).
#
# MODEL-BOOKS.6's acceptance, mechanized (the tree's criterion 1): every REGISTERED modelled
# unit (`materials/units.sexp` — the one registration place) has its own mdBook
# (`decision_one-definition-one-book`) and the book BUILDS. A unit without a book is a unit
# whose materials are unreviewable; a book under `docs/models/` that no unit registers fails
# by name too — the reverse direction is what keeps the family from accreting unregistered
# prose. The structure check (book.toml + src/SUMMARY.md present) is complemented by the
# build itself: a malformed book.toml fails the build outright. ⚠️ mdbook tolerates a
# SUMMARY naming a missing chapter (it renders a draft with a warning) — measured while
# writing the self-test — so the build arm's broken fixture is a malformed book.toml,
# which fails hard.
#
# CONTRACT: exit code is the verdict; explains on stderr; deterministic; no network. The build
# writes each book's gitignored output directory, the same standing as PORT-WEB's wasm build.
#   --self-test   run the RED/GREEN controls against synthetic fixtures and exit.
set -uo pipefail
ROOT="$(git rev-parse --show-toplevel)"; cd "$ROOT"

command -v python3 >/dev/null 2>&1 || {
  echo "UNIT-BOOKS: REFUSED — python3 is not on PATH; this check cannot judge." >&2; exit 2; }
command -v mdbook >/dev/null 2>&1 || {
  echo "UNIT-BOOKS: REFUSED — mdbook is not on PATH; this check cannot judge." >&2
  echo "  Install it with: cargo install mdbook" >&2; exit 2; }

check_books() { # $1 = corpus root (materials/units.sexp + docs/models/ under it)
python3 - "$1" <<'PY'
import subprocess
import sys
from pathlib import Path

root = Path(sys.argv[1])
sys.path.insert(0, "scripts")
import sexp as S

registry = root / "materials" / "units.sexp"
if not registry.is_file():
    print("UNIT-BOOKS: REFUSED — materials/units.sexp is absent; the unit registry this "
          "check enumerates is gone")
    print("__CHECKED__ 0"); sys.exit(2)
units = [u for u in S.read_file(registry)
         if isinstance(u, list) and u and str(u[0]) == "unit"]
if not units:
    print("UNIT-BOOKS: REFUSED — the unit registry is empty; a census over no units is a "
          "claim about nothing")
    print("__CHECKED__ 0"); sys.exit(2)

findings, checked = [], 0
registered_books: dict[str, str] = {}
for u in units:
    uid = str(S.field(u, "id", "units.sexp"))
    book_rel = str(S.field(u, "book", "units.sexp")).rstrip("/")
    checked += 1
    book_dir = root / book_rel
    if not book_rel or not book_dir.is_dir():
        findings.append(f"NO BOOK {uid}: the registry names '{book_rel}', which does not "
                        f"exist — a unit without a book is a unit whose materials are "
                        f"unreviewable")
        continue
    registered_books[book_dir.resolve().as_posix()] = uid
    for piece in ("book.toml", "src/SUMMARY.md"):
        if not (book_dir / piece).is_file():
            findings.append(f"INCOMPLETE BOOK {uid}: {book_rel} lacks {piece} — a book "
                            f"that cannot be navigated is not a book")
            break
    else:
        r = subprocess.run(["mdbook", "build", str(book_dir)],
                           capture_output=True, text=True)
        if r.returncode != 0:
            tail = [l for l in (r.stderr or r.stdout).splitlines() if l.strip()]
            findings.append(f"BOOK DOES NOT BUILD {uid}: `mdbook build {book_rel}` "
                            f"failed — {tail[-1] if tail else 'no output'}")

# the reverse direction: a book no unit registers
models = root / "docs" / "models"
if models.is_dir():
    for child in sorted(models.iterdir()):
        if not child.is_dir() or not (child / "book.toml").is_file():
            continue
        if child.resolve().as_posix() not in registered_books:
            findings.append(f"ORPHAN BOOK {child.relative_to(root)}: a book under "
                            f"docs/models/ that no unit registers — register the unit in "
                            f"materials/units.sexp or remove the book")

for f in findings:
    print(f)
print(f"__CHECKED__ {checked}")
sys.exit(1 if findings else 0)
PY
}

self_test() {
  SELFTEST_TMP() { local d="$ROOT/target/doctrine-selftest"; mkdir -p "$d"; mktemp -d "$d/XXXXXX"; }
  local t pass=0 fail=0 out rc
  t="$(SELFTEST_TMP)"

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

  registry ''
  arm "REFUSE an empty registry" 2 "registry is empty"

  rm -rf "$t"
  printf 'UNIT-BOOKS --self-test: %d pass / %d fail\n' "$pass" "$fail"
  [ "$fail" -eq 0 ]
}

[ "${1:-}" = "--self-test" ] && { self_test; exit $?; }

self_test >/dev/null 2>&1 || {
  echo "UNIT-BOOKS: REFUSED — the check does not discriminate (self-test failed)." >&2; exit 2; }

out="$(check_books "$ROOT")"; rc=$?
count="$(printf '%s' "$out" | sed -n 's/^__CHECKED__ //p')"
body="$(printf '%s' "$out" | grep -v '^__CHECKED__ ' || true)"
if [ "$rc" -eq 2 ]; then
  { echo "UNIT-BOOKS: REFUSED — the unit corpus could not be read."
    printf '%s\n' "$body" | sed 's/^/  /'; } >&2
  exit 2
fi
if [ "$rc" -ne 0 ]; then
  { echo "UNIT-BOOKS: a registered unit lacks its book, or a book lacks its unit."
    printf '%s\n' "$body" | sed 's/^/  /'
    echo "  One definition, one book: register the unit's book, or write it."; } >&2
  exit 1
fi
printf 'UNIT-BOOKS: ok (%s unit(s) — every registered unit has its book, and every book builds)\n' "${count:-0}"
exit 0
