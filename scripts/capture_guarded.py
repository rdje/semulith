#!/usr/bin/env python3
"""Capture declared finite cases, each exactly once, only on a tree and a host fit for it.

`scripts/retain_div_capture.py` owns the capture and refuses a second one. This is the procedure around it, which lived
under `target/` until P4-SYSTEM.14 a50-c2 (docs/decisions/decision_capture-guard-measured-at-load.md):

- the tracked tree is clean, and no gate of this checkout is running;
- the declaration commit is an ancestor of HEAD, and nothing a case pins, nor an authority view no manifest names, has
  moved since it;
- before each case the 1-minute load is below LOAD_LIMIT and SPAWNS children spawn and reap the collector's way, for at
  most HOLD_SECONDS, after which it stops with nothing spent;
- the tree is judged again after any hold, and the case's preflight must be ready;
- a case already holding verification.json is skipped and never run again;
- the first non-zero capture stops the run, and nothing is retried.

`--check` runs every guard but the host's and captures nothing.

Exit: 0 every case captured or already captured, or `--check` found them ready; 2 usage; 3 refused; 4 the host stayed
unfit; otherwise the capture's own exit.
"""

from __future__ import annotations

import argparse
import os
from pathlib import Path
import re
import signal
import subprocess
import sys
import time
from typing import Callable, Sequence

import sexp as S

ROOT = Path(__file__).resolve().parent.parent
LOAD_LIMIT = 32.0  # measured: 0 refusals in 210 captures at load 15 to 73, 184 of them below this
SPAWNS = 50
HOLD_SECONDS = 600
POLL_SECONDS = 30
OBJECT_ID = re.compile(r"[0-9a-f]{40}")
# What the capture's authority loader reads and a manifest does not name.
AUTHORITY_VIEWS = (
    "crates/semulith-verify/src/contract_checks_rv64gc.rs",
    "profiles/rv64gc-lab-v0/contract-obligations.sexp",
    "profiles/rv64gc-lab-v0/contract-v0.obligations.sexp",
    "profiles/rv64gc-lab-v0/contract-v1.obligations.sexp",
    "profiles/rv64gc-lab-v0/contract.sexp",
    "profiles/rv64gc-lab-v0/references.sexp",
    "profiles/rv64gc-lab-v0/requirements.sexp",
    "profiles/rv64gc-lab-v0/sources.sexp",
    "schema/contract-obligations.sexp",
    "schema/contract.sexp",
    "schema/requirements.sexp",
    "schema/sources.sexp",
)

Log = Callable[[str], None]


class Refused(Exception):
    """The tree or a case is not fit to capture from; nothing was spent."""


def _git(root: Path, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run(["git", "-C", str(root), *args], capture_output=True, text=True, check=False)


def frozen_paths(root: Path, cases: Sequence[str]) -> set[str]:
    """Every input each case's manifest pins, and the authority views no manifest names."""
    paths = set(AUTHORITY_VIEWS)
    for case in cases:
        manifest = root / "evidence" / case / "dependencies.sexp"
        if not manifest.is_file():
            raise Refused(f"{case}: no declared manifest at {manifest.relative_to(root)}")
        forms = S.parse(manifest.read_text())
        named = [str(S.children(item, "path")[0][1])
                 for form in forms if isinstance(form, list) and form and str(form[0]) == "dependencies"
                 for item in S.children(form, "input")]
        if not named:
            raise Refused(f"{case}: its manifest pins nothing")
        paths.update(named)
    return paths


def require_fit_tree(root: Path, cases: Sequence[str], commit: str) -> None:
    if OBJECT_ID.fullmatch(commit) is None:
        raise Refused("the declaration commit must be a 40-hex object id")
    if _git(root, "merge-base", "--is-ancestor", commit, "HEAD").returncode != 0:
        raise Refused(f"{commit} is not an ancestor of HEAD")
    status = _git(root, "status", "--porcelain", "--untracked-files=no")
    if status.returncode != 0 or status.stdout.strip():
        raise Refused("the tracked tree is not clean")
    moved = set(_git(root, "diff", "--name-only", commit, "HEAD").stdout.split()) & frozen_paths(root, cases)
    if moved:
        raise Refused(f"moved since {commit[:8]}: {', '.join(sorted(moved))}")


def own_gate_running(root: Path) -> bool:
    return subprocess.run(["pgrep", "-f", f"{root}/.*check_doctrines|cargo xtask focused"], capture_output=True, check=False).returncode == 0


def spawn_probe(count: int = SPAWNS) -> None:
    """Children spawned and reaped the collector's way, the operation the load-sensitive refusal strikes. OSError if one fails."""
    for _ in range(count):
        process = subprocess.Popen([sys.executable, "-I", "-B", "-S", "-c", "pass"], stdin=subprocess.DEVNULL,
                                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, start_new_session=True)
        process.wait()
        try:
            os.killpg(process.pid, signal.SIGKILL)
        except ProcessLookupError:
            pass


def host_ready(log: Log, *, load: Callable[[], float] = lambda: os.getloadavg()[0], spawn: Callable[[], None] = spawn_probe,
               sleep: Callable[[float], None] = time.sleep, clock: Callable[[], float] = time.monotonic) -> bool:
    deadline = clock() + HOLD_SECONDS
    while True:
        current = load()
        if current < LOAD_LIMIT:
            try:
                spawn()
            except OSError as error:
                log(f"spawn probe refused at load {current:.2f}: {error}")
            else:
                log(f"host ready: load {current:.2f}, {SPAWNS} of {SPAWNS} spawned and reaped")
                return True
        else:
            log(f"load {current:.2f} is at or above {LOAD_LIMIT:g}: holding")
        if clock() >= deadline:
            return False
        sleep(POLL_SECONDS)


def preflight(root: Path, case: str, commit: str) -> None:
    done = subprocess.run([sys.executable, "-B", str(root / "scripts/retain_div_capture.py"), "--case", case,
                           "--declaration-commit", commit, "--preflight-only"], capture_output=True, text=True, cwd=root, check=False)
    if done.returncode != 0:
        raise Refused(f"{case}: preflight refused: {done.stdout.strip()[-400:]}")


def capture(root: Path, case: str, commit: str, out: Path) -> int:
    directory = out / case
    directory.mkdir(parents=True, exist_ok=True)
    with (directory / "capture.json").open("wb") as stdout, (directory / "capture.err").open("wb") as stderr:
        return subprocess.run([sys.executable, "-B", str(root / "scripts/retain_div_capture.py"), "--case", case,
                               "--declaration-commit", commit], stdout=stdout, stderr=stderr, cwd=root, check=False).returncode


def run(root: Path, cases: Sequence[str], commit: str, out: Path, log: Log, *, check_only: bool = False,
        host: Callable[[Log], bool] = host_ready, ready: Callable[[Path, str, str], None] = preflight,
        take: Callable[[Path, str, str, Path], int] = capture, gate: Callable[[Path], bool] = own_gate_running) -> int:
    try:
        require_fit_tree(root, cases, commit)
        if gate(root):
            raise Refused("this checkout's own gate is running")
    except Refused as refused:
        log(f"refused: {refused}")
        return 3
    for case in cases:
        if (root / "evidence" / case / "verification.json").exists():
            log(f"{case}: already captured; never run again")
            continue
        if not check_only and not host(log):
            log(f"{case}: the host stayed unfit for {HOLD_SECONDS} s; nothing captured")
            return 4
        try:
            require_fit_tree(root, cases, commit)
            ready(root, case, commit)
        except Refused as refused:
            log(f"refused: {refused}")
            return 3
        if check_only:
            log(f"{case}: ready")
            continue
        code = take(root, case, commit, out)
        log(f"{case} capture rc={code}")
        if code != 0:
            return code
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--case", action="append", required=True, help="a declared case; repeat for each, in order")
    parser.add_argument("--declaration-commit", required=True, help="the 40-hex commit that retained the declarations")
    parser.add_argument("--out", type=Path, help="where each case's capture.json and capture.err go; target/captures/<commit> by default")
    parser.add_argument("--check", action="store_true", help="run every guard but the host's; capture nothing")
    args = parser.parse_args(argv)
    out = args.out or ROOT / "target" / "captures" / args.declaration_commit[:12]
    out.mkdir(parents=True, exist_ok=True)

    def log(line: str) -> None:
        stamped = f"{time.strftime('%H:%M:%SZ', time.gmtime())} {line}"
        print(stamped, flush=True)
        with (out / "guard.log").open("a") as file:
            file.write(stamped + "\n")

    return run(ROOT, args.case, args.declaration_commit, out, log, check_only=args.check)


if __name__ == "__main__":
    sys.exit(main())
