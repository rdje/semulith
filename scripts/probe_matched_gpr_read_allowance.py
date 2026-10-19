#!/usr/bin/env python3
"""Real artifact reads under delegated limits; synthetic observations, no capture credit."""

from __future__ import annotations

import argparse
from contextlib import contextmanager
import os
from pathlib import Path
import sys
import tempfile
import types
import unittest
from unittest.mock import patch

import matched_gpr_evaluation as E
import matched_gpr_manifest as M
import probe_matched_gpr_property_evaluation as P

ROOT = Path(__file__).resolve().parent.parent


class AllowanceTests(unittest.TestCase):
    def setUp(self):
        base = ROOT / "target/matched-gpr-read-allowance-controls"
        base.mkdir(parents=True, exist_ok=True)
        temporary = tempfile.TemporaryDirectory(dir=base)
        self.addCleanup(temporary.cleanup)
        self.f = P.Fixture(Path(temporary.name))
        self.manifest_record = self.f.inputs["dependency-manifest"]
        self.manifest_path = self.f.root / self.manifest_record["path"]
        records = [
            *self.f.graph["input"],
            self.f.child,
            self.f.normative,
            *self.f.graph["observation"],
        ]
        self.paths = {record["path"] for record in records}
        self.needed = sum((self.f.root / path).stat().st_size for path in self.paths)

    @contextmanager
    def reads(self):
        """Count actual artifact payload bytes, including failed reads; no supplied totals."""
        original = os.read
        observed = []

        def read(fd, count):
            data = original(fd, count)
            observed.append(len(data))
            return data

        with patch.object(E.A.os, "read", side_effect=read):
            yield observed

    def evaluate(self, **changes):
        arguments = self.f.arguments()
        arguments.update(changes)
        return E.evaluate_retained_unit(self.f.root, **arguments)

    def manifest(self, **changes):
        arguments = dict(
            experiment=self.f.experiment, current_candidate=self.f.candidate
        )
        arguments.update(changes)
        return M.read_dependency_manifest(self.f.root, **arguments)

    def test_default_matches_explicit_full_allowance(self):
        default = self.evaluate()
        explicit = self.evaluate(max_read_bytes=E.Q.MAX_READ_BYTES)
        self.assertEqual(default, explicit)
        self.assertEqual(default.disposition, "pending", default.reason)
        self.assertEqual(default.source_property.disposition, "matched")
        self.assertEqual(default.authentication.charged_read_bytes, self.needed)
        self.assertLessEqual(
            default.authentication.snapshot_bytes, E.Q.MAX_SNAPSHOT_BYTES
        )
        self.assertFalse(hasattr(default, "qualified"))

    def test_manifest_default_and_exact_file_allowance_match(self):
        default = self.manifest()
        with self.reads() as actual:
            exact = self.manifest(max_read_bytes=self.manifest_path.stat().st_size)
        self.assertEqual(default, exact)
        self.assertEqual(exact.disposition, "matched", exact.reason)
        self.assertEqual(sum(actual), exact.pin.byte_size)

    def test_manifest_zero_and_short_allowances_read_no_payload(self):
        for limit in [0, self.manifest_path.stat().st_size - 1]:
            with self.subTest(limit=limit), self.reads() as actual:
                result = self.manifest(max_read_bytes=limit)
                self.assertEqual(result.disposition, "refused", result.reason)
                self.assertIsNone(result.plan)
                self.assertEqual(sum(actual), 0)

    def test_evaluation_zero_and_preseed_short_allowances_read_no_payload(self):
        for limit in [0, 1, self.manifest_path.stat().st_size - 1]:
            with self.subTest(limit=limit), self.reads() as actual:
                result = self.evaluate(max_read_bytes=limit)
                self.assertEqual(result.disposition, "refused", result.reason)
                self.assertIsNone(result.authentication)
                self.assertIsNone(result.source_property)
                self.assertEqual(sum(actual), 0)

    def test_exact_aggregate_allowance_authenticates_every_byte_once(self):
        with self.reads() as actual:
            result = self.evaluate(max_read_bytes=self.needed)
        self.assertEqual(result.disposition, "pending", result.reason)
        self.assertEqual(result.authentication.charged_read_bytes, self.needed)
        self.assertEqual(result.authentication.authenticated_bytes, self.needed)
        self.assertEqual(sum(actual), self.needed)
        self.assertEqual(len(result.authentication.files), len(self.paths))

    def test_one_byte_short_aggregate_cannot_reset_the_allowance(self):
        limit = self.needed - 1
        with self.reads() as actual:
            result = self.evaluate(max_read_bytes=limit)
        self.assertEqual(result.disposition, "refused", result.reason)
        self.assertIsNotNone(result.authentication)
        self.assertLessEqual(sum(actual), limit)
        self.assertLessEqual(result.authentication.charged_read_bytes, limit)
        self.assertGreaterEqual(result.authentication.charged_read_bytes, sum(actual))
        self.assertIsNone(result.source_property)

    def test_remaining_collection_allowance_shares_the_fixed_total(self):
        # This models a caller's already charged collection, not a real Sail run.
        collected = E.Q.MAX_READ_BYTES - self.needed
        for debit, expected in [(collected, "pending"), (collected + 1, "refused")]:
            remaining = E.Q.MAX_READ_BYTES - debit
            with self.subTest(debit=debit), self.reads() as actual:
                result = self.evaluate(max_read_bytes=remaining)
                self.assertEqual(result.disposition, expected, result.reason)
                self.assertLessEqual(debit + sum(actual), E.Q.MAX_READ_BYTES)
                self.assertLessEqual(
                    debit + result.authentication.charged_read_bytes, E.Q.MAX_READ_BYTES
                )

    def test_invalid_evaluation_limits_refuse_before_record_validation(self):
        class Integer(int):
            pass

        for limit in [
            False,
            True,
            -1,
            E.Q.MAX_READ_BYTES + 1,
            1 << 100000,
            None,
            "0",
            0.0,
            Integer(1),
        ]:
            with self.subTest(kind=type(limit)), patch.object(
                E.V, "check_experiment", side_effect=OSError("record/schema I/O")
            ) as validator:
                try:
                    result = self.evaluate(max_read_bytes=limit)
                except TypeError as exc:
                    self.fail(f"invalid allowance escaped validation: {exc}")
                self.assertEqual(validator.call_count, 0)
                self.assertEqual(result.disposition, "refused")
                self.assertEqual(result.record.disposition, "unchecked")
                self.assertIsNone(result.manifest)

    def test_invalid_manifest_limits_refuse_before_binding(self):
        class Integer(int):
            pass

        for limit in [
            False,
            True,
            -1,
            M.F.DOCUMENT_BYTES + 1,
            1 << 100000,
            None,
            "0",
            0.0,
            Integer(1),
        ]:
            with self.subTest(kind=type(limit)), patch.object(
                M.R,
                "bind_relations",
                return_value=types.SimpleNamespace(
                    disposition="unsupported", reason="binding reached"
                ),
            ) as binder:
                try:
                    result = self.manifest(max_read_bytes=limit)
                except TypeError as exc:
                    self.fail(f"invalid allowance escaped validation: {exc}")
                self.assertEqual(binder.call_count, 0)
                self.assertEqual(result.disposition, "refused")
                self.assertIsNone(result.pin)
                self.assertIsNone(result.plan)

    def test_full_allowance_is_clamped_to_the_manifest_document_envelope(self):
        read = M.A.read_snapshot
        seen = []

        def observe(root, kind, record, **kwargs):
            if record["id"] == self.manifest_record["id"]:
                seen.append(kwargs["max_bytes"])
            return read(root, kind, record, **kwargs)

        with patch.object(E.A, "read_snapshot", side_effect=observe):
            result = self.evaluate(max_read_bytes=E.Q.MAX_READ_BYTES)
        self.assertEqual(result.disposition, "pending", result.reason)
        self.assertEqual(seen, [M.F.DOCUMENT_BYTES])

    def test_manifest_document_ceiling_is_inclusive_and_never_exceeded(self):
        original = self.manifest_path.read_bytes()
        cap = M.F.DOCUMENT_BYTES
        payload = original + b";" + b"x" * (cap - len(original) - 1)
        self.f.write(self.manifest_record, payload)
        with self.reads() as actual:
            result = self.manifest(max_read_bytes=cap)
        self.assertEqual(result.disposition, "matched", result.reason)
        self.assertEqual(sum(actual), cap)
        self.f.write(self.manifest_record, payload + b"x")
        with self.reads() as actual:
            result = self.manifest(max_read_bytes=cap)
        self.assertEqual(result.disposition, "refused", result.reason)
        self.assertEqual(sum(actual), 0)

    def test_failed_manifest_pin_is_terminal_without_hidden_reads(self):
        data = self.manifest_path.read_bytes()
        self.manifest_path.write_bytes(data.replace(b"input", b"Input", 1))
        with self.reads() as actual, patch.object(
            E.Q, "read_declared_files", side_effect=AssertionError("file set reached")
        ):
            result = self.evaluate(max_read_bytes=self.needed)
        self.assertEqual(result.disposition, "stale", result.reason)
        self.assertIsNone(result.authentication)
        self.assertIsNone(result.source_property)
        self.assertEqual(sum(actual), len(data))

    def test_preledger_refusal_does_not_report_the_earlier_seed_charge(self):
        self.f.observation("baseline", "raw-gpr")["byte_size"] = E.C.TRACE_BYTES + 1
        with self.reads() as actual:
            result = self.evaluate(max_read_bytes=self.needed)
        self.assertEqual(result.disposition, "refused", result.reason)
        self.assertEqual(result.record.disposition, "valid")
        self.assertEqual(result.manifest.disposition, "matched")
        self.assertIsNotNone(result.authentication)
        self.assertEqual(result.authentication.disposition, "refused")
        self.assertEqual(result.authentication.charged_read_bytes, 0)
        self.assertEqual(sum(actual), result.manifest.pin.byte_size)
        self.assertGreater(sum(actual), 0)
        self.assertIsNone(result.source_property)
        # This counter cannot refund a caller's reservation: it omits the seed.

    def test_missing_child_retains_conservative_charging(self):
        (self.f.root / self.f.normative["path"]).unlink()
        with self.reads() as actual:
            result = self.evaluate(max_read_bytes=self.needed)
        self.assertEqual(result.disposition, "unavailable", result.reason)
        self.assertIsNone(result.source_property)
        self.assertLessEqual(sum(actual), result.authentication.charged_read_bytes)
        self.assertLessEqual(result.authentication.charged_read_bytes, self.needed)

    def test_changed_child_cannot_earn_credit_or_borrow_another_budget(self):
        path = self.f.root / self.f.normative["path"]
        data = path.read_bytes()
        path.write_bytes(bytes([data[0] ^ 1]) + data[1:])
        with self.reads() as actual:
            result = self.evaluate(max_read_bytes=self.needed)
        self.assertEqual(result.disposition, "stale", result.reason)
        self.assertIsNone(result.source_property)
        self.assertLessEqual(sum(actual), result.authentication.charged_read_bytes)
        self.assertLessEqual(result.authentication.charged_read_bytes, self.needed)


MUTATIONS = {
    "evaluation-type": ("E", "type(max_read_bytes) is not int", "False", 1),
    "evaluation-domain": (
        "E",
        "not 0 <= max_read_bytes <= Q.MAX_READ_BYTES",
        "False",
        1,
    ),
    "manifest-type": ("M", "type(max_read_bytes) is not int", "False", 1),
    "manifest-domain": ("M", "not 0 <= max_read_bytes <= F.DOCUMENT_BYTES", "False", 1),
    "initial-allowance": (
        "E",
        "min(max_read_bytes, Artifacts.DOCUMENT_BYTES)",
        "Artifacts.DOCUMENT_BYTES",
        1,
    ),
    "manifest-envelope": (
        "E",
        "min(max_read_bytes, Artifacts.DOCUMENT_BYTES)",
        "max_read_bytes",
        1,
    ),
    "file-allowance": (
        "E",
        "max_read_bytes=max_read_bytes, retain_source_image=True",
        "max_read_bytes=Q.MAX_READ_BYTES, retain_source_image=True",
        1,
    ),
    "seed-double-charge": (
        "E",
        "max_read_bytes=max_read_bytes, retain_source_image=True",
        "max_read_bytes=max_read_bytes - manifest.pin.byte_size, retain_source_image=True",
        1,
    ),
    "manifest-read-cap": (
        "M",
        "max_bytes=max_read_bytes)",
        "max_bytes=F.DOCUMENT_BYTES)",
        1,
    ),
    "manifest-extra-byte": (
        "M",
        "max_bytes=max_read_bytes)",
        "max_bytes=max_read_bytes + 1)",
        1,
    ),
}


def main():
    global E, M
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mutation", choices=sorted(MUTATIONS))
    args = parser.parse_args()
    if args.mutation:
        target, before, after, count = MUTATIONS[args.mutation]
        original = E if target == "E" else M
        source = Path(original.__file__).read_text()
        if source.count(before) != count:
            raise RuntimeError("allowance mutation seam count changed")
        module = types.ModuleType("mutated_read_allowance_" + target)
        module.__file__ = original.__file__
        sys.modules[module.__name__] = module
        exec(
            compile(source.replace(before, after), module.__file__, "exec"),
            module.__dict__,
        )
        if target == "E":
            E = module
        else:
            # Only function guards change; preserve shared public dataclass identity.
            for name in ["ManifestCheck", "ManifestPlan", "_Context"]:
                setattr(module, name, getattr(original, name))
            M = module
            E.M = module
    result = unittest.TextTestRunner(verbosity=1).run(
        unittest.defaultTestLoader.loadTestsFromTestCase(AllowanceTests)
    )
    print(
        f"MATCHED-GPR-READ-ALLOWANCE: {result.testsRun} tests / {len(result.failures)} failures / "
        f"{len(result.errors)} errors; actual bounded reads, synthetic observations, no capture credit"
    )
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    sys.exit(main())
