#!/usr/bin/env bash
# ARTIFACT-COHORT: bounded planning/checking in owned fixtures; never real cleanup.
set -uo pipefail
ROOT="$(git rev-parse --show-toplevel)" || exit 2
cd "$ROOT" || exit 2

self_test() {
  local pass=0 fail=0 out rc mode mutation
  score() {
    if [ "$#" -ne 5 ]; then
      echo 'ARTIFACT-COHORT self-test HARNESS: score needs case, rc, expected rc, output and reason' >&2
      fail=$((fail+1)); return
    fi
    if [ "$2" -eq "$3" ] && printf '%s' "$4" | grep -qF -- "$5"; then
      pass=$((pass+1))
    else
      fail=$((fail+1))
      printf 'ARTIFACT-COHORT self-test MISS: %s expected rc=%s reason=%s got rc=%s\n%s\n' \
        "$1" "$3" "$5" "$2" "$4" >&2
    fi
  }
  for mode in normal optimized; do
    local python=(python3 -B)
    [ "$mode" = normal ] || python+=(-O)
    out="$("${python[@]}" scripts/probe_artifact_cleanup.py 2>&1)"; rc=$?
    score "GREEN $mode cohort controls" "$rc" 0 "$out" '26 tests / 0 failures / 0 errors'
    for mutation in release-strays tracked-ownership hash-budget root-binding plan-shape \
                    exclusive-output head-inventory directory-recheck volume-before-open git-volume-before-read; do
      out="$("${python[@]}" scripts/probe_artifact_cleanup.py --mutation "$mutation" 2>&1)"; rc=$?
      score "RED $mode $mutation" "$rc" 1 "$out" '1 tests / 1 failures / 0 errors'
    done
    out="$("${python[@]}" scripts/probe_legacy_artifact_cleanup.py 2>&1)"; rc=$?
    score "GREEN $mode historical helper" "$rc" 0 "$out" '5 tests / 0 failures / 0 errors'
    out="$("${python[@]}" scripts/probe_legacy_artifact_cleanup.py --mutation source-pin 2>&1)"; rc=$?
    score "RED $mode historical source pin" "$rc" 1 "$out" '1 tests / 1 failures / 0 errors'
  done
  printf 'ARTIFACT-COHORT --self-test: %d pass / %d fail\n' "$pass" "$fail"
  [ "$fail" -eq 0 ]
}

[ "${1:-}" = --self-test ] && [ "$#" -eq 1 ] && { self_test; exit $?; }
[ "$#" -eq 0 ] || { echo 'ARTIFACT-COHORT: unknown arguments' >&2; exit 2; }
self_test || { echo 'ARTIFACT-COHORT: REFUSED — self-test stopped discriminating' >&2; exit 2; }
git ls-files --error-unmatch -- scripts/artifact_cleanup.py scripts/probe_artifact_cleanup.py \
  scripts/probe_legacy_artifact_cleanup.py scripts/fixtures/artifact_cleanup_0067.py.txt >/dev/null 2>&1 || {
  echo 'ARTIFACT-COHORT: REFUSED — instrument and controls must be tracked' >&2; exit 2; }
echo 'ARTIFACT-COHORT: bounded planning/checking controls green; no real cleanup'
