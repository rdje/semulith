#!/usr/bin/env python3
"""Controls for the matched cases' declarations as data (scripts/matched_gpr_case.py; P4-SYSTEM.14 a44-2a).

Every declared case reads as declared and renders back byte for byte; until the tools read the data (a44-2b),
each declaration equals the in-code case it moves out of, and its prepared rows equal the capture command's
pins. A missing declaration, an invalid one, one whose id disagrees with its directory and one whose control
names no property are each refused. `--mutation NAME` removes one refusal or binding from a copy of the module
and the suite must lose the tests that refusal or binding holds.
"""
from __future__ import annotations

import argparse
import importlib.util
from pathlib import Path
import shutil
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
import capture_div as A  # noqa: E402
import matched_gpr_property as P  # noqa: E402

MODULE = ROOT / "scripts/matched_gpr_case.py"
SEAMS = {
    "missing-refusal": ("    if not path.is_file():\n", "    if False:\n"),
    "id-binding": ("    if case.case_id != case_id:\n", "    if False:\n"),
    "control-binding": ("    if case.control_property_id not in {item.property_id for item in case.properties}:\n",
                        "    if False:\n"),
    "schema": ("    if errors:\n", "    if False:\n"),
    "value-mapping": ('C.GprWitness(item["step_n"], item["register"]), item["expected"])',
                      'C.GprWitness(item["step_n"], item["register"]), 0)'),
}
MUTATION = None


def load():
    text = MODULE.read_text()
    if MUTATION:
        before, after = SEAMS[MUTATION]
        if text.count(before) != 1:
            raise RuntimeError("singular omission seam: " + MUTATION)
        text = text.replace(before, after, 1)
    directory = Path(tempfile.mkdtemp(dir=ROOT / "target/tmp"))
    path = directory / "matched_gpr_case_under_test.py"
    path.write_text(text)
    spec = importlib.util.spec_from_file_location("matched_gpr_case_under_test", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    module.ROOT = ROOT
    shutil.rmtree(directory)
    return module


class CaseTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.K = load()

    def refused(self, call, pattern):
        """The call must refuse with a CaseError matching pattern; any other outcome is a failure, never an error."""
        try:
            call()
        except self.K.CaseError as error:
            self.assertRegex(str(error), pattern)
            return
        except Exception as error:  # an unrefused case reaches another exception: that is the loss, by name
            self.fail(f"not refused as a case error: {type(error).__name__}: {error}")
        self.fail("not refused")

    def test_every_declared_case_reads_as_declared(self):
        ids = self.K.declared_case_ids()
        self.assertEqual(set(ids), set(P.reviewed_case_ids()))
        for case_id in ids:
            case, prepared = self.K.read_case(case_id)
            self.assertEqual(case.case_id, case_id)

    def test_each_declaration_equals_the_case_it_moves_out_of(self):
        for case_id in P.reviewed_case_ids():
            case, prepared = self.K.read_case(case_id)
            self.assertEqual(case, P.reviewed_case(case_id))
            self.assertEqual(prepared, A.CURATED_INPUTS[case_id])

    def test_a_declaration_renders_back_byte_for_byte(self):
        for case_id in self.K.declared_case_ids():
            text = (ROOT / self.K.case_path(case_id)).read_text()
            self.assertEqual(self.K.render(*self.K.read_case(case_id)), text)

    def test_a_case_without_a_declaration_is_refused_by_name(self):
        self.refused(lambda: self.K.read_case("rv64gc-absent-v1"), "no declaration for case rv64gc-absent-v1")

    def test_an_invalid_declaration_is_refused(self):
        text = (ROOT / self.K.case_path(P.CASE_ID)).read_text()
        bad = text.replace('(source_sha256 "a7cbbe', '(source_sha256 "NOTHEX', 1)
        self.assertNotEqual(bad, text)
        self.refused(lambda: self.K.read_document(bad, "invalid"), "source_sha256")

    def test_an_id_that_disagrees_with_its_directory_is_refused(self):
        with tempfile.TemporaryDirectory(dir=ROOT / "target/tmp") as scratch:
            root = Path(scratch)
            (root / "evidence/rv64gc-other-v9").mkdir(parents=True)
            shutil.copy2(ROOT / self.K.case_path(P.CASE_ID), root / "evidence/rv64gc-other-v9/case.sexp")
            self.refused(lambda: self.K.read_case("rv64gc-other-v9", root), "not its directory's rv64gc-other-v9")

    def test_a_control_naming_no_property_is_refused(self):
        text = (ROOT / self.K.case_path(P.CASE_ID)).read_text()
        bad = text.replace('(control (property_id "signed-quotient")', '(control (property_id "no-such-property")', 1)
        self.assertNotEqual(bad, text)
        self.refused(lambda: self.K.read_document(bad, "control"), "the control names no declared property")


def main():
    global MUTATION
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mutation", choices=sorted(SEAMS))
    MUTATION = parser.parse_args().mutation
    (ROOT / "target/tmp").mkdir(parents=True, exist_ok=True)
    result = unittest.TextTestRunner(verbosity=1).run(unittest.defaultTestLoader.loadTestsFromTestCase(CaseTests))
    print(f"MATCHED-GPR-CASE: {result.testsRun} tests / {len(result.failures)} failures / {len(result.errors)} errors; "
          "declarations as data, no capture")
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    raise SystemExit(main())
