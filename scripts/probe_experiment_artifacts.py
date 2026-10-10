#!/usr/bin/env python3
"""Real on-volume file-pin controls, with owned fixture and descriptor lifetimes."""
from __future__ import annotations

import errno
import hashlib
import os
from pathlib import Path
import tempfile
from types import SimpleNamespace
from unittest.mock import patch

import experiment_artifacts as A

ROOT = Path(__file__).resolve().parent.parent
PAYLOAD = b"artifact fixture\n"


def record(path="artifact", payload=PAYLOAD):
    return {"id": "artifact", "role": "fixture", "path": path,
            "sha256": hashlib.sha256(payload).hexdigest(), "byte_size": len(payload)}


def checked(root, kind, pin, *, close_error=False, reader=None):
    """Observe actual opens/closes, including all failure and early-return paths."""
    original_open, original_close = os.open, os.close
    live = set()
    injected = False

    def opening(*args, **kwargs):
        if str(args[0]) == "fifo" and not args[1] & os.O_NONBLOCK:
            raise ValueError("FIFO control refuses a potentially blocking open before the OS call")
        descriptor = original_open(*args, **kwargs)
        live.add(descriptor)
        return descriptor

    def closing(descriptor):
        nonlocal injected
        original_close(descriptor)
        live.remove(descriptor)
        if close_error and not injected:
            # Inject after the real close: verify remaining callbacks and failure
            # disposition without intentionally leaking an operating-system fd.
            injected = True
            raise OSError(errno.EIO, "injected close failure")

    with patch.object(A.os, "open", opening), patch.object(A.os, "close", closing):
        result = (reader or A.read_pinned)(root, kind, pin)
    if live:
        for descriptor in live:
            original_close(descriptor)
        raise ValueError("artifact reader leaked descriptors")
    return result


def run_controls():
    parent = ROOT / "target/experiment-artifact-controls"
    parent.mkdir(parents=True, exist_ok=True)
    passed = failed = 0

    def judge(name, result, disposition, reason):
        nonlocal passed, failed
        if result.disposition == disposition and reason in result.reason:
            passed += 1
        else:
            failed += 1
            print(f"ARTIFACT MISS {name}: expected {disposition}/{reason}, got {result}")

    with tempfile.TemporaryDirectory(prefix="pins-", dir=parent) as allocated:
        base = Path(allocated)
        root = base / "root"
        root.mkdir()
        if root.stat().st_dev != ROOT.stat().st_dev:
            raise ValueError("fixture is off the repository volume")
        artifact = root / "artifact"
        artifact.write_bytes(PAYLOAD)
        judge("observation matches", checked(root, "observation", record()), "matched", "match")
        judge("input matches", checked(root, "input", record()), "matched", "match")
        empty = root / "empty"
        empty.write_bytes(b"")
        judge("empty regular file has a genuine pin", checked(root, "observation", record("empty", b"")),
              "matched", "match")
        judge("wrong hash", checked(root, "input", {**record(), "sha256": "0" * 64}),
              "mismatch", "SHA256 differs")
        judge("wrong size", checked(root, "observation", {**record(), "byte_size": 1}),
              "mismatch", "byte size differs")
        judge("missing file", checked(root, "input", record("missing")), "unavailable", "cannot be read")
        judge("missing parent", checked(root, "input", record("missing/child")), "unavailable", "cannot be read")
        judge("bad pin", checked(root, "input", {**record(), "sha256": "bad"}), "refused", "invalid SHA256")
        judge("negative size", checked(root, "observation", {**record(), "byte_size": -1}),
              "refused", "invalid observation byte size")
        judge("boolean size", checked(root, "observation", {**record(), "byte_size": True}),
              "refused", "invalid observation byte size")
        judge("unknown kind", checked(root, "unknown", record()), "refused", "record kind")
        for path in ("../artifact", "/artifact", "a//b", "a/./b", "a\x85b"):
            judge("unsafe path " + repr(path), checked(root, "input", record(path)),
                  "refused", "noncanonical")
        judge("Git metadata", checked(root, "input", record(".git/HEAD")), "refused", "Git metadata")
        judge("case variant Git metadata", checked(root, "input", record(".GIT/HEAD")),
              "refused", "Git metadata")
        directory = root / "directory"
        directory.mkdir()
        judge("directory is not data", checked(root, "input", record("directory")),
              "refused", "regular file")
        fifo = root / "fifo"
        os.mkfifo(fifo)
        judge("FIFO refuses without waiting", checked(root, "input", record("fifo")),
              "refused", "regular file")
        (root / "file-link").symlink_to(artifact)
        judge("file symlink", checked(root, "input", record("file-link")), "refused", "symlink")
        directory.joinpath("artifact").write_bytes(PAYLOAD)
        (root / "directory-link").symlink_to(directory, target_is_directory=True)
        judge("parent symlink", checked(root, "input", record("directory-link/artifact")),
              "refused", "symlink")
        outside = base / "outside"
        outside.write_bytes(PAYLOAD)
        (root / "outside-link").symlink_to(outside)
        judge("outside symlink", checked(root, "input", record("outside-link")), "refused", "symlink")
        # Marker-only owned fixtures: no Git repository is initialized or amended.
        for marker_kind in ("file", "directory"):
            nested = root / ("nested-" + marker_kind)
            nested.mkdir()
            nested.joinpath("artifact").write_bytes(PAYLOAD)
            marker = nested / ".git"
            marker.write_text("fixture boundary marker\n") if marker_kind == "file" else marker.mkdir()
            judge("nested Git " + marker_kind, checked(root, "input", record(nested.name + "/artifact")),
                  "refused", "nested Git")

        original_fstat = os.fstat
        for path, expected in (("artifact", "file crosses"), ("directory/artifact", "directory crosses")):
            calls = 0

            def foreign_device(descriptor):
                nonlocal calls
                calls += 1
                info = original_fstat(descriptor)
                if calls != 2:
                    return info
                fields = {name: getattr(info, name) for name in
                          ("st_dev", "st_ino", "st_mode", "st_size", "st_mtime_ns", "st_ctime_ns")}
                fields["st_dev"] += 1
                return SimpleNamespace(**fields)

            with patch.object(A.os, "fstat", foreign_device):
                judge("mock foreign device " + path, checked(root, "input", record(path)),
                      "refused", expected)

        original_read = os.read
        requests = []

        def bounded_read(descriptor, count):
            requests.append(count)
            return original_read(descriptor, count)

        with patch.object(A.os, "read", bounded_read), patch.object(A, "CHUNK_BYTES", 4):
            judge("bounded streamed read", checked(root, "input", record()), "matched", "match")
        if not requests or max(requests) > 4:
            raise ValueError("reader exceeded its chunk bound")
        large_payload = b"L" * (2 * A.CHUNK_BYTES + 17)
        root.joinpath("large").write_bytes(large_payload)
        requests.clear()
        with patch.object(A.os, "read", bounded_read):
            judge("production-size multi-chunk read", checked(root, "input", record("large", large_payload)),
                  "matched", "match")
        if len(requests) < 4 or max(requests) > A.CHUNK_BYTES:
            raise ValueError("production chunk bound or multi-chunk witness failed")

        def race(name, mutate, reason):
            case = root / name
            case.mkdir()
            path = case / "artifact"
            path.write_bytes(PAYLOAD)
            fired = False

            def racing_read(descriptor, count):
                nonlocal fired
                data = original_read(descriptor, count)
                if data and not fired:
                    fired = True
                    mutate(case, path)
                return data

            with patch.object(A.os, "read", racing_read), patch.object(A, "CHUNK_BYTES", 4):
                judge(name, checked(root, "input", record(name + "/artifact")), "refused", reason)
            if not fired:
                raise ValueError("race control never reached the actual read")

        race("shrink", lambda case, path: path.write_bytes(b""), "shortened")
        race("growth", lambda case, path: path.write_bytes(PAYLOAD + b"extra"), "grew")
        race("rewrite", lambda case, path: path.write_bytes(b"X" * len(PAYLOAD)), "changed")
        race("disappear", lambda case, path: path.unlink(), "changed")

        def replace_parent(case, path):
            case.rename(root / (case.name + "-old"))
            case.mkdir()
            case.joinpath("artifact").write_bytes(b"different current bytes")

        race("parent-replacement", replace_parent, "parent replaced")
        race("new-git-boundary", lambda case, path: case.joinpath(".git").write_text("fixture marker\n"),
             "nested Git")
        # Replace the filename after the descriptor's final fstat, so only the
        # pathname binding predicate can detect this particular substitution.
        swap = root / "final-swap"
        swap.mkdir()
        swap.joinpath("artifact").write_bytes(PAYLOAD)
        original_stat = os.stat
        substituted = False

        def replacing_stat(path, *args, **kwargs):
            nonlocal substituted
            if path == "artifact" and kwargs.get("dir_fd") is not None and not substituted:
                substituted = True
                new = swap / "replacement"
                new.write_bytes(b"different current artifact")
                new.replace(swap / "artifact")
            return original_stat(path, *args, **kwargs)

        with patch.object(A.os, "stat", replacing_stat):
            judge("final filename substitution", checked(root, "input", record("final-swap/artifact")),
                  "refused", "path replaced")
        if not substituted:
            raise ValueError("final filename substitution never fired")
        judge("close failure still closes every descriptor", checked(root, "input", record(), close_error=True),
              "unavailable", "close failure")
        with patch.object(A.os, "read", side_effect=OSError(errno.EIO, "injected read failure")):
            judge("I/O failure closes descriptors", checked(root, "input", record()),
                  "unavailable", "read failure")
        results = A.check_files(root, {"input": [record()], "observation": [record("empty", b"")]})
        if [r.disposition for r in results] != ["matched", "matched"]:
            raise ValueError("declared-order batch check changed")
        passed += 1
    if base.exists():
        raise ValueError("owned fixture was not removed")
    print(f"EXPERIMENT-ARTIFACTS: {passed} pass / {failed} fail; descriptors/fixture cleaned")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(run_controls())
