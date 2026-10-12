#!/usr/bin/env bash
# scripts/check_memory_architecture.sh — MEMORY-ARCH invariants (MEMORY_ARCHITECTURE.md).
#
# Structural, harness-agnostic checks that the durable-memory layers exist and hold
# their shape. Cheap, deterministic, no network.
set -uo pipefail
refuse(){ printf 'MEMORY-ARCH: REFUSED — %s\n' "$1" >&2; exit 2; }
ROOT="$(git rev-parse --show-toplevel)" || refuse 'repository root unavailable'
cd "$ROOT" || refuse 'repository root unavailable'
errs=0
fail(){ echo "MEMORY-ARCH: $1" >&2; errs=$((errs+1)); }

# Layer A — the bounded resume pointer must exist and stay bounded by BOTH caps.
#
# ⛔ A LINE CAP ALONE DOES NOT BOUND THIS FILE, and the failure is measured, not hypothetical.
# On a real project running this spine, MEMORY.md sat at 60 lines — PASSING, exactly at its
# line cap — while carrying 138,403 BYTES: 2,306 bytes per line, with one line of 18,816
# bytes. A file this standard calls a "bounded resume pointer" was a 138 KB document and this
# check was green the whole time. The block headed "Current state (OVERWRITE this block each
# update — do not append)" had accumulated 18 sessions and 81.3% of the file.
#   ⇒ Line and byte caps are COMPLEMENTS: neither wrapped prose nor very long lines can bypass
#     the budget. See README_POLICY.md, which states the same rule for README.md.
#
# The line cap is deliberately TIGHTENED from an earlier 120: MEMORY_ARCHITECTURE.md §6 and
# the pointer template both say "≤ ~50 lines", so 120 was more than twice as loose as the rule
# it policed. 7168 bytes ≈ 143 B/line at 50 lines — the shape of a real pointer file — so the
# two caps bind on the same kind of document rather than one shadowing the other.
# ⛔ Never raise a cap to fit the content: demote it to docs/tasks/ (B) or docs/decisions/ (C).
CAP="${MEMORY_POINTER_LINE_CAP:-50}"
BYTE_CAP="${MEMORY_POINTER_BYTE_CAP:-7168}"
[ -f MEMORY.md ] || fail "MEMORY.md (layer-A resume pointer) is missing"
if [ -f MEMORY.md ]; then
  lines=$(wc -l < MEMORY.md | tr -d ' ')
  bytes=$(wc -c < MEMORY.md | tr -d ' ')
  [ "$lines" -le "$CAP" ] || fail "MEMORY.md has $lines lines (> cap $CAP) — it is a bounded pointer, not a log; demote content to docs/tasks/ (B) or docs/decisions/ (C)"
  [ "$bytes" -le "$BYTE_CAP" ] || fail "MEMORY.md is $bytes bytes (> cap $BYTE_CAP) — long lines bypass the line cap; demote content, do NOT raise the cap"
fi

# Layer C — decision records live one-per-file under docs/decisions/ with an INDEX.
[ -d docs/decisions ] || fail "docs/decisions/ (layer-C decision records) is missing"
[ -f docs/decisions/INDEX.md ] || fail "docs/decisions/INDEX.md is missing"
# Every decision record (excluding INDEX/TEMPLATE) must be listed in the index.
if [ -d docs/decisions ] && [ -f docs/decisions/INDEX.md ]; then
  mkdir -p "$ROOT/target/tmp" || refuse 'scratch directory unavailable'
  tmp="$(mktemp -d "$ROOT/target/tmp/memory-index.XXXXXX")" || refuse 'scratch allocation failed'
  trap 'rm -rf -- "$tmp"' EXIT
  index="$tmp/index"
  # Ignore comments and fenced examples: only an actual table link lists a record.
  python3 - docs/decisions/INDEX.md "$index" <<'INDEX_READER' || refuse 'decision index read failed'
from pathlib import Path
import re
import sys

try:
    text = Path(sys.argv[1]).read_text(encoding='utf-8')
    output, fence, comment = [], None, False
    for line in text.splitlines(keepends=True):
        marker = re.match(r' {0,3}(`{3,}|~{3,})(.*)$', line)
        if fence is not None:
            if marker and marker[1][0] == fence[0] and len(marker[1]) >= len(fence) and not marker[2].strip():
                fence = None
            continue
        if not comment and marker:
            fence = marker[1]
            continue
        while line:
            if comment:
                end = line.find('-->')
                if end < 0:
                    break
                line, comment = line[end + 3:], False
            else:
                start = line.find('<!--')
                if start < 0:
                    output.append(line)
                    break
                output.append(line[:start])
                line, comment = line[start + 4:], True
    Path(sys.argv[2]).write_text(''.join(output), encoding='utf-8')
except (OSError, UnicodeError) as exc:
    print('MEMORY-ARCH: REFUSED — decision index normalization: ' + str(exc), file=sys.stderr)
    raise SystemExit(2)
INDEX_READER
  shopt -s nullglob
  for f in docs/decisions/*.md; do
    b="${f##*/}"
    case "$b" in INDEX.md|TEMPLATE.md) continue;; esac
    # Filenames are literal data, never regular expressions.
    escaped="$b"
    for special in '\' '.' '[' ']' '*' '^' '$' '+' '?' '(' ')' '{' '}' '|'; do
      escaped="${escaped//"$special"/\\$special}"
    done
    pattern="^\| \[[^]]+\]\($escaped\) \|"
    grep -Eq -- "$pattern" "$index"
    rc=$?
    case "$rc" in
      0) ;;
      1) fail "decision record $b is not listed in docs/decisions/INDEX.md";;
      *) refuse "decision index match unavailable: $b";;
    esac
  done
fi

# Layer B — the task-tree system exists.
[ -f docs/TASK_TREE.md ] || fail "docs/TASK_TREE.md (task-tree index) is missing"
[ -d docs/tasks ] || fail "docs/tasks/ (task-tree leaves) is missing"

# Tool-neutral bootstrap entrypoints exist.
[ -f README.md ] || fail "README.md (tool-neutral entrypoint) is missing"
[ -f CLAUDE.md ] || fail "CLAUDE.md (agent bootstrap) is missing"

[ "$errs" -eq 0 ] || exit 1
exit 0
