#!/usr/bin/env python3
"""Check a semantics fragment: every form known, every instruction covered, every rule cited.

⛔ THE LANGUAGE IS DELIBERATELY TINY, and the checker REFUSES anything outside it. A semantics
notation that quietly accepts an unknown operator produces a definition whose meaning nobody can
state — which is worse than no definition, because it looks like one. Every form was added
because an RV64I instruction needed it; none was added in anticipation.

⭐ THE LANGUAGE IS DATA, NOT CODE. The form table — the 32 operators and their arity — lives
as `(operator …)` declarations in `schema/semantics.sexp` (SOT-FORMAT.2) and is loaded below
through the schema kernel; adding a semantic form is a schema edit, zero lines of Python. This
file owns what the schema cannot state: whether a bare symbol is an operand the instruction
actually has (the encoding provides the operands — a cross-file fact), whether every declared
instruction is covered, and whether every rule cites the specification locator it was derived
from.

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
import sexp as _sexp                        # noqa: E402
import check_sexp_schema as _schema         # noqa: E402

REPO = Path(__file__).resolve().parent.parent
LANGUAGE = REPO / "schema" / "semantics.sexp"

# The operator table, loaded from schema/semantics.sexp by load_language(): head -> arity,
# where `None` means variadic (at least one argument), exactly the mapping this walk implements.
FORMS: dict[str, int | None] = {}

# Operand names an instruction may reference come from its encoding, plus these implicit ones.
IMPLICIT = {"pc", "xlen"}


def load_language() -> None:
    """The semantic language, AS DATA: `(operator …)` declarations in schema/semantics.sexp.

    A variadic operator with a minimum other than 1 has no faithful mapping here (this walk
    states "at least one") — refused loudly rather than silently approximated.
    """
    try:
        _, operators = _schema.load_schema(LANGUAGE)
    except (_schema.SchemaError, _sexp.SexpError) as exc:
        raise SemError(f"the semantic language itself does not read: {exc}")
    forms: dict[str, int | None] = {}
    for name, op in operators.items():
        if op.fixed is not None:
            forms[name] = op.fixed
        elif op.min == 1:
            forms[name] = None
        else:
            raise SemError(f"({name} …) is variadic with min {op.min}, which this checker "
                           f"cannot state — the language admits only fixed arities or "
                           f"\"at least one\"")
    FORMS.clear()
    FORMS.update(forms)


class SemError(Exception):
    """A refusal."""


def check_expr(form, where: str, allowed: set[str] | None) -> None:
    if isinstance(form, int):
        return
    if isinstance(form, str):
        # `allowed is None` is the compose mode: operand scoping is a cross-file fact (the
        # encoding provides the operands), and compose mode has no encoding — arity still bites
        if allowed is not None and form not in allowed and form not in IMPLICIT:
            raise SemError(f"{where}: {form!r} is not an operand this instruction has "
                           f"(it provides {sorted(allowed)}) nor an implicit value")
        return
    if not isinstance(form, list) or not form:
        raise SemError(f"{where}: empty form")
    op = str(form[0])
    if op not in FORMS:
        raise SemError(f"{where}: unknown form {op!r}. The language is deliberately small and this "
                       f"checker refuses what it cannot state the meaning of — declare the form "
                       f"with its arity in schema/semantics.sexp, or express the rule with the "
                       f"forms that exist")
    arity = FORMS[op]
    args = form[1:]
    if arity is None:
        if not args:
            raise SemError(f"{where}: ({op} …) needs at least one argument")
    elif len(args) != arity:
        raise SemError(f"{where}: ({op} …) takes {arity} argument(s), got {len(args)}")
    for a in args:
        check_expr(a, where, allowed)


def _schema_validate_sem_file(path: Path) -> None:
    """Refuse, by name, a sem file the schema layer refuses — before the refinement rule runs.

    `MODEL-COMPOSE.6`: before this, a sem file was checked against the language only when
    someone ran the per-fragment mode by hand; the corpus is schema-validated here, in the mode
    the gate calls.
    """
    try:
        constructs, operators = _schema.load_schema(LANGUAGE)
        errors = _schema.validate_file(path, constructs, operators)
    except (_schema.SchemaError, _sexp.SexpError) as exc:
        raise SemError(f"the semantics schema itself does not read: {exc}")
    if errors:
        raise SemError(f"refused by schema/semantics.sexp — " + "; ".join(errors))


def compose(paths: list[Path]) -> int:
    """MODEL-COMPOSE.6 — decide the refinement rule over sem files in COMPOSITION ORDER.

    A name defined in file j that an earlier file already defines is an override, legal iff
    file j declares `(refines "name")`. Both lies are refused too: a refinement declaration
    naming nothing the file defines (REFINES WITHOUT OVERRIDE), and one naming nothing any
    earlier file defines (REFINES NOTHING). A silent override is the defect this rule exists
    to refuse: an extension that changes a base behaviour — CSRs changing trap handling, C
    changing IALIGN — must say so, or the composition is not sound even when every fragment
    is well-formed alone.
    """
    try:
        load_language()
    except SemError as exc:
        print(f"REFUSED: {exc}", file=sys.stderr)
        return 2
    files: list[tuple[Path, list[str], set[str]]] = []
    errors: list[str] = []
    for p in paths:
        try:
            load_ok = True
            _schema_validate_sem_file(p)
            root = _sexp.read_file(p)[0]
            if _sexp.head(root, str(p)) != "semantics":
                raise SemError(f"expected a (semantics …) document, got "
                               f"({_sexp.head(root, str(p))} …)")
        except SemError as exc:
            # a file the layer refuses is a REJECTION of the corpus (rc=1), not a refusal to
            # judge (rc=2) — only a broken language earns rc=2
            errors.append(f"{p.name}: {exc}")
            continue
        except _sexp.SexpError as exc:
            errors.append(f"{p.name}: does not parse — {exc}")
            continue
        defined: list[str] = []
        for s in _sexp.children(root, "sem"):
            name = str(_sexp.field(s, "insn", str(p)))
            where = f"{p.name} [{name}]"
            if name in defined:
                errors.append(f"{where}: defined twice")
            defined.append(name)
            for e in _sexp.children(s, "effect"):
                try:
                    for sub in e[1:]:
                        check_expr(sub, where, None)
                except SemError as exc:
                    errors.append(str(exc))
        refined = {str(_sexp.field(r, "insn", str(p))) for r in _sexp.children(root, "refines")}
        files.append((p, defined, refined))

    seen: dict[str, Path] = {}
    for p, defined, refined in files:
        names = set(defined)
        for r in sorted(refined - names):
            errors.append(f"{p.name}: declares (refines \"{r}\") but defines no semantics for "
                          f"'{r}' — a declaration with no override is a lie about what this file does")
        for r in sorted(refined & names):
            if r not in seen:
                errors.append(f"{p.name}: declares (refines \"{r}\") but no earlier fragment in "
                              f"this composition defines '{r}' — refining nothing")
        for name in defined:
            if name in seen and name not in refined:
                errors.append(f"{p.name} [{name}]: SILENT REDEFINITION — '{name}' is already "
                              f"defined in {seen[name].name}, and this file declares no "
                              f"(refines (insn \"{name}\")). An extension that changes a base behaviour "
                              f"must declare the refinement point (MODEL-COMPOSE.6)")
        for name in defined:
            seen[name] = p

    for e in errors:
        print(f"  {e}")
    if errors:
        print("\n  REJECTED — the semantics do not compose.")
        return 1
    for p, _, refined in files:
        if refined:
            print(f"  {p.name} declares refinement point(s): {', '.join(sorted(refined))}")
    print("\n  the semantics compose — every override is declared.")
    return 0


def main(argv: list[str]) -> int:
    if len(argv) == 2 and argv[1] == "--self-test":
        return _selftest()
    if len(argv) >= 3 and argv[1] == "--compose":
        return compose([Path(a) for a in argv[2:]])
    if len(argv) != 3:
        print("usage: check_semantics.py <fragment.sexp> <semantics.sexp>\n"
              "       check_semantics.py --compose <base.sem> <ext.sem>…   (composition order)\n"
              "       check_semantics.py --self-test", file=sys.stderr)
        return 2
    try:
        load_language()
    except SemError as exc:
        print(f"REFUSED: {exc}", file=sys.stderr)
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


# --------------------------------------------------------------------------- self-test

def _selftest() -> int:
    passed = failed = 0

    def arm(label: str, fn) -> None:
        nonlocal passed, failed
        try:
            fn()
        except AssertionError as exc:
            print(f"  FAIL  {label}: {exc}"); failed += 1
        except Exception as exc:                       # noqa: BLE001 — an arm must not abort
            print(f"  FAIL  {label}: unexpected {type(exc).__name__}: {exc}"); failed += 1
        else:
            print(f"  ok    {label}"); passed += 1

    root = Path("target/doctrine-selftest")
    root.mkdir(parents=True, exist_ok=True)
    tmp = Path(__import__("tempfile").mkdtemp(dir=root))

    def sem_file(name, insns, refines=()):
        """insns: {name: effect-sexp-string}; refines: iterable of insn-name strings."""
        body = "".join(
            f'(sem (insn {i}) (source "SRC §1 — why") (effect {fx}))\n'
            for i, fx in insns.items())
        refs = "".join(f'(refines (insn "{r}"))\n' for r in refines)
        p = tmp / name
        p.write_text(f'(semantics (fragment "riscv/t") (xlen 64)\n{refs}{body})')
        return p

    NOP = "(nop)"
    SET = "(set (reg rd) (add (reg rs1) (reg rs2)))"

    def composes(files, needle):
        import io, contextlib
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            rc = compose(files)
        assert rc == 0, f"rc={rc}: {buf.getvalue()}"
        assert needle in buf.getvalue(), f"no {needle!r} in:\n{buf.getvalue()}"
        return buf.getvalue()

    def refuses(files, needle):
        import io, contextlib
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            rc = compose(files)
        assert rc == 1, f"expected rc=1 got {rc}: {buf.getvalue()}"
        assert needle in buf.getvalue(), f"no {needle!r} in:\n{buf.getvalue()}"

    base = sem_file("base.sem.sexp", {"add": SET, "ecall": NOP})
    arm("GREEN one file composes, nothing overridden",
        lambda: composes([base], "the semantics compose"))

    ext = sem_file("ext.sem.sexp", {"mul": SET}, refines=("ecall",))
    # redefine ecall AND declare it
    ext.write_text('(semantics (fragment "riscv/t-ext") (xlen 64)\n'
                   '(refines (insn "ecall"))\n'
                   '(sem (insn mul) (source "SRC §2 — why") (effect ' + SET + '))\n'
                   '(sem (insn ecall) (source "SRC §3 — why") (effect ' + NOP + '))\n)')
    arm("GREEN a declared refinement is accepted, and reported",
        lambda: composes([base, ext], "declares refinement point(s): ecall"))

    silent = sem_file("silent.sem.sexp", {"add": NOP})
    arm("RED   the acceptance's shape: a silent override is refused by name",
        lambda: refuses([base, silent], "SILENT REDEFINITION"))

    lie_override = sem_file("lie1.sem.sexp", {"mul": SET}, refines=("ecall",))
    arm("RED   a declaration with no override behind it",
        lambda: refuses([base, lie_override], "defines no semantics for"))

    lie_nothing = sem_file("lie2.sem.sexp", {"mul": SET}, refines=("mul",))
    arm("RED   refining nothing — no earlier file defines it",
        lambda: refuses([base, lie_nothing], "no earlier fragment in"))

    dup = sem_file("dup.sem.sexp", {"add": SET, "sub": NOP})
    dup.write_text('(semantics (fragment "riscv/t") (xlen 64)\n'
                   f'(sem (insn add) (source "S §1") (effect {NOP}))\n'
                   f'(sem (insn add) (source "S §1") (effect {NOP}))\n)')
    arm("RED   a name defined twice in one file",
        lambda: refuses([dup], "defined twice"))

    bad = sem_file("bad.sem.sexp", {"add": "(set (reg rd))"})
    arm("RED   a wrong arity inside a known head — the schema states heads, the walk states arity",
        lambda: refuses([bad], "takes 2 argument(s)"))

    schema_bad = tmp / "schemabad.sem.sexp"
    schema_bad.write_text('(semantics (fragment "riscv/t") (xlen 64) (gizmo "x"))')
    arm("RED   a construct the schema layer refuses, by name",
        lambda: refuses([schema_bad], 'undeclared field "gizmo"'))

    import shutil
    shutil.rmtree(tmp)
    print(f"check_semantics --self-test: {passed} pass / {failed} fail")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
