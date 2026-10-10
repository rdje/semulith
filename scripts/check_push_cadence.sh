#!/usr/bin/env bash
# scripts/check_push_cadence.sh — PUSH-CADENCE. Is this push on cadence, or does it need approval?
#
# ⛔ WHY A PUSH IS NOT A COMMIT. A commit is local and reversible: reword it, drop it, rebase it,
# and nothing outside this disk ever knew. A push sends bytes to a server that may keep, cache,
# mirror or index them regardless of what happens here afterwards. The two acts differ in kind, so
# they are governed differently — and until this file existed, they were governed identically,
# which is to say not at all (`grep -i push COMMIT.md` returned nothing, and no pre-push hook
# existed).
#
# Director instruction, 2026-09-14: cadence is every 300 commits. An exceptional push happens from
# time to time and REQUIRES THE DIRECTOR'S APPROVAL.
#
# ⛔ THE GATE REFUSES, IT DOES NOT WARN. A warning printed at an outward-facing boundary is a
# warning read after the bytes have left. And it refuses an AGENT most of all: the one judgement
# this tool exists to prevent is a capable assistant deciding, reasonably and on its own, that this
# particular push is surely fine.
#
# ⛔ THE NUMBER LIVES HERE AND NOWHERE ELSE. Any document restating it is checked against this file
# by the self-test below, on the same no-duplicated-fact rule the canonical definition uses.
set -euo pipefail

CADENCE=300
APPROVAL_VAR="SEMULITH_PUSH_APPROVED"

usage() {
  cat >&2 <<'USAGE'
usage: check_push_cadence.sh [--status | --print-cadence | --gate | --self-test]
  --status         report the distance from upstream and the verdict (default)
  --print-cadence  the cadence number, for a document that must agree with it
  --gate           exit 0 if this push is permitted, 1 if it must be refused
  --self-test      fire the arms
USAGE
  exit 2
}

# The distance, or a refusal. ⛔ Never a number this script cannot actually know: "0 commits ahead"
# printed for a detached HEAD or a missing upstream is a lie that permits a push.
distance() {
  local up
  if ! git rev-parse --git-dir >/dev/null 2>&1; then
    echo "NOT-A-REPO"; return
  fi
  if ! git symbolic-ref -q HEAD >/dev/null 2>&1; then
    echo "DETACHED"; return
  fi
  if ! up="$(git rev-parse --abbrev-ref --symbolic-full-name '@{upstream}' 2>/dev/null)"; then
    echo "NO-UPSTREAM"; return
  fi
  git rev-list --count "${up}..HEAD" 2>/dev/null || echo "UNKNOWN"
}

approval() { printf '%s' "${!APPROVAL_VAR-}"; }

verdict() {
  local n; n="$(distance)"
  local why; why="$(approval)"
  case "$n" in
    NOT-A-REPO|DETACHED|NO-UPSTREAM|UNKNOWN)
      echo "REFUSE|$n|the distance from upstream cannot be determined ($n), so the cadence cannot be judged. A gate that cannot measure must refuse; a number it guesses would permit a push."
      return ;;
  esac
  if [ -n "$why" ]; then
    echo "APPROVED|$n|exceptional push approved by the director: $why"
  elif [ "$n" -ge "$CADENCE" ]; then
    echo "ON-CADENCE|$n|$n commits since the last push, cadence is $CADENCE"
  else
    echo "REFUSE|$n|$n commits since the last push; the cadence is $CADENCE, so this push is EXCEPTIONAL and needs the director's approval."
  fi
}

main() {
  case "${1---status}" in
    --print-cadence) echo "$CADENCE" ;;
    --self-test) selftest ;;
    --status|--gate)
      local v state n msg
      v="$(verdict)"; state="${v%%|*}"; v="${v#*|}"; n="${v%%|*}"; msg="${v#*|}"
      case "$state" in
        ON-CADENCE) echo "PUSH-CADENCE: ok — $msg" ;;
        APPROVED)   echo "PUSH-CADENCE: ok — $msg" ;;
        *)
          {
            echo "PUSH-CADENCE: REFUSED — $msg"
            echo
            echo "  Two ways forward, and only two:"
            echo "    1. Wait. The cadence is $CADENCE commits; this is $n."
            echo "    2. Ask the director. Only after explicit approval, run the recorded act:"
            echo "          scripts/approved_push.sh '<the director's reason>'"
            echo "       It runs full local CI, commits the approval record, then pushes."
            echo "       $APPROVAL_VAR alone no longer suffices; pre-push requires that record."
            echo
            echo "  ⛔ An agent may not supply this on its own judgement. The exception is the"
            echo "     director's to grant; the variable only carries it."
          } >&2
          [ "${1---status}" = "--gate" ] && return 1 || return 1 ;;
      esac ;;
    *) usage ;;
  esac
}

# ---------------------------------------------------------------------------------------
# Self-test. Every arm runs in a THROWAWAY repository with a real upstream, because a gate about
# distance-from-upstream cannot be tested without one.
# ---------------------------------------------------------------------------------------
selftest() {
  local owner_root
  owner_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
  local test_temp_root="$owner_root/target/push-selftest"
  mkdir -p "$test_temp_root"
  export TMPDIR="$test_temp_root" # Nested git/toolchain scratch stays on this volume too.
  local pass=0 fail=0 tmp; tmp="$(mktemp -d "$test_temp_root/cadence.XXXXXX")"
  case "$tmp" in
    "$owner_root/target/push-selftest/"*)
      echo "  ok    GREEN scratch stays below the owning repository"; pass=$((pass+1)) ;;
    *) echo "  FAIL  scratch escaped the owning repository's test directory"; fail=$((fail+1)) ;;
  esac

  arm() { # arm <label> <expected-rc> <needle> -- runs $BODY in $tmp/work
    local label="$1" want="$2" needle="$3" out rc
    set +e; out="$(cd "$tmp/work" && eval "$BODY" 2>&1)"; rc=$?; set -e
    if [ "$rc" != "$want" ]; then
      echo "  FAIL  $label: exit $rc, expected $want"; fail=$((fail+1)); return
    fi
    if [ -n "$needle" ] && ! printf '%s' "$out" | grep -qF -- "$needle"; then
      echo "  FAIL  $label: exit matched but the reason did not — wanted '$needle', got: ${out:0:120}"
      fail=$((fail+1)); return
    fi
    echo "  ok    $label"; pass=$((pass+1))
  }

  # a bare upstream and a clone tracking it
  git init -q --bare "$tmp/up.git"
  git -C "$tmp" clone -q "$tmp/up.git" work
  git -C "$tmp/work" config user.email t@t; git -C "$tmp/work" config user.name t
  git -C "$tmp/work" commit -q --allow-empty -m base
  git -C "$tmp/work" push -q --no-verify -u origin HEAD:refs/heads/main >/dev/null 2>&1 || \
    git -C "$tmp/work" push -q --no-verify -u origin HEAD:refs/heads/master >/dev/null 2>&1
  local SC; SC="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/check_push_cadence.sh"

  BODY="bash '$SC' --gate"
  arm "GREEN in sync with upstream, 0 ahead, below cadence -> refused" 1 "needs the director's approval"

  git -C "$tmp/work" commit -q --allow-empty -m one
  arm "RED   1 commit ahead is still below cadence" 1 "the cadence is 300"
  arm "RED   the refusal names BOTH ways forward" 1 "Ask the director"
  arm "RED   the refusal names the approval variable" 1 "SEMULITH_PUSH_APPROVED"
  arm "RED   the refusal forbids an agent supplying approval itself" 1 "may not supply this on its own"
  arm "RED   the refusal names the recorded approval act" 1 "scripts/approved_push.sh"
  arm "RED   the refusal explains that the variable alone is insufficient" 1 "alone no longer suffices"
  local refusal rc
  set +e; refusal="$(cd "$tmp/work" && bash "$SC" --gate 2>&1)"; rc=$?; set -e
  if [ "$rc" -eq 1 ] && ! grep -qE 'SEMULITH_PUSH_APPROVED=.*git push' <<<"$refusal"; then
    echo "  ok    GREEN refusal has no obsolete variable-only push command"; pass=$((pass+1))
  else
    echo "  FAIL  refusal retains an obsolete variable-only push command or wrong verdict"; fail=$((fail+1))
  fi

  BODY="SEMULITH_PUSH_APPROVED='shipping the review copy' bash '$SC' --gate"
  arm "GREEN an approved push is permitted" 0 "exceptional push approved"
  arm "GREEN the approval RECORDS the reason given" 0 "shipping the review copy"

  BODY="SEMULITH_PUSH_APPROVED='' bash '$SC' --gate"
  arm "RED   an EMPTY approval is not an approval" 1 "needs the director's approval"

  BODY="git checkout -q --detach && bash '$SC' --gate"
  arm "RED   a detached HEAD refuses rather than reporting a distance" 1 "cannot be judged"

  git -C "$tmp/work" checkout -q - >/dev/null 2>&1 || true
  BODY="git checkout -q -b orphan-nope 2>/dev/null; bash '$SC' --gate"
  arm "RED   a branch with no upstream refuses rather than guessing" 1 "cannot be judged"

  # the number is stated in COMMIT.md and must equal the one above
  local doc repo; repo="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
  doc="$(grep -oE 'every ([0-9]+) commits' "$repo/COMMIT.md" 2>/dev/null | head -1 | grep -oE '[0-9]+' || true)"
  if [ "$doc" = "$CADENCE" ]; then
    echo "  ok    GREEN COMMIT.md states the same cadence ($CADENCE) as this script"; pass=$((pass+1))
  else
    echo "  FAIL  GREEN COMMIT.md states '${doc:-nothing}', this script says $CADENCE"; fail=$((fail+1))
  fi

  rm -rf "$tmp"
  echo "PUSH-CADENCE --self-test: $pass pass / $fail fail"
  [ "$fail" -eq 0 ]
}

main "$@"
