#!/usr/bin/env python3
"""Bounded authenticated-byte controls; all fixtures are owned and on-volume."""
from __future__ import annotations

from dataclasses import FrozenInstanceError
import errno
import hashlib
import os
from pathlib import Path
import tempfile
from unittest.mock import patch

import experiment_artifacts as A
import probe_experiment_artifacts as P

ROOT = Path(__file__).resolve().parent.parent


def checked(root, pin, limit, *, kind="observation", close_error=False):
    return P.checked(root, kind, pin, close_error=close_error,
                     reader=lambda r, k, p: A.read_snapshot(r, k, p, max_bytes=limit))


def run_controls():
    parent = ROOT / "target/experiment-snapshot-controls"
    parent.mkdir(parents=True, exist_ok=True)
    passed = failed = 0

    def judge(name, snapshot, disposition, reason, payload=None):
        nonlocal passed, failed
        pin = snapshot.pin
        good = pin.disposition == disposition and reason in pin.reason
        if disposition == "matched":
            good = (good and type(snapshot.data) is bytes and snapshot.data == payload
                    and pin.byte_size == len(payload)
                    and pin.sha256 == hashlib.sha256(payload).hexdigest())
        else:
            good = good and snapshot.data is None
        if good:
            passed += 1
        else:
            failed += 1
            # Never print payloads, even for a failed control.
            print(f"SNAPSHOT MISS {name}: {pin}; data type={type(snapshot.data).__name__}")

    with tempfile.TemporaryDirectory(prefix="snapshot-", dir=parent) as allocated:
        base = Path(allocated)
        if base.stat().st_dev != ROOT.stat().st_dev:
            raise ValueError("snapshot fixture is off-volume")
        artifact = base / "artifact"
        artifact.write_bytes(P.PAYLOAD)
        limit = len(P.PAYLOAD)
        judge("input exact bound", checked(base, P.record(), limit, kind="input"),
              "matched", "match", P.PAYLOAD)
        judge("observation exact bound", checked(base, P.record(), limit),
              "matched", "match", P.PAYLOAD)
        base.joinpath("empty").write_bytes(b"")
        judge("zero bound empty bytes", checked(base, P.record("empty", b""), 0),
              "matched", "match", b"")
        with patch.object(A.os, "read", side_effect=ValueError("oversize payload was read")):
            judge("oversized before payload read", checked(base, P.record(), limit - 1),
                  "refused", "snapshot byte limit")
        for invalid in (-1, True, None, "16", 1.0):
            with patch.object(A.os, "open", side_effect=ValueError("invalid limit opened a path")):
                judge("invalid bound " + repr(invalid), checked(base, P.record(), invalid),
                      "refused", "invalid snapshot byte limit")
        try:
            A.read_snapshot(base, "input", P.record())
        except TypeError:
            passed += 1
        else:
            raise ValueError("snapshot silently defaulted its byte bound")
        judge("wrong digest yields no bytes", checked(base, {**P.record(), "sha256": "0" * 64}, limit),
              "mismatch", "SHA256 differs")
        judge("wrong size yields no bytes", checked(base, {**P.record(), "byte_size": 1}, limit),
              "mismatch", "byte size differs")
        judge("missing file yields no bytes", checked(base, P.record("missing"), limit),
              "unavailable", "cannot be read")
        judge("unsafe path yields no bytes", checked(base, P.record("../artifact"), limit),
              "refused", "noncanonical")
        base.joinpath("link").symlink_to(artifact)
        judge("symlink yields no bytes", checked(base, P.record("link"), limit),
              "refused", "symlink")
        judge("close error discards collected bytes", checked(base, P.record(), limit, close_error=True),
              "unavailable", "close failure")

        original_read = os.read
        calls = 0

        def partial_failure(descriptor, count):
            nonlocal calls
            calls += 1
            if calls == 2:
                raise OSError(errno.EIO, "partial snapshot I/O failure")
            return original_read(descriptor, count)

        with patch.object(A.os, "read", partial_failure), patch.object(A, "CHUNK_BYTES", 4):
            judge("partial read discards collected bytes", checked(base, P.record(), limit),
                  "unavailable", "partial snapshot I/O failure")
        if calls != 2:
            raise ValueError("partial read failure never followed a collected chunk")

        changed = False

        def changing_read(descriptor, count):
            nonlocal changed
            data = original_read(descriptor, count)
            if data and not changed:
                changed = True
                artifact.write_bytes(b"X" * limit)
            return data

        with patch.object(A.os, "read", changing_read), patch.object(A, "CHUNK_BYTES", 4):
            judge("race discards collected bytes", checked(base, P.record(), limit),
                  "refused", "changed during reading")
        if not changed:
            raise ValueError("snapshot race never reached payload reading")
        artifact.write_bytes(P.PAYLOAD)

        original_open = os.open
        paths = []

        def opening(path, flags, **kwargs):
            paths.append(path)
            return original_open(path, flags, **kwargs)

        with patch.object(A.os, "open", opening), patch.object(
                A.Path, "read_bytes", side_effect=ValueError("snapshot reopened a filename")):
            snapshot = checked(base, P.record(), limit)
            judge("one anchored read without reopening", snapshot, "matched", "match", P.PAYLOAD)
        if paths != [base, "artifact"]:
            raise ValueError("snapshot opened a path more than once")
        try:
            snapshot.data = b"replacement"
        except FrozenInstanceError:
            passed += 1
        else:
            raise ValueError("snapshot result is mutable")
        try:
            snapshot.data[0] = 0
        except TypeError:
            passed += 1
        else:
            raise ValueError("snapshot payload is mutable")
        replacement = base / "replacement"
        replacement.write_bytes(b"later bytes")
        replacement.replace(artifact)
        if snapshot.data != P.PAYLOAD:
            raise ValueError("later filename replacement altered authenticated bytes")
        passed += 1
        judge("later workspace needs new authentication", checked(base, P.record(), limit),
              "mismatch", "byte size differs")

        payload = b"L" * (2 * A.CHUNK_BYTES + 17)
        base.joinpath("large").write_bytes(payload)
        requests, consumed = [], []

        def bounded_read(descriptor, count):
            requests.append(count)
            data = original_read(descriptor, count)
            consumed.append(len(data))
            return data

        with patch.object(A.os, "read", bounded_read):
            judge("multi-chunk snapshot", checked(base, P.record("large", payload), len(payload)),
                  "matched", "match", payload)
        if len(requests) < 3 or max(requests) > A.CHUNK_BYTES or sum(consumed) != len(payload):
            raise ValueError("snapshot read exceeded chunk/total bound or lost multi-chunk witness")
    if base.exists():
        raise ValueError("snapshot fixture was not removed")
    print(f"EXPERIMENT-SNAPSHOTS: {passed} pass / {failed} fail; descriptors/fixture cleaned")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(run_controls())
