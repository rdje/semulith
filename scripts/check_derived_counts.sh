#!/usr/bin/env bash
# scripts/check_derived_counts.sh — DERIVED-COUNTS (project doctrine).
#
# A live document that states "N of something" has written down a CONSTANT THAT IS A FUNCTION OF
# THE REPOSITORY, which `docs/CLAIM_VERIFICATION.md` §5B says must be derived or gated, never
# carried. `TREE-CLAIMS` already covers the counts that describe task-trees. This covers the rest:
# registry rows, registered doctrines, book chapters, self-test arms.
#
# ⭐ FOUNDING MEASUREMENT, and it is embarrassing on purpose. In a single working session this
# repository committed TWO of these numbers wrong:
#     "24 destinations governed"  — the registry held 25 rows, stale since SEMULITH-P0-0013
#     "107 self-test arms"        — the real total was 112
# Both were maintained as RUNNING TOTALS: someone added a delta to a number they had not
# re-derived. That is the whole failure mode. A running total is not a measurement; it is a
# memory of one, and it drifts silently because nothing recomputes it.
#
# ⛔ THE SCOPE IS DATA. Which documents are live comes from `doctrine/readme_routes.tsv`'s
# `hot_live` rows — the same source `TREE-CLAIMS` uses — so a newly registered live surface is
# covered the day it is registered, and `append_history` files are excluded because a changelog
# line was true when written.
#
# ⚠️ HONEST LIMIT: it checks the counts it knows how to enumerate. A count whose population this
# script cannot enumerate is invisible to it, which is why each enumerator is NAMED below rather
# than hidden — the next reader can see exactly which claims are covered and which are not.
#
# CONTRACT: exit code is the verdict; explains on stderr; deterministic; read-only; no network.
#   --self-test   run the RED/GREEN controls against synthetic fixtures and exit.
#   --list        print each covered claim, its enumerator, and the value it currently derives.
set -uo pipefail
ROOT="$(git rev-parse --show-toplevel)"; cd "$ROOT"

# ─────────────────────────────────────────────────────────────────── the covered claims
# Each entry: <label>|<extended regex with ONE capturing group for the number>|<enumerator>
# The enumerator is shell that prints a single integer. Keep each one a single obvious command:
# an enumerator nobody can read is a second place for the truth to hide.
count_claims() {
  cat <<'CLAIMS'
routed destinations|([0-9]+) destinations governed|grep -cv '^#\|^$' doctrine/readme_routes.tsv
project doctrines|([0-9]+) registered|grep -cE '^  "[A-Z]' scripts/check_doctrines.project.sh
book chapters|([0-9]+) chapters|grep -cE '^\s*-? ?\[' docs/book/src/SUMMARY.md
self-test arms|([0-9]+) self-test arms|arm_total
open upstream issues|([0-9]+) open upstream issues|python3 scripts/upstream_exposure.py --open-count
CLAIMS
}

# The arm total spans every registered project check, and the two harness idioms in use: most
# call `arm "<name>" <rc> "<reason>"`, `check_seam_integrity.sh` calls `score`. Counting only one
# idiom would report a confident wrong number — which is this doctrine's own failure mode.
arm_total() {
  local total=0 n
  while IFS= read -r f; do
    [ -f "$f" ] || continue
    n=$(grep -cE '(^|[; ])arm "' "$f"); total=$((total + n))
    n=$(grep -cE '^[[:space:]]+score "' "$f"); total=$((total + n))
  done < <(grep -oE 'scripts/check_[a-z_]+\.sh' scripts/check_doctrines.project.sh | sort -u)
  printf '%s\n' "$total"
}
export -f arm_total 2>/dev/null || true

live_docs() {
  awk -F'\t' '!/^#/ && NF>3 && $3=="hot_live" && $1 !~ /\/$/ {print $1}' doctrine/readme_routes.tsv
}

check_counts() { # $1 = root to resolve against; $2 = claims provider fn; $3 = live-docs provider fn
  local base="$1" claims_fn="$2" docs_fn="$3" findings=0 checked=0
  local label pat enum want got doc line
  while IFS='|' read -r label pat enum; do
    [ -n "$label" ] || continue
    case "$pat" in
      '([0-9]+)'*) ;;
      *) echo "BAD PATTERN $label: '$pat' must BEGIN with its ([0-9]+) group — the number is"\
              " taken off the front of the match"; findings=$((findings+1)); continue ;;
    esac
    if ! want="$(cd "$base" && eval "$enum" 2>/dev/null | tr -d '[:space:]')" || [ -z "$want" ]; then
      echo "NO ENUMERATOR $label: '$enum' produced nothing — the check cannot judge this claim"
      findings=$((findings+1)); continue
    fi
    while IFS= read -r doc; do
      [ -f "$base/$doc" ] || continue
      while IFS= read -r line; do
        # ⛔ Extract with grep -o, NOT with a sed substitution. The first cut used
        # `sed -nE "s/.*${pat}.*/\1/p"`, whose leading `.*` is GREEDY: on "12 widgets" it
        # consumed the "1" and captured "2", so a drifting count could read as a matching one.
        # Every pattern below begins with its number group, so the match itself starts with the
        # digits and they can be taken off the front.
        got="$(printf '%s' "$line" | grep -oE "$pat" | head -1 | grep -oE '^[0-9]+')"
        [ -n "$got" ] || continue
        checked=$((checked+1))
        if [ "$got" != "$want" ]; then
          echo "COUNT DRIFT $doc: claims '$got' $label; the repository has $want  [$enum]"
          findings=$((findings+1))
        fi
      done < <(grep -E "$pat" "$base/$doc" 2>/dev/null || true)
    done < <(cd "$base" && "$docs_fn")
  done < <("$claims_fn")
  printf '__CHECKED__ %s\n' "$checked"
  [ "$findings" -eq 0 ]
}

self_test() {
  SELFTEST_TMP() { local d="$ROOT/target/doctrine-selftest"; mkdir -p "$d"; mktemp -d "$d/XXXXXX"; }
  local t pass=0 fail=0 out rc
  t="$(SELFTEST_TMP)"

  # ⛔ STRICT ARITY — docs/knowledge/self-test-arms-that-never-ran.md.
  argc() {
    [ "$2" -eq "$1" ] && return 0
    fail=$((fail+1))
    printf 'DERIVED-COUNTS self-test HARNESS: %s() got %s argument(s), expected %s — a missing `;` before `arm` swallows it\n' \
      "$3" "$2" "$1" >&2
    return 1
  }
  fx_claims() { printf '%s\n' "widgets|([0-9]+) widgets|wc -l < pop.txt"; }
  fx_docs()   { printf '%s\n' "LIVE.md"; }
  pop()  { argc 1 "$#" pop  || return; seq 1 "$1" > "$t/pop.txt"; }
  doc()  { argc 1 "$#" doc  || return; printf '%s\n' "$1" > "$t/LIVE.md"; }
  arm()  { # arm <name> <expected-rc> <expected-substring>
    argc 3 "$#" arm || return
    out="$(check_counts "$t" fx_claims fx_docs 2>&1)"; rc=$?
    if [ "$rc" != "$2" ]; then
      fail=$((fail+1)); printf 'DERIVED-COUNTS self-test MISS: %s expected rc=%s got rc=%s\n%s\n' "$1" "$2" "$rc" "$out" >&2
    elif ! printf '%s' "$out" | grep -qF "$3"; then
      fail=$((fail+1)); printf 'DERIVED-COUNTS self-test MISS: %s right verdict, wrong reason (no %s)\n%s\n' "$1" "$3" "$out" >&2
    else pass=$((pass+1)); fi
  }

  pop 7; doc 'the system has 7 widgets today.';        arm "GREEN the count matches the population" 0 "__CHECKED__ 1"
  doc 'the system has 6 widgets today.';               arm "RED   the count is stale"          1 "COUNT DRIFT"
  doc 'the system has 8 widgets today.';               arm "RED   the count is ahead"          1 "COUNT DRIFT"
  doc 'no claim of that shape here at all.';           arm "GREEN a document making no claim"  0 "__CHECKED__ 0"
  doc 'first says 7 widgets
and a second line says 6 widgets.';                    arm "RED   one of two claims drifts"    1 "COUNT DRIFT"
  pop 12; doc 'the system has 7 widgets today.';       arm "RED   the population changed under a fixed number" 1 "COUNT DRIFT"
  pop 12; doc 'the system has 12 widgets today.';      arm "GREEN re-derived after the change (two digits)" 0 "__CHECKED__ 1"
  pop 2;  doc 'the system has 12 widgets today.';      arm "RED   a two-digit claim is not read as its last digit" 1 "COUNT DRIFT"
  pop 12
  fx_claims() { printf '%s\n' "widgets|widgets: ([0-9]+)|wc -l < pop.txt"; }
  doc 'widgets: 12';                                   arm "REFUSE a pattern whose number is not first" 1 "BAD PATTERN"
  fx_claims() { printf '%s\n' "widgets|([0-9]+) widgets|wc -l < pop.txt"; }
  fx_claims() { printf '%s\n' "widgets|([0-9]+) widgets|cat no-such-file-here"; }
                                                       arm "REFUSE an enumerator that produces nothing" 1 "NO ENUMERATOR"

  rm -rf "$t"
  printf 'DERIVED-COUNTS --self-test: %d pass / %d fail\n' "$pass" "$fail"
  [ "$fail" -eq 0 ]
}

if [ "${1:-}" = "--list" ]; then
  printf '%-22s %-34s %s\n' CLAIM ENUMERATOR VALUE
  while IFS='|' read -r label pat enum; do
    [ -n "$label" ] || continue
    printf '%-22s %-34s %s\n' "$label" "$enum" "$(eval "$enum" 2>/dev/null | tr -d '[:space:]')"
  done < <(count_claims)
  exit 0
fi

[ "${1:-}" = "--self-test" ] && { self_test; exit $?; }

[ -f doctrine/readme_routes.tsv ] || { echo "DERIVED-COUNTS: ok (no routes registry yet)"; exit 0; }
self_test >/dev/null 2>&1 || {
  echo "DERIVED-COUNTS: REFUSED — the check does not discriminate (self-test failed)." >&2; exit 2; }

out="$(check_counts . count_claims live_docs)"; rc=$?
count="$(printf '%s' "$out" | sed -n 's/^__CHECKED__ //p')"
body="$(printf '%s' "$out" | grep -v '^__CHECKED__ ' || true)"
if [ "$rc" -ne 0 ]; then
  { echo "DERIVED-COUNTS: a live document states a count the repository contradicts."
    printf '%s\n' "$body" | sed 's/^/  /'
    echo "  RE-DERIVE it with the command shown — never increment a running total, which is"
    echo "  how both of this doctrine's founding defects were introduced."; } >&2
  exit 1
fi
printf 'DERIVED-COUNTS: ok (%s derived count claim(s) re-derived)\n' "${count:-0}"
exit 0
