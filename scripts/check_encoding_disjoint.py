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


def load_fragment(path: Path) -> list[Insn]:
    """Read a fragment: a unit `encoding.sexp`, a bare `fragment.sexp`, or an opcodes table."""
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
            out = []
            for i in _sexp.children(root, "insn"):
                fixed = [(int(a), int(b), int(c)) for a, b, c in _sexp.children(i, "fixed")[0][1:]]
                out.append(Insn(str(_sexp.field(i, "name")), fixed, path.name))
            return out
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
    if len(argv) == 2 and argv[1] == "--self-test":
        return _selftest()
    if len(argv) < 2:
        print("usage: check_encoding_disjoint.py <fragment…>", file=sys.stderr)
        return 2
    insns: list[Insn] = []
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
            part = load_fragment(p)
            if not part:
                print(f"REFUSED: {p} yielded no instructions — an empty fragment is not a valid one",
                      file=sys.stderr)
                return 2
            print(f"  fragment {p.name:16} {len(part):3} instruction(s)")
            insns += part
    except (CompositionError, _sexp.SexpError, ValueError) as exc:
        print(f"REFUSED: {exc}", file=sys.stderr)
        return 2

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

    import shutil
    shutil.rmtree(tmp)
    print(f"check_encoding_disjoint --self-test: {passed} pass / {failed} fail")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
