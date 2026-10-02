#!/usr/bin/env bash
# scripts/check_interaction_matrix.sh — INTERACTION-MATRIX (project doctrine).
#
# P2-SCALAR.4's acceptance, mechanized (`G-INTERACTIONS`): the declared fault × alias ×
# boundary × event × progress × restart matrix is DECLARED FIRST as tracked data
# (profiles/<unit>/interactions.sexp, schema: schema/interactions.sexp) and then EXERCISED —
# and "unexercised cells are reported, not omitted" is a verdict, not prose. The check
# RE-DERIVES the cells from the declared axes (N axes -> N*(N+1)/2 unordered pairs, diagonal
# included) and refuses by name: an omitted cell, a cell whose disposition does not resolve
# (a guest without source AND expectations, a mechanism outside the closed registry — the
# smoke reproduce leg and the offline determinism suite — or one whose artifact lost its
# needle, a degenerate cell without its reason), a tracked guest no cell names (an orphan),
# and a difference id the matrix names but references.sexp does not record.
#
# The core decision per unit lives in scripts/check_interaction_matrix.py; this driver
# discovers the tracked units, aggregates, and carries the self-test.
#
# CONTRACT: exit code is the verdict; explains on stderr; deterministic; read-only; no network.
#   --self-test   run the RED/GREEN controls against synthetic fixtures and exit.
set -uo pipefail
ROOT="$(git rev-parse --show-toplevel)"; cd "$ROOT"

command -v python3 >/dev/null 2>&1 || {
  echo "INTERACTION-MATRIX: REFUSED — python3 is not on PATH; this check cannot judge." >&2; exit 2; }

check_units() { # $1 = root; $2 = "git" (tracked only) or "fs"
python3 - "$1" "$2" <<'PY'
import subprocess, sys
from pathlib import Path

root = Path(sys.argv[1]); mode = sys.argv[2]
if mode == "git":
    out = subprocess.run(["git", "ls-files", "--", "profiles/*/profile.sexp"],
                         capture_output=True, text=True, check=True).stdout
    units = [(root / p).parent for p in out.splitlines() if p.strip()]
else:
    units = sorted(p.parent for p in root.glob("profiles/*/profile.sexp"))

if not units:
    print("INTERACTION-MATRIX: REFUSED — no unit found; this check cannot judge an empty corpus")
    print("__CHECKED__ 0"); sys.exit(2)

findings, checked = [], 0
for u in units:
    checked += 1
    r = subprocess.run([sys.executable, "scripts/check_interaction_matrix.py", str(u)],
                       capture_output=True, text=True)
    if r.returncode == 2:
        findings.append(f"CANNOT JUDGE {u.relative_to(root)}: {r.stderr.strip()}")
    elif r.returncode != 0:
        findings.extend(l for l in r.stderr.splitlines() if l.strip())
    else:
        for line in r.stdout.splitlines():
            if line.startswith("  "):
                print(f"{u.relative_to(root)}{line}")
            else:
                print(f"  {u.relative_to(root)}: {line}")

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
    printf 'INTERACTION-MATRIX self-test HARNESS: %s() got %s argument(s), expected %s — a missing `;` before `arm` swallows it\n' "$3" "$2" "$1" >&2
    return 1
  }
  arm() {
    argc 3 "$#" arm || return
    out="$(check_units "$t" fs 2>&1)"; rc=$?
    if [ "$rc" != "$2" ]; then
      fail=$((fail+1)); printf 'INTERACTION-MATRIX self-test MISS: %s expected rc=%s got rc=%s\n%s\n' "$1" "$2" "$rc" "$out" >&2
    elif ! printf '%s' "$out" | grep -qF "$3"; then
      fail=$((fail+1)); printf 'INTERACTION-MATRIX self-test MISS: %s right verdict, wrong reason (no %s)\n%s\n' "$1" "$3" "$out" >&2
    else pass=$((pass+1)); fi
  }

  # A scratch unit: two axes -> three cells, over two synthetic guests and one mechanism.
  mkdir -p "$t/profiles/p/guests"
  profile() { printf '(profile (id "p") (version "0") (status "development"))\n' \
      > "$t/profiles/p/profile.sexp"; }
  guests() {
    for g in g1 g2; do
      printf '# %s\n' "$g" > "$t/profiles/p/guests/$g.s"
      printf '(expectations (program "%s.s") (entry "0x80000000") (instructions 0))\n' "$g" \
        > "$t/profiles/p/guests/$g.expected.sexp"
    done
  }
  references() { printf '(references (profile "p") (retrieved "d") (work_dir "w") %s)\n' "$1" \
      > "$t/profiles/p/references.sexp"; }
  matrix() { # $1 = the cell forms
    printf '(interactions (profile "p") (axis (id "alpha") (covers "a")) (axis (id "beta") (covers "b")) %s)\n' \
      "$1" > "$t/profiles/p/interactions.sexp"
  }
  GOOD='(cell (axis "alpha") (axis "alpha") (guest "g1")) (cell (axis "alpha") (axis "beta") (guest "g2")) (cell (axis "beta") (axis "beta") (mechanism "smoke-reproduce"))'

  arm "REFUSE no unit at all" 2 "cannot judge"

  profile; guests; references ""; matrix "$GOOD"
  arm "GREEN a complete matrix resolves" 0 "3 cells declared"

  matrix '(cell (axis "alpha") (axis "alpha") (guest "g1")) (cell (axis "alpha") (axis "beta") (guest "g2"))'
  arm "RED   an omitted cell fails, named" 1 "OMITTED CELL p: beta×beta"

  matrix "$GOOD (cell (axis \"beta\") (axis \"beta\") (guest \"g1\"))"
  arm "RED   a cell declared twice" 1 "DUPLICATE CELL p: beta×beta"

  matrix '(cell (axis "alpha") (axis "gamma") (guest "g1")) (cell (axis "alpha") (axis "beta") (guest "g2")) (cell (axis "beta") (axis "beta") (mechanism "smoke-reproduce"))'
  arm "RED   a cell naming an undeclared axis" 1 "UNDECLARED AXIS"

  matrix "$GOOD"
  rm "$t/profiles/p/guests/g2.expected.sexp"
  arm "RED   a guest without its expectations document" 1 "UNRESOLVED GUEST"
  printf '(expectations (program "g2.s") (entry "0x80000000") (instructions 0))\n' \
    > "$t/profiles/p/guests/g2.expected.sexp"

  matrix '(cell (axis "alpha") (axis "alpha") (guest "g1")) (cell (axis "alpha") (axis "beta") (guest "g2")) (cell (axis "beta") (axis "beta") (mechanism "wishful-thinking"))'
  arm "RED   a mechanism outside the closed registry" 1 "UNKNOWN MECHANISM"

  matrix '(cell (axis "alpha") (axis "alpha") (guest "g1")) (cell (axis "alpha") (axis "beta") (guest "g2") (degenerate "both")) (cell (axis "beta") (axis "beta") (mechanism "smoke-reproduce"))'
  arm "RED   a degenerate cell that also names a guest" 1 "DEGENERATE MIXED"

  matrix "$GOOD"
  printf '(expectations (program "g3.s") (entry "0x80000000") (instructions 0))\n' \
    > "$t/profiles/p/guests/g3.expected.sexp"
  arm "RED   a tracked guest no cell names" 1 "ORPHAN GUEST p: 'g3'"
  rm "$t/profiles/p/guests/g3.expected.sexp"

  matrix '(cell (axis "alpha") (axis "alpha") (guest "g1")) (cell (axis "alpha") (axis "beta") (guest "g2") (difference "DIFF-GHOST")) (cell (axis "beta") (axis "beta") (mechanism "smoke-reproduce"))'
  arm "RED   a difference id references.sexp does not record" 1 "UNKNOWN DIFFERENCE"

  references '(difference (id "DIFF-X") (kind "k") (observed "o") (resolution "r"))'
  matrix '(cell (axis "alpha") (axis "alpha") (guest "g1")) (cell (axis "alpha") (axis "beta") (guest "g2") (difference "DIFF-X")) (cell (axis "beta") (axis "beta") (mechanism "smoke-reproduce"))'
  arm "GREEN a named difference the dossier records" 0 "3 cells declared"

  rm "$t/profiles/p/interactions.sexp"
  arm "RED   a unit with no declared matrix" 1 "NO MATRIX"

  # ── the device-model leg (P5-BOARD.2, case sifive-uart-lab-v0): no matrix is n/a by
  # declaration (the matrix attaches with the probe corpus, P5-BOARD.5); a matrix that
  # EXISTS answers the full contract unchanged.
  printf '(profile (id "p") (version "0") (status "experimental") (vehicle (route device-model) (comparison register-expectations) (authority laboratory) (source "s")))\n' \
    > "$t/profiles/p/profile.sexp"
  arm "GREEN device-model route with no matrix is n/a by declaration" 0 "device-model route declared"

  matrix '(cell (axis "alpha") (axis "alpha") (guest "g1")) (cell (axis "alpha") (axis "beta") (guest "g2"))'
  arm "RED   a device unit whose matrix omits a cell answers the full contract" 1 "OMITTED CELL p: beta×beta"

  rm -rf "$t"
  printf 'INTERACTION-MATRIX --self-test: %d pass / %d fail\n' "$pass" "$fail"
  [ "$fail" -eq 0 ]
}

[ "${1:-}" = "--self-test" ] && { self_test; exit $?; }

self_test >/dev/null 2>&1 || {
  echo "INTERACTION-MATRIX: REFUSED — the check does not discriminate (self-test failed)." >&2; exit 2; }

out="$(check_units "$ROOT" git)"; rc=$?
count="$(printf '%s' "$out" | sed -n 's/^__CHECKED__ //p')"
body="$(printf '%s' "$out" | grep -v '^__CHECKED__ ' || true)"
if [ "$rc" -eq 2 ]; then
  { echo "INTERACTION-MATRIX: REFUSED — the unit corpus could not be read."
    printf '%s\n' "$body" | sed 's/^/  /'; } >&2
  exit 2
fi
if [ "$rc" -ne 0 ]; then
  { echo "INTERACTION-MATRIX: the declared matrix does not hold."
    printf '%s\n' "$body" | sed 's/^/  /'
    echo "  Declare every cell and resolve every disposition — unexercised cells are reported, not omitted."; } >&2
  exit 1
fi
printf '%s\n' "$body"
printf 'INTERACTION-MATRIX: ok (%s unit(s) — every derived cell declared, every disposition resolved, no orphan guests)\n' "${count:-0}"
exit 0
