#!/usr/bin/env python3
"""Curate or verify the four prepared inputs of a reviewed finite case; no reference process.

The prepared inputs are reproducible interoperability artifacts built from canonical sources
through the public owners: the guest ELF (`matched_gpr_image.build_guest_image` over the case's
guest source at the fixed cold entry), the reference configuration (the profile override,
validated against its schema, mapped by the dossier owner and rendered as the
`materialize_sail_override` route renders it), the baseline expectation (a byte-exact copy of
the canonical expectation file beside the guest) and the control expectation (the baseline with
exactly the control property's value replaced by the case's wrong value, under a structured
comment that names the change). Every artifact is checked through the public source/image and
source-value owners before it is reported.

  --show    derive the four artifacts and print their sizes and digests (no file is written)
  --verify  derive them and compare with the retained bytes under evidence/<case>/
  --write   create the four files under evidence/<case>/, refusing any that already exists

The tool launches no process, opens no acquired material and grants no capture, policy or
qualification credit. Retained bytes are never replaced: a changed input needs a new case.
"""
from __future__ import annotations

import argparse
from copy import deepcopy
from dataclasses import dataclass
import hashlib
import json
import os
from pathlib import Path
import sys

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))
import check_sexp_schema as K  # noqa: E402
import dossier_sexp as D  # noqa: E402
import matched_gpr_comparison as C  # noqa: E402
import matched_gpr_image as G  # noqa: E402
import matched_gpr_property as P  # noqa: E402
import matched_gpr_source_image as B  # noqa: E402
import records_sexp as R  # noqa: E402
import sexp as S  # noqa: E402

ROOT = HERE.parent
PROFILE = "rv64gc-lab-v0"
GUESTS = "profiles/" + PROFILE + "/guests"
OVERRIDE = "profiles/" + PROFILE + "/reference/sail-" + PROFILE + ".override.sexp"
ENTRY = 0x80000000
INPUT_BYTES = 65536
NAMES = ("guest.elf", "reference-config.json", "baseline.expected.sexp", "control.expected.sexp")
ROLES = dict(zip(NAMES, ("guest-image", "reference-config", "expectation", "expectation")))


class CurationRefused(ValueError):
    """The canonical sources cannot be curated into the case's prepared inputs."""


@dataclass(frozen=True)
class PreparedInput:
    name: str
    role: str
    byte_size: int
    sha256: str
    payload: bytes


def _require(condition, reason: str) -> None:
    if not condition:
        raise CurationRefused(reason)


def _signed(value: int) -> int:
    return value - (1 << 64) if value >> 63 else value


def read_bounded(path: Path) -> bytes:
    with path.open("rb") as stream:
        payload = stream.read(INPUT_BYTES + 1)
    _require(1 <= len(payload) <= INPUT_BYTES, f"{path.name} outside 1..{INPUT_BYTES} bytes")
    return payload


def map_document(root: Path, payload: bytes, kind: str, mapper):
    """Raw schema validation, then the sole canonical mapper; a diagnostic read, not a loader."""
    text = payload.decode("utf-8")
    constructs, operators = K.load_schema(root / "schema" / (kind + ".sexp"))
    issues = K.validate_text(text, constructs, operators, kind)
    _require(not issues, f"{kind}: {issues[0] if issues else ''}")
    forms = [form for form in S.parse(text, kind) if form[0] != "comment"]
    _require(len(forms) == 1 and forms[0][0] == kind, f"expected exactly one {kind} document")
    return mapper(forms[0])


def control_note(case: P.ReviewedPropertyCase) -> str:
    control = case.control()
    return (
        f"Deliberately incorrect negative control: only boundary {control.witness.step_n} "
        f"{control.witness.register} changes from {_signed(control.expected_value)} to "
        f"{_signed(case.control_value)}. Baseline derivation text is retained to show why the "
        "value is wrong; no execution evidence."
    )


def curate(root: Path, case: P.ReviewedPropertyCase) -> tuple[PreparedInput, ...]:
    """Derive the four prepared inputs from canonical sources and check them through public owners."""
    source = read_bounded(root / GUESTS / case.program)
    _require(
        len(source) == case.source_size
        and hashlib.sha256(source).hexdigest() == case.source_sha256,
        "guest source differs from the reviewed case",
    )
    baseline = read_bounded(root / GUESTS / (Path(case.program).stem + ".expected.sexp"))
    expected = map_document(root, baseline, "expectations", D.expectations_to_doc)
    _require(
        expected["program"] == case.program and expected["instructions"] == case.instructions,
        "canonical expectation differs from the reviewed case",
    )
    override = map_document(root, read_bounded(root / OVERRIDE), "override", D.override_to_doc)
    control = case.control()
    values = C.compare_source_expectation(
        source=source, baseline_expectation=baseline, instructions=case.instructions,
        program=case.program, witness=control.witness)
    _require(
        values.disposition == "matched" and values.facts.witness_value == control.expected_value,
        "source values do not match the canonical expectation: " + values.reason,
    )
    changed = deepcopy(expected)
    step = changed["step"][control.witness.step_n]
    _require(step["writes"].get(control.witness.register) == f"0x{control.expected_value:016x}",
             "control witness is not the reviewed value in the canonical expectation")
    step["writes"][control.witness.register] = f"0x{case.control_value:016x}"
    control_bytes = R.render_forms(
        [[S.Symbol("comment"), control_note(case)], D.expectations_to_form(changed)]).encode("utf-8")
    wrong = C.compare_source_expectation(
        source=source, baseline_expectation=control_bytes, instructions=case.instructions,
        program=case.program, witness=control.witness)
    _require(
        wrong.disposition == "failed" and wrong.difference is not None
        and wrong.difference.step_n == control.witness.step_n,
        "control expectation does not fail at the control boundary alone: " + wrong.reason,
    )
    image = G.build_guest_image(source, program=case.program, entry=ENTRY)
    checked = B.check_source_image(source, image.image, program=case.program, entry=ENTRY)
    _require(checked.disposition == "matched", "image does not correspond to the source: " + checked.reason)
    payloads = {
        "guest.elf": image.image,
        "reference-config.json": (json.dumps(override, indent=2) + "\n").encode("utf-8"),
        "baseline.expected.sexp": baseline,
        "control.expected.sexp": control_bytes,
    }
    for name, payload in payloads.items():
        _require(1 <= len(payload) <= INPUT_BYTES, f"{name} outside 1..{INPUT_BYTES} bytes")
    return tuple(
        PreparedInput(name, ROLES[name], len(payloads[name]), hashlib.sha256(payloads[name]).hexdigest(),
                      payloads[name])
        for name in NAMES
    )


def case_directory(root: Path, case_id: str) -> Path:
    return root / "evidence" / case_id


def verify(root: Path, case: P.ReviewedPropertyCase) -> list[dict]:
    """Compare the derived artifacts with the retained bytes; a missing file is reported, not refused."""
    rows = []
    for item in curate(root, case):
        path = case_directory(root, case.case_id) / item.name
        retained = read_bounded(path) if path.is_file() else None
        rows.append(dict(name=item.name, role=item.role, byte_size=item.byte_size, sha256=item.sha256,
                         retained="missing" if retained is None else ("equal" if retained == item.payload else "differs")))
    return rows


def write(root: Path, case: P.ReviewedPropertyCase) -> list[dict]:
    """Create the four files, each exclusively; an existing file refuses before any write."""
    directory = case_directory(root, case.case_id)
    items = curate(root, case)
    for item in items:
        _require(not (directory / item.name).exists(), "prepared input already exists: " + item.name)
    directory.mkdir(parents=True, exist_ok=True)
    for item in items:
        fd = os.open(directory / item.name, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o644)
        with os.fdopen(fd, "wb") as stream:
            stream.write(item.payload)
    return [dict(name=item.name, role=item.role, byte_size=item.byte_size, sha256=item.sha256) for item in items]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--case", default=P.CASE_ID, help="a reviewed case id (default: the retained case)")
    parser.add_argument("--root", type=Path, default=ROOT)
    action = parser.add_mutually_exclusive_group(required=True)
    action.add_argument("--show", action="store_true")
    action.add_argument("--verify", action="store_true")
    action.add_argument("--write", action="store_true")
    args = parser.parse_args(argv)
    try:
        case = P.reviewed_case(args.case)
        root = args.root.resolve()
        if args.write:
            rows = write(root, case)
        elif args.verify:
            rows = verify(root, case)
        else:
            rows = [dict(name=i.name, role=i.role, byte_size=i.byte_size, sha256=i.sha256) for i in curate(root, case)]
    except OSError as error:
        print(json.dumps(dict(disposition="unavailable", case_id=args.case, reason=type(error).__name__)))
        return 2
    except (CurationRefused, P.PropertyError, K.SchemaError, S.SexpError, D.DossierError,
            G.ImageError, UnicodeError, KeyError, TypeError, ValueError) as error:
        print(json.dumps(dict(disposition="refused", case_id=args.case, reason=str(error))))
        return 1
    disposition = "pending"
    if args.verify and any(row["retained"] != "equal" for row in rows):
        disposition = "differs"
    print(json.dumps(dict(disposition=disposition, case_id=case.case_id, program=case.program,
                          control=dict(property_id=case.control_property_id, note=control_note(case)),
                          inputs=rows, canonical_capture=False, qualification=False), indent=2))
    return 0 if disposition == "pending" else 1


if __name__ == "__main__":
    sys.exit(main())
