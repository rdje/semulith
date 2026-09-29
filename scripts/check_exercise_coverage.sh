#!/usr/bin/env bash
# scripts/check_exercise_coverage.sh — EXERCISE-COVERAGE (project doctrine).
#
# P2-SCALAR.1's acceptance, mechanized: every RV64I form the profile DECLARES in its scope is
# EXECUTED by at least one tracked guest — coverage reported with its denominator, never as a
# bare count. The denominator is the profile dossier's `[scope]` mnemonic lists (count_total
# re-derived against them — a declaration whose count disagrees with its own enumeration is a
# DENOMINATOR LIE). The numerator is the union of mnemonics the tracked expectation documents
# declare executed; the commit gate (the verify-side offline differential) already proves those
# exact steps execute, so "declared executed" and "executed" cannot drift apart silently.
#
# SCP-02 rides the same verdict: the unit's encoding composition is resolved through the ONE
# shared resolver (`riscv_asm.resolve_composition`), so an unmet `requires` or a missing
# fragment is refused by name, and every declared form must exist in the resolved composition —
# a scope entry the composition cannot provide is an unresolved dependency, not a feature.
#
# ⛔ Composes with EXTRACTION, does not duplicate it: EXTRACTION proves every declared
# instruction HAS encoding+semantics+requirement (static sufficiency); this gate proves every
# declared form RAN under the laboratory (dynamic exercise). A model can pass one and fail the
# other in both directions.
#
# CONTRACT: exit code is the verdict; explains on stderr; deterministic; read-only; no network.
#   --self-test   run the RED/GREEN controls against synthetic fixtures and exit.
set -uo pipefail
ROOT="$(git rev-parse --show-toplevel)"; cd "$ROOT"

command -v python3 >/dev/null 2>&1 || {
  echo "EXERCISE-COVERAGE: REFUSED — python3 is not on PATH; this check cannot judge." >&2; exit 2; }

check_coverage() { # $1 = root; $2 = "git" (tracked only) or "fs"
python3 - "$1" "$2" <<'PY'
import subprocess, sys
from pathlib import Path

root = Path(sys.argv[1]); mode = sys.argv[2]
sys.path.insert(0, "scripts")
import sexp as S
from riscv_asm import resolve_composition, AsmError

if mode == "git":
    out = subprocess.run(["git", "ls-files", "--", "profiles/*/profile.sexp"],
                         capture_output=True, text=True, check=True).stdout
    profiles = [root / p for p in out.splitlines() if p.strip()]
else:
    profiles = sorted(root.glob("profiles/*/profile.sexp"))

if not profiles:
    print("EXERCISE-COVERAGE: REFUSED — no tracked profile dossier found; this check cannot judge")
    print("__CHECKED__ 0"); sys.exit(2)

findings, checked = [], 0
for prof_path in profiles:
    pdir = prof_path.parent
    tag = prof_path.relative_to(root).as_posix()
    try:
        forms = S.read_file(prof_path)
        form = next(f for f in forms if isinstance(f, list) and f and str(f[0]) == "profile")
    except (S.SexpError, StopIteration) as exc:
        findings.append(f"UNREADABLE {tag}: {exc}")
        continue
    scopes = S.children(form, "scope")
    if not scopes:
        findings.append(f"UNDECLARED SCOPE {tag}: the dossier declares no [scope] — coverage "
                        f"against a scope that was never declared proves nothing")
        continue
    scope = scopes[0]
    denominator: set[str] = set()
    for f in scope[1:]:
        if isinstance(f, list) and f and str(f[0]) not in ("count_base", "count_rv64i_additions",
                                                           "count_total", "authority", "source"):
            denominator |= {str(v).lower() for v in f[1:]}
    declared_total = None
    totals = S.children(scope, "count_total")
    if totals:
        declared_total = int(totals[0][1])
    checked += 1
    if declared_total is None:
        findings.append(f"DENOMINATOR ABSENT {tag}: [scope] carries no count_total — a denominator "
                        f"nobody states is a coverage claim nobody can check")
    elif declared_total != len(denominator):
        findings.append(f"DENOMINATOR LIE {tag}: count_total says {declared_total} but the "
                        f"mnemonic lists enumerate {len(denominator)} — the declaration "
                        f"contradicts its own enumeration")
    # SCP-02: the composition resolves through the one resolver; every declared form exists in it.
    enc_path = pdir / "encoding.sexp"
    resolved: set[str] = set()
    closure = "unresolved"
    if not enc_path.is_file():
        findings.append(f"NO COMPOSITION {tag}: no encoding.sexp beside the dossier — the "
                        f"declared scope's dependency closure cannot be decided")
    else:
        try:
            enc = S.read_file(enc_path)[0]
            comp = S.children(enc, "compose")
            base = str(S.field(comp[0], "base", str(enc_path)))
            ext = S.children(comp[0], "extensions")
            names = [base] + [str(x) for x in (ext[0][1:] if ext else [])]
            merged = resolve_composition(enc, enc_path)
            resolved = {str(S.field(i, "name")) for i in S.children(merged, "insn")}
            closure = "{" + ", ".join(names) + "}"
        except (AsmError, S.SexpError, IndexError) as exc:
            findings.append(f"UNMET DEPENDENCY {tag}: {exc}")
    for m in sorted(denominator - resolved):
        findings.append(f"UNRESOLVED FORM {tag}: [scope] declares '{m}' but the resolved "
                        f"composition does not provide it — an included feature whose "
                        f"dependency is not closed (SCP-02)")
    # exercised: the union of mnemonics the tracked expectation documents declare executed.
    exercised: set[str] = set()
    expected_files = sorted(pdir.glob("guests/*.expected.sexp"))
    if not expected_files:
        findings.append(f"NO GUESTS {tag}: no guests/*.expected.sexp — nothing is exercised")
    for ef in expected_files:
        etag = ef.relative_to(root).as_posix()
        try:
            eforms = S.read_file(ef)
            eform = next(f for f in eforms
                         if isinstance(f, list) and f and str(f[0]) == "expectations")
        except (S.SexpError, StopIteration) as exc:
            findings.append(f"UNREADABLE {etag}: {exc}")
            continue
        for step in S.children(eform, "step"):
            insn = S.children(step, "insn")
            if not insn:
                findings.append(f"UNNAMED STEP {etag}: a step declares no insn — an exercised "
                                f"form nobody names cannot be counted")
                continue
            text = str(insn[0][1]).strip()
            if text:
                exercised.add(text.split()[0].lower())
    unexercised = sorted(denominator - exercised)
    for m in unexercised:
        findings.append(f"UNEXERCISED {tag}: '{m}' is in the declared scope but no tracked "
                        f"guest executes it — coverage is {len(denominator) - len(unexercised)}"
                        f"/{len(denominator)}, not complete")
    if not findings:
        print(f"{pdir.relative_to(root).as_posix()}: exercised {len(exercised & denominator)}"
              f"/{len(denominator)} declared forms; SCP-02 closure {closure} resolved")
    print(f"__EXERCISED__ {len(denominator) - len(unexercised)}/{len(denominator)}")

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
    printf 'EXERCISE-COVERAGE self-test HARNESS: %s() got %s argument(s), expected %s\n' "$3" "$2" "$1" >&2
    return 1
  }
  arm() {
    argc 3 "$#" arm || return
    out="$(check_coverage "$t" fs 2>&1)"; rc=$?
    if [ "$rc" != "$2" ]; then
      fail=$((fail+1)); printf 'EXERCISE-COVERAGE self-test MISS: %s expected rc=%s got rc=%s\n%s\n' "$1" "$2" "$rc" "$out" >&2
    elif ! printf '%s' "$out" | grep -qF "$3"; then
      fail=$((fail+1)); printf 'EXERCISE-COVERAGE self-test MISS: %s right verdict, wrong reason (no %s)\n%s\n' "$1" "$3" "$out" >&2
    else pass=$((pass+1)); fi
  }

  # A scratch unit: a two-form scope over the REAL rv64i fragment (copied), exercised by
  # synthetic expectation documents. The fixture writer functions rebuild the unit per arm.
  mkdir -p "$t/profiles/p/guests" "$t/definitions/riscv"
  cp "$ROOT/definitions/riscv/rv64i.sexp" "$t/definitions/riscv/rv64i.sexp"

  profile() { # $1 = scope body
    printf '(profile (id "p") (version "0") (status "development") (scope %s))\n' "$1" \
      > "$t/profiles/p/profile.sexp"
  }
  encoding() {
    printf '(encoding (profile "p") (ilen 32) (compose (base "riscv/rv64i") (extensions)) (fragment-root "definitions"))\n' \
      > "$t/profiles/p/encoding.sexp"
  }
  guest() { # $1 = name; $2 = space-separated mnemonics exercised
    local steps="" n=0 m
    for m in $2; do
      steps="$steps (step (n $n) (insn \"$m x1, x0, 1\") (writes) (derivation \"d\") (source \"s\"))"
      n=$((n+1))
    done
    printf '(expectations (program "%s.s") (entry "0x80000000") (instructions %s)%s)\n' \
      "$1" "$n" "$steps" > "$t/profiles/p/guests/$1.expected.sexp"
  }
  scope2='(count_total 2) (authority architecture) (source "s") (base_op "ADD") (base_op "SUB")'

  arm "REFUSE no profile dossier at all" 2 "cannot judge"

  profile "$scope2"; encoding; guest g1 "add sub"
  arm "GREEN every declared form exercised" 0 "__EXERCISED__ 2/2"

  guest g1 "add"
  arm "RED   a declared form no guest exercises, named" 1 "UNEXERCISED"

  profile '(count_total 3) (authority architecture) (source "s") (base_op "ADD") (base_op "SUB")'
  arm "RED   a count_total that contradicts the enumeration" 1 "DENOMINATOR LIE"

  profile "$scope2"
  rm -f "$t/profiles/p/encoding.sexp"
  arm "RED   a scope whose composition is absent" 1 "NO COMPOSITION"

  encoding
  profile '((count_total 1) (authority architecture) (source "s") (base_op "MUL"))'
  guest g1 "mul"
  arm "RED   a declared form the composition does not provide (SCP-02)" 1 "UNRESOLVED FORM"

  rm -rf "$t/profiles/p/guests"; mkdir -p "$t/profiles/p/guests"
  profile "$scope2"
  arm "RED   a unit with no guests at all" 1 "NO GUESTS"

  rm -rf "$t"
  printf 'EXERCISE-COVERAGE --self-test: %d pass / %d fail\n' "$pass" "$fail"
  [ "$fail" -eq 0 ]
}

[ "${1:-}" = "--self-test" ] && { self_test; exit $?; }

self_test >/dev/null 2>&1 || {
  echo "EXERCISE-COVERAGE: REFUSED — the check does not discriminate (self-test failed)." >&2; exit 2; }

out="$(check_coverage "$ROOT" git)"; rc=$?
count="$(printf '%s' "$out" | sed -n 's/^__CHECKED__ //p')"
exercised="$(printf '%s' "$out" | sed -n 's/^__EXERCISED__ //p')"
body="$(printf '%s' "$out" | grep -v '^__CHECKED__ \|^__EXERCISED__ ' || true)"
if [ "$rc" -eq 2 ]; then
  { echo "EXERCISE-COVERAGE: REFUSED — the profile corpus could not be read."
    printf '%s\n' "$body" | sed 's/^/  /'; } >&2
  exit 2
fi
if [ "$rc" -ne 0 ]; then
  { echo "EXERCISE-COVERAGE: the declared scope is not fully exercised (coverage ${exercised:-?})."
    printf '%s\n' "$body" | sed 's/^/  /'
    echo "  Every declared form must run under the laboratory — exercise it or shrink the declaration."; } >&2
  exit 1
fi
printf 'EXERCISE-COVERAGE: ok (%s profile(s) — every declared form exercised, %s)\n' "${count:-0}" "${exercised:-?}"
exit 0
