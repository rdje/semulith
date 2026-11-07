#!/usr/bin/env python3
"""Measure a case's page-table reads on both producers, once, retained.

`REQ-D-WALK-IMPLICIT` says what a translated access reads and writes implicitly, and the matched comparison is of GPRs, so it
cannot see that: "a successful final load alone cannot establish the absence of an extra access". The pinned binary can show it
(`--trace-ptw`, `--trace-mem`), and the engine records each read crossing its boundary as its own kind (`--trace-walks`). This runs
the case's guest through both and retains the raw traces:

  profiles/<profile>/reference/<case-id>.walk.trace   the reference's, never edited
  profiles/<profile>/reference/<case-id>.walk.lab     the engine's, never edited
  profiles/<profile>/reference/<case-id>.walk.sexp    what ran, by digest (schema/config-effect.sexp)

The record carries no verdict: `compare` re-derives the result from the two traces on every read. What must hold: both read the
same PTEs with the same values, each read is 8 bytes, each walk reads at most 3, and nothing writes a PTE that was read, from the
first walk on. The order and the number of reads may differ, because TLB replacement is not architectural: measured on the corpus,
23 of 30 translating guests read in the same order, and in the other 7 the reference walks again for a page the engine still holds.
Existing names refuse reuse, so this measures exactly once, like a capture.

  python3 -B scripts/measure_walk_trace.py --case rv64gc-walk-implicit-v1

Exit: 0 retained; 1 the comparison does not hold, nothing retained; 2 refused, nothing retained.
"""
from __future__ import annotations

import argparse
import hashlib
from pathlib import Path
import re
import subprocess
import sys
import tempfile

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import dossier_sexp as D  # noqa: E402
import prepare_div_inputs as Prep  # noqa: E402
import records_sexp as R  # noqa: E402
import run_rv64gc_sail as Sail  # noqa: E402
import sexp as S  # noqa: E402

ROOT = HERE.parent
TIMEOUT_SECONDS = 120
TRACE_BYTES = 4 * 1024 * 1024
LEVELS = 3
PTE_BYTES = 8
STEP = re.compile(r"^PTW: Step, level=\d+, pte=0x([0-9A-Fa-f]+), pte_addr=0x([0-9A-Fa-f]+)$", re.M)
READ = re.compile(r"^mem\[R,0x([0-9A-Fa-f]+)\] -> 0x([0-9A-Fa-f]+)$", re.M)
WRITE = re.compile(r"^mem\[W,0x([0-9A-Fa-f]+)\] <- ", re.M)
ENGINE = re.compile(r"^ptw\[0x([0-9a-f]+)\] -> 0x([0-9a-f]+)$", re.M)


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def walk_paths(root: Path, case_id: str) -> tuple[Path, Path, Path]:
    directory = root / "profiles" / Prep.PROFILE / "reference"
    return directory / (case_id + ".walk.sexp"), directory / (case_id + ".walk.trace"), directory / (case_id + ".walk.lab")


def compare(reference: str, engine: str) -> tuple[bool, str]:
    """(holds, what it found), from the two raw traces alone."""
    steps = [(int(a, 16), int(v, 16)) for v, a in STEP.findall(reference)]
    if not steps:
        return False, "the reference's trace shows no walk"
    theirs = {(int(a, 16), int(v, 16)) for a, v in ENGINE.findall(engine)}
    ours = set(steps)
    if ours != theirs:
        return False, f"the two read different PTEs: {len(ours - theirs)} only on the reference, {len(theirs - ours)} only on the engine"
    addresses = {a for a, _ in steps}
    widths = {int(a, 16): len(v) // 2 for a, v in READ.findall(reference) if int(a, 16) in addresses}
    narrow = sorted(a for a, width in widths.items() if width != PTE_BYTES)
    if narrow or set(widths) != addresses:
        return False, f"a page-table read is not {PTE_BYTES} bytes: {[hex(a) for a in narrow] or 'no memory row for one'}"
    walks = [len(STEP.findall(block)) for block in re.split(r"^PTW: (?:Success|Fail)[^\n]*$", reference, flags=re.M)]
    if max(walks) > LEVELS:
        return False, f"a walk read {max(walks)} PTEs, above {LEVELS}"
    written = sorted({int(a, 16) for a in WRITE.findall(reference[reference.index("PTW: "):])} & addresses)
    if written:
        return False, f"a PTE was written from the first walk on: {[hex(a) for a in written]}"
    order = "in the same order" if steps == [(int(a, 16), int(v, 16)) for a, v in ENGINE.findall(engine)] else "in a different order, which TLB replacement allows"
    return True, (f"{len(ours)} distinct PTEs read on both with the same values, {order}; each read {PTE_BYTES} bytes, "
                  f"at most {max(walks)} per walk, and no PTE written from the first walk on")


def record_text(case_id: str, *, binary: str, guest: str, case_config: str, instructions: int, reference: bytes, engine: bytes) -> str:
    form = [S.Symbol("walk_trace"), [S.Symbol("case_id"), case_id], [S.Symbol("binary_sha256"), binary],
            [S.Symbol("guest_sha256"), guest], [S.Symbol("case_config_sha256"), case_config], [S.Symbol("instructions"), instructions],
            [S.Symbol("reference_trace_sha256"), sha(reference)], [S.Symbol("engine_trace_sha256"), sha(engine)]]
    return (f";; {case_id}.walk.sexp — what ran to compare this case's page-table reads (schema/config-effect.sexp).\n"
            ";; Written by scripts/measure_walk_trace.py beside its raw traces; it carries no verdict, the policy review re-derives it.\n"
            + R.render_forms([form]))


def engine_command(root: Path, guest: Path, instructions: int) -> list[str]:
    return ["cargo", "run", "-q", "-p", "semulith-cli", "--", "run", str(guest), "--profile=rv64gc-lab-v0",
            f"--steps={instructions}", "--trace-walks"]


def measure(root: Path, case_id: str, binary: Path, engine=None) -> tuple[int, str]:
    """Run once and retain, or refuse with nothing written. The caller supplies the authenticated binary."""
    case_dir = root / "evidence" / case_id
    paths = walk_paths(root, case_id)
    if any(path.exists() for path in paths):
        return 2, f"REFUSED: {case_id}'s walk trace is already retained; existing names refuse reuse"
    guest, config = case_dir / "guest.elf", case_dir / "reference-config.json"
    expected = D.load_expectations(case_dir / "baseline.expected.sexp")
    instructions = expected["instructions"]
    scratch = root / "target" / "tmp"
    scratch.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(dir=scratch) as td:
        trace = Path(td) / "walk.trace"
        process = subprocess.run([str(binary), "--config-override", str(config), "--inst-limit", str(instructions), "--trace-instr",
                                  "--trace-ptw", "--trace-mem", "--trace-output", str(trace), str(guest)],
                                 capture_output=True, text=True, timeout=TIMEOUT_SECONDS, check=False)
        if process.returncode != 0 or not trace.is_file():
            return 2, f"REFUSED: the reference process failed: rc={process.returncode}"
        reference = trace.read_bytes()
    command = engine or engine_command(root, guest, instructions)
    done = subprocess.run(command, capture_output=True, timeout=TIMEOUT_SECONDS, cwd=root, check=False)
    if done.returncode != 0:
        return 2, f"REFUSED: the engine process failed: rc={done.returncode}"
    lab = b"".join(line + b"\n" for line in done.stdout.splitlines() if line.startswith(b"ptw["))
    if len(reference) > TRACE_BYTES or len(lab) > TRACE_BYTES:
        return 2, f"REFUSED: a trace is above {TRACE_BYTES} bytes"
    held, detail = compare(reference.decode("utf-8"), lab.decode("utf-8"))
    if not held:
        return 1, f"{case_id}: {detail}"
    record_path, trace_path, lab_path = paths
    text = record_text(case_id, binary=sha(binary.read_bytes()), guest=sha(guest.read_bytes()), case_config=sha(config.read_bytes()),
                       instructions=instructions, reference=reference, engine=lab)
    with trace_path.open("xb") as stream:
        stream.write(reference)
    with lab_path.open("xb") as stream:
        stream.write(lab)
    with record_path.open("x", encoding="utf-8") as stream:
        stream.write(text)
    return 0, detail


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--case", required=True)
    args = parser.parse_args(argv)
    code, message = measure(ROOT, args.case, Sail.reference_binary())
    print(message, file=sys.stderr if code else sys.stdout)
    return code


if __name__ == "__main__":
    sys.exit(main())
