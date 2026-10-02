#!/usr/bin/env python3
"""Board composition verdict — the mechanical form of docs/CPU_ENVIRONMENT.md §5 (ENV-02).

`P5-BOARD.4`. A board composition is a conditional claim: the CPU is validated under
explicit environment assumptions, and the board must demonstrate that it satisfies them —
for EVERY assumption, a named board or device guarantee, or the composition is REJECTED.
An unmatched assumption is a rejection, never a note (the leaf's acceptance).

Three legs, each decided over the board's own data:

  discharge    every `environment-assumption` in the composed unit is discharged by named
               guarantees — `discharge_assumptions.py` over the on-disk composed
               catalogues (their freshness is BOARD-GEN's; this tool does not re-derive).
               The edges are obligation-graph edges: the platform-dependent assumptions
               discharge through `OB-PLATFORM`, the LABORATORY platform guarantee scoped
               to the CPU unit — the board-level satisfaction of those assumptions is
               what the next two legs pin.
  satisfies    every `satisfies` edge in the board definition (the reset block, the
               declared timer/interrupt-controller absences) resolves to an
               environment-assumption that EXISTS in the composed unit — the declared
               intent is checked against the composed reality, never taken on trust.
  dispositions a device dossier may defer a value to the composing board: an obligation
               marked (composition_disposition "required") must be answered by EXACTLY
               ONE board decision carrying an `answers` edge to it, and every `answers`
               edge must name such a marked obligation. Both directions refused by name —
               an unanswered composition record, an edge to nothing, a double answer.

ACCEPTED prints every edge; any leg failing REJECTS the composition with the reasons.
The BOARD-VERDICT doctrine (`scripts/check_board_verdict.sh`) runs this on every commit.

usage: board_verdict.py <board-dir>…
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import check_sexp_schema as K                      # noqa: E402
import discharge_assumptions as DA                 # noqa: E402
import merge_records as M                          # noqa: E402
import records_sexp as R                           # noqa: E402
import sexp as S                                   # noqa: E402

REPO = Path(__file__).resolve().parent.parent
BOARD_SCHEMA = REPO / "schema" / "board.sexp"
MARKER = "composition_disposition"


class VerdictRefused(Exception):
    """The composition does not hold. Carries every reason found, one per line."""


def _strings(form, name) -> list[str]:
    return [str(v) for child in S.children(form, name) for v in child[1:]]


def verdict(board_dir: Path) -> dict:
    """Decide one board's composition verdict. Raises VerdictRefused with every reason."""
    board_path = board_dir / "board.sexp"
    problems: list[str] = []

    # Leg 0: the definition must be judgeable — a verdict over a document nobody
    # validates is a claim without legs (the MODEL-COMPOSE.4 lesson).
    try:
        constructs, operators = K.load_schema(BOARD_SCHEMA)
        errors = K.validate_file(board_path, constructs, operators)
    except (K.SchemaError, S.SexpError) as exc:
        raise VerdictRefused(f"{board_path}: the schema layer cannot judge — {exc}")
    if errors:
        raise VerdictRefused(f"{board_path}: refused by board.sexp — " + "; ".join(errors))
    doc = S.read_file(board_path)[0]

    # Leg 1: discharge — every environment-assumption discharged by named guarantees.
    try:
        discharged = {(o["id"]): [g["id"] for g in gs]
                      for o, gs in DA.discharge([board_dir])}
    except (DA.DischargeRefused, M.MergeRefused) as exc:
        raise VerdictRefused(f"REJECTED — the composition does not hold:\n{exc}")

    # Leg 2: satisfies — the declared edges resolve to discharged environment-assumptions.
    obs = {o["id"]: o for o in R.load(board_dir / "contract-obligations.sexp")}
    satisfies_edges: list[tuple[str, str]] = []
    for element in ("reset", "timers", "interrupt-controller"):
        block = S.children(doc, element)[0]
        for oid in _strings(block, "satisfies"):
            target = obs.get(oid)
            if target is None or target.get("direction") != "environment-assumption":
                problems.append(
                    f"SATISFIES EDGE '{oid}' on '{element}': resolves to no "
                    f"environment-assumption in the composed unit — a declared edge to "
                    f"nothing is a rejection, not a note")
            else:
                satisfies_edges.append((element, oid))

    # Leg 3: dispositions — every board-deferred obligation answered exactly once, and
    # every answers edge naming one.
    marked = {oid for oid, o in obs.items()
              if (o.get("parameters") or {}).get(MARKER) == "required"}
    answered: dict[str, str] = {}
    bindings: list[tuple[str, str]] = []
    for d in S.children(doc, "decision"):
        did = str(S.field(d, "id"))
        for oid in _strings(d, "answers"):
            if oid not in marked:
                problems.append(
                    f"ANSWERS NOTHING: decision '{did}' names '{oid}', which is not an "
                    f"obligation the composed unit defers to the board "
                    f"({MARKER} \"required\") — an edge to nothing is a rejection")
            elif oid in answered:
                problems.append(
                    f"ANSWERED TWICE: obligation '{oid}' is answered by both "
                    f"'{answered[oid]}' and '{did}' — one disposition per record")
            else:
                answered[oid] = did
                bindings.append((did, oid))
    for oid in sorted(marked - set(answered)):
        problems.append(
            f"UNANSWERED COMPOSITION OBLIGATION '{oid}': the device dossier defers it to "
            f"the composing board ({MARKER} \"required\") and no decision answers it — "
            f"an unmatched composition record is a rejection, not a note")
    if problems:
        raise VerdictRefused("\n".join(problems))
    return {"id": str(S.field(doc, "id")),
            "discharged": discharged,
            "satisfies": satisfies_edges,
            "bindings": bindings}


# --------------------------------------------------------------------------- CLI

def main(argv: list[str]) -> int:
    if len(argv) < 2:
        print("usage: board_verdict.py <board-dir>…", file=sys.stderr)
        return 2
    rc = 0
    for arg in argv[1:]:
        try:
            report = verdict(Path(arg))
        except VerdictRefused as exc:
            print(str(exc), file=sys.stderr)
            rc = 1
            continue
        print(f"{report['id']}: composition ACCEPTED")
        for oid, guarantees in report["discharged"].items():
            print(f"  {oid} -> " + ", ".join(f"'{g}'" for g in guarantees))
        for element, oid in report["satisfies"]:
            print(f"  satisfies '{element}' -> {oid} (discharged)")
        for did, oid in report["bindings"]:
            print(f"  {did} answers {oid}")
        print(f"  all {len(report['discharged'])} environment-assumption(s) discharged, "
              f"{len(report['satisfies'])} satisfies edge(s) resolve, "
              f"{len(report['bindings'])} composition disposition(s) bind — "
              f"the composition holds")
    return rc


if __name__ == "__main__":
    sys.exit(main(sys.argv))
