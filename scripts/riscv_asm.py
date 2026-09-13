#!/usr/bin/env python3
"""A minimal RV64I assembler and ELF64 writer, for independently encoded guest programs.

WHY THIS EXISTS, and why it does not simply call a cross-compiler.
`docs/EVIDENCE_AND_GATES.md` and rule `EVD-05` require a guest program's expected observations
to be derived from the SPECIFICATION, not from any model's output. A toolchain would also be a
fine encoder, but it would be one more artifact whose provenance has to be established, and on
this host it would have to be installed off the repository volume. This assembler is 300 lines,
reads its encodings from a pinned table, and produces a file whose every byte is accounted for.

⛔ WHERE THE ENCODINGS COME FROM, and why it is not this file.
The pinned specification artifacts do NOT contain instruction encodings. Measured over all six
of them (three HTML pages and their text renderings): `grep -cE '[01]{7}'` -> 0, 0, 0, 0, 0, 0.
The format diagrams are IMAGES (31 in the RV32I chapter alone), so the bit layouts are simply
not in the bytes this project pinned. The SEMANTICS are all there in prose — which is the half
that matters for expected values — but the encodings had to come from somewhere else.

They come from `riscv-opcodes` (RISC-V International, BSD-3-Clause), pinned under
`target/refs/riscv-opcodes/` and re-derived by `scripts/fetch_references.sh`:
    extensions/rv_i, extensions/rv64_i   the fixed bits and operand list per instruction
    arg_lut.csv                          the operand field positions
This module PARSES those files. It does not carry an opcode constant of its own, so a typo here
cannot invent an instruction — it can only fail to find one.

⚠️ SHARED ANCESTRY, STATED NOT HIDDEN. `riscv-opcodes` is upstream of both Sail and Spike for
encodings, so "our bytes decode the way the model expects" is NOT an independent confirmation of
the encoding. It is independent for SEMANTICS, which is what the differential test is actually
for. The mitigation applied is a second decoder from a different codebase: `spike-dasm` is asked
to disassemble the bytes this module emits, and must return the mnemonics that were requested.

⛔ SCOPE LIMIT, deliberate. Only instruction formats whose immediates are CONTIGUOUS are
supported: R, I, I-shift, S and U. The B and J formats scramble their immediate across
non-adjacent fields, and that scrambling is exactly what lives in the images this project cannot
read — so encoding a branch here would mean typing a layout from memory, which is the thing this
module exists to avoid. Control flow is owned by `P0-PROFILE.8`, which must first establish a
readable source for those two layouts. `assemble()` raises on any unsupported format rather than
guessing.
"""

from __future__ import annotations

import csv
import re
import struct
from dataclasses import dataclass
from pathlib import Path

# Formats whose immediate occupies one contiguous field. See the scope limit above.
CONTIGUOUS_OPERANDS = {
    "rd", "rs1", "rs2", "imm12", "imm20", "shamtd", "shamtw", "imm12hi", "imm12lo",
}
SCRAMBLED_OPERANDS = {"jimm20", "bimm12hi", "bimm12lo"}


class AsmError(Exception):
    """A refusal. Never a guess."""


@dataclass(frozen=True)
class Insn:
    """One instruction's encoding, as read from the pinned tables."""

    name: str
    fixed: tuple[tuple[int, int, int], ...]   # (hi, lo, value)
    operands: tuple[str, ...]
    source: str                                # which pinned file it came from


def _place(hi: int, lo: int, value: int) -> int:
    """Put `value` into bits [hi:lo], refusing anything that would not fit."""
    width = hi - lo + 1
    if value < 0 or value >= (1 << width):
        raise AsmError(f"value {value:#x} does not fit in bits [{hi}:{lo}] ({width} bits)")
    return value << lo


def load_arg_lut(path: Path) -> dict[str, tuple[int, int]]:
    """Operand field positions, from riscv-opcodes' own arg_lut.csv."""
    lut: dict[str, tuple[int, int]] = {}
    for row in csv.reader(path.read_text().splitlines()):
        if len(row) != 3:
            continue
        lut[row[0].strip().strip('"')] = (int(row[1]), int(row[2]))
    if not lut:
        raise AsmError(f"{path} yielded no operand positions — the table format changed")
    return lut


def load_encodings(paths: list[Path]) -> dict[str, Insn]:
    """Instruction encodings, from riscv-opcodes' extension files.

    A line is `<name> <operand|hi..lo=value>...`. Pseudo-ops and imports are skipped: this
    assembler encodes real instructions only, so a pseudo-instruction must be written out.
    """
    fixed_re = re.compile(r"^(\d+)\.\.(\d+)=(\S+)$")
    single_re = re.compile(r"^(\d+)=(\S+)$")
    out: dict[str, Insn] = {}
    for path in paths:
        for raw in path.read_text().splitlines():
            line = raw.split("#", 1)[0].strip()
            if not line or line.startswith("$"):
                continue
            name, *rest = line.split()
            fixed: list[tuple[int, int, int]] = []
            operands: list[str] = []
            for tok in rest:
                m = fixed_re.match(tok)
                if m:
                    fixed.append((int(m.group(1)), int(m.group(2)), int(m.group(3), 0)))
                    continue
                m = single_re.match(tok)
                if m:
                    bit = int(m.group(1))
                    fixed.append((bit, bit, int(m.group(2), 0)))
                    continue
                operands.append(tok)
            out[name] = Insn(name, tuple(fixed), tuple(operands), path.name)
    if not out:
        raise AsmError("no instruction encodings were parsed — the table format changed")
    return out


class Assembler:
    """Encodes one instruction at a time. Refuses whatever it cannot derive."""

    def __init__(self, opcodes_dir: Path) -> None:
        self.arg_lut = load_arg_lut(opcodes_dir / "arg_lut.csv")
        self.insns = load_encodings([opcodes_dir / "rv_i", opcodes_dir / "rv64_i"])

    # -- operand parsing ---------------------------------------------------------------
    @staticmethod
    def _reg(tok: str) -> int:
        tok = tok.strip()
        if not re.fullmatch(r"x(\d|[12]\d|3[01])", tok):
            raise AsmError(f"{tok!r} is not an architectural register name (x0..x31). "
                           f"ABI names are a software convention, not architecture, and this "
                           f"assembler deliberately does not accept them.")
        return int(tok[1:])

    @staticmethod
    def _imm(tok: str) -> int:
        return int(tok, 0)

    def encode(self, mnemonic: str, args: list[str]) -> int:
        name = mnemonic.lower()
        if name not in self.insns:
            raise AsmError(f"{name!r} is not in the pinned encoding tables "
                           f"(rv_i, rv64_i) — this assembler carries no opcodes of its own")
        insn = self.insns[name]
        for op in insn.operands:
            if op in SCRAMBLED_OPERANDS:
                raise AsmError(
                    f"{name!r} uses the {op!r} field, whose immediate is scrambled across "
                    f"non-adjacent bits. That layout lives only in the specification's FIGURES, "
                    f"which are images this project cannot read — encoding it would mean typing "
                    f"a bit layout from memory. Owner: P0-PROFILE.8.")
            if op not in CONTIGUOUS_OPERANDS:
                raise AsmError(f"{name!r} uses operand field {op!r}, which this assembler "
                               f"does not support")

        word = 0
        for hi, lo, val in insn.fixed:
            word |= _place(hi, lo, val)

        # S-type splits ONE immediate across two fields; every other supported format is 1:1.
        if "imm12hi" in insn.operands and "imm12lo" in insn.operands:
            if len(args) != 3:
                raise AsmError(f"{name} expects 3 operands (rs2, imm, rs1), got {len(args)}")
            rs2, imm, rs1 = self._reg(args[0]), self._imm(args[1]), self._reg(args[2])
            if not -2048 <= imm <= 2047:
                raise AsmError(f"{name}: store offset {imm} is outside the signed 12-bit range")
            u = imm & 0xFFF
            word |= _place(*self.arg_lut["rs1"], rs1)
            word |= _place(*self.arg_lut["rs2"], rs2)
            word |= _place(*self.arg_lut["imm12hi"], (u >> 5) & 0x7F)
            word |= _place(*self.arg_lut["imm12lo"], u & 0x1F)
            return word

        supplied = [op for op in insn.operands if op in CONTIGUOUS_OPERANDS]
        if len(args) != len(supplied):
            raise AsmError(f"{name} expects {len(supplied)} operand(s) {supplied}, got {len(args)}")
        for op, arg in zip(supplied, args):
            hi, lo = self.arg_lut[op]
            if op in ("rd", "rs1", "rs2"):
                word |= _place(hi, lo, self._reg(arg))
            elif op == "imm12":
                imm = self._imm(arg)
                if not -2048 <= imm <= 2047:
                    raise AsmError(f"{name}: immediate {imm} is outside the signed 12-bit range")
                word |= _place(hi, lo, imm & 0xFFF)
            elif op == "imm20":
                imm = self._imm(arg)
                if not 0 <= imm <= 0xFFFFF:
                    raise AsmError(f"{name}: U-immediate {imm:#x} is outside the 20-bit range. "
                                   f"It is the UPPER 20 bits, written unshifted.")
                word |= _place(hi, lo, imm)
            else:                                     # shamtd / shamtw
                sh = self._imm(arg)
                width = hi - lo + 1
                if not 0 <= sh < (1 << width):
                    raise AsmError(f"{name}: shift amount {sh} does not fit in {width} bits")
                word |= _place(hi, lo, sh)
        return word

    def assemble(self, lines: list[str]) -> list[tuple[int, str]]:
        """Assemble source lines into (word, original-text) pairs."""
        out = []
        for raw in lines:
            text = raw.split("#", 1)[0].strip()
            if not text:
                continue
            mnemonic, _, rest = text.partition(" ")
            args = [a.strip() for a in rest.split(",") if a.strip()]
            out.append((self.encode(mnemonic, args), text))
        return out


# ---------------------------------------------------------------------------------------
# ELF64 little-endian RISC-V executable, one PT_LOAD segment. Field values are from the
# ELF-64 specification; each is named so the file can be checked field by field.
# ---------------------------------------------------------------------------------------
EM_RISCV = 243
ET_EXEC = 2
PT_LOAD = 1
PF_X, PF_W, PF_R = 1, 2, 4
SHT_NULL, SHT_PROGBITS, SHT_STRTAB = 0, 1, 3
SHF_ALLOC, SHF_EXECINSTR, SHF_WRITE = 0x2, 0x4, 0x1
EHDR_SIZE, PHDR_SIZE, SHDR_SIZE = 64, 56, 64


def write_elf64(path: Path, entry: int, payload: bytes) -> None:
    """Write a single-segment RV64 executable loading `payload` at `entry`.

    ⛔ A SECTION HEADER TABLE IS EMITTED EVEN THOUGH EXECUTION DOES NOT NEED ONE. A first cut
    wrote program headers only — which the Sail model loaded and ran without complaint, and which
    Spike refused outright:

        Assertion failed: (from_le(eh->e_shstrndx) < from_le(eh->e_shnum)), elfloader.cc:116

    With no sections, `e_shnum` and `e_shstrndx` are both 0 and `0 < 0` is false. The two
    reference models simply disagree about how strict an ELF loader should be. That is a HARNESS
    difference, not a semantic one, and the right response is to emit the conformant artifact
    rather than to carry a per-model variant — an input that only one comparator accepts is not a
    matched experiment.
    """
    if entry % 4:
        raise AsmError(f"entry {entry:#x} is not 4-byte aligned; IALIGN=32 for this profile")

    shstrtab = b"\0.text\0.shstrtab\0"
    name_text, name_shstr = 1, 7
    assert shstrtab[name_text:name_text + 5] == b".text"
    assert shstrtab[name_shstr:name_shstr + 9] == b".shstrtab"

    phoff = EHDR_SIZE
    text_off = phoff + PHDR_SIZE
    shstr_off = text_off + len(payload)
    shoff = shstr_off + len(shstrtab)

    ehdr = struct.pack(
        "<4sBBBBB7sHHIQQQIHHHHHH",
        b"\x7fELF", 2, 1, 1, 0, 0, b"\0" * 7,   # class 64, LSB data, version 1, SysV
        ET_EXEC, EM_RISCV, 1,
        entry, phoff, shoff, 0,
        EHDR_SIZE, PHDR_SIZE, 1, SHDR_SIZE, 3, 2,
    )
    phdr = struct.pack(
        "<IIQQQQQQ",
        PT_LOAD, PF_R | PF_W | PF_X, text_off, entry, entry,
        len(payload), len(payload), 0x1000,
    )

    def shdr(name, stype, flags, addr, off, size, align):
        return struct.pack("<IIQQQQIIQQ", name, stype, flags, addr, off, size, 0, 0, align, 0)

    sections = (
        shdr(0, SHT_NULL, 0, 0, 0, 0, 0)
        + shdr(name_text, SHT_PROGBITS, SHF_ALLOC | SHF_EXECINSTR | SHF_WRITE,
               entry, text_off, len(payload), 4)
        + shdr(name_shstr, SHT_STRTAB, 0, 0, shstr_off, len(shstrtab), 1)
    )
    assert len(ehdr) == EHDR_SIZE and len(phdr) == PHDR_SIZE and len(sections) == 3 * SHDR_SIZE
    path.write_bytes(ehdr + phdr + payload + shstrtab + sections)
