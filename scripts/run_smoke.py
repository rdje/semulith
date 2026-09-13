#!/usr/bin/env python3
"""Run the P0-PROFILE.6 matched-profile experiment end to end, and check it.

One command that: assembles the tracked guest sources, runs them on TWO independently built
reference models configured to `rv64i-lab-v0`, compares the two traces for first divergence,
checks the Sail trace against expectations DERIVED FROM THE SPECIFICATION rather than from any
model, and re-runs to confirm the result reproduces byte for byte.

⛔ NOT A COMMIT GATE. It needs the reference binaries under `target/refs/`, which are untracked
and acquired by `scripts/fetch_references.sh`. The same reasoning as `fetch_sources.sh`.

⚠️ WHAT A PASS MEANS, exactly. It means: for THESE inputs, two models agreed with each other and
with values derived from the specification, and the run reproduced. `docs/EVIDENCE_AND_GATES.md`
is explicit that finite differential testing is tested evidence and never universal proof — and
two models with shared semantic ancestry can agree while both being wrong, which is `EVD-04` and
why the independence inventory is a separate leaf.
"""

from __future__ import annotations

import hashlib
import subprocess
import sys
import tomllib
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from compare_traces import align, compare, parse_sail, parse_spike, CompareError  # noqa: E402
from riscv_asm import Assembler, write_elf64  # noqa: E402

ROOT = Path(subprocess.run(["git", "rev-parse", "--show-toplevel"],
                           capture_output=True, text=True, check=True).stdout.strip())
PROFILE = "rv64i-lab-v0"
ENTRY = 0x80000000
SAIL = ROOT / "target/refs/sail-riscv-Mac-arm64/bin/sail_riscv_sim"
SPIKE = ROOT / "target/refs/spike-build/spike"
CONFIG = ROOT / f"profiles/{PROFILE}/reference/sail-{PROFILE}.override.json"
GUESTS = ROOT / f"profiles/{PROFILE}/guests"
OUT = ROOT / "target/refs/guests"

# Spike executes a built-in reset vector before the entry point; its instruction bound counts
# those, so it is given headroom. The comparison aligns on the entry, so the extra steps are
# dropped rather than compared.
SPIKE_RESET_STEPS = 5

failures: list[str] = []


def say(ok: bool, label: str, detail: str = "") -> None:
    print(f"  {'PASS' if ok else 'FAIL'}  {label}{('  ' + detail) if detail else ''}")
    if not ok:
        failures.append(label)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def build(name: str) -> tuple[Path, int]:
    asm = Assembler(ROOT / "target/refs/riscv-opcodes")
    words = asm.assemble((GUESTS / f"{name}.s").read_text().splitlines())
    payload = b"".join(w.to_bytes(4, "little") for w, _ in words)
    OUT.mkdir(parents=True, exist_ok=True)
    elf = OUT / f"{name}.elf"
    write_elf64(elf, ENTRY, payload)
    return elf, len(words)


def run_sail(elf: Path, limit: int, out: Path) -> None:
    subprocess.run(
        [str(SAIL), "--config-override", str(CONFIG), "--inst-limit", str(limit),
         "--trace-instr", "--trace-gpr", "--trace-exception",
         "--trace-output", str(out), str(elf)],
        capture_output=True, text=True, check=False)


def run_spike(elf: Path, limit: int, out: Path) -> None:
    # Both log modes: `--log-commits` carries register writes, `-l` carries exceptions.
    subprocess.run(
        [str(SPIKE), "--isa=rv64i", "--priv=m", "-l", "--log-commits",
         f"--log={out}", f"--instructions={limit + SPIKE_RESET_STEPS}", str(elf)],
        capture_output=True, text=True, check=False)


def check_expected(name: str, trace: Path) -> None:
    spec = GUESTS / f"{name}.expected.toml"
    if not spec.is_file():
        return
    exp = tomllib.loads(spec.read_text())
    steps = align(parse_sail(trace.read_text()), ENTRY, "sail")
    if len(steps) != exp["instructions"]:
        say(False, f"{name}: step count", f"expected {exp['instructions']}, observed {len(steps)}")
        return
    bad = []
    for e in exp["step"]:
        got = dict(steps[e["n"]].writes)
        want = {k: int(v, 16) for k, v in (e.get("writes") or {}).items()}
        if got != want:
            bad.append(f"step {e['n']} ({e['insn']}): expected {want}, observed {got}")
    say(not bad, f"{name}: {len(exp['step'])} specification-derived expectations",
        "" if not bad else "; ".join(bad))


def experiment(name: str) -> None:
    print(f"\n== {name} ==")
    elf, n = build(name)
    say(True, f"{name}: assembled", f"{n} instruction(s), elf sha256 {sha256(elf)[:16]}…")

    sail_trace = OUT / f"{name}.sail.trace"
    run_sail(elf, n, sail_trace)
    spike_log = OUT / f"{name}.spike.log"
    run_spike(elf, n, spike_log)

    check_expected(name, sail_trace)

    try:
        a = align(parse_sail(sail_trace.read_text()), ENTRY, "sail")
        b = align(parse_spike(spike_log.read_text()), ENTRY, "spike")
        ok, report = compare(a, b, ("sail-riscv", "spike"))
    except CompareError as exc:
        ok, report = False, str(exc)
    say(ok, f"{name}: sail-riscv vs spike", report.splitlines()[0])
    if not ok:
        print("\n".join("      " + l for l in report.splitlines()[1:]))

    repeat = OUT / f"{name}.sail.rerun.trace"
    run_sail(elf, n, repeat)
    same = sha256(sail_trace) == sha256(repeat)
    say(same, f"{name}: reproduces", f"sha256 {sha256(sail_trace)[:16]}…")


def main() -> int:
    for tool in (SAIL, SPIKE, CONFIG):
        if not tool.exists():
            print(f"run_smoke: {tool} is missing — run scripts/fetch_references.sh first",
                  file=sys.stderr)
            return 2
    print(f"matched-profile experiment for {PROFILE}")
    for name in ("smoke-arith", "smoke-trap"):
        experiment(name)
    print()
    if failures:
        print(f"run_smoke: FAILED ({len(failures)} check(s)): {', '.join(failures)}",
              file=sys.stderr)
        return 1
    print("run_smoke: ok — both experiments agree across two models, match the "
          "specification-derived expectations, and reproduce")
    return 0


if __name__ == "__main__":
    sys.exit(main())
