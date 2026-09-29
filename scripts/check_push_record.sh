#!/usr/bin/env bash
# scripts/check_push_record.sh — PUSH-RECORD (project doctrine, PUSH-DISCIPLINE.3).
#
# The approval ledger (`docs/push-approvals.md`) is the tracked, append-only record of
# exceptional pushes — who approved, when, why, and what range of commits the push carried.
# "Append-only" is a property this check enforces, not a hope:
#
#   1. APPEND-ONLY  a staged change to the ledger must leave HEAD's content a PREFIX of the
#      new content — stronger than "no deletions": history is never rewritten, and an edit
#      inside an old entry is exactly the falsification this file exists to make visible.
#      (The ledger's creation commit is the initial append; an untracked-at-HEAD ledger
#      passes this half vacuously.)
#   2. SHAPE        every `## SEMULITH-PUSH-NNNN — <timestamp>` entry carries the required
#      fields (Approved by / Reason / Range / Suite), and the ids are sequential from 0001 —
#      a gap or a renumbering is a rewritten history wearing append-only's clothes.
#
# CONTRACT: exit code is the verdict; explains on stderr; deterministic; read-only; no network.
#   --self-test   run the RED/GREEN controls against synthetic fixtures and exit.
set -uo pipefail
ROOT="$(git rev-parse --show-toplevel)"; cd "$ROOT"
LEDGER="docs/push-approvals.md"

check_ledger() { # $1 = repo root ("git" mode reads HEAD/the index; "fs" mode the working tree)
python3 - "$1" <<'PY'
import re
import subprocess
import sys
from pathlib import Path

root = Path(sys.argv[1])
ledger = root / "docs/push-approvals.md"
findings = []

# ---- 2. SHAPE: every entry carries the required fields, ids sequential ----------------
text = ledger.read_text() if ledger.is_file() else ""
entries = [(m.group(1), m.start()) for m in re.finditer(r"(?m)^## (SEMULITH-PUSH-\d{4}) — \S+", text)]
for i, (eid, start) in enumerate(entries):
    want = f"SEMULITH-PUSH-{i + 1:04d}"
    if eid != want:
        findings.append(f"NONSEQUENTIAL {eid}: the {i + 1}(th) entry must be {want} — a gap "
                        f"or a renumbering is a rewritten history wearing append-only's clothes")
    end = entries[i + 1][1] if i + 1 < len(entries) else len(text)
    body = text[start:end]
    for field in ("Approved by:", "Reason:", "Range:", "Suite:"):
        if f"**{field}**" not in body:
            findings.append(f"MISSING FIELD {eid}: no '{field}' — an entry without it is an "
                            f"assertion without its evidence")
    m = re.search(r"\*\*Range:\*\*\s+(\S+)\.\.([0-9a-f]{40})\s+—\s+(\d+)", body)
    if not m:
        findings.append(f"BAD RANGE {eid}: the Range field is not '<upstream>..<sha> — N'")

# ---- 1. APPEND-ONLY: a staged change must keep HEAD's content a prefix -----------------
staged = subprocess.run(["git", "diff", "--cached", "--name-only", "--", str(ledger.relative_to(root))],
                        capture_output=True, text=True, cwd=root).stdout.strip()
if staged:
    head = subprocess.run(["git", "show", f"HEAD:{ledger.relative_to(root)}"],
                          capture_output=True, text=True, cwd=root)
    index = subprocess.run(["git", "show", f":{ledger.relative_to(root)}"],
                           capture_output=True, text=True, cwd=root)
    if index.returncode != 0:
        findings.append(f"NOT STAGED {ledger.name}: the ledger is named in the diff but has no "
                        f"index content — cannot judge; the check refuses rather than guess")
    elif head.returncode == 0 and not index.stdout.startswith(head.stdout):
        findings.append(f"REWRITTEN {ledger.name}: the staged ledger does not begin with HEAD's "
                        f"content — append-only means append-ONLY. A correction is a new entry, "
                        f"never an edit.")

for f in findings:
    print(f)
print(f"__CHECKED__ {len(entries)}")
sys.exit(1 if findings else 0)
PY
}

self_test() {
  SELFTEST_TMP() { local d="$ROOT/target/doctrine-selftest"; mkdir -p "$d"; mktemp -d "$d/XXXXXX"; }
  local t pass=0 fail=0 out rc
  t="$(SELFTEST_TMP)"

  argc() {
    [ "$2" -eq "$1" ] && return 0
    fail=$((fail+1))
    printf 'PUSH-RECORD self-test HARNESS: %s() got %s argument(s), expected %s — a missing `;` before `arm` swallows it\n' "$3" "$2" "$1" >&2
    return 1
  }
  arm() {
    argc 3 "$#" arm || return
    out="$(check_ledger "$t" 2>&1)"; rc=$?
    if [ "$rc" != "$2" ]; then
      fail=$((fail+1)); printf 'PUSH-RECORD self-test MISS: %s expected rc=%s got rc=%s\n%s\n' "$1" "$2" "$rc" "$out" >&2
    elif ! printf '%s' "$out" | grep -qF "$3"; then
      fail=$((fail+1)); printf 'PUSH-RECORD self-test MISS: %s right verdict, wrong reason (no %s)\n%s\n' "$1" "$3" "$out" >&2
    else pass=$((pass+1)); fi
  }

  # the fixture: a scratch repo holding first a header-only ledger, then one entry
  mkdir -p "$t/docs"
  git -C "$t" init -q; git -C "$t" config user.email t@t; git -C "$t" config user.name t
  printf '# Push approvals\n' > "$t/docs/push-approvals.md"
  git -C "$t" add -A; git -C "$t" commit -q -m "base"

  arm "GREEN the header-only ledger" 0 "__CHECKED__ 0"

  # a pure append is permitted
  cat >> "$t/docs/push-approvals.md" <<'EOF'

## SEMULITH-PUSH-0001 — 2026-09-29T00:00:00+0000

- **Approved by:** the director
- **Reason:** ship the reviewed slice
- **Range:** origin/main..0123456789012345678901234567890123456789 — 3 commit(s) since the last push, plus this record commit
- **Suite:** `make ci` green at 0123456789012345678901234567890123456789 before this record was written
EOF
  git -C "$t" add docs/push-approvals.md
  arm "GREEN a pure append" 0 "__CHECKED__ 1"
  git -C "$t" commit -q -m "first entry"

  # a second pure append is permitted
  cat >> "$t/docs/push-approvals.md" <<'EOF'

## SEMULITH-PUSH-0002 — 2026-09-29T01:00:00+0000

- **Approved by:** the director
- **Reason:** the second slice
- **Range:** origin/main..aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa — 2 commit(s) since the last push, plus this record commit
- **Suite:** `make ci` green at aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa before this record was written
EOF
  git -C "$t" add docs/push-approvals.md
  arm "GREEN a second pure append" 0 "__CHECKED__ 2"
  git -C "$t" commit -q -m "second entry"

  # editing an old entry is refused
  sed -i.bak 's/the second slice/a rewritten reason/' "$t/docs/push-approvals.md"
  rm -f "$t/docs/push-approvals.md.bak"
  git -C "$t" add docs/push-approvals.md
  arm "RED   an edited old entry (history rewritten)" 1 "REWRITTEN"
  git -C "$t" checkout -q -- docs/push-approvals.md

  # an entry missing a required field is refused
  cat >> "$t/docs/push-approvals.md" <<'EOF'

## SEMULITH-PUSH-0002 — 2026-09-29T01:00:00+0000

- **Approved by:** the director
- **Range:** origin/main..aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa — 2 commit(s) since the last push, plus this record commit
- **Suite:** `make ci` green at aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa before this record was written
EOF
  git -C "$t" add docs/push-approvals.md
  arm "RED   an entry missing its Reason" 1 "MISSING FIELD"
  git -C "$t" checkout -q -- docs/push-approvals.md

  # a gap in the sequence is refused
  cat >> "$t/docs/push-approvals.md" <<'EOF'

## SEMULITH-PUSH-0007 — 2026-09-29T01:00:00+0000

- **Approved by:** the director
- **Reason:** a skipped number
- **Range:** origin/main..aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa — 2 commit(s) since the last push, plus this record commit
- **Suite:** `make ci` green at aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa before this record was written
EOF
  git -C "$t" add docs/push-approvals.md
  arm "RED   a skipped sequence number" 1 "NONSEQUENTIAL"
  git -C "$t" checkout -q -- docs/push-approvals.md

  rm -rf "$t"
  printf 'PUSH-RECORD --self-test: %d pass / %d fail\n' "$pass" "$fail"
  [ "$fail" -eq 0 ]
}

[ "${1:-}" = "--self-test" ] && { self_test; exit $?; }

self_test >/dev/null 2>&1 || {
  echo "PUSH-RECORD: REFUSED — the check does not discriminate (self-test failed)." >&2; exit 2; }

out="$(check_ledger "$ROOT")"; rc=$?
count="$(printf '%s' "$out" | sed -n 's/^__CHECKED__ //p')"
body="$(printf '%s' "$out" | grep -v '^__CHECKED__ ' || true)"
if [ "$rc" -ne 0 ]; then
  { echo "PUSH-RECORD: the approval ledger was rewritten or misshapen."
    printf '%s\n' "$body" | sed 's/^/  /'
    echo "  The ledger is append-only: a correction is a new entry, never an edit."; } >&2
  exit 1
fi
printf 'PUSH-RECORD: ok (the ledger is append-only; %s entr%s well-formed)\n' "${count:-0}" \
  "$([ "${count:-0}" = "1" ] && echo "y" || echo "ies")"
exit 0
