#!/usr/bin/env python3
"""The extraction contract: is the definition SUFFICIENT for an engine?

`MODEL-METHOD.10` — the precondition for writing model code, stated as a verdict. An engine
must be able to extract, for every declared instruction, an ENCODING and SEMANTICS and a
REQUIREMENT; for every state element a RESET; for every obligation its CHECKS. Each leg had
its own check already — the contract's job is the INTEGRATIVE claim: the four per-instruction
sets are the SAME set, and the smaller legs hold, so "the engine can extract all it needs" is
a verdict rather than an intention. `P1-LAB` cites this check; the day it fires, model code
does not start on a definition that quietly lacks something.

THE CONTRACT, mechanically, over a unit directory:

  SCOPE        the profile's scope declares the instruction set (family lists, one name each)
  ENCODING     the composed union resolves, and names exactly the scope's set
  SEMANTICS    every instruction in the union has checked semantics (schema-validated file,
               known forms, arity true) in the unit's fragments' sem files
  REQUIREMENTS the union of requirement `(insns …)` equals the union — every instruction is
               committed to by at least one requirement, and no requirement claims an
               instruction the unit does not declare
  RESET        every state element in state.sexp carries a (reset …) with its authority
  CHECKS       every obligation carries a positive AND a negative required check

REFUSES, each naming the instruction or element and the set that's short. A definition that
fails the contract is not a definition an engine could consume — it is a wish.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import check_semantics as SEM                                # noqa: E402
import dossier_sexp as D                                     # noqa: E402
import records_sexp as R                                     # noqa: E402
import riscv_asm                                             # noqa: E402
import sexp as S                                             # noqa: E402


class ExtractionRefused(Exception):
    """The definition is not sufficient. Carries every gap, one per line."""


def _scope_names(profile_form, where: str) -> set[str]:
    scope = S.children(profile_form, "scope")
    if not scope:
        raise ExtractionRefused(f"{where}: declares no (scope …) — what instruction set is "
                                f"the unit even claiming?")
    out: set[str] = set()
    for fam in scope[0][1:]:
        if not isinstance(fam, list) or not fam:
            continue
        head = str(fam[0])
        if head.startswith("count_") or head in ("authority", "source", "comment", "note"):
            continue                                   # metadata, not instructions
        # quoted strings only: bare symbols are Symbol, quoted values are exactly str
        out |= {str(x).lower() for x in fam[1:] if type(x) is str}
    return out


def _encoding_names(unit: Path) -> set[str]:
    enc_path = unit / "encoding.sexp"
    if not enc_path.is_file():
        raise ExtractionRefused(f"{unit}: no encoding.sexp — a unit with no encoding "
                                f"declares nothing to extract")
    try:
        enc = S.read_file(enc_path)[0]
        resolved = riscv_asm.resolve_composition(enc, enc_path)
    except (S.SexpError, riscv_asm.AsmError) as exc:
        raise ExtractionRefused(f"{enc_path}: does not resolve — {exc}")
    return {str(S.field(i, "name")) for i in S.children(resolved, "insn")}


def _semantics_names(unit: Path) -> tuple[set[str], list[str]]:
    enc_path = unit / "encoding.sexp"
    enc = S.read_file(enc_path)[0]
    comp = S.children(enc, "compose")
    if not comp:
        return set(), ["the unit composes no fragments — no semantics to extract"]
    frag_root = enc_path.parent.parent.parent / str(S.field(enc, "fragment-root", str(enc_path)))
    names = [str(S.field(comp[0], "base", str(enc_path)))]
    ext = S.children(comp[0], "extensions")
    names += [str(x) for x in (ext[0][1:] if ext else [])]
    files = [frag_root / (n + ".sem.sexp") for n in names]
    present = [p for p in files if p.is_file()]
    if not present:
        return set(), ["no fragment in the composition carries a .sem.sexp — the unit has no "
                       "semantics at all"]
    try:
        SEM.load_language()
    except SEM.SemError as exc:
        raise ExtractionRefused(f"the semantic language does not load — {exc}")
    defined: set[str] = set()
    problems: list[str] = []
    for p in present:
        try:
            SEM._schema_validate_sem_file(p)
            root = S.read_file(p)[0]
        except (SEM.SemError, S.SexpError) as exc:
            problems.append(f"{p.name}: {exc}")
            continue
        for s in S.children(root, "sem"):
            name = str(S.field(s, "insn", str(p)))
            if name in defined:
                problems.append(f"{p.name} [{name}]: defined twice across the unit's semantics")
            defined.add(name)
            for e in S.children(s, "effect"):
                try:
                    for sub in e[1:]:
                        SEM.check_expr(sub, f"{p.name} [{name}]", None)
                except SEM.SemError as exc:
                    problems.append(str(exc))
    return defined, problems


def _requirement_names(unit: Path) -> set[str]:
    path = unit / "requirements.sexp"
    if not path.is_file():
        raise ExtractionRefused(f"{unit}: no requirements.sexp — the requirement leg is absent")
    try:
        return {i for r in R.load(path) for i in r.get("insns", [])}
    except (R.RecordRefused, S.SexpError) as exc:
        raise ExtractionRefused(f"{path}: does not map to records — {exc}")


def _state_resets(unit: Path, include_families: bool = False) -> list[str]:
    """Every state element carries a (reset …). Corpus-shaped: integer_registers and each
    (register …) under special_registers are the elements today; the rule generalizes by
    refusing an element without a reset rather than enumerating heads forever. The
    device-model route (P5-BOARD.2, case sifive-uart-lab-v0) also counts register_family
    blocks as elements — route-scoped, so a route whose families honestly carry no reset
    (dsp56300-lab-v0) never fires here."""
    path = unit / "state.sexp"
    if not path.is_file():
        raise ExtractionRefused(f"{unit}: no state.sexp — the reset leg is absent")
    try:
        root = S.read_file(path)[0]
    except S.SexpError as exc:
        raise ExtractionRefused(f"{path}: does not parse — {exc}")
    problems: list[str] = []
    elements = []
    for ir in S.children(root, "integer_registers"):
        elements.append(("integer_registers", ir))
    for sr in S.children(root, "special_registers"):
        for reg in S.children(sr, "register"):
            elements.append((str(S.field(reg, "id", str(path))), reg))
    if include_families:
        for fam in S.children(root, "register_family"):
            elements.append((str(S.field(fam, "id", str(path))), fam))
    if not elements:
        problems.append(f"{path.name}: declares no state element at all — an engine has no "
                        f"architectural state to extract")
    for label, el in elements:
        if not S.children(el, "reset"):
            problems.append(f"state element '{label}': carries no (reset …) — an engine "
                            f"cannot extract where this element starts")
    return problems


def _obligation_checks(unit: Path) -> list[str]:
    path = unit / "contract-obligations.sexp"
    if not path.is_file():
        return [f"{unit}: no contract-obligations.sexp — the checks leg is absent"]
    try:
        obs = R.load(path)
    except (R.RecordRefused, S.SexpError) as exc:
        return [f"{path}: does not map to records — {exc}"]
    problems = []
    for o in obs:
        checks = o.get("required_checks", [])
        if not any(c.endswith("-POS") for c in checks) or not any(c.endswith("-NEG") for c in checks):
            problems.append(f"obligation '{o.get('id')}': required_checks {checks} lack a "
                            f"positive AND a negative fixture")
    return problems


def check_extraction(unit) -> dict:
    """The contract over a unit directory. Raises ExtractionRefused naming every gap."""
    unit = Path(unit)
    if not unit.is_dir():
        raise ExtractionRefused(f"unit '{unit}' does not exist")
    gaps: list[str] = []

    prof_path = unit / "profile.sexp"
    if not prof_path.is_file():
        raise ExtractionRefused(f"{unit}: no profile.sexp — the scope leg is absent")
    try:
        forms = S.read_file(prof_path)
    except S.SexpError as exc:
        raise ExtractionRefused(f"{prof_path}: does not parse — {exc}")
    profile_form = next((f for f in forms
                         if isinstance(f, list) and f and f[0] == "profile"), None)
    if profile_form is None:
        raise ExtractionRefused(f"{prof_path.name}: no (profile …) document — the scope leg "
                                f"is absent")
    scope = _scope_names(profile_form, prof_path.name)

    if not scope:
        gaps.append(f"{prof_path.name}: the scope declares no instruction names")

    # P3-BREADTH.7 (decision_gate-applicability-by-declared-vehicle): a unit declaring
    # (vehicle (route sibling-crate)) has no definition pipeline for this contract to
    # judge — reported by name, and a declaration contradicting the documents is a gap.
    vehicle = S.children(profile_form, "vehicle")
    routes = [str(c[1]) for v in vehicle for c in S.children(v, "route")]
    if routes and routes[0] == "sibling-crate":
        if (unit / "encoding.sexp").is_file():
            raise ExtractionRefused(
                f"{unit}: declares vehicle route sibling-crate but carries an "
                f"encoding.sexp — the declaration contradicts the documents")
        if gaps:
            raise ExtractionRefused("\n".join(gaps))
        return {"instructions": len(scope), "route": "sibling-crate",
                "state_elements": "n/a (sibling-crate route)",
                "obligations": "n/a (sibling-crate route)"}

    # P4-SYSTEM.1 (case rv64gc-lab-v0): a unit declaring (vehicle (route
    # profile-resolution)) has its SELECTION resolved and citable, but the definition
    # pipeline has not started — the encoding/semantics/state legs have nothing to
    # judge yet. The obligation leg DOES apply: the resolution's decisions are the v0
    # contract's obligations, each checked both ways by declaration. A
    # definition-pipeline document beside the declaration is a contradiction, refused.
    if routes and routes[0] == "profile-resolution":
        contradictions = [name for name in ("encoding.sexp", "state.sexp")
                          if (unit / name).is_file()]
        if (unit / "guests").is_dir():
            contradictions.append("guests")
        if contradictions:
            raise ExtractionRefused(
                f"{unit}: declares vehicle route profile-resolution but carries "
                f"{', '.join(contradictions)} — the declaration contradicts the "
                f"documents")
        gaps += _obligation_checks(unit)
        if gaps:
            raise ExtractionRefused("\n".join(gaps))
        return {"instructions": len(scope), "route": "profile-resolution",
                "state_elements": "n/a (profile-resolution route)",
                "obligations": "checked both ways"}

    # P5-BOARD.2 (case sifive-uart-lab-v0): a unit declaring (vehicle (route
    # device-model)) has no instruction pipeline — the encoding/semantics/integrative
    # claim does not apply — but the two legs a device honestly answers DO: every state
    # element carries a reset, every obligation its checks. An encoding.sexp beside the
    # declaration is the same contradiction the sibling-crate route refuses.
    if routes and routes[0] == "device-model":
        if (unit / "encoding.sexp").is_file():
            raise ExtractionRefused(
                f"{unit}: declares vehicle route device-model but carries an "
                f"encoding.sexp — the declaration contradicts the documents")
        gaps += _state_resets(unit, include_families=True)
        gaps += _obligation_checks(unit)
        if gaps:
            raise ExtractionRefused("\n".join(gaps))
        return {"instructions": len(scope), "route": "device-model",
                "state_elements": "resets everywhere",
                "obligations": "checked both ways"}

    encoding = _encoding_names(unit)
    semantics, sem_problems = _semantics_names(unit)
    requirements = _requirement_names(unit)
    gaps += sem_problems
    gaps += _state_resets(unit)
    gaps += _obligation_checks(unit)

    for name, have in (("encoding", encoding), ("semantics", semantics),
                       ("requirements", requirements)):
        if not have:
            gaps.append(f"the {name} set is EMPTY — nothing to extract")

    # the integrative claim: one set, four ways
    for name, other in (("encoding", encoding), ("semantics", semantics),
                        ("requirements", requirements)):
        short = sorted(scope - other)
        if short:
            gaps.append(f"scope declares {len(short)} instruction(s) the {name} set does not "
                        f"cover: {', '.join(short[:8])}{' …' if len(short) > 8 else ''}")
    for name, other in (("encoding", encoding), ("semantics", semantics),
                        ("requirements", requirements)):
        extra = sorted(other - scope)
        if extra:
            gaps.append(f"the {name} set names {len(extra)} instruction(s) the scope does not "
                        f"declare: {', '.join(extra[:8])}{' …' if len(extra) > 8 else ''}")

    if gaps:
        raise ExtractionRefused("\n".join(gaps))
    return {"instructions": len(scope), "state_elements": "reset everywhere",
            "obligations": "checked both ways"}


def main(argv: list[str]) -> int:
    if len(argv) == 2 and argv[1] == "--self-test":
        return _selftest()
    if len(argv) != 2:
        print("usage: check_extraction.py <unit-dir>   |   check_extraction.py --self-test",
              file=sys.stderr)
        return 2
    try:
        census = check_extraction(argv[1])
    except ExtractionRefused as exc:
        print("REFUSED — the definition is not sufficient for an engine:", file=sys.stderr)
        print(str(exc), file=sys.stderr)
        return 1
    if census.get("route") == "sibling-crate":
        print(f"sibling-crate route declared ({census['instructions']} scope forms) — the "
              f"extraction contract applies to generated-definition units; this unit's "
              f"model is the hand-written crate, gated by its own tests")
        return 0
    if census.get("route") == "device-model":
        print(f"device-model route declared ({census['instructions']} scope registers; "
              f"{census['state_elements']}; obligations {census['obligations']})")
        return 0
    if census.get("route") == "profile-resolution":
        print(f"profile-resolution route declared ({census['instructions']} scope forms; "
              f"{census['state_elements']}; obligations {census['obligations']}) — the "
              f"selection is resolved and citable; the definition pipeline has not started")
        return 0
    print(f"the definition is SUFFICIENT for an engine: {census['instructions']} instructions, "
          f"each with encoding + semantics + requirement; {census['state_elements']}; "
          f"obligations {census['obligations']}")
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

    unit = tmp / "profiles" / "u"
    (tmp / "definitions/riscv").mkdir(parents=True)
    (tmp / "profiles").mkdir(parents=True)
    u = unit
    u.mkdir(parents=True, exist_ok=True)

    def build(sem_rules=("add", "sub"), req_insns=("add", "sub"), with_reset=True,
              neg_checks=True, scope=("add", "sub")):
        (tmp / "definitions/riscv/t.sexp").write_text(
            '(fragment (id "riscv/t") (kind extension)\n'
            '(insn (name add) (fixed (6 2 0x13) (1 0 0x3)) (operands rd rs1 rs2))\n'
            '(insn (name sub) (fixed (6 2 0x13) (1 0 0x3)) (operands rd rs1 rs2)))\n')
        rules = "".join(
            f'(sem (insn {i}) (source "S §1 — why") (effect (set (reg rd) (add (reg rs1) (reg rs2)))))\n'
            for i in sem_rules)
        (tmp / "definitions/riscv/t.sem.sexp").write_text(
            f'(semantics (fragment "riscv/t") (xlen 64)\n{rules})')
        (u / "encoding.sexp").write_text(
            '(encoding (profile "u") (ilen 32)\n  (compose (base "riscv/t") (extensions))\n'
            '  (fragment-root "definitions"))\n')
        fam = " ".join(f'"{n.upper()}"' for n in scope)
        (u / "profile.sexp").write_text(
            f'(profile (id "u") (version "0") (status "development") (architecture "RISC-V")\n'
            f'  (scope (count_base {len(scope)}) (count_total {len(scope)}) (demo {fam}))\n'
            f'  (decision (id "D-X") (authority architecture) (statement "s") (source "S §1")))\n')
        reqs = [{"id": "REQ-D-X", "profile_ids": ["u"], "kind": "instruction", "statement": "s",
                 "insns": list(req_insns),
                 "source_refs": [{"source_id": "S", "locator": "§1"}],
                 "applicability": "included", "research_status": "resolved",
                 "implementation_status": "planned",
                 "source_semantics": {"category": "defined", "detail": "d"},
                 "risk": "low", "obligation_ids": ["OB-X"], "dependencies": [],
                 "implementation_refs": [], "evidence_ids": []}]
        (u / "requirements.sexp").write_text(R.dump(reqs))
        checks = ["CHK-X-POS"] + (["CHK-X-NEG"] if neg_checks else [])
        obs = [{"id": "OB-X", "contract_id": "c", "contract_version": "0",
                "profile_ids": ["u"], "direction": "cpu-guarantee", "statement": "s",
                "authority": "architecture",
                "source_refs": [{"source_id": "S", "locator": "§1"}],
                "parameters": {}, "dependencies": [], "required_checks": checks}]
        (u / "contract-obligations.sexp").write_text(R.dump(obs))
        reset = "(reset (value \"0\") (authority laboratory) (source \"S\") (statement \"r\"))" \
            if with_reset else ""
        (u / "state.sexp").write_text(
            f'(state (profile_id "u") (xlen 64)\n'
            f'  (integer_registers (count 32) (width_bits 64) {reset}))\n')

    def sufficient():
        c = check_extraction(u)
        assert c["instructions"] == 2, c

    def refused(needle):
        try:
            check_extraction(u)
        except ExtractionRefused as exc:
            assert needle in str(exc), f"refused, but for the wrong reason: {exc}"
        else:
            raise AssertionError(f"sufficient; it must be refused ({needle})")

    build()
    arm("GREEN a complete unit is sufficient", sufficient)
    build(sem_rules=("add",))
    arm("RED   the acceptance's shape: one instruction's semantics removed",
        lambda: refused("does not cover: sub"))
    build(req_insns=("add",))
    arm("RED   an instruction no requirement commits to",
        lambda: refused("requirements set does not cover"))
    build(req_insns=("add", "sub", "ghost"))
    arm("RED   a requirement naming an instruction the scope does not declare",
        lambda: refused("the scope does not declare"))
    build(with_reset=False)
    arm("RED   a state element without a reset",
        lambda: refused("carries no (reset …)"))
    build(neg_checks=False)
    arm("RED   an obligation with no negative fixture",
        lambda: refused("positive AND a negative"))

    import shutil
    shutil.rmtree(tmp)
    print(f"check_extraction --self-test: {passed} pass / {failed} fail")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
