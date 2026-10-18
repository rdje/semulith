#!/usr/bin/env python3
"""Collect one bounded fresh POSIX reference process; no method/qualification credit."""
from __future__ import annotations

from contextlib import ExitStack
from dataclasses import dataclass
import errno
import os
from pathlib import Path
import re
import signal
import stat
import subprocess
import sys

import experiment_artifacts as A
from experiment_verification import is_canonical_path
import matched_gpr_execution as E

FILE_BYTES = 8 * 1024 * 1024
TOTAL_BYTES = 128 * 1024 * 1024
TRACE_BYTES = 4 * 1024 * 1024
STREAM_BYTES = 64 * 1024
PROCESS_SECONDS = 30
# No shell or caller code: this new process becomes the reference with exact argv.
_EXEC = (
    "import os,resource,sys; n=int(sys.argv[1]); "
    "resource.setrlimit(resource.RLIMIT_FSIZE,(n,n)); "
    "os.execv(sys.argv[2],sys.argv[2:])"
)


@dataclass(frozen=True)
class OutputTarget:
    role: str
    observation_id: str
    path: str


@dataclass(frozen=True)
class CaptureRequest:
    run_id: str
    run_kind: str
    instructions: int
    binary_path: str
    binary_sha256: str
    inputs: tuple[E.InputBinding, ...]
    outputs: tuple[OutputTarget, ...]
    argv: tuple[str, ...]


@dataclass(frozen=True)
class CapturedOutput:
    role: str
    observation_id: str
    path: str
    byte_size: int
    sha256: str


@dataclass(frozen=True)
class ProcessCapture:
    disposition: str  # recorded / stale / unavailable / refused; not comparison success
    reason: str
    process_exit: int | None = None
    pid: int | None = None
    outputs: tuple[CapturedOutput, ...] = ()


class CaptureError(ValueError):
    """The finite request or output workspace cannot be used safely."""


def _need(condition, reason):
    if not condition:
        raise CaptureError(reason)


def _text(value, label):
    _need(type(value) is str and 0 < len(value) <= 65536, "invalid " + label)
    return value


def _id(value):
    value = _text(value, "ID")
    _need(re.fullmatch(r"[A-Za-z][A-Za-z0-9._:/-]*", value) is not None, "invalid ID")
    return value


def _path(value):
    value = _text(value, "path")
    _need(
        is_canonical_path(value)
        and all(p.casefold() != ".git" for p in value.split("/")),
        "unsafe path",
    )
    return value


def _sha(value):
    value = _text(value, "SHA256")
    _need(re.fullmatch(r"[0-9a-f]{64}", value) is not None, "invalid SHA256")
    return value


def _freeze(request):
    _need(type(request) is CaptureRequest, "expected CaptureRequest")
    rid, kind = _id(request.run_id), request.run_kind
    _need(type(kind) is str and kind in E.RUN_KINDS, "invalid run kind")
    count = request.instructions
    _need(type(count) is int and 1 <= count <= 4096, "invalid boundary budget")
    binary, digest = _path(request.binary_path), _sha(request.binary_sha256)
    _need(
        type(request.inputs) is tuple and len(request.inputs) == 8,
        "expected eight inputs",
    )
    inputs = []
    for item in request.inputs:
        _need(type(item) is E.InputBinding, "expected plain input binding")
        inputs.append(
            E.InputBinding(
                _text(item.role, "role"),
                _id(item.input_id),
                _path(item.path),
                _sha(item.sha256),
            )
        )
    roles = {item.role: item for item in inputs}
    _need(len(roles) == 8 and set(roles) == E.PRINCIPAL_ROLES, "input roles differ")
    _need(len({item.input_id for item in inputs}) == 8, "duplicate input ID")
    _need(
        type(request.outputs) is tuple and len(request.outputs) == 4,
        "expected four output targets",
    )
    outputs = []
    for item in request.outputs:
        _need(type(item) is OutputTarget, "expected plain output target")
        outputs.append(
            OutputTarget(
                _text(item.role, "output role"),
                _id(item.observation_id),
                _path(item.path),
            )
        )
    by_role = {item.role: item for item in outputs}
    _need(
        len(by_role) == 4 and set(by_role) == set(E.OUTPUT_ROLES), "output roles differ"
    )
    _need(len({item.observation_id for item in outputs}) == 4, "duplicate output ID")
    _need(
        not {item.input_id for item in inputs}
        & {item.observation_id for item in outputs},
        "input/output ID alias",
    )
    paths = [binary, *(item.path for item in inputs), *(item.path for item in outputs)]
    _need(len(set(paths)) == len(paths), "input/output path alias")
    argv = (
        binary,
        "--config-override",
        roles["reference-config"].path,
        "--inst-limit",
        str(count),
        "--trace-instr",
        "--trace-gpr",
        "--trace-exception",
        "--trace-output",
        by_role["raw-gpr"].path,
        roles["guest-image"].path,
    )
    _need(
        type(request.argv) is tuple
        and len(request.argv) == 11
        and all(type(arg) is str for arg in request.argv)
        and request.argv == argv,
        "argv differs from fixed public invocation",
    )
    return CaptureRequest(
        rid,
        kind,
        count,
        binary,
        digest,
        tuple(inputs),
        tuple(by_role[role] for role in E.OUTPUT_ROLES),
        argv,
    )


def freeze_request(
    plan: E.ExecutionPlan, *, run_id: str, outputs: tuple[OutputTarget, ...]
) -> CaptureRequest:
    """Freeze a public binder-produced plan; raw validation/ownership are prerequisites."""
    try:
        _need(type(plan) is E.ExecutionPlan, "expected public execution plan")
        _need(
            type(plan.runs) is tuple
            and len(plan.runs) == 3
            and all(type(run) is E.RunBinding for run in plan.runs),
            "expected three public runs",
        )
        run_id = _id(run_id)
        selected = [run for run in plan.runs if _id(run.run_id) == run_id]
        _need(len(selected) == 1, "run selection is not singular")
        run = selected[0]
        kind = _text(run.kind, "run kind")
        _need(kind in E.RUN_KINDS, "invalid selected run kind")
        _need(
            type(plan.common_inputs) is tuple and len(plan.common_inputs) == 7,
            "expected seven common inputs",
        )
        expectation = (
            plan.control_expectation if kind == "control" else plan.baseline_expectation
        )
        _need(
            type(expectation) is E.InputBinding
            and _id(run.expectation_id) == _id(expectation.input_id),
            "selected expectation differs",
        )
        request = _freeze(
            CaptureRequest(
                run.run_id,
                run.kind,
                plan.instructions,
                plan.binary_path,
                plan.binary_sha256,
                (*plan.common_inputs, expectation),
                outputs,
                run.argv,
            )
        )
        _need(
            type(run.observations) is tuple and len(run.observations) == 4,
            "expected four selected observations",
        )
        observations = []
        for pair in run.observations:
            _need(
                type(pair) is tuple and len(pair) == 2, "invalid selected observation"
            )
            observations.append((_text(pair[0], "observation role"), _id(pair[1])))
        if tuple(observations) != tuple(
            (item.role, item.observation_id) for item in request.outputs
        ):
            raise CaptureError("selected outputs differ")
        return request
    except (AttributeError, TypeError, IndexError) as exc:
        raise CaptureError("malformed public execution plan") from exc


def _identity(info):
    return (
        info.st_dev,
        info.st_ino,
        info.st_mode,
        info.st_size,
        info.st_mtime_ns,
        info.st_ctime_ns,
    )


def _parents(root, outputs, resources):
    """Anchor selected parents before changing any owned leaf; never create dirs."""
    flags = os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW
    root_fd = os.open(root, flags)
    resources.callback(os.close, root_fd)
    device = os.fstat(root_fd).st_dev
    directories = {(): root_fd}
    anchors, chain = {}, []
    for output in outputs:
        parts = output.path.split("/")
        for n in range(1, len(parts)):
            key = tuple(parts[:n])
            if key in directories:
                continue
            parent = directories[key[:-1]]
            child = os.open(key[-1], flags, dir_fd=parent)
            resources.callback(os.close, child)
            info = os.fstat(child)
            _need(info.st_dev == device, "output parent crosses repository volume")
            directories[key] = child
            chain.append((parent, key[-1], child, info.st_dev, info.st_ino))
        parent = directories[tuple(parts[:-1])]
        try:
            info = os.stat(parts[-1], dir_fd=parent, follow_symlinks=False)
        except FileNotFoundError:
            pass
        else:
            _need(
                stat.S_ISREG(info.st_mode) and info.st_dev == device,
                "existing output is unsafe",
            )
        anchors[output.role] = (parent, parts[-1])
    return anchors, chain


def _check_parents(chain):
    for parent, name, child, device, inode in chain:
        info = os.stat(name, dir_fd=parent, follow_symlinks=False)
        _need((info.st_dev, info.st_ino) == (device, inode), "output parent replaced")
        try:
            os.stat(".git", dir_fd=child, follow_symlinks=False)
        except FileNotFoundError:
            continue
        raise CaptureError("output parent became a nested Git repository")


def _stop_group(process):
    try:
        os.killpg(process.pid, signal.SIGKILL)
    except ProcessLookupError:
        pass
    finally:
        process.wait()


def capture_run(root: Path, *, request: CaptureRequest) -> ProcessCapture:
    """Observe one fresh process and bounded outputs; never write a receipt or qualify."""
    pid = status = None
    try:
        request = _freeze(request)
        _need(
            os.name == "posix"
            and all(hasattr(os, flag) for flag in ("O_DIRECTORY", "O_NOFOLLOW")),
            "safe POSIX process collection unavailable",
        )
        root = Path(root)
        remaining = TOTAL_BYTES
        binary = E.InputBinding(
            "reference-binary", "sail-riscv", request.binary_path, request.binary_sha256
        )

        def pins():
            nonlocal remaining
            for item in (binary, *request.inputs):
                pin = A.read_bounded_pin(
                    root,
                    "input",
                    dict(id=item.input_id, path=item.path, sha256=item.sha256),
                    max_bytes=min(FILE_BYTES, remaining),
                )
                _need(
                    type(pin) is A.PinResult
                    and pin.record_kind == "input"
                    and (pin.record_id, pin.path) == (item.input_id, item.path)
                    and pin.disposition
                    in ("matched", "mismatch", "unavailable", "refused")
                    and type(pin.reason) is str,
                    "invalid pin finding",
                )
                if pin.disposition != "matched":
                    disposition = (
                        "stale" if pin.disposition == "mismatch" else pin.disposition
                    )
                    return ProcessCapture(
                        disposition, "input pin: " + pin.reason, status, pid
                    )
                _need(
                    pin.sha256 == item.sha256
                    and type(pin.byte_size) is int
                    and 0 <= pin.byte_size <= min(FILE_BYTES, remaining),
                    "invalid pin accounting",
                )
                remaining -= pin.byte_size
            return None

        refused = pins()
        if refused is not None:
            return refused
        with ExitStack() as resources:
            protected = (binary, *request.inputs)
            anchors, chain = _parents(root, (*protected, *request.outputs), resources)
            _check_parents(chain)
            protected_files = set()
            for item in protected:
                parent, name = anchors[item.role]
                info = os.stat(name, dir_fd=parent, follow_symlinks=False)
                _need(stat.S_ISREG(info.st_mode), "protected input changed type")
                protected_files.add((info.st_dev, info.st_ino))
            existing_outputs = set()
            for output in request.outputs:
                parent, name = anchors[output.role]
                try:
                    info = os.stat(name, dir_fd=parent, follow_symlinks=False)
                except FileNotFoundError:
                    continue
                physical = (info.st_dev, info.st_ino)
                _need(
                    physical not in protected_files,
                    "output physically aliases protected input",
                )
                _need(
                    physical not in existing_outputs,
                    "outputs physically alias each other",
                )
                existing_outputs.add(physical)
            _check_parents(chain)
            for output in request.outputs:
                parent, name = anchors[output.role]
                try:
                    os.unlink(name, dir_fd=parent)
                except FileNotFoundError:
                    pass
            streams = {}
            # Exclusive reservations prove namespace disjointness even for names
            # that were absent, including case/normalization aliases on this FS.
            for output in request.outputs:
                parent, name = anchors[output.role]
                descriptor = os.open(
                    name,
                    os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW,
                    0o600,
                    dir_fd=parent,
                )
                resources.callback(os.close, descriptor)
                if output.role in ("process-stdout", "process-stderr"):
                    streams[output.role] = descriptor
            for role in ("raw-gpr", "process-receipt"):
                parent, name = anchors[role]
                os.unlink(name, dir_fd=parent)
            env = os.environ.copy()
            owned_parent = (
                root
                / Path(
                    next(
                        item.path
                        for item in request.outputs
                        if item.role == "process-stdout"
                    )
                ).parent
            )
            env.update(
                TMPDIR=str(owned_parent.resolve()),
                XDG_CACHE_HOME=str(owned_parent.resolve() / ".cache"),
            )
            _check_parents(chain)
            process = subprocess.Popen(
                [
                    sys.executable,
                    "-I",
                    "-B",
                    "-S",
                    "-c",
                    _EXEC,
                    str(TRACE_BYTES),
                    *request.argv,
                ],
                cwd=root,
                stdin=subprocess.DEVNULL,
                stdout=streams["process-stdout"],
                stderr=streams["process-stderr"],
                start_new_session=True,
                env=env,
            )
            pid = process.pid
            try:
                try:
                    status = process.wait(timeout=PROCESS_SECONDS)
                except subprocess.TimeoutExpired:
                    return ProcessCapture(
                        "refused",
                        "reference exceeded process time limit",
                        process_exit=None,
                        pid=pid,
                    )
            finally:
                _stop_group(process)
            _check_parents(chain)
            refused = pins()
            if refused is not None:
                return refused
            outputs = []
            for output in request.outputs:
                if output.role == "process-receipt":
                    continue
                parent, name = anchors[output.role]
                before = os.stat(name, dir_fd=parent, follow_symlinks=False)
                if output.role in streams:
                    _need(
                        _identity(before) == _identity(os.fstat(streams[output.role])),
                        "stream path replaced",
                    )
                limit = TRACE_BYTES if output.role == "raw-gpr" else STREAM_BYTES
                observed = A.observe_bounded_file(
                    root, output.path, max_bytes=min(limit, remaining)
                )
                _need(
                    type(observed) is A.ObservedFile
                    and observed.path == output.path
                    and observed.disposition in ("observed", "unavailable", "refused")
                    and type(observed.reason) is str,
                    "invalid output finding",
                )
                if observed.disposition != "observed":
                    return ProcessCapture(
                        observed.disposition, "output: " + observed.reason, status, pid
                    )
                _need(
                    _identity(before)
                    == _identity(os.stat(name, dir_fd=parent, follow_symlinks=False)),
                    "output changed during collection",
                )
                _need(
                    type(observed.byte_size) is int
                    and 0 <= observed.byte_size <= min(limit, remaining),
                    "invalid output accounting",
                )
                remaining -= observed.byte_size
                outputs.append(
                    CapturedOutput(
                        output.role,
                        output.observation_id,
                        output.path,
                        observed.byte_size,
                        _sha(observed.sha256),
                    )
                )
            _check_parents(chain)
            return ProcessCapture(
                "recorded",
                "fresh process/output metadata; comparison and qualification pending",
                status,
                pid,
                tuple(outputs),
            )
    except (CaptureError, AttributeError, TypeError, ValueError) as exc:
        return ProcessCapture("refused", str(exc), status, pid)
    except OSError as exc:
        disposition = (
            "refused"
            if exc.errno in (errno.ELOOP, errno.ENOTDIR, errno.EEXIST)
            else "unavailable"
        )
        return ProcessCapture(
            disposition,
            "process/output I/O: " + (exc.strerror or type(exc).__name__),
            status,
            pid,
        )
