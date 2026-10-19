#!/usr/bin/env python3
"""Check the published selected Sail descriptor offline; no capture credit."""
from __future__ import annotations

from copy import deepcopy
import hashlib
from pathlib import Path
import subprocess
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch

import check_sexp_schema as K
import dossier_sexp as D
import matched_gpr_identity as I
import sexp as S

ROOT = Path(__file__).resolve().parent.parent
PARENT = "profiles/rv64gc-lab-v0/references.sexp"
IDENTITY = "profiles/rv64gc-lab-v0/retained/sail-identity.sexp"
SCHEMA = "schema/references.sexp"
IDENTITY_SHA256 = "b0d88c7ae4b3cbb6b856af338811947dd58c6d8e754043d901f2952aeaecea77"
IDENTITY_BYTES = 711


def publication_metadata():
    # Historical publication metadata, never rediscovered on the checking host.
    return dict(
        profile="rv64gc-lab-v0", retrieved="2026-10-19", work_dir="target/refs",
        host=dict(os="Darwin", kernel="27.0.0", arch="arm64",
                  cxx="Apple clang version 21.0.0 (clang-2100.3.34.2)",
                  note="Descriptor publication host; the date is publication, not "
                       "binary acquisition. No execution is attested."),
        path=IDENTITY,
    )


def bounded_bytes(path):
    with path.open("rb") as stream:
        payload = stream.read(I.IDENTITY_BYTES + 1)
    if not 1 <= len(payload) <= I.IDENTITY_BYTES:
        raise ValueError("publication input exceeds its 64 KiB envelope")
    return payload


def selected_parent(root, payload=None):
    """Test-only selection: raw schema before the existing sole dossier mapper."""
    if payload is None:
        payload = bounded_bytes(root / PARENT)
    if type(payload) is not bytes or not 1 <= len(payload) <= I.IDENTITY_BYTES:
        raise ValueError("invalid bounded parent bytes")
    text = payload.decode("utf-8")
    constructs, operators = K.load_schema(root / SCHEMA)
    issues = K.validate_text(text, constructs, operators, PARENT)
    if issues:
        raise ValueError(issues[0])
    forms = [form for form in S.parse(text, PARENT) if form[0] != "comment"]
    if len(forms) != 1 or forms[0][0] != "references":
        raise ValueError("expected one parent references document")
    document = D.references_to_doc(forms[0])
    candidates = [c for c in document.get("candidate", []) if c["id"] == "sail-riscv"]
    if document["profile"] != "rv64gc-lab-v0" or len(candidates) != 1:
        raise ValueError("expected one selected Sail candidate in this profile")
    I.bind_reference_identity(candidates[0])
    return candidates[0]


def identity_input(path=IDENTITY, digest=IDENTITY_SHA256):
    return dict(id="SAIL-IDENTITY", role="reference-identity", path=path, sha256=digest)


class RetainedIdentityTests(unittest.TestCase):
    def setUp(self):
        self.candidate = selected_parent(ROOT)
        self.context = I.bind_reference_identity(self.candidate)
        self.payload = bounded_bytes(ROOT / IDENTITY)
        base = ROOT / "target/retained-sail-identity-controls"
        base.mkdir(parents=True, exist_ok=True)
        temporary = TemporaryDirectory(dir=base)
        self.addCleanup(temporary.cleanup)
        self.temporary = Path(temporary.name)

    def checked_copy(self, payload, *, digest=None, candidate=None):
        path = self.temporary / "identity.sexp"
        path.write_bytes(payload)
        relative = path.relative_to(ROOT).as_posix()
        return I.read_reference_identity(
            ROOT, identity_input(relative, digest or hashlib.sha256(payload).hexdigest()),
            self.candidate if candidate is None else candidate)

    def test_actual_pin_schema_and_exact_selected_projection(self):
        self.assertEqual(len(self.payload), IDENTITY_BYTES)
        self.assertEqual(hashlib.sha256(self.payload).hexdigest(), IDENTITY_SHA256)
        self.assertEqual(I.encode_reference_identity(self.context, **publication_metadata()),
                         self.payload)
        result = I.read_reference_identity(ROOT, identity_input(), self.candidate)
        self.assertEqual((result.disposition, result.pin.disposition), ("matched", "matched"))
        self.assertEqual(result.execution_identity, self.context.fields)
        document = D.references_to_doc(S.parse(self.payload.decode(), IDENTITY)[0])
        self.assertEqual(set(document), {"profile", "retrieved", "work_dir", "host", "candidate"})
        selected = document["candidate"][0]
        self.assertEqual(len(document["candidate"]), 1)
        self.assertEqual(set(selected), set(dict(self.context.fields)) | {"role", "status", "lineage"})
        self.assertEqual(selected["role"], "selected execution identity")
        self.assertEqual(selected["status"], "retained descriptor")
        self.assertEqual(selected["lineage"], "unexamined; no ancestry or independence credit")
        metadata = publication_metadata()
        for field in ("profile", "retrieved", "work_dir", "host"):
            self.assertEqual(document[field], metadata[field])

    def test_changed_current_execution_fields_are_stale_with_matched_pin(self):
        changes = [dict(origin="https://example.invalid/changed"), dict(kind="changed"),
                   dict(binary="other/sail"), dict(binary_sha256="0" * 64),
                   dict(release="changed"), dict(version=""), dict(source_commit="changed"),
                   dict(asset="changed.zip"), dict(asset_sha256="0" * 64)]
        for change in changes:
            with self.subTest(change=change):
                result = I.read_reference_identity(ROOT, identity_input(),
                                                   dict(self.candidate, **change))
                self.assertEqual((result.disposition, result.pin.disposition), ("stale", "matched"))
        absent = dict(self.candidate)
        del absent["release"]
        self.assertEqual(I.read_reference_identity(ROOT, identity_input(), absent).disposition, "stale")

    def test_parent_descriptive_prose_is_excluded(self):
        changed = deepcopy(self.candidate)
        changed.update(role="changed", status="changed", lineage="changed",
                       matched_scope="changed", terms="changed", invocation="changed")
        context = I.bind_reference_identity(changed)
        self.assertEqual(context, self.context)
        self.assertEqual(I.encode_reference_identity(context, **publication_metadata()), self.payload)
        self.assertNotIn(b"matched_scope", self.payload)
        self.assertNotIn(b"experiment", self.payload)

    def test_frozen_selected_context_survives_caller_change(self):
        self.candidate.update(binary_sha256="0" * 64, release="changed")
        self.assertEqual(I.encode_reference_identity(self.context, **publication_metadata()), self.payload)
        result = I.check_reference_identity_bytes(self.payload, path=IDENTITY, context=self.context)
        self.assertEqual(result.disposition, "matched")

    def test_minimal_copy_needs_neither_binary_nor_materials(self):
        for relative in (PARENT, IDENTITY, SCHEMA):
            path = self.temporary / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(bounded_bytes(ROOT / relative))
        self.assertFalse((self.temporary / ".materials").exists())
        self.assertFalse((self.temporary / self.candidate["binary"]).exists())
        self.assertEqual(len(list(self.temporary.rglob("*.sexp"))), 3)
        I._schema.cache_clear()
        try:
            with patch.object(I, "ROOT", self.temporary), \
                    patch.object(subprocess, "Popen", side_effect=AssertionError("process launched")):
                candidate = selected_parent(self.temporary)
                result = I.read_reference_identity(self.temporary, identity_input(), candidate)
                self.assertEqual((result.disposition, result.pin.disposition), ("matched", "matched"))
        finally:
            I._schema.cache_clear()

    def test_changed_retained_bytes_do_not_match_the_original_pin(self):
        result = self.checked_copy(self.payload + b"\n", digest=IDENTITY_SHA256)
        self.assertEqual((result.disposition, result.pin.disposition), ("stale", "mismatch"))

    def test_repinning_changed_execution_identity_still_reports_stale(self):
        changed = dict(self.candidate, binary_sha256="0" * 64)
        payload = I.encode_reference_identity(I.bind_reference_identity(changed), **publication_metadata())
        result = self.checked_copy(payload)
        self.assertEqual((result.disposition, result.pin.disposition), ("stale", "matched"))

    def test_missing_descriptor_is_unavailable(self):
        relative = (self.temporary / "absent.sexp").relative_to(ROOT).as_posix()
        result = I.read_reference_identity(ROOT, identity_input(relative), self.candidate)
        self.assertEqual(result.disposition, "unavailable")

    def test_invalid_descriptor_cannot_succeed_with_a_matching_pin(self):
        for payload in (b"", b"x" * (I.IDENTITY_BYTES + 1), b"(\xff", self.payload + self.payload):
            with self.subTest(size=len(payload)):
                self.assertEqual(self.checked_copy(payload).disposition, "refused")

    def test_parent_raw_schema_precedes_mapping(self):
        with patch.object(D, "references_to_doc", side_effect=AssertionError("mapper reached")):
            for payload in (b"(references (unexpected true))", b"x" * (I.IDENTITY_BYTES + 1)):
                with self.subTest(size=len(payload)), self.assertRaises(ValueError):
                    selected_parent(ROOT, payload)

    def test_emit_and_byte_check_do_not_access_artifacts_or_processes(self):
        with patch.object(I.A, "read_snapshot", side_effect=AssertionError("artifact opened")), \
                patch.object(subprocess, "Popen", side_effect=AssertionError("process launched")):
            self.assertEqual(I.encode_reference_identity(self.context, **publication_metadata()), self.payload)
            result = I.check_reference_identity_bytes(self.payload, path=IDENTITY, context=self.context)
            self.assertEqual(result.disposition, "matched")


def main():
    result = unittest.TextTestRunner(verbosity=1).run(
        unittest.defaultTestLoader.loadTestsFromTestCase(RetainedIdentityTests))
    print(f"RETAINED-SAIL-IDENTITY: {result.testsRun} tests / {len(result.failures)} failures / "
          f"{len(result.errors)} errors; published descriptor, offline, no capture credit")
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    raise SystemExit(main())
