#!/usr/bin/env python3
"""Synthetic process controls and an optional live Sail smoke; no qualification."""
from __future__ import annotations

from dataclasses import fields, replace
import hashlib
import json
import os
from pathlib import Path
import signal
import sys
import tempfile
import time
import types
import unittest
from unittest import mock
import argparse

import matched_gpr_collector as C
import probe_matched_gpr_evaluation as B

ROOT = Path(__file__).resolve().parent.parent
CHILD = r"""
import json,os,pathlib,signal,subprocess,sys,time
config=json.loads(pathlib.Path(sys.argv[2]).read_text())
mode=config.get('mode','ok'); trace=pathlib.Path(sys.argv[9])
if mode == 'descendant':
    code="import pathlib,time; p=pathlib.Path("+repr(config['heartbeat'])+"); [(p.write_text(str(time.monotonic())),time.sleep(.02)) for _ in range(200)]"
    child=subprocess.Popen([sys.executable,'-B','-c',code])
    pathlib.Path(config['child_pid']).write_text(str(child.pid))
    deadline=time.monotonic()+2
    while not pathlib.Path(config['heartbeat']).exists() and time.monotonic()<deadline: time.sleep(.01)
if mode == 'timeout': time.sleep(.8)
if mode != 'missing':
    trace.write_bytes(b'X'*(4194305 if mode=='trace-large' else 5))
if mode=='stream-large': os.write(1,b'X'*65537)
if mode=='streams': os.write(1,b'fresh stdout\x00'); os.write(2,b'fresh stderr\xff')
if mode=='mutate':
    path=pathlib.Path(config['target']); path.write_bytes(path.read_bytes()+b'changed')
if mode=='signal': os.kill(os.getpid(),signal.SIGTERM)
if mode=='argv': trace.write_text(json.dumps(dict(argv=sys.argv,pid=os.getpid(),cwd=os.getcwd(),stdin=len(sys.stdin.buffer.read()),tmp=os.environ['TMPDIR'])))
sys.exit(7 if mode=='failed' else 0)
"""


class Fixture(B.Fixture):
    def __init__(self, root):
        super().__init__(root)
        self.candidate["binary"] = "reference"
        path = root / "reference"
        path.write_text("#!" + sys.executable + " -B\n" + CHILD)
        path.chmod(0o755)
        self.candidate["binary_sha256"] = hashlib.sha256(path.read_bytes()).hexdigest()
        for producer in self.graph["producer"]:
            if producer["role"] == "reference":
                producer["version"] = "sha256:" + self.candidate["binary_sha256"]
        for run in self.runs.values():
            run["argv"][0] = "reference"
        self.mode("ok")

    def mode(self, value, **extra):
        self.write(
            self.inputs["reference-config"],
            json.dumps(dict(mode=value, **extra)).encode(),
        )

    def request(self, kind="baseline"):
        checked = C.E.bind_execution(self.experiment, self.candidate)
        if checked.disposition != "matched":
            raise ValueError(checked.reason)
        return C.freeze_request(
            checked.plan,
            run_id=self.runs[kind]["id"],
            outputs=tuple(
                C.OutputTarget(
                    role,
                    self.observation(kind, role)["id"],
                    self.observation(kind, role)["path"],
                )
                for role in C.E.OUTPUT_ROLES
            ),
        )

    def path(self, role, kind="baseline"):
        return self.root / self.observation(kind, role)["path"]


class CollectorTests(unittest.TestCase):
    def setUp(self):
        base = ROOT / "target/p4-system-14/a42v/fixtures"
        base.mkdir(parents=True, exist_ok=True)
        temporary = tempfile.TemporaryDirectory(dir=base)
        self.addCleanup(temporary.cleanup)
        self.f = Fixture(Path(temporary.name))

    def run_capture(self, request=None, disposition="recorded"):
        try:
            result = C.capture_run(self.f.root, request=request or self.f.request())
        except (
            AttributeError,
            IndexError,
            KeyError,
            TypeError,
            ValueError,
            OSError,
            AssertionError,
        ) as exc:
            self.fail("collector escaped as " + type(exc).__name__ + ": " + str(exc))
        self.assertEqual(result.disposition, disposition, result)
        self.assertFalse(hasattr(result, "qualified"))
        if disposition == "recorded":
            self.assertEqual(
                [o.role for o in result.outputs], list(C.E.OUTPUT_ROLES[:3])
            )
            self.assertIsInstance(result.process_exit, int)
            self.assertGreater(result.pid, 0)
            self.assertFalse(self.f.path("process-receipt").exists())
            for output in result.outputs:
                data = (self.f.root / output.path).read_bytes()
                self.assertEqual(output.byte_size, len(data))
                self.assertEqual(output.sha256, hashlib.sha256(data).hexdigest())
        return result

    def test_real_child_exact_argv_cwd_stdin_and_owned_temp(self):
        self.f.mode("argv")
        request = self.f.request()
        result = self.run_capture(request)
        data = json.loads(self.f.path("raw-gpr").read_text())
        self.assertEqual(tuple(data["argv"]), request.argv)
        self.assertEqual(data["pid"], result.pid)
        self.assertEqual(data["cwd"], str(self.f.root))
        self.assertEqual(data["stdin"], 0)
        self.assertEqual(data["tmp"], str(self.f.path("process-stdout").parent))
        self.assertEqual(result.process_exit, 0)

    def test_two_real_calls_have_distinct_pids(self):
        first = self.run_capture()
        second = self.run_capture()
        self.assertNotEqual(first.pid, second.pid)

    def test_clear_only_owned_outputs_and_keep_empty_streams(self):
        sentinel = self.f.path("raw-gpr").parent / "unrelated"
        sentinel.write_bytes(b"keep")
        for role in C.E.OUTPUT_ROLES:
            self.f.path(role).write_bytes(b"stale")
        self.run_capture()
        self.assertEqual(sentinel.read_bytes(), b"keep")
        self.assertEqual(self.f.path("process-stdout").read_bytes(), b"")
        self.assertEqual(self.f.path("process-stderr").read_bytes(), b"")
        self.assertEqual(self.f.path("raw-gpr").read_bytes(), b"X" * 5)

    def test_missing_trace_never_reuses_old_trace(self):
        self.f.mode("missing")
        self.f.path("raw-gpr").write_bytes(b"old successful trace")
        result = self.run_capture(disposition="unavailable")
        self.assertIsNotNone(result.pid)
        self.assertFalse(self.f.path("raw-gpr").exists())
        self.assertEqual(result.outputs, ())

    def test_binary_and_every_principal_pin_checked_before_execution(self):
        request = self.f.request()
        for item in [
            C.E.InputBinding(
                "reference-binary",
                "sail-riscv",
                request.binary_path,
                request.binary_sha256,
            ),
            *request.inputs,
        ]:
            with self.subTest(item=item.input_id):
                path = self.f.root / item.path
                before = path.read_bytes()
                path.write_bytes(before + b"changed")
                with mock.patch.object(
                    C.subprocess,
                    "Popen",
                    side_effect=AssertionError("unexpected process"),
                ):
                    result = self.run_capture(request, disposition="stale")
                    self.assertIsNone(result.pid)
                path.write_bytes(before)

    def test_missing_binary_is_unavailable_before_execution(self):
        request = self.f.request()
        (self.f.root / request.binary_path).unlink()
        with mock.patch.object(
            C.subprocess, "Popen", side_effect=AssertionError("unexpected process")
        ):
            self.run_capture(request, disposition="unavailable")

    def test_changed_binary_and_input_after_execution(self):
        for target in ["reference", self.f.inputs["guest-image"]["path"]]:
            with self.subTest(target=target):
                before = (self.f.root / target).read_bytes()
                self.f.mode("mutate", target=target)
                result = self.run_capture(disposition="stale")
                self.assertIsNotNone(result.pid)
                self.assertEqual(result.process_exit, 0)
                (self.f.root / target).write_bytes(before)

    def test_frozen_request_cannot_redirect_after_first_read(self):
        request = self.f.request()
        old = C.A.read_bounded_pin
        changed = False

        def reading(*args, **kwargs):
            nonlocal changed
            if not changed:
                changed = True
                object.__setattr__(request, "argv", ("evil",))
                object.__setattr__(request, "outputs", ())
            return old(*args, **kwargs)

        with mock.patch.object(C.A, "read_bounded_pin", side_effect=reading):
            self.run_capture(request)
        self.assertTrue(changed)

    def test_malformed_and_aliased_requests_refuse_before_io(self):
        request = self.f.request()
        alias = replace(
            request,
            outputs=(
                replace(request.outputs[0], path=request.inputs[0].path),
                *request.outputs[1:],
            ),
            argv=(*request.argv[:9], request.inputs[0].path, request.argv[10]),
        )
        cases = [
            alias,
            replace(request, argv=(request.argv[0], "--wrong", *request.argv[2:])),
            replace(request, instructions=True),
            replace(request, argv=("shell",)),
            replace(request, inputs=()),
            replace(
                request,
                outputs=(
                    replace(request.outputs[0], path=request.inputs[0].path),
                    *request.outputs[1:],
                ),
            ),
            replace(
                request,
                outputs=(
                    replace(request.outputs[0], path="../outside"),
                    *request.outputs[1:],
                ),
            ),
        ]
        with mock.patch.object(
            C.A, "read_bounded_pin", side_effect=AssertionError("unexpected I/O")
        ):
            for item in cases:
                with self.subTest(item=item):
                    self.run_capture(item, disposition="refused")

    def test_physical_input_alias_refuses_before_cleanup(self):
        request = self.f.request()
        item = next(i for i in request.inputs if i.role == "guest-image")
        source = self.f.root / item.path
        before = source.read_bytes()
        target = self.f.path("raw-gpr")
        target.unlink()
        os.link(source, target)
        result = C.capture_run(self.f.root, request=request)
        self.assertEqual(source.read_bytes(), before)
        self.assertEqual(result.disposition, "refused", result)
        self.assertIsNone(result.pid)
        target.unlink()
        alias = item.path.upper()
        if (self.f.root / alias).exists() and source.samefile(self.f.root / alias):
            request = replace(
                request,
                outputs=(replace(request.outputs[0], path=alias), *request.outputs[1:]),
                argv=(*request.argv[:9], alias, request.argv[10]),
            )
            result = C.capture_run(self.f.root, request=request)
            self.assertEqual(source.read_bytes(), before)
            self.assertEqual(result.disposition, "refused", result)
            self.assertIsNone(result.pid)

    def test_existing_output_physical_alias_refuses_before_cleanup(self):
        request = self.f.request()
        source = self.f.path("raw-gpr")
        target = self.f.path("process-stderr")
        before = source.read_bytes()
        target.unlink()
        os.link(source, target)
        result = C.capture_run(self.f.root, request=request)
        self.assertEqual(result.disposition, "refused", result)
        self.assertEqual(source.read_bytes(), before)
        self.assertEqual(target.read_bytes(), before)
        self.assertIsNone(result.pid)

    def test_absent_namespace_alias_refuses_before_launch(self):
        # Model case-insensitive final-leaf syscalls on every CI filesystem.
        self.f.observation("baseline", "raw-gpr")["path"] = "outputs/ALIAS.capture"
        self.f.observation("baseline", "process-stdout")[
            "path"
        ] = "outputs/alias.capture"
        self.f.runs["baseline"]["argv"][9] = "outputs/ALIAS.capture"
        request = self.f.request()
        original_open, original_stat, original_unlink = os.open, os.stat, os.unlink

        def name(path, kwargs):
            return (
                "alias.capture"
                if path == "ALIAS.capture" and kwargs.get("dir_fd") is not None
                else path
            )

        def opening(path, *args, **kwargs):
            return original_open(name(path, kwargs), *args, **kwargs)

        def stating(path, *args, **kwargs):
            return original_stat(name(path, kwargs), *args, **kwargs)

        def unlinking(path, *args, **kwargs):
            return original_unlink(name(path, kwargs), *args, **kwargs)

        with mock.patch.object(C.os, "open", side_effect=opening), mock.patch.object(
            C.os, "stat", side_effect=stating
        ), mock.patch.object(C.os, "unlink", side_effect=unlinking), mock.patch.object(
            C.subprocess,
            "Popen",
            side_effect=AssertionError("namespace collision reached execution"),
        ):
            result = self.run_capture(request, disposition="refused")
            self.assertIsNone(result.pid)

    def test_public_plan_selection_binds_output_ids(self):
        plan = C.E.bind_execution(self.f.experiment, self.f.candidate).plan
        request = self.f.request()
        with self.assertRaises(C.CaptureError):
            C.freeze_request(plan, run_id="absent", outputs=request.outputs)
        outputs = (
            replace(request.outputs[0], observation_id="wrong"),
            *request.outputs[1:],
        )
        with self.assertRaises(C.CaptureError):
            C.freeze_request(plan, run_id=request.run_id, outputs=outputs)

    def test_unsafe_final_target_refuses_before_any_cleanup(self):
        request = self.f.request()
        first = self.f.path("raw-gpr")
        first.write_bytes(b"preserve")
        target = self.f.path("process-stderr")
        target.unlink()
        target.symlink_to(first)
        with mock.patch.object(
            C.subprocess, "Popen", side_effect=AssertionError("unexpected process")
        ):
            self.run_capture(request, disposition="refused")
        self.assertEqual(first.read_bytes(), b"preserve")
        self.assertTrue(target.is_symlink())

    def test_parent_symlink_and_nested_git_refuse_without_changes(self):
        request = self.f.request()
        parent = self.f.path("raw-gpr").parent
        for kind in ["symlink", "git-file", "git-directory"]:
            with self.subTest(kind=kind):
                self.f.path("raw-gpr").write_bytes(b"protected existing output")
                if kind == "symlink":
                    moved = parent.with_name(parent.name + "-real")
                    parent.rename(moved)
                    parent.symlink_to(moved, target_is_directory=True)
                elif kind == "git-file":
                    (parent / ".git").write_text("fixture boundary marker")
                else:
                    (parent / ".git").mkdir()
                try:
                    before = self.f.path("raw-gpr").read_bytes()
                    self.run_capture(request, disposition="refused")
                    self.assertEqual(self.f.path("raw-gpr").read_bytes(), before)
                finally:
                    if kind == "symlink":
                        parent.unlink()
                        moved.rename(parent)
                    elif kind == "git-file":
                        (parent / ".git").unlink()
                    else:
                        (parent / ".git").rmdir()

    def test_failed_and_signaled_processes_are_recorded_failed_data(self):
        for mode, status in [("failed", 7), ("signal", -signal.SIGTERM)]:
            with self.subTest(mode=mode):
                self.f.mode(mode)
                result = self.run_capture()
                self.assertEqual(result.process_exit, status)

    def test_binary_streams_remain_separate(self):
        self.f.mode("streams")
        self.run_capture()
        self.assertEqual(self.f.path("process-stdout").read_bytes(), b"fresh stdout\0")
        self.assertEqual(
            self.f.path("process-stderr").read_bytes(), b"fresh stderr\xff"
        )

    def test_stream_overflow_refuses_without_truncating(self):
        self.f.mode("stream-large")
        self.run_capture(disposition="refused")
        self.assertEqual(self.f.path("process-stdout").stat().st_size, 65537)

    def test_hard_file_limit_bounds_reference_trace_writes(self):
        self.f.mode("trace-large")
        result = C.capture_run(self.f.root, request=self.f.request())
        self.assertLessEqual(self.f.path("raw-gpr").stat().st_size, C.TRACE_BYTES)
        self.assertNotEqual(result.process_exit, 0)
        self.assertFalse(hasattr(result, "qualified"))

    def test_deadline_kills_and_reaps_process(self):
        self.f.mode("timeout")
        with mock.patch.object(C, "PROCESS_SECONDS", 0.1):
            result = self.run_capture(disposition="refused")
        self.assertIn("process time limit", result.reason)
        self.assertIs(type(result.pid), int)
        with self.assertRaises(ProcessLookupError):
            os.kill(result.pid, 0)

    def test_successful_parent_leaves_no_running_descendant(self):
        parent = self.f.path("raw-gpr").parent
        heartbeat = parent / "heartbeat"
        pidfile = parent / "child.pid"
        self.f.mode("descendant", heartbeat=str(heartbeat), child_pid=str(pidfile))
        try:
            self.run_capture()
            first = heartbeat.read_bytes()
            time.sleep(0.12)
            self.assertEqual(
                heartbeat.read_bytes(), first, "owned descendant still running"
            )
        finally:
            if pidfile.exists():
                try:
                    os.kill(int(pidfile.read_text()), signal.SIGKILL)
                except ProcessLookupError:
                    pass

    def test_pin_and_total_budgets_refuse_before_payload_reads(self):
        request = self.f.request()
        with mock.patch.object(C, "FILE_BYTES", 1):
            self.run_capture(request, disposition="refused")
        with mock.patch.object(C, "TOTAL_BYTES", 1):
            self.run_capture(request, disposition="refused")

    def test_descriptors_close_on_spawn_failure_and_unexpected_exception(self):
        opening, closing = os.open, os.close
        live = set()

        def opened(*args, **kwargs):
            fd = opening(*args, **kwargs)
            live.add(fd)
            return fd

        def closed(fd):
            closing(fd)
            live.discard(fd)

        with mock.patch.object(C.os, "open", side_effect=opened), mock.patch.object(
            C.os, "close", side_effect=closed
        ):
            with mock.patch.object(
                C.subprocess, "Popen", side_effect=OSError("injected spawn failure")
            ):
                self.run_capture(disposition="unavailable")
            self.assertEqual(live, set())
            with mock.patch.object(
                C.subprocess,
                "Popen",
                side_effect=RuntimeError("unexpected implementation failure"),
            ):
                with self.assertRaises(RuntimeError):
                    self.run_capture()
            self.assertEqual(live, set())

    def test_new_observation_has_no_pin_or_payload_and_legacy_pin_still_discriminates(
        self,
    ):
        path = self.f.path("raw-gpr")
        path.write_bytes(b"fresh")
        relative = str(path.relative_to(self.f.root))
        observed = C.A.observe_bounded_file(self.f.root, relative, max_bytes=5)
        self.assertEqual(observed.disposition, "observed")
        self.assertEqual(observed.sha256, hashlib.sha256(b"fresh").hexdigest())
        self.assertFalse(hasattr(observed, "pin"))
        self.assertFalse(hasattr(observed, "data"))
        pin = C.A.read_bounded_pin(
            self.f.root,
            "input",
            dict(id="test", path=relative, sha256="0" * 64),
            max_bytes=5,
        )
        self.assertEqual(pin.disposition, "mismatch")
        self.assertEqual(
            C.A.observe_bounded_file(self.f.root, relative, max_bytes=4).disposition,
            "refused",
        )
        with mock.patch.object(
            C.A,
            "observe_bounded_file",
            return_value=C.A.ObservedFile("other", "observed", "fixture", 0, "0" * 64),
        ):
            self.run_capture(disposition="refused")

    def test_observation_bad_requests_and_unsafe_files(self):
        for path, limit in [
            (None, 1),
            ("../bad", 1),
            (".git/HEAD", 1),
            ("x", True),
            ("x", -1),
        ]:
            with self.subTest(path=path):
                self.assertEqual(
                    C.A.observe_bounded_file(
                        self.f.root, path, max_bytes=limit
                    ).disposition,
                    "refused",
                )
        path = self.f.path("raw-gpr")
        path.unlink()
        path.symlink_to(self.f.path("process-stdout"))
        self.assertEqual(
            C.A.observe_bounded_file(
                self.f.root, str(path.relative_to(self.f.root)), max_bytes=5
            ).disposition,
            "refused",
        )


MUTATIONS = {
    "physical-input-alias": ("physical not in protected_files", "True"),
    "physical-output-alias": ("physical not in existing_outputs", "True"),
    "exclusive-reservations": ("| os.O_EXCL", ""),
    "observation-mode": ("observe_only=True", "observe_only=False"),
    "output-finding": ("and observed.path == output.path", "and True"),
    "request-freeze": ("request = _freeze(request)", "_freeze(request)"),
    "owned-clear": (
        "os.unlink(name, dir_fd=parent)\n                except FileNotFoundError:",
        "None\n                except FileNotFoundError:",
    ),
    "pre-pins": (
        "refused = pins()\n        if refused is not None:",
        "refused = None\n        if refused is not None:",
    ),
    "post-pins": (
        "refused = pins()\n            if refused is not None:",
        "refused = None\n            if refused is not None:",
    ),
    "fixed-argv": ("and request.argv == argv", "and True"),
    "output-alias": ("len(set(paths)) == len(paths)", "True"),
    "selected-outputs": (
        "if tuple(observations) !=",
        "if False and tuple(observations) !=",
    ),
    "special-output": ("stat.S_ISREG(info.st_mode) and info.st_dev == device", "True"),
    "nested-git": (
        'raise CaptureError("output parent became a nested Git repository")',
        "pass",
    ),
    "stream-bound": ("else STREAM_BYTES", "else TRACE_BYTES"),
    "hard-file-bound": (
        "str(TRACE_BYTES)",
        "str(TRACE_BYTES * 2)",
    ),
    "group-cleanup": (
        "                _stop_group(process)",
        "                process.wait()",
    ),
    "deadline": ("process.wait(timeout=PROCESS_SECONDS)", "process.wait(timeout=None)"),
}


def _real_sail_smoke():
    """Real binary/guest through a prospective envelope, without canonical publication."""
    from pathlib import Path
    from copy import deepcopy
    import hashlib, json, sys
    import matched_gpr_collector as C
    import matched_gpr_artifacts as F
    import matched_gpr_identity as I
    import probe_matched_gpr_execution as P
    import probe_matched_gpr_identity as PI
    import probe_matched_gpr_comparison as PC
    import matched_gpr_image as G
    import dossier_sexp as D
    import run_rv64gc_sail as S

    root = ROOT
    if Path.cwd().resolve() != root:
        raise ValueError("run the smoke from the repository root")
    base = root
    for part in ("target", "p4-system-14", "a42v"):
        base = base / part
        if base.is_symlink():
            raise ValueError("live scratch parent is a symlink")
        base.mkdir(exist_ok=True)
        if base.stat().st_dev != root.stat().st_dev or os.path.lexists(base / ".git"):
            raise ValueError("unsafe live scratch parent")
    unit = root / "profiles/rv64gc-lab-v0"
    refs = D.load_references(unit / "references.sexp")
    candidate = next(c for c in refs["candidate"] if c["id"] == "sail-riscv")
    pin = C.A.read_bounded_pin(
        root,
        "input",
        dict(
            id="sail-riscv", path=candidate["binary"], sha256=candidate["binary_sha256"]
        ),
        max_bytes=C.FILE_BYTES,
    )
    if pin.disposition != "matched":
        raise ValueError("reference binary " + pin.disposition + ": " + pin.reason)
    with tempfile.TemporaryDirectory(dir=base, prefix="live-") as allocated:
        out = Path(allocated).relative_to(root)
        source = (unit / "guests/m-div.s").read_bytes()
        image = G.build_guest_image(source, program="m-div.s", entry=0x80000000).image
        (out / "guest.elf").write_bytes(image)
        config = D.load_override(unit / "reference/sail-rv64gc-lab-v0.override.sexp")
        (out / "config.json").write_text(json.dumps(config, indent=2) + "\n")
        identity = deepcopy(refs)
        identity.pop("experiment", None)
        identity["candidate"] = [deepcopy(candidate)]
        identity_bytes = PI.encode(identity)
        (out / "identity.sexp").write_bytes(identity_bytes)
        if (
            I.check_reference_identity_bytes(
                identity_bytes,
                path=str(out / "identity.sexp"),
                context=I.bind_reference_identity(candidate),
            ).disposition
            != "matched"
        ):
            raise ValueError("live identity does not bind")
        expected = D.load_expectations(unit / "guests/m-div.expected.sexp")
        control = deepcopy(expected)
        control["step"][2]["writes"]["x7"] = "0xfffffffffffffffc"
        (out / "control.sexp").write_bytes(PC.encode(control))
        leaves = []
        for number, name in enumerate(
            [
                "scripts/matched_gpr_collector.py",
                "scripts/experiment_artifacts.py",
                "scripts/matched_gpr_execution.py",
            ]
        ):
            leaves.append(
                dict(
                    id="helper-" + str(number),
                    role="implementation",
                    path=name,
                    sha256=hashlib.sha256(Path(name).read_bytes()).hexdigest(),
                )
            )
        (out / "dependencies.sexp").write_bytes(
            F.encode_dependencies(
                dict(format_version="matched-gpr-dependencies-v1", input=leaves),
                path=str(out / "dependencies.sexp"),
            )
        )
        experiment, _ = P.fixture()
        experiment.update(program="m-div.s", instructions=27)
        graph = experiment["verification"]
        paths = {
            "guest-source": "profiles/rv64gc-lab-v0/guests/m-div.s",
            "guest-image": str(out / "guest.elf"),
            "reference-config": str(out / "config.json"),
            "reference-identity": str(out / "identity.sexp"),
            "collector": "scripts/probe_matched_gpr_collector.py",
            "adapter": "scripts/run_rv64gc_sail.py",
            "dependency-manifest": str(out / "dependencies.sexp"),
            "expectation": "profiles/rv64gc-lab-v0/guests/m-div.expected.sexp",
            "mutant-expectation": str(out / "control.sexp"),
        }
        for item in graph["input"]:
            item["path"] = paths[item["id"]]
            item["sha256"] = hashlib.sha256(Path(item["path"]).read_bytes()).hexdigest()
        for item in graph["observation"]:
            item["path"] = str(out / (item["id"] + ".data"))
            item["byte_size"] = 0
            item["sha256"] = "0" * 64
        for producer in graph["producer"]:
            if producer["role"] == "reference":
                producer["version"] = "sha256:" + candidate["binary_sha256"]
        for run in graph["run"]:
            trace = next(
                o["path"]
                for o in graph["observation"]
                if o["id"] in run["observation_ids"] and o["role"] == "raw-gpr"
            )
            run["argv"] = [
                candidate["binary"],
                "--config-override",
                paths["reference-config"],
                "--inst-limit",
                "27",
                "--trace-instr",
                "--trace-gpr",
                "--trace-exception",
                "--trace-output",
                trace,
                paths["guest-image"],
            ]
        checked = C.E.bind_execution(experiment, candidate)
        if checked.disposition != "matched":
            raise ValueError(checked.reason)
        rows = []
        traces = []
        for run in checked.plan.runs:
            targets = tuple(
                C.OutputTarget(
                    role,
                    oid,
                    next(o["path"] for o in graph["observation"] if o["id"] == oid),
                )
                for role, oid in run.observations
            )
            result = C.capture_run(
                root,
                request=C.freeze_request(
                    checked.plan, run_id=run.run_id, outputs=targets
                ),
            )
            if result.disposition != "recorded" or result.process_exit != 0:
                raise ValueError(str(result))
            trace = next(o for o in result.outputs if o.role == "raw-gpr")
            data = Path(trace.path).read_bytes()
            traces.append(data)
            compared = S.compare_observations(
                control if run.kind == "control" else expected,
                data.decode(),
                result.process_exit,
            )
            want = "DIVERGE" if run.kind == "control" else "AGREE"
            if compared.verdict != want:
                raise ValueError(str(compared))
            if run.kind == "control" and (
                compared.gpr_difference is None
                or compared.gpr_difference.step_n != 2
                or dict(compared.gpr_difference.observed).get("x7") != (1 << 64) - 3
                or dict(compared.gpr_difference.expected).get("x7") != (1 << 64) - 4
            ):
                raise ValueError("wrong control witness")
            rows.append(
                dict(
                    kind=run.kind,
                    pid=result.pid,
                    exit=result.process_exit,
                    verdict=compared.verdict,
                    trace_bytes=trace.byte_size,
                    trace_sha256=trace.sha256,
                )
            )
        if (
            len({row["pid"] for row in rows}) != 3
            or not traces[0] == traces[1] == traces[2]
        ):
            raise ValueError("not three fresh byte-identical traces")
        report = dict(
            reference_binary=candidate["binary"],
            binary_sha256=candidate["binary_sha256"],
            binary_bytes=pin.byte_size,
            runs=rows,
            byte_identical=True,
            canonical_capture=False,
            qualification="closed",
            closure_adequacy="not established",
            receipt_writer="not implemented",
        )
    report["artifacts_retained"] = False
    print(json.dumps(report, sort_keys=True))
    print(
        "LIVE SAIL SMOKE: three fresh PIDs / exit0 / AGREE AGREE DIVERGE / step2 x7 -3 vs -4 / identical traces; no canonical capture or qualification credit"
    )
    return 0


def real_sail_smoke():
    import dossier_sexp as D
    import matched_gpr_image as G
    import run_rv64gc_sail as S

    try:
        return _real_sail_smoke()
    except (
        OSError,
        ValueError,
        D.DossierError,
        G.ImageUnavailable,
        S.SailError,
    ) as exc:
        print("LIVE SAIL SMOKE: UNAVAILABLE OR REFUSED: " + str(exc))
        return 2


def main():
    global C
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mutation", choices=MUTATIONS)
    parser.add_argument("--real-sail-smoke", action="store_true")
    args = parser.parse_args()
    if args.real_sail_smoke:
        if args.mutation:
            parser.error("live smoke cannot use a mutation")
        return real_sail_smoke()
    if args.mutation:
        owner = C.A if args.mutation == "observation-mode" else C
        source = Path(owner.__file__).read_text()
        # These mutations own the original one-process API. Receipt publication
        # has its own independently calibrated probe and repeats some idioms.
        if owner is C:
            source = source.partition(
                "\n\n@dataclass(frozen=True)\nclass PublishedCapture:"
            )[0]
        before, after = MUTATIONS[args.mutation]
        if source.count(before) != 1:
            raise RuntimeError(
                "collector mutation seam is not singular: " + args.mutation
            )
        module = types.ModuleType("mutated_collector")
        module.__file__ = owner.__file__
        sys.modules[module.__name__] = module
        exec(
            compile(source.replace(before, after), owner.__file__, "exec"),
            module.__dict__,
        )
        if args.mutation == "observation-mode":
            C.A = module
        else:
            C = module
    result = unittest.TextTestRunner(verbosity=1).run(
        unittest.defaultTestLoader.loadTestsFromTestCase(CollectorTests)
    )
    print(
        f"MATCHED-GPR-COLLECTOR: {result.testsRun} tests / {len(result.failures)} failures / {len(result.errors)} errors; synthetic child processes, no Sail capture credit"
    )
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    raise SystemExit(main())
