#!/usr/bin/env python3
"""Lossless expectation-key controls, through the public mapper and loader."""
from __future__ import annotations

import argparse
import copy
from pathlib import Path
import sys
import tempfile
import types

import dossier_sexp as D
import records_sexp as R
import sexp as S

ROOT = Path(__file__).resolve().parent.parent


def document():
    return {"program": "mapping-fixture.s", "instructions": 1,
            "step": [{"n": 0, "insn": "fixture", "writes": {"x1": "0x1"},
                      "derivation": "synthetic mapping control", "source": "fixture"}]}


def duplicated(*, value="0x2", middle=False):
    form = D.expectations_to_form(document())
    writes = S.children(S.children(form, "step")[0], "writes")[0]
    if middle:
        writes.append([S.Symbol("write"), [S.Symbol("reg"), "x2"], [S.Symbol("value"), "0x3"]])
    writes.append([S.Symbol("write"), [S.Symbol("reg"), "x1"], [S.Symbol("value"), value]])
    return form


def run_controls():
    parent = ROOT / "target/expectation-mapping-controls"
    parent.mkdir(parents=True, exist_ok=True)
    passed = failed = 0

    def equal(name, actual, expected):
        nonlocal passed, failed
        if actual == expected:
            passed += 1
        else:
            failed += 1
            print(f"EXPECTATION MISS {name}: dictionary changed")

    def refuse(name, operation, step=0):
        nonlocal passed, failed
        try:
            operation()
        except D.DossierError as exc:
            reason = str(exc)
            if ("mapping-fixture.s" in reason and f"step {step}:" in reason
                    and "duplicate write register 'x1'" in reason):
                passed += 1
            else:
                failed += 1
                print(f"EXPECTATION MISS {name}: wrong refusal: {reason}")
        else:
            failed += 1
            print(f"EXPECTATION MISS {name}: duplicate write accepted")

    equal("ordinary mapping", D.expectations_to_doc(D.expectations_to_form(document())), document())
    for name, writes in (("empty writes", {}), ("distinct same-valued keys", {"x1": "0x1", "x2": "0x1"}),
                         ("device keys retain arbitrary labels", {"UART_DATA": "0x1", "UART_STATUS": "0x2"})):
        doc = document()
        doc["step"][0]["writes"] = writes
        equal(name, D.expectations_to_doc(D.expectations_to_form(doc)), doc)
    doc = document()
    doc["instructions"] = 2
    doc["step"].append({**copy.deepcopy(doc["step"][0]), "n": 1})
    equal("same key in different steps", D.expectations_to_doc(D.expectations_to_form(doc)), doc)
    refuse("conflicting keys", lambda: D.expectations_to_doc(duplicated()))
    refuse("identical keys", lambda: D.expectations_to_doc(duplicated(value="0x1")))
    refuse("nonadjacent keys", lambda: D.expectations_to_doc(duplicated(middle=True)))
    form = D.expectations_to_form(doc)
    late = S.children(duplicated(), "step")[0]
    S.children(late, "n")[0][1] = 1
    form[-1] = late
    refuse("late-step keys", lambda: D.expectations_to_doc(form), step=1)
    with tempfile.TemporaryDirectory(prefix="mapping-", dir=parent) as allocated:
        base = Path(allocated)
        if base.stat().st_dev != ROOT.stat().st_dev:
            raise ValueError("expectation fixture is off-volume")
        path = base / "fixture.expected.sexp"
        path.write_text(R.render_forms([duplicated()]))
        refuse("public loader conflicting keys", lambda: D.load_expectations(path))
        path.write_text(R.render_forms([duplicated(value="0x1")]))
        refuse("public loader identical keys", lambda: D.load_expectations(path))
        path.write_text(R.render_forms([D.expectations_to_form(document())]))
        equal("public loader positive", D.load_expectations(path), document())
    if base.exists():
        raise ValueError("expectation fixture was not removed")
    print(f"EXPECTATION-MAPPING: {passed} pass / {failed} fail; fixture cleaned")
    return 1 if failed else 0


def main():
    global D
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--mutation", choices=["ignore-duplicate-writes"])
    group.add_argument("--emit", choices=["positive", "conflicting", "identical"])
    args = parser.parse_args()
    if args.emit:
        form = (D.expectations_to_form(document()) if args.emit == "positive"
                else duplicated(value="0x1" if args.emit == "identical" else "0x2"))
        print(R.render_forms([form]), end="")
        return 0
    if args.mutation:
        source = (ROOT / "scripts/dossier_sexp.py").read_text()
        before = "            if reg in writes:"
        if source.count(before) != 1:
            raise ValueError("expectation mutation must match exactly once")
        module = types.ModuleType("expectation_mapping_mutant")
        module.__file__ = str(ROOT / "scripts/dossier_sexp.py")
        sys.modules[module.__name__] = module
        exec(compile(source.replace(before, "            if False:"), module.__file__, "exec"),
             module.__dict__)
        D = module
    return run_controls()


if __name__ == "__main__":
    raise SystemExit(main())
