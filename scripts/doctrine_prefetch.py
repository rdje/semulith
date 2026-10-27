#!/usr/bin/env python3
"""Run a doctrine self-test's recorded probe invocations in parallel (XTASK.8 slice c).

`doctrine_prefetch.py <argv-file> <out-dir> [--jobs N]` reads the invocations a self-test recorded on its
recording pass — one per line, the arguments after `python3` separated by U+001F — runs each DISTINCT one once,
in parallel, from the repository root, and writes its combined output and exit status to <out-dir>/<key>.out
and <key>.rc, where <key> is the line itself with every `/` as U+001E (a file name the self-test rebuilds from
its own argv by parameter expansion alone). The self-test then answers an invocation from the record when the
argv matches exactly and runs it live otherwise — a missed shape costs time, never a wrong answer. Nothing here
decides a verdict: the outputs are the probes' own, scored by the check as before.

`--list` prints the distinct invocations (fields separated by U+001F) and runs nothing.
"""
from __future__ import annotations

import argparse
import os
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

sys.dont_write_bytecode = True
# the repository root: the nearest ancestor holding scripts/sexp.py (the runner may be copied under target/ to
# measure before it is tracked)
ROOT = next(p for p in Path(__file__).resolve().parents if (p / "scripts" / "sexp.py").is_file())
SEP = "\x1f"


def read_invocations(path: Path) -> list[list[str]]:
    """The distinct argument lists recorded, in first-seen order (the heavy arms tend to come last)."""
    seen: dict[tuple[str, ...], None] = {}
    for line in path.read_text().splitlines():
        if line:
            seen.setdefault(tuple(line.split(SEP)), None)
    return [list(k) for k in seen]


def key(args: list[str]) -> str:
    return SEP.join(args).replace("/", "\x1e")


def run_one(args: list[str], out_dir: Path) -> int:
    proc = subprocess.run(["python3", *args], cwd=ROOT, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE,
                          stderr=subprocess.STDOUT, check=False)
    k = key(args)
    (out_dir / (k + ".out")).write_bytes(proc.stdout)
    (out_dir / (k + ".rc")).write_text(f"{proc.returncode}\n")
    return proc.returncode


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("argv_file")
    parser.add_argument("out_dir", nargs="?")
    parser.add_argument("--jobs", type=int, default=os.cpu_count() or 4)
    parser.add_argument("--list", action="store_true")
    args = parser.parse_args(argv[1:])
    invocations = read_invocations(Path(args.argv_file))
    if args.list:
        for inv in invocations:
            print(SEP.join(inv))
        return 0
    if not args.out_dir:
        print("doctrine_prefetch: an output directory is required unless --list", file=sys.stderr)
        return 2
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    # the longest-running invocations are the ones recorded last; start them first so the pool's tail is short
    with ThreadPoolExecutor(max_workers=max(1, args.jobs)) as pool:
        results = list(pool.map(lambda inv: run_one(inv, out_dir), reversed(invocations)))
    print(f"doctrine_prefetch: {len(results)} distinct invocation(s) recorded under {out_dir}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
