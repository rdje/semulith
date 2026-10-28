#!/usr/bin/env python3
"""Verify the prepared inputs of every reviewed case through public owners; no execution/qualification."""
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

import capture_div as Command
import check_sexp_schema as K
import dossier_sexp as D
import experiment_artifacts as A
import matched_gpr_artifacts as F
import matched_gpr_collector as Collector
import matched_gpr_comparison as C
import matched_gpr_image as G
import matched_gpr_property as P
import matched_gpr_source_image as B
import prepare_div_inputs as Prep
import records_sexp as R
import sexp as S

ROOT = Path(__file__).resolve().parent.parent
GUESTS = "profiles/rv64gc-lab-v0/guests"
OVERRIDE = "profiles/rv64gc-lab-v0/reference/sail-rv64gc-lab-v0.override.sexp"
INPUT_BYTES = 65536
FAMILY_FILES = 45  # two declared cases of 22 slots each (the case declaration since P4-SYSTEM.14 a44-2a), plus the index
FAMILY_BYTES = 32 * 1024 * 1024
CASES = (P.CASE_ID, P.M_FORMS_CASE_ID)
# The pins this probe states on its own; a test holds them equal to the capture command's table.
PREPARED = {
    P.CASE_ID: {
        "guest.elf": ("guest-image", 4416,
                      "38a327660cb1c699e15694fe98d0467e909726555688074d558768300138e153"),
        "reference-config.json": ("reference-config", 7609,
                                  "666d937305f503aa2754784186945f033ade43601f9c9d0073a9ffeefeb43ed2"),
        "baseline.expected.sexp": ("expectation", 5847,
                                   "87a5b54c50e147017a2dc60d69869d36679067026d7f449d75db6a344199907e"),
        "control.expected.sexp": ("expectation", 5443,
                                  "3f8d591db326a6a83a47921b7743297edc758eb602fa70660b770d37a07c758e"),
    },
    P.M_FORMS_CASE_ID: {
        "guest.elf": ("guest-image", 4440,
                      "208865142e1569636925a5cea6abff6fc4495f317d5d8e79a06e48d3b0f061b1"),
        "reference-config.json": ("reference-config", 7609,
                                  "666d937305f503aa2754784186945f033ade43601f9c9d0073a9ffeefeb43ed2"),
        "baseline.expected.sexp": ("expectation", 7937,
                                   "561b5da3cf87ea4825fca4e1a001a9c7d26321e491d86515c571f47b0019f44f"),
        "control.expected.sexp": ("expectation", 7440,
                                  "ba99e4eca2e784d8389859e35cf04590c180162807311361eef70add589f4ba0"),
    },
}
TOTALS = {P.CASE_ID: 23315, P.M_FORMS_CASE_ID: 27426}
BUDGETS = {P.CASE_ID: (27, 54), P.M_FORMS_CASE_ID: (33, 66)}


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


def prefix(case_id):
    return "evidence/" + case_id


def input_record(case_id, name, path=None, digest=None):
    role, _, pinned = PREPARED[case_id][name]
    return dict(id="DIV-" + name, role=role, path=path or prefix(case_id) + "/" + name,
                sha256=pinned if digest is None else digest)


def prepared_bytes(root, case_id):
    check_retention_layout(root)
    result = {}
    for name, (_, size, _) in PREPARED[case_id].items():
        snapshot = A.read_snapshot(root, "input", input_record(case_id, name), max_bytes=INPUT_BYTES)
        if snapshot.pin.disposition != "matched" or len(snapshot.data) != size:
            raise ValueError("prepared artifact pin/size differs: " + name)
        result[name] = snapshot.data
    return result


def retention_limits():
    """Every declared case's finite slots; absent future outputs are permitted."""
    limits = {"README.md": 4096}
    for case_id in CASES:
        for name in PREPARED[case_id]:
            limits[case_id + "/" + name] = INPUT_BYTES
        for run in ("baseline", "repeat", "control"):
            for suffix, bound in (("trace", Collector.TRACE_BYTES),
                                  ("stdout", Collector.STREAM_BYTES),
                                  ("stderr", Collector.STREAM_BYTES),
                                  ("receipt.sexp", F.DOCUMENT_BYTES)):
                limits[case_id + "/" + run + "." + suffix] = bound
        for name in ("case.sexp", "planned-experiment.sexp", "dependencies.sexp", "authorities.sexp",
                     "measured-experiment.sexp", "verification.json"):
            limits[case_id + "/" + name] = INPUT_BYTES
    return limits


def check_retention_layout(root):
    """Census known quiescent paths only; do not descend into unknown directories."""
    limits = retention_limits()
    directory = root / "evidence"
    device = root.stat().st_dev
    for folder in (directory, *(directory / case_id for case_id in CASES)):
        info = folder.lstat()
        if not stat.S_ISDIR(info.st_mode) or info.st_dev != device:
            raise ValueError("retention directory type/volume differs")
    declared = {"README.md", *CASES}
    names = set()
    with os.scandir(directory) as entries:
        for entry in entries:
            if entry.name not in declared:
                raise ValueError("undeclared retained family member")
            names.add(entry.name)
    if names != declared:
        raise ValueError("incomplete retained family layout")
    members = [directory / "README.md"]
    for case_id in CASES:
        with os.scandir(directory / case_id) as entries:
            for entry in entries:
                if case_id + "/" + entry.name not in limits:
                    raise ValueError("undeclared retained case member")
                members.append(directory / case_id / entry.name)
    total = 0
    for path in members:
        info = path.lstat()
        relative = path.relative_to(directory).as_posix()
        if (not stat.S_ISREG(info.st_mode) or info.st_dev != device
                or not 0 <= info.st_size <= limits[relative]):
            raise ValueError("retained member type/volume/role bound differs")
        total += info.st_size
    if len(members) > FAMILY_FILES or total > FAMILY_BYTES:
        raise ValueError("retention family exceeds its declared envelope")
    return tuple(path.relative_to(directory).as_posix() for path in members), total


class CaseInputTests(unittest.TestCase):
    """One reviewed case's four prepared inputs; subclassed once per case."""

    CASE_ID = None

    @classmethod
    def setUpClass(cls):
        if cls.CASE_ID is None:
            raise unittest.SkipTest("abstract per-case test class")

    def setUp(self):
        self.case = P.reviewed_case(self.CASE_ID)
        self.payloads = prepared_bytes(ROOT, self.CASE_ID)
        self.source = bounded_bytes(ROOT / GUESTS / self.case.program)
        self.baseline = self.payloads["baseline.expected.sexp"]
        self.control = self.payloads["control.expected.sexp"]
        self.step = self.case.control().witness.step_n
        self.register = self.case.control().witness.register
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
        return input_record(self.CASE_ID, name, path.relative_to(ROOT).as_posix(), digest)

    def test_actual_four_pins_and_sizes(self):
        self.assertEqual(len(self.payloads), 4)
        self.assertEqual(sum(map(len, self.payloads.values())), TOTALS[self.CASE_ID])
        for name, (_, size, digest) in PREPARED[self.CASE_ID].items():
            self.assertEqual(len(self.payloads[name]), size)
            self.assertEqual(hashlib.sha256(self.payloads[name]).hexdigest(), digest)

    def test_pins_equal_the_capture_commands_table(self):
        rows = Command.prepared_inputs(self.CASE_ID)
        self.assertEqual(len(rows), 5)
        for role, _, path, size, digest in rows[:4]:
            name = path.rsplit("/", 1)[1]
            self.assertEqual(path, prefix(self.CASE_ID) + "/" + name)
            self.assertEqual((role, size, digest), PREPARED[self.CASE_ID][name])
        self.assertEqual(rows[4], Command.IDENTITY_ROW)  # the profile's identity, shared by every case
        with self.assertRaises(Command.AuthorityError):
            Command.prepared_inputs("rv64gc-unpinned")

    def test_baseline_is_the_complete_canonical_copy(self):
        canonical = GUESTS + "/" + Path(self.case.program).stem + ".expected.sexp"
        self.assertEqual(self.baseline, bounded_bytes(ROOT / canonical))
        document = mapped(self.baseline, "expectations", D.expectations_to_doc)
        instructions, fetches = BUDGETS[self.CASE_ID]
        self.assertEqual((document["program"], document["instructions"], document["fetches"]),
                         (self.case.program, instructions, fetches))
        self.assertEqual([step["n"] for step in document["step"]], list(range(instructions)))

    def test_complete_image_matches_public_reconstruction(self):
        image = self.payloads["guest.elf"]
        built = G.build_guest_image(self.source, program=self.case.program, entry=0x80000000)
        self.assertEqual(image, built.image)
        result = B.check_source_image(self.source, image, program=self.case.program, entry=0x80000000)
        self.assertEqual(result.disposition, "matched", result.reason)
        self.assertEqual(result.facts.image_sha256, PREPARED[self.CASE_ID]["guest.elf"][2])

    def test_all_source_values_and_the_control_value_match(self):
        result = self.source_finding(self.baseline)
        self.assertEqual(result.disposition, "matched", result.reason)
        self.assertEqual(len(result.facts.derivation.steps), self.case.instructions)
        self.assertEqual(result.facts.witness_value, self.case.control().expected_value)
        for item in self.case.properties:
            writes = dict(result.facts.derivation.steps[item.witness.step_n].writes)
            self.assertEqual(writes.get(int(item.witness.register[1:])), item.expected_value, item.property_id)

    def test_control_is_exactly_one_typed_wrong_value(self):
        base = mapped(self.baseline, "expectations", D.expectations_to_doc)
        changed = mapped(self.control, "expectations", D.expectations_to_doc)
        self.assertEqual(changed["step"][self.step]["writes"][self.register], f"0x{self.case.control_value:016x}")
        restored = deepcopy(changed)
        restored["step"][self.step]["writes"][self.register] = base["step"][self.step]["writes"][self.register]
        self.assertEqual(restored, base)
        expected = R.render_forms([[S.Symbol("comment"), Prep.control_note(self.case)],
                                   D.expectations_to_form(changed)]).encode("utf-8")
        self.assertEqual(expected, self.control)
        result = self.source_finding(self.control)
        self.assertEqual(result.disposition, "failed")
        self.assertEqual(result.difference.step_n, self.step)
        self.assertEqual(result.difference.observed, ((self.register, self.case.control().expected_value),))
        self.assertEqual(result.difference.expected, ((self.register, self.case.control_value),))

    def test_config_is_exact_public_materialization(self):
        canonical = mapped(bounded_bytes(ROOT / OVERRIDE), "override", D.override_to_doc)
        payload = self.payloads["reference-config.json"]
        self.assertEqual(payload, (json.dumps(canonical, indent=2) + "\n").encode("utf-8"))
        self.assertEqual(json.loads(payload), canonical)
        changed = deepcopy(canonical)
        changed["base"]["writable_misa"] = True
        self.assertNotEqual(changed, json.loads(payload))

    def test_curation_tool_reproduces_the_retained_bytes(self):
        items = Prep.curate(ROOT, self.case)
        self.assertEqual([item.name for item in items], list(PREPARED[self.CASE_ID]))
        for item in items:
            self.assertEqual(item.payload, self.payloads[item.name], item.name)
            self.assertEqual((item.role, item.byte_size, item.sha256), PREPARED[self.CASE_ID][item.name])
        self.assertEqual([row["retained"] for row in Prep.verify(ROOT, self.case)], ["equal"] * 4)

    def test_changed_artifacts_are_not_accepted_under_the_original_pins(self):
        for name, payload in self.payloads.items():
            with self.subTest(name=name):
                record = self.fixture_record(name, payload + b"\n")
                result = A.read_snapshot(ROOT, "input", record, max_bytes=INPUT_BYTES)
                self.assertEqual(result.pin.disposition, "mismatch")

    def test_missing_artifacts_are_unavailable(self):
        for name in PREPARED[self.CASE_ID]:
            record = input_record(self.CASE_ID, name, (self.temporary / name).relative_to(ROOT).as_posix())
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

    def test_supplied_byte_findings_launch_no_process_or_artifact_read(self):
        with patch.object(subprocess, "Popen", side_effect=AssertionError("process launched")), \
                patch.object(A, "read_snapshot", side_effect=AssertionError("artifact read")):
            self.assertEqual(self.source_finding(self.baseline).disposition, "matched")
            result = B.check_source_image(self.source, self.payloads["guest.elf"],
                                          program=self.case.program, entry=0x80000000)
            self.assertEqual(result.disposition, "matched")

    def test_package_copy_needs_no_binary_or_materials(self):
        for case_id in CASES:
            for name in PREPARED[case_id]:
                path = self.temporary / prefix(case_id) / name
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_bytes(bounded_bytes(ROOT / prefix(case_id) / name))
        (self.temporary / "evidence/README.md").write_bytes(bounded_bytes(ROOT / "evidence/README.md"))
        self.assertFalse((self.temporary / "target/refs").exists())
        self.assertFalse((self.temporary / ".materials").exists())
        self.assertEqual(prepared_bytes(self.temporary, self.CASE_ID), self.payloads)


class RetainedCaseInputTests(CaseInputTests):
    CASE_ID = P.CASE_ID


class MFormsCaseInputTests(CaseInputTests):
    CASE_ID = P.M_FORMS_CASE_ID


class FamilyTests(unittest.TestCase):
    def setUp(self):
        base = ROOT / "target/prepared-div-input-controls"
        base.mkdir(parents=True, exist_ok=True)
        temporary = TemporaryDirectory(dir=base)
        self.addCleanup(temporary.cleanup)
        self.temporary = Path(temporary.name)

    def test_raw_schema_precedes_mapping(self):
        with patch.object(D, "expectations_to_doc", side_effect=AssertionError("mapper reached")):
            with self.assertRaises(ValueError):
                mapped(b"(expectations (unknown true))", "expectations", D.expectations_to_doc)

    def test_index_and_declared_retention_envelopes_fit(self):
        index = bounded_bytes(ROOT / "evidence/README.md")
        self.assertLessEqual(len(index), 4096)
        self.assertLessEqual(len(index.splitlines()), 80)
        self.assertEqual((Collector.TRACE_BYTES, Collector.STREAM_BYTES, F.DOCUMENT_BYTES),
                         (4 * 1024 * 1024, INPUT_BYTES, INPUT_BYTES))
        limits = retention_limits()
        self.assertEqual(len(limits), FAMILY_FILES)
        self.assertEqual(sum(limits.values()), 27660288)  # +2 x 65536: the two case declarations (a44-2a)
        self.assertLess(sum(limits.values()), FAMILY_BYTES)
        self.assertLessEqual(max(Collector.TRACE_BYTES, Collector.STREAM_BYTES,
                                 F.DOCUMENT_BYTES, INPUT_BYTES), 4 * 1024 * 1024)
        members, total = check_retention_layout(ROOT)
        self.assertEqual(len(members), 1 + 22 + 22)
        self.assertEqual(set(P.reviewed_case_ids()), set(CASES))

    def test_undeclared_linked_and_oversized_members_refuse(self):
        for change in ("sibling", "unknown", "stream", "metadata", "link", "missing-case"):
            with self.subTest(change=change), TemporaryDirectory(dir=self.temporary) as directory:
                root = Path(directory)
                (root / "evidence").mkdir()
                (root / "evidence/README.md").write_text("bounded fixture index\n")
                for case_id in CASES:
                    folder = root / "evidence" / case_id
                    folder.mkdir()
                    for name in PREPARED[case_id]:
                        (folder / name).write_bytes(bounded_bytes(ROOT / prefix(case_id) / name))
                folder = root / "evidence" / CASES[0]
                if change == "sibling":
                    (root / "evidence/undeclared-case").mkdir()
                elif change == "unknown":
                    (folder / "unknown").mkdir()
                elif change == "stream":
                    (folder / "baseline.stdout").write_bytes(b"x" * (Collector.STREAM_BYTES + 1))
                elif change == "metadata":
                    (folder / "authorities.sexp").write_bytes(b"x" * (INPUT_BYTES + 1))
                elif change == "link":
                    (folder / "baseline.trace").symlink_to("missing")
                else:
                    for name in PREPARED[CASES[1]]:
                        (root / "evidence" / CASES[1] / name).unlink()
                    (root / "evidence" / CASES[1]).rmdir()
                with self.assertRaises((ValueError, FileNotFoundError)):
                    prepared_bytes(root, CASES[0])

    def test_write_is_exclusive_and_refuses_an_existing_file(self):
        case = P.reviewed_case(P.M_FORMS_CASE_ID)
        items = Prep.curate(ROOT, case)
        root = self.temporary / "fresh"
        root.mkdir()
        with patch.object(Prep, "curate", return_value=items):
            rows = Prep.write(root, case)
            self.assertEqual([row["name"] for row in rows], list(PREPARED[case.case_id]))
            for item in items:
                self.assertEqual((root / "evidence" / case.case_id / item.name).read_bytes(), item.payload)
            with self.assertRaises(Prep.CurationRefused):
                Prep.write(root, case)
            partial = self.temporary / "partial"
            (partial / "evidence" / case.case_id).mkdir(parents=True)
            (partial / "evidence" / case.case_id / "control.expected.sexp").write_bytes(b"older")
            with self.assertRaises(Prep.CurationRefused):
                Prep.write(partial, case)
            self.assertEqual(sorted(p.name for p in (partial / "evidence" / case.case_id).iterdir()),
                             ["control.expected.sexp"])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mutation", choices=["actual-layout"])
    args = parser.parse_args()
    classes = (RetainedCaseInputTests, MFormsCaseInputTests, FamilyTests)
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
        classes = (module.RetainedCaseInputTests, module.MFormsCaseInputTests, module.FamilyTests)
    suite = unittest.TestSuite(unittest.defaultTestLoader.loadTestsFromTestCase(cls) for cls in classes)
    result = unittest.TextTestRunner(verbosity=1).run(suite)
    print(f"DIV-CAPTURE-INPUTS: {result.testsRun} tests / {len(result.failures)} failures / "
          f"{len(result.errors)} errors; prepared artifacts of every reviewed case, no reference process or capture credit")
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    raise SystemExit(main())
