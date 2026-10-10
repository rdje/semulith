#!/usr/bin/env python3
"""Offline process/output/pin controls for the public scalar smoke runner."""
from __future__ import annotations

import contextlib
import hashlib
import io
from pathlib import Path
import shlex
import subprocess
import tempfile

import run_smoke as S


class ProbeFailure(Exception):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ProbeFailure(message)


def refusal(call, label: str) -> None:
    try:
        call()
    except S.ReferenceRefusal:
        return
    raise ProbeFailure(label)


def controls(work: Path) -> int:
    count = 0
    output = work / "current.trace"
    tool = work / "reference"

    def executable(status: int, content: str | None) -> None:
        body = "#!/bin/sh\n"
        if content is not None:
            body += (f"printf %s {shlex.quote(content)} > "
                     f"{shlex.quote(str(output))}\n")
        body += f"exit {status}\n"
        tool.write_text(body, encoding="utf-8")
        tool.chmod(0o755)

    S.SAIL = S.SPIKE = tool
    S.config = lambda: work / "unused-config.json"
    for label, run in (("Sail", S.run_sail), ("Spike", S.run_spike)):
        call = lambda: run(work / "unused.elf", 3, output)
        executable(7, "new trace from failed process\n")
        refusal(call, f"{label}: failed process with output accepted")
        count += 1

        executable(0, None)
        output.write_text("stale trace\n")
        refusal(call, f"{label}: stale output accepted as fresh")
        require(not output.exists(), f"{label}: no-output run retained old output")
        count += 1

        executable(7, None)
        output.write_text("stale trace\n")
        refusal(call, f"{label}: failed process with stale output accepted")
        require(not output.exists(), f"{label}: failed run retained old output")
        count += 1

        executable(0, "")
        refusal(call, f"{label}: empty fresh output accepted")
        count += 1

        executable(0, "fresh trace\n")
        output.write_text("stale trace\n")
        call()
        require(output.read_bytes() == b"fresh trace\n",
                f"{label}: successful output was not replaced exactly")
        count += 1

    executable(0, "fresh trace\n")
    digest = hashlib.sha256(tool.read_bytes()).hexdigest()
    candidates = [{"id": label, "binary_sha256": digest}
                  for label in ("sail-riscv", "spike")]
    S.D.load_references = lambda path: {"candidate": candidates}
    for label in ("sail-riscv", "spike"):
        S.verify_reference(label, tool)
        count += 1
    tool.write_text(tool.read_text() + "\n")
    refusal(lambda: S.verify_reference("sail-riscv", tool),
            "wrong binary pin accepted")
    count += 1
    refusal(lambda: S.verify_reference("unknown", tool),
            "absent candidate pin accepted")
    count += 1
    candidates[0].pop("binary_sha256")
    refusal(lambda: S.verify_reference("sail-riscv", tool),
            "undeclared binary digest accepted")
    count += 1
    candidates[0]["binary_sha256"] = digest

    attempted = []
    S.experiment = attempted.append
    S.OVERRIDE_SEXP = tool
    S.failures = []
    with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
        result = S.main()
    require(result == 2 and not attempted,
            "command compared before authenticating references")
    return count + 1


def run(mode: str, work: Path) -> int:
    saved = {name: getattr(S, name, None) for name in
             ("SAIL", "SPIKE", "config", "verify_reference", "experiment",
              "OVERRIDE_SEXP", "failures")}
    original_load = S.D.load_references
    original_run = subprocess.run
    original_unlink = Path.unlink
    try:
        if mode == "ignore-status":
            def ignore_status(*args, **kwargs):
                result = original_run(*args, **kwargs)
                result.returncode = 0
                return result
            S.subprocess.run = ignore_status
        elif mode == "keep-stale":
            Path.unlink = lambda self, *args, **kwargs: None
        elif mode == "ignore-pins":
            S.verify_reference = lambda *args: None
        return controls(work)
    finally:
        for name, value in saved.items():
            if value is None and hasattr(S, name):
                delattr(S, name)
            else:
                setattr(S, name, value)
        S.D.load_references = original_load
        S.subprocess.run = original_run
        Path.unlink = original_unlink


def main() -> int:
    root = S.ROOT / "target" / "smoke-probe"
    root.mkdir(parents=True, exist_ok=True)
    try:
        with tempfile.TemporaryDirectory(dir=root) as tmp:
            work = Path(tmp)
            count = run("normal", work)
            for mode, needle in (("ignore-status", "failed process with output accepted"),
                                 ("keep-stale", "stale output accepted as fresh"),
                                 ("ignore-pins", "wrong binary pin accepted")):
                try:
                    run(mode, work)
                except ProbeFailure as exc:
                    require(needle in str(exc), f"{mode}: wrong control failed: {exc}")
                else:
                    raise ProbeFailure(f"{mode}: defective lifecycle passed the controls")
    except (ProbeFailure, AttributeError) as exc:
        print(f"probe_smoke_runner: FAIL — {exc}")
        return 1
    print(f"probe_smoke_runner: ok — {count} process/output/pin controls; "
          "three defective lifecycles rejected")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
