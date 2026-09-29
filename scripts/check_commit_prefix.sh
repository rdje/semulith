#!/usr/bin/env bash
# scripts/check_commit_prefix.sh — COMMIT-PREFIX (project doctrine, PREFIX-DISCIPLINE.1).
#
# The director ruled 2026-09-30: the work-unit prefix is SEMULITH, never SEMILITH. 123 commits
# at ruling time carry both spellings and history is immutable, so the doctrine's object is the
# BOUNDARY where new subjects enter: `.githooks/commit-msg` must REFUSE a subject whose leading
# work-unit id does not begin with `SEMULITH-`, and must ACCEPT one that does.
#
# The hook is a NEUTRAL scaffold file — `scripts/update_scaffold.sh` syncs it from the spine,
# and carrying the pin upstream is unavailable by policy (other repositories are read-only).
# A sync therefore reverts the pin silently. That is the measured exposure the spine-defect
# repairs already carry (`check_task_acceptance.sh`, watched by SEAM-INTEGRITY), and the answer
# has the same shape: the local pin plus this probe, which makes a silent revert loud at the
# very next commit.
#
# The probe is BEHAVIOURAL, never textual — it runs the hook on synthetic messages and judges
# what the hook DOES:
#
#   1. REFUSES      a SEMILITH- subject is refused (rc != 0)               [the pin is alive]
#   2. RIGHT REASON the refusal names SEMULITH                              [not red for nothing]
#   3. ACCEPTS      a SEMULITH- subject passes (rc == 0)                    [not over-tight]
#
# CONTRACT: exit code is the verdict; explains on stderr; deterministic; the repository is
#   read-only to it (synthetic messages live under target/doctrine_scratch/ and are removed);
#   no network.
#   --self-test   run the RED/GREEN controls against synthetic hook fixtures and exit.
set -uo pipefail
ROOT="$(git rev-parse --show-toplevel)"; cd "$ROOT"
HOOK=".githooks/commit-msg"
PINNED="SEMULITH-"
MISSPELLED="SEMILITH-"

# probe HOOKFILE — run HOOKFILE against a misspelled and a pinned synthetic subject.
# Echoes one finding per line, then __CHECKED__ 2; rc 1 if any finding, else 0.
probe() {
  local hook="$1" d out_bad rc_bad out_good rc_good findings=0
  d="$(mkdir -p "$ROOT/target/doctrine_scratch" && mktemp -d "$ROOT/target/doctrine_scratch/commit-prefix.XXXXXX")"
  printf '%s\n' "${MISSPELLED}PX-0001 (leaf PREFIX-DISCIPLINE.1): a misspelled prefix" > "$d/msg-bad"
  printf '%s\n' "${PINNED}PX-0001 (leaf PREFIX-DISCIPLINE.1): the pinned prefix"          > "$d/msg-good"
  out_bad="$(bash "$hook" "$d/msg-bad" 2>&1)";  rc_bad=$?
  out_good="$(bash "$hook" "$d/msg-good" 2>&1)"; rc_good=$?
  rm -rf "$d"
  if [ "$rc_bad" -eq 0 ]; then
    echo "NOT REFUSED: a ${MISSPELLED} subject passed ${hook} — the pin is absent or dead"
    findings=$((findings+1))
  elif ! printf '%s' "$out_bad" | grep -qF "SEMULITH"; then
    echo "WRONG REASON: the ${MISSPELLED} subject was refused but the refusal does not name SEMULITH — red for nothing is not the pin"
    findings=$((findings+1))
  fi
  if [ "$rc_good" -ne 0 ]; then
    echo "OVER-TIGHT: a ${PINNED} subject is refused by ${hook} — the pin rejects the spelling it exists to protect"
    findings=$((findings+1))
  fi
  echo "__CHECKED__ 2"
  [ "$findings" -eq 0 ]
}

self_test() {
  local t pass=0 fail=0 out rc
  t="$(mkdir -p "$ROOT/target/doctrine-selftest" && mktemp -d "$ROOT/target/doctrine-selftest/commit-prefix.XXXXXX")"

  argc() {
    [ "$2" -eq "$1" ] && return 0
    fail=$((fail+1))
    printf 'COMMIT-PREFIX self-test HARNESS: %s() got %s argument(s), expected %s — a missing `;` before `arm` swallows it\n' "$3" "$2" "$1" >&2
    return 1
  }
  arm() {
    argc 3 "$#" arm || return
    out="$(probe "$FIXTURE" 2>&1)"; rc=$?
    if [ "$rc" != "$2" ]; then
      fail=$((fail+1)); printf 'COMMIT-PREFIX self-test MISS: %s expected rc=%s got rc=%s\n%s\n' "$1" "$2" "$rc" "$out" >&2
    elif ! printf '%s' "$out" | grep -qF "$3"; then
      fail=$((fail+1)); printf 'COMMIT-PREFIX self-test MISS: %s right verdict, wrong reason (no %s)\n%s\n' "$1" "$3" "$out" >&2
    else pass=$((pass+1)); fi
  }

  # fixture: the pre-pin hook — identifier-shape check only, no prefix pin (the real hook's
  # shape before this doctrine's pin; a scaffold sync restores exactly this)
  FIXTURE="$t/hook-unpinned"
  cat > "$FIXTURE" <<'EOF'
#!/usr/bin/env bash
subject="$(head -1 "$1")"
if ! printf '%s' "$subject" | grep -Eq '^[A-Za-z][A-Za-z0-9._-]+'; then
  echo "commit-msg: subject must begin with an identifier-shaped work-unit id" >&2
  exit 1
fi
exit 0
EOF
  arm "RED   an unpinned hook (the scaffold-sync revert)" 1 "NOT REFUSED"

  # fixture: an always-refusing hook — red, but for no reason; refuses the pinned spelling too
  FIXTURE="$t/hook-refuse-all"
  printf '#!/usr/bin/env bash\necho "commit-msg: no" >&2\nexit 1\n' > "$FIXTURE"
  arm "RED   an always-refusing hook (red without the reason)" 1 "WRONG REASON"

  # fixture: an over-tight hook — refuses everything, naming SEMULITH (right reason, wrong reach)
  FIXTURE="$t/hook-over-tight"
  printf '#!/usr/bin/env bash\necho "commit-msg: the work-unit id must begin with SEMULITH-" >&2\nexit 1\n' > "$FIXTURE"
  arm "RED   an over-tight hook (refuses SEMULITH- too)" 1 "OVER-TIGHT"

  # fixture: a correctly pinned minimal hook — the check is coupled to BEHAVIOUR, not text
  FIXTURE="$t/hook-pinned"
  cat > "$FIXTURE" <<'EOF'
#!/usr/bin/env bash
subject="$(head -1 "$1")"
if ! printf '%s' "$subject" | grep -Eq '^SEMULITH-'; then
  echo "commit-msg: the work-unit id must begin with the pinned project prefix 'SEMULITH-'" >&2
  exit 1
fi
exit 0
EOF
  arm "GREEN a correctly pinned hook" 0 "__CHECKED__ 2"

  rm -rf "$t"
  printf 'COMMIT-PREFIX --self-test: %d pass / %d fail\n' "$pass" "$fail"
  [ "$fail" -eq 0 ]
}

[ "${1:-}" = "--self-test" ] && { self_test; exit $?; }

self_test >/dev/null 2>&1 || {
  echo "COMMIT-PREFIX: REFUSED — the check does not discriminate (self-test failed)." >&2; exit 2; }

[ -f "$HOOK" ] || {
  echo "COMMIT-PREFIX: REFUSED — $HOOK does not exist; the boundary this doctrine watches is gone." >&2
  exit 2; }

out="$(probe "$HOOK")"; rc=$?
body="$(printf '%s' "$out" | grep -v '^__CHECKED__ ' || true)"
if [ "$rc" -ne 0 ]; then
  { echo "COMMIT-PREFIX: the commit-msg hook does not pin the SEMULITH- work-unit prefix."
    printf '%s\n' "$body" | sed 's/^/  /'
    echo "  The prefix is SEMULITH, never SEMILITH (director ruling 2026-09-30,"
    echo "  decision_work-unit-prefix-semulith). If a scaffold sync reverted the neutral hook,"
    echo "  restore the pin — the ruling stands."; } >&2
  exit 1
fi
printf 'COMMIT-PREFIX: ok (the hook refuses SEMILITH- naming SEMULITH, accepts SEMULITH-)\n'
exit 0
