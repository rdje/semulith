#!/usr/bin/env python3
"""Pure expectation-entry controls; metadata binding grants no image validity."""
from __future__ import annotations

import argparse
from dataclasses import FrozenInstanceError, asdict
from pathlib import Path
import subprocess
import sys
import types
import unittest
from unittest import mock

import matched_gpr_comparison as C
import matched_gpr_image as G
import probe_matched_gpr_comparison as P


def document(*, instructions=1, program="fixture.s", entry="0x80000002"):
    doc = P.P.expected([{} for _ in range(instructions)])
    doc.update(program=program, entry=entry)
    return doc


class EntryTests(unittest.TestCase):
    def setUp(self):
        self.doc = document()

    def arguments(self, **kwargs):
        args = dict(payload=P.encode(self.doc), instructions=1, program="fixture.s")
        args.update(kwargs); return args

    def context(self, **kwargs):
        try:
            return C.expectation_image_context(**self.arguments(**kwargs))
        except (C.UnitError, TypeError, AttributeError, KeyError, OSError) as exc:
            self.fail(f"valid context refused as {type(exc).__name__}: {exc}")

    def refused(self, reason, **kwargs):
        try:
            with self.assertRaisesRegex(C.UnitError, reason):
                C.expectation_image_context(**self.arguments(**kwargs))
        except (TypeError, AttributeError, KeyError, OSError) as exc:
            self.fail(f"context refusal escaped as {type(exc).__name__}: {exc}")

    def test_exact_selected_metadata(self):
        self.assertEqual(self.context(), C.ExpectationImageContext("fixture.s", 1, 0x80000002))
        self.assertIs(type(self.context().entry), int)

    def test_entry_zero_and_unsigned_maximum_are_inclusive(self):
        for text, expected in (("0x0", 0), ("0xffffffffffffffff", 18446744073709551615)):
            with self.subTest(text=text):
                self.doc["entry"] = text; self.assertEqual(self.context().entry, expected)

    def test_aliases_and_leading_zeros_preserve_numeric_entry(self):
        for text in ("0X000080000002", "0x" + "0" * 10000 + "80000002"):
            with self.subTest(length=len(text)):
                self.doc["entry"] = text; self.assertEqual(self.context().entry, 2147483650)

    def test_odd_entry_is_metadata_not_alignment_credit(self):
        self.doc["entry"] = "0x1"; self.assertEqual(self.context().entry, 1)

    def test_out_of_rv64_and_non_hex_entries_refuse(self):
        for text in ("0x10000000000000000", "-0x1", "2147483648", "0x", "0xno", " 0x1", "0x1 "):
            with self.subTest(text=text):
                self.doc["entry"] = text; self.refused("hexadecimal RV64")

    def test_entry_is_explicit_without_a_default(self):
        self.doc.pop("entry"); self.refused("explicit string entry")

    def test_wrong_program_refuses_before_entry_metadata(self):
        self.doc.update(program="other.s"); self.doc.pop("entry")
        self.refused("expectation program differs from parent")

    def test_program_is_exact_without_path_inference(self):
        for text in ("Fixture.s", "./fixture.s", "fixture.s "):
            with self.subTest(text=text):
                self.doc["program"] = text; self.refused("expectation program differs from parent")

    def test_missing_parent_program_refuses_before_parser(self):
        with mock.patch.object(C, "_expectation", side_effect=AssertionError("parser entered")):
            self.refused("explicit parent program", program=None)

    def test_invalid_parent_program_refuses_before_parser(self):
        class Label(str): pass
        for value in ("", "x" * 65537, True, 1, [], Label("fixture.s")):
            with self.subTest(kind=type(value).__name__), \
                    mock.patch.object(C, "_expectation", side_effect=AssertionError("parser entered")):
                self.refused("parent program must be a plain string", program=value)

    def test_inclusive_parent_program_limit_and_unicode_label(self):
        for label in ("x" * 65536, "guest Ω / label"):
            with self.subTest(length=len(label)):
                self.doc["program"] = label; self.assertEqual(self.context(program=label).program, label)

    def test_invalid_parent_budget_refuses_before_parser(self):
        for value in (0, -1, 4097, True, False, None, 1.0, "1"):
            with self.subTest(value=value), \
                    mock.patch.object(C, "_expectation", side_effect=AssertionError("parser entered")):
                self.refused("parent budget", instructions=value)

    def test_maximum_complete_parent_budget_is_inclusive(self):
        self.doc = document(instructions=4096)
        self.assertEqual(self.context(instructions=4096), C.ExpectationImageContext("fixture.s", 4096, 2147483650))

    def test_declared_budget_must_equal_selected_budget(self):
        self.refused("instruction budget differs from parent", instructions=2)

    def test_complete_ordered_steps_still_required(self):
        for steps in ([self.doc["step"][0]] * 2, [dict(self.doc["step"][0], n=1)]):
            with self.subTest(count=len(steps)):
                self.doc["step"] = steps; self.refused("complete ordered budget")

    def test_gpr_validation_is_shared_with_the_existing_owner(self):
        for writes in ({"x0": "0x1"}, {"x1": "0x10000000000000000"}):
            with self.subTest(writes=writes):
                self.doc["step"][0]["writes"] = writes; self.refused("canonical x1|hexadecimal RV64")

    def test_invalid_payload_type_and_empty_refuse_before_parser(self):
        for payload in (None, bytearray(b"x"), memoryview(b"x"), "text", b""):
            with self.subTest(kind=type(payload).__name__), \
                    mock.patch.object(C, "_expectation", side_effect=AssertionError("parser entered")):
                self.refused("immutable snapshot|payload outside", payload=payload)

    def test_inclusive_expectation_bytes_and_one_byte_overflow(self):
        valid = P.encode(self.doc)
        payload = b";" + b"x" * (1048576 - len(valid) - 2) + b"\n" + valid
        self.assertEqual(len(payload), 1048576)
        self.assertEqual(self.context(payload=payload).entry, 2147483650)
        with mock.patch.object(C, "_expectation", side_effect=AssertionError("parser entered")):
            self.refused("payload outside", payload=payload + b"x")

    def test_raw_schema_precedes_mapper(self):
        valid = P.encode(self.doc)
        for bad in (valid.replace(b'(entry "0x80000002")', b'(entry 1)'),
                    valid.replace(b'(expectations', b'(expectations (unknown "hidden")', 1),
                    valid.replace(b'(expectations', b'(expectations (instructions 1)', 1)):
            with self.subTest(payload=bad[:60]), \
                    mock.patch.object(C.D, "expectations_to_doc", side_effect=AssertionError("mapper entered")):
                self.refused("shape", payload=bad)

    def test_utf8_and_document_root_refusals(self):
        for payload in (b"\xff", P.encode(self.doc) * 2, b'(comment "only")'):
            with self.subTest(length=len(payload)):
                self.refused("cannot decode/validate|exactly one expectations", payload=payload)

    def test_sole_decoder_receives_exact_bytes_and_selected_budget(self):
        self.doc = document(instructions=2); payload = P.encode(self.doc)
        with mock.patch.object(C, "_expectation", wraps=C._expectation) as decoder, \
                mock.patch.object(C.D, "expectations_to_doc", wraps=C.D.expectations_to_doc) as mapper:
            self.context(payload=payload, instructions=2)
        decoder.assert_called_once_with(payload, 2, "image expectation")
        self.assertEqual(mapper.call_count, 1)

    def test_unsupported_flags_are_only_metadata_here(self):
        self.doc["cross_model"] = False
        self.assertEqual(self.context().entry, 2147483650)

    def test_context_is_frozen_and_contains_only_three_metadata_fields(self):
        context = self.context()
        with self.assertRaises(FrozenInstanceError): context.entry = 0
        self.assertEqual(asdict(context), dict(program="fixture.s", instructions=1, entry=2147483650))
        self.assertFalse(any(isinstance(value, (bytes, bytearray, memoryview)) for value in asdict(context).values()))
        self.assertFalse(hasattr(context, "qualified")); self.assertFalse(hasattr(context, "pin"))

    def test_schema_failure_does_not_yield_context(self):
        with mock.patch.object(C, "_schema", side_effect=OSError("synthetic schema unavailable")):
            self.refused("cannot decode/validate")

    def test_no_artifact_loader_build_process_or_path_write(self):
        with mock.patch.object(C.D, "load_expectations", side_effect=AssertionError("path loader")), \
                mock.patch.object(G, "build_guest_image", side_effect=AssertionError("image built")), \
                mock.patch.object(subprocess, "run", side_effect=AssertionError("process launched")), \
                mock.patch.object(Path, "write_bytes", side_effect=AssertionError("path written")):
            self.context()


MUTATIONS = {
    "required-program": (
        'if program is None:\n        raise UnitError("image context requires an explicit parent program")',
        'if False:\n        raise UnitError("image context requires an explicit parent program")'),
    "program-type": ('if program is not None and (type(program) is not str or not 1 <= len(program) <= 65536):', 'if False:'),
    "budget-cap": P.MUTATIONS["budget-cap"],
    "byte-bounds": P.MUTATIONS["byte-bounds"],
    "payload-type": ('if type(payload) is not bytes:', 'if False:'),
    "payload-forward": ('doc = _expectation(payload, instructions, "image expectation")',
                        'doc = _expectation(b\'(expectations (program "fixture.s") (entry "0x0") (instructions 1) (step (n 0) (insn "x") (derivation "x") (source "x") (writes)))\', instructions, "image expectation")'),
    "budget-forward": ('doc = _expectation(payload, instructions, "image expectation")', 'doc = _expectation(payload, 1, "image expectation")'),
    "raw-schema": P.MUTATIONS["raw-schema"],
    "root-count": P.MUTATIONS["root-count"],
    "step-sequence": P.MUTATIONS["step-sequence"],
    "program-identity": (
        'doc = _expectation(payload, instructions, "image expectation")\n    if doc["program"] != program:',
        'doc = _expectation(payload, instructions, "image expectation")\n    if False:'),
    "explicit-entry": ('if type(entry) is not str:', 'if False:'),
    "rv64-range": P.MUTATIONS["rv64-range"],
    "entry-forward": ('_rv64(entry, "image expectation entry")', '_rv64("0x0", "image expectation entry")'),
    "immutable": ('@dataclass(frozen=True)\nclass ExpectationImageContext:', '@dataclass\nclass ExpectationImageContext:'),
    "metadata-budget": ('ExpectationImageContext(program, instructions, _rv64(entry, "image expectation entry"))',
                        'ExpectationImageContext(program, 0, _rv64(entry, "image expectation entry"))'),
}


def main():
    global C
    parser = argparse.ArgumentParser(description=__doc__); parser.add_argument("--mutation", choices=MUTATIONS)
    args = parser.parse_args()
    if args.mutation:
        source = Path(C.__file__).read_text(); before, after = MUTATIONS[args.mutation]
        if source.count(before) != 1: raise RuntimeError("mutation site count changed")
        module = types.ModuleType("entry_context_mutant"); module.__file__ = C.__file__
        sys.modules[module.__name__] = module
        exec(compile(source.replace(before, after), C.__file__, "exec"), module.__dict__); C = module
    result = unittest.TextTestRunner(verbosity=1).run(unittest.defaultTestLoader.loadTestsFromTestCase(EntryTests))
    print(f"MATCHED-GPR-ENTRY: {result.testsRun} tests / {len(result.failures)} failures / "
          f"{len(result.errors)} errors; metadata only")
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    raise SystemExit(main())
