#!/usr/bin/env python3
"""Which guests agree with the pinned reference under the profile override, and under one case's configuration?

Every guest of the run order goes through the pinned Sail binary twice, once per configuration, and each run gets the one
verdict `run_rv64gc_sail.compare_trace` gives it: AGREE, DIVERGE, or REFUSED when the evidence is absent or malformed. The
case's configuration is the one `prepare_div_inputs.reference_config` renders, so this measures what the case would pin.

This is a live experiment and not CI: it needs the untracked reference binary. It compares declared GPR changes only, grants no
credit, and says what a configuration changes across the corpus before a case is declared on it (decision_reference-config-per-case.md).

  python3 -B scripts/census_reference_config.py --case rv64gc-csr-set-v4
  python3 -B scripts/census_reference_config.py --case rv64gc-svade-v2 --alternative   # the case's own against what it declares

Writes only under --out (default target/reference-config-census/<case>), and reads the tracked guests.
"""
from __future__ import annotations

import argparse
from collections import Counter
import json
from pathlib import Path
import subprocess
import sys

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))
import dossier_sexp as D  # noqa: E402
import prepare_div_inputs as Prep  # noqa: E402
from riscv_asm import Assembler, write_elf64  # noqa: E402
import run_rv64gc_sail as Sail  # noqa: E402

ROOT = HERE.parent
UNIT = ROOT / "profiles" / Prep.PROFILE
GUESTS = UNIT / "guests"
TIMEOUT_SECONDS = 120


def run_order() -> list[str]:
    lines = (GUESTS / "run-order.txt").read_text().splitlines()
    return [line.split("#")[0].strip().removesuffix(".s") for line in lines if line.split("#")[0].strip()]


def verdict(binary: Path, config: Path, elf: Path, trace: Path, expected: dict) -> dict:
    """One guest under one configuration; a stale trace cannot answer for this run."""
    trace.unlink(missing_ok=True)
    process = subprocess.run([str(binary), "--config-override", str(config), "--inst-limit", str(expected["instructions"]),
                              "--trace-instr", "--trace-gpr", "--trace-exception", "--trace-output", str(trace), str(elf)],
                             capture_output=True, text=True, timeout=TIMEOUT_SECONDS, check=False)
    try:
        if not trace.is_file():
            raise Sail.SailError(f"no trace: rc={process.returncode}")
        outcome, detail = Sail.compare_trace(expected, trace.read_text(), process.returncode)
    except Sail.SailError as error:
        outcome, detail = "REFUSED", str(error)
    return dict(verdict=outcome, detail=detail)


def configurations(case_id: str, alternative: bool) -> dict:
    """The two configurations compared, in report order and named for the report."""
    case = Prep.reference_config(ROOT, case_id)
    if alternative:
        declared = Prep.alternative_config(ROOT, case_id)
        if declared is None:
            raise Prep.CurationRefused(f"{case_id} declares no alternative")
        return {"case": case, "alternative": declared}
    return {"profile": Prep.map_document(ROOT, Prep.read_bounded(ROOT / Prep.OVERRIDE), "override", D.override_to_doc), "case": case}


def census(configs: dict, out: Path, binary: Path) -> list[dict]:
    out.mkdir(parents=True, exist_ok=True)
    for name, config in configs.items():
        (out / f"{name}.json").write_text(json.dumps(config, indent=2) + "\n")
    assembler = Assembler(UNIT / "encoding.sexp")
    rows = []
    for name in run_order():
        expected = D.load_expectations(GUESTS / f"{name}.expected.sexp")
        if not expected.get("cross_model", True):
            rows.append(dict(guest=name, **{config: dict(verdict="NOT-COMPARED", detail="cross-model comparison disabled by its record") for config in configs}))
            continue
        entry = int(expected["entry"], 16)
        elf = out / f"{name}.elf"
        write_elf64(elf, entry, assembler.assemble_image((GUESTS / f"{name}.s").read_text().splitlines(), base=entry), assembler.ialign)
        rows.append(dict(guest=name, **{config: verdict(binary, out / f"{config}.json", elf, out / f"{name}.{config}.trace", expected)
                                        for config in configs}))
    return rows


def report(rows: list[dict], first: str = "profile", second: str = "case") -> str:
    moved = Counter((row[first]["verdict"], row[second]["verdict"]) for row in rows)
    lines = [f"{len(rows)} guests"]
    lines += [f"{count:4d}  {first} {before} -> {second} {after}" for (before, after), count in moved.most_common()]
    lines += [f"{row['guest']:<22}{row[first]['verdict']:<9}-> {row[second]['verdict']:<9}| {row[second]['detail'][:80]}"
              for row in rows if row[first]["verdict"] != row[second]["verdict"]]
    return "\n".join(lines) + "\n"


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--case", required=True, help="the case whose configuration to compare with the profile override")
    parser.add_argument("--alternative", action="store_true", help="compare the case's configuration with the alternative it declares")
    parser.add_argument("--out", type=Path, help="working directory, default target/reference-config-census/<case>")
    args = parser.parse_args(argv)
    out = args.out or ROOT / "target" / "reference-config-census" / args.case
    try:
        configs = configurations(args.case, args.alternative)
    except Prep.CurationRefused as refused:
        print(f"REFUSED: {refused}", file=sys.stderr)
        return 2
    rows = census(configs, out, Sail.reference_binary())
    (out / "census.json").write_text(json.dumps(rows, indent=1) + "\n")
    text = report(rows, *configs)
    (out / "census.txt").write_text(text)
    sys.stdout.write(text)
    return 0


if __name__ == "__main__":
    sys.exit(main())
