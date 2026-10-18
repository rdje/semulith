#!/usr/bin/env python3
"""Read-only bounded file observations and supplied-pin artifact authentication.

Results describe bytes at a repository-relative path during this check. They do
not authenticate process execution, comparison correctness or evidence adequacy.
No Git, extraction, cache, artifact store or filesystem mutation is involved.
"""
from __future__ import annotations

from contextlib import ExitStack
from dataclasses import dataclass
import errno
import hashlib
import os
from pathlib import Path
import re
import stat

from experiment_verification import is_canonical_path

CHUNK_BYTES = 1024 * 1024


@dataclass(frozen=True)
class PinResult:
    record_kind: str
    record_id: str
    path: str
    disposition: str  # matched / mismatch / unavailable / refused
    reason: str
    byte_size: int | None = None
    sha256: str | None = None


@dataclass(frozen=True)
class Snapshot:
    pin: PinResult
    data: bytes | None  # Available only after a bounded, successful authenticated read.


@dataclass(frozen=True)
class ObservedFile:
    """Stable bounded file metadata, without a supplied-pin authentication claim."""

    path: str
    disposition: str  # observed / unavailable / refused
    reason: str
    byte_size: int | None = None
    sha256: str | None = None


class UnsafeArtifact(Exception):
    """The reader cannot establish a safe, stable project-owned file identity."""


def _identity(info):
    return (info.st_dev, info.st_ino, info.st_mode, info.st_size,
            info.st_mtime_ns, info.st_ctime_ns)


def _git_boundary(directory_fd: int):
    try:
        os.stat(".git", dir_fd=directory_fd, follow_symlinks=False)
    except FileNotFoundError:
        return
    raise UnsafeArtifact("nested Git repository")


def _read_pinned(root: Path, record_kind: str, record: dict,
                 byte_limit: int | None = None, *, retain_payload: bool = False,
                 observe_only: bool = False) -> Snapshot:
    """Authenticate one input/observation pin without following symlinks.

    The caller supplies the trusted runtime repository root. Record shape normally
    comes from the reference schema; standalone calls also refuse invalid pins.
    Directory descriptors anchor traversal. Legacy reads stop at the initial size
    plus one byte. Bounded reads never request a growth sentinel beyond the byte
    limit; final file/path identities still detect growth at the exact cap.
    Every acquired descriptor gets a close callback; remaining
    callbacks run even if one close fails, and that failure yields no pin match.
    """
    rid, raw = record.get("id", "<unnamed>"), record.get("path", "")

    def result(disposition, reason, size=None, digest=None, data=None):
        return Snapshot(PinResult(record_kind, rid, raw, disposition, reason, size, digest), data)

    if record_kind not in {"input", "observation"}:
        return result("refused", "unknown artifact record kind")
    if not isinstance(raw, str) or not is_canonical_path(raw):
        return result("refused", "noncanonical relative path")
    parts = raw.split("/")
    if any(part.casefold() == ".git" for part in parts):
        return result("refused", "Git metadata is not a capture artifact")
    digest_pin = record.get("sha256")
    if not isinstance(digest_pin, str) or re.fullmatch(r"[0-9a-f]{64}", digest_pin) is None:
        return result("refused", "invalid SHA256 pin")
    size_pin = record.get("byte_size") if record_kind == "observation" else None
    if record_kind == "observation" and (type(size_pin) is not int or size_pin < 0):
        return result("refused", "invalid observation byte size")
    if not all(hasattr(os, flag) for flag in ("O_NOFOLLOW", "O_DIRECTORY", "O_NONBLOCK")):
        return result("refused", "safe descriptor traversal is unavailable")

    parents = []
    try:
        with ExitStack() as resources:
            def open_descriptor(path, flags, *, dir_fd=None):
                descriptor = os.open(path, flags, dir_fd=dir_fd)
                resources.callback(os.close, descriptor)
                return descriptor

            directory_flags = os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW
            current = open_descriptor(root, directory_flags)
            device = os.fstat(current).st_dev
            for part in parts[:-1]:
                child = open_descriptor(part, directory_flags, dir_fd=current)
                info = os.fstat(child)
                if info.st_dev != device:
                    raise UnsafeArtifact("directory crosses repository volume")
                _git_boundary(child)
                parents.append((current, part, info.st_dev, info.st_ino, child))
                current = child
            # Nonblocking avoids hanging on a FIFO before fstat can reject its type.
            file_fd = open_descriptor(parts[-1], os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK,
                                      dir_fd=current)
            before = os.fstat(file_fd)
            if before.st_dev != device:
                raise UnsafeArtifact("file crosses repository volume")
            if not stat.S_ISREG(before.st_mode):
                raise UnsafeArtifact("artifact is not a regular file")
            if byte_limit is not None and before.st_size > byte_limit:
                label = "snapshot" if retain_payload else "pin"
                raise UnsafeArtifact(f"artifact exceeds {label} byte limit")
            if size_pin is not None and before.st_size != size_pin:
                return result("mismatch", "observation byte size differs", before.st_size)

            digest, remaining = hashlib.sha256(), before.st_size
            chunks = [] if retain_payload else None
            while remaining:
                chunk = os.read(file_fd, min(remaining, CHUNK_BYTES))
                if not chunk:
                    raise UnsafeArtifact("artifact shortened during reading")
                digest.update(chunk)
                if chunks is not None:
                    chunks.append(chunk)
                remaining -= len(chunk)
            if (byte_limit is None or before.st_size < byte_limit) and os.read(file_fd, 1):
                raise UnsafeArtifact("artifact grew during reading")
            if _identity(os.fstat(file_fd)) != _identity(before):
                raise UnsafeArtifact("artifact changed during reading")
            try:
                after = os.stat(parts[-1], dir_fd=current, follow_symlinks=False)
            except FileNotFoundError:
                raise UnsafeArtifact("artifact path disappeared during reading") from None
            if _identity(after) != _identity(before):
                raise UnsafeArtifact("artifact path replaced during reading")
            for parent_fd, part, parent_device, parent_inode, child_fd in parents:
                try:
                    info = os.stat(part, dir_fd=parent_fd, follow_symlinks=False)
                except FileNotFoundError:
                    raise UnsafeArtifact("artifact parent disappeared during reading") from None
                if (info.st_dev, info.st_ino) != (parent_device, parent_inode):
                    raise UnsafeArtifact("artifact parent replaced during reading")
                _git_boundary(child_fd)
            observed = digest.hexdigest()
            if observe_only:
                digest_pin = observed
            if observed != digest_pin:
                return result("mismatch", "SHA256 differs", before.st_size, observed)
            return result("matched", "file bytes match the declared pin", before.st_size, observed,
                          b"".join(chunks) if chunks is not None else None)
    except UnsafeArtifact as error:
        return result("refused", str(error))
    except OSError as error:
        if error.errno in {errno.ELOOP, errno.ENOTDIR}:
            return result("refused", "symlink or non-directory in artifact path")
        return result("unavailable", f"file cannot be read: {error.strerror or type(error).__name__}")


def read_pinned(root: Path, record_kind: str, record: dict) -> PinResult:
    """Authenticate a pin with bounded streaming memory, without retaining payload."""
    return _read_pinned(root, record_kind, record).pin


def read_bounded_pin(root: Path, record_kind: str, record: dict, *, max_bytes: int) -> PinResult:
    """Authenticate with an explicit total read bound and no retained payload.

    Oversized files refuse before payload reading. Invalid limits refuse before
    opening; zero permits an empty file without a read. All traversal, stability
    and cleanup checks are shared with the legacy pin and snapshot APIs.
    """
    if type(max_bytes) is not int or max_bytes < 0:
        return PinResult(record_kind, record.get("id", "<unnamed>"),
                         record.get("path", ""), "refused", "invalid pin byte limit")
    return _read_pinned(root, record_kind, record, byte_limit=max_bytes).pin


def read_snapshot(root: Path, record_kind: str, record: dict, *, max_bytes: int) -> Snapshot:
    """Return immutable authenticated bytes with an explicit caller byte bound.

    This shares the pin reader's one descriptor-anchored traversal. An oversized
    file refuses before payload reading. Failure yields no data, including a close
    error after collecting bytes. Snapshot assembly uses memory proportional to
    the bound (chunks and the joined bytes can coexist); it never reopens a path.
    Later file changes do not alter the snapshot, but can invalidate currentness.
    This API does not authenticate execution, comparison or retention adequacy.
    """
    if type(max_bytes) is not int or max_bytes < 0:
        return Snapshot(PinResult(record_kind, record.get("id", "<unnamed>"),
                                  record.get("path", ""), "refused", "invalid snapshot byte limit"), None)
    return _read_pinned(root, record_kind, record, byte_limit=max_bytes, retain_payload=True)


def check_files(root: Path, verification: dict) -> list[PinResult]:
    """Check schema/graph-validated records in declared order, with no success flag."""
    return [read_pinned(root, family, record)
            for family in ("input", "observation") for record in verification[family]]


def observe_bounded_file(root: Path, path: str, *, max_bytes: int) -> ObservedFile:
    """Hash a fresh file through the shared anchored/stable reader, without a pin.

    There is deliberately no expected digest and no payload or PinResult in this
    API. All existing authentication entrypoints keep observe_only disabled.
    """
    if (
        type(path) is not str
        or not 1 <= len(path) <= 65536
        or type(max_bytes) is not int
        or max_bytes < 0
    ):
        return ObservedFile(
            path if type(path) is str else "",
            "refused",
            "invalid bounded observation request",
        )
    record = {"id": "fresh-output", "path": path, "sha256": "0" * 64}
    pin = _read_pinned(
        root, "input", record, byte_limit=max_bytes, observe_only=True
    ).pin
    if pin.disposition == "matched":
        return ObservedFile(
            path,
            "observed",
            "stable bounded file observed; no supplied pin",
            pin.byte_size,
            pin.sha256,
        )
    disposition = (
        pin.disposition if pin.disposition in ("unavailable", "refused") else "refused"
    )
    return ObservedFile(path, disposition, pin.reason)
