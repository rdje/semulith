#!/usr/bin/env python3
"""scripts/run_dsp56300_smoke.py — the dsp56300-lab-v0 differential campaign.

For every `profiles/dsp56300-lab-v0/guests/<name>.a56` with a sibling `<name>.meta`:
assemble with the pinned `dsp56300-asm`, run the case on the reference (`difftest`) and on
Semulith's model (`cargo run -p semulith-dsp56300`), and judge the two canonical end-state
dumps with `scripts/compare_dumps.py` (checkpoint-level, field-exact; `cyc` skipped by
recorded rule).

⛔ DELIBERATELY NOT A COMMIT GATE — the same discipline as `run_semulith_smoke.py`: it
needs the untracked, network-acquired reference binaries under `target/refs/`. If they are
missing it REFUSES with the build command (P3-BREADTH.3 slice 2's on-volume build), never
skips silently. The commit-level proof of the same ground truth is the crate's unit tests
(manual-derived expectations, EVD-05), which run under `make check`.

Usage: scripts/run_dsp56300_smoke.py
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(subprocess.run(["git", "rev-parse", "--show-toplevel"],
                           capture_output=True, text=True, check=True).stdout.strip())
GUESTS = ROOT / "profiles" / "dsp56300-lab-v0" / "guests"
ASM = ROOT / "target" / "refs" / "dsp56300-build" / "release" / "dsp56300-asm"
DIFFTEST = ROOT / "target" / "refs" / "dsp56300-build" / "release" / "difftest"
WORK = ROOT / "target" / "dsp56300-smoke"


def refuse(msg: str) -> "NoReturn":  # noqa: F821
    print(f"run_dsp56300_smoke: REFUSED — {msg}", file=sys.stderr)
    sys.exit(2)


def main() -> int:
    for tool in (ASM, DIFFTEST):
        if not tool.is_file():
            refuse(
                f"{tool} is not built. Build the pinned reference on-volume "
                "(P3-BREADTH.3 slice 2): CARGO_HOME=.app-data/cargo-home "
                "CARGO_TARGET_DIR=target/refs/dsp56300-build cargo build --release "
                "--manifest-path target/refs/dsp56300-src/Cargo.toml "
                "--bin dsp56300-asm --bin difftest"
            )
    cases = sorted(GUESTS.glob("*.a56"))
    if not cases:
        refuse(f"no guests under {GUESTS}")
    WORK.mkdir(parents=True, exist_ok=True)
    subprocess.run(["cargo", "build", "-q", "-p", "semulith-dsp56300"], cwd=ROOT, check=True)
    runner = ROOT / "target" / "debug" / "semulith-dsp56300"

    passed = failed = 0
    for src in cases:
        meta = src.with_suffix(".meta")
        if not meta.is_file():
            refuse(f"{src.name} has no sibling .meta — a case without a stop is not a case")
        lod = WORK / f"{src.stem}.lod"
        r = subprocess.run(
            [str(ASM), str(src), "-o", str(lod), "-f", "lod"],
            capture_output=True, text=True)
        if r.returncode != 0:
            refuse(f"the pinned assembler refused {src.name}: {r.stderr.strip()}")

        ref = subprocess.run(
            [str(DIFFTEST), "corpus", str(lod), str(meta), "--dump-mem", "--dump-stack"],
            capture_output=True, text=True)
        sem = subprocess.run(
            [str(runner), str(lod), str(meta), "--dump-mem", "--dump-stack"],
            capture_output=True, text=True)
        if ref.returncode != 0:
            refuse(f"the reference stopped on {src.name}: {ref.stderr.strip()}")
        if sem.returncode != 0:
            print(f"FAIL {src.stem}: the Semulith model stopped: {sem.stderr.strip()}")
            failed += 1
            continue

        (WORK / f"{src.stem}.ref.dump").write_text(ref.stdout)
        (WORK / f"{src.stem}.sem.dump").write_text(sem.stdout)
        verdict = subprocess.run(
            [sys.executable, str(ROOT / "scripts" / "compare_dumps.py"),
             str(WORK / f"{src.stem}.ref.dump"), str(WORK / f"{src.stem}.sem.dump")],
            capture_output=True, text=True)
        line = (verdict.stdout or verdict.stderr).strip()
        if verdict.returncode == 0:
            passed += 1
            print(f"AGREE {src.stem}: {line}")
        else:
            failed += 1
            print(f"FAIL {src.stem}: {line}")
    print(f"dsp56300 smoke: {passed} agree / {failed} fail")
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
