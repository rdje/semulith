#!/usr/bin/env python3
"""Run the P1-LAB.8 first-execution-slice experiment: semulith vs the references.

One command that: assembles the tracked guest sources (and compiles the tracked `.c`
guest with the pinned toolchain — `scripts/build_c_guest.sh`, its ELF a build artifact
with the same standing as the reference binaries), runs them on SEMULITH's definitional
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
from compare_traces import (align, compare, check_expected_divergence, parse_sail,
                            parse_semulith, parse_spike, CompareError)
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
C_GUEST_BUDGET = 1_000_000
failures: list[str] = []


def say(ok: bool, label: str, detail: str = "") -> None:
    print(f"  {'PASS' if ok else 'FAIL'}  {label}{('  ' + detail) if detail else ''}")
    if not ok:
        failures.append(label)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def build(name: str) -> tuple[Path, int | None]:
    c_src = GUESTS / f"{name}.c"
    if c_src.is_file():
        # The compiled guest: the pinned toolchain builds the ELF (a build
        # artifact with the same standing as the reference binaries); the
        # instruction count is a fact of the compiled artifact, not of a source
        # listing, so None — the caller learns the executed count by running.
        proc = subprocess.run([str(ROOT / "scripts/build_c_guest.sh"), name],
                              capture_output=True, text=True, check=False)
        if proc.returncode != 0:
            print(f"  build_c_guest failed (rc={proc.returncode}):\n{proc.stderr}",
                  file=sys.stderr)
            raise SystemExit(2)
        return OUT / f"{name}.elf", None
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


def elf_entry(elf: Path) -> int:
    """The ELF64 header's e_entry — where a compiled image actually starts (the
    declared ENTRY constant is the assembled guests' image base, and a linked
    ELF's headers and literal pools legitimately precede its first instruction)."""
    return int.from_bytes(elf.read_bytes()[24:32], "little")


def experiment(name: str) -> None:
    print(f"\n== {name} ==")
    elf, assembled = build(name)
    entry = ENTRY if assembled is not None else elf_entry(elf)
    semulith_trace = OUT / f"{name}.semulith.trace"
    if assembled is None:
        # Compiled guest: run with a generous budget — the closing ebreak stops
        # the run long before it — and take the executed count from the trace.
        run_semulith(elf, C_GUEST_BUDGET, semulith_trace)
        ours = align(parse_semulith(semulith_trace.read_text()), entry, "semulith")
        n = len(ours)
        say(n < C_GUEST_BUDGET, f"{name}: compiled, retired inside the budget",
            f"{n} executed step(s), entry {entry:#x}, elf sha256 {sha256(elf)[:16]}…")
    else:
        n = executed_steps(name, assembled)
        say(True, f"{name}: assembled",
            f"{assembled} instruction(s), {n} executed step(s), elf sha256 {sha256(elf)[:16]}…")
        run_semulith(elf, n, semulith_trace)
        ours = align(parse_semulith(semulith_trace.read_text()), entry, "semulith")

    spec = GUESTS / f"{name}.expected.sexp"
    exp = D.load_expectations(spec) if spec.is_file() else None
    div = (exp or {}).get("expect_divergence")

    # The references' run length. An expected-divergence guest is straight-line by
    # construction: the references retire the WHOLE program (semulith stops at the declared
    # divergence), plus the one measured run-off-the-end step both references take
    # identically (the zero word past the payload raises illegal-instruction on each) — so
    # the reference-vs-reference control below compares full traces, never a prefix.
    ref_n = n if div is None else assembled + 1

    sail_trace = OUT / f"{name}.sail.trace"
    run_sail(elf, ref_n, sail_trace)
    sail = align(parse_sail(sail_trace.read_text()), entry, "sail")

    check_expected(name, ours, "semulith run")

    cross = True
    if exp is not None:
        cross = exp.get("cross_model", True)
    spike = None
    if cross or div is not None:
        spike_log = OUT / f"{name}.spike.log"
        run_spike(elf, ref_n, spike_log)
        spike = align(parse_spike(spike_log.read_text()), entry, "spike")
    if not cross and div is None:
        print(f"  SKIP  {name}: sail-riscv vs spike  "
              f"disabled — see difference DIFF-PLATFORM-SPIKE in references.sexp")

    if div is not None:
        expected_divergence(name, div, ours, sail, spike)
    else:
        pairs = [("sail-riscv", sail)] + ([("spike", spike)] if cross else [])
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


def expected_divergence(name: str, div: dict, ours, sail, spike) -> None:
    """The four-step protocol for a guest whose expectations declare `expect_divergence`
    (P2-SCALAR.4): the comparison is not DISABLED (`cross_model` stays what it is) — it is
    a comparison that must FAIL in exactly one declared way.

    (a) semulith matches its own specification-derived expectations — already checked by
        `check_expected` in `experiment`, like every other guest;
    (b) compare(semulith, each reference) reports FIRST DIVERGENCE at exactly `at_step`,
        with semulith's step carrying the policy trap;
    (c) sail vs spike AGREE over their full length — the references stay each other's
        control, so the divergence is attributable to the declared difference alone;
    (d) the difference id exists in references.sexp (also commit-gated: the
        INTERACTION-MATRIX doctrine re-checks it against the declared matrix).
    """
    diff_id, at_step = div["difference"], div["at_step"]
    for model_name, theirs in (("sail-riscv", sail), ("spike", spike)):
        ok, report = check_expected_divergence(ours, theirs, at_step, diff_id,
                                               ("semulith", model_name))
        if ok and ours[at_step].trap is None:
            ok, report = False, (f"{diff_id}: semulith's step {at_step} carries NO trap — "
                                 f"the declared divergence is the policy trap; something "
                                 f"else diverged")
        say(ok, f"{name}: semulith vs {model_name} — expected divergence",
            report.splitlines()[0])
        if not ok:
            print("\n".join("      " + l for l in report.splitlines()[1:]))
    try:
        ok, report = compare(sail, spike, ("sail-riscv", "spike"))
    except CompareError as exc:
        ok, report = False, str(exc)
    say(ok, f"{name}: sail-riscv vs spike — the references stay each other's control",
        report.splitlines()[0])
    if not ok:
        print("\n".join("      " + l for l in report.splitlines()[1:]))
    known = {d["id"] for d in
             D.load_references(ROOT / f"profiles/{PROFILE}/references.sexp")
             .get("difference", [])}
    say(diff_id in known, f"{name}: difference {diff_id} is recorded in references.sexp")


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
                 "c-scope",
                 "bound-shift", "bound-shiftw", "bound-arith", "bound-ext", "bound-alias",
                 "fault-jal-mis", "fault-jalr-mis", "fault-branch-nt", "fault-fetch",
                 "fault-ld-mis-h", "fault-ld-mis-d", "fault-st-mis-h", "fault-st-mis-w",
                 "fault-st-mis-d", "fault-ld-x0-mis", "fault-ld-x0-fault", "fault-access-ld",
                 "fault-access-sd", "fault-reserved", "fault-shiftw-res", "fault-fence",
                 "fault-hints", "fault-selfmod",
                 "it-prio-jump", "it-prio-load", "it-fault-alias", "it-fault-wrap-ld",
                 "it-fault-wrap-sd", "it-alias-bound", "it-progress-loop", "it-fencei"):
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
