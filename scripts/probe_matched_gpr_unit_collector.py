#!/usr/bin/env python3
"""Real synthetic children test shared unit limits; no canonical/qualification credit."""
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
import matched_gpr_unit_collector as U
import matched_gpr_artifacts as F
from probe_matched_gpr_collector import Fixture

ROOT = Path(__file__).resolve().parent.parent


class UnitTests(unittest.TestCase):
    def setUp(self):
        base = ROOT / "target/p4-system-14/a42x/fixtures"
        base.mkdir(parents=True, exist_ok=True)
        directory = tempfile.TemporaryDirectory(dir=base)
        self.addCleanup(directory.cleanup)
        self.f = Fixture(Path(directory.name))
        self.clear()

    def clear(self):
        for item in self.f.graph["observation"]:
            path = self.f.root / item["path"]
            if path.exists() or path.is_symlink():
                path.unlink()

    def request(self):
        plan = C.E.bind_execution(self.f.experiment, self.f.candidate)
        self.assertEqual(plan.disposition, "matched", plan)
        return U.freeze_unit(
            plan.plan,
            outputs=tuple(
                C.OutputTarget(o["role"], o["id"], o["path"])
                for o in self.f.graph["observation"]
            ),
        )

    def outcome(self, disposition="recorded", request=None, **kwargs):
        try:
            result = U.capture_unit(
                self.f.root, request=request or self.request(), **kwargs
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
            self.fail("unit escaped as " + type(exc).__name__ + ": " + str(exc))
        self.assertEqual(result.disposition, disposition, result)
        self.assertFalse(hasattr(result, "qualified"))
        self.assertIs(type(result.charged_read_bytes), int)
        self.assertGreaterEqual(result.charged_read_bytes, 0)
        limit = kwargs.get("max_read_bytes", C.TOTAL_BYTES)
        if type(limit) is int and 0 <= limit <= C.TOTAL_BYTES:
            self.assertLessEqual(result.charged_read_bytes, limit)
        else:
            self.assertEqual(result.charged_read_bytes, 0)
        return result

    def measured(self, function, **kwargs):
        size = 0
        pin = C.A.read_bounded_pin
        observe = C.A.observe_bounded_file

        def reading(*args, **opts):
            nonlocal size
            result = pin(*args, **opts)
            if result.disposition == "matched":
                size += result.byte_size
            return result

        def observing(*args, **opts):
            nonlocal size
            result = observe(*args, **opts)
            if result.disposition == "observed":
                size += result.byte_size
            return result

        with mock.patch.object(
            C.A, "read_bounded_pin", side_effect=reading
        ), mock.patch.object(C.A, "observe_bounded_file", side_effect=observing):
            result = function(**kwargs)
        return result, size

    def test_malformed_public_plan_is_a_typed_refusal(self):
        plan = C.E.bind_execution(self.f.experiment, self.f.candidate).plan
        outputs = tuple(
            C.OutputTarget(o["role"], o["id"], o["path"])
            for o in self.f.graph["observation"]
        )
        bad = replace(
            plan.runs[0], observations=(("raw-gpr", []), *plan.runs[0].observations[1:])
        )
        for value in [None, replace(plan, runs=(bad, *plan.runs[1:]))]:
            with self.subTest(value=value), self.assertRaises(C.CaptureError):
                U.freeze_unit(value, outputs=outputs)

    def test_three_real_processes_and_receipts_with_exact_charge(self):
        result, actual = self.measured(self.outcome)
        self.assertEqual(len(result.runs), 3)
        self.assertEqual(len({r.process.pid for r in result.runs}), 3)
        self.assertEqual(result.charged_read_bytes, actual)
        self.assertEqual(actual, sum(r.charged_read_bytes for r in result.runs))
        for published, kind in zip(result.runs, C.E.RUN_KINDS):
            self.assertEqual(published.process.process_exit, 0)
            receipt = published.receipt
            payload = (self.f.root / receipt.path).read_bytes()
            doc = F.parse_capture(payload, path=receipt.path)
            self.assertEqual(doc["run_kind"], kind)
            self.assertEqual(
                (len(payload), hashlib.sha256(payload).hexdigest()),
                (receipt.byte_size, receipt.sha256),
            )
            self.assertEqual(len(doc["observation"]), 3)
        self.assertTrue(
            all((self.f.root / o["path"]).exists() for o in self.f.graph["observation"])
        )

    def test_process_allowance_exact_and_one_short(self):
        request = self.f.request()
        first, actual = self.measured(
            lambda: C.capture_run(self.f.root, request=request)
        )
        self.assertEqual(first.disposition, "recorded", first)
        self.assertEqual(first.charged_read_bytes, actual)
        exact = C.capture_run(self.f.root, request=request, max_read_bytes=actual)
        self.assertEqual(exact.disposition, "recorded", exact)
        self.assertEqual(exact.charged_read_bytes, actual)
        short = C.capture_run(self.f.root, request=request, max_read_bytes=actual - 1)
        self.assertEqual(short.disposition, "refused", short)
        self.assertEqual(short.charged_read_bytes, actual - 1)

    def test_publication_allowance_exact_and_one_short(self):
        request = self.f.request()
        first, actual = self.measured(
            lambda: C.capture_run_with_receipt(self.f.root, request=request)
        )
        self.assertEqual(first.disposition, "recorded", first)
        self.assertEqual(first.charged_read_bytes, actual)
        exact = C.capture_run_with_receipt(
            self.f.root, request=request, max_read_bytes=actual
        )
        self.assertEqual(exact.disposition, "recorded", exact)
        self.assertEqual(exact.charged_read_bytes, actual)
        short = C.capture_run_with_receipt(
            self.f.root, request=request, max_read_bytes=actual - 1
        )
        self.assertEqual(short.disposition, "refused", short)
        self.assertEqual(short.charged_read_bytes, actual - 1)
        self.assertFalse(self.f.path("process-receipt").exists())

    def test_unit_allowance_exact_and_one_short(self):
        first, actual = self.measured(self.outcome)
        self.assertEqual(first.charged_read_bytes, actual)
        self.clear()
        exact = self.outcome(max_read_bytes=actual)
        self.assertEqual(exact.charged_read_bytes, actual)
        self.clear()
        short, read = self.measured(
            self.outcome, disposition="refused", max_read_bytes=actual - 1
        )
        self.assertLessEqual(read, actual - 1)
        self.assertEqual(short.charged_read_bytes, actual - 1)
        self.assertLessEqual(len(short.runs), 3)

    def test_invalid_limits_refuse_before_process_or_reader(self):
        request = self.request()
        with mock.patch.object(
            C.A, "read_bounded_pin", side_effect=AssertionError("unexpected read")
        ), mock.patch.object(
            C.subprocess, "Popen", side_effect=AssertionError("unexpected process")
        ):
            for value in [True, -1, C.TOTAL_BYTES + 1, "1", None]:
                with self.subTest(value=value):
                    self.outcome("refused", request, max_read_bytes=value)
            for value in [True, -1, C.TOTAL_BYTES + 1, "1"]:
                for helper in [C.capture_run, C.capture_run_with_receipt]:
                    with self.subTest(helper=helper.__name__, value=value):
                        result = helper(
                            self.f.root, request=request.runs[0], max_read_bytes=value
                        )
                        self.assertEqual(result.disposition, "refused", result)
                        self.assertEqual(result.charged_read_bytes, 0)

    def test_failed_pin_consumes_reserved_allowance_and_stops(self):
        request = self.request()
        failure = C.A.PinResult(
            "input",
            "sail-riscv",
            request.runs[0].binary_path,
            "unavailable",
            "synthetic unavailable",
        )
        with mock.patch.object(
            C.A, "read_bounded_pin", return_value=failure
        ), mock.patch.object(
            C.subprocess, "Popen", side_effect=AssertionError("unexpected process")
        ):
            result = self.outcome("unavailable", request, max_read_bytes=17)
        self.assertEqual(result.charged_read_bytes, 17)
        self.assertEqual(len(result.runs), 1)
        self.assertIsNone(result.runs[0].process.pid)

    def test_malformed_pin_cannot_refund_unjudgeable_read(self):
        request = self.request()
        for size in [-1, 18, True]:
            with self.subTest(size=size):
                finding = C.A.PinResult(
                    "input",
                    "sail-riscv",
                    request.runs[0].binary_path,
                    "matched",
                    "malformed",
                    size,
                    request.runs[0].binary_sha256,
                )
                with mock.patch.object(C.A, "read_bounded_pin", return_value=finding):
                    result = C.capture_run(
                        self.f.root, request=request.runs[0], max_read_bytes=17
                    )
                self.assertEqual(result.disposition, "refused", result)
                self.assertEqual(result.charged_read_bytes, 17)

    def test_failed_or_escaping_observer_keeps_reservation(self):
        request = self.f.request()
        for failure in [
            C.A.ObservedFile(request.outputs[0].path, "unavailable", "synthetic"),
            OSError(errno.EIO, "synthetic"),
        ]:
            with self.subTest(failure=type(failure).__name__):
                kwargs = (
                    {"side_effect": failure}
                    if isinstance(failure, Exception)
                    else {"return_value": failure}
                )
                with mock.patch.object(C.A, "observe_bounded_file", **kwargs):
                    result = C.capture_run(
                        self.f.root, request=request, max_read_bytes=100000
                    )
                self.assertEqual(result.disposition, "unavailable", result)
                self.assertEqual(result.charged_read_bytes, 100000)
                self.assertIsNotNone(result.pid)

    def test_publication_failed_read_keeps_remaining_reservation(self):
        original = C.A.read_bounded_pin

        def reading(root, kind, record, **kwargs):
            if kind == "observation":
                return C.A.PinResult(
                    kind, record["id"], record["path"], "unavailable", "synthetic"
                )
            return original(root, kind, record, **kwargs)

        with mock.patch.object(C.A, "read_bounded_pin", side_effect=reading):
            result = C.capture_run_with_receipt(
                self.f.root, request=self.f.request(), max_read_bytes=100000
            )
        self.assertEqual(result.disposition, "refused", result)
        self.assertEqual(result.charged_read_bytes, 100000)
        self.assertFalse(self.f.path("process-receipt").exists())

    def test_invalid_delegated_accounting_charges_everything(self):
        for charge in [-1, 101, True]:
            with self.subTest(charge=charge):
                fake = C.PublishedCapture("refused", "fake", charged_read_bytes=charge)
                with mock.patch.object(
                    C, "capture_run_with_receipt", return_value=fake
                ) as delegated:
                    result = self.outcome("refused", max_read_bytes=100)
                self.assertEqual(result.charged_read_bytes, 100)
                self.assertEqual(delegated.call_count, 1)
                self.assertEqual(result.runs, ())

    def test_invalid_process_accounting_not_refunded_by_publisher(self):
        fake = C.ProcessCapture("refused", "fake", charged_read_bytes=101)
        with mock.patch.object(C, "capture_run", return_value=fake):
            result = C.capture_run_with_receipt(
                self.f.root, request=self.f.request(), max_read_bytes=100
            )
        self.assertEqual(result.disposition, "refused", result)
        self.assertEqual(result.charged_read_bytes, 100)

    def test_global_aliases_and_common_input_changes_refuse_before_io(self):
        request = self.request()
        base, repeat, control = request.runs
        cases = [
            replace(
                request,
                runs=(
                    base,
                    repeat,
                    replace(
                        control,
                        outputs=(
                            control.outputs[0],
                            replace(control.outputs[1], path=base.outputs[1].path),
                            *control.outputs[2:],
                        ),
                    ),
                ),
            ),
            replace(
                request,
                runs=(
                    base,
                    repeat,
                    replace(
                        control,
                        outputs=(
                            control.outputs[0],
                            replace(
                                control.outputs[1],
                                observation_id=base.outputs[1].observation_id,
                            ),
                            *control.outputs[2:],
                        ),
                    ),
                ),
            ),
            replace(
                request, runs=(base, replace(repeat, inputs=control.inputs), control)
            ),
        ]
        source = next(i for i in control.inputs if i.role == "guest-source")
        cases.append(
            replace(
                request,
                runs=(
                    base,
                    repeat,
                    replace(
                        control,
                        inputs=tuple(
                            replace(i, sha256="0" * 64) if i == source else i
                            for i in control.inputs
                        ),
                    ),
                ),
            )
        )
        with mock.patch.object(
            U, "_reserve", side_effect=AssertionError("unexpected filesystem preflight")
        ):
            for case in cases:
                with self.subTest(case=case):
                    self.outcome("refused", case)

    def test_each_preexisting_output_preserved_before_any_process(self):
        request = self.request()
        original = os.open

        def opening(path, flags, *args, **kwargs):
            if flags & os.O_CREAT:
                raise AssertionError("pre-existing output reached reservation write")
            return original(path, flags, *args, **kwargs)

        for item in self.f.graph["observation"]:
            path = self.f.root / item["path"]
            path.write_bytes(b"prior capture")
            with self.subTest(path=item["path"]), mock.patch.object(
                C.subprocess, "Popen", side_effect=AssertionError("unexpected process")
            ), mock.patch.object(U.os, "open", side_effect=opening):
                self.outcome("refused", request)
                self.assertEqual(path.read_bytes(), b"prior capture")
            path.unlink()

    def test_other_runs_input_alias_preserved(self):
        request = self.request()
        base, repeat, control = request.runs
        other = next(i for i in control.inputs if i.role == "expectation")
        path = self.f.root / other.path
        before = path.read_bytes()
        # Existing hardlink and actual case aliases must both refuse before cleanup.
        target = self.f.path("process-stdout")
        os.link(path, target)
        self.outcome("refused", request)
        self.assertEqual(path.read_bytes(), before)
        target.unlink()
        alias = other.path.upper()
        if (self.f.root / alias).exists() and path.samefile(self.f.root / alias):
            changed = replace(
                base,
                outputs=(
                    base.outputs[0],
                    replace(base.outputs[1], path=alias),
                    *base.outputs[2:],
                ),
            )
            self.outcome("refused", replace(request, runs=(changed, repeat, control)))
            self.assertEqual(path.read_bytes(), before)

    def test_absent_cross_run_namespace_alias_refuses_before_child(self):
        self.f.observation("baseline", "raw-gpr")["path"] = "outputs/ALIAS.data"
        self.f.runs["baseline"]["argv"][9] = "outputs/ALIAS.data"
        self.f.observation("control", "process-stdout")["path"] = "outputs/alias.data"
        request = self.request()
        opening, stating, unlinking = os.open, os.stat, os.unlink

        def name(p, kwargs):
            return (
                "alias.data"
                if p == "ALIAS.data" and kwargs.get("dir_fd") is not None
                else p
            )

        def op(p, *args, **kwargs):
            return opening(name(p, kwargs), *args, **kwargs)

        def st(p, *args, **kwargs):
            return stating(name(p, kwargs), *args, **kwargs)

        def un(p, *args, **kwargs):
            return unlinking(name(p, kwargs), *args, **kwargs)

        with mock.patch.object(U.os, "open", side_effect=op), mock.patch.object(
            U.os, "stat", side_effect=st
        ), mock.patch.object(U.os, "unlink", side_effect=un), mock.patch.object(
            C.subprocess,
            "Popen",
            side_effect=AssertionError("namespace alias reached process"),
        ):
            self.outcome("refused", request)
        self.assertFalse((self.f.root / "outputs/alias.data").exists())

    def test_all_requests_frozen_before_first_reader(self):
        request = self.request()
        original = C.A.read_bounded_pin
        changed = False

        def reading(*args, **kwargs):
            nonlocal changed
            if not changed:
                changed = True
                object.__setattr__(request.runs[2], "argv", ("redirected",))
                object.__setattr__(request, "runs", ())
            return original(*args, **kwargs)

        with mock.patch.object(C.A, "read_bounded_pin", side_effect=reading):
            result = self.outcome(request=request)
        self.assertTrue(changed)
        self.assertEqual(len(result.runs), 3)
        self.assertEqual(request.runs, ())

    def test_failed_and_signal_exit_stop_after_one_receipt(self):
        for mode, status in [("failed", 7), ("signal", -15)]:
            self.clear()
            self.f.mode(mode)
            with self.subTest(mode=mode):
                result = self.outcome("failed")
                self.assertEqual(len(result.runs), 1)
                self.assertEqual(result.runs[0].process.process_exit, status)
                self.assertTrue(self.f.path("process-receipt").exists())
                self.assertTrue(
                    all(
                        not self.f.path(role, "repeat").exists()
                        for role in C.E.OUTPUT_ROLES
                    )
                )

    def test_missing_trace_stops_without_later_files(self):
        self.f.mode("missing")
        result = self.outcome("unavailable")
        self.assertEqual(len(result.runs), 1)
        self.assertIsNone(result.runs[0].receipt)
        self.assertTrue(
            all(
                not self.f.path(role, kind).exists()
                for kind in ("repeat", "control")
                for role in C.E.OUTPUT_ROLES
            )
        )

    def test_duplicate_pid_refuses_and_charges_delegated_allowance(self):
        original = C.capture_run_with_receipt
        first = None
        calls = 0

        def collecting(*args, **kwargs):
            nonlocal first, calls
            result = original(*args, **kwargs)
            calls += 1
            if first is None:
                first = result.process.pid
                return result
            return replace(result, process=replace(result.process, pid=first))

        with mock.patch.object(C, "capture_run_with_receipt", side_effect=collecting):
            result = self.outcome("refused")
        self.assertEqual(calls, 2)
        self.assertEqual(len(result.runs), 1)
        self.assertEqual(result.charged_read_bytes, C.TOTAL_BYTES)

    def test_wrong_metadata_or_disposition_cannot_refund_delegate(self):
        original = C.capture_run_with_receipt
        for invalid in ["output", "disposition"]:
            self.clear()

            def collecting(*args, **kwargs):
                result = original(*args, **kwargs)
                return (
                    replace(
                        result, receipt=replace(result.receipt, observation_id="alien")
                    )
                    if invalid == "output"
                    else replace(result, disposition="unsupported")
                )

            with self.subTest(invalid=invalid), mock.patch.object(
                C, "capture_run_with_receipt", side_effect=collecting
            ):
                result = self.outcome("refused")
                self.assertEqual(result.charged_read_bytes, C.TOTAL_BYTES)
                self.assertEqual(result.runs, ())

    def test_nested_git_parent_refuses_before_read_or_process(self):
        (self.f.path("raw-gpr").parent / ".git").write_bytes(b"owned fixture marker")
        with mock.patch.object(
            C.A, "read_bounded_pin", side_effect=AssertionError("read beyond boundary")
        ), mock.patch.object(
            C.subprocess, "Popen", side_effect=AssertionError("process beyond boundary")
        ):
            self.outcome("refused")

    def test_partial_reservation_failure_preserves_foreign_replacement(self):
        original = os.open
        created = None
        calls = 0

        def opening(path, flags, *args, **kwargs):
            nonlocal created, calls
            if flags & os.O_CREAT:
                calls += 1
                if calls == 2:
                    created.unlink()
                    created.write_bytes(b"foreign replacement")
                    raise OSError(errno.ENOSPC, "synthetic reservation failure")
                created = self.f.path("raw-gpr")
            return original(path, flags, *args, **kwargs)

        with mock.patch.object(U.os, "open", side_effect=opening), mock.patch.object(
            C.subprocess, "Popen", side_effect=AssertionError("unexpected child")
        ):
            result = self.outcome("unavailable")
        self.assertEqual(result.charged_read_bytes, 0)
        self.assertTrue(created.exists())
        self.assertEqual(created.read_bytes(), b"foreign replacement")

    def test_new_git_boundary_revokes_reservation_cleanup(self):
        original = os.open
        calls = 0

        def opening(path, flags, *args, **kwargs):
            nonlocal calls
            if flags & os.O_CREAT:
                calls += 1
                if calls == 2:
                    (self.f.path("raw-gpr").parent / ".git").write_bytes(
                        b"owned fixture marker"
                    )
                    raise OSError(errno.ENOSPC, "synthetic reservation failure")
            return original(path, flags, *args, **kwargs)

        with mock.patch.object(U.os, "open", side_effect=opening):
            self.outcome("refused")
        self.assertTrue(self.f.path("raw-gpr").exists())
        self.assertEqual(self.f.path("raw-gpr").read_bytes(), b"")

    def test_old_positional_result_constructors_keep_fields(self):
        process = C.ProcessCapture("refused", "reason", 7, 123, ())
        self.assertEqual(
            (
                process.process_exit,
                process.pid,
                process.outputs,
                process.charged_read_bytes,
            ),
            (7, 123, (), 0),
        )
        published = C.PublishedCapture("refused", "reason", process, None)
        self.assertIs(published.process, process)
        self.assertEqual(published.charged_read_bytes, 0)

    def test_successful_unit_cannot_overwrite_its_prior_capture(self):
        self.outcome()
        before = {
            o["path"]: (self.f.root / o["path"]).read_bytes()
            for o in self.f.graph["observation"]
        }
        with mock.patch.object(
            C.subprocess,
            "Popen",
            side_effect=AssertionError("old capture reached process"),
        ):
            self.outcome("refused")
        self.assertEqual(before, {p: (self.f.root / p).read_bytes() for p in before})


MUTATIONS = {
    "unit-freeze": (
        "unit",
        "        request = _freeze(request)",
        "        _freeze(request)",
    ),
    "unit-shared-limit": (
        "unit",
        "max_read_bytes=reserved",
        "max_read_bytes=C.TOTAL_BYTES",
    ),
    "unit-charge": (
        "unit",
        "remaining = reserved - result.charged_read_bytes",
        "remaining = reserved",
    ),
    "unit-accounting": (
        "unit",
        "and 0 <= result.charged_read_bytes <= reserved",
        "and True",
    ),
    "unit-output-binding": (
        "unit",
        "== (target.role, target.observation_id, target.path),",
        "== (target.role, target.observation_id, target.path) or True,",
    ),
    "unit-unique-pid": ("unit", "process.pid not in pids", "True"),
    "unit-failed-exit": ("unit", "if process.process_exit != 0:", "if False:"),
    "unit-existing-output": (
        "unit",
        'raise C.CaptureError("unit output already exists; use a fresh capture set")',
        "pass",
    ),
    "unit-exclusive-reservations": ("unit", "| os.O_EXCL", ""),
    "unit-cleanup-identity": (
        "unit",
        "if (info.st_dev, info.st_ino) == (device, inode):",
        "if True:",
    ),
    "unit-cleanup-boundary": (
        "unit",
        "        # A newly observed Git boundary revokes cleanup authority as well.\n        C._check_parents(chain)",
        "        # omitted cleanup boundary",
    ),
    "pin-charge": (
        "collector",
        "                remaining += cap - pin.byte_size",
        "                remaining += cap",
    ),
    "observation-charge": (
        "collector",
        "                remaining += cap - observed.byte_size",
        "                remaining += cap",
    ),
    "publication-process-charge": (
        "collector",
        "        remaining += reserved - process.charged_read_bytes",
        "        remaining += reserved",
    ),
    "publication-read-charge": (
        "collector",
        "\n            remaining += cap - pin.byte_size",
        "\n            remaining += cap",
    ),
    "failed-pin-charge": (
        "collector",
        '                if pin.disposition != "matched":',
        '                if pin.disposition != "matched":\n                    remaining += cap',
    ),
}


def real_sail_smoke():
    """Run the existing public guest comparison from one fresh three-run collector."""
    import contextlib
    import io
    import json
    import probe_matched_gpr_collector as live

    original_capture = C.capture_run
    original_bind = C.E.bind_execution
    state = {}

    def binding(*args, **kwargs):
        result = original_bind(*args, **kwargs)
        if result.disposition == "matched":
            state["plan"] = result.plan
        return result

    def collecting(root, *, request):
        if "unit" not in state:
            plan = state["plan"]
            # This owned smoke declares each output as <observation ID>.data.
            # Check every subsequent request against the complete frozen unit.
            outputs = tuple(
                C.OutputTarget(
                    role, oid, str(Path(run.argv[9]).parent / (oid + ".data"))
                )
                for run in plan.runs
                for role, oid in run.observations
            )
            unit_request = U.freeze_unit(plan, outputs=outputs)
            with mock.patch.object(C, "capture_run", original_capture):
                result = U.capture_unit(root, request=unit_request)
            if result.disposition != "recorded":
                raise ValueError(str(result))
            state.update(unit=result, request=unit_request, receipts=[])
            for published in result.runs:
                item = published.receipt
                payload = (root / item.path).read_bytes()
                doc = F.parse_capture(payload, path=item.path)
                if (len(payload), hashlib.sha256(payload).hexdigest()) != (
                    item.byte_size,
                    item.sha256,
                ):
                    raise ValueError("live unit receipt pin differs")
                state["receipts"].append(
                    dict(kind=doc["run_kind"], bytes=item.byte_size, sha256=item.sha256)
                )
        index = C.E.RUN_KINDS.index(request.run_kind)
        if request != state["request"].runs[index]:
            raise ValueError("live request differs from frozen complete unit")
        return state["unit"].runs[index].process

    output = io.StringIO()
    with contextlib.redirect_stdout(output), mock.patch.object(
        C.E, "bind_execution", binding
    ), mock.patch.object(C, "capture_run", collecting):
        status = live.real_sail_smoke()
    if status:
        print(output.getvalue(), end="")
        return status
    report = json.loads(output.getvalue().splitlines()[0])
    report.update(
        unit_collection="one bounded baseline/repeat/control call",
        charged_read_bytes=state["unit"].charged_read_bytes,
        read_limit=C.TOTAL_BYTES,
        receipt_writer="three fresh bounded receipts published",
        receipts=state["receipts"],
    )
    print(json.dumps(report, sort_keys=True))
    print(
        "LIVE UNIT SMOKE: one shared budget / three fresh process receipts / AGREE AGREE DIVERGE; scratch removed, qualification closed"
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
    global C, U
    if args.mutation:
        owner, before, after = MUTATIONS[args.mutation]
        original = C if owner == "collector" else U
        source = Path(original.__file__).read_text()
        if source.count(before) != 1:
            raise SystemExit("mutation seam not singular: " + args.mutation)
        module = types.ModuleType("unit_collector_mutant")
        module.__file__ = original.__file__
        sys.modules[module.__name__] = module
        exec(
            compile(source.replace(before, after, 1), original.__file__, "exec"),
            module.__dict__,
        )
        if owner == "collector":
            C = module
            U.C = module
            import probe_matched_gpr_collector as fixtures

            fixtures.C = module
        else:
            U = module
    result = unittest.TextTestRunner(stream=sys.stdout, verbosity=0).run(
        unittest.defaultTestLoader.loadTestsFromTestCase(UnitTests)
    )
    print(
        f"MATCHED-GPR-UNIT-COLLECTOR: {result.testsRun} tests / {len(result.failures)} failures / {len(result.errors)} errors; synthetic unit processes, qualification closed"
    )
    return int(not result.wasSuccessful())


if __name__ == "__main__":
    raise SystemExit(main())
