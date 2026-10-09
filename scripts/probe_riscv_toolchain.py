#!/usr/bin/env python3
"""Public C-build/ACT4 selection controls with isolated on-volume fake tools."""
from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from unittest.mock import patch

import riscv_toolchain as T
import run_act4_campaign as A

ROOT = Path(__file__).resolve().parent.parent


def fake(path: Path, banner: str, *, backend: bool = True, version_rc: int = 0) -> None:
    path.write_text(f'''#!{sys.executable}
import pathlib, sys
with open({str(path.parent / 'calls.log')!r}, 'a') as log:
 log.write({path.name!r} + ' ' + ' '.join(sys.argv[1:]) + '\\n')
if '--version' in sys.argv or sys.argv[1:] == ['version']:
 print({banner!r}); sys.exit({version_rc})
if '-' in sys.argv and not {backend!r}:
 print('missing RISC-V backend', file=sys.stderr); sys.exit(3)
if '-o' in sys.argv:
 pathlib.Path(sys.argv[sys.argv.index('-o')+1]).write_bytes(b'fixture artifact')
''')
    path.chmod(0o755)


def run(mutation: str | None) -> int:
    base = ROOT / "target/toolchain-probe"
    base.mkdir(parents=True, exist_ok=True)
    failures = []
    count = 0
    with tempfile.TemporaryDirectory(dir=base) as scratch:
        root = Path(scratch)
        scripts = root / "scripts"
        scripts.mkdir()
        for name in ("build_c_guest.sh", "build_c_guest.py", "riscv_toolchain.py"):
            shutil.copyfile(ROOT / "scripts" / name, scripts / name)
        if mutation == "ignore-version":
            source = scripts / "riscv_toolchain.py"
            old = "if result.returncode or re.search(pattern, text) is None:"
            assert old in source.read_text()
            source.write_text(source.read_text().replace(old, "if result.returncode:"))
        source = root / "profiles/rv64i-lab-v0/guests/c-scope.c"
        source.parent.mkdir(parents=True)
        source.write_text("void _start(void) {}\n")
        bin_dir = root / "bin"
        bin_dir.mkdir()
        (bin_dir / "python3").symlink_to(sys.executable)
        clang, lld, nm = (bin_dir / name for name in ("clang", "ld.lld", "llvm-nm"))
        good_clang, good_lld = "clang version 21.1.8", "LLD 21.1.8"
        out = root / "target/refs/guests"

        cases = [
            ("pinned", good_clang, good_lld, True, False, False, 0, ""),
            ("wrong-clang", "clang version 99.0.0", good_lld, True, False, False, 0,
             "expected clang version 21.1.8"),
            ("wrong-lld", good_clang, "LLD 99.0.0", True, False, False, 0, "expected LLD 21.1.8"),
            ("suffix-version", "clang version 21.1.80", good_lld, True, False, False, 0,
             "expected clang version 21.1.8"),
            ("missing-clang", good_clang, good_lld, True, True, False, 0, "executable is missing"),
            ("missing-lld", good_clang, good_lld, True, False, True, 0, "executable is missing"),
            ("no-backend", good_clang, good_lld, False, False, False, 0, "RISC-V backend probe failed"),
            ("version-failure", good_clang, good_lld, True, False, False, 4,
             "expected clang version 21.1.8"),
        ]
        for name, cb, lb, backend, missing_c, missing_l, version_rc, reason in cases:
            fake(clang, cb, backend=backend, version_rc=version_rc)
            fake(lld, lb)
            fake(nm, "LLVM version 21.1.8")
            env = dict(os.environ, SEMULITH_RISCV_CLANG=str(clang) + ("-absent" if missing_c else ""),
                       SEMULITH_RISCV_LLD=str(lld) + ("-absent" if missing_l else ""),
                       PYTHONDONTWRITEBYTECODE="1")
            for caller in ("C", "ACT4"):
                count += 1
                out.mkdir(parents=True, exist_ok=True)
                obj, elf = out / "c-scope.o", out / "c-scope.elf"
                obj.write_bytes(b"previous object")
                elf.write_bytes(b"previous ELF")
                (bin_dir / "calls.log").unlink(missing_ok=True)
                if caller == "C":
                    p = subprocess.run(["bash", str(scripts / "build_c_guest.sh")],
                                       env=env, capture_output=True, text=True, check=False)
                    rc, text = p.returncode, p.stdout + p.stderr
                else:
                    with patch.dict(os.environ, env, clear=True), patch.object(A, "OUT", out):
                        try:
                            A.toolchain()
                            rc, text = 0, ""
                        except A.Refusal as error:
                            rc, text = 2, str(error)
                expected = 2 if reason else 0
                writes = (bin_dir / "calls.log").read_text() if (bin_dir / "calls.log").exists() else ""
                okay = rc == expected and reason in text
                if reason:
                    okay &= obj.read_bytes() == b"previous object" and elf.read_bytes() == b"previous ELF"
                    if name != "no-backend":
                        okay &= " -o " not in writes
                elif caller == "C":
                    okay &= obj.read_bytes() == elf.read_bytes() == b"fixture artifact"
                okay &= not list(out.glob("toolchain-probe-*"))
                if not okay:
                    failures.append(f"{caller}/{name}: expected rc={expected}, reason={reason!r}; "
                                    f"got rc={rc}: {text.strip()}")

        # Symbol-reader identity is an ACT4 prerequisite, checked before probing.
        fake(clang, good_clang)
        fake(lld, good_lld)
        fake(nm, "LLVM version 99.0.0")
        with patch.dict(os.environ, {"SEMULITH_RISCV_CLANG": str(clang),
                                     "SEMULITH_RISCV_LLD": str(lld)}), patch.object(A, "OUT", out):
            count += 1
            try:
                A.toolchain()
                failures.append("ACT4 accepted wrong symbol-reader identity")
            except A.Refusal as error:
                if "expected LLVM version 21.1.8" not in str(error):
                    failures.append(str(error))

        # Exercise portable PATH discovery with no host Homebrew dependency and
        # the actual Zig 'version' public command, not '--version'.
        fake(nm, "LLVM version 21.1.8")
        count += 1
        env = dict(os.environ, SEMULITH_RISCV_CLANG="bin/clang",
                   SEMULITH_RISCV_LLD="bin/ld.lld", PYTHONDONTWRITEBYTECODE="1")
        result = subprocess.run(["bash", str(scripts / "build_c_guest.sh")],
                                cwd=bin_dir, env=env, capture_output=True, text=True)
        if result.returncode or (out / "c-scope.elf").read_bytes() != b"fixture artifact":
            failures.append("C wrapper did not resolve relative overrides from its repository root")
        lld.unlink()
        zig = bin_dir / "zig"
        zig.write_text(f'''#!{sys.executable}
import sys
print('0.16.0' if sys.argv[1:] == ['version'] else 'LLD 21.1.8')
''')
        zig.chmod(0o755)
        which = shutil.which
        def local_which(candidate: str) -> str | None:
            return None if candidate.startswith("/opt/homebrew/") else which(candidate)
        env = dict(os.environ, PATH=str(bin_dir))
        env.pop("SEMULITH_RISCV_CLANG", None)
        env.pop("SEMULITH_RISCV_LLD", None)
        with patch.dict(os.environ, env, clear=True), patch.object(T.shutil, "which", local_which):
            count += 1
            selected = T.select(out, require_nm=True)
            if selected.clang != str(clang) or selected.lld != (str(zig), "ld.lld"):
                failures.append("PATH/Zig selection differs")
            count += 1
            zig.write_text(zig.read_text().replace("0.16.0", "0.17.0"))
            try:
                T.select(out)
                failures.append("wrong Zig driver accepted")
            except T.Refusal as error:
                if "expected Zig 0.16.0" not in str(error):
                    failures.append(str(error))

    for failure in failures:
        print(f"CONTROL-MISSED: {failure}")
    print(f"Toolchain probe: {count - len(failures)}/{count} controls passed")
    return 1 if failures else 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mutation", choices=["ignore-version"])
    sys.exit(run(parser.parse_args().mutation))
