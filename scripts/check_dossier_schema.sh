#!/usr/bin/env bash
# scripts/check_dossier_schema.sh — DOSSIER-SCHEMA (project doctrine).
#
# WHY THIS EXISTS, measured rather than argued. Until 2026-10-01 no gate validated the
# dossier documents (profile/state/sources/references/encoding/interactions/…) against
# their schemas as a class: RECORD-SCHEMA covers the record files, and the other gates
# consume the dossier through the strict mapping owner — which refuses undeclared FIELDS
# but not facet violations. Measured consequence: `profiles/rv64i-lab-v0/profile.sexp`
# carried two `note` fields on D-FENCE against the schema's single-valued declaration,
# and nothing said a word (found by P3-BREADTH.5 slice 2's corpus re-validation). A schema
# nothing enforces is documentation, not a contract.
#
# THE RULE: every tracked `profiles/*/*.sexp` whose basename has a same-named
# `schema/*.sexp` validates against it through the one checker
# (`scripts/check_sexp_schema.py`). A dossier document whose basename has NO same-named
# schema is skipped and counted BY NAME in the verdict — absence is reported, never
# silent. A checker refusal (rc 2 — cannot judge) propagates as this gate's refusal.
#
# Fired RED before registration: the pre-fix D-FENCE document (recovered from git history)
# fails this sweep with `duplicated single-valued field "note"` — the exact drift class
# the gate exists to catch — and the self-test's RED arm fires on a facet violation in a
# scratch corpus.
#
# CONTRACT: exit code is the verdict; explains on stderr; deterministic; read-only; no
# network.  --self-test   run the RED/GREEN controls against synthetic fixtures and exit.
set -uo pipefail
ROOT="$(git rev-parse --show-toplevel)"; cd "$ROOT"

command -v python3 >/dev/null 2>&1 || {
  echo "DOSSIER-SCHEMA: REFUSED — python3 is not on PATH; this check cannot judge." >&2; exit 2; }

CHECKER="$ROOT/scripts/check_sexp_schema.py"
[ -f "$CHECKER" ] || {
  echo "DOSSIER-SCHEMA: REFUSED — the schema checker is missing; this gate cannot judge." >&2; exit 2; }

check_tree() { # $1 = root (the tree to sweep); $2 = "git" (tracked only) or "fs"
python3 - "$1" "$2" "$CHECKER" <<'PY'
import subprocess, sys
from pathlib import Path

root = Path(sys.argv[1]); mode = sys.argv[2]
checker = Path(sys.argv[3])
if mode == "git":
    out = subprocess.run(["git", "ls-files", "--", "profiles/*/*.sexp"],
                         capture_output=True, text=True, check=True).stdout
    docs = [root / p for p in out.splitlines() if p.strip()]
else:
    docs = sorted((root / "profiles").glob("*/*.sexp"))

findings, validated, skipped = [], [], []
# The two suffixed document families map to their family schema: <guest>.expected.sexp →
# expectations.sexp, <name>.override.sexp → override.sexp. Everything else needs a
# same-named schema or it is skipped — and counted by name in the verdict.
SUFFIX_SCHEMAS = ((".expected.sexp", "expectations.sexp"),
                  (".override.sexp", "override.sexp"))
for doc in sorted(docs):
    schema_name = doc.name
    for suffix, family in SUFFIX_SCHEMAS:
        if doc.name.endswith(suffix):
            schema_name = family
            break
    schema = root / "schema" / schema_name
    tag = doc.relative_to(root).as_posix()
    if not schema.is_file():
        skipped.append(doc.name)
        continue
    r = subprocess.run([sys.executable, str(checker), str(doc), str(schema)],
                       capture_output=True, text=True)
    if r.returncode == 2:
        findings.append(f"CANNOT JUDGE {tag}: {(r.stderr or r.stdout).strip()}")
    elif r.returncode != 0:
        findings.append(f"REFUSED {tag}: {(r.stderr or r.stdout).strip().splitlines()[0]}")
    else:
        validated.append(tag)
for f in findings:
    print(f)
print(f"__VALIDATED__ {len(validated)} __SKIPPED__ {len(skipped)} "
      f"({', '.join(sorted(set(skipped))) if skipped else 'none'})")
sys.exit(1 if findings else 0)
PY
}

# ── self-test ────────────────────────────────────────────────────────────────────────────
SELFTEST_TMP() { local d="$ROOT/target/doctrine-selftest"; mkdir -p "$d"; mktemp -d "$d/XXXXXX"; }

self_test() {
  local t pass=0 fail=0 out rc
  t="$(SELFTEST_TMP)"; mkdir -p "$t/profiles/p" "$t/schema"

  # ⛔ STRICT ARITY (docs/knowledge/self-test-arms-that-never-ran.md).
  argc() {
    [ "$2" -eq "$1" ] && return 0
    fail=$((fail+1))
    printf 'DOSSIER-SCHEMA self-test HARNESS: %s() got %s argument(s), expected %s — a missing `;` before `arm` swallows it\n' \
      "$3" "$2" "$1" >&2
    return 1
  }
  arm() { # arm <name> <rc> <expected-rc> <output> <reason substring>
    argc 5 "$#" arm || return
    if [ "$2" = "$3" ] && printf '%s' "$4" | grep -qF "$5"; then
      pass=$((pass+1))
    else
      fail=$((fail+1))
      printf 'DOSSIER-SCHEMA self-test MISS: %s — expected rc=%s (reason: %s), got rc=%s\n%s\n' \
        "$1" "$3" "$5" "$2" "$4" >&2
    fi
  }

  # A minimal schema with one facet: id must match ^p[0-9]+$.
  cat > "$t/schema/profile.sexp" <<'EOF'
(schema (id "profile"))
(construct (name profile)
  (field (name id) (type string) (pattern "^p[0-9]+$")))
EOF

  printf '(profile (id "p1"))\n' > "$t/profiles/p/profile.sexp"
  out="$(check_tree "$t" fs 2>&1)"; rc=$?
  arm "GREEN a conforming document validates" "$rc" 0 "$out" "__VALIDATED__ 1"

  printf '(profile (id "nope"))\n' > "$t/profiles/p/profile.sexp"
  out="$(check_tree "$t" fs 2>&1)"; rc=$?
  arm "RED a facet violation is refused, naming it" "$rc" 1 "$out" "does not match"

  printf '(profile (id "p1"))\n' > "$t/profiles/p/profile.sexp"
  printf '(baseline (note "no same-named schema"))\n' > "$t/profiles/p/baseline.sexp"
  out="$(check_tree "$t" fs 2>&1)"; rc=$?
  arm "GREEN a document with no same-named schema is skipped BY NAME" "$rc" 0 "$out" "__SKIPPED__ 1 (baseline.sexp)"

  rm -rf "$t"
  printf 'DOSSIER-SCHEMA --self-test: %d pass / %d fail\n' "$pass" "$fail"
  [ "$fail" -eq 0 ]
}

if [ "${1:-}" = "--self-test" ]; then
  self_test
  exit $?
fi

# Re-run the controls before judging: a check that no longer discriminates must refuse,
# not pass (the project-doctrine contract in scripts/check_doctrines.project.sh).
self_test >/dev/null 2>&1 || {
  echo "DOSSIER-SCHEMA: REFUSED — the check does not discriminate (self-test failed)." >&2
  exit 2; }

out="$(check_tree "$ROOT" git)"; rc=$?
if [ "$rc" -ne 0 ]; then
  { echo "DOSSIER-SCHEMA: a dossier document violates its schema."
    printf '%s\n' "$out" | grep -v '^__VALIDATED__' | sed 's/^/  /'
    echo "  The SCHEMA is the contract: fix the document, or change the schema with the"
    echo "  case named — never leave the two disagreeing."; } >&2
  exit 1
fi
printf 'DOSSIER-SCHEMA: ok (%s)\n' "$(printf '%s\n' "$out" | sed -n 's/^__VALIDATED__ //p')"
exit 0
