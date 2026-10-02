#!/usr/bin/env python3
"""Assumption / guarantee discharge — the mechanical form of docs/CPU_ENVIRONMENT.md §5.

`MODEL-COMPOSE.3`. A composition is a conditional claim: the CPU is validated under explicit
environment assumptions, and the board or laboratory must demonstrate that it satisfies them.
This tool is that demonstration, made a verdict: every `environment-assumption` in the merged
obligation set is discharged by named guarantees, or the composition is REJECTED with the
undischarged assumption and the reason named.

THE RULE (design recorded in the owning leaf, `docs/tasks/MODEL-COMPOSE.md`, before code):

  discharged   an environment-assumption is discharged when EVERY one of its `dependencies`
               resolves in the union to an obligation whose direction is a guarantee — the rule
               keys on "not an environment-assumption", so a future direction value (a device's
               guarantee) is accepted by construction. `SOT-FORMAT.5` measured the corpus:
               every assumption's dependencies already point at `cpu-guarantee` obligations
               (`OB-ENV-RESET` -> `OB-ENTRY-STATE`, and kin) — the operator makes that edge a
               verdict instead of a hope.
  missing      a dependency resolving to nothing is refused earlier, by `merge_units`' closure
               (DANGLING DEP) — removing one guarantee fires RED there, naming the assumption
               and the guarantee. This tool consumes the union; it does not re-implement it.
  chain        a dependency landing on another environment-assumption is an undischarged chain —
               a demand pointing at a demand, not at a supply. Refused by name.
  empty        an assumption carrying NO dependency names no guarantee at all — undischargeable
               by construction. Refused by name.

THE COMPLEMENT, STATED SO NOBODY REVERSES IT: an unclaimed guarantee is not an error. A unit
may offer guarantees the other side does not assume; discharge is demanded of assumptions,
not of supplies.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import merge_records as M                                # noqa: E402


class DischargeRefused(Exception):
    """The composition does not hold. Carries every undischarged assumption, one per line."""


def discharge(unit_dirs) -> list[tuple[dict, list[dict]]]:
    """The merged unit's environment-assumptions, each paired with its discharging guarantees.

    Raises MergeRefused (the union itself does not compose) or DischargeRefused (an assumption
    is undischarged) — a composition is accepted only when neither fires.
    """
    merged = M.merge_units(unit_dirs)
    obs = merged.obligations
    report: list[tuple[dict, list[dict]]] = []
    problems: list[str] = []
    for oid, o in obs.items():
        if o.get("direction") != "environment-assumption":
            continue
        deps = o.get("dependencies", [])
        if not deps:
            problems.append(
                f"UNDISCHARGEABLE ASSUMPTION '{oid}': carries no dependency — nothing names "
                f"the guarantee that discharges it")
            continue
        discharged_by: list[dict] = []
        for dep in deps:
            target = obs.get(dep)
            if target is None:                          # unreachable: merge closure refuses first
                problems.append(
                    f"UNDISCHARGED ASSUMPTION '{oid}': its guarantee '{dep}' is not in the union")
            elif target.get("direction") == "environment-assumption":
                problems.append(
                    f"UNDISCHARGED CHAIN '{oid}' -> '{dep}': a dependency landing on another "
                    f"environment-assumption is a demand pointing at a demand, not a supply — "
                    f"name the guarantee that satisfies it")
            else:
                discharged_by.append(target)
        report.append((o, discharged_by))
    if problems:
        raise DischargeRefused("\n".join(problems))
    return report


# --------------------------------------------------------------------------- CLI

def main(argv: list[str]) -> int:
    if len(argv) == 2 and argv[1] == "--self-test":
        return _selftest()
    if len(argv) < 2:
        print("usage: discharge_assumptions.py <unit-dir>…   |   discharge_assumptions.py "
              "--self-test", file=sys.stderr)
        return 2
    try:
        report = discharge(argv[1:])
    except M.MergeRefused as exc:
        print("REJECTED — these units do not compose:", file=sys.stderr)
        print(str(exc), file=sys.stderr)
        return 1
    except DischargeRefused as exc:
        print("REJECTED — the composition does not hold:", file=sys.stderr)
        print(str(exc), file=sys.stderr)
        return 1
    for assumption, guarantees in report:
        edges = ", ".join(f"'{g['id']}' ({g.get('direction')})" for g in guarantees)
        print(f"  {assumption['id']} -> {edges}")
    print(f"all {len(report)} environment-assumption(s) discharged by named guarantee(s) — "
          f"the composition holds")
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

    def unit(name, obs):
        d = tmp / name
        d.mkdir(parents=True, exist_ok=True)
        (d / "contract-obligations.sexp").write_text(
            __import__("records_sexp").dump(obs))
        (d / "sources.sexp").write_text(
            '(sources (publication "P") (revision "r") (base_url "u") (retrieved "d") '
            '(work_dir "w") (source (id "S") (file "s.html") (title "t") '
            '(sha256 "' + "a" * 64 + '") (bytes 1) (http_status 200) (supplies "s")))\n')
        return d

    def ob(oid, direction, deps=()):
        return {"id": oid, "contract_id": "c", "contract_version": "0",
                "profile_ids": ["p"], "direction": direction, "statement": "s",
                "authority": "laboratory",
                "source_refs": [{"source_id": "S", "locator": "§1"}],
                "parameters": {}, "dependencies": list(deps),
                "required_checks": ["CHK-POS", "CHK-NEG"]}

    def holds(*dirs):
        try:
            return discharge(dirs)
        except Exception as exc:
            raise AssertionError(f"should hold, refused: {exc}")

    def refuses(dirs, needle):
        try:
            discharge(dirs)
        except (DischargeRefused, M.MergeRefused) as exc:
            assert needle in str(exc), f"refused, but for the wrong reason: {exc}"
        else:
            raise AssertionError(f"held; it must be refused ({needle})")

    solo = unit("solo", [ob("OB-G1", "cpu-guarantee"), ob("OB-G2", "cpu-guarantee"),
                         ob("OB-ENV", "environment-assumption", deps=("OB-G1", "OB-G2"))])
    r = holds(solo)
    arm("GREEN one unit discharges its own assumptions", lambda: (
        _eq(len(r), 1), _eq([g["id"] for g in r[0][1]], ["OB-G1", "OB-G2"])))

    cpu = unit("cpu", [ob("OB-ENV", "environment-assumption", deps=("OB-G1",))])
    dev = unit("dev", [ob("OB-G1", "cpu-guarantee")])
    arm("GREEN a guarantee carried by the other unit discharges across the boundary",
        lambda: _eq(len(holds(cpu, dev)), 1))

    # P5-BOARD.2 (case sifive-uart-lab-v0): the rule keys on "not an
    # environment-assumption", so a device-guarantee discharges by construction — pinned
    # here so a future narrowing of the rule fires RED instead of drifting.
    dcpu = unit("dcpu", [ob("OB-ENV", "environment-assumption", deps=("OB-UART",))])
    ddev = unit("ddev", [ob("OB-UART", "device-guarantee")])
    arm("GREEN a device-guarantee discharges across the boundary (P5-BOARD.2)",
        lambda: _eq(len(holds(dcpu, ddev)), 1))

    arm("RED   the acceptance control: one guarantee removed — rejected naming it",
        lambda: refuses([unit("cpu2", [ob("OB-ENV", "environment-assumption",
                                         deps=("OB-GONE",))])], "DANGLING DEP"))

    chain = unit("chain", [ob("OB-ENV", "environment-assumption", deps=("OB-ENV2",)),
                           ob("OB-ENV2", "environment-assumption", deps=())])
    arm("RED   a chain — a demand pointing at a demand",
        lambda: refuses([chain], "UNDISCHARGED CHAIN"))

    empty = unit("empty", [ob("OB-ENV", "environment-assumption")])
    arm("RED   an assumption naming no guarantee at all",
        lambda: refuses([empty], "UNDISCHARGEABLE ASSUMPTION"))

    unclaimed = unit("unclaimed", [ob("OB-G1", "cpu-guarantee"),
                                   ob("OB-ENV", "environment-assumption", deps=("OB-G1",)),
                                   ob("OB-G-ORPHAN", "cpu-guarantee")])
    arm("GREEN an unclaimed guarantee is not an error — discharge is demanded of assumptions",
        lambda: _eq(len(holds(unclaimed)), 1))

    import shutil
    shutil.rmtree(tmp)
    print(f"discharge_assumptions --self-test: {passed} pass / {failed} fail")
    return 1 if failed else 0


def _eq(got, want) -> None:
    assert got == want, f"got {got!r}, want {want!r}"


if __name__ == "__main__":
    sys.exit(main(sys.argv))
