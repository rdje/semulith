#!/usr/bin/env python3
"""The spec-side constants of the rv64gc workload suite (P4-SYSTEM.15 slice f), derived here — in Python's
arbitrary-precision integers and its IEEE binary64 / binary32 arithmetic (the C abstract machine's values for the
operations the sources name) — and checked against the EMIT constants the tracked C sources carry. Never a model's
output: a workload whose expected values came from the engine would test self-consistency and nothing else (EVD-05).

    python3 scripts/derive_workload_constants.py            # print every constant, per workload and slot
    python3 scripts/derive_workload_constants.py --check    # compare with profiles/rv64gc-lab-v0/workload/wl-*.c

The campaign runner refuses to build when --check finds drift.
"""
from __future__ import annotations

import functools
import re
import struct
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
WORKLOAD = ROOT / "profiles/rv64gc-lab-v0/workload"
M64 = (1 << 64) - 1
M32 = (1 << 32) - 1


def tdiv(a: int, b: int) -> tuple[int, int]:
    """C99 division: the quotient truncates toward zero, the remainder takes the dividend's sign."""
    q = abs(a) // abs(b)
    q = q if (a < 0) == (b < 0) else -q
    return q, a - q * b


def u64(v: int) -> int:
    return v & M64


def f32(x: float) -> float:
    return struct.unpack("f", struct.pack("f", x))[0]


def bits64(x: float) -> int:
    return struct.unpack("<Q", struct.pack("<d", x))[0]


def bits32(x: float) -> int:
    return struct.unpack("<I", struct.pack("<f", x))[0]


def integer() -> list[int]:
    def collatz(n: int) -> int:
        s = 0
        while n != 1:
            n = 3 * n + 1 if n & 1 else n // 2
            s += 1
        return s

    def lcg(x: int, rounds: int) -> int:
        for _ in range(rounds):
            x = (x * 1664525 + 1013904223) & M32
        return x

    q1, r1 = tdiv(-7, 2)
    q2, r2 = tdiv(7, -2)
    p = (M64) * (M64)
    p2 = -3 * 5
    a, b = 0x80000000, 3
    q3, r3 = tdiv(-2147483648, 7)
    return [
        collatz(27), collatz(97), pow(3, 200, 1000000007), lcg(1, 10),
        u64(q1 * 1000 + r1), u64(q2 * 1000 + r2),
        ((p >> 64) ^ (p & M64)) & M64, u64((p2 >> 64) + -15),
        (a // b + a % b + (a * b)) & M32, u64(q3 - r3),
    ]


def memory() -> list[int]:
    data = [((i * 2654435761) ^ (i << 7)) & 0xffff for i in range(64)]
    srt = sorted(data)

    def crc32(bs: bytes) -> int:
        c = 0xffffffff
        for byte in bs:
            c ^= byte
            for _ in range(8):
                c = (c >> 1) ^ (0xedb88320 if c & 1 else 0)
        return c ^ 0xffffffff

    pattern = bytes((i * 37 + 11) & 0xff for i in range(256))
    seed = 0x0123456789abcdef
    b, h, w, d = seed & 0xff, (seed >> 8) & 0xffff, (seed >> 24) & M32, (seed * 3) & M64
    return [
        sum(srt[i] * (i + 1) for i in range(64)) & M64, srt[0], srt[63], crc32(pattern),
        (b + h + w + d) & M64, d & 0xff,
        functools.reduce(lambda s, v: (s * 31 + v) & M64, [i * i + 1 for i in range(16)], 0),
    ]


def float_() -> list[int]:
    a, b, c = 1.5, -2.25, 0.125
    af, bf = f32(3.5), f32(0.75)
    return [
        bits64(a * b + c), bits64(6.25 ** 0.5), bits64(7.0 / 8.0), bits32(f32(af * bf)),
        0, 1, 1, u64(int(-7.75)), bits64(float(-13)), 1 << 0, bits64(af),
    ]


def calls() -> list[int]:
    sys.setrecursionlimit(10000)

    def ack(m: int, n: int) -> int:
        return n + 1 if m == 0 else (ack(m - 1, 1) if n == 0 else ack(m - 1, ack(m, n - 1)))

    def fib(n: int) -> int:
        return n if n < 2 else fib(n - 1) + fib(n - 2)

    disp = [lambda x: x + 7, lambda x: x * 3, lambda x: x ^ 0x55, lambda x: x >> 1]
    d, x = 0, 100
    for i in range(12):
        x = disp[i % 4](x) & M64
        d = (d * 131 + x) & M64
    return [ack(2, 3), fib(15), d, sum((k + 1) * (k + 1) for k in range(9))]


WORKLOADS = {"wl-integer": integer, "wl-memory": memory, "wl-float": float_, "wl-calls": calls}
EMIT = re.compile(r"EMIT\((.*?),\s*((?:\(u64\)\(i64\)\()?[-0-9a-fA-Fx+\s<()u|l]+?)\);", re.S)


def constants_in(source: str) -> list[int]:
    """Every EMIT's expected constant, as the C compiler would evaluate it (integers, casts, shifts, sums)."""
    out = []
    for m in EMIT.finditer(source):
        expr = m.group(2)
        expr = re.sub(r"(0x[0-9a-fA-F]+|\d+)(ull|ul|ll|u|l)\b", r"\1", expr)
        expr = expr.replace("(u64)(i64)", "").replace("(u64)", "")
        value = eval(expr, {"__builtins__": {}})  # noqa: S307 — a numeric literal expression from a tracked source
        out.append(value & M64)
    return out


def main(argv: list[str]) -> int:
    check = "--check" in argv
    drift = 0
    for name, derive in WORKLOADS.items():
        want = derive()
        if check:
            have = constants_in((WORKLOAD / f"{name}.c").read_text())
            if have != want:
                drift += 1
                for i, (h, w) in enumerate(zip(have, want)):
                    if h != w:
                        print(f"DRIFT {name} slot {i}: the source carries {h:#x}, the derivation says {w:#x}")
                if len(have) != len(want):
                    print(f"DRIFT {name}: {len(have)} EMIT constant(s) in the source, {len(want)} derived")
        else:
            for i, w in enumerate(want):
                print(f"{name} slot {i}: {w:#x}")
    if check:
        total = sum(len(d()) for d in WORKLOADS.values())
        if drift:
            print(f"derive_workload_constants: DRIFT in {drift} workload(s)")
            return 1
        print(f"derive_workload_constants: ok — {total} constants in {len(WORKLOADS)} workloads re-derived and equal")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
