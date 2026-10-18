#!/usr/bin/env python3
"""Fresh synthetic process/receipt controls; no Sail or qualification credit."""
from __future__ import annotations

import argparse
from dataclasses import replace
import errno
import hashlib
import os
from pathlib import Path
import sys
import tempfile
import types
import unittest
from unittest import mock

import matched_gpr_collector as C
import matched_gpr_artifacts as F
import matched_gpr_receipt as R
from probe_matched_gpr_collector import Fixture

ROOT = Path(__file__).resolve().parent.parent


class PublicationTests(unittest.TestCase):
    def setUp(self):
        base = ROOT / "target/p4-system-14/a42w/fixtures"
        base.mkdir(parents=True, exist_ok=True)
        directory = tempfile.TemporaryDirectory(dir=base)
        self.addCleanup(directory.cleanup)
        self.f = Fixture(Path(directory.name))

    def publish(self, disposition="recorded", request=None):
        try:
            result = C.capture_run_with_receipt(
                self.f.root, request=request or self.f.request()
            )
        except (
            AttributeError,
            IndexError,
            KeyError,
            TypeError,
            ValueError,
            OSError,
            AssertionError,
        ) as exc:
            self.fail("publication escaped as " + type(exc).__name__ + ": " + str(exc))
        self.assertEqual(result.disposition, disposition, result)
        self.assertFalse(hasattr(result, "qualified"))
        if disposition != "recorded":
            self.assertIsNone(result.receipt)
        return result

    def test_fresh_receipt_roundtrip_binds_all_actual_fields(self):
        request = self.f.request()
        result = self.publish(request=request)
        payload = self.f.path("process-receipt").read_bytes()
        doc = F.parse_capture(payload, path=result.receipt.path)
        self.assertEqual(doc["run_id"], request.run_id)
        self.assertEqual(doc["run_kind"], "baseline")
        self.assertEqual(doc["argv"], list(request.argv))
        self.assertEqual(doc["process_exit"], result.process.process_exit)
        self.assertEqual(doc["reference_candidate_id"], "sail-riscv")
        self.assertEqual(doc["reference_binary_sha256"], request.binary_sha256)
        collector = next(i for i in request.inputs if i.role == "collector")
        self.assertEqual(doc["collector_input_id"], collector.input_id)
        self.assertEqual(
            doc["input"], [dict(id=i.input_id, sha256=i.sha256) for i in request.inputs]
        )
        self.assertEqual(
            doc["observation"],
            [
                dict(
                    id=i.observation_id,
                    role=i.role,
                    path=i.path,
                    byte_size=i.byte_size,
                    sha256=i.sha256,
                )
                for i in result.process.outputs
            ],
        )
        self.assertEqual(set(doc["host"]), {"os", "kernel", "arch"})
        self.assertTrue(all(doc["host"].values()))
        self.assertEqual(
            doc["tool"][:2],
            [
                dict(id="collector", version="sha256:" + collector.sha256),
                dict(id="reference", version="sha256:" + request.binary_sha256),
            ],
        )
        self.assertEqual(doc["tool"][2]["id"], "python")
        self.assertEqual(result.receipt.byte_size, len(payload))
        self.assertEqual(result.receipt.sha256, hashlib.sha256(payload).hexdigest())
        self.assertLessEqual(len(payload), R.RECEIPT_BYTES)
        run = dict(self.f.runs["baseline"], process_exit=result.process.process_exit)
        outputs = [
            dict(
                id=i.observation_id,
                role=i.role,
                path=i.path,
                byte_size=i.byte_size,
                sha256=i.sha256,
            )
            for i in (*result.process.outputs, result.receipt)
        ]
        check = R.read_run_receipt(
            self.f.root,
            run=run,
            inputs=[
                dict(id=i.input_id, role=i.role, path=i.path, sha256=i.sha256)
                for i in request.inputs
            ],
            observations=outputs,
            current_candidate=self.f.candidate,
        )
        self.assertEqual(check.disposition, "matched", check)
        self.assertEqual(check.facts.process_exit, 0)

    def test_repeat_and_control_are_separate_fresh_receipts(self):
        results = [
            self.publish(request=self.f.request(kind))
            for kind in ("baseline", "repeat", "control")
        ]
        self.assertEqual(len({r.process.pid for r in results}), 3)
        for result, kind in zip(results, ("baseline", "repeat", "control")):
            doc = F.parse_capture(
                (self.f.root / result.receipt.path).read_bytes(),
                path=result.receipt.path,
            )
            self.assertEqual(doc["run_kind"], kind)
            self.assertEqual(doc["process_exit"], 0)

    def test_failed_and_signal_exits_preserved_as_failed_data(self):
        for mode, status in [("failed", 7), ("signal", -15)]:
            with self.subTest(mode=mode):
                self.f.mode(mode)
                result = self.publish()
                doc = F.parse_capture(
                    self.f.path("process-receipt").read_bytes(),
                    path=result.receipt.path,
                )
                self.assertEqual(result.process.process_exit, status)
                self.assertEqual(doc["process_exit"], status)

    def test_missing_output_propagates_without_stale_receipt(self):
        self.f.mode("missing")
        result = self.publish("unavailable")
        self.assertEqual(result.process.disposition, "unavailable")
        self.assertEqual(result.process.process_exit, 0)
        self.assertFalse(self.f.path("process-receipt").exists())

    def test_invalid_request_refuses_before_process_or_io(self):
        request = replace(self.f.request(), argv=("bad",))
        with mock.patch.object(
            C, "capture_run", side_effect=AssertionError("unexpected collection")
        ):
            self.publish("refused", request)

    def test_request_and_host_freeze_before_collection(self):
        request = self.f.request()
        original = C.capture_run
        import platform

        host = types.SimpleNamespace(
            system="original OS", release="original kernel", machine="original arch"
        )

        def collecting(*args, **kwargs):
            object.__setattr__(request, "run_id", "changed")
            host.system = "changed OS"
            return original(*args, **kwargs)

        with mock.patch.object(
            C, "capture_run", side_effect=collecting
        ), mock.patch.object(platform, "uname", return_value=host):
            result = self.publish(request=request)
        doc = F.parse_capture(
            self.f.path("process-receipt").read_bytes(), path=result.receipt.path
        )
        self.assertEqual(doc["run_id"], self.f.runs["baseline"]["id"])
        self.assertEqual(doc["host"]["os"], "original OS")

    def test_output_change_between_collection_and_publication_refuses(self):
        original = C.capture_run

        def collecting(*args, **kwargs):
            result = original(*args, **kwargs)
            self.f.path("raw-gpr").write_bytes(b"changed trace")
            return result

        with mock.patch.object(C, "capture_run", side_effect=collecting):
            self.publish("refused")
        self.assertFalse(self.f.path("process-receipt").exists())

    def test_output_change_after_write_refuses_and_removes_owned_receipt(self):
        original = os.fsync

        def syncing(fd):
            original(fd)
            self.f.path("raw-gpr").write_bytes(b"changed trace")

        with mock.patch.object(C.os, "fsync", side_effect=syncing):
            self.publish("refused")
        self.assertFalse(self.f.path("process-receipt").exists())

    def test_receipt_conflict_preserves_existing_bytes(self):
        original = C.capture_run

        def collecting(*args, **kwargs):
            result = original(*args, **kwargs)
            self.f.path("process-receipt").write_bytes(b"existing foreign receipt")
            return result

        with mock.patch.object(C, "capture_run", side_effect=collecting):
            self.publish("refused")
        self.assertEqual(
            self.f.path("process-receipt").read_bytes(), b"existing foreign receipt"
        )

    def test_receipt_symlink_preserves_target(self):
        original = C.capture_run
        sentinel = self.f.root / "sentinel"
        sentinel.write_bytes(b"protected")

        def collecting(*args, **kwargs):
            result = original(*args, **kwargs)
            self.f.path("process-receipt").symlink_to("../sentinel")
            return result

        with mock.patch.object(C, "capture_run", side_effect=collecting):
            self.publish("refused")
        self.assertEqual(sentinel.read_bytes(), b"protected")
        self.assertTrue(self.f.path("process-receipt").is_symlink())

    def test_nested_git_parent_after_collection_refuses(self):
        original = C.capture_run

        def collecting(*args, **kwargs):
            result = original(*args, **kwargs)
            (self.f.path("process-receipt").parent / ".git").write_bytes(
                b"foreign boundary"
            )
            return result

        with mock.patch.object(C, "capture_run", side_effect=collecting):
            self.publish("refused")
        self.assertFalse(self.f.path("process-receipt").exists())

    def test_short_writes_publish_complete_receipt(self):
        original = os.write

        def writing(fd, payload):
            return original(fd, payload[:17])

        with mock.patch.object(C.os, "write", side_effect=writing):
            result = self.publish()
        self.assertEqual(
            self.f.path("process-receipt").stat().st_size, result.receipt.byte_size
        )
        F.parse_capture(
            self.f.path("process-receipt").read_bytes(), path=result.receipt.path
        )

    def test_no_progress_write_refuses_and_cleans_partial(self):
        with mock.patch.object(C.os, "write", return_value=0):
            self.publish("refused")
        self.assertFalse(self.f.path("process-receipt").exists())

    def test_partial_write_error_is_unavailable_and_cleans_partial(self):
        original = os.write
        calls = 0

        def writing(fd, payload):
            nonlocal calls
            calls += 1
            if calls > 1:
                raise OSError(errno.ENOSPC, "synthetic disk full")
            return original(fd, payload[:17])

        with mock.patch.object(C.os, "write", side_effect=writing):
            self.publish("unavailable")
        self.assertFalse(self.f.path("process-receipt").exists())

    def test_replaced_receipt_refuses_without_deleting_replacement(self):
        original = os.fsync

        def syncing(fd):
            original(fd)
            self.f.path("process-receipt").unlink()
            self.f.path("process-receipt").write_bytes(b"replacement")

        with mock.patch.object(C.os, "fsync", side_effect=syncing):
            self.publish("refused")
        self.assertTrue(self.f.path("process-receipt").exists())
        self.assertEqual(self.f.path("process-receipt").read_bytes(), b"replacement")

    def test_codec_failure_refuses_before_receipt_write(self):
        def encoding(doc, **kwargs):
            raise F.ArtifactError("synthetic codec failure")

        with mock.patch.object(F, "encode_capture", side_effect=encoding):
            self.publish("refused")
        self.assertFalse(self.f.path("process-receipt").exists())

    def test_schema_io_is_unavailable_without_receipt(self):
        with mock.patch.object(
            F, "encode_capture", side_effect=OSError(errno.EIO, "schema I/O")
        ):
            self.publish("unavailable")
        self.assertFalse(self.f.path("process-receipt").exists())

    def test_byte_checker_tool_io_remains_unavailable(self):
        with mock.patch.object(
            R,
            "check_receipt_bytes",
            return_value=R.ReceiptCheck("unavailable", "schema unavailable"),
        ):
            self.publish("unavailable")
        self.assertFalse(self.f.path("process-receipt").exists())

    def test_oversized_encoded_payload_refuses_before_write(self):
        with mock.patch.object(
            F, "encode_capture", return_value=b"X" * (R.RECEIPT_BYTES + 1)
        ), mock.patch.object(
            R,
            "check_receipt_bytes",
            side_effect=AssertionError("oversize reached parser"),
        ):
            self.publish("refused")
        self.assertFalse(self.f.path("process-receipt").exists())

    def test_damaged_receipt_bytes_refuse_and_clean_owned_inode(self):
        original = os.fsync

        def syncing(fd):
            original(fd)
            os.pwrite(fd, b"X", 0)

        with mock.patch.object(C.os, "fsync", side_effect=syncing):
            self.publish("refused")
        self.assertFalse(self.f.path("process-receipt").exists())

    def test_contradictory_encoded_exit_refuses_byte_binding(self):
        original = F.encode_capture

        def encoding(doc, **kwargs):
            return original(dict(doc, process_exit=99), **kwargs)

        with mock.patch.object(F, "encode_capture", side_effect=encoding):
            self.publish("refused")
        self.assertFalse(self.f.path("process-receipt").exists())

    def test_wrong_output_metadata_cannot_publish(self):
        original = C.capture_run

        def collecting(*args, **kwargs):
            result = original(*args, **kwargs)
            return replace(
                result,
                outputs=(
                    replace(result.outputs[0], path="elsewhere"),
                    *result.outputs[1:],
                ),
            )

        with mock.patch.object(C, "capture_run", side_effect=collecting):
            self.publish("refused")
        self.assertFalse(self.f.path("process-receipt").exists())

    def test_publication_read_bounds_and_no_payload_retention(self):
        original = C.A.read_bounded_pin
        calls = []

        def reading(*args, **kwargs):
            pin = original(*args, **kwargs)
            if args[1] == "observation":
                calls.append((args[2]["id"], kwargs["max_bytes"]))
                self.assertFalse(hasattr(pin, "data"))
            return pin

        with mock.patch.object(C.A, "read_bounded_pin", side_effect=reading):
            self.publish()
        expected = [
            (
                self.f.observation("baseline", role)["id"],
                C.TRACE_BYTES if role == "raw-gpr" else C.STREAM_BYTES,
            )
            for role in C.E.OUTPUT_ROLES[:3]
        ]
        self.assertEqual(
            calls,
            expected
            + [
                (
                    self.f.observation("baseline", "process-receipt")["id"],
                    R.RECEIPT_BYTES,
                )
            ]
            + expected,
        )


MUTATIONS = {
    "request-freeze": (
        "        request = _freeze(request)\n        _need(\n            max_read_bytes is None",
        "        _need(\n            max_read_bytes is None",
    ),
    "host-freeze": (
        "            host=host,",
        '            host=dict(os=platform.uname().system, kernel=host["kernel"], arch=host["arch"]),',
    ),
    "actual-exit": (
        "            process_exit=process.process_exit,\n            reference_candidate_id=",
        "            process_exit=0,\n            reference_candidate_id=",
    ),
    "receipt-bound": (
        "type(payload) is bytes and 0 < len(payload) <= R.RECEIPT_BYTES",
        "type(payload) is bytes and 0 < len(payload)",
    ),
    "byte-binding": ('if checked.disposition != "matched":', "if False:"),
    "pre-outputs": (
        "        outputs()\n        with ExitStack()",
        "        # omitted\n        with ExitStack()",
    ),
    "post-outputs": (
        "                outputs()\n                _check_parents(chain)",
        "                # omitted\n                _check_parents(chain)",
    ),
    "exclusive-write": (
        "fd = os.open(\n                name,\n                os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW,",
        "fd = os.open(\n                name,\n                os.O_WRONLY | os.O_CREAT | os.O_TRUNC | os.O_NOFOLLOW,",
    ),
    "partial-cleanup": (
        "                if not complete:",
        "                if False:",
    ),
    "cleanup-identity": (
        "if (info.st_dev, info.st_ino) == (\n                            created.st_dev,\n                            created.st_ino,\n                        ):",
        "if True:",
    ),
    "receipt-pin": (
        '            pin = A.read_bounded_pin(root, "observation", record, max_bytes=cap)',
        '            if "role" not in record: return\n            pin = A.read_bounded_pin(root, "observation", record, max_bytes=cap)',
    ),
}


def real_sail_smoke():
    """Reuse the public acquisition/guest smoke with fresh receipt publication."""
    import contextlib
    import io
    import json
    import probe_matched_gpr_collector as live

    original = C.capture_run
    receipts = []

    def collect(root, *, request):
        # Delegate the old smoke's one-process seam to the new public wrapper.
        # Restore its lower-level dependency during this call to avoid recursion.
        with mock.patch.object(C, "capture_run", original):
            result = C.capture_run_with_receipt(root, request=request)
        if result.disposition != "recorded":
            raise ValueError(str(result))
        item = result.receipt
        payload = (root / item.path).read_bytes()
        doc = F.parse_capture(payload, path=item.path)
        if (len(payload), hashlib.sha256(payload).hexdigest()) != (
            item.byte_size,
            item.sha256,
        ):
            raise ValueError("live receipt pin differs")
        if doc["process_exit"] != result.process.process_exit or doc["argv"] != list(
            request.argv
        ):
            raise ValueError("live receipt execution differs")
        receipts.append(
            dict(kind=doc["run_kind"], bytes=item.byte_size, sha256=item.sha256)
        )
        return result.process

    captured = io.StringIO()
    with contextlib.redirect_stdout(captured), mock.patch.object(
        C, "capture_run", collect
    ):
        status = live.real_sail_smoke()
    if status:
        print(captured.getvalue(), end="")
        return status
    report = json.loads(captured.getvalue().splitlines()[0])
    if len(receipts) != 3 or [r["kind"] for r in receipts] != [
        "baseline",
        "repeat",
        "control",
    ]:
        raise ValueError("live receipt census differs")
    report.update(
        receipt_writer="three fresh bounded receipts published", receipts=receipts
    )
    print(json.dumps(report, sort_keys=True))
    print(
        "LIVE RECEIPT SMOKE: three fresh processes/receipts, AGREE AGREE DIVERGE; scratch removed, qualification closed"
    )
    return 0


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mutation", choices=sorted(MUTATIONS))
    parser.add_argument("--real-sail-smoke", action="store_true")
    args = parser.parse_args()
    if args.real_sail_smoke:
        if args.mutation:
            parser.error("live smoke cannot use a mutation")
        return real_sail_smoke()
    global C
    if args.mutation:
        source = Path(C.__file__).read_text()
        before, after = MUTATIONS[args.mutation]
        if source.count(before) != 1:
            raise SystemExit("mutation seam not singular: " + args.mutation)
        module = types.ModuleType("publication_mutant")
        module.__file__ = C.__file__
        sys.modules[module.__name__] = module
        exec(
            compile(source.replace(before, after, 1), C.__file__, "exec"),
            module.__dict__,
        )
        C = module
        import probe_matched_gpr_collector as fixtures

        fixtures.C = module
    result = unittest.TextTestRunner(stream=sys.stdout, verbosity=0).run(
        unittest.defaultTestLoader.loadTestsFromTestCase(PublicationTests)
    )
    print(
        f"MATCHED-GPR-PUBLICATION: {result.testsRun} tests / {len(result.failures)} failures / {len(result.errors)} errors; synthetic process receipts, qualification closed"
    )
    return int(not result.wasSuccessful())


if __name__ == "__main__":
    raise SystemExit(main())
