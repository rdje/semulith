#!/usr/bin/env python3
"""Explicit read-budget controls; owned on-volume fixtures and descriptor census."""
from __future__ import annotations

import argparse
import contextlib
import errno
import io
import os
from pathlib import Path
import sys
import tempfile
import types
from unittest.mock import patch

import experiment_artifacts as A
import probe_experiment_artifacts as P
import probe_experiment_snapshots as Q

ROOT = Path(__file__).resolve().parent.parent


def checked(root, pin, limit, *, mode="pin", close_error=False):
    reader = A.read_bounded_pin if mode == "pin" else A.read_snapshot
    return P.checked(root, "input", pin, close_error=close_error,
                     reader=lambda r, k, p: reader(r, k, p, max_bytes=limit))


def run_controls():
    parent = ROOT / "target/experiment-read-limit-controls"
    parent.mkdir(parents=True, exist_ok=True)
    passed = failed = 0

    def expect(name, condition):
        nonlocal passed, failed
        if condition:
            passed += 1
        else:
            failed += 1
            print("READ-LIMIT MISS " + name)

    def judge(name, operation, disposition, reason, *, mode="pin", payload=None):
        try:
            result = operation()
        except (ValueError, OSError, TypeError) as error:
            expect(name + ": unexpected " + type(error).__name__, False)
            return
        pin = result.pin if mode == "snapshot" else result
        good = (type(pin) is A.PinResult and pin.disposition == disposition and reason in pin.reason)
        if mode == "snapshot":
            good = good and (result.data == payload and type(result.data) is bytes
                             if disposition == "matched" else result.data is None)
        expect(name, good)

    with tempfile.TemporaryDirectory(prefix="limits-", dir=parent) as allocated:
        base = Path(allocated)
        if base.stat().st_dev != ROOT.stat().st_dev:
            raise ValueError("read-limit fixture is off-volume")
        artifact = base / "artifact"
        artifact.write_bytes(P.PAYLOAD)
        limit = len(P.PAYLOAD)
        base.joinpath("empty").write_bytes(b"")
        judge("bounded pin matches", lambda: checked(base, P.record(), limit), "matched", "match")
        judge("bounded observation matches", lambda: P.checked(base, "observation", P.record(),
              reader=lambda r, k, p: A.read_bounded_pin(r, k, p, max_bytes=limit)), "matched", "match")
        with patch.object(A.os, "read", side_effect=ValueError("oversize file was read")):
            judge("oversized pin refuses before reading", lambda: checked(base, P.record(), limit - 1),
                  "refused", "pin byte limit")
        for invalid in (-1, True, None, "16", 1.0):
            with patch.object(A.os, "open", side_effect=ValueError("invalid limit opened a path")):
                judge("invalid pin limit " + repr(invalid), lambda n=invalid: checked(base, P.record(), n),
                      "refused", "invalid pin byte limit")
        try:
            A.read_bounded_pin(base, "input", P.record())
        except TypeError:
            expect("pin limit is required", True)
        else:
            expect("pin limit is required", False)
        for name, pin, disposition, reason in (
                ("digest mismatch", {**P.record(), "sha256": "0" * 64}, "mismatch", "SHA256 differs"),
                ("missing file", P.record("missing"), "unavailable", "cannot be read"),
                ("unsafe path", P.record("../artifact"), "refused", "noncanonical")):
            judge(name, lambda p=pin: checked(base, p, limit), disposition, reason)
        base.joinpath("link").symlink_to(artifact)
        judge("symlink refused", lambda: checked(base, P.record("link"), limit), "refused", "symlink")
        base.joinpath("nested").mkdir()
        base.joinpath("nested/.git").write_text("owned marker only; not a Git repository")
        base.joinpath("nested/artifact").write_bytes(P.PAYLOAD)
        judge("nested Git marker refused", lambda: checked(base, P.record("nested/artifact"), limit),
              "refused", "nested Git")
        with patch.object(A.os, "read", side_effect=OSError(errno.EIO, "bounded read failure")):
            judge("I/O failure", lambda: checked(base, P.record(), limit), "unavailable", "read failure")
        judge("close failure", lambda: checked(base, P.record(), limit, close_error=True),
              "unavailable", "close failure")

        original_read = os.read
        for mode in ("pin", "snapshot"):
            for scenario in ("exact", "empty", "growth-at-cap", "growth-with-room", "short-reads"):
                payload = b"" if scenario == "empty" else P.PAYLOAD
                artifact.write_bytes(payload)
                bound = len(payload) + (scenario == "growth-with-room")
                requests, consumed = [], []
                changed = False

                def reading(descriptor, count):
                    nonlocal changed
                    requests.append(count)
                    data = original_read(descriptor, min(count, 2) if scenario == "short-reads" else count)
                    consumed.append(len(data))
                    if scenario.startswith("growth") and not changed:
                        changed = True
                        with artifact.open("ab") as stream:
                            stream.write(b"X")
                    return data

                with patch.object(A.os, "read", reading):
                    judge(mode + " " + scenario,
                          lambda: checked(base, P.record(payload=payload), bound, mode=mode),
                          "refused" if scenario.startswith("growth") else "matched",
                          "changed during reading" if scenario == "growth-at-cap" else
                          "grew during reading" if scenario == "growth-with-room" else "match",
                          mode=mode, payload=payload)
                expect(mode + " " + scenario + " consumes at most bound", sum(consumed) <= bound)
                if scenario in {"exact", "empty", "growth-at-cap"}:
                    expect(mode + " " + scenario + " has no over-budget sentinel", sum(requests) == len(payload))
                if scenario.startswith("growth"):
                    expect(mode + " " + scenario + " actually changed file", changed)
                if scenario == "short-reads":
                    expect(mode + " short reads are complete", len(consumed) > 1 and sum(consumed) == len(payload))

        artifact.write_bytes(P.PAYLOAD)
        original_snapshot = A.Snapshot
        retained = []

        def snapshot(pin, data):
            retained.append(data is not None)
            return original_snapshot(pin, data)

        with patch.object(A, "Snapshot", snapshot):
            judge("pin-only result matches", lambda: checked(base, P.record(), limit), "matched", "match")
        expect("pin-only creates no snapshot payload", retained == [False])

        payload = b"L" * (2 * A.CHUNK_BYTES + 17)
        base.joinpath("large").write_bytes(payload)
        requests, consumed = [], []

        def streaming(descriptor, count):
            requests.append(count)
            data = original_read(descriptor, count)
            consumed.append(len(data))
            return data

        retained.clear()
        with patch.object(A.os, "read", streaming), patch.object(A, "Snapshot", snapshot):
            judge("multi-chunk bounded pin", lambda: checked(base, P.record("large", payload), len(payload)),
                  "matched", "match")
        expect("multi-chunk pin stays streamed and bounded",
               len(requests) >= 3 and max(requests) <= A.CHUNK_BYTES
               and sum(consumed) == len(payload) and retained == [False])

        # A legitimate short read can make cumulative requested counts exceed
        # consumed bytes. Exercise the real snapshot suite against that stream.
        def short_read(descriptor, count):
            return original_read(descriptor, max(1, count // 2))

        try:
            with patch.object(A.os, "read", short_read), contextlib.redirect_stdout(io.StringIO()):
                snapshot_rc = Q.run_controls()
        except (ValueError, OSError):
            snapshot_rc = 1
        expect("snapshot suite accepts legitimate short reads", snapshot_rc == 0)
    if base.exists():
        raise ValueError("read-limit fixture was not removed")
    print(f"EXPERIMENT-READ-LIMITS: {passed} pass / {failed} fail; descriptors/fixture cleaned")
    return 1 if failed else 0


def main():
    global A
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mutation", choices=("ignore-pin-limit", "ignore-invalid-pin-limit",
                                               "ignore-sentinel-budget", "retain-pin-payload"))
    args = parser.parse_args()
    if args.mutation:
        path = ROOT / "scripts/experiment_artifacts.py"
        source = path.read_text()
        pin_call = "return _read_pinned(root, record_kind, record, byte_limit=max_bytes).pin"
        before, after = {
            "ignore-pin-limit": (pin_call, "return _read_pinned(root, record_kind, record).pin"),
            "ignore-invalid-pin-limit": (
                "if type(max_bytes) is not int or max_bytes < 0:\n        return PinResult",
                "if False:\n        return PinResult"),
            "ignore-sentinel-budget": ("(byte_limit is None or before.st_size < byte_limit)", "True"),
            "retain-pin-payload": (pin_call,
                "return _read_pinned(root, record_kind, record, byte_limit=max_bytes, retain_payload=True).pin"),
        }[args.mutation]
        if source.count(before) != 1:
            raise ValueError("read-limit mutation must match exactly once: " + args.mutation)
        module = types.ModuleType("experiment_read_limit_mutant")
        module.__file__ = str(path)
        sys.modules[module.__name__] = module
        exec(compile(source.replace(before, after), str(path), "exec"), module.__dict__)
        A = module
    return run_controls()


if __name__ == "__main__":
    raise SystemExit(main())
