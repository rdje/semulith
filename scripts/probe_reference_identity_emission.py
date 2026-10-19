#!/usr/bin/env python3
"""Bounded descriptor emission controls; no binary, process or capture credit."""
from __future__ import annotations

import argparse
from pathlib import Path
import sys
import types
import unittest
from unittest.mock import patch

import matched_gpr_identity as M
import probe_matched_gpr_identity as P


class EmissionTests(unittest.TestCase):
    def setUp(self):
        self.candidate = P.candidate()
        self.context = M.bind_reference_identity(self.candidate)
        self.metadata = dict(
            profile="synthetic", retrieved="2026-10-19", work_dir="captures",
            host=dict(os="fixture", kernel="fixture", arch="fixture", cxx="fixture"),
            path="captures/identity.sexp",
        )

    def emit(self, context=None, **changes):
        arguments = dict(self.metadata, **changes)
        return M.encode_reference_identity(self.context if context is None else context,
                                           **arguments)

    def emitted(self, context=None, **changes):
        try:
            return self.emit(context, **changes)
        except M.IdentityError as exc:
            self.fail("valid descriptor refused: " + str(exc))

    def parse(self, payload):
        return M.D.references_to_doc(M.S.parse(payload.decode(), "descriptor")[0])

    def refuse_before_tools(self, context=None, **changes):
        with patch.object(M.R, "render_forms", side_effect=AssertionError("serializer reached")), \
                patch.object(M, "check_reference_identity_bytes",
                             side_effect=AssertionError("consumer reached")):
            try:
                self.emit(context, **changes)
            except M.IdentityError:
                return
            except Exception as exc:
                self.fail("invalid request escaped as " + type(exc).__name__)
            self.fail("invalid request emitted bytes")

    def test_deterministic_single_candidate_round_trip(self):
        payload = self.emitted()
        self.assertEqual(payload, self.emitted())
        result = M.check_reference_identity_bytes(payload, path=self.metadata["path"],
                                                 context=self.context)
        self.assertEqual(result.disposition, "matched", result.reason)
        self.assertIsNone(result.pin)
        document = self.parse(payload)
        self.assertEqual(len(document["candidate"]), 1)
        self.assertFalse(document.get("experiment"))
        selected = document["candidate"][0]
        self.assertEqual(set(selected), set(M.REQUIRED_FIELDS) | {"role", "status", "lineage"})
        self.assertEqual(dict(result.execution_identity), dict(self.context.fields))
        self.assertEqual(document["host"], self.metadata["host"])

    def test_parent_descriptive_changes_cannot_change_the_projection(self):
        expected = self.emitted()
        self.candidate.update(status="changed", lineage="changed", matched_scope="changed",
                              build_note="changed", role="changed", experiments=[object()])
        self.assertEqual(self.emitted(M.bind_reference_identity(self.candidate)), expected)
        self.assertNotIn(b"changed", expected)

    def test_all_optional_fields_preserve_values_and_empty_presence(self):
        self.candidate.update(release="v1", version="", source_commit="abc",
                              asset="sail.zip", asset_sha256="b" * 64)
        context = M.bind_reference_identity(self.candidate)
        selected = self.parse(self.emitted(context))["candidate"][0]
        for key in M.OPTIONAL_FIELDS:
            self.assertIn(key, selected)
            self.assertEqual(selected[key], self.candidate[key])

    def test_optional_absence_differs_from_present_empty_value(self):
        absent = self.emitted()
        present = M.bind_reference_identity(dict(self.candidate, version=""))
        encoded = self.emitted(present)
        self.assertNotEqual(absent, encoded)
        result = M.check_reference_identity_bytes(encoded, path=self.metadata["path"],
                                                 context=self.context)
        self.assertEqual(result.disposition, "stale")

    def test_bound_context_and_metadata_freeze_before_serialization(self):
        expected = self.emitted()
        self.candidate["binary_sha256"] = "b" * 64
        writer = M.D.references_to_form
        def mutate(document):
            self.metadata["host"]["os"] = "changed during serialization"
            return writer(document)
        with patch.object(M.D, "references_to_form", side_effect=mutate):
            self.assertEqual(self.emitted(), expected)

    def test_inclusive_encoded_byte_ceiling(self):
        host = dict(self.metadata["host"], note="")
        base = self.emitted(host=host)
        host["note"] = "x" * (M.IDENTITY_BYTES - len(base))
        exact = self.emitted(host=host)
        self.assertEqual(len(exact), M.IDENTITY_BYTES)
        host["note"] += "x"
        with self.assertRaises(M.IdentityError):
            self.emit(host=host)

    def test_utf8_quotes_and_control_escaping_round_trip(self):
        host = dict(self.metadata["host"], note='quotes " slash \\ newline\n雪🙂')
        context = M.bind_reference_identity(dict(self.candidate, origin='https://example.invalid/雪"'))
        payload = self.emitted(context, host=host)
        self.assertEqual(self.parse(payload)["host"]["note"], host["note"])
        self.assertEqual(self.parse(payload)["candidate"][0]["origin"], dict(context.fields)["origin"])
        self.assertEqual(payload, self.emitted(context, host=host))

    def test_encoded_expansion_refuses_before_byte_consumer(self):
        for value in ["雪" * (M.IDENTITY_BYTES // 2), "\n" * (M.IDENTITY_BYTES // 2)]:
            with self.subTest(expansion=len(value.encode("utf-8"))), patch.object(
                M, "check_reference_identity_bytes", side_effect=AssertionError("consumer reached")
            ), self.assertRaises(M.IdentityError):
                self.emit(host=dict(self.metadata["host"], note=value))

    def test_aggregate_text_bound_precedes_serialization(self):
        self.refuse_before_tools(profile="x" * (M.IDENTITY_BYTES // 2),
                                 retrieved="y" * (M.IDENTITY_BYTES // 2))

    def test_single_large_field_refuses_before_serialization(self):
        self.refuse_before_tools(host=dict(self.metadata["host"], note="x" * M.IDENTITY_BYTES))
        context = M.bind_reference_identity(dict(self.candidate, origin="x" * M.IDENTITY_BYTES))
        self.refuse_before_tools(context)

    def test_malformed_context_shapes_refuse_before_tools(self):
        class Text(str):
            pass
        fields = self.context.fields
        variants = [object(), M.ReferenceIdentity(None), M.ReferenceIdentity(list(fields)),
                    M.ReferenceIdentity(()), M.ReferenceIdentity(fields * 3),
                    M.ReferenceIdentity((None, *fields[1:])),
                    M.ReferenceIdentity((("id",), *fields[1:])),
                    M.ReferenceIdentity((("id", False), *fields[1:])),
                    M.ReferenceIdentity((("id", Text("sail-riscv")), *fields[1:])),
                    M.ReferenceIdentity((("unknown" * 10000, "x"), *fields[1:])),
                    M.ReferenceIdentity(tuple(reversed(fields))),
                    M.ReferenceIdentity((*fields, fields[0]))]
        for context in variants:
            with self.subTest(kind=type(context)):
                self.refuse_before_tools(context)

    def test_context_shape_and_names_refuse_before_rebinding(self):
        fields = self.context.fields
        for context in [M.ReferenceIdentity(()), M.ReferenceIdentity(fields * 3),
                        M.ReferenceIdentity((("id",), *fields[1:])),
                        M.ReferenceIdentity((("unknown" * 10000, "x"), *fields[1:]))]:
            with self.subTest(fields=len(context.fields)), patch.object(
                M, "bind_reference_identity", side_effect=AssertionError("unbounded binding")
            ):
                self.refuse_before_tools(context)

    def test_invalid_execution_semantics_refuse_before_tools(self):
        for changes in [dict(id="other"), dict(binary="/outside/sail"),
                        dict(binary_sha256="wrong"), dict(asset_sha256="wrong")]:
            candidate = dict(self.candidate, **changes)
            fields = tuple((key, candidate[key]) for key in M.REQUIRED_FIELDS + M.OPTIONAL_FIELDS
                           if key in candidate)
            with self.subTest(changes=tuple(changes)):
                self.refuse_before_tools(M.ReferenceIdentity(fields))

    def test_invalid_metadata_shapes_and_values_refuse_before_tools(self):
        class Text(str):
            pass
        for key in ["profile", "retrieved", "work_dir"]:
            for value in [None, False, 7, "", Text("value")]:
                with self.subTest(key=key, kind=type(value)):
                    self.refuse_before_tools(**{key: value})
        for host in [None, (), {}, dict(self.metadata["host"], extra="x"),
                     dict(self.metadata["host"], note=7),
                     dict(self.metadata["host"], os=""),
                     dict(self.metadata["host"], cxx=None),
                     {**self.metadata["host"], 1: "x"}]:
            with self.subTest(host_kind=type(host)):
                self.refuse_before_tools(host=host)

    def test_unsafe_paths_refuse_before_tools(self):
        for value in [None, False, "", ".", "../x", "/outside", "a//b", "a\\b", "a:b", "a\nb",
                      "x" * (M.IDENTITY_BYTES + 1)]:
            with self.subTest(kind=type(value)):
                self.refuse_before_tools(path=value)
        for value in [".", "/outside", "../outside", "a\\b"]:
            with self.subTest(work_dir=value):
                self.refuse_before_tools(work_dir=value)

    def test_non_utf8_text_refuses_without_consumer_or_partial_output(self):
        with patch.object(M, "check_reference_identity_bytes",
                          side_effect=AssertionError("consumer reached")), self.assertRaises(M.IdentityError):
            self.emit(host=dict(self.metadata["host"], note="\ud800"))

    def test_output_drift_is_rejected_by_existing_byte_owner(self):
        writer = M.D.references_to_form
        def drift(document):
            document["candidate"][0]["binary_sha256"] = "b" * 64
            return writer(document)
        with patch.object(M.D, "references_to_form", side_effect=drift), \
                self.assertRaises(M.IdentityError):
            self.emit()

    def test_schema_unavailability_refuses_emission(self):
        with patch.object(M, "_schema", side_effect=OSError("schema unavailable")), \
                self.assertRaisesRegex(M.IdentityError, "schema unavailable"):
            self.emit()

    def test_no_artifact_or_binary_access(self):
        with patch.object(M.A, "read_snapshot", side_effect=AssertionError("artifact read")), \
                patch.object(M.A.os, "open", side_effect=AssertionError("binary open")):
            payload = self.emitted()
        self.assertIs(type(payload), bytes)
        self.assertFalse(hasattr(payload, "qualified"))


MUTATIONS = {'context-type': ('type(context) is not ReferenceIdentity or type(context.fields) is '
                  'not tuple',
                  'False'),
 'context-shape': ('if (not len(REQUIRED_FIELDS) <= len(fields) <=',
                   'if (False and not len(REQUIRED_FIELDS) <= len(fields) <='),
 'unknown-field': ('if any(key not in REQUIRED_FIELDS + OPTIONAL_FIELDS for key, _ in '
                   'fields):',
                   'if False:'),
 'host-shape': ('if (type(host) is not dict or not 4 <= len(host) <= 5 or',
                'if (False and type(host) is not dict or False and not 4 <= len(host) '
                '<= 5 or'),
 'metadata-type': ('if any(type(value) is not str or not value for value in '
                   'required_text):',
                   'if False:'),
 'text-bound': ('if sum(len(value) for value in text) > IDENTITY_BYTES:', 'if False:'),
 'path-bound': ('if (type(path) is not str or not 1 <= len(path) <= IDENTITY_BYTES or',
                'if (False and type(path) is not str or False and not 1 <= len(path) '
                '<= IDENTITY_BYTES or'),
 'canonical-fields': ('if bind_reference_identity(dict(fields)) != context:',
                      'if False:'),
 'host-freeze': ('host=dict(host))', 'host=host)'),
 'optional-emission': ('selected = dict(fields)',
                       'selected = {key: value for key, value in fields if key in '
                       'REQUIRED_FIELDS}'),
 'encoded-bound': ('if not 1 <= len(payload) <= IDENTITY_BYTES:', 'if False:'),
 'round-trip': ('if checked.disposition != "matched":', 'if False:')}


def main():
    global M
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mutation", choices=MUTATIONS)
    args = parser.parse_args()
    if args.mutation:
        source = Path(M.__file__).read_text()
        before, after = MUTATIONS[args.mutation]
        if source.count(before) != 1:
            raise RuntimeError("emission mutation seam count changed")
        module = types.ModuleType("mutated_identity_emission")
        module.__file__ = M.__file__
        sys.modules[module.__name__] = module
        exec(compile(source.replace(before, after, 1), module.__file__, "exec"), module.__dict__)
        M = module
    result = unittest.TextTestRunner(verbosity=1).run(
        unittest.defaultTestLoader.loadTestsFromTestCase(EmissionTests))
    print(f"REFERENCE-IDENTITY-EMISSION: {result.testsRun} tests / {len(result.failures)} failures / "
          f"{len(result.errors)} errors; synthetic descriptor metadata, no capture credit")
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    sys.exit(main())
