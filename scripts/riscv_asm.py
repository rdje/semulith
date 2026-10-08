#!/usr/bin/env python3
"""A RISC-V assembler and ELF64 writer, for independently encoded guest programs.

WHY THIS EXISTS, and why it does not simply call a cross-compiler.
`docs/EVIDENCE_AND_GATES.md` and rule `EVD-05` require a guest program's expected observations
to be derived from the SPECIFICATION, not from any model's output. A toolchain would also be a
fine encoder, but it would be one more artifact whose provenance has to be established, and on
this host it would have to be installed off the repository volume. This assembler reads its
encodings from pinned tables and produces a file whose every byte is accounted for.

⛔ WHERE THE ENCODINGS COME FROM, and why it is not this file.
The pinned specification artifacts do NOT contain instruction encodings. Measured over all six
of them (three HTML pages and their text renderings): `grep -cE '[01]{7}'` -> 0, 0, 0, 0, 0, 0.
The format diagrams are IMAGES (31 in the RV32I chapter alone), so the bit layouts are simply
not in the bytes this project pinned. The SEMANTICS are all there in prose — which is the half
that matters for expected values — but the encodings had to come from somewhere else.

They come from `riscv-opcodes` (RISC-V International, BSD-3-Clause), pinned under
`target/refs/riscv-opcodes/` and re-derived by `scripts/fetch_references.sh`:
    extensions/rv_i, extensions/rv64_i   the fixed bits and operand list per instruction
    extensions/rv_zicsr, rv_zicntr, rv_system, rv_s   Zicsr, Zicntr and the privileged
                                         system instructions (the rv64gc pin, P4-SYSTEM.2)
    extensions/rv_a, extensions/rv64_a   the A extension's 22 atomic forms (the rv64gc
                                         pin, P4-SYSTEM.4 slice a)
    extensions/rv_f, extensions/rv64_f   the F extension's 30 forms (the rv64gc pin,
                                         P4-SYSTEM.7 slice c2)
    arg_lut.csv                          the operand field positions
    csrs.csv                             the CSR name-to-address map (csr operand spellings)
This module PARSES those files. It does not carry an opcode constant of its own, so a typo here
cannot invent an instruction — it can only fail to find one.

⛔ WHICH REGISTER FILE AN OPERAND NAMES IS DERIVED, NOT TYPED (P4-SYSTEM.7 slice c3). The pinned
rows name only the FIELD (`rd rs1 rs2 rs3`); `fcvt.w.s rd, rs1` reads an f-register and writes
an x-register, and nothing in the table says so. The semantics do: a rule reads `(freg rs1)` or
`(reg rs1)`. A unit's assembler therefore reads its composed fragments' `.sem.sexp` rules and
spells an operand `f0..f31` exactly when its rule names it through `(freg …)`, `x0..x31`
otherwise — and refuses the other spelling BY NAME, so `fadd.s x1, x2, x3` is an error, never
a silently different instruction. The rounding-mode field `rm` is spelled as its 3-bit value
(0..7; the mode names live in the specification's Table 2, which this module does not carry —
a guest's directive names the mode).

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

# Formats whose immediate occupies one contiguous field. `fm`/`pred`/`succ` are FENCE's 4-bit
# fields (`P2-SCALAR.1`); the generic width-checked path range-checks them 0..15 like `shamt`.
# `csr` and `zimm5` are Zicsr's (`P4-SYSTEM.2` slice a): `csr` shares bits 31..20 with `imm12`
# and is distinguished from it BY FIELD NAME, exactly as the pinned arg_lut.csv rows do — imm12
# is signed (-2048..2047), csr is the unsigned 12-bit CSR address (0..0xFFF, or a name resolved
# through the pinned csrs.csv); `zimm5` is the unsigned 5-bit immediate of the csrr*i forms.
# `aq` and `rl` are the A extension's ordering bits (`P4-SYSTEM.4` slice a): they are whitelisted
# so the operand-field gate below knows them, but no operand ever SPELLS them — the
# `.aq`/`.rl`/`.aqrl` mnemonic suffix supplies their values (see encode()). The POSITIONS
# always come from the pinned arg_lut.csv at load time — derived, never typed.
CONTIGUOUS_OPERANDS = {
    "rd", "rs1", "rs2", "imm12", "imm20", "shamtd", "shamtw", "imm12hi", "imm12lo",
    "fm", "pred", "succ", "csr", "zimm5", "aq", "rl", "rs3", "rm",
}
# The register-valued fields: their spelling is x0..x31 or f0..f31 by the instruction's own
# semantics (load_register_files); every other field is a number.
REGISTER_FIELDS = ("rd", "rs1", "rs2", "rs3")
# Fields whose immediate is spread across non-adjacent bits; the layout is read from the pinned
# descriptor table rather than written down here.
SCRAMBLED_OPERANDS = {"jimm20", "bimm12hi", "bimm12lo"}

# The A extension's ordering suffix: a closed set, carrying the (aq, rl) field values.
# All four combinations — none included — assemble and execute identically at one hart
# (every aq/rl effect is defined "as viewed by other RISC-V harts"; the chapter's
# "Software should not" is a software rule, not a decode illegality — P4-SYSTEM.4's
# design brief, decision 1).
AQRL_SUFFIXES = {"aq": (1, 0), "rl": (0, 1), "aqrl": (1, 1)}


class AsmError(Exception):
    """A refusal. Never a guess."""


@dataclass(frozen=True)
class Insn:
    """One instruction's encoding, as read from the pinned tables."""

    name: str
    fixed: tuple[tuple[int, int, int], ...]   # (hi, lo, value)
    operands: tuple[str, ...]
    source: str                                # which pinned file it came from
    of: str = ""                               # a pseudo-op's base (`rv_zicsr::csrrs`), else ""


@dataclass(frozen=True)
class AssembledUnit:
    """One emitted unit, retaining its byte length and address (including raw data)."""

    value: int
    length: int
    pc: int
    text: str


def _place(hi: int, lo: int, value: int) -> int:
    """Put `value` into bits [hi:lo], refusing anything that would not fit."""
    width = hi - lo + 1
    if value < 0 or value >= (1 << width):
        raise AsmError(f"value {value:#x} does not fit in bits [{hi}:{lo}] ({width} bits)")
    return value << lo


def load_immediate_layout(path: Path, arg_lut: dict[str, tuple[int, int]],
                          fields=None) -> dict[str, list[tuple[int, int]]]:
    """The bit layout of each scrambled immediate field, from riscv-opcodes' own table.

    Returns, per field, the immediate bit ranges it carries in MSB-to-LSB order — so
    `bimm12hi` -> [(12, 12), (10, 5)] means its top bit holds imm[12] and the rest holds
    imm[10:5].

    ⛔ REFUSES a layout whose accounted bits do not total the field's width. That check is what
    makes parsing a foreign table safe: a descriptor this module misreads almost certainly
    produces the wrong total, and a silently wrong immediate is an instruction that assembles and
    jumps to the wrong address.

    `fields` (P4-SYSTEM.12 slice a): the fields to read — the base's scrambled set by default;
    the compressed immediates' PIECE fields for the C fragment, whose descriptors name the
    immediate's kind (`uimm[…]`, `nzimm[…]`, `nzuimm[…]`) as well as its bits.
    """
    text = path.read_text()
    body = re.search(r"\{(.*?)\n\}", text[text.index('"imm20"') - 200:], re.S)
    if not body:
        raise AsmError(f"{path}: no immediate descriptor table found — the table format changed")
    raw = dict(re.findall(r'"([a-z0-9_]+)":\s*"([^"]+)"', body.group(1)))

    out: dict[str, list[tuple[int, int]]] = {}
    for field in sorted(SCRAMBLED_OPERANDS if fields is None else fields):
        if field not in raw:
            raise AsmError(f"{path}: no descriptor for {field!r}")
        # the table is LaTeX-decorated in the source: `$\vert$` stands for the separator
        inner = re.fullmatch(r"(?:nz|u|nzu)?imm\[(.*)\]", re.sub(r"\$\\+vert\$", "|", raw[field]))
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


def load_encodings(paths: list[Path], allow_empty: bool = False) -> dict[str, Insn]:
    """Instruction encodings, from riscv-opcodes' extension files.

    A line is `<name> <operand|hi..lo=value>...`. Pseudo-ops and imports are skipped: a
    pseudo-instruction of a REAL instruction is written out (the rv64i policy — `nop` is
    `addi x0, x0, 0`). The one exception is load_pseudo_ops below, for forms a profile
    selects that exist upstream ONLY as pseudo-ops. `allow_empty` is for a table that
    legitimately carries no real rows (rv_zicntr is pseudo-only); the caller must then
    prove the fragment is not empty by its pseudo rows.
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
    if not out and not allow_empty:
        raise AsmError("no instruction encodings were parsed — the table format changed")
    return out


def load_pseudo_ops(paths: list[Path]) -> dict[str, Insn]:
    """Pseudo-op rows, from riscv-opcodes' extension files — DERIVED, never typed.

    A row is `$pseudo_op <base::insn> <name> <operand|hi..lo=value>...` and is
    self-contained: every fixed bit of the spelling is on the row. Zicntr's counter reads
    (rdcycle/rdtime/rdinstret) exist upstream ONLY in this form — measured at the
    P4-SYSTEM.2 re-pin — so a profile selecting them takes them from here. A pseudo-op is
    NOT a new encoding: its fixed bits specialize its base instruction's, which is why it
    travels as a `(pseudo …)` in a fragment and never as an `(insn …)`.
    """
    fixed_re = re.compile(r"^(\d+)\.\.(\d+)=(\S+)$")
    single_re = re.compile(r"^(\d+)=(\S+)$")
    out: dict[str, Insn] = {}
    for path in paths:
        for raw in path.read_text().splitlines():
            line = raw.split("#", 1)[0].strip()
            if not line.startswith("$pseudo_op"):
                continue
            _, base, name, *rest = line.split()
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
            out[name] = Insn(name, tuple(fixed), tuple(operands), path.name, of=base)
    return out


def load_csr_names(path: Path) -> dict[str, int]:
    """The CSR name-to-address map, from riscv-opcodes' csrs.csv (`0xC00, "cycle"` rows).

    Used to resolve a csr OPERAND spelled as a name (`csrrw x1, cycle, x2`); a numeric
    address never consults it. An unknown name or an absent table is a refusal, never a
    guess at an address.
    """
    lut: dict[str, int] = {}
    for row in csv.reader(path.read_text().splitlines()):
        if len(row) != 2:
            continue
        addr, name = row[0].strip(), row[1].strip().strip('"')
        if not addr.startswith("0x"):
            continue
        lut[name] = int(addr, 16)
    if not lut:
        raise AsmError(f"{path} yielded no CSR names — the table format changed")
    return lut


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
    # alone — the corpus writes the bare marker, but the grammar does not require it. Every
    # (extensions) FORM contributes: the schema's (repeat yes) is one string per form, so a
    # multi-extension composition carries several — reading only ext[0] silently dropped
    # every extension after the first form (measured, P4-SYSTEM.2 slice a: the first
    # three-extension composition exposed it).
    ext = _sexp.children(comp[0], "extensions")
    for e in ext:
        names += [str(x) for x in e[1:]]
    merged = ["fragment"]
    declared: set[str] = set()
    for name in names:
        frag_path = root / (name + ".sexp")
        if not frag_path.is_file():
            raise AsmError(f"{path}: composes {name!r}, but {frag_path} does not exist")
        frag = _sexp.read_file(frag_path)[0]
        declared.add(str(_sexp.field(frag, "id", str(frag_path))))
        # 0-or-more like extensions: a fragment with no (requires) marker depends on nothing;
        # with several markers (the schema's repeat) every one must be provided
        reqs = _sexp.children(frag, "requires")
        for r in reqs:
            for req in r[1:]:
                if str(req) not in declared:
                    raise AsmError(
                        f"{path}: fragment {name!r} requires {str(req)!r}, which this "
                        f"composition does not provide before it. A fragment with an unmet "
                        f"dependency composes by luck, not by construction.")
        merged += [c for c in frag if isinstance(c, list)
                   and c and c[0] in ("field", "scatter", "insn", "pseudo", "specializes")]
    return merged


def _semantic_documents(path: Path):
    """The unit's composed semantics documents, in declaration order."""
    import sexp as _sexp
    forms = _sexp.read_file(path)
    enc = forms[0] if forms else []
    comp = _sexp.children(enc, "compose")
    if not comp:
        return []
    root = path.parent.parent.parent / str(_sexp.field(enc, "fragment-root", str(path)))
    names = [str(_sexp.field(comp[0], "base", str(path)))]
    for e in _sexp.children(comp[0], "extensions"):
        names += [str(x) for x in e[1:]]
    documents = []
    for name in names:
        sem_path = root / (name + ".sem.sexp")
        if sem_path.is_file():
            documents.append((sem_path, _sexp.read_file(sem_path)[0]))
    return documents


def load_register_files(path: Path) -> dict[str, set[str]]:
    """Per instruction, the operand fields its semantics read or write through `(freg …)` —
    the operands this assembler spells f0..f31 (P4-SYSTEM.7 slice c3). Derived from the
    unit's composed fragments' `.sem.sexp` rules, in composition order, a later rule (a
    declared refinement) replacing an earlier one. A fragment without a semantics document
    contributes nothing (every operand stays an x-register — the rv64i-era default the
    tables themselves imply). One field in BOTH files within one rule is refused: no spelling
    could be right (check_semantics.check_fp refuses the same rule upstream)."""
    import sexp as _sexp
    files: dict[str, set[str]] = {}
    expansions = []
    for sem_path, document in _semantic_documents(path):
        expansions.extend(_sexp.children(document, "expand"))
        for rule in _sexp.children(document, "sem"):
            insn = str(_sexp.field(rule, "insn", str(sem_path)))
            reg_ops: set[str] = set()
            freg_ops: set[str] = set()

            def walk(f) -> None:
                if not isinstance(f, list) or not f:
                    return
                head = str(f[0])
                if head in ("reg", "freg") and len(f) == 2:
                    (freg_ops if head == "freg" else reg_ops).add(str(f[1]))
                for a in f[1:]:
                    walk(a)

            for effect in _sexp.children(rule, "effect"):
                walk(effect)
            both = reg_ops & freg_ops
            if both:
                raise AsmError(f"{sem_path.name} [{insn}]: operand(s) {sorted(both)} are read "
                               f"as BOTH (reg …) and (freg …) — no spelling could be right")
            files[insn] = freg_ops
    # A compressed register field names the file its mapped BASE operand belongs to.
    # Derive that relationship from the declarations, rather than a C-specific FP list.
    for rule in expansions:
        insn = str(_sexp.field(rule, "insn"))
        targets = _sexp.children(rule, "to")
        base = targets[0][1] if targets else None
        if base is not None and str(base) not in files:
            raise AsmError(f"{insn}: expansion base {base!r} has no register-file declaration")
        floating = files.get(str(base), set())
        fields = set()
        for binding in _sexp.children(rule, "operand"):
            if str(_sexp.field(binding, "name")) not in floating:
                continue
            def raw_fields(expr):
                if isinstance(expr, list) and expr:
                    if expr[0] == "field":
                        fields.add(str(expr[1]))
                    for arg in expr[1:]:
                        raw_fields(arg)
            raw_fields(_sexp.children(binding, "value")[0][1])
        files[insn] = fields
    return files


def load_canonical_encoding(path: Path, with_pseudos: bool = False):
    """Read `encoding.sexp` — the encodings the REPOSITORY owns.

    ⛔ THIS IS THE PATH THAT MATTERS. The assembler used to read an untracked, network-acquired
    directory, so a fresh clone could not build a model at all. The canonical definition is
    tracked, so the model's encodings travel with the repository and a gate re-derives them
    against the pinned upstream when that upstream is present.

    With `with_pseudos` the tuple gains the fragment's `(pseudo …)` forms — assembler
    spellings that add nothing to the encoding space (see schema/fragment.sexp). Callers
    that lower the encoding SPACE (gen_definition) leave it off and see no change.
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
    if not with_pseudos:
        return arg_lut, insns, layout
    pseudos: dict[str, Insn] = {}
    for p in _sexp.children(enc, "pseudo"):
        name = str(_sexp.field(p, "name"))
        fixed = tuple((int(a), int(b), int(c)) for a, b, c in _sexp.children(p, "fixed")[0][1:])
        ops = tuple(str(o) for o in _sexp.children(p, "operands")[0][1:])
        pseudos[name] = Insn(name, fixed, ops, str(_sexp.field(p, "from")),
                             of=str(_sexp.field(p, "of")))
    return arg_lut, insns, layout, pseudos


class Assembler:
    """Encodes one instruction at a time. Refuses whatever it cannot derive."""

    def __init__(self, source: Path) -> None:
        """`source` is either a profile's `encoding.sexp` (the canonical definition, preferred)
        or the pinned upstream table directory (used only by table-derivation tooling).

        IALIGN is profile DATA, never assumed: constructed from a unit's encoding.sexp the
        value comes from the sibling profile.sexp's `(ialign …)` field through the dossier
        mapping owner; a unit that declares nothing gets 32, the only architectural value an
        ILEN=32 base without C can have. The table-directory route is the rv64i-era tables,
        IALIGN=32 by construction.

        CSR name resolution is likewise the unit's own data where the unit OWNS it
        (P4-SYSTEM.2 slice h, the csr-name↔address ownership migration): a sibling
        state.sexp carrying csr elements is the owner, and the assembler resolves names
        through it; a unit without CSR state (rv64i-lab-v0) and the table-directory route
        keep resolving through the pinned csrs.csv — the upstream derivation source the
        state document's own addresses were checked against (the 33/33 probe)."""
        self.ialign = 32
        self.fregs: dict[str, set[str]] = {}
        self.c_reserved = {}
        if source.is_file():
            self.arg_lut, self.insns, self.imm_layout, self.pseudos = \
                load_canonical_encoding(source, with_pseudos=True)
            self.fregs = load_register_files(source)
            import sexp as X
            for _, document in _semantic_documents(source):
                for rule in X.children(document, "expand"):
                    predicates = X.children(rule, "reserved")
                    if predicates:
                        self.c_reserved[str(X.field(rule, "insn"))] = predicates[0][1]
            prof = source.parent / "profile.sexp"
            if prof.is_file():
                import dossier_sexp as D
                declared = D.load_profile(prof).get("profile", {}).get("ialign")
                if declared is not None:
                    self.ialign = int(declared)
            self._csrs: dict[str, int] | None = None
            self._csr_source = "the pinned csrs.csv"
            state = source.parent / "state.sexp"
            if state.is_file():
                import dossier_sexp as D
                csrs = {str(c["id"]): int(str(c["address"]), 0)
                        for c in D.load_state(state).get("csr", [])}
                if csrs:
                    self._csrs = csrs
                    self._csr_source = f"{state.parent.name}'s state.sexp"
            return
        self.arg_lut = load_arg_lut(source / "arg_lut.csv")
        self.insns = load_encodings([source / "rv_i", source / "rv64_i"])
        self.imm_layout = load_immediate_layout(source / "constants.py", self.arg_lut)
        self.pseudos = {}
        self._csrs = None
        self._csr_source = "the pinned csrs.csv"
        self._csr_table = source / "csrs.csv"

    def _csr(self, tok: str) -> int:
        """A csr operand: a numeric address, or a name resolved through the unit's owner
        (a CSR-carrying state.sexp) or the pinned csrs.csv — never invented."""
        try:
            addr = int(tok, 0)
        except ValueError:
            if self._csrs is None:
                table = getattr(self, "_csr_table", None) or \
                    Path(__file__).resolve().parent.parent / "target/refs/riscv-opcodes/csrs.csv"
                if not table.is_file():
                    raise AsmError(
                        f"csr operand {tok!r} is a name, but the pinned csrs.csv it resolves "
                        f"through is not present at {table} — run scripts/fetch_references.sh")
                self._csrs = load_csr_names(table)
            if tok not in self._csrs:
                raise AsmError(f"csr operand {tok!r} is not in {self._csr_source} — this "
                               f"assembler carries no CSR addresses of its own")
            addr = self._csrs[tok]
        if not 0 <= addr <= 0xFFF:
            raise AsmError(f"CSR address {addr:#x} is outside the unsigned 12-bit range. The "
                           f"csr field shares bits 31..20 with imm12 but is UNSIGNED — the "
                           f"pinned arg_lut.csv rows distinguish them by field name.")
        return addr

    # -- operand parsing ---------------------------------------------------------------
    @staticmethod
    def _reg(tok: str) -> int:
        tok = tok.strip()
        if not re.fullmatch(r"x(\d|[12]\d|3[01])", tok):
            raise AsmError(f"{tok!r} is not an architectural register name (x0..x31). "
                           f"ABI names are a software convention, not architecture, and this "
                           f"assembler deliberately does not accept them.")
        return int(tok[1:])

    def _reg_of(self, insn: str, field: str, tok: str) -> int:
        """A register operand, spelled in the file the instruction's semantics name it
        through: f0..f31 for a `(freg field)` operand, x0..x31 otherwise — the other
        spelling refused BY NAME (P4-SYSTEM.7 slice c3)."""
        if field in self.fregs.get(insn, set()):
            t = tok.strip()
            if not re.fullmatch(r"f(\d|[12]\d|3[01])", t):
                raise AsmError(f"{insn}: operand {field} is an f-register (its semantics read "
                               f"(freg {field})) — spell it f0..f31, got {t!r}")
            return int(t[1:])
        if re.fullmatch(r"f\d+", tok.strip()):
            raise AsmError(f"{insn}: operand {field} is an x-register (its semantics read "
                           f"(reg {field})) — spell it x0..x31, got {tok.strip()!r}")
        return self._reg(tok)

    @staticmethod
    def _imm(tok: str) -> int:
        try:
            return int(tok, 0)
        except ValueError:
            raise AsmError(f"immediate {tok!r} is not a numeric literal") from None

    @staticmethod
    def _paren_reg(name: str, tok: str) -> int:
        """The A forms' parenthesized address operand, `(rs1)` — nothing else is spelled."""
        m = re.fullmatch(r"\(\s*([^()]+?)\s*\)", tok)
        if not m:
            raise AsmError(f"{name}: the address operand is spelled (rs1), got {tok!r} — "
                           f"the A forms take no offset, so a bare register or an "
                           f"offset(rs1) shape is not this instruction")
        return Assembler._reg(m.group(1))

    def encode(self, mnemonic: str, args: list[str]) -> int:
        name = mnemonic.lower()
        suffix = None
        insn = self.insns.get(name) or self.pseudos.get(name)
        if insn is None and "." in name:
            # The A ordering suffix rides the MNEMONIC (`lr.w.aq`), while the pinned
            # tables list the base names — the mnemonic token is looked up whole, so the
            # suffix is split here and re-applied as the aq/rl FIELD VALUES, never as a
            # table name. A suffix on a name the tables do not carry, a suffix outside
            # the closed .aq/.rl/.aqrl set, and a suffix on a non-atomic form are all
            # refusals BY NAME, never guesses (P4-SYSTEM.4 slice a).
            base, _, suffix = name.rpartition(".")
            insn = self.insns.get(base)
            if insn is not None:
                if suffix not in AQRL_SUFFIXES:
                    raise AsmError(
                        f"{name!r}: ordering suffix {suffix!r} is not one of .aq/.rl/.aqrl "
                        f"— the only suffixes the A extension defines")
                if not {"aq", "rl"} <= set(insn.operands):
                    raise AsmError(
                        f"{name!r}: an .aq/.rl ordering suffix belongs to an A form; "
                        f"{base!r} has no aq/rl field in the pinned tables")
                name = base
        if insn is None:
            raise AsmError(f"{mnemonic.lower()!r} is not in the canonical definition's "
                           f"encoding space — this assembler carries no opcodes of its own")
        if name.startswith("c."):
            return self._encode_compressed(name, insn, args)
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
            rs2, imm = self._reg_of(name, "rs2", args[0]), self._imm(args[1])
            rs1 = self._reg_of(name, "rs1", args[2])
            if not -2048 <= imm <= 2047:
                raise AsmError(f"{name}: store offset {imm} is outside the signed 12-bit range")
            u = imm & 0xFFF
            word |= _place(*self.arg_lut["rs1"], rs1)
            word |= _place(*self.arg_lut["rs2"], rs2)
            word |= _place(*self.arg_lut["imm12hi"], (u >> 5) & 0x7F)
            word |= _place(*self.arg_lut["imm12lo"], u & 0x1F)
            return word

        # Zicsr's three-register forms spell `name rd, csr, rs1` while the pinned table lists
        # the fields `rd rs1 csr` — the csr occupies bits 31..20, the position every other
        # format's immediate holds, and the assembly convention writes it in the immediate
        # slot. The spelling is proven, not assumed: spike-dasm (the module's documented
        # second decoder) disassembles the emitted word back to the requested spelling
        # (`DASM(c00110f3)` -> `csrrw ra, cycle, sp`, measured at P4-SYSTEM.2 slice a).
        if set(insn.operands) == {"rd", "rs1", "csr"}:
            if len(args) != 3:
                raise AsmError(f"{name} expects 3 operands (rd, csr, rs1), got {len(args)}")
            word |= _place(*self.arg_lut["rd"], self._reg(args[0]))
            word |= _place(*self.arg_lut["csr"], self._csr(args[1]))
            word |= _place(*self.arg_lut["rs1"], self._reg(args[2]))
            return word

        # The A forms: the pinned tables list the fields `rd rs1 [rs2] aq rl` with rs1 the
        # ADDRESS, and the assembly convention writes it parenthesized and LAST —
        # `lr.w rd, (rs1)` / `sc.w rd, rs2, (rs1)` / `amoadd.w rd, rs2, (rs1)`. The
        # .aq/.rl/.aqrl mnemonic suffix supplies the aq/rl field values (absent suffix:
        # both zero). Any other shape is refused by name, never guessed — the spelling is
        # proven, not assumed: spike-dasm (the module's documented second decoder)
        # disassembles the emitted words back to the requested spellings, suffixes
        # included (P4-SYSTEM.4 slice a).
        if {"aq", "rl"} <= set(insn.operands):
            regs = [op for op in insn.operands if op in ("rd", "rs1", "rs2")]
            want = len(regs)                       # 2 for lr (rd rs1), 3 for sc/amo
            spelling = "(rd, (rs1))" if want == 2 else "(rd, rs2, (rs1))"
            if len(args) != want:
                raise AsmError(f"{name} expects {want} operands {spelling}, got {len(args)}")
            word |= _place(*self.arg_lut["rd"], self._reg(args[0]))
            if want == 3:
                word |= _place(*self.arg_lut["rs2"], self._reg(args[1]))
            word |= _place(*self.arg_lut["rs1"], self._paren_reg(name, args[-1]))
            aq, rl = AQRL_SUFFIXES.get(suffix, (0, 0))
            word |= _place(*self.arg_lut["aq"], aq)
            word |= _place(*self.arg_lut["rl"], rl)
            return word

        # fence.i's ZERO-OPERAND spelling: the chapter's own standard-software rule zeroes
        # the three fields — "base implementations shall ignore these fields [funct12,
        # rs1, rd], and standard software shall zero these fields" (RVI-ZIFENCEI 2.0) —
        # so the bare mnemonic assembles with imm12/rs1/rd zeroed (the ecall/ebreak
        # zero-operand precedent). Measured at P4-SYSTEM.6 slice a: the table's operand
        # list would otherwise force the full `fence.i 0, x0, x0` spelling, which stays
        # accepted; a partial spelling (1–2 operands) refuses on arity, by name.
        if name == "fence.i" and not args:
            args = ["0", "x0", "x0"]

        supplied = [op for op in insn.operands if op in CONTIGUOUS_OPERANDS]
        if len(args) != len(supplied):
            raise AsmError(f"{name} expects {len(supplied)} operand(s) {supplied}, got {len(args)}")
        for op, arg in zip(supplied, args):
            hi, lo = self.arg_lut[op]
            if op in REGISTER_FIELDS:
                word |= _place(hi, lo, self._reg_of(name, op, arg))
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
            elif op == "csr":
                word |= _place(hi, lo, self._csr(arg))
            else:                     # shamtd / shamtw / fm / pred / succ / zimm5 / rm
                sh = self._imm(arg)
                width = hi - lo + 1
                if not 0 <= sh < (1 << width):
                    raise AsmError(f"{name}: operand field {op} value {sh} does not fit in "
                                   f"{width} bits")
                word |= _place(hi, lo, sh)
        return word

    def _encode_compressed(self, name: str, insn: Insn, args: list[str]) -> int:
        """One argument per register, one per grouped scattered immediate, field order.

        Compact registers spell their architectural x8..x15/f8..f15 indices. Signedness
        comes from the pinned immediate descriptor kind; the union of its pieces owns
        the width and low zero bits. C.LUI takes its unshifted signed six-bit value.
        Reserved/specialized encodings can always be placed explicitly with `.half`.
        """
        immediates = [field for field in insn.operands if field in self.imm_layout]
        groups = []
        for field in insn.operands:
            if field in immediates:
                if not any(isinstance(group, list) for group in groups):
                    groups.append(immediates)
            else:
                groups.append(field)
        if name == "c.nop" and not args:
            args = ["0"]
        if len(args) != len(groups):
            raise AsmError(f"{name} expects {len(groups)} operand(s) in field order {groups}, got {len(args)}")
        word = sum(_place(hi, lo, value) for hi, lo, value in insn.fixed)
        for group, arg in zip(groups, args):
            if isinstance(group, str):
                index = self._reg_of(name, group, arg)
                hi, lo = self.arg_lut[group]
                if hi - lo + 1 == 3:
                    if not 8 <= index <= 15:
                        raise AsmError(f"{name}: compact register {arg} must be x8..x15 or f8..f15")
                    index -= 8
                elif hi - lo + 1 != 5:
                    raise AsmError(f"{name}: unsupported register field {group}")
                word |= _place(hi, lo, index)
                continue
            pieces = {bit for field in group for hi, lo in self.imm_layout[field]
                      for bit in range(lo, hi + 1)}
            low, high = min(pieces), max(pieces)
            if pieces != set(range(low, high + 1)):
                raise AsmError(f"{name}: immediate pieces are not a contiguous value")
            value = self._imm(arg)
            if name == "c.lui":
                value <<= low
            signed = not all(field.startswith(("c_uimm", "c_nzuimm")) for field in group)
            limit = 1 << (high + 1 - int(signed))
            minimum = -limit if signed else 0
            if not minimum <= value < limit:
                raise AsmError(f"{name}: immediate {arg} is outside its {'signed' if signed else 'unsigned'} range")
            if value % (1 << low):
                raise AsmError(f"{name}: immediate {arg} must be a multiple of {1 << low} bytes")
            for field in group:
                word |= self._place_scrambled(field, value & ((1 << (high + 1)) - 1))
        # Do not silently assemble another member of an overlapping encoding family.
        candidates = []
        for candidate in self.insns.values():
            if not candidate.name.startswith("c."):
                continue
            mask = sum(((1 << (hi - lo + 1)) - 1) << lo for hi, lo, _ in candidate.fixed)
            fixed = sum(value << lo for hi, lo, value in candidate.fixed)
            if word & mask == fixed:
                candidates.append((mask.bit_count(), candidate.name))
        actual = sorted(candidates, key=lambda item: (-item[0], item[1]))[0][1]
        if actual != name:
            raise AsmError(f"{name}: these operands encode the specialization {actual}; use that spelling or .half")
        if name in self.c_reserved and self._reserved_value(self.c_reserved[name], word):
            raise AsmError(f"{name}: reserved operands; use .half for the explicit code point")
        return word

    def _reserved_value(self, expr, word):
        """Evaluate the declared pure reserved predicate over original encoding fields."""
        head, *args = expr
        if head == "lit":
            return int(args[0])
        if head in ("field", "imm"):
            field = str(args[0])
            hi, lo = self.arg_lut[field]
            raw = (word >> lo) & ((1 << (hi - lo + 1)) - 1)
            if field not in self.imm_layout:
                return raw
            value, cursor = 0, hi - lo + 1
            for upper, lower in self.imm_layout[field]:
                width = upper - lower + 1
                cursor -= width
                value |= ((raw >> cursor) & ((1 << width) - 1)) << lower
            return value
        if head in ("eq", "or"):
            a, b = (self._reserved_value(arg, word) for arg in args)
            return int(a == b) if head == "eq" else a | b
        raise AsmError(f"reserved predicate {head!r} is outside the assembler's pure vocabulary")

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

    def assemble_units(self, lines: list[str], base: int = 0) -> list[AssembledUnit]:
        """Assemble source lines into sized units with their original text and byte address.

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
            pc += 2 if mnemonic.lower() == ".half" or mnemonic.lower().startswith("c.") else 4

        out = []
        for at, text, mnemonic, args in stmts:
            # A bare name is a LABEL only where a label is legal — an instruction with a
            # scrambled B/J offset. Everywhere else it belongs to the operand parser (a
            # csr name resolves through the pinned csrs.csv; anything else is refused
            # there). Measured at P4-SYSTEM.2 slice a: resolving names for every operand
            # ate `csrrw x1, cycle, x2`'s csr name as an undefined label.
            insn = self.insns.get(mnemonic.lower()) or self.pseudos.get(mnemonic.lower())
            takes_label = insn is not None and any(op in SCRAMBLED_OPERANDS
                                                   for op in insn.operands)
            takes_label |= mnemonic.lower() in ("c.j", "c.beqz", "c.bnez")
            resolved = []
            for a in args:
                if (takes_label
                        and re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", a)
                        and not re.fullmatch(r"x\d+", a)):
                    if a not in labels:
                        raise AsmError(f"{text!r}: label {a!r} is never defined")
                    resolved.append(str(labels[a] - at))
                else:
                    resolved.append(a)
            if mnemonic in (".word", ".half"):
                # A raw data word (P2-SCALAR.3): the honest spelling of "this guest
                # deliberately places these exact bytes" — the reserved encodings the
                # mnemonic path's range checks exist to refuse. Numeric literals only.
                if len(resolved) != 1:
                    raise AsmError(f"{text!r}: {mnemonic} takes exactly one operand")
                try:
                    value = int(resolved[0], 0)
                except ValueError:
                    raise AsmError(
                        f"{text!r}: {mnemonic} takes a numeric literal, got {resolved[0]!r}"
                    ) from None
                length = 2 if mnemonic == ".half" else 4
                if not 0 <= value < (1 << (length * 8)):
                    raise AsmError(f"{text!r}: {mnemonic} value {value:#x} is outside {length * 8} bits")
                out.append(AssembledUnit(value, length, at, text))
                continue
            length = 2 if mnemonic.lower().startswith("c.") else 4
            out.append(AssembledUnit(self.encode(mnemonic, resolved), length, at, text))
        return out

    def assemble(self, lines: list[str], base: int = 0) -> list[tuple[int, str]]:
        """Legacy word API. Short units require assemble_units/assemble_image explicitly."""
        units = self.assemble_units(lines, base)
        if any(unit.length != 4 for unit in units):
            raise AsmError("short units require assemble_units or assemble_image; word API refuses padding")
        return [(unit.value, unit.text) for unit in units]

    def assemble_image(self, lines: list[str], base: int = 0) -> bytes:
        """The exact little-endian byte image, with no padding between units."""
        return b"".join(unit.value.to_bytes(unit.length, "little")
                        for unit in self.assemble_units(lines, base))


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


def write_elf64(path: Path, entry: int, payload: bytes, ialign: int) -> None:
    """Write a single-segment RV64 executable loading `payload` at `entry`.

    `ialign` is the profile's instruction-address alignment in BITS (rv64i: 32; rv64gc with
    C: 16, D-IALIGN-16) — profile data, derived by the caller from the unit's profile.sexp,
    never assumed here (the rv64i-era assumption this signature retired hard-coded 32).

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
    if entry % (ialign // 8):
        raise AsmError(f"entry {entry:#x} is not {ialign // 8}-byte aligned; IALIGN={ialign} "
                       f"for this profile")

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
