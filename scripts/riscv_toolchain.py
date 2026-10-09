#!/usr/bin/env python3
"""Read-only discovery of the C/ACT4 toolchain pinned by the guest decision.

Explicit overrides are authoritative: an unusable override refuses rather than
falling back. Check all identities before creating an on-volume backend probe.
No installation, global cache or shell command lookup is involved.
"""
from __future__ import annotations

import os
import re
import shutil
import subprocess
import tempfile
from dataclasses import dataclass
from pathlib import Path

LLVM_VERSION = "21.1.8"
ZIG_VERSION = "0.16.0"


class Refusal(Exception):
    """The pinned toolchain cannot be used; never an implicit substitution."""


@dataclass(frozen=True)
class Toolchain:
    clang: str
    lld: tuple[str, ...]
    clang_identity: str
    lld_identity: str
    nm: str | None = None


def _executable(candidate: str) -> str:
    found = shutil.which(candidate)
    if found is None:
        raise Refusal(f"{candidate}: executable is missing")
    return str(Path(found).absolute())


def _identity(argv: tuple[str, ...], pattern: str, expected: str,
              query: str = "--version") -> str:
    try:
        result = subprocess.run([*argv, query], capture_output=True,
                                text=True, check=False)
    except OSError as error:
        raise Refusal(f"{argv[0]}: version query failed: {error}") from error
    text = result.stdout.strip()
    if result.returncode or re.search(pattern, text) is None:
        raise Refusal(f"{' '.join(argv)}: expected {expected}; got "
                      f"{text or result.stderr.strip() or '<no identity>'}")
    return text.splitlines()[0]


def _llvm_identity(argv: tuple[str, ...], name: str) -> str:
    pattern = rf"\b{re.escape(name)} {re.escape(LLVM_VERSION)}(?=\s|$)"
    return _identity(argv, pattern, f"{name} {LLVM_VERSION}")


def _compiler_candidates() -> list[str]:
    override = os.environ.get("SEMULITH_RISCV_CLANG")
    return ([override] if override else
            ["/opt/homebrew/opt/llvm@21/bin/clang", "clang"])


def _linker() -> tuple[tuple[str, ...], str]:
    override = os.environ.get("SEMULITH_RISCV_LLD")
    candidates = [(override,)] if override else [("ld.lld",), ("zig", "ld.lld")]
    errors = []
    for candidate in candidates:
        try:
            argv = (_executable(candidate[0]), *candidate[1:])
            if len(argv) == 2:
                # The Zig driver is also pinned, although the effective linker
                # identity is the LLD banner, not the driver version.
                _identity((argv[0],), rf"^{re.escape(ZIG_VERSION)}$",
                          f"Zig {ZIG_VERSION}", query="version")
            return argv, _llvm_identity(argv, "LLD")
        except Refusal as error:
            errors.append(str(error))
    raise Refusal("no pinned linker: " + "; ".join(errors))


def select(work: Path, *, require_nm: bool = False) -> Toolchain:
    """Validate identities, then probe RV64I compilation in the caller's work dir."""
    lld, lld_identity = _linker()
    errors = []
    for candidate in _compiler_candidates():
        try:
            clang = _executable(candidate)
            clang_identity = _llvm_identity((clang,), "clang version")
            nm = None
            if require_nm:
                nm = _executable(str(Path(clang).parent / "llvm-nm"))
                _llvm_identity((nm,), "LLVM version")
            # All selected tools have passed identity checks. Keep concurrent
            # probes distinct, remove them on either success or refusal.
            work.mkdir(parents=True, exist_ok=True)
            with tempfile.TemporaryDirectory(prefix="toolchain-probe-", dir=work) as scratch:
                result = subprocess.run(
                    [clang, "--target=riscv64-unknown-elf", "-march=rv64i", "-mabi=lp64",
                     "-x", "c", "-c", "-o", str(Path(scratch) / "probe.o"), "-"],
                    input="int f(int a, int b) { return a + b; }\n",
                    capture_output=True, text=True, check=False)
                if result.returncode:
                    raise Refusal(f"{clang}: RISC-V backend probe failed: "
                                  f"{result.stderr.strip()}")
            return Toolchain(clang, lld, clang_identity, lld_identity, nm)
        except (Refusal, OSError) as error:
            errors.append(str(error))
    raise Refusal("no pinned compiler: " + "; ".join(errors))
