#!/usr/bin/env bash
# scripts/pre_push.sh — the push boundary's full behavior (PUSH-DISCIPLINE.2).
#
# Policy 16: full CI runs BEFORE a push; selected checks for ordinary commits. Until this leaf,
# the full suite ran server-side ON push — a red CI run told you what you already shipped. The
# boundary now runs, in order:
#
#   1. CADENCE — `check_push_cadence.sh --gate`, unchanged, and FIRST: a push the cadence
#      refuses never burns the suite. The cadence number lives in that script alone.
#   2. THE NAMED SUITE — `make ci` (membership named in the Makefile, in this script's
#      output, and in the green record): check + gate + bench + smoke-bench + book. It runs
#      on BOTH paths — a cadence push and a director-approved exceptional push alike; an
#      approved push is not an unverified one.
#   3. THE GREEN-RUN RECORD — `target/push/last-green.txt` (+ `last-green.log`): untracked,
#      on-volume, overwritten per green run. It answers "what did the last green pre-push
#      run cover, and when" without git archaeology. ⛔ It is NOT the tracked append-only
#      approval record — that is PUSH-DISCIPLINE.3's artifact, a different thing.
#
# Refusal NAMES what failed (the suite's failing leg, from make's own error line) and points
# at the log. A green suite is no approval: the cadence/approval question and the suite
# question are different questions, and this script asks both, in that order.
#
#   --self-test   run the RED/GREEN controls in scratch repos (a stub Makefile, a real bare
#                 upstream for the cadence leg) and exit.
set -uo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# The repo being pushed (git runs hooks with cwd at the worktree top-level; the self-test
# points this at a scratch repo).
repo_root() { git rev-parse --show-toplevel 2>/dev/null; }

run_boundary() { # $1 = repo root
  local root="$1" out rc
  # 1. cadence first — the cheap refusal never burns the suite.
  out="$(cd "$root" && bash "$HERE/check_push_cadence.sh" --gate 2>&1)"; rc=$?
  if [ "$rc" -ne 0 ]; then
    printf '%s\n' "$out" >&2
    return "$rc"
  fi
  printf '%s\n' "$out"
  # 2. the named suite, on both paths.
  local record_dir="$root/target/push"
  local log="$record_dir/last-green.log"
  mkdir -p "$record_dir"
  echo "pre-push: running the full local suite: make ci (check + gate + bench + smoke-bench + book)"
  if ! (cd "$root" && make ci) >"$log" 2>&1; then
    local leg
    leg="$(grep -oE '\*\*\* \[[^]]*\]' "$log" | head -1 || true)"
    echo "pre-push: REFUSED — the full local suite is red${leg:+ at leg $leg}." >&2
    echo "  the run's log: ${log#$root/} — fix the failure and re-run \`make ci\` before pushing." >&2
    echo "  ⛔ A push of a red tree is exactly what this boundary exists to refuse." >&2
    return 1
  fi
  # 3. the green-run record: what was verified, and when — without git archaeology.
  local sha when
  sha="$(git -C "$root" rev-parse HEAD)"
  when="$(date '+%Y-%m-%dT%H:%M:%S%z')"
  cat > "$record_dir/last-green.txt" <<EOF
pre-push green record — written by scripts/pre_push.sh (PUSH-DISCIPLINE.2).
Untracked (target/), on-volume, overwritten per green run. NOT the tracked append-only
approval record (that is PUSH-DISCIPLINE.3's artifact, a different thing).

when:    $when
commit:  $sha
suite:   make ci = make check (fmt + clippy -D warnings + cargo test --all)
                  + make gate (every doctrine, incl. the wasm build and all self-tests)
                  + make bench + make smoke-bench (the browser bench)
                  + make book (the project book and every model book)
verdict: all legs green
log:     target/push/last-green.log
EOF
  echo "pre-push: the full local suite is green; the record is target/push/last-green.txt"
  return 0
}

self_test() {
  local pass=0 fail=0 tmp; tmp="$(mktemp -d)"

  arm() { # arm <label> <expected-rc> <needle> — runs $BODY in $tmp/work
    local label="$1" want="$2" needle="$3" out rc
    out="$(cd "$tmp/work" && eval "$BODY" 2>&1)"; rc=$?
    if [ "$rc" != "$want" ]; then
      echo "  FAIL  $label: exit $rc, expected $want — ${out:0:160}"; fail=$((fail+1)); return
    fi
    if [ -n "$needle" ] && ! printf '%s' "$out" | grep -qF -- "$needle"; then
      echo "  FAIL  $label: exit matched but the reason did not — wanted '$needle', got: ${out:0:160}"
      fail=$((fail+1)); return
    fi
    echo "  ok    $label"; pass=$((pass+1))
  }

  # a bare upstream and a clone tracking it (the cadence leg needs a real one — the .1 pattern)
  git init -q --bare "$tmp/up.git"
  git -C "$tmp" clone -q "$tmp/up.git" work
  git -C "$tmp/work" config user.email t@t; git -C "$tmp/work" config user.name t
  git -C "$tmp/work" commit -q --allow-empty -m base
  git -C "$tmp/work" push -q --no-verify -u origin HEAD:refs/heads/main >/dev/null 2>&1 || \
    git -C "$tmp/work" push -q --no-verify -u origin HEAD:refs/heads/master >/dev/null 2>&1
  local PP="$HERE/pre_push.sh"

  # the stub suite: a scratch Makefile whose ci target passes or fails per arm
  suite_ok()   { printf 'ci:\n\t@date +%%s >> ci-marker\n\t@echo stub-ci green\n' > "$tmp/work/Makefile"; }
  suite_fail() { printf 'ci:\n\t@false # the deliberately broken check\n' > "$tmp/work/Makefile"; }

  BODY="bash '$PP'"
  suite_fail
  arm "RED   the cadence refusal comes FIRST — below cadence, no approval" 1 "needs the director's approval"
  if [ -f "$tmp/work/ci-marker" ] || [ -f "$tmp/work/target/push/last-green.txt" ]; then
    echo "  FAIL  the refused push ran the suite or wrote a record"; fail=$((fail+1))
  else
    echo "  ok    RED   the refused push never burns the suite (no marker, no record)"; pass=$((pass+1))
  fi

  BODY="SEMULITH_PUSH_APPROVED='self-test' bash '$PP'"
  arm "RED   approved, but the suite is deliberately broken — the refusal names the leg" 1 "the full local suite is red"
  arm "RED   … and points at the log" 1 "target/push/last-green.log"
  if [ -f "$tmp/work/target/push/last-green.txt" ]; then
    echo "  FAIL  a red suite wrote a green record"; fail=$((fail+1))
  else
    echo "  ok    RED   a red suite writes NO green record"; pass=$((pass+1))
  fi

  suite_ok
  arm "GREEN approved and the suite green — the boundary permits" 0 "the full local suite is green"
  if [ -f "$tmp/work/target/push/last-green.txt" ] \
     && grep -qF "commit:  $(git -C "$tmp/work" rev-parse HEAD)" "$tmp/work/target/push/last-green.txt" \
     && grep -qF "make ci = make check" "$tmp/work/target/push/last-green.txt"; then
    echo "  ok    GREEN the record names the commit and the suite's membership"; pass=$((pass+1))
  else
    echo "  FAIL  the record is missing or does not name the commit/suite"; fail=$((fail+1))
  fi

  # a later red run must NOT overwrite the record of the last green one
  suite_fail
  arm "RED   a red run after a green one is refused" 1 "the full local suite is red"
  if grep -qF "verdict: all legs green" "$tmp/work/target/push/last-green.txt"; then
    echo "  ok    GREEN the red run did NOT overwrite the last green record"; pass=$((pass+1))
  else
    echo "  FAIL  the record was overwritten by a red run"; fail=$((fail+1))
  fi

  rm -rf "$tmp"
  echo "PRE-PUSH self-test: $pass pass / $fail fail"
  [ "$fail" -eq 0 ]
}

if [ "${1:-}" = "--self-test" ]; then
  self_test; exit $?
fi

ROOT="$(repo_root)" || {
  echo "pre-push: REFUSED — not a git repository; the boundary cannot be judged." >&2; exit 2; }
[ -n "$ROOT" ] || {
  echo "pre-push: REFUSED — not a git repository; the boundary cannot be judged." >&2; exit 2; }
run_boundary "$ROOT"
