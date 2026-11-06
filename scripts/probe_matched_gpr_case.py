#!/usr/bin/env python3
"""Controls for the matched cases' declarations as data (scripts/matched_gpr_case.py; P4-SYSTEM.14 a44-2a, a44-2b).

Every declared case reads as declared and renders back byte for byte. The tools read the data (a44-2b): the
review's case and the capture command's pins are the declaration's, field for field, and each declaration
agrees with the retained planned record and dependency manifest its capture declared. A missing declaration,
an invalid one, one whose id disagrees with its directory and one whose control names no property are each
refused. `--mutation NAME` removes one refusal or binding from a copy of the module and the suite must lose
the tests that refusal or binding holds.
"""
from __future__ import annotations

import argparse
import importlib.util
from pathlib import Path
import re
import shutil
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
import capture_div as A  # noqa: E402
import matched_gpr_property as P  # noqa: E402
import sexp as S  # noqa: E402

MODULE = ROOT / "scripts/matched_gpr_case.py"
SEAMS = {
    "delivery-binding": ("        if (word is None) != (length is None) or (word is None and (writes or fetches not in (0, 1))):\n", "        if False:\n"),
    "delivery-render": ('fetched = "" if word is None else ', 'fetched = " (word 0) (length 0)" if word is None else '),
    "missing-refusal": ("    if not path.is_file():\n", "    if False:\n"),
    "id-binding": ('    if declaration["id"] != case_id:\n', "    if False:\n"),
    "control-binding": ('    if declaration["control"]["property_id"] not in {row[0] for row in declaration["properties"]}:\n',
                        "    if False:\n"),
    "schema": ("    if errors:\n", "    if False:\n"),
    "value-mapping": ('item["register"], item["expected"], item["statement"])',
                      'item["register"], 0, item["statement"])'),
}
# The cases whose capture declared a planned record and a dependency manifest; a declared case without them
# is named here when it lands, never skipped silently.
# Sorted. The 23 superseded directories left the tree at P4-SYSTEM.14 a49-4, each listed with its last commit in the book's retired-cases page.
PLANNED = ("rv64gc-alu-imm-v2", "rv64gc-alu-reg-v2", "rv64gc-atomics-v1", "rv64gc-c-forms-v1", "rv64gc-counters-v2", "rv64gc-csr-access-v2", "rv64gc-csr-set-v3", "rv64gc-d-forms-v1", "rv64gc-ecall-ebreak-v2", "rv64gc-f-forms-v1", "rv64gc-fencei-v2", "rv64gc-ialign-16-v2", "rv64gc-jalr-lsb-v2", "rv64gc-load-ext-v2", "rv64gc-load-x0-v2", "rv64gc-lui-auipc-v2", "rv64gc-m-forms-v3", "rv64gc-m-forms-v7", "rv64gc-no-delay-slots-v2", "rv64gc-shamt-v2", "rv64gc-signed-div-truncation-v2", "rv64gc-sstc-v2", "rv64gc-wsuffix-v2", "rv64gc-xlen-forms-v4", "rv64gc-zicntr-v3")
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
        self.assertEqual(ids, P.reviewed_case_ids())
        for case_id in ids:
            self.assertEqual(self.K.read_case(case_id)["id"], case_id)

    def test_the_review_reads_each_case_from_its_declaration(self):
        for case_id in P.reviewed_case_ids():
            d, case = self.K.read_case(case_id), P.reviewed_case(case_id)
            a = case.authority
            self.assertEqual(
                (case.case_id, case.profile_id, case.program, case.instructions, case.source_size, case.source_sha256,
                 case.requirement_id, case.obligation_ids, case.contract_id, case.contract_version,
                 case.control_property_id, case.control_value, case.control_reason, case.control_id,
                 case.control_statement, case.limitation, case.reviewed_steps, case.source_id, case.source_locator, case.category, case.risk, case.coverage),
                tuple(d[name] for name in ("id", "profile_id", "program", "instructions", "source_size",
                                           "source_sha256", "requirement_id", "obligation_ids", "contract_id",
                                           "contract_version"))
                + (d["control"]["property_id"], d["control"]["value"], d["control"]["reason"], d["control"]["id"],
                   d["control"]["statement"], d["limitation"],
                   d["steps"], d["source_id"], d["source_locator"], d["category"], d["risk"], d["coverage"]))
            self.assertEqual(tuple((item.property_id, item.cell, item.witness.step_n, item.witness.register,
                                    item.expected_value, item.statement) for item in case.properties),
                             d["properties"])
            self.assertEqual((a.profile_id, a.requirement_id, a.requirement_semantic_sha256, a.obligation_id,
                              a.obligation_semantic_sha256, a.source_id, a.source_sha256),
                             (d["profile_id"], d["requirement_id"], d["authority"]["requirement_semantic_sha256"],
                              d["authority"]["obligation_id"], d["authority"]["obligation_semantic_sha256"],
                              d["source_id"], d["authority"]["source_sha256"]))
            self.assertEqual(tuple((item.role, item.input_id, item.path, item.sha256) for item in case.required_inputs),
                             d["required_inputs"])
            self.assertEqual(A.prepared_inputs(case_id),
                             tuple((role, identity, A.prefix(case_id) + "/" + name, size, digest)
                                   for role, identity, name, size, digest in d["prepared"]) + (A.IDENTITY_ROW,))

    def test_each_declaration_agrees_with_its_retained_planned_record(self):
        ids = tuple(case_id for case_id in self.K.declared_case_ids()
                    if (ROOT / "evidence" / case_id / "planned-experiment.sexp").is_file())
        self.assertEqual(ids, PLANNED)
        for case_id in ids:
            d = self.K.read_case(case_id)
            directory = ROOT / "evidence" / case_id
            experiment = next(form for form in S.parse((directory / "planned-experiment.sexp").read_text())
                              if isinstance(form, list) and form and str(form[0]) == "experiment")
            graph = S.children(experiment, "verification")[0]
            self.assertEqual((S.field(experiment, "program"), S.field(experiment, "instructions")),
                             (d["program"], d["instructions"]))
            planned = sorted((S.field(item, "id"), S.field(item, "statement"),
                              S.field(S.children(item, "gpr_witness")[0], "step_n"),
                              S.field(S.children(item, "gpr_witness")[0], "register"))
                             for item in S.children(graph, "property"))
            self.assertEqual(planned, sorted((identity, statement, step, register)
                                             for identity, _, step, register, _, statement in d["properties"]))
            control = S.children(graph, "control_run")[0]
            self.assertEqual(([child[1] for child in S.children(control, "property_ids")], S.field(control, "reason")),
                             ([d["control"]["property_id"]], d["control"]["reason"]))
            if d["control"]["id"] is not None:  # declared since a43b-2b (D1): the record carries the case's own words
                self.assertEqual((S.field(control, "id"), S.field(experiment, "control")),
                                 (d["control"]["id"], d["control"]["statement"]))
            self.assertIn(d["limitation"], [child[1] for child in S.children(graph, "limitations")])
            inputs = {(S.field(item, "role"), S.field(item, "id"), S.field(item, "path"), S.field(item, "sha256"))
                      for item in S.children(graph, "input")}
            self.assertIn(("guest-source", "guest-source", "profiles/rv64gc-lab-v0/guests/" + d["program"],
                           d["source_sha256"]), inputs)
            for role, identity, name, _, digest in d["prepared"]:
                self.assertIn((role, identity, "evidence/" + case_id + "/" + name, digest), inputs)
            manifest = next(form for form in S.parse((directory / "dependencies.sexp").read_text())
                            if isinstance(form, list) and form and str(form[0]) != "comment")
            children = {(S.field(item, "role"), S.field(item, "id"), S.field(item, "path"), S.field(item, "sha256"))
                        for item in S.children(manifest, "input")}
            for row in d["required_inputs"]:
                self.assertIn(row, children)

    def test_a_declaration_renders_back_byte_for_byte(self):
        for case_id in self.K.declared_case_ids():
            text = (ROOT / self.K.case_path(case_id)).read_text()
            self.assertEqual(self.K.render(self.K.read_case(case_id)), text)

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

    def first_step(self, fields):
        """The declaration of a case whose first step carries exactly these fields after its pc."""
        text = (ROOT / self.K.case_path(P.CASE_ID)).read_text()
        pc = re.search(r"\(step \(n 0\) \(pc (\S+?)\)", text).group(1)
        row = "  (step (n 0) (pc " + pc + ") " + fields + ")\n"
        changed, count = re.subn(r"  \(step \(n 0\) [^\n]*\n", row, text)
        self.assertEqual(count, 1)
        return changed

    def test_a_delivery_boundary_reads_bare_and_renders_back(self):
        """The typed event binding (P4-SYSTEM.14 a43e-1): a delivered interrupt is a boundary with no word and no length."""
        text = self.first_step("(fetches 0)")
        declaration = self.K.read_document(text, "boundary")
        self.assertEqual(declaration["steps"][0][2:], (None, None, 0, ()))
        self.assertEqual(self.K.render(declaration), text)

    def test_a_fetch_fault_boundary_may_read_one_parcel(self):
        """A straddling fetch reads its first parcel and faults at its second: no word retires, and nothing is written (a49-1)."""
        text = self.first_step("(fetches 1)")
        declaration = self.K.read_document(text, "boundary")
        self.assertEqual(declaration["steps"][0][2:], (None, None, 1, ()))
        self.assertEqual(self.K.render(declaration), text)

    def test_a_step_half_fetched_or_writing_without_a_word_is_refused(self):
        for fields in ("(word 19) (fetches 0)", "(length 4) (fetches 0)", "(fetches 2)", "(fetches 0) (write (register 1) (value 1))", "(fetches 1) (write (register 1) (value 1))"):
            with self.subTest(fields=fields):
                self.refused(lambda: self.K.read_document(self.first_step(fields), "half"), "must fetch a word of a length")

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
