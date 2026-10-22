#!/usr/bin/env python3
"""Requirement-status derivation controls on synthetic graphs; derivation only, no credit."""
from __future__ import annotations

import argparse
import importlib.util
import json
import os
from pathlib import Path
import shutil
import sys
from tempfile import TemporaryDirectory
import unittest

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
ROOT = next(p for p in HERE.parents if (p / "scripts" / "sexp.py").is_file())
MUTATION = None
# Each seam replaces one load-bearing predicate in a copied module; its test must then fail.
SEAMS = {
    "credit-pending": ('    return receipt.get(CREDITED_FIELD) is True\n', '    return True\n'),
    "ignore-drift": ('    drift = [row for row in rows if row["recorded"] != row["derived"]]\n',
                     '    drift = []\n'),
    "skip-supersession": ('                if ob not in effective:\n', '                if False:\n'),
    "unresolved-closes": ('        elif r["research_status"] == "resolved" and r["obligation_ids"] and set(r["obligation_ids"]) <= credited_set:\n',
                          '        elif r["obligation_ids"] and set(r["obligation_ids"]) <= credited_set:\n'),
    "argument-optional": ('        if excluded and argued:\n', '        if excluded:\n'),
    "declared-credits": ('            cases.append(dict(id=case.name, profile=None, credited=False, evaluation="declared",\n',
                         '            cases.append(dict(id=case.name, profile=None, credited=True, evaluation="declared",\n'),
}
MUTATION_TESTS = {
    "credit-pending": "test_pending_case_stays_uncredited_and_planned",
    "ignore-drift": "test_recorded_status_drift_is_reported",
    "skip-supersession": "test_case_naming_superseded_obligation_is_a_finding",
    "unresolved-closes": "test_unresolved_source_caps_closure_at_partial",
    "argument-optional": "test_exclusion_without_argument_is_a_finding",
    "declared-credits": "test_declared_case_without_receipt_credits_nothing",
}


def load_module(workdir: Path):
    """Import the module under test from a copy, with the chosen seam applied."""
    src = (HERE / "requirement_status.py").read_text()
    if MUTATION:
        old, new = SEAMS[MUTATION]
        assert src.count(old) == 1, MUTATION
        src = src.replace(old, new, 1)
    target = workdir / "scripts"; target.mkdir(exist_ok=True)
    for name in ("records_sexp.py", "sexp.py", "record_catalog.py", "check_sexp_schema.py"):
        source = (HERE / name) if (HERE / name).exists() else (ROOT / "scripts" / name)
        shutil.copy(source, target / name)
    (target / "requirement_status.py").write_text(src)
    spec = importlib.util.spec_from_file_location("requirement_status_under_test", target / "requirement_status.py")
    module = importlib.util.module_from_spec(spec); spec.loader.exec_module(module)
    return module


def req(rid, obligations, *, status="planned", research="resolved", applicability="included",
        category="defined", impl=None):
    impl_text = f' (implementation_refs (artifact_id "{impl}") (locator "1"))' if impl else ""
    obs = " ".join(f'(obligation_ids "{o}")' for o in obligations)
    return (f'(requirement (id "{rid}") (profile_ids "fx-v0") (kind instruction) (statement "s") '
            f'(source_refs (source_id "SRC") (locator "1")) (applicability {applicability}) '
            f'(research_status {research}) (implementation_status {status}) '
            f'(source_semantics (category {category}) (detail "d")) (risk low) {obs}{impl_text})\n')


def obligation(oid):
    return (f'(obligation (id "{oid}") (contract_id "fx-env") (contract_version "1") (profile_ids "fx-v0") '
            f'(direction cpu-guarantee) (statement "s") (authority architecture) '
            f'(source_refs (source_id "SRC") (locator "1")) (parameters) (required_checks "c1"))\n')


def case(root, cid, bindings, *, credited=False, evaluation="pending", profile="fx-v0", receipt=None, nested=True):
    """A case directory in the real record shape: properties nested under (verification …)."""
    d = root / "evidence" / cid; d.mkdir(parents=True)
    props = " ".join(f'(property (id "p{i}") (requirement_id "{r}") ' + " ".join(f'(obligation_ids "{o}")' for o in obs) + ")"
                     for i, (r, obs) in enumerate(bindings))
    graph = f'(verification (format_version "matched-gpr-v1") {props})' if nested else props
    (d / "planned-experiment.sexp").write_text(f'(experiment (id "{cid}") (program "p.s") {graph})\n')
    body = receipt if receipt is not None else json.dumps(dict(case_id=cid, profile_id=profile, evaluation=evaluation,
                                                              disposition="pending", qualification=credited))
    (d / "verification.json").write_text(body)


def graph(root, requirements, obligations=("OB-A", "OB-B"), *, policy=True, profile="fx-v0"):
    p = root / "profiles" / profile; p.mkdir(parents=True)
    (p / "requirements.sexp").write_text("".join(requirements))
    (p / "contract-obligations.sexp").write_text("".join(obligation(o) for o in obligations))
    if policy:
        (p / "EVIDENCE_POLICY.md").write_text("# policy\n")
    return p


class StatusTests(unittest.TestCase):
    def setUp(self):
        base = ROOT / "target" / "tmp"; base.mkdir(parents=True, exist_ok=True)
        self._tmp = TemporaryDirectory(dir=str(base)); self.root = Path(self._tmp.name)
        self.M = load_module(self.root)

    def tearDown(self):
        self._tmp.cleanup()

    def run_root(self, root=None):
        return self.M.derive(root or self.root)

    def test_no_evidence_derives_planned(self):
        graph(self.root, [req("R1", ["OB-A"])])
        t = self.run_root()[0]
        self.assertEqual((t["derived"]["planned"], t["drift"], t["findings"]), (1, [], []))

    def test_credited_every_obligation_derives_implemented(self):
        graph(self.root, [req("R1", ["OB-A", "OB-B"], status="implemented")])
        case(self.root, "c1", [("R1", ["OB-A", "OB-B"])], credited=True, evaluation="satisfied")
        t = self.run_root()[0]
        self.assertEqual((t["rows"][0]["derived"], t["drift"], t["credited_cases"]), ("implemented", [], 1))

    def test_partially_credited_derives_partial(self):
        graph(self.root, [req("R1", ["OB-A", "OB-B"], status="partial")])
        case(self.root, "c1", [("R1", ["OB-A"])], credited=True, evaluation="satisfied")
        self.assertEqual(self.run_root()[0]["rows"][0]["derived"], "partial")

    def test_implementation_refs_without_evidence_derives_partial(self):
        graph(self.root, [req("R1", ["OB-A"], status="partial", impl="crate")])
        self.assertEqual(self.run_root()[0]["rows"][0]["derived"], "partial")

    def test_pending_case_stays_uncredited_and_planned(self):
        graph(self.root, [req("R1", ["OB-A"])])
        case(self.root, "c1", [("R1", ["OB-A"])], credited=False, evaluation="pending")
        row = self.run_root()[0]["rows"][0]
        self.assertEqual((row["derived"], row["uncredited"]), ("planned", ["c1:pending"]))

    def test_unresolved_source_caps_closure_at_partial(self):
        graph(self.root, [req("R1", ["OB-A"], status="partial", research="partial")])
        case(self.root, "c1", [("R1", ["OB-A"])], credited=True, evaluation="satisfied")
        row = self.run_root()[0]["rows"][0]
        self.assertEqual(row["derived"], "partial"); self.assertIn("caps closure", row["why"])

    def test_excluded_with_argument_derives_not_applicable(self):
        graph(self.root, [req("R1", ["OB-A"], status="not-applicable", applicability="excluded", category="not-applicable")])
        t = self.run_root()[0]
        self.assertEqual((t["rows"][0]["derived"], t["findings"]), ("not-applicable", []))

    def test_exclusion_without_argument_is_a_finding(self):
        graph(self.root, [req("R1", ["OB-A"], status="not-applicable", applicability="excluded")])
        t = self.run_root()[0]
        self.assertEqual(t["rows"][0]["derived"], "planned"); self.assertEqual(len(t["findings"]), 1)
        self.assertEqual(self.M.report([t])[0], 1)

    def test_recorded_status_drift_is_reported(self):
        graph(self.root, [req("R1", ["OB-A"], status="implemented")])
        t = self.run_root()[0]
        code, line, details = self.M.report([t])
        self.assertEqual((code, len(t["drift"])), (1, 1)); self.assertIn("drift or finding", line)
        self.assertTrue(any("R1" in d and "`implemented`" in d and "`planned`" in d for d in details))

    def test_case_naming_superseded_obligation_is_a_finding(self):
        graph(self.root, [req("R1", ["OB-A"])])
        case(self.root, "c1", [("R1", ["OB-OLD"])], credited=True, evaluation="satisfied")
        t = self.run_root()[0]
        self.assertEqual(t["rows"][0]["derived"], "planned")
        self.assertTrue(any("OB-OLD" in f and "effective contract" in f for f in t["findings"]))

    def test_case_naming_unknown_requirement_is_a_finding(self):
        graph(self.root, [req("R1", ["OB-A"])])
        case(self.root, "c1", [("R9", ["OB-A"])], credited=True)
        self.assertTrue(any("unknown requirement R9" in f for f in self.run_root()[0]["findings"]))

    def test_case_of_another_profile_is_not_counted(self):
        graph(self.root, [req("R1", ["OB-A"])])
        case(self.root, "c1", [("R1", ["OB-A"])], credited=True, profile="other-v0")
        t = self.run_root()[0]
        self.assertEqual((t["rows"][0]["derived"], t["cases"]), ("planned", 0))

    def test_profile_without_policy_is_not_judged(self):
        graph(self.root, [req("R1", ["OB-A"], status="implemented")], policy=False)
        self.assertEqual(self.run_root(), [])
        self.assertEqual(self.M.report([])[0], 0)

    def test_oversized_or_malformed_receipt_refuses(self):
        graph(self.root, [req("R1", ["OB-A"])])
        case(self.root, "c1", [("R1", ["OB-A"])], receipt="x" * (self.M.MAX_DOCUMENT_BYTES + 1))
        with self.assertRaises(self.M.Refused): self.run_root()
        shutil.rmtree(self.root / "evidence")
        case(self.root, "c2", [("R1", ["OB-A"])], receipt="{not json")
        with self.assertRaises(self.M.Refused): self.run_root()

    def test_declared_case_without_receipt_credits_nothing(self):
        """A planned record with no receipt is a declared case: counted, bound, never credited."""
        graph(self.root, [req("R1", ["OB-A"]), req("R2", ["OB-B"])])
        case(self.root, "c1", [("R1", ["OB-A"])])
        (self.root / "evidence" / "c1" / "verification.json").unlink()
        t = self.run_root()[0]
        self.assertEqual((t["cases"], t["credited_cases"], t["declared_cases"]), (1, 0, 1))
        self.assertEqual([r["derived"] for r in t["rows"]], ["planned", "planned"])
        self.assertEqual(t["rows"][0]["uncredited"], ["c1:declared"])
        self.assertEqual((t["drift"], t["findings"]), ([], []))
        self.assertIn("1 case(s), 0 credited, 1 declared", self.M.report([t])[1])
        # A declared case naming another profile's requirement belongs to neither profile.
        graph(self.root, [req("R9", ["OB-A"])], profile="fy-v0")
        tables = self.run_root()
        self.assertEqual([(x["profile"], x["cases"]) for x in tables], [("fx-v0", 1), ("fy-v0", 0)])
        # The directory must still carry the experiment it declares.
        (self.root / "evidence" / "c1" / "planned-experiment.sexp").write_text('(experiment (id "other"))\n')
        with self.assertRaises(self.M.Refused): self.run_root()

    def test_properties_are_read_under_verification_and_at_the_root(self):
        """The real records nest properties in the verification graph; a flat record still binds."""
        graph(self.root, [req("R1", ["OB-A"]), req("R2", ["OB-B"])])
        case(self.root, "c1", [("R1", ["OB-A"])], credited=True)
        case(self.root, "c2", [("R2", ["OB-B"])], credited=True, nested=False)
        t = self.run_root()[0]
        self.assertEqual([r["derived"] for r in t["rows"]], ["implemented", "implemented"])
        shutil.rmtree(self.root / "evidence")
        case(self.root, "c3", [], credited=True)
        with self.assertRaises(self.M.Refused): self.run_root()

    def test_case_without_declaration_refuses(self):
        graph(self.root, [req("R1", ["OB-A"])])
        case(self.root, "c1", [("R1", ["OB-A"])])
        (self.root / "evidence" / "c1" / "planned-experiment.sexp").unlink()
        with self.assertRaises(self.M.Refused): self.run_root()

    def test_cli_json_and_exit_codes(self):
        graph(self.root, [req("R1", ["OB-A"], status="implemented")])
        from contextlib import redirect_stdout, redirect_stderr
        from io import StringIO
        out, err = StringIO(), StringIO()
        with redirect_stdout(out), redirect_stderr(err):
            code = self.M.main(["--root", str(self.root), "--json"])
        table = json.loads(out.getvalue())
        self.assertEqual((code, table[0]["drift"][0]["id"]), (1, "R1")); self.assertIn("REQUIREMENT-STATUS:", err.getvalue())
        with redirect_stdout(out), redirect_stderr(err):
            self.assertEqual(self.M.main(["--root", str(self.root), "--profile", "missing"]), 2)

    def test_real_tree_has_no_drift(self):
        tables = self.run_root(ROOT)
        self.assertTrue(tables)
        for t in tables:
            self.assertEqual((t["drift"], t["findings"]), ([], []), t["profile"])
        self.assertEqual(self.M.report(tables)[0], 0)
        gc = next(t for t in tables if t["profile"] == "rv64gc-lab-v0")
        m = next(r for r in gc["rows"] if r["id"] == "REQ-GC-M")
        # Both retained cases bind REQ-GC-M and neither credits it: the retained case is pending,
        # the m-forms case is declared and awaits its capture.
        self.assertEqual(sorted(m["uncredited"]), ["rv64gc-m-forms-v3:declared", "rv64gc-signed-div-truncation-v2:pending"])
        self.assertEqual((gc["cases"], gc["credited_cases"], gc["declared_cases"]), (2, 0, 1))


def main():
    global MUTATION
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mutation", choices=sorted(SEAMS))
    MUTATION = parser.parse_args().mutation
    if MUTATION:
        suite = unittest.defaultTestLoader.loadTestsFromName(MUTATION_TESTS[MUTATION], StatusTests)
    else:
        suite = unittest.defaultTestLoader.loadTestsFromTestCase(StatusTests)
    result = unittest.TextTestRunner(stream=sys.stderr, verbosity=1).run(suite)
    print(f"REQUIREMENT-STATUS-PROBE: {result.testsRun} tests / {len(result.failures)} failures / {len(result.errors)} errors; derivation only, no qualification credit")
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    sys.exit(main())
