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

A case may carry its own reference configuration: `reference/<case-id>.overlay.sexp` beside the
profile override, applied over the mapped override here and nowhere else, so the profile override
and every other case's configuration do not move (decision_reference-config-per-case.md). A case
may also declare what selects otherwise, `reference/<case-id>.alternative.sexp`: it renders here and
is run only by `measure_config_effect.py` (decision_declared-alternative-configuration.md).

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
# The pinned binary's published MMIO region attributes (`sail_riscv_sim --print-default-config`), for a device an overlay places.
DEVICE_REGION_ATTRIBUTES = {
    "mem_type": "IOMemory", "cacheable": False, "coherent": True, "executable": False, "readable": True, "writable": True,
    "read_idempotent": False, "write_idempotent": False,
    "misaligned_exceptions": {"load_store": {"None": None}, "vector": {"None": None}, "amo": "AccessFault", "lrsc": "AccessFault"},
    "atomic_support": "AMONone", "misaligned_atomicity_granule_size_exp": 0, "vector_misaligned_atomicity_granule_size_exp": 0,
    "reservability": "RsrvNone", "supports_cbo_zero": False, "supports_pte_read": False, "supports_pte_write": False,
}
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


def overlay_path(case_id: str) -> str:
    return "profiles/" + PROFILE + "/reference/" + case_id + ".overlay.sexp"


def overlay_to_doc(form) -> dict:
    doc = {
        "case_id": str(S.children(form, "case_id")[0][1]),
        "extensions": [str(child[1]) for child in S.children(form, "extension")],
    }
    for clint in S.children(form, "clint"):
        doc.update(clint_base=S.children(clint, "base")[0][1], clint_size=S.children(clint, "size")[0][1])
    for tick in S.children(form, "instructions_per_tick"):
        doc["instructions_per_tick"] = tick[1]
    for amo in S.children(form, "misaligned_amo"):
        doc["misaligned_amo"] = str(amo[1])
    if S.children(form, "require_exact_reservation_addr"):
        doc["require_exact_reservation_addr"] = True
    return doc


def apply_overlay(config: dict, overlay: dict) -> dict:
    """The profile's mapped configuration with one case's overlay applied; every change must change something."""
    result = deepcopy(config)
    for name in overlay["extensions"]:
        entry = result["extensions"].get(name)
        _require(entry is not None, f"overlay names unknown extension {name}")
        _require(entry["supported"] is False, f"overlay enables {name}, which the profile override already supports")
        entry["supported"] = True
    platform = result["platform"]
    if "clint_base" in overlay:
        _require(platform["clint"] == {"supported": False}, "overlay places a CLINT over a profile override that declares one")
        base, size = overlay["clint_base"], overlay["clint_size"]
        _require(base > 0 and size > 0, "overlay's CLINT needs a positive base and size")
        platform["clint"] = {"supported": True, "base": base, "size": size}
        regions = result["memory"]["regions"]
        for region in regions:
            start = int(region["base"]["value"], 16)
            _require(base + size <= start or start + int(region["size"]["value"], 16) <= base,
                     f"overlay's CLINT region overlaps the region at {region['base']['value']}")
        device = {"base": {"len": 64, "value": f"0x{base:X}"}, "size": {"len": 64, "value": f"0x{size:X}"},
                  "attributes": deepcopy(DEVICE_REGION_ATTRIBUTES), "include_in_device_tree": False}
        # The binary refuses regions out of order (measured, a43b-3a), so the device goes where its base puts it.
        position = sum(1 for region in regions if int(region["base"]["value"], 16) < base)
        regions.insert(position, device)
    if "instructions_per_tick" in overlay:
        _require(overlay["instructions_per_tick"] >= 1, "overlay's tick rate must be positive")
        _require("instructions_per_tick" not in platform, "overlay sets a tick rate the profile override already declares")
        platform["instructions_per_tick"] = overlay["instructions_per_tick"]
    if "misaligned_amo" in overlay:
        exceptions = result["memory"]["misaligned"]["exceptions"]
        rendered = {"Some": overlay["misaligned_amo"]}
        _require(exceptions.get("amo") != rendered, "overlay selects a misaligned AMO the profile override already declares")
        exceptions["amo"] = rendered
    if "require_exact_reservation_addr" in overlay:
        reservation = platform.setdefault("reservation", {})
        _require("require_exact_reservation_addr" not in reservation, "overlay sets an exact reservation the profile override already declares")
        reservation["require_exact_reservation_addr"] = True
    _require(result != config, "the overlay changes nothing")
    return result


def reference_config(root: Path, case_id: str) -> dict:
    """The case's reference configuration: the mapped profile override, under the case's overlay if it declares one."""
    override = map_document(root, read_bounded(root / OVERRIDE), "override", D.override_to_doc)
    path = root / overlay_path(case_id)
    if not path.is_file():
        return override
    overlay = map_document(root, read_bounded(path), "overlay", overlay_to_doc)
    _require(overlay["case_id"] == case_id, f"overlay {overlay_path(case_id)} declares case {overlay['case_id']}")
    return apply_overlay(override, overlay)


def alternative_path(case_id: str) -> str:
    return "profiles/" + PROFILE + "/reference/" + case_id + ".alternative.sexp"


def alternative_to_doc(form) -> dict:
    def one(name):
        found = S.children(form, name)
        return str(found[0][1]) if found else None
    return {
        "case_id": one("case_id"),
        "extensions_off": [str(child[1]) for child in S.children(form, "extension_off")],
        "extensions_on": [str(child[1]) for child in S.children(form, "extension_on")],
        "misaligned": {kind: one("misaligned_" + kind) for kind in ("load_store", "lrsc", "amo") if one("misaligned_" + kind)},
    }


def apply_alternative(config: dict, alternative: dict) -> dict:
    """A case's configuration as its declared alternative selects otherwise; every switch must change something."""
    result = deepcopy(config)
    for names, wanted, word in ((alternative["extensions_off"], False, "off"), (alternative["extensions_on"], True, "on")):
        for name in names:
            entry = result["extensions"].get(name)
            _require(entry is not None, f"alternative names unknown extension {name}")
            _require(entry["supported"] is not wanted, f"alternative turns {name} {word}, which this configuration already has")
            entry["supported"] = wanted
    exceptions = result["memory"]["misaligned"]["exceptions"]
    for kind, selected in alternative["misaligned"].items():
        rendered = {"None": None} if selected == "None" else {"Some": selected}
        _require(exceptions.get(kind) != rendered, f"alternative selects {selected} for misaligned {kind}, which this configuration already declares")
        exceptions[kind] = rendered
    _require(result != config, "the alternative changes nothing")
    return result


def alternative_config(root: Path, case_id: str) -> dict | None:
    """What the case declares to select otherwise, over its own configuration; None when it declares nothing."""
    path = root / alternative_path(case_id)
    if not path.is_file():
        return None
    alternative = map_document(root, read_bounded(path), "alternative", alternative_to_doc)
    _require(alternative["case_id"] == case_id, f"alternative {alternative_path(case_id)} declares case {alternative['case_id']}")
    return apply_alternative(reference_config(root, case_id), alternative)


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
    config = reference_config(root, case.case_id)
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
        "reference-config.json": (json.dumps(config, indent=2) + "\n").encode("utf-8"),
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
