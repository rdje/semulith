#!/usr/bin/env bash
# scripts/check_source_format.sh — SOURCE-FORMAT (project doctrine).
#
# WHY THIS EXISTS: `SOT-FORMAT` retired the format split — every source of truth the generator
# engine extracts from is S-expression — but retirement recorded in prose is how a split
# returns by accident: one `profile.toml` copied back from an old branch, one JSONL export
# re-committed, and the merge rule `SOT-FORMAT.5` defines is meaningless again. This gate
# refuses the return.
#
# Corpus: the four source-of-truth families the routes registry governs as partitioned
# destinations — `definitions/`, `schema/`, `profiles/`, `materials/` (doctrine/readme_routes.tsv
# owns which families hold sources of truth; this check names the same four with that owner
# recorded here). Scope per the tree's non-goals: `examples/` stays JSONL on purpose (frozen
# delivery artifacts, `SOT-FORMAT.3`), `docs/` stays Markdown, and under `profiles/` the
# dossier prose (`*.md`) and guest programs (`*.s`) are not sources of truth. The gate refuses
# exactly the split's shapes, never prose or programs.
#
# Arms:
#   FORMAT  a tracked `.toml` / `.json` / `.jsonl` / `.yaml` / `.yml` in any of the four
#           families is refused by name — a source of truth outside the format.
#   PARSES  every tracked `.sexp` in the corpus parses with `scripts/sexp.py` — "in the
#           format" means the one reader reads it.
# An empty corpus is REFUSED (nothing to judge) — the same discipline the record gates carry.
#
# Schema coverage is deliberately NOT this gate's lane: RECORD-SCHEMA owns the record
# catalogues, PROFILE-CONSISTENCY the dossier, the kernel the fixpoint, compare_readers.py the
# reader agreement. Two gates reporting one breach is noise; SOURCE-FORMAT owns exactly one
# question — nothing outside the format, nothing unreadable inside it.
#
# CONTRACT: exit code is the verdict; explains on stderr; deterministic; read-only; no network.
#   --self-test   run the RED/GREEN controls against synthetic fixtures and exit.
set -uo pipefail
ROOT="$(git rev-parse --show-toplevel)"; cd "$ROOT"

command -v python3 >/dev/null 2>&1 || {
  echo "SOURCE-FORMAT: REFUSED — python3 is not on PATH; this check cannot judge." >&2; exit 2; }

FAMILIES="definitions schema profiles materials"
RETIRED_RE='\.(toml|json|jsonl|yaml|yml)$'

check_source_format() { # $1 = root to scan; $2 = "git" (tracked only) or "fs" (everything there)
python3 - "$1" "$2" $FAMILIES <<'PY'
import re, subprocess, sys
from pathlib import Path

sys.path.insert(0, "scripts")
import sexp as S

root = Path(sys.argv[1]); mode = sys.argv[2]; families = sys.argv[3:]
retired = re.compile(r"\.(toml|json|jsonl|yaml|yml)$")

if mode == "git":
    out = subprocess.run(["git", "ls-files", "--", *families],
                         capture_output=True, text=True, check=True).stdout
    paths = [root / p for p in out.splitlines() if p.strip()]
else:
    paths = [p for fam in families for p in (root / fam).rglob("*") if p.is_file()]

findings, corpus = [], []
for p in sorted(paths):
    rel = str(p.relative_to(root)) if p.is_relative_to(root) else str(p)
    if retired.search(str(p)):
        ext = str(p).rsplit(".", 1)[-1]
        findings.append(
            f"OUTSIDE FORMAT {rel}: a .{ext} file inside a source-of-truth family — the "
            f"format split is retired (decision_one-format-every-source-of-truth); a source "
            f"of truth is S-expression or it is refused")
        continue
    if str(p).endswith(".sexp"):
        corpus.append((p, rel))

if not paths:
    print("SOURCE-FORMAT: REFUSED — no file at all under the source-of-truth families; "
          "this check cannot judge an empty corpus")
    print("__CHECKED__ 0"); sys.exit(2)
if not corpus:
    findings.append("NO SEXP SOURCE: not one .sexp under the source-of-truth families — "
                    "the engine has nothing to extract from")

for p, rel in corpus:
    try:
        S.read_file(p)
    except S.SexpError as exc:
        findings.append(f"UNREADABLE {rel}: does not parse with scripts/sexp.py — {exc}")

for f in findings:
    print(f)
print(f"__CHECKED__ {len(corpus)}")
sys.exit(1 if findings else 0)
PY
}

self_test() {
  SELFTEST_TMP() { local d="$ROOT/target/doctrine-selftest"; mkdir -p "$d"; mktemp -d "$d/XXXXXX"; }
  local t pass=0 fail=0 out rc
  t="$(SELFTEST_TMP)"; mkdir -p "$t/definitions" "$t/schema" "$t/profiles/p" "$t/materials"

  argc() {
    [ "$2" -eq "$1" ] && return 0
    fail=$((fail+1))
    printf 'SOURCE-FORMAT self-test HARNESS: %s() got %s argument(s), expected %s — a missing `;` before `arm` swallows it\n' "$3" "$2" "$1" >&2
    return 1
  }
  arm() {
    argc 3 "$#" arm || return
    out="$(check_source_format "$t" fs 2>&1)"; rc=$?
    if [ "$rc" != "$2" ]; then
      fail=$((fail+1)); printf 'SOURCE-FORMAT self-test MISS: %s expected rc=%s got rc=%s\n%s\n' "$1" "$2" "$rc" "$out" >&2
    elif ! printf '%s' "$out" | grep -qF "$3"; then
      fail=$((fail+1)); printf 'SOURCE-FORMAT self-test MISS: %s right verdict, wrong reason (no %s)\n%s\n' "$1" "$3" "$out" >&2
    else pass=$((pass+1)); fi
  }

  printf '%s\n' '(fragment (id "riscv/x") (kind extension) (requires "riscv/rv64i"))' \
    > "$t/definitions/x.sexp"
  arm "GREEN a corpus of well-formed .sexp" 0 "__CHECKED__ 1"

  printf '%s\n' '[profile]' 'id = "ghost"' > "$t/profiles/p/profile.toml"
  arm "RED   the split returns: a .toml in a source-of-truth family" 1 "OUTSIDE FORMAT"

  printf '%s\n' '{"id":"REQ-GHOST"}' > "$t/materials/requirements.jsonl"
  arm "RED   a records-shaped .jsonl re-committed" 1 "OUTSIDE FORMAT"

  printf '%s\n' '(sources (source (id "A"' > "$t/profiles/p/sources.sexp"
  arm "RED   a .sexp the one reader refuses" 1 "UNREADABLE"

  printf '%s\n' '# dossier prose, not a source of truth' > "$t/profiles/p/DOSSIER.md"
  printf '%s\n' '    add a0, a1, a2' > "$t/profiles/p/guests.s"
  rm -f "$t/profiles/p/profile.toml" "$t/materials/requirements.jsonl" "$t/profiles/p/sources.sexp"
  arm "GREEN dossier prose and guest programs are not refused" 0 "__CHECKED__ 1"

  rm -f "$t/definitions/x.sexp"
  arm "RED   a corpus with no .sexp at all — the engine has nothing to extract from" 1 "NO SEXP SOURCE"

  rm -f "$t/profiles/p/DOSSIER.md" "$t/profiles/p/guests.s"
  arm "RED   an empty corpus is refused, not passed" 2 "cannot judge"

  rm -rf "$t"
  printf 'SOURCE-FORMAT --self-test: %d pass / %d fail\n' "$pass" "$fail"
  [ "$fail" -eq 0 ]
}

[ "${1:-}" = "--self-test" ] && { self_test; exit $?; }

self_test >/dev/null 2>&1 || {
  echo "SOURCE-FORMAT: REFUSED — the check does not discriminate (self-test failed)." >&2; exit 2; }

out="$(check_source_format "$ROOT" git)"; rc=$?
count="$(printf '%s' "$out" | sed -n 's/^__CHECKED__ //p')"
body="$(printf '%s' "$out" | grep -v '^__CHECKED__ ' || true)"
if [ "$rc" -eq 2 ]; then
  { echo "SOURCE-FORMAT: REFUSED — the source-of-truth corpus could not be read."
    printf '%s\n' "$body" | sed 's/^/  /'; } >&2
  exit 2
fi
if [ "$rc" -ne 0 ]; then
  { echo "SOURCE-FORMAT: a source of truth lives outside the one format."
    printf '%s\n' "$body" | sed 's/^/  /'
    echo "  The format decision is authoritative. Convert the file, or it does not land."; } >&2
  exit 1
fi
printf 'SOURCE-FORMAT: ok (%s source-of-truth file(s) under definitions/ schema/ profiles/ materials/, all in the one format)\n' "${count:-0}"
exit 0
