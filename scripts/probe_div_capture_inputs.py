#!/usr/bin/env python3
"""Verify prepared DIV inputs through public owners; no execution/qualification."""
from __future__ import annotations

import argparse
from copy import deepcopy
import hashlib
import json
import os
from pathlib import Path
import stat
import subprocess
import sys
from tempfile import TemporaryDirectory
import types
import unittest
from unittest.mock import patch

import check_sexp_schema as K
import dossier_sexp as D
import experiment_artifacts as A
import matched_gpr_artifacts as F
import matched_gpr_collector as Collector
import matched_gpr_comparison as C
import matched_gpr_image as G
import matched_gpr_property as P
import matched_gpr_source_image as B
import records_sexp as R
import sexp as S

ROOT = Path(__file__).resolve().parent.parent
PREFIX = "evidence/rv64gc-signed-div-truncation-v2"
SOURCE = "profiles/rv64gc-lab-v0/guests/m-div.s"
BASELINE = "profiles/rv64gc-lab-v0/guests/m-div.expected.sexp"
OVERRIDE = "profiles/rv64gc-lab-v0/reference/sail-rv64gc-lab-v0.override.sexp"
INPUT_BYTES = 65536
CONTROL_NOTE = (
    "Deliberately incorrect negative control: only boundary 2 x7 changes from -3 to -4. "
    "Baseline derivation text is retained to show why the value is wrong; no execution evidence."
)
PREPARED = {
    "guest.elf": ("guest-image", 4416,
                  "38a327660cb1c699e15694fe98d0467e909726555688074d558768300138e153"),
    "reference-config.json": ("reference-config", 7609,
                              "666d937305f503aa2754784186945f033ade43601f9c9d0073a9ffeefeb43ed2"),
    "baseline.expected.sexp": ("expectation", 5847,
                               "87a5b54c50e147017a2dc60d69869d36679067026d7f449d75db6a344199907e"),
    "control.expected.sexp": ("expectation", 5443,
                              "3f8d591db326a6a83a47921b7743297edc758eb602fa70660b770d37a07c758e"),
}


def bounded_bytes(path):
    with path.open("rb") as stream:
        payload = stream.read(INPUT_BYTES + 1)
    if not 1 <= len(payload) <= INPUT_BYTES:
        raise ValueError("prepared input exceeds 1..65536 bytes")
    return payload


def mapped(payload, kind, mapper):
    """Diagnostic-only raw validation followed by the existing single mapper."""
    if type(payload) is not bytes or not 1 <= len(payload) <= INPUT_BYTES:
        raise ValueError("invalid bounded document bytes")
    text = payload.decode("utf-8")
    constructs, operators = K.load_schema(ROOT / "schema" / (kind + ".sexp"))
    issues = K.validate_text(text, constructs, operators, kind)
    if issues:
        raise ValueError(issues[0])
    forms = [form for form in S.parse(text, kind) if form[0] != "comment"]
    if len(forms) != 1 or forms[0][0] != kind:
        raise ValueError("expected exactly one " + kind + " document")
    return mapper(forms[0])


def input_record(name, path=None, digest=None):
    role, _, pinned = PREPARED[name]
    return dict(id="DIV-" + name, role=role, path=path or PREFIX + "/" + name,
                sha256=pinned if digest is None else digest)


def prepared_bytes(root):
    check_retention_layout(root)
    result = {}
    for name, (_, size, _) in PREPARED.items():
        snapshot = A.read_snapshot(root, "input", input_record(name), max_bytes=INPUT_BYTES)
        if snapshot.pin.disposition != "matched" or len(snapshot.data) != size:
            raise ValueError("prepared artifact pin/size differs: " + name)
        result[name] = snapshot.data
    return result


def retention_limits():
    """The one declared case's finite slots; absent future outputs are permitted."""
    limits = {"README.md": 4096}
    case = PREFIX.split("/", 1)[1]
    for name in PREPARED:
        limits[case + "/" + name] = INPUT_BYTES
    for run in ("baseline", "repeat", "control"):
        for suffix, bound in (("trace", Collector.TRACE_BYTES),
                              ("stdout", Collector.STREAM_BYTES),
                              ("stderr", Collector.STREAM_BYTES),
                              ("receipt.sexp", F.DOCUMENT_BYTES)):
            limits[case + "/" + run + "." + suffix] = bound
    for name in ("planned-experiment.sexp", "dependencies.sexp", "authorities.sexp",
                 "measured-experiment.sexp", "verification.json"):
        limits[case + "/" + name] = INPUT_BYTES
    return limits


def check_retention_layout(root):
    """Census known quiescent paths only; do not descend into unknown directories."""
    limits = retention_limits()
    case = PREFIX.split("/", 1)[1]
    directory = root / "evidence"
    device = root.stat().st_dev
    for folder in (directory, directory / case):
        info = folder.lstat()
        if not stat.S_ISDIR(info.st_mode) or info.st_dev != device:
            raise ValueError("retention directory type/volume differs")
    names = set()
    with os.scandir(directory) as entries:
        for entry in entries:
            if entry.name not in {"README.md", case}:
                raise ValueError("undeclared retained family member")
            names.add(entry.name)
    if names != {"README.md", case}:
        raise ValueError("incomplete retained family layout")
    members = [directory / "README.md"]
    with os.scandir(directory / case) as entries:
        for entry in entries:
            if case + "/" + entry.name not in limits:
                raise ValueError("undeclared retained case member")
            members.append(directory / case / entry.name)
    total = 0
    for path in members:
        info = path.lstat()
        relative = path.relative_to(directory).as_posix()
        if (not stat.S_ISREG(info.st_mode) or info.st_dev != device
                or not 0 <= info.st_size <= limits[relative]):
            raise ValueError("retained member type/volume/role bound differs")
        total += info.st_size
    if len(members) > 22 or total > 16 * 1024 * 1024:
        raise ValueError("retention family exceeds its declared envelope")
    return tuple(path.relative_to(directory).as_posix() for path in members), total


class PreparedInputTests(unittest.TestCase):
    def setUp(self):
        self.payloads = prepared_bytes(ROOT)
        self.source = bounded_bytes(ROOT / SOURCE)
        self.case = P.signed_division_case()
        self.baseline = self.payloads["baseline.expected.sexp"]
        self.control = self.payloads["control.expected.sexp"]
        base = ROOT / "target/prepared-div-input-controls"
        base.mkdir(parents=True, exist_ok=True)
        temporary = TemporaryDirectory(dir=base)
        self.addCleanup(temporary.cleanup)
        self.temporary = Path(temporary.name)

    def source_finding(self, expectation):
        return C.compare_source_expectation(
            source=self.source, baseline_expectation=expectation,
            instructions=self.case.instructions, program=self.case.program,
            witness=self.case.control().witness)

    def fixture_record(self, name, payload, *, repin=False):
        path = self.temporary / name
        path.write_bytes(payload)
        digest = hashlib.sha256(payload).hexdigest() if repin else None
        return input_record(name, path.relative_to(ROOT).as_posix(), digest)

    def test_actual_four_pins_and_sizes(self):
        self.assertEqual(len(self.payloads), 4)
        self.assertEqual(sum(map(len, self.payloads.values())), 23315)
        for name, (_, size, digest) in PREPARED.items():
            self.assertEqual(len(self.payloads[name]), size)
            self.assertEqual(hashlib.sha256(self.payloads[name]).hexdigest(), digest)

    def test_baseline_is_the_complete_canonical_copy(self):
        self.assertEqual(self.baseline, bounded_bytes(ROOT / BASELINE))
        document = mapped(self.baseline, "expectations", D.expectations_to_doc)
        self.assertEqual((document["program"], document["instructions"], document["fetches"]),
                         ("m-div.s", 27, 54))
        self.assertEqual([step["n"] for step in document["step"]], list(range(27)))

    def test_complete_image_matches_public_reconstruction(self):
        image = self.payloads["guest.elf"]
        built = G.build_guest_image(self.source, program=self.case.program, entry=0x80000000)
        self.assertEqual(image, built.image)
        result = B.check_source_image(self.source, image, program=self.case.program, entry=0x80000000)
        self.assertEqual(result.disposition, "matched", result.reason)
        self.assertEqual(result.facts.image_sha256, PREPARED["guest.elf"][2])

    def test_all_source_values_and_the_reviewed_quotient_match(self):
        result = self.source_finding(self.baseline)
        self.assertEqual(result.disposition, "matched", result.reason)
        self.assertEqual(len(result.facts.derivation.steps), 27)
        self.assertEqual(result.facts.witness_value, self.case.control().expected_value)

    def test_control_is_exactly_one_typed_wrong_value(self):
        base = mapped(self.baseline, "expectations", D.expectations_to_doc)
        changed = mapped(self.control, "expectations", D.expectations_to_doc)
        self.assertEqual(changed["step"][2]["writes"]["x7"], "0xfffffffffffffffc")
        restored = deepcopy(changed)
        restored["step"][2]["writes"]["x7"] = base["step"][2]["writes"]["x7"]
        self.assertEqual(restored, base)
        expected = R.render_forms([[S.Symbol("comment"), CONTROL_NOTE],
                                   D.expectations_to_form(changed)]).encode("utf-8")
        self.assertEqual(expected, self.control)
        result = self.source_finding(self.control)
        self.assertEqual(result.disposition, "failed")
        self.assertEqual(result.difference.step_n, 2)
        self.assertEqual(result.difference.observed, (("x7", self.case.control().expected_value),))
        self.assertEqual(result.difference.expected, (("x7", self.case.control_value),))

    def test_config_is_exact_public_materialization(self):
        canonical = mapped(bounded_bytes(ROOT / OVERRIDE), "override", D.override_to_doc)
        payload = self.payloads["reference-config.json"]
        self.assertEqual(payload, (json.dumps(canonical, indent=2) + "\n").encode("utf-8"))
        self.assertEqual(json.loads(payload), canonical)
        changed = deepcopy(canonical)
        changed["base"]["writable_misa"] = True
        self.assertNotEqual(changed, json.loads(payload))

    def test_changed_artifacts_are_not_accepted_under_the_original_pins(self):
        for name, payload in self.payloads.items():
            with self.subTest(name=name):
                record = self.fixture_record(name, payload + b"\n")
                result = A.read_snapshot(ROOT, "input", record, max_bytes=INPUT_BYTES)
                self.assertEqual(result.pin.disposition, "mismatch")

    def test_missing_artifacts_are_unavailable(self):
        for name in PREPARED:
            record = input_record(name, (self.temporary / name).relative_to(ROOT).as_posix())
            self.assertEqual(A.read_snapshot(ROOT, "input", record,
                                            max_bytes=INPUT_BYTES).pin.disposition, "unavailable")

    def test_repinning_a_changed_image_does_not_restore_correspondence(self):
        payload = self.payloads["guest.elf"]
        for changed in (bytes([payload[0] ^ 1]) + payload[1:], payload[:-1] + bytes([payload[-1] ^ 1])):
            record = self.fixture_record("guest.elf", changed, repin=True)
            snapshot = A.read_snapshot(ROOT, "input", record, max_bytes=INPUT_BYTES)
            self.assertEqual(snapshot.pin.disposition, "matched")
            result = B.check_source_image(self.source, snapshot.data, program=self.case.program,
                                          entry=0x80000000)
            self.assertEqual(result.disposition, "refused")

    def test_additional_control_change_is_detected_by_the_source_author(self):
        changed = mapped(self.control, "expectations", D.expectations_to_doc)
        changed["step"][1]["writes"]["x6"] = "0x0000000000000003"
        result = self.source_finding(R.render_forms([D.expectations_to_form(changed)]).encode())
        self.assertEqual(result.disposition, "failed")
        self.assertEqual(result.difference.step_n, 1)

    def test_matching_pin_cannot_exceed_the_prepared_input_bound(self):
        record = self.fixture_record("guest.elf", b"x" * (INPUT_BYTES + 1), repin=True)
        result = A.read_snapshot(ROOT, "input", record, max_bytes=INPUT_BYTES)
        self.assertEqual(result.pin.disposition, "refused")

    def test_raw_schema_precedes_mapping(self):
        with patch.object(D, "expectations_to_doc", side_effect=AssertionError("mapper reached")):
            with self.assertRaises(ValueError):
                mapped(b"(expectations (unknown true))", "expectations", D.expectations_to_doc)

    def test_supplied_byte_findings_launch_no_process_or_artifact_read(self):
        with patch.object(subprocess, "Popen", side_effect=AssertionError("process launched")), \
                patch.object(A, "read_snapshot", side_effect=AssertionError("artifact read")):
            self.assertEqual(self.source_finding(self.baseline).disposition, "matched")
            result = B.check_source_image(self.source, self.payloads["guest.elf"],
                                          program=self.case.program, entry=0x80000000)
            self.assertEqual(result.disposition, "matched")

    def test_package_copy_needs_no_binary_or_materials(self):
        for name, payload in self.payloads.items():
            path = self.temporary / PREFIX / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(payload)
        (self.temporary / "evidence/README.md").write_bytes(bounded_bytes(ROOT / "evidence/README.md"))
        self.assertFalse((self.temporary / "target/refs").exists())
        self.assertFalse((self.temporary / ".materials").exists())
        self.assertEqual(prepared_bytes(self.temporary), self.payloads)

    def test_index_and_declared_retention_envelopes_fit(self):
        index = bounded_bytes(ROOT / "evidence/README.md")
        self.assertLessEqual(len(index), 4096)
        self.assertLessEqual(len(index.splitlines()), 80)
        self.assertEqual((Collector.TRACE_BYTES, Collector.STREAM_BYTES, F.DOCUMENT_BYTES),
                         (4 * 1024 * 1024, INPUT_BYTES, INPUT_BYTES))
        limits = retention_limits()
        self.assertEqual(len(limits), 22)
        self.assertEqual(sum(limits.values()), 13766656)
        self.assertLess(sum(limits.values()), 16 * 1024 * 1024)
        self.assertLessEqual(max(Collector.TRACE_BYTES, Collector.STREAM_BYTES,
                                 F.DOCUMENT_BYTES, INPUT_BYTES), 4 * 1024 * 1024)

    def test_undeclared_linked_and_oversized_members_refuse(self):
        case = PREFIX.split("/", 1)[1]
        for change in ("sibling", "unknown", "stream", "metadata", "link"):
            with self.subTest(change=change), TemporaryDirectory(dir=self.temporary) as directory:
                root = Path(directory)
                folder = root / "evidence" / case
                folder.mkdir(parents=True)
                (root / "evidence/README.md").write_text("bounded fixture index\n")
                for name, payload in self.payloads.items():
                    (folder / name).write_bytes(payload)
                if change == "sibling":
                    (root / "evidence/undeclared-case").mkdir()
                elif change == "unknown":
                    (folder / "unknown").mkdir()
                elif change == "stream":
                    (folder / "baseline.stdout").write_bytes(b"x" * (Collector.STREAM_BYTES + 1))
                elif change == "metadata":
                    (folder / "authorities.sexp").write_bytes(b"x" * (INPUT_BYTES + 1))
                else:
                    (folder / "baseline.trace").symlink_to("missing")
                with self.assertRaises(ValueError):
                    prepared_bytes(root)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mutation", choices=["actual-layout"])
    args = parser.parse_args()
    tests = PreparedInputTests
    if args.mutation:
        before = "    check_retention_layout(root)\n    result = {}\n"
        source = Path(__file__).read_text()
        if source.count(before) != 1:
            raise RuntimeError("prepared-input layout mutation seam count changed")
        module = types.ModuleType("mutated_prepared_div_inputs")
        module.__file__ = __file__
        sys.modules[module.__name__] = module
        exec(compile(source.replace(before, "    result = {}\n", 1), __file__, "exec"),
             module.__dict__)
        tests = module.PreparedInputTests
    result = unittest.TextTestRunner(verbosity=1).run(
        unittest.defaultTestLoader.loadTestsFromTestCase(tests))
    print(f"DIV-CAPTURE-INPUTS: {result.testsRun} tests / {len(result.failures)} failures / "
          f"{len(result.errors)} errors; prepared artifacts, no reference process or capture credit")
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    raise SystemExit(main())
