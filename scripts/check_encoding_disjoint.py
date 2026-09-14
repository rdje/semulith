#!/usr/bin/env python3
"""Decide whether instruction-encoding fragments COMPOSE — the decidable half of composition.

⭐ WHY THIS IS THE FIRST THING BUILT. `decision_composition-model` commits to reaching breadth by
assembling proven small models rather than by gating large ones less. Union of encodings is the one
composition operator that is **decidable**: an instruction's fixed bits form a (mask, value) pair,
and two instructions collide exactly when some 32-bit word matches both. That is a finite check, so
"these fragments compose" is a **verdict** rather than a hope — and it catches a real class of
mistake mechanically, on the day two fragments are first put together.

⚠️ AND IT IS ONLY THE EASY HALF, stated so nobody reads a green result as more than it is. Union of
*semantics* is not decidable in general: an extension can change the meaning of a base instruction
— adding CSRs changes trap behaviour, adding `C` changes `IALIGN` and therefore which branch
targets fault. A disjoint encoding space says the decoder composes. It says nothing about whether
the meanings do. `MODEL-COMPOSE.6` owns that with explicitly declared refinement points.

Two instructions collide when their fixed bits are compatible on every bit both constrain:

    overlap  ⇔  (value_a ^ value_b) & mask_a & mask_b == 0

Usage:  check_encoding_disjoint.py <fragment.sexp|opcodes-dir> [more…]
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import sexp as _sexp  # noqa: E402


class Insn:
    __slots__ = ("name", "mask", "value", "origin")

    def __init__(self, name: str, fixed: list[tuple[int, int, int]], origin: str):
        self.name, self.origin = name, origin
        self.mask = self.value = 0
        for hi, lo, val in fixed:
            width = hi - lo + 1
            if val >= (1 << width):
                raise ValueError(f"{name}: fixed value {val:#x} does not fit bits [{hi}:{lo}]")
            self.mask |= ((1 << width) - 1) << lo
            self.value |= val << lo


def load_fragment(path: Path) -> list[Insn]:
    """Read a fragment: either an `encoding.sexp` or a riscv-opcodes table file."""
    if path.suffix == ".sexp":
        enc = _sexp.read_file(path)[0]
        out = []
        for i in _sexp.children(enc, "insn"):
            fixed = [(int(a), int(b), int(c)) for a, b, c in _sexp.children(i, "fixed")[0][1:]]
            out.append(Insn(str(_sexp.field(i, "name")), fixed, path.name))
        return out
    # a riscv-opcodes extension table
    fixed_re = re.compile(r"^(\d+)\.\.(\d+)=(\S+)$")
    single_re = re.compile(r"^(\d+)=(\S+)$")
    out = []
    for raw in path.read_text().splitlines():
        line = raw.split("#", 1)[0].strip()
        if not line or line.startswith("$"):
            continue
        name, *rest = line.split()
        fixed: list[tuple[int, int, int]] = []
        for tok in rest:
            m = fixed_re.match(tok)
            if m:
                fixed.append((int(m.group(1)), int(m.group(2)), int(m.group(3), 0)))
                continue
            m = single_re.match(tok)
            if m:
                b = int(m.group(1))
                fixed.append((b, b, int(m.group(2), 0)))
        if fixed:
            out.append(Insn(name, fixed, path.name))
    return out


def collisions(insns: list[Insn]) -> list[tuple[Insn, Insn]]:
    """Every pair whose encodings overlap. O(n²) and n is in the hundreds — exhaustive is fine,
    and an exhaustive answer is the point: a sampled one would not be a decision."""
    out = []
    for i in range(len(insns)):
        a = insns[i]
        for j in range(i + 1, len(insns)):
            b = insns[j]
            common = a.mask & b.mask
            if (a.value ^ b.value) & common == 0:
                out.append((a, b))
    return out


def main(argv: list[str]) -> int:
    if len(argv) < 2:
        print("usage: check_encoding_disjoint.py <fragment…>", file=sys.stderr)
        return 2
    insns: list[Insn] = []
    for arg in argv[1:]:
        p = Path(arg)
        if not p.exists():
            print(f"REFUSED: {p} does not exist", file=sys.stderr)
            return 2
        part = load_fragment(p)
        if not part:
            print(f"REFUSED: {p} yielded no instructions — an empty fragment is not a valid one",
                  file=sys.stderr)
            return 2
        print(f"  fragment {p.name:16} {len(part):3} instruction(s)")
        insns += part

    dupes = [n for n in {i.name for i in insns} if sum(1 for i in insns if i.name == n) > 1]
    bad = collisions(insns)
    print(f"\n  composed set: {len(insns)} instruction(s) from {len(argv) - 1} fragment(s)")
    if dupes:
        print(f"  DUPLICATE NAME(S): {sorted(dupes)}")
    if bad:
        print(f"  COLLISIONS: {len(bad)}")
        for a, b in bad[:10]:
            print(f"    {a.name} ({a.origin}) overlaps {b.name} ({b.origin})  "
                  f"mask={a.mask & b.mask:#010x}")
        print("\n  REJECTED — these fragments do not compose. A decoder cannot be generated from a")
        print("  set in which one word matches two instructions.")
        return 1
    print("  no collisions, no duplicate names — the fragments COMPOSE.")
    print("  ⚠️ This decides the DECODER composes. It says nothing about whether the semantics do.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
