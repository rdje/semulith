#!/usr/bin/env python3
"""scripts/compare_dumps.py — the checkpoint-level canonical-state comparator.

The DSP56300 evidence shape is NOT the RISC-V per-instruction commit walk: the reference
(`mborgerson/dsp56300`'s difftest, tools/difftest/README.md at the pinned commit) compares
per-CASE canonical end-state — registers, deviation-encoded memory windows, hardware stack
slots — and its harness is engine-agnostic by contract ("anything that can produce the
canonical dump format can be compared"). This comparator is that judgement for two dump
files (reference vs Semulith's `semulith-dsp56300` runner):

- the case names must be equal;
- every key except `cyc` must be present on BOTH sides with the same value — a missing
  key is a mismatch, never a default (both engines deviation-encode against the same
  init, so the key SETS are comparable);
- `cyc` is SKIPPED BY RECORDED RULE: it is informational upstream (LIMITATIONS §4 — base
  cycle table only, pipeline interlocks unmodelled), Semulith's model emits no timing, and
  no cycle claim may ever ride this path. The skip is reported, never silent.

CONTRACT: exit code is the verdict (0 agree, 1 disagree, 2 cannot judge); explains on
stderr; deterministic; read-only; no network. `--self-test` runs RED/GREEN arms.

Usage: scripts/compare_dumps.py <dump-a> <dump-b> | --self-test
"""

from __future__ import annotations

import sys
import tempfile
from pathlib import Path

SKIPPED_KEYS = {"cyc"}


def parse_dump(path: Path) -> tuple[str, dict[str, str]]:
    case = None
    fields: dict[str, str] = {}
    saw_end = False
    for n, raw in enumerate(path.read_text().splitlines(), 1):
        line = raw.strip()
        if not line:
            continue
        head, _, rest = line.partition(" ")
        if head == "case":
            case = rest
        elif head == "end":
            saw_end = True
        elif head and rest:
            if head in fields:
                raise ValueError(f"{path}:{n}: duplicate key {head!r}")
            fields[head] = rest
        else:
            raise ValueError(f"{path}:{n}: not a key/value line: {raw!r}")
    if case is None or not saw_end:
        raise ValueError(f"{path}: not a complete dump (needs `case` and `end`)")
    return case, fields


def compare(path_a: Path, path_b: Path) -> tuple[bool, str]:
    case_a, a = parse_dump(path_a)
    case_b, b = parse_dump(path_b)
    if case_a != case_b:
        return False, f"case names differ: {case_a!r} vs {case_b!r}"
    skipped = sorted(SKIPPED_KEYS & (a.keys() | b.keys()))
    a = {k: v for k, v in a.items() if k not in SKIPPED_KEYS}
    b = {k: v for k, v in b.items() if k not in SKIPPED_KEYS}
    for key in sorted(a.keys() | b.keys()):
        va, vb = a.get(key), b.get(key)
        if va is None:
            return False, f"key {key!r} present only in {path_b} (={vb})"
        if vb is None:
            return False, f"key {key!r} present only in {path_a} (={va})"
        if va != vb:
            return False, f"FIRST MISMATCH {key}: {va} vs {vb}"
    note = f" (skipped by rule: {', '.join(skipped)})" if skipped else ""
    return True, f"AGREE over {len(a)} fields for case {case_a!r}{note}"


def self_test() -> int:
    arms = 0
    with tempfile.TemporaryDirectory() as td:
        d = Path(td)

        def write(name: str, text: str) -> Path:
            p = d / name
            p.write_text(text)
            return p

        base = "case t\nsteps 3\npc 000100\na1 1f253d\ncyc 29\nend\n"
        # GREEN: identical apart from the skipped key.
        agree, _ = compare(write("g1", base), write("g2", base.replace("cyc 29", "cyc 31")))
        arms += 1
        if not agree:
            print("compare_dumps --self-test RED MISS: cyc difference must be skipped")
            return 1
        # RED: a value mismatch is detected and named.
        agree, msg = compare(write("r1", base), write("r2", base.replace("a1 1f253d", "a1 1f253e")))
        arms += 1
        if agree or "a1" not in msg:
            print("compare_dumps --self-test RED MISS: a value mismatch was not caught")
            return 1
        # RED: a missing key is a mismatch, not a default zero.
        agree, msg = compare(write("r3", base), write("r4", base.replace("a1 1f253d\n", "")))
        arms += 1
        if agree or "present only" not in msg:
            print("compare_dumps --self-test RED MISS: a missing key was defaulted")
            return 1
        # RED: different case names are a mismatch.
        agree, _ = compare(write("r5", base), write("r6", base.replace("case t", "case u")))
        arms += 1
        if agree:
            print("compare_dumps --self-test RED MISS: case-name mismatch was not caught")
            return 1
    print(f"compare_dumps --self-test: {arms} pass / 0 fail")
    return 0


def main() -> int:
    if len(sys.argv) == 2 and sys.argv[1] == "--self-test":
        return self_test()
    if len(sys.argv) != 3:
        print(__doc__, file=sys.stderr)
        return 2
    try:
        agree, msg = compare(Path(sys.argv[1]), Path(sys.argv[2]))
    except (OSError, ValueError) as e:
        print(f"compare_dumps: cannot judge — {e}", file=sys.stderr)
        return 2
    print(msg, file=sys.stderr if not agree else sys.stdout)
    return 0 if agree else 1


if __name__ == "__main__":
    sys.exit(main())
