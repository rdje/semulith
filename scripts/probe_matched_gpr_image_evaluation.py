#!/usr/bin/env python3
"""On-volume authenticated image-composition controls; never qualification evidence."""
from __future__ import annotations

import argparse
from copy import deepcopy
from dataclasses import fields, is_dataclass
import gc
import hashlib
from pathlib import Path
import sys
import tempfile
import types
import unittest
from unittest import mock
import weakref

import matched_gpr_evaluation as E
import probe_matched_gpr_evaluation as P

ROOT = Path(__file__).resolve().parent.parent


def has_payload(value):
    if isinstance(value, (bytes, bytearray, memoryview)):
        return True
    if is_dataclass(value):
        return any(has_payload(getattr(value, field.name)) for field in fields(value))
    if isinstance(value, (tuple, list)):
        return any(has_payload(item) for item in value)
    if isinstance(value, dict):
        return any(has_payload(item) for item in (*value.keys(), *value.values()))
    return False


class ImageEvaluationTests(unittest.TestCase):
    def setUp(self):
        base = ROOT / "target/p4-system-14/a42d3b/fixtures"
        base.mkdir(parents=True, exist_ok=True)
        temporary = tempfile.TemporaryDirectory(dir=base)
        self.addCleanup(temporary.cleanup)
        self.f = P.Fixture(Path(temporary.name))

    def outcome(self, disposition="pending", reason=None):
        try:
            checked = E.evaluate_retained_unit(self.f.root, **self.f.arguments())
        except (AttributeError, IndexError, KeyError, TypeError, ValueError, OSError, AssertionError) as exc:
            self.fail(f"image evaluation escaped as {type(exc).__name__}: {exc}")
        detail = (checked.reason, checked.comparison.reason if checked.comparison else None)
        self.assertEqual(checked.disposition, disposition, detail)
        if reason:
            self.assertIn(reason, checked.reason)
        self.assertFalse(has_payload(checked))
        return checked

    def content(self, disposition="pending", image="matched", reason=None):
        checked = self.outcome(disposition, reason)
        self.assertEqual(checked.record.disposition, "valid")
        self.assertIsNotNone(checked.authentication)
        self.assertEqual(checked.authentication.disposition, "matched")
        self.assertIsNotNone(checked.comparison)
        self.assertEqual(checked.comparison.disposition, "satisfied")
        self.assertIsNotNone(checked.source_image)
        self.assertEqual(checked.source_image.disposition, image)
        return checked

    def repin(self, role, payload):
        self.f.write(self.f.inputs[role], payload)
        self.f.publish_receipts()

    def expectations(self, **fields):
        for role, doc in (("expectation", self.f.base), ("mutant-expectation", self.f.control)):
            for key, value in fields.items():
                if value is None:
                    doc.pop(key, None)
                else:
                    doc[key] = value
            self.f.write(self.f.inputs[role], P.PC.encode(doc))
        self.f.publish_receipts()

    def trace(self, payload):
        self.f.trace = payload
        for kind in self.f.runs:
            self.f.write(self.f.observation(kind, "raw-gpr"), payload)
        self.f.publish_receipts()

    def test_positive_retains_separate_frozen_metadata_without_qualification(self):
        checked = self.content(reason="complete method/policy adequacy pending")
        self.assertEqual((checked.source_image.facts.program, checked.source_image.facts.entry),
                         (self.f.experiment["program"], self.f.entry))
        self.assertEqual(checked.source_image.facts.source_sha256, self.f.inputs["guest-source"]["sha256"])
        self.assertEqual(checked.source_image.facts.image_sha256, self.f.inputs["guest-image"]["sha256"])
        self.assertEqual(tuple(item.check.disposition for item in checked.receipts), ("matched",) * 3)
        self.assertFalse(hasattr(checked, "qualified"))

    def test_old_positional_result_fields_keep_their_meaning(self):
        comparison = E.C.ComparisonUnit("unsupported", "synthetic")
        checked = E.EvaluationCheck("unsupported", "legacy", E.RecordCheck("valid"),
                                    None, None, None, (), comparison)
        self.assertIs(checked.comparison, comparison)
        self.assertIsNone(checked.source_image)

    def test_exact_authenticated_snapshots_and_context_reach_each_owner_once(self):
        label = "renamed / synthetic Ω.s"
        self.f.experiment["program"] = label
        self.expectations(program=label)
        source = (self.f.root / self.f.inputs["guest-source"]["path"]).read_bytes()
        image = (self.f.root / self.f.inputs["guest-image"]["path"]).read_bytes()
        expected = (self.f.root / self.f.inputs["expectation"]["path"]).read_bytes()
        with mock.patch.object(E.C, "expectation_image_context", wraps=E.C.expectation_image_context) as context, \
                mock.patch.object(E.F, "check_source_image", wraps=E.F.check_source_image) as checking:
            checked = self.content()
        context.assert_called_once_with(expected, instructions=1, program=label)
        checking.assert_called_once_with(source, image, program=label, entry=self.f.entry)
        self.assertEqual(checked.source_image.facts.program, label)

    def test_two_boundary_budget_is_forwarded_without_a_one_step_default(self):
        self.f.experiment["instructions"] = 2
        for run in self.f.runs.values():
            run["argv"][4] = "2"
        self.f.source = b"addi x1, x0, 1\naddi x2, x0, 2\n"
        self.f.image = P.G.build_guest_image(self.f.source, program=self.f.experiment["program"], entry=self.f.entry).image
        self.f.write(self.f.inputs["guest-source"], self.f.source)
        self.f.write(self.f.inputs["guest-image"], self.f.image)
        self.f.base = P.PC.P.expected([{"x1": "0x1"}, {"x2": "0x2"}])
        self.f.base.update(program=self.f.experiment["program"], entry=hex(self.f.entry))
        for step, insn in zip(self.f.base["step"], ("addi x1, x0, 1", "addi x2, x0, 2")):
            step["insn"] = insn
        self.f.control = deepcopy(self.f.base)
        self.f.control["step"][0]["writes"]["x1"] = "0x2"
        self.expectations()
        self.trace(b"[0] [M]: 0x0000000080000000 (0x00100093) addi x1, x0, 1\nx1 <- 0x0000000000000001\n"
                   b"[1] [M]: 0x0000000080000004 (0x00200113) addi x2, x0, 2\nx2 <- 0x0000000000000002\n")
        with mock.patch.object(E.C, "expectation_image_context", wraps=E.C.expectation_image_context) as context:
            self.content()
        self.assertEqual(context.call_count, 1)
        self.assertEqual(context.call_args.kwargs["instructions"], 2)

    def test_nondefault_halfword_entry_rebuilds_the_selected_image(self):
        entry = self.f.entry + 2
        image = P.G.build_guest_image(self.f.source, program=self.f.experiment["program"], entry=entry).image
        self.repin("guest-image", image)
        self.expectations(entry=hex(entry))
        self.trace(self.f.trace.replace(b"0x0000000080000000", b"0x0000000080000002"))
        checked = self.content()
        self.assertEqual(checked.source_image.facts.entry, entry)

    def test_one_read_per_declared_file_including_the_manifest_seed(self):
        with mock.patch.object(E.A, "read_snapshot", wraps=E.A.read_snapshot) as snapshots, \
                mock.patch.object(E.A, "read_bounded_pin", wraps=E.A.read_bounded_pin) as pins, \
                mock.patch.object(E.Q, "read_declared_files", wraps=E.Q.read_declared_files) as ledger:
            checked = self.content()
        calls = [*snapshots.call_args_list, *pins.call_args_list]
        paths = [call.args[2]["path"] for call in calls]
        self.assertEqual((snapshots.call_count, pins.call_count), (19, 3))
        self.assertEqual(len(paths), len(set(paths)))
        self.assertEqual(paths.count(self.f.inputs["dependency-manifest"]["path"]), 1)
        self.assertIs(ledger.call_args.kwargs["retain_source_image"], True)
        total = sum(path.stat().st_size for path in self.f.root.rglob("*") if path.is_file())
        self.assertEqual((checked.authentication.authenticated_bytes, checked.authentication.charged_read_bytes),
                         (total, total))
        limits = {call.args[2]["id"]: call.kwargs["max_bytes"] for call in snapshots.call_args_list}
        self.assertEqual((limits["guest-source"], limits["guest-image"]), (1048576, 65536))

    def test_snapshot_summary_counts_seventeen_payloads_and_excludes_unused_room(self):
        reader = E.Q.read_declared_files
        measured = []
        def read(*args, **kwargs):
            bundle = reader(*args, **kwargs)
            payloads = [fact.data for fact in bundle.files if fact.data is not None]
            measured.append((len(payloads), sum(map(len, payloads)), bundle.retained_bytes))
            return bundle
        with mock.patch.object(E.Q, "read_declared_files", side_effect=read):
            checked = self.content()
        self.assertEqual(measured, [(17, checked.authentication.snapshot_bytes, checked.authentication.snapshot_bytes)])

    def test_return_releases_the_authenticated_bundle(self):
        reader = E.Q.read_declared_files
        references = []
        def read(*args, **kwargs):
            bundle = reader(*args, **kwargs)
            references.append(weakref.ref(bundle))
            return bundle
        with mock.patch.object(E.Q, "read_declared_files", side_effect=read):
            checked = self.content()
        gc.collect()
        self.assertIsNone(references[0]())
        self.assertFalse(has_payload(checked))

    def test_later_source_and_image_path_changes_cannot_replace_authenticated_bytes(self):
        reader = E.Q.read_declared_files
        def read(*args, **kwargs):
            bundle = reader(*args, **kwargs)
            (self.f.root / self.f.inputs["guest-source"]["path"]).write_bytes(b"addi x1, x0, 2\n")
            (self.f.root / self.f.inputs["guest-image"]["path"]).write_bytes(b"changed after authentication")
            return bundle
        with mock.patch.object(E.Q, "read_declared_files", side_effect=read):
            self.content()
        self.assertEqual(self.outcome("stale").authentication.disposition, "stale")

    def test_parent_program_mutation_after_selection_cannot_change_image_context(self):
        reading = E.M.read_dependency_manifest
        def read(*args, **kwargs):
            result = reading(*args, **kwargs)
            kwargs["experiment"]["program"] = "changed after freeze"
            return result
        with mock.patch.object(E.M, "read_dependency_manifest", side_effect=read):
            checked = self.content()
        self.assertEqual(checked.source_image.facts.program, self.f.experiment["program"])

    def test_missing_entry_refuses_after_a_satisfied_comparison_before_build(self):
        self.expectations(entry=None)
        with mock.patch.object(E.F, "check_source_image", side_effect=AssertionError("image consumer entered")):
            checked = self.outcome("refused", "image context")
        self.assertEqual(checked.comparison.disposition, "satisfied")
        self.assertEqual(checked.authentication.disposition, "matched")
        self.assertIsNone(checked.source_image)

    def test_malformed_and_out_of_range_entries_refuse_as_context_findings(self):
        for entry in ("0xno", "-0x1", "2147483648", "0x10000000000000000"):
            with self.subTest(entry=entry):
                self.expectations(entry=entry)
                checked = self.outcome("refused", "image context")
                self.assertEqual(checked.comparison.disposition, "satisfied")
                self.assertIsNone(checked.source_image)

    def test_odd_entry_is_a_separate_builder_content_refusal(self):
        self.expectations(entry="0x80000001")
        checked = self.content("refused", "refused", "source/image")
        self.assertIsNone(checked.source_image.facts)

    def test_entry_mismatch_keeps_both_image_fingerprints(self):
        self.expectations(entry="0x80000004")
        checked = self.content("refused", "refused", "supplied ELF bytes differ")
        self.assertIsNotNone(checked.source_image.facts)
        self.assertEqual(checked.source_image.facts.entry, self.f.entry + 4)
        self.assertNotEqual(checked.source_image.facts.image_sha256, checked.source_image.facts.rebuilt_image_sha256)

    def test_repinned_complete_elf_header_padding_payload_and_sections_must_match(self):
        original = self.f.image
        for offset in (24, 200, 4096, len(original) - 1):
            with self.subTest(offset=offset):
                changed = bytearray(original); changed[offset] ^= 1
                self.repin("guest-image", bytes(changed))
                checked = self.content("refused", "refused", "supplied ELF bytes differ")
                self.assertIsNotNone(checked.source_image.facts)
                self.assertEqual(checked.source_image.facts.image_sha256, hashlib.sha256(changed).hexdigest())
                self.assertNotEqual(checked.source_image.facts.image_sha256, checked.source_image.facts.rebuilt_image_sha256)

    def test_repinned_changed_source_cannot_reuse_the_old_elf(self):
        self.repin("guest-source", b"addi x1, x0, 2\n")
        self.content("refused", "refused", "supplied ELF bytes differ")

    def test_byte_equivalent_source_comments_match_with_the_new_source_fingerprint(self):
        source = b"# synthetic extra comment\n" + self.f.source
        self.repin("guest-source", source)
        checked = self.content()
        self.assertEqual(checked.source_image.facts.source_sha256, hashlib.sha256(source).hexdigest())
        self.assertEqual(checked.source_image.facts.image_sha256, hashlib.sha256(self.f.image).hexdigest())

    def test_empty_authenticated_source_is_a_separate_content_refusal(self):
        self.repin("guest-source", b"")
        self.content("refused", "refused", "source/image")

    def test_empty_authenticated_image_refuses_before_reconstruction(self):
        self.repin("guest-image", b"")
        with mock.patch.object(E.F.G, "build_guest_image", side_effect=AssertionError("image built")):
            self.content("refused", "refused", "image must be plain bytes")

    def test_inclusive_source_cap_can_match(self):
        source = b"#" + b"x" * (1048576 - len(self.f.source) - 2) + b"\n" + self.f.source
        self.assertEqual(len(source), 1048576)
        self.repin("guest-source", source)
        self.content()

    def test_inclusive_image_cap_authenticates_but_extra_bytes_fail_correspondence(self):
        image = self.f.image + b"\0" * (65536 - len(self.f.image))
        self.repin("guest-image", image)
        self.content("refused", "refused", "supplied ELF bytes differ")

    def test_source_and_image_overflow_refuse_in_authentication_before_consumers(self):
        for role, size in (("guest-source", 1048577), ("guest-image", 65537)):
            original = (self.f.root / self.f.inputs[role]["path"]).read_bytes()
            try:
                with self.subTest(role=role):
                    self.repin(role, b"x" * size)
                    with mock.patch.object(E.F, "check_source_image", side_effect=AssertionError("image consumer")):
                        checked = self.outcome("refused", "files")
                    self.assertIsNone(checked.comparison)
                    self.assertIsNone(checked.source_image)
                    self.assertEqual(checked.authentication.snapshot_bytes, 0)
            finally:
                self.repin(role, original)

    def test_unavailable_construction_keeps_satisfied_comparison_and_authentication(self):
        with mock.patch.object(E.F.G, "build_guest_image", side_effect=E.F.G.ImageUnavailable("synthetic unavailable")):
            checked = self.content("unavailable", "unavailable", "source/image")
        self.assertIsNone(checked.source_image.facts)

    def test_unexpected_programming_failures_propagate(self):
        with mock.patch.object(E.F.G, "build_guest_image", side_effect=RuntimeError("synthetic programming failure")), \
                self.assertRaisesRegex(RuntimeError, "synthetic programming failure"):
            E.evaluate_retained_unit(self.f.root, **self.f.arguments())

    def test_failed_comparison_precedes_invalid_entry_or_unavailable_image_tools(self):
        self.f.runs["baseline"].update(process_exit=1, verdict="REFUSED")
        self.expectations(entry="0xno")
        with mock.patch.object(E.C, "expectation_image_context", side_effect=AssertionError("entry consumer")), \
                mock.patch.object(E.F, "check_source_image", side_effect=AssertionError("image consumer")):
            checked = self.outcome("failed")
        self.assertEqual(checked.comparison.disposition, "failed")
        self.assertIsNone(checked.source_image)

    def test_unsupported_comparison_precedes_invalid_entry_or_image_tools(self):
        self.expectations(cross_model=False, entry="0xno")
        with mock.patch.object(E.C, "expectation_image_context", side_effect=AssertionError("entry consumer")), \
                mock.patch.object(E.F, "check_source_image", side_effect=AssertionError("image consumer")):
            checked = self.outcome("unsupported")
        self.assertEqual(checked.comparison.disposition, "unsupported")
        self.assertIsNone(checked.source_image)


MUTATIONS = {
    "retention": ('retain_source_image=True)', 'retain_source_image=False)'),
    "context-budget": ('instructions=execution.instructions, program=program)', 'instructions=1, program=program)'),
    "context-program": ('instructions=execution.instructions, program=program)', 'instructions=execution.instructions, program="synthetic.s")'),
    "context-validation": ('image_context = C.expectation_image_context(\n            _payload(files, "input", execution.baseline_expectation.input_id),\n            instructions=execution.instructions, program=program)',
                           'image_context = C.ExpectationImageContext(program, execution.instructions, 0x80000000)'),
    "context-refusal": ('except C.UnitError as exc:\n        return finish("refused", "image context: " + str(exc), identity=identity,\n                      receipts=tuple(receipts), comparison=comparison)', 'except C.UnitError:\n        raise'),
    "source-selection": ('_payload(files, "input", source_input.input_id)', '_payload(files, "input", image_input.input_id)'),
    "image-selection": ('_payload(files, "input", image_input.input_id)', '_payload(files, "input", source_input.input_id)'),
    "source-reopen": ('_payload(files, "input", source_input.input_id)', '(root / source_input.path).read_bytes()'),
    "image-reopen": ('_payload(files, "input", image_input.input_id)', '(root / image_input.path).read_bytes()'),
    "entry-forward": ('program=image_context.program, entry=image_context.entry)', 'program=image_context.program, entry=0x80000000)'),
    "image-label": ('program=image_context.program, entry=image_context.entry)', 'program="synthetic.s", entry=image_context.entry)'),
    "image-status": ('if source_image.disposition != "matched":', 'if False:'),
    "image-finding": ('identity, receipts, comparison, source_image)', 'identity, receipts, comparison, None)'),
    "comparison-order": P.MUTATIONS["comparison-status"],
}


def main():
    global E
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mutation", choices=MUTATIONS)
    args = parser.parse_args()
    if args.mutation:
        source = Path(E.__file__).read_text(); before, after = MUTATIONS[args.mutation]
        if source.count(before) != 1:
            raise RuntimeError("mutation site count changed")
        module = types.ModuleType("image_evaluation_mutant"); module.__file__ = E.__file__
        sys.modules[module.__name__] = module
        exec(compile(source.replace(before, after), E.__file__, "exec"), module.__dict__)
        E = module
    result = unittest.TextTestRunner(verbosity=1).run(unittest.defaultTestLoader.loadTestsFromTestCase(ImageEvaluationTests))
    print(f"MATCHED-GPR-IMAGE-EVALUATION: {result.testsRun} tests / {len(result.failures)} failures / "
          f"{len(result.errors)} errors; synthetic only")
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    raise SystemExit(main())
