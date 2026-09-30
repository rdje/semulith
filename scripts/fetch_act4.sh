#!/usr/bin/env bash
# fetch_act4.sh — acquire the pinned ACT4 generated suite (P2-SCALAR.5 strand 2).
#
# A blobless sparse clone of github.com/riscv/riscv-arch-test at the pinned commit
# e2216915d9a17acc142610831d88de8b65683866 (branch act4), checked out to exactly the
# three paths the RV64I campaign needs — tests/env (the macro headers),
# tests/rv64i/I (the 51 generated test files), config (the example DUT configs) —
# 45 MB of the ~672 MB full tree. The clone lives at target/refs/riscv-arch-test/:
# untracked, on the repository volume (data-locality policy), the same standing as the
# reference binaries. The docs/test-plan half of the suite is a separate acquisition:
# the catalogued material RISCV-ARCH-TEST-ACT4 (materials/catalog.sexp, .materials/).
#
# Needs the network, so it is deliberately NOT a commit gate — the same reasoning as
# scripts/fetch_references.sh. A clone present at the WRONG commit is refused, never
# silently re-pinned.
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"; cd "$ROOT"
PIN=e2216915d9a17acc142610831d88de8b65683866
DIR=target/refs/riscv-arch-test
URL=https://github.com/riscv/riscv-arch-test

if [ -d "$DIR/.git" ]; then
  HEAD=$(git -C "$DIR" rev-parse HEAD)
  [ "$HEAD" = "$PIN" ] || { echo "fetch_act4: $DIR is at $HEAD, not the pinned $PIN —" \
    "remove the directory and re-run (the pin moves by reviewed decision, never by a script)" >&2; exit 2; }
  echo "fetch_act4: already at the pinned $PIN"
else
  git clone --filter=blob:none --no-checkout "$URL" "$DIR"
  git -C "$DIR" sparse-checkout set tests/env tests/rv64i/I config
  git -C "$DIR" checkout "$PIN"
fi

# The census is the verification: the pin's content, counted, not assumed.
FILES=$(find "$DIR/tests/rv64i/I" -name 'I-*.S' | wc -l | tr -d ' ')
SIGUPD=$(grep -h -c "RVTEST_SIGUPD(" "$DIR"/tests/rv64i/I/I-*.S | paste -sd+ - | bc)
echo "fetch_act4: ok — $FILES RV64I test files, $SIGUPD RVTEST_SIGUPD invocations"
[ "$FILES" = "51" ] || { echo "fetch_act4: expected 51 test files, counted $FILES" >&2; exit 1; }
