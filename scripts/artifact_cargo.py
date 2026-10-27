#!/usr/bin/env python3
"""Bound the public Cargo invocations used by the two cleanup-aware producers.

`run` performs a bound invocation only. `capture` surrounds one with an anchored
output census and publishes changed outputs. No cache deletion is performed here.
"""
from __future__ import annotations

from contextlib import ExitStack
from dataclasses import dataclass
import datetime
import os
from pathlib import Path
import selectors
import signal
import subprocess
import time

import artifact_cleanup as A
import artifact_output_provenance as O

ROOT = Path(__file__).resolve().parent.parent
PIPE_BYTES = 8 * 1024 * 1024
TIMEOUT = 300

USAGE = """# ANCHOR: usage
### Bound Cargo producers

The C-engine and C-guest-image probes explicitly bind both Cargo output
directories to their existing roots. They use an offline host test command,
the repository-local Cargo home and temporary storage. Ambient `CARGO_*`,
`RUSTC*`, `RUSTFLAGS`, `RUSTDOC*` and Git overrides are removed from the child
environment. The installed Rust toolchain remains a read-only external
dependency. Project Cargo configuration and build inputs remain trusted inputs;
this helper does not interpret arbitrary Cargo configuration or sandbox builds.

```sh
python3 -B scripts/probe_c_engine.py
python3 -B scripts/probe_c_guest_image.py
python3 -B scripts/probe_artifact_cargo.py
```

Descriptor checks reject symlink, nested-Git and foreign-volume ancestors before
launch. Source/manifest bytes are checked again after the child has returned.
Each captured pipe is bounded to8MiB and the process has a300-second deadline.
Interruption, timeout or overflow kills and joins the owned process group;
partial output is not returned as a completed observation. These checks require
caller quiescence; they do not attest loaded code or exclude filesystem races.

Both producers call `capture`: a bounded `cargo --version`, an anchored census of
the producer's `debug/incremental` caches before and after the invocation, and
publication of the changed outputs with the recorder, producer, runner and
census pins, all rechecked immediately before publication. The producer prints
one `output provenance:` line: recorded/observed/unclaimed counts and the ledger
outcome. A nonzero build records nothing; it can only retire rows whose files
it removed, because rustc garbage-collects earlier sessions even when a build
fails. A changed source, a census boundary or a publication error publishes
nothing and leaves the previous ledger exact. `run` remains the bare command
boundary and publishes nothing.

Strict selection is owned by ARTIFACT-CLEANUP.17, guarded deletion by .16 and
the host-bound operator workflow by .14. Existing plans and receipts retain
their historical meaning. No cache deletion occurs here.
# ANCHOR_END: usage
"""


def command(producer: str, manifest: str) -> tuple[str, ...]:
    O.need(type(producer) is str and producer in O.PRODUCERS, "unknown Cargo producer")
    O.relative(manifest)
    root, test_filter = O.PRODUCERS[producer]
    O.need(manifest.startswith("target/p4-system-12/") and manifest.endswith("/Cargo.toml")
           and not A.beneath(manifest, root), "manifest outside owned input namespace")
    return ("cargo", "test", "--offline", "--manifest-path", manifest,
            "--target-dir", root, "--config", 'build.build-dir="' + root + '"',
            "--lib", test_filter, "--", "--nocapture")


def environment() -> dict[str, str]:
    env = {name: value for name, value in os.environ.items()
           if not name.startswith(("CARGO_", "RUSTC", "RUSTDOC", "GIT_"))
           and name not in {"RUSTFLAGS", "RUST_ENCODED_RUSTFLAGS"}}
    env.update(CARGO_HOME=str(ROOT / ".app-data/cargo-home"),
               TMPDIR=str(ROOT / "target/p4-system-12"),
               TMP=str(ROOT / "target/p4-system-12"), TEMP=str(ROOT / "target/p4-system-12"),
               CARGO_TERM_COLOR="never", PYTHONDONTWRITEBYTECODE="1")
    return env


def _stop(child):
    """Join the leader even if killing its group fails; never leave owned children."""
    try:
        os.killpg(child.pid, signal.SIGKILL)
    except (ProcessLookupError, PermissionError):
        # ESRCH: the group is gone. EPERM (macOS): every member has already exited — an unreaped
        # leader cannot be signalled, and a live descendant would have taken the signal instead
        # (measured 2026-10-27, XTASK.8: the pooled gate made the leader finish first). Either way
        # nothing owned is left running; the leader is joined below.
        pass
    finally:
        child.wait()


def _process(argv, env, *, timeout=TIMEOUT, pipe_bytes=PIPE_BYTES):
    O.need(type(timeout) in {int, float} and 0 < timeout <= TIMEOUT, "process deadline bound")
    O.need(type(pipe_bytes) is int and 0 < pipe_bytes <= PIPE_BYTES, "process pipe bound")
    with subprocess.Popen(argv, cwd=ROOT, env=env, stdin=subprocess.DEVNULL,
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE, start_new_session=True) as child:
        buffers = [bytearray(), bytearray()]
        deadline = time.monotonic() + timeout
        try:
            with selectors.DefaultSelector() as selector:
                selector.register(child.stdout, selectors.EVENT_READ, 0)
                selector.register(child.stderr, selectors.EVENT_READ, 1)
                while selector.get_map():
                    remaining = deadline - time.monotonic()
                    O.need(remaining > 0, "Cargo process timed out")
                    for event, _ in selector.select(remaining):
                        index = event.data
                        data = os.read(event.fd, min(65536, pipe_bytes - len(buffers[index]) + 1))
                        if not data:
                            selector.unregister(event.fileobj)
                        else:
                            buffers[index].extend(data)
                            O.need(len(buffers[index]) <= pipe_bytes, "Cargo output exceeds bound")
            code = child.wait(timeout=max(0.001, deadline - time.monotonic()))
            # The entire session belongs to this invocation, including a child
            # that closed both pipes before outliving its Cargo parent.
            _stop(child)
            return subprocess.CompletedProcess(argv, code, *(bytes(b).decode("utf-8", errors="replace")
                                                            for b in buffers))
        except subprocess.TimeoutExpired as error:
            _stop(child)
            raise O.ProvenanceError("Cargo process timed out") from error
        except BaseException:
            _stop(child)
            raise


@dataclass(frozen=True)
class Capture:
    result: subprocess.CompletedProcess
    observed: int
    recorded: int
    unclaimed: int
    publication: O.Publication | None


def _invoke(producer: str, manifest: Path, census=None):
    """One bound invocation; `census(owned)` observes the output root before and after it."""
    O.need(ROOT == A.ROOT == O.ROOT, "Cargo/planner/provenance roots differ")
    O.need(isinstance(manifest, Path), "manifest Path required")
    try:
        name = manifest.relative_to(ROOT).as_posix()
    except ValueError as error:
        raise O.ProvenanceError("manifest outside runtime root") from error
    argv = command(producer, name)
    # Public Git verifies that a copied runtime cannot silently borrow its parent.
    tracked = A.tracked_paths(ROOT)
    with A.OwnedRoot(ROOT) as owned, ExitStack() as resources:
        O._root_guard(owned)
        snapshots = {source: O._source(owned, source) for source in
                     (O.OBJECT, producer, *O.SUPPORTING_OBJECTS)}
        parent, leaf = name.rsplit("/", 1)
        directory = resources.enter_context(owned.directory(parent))
        before, _ = owned.snapshot(directory, leaf, name, O.SOURCE_BYTES)
        for path in (O.PRODUCERS[producer][0], ".app-data/cargo-home", "target/p4-system-12"):
            resources.enter_context(owned.directory(path, create=True))
        prior = None if census is None else census(owned)
        result = _process(argv, environment())
        later = None if census is None else census(owned)
        after, _ = owned.snapshot(directory, leaf, name, O.SOURCE_BYTES)
        O.need(before == after, "manifest changed during Cargo invocation")
        O.need(all(O._source(owned, source) == fact for source, fact in snapshots.items()),
               "producer source changed during Cargo invocation")
        O._root_guard(owned)
    return result, snapshots, tracked, prior, later


def run(producer: str, manifest: Path):
    """Run only a bound producer command; preserve its normal exit/stdout/stderr."""
    return _invoke(producer, manifest)[0]


def tool_version() -> str:
    """One bounded `cargo --version` line, recorded with each observation."""
    result = _process(("cargo", "--version"), environment(), timeout=30, pipe_bytes=4096)
    O.need(result.returncode == 0, "Cargo version query failed")
    text = result.stdout.strip()
    O.need(0 < len(text.encode("utf-8")) <= 1024 and "\n" not in text and "\r" not in text, "tool version bound")
    return text


def capture(producer: str, manifest: Path) -> Capture:
    """Run one bound build, record its changed outputs and publish them; a failed build publishes nothing."""
    version = tool_version()
    stamp = datetime.datetime.now(datetime.timezone.utc).isoformat()
    result, snapshots, tracked, prior, later = _invoke(producer, manifest, census=lambda owned: O.census(owned, producer))
    if result.returncode == 0:
        rows, unclaimed = O.observe(stamp, snapshots[O.OBJECT], snapshots[producer], result.args, version,
                                    result.returncode, tuple(snapshots[name] for name in O.SUPPORTING_OBJECTS),
                                    prior, later, tracked_paths=tracked)
    else:
        rows, unclaimed = (), 0  # a failed build records nothing; publication may still retire absent rows
    with A.OwnedRoot(ROOT) as owned:
        publication = O.publish(owned, rows, producer, frozenset(item.path for item in later))
    return Capture(result, len(later), len(rows), unclaimed, publication)


def describe(capture: Capture) -> str:
    """One line for the producer's output: what was observed, recorded and published."""
    publication = capture.publication
    if publication is None or not publication.written:
        ledger = "ledger unchanged" if publication is None or publication.ledger_sha256 is None else (
            f"ledger unchanged ({publication.records} records, sha256 {publication.ledger_sha256[:16]})")
    else:
        ledger = (f"ledger {publication.records} records/{publication.byte_size} B sha256 {publication.ledger_sha256[:16]}; "
                  f"added {publication.added}, replaced {publication.replaced}, retired {publication.retired}, "
                  f"retained {publication.retained}")
    return (f"output provenance: recorded {capture.recorded} of {capture.observed} observed outputs "
            f"({capture.unclaimed} unclaimed); {ledger}")
