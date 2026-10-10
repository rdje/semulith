#!/usr/bin/env python3
"""Read-only file-pin authentication for declared matched-experiment artifacts.

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


def read_pinned(root: Path, record_kind: str, record: dict) -> PinResult:
    """Authenticate one input/observation pin without following symlinks.

    The caller supplies the trusted runtime repository root. Record shape normally
    comes from the reference schema; standalone calls also refuse invalid pins.
    Directory descriptors anchor traversal. Reads stop at the initial file size
    plus one byte. Every acquired descriptor gets a close callback; remaining
    callbacks run even if one close fails, and that failure yields no pin match.
    """
    rid, raw = record.get("id", "<unnamed>"), record.get("path", "")

    def result(disposition, reason, size=None, digest=None):
        return PinResult(record_kind, rid, raw, disposition, reason, size, digest)

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
            if size_pin is not None and before.st_size != size_pin:
                return result("mismatch", "observation byte size differs", before.st_size)

            digest, remaining = hashlib.sha256(), before.st_size
            while remaining:
                chunk = os.read(file_fd, min(remaining, CHUNK_BYTES))
                if not chunk:
                    raise UnsafeArtifact("artifact shortened during reading")
                digest.update(chunk)
                remaining -= len(chunk)
            if os.read(file_fd, 1):
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
            if observed != digest_pin:
                return result("mismatch", "SHA256 differs", before.st_size, observed)
            return result("matched", "file bytes match the declared pin", before.st_size, observed)
    except UnsafeArtifact as error:
        return result("refused", str(error))
    except OSError as error:
        if error.errno in {errno.ELOOP, errno.ENOTDIR}:
            return result("refused", "symlink or non-directory in artifact path")
        return result("unavailable", f"file cannot be read: {error.strerror or type(error).__name__}")


def check_files(root: Path, verification: dict) -> list[PinResult]:
    """Check schema/graph-validated records in declared order, with no success flag."""
    return [read_pinned(root, family, record)
            for family in ("input", "observation") for record in verification[family]]
