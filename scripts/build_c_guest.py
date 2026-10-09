#!/usr/bin/env python3
"""Build the RV64I C guest using the shared pinned toolchain resolver."""
from __future__ import annotations

import hashlib
import subprocess
import sys
from pathlib import Path

import riscv_toolchain as T

ROOT = Path(__file__).resolve().parent.parent


def main() -> int:
    guest = sys.argv[1] if len(sys.argv) > 1 else "c-scope"
    source = ROOT / "profiles/rv64i-lab-v0/guests" / f"{guest}.c"
    if not source.is_file():
        print(f"build_c_guest: profiles/rv64i-lab-v0/guests/{guest}.c does not exist",
              file=sys.stderr)
        return 2
    work = ROOT / "target/refs/guests"
    try:
        tools = T.select(work)
        obj, elf = work / f"{guest}.o", work / f"{guest}.elf"
        subprocess.run(
            [tools.clang, "--target=riscv64-unknown-elf", "-march=rv64i", "-mabi=lp64",
             "-mno-relax", "-mcmodel=medany", "-msmall-data-limit=0", "-O1",
             "-ffreestanding", "-fno-builtin", "-nostdlib", "-Wall", "-Wextra", "-Werror",
             "-c", str(source.relative_to(ROOT)), "-o", str(obj.relative_to(ROOT))],
            cwd=ROOT, check=True)
        subprocess.run([*tools.lld, "--image-base=0x80000000", "--entry=_start",
                        "-o", str(elf.relative_to(ROOT)), str(obj.relative_to(ROOT))],
                       cwd=ROOT, check=True)
    except (T.Refusal, OSError, subprocess.CalledProcessError) as error:
        print(f"build_c_guest: REFUSED — {error}", file=sys.stderr)
        return 2
    print(f"build_c_guest: {guest}.elf built")
    print(f"  clang: {tools.clang_identity} [{tools.clang}]")
    print(f"  lld:   {tools.lld_identity} [{' '.join(tools.lld)}]")
    print(f"  sha256: {hashlib.sha256(elf.read_bytes()).hexdigest()}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
