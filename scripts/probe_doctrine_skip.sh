#!/usr/bin/env bash
# scripts/probe_doctrine_skip.sh — the controls of scripts/doctrine_skip.sh (XTASK.16): which staged sets may answer a
# check from its last green run, which documents the tracked data names, and what the key follows. It works only in a
# scratch repository under target/, so it drops the GIT_* variables a hook would hand it; the rule itself never does.
set -uo pipefail
ROOT="$(git rev-parse --show-toplevel)" || exit 2
unset GIT_DIR GIT_WORK_TREE GIT_INDEX_FILE GIT_COMMON_DIR GIT_OBJECT_DIRECTORY GIT_ALTERNATE_OBJECT_DIRECTORIES GIT_NAMESPACE GIT_PREFIX
# shellcheck source=scripts/doctrine_skip.sh
. "$ROOT/scripts/doctrine_skip.sh" || exit 2
mkdir -p "$ROOT/target/doctrine-selftest" || exit 2
t="$(mktemp -d "$ROOT/target/doctrine-selftest/doctrine-skip.XXXXXX")" || exit 2
[ -n "$t" ] && [ -d "$t" ] || { echo "probe_doctrine_skip: no scratch directory" >&2; exit 2; }
trap 'rm -rf "$t"' EXIT
cd "$t" || exit 2
git init -q . 2>/dev/null || exit 2
[ "$(cd "$(git rev-parse --show-toplevel)" && pwd -P)" = "$(pwd -P)" ] || { echo "probe_doctrine_skip: the scratch repository is not its own" >&2; exit 2; }
mkdir -p docs/tasks docs/decisions docs/models/u/src xtask/src crates/core scripts .githooks added-later profiles/u/selections
for f in docs/tasks/A.md docs/decisions/d.md docs/decisions/named.md docs/models/u/src/page.md docs/INFORMATION_CATALOG.md README.md MEMORY.md \
         CHANGELOG.md xtask/src/main.rs crates/core/lib.rs scripts/tool.py .githooks/pre-commit Cargo.lock Makefile notes.txt added-later/x.rs; do
  echo "one" > "$f"
done
printf '(selection (object "docs/decisions/named.md"))\n(unit (book "docs/models/u/"))\n' > profiles/u/selections/s.sexp
git add -A || exit 2

pass=0; fail=0
arm() { # label, expected exit status, command…
  local label="$1" want="$2" got; shift 2
  "$@" >/dev/null 2>&1; got=$?
  if [ "$got" = "$want" ]; then pass=$((pass+1)); else fail=$((fail+1)); printf 'probe_doctrine_skip MISS: %s (exit %s, want %s)\n' "$label" "$got" "$want" >&2; fi
}
same() { [ "$1" = "$2" ]; }
named="$(doctrine_named_documents)"
only() { staged="$1" doctrine_only_ledger "${2-$named}"; }  # a staged set, one path per line; the named documents

# 1. The documents the tracked data names are derived, never listed.
arm "the named documents are the two the data names"            0 same "$named" $'docs/decisions/named.md\ndocs/models/u/'

# 2. Which staged sets may skip. The founding case first: a driver alone.
arm "RED a staged driver never skips its own check"             1 only "xtask/src/main.rs"
arm "RED the engine never skips"                                1 only "crates/core/lib.rs"
arm "RED a script never skips"                                  1 only "scripts/tool.py"
arm "RED the lockfile never skips"                              1 only "Cargo.lock"
arm "RED a hook never skips"                                    1 only ".githooks/pre-commit"
arm "RED dossier data never skips"                              1 only "profiles/u/selections/s.sexp"
arm "RED a directory nobody declared never skips"               1 only "added-later/x.rs"
arm "RED a root file nobody declared never skips"               1 only "notes.txt"
arm "RED a document nobody declared never skips"                1 only "docs/INFORMATION_CATALOG.md"
arm "RED the landing page never skips"                          1 only "README.md"
arm "RED a unit-book page never skips"                          1 only "docs/models/u/src/page.md"
arm "RED a decision record the data names never skips"          1 only $'docs/tasks/A.md\ndocs/decisions/named.md'
arm "RED one code path among ledger entries never skips"        1 only $'docs/tasks/A.md\nMEMORY.md\nxtask/src/main.rs'
arm "RED a file beside a ledger file is not ledger"             1 only "MEMORY.md.bak"
arm "RED nothing staged is not a ledger commit"                 1 only ""
arm "GREEN the ledger alone may skip"                           0 only $'docs/tasks/A.md\nMEMORY.md\nCHANGELOG.md\ndocs/decisions/d.md'

# 3. Which checks may skip at all.
arm "RED an undeclared check never skips"                       1 doctrine_skips GATE-REPORT
arm "GREEN a declared check may"                                0 doctrine_skips PROFILE-CONSISTENCY

# 4. What the key follows: every tracked byte outside the ledger, and the ledger documents the data names.
k0="$(doctrine_inputs_key "$named")"
arm "the key is a digest"                                       0 test "${#k0}" = 64
echo two > docs/tasks/A.md; echo two > MEMORY.md; echo two > docs/decisions/d.md; echo new > docs/tasks/B.md; git add -A
arm "GREEN the ledger moving leaves the key"                    0 same "$k0" "$(doctrine_inputs_key "$named")"
for f in docs/decisions/named.md docs/models/u/src/page.md docs/INFORMATION_CATALOG.md README.md xtask/src/main.rs crates/core/lib.rs scripts/tool.py \
         Cargo.lock .githooks/pre-commit added-later/x.rs notes.txt; do
  before="$(doctrine_inputs_key "$named")"; echo two > "$f"; git add -A
  arm "RED $f moving moves the key"                             1 same "$before" "$(doctrine_inputs_key "$named")"
done
before="$(doctrine_inputs_key "$named")"; echo x > scripts/new.py; git add -A
arm "RED a new code file moves the key"                         1 same "$before" "$(doctrine_inputs_key "$named")"
before="$(doctrine_inputs_key "$named")"; echo x > MEMORY.md.bak; git add -A
arm "RED a file beside a ledger file moves the key"             1 same "$before" "$(doctrine_inputs_key "$named")"
before="$(doctrine_inputs_key "$named")"; git rm -q --cached Makefile
arm "RED a removed code file moves the key"                     1 same "$before" "$(doctrine_inputs_key "$named")"
printf '(selection (object "docs/decisions/d.md"))\n' >> profiles/u/selections/s.sexp; git add -A
renamed="$(doctrine_named_documents)"
arm "RED data naming one more decision makes it an input"       1 only "docs/decisions/d.md" "$renamed"
arm "RED and its bytes join the key"                            1 same "$(doctrine_inputs_key "$named")" "$(doctrine_inputs_key "$renamed")"

want=37
[ $((pass+fail)) -eq "$want" ] || { echo "probe_doctrine_skip HARNESS: $((pass+fail)) arm(s) ran, $want declared" >&2; exit 2; }
echo "probe_doctrine_skip: $pass pass / $fail fail"
[ "$fail" -eq 0 ]
