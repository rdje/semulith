#!/usr/bin/env bash
# TASK-HISTORY: the approved finite capture, original identities and navigation stay frozen.
# Reader never invokes Git; this gate also compares the committed descriptor and runs controls.
set -uo pipefail
ROOT="$(git rev-parse --show-toplevel)" || exit 2
cd "$ROOT" || exit 2

self_test() {
  local pass=0 fail=0 out rc
  arm() {
    if [ "$#" -ne 3 ]; then
      printf 'TASK-HISTORY self-test HARNESS: arm requires case, rc and reason\n' >&2
      fail=$((fail+1)); return
    fi
    out="$(python3 scripts/probe_task_history.py --case "$1" 2>&1)"; rc=$?
    if [ "$rc" -eq "$2" ] && printf '%s' "$out" | grep -qF "$3"; then
      pass=$((pass+1))
    else
      fail=$((fail+1))
      printf 'TASK-HISTORY self-test MISS: %s expected rc=%s reason=%s got rc=%s\n%s\n' \
        "$1" "$2" "$3" "$rc" "$out" >&2
    fi
  }
  arm "green" 0 "all12 Python/tar originals exact; no Git/extraction; navigation/freeze exact"
  arm "missing-descriptor" 1 "descriptor.json"
  arm "unknown-field" 1 "unknown descriptor fields"
  arm "duplicate-key" 1 "duplicate JSON key"
  arm "oversized-descriptor" 1 "archive file exceeds bound"
  arm "string-count" 1 "descriptor count exceeds bound or is not an integer"
  arm "bool-count" 1 "descriptor count exceeds bound or is not an integer"
  arm "unsafe-object" 1 "unsafe archive object path"
  arm "changed-descriptor" 1 "approved descriptor identity differs"
  arm "previous-descriptor" 1 "changed committed descriptor"
  arm "missing-object" 1 "finite terminal coverage differs"
  arm "object-digest" 1 "object digest differs"
  arm "extra-file" 1 "finite terminal coverage differs"
  arm "terminal-symlink" 1 "symlink in archive terminal"
  arm "parent-symlink" 1 "symlink in archive path"
  arm "changed-stub" 1 "navigation stub differs"
  arm "missing-stub" 1 "P4-SYSTEM-12.md"
  arm "unknown-read" 1 "unknown archived logical path"
  arm "escaping-read" 1 "unknown archived logical path"
  arm "expansion-bound" 1 "archive expansion exceeds bound"
  arm "truncated-gzip" 1 "unreadable archive object"
  arm "nonregular-member" 1 "archive member must be a plain regular file"
  arm "duplicate-member" 1 "duplicate archive member"
  arm "extra-member" 1 "unknown or unsafe archive member"
  arm "unsafe-member" 1 "unknown or unsafe archive member"
  arm "missing-member" 1 "archive member census differs"
  arm "oversized-member" 1 "archive member exceeds bound"
  arm "noncanonical-tar" 1 "noncanonical tar encoding"
  arm "manifest-identity" 1 "manifest identity differs"
  arm "member-identity" 1 "original member identity differs"
  arm "source-bytes" 1 "source byte count differs"
  arm "source-lines" 1 "source line count differs"
  arm "manifest-fields" 1 "unknown manifest fields"
  arm "manifest-duplicate" 1 "duplicate manifest member"
  arm "manifest-path" 1 "unknown manifest member path"
  arm "manifest-string-count" 1 "malformed manifest member identity"
  arm "malformed-json" 1 "malformed archive JSON"
  arm "non-utf8" 1 "original member is not UTF-8"
  arm "manifest-capture" 1 "manifest capture differs"
  arm "oversized-json-integer" 1 "malformed archive JSON"
  arm "front-bound" 1 "archive file exceeds bound"
  arm "extra-directory" 1 "unknown terminal directory"
  arm "corrupt-read" 1 "object digest differs"
  arm "links-green" 0 "incoming history path/anchor resolves"
  arm "links-anchor" 1 "unretained history link anchor"
  arm "links-include" 1 "sealed narrative used as live include"
  printf 'TASK-HISTORY --self-test: %d pass / %d fail\n' "$pass" "$fail"
  [ "$fail" -eq 0 ]
}

[ "${1:-}" = "--self-test" ] && { self_test; exit $?; }
[ "$#" -eq 0 ] || { echo 'TASK-HISTORY: unknown arguments' >&2; exit 2; }
self_test >/dev/null 2>&1 || {
  echo 'TASK-HISTORY: REFUSED — self-test stopped discriminating' >&2; exit 2; }
mkdir -p "$ROOT/target/history-check"
previous="$(mktemp "$ROOT/target/history-check/tasks.XXXXXX")" || exit 2
trap 'rm -f "$previous"' EXIT
tracked="$(git ls-tree --name-only HEAD -- docs/task-history/descriptor.json)" || exit 2
if [ -n "$tracked" ]; then
  git show HEAD:docs/task-history/descriptor.json > "$previous" || exit 2
  python3 scripts/task_history_archive.py --previous "$previous" || exit $?
else
  python3 scripts/task_history_archive.py || exit $?
fi
python3 scripts/check_task_history_links.py
