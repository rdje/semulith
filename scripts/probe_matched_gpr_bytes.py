#!/usr/bin/env python3
"""Frozen-context byte-consumer controls; synthetic data, never method credit."""
from __future__ import annotations

import argparse
from contextlib import ExitStack
from copy import deepcopy
from dataclasses import FrozenInstanceError, replace
from pathlib import Path
import subprocess
import sys
import types
import unittest
from unittest import mock

import matched_gpr_identity as I
import matched_gpr_receipt as R
import probe_matched_gpr_identity as PI
import probe_matched_gpr_receipt as PR
import probe_matched_gpr_files as PF


class ByteTests(unittest.TestCase):
    def setUp(self):
        self.candidate = PI.candidate()
        self.identity_payload = PI.encode(PI.document(self.candidate))
        self.identity = I.bind_reference_identity(self.candidate)
        self.capture, self.args = PR.fixture()
        self.receipt_payload = PR.P.raw(self.capture, "capture")
        self.receipt = R.bind_receipt_context(**self.args)

    def identity_result(self, payload=None, context=None, path="identity.sexp"):
        try:
            return I.check_reference_identity_bytes(
                self.identity_payload if payload is None else payload, path=path,
                context=self.identity if context is None else context)
        except (AttributeError, KeyError, TypeError, ValueError, OSError, AssertionError) as exc:
            self.fail(f"identity boundary escaped as {type(exc).__name__}: {exc}")

    def receipt_result(self, payload=None, context=None):
        try:
            return R.check_receipt_bytes(self.receipt_payload if payload is None else payload,
                                         context=self.receipt if context is None else context)
        except (AttributeError, KeyError, TypeError, ValueError, OSError, AssertionError) as exc:
            self.fail(f"receipt boundary escaped as {type(exc).__name__}: {exc}")

    def no_artifacts(self):
        stack = ExitStack()
        for name in ("read_snapshot", "read_bounded_pin", "read_pinned"):
            stack.enter_context(mock.patch.object(I.A, name, side_effect=AssertionError("artifact I/O")))
        stack.enter_context(mock.patch.object(subprocess, "run", side_effect=AssertionError("process")))
        return stack

    def test_positive_bytes_have_no_authentication_pin(self):
        with self.no_artifacts():
            identity = self.identity_result(); receipt = self.receipt_result()
        self.assertEqual((identity.disposition, receipt.disposition), ("matched", "matched"))
        self.assertIsNone(identity.pin); self.assertIsNone(receipt.pin)
        self.assertEqual(identity.execution_identity, self.identity.fields)
        self.assertEqual(receipt.facts.argv, tuple(self.capture["argv"]))
        self.assertNotIn("authenticated", receipt.reason)
        self.assertIn("authentication/process/method credit pending", receipt.reason)

    def test_binders_do_not_parse_or_read(self):
        with self.no_artifacts(), mock.patch.object(I, "_schema", side_effect=AssertionError("schema")), \
                mock.patch.object(R.F, "_schema", side_effect=AssertionError("schema")):
            self.assertEqual(I.bind_reference_identity(self.candidate), self.identity)
            self.assertEqual(R.bind_receipt_context(**self.args), self.receipt)

    def test_identity_freezes_required_fields(self):
        for field in I.REQUIRED_FIELDS:
            with self.subTest(field=field):
                candidate = PI.candidate(); context = I.bind_reference_identity(candidate)
                candidate[field] = "changed"
                self.assertEqual(self.identity_result(context=context).disposition, "matched")

    def test_identity_freezes_optional_presence_and_value(self):
        for field in I.OPTIONAL_FIELDS:
            with self.subTest(field=field):
                candidate = PI.candidate(); candidate[field] = "b" * 64 if field == "asset_sha256" else "v1"
                payload = PI.encode(PI.document(candidate)); context = I.bind_reference_identity(candidate)
                candidate.pop(field)
                self.assertEqual(self.identity_result(payload, context).disposition, "matched")
                self.assertEqual(self.identity_result(payload, I.bind_reference_identity(candidate)).disposition, "stale")
                candidate[field] = "c" * 64 if field == "asset_sha256" else "v2"
                self.assertEqual(self.identity_result(payload, I.bind_reference_identity(candidate)).disposition, "stale")

    def test_descriptive_fields_are_excluded(self):
        self.candidate.update(status="changed", lineage="changed", extra=["mutable"])
        self.assertEqual(I.bind_reference_identity(self.candidate), self.identity)
        self.assertEqual(self.identity_result().disposition, "matched")

    def test_accepted_string_subclasses_freeze_to_plain_values(self):
        class Label(str):
            pass
        candidate = {field: Label(value) for field, value in self.candidate.items()}
        context = I.bind_reference_identity(candidate)
        with self.subTest(check="plain immutable values"):
            self.assertTrue(all(type(value) is str for _, value in context.fields))
        with self.subTest(check="accepted context roundtrip"):
            self.assertEqual(self.identity_result(context=context).disposition, "matched")
        with self.subTest(check="accepted diagnostic path"):
            self.assertEqual(self.identity_result(path=Label("identity.sexp")).disposition, "matched")

    def test_invalid_identity_binder_raises_before_io(self):
        with self.no_artifacts():
            for field, value in (("id", "other"), ("binary", "../sail"),
                                 ("binary_sha256", "A" * 64), ("release", 7)):
                with self.subTest(field=field):
                    candidate = PI.candidate(); candidate[field] = value
                    with self.assertRaises(I.IdentityError): I.bind_reference_identity(candidate)

    def test_contexts_and_results_are_frozen(self):
        facts = self.receipt_result().facts
        self.assertIsNotNone(facts)
        for value, field in ((self.identity, "fields"), (self.receipt, "argv"),
                             (self.identity_result(), "reason"), (facts, "argv")):
            with self.subTest(field=field), self.assertRaises(FrozenInstanceError):
                setattr(value, field, ())
        self.assertIs(type(self.identity.fields), tuple)
        self.assertTrue(all(type(pair) is tuple for pair in self.identity.fields))
        for field in ("argv", "inputs", "outputs", "receipt"):
            self.assertIs(type(getattr(self.receipt, field)), tuple)

    def test_invalid_identity_context_or_path_refuses_before_parser(self):
        contexts = (object(), self.candidate,
                    replace(self.identity, fields=list(self.identity.fields)),
                    replace(self.identity, fields=self.identity.fields + self.identity.fields),
                    replace(self.identity, fields=(("unknown", "value"),) + self.identity.fields),
                    replace(self.identity, fields=tuple(reversed(self.identity.fields))),
                    replace(self.identity, fields=(("id", 7),) + self.identity.fields[1:]))
        with mock.patch.object(I, "_descriptor", side_effect=AssertionError("parser")):
            for context in contexts:
                with self.subTest(context=context):
                    self.assertEqual(self.identity_result(context=context).disposition, "refused")
            for path in (None, 7, "", "/identity", "../identity", "a//b", "a\\b"):
                with self.subTest(path=path):
                    self.assertEqual(self.identity_result(path=path).disposition, "refused")

    def test_bad_receipt_context_refuses_before_codec(self):
        with mock.patch.object(R.F, "parse_capture", side_effect=AssertionError("codec")):
            self.assertEqual(self.receipt_result(context=self.args).disposition, "refused")

    def test_identity_context_type_and_count_precede_mapping(self):
        contexts = (replace(self.identity, fields=list(self.identity.fields)),
                    replace(self.identity, fields=self.identity.fields * 1000))
        with mock.patch.object(I, "_execution_identity", side_effect=AssertionError("context mapping")):
            for context in contexts:
                with self.subTest(context=context):
                    self.assertEqual(self.identity_result(context=context).disposition, "refused")

    def test_byte_types_and_bounds_precede_schema(self):
        for consumer, payload in ((self.identity_result, self.identity_payload),
                                  (self.receipt_result, self.receipt_payload)):
            with self.subTest(consumer=consumer.__name__):
                exact = payload + b" " * (65536 - len(payload))
                self.assertEqual(consumer(exact).disposition, "matched")
                with mock.patch.object(I, "_schema", side_effect=AssertionError("schema")), \
                        mock.patch.object(R.F, "_schema", side_effect=AssertionError("schema")):
                    for bad in (b"", exact + b" ", bytearray(payload), memoryview(payload), "text"):
                        self.assertEqual(consumer(bad).disposition, "refused")

    def test_malformed_bytes_refuse_without_facts(self):
        for bad in (b"\xff", b"(", b"(references (unknown 1))", b"(capture (unknown 1))"):
            with self.subTest(payload=bad):
                identity = self.identity_result(bad); receipt = self.receipt_result(bad)
                self.assertEqual((identity.disposition, receipt.disposition), ("refused", "refused"))
                self.assertEqual(identity.execution_identity, ()); self.assertIsNone(receipt.facts)

    def test_identity_retains_raw_schema_before_mapper(self):
        bad = self.identity_payload.replace(b'(kind "executable")', b'(kind "executable") (kind "executable")')
        self.assertNotEqual(bad, self.identity_payload)
        with mock.patch.object(I.D, "references_to_doc", side_effect=AssertionError("mapper")):
            self.assertEqual(self.identity_result(bad).disposition, "refused")

    def test_receipt_uses_sole_codec_once(self):
        with mock.patch.object(R.F, "parse_capture", wraps=R.F.parse_capture) as parser:
            self.assertEqual(self.receipt_result().disposition, "matched")
        parser.assert_called_once_with(self.receipt_payload, path="outputs/base.receipt.sexp")

    def test_receipt_freezes_all_used_mutable_context(self):
        self.args["run"].update(id="changed", kind="control", process_exit=-9)
        self.args["run"]["argv"].reverse(); self.args["run"]["input_ids"].clear()
        self.args["run"]["observation_ids"].clear()
        self.args["current_candidate"]["binary_sha256"] = "f" * 64
        for record in self.args["inputs"] + self.args["observations"]: record.clear()
        self.assertEqual(self.receipt_result().disposition, "matched")
        self.assertEqual(self.receipt_result().facts.process_exit, 0)

    def test_receipt_rebinding_detects_used_field_changes(self):
        changes = (("run", "process_exit", -9), ("run", "argv", ["different"]),
                   ("current_candidate", "binary_sha256", "e" * 64))
        for container, field, value in changes:
            with self.subTest(field=field):
                args = deepcopy(self.args); args[container][field] = value
                context = R.bind_receipt_context(**args)
                self.assertEqual(self.receipt_result(context=context).disposition, "refused")
                self.assertEqual(self.receipt_result().disposition, "matched")
        for container, field, value in (("inputs", "sha256", "d" * 64),
                                        ("observations", "byte_size", 999)):
            args = deepcopy(self.args); args[container][0][field] = value
            self.assertEqual(self.receipt_result(context=R.bind_receipt_context(**args)).disposition, "refused")

    def test_coherent_failed_processes_are_bound_data(self):
        for status in (-9, 1, 127):
            with self.subTest(status=status):
                doc, args = PR.fixture(); doc["process_exit"] = args["run"]["process_exit"] = status
                args["run"]["verdict"] = "REFUSED"
                checked = self.receipt_result(PR.P.raw(doc, "capture"), R.bind_receipt_context(**args))
                self.assertEqual(checked.disposition, "matched")
                self.assertEqual(checked.facts.process_exit, status); self.assertIsNone(checked.pin)

    def test_invalid_receipt_binder_raises_before_io(self):
        for field, value in (("argv", ["x"] * 12), ("process_exit", True), ("input_ids", ["missing"])):
            with self.subTest(field=field), self.no_artifacts():
                args = deepcopy(self.args); args["run"][field] = value
                with self.assertRaises(R.BindingError): R.bind_receipt_context(**args)
        args = deepcopy(self.args); args["observations"][0]["path"] = "../trace"
        with self.assertRaises(R.BindingError): R.bind_receipt_context(**args)

    def test_schema_io_dispositions_preserve_existing_contract(self):
        with mock.patch.object(I, "_schema", side_effect=OSError("schema unavailable")):
            self.assertEqual(self.identity_result().disposition, "refused")
        with mock.patch.object(R.F, "_schema", side_effect=OSError("schema unavailable")):
            checked = self.receipt_result()
            self.assertEqual(checked.disposition, "unavailable"); self.assertIsNone(checked.pin)

    def test_legacy_readers_and_byte_checks_share_results(self):
        for cls in (PI.IdentityTests, PR.ReceiptTests):
            # Fixture setup only; invoke the public APIs directly, not another test.
            case = cls(); case.setUp(); self.addCleanup(case.doCleanups)
            if cls is PI.IdentityTests:
                legacy = I.read_reference_identity(case.root, case.record, case.current)
                pure = I.check_reference_identity_bytes(case.path.read_bytes(), path=case.record["path"],
                                                         context=I.bind_reference_identity(case.current))
                self.assertEqual(replace(legacy, pin=None), pure)
            else:
                legacy = R.read_run_receipt(case.root, **case.args)
                pure = R.check_receipt_bytes(case.path.read_bytes(), context=R.bind_receipt_context(**case.args))
                self.assertEqual((legacy.disposition, legacy.facts), (pure.disposition, pure.facts))
                self.assertIsNotNone(legacy.pin); self.assertIsNone(pure.pin)

    def test_exact_declared_snapshots_bind_after_path_and_context_change(self):
        case = PF.FileSetTests(); case.setUp(); self.addCleanup(case.doCleanups)
        graph = case.graph
        identity_record = next(item for item in graph["input"] if item["role"] == "reference-identity")
        case.write(identity_record, PI.encode(PI.document(case.candidate)))
        for run in graph["run"]:
            selected = [item for item in graph["input"] if item["id"] in run["input_ids"]]
            outputs = [item for item in graph["observation"] if item["id"] in run["observation_ids"]]
            receipt = next(item for item in outputs if item["role"] == "process-receipt")
            doc = PR.P.capture()
            doc.update(run_id=run["id"], run_kind=run["kind"], argv=list(run["argv"]),
                       reference_binary_sha256=case.candidate["binary_sha256"],
                       input=[dict(id=item["id"], sha256=item["sha256"]) for item in selected
                              if item is not case.manifest_record],
                       observation=[dict(item) for item in outputs if item is not receipt])
            # The receipt inventory includes the final manifest digest. Publish the
            # unchanged manifest before encoding the receipt; this is fixture setup.
            doc["input"].append(dict(id=case.manifest_record["id"], sha256=case.manifest_record["sha256"]))
            case.write(receipt, PR.P.raw(doc, "capture"))
        identity = I.bind_reference_identity(case.candidate)
        contexts = {run["id"]: R.bind_receipt_context(
            run=run, inputs=[item for item in graph["input"] if item["id"] in run["input_ids"]],
            observations=[item for item in graph["observation"] if item["id"] in run["observation_ids"]],
            current_candidate=case.candidate) for run in graph["run"]}
        # This final evaluation cycle freezes all context before manifest/file I/O.
        case.bind(); bundle = case.result()
        for item in bundle.files:
            if item.data is not None: (case.root / item.path).write_bytes(b"changed later")
        for run in graph["run"]: run["process_exit"] = -9; run["argv"].clear()
        case.candidate.clear()
        with self.no_artifacts():
            checked = I.check_reference_identity_bytes(
                next(item.data for item in bundle.files if item.record_id == identity_record["id"]),
                path=identity_record["path"], context=identity)
            self.assertEqual(checked.disposition, "matched")
            for context in contexts.values():
                receipt_id = dict(context.receipt)["id"]
                payload = next(item.data for item in bundle.files if item.record_id == receipt_id)
                checked = R.check_receipt_bytes(payload, context=context)
                self.assertEqual(checked.disposition, "matched", checked)
                self.assertEqual(checked.facts.process_exit, 0); self.assertIsNone(checked.pin)


MUTATIONS = {
    "identity-freeze": ("I", 'tuple((field, str(value)) for field, value in fields)',
                        'tuple([field, value] for field, value in fields)'),
    "identity-string-freeze": ("I", 'tuple((field, str(value)) for field, value in fields)', 'fields'),
    "identity-context": ("I", 'type(context) is not ReferenceIdentity', 'False'),
    "identity-path": ("I", 'not is_canonical_path(path)', 'False'),
    "identity-fields": ("I", 'type(fields) is not tuple', 'False'),
    "identity-count": ("I", 'len(REQUIRED_FIELDS) <= len(fields) <=\n            len(REQUIRED_FIELDS) + len(OPTIONAL_FIELDS)', 'True'),
    "identity-canonical": ("I", 'if _execution_identity(dict(fields)) != fields:', 'if False:'),
    "identity-parser": ("I", 'return _check_identity(payload, path, fields)',
                        'return IdentityCheck("matched", "omitted", execution_identity=fields)'),
    "identity-frozen": ("I", '@dataclass(frozen=True)\nclass ReferenceIdentity:', '@dataclass\nclass ReferenceIdentity:'),
    "receipt-binder": ("R", 'return _context(run, inputs, observations, current_candidate)',
                       'return _context(run, inputs, observations, dict(current_candidate, binary_sha256="0" * 64))'),
    "receipt-context": ("R", 'if type(context) is not ReceiptContext:', 'if False:'),
    "receipt-parser": ("R", 'checked = _check_receipt(payload, context)',
                       'checked = ReceiptCheck("refused", "omitted")'),
    "receipt-claim": ("R", 'if checked.disposition == "matched":', 'if False:'),
    "receipt-frozen": ("R", '@dataclass(frozen=True)\nclass ReceiptContext:', '@dataclass\nclass ReceiptContext:'),
}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mutation", choices=MUTATIONS); args = parser.parse_args()
    if args.mutation:
        name, before, after = MUTATIONS[args.mutation]; original = globals()[name]
        source = Path(original.__file__).read_text()
        start, end = 0, len(source)
        if name == "I" and args.mutation in {
                "identity-context", "identity-path", "identity-fields",
                "identity-count", "identity-canonical", "identity-parser"}:
            start = source.index("def check_reference_identity_bytes(")
            end = source.index("\n\ndef read_reference_identity(", start)
        selected = source[start:end]
        if selected.count(before) != 1: raise SystemExit("mutation seam is not singular")
        changed = source[:start] + selected.replace(before, after, 1) + source[end:]
        module = types.ModuleType("mutated_bytes_" + name); module.__file__ = original.__file__
        sys.modules[module.__name__] = module
        exec(compile(changed, module.__file__, "exec"), module.__dict__)
        globals()[name] = module
    result = unittest.TextTestRunner(verbosity=1).run(unittest.defaultTestLoader.loadTestsFromTestCase(ByteTests))
    print(f"MATCHED-GPR-BYTES: {result.testsRun} tests / {len(result.failures)} failures / "
          f"{len(result.errors)} errors; synthetic only")
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    raise SystemExit(main())
