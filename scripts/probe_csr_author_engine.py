#!/usr/bin/env python3
"""CSR-AUTHOR-ENGINE: the expectations author and the lab engine keep the same bits of every CSR the author writes.

P4-SYSTEM.20 slice b1 (decision_csr-write-three-producers.md, "a probe holding the author to the engine, each CSR field by
field"). For each CSR the author can write, a short guest writes a sequence of values and reads the CSR back into x3; the
author derives the read-back spec-side (`derive_snapshot`) and the engine runs the same image (`semulith run`). A case
agrees when both read back the same value. The values are chosen to reach every field: all ones, zero, the two alternating
patterns, and for a CSR with a `one-of` field each legal value followed by each illegal one, so a field that must keep its
old value is seen keeping it.

Usage, from the repository root:
    python3 -B scripts/probe_csr_author_engine.py              # every case; exit 0 when all agree
    python3 -B scripts/probe_csr_author_engine.py --mutation tvec-mode-bit0
                                                               # the author's pre-b1 tvec rule; exit 1, its cases named
The engine is built once (`cargo build -q --offline -p semulith-cli`). Nothing is written outside target/."""
from __future__ import annotations

import argparse
import re
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
import derive_rv64gc_expectations as Author  # noqa: E402
from riscv_asm import Assembler, write_elf64  # noqa: E402

UNIT = ROOT / "profiles/rv64gc-lab-v0"
ENGINE = ROOT / "target/debug/semulith"
CSRS = ("medeleg mideleg mtvec stvec mepc sepc mcause scause mtval stval mscratch sscratch mie sie mip sip "
        "mcounteren scounteren menvcfg stimecmp fflags frm fcsr").split()
FP = {"fflags", "frm", "fcsr"}
SENTINEL = 0x5A5

# How a 64-bit value reaches x2 with real instructions only (x4 is scratch; x3 is the read-back).
LOADS = {
    0: ["addi x2, x0, 0"],
    (1 << 64) - 1: ["addi x2, x0, -1"],
    0x5555555555555555: ["lui x2, 0x55555", "addi x2, x2, 0x555", "slli x4, x2, 32", "or x2, x2, x4"],
    0xAAAAAAAAAAAAAAAA: ["lui x2, 0x55555", "addi x2, x2, 0x555", "slli x4, x2, 32", "or x2, x2, x4",
                         "xori x2, x2, -1"],
}
for small in range(1, 4):
    LOADS[small] = [f"addi x2, x0, {small}"]


def one_of_fields(name: str) -> list[tuple[int, list[int], int]]:
    """(bit_lo, legal values, field width) for every `one-of` field the state table declares for `name`."""
    import dossier_sexp as D
    doc = D.load_state(UNIT / "state.sexp")
    csr = next((c for c in doc.get("csr", []) if c["id"] == name), None)
    out = []
    for f in (csr or {}).get("fields", []):
        lg = f.get("legalize") or {}
        if lg.get("kind") == "one-of":
            out.append((f["bit_lo"], lg["values"], f["bit_hi"] - f["bit_lo"] + 1))
    return out


def cases() -> list[tuple[str, tuple[int, ...]]]:
    out = []
    for c in CSRS:
        for v in (0, (1 << 64) - 1, 0x5555555555555555, 0xAAAAAAAAAAAAAAAA):
            out.append((c, (v,)))
        for lo, legal, width in one_of_fields(c):
            illegal = [x for x in range(1 << width) if x not in legal]
            for good in legal:
                for bad in illegal:
                    first, second = good << lo, bad << lo
                    if first in LOADS and second in LOADS:
                        out.append((c, (first, second)))
    return out


def guest(csr: str, values: tuple[int, ...]) -> str:
    lines = ["lui x2, 6", "csrrs x0, mstatus, x2"] if csr in FP else []   # FS = Dirty, so the FP CSRs are reachable
    for v in values:
        lines += LOADS[v] + [f"csrrw x0, {csr}, x2"]
    # x3 is seeded first: the engine prints a register only when it changes, so a read-back equal to x3's old value would
    # print nothing. 0x5a5 mixes odd and even bits, so no written pattern, under any mask, reads back as it.
    return "\n".join(lines + [f"addi x3, x0, {SENTINEL}", f"csrrs x3, {csr}, x0"]) + "\n"


def author_reads(text: str) -> int | str:
    n = len(text.splitlines())
    try:
        snap = Author.derive_snapshot(text.encode(), program="probe.s", instructions=n)
    except Exception as exc:  # noqa: BLE001 — a refusal is a result, reported as such
        return f"REFUSED {exc}"[:60]
    return dict(snap.steps[n - 1].writes).get(3, "no x3 write")


def engine_reads(text: str, asm: Assembler, scratch: Path) -> int | str:
    n = len(text.splitlines())
    elf = scratch / "probe.elf"
    write_elf64(elf, Author.ENTRY, asm.assemble_image(text.splitlines(), base=Author.ENTRY), asm.ialign)
    p = subprocess.run([str(ENGINE), "run", str(elf), "--profile=rv64gc-lab-v0", f"--steps={n}"],
                       capture_output=True, text=True, timeout=60, check=False)
    found = re.findall(r"x3 <- (0x[0-9a-f]+)", p.stdout)
    if not found or int(found[-1], 16) == SENTINEL:
        return f"no x3 write (rc={p.returncode})" if p.returncode else "no x3 write"
    return int(found[-1], 16)


def mutate(name: str) -> None:
    """Restore a defect the probe exists to catch, in this process's author only."""
    if name != "tvec-mode-bit0":
        raise SystemExit(f"probe_csr_author_engine: unknown mutation {name}")
    write = Author.csr_write_value

    def legacy(h, csr, v):
        if csr in ("mtvec", "stvec"):
            h.csr[csr] = (v & ~0b11) | (v & 0b1)   # the author's rule before slice b1: MODE takes bit 0 of any value
            return
        write(h, csr, v)
    Author.csr_write_value = legacy


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--mutation")
    args = ap.parse_args(argv)
    if args.mutation:
        mutate(args.mutation)
    built = subprocess.run(["cargo", "build", "-q", "--offline", "-p", "semulith-cli"], cwd=ROOT,
                           capture_output=True, text=True, check=False)
    if built.returncode or not ENGINE.is_file():
        print(f"CSR-AUTHOR-ENGINE: REFUSED — the engine did not build: {built.stderr.strip()[-300:]}", file=sys.stderr)
        return 2
    asm = Assembler(UNIT / "encoding.sexp")
    (ROOT / "target/tmp").mkdir(parents=True, exist_ok=True)
    differ = []
    all_cases = cases()
    with tempfile.TemporaryDirectory(dir=ROOT / "target/tmp", prefix="csr-author-engine.") as tmp:
        for csr, values in all_cases:
            text = guest(csr, values)
            a, e = author_reads(text), engine_reads(text, asm, Path(tmp))
            if a != e:
                fa = hex(a) if isinstance(a, int) else a
                fe = hex(e) if isinstance(e, int) else e
                differ.append(f"  {csr} <- {' then '.join(hex(v) for v in values)}: author {fa}, engine {fe}")
    for line in differ:
        print(line)
    print(f"CSR-AUTHOR-ENGINE: {len(all_cases)} cases over {len(CSRS)} CSRs, {len(differ)} differ")
    return 1 if differ else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
