#!/usr/bin/env bash
# build_c_guest.sh — compile a tracked .c guest into its ELF with the PINNED toolchain.
#
# Pinned by `decision_c-guest-routing-and-toolchain` (2026-09-30): a clang WITH a
# RISC-V backend (measured: Homebrew llvm@21 clang 21.1.8 — Apple clang has none) plus
# an ld.lld (measured: zig 0.16.0's bundled lld, Homebrew LLD 21.1.8). A toolchain that
# cannot target riscv64 is REFUSED BY NAME, never silently substituted; nothing is
# installed by this script.
#
# The ELF is a build artifact — untracked, on-volume under target/refs/guests/, with
# the same standing as the reference binaries: the live differential needs it, the
# commit gate does not.
#
# usage: scripts/build_c_guest.sh [guest-name]   (default: c-scope)
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"; cd "$ROOT"
GUEST="${1:-c-scope}"
SRC="profiles/rv64i-lab-v0/guests/$GUEST.c"
[ -f "$SRC" ] || { echo "build_c_guest: $SRC does not exist" >&2; exit 2; }
WORK="target/refs/guests"
mkdir -p "$WORK"

# --- compiler discovery: every candidate is PROBED for the RISC-V backend ----------
probe_clang() {
  printf 'int f(int a, int b) { return a + b; }\n' | \
    "$1" --target=riscv64-unknown-elf -march=rv64i -mabi=lp64 -x c -c \
      -o "$WORK/.probe.o" - >/dev/null 2>&1
}
CLANG=""
for c in "${SEMULITH_RISCV_CLANG:-}" /opt/homebrew/opt/llvm@21/bin/clang clang; do
  [ -n "$c" ] || continue
  command -v "$c" >/dev/null 2>&1 || continue
  if probe_clang "$c"; then CLANG="$c"; break; fi
done
rm -f "$WORK/.probe.o"
[ -n "$CLANG" ] || { echo "build_c_guest: no clang with a RISC-V backend found" \
  "(probed \$SEMULITH_RISCV_CLANG, /opt/homebrew/opt/llvm@21/bin/clang, clang) —" \
  "see docs/decisions/decision_c-guest-routing-and-toolchain.md" >&2; exit 2; }

# --- linker discovery ---------------------------------------------------------------
LLD=()
if [ -n "${SEMULITH_RISCV_LLD:-}" ]; then LLD=("$SEMULITH_RISCV_LLD")
elif command -v ld.lld >/dev/null 2>&1; then LLD=(ld.lld)
elif command -v zig >/dev/null 2>&1; then LLD=(zig ld.lld)
else echo "build_c_guest: no ld.lld found (probed \$SEMULITH_RISCV_LLD, ld.lld, zig)" >&2; exit 2
fi

# --- compile + link: RV64I only, no relaxation, medany (the image lives at           ---
# --- 0x80000000, outside medlow's range), no gp-relative small data (gp is never     ---
# --- initialized in the laboratory)                                                  ---
"$CLANG" --target=riscv64-unknown-elf \
  -march=rv64i -mabi=lp64 -mno-relax -mcmodel=medany -msmall-data-limit=0 \
  -O1 -ffreestanding -fno-builtin -nostdlib -Wall -Wextra -Werror \
  -c "$SRC" -o "$WORK/$GUEST.o"
"${LLD[@]}" --image-base=0x80000000 --entry=_start -o "$WORK/$GUEST.elf" "$WORK/$GUEST.o"

echo "build_c_guest: $GUEST.elf built"
echo "  clang: $($CLANG --version | head -1) [$CLANG]"
echo "  lld:   $("${LLD[@]}" --version | head -1) [${LLD[*]}]"
echo "  sha256: $(shasum -a 256 "$WORK/$GUEST.elf" | cut -d' ' -f1)"
