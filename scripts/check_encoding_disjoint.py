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

A UNIT'S COMPOSITION is checked through the same engine (`MODEL-COMPOSE.4`): a unit's
`encoding.sexp` is schema-validated against `schema/encoding.sexp` before it is read (an
undeclared field is refused by name, never silently skipped), its `compose` form is resolved
through the ONE shared resolver (`riscv_asm.resolve_composition` — missing fragments and unmet
`requires` refused exactly as the assembler refuses them), and the resolved union is decided
here. Slots make a composition PARTIAL: `(status partial)` plus `(slot (id …) (requires …))`
declares an unbound hole and what it must eventually provide; the bound parts are decided as
usual and the composition is reported partial. Partial is DECLARED, never inferred from silence:
slots without `(status partial)` claim completeness while unbound (refused), and `(status
partial)` with no slots declares a hole that is not there (refused). A slot's `requires` name
fragments that need not exist yet — requiring a part that does not exist is the point of a slot.

Two instructions collide when their fixed bits are compatible on every bit both constrain:

    overlap  ⇔  (value_a ^ value_b) & mask_a & mask_b == 0

Usage:  check_encoding_disjoint.py <fragment.sexp | unit encoding.sexp | opcodes-dir> [more…]
        check_encoding_disjoint.py --self-test
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import sexp as _sexp                          # noqa: E402

REPO_ROOT = Path(__file__).resolve().parent.parent
SCHEMA_FOR = {
    "encoding": REPO_ROOT / "schema" / "encoding.sexp",
    "fragment": REPO_ROOT / "schema" / "fragment.sexp",
}


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


class CompositionError(Exception):
    """A refusal: the composition document is not well-formed enough to judge."""


def _schema_validate(path: Path, family: str) -> None:
    """Refuse, by name, a document the schema layer refuses — before any consumer reads it."""
    import check_sexp_schema as K
    schema = SCHEMA_FOR[family]
    try:
        constructs, operators = K.load_schema(schema)
        errors = K.validate_file(path, constructs, operators)
    except (K.SchemaError, _sexp.SexpError) as exc:
        raise CompositionError(f"{path}: the {family} schema itself cannot be read — {exc}")
    if errors:
        raise CompositionError(
            f"{path}: refused by schema/{family}.sexp — " + "; ".join(errors))


def composition_slots(enc) -> tuple[str, list[tuple[str, list[str]]]]:
    """The (status, slots) a compose form declares. Status defaults to a completeness claim."""
    comp = _sexp.children(enc, "compose")
    if not comp:
        return "complete", []
    status_found = _sexp.children(comp[0], "status")
    status = str(status_found[0][1]) if status_found else "complete"
    slots = []
    for s in _sexp.children(comp[0], "slot"):
        requires: list[str] = []
        for r in _sexp.children(s, "requires"):
            requires += [str(x) for x in r[1:]]
        slots.append((str(_sexp.field(s, "id")), requires))
    return status, slots


def check_slot_rules(path: Path, enc) -> list[tuple[str, list[str]]]:
    """MODEL-COMPOSE.4: partial is declared, never inferred from silence — both directions."""
    status, slots = composition_slots(enc)
    if slots and status != "partial":
        raise CompositionError(
            f"{path}: {len(slots)} slot(s) unbound but no (status partial) — a composition "
            f"claiming completeness while a hole is open. Declare partial, or bind the slot.")
    if status == "partial" and not slots:
        raise CompositionError(
            f"{path}: declares (status partial) but binds every part — a hole is declared "
            f"that is not there. Partial is declared, never claimed for nothing.")
    return slots


def load_fragment(path: Path) -> tuple[list[Insn], list[Insn]]:
    """Read a fragment: a unit `encoding.sexp`, a bare `fragment.sexp`, or an opcodes table.

    Returns (instructions, pseudo-instructions). A `(pseudo …)` is an assembler spelling,
    NOT an encoding (schema/fragment.sexp): it never joins the instruction set the
    collision rule judges — it is decided under the specialization rule in main(). An
    opcodes table yields instructions only (its `$pseudo_op` rows are skipped, exactly as
    the assembler's table route skips them).
    """
    if path.suffix == ".sexp":
        forms = _sexp.read_file(path)
        if len(forms) != 1:
            raise CompositionError(f"{path}: expected exactly one top-level form")
        root = forms[0]
        head = _sexp.head(root, str(path))
        if head == "encoding":
            _schema_validate(path, "encoding")
            import riscv_asm
            try:
                resolved = riscv_asm.resolve_composition(root, path)
            except riscv_asm.AsmError as exc:
                raise CompositionError(str(exc))
            root, head = resolved, "fragment"
        if head == "fragment":
            if path.name != "encoding.sexp":            # unit docs were validated above
                _schema_validate(path, "fragment")
            insns, pseudos = [], []
            for i in _sexp.children(root, "insn"):
                fixed = [(int(a), int(b), int(c)) for a, b, c in _sexp.children(i, "fixed")[0][1:]]
                insns.append(Insn(str(_sexp.field(i, "name")), fixed, path.name))
            for p in _sexp.children(root, "pseudo"):
                fixed = [(int(a), int(b), int(c)) for a, b, c in _sexp.children(p, "fixed")[0][1:]]
                pseudos.append(Insn(str(_sexp.field(p, "name")), fixed, path.name))
            return insns, pseudos
        raise CompositionError(
            f"{path}: expected an (encoding …) unit document or a (fragment …) — got "
            f"({head} …)")
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
    return out, []


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


def load_specializations(path: Path) -> list[tuple[str, str]]:
    """The (special, general) pairs a fragment — or a unit's resolved composition — DECLARES
    (`(specializes …)`, schema/fragment.sexp; P4-SYSTEM.12 slice a). An opcodes table
    declares none."""
    if path.suffix != ".sexp":
        return []
    root = _sexp.read_file(path)[0]
    if _sexp.head(root, str(path)) == "encoding":
        import riscv_asm
        try:
            root = riscv_asm.resolve_composition(root, path)
        except riscv_asm.AsmError as exc:
            raise CompositionError(str(exc))
    return [(str(_sexp.field(s, "special", str(path))), str(_sexp.field(s, "general", str(path))))
            for s in _sexp.children(root, "specializes")]


def judge_overlaps(insns: list[Insn], specs: list[tuple[str, str]]):
    """(undeclared collisions, accepted specializations, declaration problems).

    An overlap is legal exactly when it is DECLARED and IS a strict specialization: the special
    row's fixed bits a strict superset of the general row's, the two agreeing where the general
    row constrains — so every word of the special row is also a word of the general one, and a
    decoder that tries the special row first is unambiguous. A declaration naming a row the
    composition lacks, or a pair that is not such a specialization, is itself refused: a
    declaration must not be a way to silence a collision."""
    by = {i.name: i for i in insns}
    problems, accepted = [], set()
    for special, general in specs:
        s, g = by.get(special), by.get(general)
        if s is None or g is None:
            problems.append(f"specialization {special} ⊂ {general} names an instruction the "
                            f"composition does not carry")
            continue
        if g.mask & ~s.mask or not (s.mask & ~g.mask) or (s.value ^ g.value) & g.mask:
            problems.append(f"specialization {special} ⊂ {general} is declared, but {special}'s "
                            f"word set is not strictly inside {general}'s")
            continue
        accepted.add(frozenset((special, general)))
    bad = [(a, b) for a, b in collisions(insns) if frozenset((a.name, b.name)) not in accepted]
    return bad, sorted(tuple(sorted(x)) for x in accepted), problems


def pseudo_problems(insns: list[Insn], pseudos: list[Insn]) -> list[str]:
    """Decide the pseudo-instructions against the composed instruction set.

    A pseudo is legal exactly when every word it assembles is already a word of a composed
    instruction — it adds nothing to the encoding space. Two failures are named: a pseudo
    NO instruction realizes (it would silently EXTEND the space, which is an encoding
    sneaking in through the assembler door), and a pseudo overlapping an instruction it
    does not fully specialize (one word, two decode classes — the ambiguity the collision
    rule exists to refuse, one level down).
    """
    out = []
    for p in pseudos:
        realized = False
        for i in insns:
            common = p.mask & i.mask
            if (p.value ^ i.value) & common:
                continue                            # disjoint word sets: no relation
            if i.mask & ~p.mask:
                out.append(f"pseudo {p.name} ({p.origin}) overlaps {i.name} ({i.origin}) "
                           f"without specializing it — one word, two decode classes")
            else:
                realized = True                     # p's word set ⊆ i's word set
        if not realized:
            out.append(f"pseudo {p.name} ({p.origin}) is realized by NO composed instruction "
                       f"— it would extend the encoding space it is declared not to touch")
    return out


def main(argv: list[str]) -> int:
    if len(argv) == 2 and argv[1] == "--self-test":
        return _selftest()
    if len(argv) < 2:
        print("usage: check_encoding_disjoint.py <fragment…>", file=sys.stderr)
        return 2
    insns: list[Insn] = []
    pseudos: list[Insn] = []
    specs: list[tuple[str, str]] = []
    all_slots: list[tuple[str, list[str]]] = []
    try:
        for arg in argv[1:]:
            p = Path(arg)
            if not p.exists():
                print(f"REFUSED: {p} does not exist", file=sys.stderr)
                return 2
            if p.suffix == ".sexp":
                forms = _sexp.read_file(p)
                if len(forms) == 1 and _sexp.head(forms[0], str(p)) == "encoding":
                    all_slots += check_slot_rules(p, forms[0])
            part, part_pseudos = load_fragment(p)
            if not part and not part_pseudos:
                print(f"REFUSED: {p} yielded no instructions — an empty fragment is not a valid one",
                      file=sys.stderr)
                return 2
            print(f"  fragment {p.name:16} {len(part):3} instruction(s)"
                  + (f", {len(part_pseudos)} pseudo-instruction(s)" if part_pseudos else ""))
            insns += part
            pseudos += part_pseudos
            specs += load_specializations(p)
    except (CompositionError, _sexp.SexpError, ValueError) as exc:
        print(f"REFUSED: {exc}", file=sys.stderr)
        return 2

    names = [i.name for i in insns] + [p.name for p in pseudos]
    dupes = [n for n in set(names) if names.count(n) > 1]
    bad, accepted, spec_problems = judge_overlaps(insns, specs)
    problems = pseudo_problems(insns, pseudos) + spec_problems
    print(f"\n  composed set: {len(insns)} instruction(s)"
          + (f" (+ {len(pseudos)} pseudo-instruction(s))" if pseudos else "")
          + f" from {len(argv) - 1} fragment(s)")
    if accepted:
        print(f"  declared specializations: {len(accepted)} (the special row decodes first)")
    if dupes:
        print(f"  DUPLICATE NAME(S): {sorted(dupes)}")
    if bad:
        print(f"  COLLISIONS: {len(bad)}")
        for a, b in bad[:10]:
            print(f"    {a.name} ({a.origin}) overlaps {b.name} ({b.origin})  "
                  f"mask={a.mask & b.mask:#010x}")
    if problems:
        print(f"  PSEUDO PROBLEMS: {len(problems)}")
        for line in problems[:10]:
            print(f"    {line}")
    if bad or problems:
        print("\n  REJECTED — these fragments do not compose. A decoder cannot be generated from a")
        print("  set in which one word matches two instructions.")
        return 1
    if dupes:
        print("\n  REJECTED — duplicate instruction names in one composition.")
        return 1
    print("  no collisions, no duplicate names — the fragments COMPOSE.")
    print("  ⚠️ This decides the DECODER composes. It says nothing about whether the semantics do.")
    if all_slots:
        print(f"\n  PARTIAL — {len(all_slots)} slot(s) unbound:")
        for sid, requires in all_slots:
            req = ", ".join(requires) if requires else "nothing declared"
            print(f"    {sid} requires {req}")
        print("  the bound parts compose; the slot's requirements are checkable before its "
              "unit exists. Partial is declared, never inferred from silence.")
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
    defs = tmp / "definitions"
    unit_dir = tmp / "profiles" / "p"
    defs.mkdir(parents=True)
    unit_dir.mkdir(parents=True)

    def frag(name, frag_id, insns, requires=None):
        req = f' (requires "{requires}")' if requires else ""
        body = "".join(
            f'(insn (name "{n}") (fixed (31 25 0x0) (14 12 {f3}) (6 2 0x13) (1 0 0x3)))\n'
            for n, f3 in insns)
        p = defs / f"{frag_id}.sexp"          # resolution looks up root/<id>.sexp
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(f'(fragment (id "{frag_id}") (kind extension){req}\n{body})')
        return frag_id

    def raw_frag(frag_id, body):
        p = defs / f"{frag_id}.sexp"
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(f'(fragment (id "{frag_id}") (kind extension)\n{body})')
        return frag_id

    def enc_doc(base, exts, extra_compose=""):
        ext = "".join(f' (extensions "{e}")' for e in exts)
        doc = (f'(encoding (profile "p") (ilen 32)\n'
               f'  (compose (base "{base}"){ext}{extra_compose})\n'
               f'  (fragment-root "definitions"))\n')
        p = unit_dir / "encoding.sexp"
        p.write_text(doc)
        return p

    frag("base", "riscv/t-base", [("add", 0), ("sub", 1)])
    frag("ext", "riscv/t-ext", [("mul", 2)])
    frag("clash", "riscv/t-clash", [("add", 0)])
    frag("needy", "riscv/t-needy", [("div", 3)], requires="riscv/t-missing")

    # pseudo-instruction arms: a csr-like base instruction (funct3 2) and pseudo spellings
    # of it — the Zicntr/csrrs shape (P4-SYSTEM.2 slice a).
    raw_frag("riscv/t-csr",
             '(insn (name "csrish") (fixed (14 12 0x2) (6 2 0x13) (1 0 0x3)))\n')
    raw_frag("riscv/t-pseudo",
             '(pseudo (name "rdish") (of "t::csrish") '
             '(fixed (31 20 0x5) (19 15 0x0) (14 12 0x2) (6 2 0x13) (1 0 0x3)) '
             '(operands) (from "t"))\n')
    raw_frag("riscv/t-ghost-pseudo",
             '(pseudo (name "ghost") (of "t::csrish") '
             '(fixed (31 20 0x5) (19 15 0x0) (14 12 0x4) (6 2 0x13) (1 0 0x3)) '
             '(operands) (from "t"))\n')
    raw_frag("riscv/t-ambi-pseudo",
             '(pseudo (name "ambi") (of "t::csrish") '
             '(fixed (31 28 0x1) (14 12 0x2)) (operands) (from "t"))\n')
    frag("dupe", "riscv/t-dupe", [("add", 7)])

    import subprocess
    ok = frag("okslot", "riscv/t-slot", [("rem", 4)])

    def run(*args):
        return subprocess.run([sys.executable, __file__, *args],
                              capture_output=True, text=True)

    def composes(args, needle):
        r = run(*args)
        assert r.returncode == 0, f"rc={r.returncode}: {r.stdout}{r.stderr}"
        assert needle in r.stdout, f"no {needle!r} in:\n{r.stdout}"
        return r.stdout

    def refuses(args, needle, rc):
        r = run(*args)
        assert r.returncode == rc, f"expected rc={rc} got {r.returncode}: {r.stdout}{r.stderr}"
        assert needle in (r.stdout + r.stderr), f"no {needle!r} in:\n{r.stdout}{r.stderr}"

    arm("GREEN a complete unit composes through the shared resolver",
        lambda: composes([str(enc_doc("riscv/t-base", ["riscv/t-ext"]))],
                         "the fragments COMPOSE"))
    arm("GREEN a declared slot reports partial, requiring a part that does not exist yet",
        lambda: composes(
            [str(enc_doc("riscv/t-base", [], f' (status partial) (slot (id clint) (requires "riscv/t-timer"))'))],
            "PARTIAL — 1 slot(s) unbound"))
    arm("RED   slots without a partial declaration claim completeness",
        lambda: refuses([str(enc_doc("riscv/t-base", [], ' (slot (id clint))'))],
                        "claiming completeness while a hole is open", 2))
    arm("RED   a partial declaration with nothing unbound",
        lambda: refuses([str(enc_doc("riscv/t-base", [], ' (status partial)'))],
                        "a hole is declared that is not there", 2))
    arm("RED   an undeclared compose field is refused by the schema layer, not skipped",
        lambda: refuses([str(enc_doc("riscv/t-base", [], ' (widget "x")'))],
                        'undeclared field "widget"', 2))
    arm("RED   a fragment the composition names but does not have",
        lambda: refuses([str(enc_doc("riscv/t-ghost", []))], "does not exist", 2))
    arm("RED   a fragment whose requires the composition does not provide",
        lambda: refuses([str(enc_doc("riscv/t-needy", []))], "unmet dependency", 2))
    arm("RED   a collision through the resolved unit path is still a rejection",
        lambda: refuses([str(enc_doc("riscv/t-base", ["riscv/t-clash"]))],
                        "COLLISIONS: 1", 1))
    arm("GREEN a pseudo-instruction specializing a composed instruction adds nothing",
        lambda: composes([str(enc_doc("riscv/t-base", ["riscv/t-csr", "riscv/t-pseudo"]))],
                         "pseudo-instruction(s)"))
    arm("RED   a pseudo no composed instruction realizes extends the encoding space",
        lambda: refuses([str(enc_doc("riscv/t-base", ["riscv/t-csr", "riscv/t-ghost-pseudo"]))],
                        "extend the encoding space", 1))
    arm("RED   a pseudo overlapping without specializing is the collision rule one level down",
        lambda: refuses([str(enc_doc("riscv/t-base", ["riscv/t-csr", "riscv/t-ambi-pseudo"]))],
                        "without specializing", 1))
    arm("RED   duplicate instruction names are a rejection, not an advisory",
        lambda: refuses([str(enc_doc("riscv/t-base", ["riscv/t-dupe"]))],
                        "DUPLICATE NAME(S)", 1))

    import shutil
    # declared specializations (P4-SYSTEM.12 slice a): the c.addi/c.nop shape — a general row
    # and a special row whose fixed bits strictly contain it. These fragments are read
    # DIRECTLY, so they are schema-complete (the composed-unit arms above never validate theirs).
    def spec_frag(frag_id, body):
        p = defs / f"{frag_id}.sexp"
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(f'(fragment (id "{frag_id}") (kind isa-extension) (requires)\n'
                     f'  (source (file (name "t") (sha256 "0")) (origin "t") (license "t"))\n{body})')
    GEN = '(insn (name gen) (fixed (1 0 0x1) (15 13 0x0)) (operands) (from "t"))\n'
    SPC = '(insn (name spc) (fixed (1 0 0x1) (15 13 0x0) (11 7 0x0)) (operands) (from "t"))\n'
    OTH = '(insn (name oth) (fixed (1 0 0x1) (15 13 0x0) (6 2 0x3)) (operands) (from "t"))\n'
    DECL = '(specializes (special spc) (general gen) (from "t"))\n'
    spec_frag("riscv/t-spec-ok", GEN + SPC + DECL)
    spec_frag("riscv/t-spec-undeclared", GEN + SPC)
    spec_frag("riscv/t-spec-reversed", GEN + SPC + '(specializes (special gen) (general spc) (from "t"))\n')
    spec_frag("riscv/t-spec-ghost", GEN + OTH + '(specializes (special ghost) (general gen) (from "t"))\n'
              + '(specializes (special oth) (general gen) (from "t"))\n')
    spec_frag("riscv/t-spec-other", OTH)
    arm("GREEN a declared strict specialization composes, reported",
        lambda: composes([str(defs / "riscv/t-spec-ok.sexp")], "declared specializations: 1"))
    arm("RED   the same overlap undeclared is still a collision",
        lambda: refuses([str(defs / "riscv/t-spec-undeclared.sexp")], "COLLISIONS: 1", 1))
    arm("RED   a declaration whose 'special' row is the wider one is refused, not obeyed",
        lambda: refuses([str(defs / "riscv/t-spec-reversed.sexp")], "is not strictly inside", 1))
    arm("RED   a declaration naming an instruction the composition lacks is refused",
        lambda: refuses([str(defs / "riscv/t-spec-ghost.sexp")], "does not carry", 1))
    arm("RED   a declaration cannot silence an overlap it does not name",
        lambda: refuses([str(defs / "riscv/t-spec-ok.sexp"), str(defs / "riscv/t-spec-other.sexp")],
                        "COLLISIONS: 2", 1))

    shutil.rmtree(tmp)
    print(f"check_encoding_disjoint --self-test: {passed} pass / {failed} fail")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
