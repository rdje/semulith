#!/usr/bin/env bash
# scripts/approved_push.sh — THE ACT of an exceptional push (PUSH-DISCIPLINE.3).
#
# An exceptional push (below the 300-commit cadence) requires the director's approval, and the
# approval leaves a durable, tracked, append-only trace — written by THIS act, never afterwards
# from memory. Usage:
#
#   scripts/approved_push.sh '<the director's reason, verbatim>' [git-push args…]
#
# The order is the honesty:
#   1. the reason is non-empty (an empty approval is not an approval — the .1 rule);
#   2. the named full local suite (`make ci`) is GREEN — a red suite refuses and NOTHING is
#      written (a record of a push that never happened would be a lie in the ledger);
#   3. the entry is appended to `docs/push-approvals.md` and COMMITTED as its own commit
#      (`SEMULITH-PUSH-NNNN: push approved — <reason>`) — the only way the record travels in
#      the pushed history;
#   4. `git push` runs with SEMULITH_PUSH_APPROVED set, so the pre-push boundary re-verifies
#      everything: the cadence/approval, the suite (again — the re-run is the tamper guard),
#      and that the ledger's latest entry covers HEAD with the same reason.
#
# ⛔ An agent may not invoke this on its own judgement. The reason is the director's; the
# script only carries it. (The commit-msg/pre-commit hooks run on the record commit like any
# other; the append is what the PUSH-RECORD doctrine allows.)
#
#   --self-test   drive the WHOLE act in a scratch repo against a LOCAL bare upstream (a real
#                 push to a path under target/, never the real remote) and exit.
set -euo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LEDGER="docs/push-approvals.md"

die() { echo "approved-push: REFUSED — $1" >&2; exit "${2:-1}"; }

self_test() {
  local pass=0 fail=0 tmp; tmp="$(mktemp -d)"

  arm() { # arm <label> <expected-rc> <needle> — runs $BODY
    local label="$1" want="$2" needle="$3" out rc
    set +e; out="$(eval "$BODY" 2>&1)"; rc=$?; set -e
    if [ "$rc" != "$want" ]; then
      echo "  FAIL  $label: exit $rc, expected $want — ${out:0:160}"; fail=$((fail+1)); return
    fi
    if [ -n "$needle" ] && ! printf '%s' "$out" | grep -qF -- "$needle"; then
      echo "  FAIL  $label: exit matched but the reason did not — wanted '$needle', got: ${out:0:160}"
      fail=$((fail+1)); return
    fi
    echo "  ok    $label"; pass=$((pass+1))
  }

  # A scratch repo with a local bare upstream, the stub suite, the ledger, and the boundary.
  git init -q --bare "$tmp/up.git"
  git -C "$tmp" clone -q "$tmp/up.git" work
  git -C "$tmp/work" config user.email t@t; git -C "$tmp/work" config user.name t
  mkdir -p "$tmp/work/docs"
  cp "$HERE/../../$LEDGER" "$tmp/work/$LEDGER" 2>/dev/null || cp "$(git rev-parse --show-toplevel)/$LEDGER" "$tmp/work/$LEDGER"
  printf 'ci:\n\t@echo stub-ci green\n' > "$tmp/work/Makefile"
  git -C "$tmp/work" add -A; git -C "$tmp/work" commit -q -m "base"
  git -C "$tmp/work" push -q --no-verify -u origin HEAD:refs/heads/main >/dev/null 2>&1 || \
    git -C "$tmp/work" push -q --no-verify -u origin HEAD:refs/heads/master >/dev/null 2>&1
  git -C "$tmp/work" commit -q --allow-empty -m "one below-cadence commit"
  # the boundary, for real: a pre-push shim exec'ing the REAL pre_push.sh (only pre-push —
  # the scratch's record commits must not run the real pre-commit enforcer over a stub tree)
  mkdir -p "$tmp/hooks"
  printf '#!/usr/bin/env bash\nexec bash "%s/pre_push.sh"\n' "$HERE" > "$tmp/hooks/pre-push"
  chmod +x "$tmp/hooks/pre-push"
  git -C "$tmp/work" config core.hooksPath "$tmp/hooks"
  local AP="$HERE/approved_push.sh"

  BODY="cd '$tmp/work' && bash '$AP' ''"
  arm "RED   an EMPTY approval is not an approval" 1 "an empty approval is not an approval"

  BODY="cd '$tmp/work' && printf 'ci:\n\t@false # the deliberately broken check\n' > Makefile && bash '$AP' 'the reason'"
  arm "RED   a red suite refuses and writes NOTHING" 1 "the full local suite is red"
  if [ -f "$tmp/work/$LEDGER" ] && grep -q "^## SEMULITH-PUSH-" "$tmp/work/$LEDGER"; then
    echo "  FAIL  a red suite left a ledger entry"; fail=$((fail+1))
  else
    echo "  ok    RED   a red suite left no ledger entry"; pass=$((pass+1))
  fi
  [ "$(git -C "$tmp/work" rev-list --count @{u}..HEAD)" = "1" ] && {
    echo "  ok    RED   and made no commit"; pass=$((pass+1)); } || {
    echo "  FAIL  a red suite committed something"; fail=$((fail+1)); }

  BODY="cd '$tmp/work' && printf 'ci:\n\t@echo stub-ci green\n' > Makefile && bash '$AP' 'ship the reviewed slice'"
  arm "GREEN the full act: suite green, record committed, push proceeds" 0 "approved-push: pushed"
  local last_entry work_sha
  last_entry="$(sed -n '/^## SEMULITH-PUSH/,$p' "$tmp/work/$LEDGER")"
  work_sha="$(git -C "$tmp/work" rev-parse HEAD~1)"   # the entry names the WORK head; the record commit rides on top
  if printf '%s' "$last_entry" | grep -qF "ship the reviewed slice" \
     && printf '%s' "$last_entry" | grep -qF "$work_sha"; then
    echo "  ok    GREEN the entry names the reason and the work head"; pass=$((pass+1))
  else
    echo "  FAIL  the entry is missing the reason or the work head"; fail=$((fail+1))
  fi
  if git -C "$tmp/up.git" log --format='%s' -1 main 2>/dev/null | grep -qF "push approved — ship the reviewed slice" \
     || git -C "$tmp/up.git" log --format='%s' -1 master 2>/dev/null | grep -qF "push approved — ship the reviewed slice"; then
    echo "  ok    GREEN the record commit is IN the pushed history"; pass=$((pass+1))
  else
    echo "  FAIL  the upstream does not carry the record commit"; fail=$((fail+1))
  fi

  rm -rf "$tmp"
  echo "APPROVED-PUSH self-test: $pass pass / $fail fail"
  [ "$fail" -eq 0 ]
}

[ "${1:-}" = "--self-test" ] && { self_test; exit $?; }

# ---- the act -----------------------------------------------------------------------------

reason="${1:-}"; shift || true
[ -n "$reason" ] || die "an empty approval is not an approval. Usage:
  scripts/approved_push.sh '<the director’s reason, verbatim>' [git-push args…]
⛔ The reason is the director's; this script only carries it. An agent may not
invoke this on its own judgement."

ROOT="$(git rev-parse --show-toplevel)"; cd "$ROOT"
[ -f "$LEDGER" ] || die "$LEDGER is absent — the ledger this act appends to is gone." 2

# 1. the suite, green FIRST — nothing is written over a red tree.
echo "approved-push: running the full local suite first: make ci (check + gate + bench + smoke-bench + book)"
if ! make ci; then
  die "the full local suite is red — nothing was written, no record committed, no push attempted. Fix it and re-run."
fi

# 2. the entry, appended and committed as its own commit.
seq="$(grep -c '^## SEMULITH-PUSH-' "$LEDGER" || true)"
next="$(printf 'SEMULITH-PUSH-%04d' "$((seq + 1))")"
head_sha="$(git rev-parse HEAD)"
upstream="$(git rev-parse --abbrev-ref '@{u}' 2>/dev/null || true)"
[ -n "$upstream" ] || die "no upstream tracking branch — the range this push covers cannot be derived." 2
ahead="$(git rev-list --count "${upstream}..HEAD")"
when="$(date '+%Y-%m-%dT%H:%M:%S%z')"
cat >> "$LEDGER" <<EOF

## $next — $when

- **Approved by:** the director
- **Reason:** $reason
- **Range:** $upstream..$head_sha — $ahead commit(s) since the last push, plus this record commit
- **Suite:** \`make ci\` green at $head_sha before this record was written
EOF
git add "$LEDGER"
git commit -q -F - <<EOF
$next: push approved — $reason

The record of an exceptional push, written by the same act that permits it
(scripts/approved_push.sh, PUSH-DISCIPLINE.3). The suite was green at the recorded
HEAD before the record was written; the range is derived from git.
EOF

# 3. the push — the boundary re-verifies cadence, the suite, and the record.
SEMULITH_PUSH_APPROVED="$reason" git push "$@"
echo "approved-push: pushed; the record is $LEDGER ($next), committed and carried in the pushed history."
