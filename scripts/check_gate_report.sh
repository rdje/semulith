#!/usr/bin/env bash
# scripts/check_gate_report.sh — GATE-REPORT (project doctrine).
#
# A gate report is the one document in a project that everything else is summarised INTO, which
# makes it the one most worth writing by hand and the one least safe to. `ROADMAP.md` §P1 asks for
# it to be *generated from pinned inputs*; this check enforces that the tracked report still IS
# that function of its inputs, exactly as `KNOWLEDGE-MAP` does for the orientation map.
#
# ⭐ WHAT THIS ACTUALLY PROTECTS. Not tidiness — the VERDICT. A hand-edited gate report is how a
# project comes to hold a `passed` that nothing produced, and `EVD-08` names that outcome
# specifically: never `passed` with a missing required check. The generator has no code path to
# `passed` while declared checks exceed implemented ones; this check is what stops someone
# reaching that word with an editor instead.
#
# ⚠️ HONEST LIMIT: it proves the report is in sync with its inputs. It says nothing about whether
# those inputs are true — the requirements, obligations and experiment records have their own
# gate (`RECORD-SCHEMA`) and their own honest limits.
#
# CONTRACT: exit code is the verdict; explains on stderr; deterministic; read-only; no network.
#   --self-test   run the RED/GREEN controls and exit.
set -uo pipefail
ROOT="$(git rev-parse --show-toplevel)"; cd "$ROOT"

command -v python3 >/dev/null 2>&1 || {
  echo "GATE-REPORT: REFUSED — python3 is not on PATH; this check cannot judge." >&2; exit 2; }

report_for() { python3 scripts/gate_report.py "$1" --stdout 2>/dev/null; }

self_test() {
  local pass=0 fail=0 prof p tmp generated
  # The controls run against the REAL profiles, because the generator reads a profile directory
  # and a synthetic one would be a different function. A profile with no report is skipped by the
  # real run too, so it is not a control.
  for p in profiles/*/; do
    prof="$(basename "$p")"
    [ -f "${p%/}/G0-REPORT.md" ] || continue
    generated="$(report_for "$prof")"
    if [ -z "$generated" ]; then
      fail=$((fail+1)); echo "GATE-REPORT self-test MISS: $prof generated nothing" >&2; continue
    fi
    # GREEN: the generator agrees with itself (determinism).
    if [ "$generated" = "$(report_for "$prof")" ]; then pass=$((pass+1))
    else fail=$((fail+1)); echo "GATE-REPORT self-test MISS: $prof is not deterministic" >&2; fi
    # RED: a single edited character must be detected.
    tmp="$(printf '%s' "$generated" | sed 's/incomplete/passed/')"
    if [ "$tmp" != "$generated" ]; then pass=$((pass+1))
    else fail=$((fail+1)); echo "GATE-REPORT self-test MISS: $prof control did not alter the text" >&2; fi
    # RED: the generated text must actually differ from a tampered file's content.
    if ! printf '%s' "$tmp" | diff -q - <(printf '%s' "$generated") >/dev/null 2>&1; then pass=$((pass+1))
    else fail=$((fail+1)); echo "GATE-REPORT self-test MISS: $prof tamper is undetectable" >&2; fi
  done
  [ "$pass" -gt 0 ] || { echo "GATE-REPORT self-test: no profile carried a report to test" >&2; fail=$((fail+1)); }
  printf 'GATE-REPORT --self-test: %d pass / %d fail\n' "$pass" "$fail"
  [ "$fail" -eq 0 ]
}

[ "${1:-}" = "--self-test" ] && { self_test; exit $?; }

[ -d profiles ] || { echo "GATE-REPORT: ok (no profiles/ yet)"; exit 0; }
self_test >/dev/null 2>&1 || {
  echo "GATE-REPORT: REFUSED — the check does not discriminate (self-test failed)." >&2; exit 2; }

stale=0 checked=0
for p in profiles/*/; do
  prof="$(basename "$p")"
  report="${p%/}/G0-REPORT.md"
  [ -f "$report" ] || continue
  checked=$((checked+1))
  if ! diff -q <(report_for "$prof") "$report" >/dev/null 2>&1; then
    { echo "GATE-REPORT: $report is out of sync with the inputs it is generated from."
      diff <(report_for "$prof") "$report" | head -20 | sed 's/^/    /'
      echo "  Regenerate it — never edit it:"
      echo "    scripts/gate_report.py $prof"
      echo "  ⛔ A hand-edited gate report is how a project comes to hold a verdict nothing produced."
    } >&2
    stale=$((stale+1))
  fi
done

[ "$stale" -eq 0 ] || exit 1
printf 'GATE-REPORT: ok (%s generated report(s) in sync with their inputs)\n' "$checked"
exit 0
