#!/usr/bin/env python3
"""Check a semantics fragment: every form known, every instruction covered, every rule cited.

⛔ THE LANGUAGE IS DELIBERATELY TINY, and the checker REFUSES anything outside it. A semantics
notation that quietly accepts an unknown operator produces a definition whose meaning nobody can
state — which is worse than no definition, because it looks like one. Every form below was added
because an RV64I instruction needed it; none was added in anticipation.

⚠️ WHAT THIS CHECKS AND WHAT IT DOES NOT. It checks that the semantics are *well-formed, complete
and cited*: every declared instruction has an effect, every form is known, every operand it names
is one the encoding actually provides, and every rule carries the specification locator it was
derived from. It does **not** check that the semantics are *correct* — that is what a differential
experiment against a reference model is for, and why `P0-PROFILE.6` exists. A green result here
means the definition says something checkable, not that what it says is true.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import sexp as _sexp  # noqa: E402

# Every operator, with its arity. Arity `None` means variadic (at least one argument).
FORMS: dict[str, int | None] = {
    # values
    "reg": 1, "pc": 0, "imm": 1, "lit": 1,
    # integer arithmetic and logic, all on XLEN-wide two's-complement values
    "add": 2, "sub": 2, "and": 2, "or": 2, "xor": 2,
    "shl": 2, "shr": 2, "sar": 2,          # shr logical, sar arithmetic
    "slt": 2, "sltu": 2,                    # set-less-than, signed and unsigned
    "eq": 2, "ne": 2, "lt": 2, "ltu": 2, "ge": 2, "geu": 2,
    # width manipulation — explicit, because implicit width is where models diverge
    "trunc": 2, "sext": 2, "zext": 2,
    "bits": 3,                              # (bits hi lo v)
    # memory
    "load": 3,                              # (load width signed? addr)
    "store": 3,                             # (store width addr value)
    # effects
    "set": 2, "set-pc": 1, "seq": None, "nop": 0, "if": 3,
    "trap": 2,                              # (trap cause tval)
}
# Operand names an instruction may reference come from its encoding, plus these implicit ones.
IMPLICIT = {"pc", "xlen"}


class SemError(Exception):
    """A refusal."""


def check_expr(form, where: str, allowed: set[str]) -> None:
    if isinstance(form, int):
        return
    if isinstance(form, str):
        if form not in allowed and form not in IMPLICIT:
            raise SemError(f"{where}: {form!r} is not an operand this instruction has "
                           f"(it provides {sorted(allowed)}) nor an implicit value")
        return
    if not isinstance(form, list) or not form:
        raise SemError(f"{where}: empty form")
    op = str(form[0])
    if op not in FORMS:
        raise SemError(f"{where}: unknown form {op!r}. The language is deliberately small and this "
                       f"checker refuses what it cannot state the meaning of — add the form to "
                       f"FORMS with its arity, or express the rule with the forms that exist")
    arity = FORMS[op]
    args = form[1:]
    if arity is None:
        if not args:
            raise SemError(f"{where}: ({op} …) needs at least one argument")
    elif len(args) != arity:
        raise SemError(f"{where}: ({op} …) takes {arity} argument(s), got {len(args)}")
    for a in args:
        check_expr(a, where, allowed)


def main(argv: list[str]) -> int:
    if len(argv) != 3:
        print("usage: check_semantics.py <fragment.sexp> <semantics.sexp>", file=sys.stderr)
        return 2
    enc_path, sem_path = Path(argv[1]), Path(argv[2])
    try:
        enc = _sexp.read_file(enc_path)[0]
        sem = _sexp.read_file(sem_path)[0]
    except _sexp.SexpError as exc:
        print(f"REFUSED: {exc}", file=sys.stderr)
        return 2

    operands: dict[str, set[str]] = {}
    for i in _sexp.children(enc, "insn"):
        name = str(_sexp.field(i, "name"))
        ops = {str(o) for o in _sexp.children(i, "operands")[0][1:]}
        # a split store immediate is written as one operand in the semantics
        if "imm12hi" in ops:
            ops = (ops - {"imm12hi", "imm12lo"}) | {"imm12"}
        if "bimm12hi" in ops:
            ops = (ops - {"bimm12hi", "bimm12lo"}) | {"bimm12"}
        operands[name] = ops | {"shamt"} if ("shamtd" in ops or "shamtw" in ops) else ops

    errors: list[str] = []
    covered: set[str] = set()
    for s in _sexp.children(sem, "sem"):
        name = str(_sexp.field(s, "insn", str(sem_path)))
        where = f"{sem_path.name} [{name}]"
        if name not in operands:
            errors.append(f"{where}: no instruction of that name in {enc_path.name}")
            continue
        if name in covered:
            errors.append(f"{where}: defined twice")
        covered.add(name)
        if not _sexp.children(s, "source"):
            errors.append(f"{where}: cites no specification locator. A semantic rule with no "
                          f"source is a rule nobody can check against the document it came from")
        effects = _sexp.children(s, "effect")
        if not effects:
            errors.append(f"{where}: has no (effect …)")
        for e in effects:
            try:
                for sub in e[1:]:
                    check_expr(sub, where, operands[name])
            except SemError as exc:
                errors.append(str(exc))

    missing = sorted(set(operands) - covered)
    if missing:
        errors.append(f"{len(missing)} declared instruction(s) have NO semantics: "
                      f"{', '.join(missing[:12])}{' …' if len(missing) > 12 else ''}")

    for e in errors:
        print(f"  {e}")
    print(f"\n  {len(covered)} of {len(operands)} declared instruction(s) have checked semantics")
    if errors:
        print("  REJECTED — the definition is not yet something an engine could consume.")
        return 1
    print("  ⚠️ Well-formed, complete and cited. NOT verified correct — that is what a differential")
    print("  experiment against a reference model is for.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
