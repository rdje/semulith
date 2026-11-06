#!/usr/bin/env python3
"""Measure what a case's reference configuration does: the case's guest under another configuration, once, retained.

The policy's `implementation-defined` row asks for a "pinned matching reference configuration with a behavior-changing control" and
calls "a configuration file without an observed effect" insufficient. A case's capture observes only its own configuration, so this
tool runs the same guest through the same pinned binary under the alternative the case declares (`<case-id>.alternative.sexp`), or
under the profile override when it declares none, and retains the raw trace beside the case's configuration:

  profiles/<profile>/reference/<case-id>.effect.trace   the reference's raw trace, never edited
  profiles/<profile>/reference/<case-id>.effect.sexp    what ran: the binary, the guest and both configurations, by digest (schema/config-effect.sexp)

The record carries no verdict. The policy review re-derives the first difference offline from the retained trace and the case's own
baseline expectation, on every read. Existing names refuse reuse, so this measures exactly once, like a capture. It needs the untracked
reference binary; it grants no credit. A run that does not differ retains nothing: that configuration has no observed effect here.

  python3 -B scripts/measure_config_effect.py --case rv64gc-csr-set-v3

Exit: 0 retained; 1 the run does not differ, nothing retained; 2 refused, nothing run or retained.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))
import dossier_sexp as D  # noqa: E402
import prepare_div_inputs as Prep  # noqa: E402
import records_sexp as R  # noqa: E402
import run_rv64gc_sail as Sail  # noqa: E402
import sexp as S  # noqa: E402

ROOT = HERE.parent
TIMEOUT_SECONDS = 120
REFUSALS = (Prep.CurationRefused, Prep.K.SchemaError, S.SexpError)
TRACE_BYTES = 4 * 1024 * 1024  # the collector's bound on a trace


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def effect_paths(root: Path, case_id: str) -> tuple[Path, Path]:
    """The record and the raw trace, beside the case's overlay."""
    directory = root / "profiles" / Prep.PROFILE / "reference"
    return directory / (case_id + ".effect.sexp"), directory / (case_id + ".effect.trace")


def profile_config(root: Path) -> bytes:
    """The profile override's configuration, rendered as `prepare_div_inputs` renders every case's."""
    config = Prep.map_document(root, Prep.read_bounded(root / Prep.OVERRIDE), "override", D.override_to_doc)
    return (json.dumps(config, indent=2) + "\n").encode("utf-8")


def alternative_config(root: Path, case_id: str) -> tuple[bytes, str]:
    """What the case's configuration is compared with, and its name: the alternative it declares, else the profile override."""
    declared = Prep.alternative_config(root, case_id)
    if declared is None:
        return profile_config(root), "the profile override"
    return (json.dumps(declared, indent=2) + "\n").encode("utf-8"), "its declared alternative"


def record_text(case_id: str, *, binary: str, guest: str, case_config: str, alternative: str, instructions: int, trace: bytes) -> str:
    form = [S.Symbol("config_effect"), [S.Symbol("case_id"), case_id], [S.Symbol("binary_sha256"), binary],
            [S.Symbol("guest_sha256"), guest], [S.Symbol("case_config_sha256"), case_config],
            [S.Symbol("alternative_config_sha256"), alternative], [S.Symbol("instructions"), instructions],
            [S.Symbol("trace_sha256"), sha(trace)], [S.Symbol("trace_bytes"), len(trace)]]
    return (f";; {case_id}.effect.sexp — what ran to observe this case's reference configuration (schema/config-effect.sexp).\n"
            ";; Written by scripts/measure_config_effect.py beside its raw trace; it carries no verdict, the policy review re-derives it.\n"
            + R.render_forms([form]))


def measure(root: Path, case_id: str, binary: Path) -> tuple[int, str]:
    """Run once and retain, or refuse with nothing written. The caller supplies the authenticated binary."""
    case_dir = root / "evidence" / case_id
    record_path, trace_path = effect_paths(root, case_id)
    if record_path.exists() or trace_path.exists():
        return 2, f"REFUSED: {case_id}'s configuration effect is already retained; existing names refuse reuse"
    guest, case_config = case_dir / "guest.elf", case_dir / "reference-config.json"
    expected = D.load_expectations(case_dir / "baseline.expected.sexp")
    try:
        alternative, named = alternative_config(root, case_id)
    except REFUSALS as refused:
        return 2, f"REFUSED: {case_id}'s declared alternative: {refused}"
    if sha(alternative) == sha(case_config.read_bytes()):
        return 2, f"REFUSED: {case_id} has no configuration of its own to measure"
    scratch = root / "target" / "tmp"
    scratch.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(dir=scratch) as td:
        config, trace = Path(td) / "alternative.json", Path(td) / "effect.trace"
        config.write_bytes(alternative)
        process = subprocess.run([str(binary), "--config-override", str(config), "--inst-limit", str(expected["instructions"]),
                                  "--trace-instr", "--trace-gpr", "--trace-exception", "--trace-output", str(trace), str(guest)],
                                 capture_output=True, text=True, timeout=TIMEOUT_SECONDS, check=False)
        if process.returncode != 0 or not trace.is_file():
            return 2, f"REFUSED: the reference process failed: rc={process.returncode}"
        data = trace.read_bytes()
    if len(data) > TRACE_BYTES:
        return 2, f"REFUSED: the trace holds {len(data)} bytes, above {TRACE_BYTES}"
    result = Sail.compare_observations(expected, data.decode("utf-8"), process.returncode)
    if result.verdict != "DIVERGE":
        return 1, f"{case_id}'s guest reads {result.verdict} under {named}: this configuration has no observed effect here"
    text = record_text(case_id, binary=sha(binary.read_bytes()), guest=sha(guest.read_bytes()), case_config=sha(case_config.read_bytes()),
                       alternative=sha(alternative), instructions=expected["instructions"], trace=data)
    with trace_path.open("xb") as stream:
        stream.write(data)
    with record_path.open("x", encoding="utf-8") as stream:
        stream.write(text)
    return 0, result.detail


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--case", required=True)
    args = parser.parse_args(argv)
    code, message = measure(ROOT, args.case, Sail.reference_binary())
    print(message, file=sys.stderr if code else sys.stdout)
    return code


if __name__ == "__main__":
    sys.exit(main())
