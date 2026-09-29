#!/usr/bin/env python3
"""Run the P1-LAB.8 first-execution-slice experiment: semulith vs the references.

One command that: assembles the tracked guest sources, runs them on SEMULITH's definitional
interpreter (`semulith run`, the P1-LAB.8 deliverable) and on the pinned reference models
configured to `rv64i-lab-v0`, compares the observation traces for FIRST divergence through
the one normalized vocabulary, checks semulith's trace against expectations DERIVED FROM
THE SPECIFICATION rather than from any model, and re-runs to confirm the result reproduces.

⛔ NOT A COMMIT GATE. It needs the reference binaries under `target/refs/`, which are
untracked and acquired by `scripts/fetch_references.sh` — the same standing as
`run_smoke.py`. The commit gate is the verify-side offline differential: the generated
guest fixture (GUEST-GEN) re-runs these same guests against the same specification-derived
expectations on every `make check`, no reference binaries needed.

⚠️ WHAT A PASS MEANS, exactly: for THESE inputs, semulith and the reference models agreed
with each other and with values derived from the specification, and the run reproduced.
`docs/EVIDENCE_AND_GATES.md` is explicit that finite differential testing is tested
evidence, never universal proof — and two models that share semantic ancestry can agree
while both being wrong (EVD-04; the independence inventory in `references.sexp` is the
separate record).
"""

from __future__ import annotations

import hashlib
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from compare_traces import (align, compare, parse_sail, parse_semulith, parse_spike,
                            CompareError)
from riscv_asm import Assembler, write_elf64
import dossier_sexp as D

ROOT = Path(subprocess.run(["git", "rev-parse", "--show-toplevel"],
                           capture_output=True, text=True, check=True).stdout.strip())
PROFILE = "rv64i-lab-v0"
ENTRY = 0x80000000
SAIL = ROOT / "target/refs/sail-riscv-Mac-arm64/bin/sail_riscv_sim"
SPIKE = ROOT / "target/refs/spike-build/spike"
OVERRIDE_SEXP = ROOT / f"profiles/{PROFILE}/reference/sail-{PROFILE}.override.sexp"
GUESTS = ROOT / f"profiles/{PROFILE}/guests"
OUT = ROOT / "target/refs/guests"

SPIKE_RESET_STEPS = 5
failures: list[str] = []


def say(ok: bool, label: str, detail: str = "") -> None:
    print(f"  {'PASS' if ok else 'FAIL'}  {label}{('  ' + detail) if detail else ''}")
    if not ok:
        failures.append(label)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def build(name: str) -> tuple[Path, int]:
    asm = Assembler(ROOT / f"profiles/{PROFILE}/encoding.sexp")
    words = asm.assemble((GUESTS / f"{name}.s").read_text().splitlines())
    payload = b"".join(w.to_bytes(4, "little") for w, _ in words)
    OUT.mkdir(parents=True, exist_ok=True)
    elf = OUT / f"{name}.elf"
    write_elf64(elf, ENTRY, payload)
    return elf, len(words)


def config() -> Path:
    return D.materialize_sail_override(ROOT, PROFILE)


def run_sail(elf: Path, limit: int, out: Path) -> None:
    subprocess.run(
        [str(SAIL), "--config-override", str(config()), "--inst-limit", str(limit),
         "--trace-instr", "--trace-gpr", "--trace-exception",
         "--trace-output", str(out), str(elf)],
        capture_output=True, text=True, check=False)


def run_spike(elf: Path, limit: int, out: Path) -> None:
    subprocess.run(
        [str(SPIKE), "--isa=rv64i", "--priv=m", "-l", "--log-commits",
         f"--log={out}", f"--instructions={limit + SPIKE_RESET_STEPS}", str(elf)],
        capture_output=True, text=True, check=False)


def run_semulith(elf: Path, limit: int, out: Path) -> None:
    proc = subprocess.run(
        ["cargo", "run", "--quiet", "-p", "semulith-cli", "--",
         "run", str(elf), f"--steps={limit}"],
        capture_output=True, text=True, check=False)
    if proc.returncode != 0:
        print(f"  semulith run failed (rc={proc.returncode}):\n{proc.stderr}", file=sys.stderr)
    out.write_text(proc.stdout)


def check_expected(name: str, steps, parsed_by: str) -> None:
    """The specification-derived expectations checked against SEMULITH's own trace."""
    spec = GUESTS / f"{name}.expected.sexp"
    if not spec.is_file():
        return
    exp = D.load_expectations(spec)
    if len(steps) != exp["instructions"]:
        say(False, f"{name}: semulith step count",
            f"expected {exp['instructions']}, observed {len(steps)} (parsed by {parsed_by})")
        return
    bad = []
    for e in exp["step"]:
        got = dict(steps[e["n"]].writes)
        want = {k: int(v, 16) for k, v in (e.get("writes") or {}).items()}
        if got != want:
            bad.append(f"step {e['n']} ({e['insn']}): expected {want}, observed {got}")
    say(not bad, f"{name}: semulith vs {len(exp['step'])} specification-derived expectations",
        "" if not bad else "; ".join(bad))
    never = exp.get("never_written") or []
    if never:
        written = {reg for st in steps for reg, _ in st.writes}
        violated = sorted(set(never) & written)
        say(not violated, f"{name}: semulith — {len(never)} register(s) that must never be written",
            "" if not violated else f"but {violated} were written")


def executed_steps(name: str, assembled: int) -> int:
    spec = GUESTS / f"{name}.expected.sexp"
    if spec.is_file():
        return D.load_expectations(spec)["instructions"]
    return assembled


def experiment(name: str) -> None:
    print(f"\n== {name} ==")
    elf, assembled = build(name)
    n = executed_steps(name, assembled)
    say(True, f"{name}: assembled",
        f"{assembled} instruction(s), {n} executed step(s), elf sha256 {sha256(elf)[:16]}…")

    semulith_trace = OUT / f"{name}.semulith.trace"
    run_semulith(elf, n, semulith_trace)
    ours = align(parse_semulith(semulith_trace.read_text()), ENTRY, "semulith")

    sail_trace = OUT / f"{name}.sail.trace"
    run_sail(elf, n, sail_trace)
    sail = align(parse_sail(sail_trace.read_text()), ENTRY, "sail")

    check_expected(name, ours, "semulith run")

    spec = GUESTS / f"{name}.expected.sexp"
    cross = True
    if spec.is_file():
        cross = D.load_expectations(spec).get("cross_model", True)
    pairs = [("sail-riscv", sail)]
    if cross:
        spike_log = OUT / f"{name}.spike.log"
        run_spike(elf, n, spike_log)
        pairs.append(("spike", align(parse_spike(spike_log.read_text()), ENTRY, "spike")))
    else:
        print(f"  SKIP  {name}: sail-riscv vs spike  "
              f"disabled — see difference DIFF-PLATFORM-SPIKE in references.sexp")
    for model_name, theirs in pairs:
        try:
            ok, report = compare(ours, theirs, ("semulith", model_name))
        except CompareError as exc:
            ok, report = False, str(exc)
        say(ok, f"{name}: semulith vs {model_name}", report.splitlines()[0])
        if not ok:
            print("\n".join("      " + l for l in report.splitlines()[1:]))

    repeat = OUT / f"{name}.semulith.rerun.trace"
    run_semulith(elf, n, repeat)
    same = sha256(semulith_trace) == sha256(repeat)
    say(same, f"{name}: semulith reproduces", f"sha256 {sha256(semulith_trace)[:16]}…")


def main() -> int:
    for tool in (SAIL, OVERRIDE_SEXP):
        if not tool.exists():
            print(f"run_semulith_smoke: {tool} is missing — the tracked override or a "
                  f"reference binary is absent (binaries come from "
                  f"scripts/fetch_references.sh)", file=sys.stderr)
            return 2
    if not SPIKE.exists():
        print("run_semulith_smoke: spike is missing — fetch it with "
              "scripts/fetch_references.sh (the semulith-vs-sail comparisons still run)",
              file=sys.stderr)
    print(f"the P1-LAB.8 first-execution-slice experiment for {PROFILE}")
    for name in ("smoke-arith", "guest-control", "smoke-trap", "guest-no-device",
                 "scope-alu", "scope-mem", "scope-branch", "scope-ecall", "scope-ebreak",
                 "bound-shift", "bound-shiftw", "bound-arith", "bound-ext", "bound-alias"):
        experiment(name)
    print()
    if failures:
        print(f"run_semulith_smoke: FAILED ({len(failures)} check(s)): {', '.join(failures)}",
              file=sys.stderr)
        return 1
    print("run_semulith_smoke: ok — semulith matches the specification-derived expectations "
          "and reproduces; every cross-model comparison that is enabled agrees")
    return 0


if __name__ == "__main__":
    sys.exit(main())
