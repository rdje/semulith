#!/usr/bin/env bash
# scripts/probe_ledger_independence.sh — the measurement the commit gate's ledger rests on (XTASK.16).
#
# `scripts/doctrine_skip.sh` lets six checks be answered from their last green run on a commit that stages only
# LEDGER documentation. That is sound only if none of them reads the ledger. This probe measures it: it removes every
# ledger file from the working tree, runs each of those checks, and puts the files back. A check that fails without
# the ledger reads it, and either the ledger or the check has to change.
#
# Usage:
#   bash scripts/probe_ledger_independence.sh              every skipping check (about 20 minutes)
#   bash scripts/probe_ledger_independence.sh --only ID    one check
#   bash scripts/probe_ledger_independence.sh --no-named [--only ID]
#       the control: the documents tracked data names are removed too, as if they were ledger. PROFILE-CONSISTENCY
#       reads three of them, so it must FAIL here; if it passes, this probe no longer discriminates.
#
# It touches only tracked ledger files, refuses unless each of them is unmodified, and restores exactly those from
# the index on every exit. If it is killed outright:  git checkout -- docs CHANGELOG.md MEMORY.md LIVE_STATUS.md KNOWLEDGE_MAP.md DEV_NOTES.md
# Exit 0 every check passed, 1 a check failed, 2 refused.
set -uo pipefail
ROOT="$(git rev-parse --show-toplevel)" || exit 2
cd "$ROOT" || exit 2
mkdir -p "$ROOT/target/tmp" || exit 2
export TMPDIR="$ROOT/target/tmp"
# shellcheck source=scripts/doctrine_skip.sh
. "$ROOT/scripts/doctrine_skip.sh" || exit 2

only=""; with_named=1
while [ $# -gt 0 ]; do
  case "$1" in
    --only) only="${2:?--only needs a check id}"; shift 2;;
    --no-named) with_named=0; shift;;
    *) echo "probe_ledger_independence: unknown argument $1" >&2; exit 2;;
  esac
done

named=""; [ "$with_named" = 1 ] && named="$(doctrine_named_documents)"
work="$(mktemp -d "$ROOT/target/tmp/ledger-independence.XXXXXX")" || exit 2
[ -n "$work" ] && [ -d "$work" ] || exit 2
: > "$work/ledger"
while IFS= read -r path; do
  doctrine_is_ledger "$path" "$named" && printf '%s\n' "$path" >> "$work/ledger"
done < <(git ls-files)
count="$(wc -l < "$work/ledger" | tr -d ' ')"
[ "$count" -gt 0 ] || { echo "probe_ledger_independence: the ledger names no tracked file" >&2; rm -rf "$work"; exit 2; }
if [ -n "$(tr '\n' '\0' < "$work/ledger" | xargs -0 git status --porcelain -- 2>/dev/null)" ]; then
  echo "probe_ledger_independence: REFUSED — a ledger file is modified or staged; commit or restore it first" >&2
  rm -rf "$work"; exit 2
fi

# the skipping checks and their scripts, read from the registry, in its order
checks=()
while IFS='|' read -r id script; do
  doctrine_skips "$id" || continue
  [ -z "$only" ] || [ "$only" = "$id" ] || continue
  checks+=("$id|$script")
done < <(sed -n 's/^  "\([A-Z][A-Z-]*\)|.*|\(scripts\/[A-Za-z0-9_]*\.sh\)"$/\1|\2/p' scripts/check_doctrines.project.sh)
[ "${#checks[@]}" -gt 0 ] || { echo "probe_ledger_independence: no skipping check named ${only:-in the registry}" >&2; rm -rf "$work"; exit 2; }

restore() {
  tr '\n' '\0' < "$work/ledger" | xargs -0 git checkout -q -- 2>/dev/null
  local left; left="$(tr '\n' '\0' < "$work/ledger" | xargs -0 git status --porcelain -- 2>/dev/null | wc -l | tr -d ' ')"
  echo "probe_ledger_independence: restored $count ledger file(s); $left left differing"
  rm -rf "$work"
}
trap restore EXIT
tr '\n' '\0' < "$work/ledger" | xargs -0 rm -f
echo "probe_ledger_independence: $count ledger file(s) absent$([ "$with_named" = 1 ] || echo ' (the named documents among them: the control)'); ${#checks[@]} check(s)"

failed=0
for entry in "${checks[@]}"; do
  id="${entry%%|*}"; script="${entry#*|}"
  start="$(date +%s)"
  "$script" > "$work/out" 2>&1; rc=$?
  verdict="$(grep -v 'child setpgid' "$work/out" | grep -v '^[[:space:]]*$' | tail -1 | cut -c1-150)"
  echo "  $id rc=$rc $(( $(date +%s) - start ))s :: $verdict"
  [ "$rc" -eq 0 ] || failed=$((failed+1))
done
if [ "$failed" -eq 0 ]; then echo "probe_ledger_independence: ok (${#checks[@]} check(s) pass without the ledger)"; exit 0; fi
echo "probe_ledger_independence: $failed check(s) read the ledger"
exit 1
