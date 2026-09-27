#!/usr/bin/env bash
# scripts/check_scope_coverage.sh — SCOPE-COVERAGE (project doctrine).
#
# The director's rule, mechanized (MODEL-METHOD.6): no model implementation for a profile while
# a category its DECLARED SCOPE requires is `missing`. The unit registry (materials/units.sexp)
# declares, per unit, the categories its scope REQUIRES; the census
# (materials/category-needs.sexp) declares what each category's disposition is. This gate
# refuses the day a required category is `missing` — or has no census row at all — because
# model code built on a category whose facts are not extractable is code built on an
# intention. `P1-LAB`'s precondition is THIS VERDICT, not a judgement call.
#
# ⛔ Composes with EXTRACTION (MODEL-METHOD.10), does not duplicate it: a category may be
# covered while the definition is still insufficient (one set, four ways), and both must pass.
# Coverage says the category's facts are OWNED; extraction says they are EXTRACTABLE.
#
# CONTRACT: exit code is the verdict; explains on stderr; deterministic; read-only; no network.
#   --self-test   run the RED/GREEN controls against synthetic fixtures and exit.
set -uo pipefail
ROOT="$(git rev-parse --show-toplevel)"; cd "$ROOT"

command -v python3 >/dev/null 2>&1 || {
  echo "SCOPE-COVERAGE: REFUSED — python3 is not on PATH; this check cannot judge." >&2; exit 2; }

check_coverage() { # $1 = root; $2 = "git" (tracked only) or "fs"
python3 - "$1" "$2" <<'PY'
import subprocess, sys
from pathlib import Path

root = Path(sys.argv[1]); mode = sys.argv[2]
sys.path.insert(0, "scripts")
import records_sexp as R
import sexp as S

if mode == "git":
    out = subprocess.run(["git", "ls-files", "--", "materials/units.sexp"],
                         capture_output=True, text=True, check=True).stdout
    registries = [root / p for p in out.splitlines() if p.strip()]
else:
    registries = sorted(root.glob("materials/units.sexp"))

if not registries:
    print("SCOPE-COVERAGE: REFUSED — no unit registry found; this check cannot judge")
    print("__CHECKED__ 0"); sys.exit(2)

findings, checked = [], 0
for reg in registries:
    try:
        units = R.load(reg)
    except (R.RecordRefused, S.SexpError) as exc:
        findings.append(f"UNREADABLE {reg.relative_to(root)}: {exc}")
        continue
    needs_path = reg.parent / "category-needs.sexp"
    needs: dict[tuple[str, str], dict] = {}
    if needs_path.is_file():
        try:
            needs = {(n.get("unit"), n.get("category")): n
                     for n in R.load(needs_path)}
        except (R.RecordRefused, S.SexpError):
            findings.append(f"UNREADABLE {needs_path.relative_to(root)}: the census beside "
                            f"the registry does not map — coverage against a census nobody "
                            f"can read proves nothing")
    else:
        findings.append(f"NO CENSUS {reg.relative_to(root)}: no category-needs.sexp beside "
                        f"the registry — required categories cannot be checked without it")
    for u in units:
        checked += 1
        uid = u.get("id")
        required = u.get("requires") or []
        if not required:
            findings.append(f"UNDECLARED SCOPE {reg.name} [{uid}]: the unit declares no "
                            f"required categories — model code may not start against a scope "
                            f"that was never declared")
            continue
        for cat in required:
            row = needs.get((uid, cat))
            if row is None:
                findings.append(f"UNCOVERED REQUIRED {reg.name} [{uid} requires {cat}]: no "
                                f"census row at all — the declared scope is uncovered")
            elif row.get("disposition") == "missing":
                findings.append(f"MISSING REQUIRED {reg.name} [{uid} requires {cat}]: the "
                                f"census disposition is 'missing' — model code may not start "
                                f"against a category the unit's scope requires and the "
                                f"catalogue lacks. Close the gap or shrink the declaration.")
            elif row.get("disposition") not in ("covered", "partial", "out-of-scope",
                                                "deferred-to-board"):
                findings.append(f"UNKNOWN DISPOSITION {reg.name} [{uid} requires {cat}]: "
                                f"'{row.get('disposition')}' is not a disposition the gate "
                                f"can judge")

for f in findings:
    print(f)
print(f"__CHECKED__ {checked}")
sys.exit(1 if findings else 0)
PY
}

self_test() {
  SELFTEST_TMP() { local d="$ROOT/target/doctrine-selftest"; mkdir -p "$d"; mktemp -d "$d/XXXXXX"; }
  local t pass=0 fail=0 out rc
  t="$(SELFTEST_TMP)"; mkdir -p "$t/materials"

  argc() {
    [ "$2" -eq "$1" ] && return 0
    fail=$((fail+1))
    printf 'SCOPE-COVERAGE self-test HARNESS: %s() got %s argument(s), expected %s — a missing `;` before `arm` swallows it\n' "$3" "$2" "$1" >&2
    return 1
  }
  arm() {
    argc 3 "$#" arm || return
    out="$(check_coverage "$t" fs 2>&1)"; rc=$?
    if [ "$rc" != "$2" ]; then
      fail=$((fail+1)); printf 'SCOPE-COVERAGE self-test MISS: %s expected rc=%s got rc=%s\n%s\n' "$1" "$2" "$rc" "$out" >&2
    elif ! printf '%s' "$out" | grep -qF "$3"; then
      fail=$((fail+1)); printf 'SCOPE-COVERAGE self-test MISS: %s right verdict, wrong reason (no %s)\n%s\n' "$1" "$3" "$out" >&2
    else pass=$((pass+1)); fi
  }

  units() { printf '%s\n' "$1" > "$t/materials/units.sexp"; }
  needs() { printf '%s\n' "$1" > "$t/materials/category-needs.sexp"; }
  rm -f "$t/materials/units.sexp" "$t/materials/category-needs.sexp"

  arm "REFUSE no unit registry at all" 2 "cannot judge"

  units '(unit (id "p") (kind processor) (layer processor) (book "b") (requires "C01"))'
  rm -f "$t/materials/category-needs.sexp"
  arm "REFUSE a registry with no census beside it" 1 "NO CENSUS"

  needs '(category-need (category "C01") (layer processor) (kind k) (unit "p") (disposition covered) (material "M"))'
  arm "GREEN a required category covered" 0 "__CHECKED__ 1"

  needs '(category-need (category "C01") (layer processor) (kind k) (unit "p") (disposition missing) (reason "owed"))'
  arm "RED   the acceptance's shape: a required category missing" 1 "MISSING REQUIRED"

  needs '(category-need (category "C99") (layer processor) (kind k) (unit "p") (disposition covered) (material "M"))'
  arm "RED   a required category with no census row" 1 "UNCOVERED REQUIRED"

  units '(unit (id "p") (kind processor) (layer processor) (book "b"))'
  arm "RED   a unit that declares no scope" 1 "UNDECLARED SCOPE"

  units '(unit (id "p") (kind processor) (layer processor) (book "b") (requires "C01"))'
  needs '(category-need (category "C01") (layer processor) (kind k) (unit "p") (disposition covered) (material "M"))
(category-need (category "C07") (layer processor) (kind k) (unit "p") (disposition missing) (reason "excluded subsystem"))'
  arm "GREEN a missing category the scope does NOT require is legal" 0 "__CHECKED__ 1"

  rm -rf "$t"
  printf 'SCOPE-COVERAGE --self-test: %d pass / %d fail\n' "$pass" "$fail"
  [ "$fail" -eq 0 ]
}

[ "${1:-}" = "--self-test" ] && { self_test; exit $?; }

self_test >/dev/null 2>&1 || {
  echo "SCOPE-COVERAGE: REFUSED — the check does not discriminate (self-test failed)." >&2; exit 2; }

out="$(check_coverage "$ROOT" git)"; rc=$?
count="$(printf '%s' "$out" | sed -n 's/^__CHECKED__ //p')"
body="$(printf '%s' "$out" | grep -v '^__CHECKED__ ' || true)"
if [ "$rc" -eq 2 ]; then
  { echo "SCOPE-COVERAGE: REFUSED — the unit corpus could not be read."
    printf '%s\n' "$body" | sed 's/^/  /'; } >&2
  exit 2
fi
if [ "$rc" -ne 0 ]; then
  { echo "SCOPE-COVERAGE: model code may not start — the declared scope is uncovered."
    printf '%s\n' "$body" | sed 's/^/  /'
    echo "  The declaration is the authority. Close the gap or shrink the declaration."; } >&2
  exit 1
fi
printf 'SCOPE-COVERAGE: ok (%s unit(s) may code — every required category covered)\n' "${count:-0}"
exit 0
