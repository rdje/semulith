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
# Two placements, one rule: PER-PROFILE reports live at `profiles/<id>/G?-REPORT.md`; a
# CROSS-ARCHITECTURE gate's report lives at the repo level (today: `BREADTH` →
# `docs/BREADTH-REPORT.md`, P3-BREADTH.6 slice 3 — the gate spans every registered unit, so no
# profile directory may own it). Both get the same sync enforcement and the same controls.
#
# CONTRACT: exit code is the verdict; explains on stderr; deterministic; read-only; no network.
#   --self-test   run the RED/GREEN controls and exit.
set -uo pipefail
ROOT="$(git rev-parse --show-toplevel)"; cd "$ROOT"

command -v python3 >/dev/null 2>&1 || {
  echo "GATE-REPORT: REFUSED — python3 is not on PATH; this check cannot judge." >&2; exit 2; }

report_for() { python3 scripts/gate_report.py "$1" --gate "$2" --stdout 2>/dev/null; }
report_repo() { python3 scripts/gate_report.py --gate "$1" --stdout 2>/dev/null; }

# The repo-level gate reports: gate<TAB>path, one per line. A cross-architecture gate whose
# report exists is checked here; one that does not exist yet is not (a profile with no report
# is skipped for the same reason).
repo_reports() {
  printf 'BREADTH\tdocs/BREADTH-REPORT.md\n'
}

self_test() {
  local pass=0 fail=0 prof p tmp generated report gate
  # The CONTRACT MEASURE's own controls (P4-SYSTEM.10 slice a): every report's contract axis is
  # this count, so a measure that stopped discriminating would sync perfectly and still lie.
  if python3 scripts/gate_report.py --self-test >/dev/null 2>&1; then pass=$((pass+1))
  else fail=$((fail+1)); echo "GATE-REPORT self-test MISS: the contract measure's controls failed (scripts/gate_report.py --self-test)" >&2; fi
  # The controls run against the REAL profiles, because the generator reads a profile directory
  # and a synthetic one would be a different function. A profile with no report is skipped by the
  # real run too, so it is not a control.
  for p in profiles/*/; do
    prof="$(basename "$p")"
    for report in "${p%/}"/G?-REPORT.md; do
      [ -f "$report" ] || continue
      gate="$(basename "$report" | cut -d- -f1)"
      generated="$(report_for "$prof" "$gate")"
      if [ -z "$generated" ]; then
        fail=$((fail+1)); echo "GATE-REPORT self-test MISS: $prof/$gate generated nothing" >&2; continue
      fi
      # GREEN: the generator agrees with itself (determinism).
      if [ "$generated" = "$(report_for "$prof" "$gate")" ]; then pass=$((pass+1))
      else fail=$((fail+1)); echo "GATE-REPORT self-test MISS: $prof/$gate is not deterministic" >&2; fi
      # RED: a single edited character must be detected. The edit targets the `**Verdict:`
      # marker itself, NOT the word `incomplete` — the first cut of this arm sed'd
      # s/incomplete/passed/, which silently stops discriminating the day a report legitimately
      # reads `passed` (measured 2026-09-30: G1 passed and the arm's "control" altered nothing).
      tmp="$(printf '%s' "$generated" | sed 's/\*\*Verdict:/**Xerdict:/')"
      if [ "$tmp" != "$generated" ]; then pass=$((pass+1))
      else fail=$((fail+1)); echo "GATE-REPORT self-test MISS: $prof/$gate control did not alter the text" >&2; fi
      # RED: the generated text must actually differ from a tampered file's content.
      if ! printf '%s' "$tmp" | diff -q - <(printf '%s' "$generated") >/dev/null 2>&1; then pass=$((pass+1))
      else fail=$((fail+1)); echo "GATE-REPORT self-test MISS: $prof/$gate tamper is undetectable" >&2; fi
    done
  done
  # The repo-level reports (cross-architecture gates): the same three controls.
  local rgate rpath
  while IFS=$'\t' read -r rgate rpath; do
    [ -f "$rpath" ] || continue
    generated="$(report_repo "$rgate")"
    if [ -z "$generated" ]; then
      fail=$((fail+1)); echo "GATE-REPORT self-test MISS: $rpath generated nothing" >&2; continue
    fi
    if [ "$generated" = "$(report_repo "$rgate")" ]; then pass=$((pass+1))
    else fail=$((fail+1)); echo "GATE-REPORT self-test MISS: $rpath is not deterministic" >&2; fi
    tmp="$(printf '%s' "$generated" | sed 's/\*\*Verdict:/**Xerdict:/')"
    if [ "$tmp" != "$generated" ]; then pass=$((pass+1))
    else fail=$((fail+1)); echo "GATE-REPORT self-test MISS: $rpath control did not alter the text" >&2; fi
    if ! printf '%s' "$tmp" | diff -q - <(printf '%s' "$generated") >/dev/null 2>&1; then pass=$((pass+1))
    else fail=$((fail+1)); echo "GATE-REPORT self-test MISS: $rpath tamper is undetectable" >&2; fi
  done < <(repo_reports)
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
  for report in "${p%/}"/G?-REPORT.md; do
    [ -f "$report" ] || continue
    gate="$(basename "$report" | cut -d- -f1)"
    checked=$((checked+1))
    if ! diff -q <(report_for "$prof" "$gate") "$report" >/dev/null 2>&1; then
      { echo "GATE-REPORT: $report is out of sync with the inputs it is generated from."
        diff <(report_for "$prof" "$gate") "$report" | head -20 | sed 's/^/    /'
        echo "  Regenerate it — never edit it:"
        echo "    scripts/gate_report.py $prof --gate $gate"
        echo "  ⛔ A hand-edited gate report is how a project comes to hold a verdict nothing produced."
      } >&2
      stale=$((stale+1))
    fi
  done
done

# The repo-level reports (cross-architecture gates), same rule.
while IFS=$'\t' read -r rgate rpath; do
  [ -f "$rpath" ] || continue
  checked=$((checked+1))
  if ! diff -q <(report_repo "$rgate") "$rpath" >/dev/null 2>&1; then
    { echo "GATE-REPORT: $rpath is out of sync with the inputs it is generated from."
      diff <(report_repo "$rgate") "$rpath" | head -20 | sed 's/^/    /'
      echo "  Regenerate it — never edit it:"
      echo "    scripts/gate_report.py --gate $rgate"
      echo "  ⛔ A hand-edited gate report is how a project comes to hold a verdict nothing produced."
    } >&2
    stale=$((stale+1))
  fi
done < <(repo_reports)

[ "$stale" -eq 0 ] || exit 1
printf 'GATE-REPORT: ok (%s generated report(s) in sync with their inputs)\n' "$checked"
exit 0
