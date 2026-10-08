#!/usr/bin/env python3
"""gen_definition.py — generate `semulith-core`'s canonical-definition module from the
unit's encoding composition and the semantics data (P1-LAB.6; OWN-01/OWN-03).

The decode table, operand-field table, and the semantics effect trees of
`crates/semulith-core/src/definition.rs` DERIVE from the canonical definition
(`docs/ARCHITECTURE.md` §2): `profiles/rv64i-lab-v0/encoding.sexp` composing the fragment
`definitions/riscv/rv64i.sexp`, with `definitions/riscv/rv64i.sem.sexp` the semantics data
— the execution authority (`decision_interpreter-before-compiler`). The module is the
definition's lowered mirror; the pair is governed by the DEF-GEN doctrine
(`scripts/check_definition_gen.sh`): drift is `regenerate and diff`, never a hand edit.

OWN-01 has exactly one executable owner per semantic rule: the semantics DATA. This
module carries that data, lowered — there is no handwritten second copy of any rule, and
the interpreter slice (P1-LAB.8) evaluates exactly these trees.

OWN-03's generation manifest rides in the module as data: every canonical input named by
repository-relative path and sha256, the generator named and content-hashed, the
configuration (profile, ilen, composed fragments) carried as data, and the upstream
source fingerprints from the composed fragments. Emission is byte-deterministic — the
same input bytes always yield the same module bytes.

The generator REFUSES (exit 2, naming the construct) on any shape it does not know how to
emit, because a generator that guesses is a second definition wearing the first one's
clothes:

- a unit other than `rv64i-lab-v0` or — since `P4-SYSTEM.2` slice (d), tracked since the
  slice (h) route flip — `rv64gc-lab-v0`, whose module is the committed
  `crates/semulith-core/src/definition_rv64gc.rs` (the same generator, the same census);
- an ILEN other than 32 — C adds 16-bit parcels within that maximum length;
- a composition whose encoding/fragment/semantics documents the schema layer refuses;
- a composed fragment with no semantics document beside it (`<fragment>.sem.sexp`, the
  corpus convention `scripts/check_semantics_corpus.sh` pairs by);
- an encoding instruction with no semantics rule, or a rule for an instruction the
  encoding does not declare, or a rule defined twice without a declared `(refines …)`
  across the composition (the MODEL-COMPOSE.6 rule, re-derived here because this
  generator is the one emitting the executable table);
- a semantics rule citing no specification locator, or carrying other than exactly one
  effect;
- an effect whose operand references the encoding does not provide — the binding rule of
  `scripts/check_semantics.py` (split S-immediates read as `imm12`, split B-immediates as
  `bimm12`, either shift field as `shamt`), re-derived here, with `pc`/`xlen` implicit;
- a bare operand symbol where `(reg …)`/`(imm …)` is required — the lowering must know
  which the reference is, and a bare symbol does not say;
- a non-literal width in `(trunc …)`/`(sext …)`/`(zext …)`/`(bits …)` — the language's
  contract is "widths are always explicit", and this lowering states them as data;
- an A-extension operator (`load-reserved`/`store-conditional`/`amo`) where the
  composition does not compose `riscv/a` — their `Sem` variants emit WITH the fragment
  (P4-SYSTEM.4 slice b: the tracked rv64gc module keeps its byte surface until the
  atomic bind, and a module carrying variants its evaluator match cannot see would not
  compile — the same discipline that keeps the privileged operators off the rv64i
  module), and off the rv64gc module entirely;
- an `(amo …)` whose operation literal is not one of the closed Zaamo nine the
  composition itself encodes — the set is DERIVED from the composed encodings' own
  funct5 fixed bits (a constant that is a function of the pinned tables is derived,
  never typed);
- a floating-point operator (`freg`, `fbox`, `fadd`, … — `schema/semantics.sexp`'s
  floating-point block) where the composition does not compose `riscv/f` — the variants
  emit WITH the fragment (P4-SYSTEM.7 slice c3, the A precedent); and an FP rule the
  semantics checker's `check_fp` refuses (an unresolved rm, a non-literal format, one
  operand in both register files) — re-derived here because this generator emits the
  executable table;
- fixed-bit fields that overlap or do not fit their range.

Usage:
  python3 scripts/gen_definition.py                  # regenerate the committed module
  python3 scripts/gen_definition.py --check          # exit 0 iff the committed module is current
  python3 scripts/gen_definition.py --encoding E --state S --out O   # explicit paths (self-tests)
"""
from __future__ import annotations

import argparse
import difflib
import hashlib
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
import sexp as X                                # noqa: E402
import riscv_asm as R                           # noqa: E402
import check_semantics as SEM                   # noqa: E402
import check_sexp_schema as SCHEMA              # noqa: E402

PROFILE = "rv64i-lab-v0"
PROFILES = ("rv64i-lab-v0", "rv64gc-lab-v0")
ENCODING = ROOT / "profiles" / PROFILE / "encoding.sexp"
STATE = ROOT / "profiles" / PROFILE / "state.sexp"
OUT = ROOT / "crates" / "semulith-core" / "src" / "definition.rs"
SCHEMA_DIR = ROOT / "schema"

SUPPORTED_ILEN = 32

# The language's effect heads and their arities, from schema/semantics.sexp through
# check_semantics' own table — the SEMANTICS doctrine is the checker of record for
# well-formedness; the generator re-derives binding because it emits the executable table.
BINARY_OPS = {"add": "Add", "sub": "Sub", "and": "And", "or": "Or", "xor": "Xor",
              "shl": "Shl", "shr": "Shr", "sar": "Sar", "slt": "Slt", "sltu": "Sltu",
              "eq": "Eq", "ne": "Ne", "lt": "Lt", "ltu": "Ltu", "ge": "Ge", "geu": "Geu"}
WIDTH_OPS = {"trunc": "Trunc", "sext": "Sext", "zext": "Zext"}
# P4-SYSTEM.2 slice (b): the privileged operators, lowered for the rv64gc module only —
# the rv64i module's byte surface is frozen by DEF-GEN, and its corpus never names them.
EXTENDED_UNARY = {"csr-state": "CsrState", "csr-read": "CsrRead", "xret": "Xret"}
EXTENDED_BINARY = {"csr-write": "CsrWrite", "trap-deliver": "TrapDeliver",
                   "csr-rw": "CsrRw"}
EXTENDED_QUATERNARY = {"tlb-invalidate": "TlbInvalidate"}
# P4-SYSTEM.4 slice (b): the A extension's operators. They lower only where the
# composition composes `riscv/a` — their Sem variants emit WITH the fragment, so the
# tracked rv64gc module (the slot still declared) keeps its byte surface until the
# atomic bind (slice e), and an A operator in a composition without A is a refusal,
# named (a module carrying variants its evaluator match cannot see would not compile).
A_TERNARY = {"load-reserved": "LoadReserved", "store-conditional": "StoreConditional"}
A_OPERATORS = set(A_TERNARY) | {"amo"}
BASE_UNARY = {"set-pc": "SetPc"}
# P4-SYSTEM.7 slice (c3): the floating-point block. Its operators lower only where the
# composition composes `riscv/f` (the A precedent: the tracked rv64gc module keeps its byte
# surface until the F bind, slice c6). The format, and f2i/i2f's integer width and
# signedness, are LITERALS lowered as data (check_semantics.check_fp refuses anything else).
F_FORMAT_UNARY = {"fbox": "FBox", "funbox": "FUnbox", "fclass": "FClass"}            # (op n v)
F_FORMAT_BINARY = {"fmin": "FMin", "fmax": "FMax",
                   "feq": "FEq", "flt": "FLt", "fle": "FLe"}                         # (op n a b)
F_ROUNDED_UNARY = {"fsqrt": "FSqrt"}                                                 # (op n rm a)
F_ROUNDED_BINARY = {"fadd": "FAdd", "fsub": "FSub", "fmul": "FMul", "fdiv": "FDiv"}  # (op n rm a b)
F_ROUNDED_TERNARY = {"fmadd": "FMadd"}                                               # (op n rm a b c)
F_CONVERSIONS = {"f2i": "FToI", "i2f": "IToF"}                                       # (op n iw s rm v)
F_OPERATORS = (set(F_FORMAT_UNARY) | set(F_FORMAT_BINARY) | set(F_ROUNDED_UNARY)
               | set(F_ROUNDED_BINARY) | set(F_ROUNDED_TERNARY) | set(F_CONVERSIONS)
               | {"freg", "rounding"})
# P4-SYSTEM.7 slice (d2): D's one operator, the format conversion. It lowers only where the
# composition composes `riscv/d` (the F precedent: the tracked rv64gc module keeps its byte
# surface until the D bind, slice d5); both formats are literals lowered as data.
D_FORMAT_PAIR = {"f2f": "FToF"}                                                      # (op m n rm a)
# P4-SYSTEM.11 slice (a): M's eight arithmetic operators. They lower only where the
# composition composes `riscv/m` (the A/F/D precedent: the tracked rv64gc module keeps its
# byte surface until the M bind, slice b).
M_BINARY = {"mul": "Mul", "mulh": "MulH", "mulhsu": "MulHsu", "mulhu": "MulHu",
            "div": "Div", "divu": "DivU", "rem": "Rem", "remu": "RemU"}


class Surface:
    """Which operator families a module lowers — one value threaded through the lowering
    rather than one parameter per family. `extended` is the rv64gc module's privileged
    surface (P4-SYSTEM.2 slice d); `a` the A extension's (P4-SYSTEM.4 slice b) with
    `amo_set` its closed operation set; `f` the floating-point block's (P4-SYSTEM.7 slice
    c3); `d` the format conversion D adds (P4-SYSTEM.7 slice d2); `m` M's multiply/divide
    (P4-SYSTEM.11 slice a). Each family emits WITH its fragment: a module carrying variants
    its evaluator match cannot see would not compile."""

    def __init__(self, extended: bool = False, a: bool = False,
                 amo_set: frozenset = frozenset(), f: bool = False, d: bool = False,
                 m: bool = False) -> None:
        self.extended, self.a, self.amo_set, self.f, self.d = extended, a, amo_set, f, d
        self.m = m


def amo_operations(insns: dict) -> dict[int, str]:
    """The closed Zaamo operation set, DERIVED from the composed encodings: every
    amo*.w/.d row's funct5 is its own fixed bits 31..27, keyed to the operation the row
    names — a constant that is a function of the pinned tables is derived, never typed.
    Empty when the composition carries no AMO (the tracked rv64gc slot, P4-SYSTEM.4)."""
    out: dict[int, str] = {}
    for name, insn in insns.items():
        if not name.startswith("amo"):
            continue
        funct5 = 0
        for hi, lo, v in insn.fixed:
            for bit in range(max(lo, 27), min(hi, 31) + 1):
                funct5 |= ((v >> (bit - lo)) & 1) << (bit - 27)
        out.setdefault(funct5, name.split(".")[0])
    return out


class Refusal(Exception):
    """The definition (or the language) says something this generator cannot emit."""


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def repo_rel(path: Path) -> str:
    """The repository-relative name of a canonical input. Inputs must live inside the
    repository (the repo-relative-paths rule); an override pointing elsewhere is a
    refusal, never a relative_to crash."""
    try:
        return str(path.resolve().relative_to(ROOT))
    except ValueError:
        raise Refusal(f"{path}: is not inside the repository — canonical inputs must be "
                      "repository-relative, and the manifest names them as such")


def rust_str(text: str) -> str:
    return '"' + text.replace("\\", "\\\\").replace('"', '\\"') + '"'


def schema_validate(path: Path, schema_name: str) -> None:
    """Refuse, naming the construct, a document the schema layer refuses (SOT-FORMAT.2)."""
    try:
        constructs, operators = SCHEMA.load_schema(SCHEMA_DIR / schema_name)
        errors = SCHEMA.validate_file(path, constructs, operators)
    except (SCHEMA.SchemaError, X.SexpError) as exc:
        raise Refusal(f"the schema {schema_name} itself does not read: {exc}")
    if errors:
        raise Refusal(f"{path.name}: refused by {schema_name} — " + "; ".join(errors))


def bound_operands(operands: tuple[str, ...]) -> set[str]:
    """The operand names a semantics rule may reference, per the binding rule of
    `scripts/check_semantics.py`: the encoding provides the fields; a split store
    immediate reads as one `imm12`, a split branch immediate as one `bimm12`, and either
    shift field reads as `shamt`. `pc` and `xlen` are implicit (checked at the caller)."""
    names = set(operands)
    if "imm12hi" in names:
        names -= {"imm12hi", "imm12lo"}
        names.add("imm12")
    if "bimm12hi" in names:
        names -= {"bimm12hi", "bimm12lo"}
        names.add("bimm12")
    if "shamtd" in names or "shamtw" in names:
        names.add("shamt")
    return names


def load_semantics(root: Path, names: list[str], insns: dict[str, R.Insn],
                   pseudos: dict[str, R.Insn] | None = None) -> tuple[dict, dict, dict]:
    """Every composed fragment's semantics rules, keyed by instruction, in composition
    order, under the MODEL-COMPOSE.6 refinement rule — re-derived here (see module doc).

    Returns (rules, pseudo_rules, expansions): a rule naming a PSEUDO (Zicntr's counter reads)
    is checked against the pseudo's operand row and returned separately — it never decodes
    (the word matches the realizing instruction), so it rides as metadata, not a table row.
    An EXPANSION (P4-SYSTEM.12 slice b — a compressed instruction declared by the base
    instruction it expands into) rides beside its rule: the rule entry carries its source and,
    for an own-rule expansion (C.JALR), its effect; the expansion carries the base, the operand
    bindings and the reserved condition. Every binding set is re-judged here against the base
    rule it feeds: exactly the operands that rule reads."""
    try:
        SEM.load_language()
    except SEM.SemError as exc:
        raise Refusal(f"the semantic language itself does not read: {exc}")

    rules: dict[str, tuple[str, X.Sexp]] = {}
    pseudo_rules: dict[str, str] = {}
    expansions: dict[str, tuple[str | None, list, X.Sexp | None]] = {}
    seen: dict[str, Path] = {}
    for name in names:
        sem_path = root / (name + ".sem.sexp")
        if not sem_path.is_file():
            raise Refusal(f"fragment {name!r} has no semantics document at {sem_path} — "
                          "the corpus pairs <fragment>.sexp with <fragment>.sem.sexp; an "
                          "encoding without its semantics is not a definition an engine "
                          "could consume (EXTRACTION)")
        schema_validate(sem_path, "semantics.sexp")
        try:
            doc = X.read_file(sem_path)[0]
        except X.SexpError as exc:
            raise Refusal(f"{sem_path}: does not parse — {exc}")
        if X.head(doc, str(sem_path)) != "semantics":
            raise Refusal(f"{sem_path}: expected a (semantics …) document")

        defined: list[str] = []
        refined = {str(X.field(r, "insn", str(sem_path)))
                   for r in X.children(doc, "refines")}
        for s in X.children(doc, "sem"):
            insn = str(X.field(s, "insn", str(sem_path)))
            where = f"{sem_path.name} [{insn}]"
            if insn in defined:
                raise Refusal(f"{where}: defined twice")
            defined.append(insn)
            if insn not in insns and insn not in (pseudos or {}):
                raise Refusal(f"{where}: no instruction of that name in the composed "
                              f"encoding — a semantics rule for a word the encoding does "
                              f"not declare is a rule nothing can decode to")
            sources = X.children(s, "source")
            if len(sources) != 1 or not (len(sources[0]) == 2 and isinstance(sources[0][1], str)):
                raise Refusal(f"{where}: a semantics rule must cite exactly one "
                              "specification locator — a rule nobody can trace to a "
                              "document is a rule nobody can dispute")
            effects = X.children(s, "effect")
            if len(effects) != 1 or len(effects[0][1:]) != 1:
                raise Refusal(f"{where}: must carry exactly one effect expression, has "
                              f"{len(effects[0][1:]) if effects else 0}")
            effect = effects[0][1]
            operand_names = (insns[insn].operands if insn in insns
                             else (pseudos or {})[insn].operands)
            try:
                SEM.check_expr(effect, where, bound_operands(operand_names))
                SEM.check_fp(effect, where, bound_operands(operand_names))
                SEM.check_division(effect, where)
            except SEM.SemError as exc:
                raise Refusal(str(exc))
            if insn in (pseudos or {}):
                # A pseudo never decodes — its rule's meaning is the realizing
                # instruction's (the counter reads ARE csrrs with fixed fields); the
                # locator rides as the pseudo's citation.
                pseudo_rules[insn] = str(sources[0][1])
            else:
                rules[insn] = (str(sources[0][1]), effect)
                expansions.pop(insn, None)         # a later declared refinement replaces it

        for x in X.children(doc, "expand"):
            insn = str(X.field(x, "insn", str(sem_path)))
            where = f"{sem_path.name} [{insn}]"
            if insn in defined:
                raise Refusal(f"{where}: defined twice")
            defined.append(insn)
            if insn not in insns:
                raise Refusal(f"{where}: an expansion for no instruction of the composed encoding")
            try:
                _, base, _ = SEM.check_expand(x, where, bound_operands(insns[insn].operands))
            except SEM.SemError as exc:
                raise Refusal(str(exc))
            binds = [(str(X.field(o, "name", where)), X.field(o, "value", where))
                     for o in X.children(x, "operand")]
            reserved = X.children(x, "reserved")
            own = X.children(x, "effect")
            expansions[insn] = (base, binds, reserved[0][1] if reserved else None)
            rules[insn] = (str(X.field(x, "source", where)), own[0][1] if own else None)

        for r in sorted(refined - set(defined)):
            raise Refusal(f"{sem_path.name}: declares (refines (insn {rust_str(r)})) but "
                          f"defines no semantics for {r!r} — a declaration with no "
                          "override is a lie about what this file does")
        for r in sorted(refined & set(defined)):
            if r not in seen:
                raise Refusal(f"{sem_path.name}: declares (refines (insn {rust_str(r)})) "
                              f"but no earlier fragment in this composition defines "
                              f"{r!r} — refining nothing")
        for insn in defined:
            if insn in seen and insn not in refined:
                raise Refusal(f"{sem_path.name} [{insn}]: SILENT REDEFINITION — {insn!r} "
                              f"is already defined in {seen[insn].name}, and this file "
                              "declares no (refines (insn …)). An extension that changes "
                              "a base behaviour must declare the refinement point "
                              "(MODEL-COMPOSE.6)")
        for insn in defined:
            seen[insn] = sem_path

    missing = sorted(set(insns) - set(rules))
    if missing:
        raise Refusal(f"{len(missing)} declared instruction(s) have NO semantics: "
                      f"{', '.join(missing[:12])}{' …' if len(missing) > 12 else ''} — "
                      "the execution authority must cover every declared instruction")
    # an expansion's base must be a composed instruction with a rule, and the bindings must be
    # EXACTLY the operands that rule reads (check_semantics' compose rule, re-derived here)
    for insn, (base, binds, _) in expansions.items():
        if base is None:
            continue
        if base not in rules or base in expansions:
            raise Refusal(f"{insn}: expands into {base!r}, which is not a composed base instruction")
        reads = SEM.operands_read(rules[base][1])
        bound = {n for n, _ in binds}
        if bound != reads:
            raise Refusal(f"{insn}: binds {sorted(bound)}, but {base}'s rule reads {sorted(reads)}")
    return rules, pseudo_rules, expansions


def fixed_mask(name: str, fixed: tuple[tuple[int, int, int], ...]) -> tuple[int, int]:
    """The (mask, value) a decoder matches on, from the fixed-bit triples. Overlapping or
    ill-fitting fixed fields are refused: a decoder built on them would not mean what the
    table says."""
    mask, value = 0, 0
    for hi, lo, val in fixed:
        if not 0 <= lo <= hi <= 31:
            raise Refusal(f"{name}: fixed field [{hi}:{lo}] sits outside the 32-bit word")
        width = hi - lo + 1
        if val < 0 or val >= (1 << width):
            raise Refusal(f"{name}: fixed value {val:#x} does not fit in bits [{hi}:{lo}] "
                          f"({width} bits)")
        bits = ((1 << width) - 1) << lo
        if mask & bits and (value & bits) != (val << lo):
            raise Refusal(f"{name}: two fixed fields claim bits [{hi}:{lo}] with "
                          "different values — the encoding is not a function")
        mask |= bits
        value |= val << lo
    return mask, value


def lit64(v: int) -> str:
    """A u64 literal masked to 64 bits: `(lit -2)` and `(lit 0xffff…)` are the same
    two's-complement constant."""
    return f"0x{v & 0xFFFF_FFFF_FFFF_FFFF:016x}"


def indent_tree(text: str) -> str:
    """Parenthesis-depth indentation for the fully-broken constructor expression, so
    the generator's shape and rustfmt's agree — drift is content, never formatting
    (the P1-LAB.3 lesson, applied to a deeper tree)."""
    out, depth = [], 0
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith((")", "]")):
            depth -= 1
        out.append("    " * depth + stripped)
        if stripped.endswith(("(", "[")):
            depth += 1
    return "\n".join(out)


def emit_sem(form: X.Sexp, where: str, surface: Surface = Surface()) -> str:
    """Lower one effect expression to the `Sem` tree literal, fully broken one level per
    line; `indent_tree` gives it the shape rustfmt would. `extended` is the rv64gc
    module's operator surface (P4-SYSTEM.2 slice d): the privileged operators lower only
    there — the rv64i module's byte surface is frozen by DEF-GEN, and a privileged
    operator in its corpus is a refusal, named, never silently emitted uncallable. The
    A extension's operators lower only where the composition composes `riscv/a`, with the
    closed Zaamo set derived from the composed encodings (`amo_operations`); the
    floating-point block's only where it composes `riscv/f` (`Surface`)."""
    extended, a_variants, amo_set = surface.extended, surface.a, surface.amo_set

    def sub(x):
        return emit_sem(x, where, surface)
    if isinstance(form, int):
        return f"Sem::Lit({lit64(form)})"
    if isinstance(form, str):
        raise Refusal(f"{where}: a bare operand reference {form!r} — the lowering must "
                      "know whether the reference is a register or an immediate; write "
                      "(reg …) or (imm …)")
    if not isinstance(form, list) or not form:
        raise Refusal(f"{where}: empty form")
    op = str(form[0])
    args = form[1:]
    unary = dict(BASE_UNARY, **EXTENDED_UNARY)
    binary = dict(BINARY_OPS, trap="Trap", **EXTENDED_BINARY)
    if surface.m:
        binary = dict(binary, **M_BINARY)
    ternary = {"load": "Load", "store": "Store", "if": "If"}
    if a_variants:
        ternary = dict(ternary, **A_TERNARY)
    if not extended and op in (set(EXTENDED_UNARY) | set(EXTENDED_BINARY) | set(EXTENDED_QUATERNARY)
                               | A_OPERATORS | F_OPERATORS | set(D_FORMAT_PAIR) | set(M_BINARY)
                               | {"field", "inst", "mode"}):
        raise Refusal(f"{where}: ({op} …) is the rv64gc module's operator surface "
                      f"(P4-SYSTEM.2 slice b) — the rv64i corpus does not lower it")
    if extended and not a_variants and op in A_OPERATORS:
        raise Refusal(f"{where}: ({op} …) is the A extension's operator surface "
                      f"(P4-SYSTEM.4 slice b), but this composition does not compose "
                      f"riscv/a — the variants emit WITH the fragment, so a module "
                      f"carrying them without it would not compile against its evaluator")
    if extended and not surface.f and op in F_OPERATORS:
        raise Refusal(f"{where}: ({op} …) is the floating-point operator surface "
                      f"(P4-SYSTEM.7 slice c3), but this composition does not compose "
                      f"riscv/f — the variants emit WITH the fragment, so a module "
                      f"carrying them without it would not compile against its evaluator")
    if extended and not surface.d and op in D_FORMAT_PAIR:
        raise Refusal(f"{where}: ({op} …) is the D extension's format conversion "
                      f"(P4-SYSTEM.7 slice d2), but this composition does not compose "
                      f"riscv/d — the variant emits WITH the fragment, so a module "
                      f"carrying it without it would not compile against its evaluator")
    if extended and not surface.m and op in M_BINARY:
        raise Refusal(f"{where}: ({op} …) is the M extension's multiply/divide surface "
                      f"(P4-SYSTEM.11 slice a), but this composition does not compose "
                      f"riscv/m — the variants emit WITH the fragment, so a module "
                      f"carrying them without it would not compile against its evaluator")
    if op == "reg" and len(args) == 1 and isinstance(args[0], str):
        return f"Sem::Reg({rust_str(str(args[0]))})"
    if op in EXTENDED_QUATERNARY and len(args) == 4:
        return f"Sem::{EXTENDED_QUATERNARY[op]}(\n" + "".join(f"&{sub(arg)},\n" for arg in args) + ")"
    if op == "freg" and len(args) == 1 and isinstance(args[0], str):
        return f"Sem::FReg({rust_str(str(args[0]))})"
    if op == "rounding" and len(args) == 1:
        return f"Sem::Rounding(\n&{sub(args[0])},\n)"
    if op in F_FORMAT_UNARY and len(args) == 2:
        return f"Sem::{F_FORMAT_UNARY[op]}(\n{args[0]},\n&{sub(args[1])},\n)"
    if op in F_FORMAT_BINARY and len(args) == 3:
        return f"Sem::{F_FORMAT_BINARY[op]}(\n{args[0]},\n&{sub(args[1])},\n&{sub(args[2])},\n)"
    if op in F_ROUNDED_UNARY and len(args) == 3:
        return f"Sem::{F_ROUNDED_UNARY[op]}(\n{args[0]},\n&{sub(args[1])},\n&{sub(args[2])},\n)"
    if op in F_ROUNDED_BINARY and len(args) == 4:
        return (f"Sem::{F_ROUNDED_BINARY[op]}(\n{args[0]},\n&{sub(args[1])},\n"
                f"&{sub(args[2])},\n&{sub(args[3])},\n)")
    if op in F_ROUNDED_TERNARY and len(args) == 5:
        return (f"Sem::{F_ROUNDED_TERNARY[op]}(\n{args[0]},\n&{sub(args[1])},\n"
                f"&{sub(args[2])},\n&{sub(args[3])},\n&{sub(args[4])},\n)")
    if op in D_FORMAT_PAIR and len(args) == 4:
        return (f"Sem::{D_FORMAT_PAIR[op]}(\n{args[0]},\n{args[1]},\n"
                f"&{sub(args[2])},\n&{sub(args[3])},\n)")
    if op in F_CONVERSIONS and len(args) == 5:
        signed = "true" if args[2] == 1 else "false"
        return (f"Sem::{F_CONVERSIONS[op]}(\n{args[0]},\n{args[1]},\n{signed},\n"
                f"&{sub(args[3])},\n&{sub(args[4])},\n)")
    if op == "imm" and len(args) == 1 and isinstance(args[0], str):
        return f"Sem::Imm({rust_str(str(args[0]))})"
    if op == "field" and len(args) == 1 and isinstance(args[0], str):
        # (field X) — the RAW numeric value of an operand field (P4-SYSTEM.2 slice b):
        # a register index, a csr address, a zimm5 — not the register the field names.
        return f"Sem::Field({rust_str(str(args[0]))})"
    if op == "inst" and not args:
        return "Sem::Inst"
    if op == "mode" and not args:
        return "Sem::Mode"
    if op == "pc" and not args:
        return "Sem::Pc"
    if op == "xlen" and not args:
        return "Sem::Xlen"
    if op == "lit" and len(args) == 1 and isinstance(args[0], int):
        return f"Sem::Lit({lit64(args[0])})"
    if op == "nop" and not args:
        return "Sem::Nop"
    if op == "amo" and len(args) == 4:
        # (amo op width addr value) — one of the closed Zaamo nine (P4-SYSTEM.4 slice
        # b). The op is the operation's funct5 encoding as (lit N), and N must be one
        # the composition itself encodes — the set is derived (amo_operations), so a
        # sem file cannot invent an operation the pinned tables do not carry.
        lit = args[0]
        if not (isinstance(lit, list) and len(lit) == 2 and lit[0] == "lit"
                and isinstance(lit[1], int)):
            raise Refusal(f"{where}: (amo op …) takes the operation's funct5 as a "
                          f"(lit N) — the value the instruction's own fixed bits carry")
        if lit[1] not in amo_set:
            raise Refusal(f"{where}: amo op {lit[1]:#04x} is not one of the closed Zaamo "
                          f"nine this composition encodes "
                          f"({', '.join(f'{v:#04x}' for v in sorted(amo_set)) or 'none — no AMO composed'}) "
                          f"— derived from the composed encodings' own funct5 fixed bits")
        return (f"Sem::Amo(\n{lit[1]},\n&{sub(args[1])},\n"
                f"&{sub(args[2])},\n"
                f"&{sub(args[3])},\n)")
    if op == "seq":
        inner = ",\n".join(f"&{sub(a)}" for a in args)
        return f"Sem::Seq(&[\n{inner},\n])"
    if op in binary and len(args) == 2:
        return (f"Sem::{binary[op]}(\n&{sub(args[0])},\n"
                f"&{sub(args[1])},\n)")
    if op in WIDTH_OPS and len(args) == 2 and isinstance(args[0], int):
        return f"Sem::{WIDTH_OPS[op]}(\n{args[0]},\n&{sub(args[1])},\n)"
    if op == "bits" and len(args) == 3 and isinstance(args[0], int) and isinstance(args[1], int):
        return f"Sem::Bits(\n{args[0]},\n{args[1]},\n&{sub(args[2])},\n)"
    if op == "set" and len(args) == 2:
        return (f"Sem::Set(\n&{sub(args[0])},\n"
                f"&{sub(args[1])},\n)")
    if op in unary and len(args) == 1:
        return f"Sem::{unary[op]}(\n&{sub(args[0])},\n)"
    if op in ternary and len(args) == 3:
        return (f"Sem::{ternary[op]}(\n&{sub(args[0])},\n"
                f"&{sub(args[1])},\n&{sub(args[2])},\n)")
    if op in (set(binary) | set(WIDTH_OPS) | {"bits"}) and args:
        raise Refusal(f"{where}: ({op} …) has an argument this lowering cannot state "
                      "as data — width arguments of trunc/sext/zext/bits must be literal "
                      "integers; write the width explicitly")
    raise Refusal(f"{where}: unknown or malformed form ({op} …) — the SEMANTICS doctrine "
                  "is the checker of record; this generator refuses to emit what it "
                  "cannot lower")


def load_inputs(encoding_path: Path, state_path: Path):
    """Read and validate the whole definition; return everything emission needs."""
    schema_validate(encoding_path, "encoding.sexp")
    forms = X.read_file(encoding_path)
    if len(forms) != 1 or X.head(forms[0], str(encoding_path)) != "encoding":
        raise Refusal(f"{encoding_path}: expected exactly one (encoding …) form")
    enc = forms[0]
    profile = str(X.field(enc, "profile", str(encoding_path)))
    if profile not in PROFILES:
        raise Refusal(f"profile {profile!r} — this generator is scoped to {PROFILES!r}; "
                      "another unit is generator work, not a config knob")
    extended = profile == "rv64gc-lab-v0"
    ilen = int(X.field(enc, "ilen", str(encoding_path)))
    if ilen != SUPPORTED_ILEN:
        raise Refusal(f"ilen {ilen} — this generator emits a 32-bit decode table only; "
                      "another instruction length is generator work, never silently "
                      "assumed")

    # Composition order (base first, then extensions) — read here for the manifest and
    # the semantics walk; the name→fragment resolution itself stays with the one shared
    # resolver (`riscv_asm.resolve_composition`).
    comp = X.children(enc, "compose")
    if not comp:
        raise Refusal(f"{encoding_path}: no (compose …) — a unit that composes nothing "
                      "owns no encodings")
    names = [str(X.field(comp[0], "base", str(encoding_path)))]
    ext = X.children(comp[0], "extensions")
    for e in ext:
        names += [str(x) for x in e[1:]]

    # The one shared resolver: fields, instructions, and scatter layouts, validated.
    # Pseudos ride too (P4-SYSTEM.2): they add nothing to the decode table — a word of
    # theirs matches the realizing instruction's row — but their names/operands/sources
    # emit as metadata so the coverage census (slice f) can map the architectural
    # spellings, and a semantics rule may name a pseudo.
    loaded = R.load_canonical_encoding(encoding_path, with_pseudos=True)
    arg_lut, insns, layout, pseudos = loaded
    root = encoding_path.parent.parent.parent / str(X.field(enc, "fragment-root",
                                                            str(encoding_path)))

    # Every declared operand names a field. One that does not would extract SILENTLY at
    # runtime — the guessed translation ARCHITECTURE §2 forbids: an unsupported construct
    # is a model-generation failure, named.
    for insn in insns.values():
        for op in insn.operands:
            if op not in arg_lut:
                raise Refusal(f"{insn.name}: operand {op!r} names no field — extraction "
                              "for it would be silent; declare the field or drop the operand")

    # Every composed fragment is schema-valid; its pinned-source fingerprints ride in
    # the manifest (OWN-03's source fingerprints).
    source_pins: dict[str, str] = {}
    for name in names:
        frag_path = root / (name + ".sexp")
        schema_validate(frag_path, "fragment.sexp")
        try:
            frag = X.read_file(frag_path)[0]
        except X.SexpError as exc:
            raise Refusal(f"{frag_path}: does not parse — {exc}")
        for f in X.children(X.children(frag, "source")[0], "file"):
            pin_name, pin_sha = str(X.field(f, "name")), str(X.field(f, "sha256"))
            if pin_name in source_pins and source_pins[pin_name] != pin_sha:
                raise Refusal(f"{frag_path}: source {pin_name!r} pins sha256 {pin_sha} "
                              f"but an earlier fragment pins {source_pins[pin_name]} — "
                              "one name, one pinned byte set")
            source_pins[pin_name] = pin_sha

    rules, pseudo_rules, expansions = load_semantics(root, names, insns, pseudos)

    # The manifest names every canonical input (the state descriptor is fingerprinted
    # here; its executable half is `state.rs`'s own derivation, governed by STATE-GEN).
    inputs = {repo_rel(encoding_path): sha256(encoding_path),
              repo_rel(state_path): sha256(state_path)}
    for name in names:
        inputs[repo_rel(root / (name + ".sexp"))] = sha256(root / (name + ".sexp"))
        inputs[repo_rel(root / (name + ".sem.sexp"))] = sha256(root / (name + ".sem.sexp"))

    fields = []
    for fname, (hi, lo) in sorted(arg_lut.items()):
        pieces = tuple(layout.get(fname, ()))
        fields.append((fname, hi, lo, pieces))
    a_variants = "riscv/a" in names
    f_variants = "riscv/f" in names
    d_variants = "riscv/d" in names
    m_variants = "riscv/m" in names
    c_variants = "riscv/c" in names
    if expansions and not (extended and c_variants):
        raise Refusal("expansions require the rv64gc composition with riscv/c — the binding "
                      "metadata emits WITH the fragment")
    return dict(profile=profile, ilen=ilen, names=names, insns=insns,
                pseudos=pseudos, pseudo_rules=pseudo_rules, extended=extended,
                fields=fields, rules=rules, inputs=inputs, source_pins=source_pins,
                a_variants=a_variants, amo_ops=amo_operations(insns), f_variants=f_variants,
                d_variants=d_variants, m_variants=m_variants,
                c_variants=c_variants, expansions=expansions)


def emit(data: dict, generator_sha: str) -> str:
    insns = data["insns"]
    extended = data["extended"]
    compressed = data["c_variants"]
    surface = Surface(extended, data["a_variants"], frozenset(data["amo_ops"]),
                      data["f_variants"], data["d_variants"], data["m_variants"])
    w = []
    a = w.append
    a("//! GENERATED — do not edit (OWN-03). Regenerate with `python3 scripts/gen_definition.py`;")
    a("//! drift between this module and the canonical definition it derives from is refused")
    a("//! by the DEF-GEN doctrine (`scripts/check_definition_gen.sh`). These tables are the")
    a("//! executable skeleton of the unit's canonical definition (`docs/ARCHITECTURE.md` §2):")
    if extended:
        a("//! the decode metadata, the operand-field table, and the semantics effect trees,")
        a("//! lowered from rv64gc-lab-v0's composition (base riscv/rv64i + the Zicsr, Zicntr")
        a("//! and privileged-system fragments, P4-SYSTEM.2) — including the privileged operator")
        a("//! surface of `schema/semantics.sexp`. This module landed tracked at the route")
        a("//! flip (P4-SYSTEM.2 slice h, decision_generated-mirror-needs-tracked-input: a")
        a("//! tracked generated module needs its canonical inputs tracked in the same commit).")
    else:
        a("//! the decode metadata, the operand-field table, and the semantics effect trees,")
        a("//! lowered from `profiles/rv64i-lab-v0/encoding.sexp` composing `riscv/rv64i`, with")
        a("//! `definitions/riscv/rv64i.sem.sexp` the execution authority's semantics data.")
    a("//!")
    a("//! OWN-01: every semantic rule has exactly one executable owner — the semantics")
    a("//! DATA. This module is its lowered mirror; there is no handwritten second copy of")
    a("//! any rule, and the interpreter slice (`P1-LAB.8`) evaluates exactly these trees.")
    a("//!")
    a("//! Canonical inputs (sha256):")
    for path in sorted(data["inputs"]):
        a(f"//!   `{path}`  `{data['inputs'][path]}`")
    a(f"//! Generator: `scripts/gen_definition.py` (sha256 `{generator_sha}`)")
    a("")
    a("/// OWN-03's generation manifest: the canonical inputs, the generator, the")
    a("/// configuration, and the upstream source fingerprints this module derives from.")
    a("/// Values, not behaviour: reading the manifest never touches the filesystem — the")
    a("/// fingerprints were computed at generation time, and the DEF-GEN doctrine refuses")
    a("/// the day the bytes behind them change without regeneration.")
    a("pub struct DefinitionManifest {")
    a("    /// The unit this definition was generated for.")
    a("    pub profile: &'static str,")
    a("    /// The instruction length in bits (ILEN = 32 for this profile).")
    a("    pub ilen: u32,")
    a("    /// The fragments the composition resolves, base first, then extensions.")
    a("    pub fragments: &'static [&'static str],")
    a("    /// The generator that produced this module, named and content-hashed.")
    a("    pub generator: GeneratorPin,")
    a("    /// Every canonical input, by repository-relative path and content hash.")
    a("    pub inputs: &'static [InputPin],")
    a("    /// The upstream source fingerprints the composed fragments carry.")
    a("    pub sources: &'static [SourcePin],")
    a("}")
    a("")
    a("/// The generator, identified by name and content — OWN-03's generator fingerprint.")
    a("pub struct GeneratorPin {")
    a("    pub name: &'static str,")
    a("    pub sha256: &'static str,")
    a("}")
    a("")
    a("/// One canonical input: the path, and the sha256 of the exact bytes.")
    a("pub struct InputPin {")
    a("    pub path: &'static str,")
    a("    pub sha256: &'static str,")
    a("}")
    a("")
    a("/// One upstream source the definition was generated from, pinned by the fragment.")
    a("pub struct SourcePin {")
    a("    pub file: &'static str,")
    a("    pub sha256: &'static str,")
    a("}")
    a("")
    frag_list = ", ".join(rust_str(n) for n in data["names"])
    a("pub static MANIFEST: DefinitionManifest = DefinitionManifest {")
    a(f"    profile: {rust_str(data['profile'])},")
    a(f"    ilen: {data['ilen']},")
    # rustfmt lays an array out vertically once it is wide enough — measured, not
    # guessed: the 4-fragment line (79 chars) stays inline under `cargo fmt --check`,
    # P4-SYSTEM.4 slice e's 5-fragment line (90) is broken one element per line. The
    # emission must be rustfmt-stable BY CONSTRUCTION, so 80 is the cutoff.
    frag_inline = f"    fragments: &[{frag_list}],"
    if len(frag_inline) > 80:
        frag_lines = "\n".join(f"        {rust_str(n)}," for n in data["names"])
        frag_block = f"    fragments: &[\n{frag_lines}\n    ],"
    else:
        frag_block = frag_inline
    a(frag_block)
    a("    generator: GeneratorPin {")
    a("        name: \"scripts/gen_definition.py\",")
    a(f"        sha256: {rust_str(generator_sha)},")
    a("    },")
    a("    inputs: &[")
    for path in sorted(data["inputs"]):
        a("        InputPin {")
        a(f"            path: {rust_str(path)},")
        a(f"            sha256: {rust_str(data['inputs'][path])},")
        a("        },")
    a("    ],")
    a("    sources: &[")
    for fname in sorted(data["source_pins"]):
        a("        SourcePin {")
        a(f"            file: {rust_str(fname)},")
        a(f"            sha256: {rust_str(data['source_pins'][fname])},")
        a("        },")
    a("    ],")
    a("};")
    a("")
    a("/// One operand field of the encoding: its bit range in the 32-bit word, and, for")
    a("/// the scattered B/J immediates, the immediate-bit pieces the field carries in")
    a("/// MSB-first order — `(12, 12)` first means the field's top bit holds imm[12].")
    a("/// Empty `scatter` marks a contiguous field.")
    a("pub struct FieldDef {")
    a("    pub name: &'static str,")
    a("    pub hi: u8,")
    a("    pub lo: u8,")
    a("    pub scatter: &'static [(u8, u8)],")
    a("}")
    a("")
    a(f"/// The {len(data['fields'])} operand fields the composed fragments declare, sorted by")
    a("/// name: what the decoder extracts, and how the scrambled immediates unscramble.")
    a("/// Every declared operand names a field — this generator refuses one that does not,")
    a("/// because extraction for it would be silent (ARCHITECTURE §2: an unsupported")
    a("/// construct is a model-generation failure, never a guessed translation).")
    a("pub static FIELDS: &[FieldDef] = &[")
    for fname, hi, lo, pieces in data["fields"]:
        a("    FieldDef {")
        a(f"        name: {rust_str(fname)},")
        a(f"        hi: {hi},")
        a(f"        lo: {lo},")
        if pieces:
            inner = ", ".join(f"({p[0]}, {p[1]})" for p in pieces)
            inline = f"        scatter: &[{inner}],"
            if len(inline) > 80:
                a("        scatter: &[")
                for top, bottom in pieces:
                    a(f"            ({top}, {bottom}),")
                a("        ],")
            else:
                a(inline)
        else:
            a("        scatter: &[],")
        a("    },")
    a("];")
    a("")
    a("/// One instruction of the composed definition: the fixed bits a decoder matches on")
    a("/// (`mask`/`value` — a word decodes to this instruction iff `word & mask = value`),")
    a("/// the operands the encoding declares, the upstream table the encoding came from,")
    a("/// the specification locator the semantics rule cites, and the rule's effect tree.")
    a("pub struct InsnDef {")
    a("    pub name: &'static str,")
    a("    pub mask: u32,")
    a("    pub value: u32,")
    a("    /// The operand fields as the encoding declares them, in operand order. A split")
    a("    /// immediate appears as its two fields (`imm12hi`/`imm12lo`, `bimm12hi`/`bimm12lo`);")
    a("    /// the semantics trees read the composed `imm12`/`bimm12` (and `shamt` for either")
    a("    /// shift field) — the binding rule of `scripts/check_semantics.py`, which the")
    a("    /// generator re-derives and the tests below re-check as data.")
    a("    pub operands: &'static [&'static str],")
    a("    /// The upstream encoding table this instruction's fixed bits were generated from.")
    a("    pub from: &'static str,")
    a("    /// The specification locator the semantics rule was derived from.")
    a("    pub source: &'static str,")
    a("    /// The semantics rule's effect, lowered from the semantics data — the one")
    a("    /// executable owner of the behaviour (OWN-01).")
    a("    pub effect: &'static Sem,")
    if extended:
        a("    /// Instruction length in bytes: an expansion consumes one 16-bit parcel.")
        a("    pub length: u8,")
        a("    /// Operand mappings evaluated over the compressed fields BEFORE the effect.")
        a("    pub expansion: Option<&'static Expansion>,")
    a("}")
    a("")
    if extended:
        a("/// A compressed instruction's declared expansion. The effect is lowered from the")
        a("/// named base rule (C.JALR has its own); bindings retain their value widths, so")
        a("/// the base rule sign-extends a scattered immediate from its OWN top bit.")
        a("pub struct Expansion {")
        a("    pub base: Option<&'static str>,")
        a("    pub bindings: &'static [OperandBinding],")
        a("    /// Evaluated over the original fields; true delivers illegal instruction.")
        a("    pub reserved: Option<&'static Sem>,")
        a("}")
        a("")
        a("pub struct OperandBinding {")
        a("    pub name: &'static str,")
        a("    pub value: &'static Sem,")
        a("}")
        a("")
    ordered = sorted(insns, key=lambda n: (-fixed_mask(n, insns[n].fixed)[0].bit_count(), n)) \
        if compressed else sorted(insns)
    order = "by descending fixed-bit specificity, then name" if compressed else "by name"
    a(f"/// The {len(ordered)} instructions of the composed definition, sorted {order}. Every")
    a("/// declared instruction carries its semantics — completeness is a generation-time")
    a("/// refusal, not a hope (EXTRACTION).")
    a("pub static INSNS: &[InsnDef] = &[")
    for name in ordered:
        insn = insns[name]
        mask, value = fixed_mask(name, insn.fixed)
        source, effect = data["rules"][name]
        expansion = data["expansions"].get(name)
        if expansion and expansion[0] is not None:
            effect = data["rules"][expansion[0]][1]
        ops = ", ".join(rust_str(o) for o in insn.operands)
        where = f"semantics of {name}"
        a("    InsnDef {")
        a(f"        name: {rust_str(name)},")
        a(f"        mask: 0x{mask:08x},")
        a(f"        value: 0x{value:08x},")
        a(f"        operands: &[{ops}],")
        a(f"        from: {rust_str(insn.source)},")
        a(f"        source: {rust_str(source)},")
        tree = indent_tree(emit_sem(effect, where, surface))
        tree_lines = tree.splitlines()
        if extended:
            tree_lines[-1] += ","
        a(f"        effect: &{tree_lines[0]}")
        for line in tree_lines[1:]:
            a(f"        {line}")
        if extended:
            a(f"        length: {2 if expansion else 4},")
            if expansion:
                base, binds, reserved = expansion
                a("        expansion: Some(&Expansion {")
                a(f"            base: {'Some(' + rust_str(base) + ')' if base else 'None'},")
                a("            bindings: &[")
                for operand, value_expr in binds:
                    a("                OperandBinding {")
                    a(f"                    name: {rust_str(operand)},")
                    lines = indent_tree(emit_sem(value_expr, where, surface)).splitlines()
                    a(f"                    value: &{lines[0]}")
                    for line in lines[1:]:
                        a(f"                    {line}")
                    a("                },")
                a("            ],")
                if reserved is None:
                    a("            reserved: None,")
                else:
                    lines = indent_tree(emit_sem(reserved, where, surface)).splitlines()
                    a(f"            reserved: Some(&{lines[0]}")
                    for line in lines[1:]:
                        a(f"            {line}")
                    a("            ),")
                a("        }),")
            else:
                a("        expansion: None,")
        a("    },")
    a("];")
    a("")
    a("/// One node of a canonical semantics effect, lowered from the S-expression operator")
    if extended:
        # the language's size is DERIVED from the loaded schema (P4-SYSTEM.7 slice c3: the
        # typed "43" had been wrong since the A operators landed — 44 forms)
        a(f"/// language (`schema/semantics.sexp`, the {len(SEM.FORMS)} forms `scripts/check_semantics.py`")
    else:
        a("/// language (`schema/semantics.sexp`, the 32 forms `scripts/check_semantics.py`")
    a("/// checks) by `scripts/gen_definition.py`. Literals are XLEN-wide two's-complement")
    a("/// constants, masked to 64 bits; widths are explicit data everywhere the language")
    a("/// states them (`Trunc`/`Sext`/`Zext`/`Bits`). Evaluation — what the forms DO — is")
    a("/// the interpreter slice's job (`P1-LAB.8`); this type is the data it evaluates.")
    a("#[derive(Clone, Copy, Debug)]")
    a("pub enum Sem {")
    a("    /// `(lit N)` — an XLEN-wide two's-complement constant.")
    a("    Lit(u64),")
    a("    /// `(reg NAME)` — an architectural register operand.")
    a("    Reg(&'static str),")
    a("    /// `(imm NAME)` — an immediate operand.")
    a("    Imm(&'static str),")
    a("    /// `(pc)` — the address of the executing instruction.")
    a("    Pc,")
    a("    /// `(xlen)` — the XLEN constant (64 for this profile).")
    a("    Xlen,")
    for sexp_name, rust_name in BINARY_OPS.items():
        a(f"    /// `({sexp_name} a b)` — see `schema/semantics.sexp` for the contract.")
        a(f"    {rust_name}(&'static Sem, &'static Sem),")
    a("    /// `(trunc N v)` — the low N bits of `v`.")
    a("    Trunc(u64, &'static Sem),")
    a("    /// `(sext N v)` — sign-extend the low N bits of `v` to XLEN.")
    a("    Sext(u64, &'static Sem),")
    a("    /// `(zext N v)` — zero-extend the low N bits of `v` to XLEN.")
    a("    Zext(u64, &'static Sem),")
    a("    /// `(bits hi lo v)` — the bits [hi:lo] of `v`.")
    a("    Bits(u8, u8, &'static Sem),")
    a("    /// `(load width signed? addr)` — `signed?` is `1` for sign extension, `0` for")
    a("    /// zero extension (D-LOAD-EXT).")
    a("    Load(&'static Sem, &'static Sem, &'static Sem),")
    a("    /// `(store width addr value)` — the low `width` bits of `value`.")
    a("    Store(&'static Sem, &'static Sem, &'static Sem),")
    a("    /// `(set (reg rd) value)` — write a register.")
    a("    Set(&'static Sem, &'static Sem),")
    a("    /// `(set-pc target)` — a control transfer.")
    a("    SetPc(&'static Sem),")
    a("    /// `(seq a b …)` — effects in order.")
    a("    Seq(&'static [&'static Sem]),")
    a("    /// `(nop)` — no observable effect (D-FENCE's rule for this profile).")
    a("    Nop,")
    a("    /// `(if cond then else)` — a semantic branch.")
    a("    If(&'static Sem, &'static Sem, &'static Sem),")
    a("    /// `(trap cause tval)` — a requested trap (D-ECALL-EBREAK).")
    a("    Trap(&'static Sem, &'static Sem),")
    if extended:
        # P4-SYSTEM.2 slice b's operator surface — the rv64gc module only. Evaluation is
        # the interpreter's (the slice-d scratch proof; the tracked exec.rs arms land at
        # the flip), per the operators' contracts in `schema/semantics.sexp`.
        a("    /// `(field NAME)` — the RAW numeric value of an operand field (a register")
        a("    /// index, a csr address, a zimm5), not the register the field names.")
        a("    Field(&'static str),")
        a("    /// `(inst)` — the instruction word (illegal-instruction xtval carries it).")
        a("    Inst,")
        a("    /// `(mode)` — the current privilege mode (0=U, 1=S, 3=M).")
        a("    Mode,")
        a("    /// `(csr-state a)` — the machine's own read of CSR state (no permission model).")
        a("    CsrState(&'static Sem),")
        a("    /// `(csr-read a)` — an architectural CSR read under the uniform permission model.")
        a("    CsrRead(&'static Sem),")
        a("    /// `(csr-write a v)` — an architectural CSR write, legalized per the state")
        a("    /// document's declared per-field tables.")
        a("    CsrWrite(&'static Sem, &'static Sem),")
        a("    /// `(csr-rw a v)` — the atomic CSR read-write: both judged first, v written,")
        a("    /// the OLD value yielded; a refusal delivers cause 2 before any effect.")
        a("    CsrRw(&'static Sem, &'static Sem),")
        a("    /// `(trap-deliver cause tval)` — synchronous trap delivery: delegation,")
        a("    /// the xPIE/xIE/xPP stack, xepc/xcause/xtval, pc <- xtvec.")
        a("    TrapDeliver(&'static Sem, &'static Sem),")
        a("    /// `(xret x)` — the privilege-stack pop and pc <- xepc.")
        a("    Xret(&'static Sem),")
        a("    /// `(tlb-invalidate va asid all-va? all-asid?)` — scope follows x0 register")
        a("    /// identity, retaining page/ASID zero selections (RVP-SUPERVISOR §11.1.2.1).")
        a("    TlbInvalidate(&'static Sem, &'static Sem, &'static Sem, &'static Sem),")
    if extended and data["a_variants"]:
        # P4-SYSTEM.4 slice b's A-operator surface — emitted exactly when the composition
        # composes `riscv/a` (the atomic bind, slice e): the evaluator's exhaustive match
        # learns the arms in the same commit, so a module never carries a variant nothing
        # can evaluate (the tracked module keeps its byte surface until then).
        a("    /// `(load-reserved width signed? addr)` — LR's load: translates under the")
        a("    /// load rules, sets/replaces the hart's reservation (physical address,")
        a("    /// width, valid), yields the loaded value (RVI-A §12.1.2).")
        a("    LoadReserved(&'static Sem, &'static Sem, &'static Sem),")
        a("    /// `(store-conditional width addr value)` — SC: success (reservation valid")
        a("    /// ∧ physical address ∧ width match) writes and yields 0; failure writes")
        a("    /// nothing and yields 1; the reservation is cleared either way (the")
        a("    /// deterministic policy, P4-SYSTEM.4 decision 3).")
        a("    StoreConditional(&'static Sem, &'static Sem, &'static Sem),")
        a("    /// `(amo op width addr value)` — one of the closed Zaamo nine (op the")
        a("    /// funct5 encoding): one store/AMO-rules translation, the old value read,")
        a("    /// op applied at width, the result written, the old value yielded —")
        a("    /// never a seq(load, op, store) (P4-SYSTEM.4 decision 5).")
        a("    Amo(u64, &'static Sem, &'static Sem, &'static Sem),")
    if extended and data["f_variants"]:
        # P4-SYSTEM.7 slice c3's floating-point surface — emitted exactly when the
        # composition composes `riscv/f` (the F bind, slice c6). The contracts are
        # `schema/semantics.sexp`'s floating-point block; the arithmetic is the model
        # layer's (`fp.rs`), never the backend's directly.
        a("    /// `(freg NAME)` — the f-register the operand field names: the raw FLEN = 64")
        a("    /// bits of the pre-instruction file; as a `set` target, a write that marks FS Dirty.")
        a("    FReg(&'static str),")
        a("    /// `(rounding rm)` — the effective rounding mode (0..4); DYN resolves to frm;")
        a("    /// a reserved mode raises illegal-instruction (cause 2).")
        a("    Rounding(&'static Sem),")
        a("    /// `(fbox n v)` — v's low n bits NaN-boxed into FLEN (all 1s above).")
        a("    FBox(u8, &'static Sem),")
        a("    /// `(funbox n v)` — the n-bit operand of an FLEN value: its low n bits when")
        a("    /// properly NaN-boxed, else the n-bit canonical NaN.")
        a("    FUnbox(u8, &'static Sem),")
        a("    /// `(fclass n a)` — the 10-bit class mask; raises no flag.")
        a("    FClass(u8, &'static Sem),")
        for rust in ("FMin", "FMax"):
            a(f"    /// `({rust[1:].lower()} n a b)` — minimumNumber/maximumNumber as RVI-F")
            a("    /// §20.1.6 amends them (−0 < +0; NaN rules; NV on a signaling input).")
            a(f"    {rust}(u8, &'static Sem, &'static Sem),")
        for rust, what in (("FEq", "a = b, quiet"), ("FLt", "a < b, signaling"),
                           ("FLe", "a ≤ b, signaling")):
            a(f"    /// `({rust[1:].lower()} n a b)` — 1 if {what}; 0 if either is NaN.")
            a(f"    {rust}(u8, &'static Sem, &'static Sem),")
        a("    /// `(fsqrt n rm a)` — √a, rounded; flags accrued.")
        a("    FSqrt(u8, &'static Sem, &'static Sem),")
        for rust, what in (("FAdd", "a+b"), ("FSub", "a-b"), ("FMul", "a×b"), ("FDiv", "a÷b")):
            a(f"    /// `({rust[1:].lower()} n rm a b)` — {what}, rounded; flags accrued.")
            a(f"    {rust}(u8, &'static Sem, &'static Sem, &'static Sem),")
        a("    /// `(fmadd n rm a b c)` — (a×b)+c with one rounding; ∞×0 raises NV.")
        a("    FMadd(u8, &'static Sem, &'static Sem, &'static Sem, &'static Sem),")
        a("    /// `(f2i n iw signed rm a)` — float to an iw-bit integer, clipped with NV.")
        a("    FToI(u8, u8, bool, &'static Sem, &'static Sem),")
        a("    /// `(i2f n iw signed rm v)` — v's low iw bits to an n-bit float, rounded.")
        a("    IToF(u8, u8, bool, &'static Sem, &'static Sem),")
    if extended and data["d_variants"]:
        # P4-SYSTEM.7 slice d2's one D operator — emitted exactly when the composition
        # composes `riscv/d` (the D bind, slice d5).
        a("    /// `(f2f m n rm a)` — an n-bit float to an m-bit float: narrowing rounds,")
        a("    /// widening is exact; a signaling NaN raises NV, any NaN yields the canonical NaN.")
        a("    FToF(u8, u8, &'static Sem, &'static Sem),")
    if extended and data["m_variants"]:
        # P4-SYSTEM.11 slice a's M operators — emitted exactly when the composition composes
        # `riscv/m` (the M bind, slice b). Width-generic: each works at its operands' width.
        for rust, what in (("Mul", "the low w bits of a×b"),
                           ("MulH", "the high w bits of the 2w-bit a×b, signed×signed"),
                           ("MulHsu", "the high w bits of the 2w-bit a×b, signed×unsigned"),
                           ("MulHu", "the high w bits of the 2w-bit a×b, unsigned×unsigned"),
                           ("Div", "a÷b signed, truncating; overflow wraps; b ≠ 0 (guarded)"),
                           ("DivU", "a÷b unsigned; b ≠ 0 (guarded)"),
                           ("Rem", "the signed remainder, the dividend's sign; b ≠ 0 (guarded)"),
                           ("RemU", "the unsigned remainder; b ≠ 0 (guarded)")):
            a(f"    /// `({rust.lower()} a b)` — {what}.")
            a(f"    {rust}(&'static Sem, &'static Sem),")
    a("}")
    a("")
    a("/// Decode an instruction's bits to its definition by fixed-bit specificity: the first"
      if compressed else
      "/// Decode a 32-bit word to its instruction definition by the fixed bits: the first")
    a(f"/// entry whose `mask`ed bits equal its `value`. Linear over the {len(ordered)}")
    a("/// entries — no allocation, and no failure family of its own: a word no entry")
    a("/// matches is the reserved-decode case (`outcome::UndefinedCase::ReservedDecode`,")
    a("/// REQ-D-RESERVED-DECODE), and that classification is the caller's, not this")
    a("/// table's. Operand extraction and evaluation land with the interpreter slice")
    a("/// (`P1-LAB.8`).")
    a("#[must_use]")
    a("pub fn decode(word: u32) -> Option<&'static InsnDef> {")
    a("    INSNS.iter().find(|insn| word & insn.mask == insn.value)")
    a("}")
    a("")
    if data["pseudos"]:
        a("/// One pseudo-instruction of the composition (Zicntr's counter reads): an")
        a("/// assembler spelling whose encoding SPECIALIZES a real instruction's — it adds")
        a("/// nothing to the decode space (check_encoding_disjoint's specialization rule),")
        a("/// so it never appears in INSNS; the row exists so the coverage census maps the")
        a("/// architectural spelling to the realizing instruction (P4-SYSTEM.2 slice f).")
        a("pub struct PseudoDef {")
        a("    pub name: &'static str,")
        a("    /// The realizing instruction (the pinned table's `of` base).")
        a("    pub of: &'static str,")
        a("    pub mask: u32,")
        a("    pub value: u32,")
        a("    pub operands: &'static [&'static str],")
        a("    /// The specification locator the pseudo's semantics rule cites.")
        a("    pub source: &'static str,")
        a("}")
        a("")
        a(f"/// The {len(data['pseudos'])} pseudo-instructions, sorted by name.")
        a("pub static PSEUDOS: &[PseudoDef] = &[")
        for name in sorted(data["pseudos"]):
            p = data["pseudos"][name]
            mask, value = fixed_mask(name, p.fixed)
            ops = ", ".join(rust_str(o) for o in p.operands)
            source = data["pseudo_rules"].get(name, "")
            a("    PseudoDef {")
            a(f"        name: {rust_str(name)},")
            a(f"        of: {rust_str(p.of)},")
            a(f"        mask: 0x{mask:08x},")
            a(f"        value: 0x{value:08x},")
            a(f"        operands: &[{ops}],")
            a(f"        source: {rust_str(source)},")
            a("    },")
        a("];")
        a("")
    if not extended:
        a("#[cfg(test)]")
        a("mod tests;")
        a("")
    return "\n".join(w)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--encoding", type=Path, default=ENCODING)
    ap.add_argument("--state", type=Path, default=STATE)
    ap.add_argument("--out", type=Path, default=OUT)
    ap.add_argument("--check", action="store_true",
                    help="exit 0 iff the committed module already matches regeneration")
    args = ap.parse_args(argv)

    try:
        data = load_inputs(args.encoding, args.state)
        text = emit(data, sha256(Path(__file__).resolve()))
    except (Refusal, R.AsmError, X.SexpError) as exc:
        print(f"gen_definition: REFUSED — {exc}", file=sys.stderr)
        return 2

    if args.check:
        committed = args.out.read_text(encoding="utf-8") if args.out.exists() else ""
        if committed == text:
            return 0
        diff = "\n".join(difflib.unified_diff(
            committed.splitlines(), text.splitlines(),
            fromfile=str(args.out), tofile=f"{args.out} (regenerated)", n=2))
        print(f"gen_definition: DRIFT — {args.out} no longer matches the canonical "
              f"definition:\n{diff}\n"
              f"Regenerate — never edit: python3 scripts/gen_definition.py", file=sys.stderr)
        return 1

    args.out.write_text(text, encoding="utf-8")
    print(f"gen_definition: wrote {args.out} ({len(text)} bytes)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
