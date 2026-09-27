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

⛔ THE B AND J SCRAMBLE IS DERIVED, NOT TYPED. Those two formats spread their immediate across
non-adjacent fields, and that layout is one of the things the pinned specification renders only as
an image. It is NOT typed here: `riscv-opcodes`'s `src/riscv_opcodes/constants.py` states it in
machine-readable form —

    "imm20":    "imm[31:12]"
    "bimm12hi": "imm[12|10:5]"        "bimm12lo": "imm[4:1|11]"
    "jimm20":   "imm[20|10:1|11|19:12]"

— and this module parses those descriptors. The derivation is SELF-VALIDATING: the bits a
descriptor accounts for must total exactly the width of the field it fills (7, 5, 20, 20), and
`load_immediate_layout()` refuses the table if any of them disagrees. A layout this module cannot
reconcile is a layout it will not use.

⚠️ Every immediate here is in BYTES and the low bit is not encoded: the specification states that
B- and J-immediates encode "signed offsets in multiples of 2 bytes". An odd offset is refused
rather than silently truncated.
"""

from __future__ import annotations

import csv
import re
import struct
from dataclasses import dataclass
from pathlib import Path

# Formats whose immediate occupies one contiguous field.
CONTIGUOUS_OPERANDS = {
    "rd", "rs1", "rs2", "imm12", "imm20", "shamtd", "shamtw", "imm12hi", "imm12lo",
}
# Fields whose immediate is spread across non-adjacent bits; the layout is read from the pinned
# descriptor table rather than written down here.
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


def load_immediate_layout(path: Path, arg_lut: dict[str, tuple[int, int]]) -> dict[str, list[tuple[int, int]]]:
    """The bit layout of each scrambled immediate field, from riscv-opcodes' own table.

    Returns, per field, the immediate bit ranges it carries in MSB-to-LSB order — so
    `bimm12hi` -> [(12, 12), (10, 5)] means its top bit holds imm[12] and the rest holds
    imm[10:5].

    ⛔ REFUSES a layout whose accounted bits do not total the field's width. That check is what
    makes parsing a foreign table safe: a descriptor this module misreads almost certainly
    produces the wrong total, and a silently wrong immediate is an instruction that assembles and
    jumps to the wrong address.
    """
    text = path.read_text()
    body = re.search(r"\{(.*?)\n\}", text[text.index('"imm20"') - 200:], re.S)
    if not body:
        raise AsmError(f"{path}: no immediate descriptor table found — the table format changed")
    raw = dict(re.findall(r'"([a-z0-9_]+)":\s*"([^"]+)"', body.group(1)))

    out: dict[str, list[tuple[int, int]]] = {}
    for field in sorted(SCRAMBLED_OPERANDS):
        if field not in raw:
            raise AsmError(f"{path}: no descriptor for {field!r}")
        # the table is LaTeX-decorated in the source: `$\vert$` stands for the separator
        inner = re.fullmatch(r"imm\[(.*)\]", re.sub(r"\$\\+vert\$", "|", raw[field]))
        if not inner:
            raise AsmError(f"{path}: {field!r} descriptor {raw[field]!r} is not an imm[...] form")
        parts: list[tuple[int, int]] = []
        for piece in inner.group(1).split("|"):
            hi, lo = (int(x) for x in piece.split(":")) if ":" in piece else (int(piece),) * 2
            parts.append((hi, lo))
        accounted = sum(hi - lo + 1 for hi, lo in parts)
        fhi, flo = arg_lut[field]
        width = fhi - flo + 1
        if accounted != width:
            raise AsmError(
                f"{path}: {field!r} descriptor {raw[field]!r} accounts for {accounted} bit(s) but "
                f"the field is {width} wide. This module will not use a layout it cannot "
                f"reconcile — a silently wrong immediate is a jump to the wrong address.")
        out[field] = parts
    return out


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


def resolve_composition(enc, path: Path):
    """Resolve a unit's `compose` form into one synthetic `(fragment …)` form.

    ⭐ A unit COMPOSES fragments; it never carries a copy of an instruction. ONE RESOLVER owns
    the name → fragment-file resolution (missing fragment, unmet `requires` — both refused by
    name), consumed by the assembler and by the composition checker alike. A second
    hand-written resolver is how a silent regression happens: `MODEL-COMPOSE.2` moved the
    instructions into fragments, and the disjointness checker — reading compositions its own
    way — quietly lost the ability to read a unit at all (measured, `MODEL-COMPOSE.4`).
    """
    import sexp as _sexp
    comp = _sexp.children(enc, "compose")
    if not comp:
        return enc
    root = path.parent.parent.parent / str(_sexp.field(enc, "fragment-root", str(path)))
    names = [str(_sexp.field(comp[0], "base", str(path)))]
    # repeat fields are 0-or-more: a compose with no (extensions) marker composes the base
    # alone — the corpus writes the bare marker, but the grammar does not require it
    ext = _sexp.children(comp[0], "extensions")
    names += [str(x) for x in (ext[0][1:] if ext else [])]
    merged = ["fragment"]
    declared: set[str] = set()
    for name in names:
        frag_path = root / (name + ".sexp")
        if not frag_path.is_file():
            raise AsmError(f"{path}: composes {name!r}, but {frag_path} does not exist")
        frag = _sexp.read_file(frag_path)[0]
        declared.add(str(_sexp.field(frag, "id", str(frag_path))))
        # 0-or-more like extensions: a fragment with no (requires) marker depends on nothing
        reqs = _sexp.children(frag, "requires")
        for req in (reqs[0][1:] if reqs else []):
            if str(req) not in declared:
                raise AsmError(
                    f"{path}: fragment {name!r} requires {str(req)!r}, which this composition "
                    f"does not provide before it. A fragment with an unmet dependency composes "
                    f"by luck, not by construction.")
        merged += [c for c in frag if isinstance(c, list)
                   and c and c[0] in ("field", "scatter", "insn")]
    return merged


def load_canonical_encoding(path: Path) -> tuple[dict, dict, dict]:
    """Read `encoding.sexp` — the encodings the REPOSITORY owns.

    ⛔ THIS IS THE PATH THAT MATTERS. The assembler used to read an untracked, network-acquired
    directory, so a fresh clone could not build a model at all. The canonical definition is
    tracked, so the model's encodings travel with the repository and a gate re-derives them
    against the pinned upstream when that upstream is present.
    """
    import sexp as _sexp
    forms = _sexp.read_file(path)
    if len(forms) != 1 or _sexp.head(forms[0], str(path)) != "encoding":
        raise AsmError(f"{path}: expected exactly one (encoding …) form")
    enc = forms[0]

    # A unit composes fragments; it never carries a copy of an instruction. The resolver is
    # shared with the composition checker — see resolve_composition for why there is one.
    enc = resolve_composition(enc, path)

    arg_lut: dict[str, tuple[int, int]] = {}
    for f in _sexp.children(enc, "field"):
        arg_lut[str(_sexp.field(f, "name"))] = (int(_sexp.field(f, "hi")),
                                                int(_sexp.field(f, "lo")))
    layout: dict[str, list[tuple[int, int]]] = {}
    for sc in _sexp.children(enc, "scatter"):
        name = str(_sexp.field(sc, "name"))
        hi, lo = int(_sexp.field(sc, "hi")), int(_sexp.field(sc, "lo"))
        arg_lut[name] = (hi, lo)
        pieces = [(int(a), int(b)) for a, b in _sexp.children(sc, "pieces")[0][1:]]
        accounted = sum(a - b + 1 for a, b in pieces)
        if accounted != hi - lo + 1:
            raise AsmError(
                f"{path}: scatter {name!r} accounts for {accounted} bit(s) but the field is "
                f"{hi - lo + 1} wide — a layout this module cannot reconcile is one it will not "
                f"use, because a silently wrong immediate is a jump to the wrong address")
        layout[name] = pieces

    insns: dict[str, Insn] = {}
    for i in _sexp.children(enc, "insn"):
        name = str(_sexp.field(i, "name"))
        fixed = tuple((int(a), int(b), int(c)) for a, b, c in _sexp.children(i, "fixed")[0][1:])
        ops = tuple(str(o) for o in _sexp.children(i, "operands")[0][1:])
        insns[name] = Insn(name, fixed, ops, str(_sexp.field(i, "from")))
    if not insns:
        raise AsmError(f"{path}: no instructions — an empty encoding is not a valid one")
    return arg_lut, insns, layout


class Assembler:
    """Encodes one instruction at a time. Refuses whatever it cannot derive."""

    def __init__(self, source: Path) -> None:
        """`source` is either a profile's `encoding.sexp` (the canonical definition, preferred)
        or the pinned upstream table directory (used only by `gen_encoding.py` to build it)."""
        if source.is_file():
            self.arg_lut, self.insns, self.imm_layout = load_canonical_encoding(source)
            return
        self.arg_lut = load_arg_lut(source / "arg_lut.csv")
        self.insns = load_encodings([source / "rv_i", source / "rv64_i"])
        self.imm_layout = load_immediate_layout(source / "constants.py", self.arg_lut)

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
            if op not in CONTIGUOUS_OPERANDS and op not in SCRAMBLED_OPERANDS:
                raise AsmError(f"{name!r} uses operand field {op!r}, which this assembler "
                               f"does not support")

        word = 0
        for hi, lo, val in insn.fixed:
            word |= _place(hi, lo, val)

        # ---- scrambled immediates: B-type and J-type ---------------------------------------
        scrambled = [op for op in insn.operands if op in SCRAMBLED_OPERANDS]
        if scrambled:
            return self._encode_scrambled(name, insn, args, word, scrambled)

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

    def _place_scrambled(self, field: str, imm: int) -> int:
        """Scatter `imm`'s bits into `field` per the pinned descriptor, MSB piece first."""
        hi, lo = self.arg_lut[field]
        value, pos = 0, hi - lo + 1
        for bhi, blo in self.imm_layout[field]:
            n = bhi - blo + 1
            pos -= n
            value |= ((imm >> blo) & ((1 << n) - 1)) << pos
        return _place(hi, lo, value)

    def _encode_scrambled(self, name, insn, args, word, scrambled) -> int:
        """B-type (`beq rs1, rs2, off`) and J-type (`jal rd, off`). Offsets are BYTES."""
        if "jimm20" in scrambled:                                   # J-type: rd, offset
            if len(args) != 2:
                raise AsmError(f"{name} expects 2 operands (rd, offset), got {len(args)}")
            word |= _place(*self.arg_lut["rd"], self._reg(args[0]))
            imm, bits, field = self._imm(args[1]), 21, "jimm20"
        else:                                                       # B-type: rs1, rs2, offset
            if len(args) != 3:
                raise AsmError(f"{name} expects 3 operands (rs1, rs2, offset), got {len(args)}")
            word |= _place(*self.arg_lut["rs1"], self._reg(args[0]))
            word |= _place(*self.arg_lut["rs2"], self._reg(args[1]))
            imm, bits, field = self._imm(args[2]), 13, None

        # The specification: B- and J-immediates encode "signed offsets in multiples of 2 bytes".
        # Bit 0 is therefore not encoded at all, and an odd offset is refused rather than
        # silently truncated into a jump somewhere else.
        if imm % 2:
            raise AsmError(f"{name}: offset {imm} is odd; B- and J-immediates encode signed "
                           f"offsets in MULTIPLES OF 2 BYTES, so bit 0 is not encoded")
        lim = 1 << (bits - 1)
        if not -lim <= imm < lim:
            raise AsmError(f"{name}: offset {imm} is outside the signed {bits}-bit range "
                           f"[{-lim}, {lim - 1}]")
        u = imm & ((1 << bits) - 1)
        if field:
            word |= self._place_scrambled(field, u)
        else:
            word |= self._place_scrambled("bimm12hi", u)
            word |= self._place_scrambled("bimm12lo", u)
        return word

    def assemble(self, lines: list[str], base: int = 0) -> list[tuple[int, str]]:
        """Assemble source lines into (word, original-text) pairs.

        Two passes, because a branch may target a label defined later. A bare name where an
        offset is expected is resolved to `target - pc`, which is what the specification means by
        "added to the address of the branch instruction".
        """
        stmts: list[tuple[int, str, str, list[str]]] = []   # (pc, text, mnemonic, args)
        labels: dict[str, int] = {}
        pc = base
        for raw in lines:
            text = raw.split("#", 1)[0].strip()
            if not text:
                continue
            while text.endswith(":") or ":" in text.split()[0]:
                name, _, text = text.partition(":")
                name = name.strip()
                if name in labels:
                    raise AsmError(f"label {name!r} is defined twice")
                labels[name] = pc
                text = text.strip()
                if not text:
                    break
            if not text:
                continue
            mnemonic, _, rest = text.partition(" ")
            args = [a.strip() for a in rest.split(",") if a.strip()]
            stmts.append((pc, text, mnemonic, args))
            pc += 4

        out = []
        for at, text, mnemonic, args in stmts:
            resolved = []
            for a in args:
                if re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", a) and not re.fullmatch(r"x\d+", a):
                    if a not in labels:
                        raise AsmError(f"{text!r}: label {a!r} is never defined")
                    resolved.append(str(labels[a] - at))
                else:
                    resolved.append(a)
            out.append((self.encode(mnemonic, resolved), text))
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
