#!/usr/bin/env python3
"""Collect three fresh bounded process/receipt pairs; no comparison/qualification."""
from __future__ import annotations

from contextlib import ExitStack
from dataclasses import dataclass
import errno
import os
from pathlib import Path

import matched_gpr_collector as C


@dataclass(frozen=True)
class UnitRequest:
    runs: tuple[C.CaptureRequest, ...]


@dataclass(frozen=True)
class UnitCapture:
    disposition: str  # recorded / failed / stale / unavailable / refused
    reason: str
    runs: tuple[C.PublishedCapture, ...] = ()
    charged_read_bytes: int = 0


def _freeze(request):
    C._need(
        type(request) is UnitRequest
        and type(request.runs) is tuple
        and len(request.runs) == 3,
        "expected three frozen run requests",
    )
    runs = tuple(C._freeze(run) for run in request.runs)
    C._need(
        tuple(run.run_kind for run in runs) == C.E.RUN_KINDS,
        "expected baseline/repeat/control order",
    )
    C._need(len({run.run_id for run in runs}) == 3, "duplicate unit run ID")
    base, repeat, control = runs
    C._need(
        all(
            (r.instructions, r.binary_path, r.binary_sha256)
            == (base.instructions, base.binary_path, base.binary_sha256)
            for r in runs
        ),
        "unit execution identity differs",
    )
    common = [{i.role: i for i in r.inputs if i.role != "expectation"} for r in runs]
    C._need(
        common[0] == common[1] == common[2] and base.inputs == repeat.inputs,
        "unit common inputs differ",
    )
    expected = [next(i for i in r.inputs if i.role == "expectation") for r in runs]
    C._need(
        expected[2].input_id != expected[0].input_id
        and expected[2].path != expected[0].path,
        "control expectation is not distinct",
    )
    inputs = (*base.inputs, expected[2])
    outputs = tuple(o for r in runs for o in r.outputs)
    C._need(len({i.input_id for i in inputs}) == 9, "duplicate unit input ID")
    C._need(len({o.observation_id for o in outputs}) == 12, "duplicate unit output ID")
    C._need(
        not {i.input_id for i in inputs} & {o.observation_id for o in outputs},
        "unit input/output ID alias",
    )
    paths = [base.binary_path, *(i.path for i in inputs), *(o.path for o in outputs)]
    C._need(len(set(paths)) == len(paths), "unit input/output path alias")
    return UnitRequest(runs)


def _bind_unit(
    plan: C.E.ExecutionPlan, *, outputs: tuple[C.OutputTarget, ...]
) -> UnitRequest:
    """Freeze a validated public execution plan and its twelve owned output targets."""
    C._need(
        type(plan) is C.E.ExecutionPlan
        and type(outputs) is tuple
        and len(outputs) == 12,
        "expected public plan and twelve output targets",
    )
    C._need(
        all(type(o) is C.OutputTarget for o in outputs), "invalid unit output target"
    )
    C._need(
        type(plan.runs) is tuple
        and len(plan.runs) == 3
        and all(type(r) is C.E.RunBinding for r in plan.runs),
        "invalid public runs",
    )
    by_id = {C._id(o.observation_id): o for o in outputs}
    C._need(len(by_id) == 12, "duplicate unit output ID")
    runs = []
    for kind in C.E.RUN_KINDS:
        selected = [r for r in plan.runs if r.kind == kind]
        C._need(len(selected) == 1, "unit run selection is not singular")
        run = selected[0]
        C._need(
            type(run.observations) is tuple and len(run.observations) == 4,
            "invalid public output selection",
        )
        targets = []
        for pair in run.observations:
            C._need(
                type(pair) is tuple and len(pair) == 2 and pair[1] in by_id,
                "unknown public unit output",
            )
            targets.append(by_id[pair[1]])
        runs.append(C.freeze_request(plan, run_id=run.run_id, outputs=tuple(targets)))
    return _freeze(UnitRequest(tuple(runs)))


def freeze_unit(
    plan: C.E.ExecutionPlan, *, outputs: tuple[C.OutputTarget, ...]
) -> UnitRequest:
    """Freeze all used plan fields; malformed public plans raise CaptureError before I/O."""
    try:
        return _bind_unit(plan, outputs=outputs)
    except (AttributeError, IndexError, KeyError, TypeError) as exc:
        raise C.CaptureError("malformed public unit plan") from exc


def _reserve(root, request, resources):
    """Require fresh names and prove actual namespace separation before any child."""
    base = request.runs[0]
    inputs = (
        *base.inputs,
        next(i for i in request.runs[2].inputs if i.role == "expectation"),
    )
    protected_paths = [base.binary_path, *(i.path for i in inputs)]
    outputs = [o for r in request.runs for o in r.outputs]
    # The shared directory anchor indexes by role; use unique local keys because
    # all three runs intentionally reuse the four observation role names.
    records = tuple(
        C.OutputTarget(str(n), "anchor", path)
        for n, path in enumerate([*protected_paths, *(o.path for o in outputs)])
    )
    anchors, chain = C._parents(root, records, resources)
    C._check_parents(chain)
    selected = [anchors[str(n)] for n in range(len(protected_paths), len(records))]
    for parent, name in selected:
        try:
            os.stat(name, dir_fd=parent, follow_symlinks=False)
        except FileNotFoundError:
            continue
        raise C.CaptureError("unit output already exists; use a fresh capture set")
    reservations = []
    try:
        for parent, name in selected:
            fd = os.open(
                name,
                os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW,
                0o600,
                dir_fd=parent,
            )
            resources.callback(os.close, fd)
            info = os.fstat(fd)
            reservations.append((parent, name, info.st_dev, info.st_ino))
        C._check_parents(chain)
        for parent, name, device, inode in reservations:
            info = os.stat(name, dir_fd=parent, follow_symlinks=False)
            C._need(
                (info.st_dev, info.st_ino) == (device, inode),
                "unit reservation replaced",
            )
    finally:
        # A newly observed Git boundary revokes cleanup authority as well.
        C._check_parents(chain)
        for parent, name, device, inode in reservations:
            try:
                info = os.stat(name, dir_fd=parent, follow_symlinks=False)
                if (info.st_dev, info.st_ino) == (device, inode):
                    os.unlink(name, dir_fd=parent)
            except FileNotFoundError:
                pass
    return chain


def capture_unit(
    root: Path, *, request: UnitRequest, max_read_bytes: int = C.TOTAL_BYTES
) -> UnitCapture:
    """Collect the complete fresh unit within one conservative artifact-read bound."""
    runs = []
    allowance = remaining = 0

    def finish(disposition, reason):
        return UnitCapture(disposition, reason, tuple(runs), allowance - remaining)

    try:
        request = _freeze(request)
        C._need(
            type(max_read_bytes) is int and 0 <= max_read_bytes <= C.TOTAL_BYTES,
            "invalid unit read allowance",
        )
        allowance = remaining = max_read_bytes
        root = Path(root)
        with ExitStack() as resources:
            chain = _reserve(root, request, resources)
            pids = set()
            for run in request.runs:
                C._check_parents(chain)
                reserved = remaining
                remaining = 0
                result = C.capture_run_with_receipt(
                    root, request=run, max_read_bytes=reserved
                )
                C._need(
                    type(result) is C.PublishedCapture
                    and type(result.charged_read_bytes) is int
                    and 0 <= result.charged_read_bytes <= reserved,
                    "invalid unit delegated accounting",
                )
                C._need(
                    result.disposition
                    in ("recorded", "stale", "unavailable", "refused")
                    and type(result.reason) is str,
                    "invalid unit run disposition",
                )
                process = result.process
                if result.disposition == "recorded":
                    C._need(
                        type(process) is C.ProcessCapture
                        and process.disposition == "recorded"
                        and type(process.pid) is int
                        and process.pid > 0
                        and type(process.process_exit) is int
                        and type(process.charged_read_bytes) is int
                        and 0 <= process.charged_read_bytes <= result.charged_read_bytes
                        and type(process.outputs) is tuple
                        and len(process.outputs) == 3
                        and type(result.receipt) is C.CapturedOutput,
                        "incomplete collected unit run",
                    )
                    outputs = (*process.outputs, result.receipt)
                    for output, target in zip(outputs, run.outputs):
                        C._need(
                            type(output) is C.CapturedOutput
                            and (output.role, output.observation_id, output.path)
                            == (target.role, target.observation_id, target.path),
                            "unit output metadata differs",
                        )
                        limit = (
                            C.TRACE_BYTES
                            if output.role == "raw-gpr"
                            else C.STREAM_BYTES
                        )
                        C._need(
                            type(output.byte_size) is int
                            and 0 <= output.byte_size <= limit,
                            "invalid unit output size",
                        )
                        C._sha(output.sha256)
                    C._need(process.pid not in pids, "unit process identity repeated")
                    pids.add(process.pid)
                remaining = reserved - result.charged_read_bytes
                runs.append(result)
                C._check_parents(chain)
                if result.disposition != "recorded":
                    return finish(result.disposition, "unit run: " + result.reason)
                if process.process_exit != 0:
                    return finish("failed", "unit process did not exit zero")
            return finish(
                "recorded",
                "three fresh process/receipt pairs; comparison and qualification pending",
            )
    except (
        C.CaptureError,
        AttributeError,
        IndexError,
        KeyError,
        TypeError,
        ValueError,
    ) as exc:
        return finish("refused", str(exc))
    except OSError as exc:
        disposition = (
            "refused"
            if exc.errno in (errno.ELOOP, errno.ENOTDIR, errno.EEXIST)
            else "unavailable"
        )
        return finish(disposition, "unit I/O: " + (exc.strerror or type(exc).__name__))
