#!/usr/bin/env python3
"""The INTERACTION-MATRIX core check (P2-SCALAR.4, `G-INTERACTIONS`): one unit's declared
interaction matrix, re-derived and resolved.

The driver is `scripts/check_interaction_matrix.sh` (discovery + self-test); this module
decides ONE unit directory. The rules, each refusing by name:

  1. COMPLETE   the 21 cells are RE-DERIVED from the declared axes (N axes -> N*(N+1)/2
                unordered pairs, diagonal included); an omitted cell fails, named — "the
                matrix is declared first and then exercised; unexercised cells are
                reported, not omitted" is mechanized here.
  2. RESOLVED   every disposition resolves: a guest cell names a tracked guest with BOTH
                source and expectations; a mechanism cell names the closed registry below
                (and the mechanism's artifact still carries its needle); a degenerate cell
                carries a non-empty reason and nothing else.
  3. NO ORPHANS every tracked guest maps to at least one cell — a guest no cell names is
                interaction evidence nobody declared.
  4. DIFFS      every difference id named in the matrix — by a cell, or by a named guest's
                `expect_divergence` declaration — exists in the unit's references.sexp.
  5. DEVICE N/A a unit declaring (vehicle (route device-model)) with NO matrix is
                not-a-finding (P5-BOARD.2, case sifive-uart-lab-v0): the matrix attaches
                with the probe corpus (P5-BOARD.5). A device unit that HAS a matrix
                answers rules 1-4 unchanged.

usage: check_interaction_matrix.py <unit-dir>
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import sexp as S                                # noqa: E402
import dossier_sexp as D                        # noqa: E402
import check_sexp_schema as K                   # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
SCHEMA = ROOT / "schema" / "interactions.sexp"


# The closed mechanism registry: a restart-axis cell names one of these, and the named
# mechanism must still EXIST — the needle is the artifact's own proof of life. A mechanism
# whose artifact loses the needle resolves to nothing, which is a finding, not a rename.
MECHANISMS = {
    "smoke-reproduce": ("scripts/run_semulith_smoke.py", "semulith reproduces"),
    "offline-determinism": ("crates/semulith-verify/src/run/tests.rs",
                            "every_guest_re_executes_identically_from_cold_reset"),
    # P3-BREADTH.7 slice 2 (case dsp56300-lab-v0): the DSP subset's two measured legs —
    # the differential end-state agreement driver, and the typed-stop boundary type.
    "dsp56300-smoke-agreement": ("scripts/run_dsp56300_smoke.py", "dsp56300 smoke: "),
    "dsp56300-typed-stop": ("crates/semulith-dsp56300/src/machine.rs",
                            "pub enum ModelStop"),
}


def _strings(form, name: str) -> list[str]:
    return [str(v) for c in S.children(form, name) for v in c[1:]]


def _declared_route(unit: Path) -> str | None:
    """The unit's declared vehicle route, or None. An absent or unreadable profile is
    not a declaration."""
    prof = unit / "profile.sexp"
    if not prof.is_file():
        return None
    try:
        forms = S.read_file(prof)
        form = next(f for f in forms
                    if isinstance(f, list) and f and str(f[0]) == "profile")
    except (S.SexpError, StopIteration):
        return None
    routes = [str(c[1]) for v in S.children(form, "vehicle")
              for c in S.children(v, "route")]
    return routes[0] if routes else None


def _device_route_declared(unit: Path) -> bool:
    """The unit's profile declares (vehicle (route device-model)) — P5-BOARD.2, case
    sifive-uart-lab-v0."""
    return _declared_route(unit) == "device-model"


def check_unit(unit: Path) -> tuple[list[str], list[str]]:
    """Return (findings, cell report lines) for one unit directory."""
    tag = unit.name
    matrix_path = unit / "interactions.sexp"
    if not matrix_path.is_file():
        if _device_route_declared(unit):
            return ([], [f"device-model route declared — the matrix attaches with the "
                         f"probe corpus (P5-BOARD.5)"])
        # P4-SYSTEM.1 (case rv64gc-lab-v0): a profile-resolution unit has no executed
        # corpus to matrix — n/a by declaration; an interactions.sexp beside the
        # declaration is judged below like any other matrix (its dispositions must
        # still resolve).
        if _declared_route(unit) == "profile-resolution":
            return ([], [f"profile-resolution route declared — the matrix attaches "
                         f"with the definition pipeline (P4-SYSTEM.2+)"])
        return ([f"NO MATRIX {tag}: no interactions.sexp beside the dossier — the "
                 f"interaction matrix is declared first and then exercised; an undeclared "
                 f"matrix is not an exercised one"], [])
    constructs, operators = K.load_schema(SCHEMA)
    errors = K.validate_file(matrix_path, constructs, operators)
    if errors:
        return ([f"INVALID {e}" for e in errors], [])

    forms = [f for f in S.read_file(matrix_path)
             if isinstance(f, list) and f and str(f[0]) == "interactions"]
    if len(forms) != 1:
        return ([f"INVALID {matrix_path.name}: expected exactly one (interactions …) "
                 f"form"], [])
    form = forms[0]

    findings: list[str] = []
    axes = [str(S.field(a, "id", matrix_path.name))
            for a in S.children(form, "axis")]
    if len(set(axes)) != len(axes):
        findings.append(f"DUPLICATE AXIS {tag}: the axis list repeats an id — the cell "
                        f"count would be under-derived")
    declared = set(axes)
    want = {tuple(sorted((axes[i], axes[j])))
            for i in range(len(axes)) for j in range(i, len(axes))}

    # ---- the cells ---------------------------------------------------------------
    cells: dict[tuple[str, str], list] = {}
    for cell in S.children(form, "cell"):
        pair_axes = _strings(cell, "axis")
        if len(pair_axes) != 2:
            findings.append(f"BAD CELL {tag}: a cell names {len(pair_axes)} axes "
                            f"({pair_axes}) — a cell is one axis PAIR")
            continue
        pair = tuple(sorted(pair_axes))
        unknown = [a for a in pair if a not in declared]
        if unknown:
            findings.append(f"UNDECLARED AXIS {tag}: cell {pair[0]}×{pair[1]} names "
                            f"{unknown}, which no (axis …) declares")
            continue
        if pair in cells:
            findings.append(f"DUPLICATE CELL {tag}: {pair[0]}×{pair[1]} is declared twice")
            continue
        cells[pair] = cell

    for pair in sorted(want - set(cells)):
        findings.append(f"OMITTED CELL {tag}: {pair[0]}×{pair[1]} has no cell — an "
                        f"unexercised cell is REPORTED (mechanism or degenerate-with-"
                        f"reason), never omitted")

    # ---- dispositions resolve ------------------------------------------------------
    guests_named: set[str] = set()
    diffs_named: set[str] = set()
    report: list[str] = []
    for pair in sorted(cells):
        cell = cells[pair]
        guests = _strings(cell, "guest")
        mechs = _strings(cell, "mechanism")
        diffs = _strings(cell, "difference")
        degen = [str(c[1]) for c in S.children(cell, "degenerate") if len(c) == 2]
        label = f"{pair[0]}×{pair[1]}"
        if not guests and not mechs and not degen:
            findings.append(f"EMPTY DISPOSITION {tag}: {label} dispositions nothing — "
                            f"the cell does not say how the pair is exercised or why it "
                            f"cannot be")
            continue
        if degen and (guests or mechs or diffs):
            findings.append(f"DEGENERATE MIXED {tag}: {label} is degenerate AND names "
                            f"guests/mechanisms — a pair that cannot arise has no exerciser")
        for g in guests:
            guests_named.add(g)
            missing = [p.name for p in (unit / "guests" / f"{g}.s",
                                        unit / "guests" / f"{g}.expected.sexp")
                       if not p.is_file()]
            if missing:
                findings.append(f"UNRESOLVED GUEST {tag}: {label} names '{g}', but "
                                f"{', '.join(missing)} is absent — a guest cell needs the "
                                f"source AND the expectations")
        for m in mechs:
            if m not in MECHANISMS:
                findings.append(f"UNKNOWN MECHANISM {tag}: {label} names '{m}' — the "
                                f"registry is closed: {sorted(MECHANISMS)}")
                continue
            rel, needle = MECHANISMS[m]
            artifact = ROOT / rel
            if not artifact.is_file() or needle not in artifact.read_text():
                findings.append(f"MECHANISM MISSING {tag}: {label} names '{m}', but "
                                f"{rel} does not carry '{needle}' — the mechanism no "
                                f"longer exists")
        diffs_named.update(diffs)
        what = ([f"guests {', '.join(guests)}"] if guests else []) + \
               ([f"mechanism {', '.join(mechs)}"] if mechs else []) + \
               (["degenerate"] if degen else [])
        report.append(f"  {label}: {'; '.join(what)}")

    # ---- no orphan guests ------------------------------------------------------------
    for exp_path in sorted((unit / "guests").glob("*.expected.sexp")):
        name = exp_path.name[: -len(".expected.sexp")]
        if name not in guests_named:
            findings.append(f"ORPHAN GUEST {tag}: '{name}' is tracked but no cell names "
                            f"it — every guest is interaction evidence for SOME cell, or "
                            f"the matrix does not describe the corpus")

    # ---- difference ids exist in references.sexp --------------------------------------
    for g in sorted(guests_named):
        exp_path = unit / "guests" / f"{g}.expected.sexp"
        if not exp_path.is_file():
            continue                    # already named by UNRESOLVED GUEST
        try:
            div = D.load_expectations(exp_path).get("expect_divergence")
        except D.DossierError as exc:
            findings.append(f"UNREADABLE {tag}: {exp_path.name} does not map — {exc}")
            continue
        if div is not None:
            diffs_named.add(str(div["difference"]))
    if diffs_named:
        refs_path = unit / "references.sexp"
        known: set[str] = set()
        if refs_path.is_file():
            known = {str(d["id"]) for d in
                     D.load_references(refs_path).get("difference", [])}
        else:
            findings.append(f"NO REFERENCES {tag}: difference ids are named but "
                            f"references.sexp is absent")
        for d in sorted(diffs_named - known):
            findings.append(f"UNKNOWN DIFFERENCE {tag}: '{d}' is named in the matrix but "
                            f"references.sexp records no such difference — an expected "
                            f"divergence without its record is an unjustified mask")

    return findings, report


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("usage: check_interaction_matrix.py <unit-dir>", file=sys.stderr)
        return 2
    unit = Path(argv[1])
    try:
        findings, report = check_unit(unit)
    except (S.SexpError, K.SchemaError, D.DossierError) as exc:
        print(str(exc), file=sys.stderr)
        return 2
    for line in report:
        print(line)
    for f in findings:
        print(f, file=sys.stderr)
    if findings:
        return 1
    # Cell report lines are indented ("  label: …"); an unindented line is a unit note
    # (the device-model n/a declaration), never a cell — count cells, not lines.
    cells = sum(1 for line in report if line.startswith("  "))
    print(f"{cells} cells declared, every disposition resolves")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
