#!/usr/bin/env python3
"""Policy-leg measurement controls on synthetic retained cases; measurement only, no credit."""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
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
    "credit-pending": ('    missing = [leg.id for leg in legs if leg.disposition != "satisfied"]\n', '    missing = []\n'),
    "trust-receipt": ('    if receipt.get("qualification") is True and missing:\n', '    if False:\n'),
    "infer-feature": ('    feature = [FEATURE_DISPOSITIONS.get(ob) for ob in obligation_ids]\n',
                      '    feature = [FEATURE_DISPOSITIONS.get(ob, "none applies (inferred)") for ob in obligation_ids]\n'),
    "any-control": ('    at_witness = diff.get("step_n") == witness_step and observed == {witness_register}\n',
                    '    at_witness = True\n'),
    "coverage-optional": ('    _leg(legs, "form-coverage", bool(required) and predeclared == required,\n',
                          '    _leg(legs, "form-coverage", bool(required),\n'),
    "lock-stale": ('    stale = method.get("disposition") == "stale"\n', '    stale = False\n'),
    "first-property": ('    witness_step, witness_register = witnesses[named[0]]\n',
                       '    witness_step, witness_register = next(iter(witnesses.values()))\n'),
}
MUTATION_TESTS = {
    "credit-pending": "test_undeclared_boundary_rows_keep_the_case_pending",
    "trust-receipt": "test_receipt_claiming_qualification_is_a_finding",
    "infer-feature": "test_undeclared_feature_disposition_is_pending",
    "any-control": "test_control_diverging_elsewhere_is_pending",
    "coverage-optional": "test_partial_form_coverage_is_pending",
    "lock-stale": "test_stale_method_is_invalidated_not_blocked",
    "first-property": "test_control_leg_reads_the_property_the_control_run_names",
}
METHOD = dict(disposition="satisfied", capture_binding="matched", record_disposition="valid",
              charged_read_bytes=1, record_sha256="a", planned_sha256="b")
STALE = dict(METHOD, disposition="stale", capture_binding=None, record_disposition=None,
             reason="evidence/cx/dependencies.sexp: pinned bytes differ")


def moved_inputs(root: Path, case_id: str) -> list[str]:
    """Pinned inputs whose current bytes differ from the case's manifest — read independently of the method."""
    sys.path.insert(0, str(root / "scripts"))
    import sexp as S
    forms = S.parse((root / "evidence" / case_id / "dependencies.sexp").read_text())
    manifest = next(f for f in forms if isinstance(f, list) and f and str(f[0]) == "dependencies")
    moved = []
    for item in S.children(manifest, "input"):
        path, pin = str(S.children(item, "path")[0][1]), str(S.children(item, "sha256")[0][1])
        target = root / path
        if not target.is_file() or hashlib.sha256(target.read_bytes()).hexdigest() != pin:
            moved.append(path)
    return moved


def load_module(workdir: Path):
    """Import the module under test from a copy, with the chosen seam applied."""
    src = (HERE / "review_div_policy.py").read_text()
    if MUTATION:
        old, new = SEAMS[MUTATION]
        assert src.count(old) == 1, MUTATION
        src = src.replace(old, new, 1)
    target = workdir / "scripts"; target.mkdir(exist_ok=True)
    for name in ("records_sexp.py", "sexp.py", "record_catalog.py", "check_sexp_schema.py"):
        shutil.copy(ROOT / "scripts" / name, target / name)
    (target / "review_div_policy.py").write_text(src)
    spec = importlib.util.spec_from_file_location("review_div_policy_under_test", target / "review_div_policy.py")
    module = importlib.util.module_from_spec(spec); sys.modules[spec.name] = module; spec.loader.exec_module(module)
    return module


def fixture(root: Path, *, obligation="OB-GC-M", insns=("div", "rem"), risk="medium", declare_boundaries=False,
            steps=None, expected_reads_reference=False, repeat=True, control="DIVERGE", control_step=0,
            control_register="x7", qualification=False, stale_policy=False, witness_source="SRC §1",
            control_property="p0"):
    """One synthetic retained case under profile fx-v0; every knob breaks exactly one leg."""
    profile = root / "profiles" / "fx-v0"; profile.mkdir(parents=True)
    obs = " ".join(f'(insns "{i}")' for i in insns)
    (profile / "requirements.sexp").write_text(
        f'(requirement (id "REQ-X") (profile_ids "fx-v0") (kind instruction) (statement "s") {obs} '
        f'(source_refs (source_id "SRC") (locator "1")) (applicability included) (research_status resolved) '
        f'(implementation_status planned) (source_semantics (category defined) (detail "d")) (risk {risk}) '
        f'(obligation_ids "{obligation}"))\n')
    (profile / "contract-obligations.sexp").write_text(
        f'(obligation (id "{obligation}") (contract_id "fx-env") (contract_version "1") (profile_ids "fx-v0") '
        f'(direction cpu-guarantee) (statement "s") (authority architecture) (source_refs (source_id "SRC") (locator "1")) '
        f'(parameters) (required_checks "c1"))\n')
    policy = b"# policy\n"; (profile / "EVIDENCE_POLICY.md").write_bytes(policy)
    case = root / "evidence" / "cx"; case.mkdir(parents=True)
    steps = steps or [(0, "div x7, x5, x6", witness_source), (1, "rem x8, x5, x6", "SRC §1 (Table 1)"),
                      (2, "div x9, x5, x0", "SRC §1 (Table 1)")]
    (case / "baseline.expected.sexp").write_text(
        '(expectations (program "p.s") (entry "0x0") (instructions 3) (fetches 6)\n' + "".join(
            f'  (step (n {n}) (insn "{insn}") (writes (write (reg "x7") (value "0x1"))) (derivation "d") (source "{source}"))\n'
            for n, insn, source in steps) + ')\n')
    props = [f'(property (id "p0") (requirement_id "REQ-X") (obligation_ids "{obligation}") (observation_kinds "gpr-change") '
             f'(statement "s") (gpr_witness (step_n 0) (register "x7")))']
    if declare_boundaries:
        props += [f'(property (id "p{n}") (requirement_id "REQ-X") (obligation_ids "{obligation}") (observation_kinds "gpr-change") '
                  f'(statement "s") (gpr_witness (step_n {n}) (register "x7")))' for n, _, s in steps if "Table" in s]
    expected_inputs = '(input_ids "guest-source") (input_ids "expectation")' + (
        ' (input_ids "reference-config")' if expected_reads_reference else "")
    control_run = (f'(control_run (id "c0") (run_id "control") (baseline_id "baseline") (mutation_input_ids "mutant-expectation") '
                   f'(property_ids "{control_property}") (expected_verdict "DIVERGE") (observed_verdict "{control}") (reason "r"))')
    (case / "planned-experiment.sexp").write_text(
        '(experiment (id "cx") (program "p.s") (instructions 3) (models "m") (verdict "AGREE") (reproduced "r") (control "c")\n'
        '  (verification (format_version "matched-gpr-v1") (comparison_rule "rule-v1") (limitations "l")\n    '
        + "\n    ".join(props) + '\n    ' + control_run + '\n'
        '    (input (id "guest-source") (role "guest-source") (path "profiles/fx-v0/guests/p.s") (sha256 "0"))\n'
        '    (input (id "collector") (role "collector") (path "scripts/c.py") (sha256 "0"))\n'
        '    (input (id "reference-config") (role "reference-config") (path "evidence/cx/ref.json") (sha256 "0"))\n'
        '    (input (id "reference-identity") (role "reference-identity") (path "profiles/fx-v0/retained/id.sexp") (sha256 "0"))\n'
        '    (input (id "expectation") (role "expectation") (path "evidence/cx/baseline.expected.sexp") (sha256 "0"))\n'
        '    (input (id "mutant-expectation") (role "expectation") (path "evidence/cx/control.expected.sexp") (sha256 "0"))\n'
        '    (producer (id "reference") (role "reference") (version "v") (candidate_id "m") (input_ids "guest-source") '
        '(input_ids "reference-config") (input_ids "reference-identity"))\n'
        f'    (producer (id "expected") (role "expected") (version "v") {expected_inputs})))\n')
    runs = [dict(run_kind="baseline", comparison=dict(verdict="AGREE", gpr_difference=None))]
    if repeat:
        runs.append(dict(run_kind="repeat", comparison=dict(verdict="AGREE", gpr_difference=None)))
    diff = None if control != "DIVERGE" else dict(step_n=control_step, observed=[[control_register, 1]], expected=[[control_register, 2]])
    runs.append(dict(run_kind="control", comparison=dict(verdict=control, gpr_difference=diff)))
    (case / "verification.json").write_text(json.dumps(dict(
        case_id="cx", profile_id="fx-v0", qualification=qualification, evaluation="pending", disposition="pending",
        limitations=["l"], comparison=dict(runs=runs))))
    pin = hashlib.sha256(policy).hexdigest() if not stale_policy else "0" * 64
    (case / "dependencies.sexp").write_text(
        f'(dependencies (format_version "v") (input (id "d1") (role "dependency") (path "profiles/fx-v0/EVIDENCE_POLICY.md") (sha256 "{pin}")))\n')
    return case


class PolicyTests(unittest.TestCase):
    def setUp(self):
        base = ROOT / "target" / "tmp"; base.mkdir(parents=True, exist_ok=True)
        self._tmp = TemporaryDirectory(dir=str(base)); self.root = Path(self._tmp.name)
        self.M = load_module(self.root)

    def tearDown(self):
        self._tmp.cleanup()

    def measure(self, method=METHOD, case="cx"):
        return self.M.measure_policy(self.root, method=dict(method), case_id=case)

    def legs(self, table):
        return {leg["id"]: leg["disposition"] for leg in table["legs"]}

    def test_every_leg_satisfied_grants_no_credit(self):
        fixture(self.root, declare_boundaries=True)
        t = self.measure()
        self.assertEqual((t["disposition"], t["missing"], t["findings"], t["credited"]), ("satisfied", [], [], False))
        self.assertEqual(set(self.legs(t).values()), {"satisfied"})
        self.assertEqual(t["coverage"], dict(required=["div", "rem"], exercised=["div", "rem"], predeclared=["div", "rem"]))

    def test_undeclared_boundary_rows_keep_the_case_pending(self):
        fixture(self.root, insns=("div",))
        t = self.measure()
        self.assertEqual((t["disposition"], t["missing"]), ("pending", ["boundary-fixtures"]))
        self.assertEqual(t["boundary"], dict(present=[1, 2], predeclared=[]))
        self.assertFalse(t["credited"])

    def test_partial_form_coverage_is_pending(self):
        fixture(self.root, insns=("div", "rem", "mul"), declare_boundaries=True)
        t = self.measure()
        self.assertEqual(t["missing"], ["form-coverage"]); self.assertIn("2 of 3 forms predeclared", self.legs_text(t, "form-coverage"))

    def legs_text(self, table, leg_id):
        return next(leg["measured"] for leg in table["legs"] if leg["id"] == leg_id)

    def test_expectation_step_without_source_is_pending(self):
        fixture(self.root, declare_boundaries=True,
                steps=[(0, "div x7, x5, x6", "SRC §1"), (1, "rem x8, x5, x6", ""), (2, "div x9, x5, x0", "SRC §1 (Table 1)")])
        self.assertIn("source-located-expectations", self.measure()["missing"])

    def test_witness_not_citing_requirement_source_is_pending(self):
        fixture(self.root, declare_boundaries=True, witness_source="OTHER §9")
        self.assertEqual(self.measure()["missing"], ["source-located-expectations"])

    def test_expected_producer_reading_reference_inputs_is_pending(self):
        fixture(self.root, declare_boundaries=True, expected_reads_reference=True)
        t = self.measure()
        self.assertEqual(t["missing"], ["source-located-expectations"]); self.assertIn("reads reference inputs", self.legs_text(t, "source-located-expectations"))

    def test_missing_repeat_run_is_pending(self):
        fixture(self.root, declare_boundaries=True, repeat=False)
        self.assertEqual(self.measure()["missing"], ["repeated-execution"])

    def test_agreeing_control_is_pending(self):
        fixture(self.root, declare_boundaries=True, control="AGREE")
        self.assertEqual(self.measure()["missing"], ["discriminating-control"])

    def test_control_diverging_elsewhere_is_pending(self):
        fixture(self.root, declare_boundaries=True, control_step=1, control_register="x8")
        t = self.measure()
        self.assertEqual(t["missing"], ["discriminating-control"]); self.assertIn("witness step 0 x7", self.legs_text(t, "discriminating-control"))

    def test_control_leg_reads_the_property_the_control_run_names(self):
        """The control changes p1's value (step 1, x7): named, the leg is satisfied; the first property is not it."""
        fixture(self.root, declare_boundaries=True, control_step=1, control_property="p1")
        t = self.measure()
        self.assertEqual((t["disposition"], t["missing"]), ("satisfied", []))
        self.assertIn("witness step 1 x7", self.legs_text(t, "discriminating-control"))
        self.tearDown(); self.setUp()
        fixture(self.root, declare_boundaries=True, control_step=1, control_property="p0")
        self.assertEqual(self.measure()["missing"], ["discriminating-control"])
        self.tearDown(); self.setUp()
        case = fixture(self.root, declare_boundaries=True, control_property="absent")
        with self.assertRaises(self.M.Refused): self.measure()
        planned = case / "planned-experiment.sexp"
        sibling = '(control_run (id "c1") (run_id "control") (property_ids "p0") (expected_verdict "DIVERGE") (observed_verdict "DIVERGE") (reason "r"))\n    '
        planned.write_text(planned.read_text().replace('(control_run (id "c0")', sibling + '(control_run (id "c0")', 1))
        with self.assertRaises(self.M.Refused): self.measure()

    def test_receipt_claiming_qualification_is_a_finding(self):
        fixture(self.root, qualification=True)
        t = self.measure()
        self.assertEqual(t["disposition"], "pending"); self.assertEqual(len(t["findings"]), 1)
        self.assertIn("claims qualification", t["findings"][0]); self.assertEqual(self.M.summary(t)[0], 1)
        self.assertFalse(t["credited"])

    def test_unsatisfied_method_is_blocked(self):
        fixture(self.root, declare_boundaries=True)
        for disposition in ("refused", "unavailable", "unsupported"):
            t = self.measure(method=dict(METHOD, disposition=disposition, capture_binding=None))
            self.assertEqual((t["disposition"], self.M.summary(t)[0], t["invalidated_by"]), ("blocked", 1, None), disposition)
            self.assertIn("matched-reference-comparison", t["missing"]); self.assertIn("currentness", t["missing"])
            self.assertIn("legs measured but blocked", t["findings"][0])

    def test_stale_method_is_invalidated_not_blocked(self):
        fixture(self.root, declare_boundaries=True)
        t = self.measure(method=STALE)
        self.assertEqual((t["disposition"], t["findings"], t["credited"]), ("invalidated", [], False))
        self.assertEqual(t["missing"], ["matched-reference-comparison", "currentness"])
        self.assertEqual(t["invalidated_by"], STALE["reason"]); self.assertEqual(t["method"]["reason"], STALE["reason"])
        code, line = self.M.summary(t)
        self.assertEqual(code, 0); self.assertIn("DIV-POLICY: invalidated — 8 of 10", line)
        self.assertIn("invalidated by evidence/cx/dependencies.sexp", line); self.assertIn("no qualification credit", line)

    def test_qualification_over_invalidated_method_is_a_finding(self):
        fixture(self.root, declare_boundaries=True, qualification=True)
        t = self.measure(method=STALE)
        self.assertEqual((t["disposition"], len(t["findings"]), t["credited"]), ("invalidated", 1, False))
        self.assertIn("claims qualification", t["findings"][0]); self.assertEqual(self.M.summary(t)[0], 1)

    def test_high_risk_requires_a_second_method(self):
        fixture(self.root, declare_boundaries=True, risk="high")
        t = self.measure()
        self.assertEqual(t["missing"], ["risk-method"]); self.assertIn("second method", self.legs_text(t, "risk-method"))

    def test_undeclared_feature_disposition_is_pending(self):
        fixture(self.root, obligation="OB-Y", declare_boundaries=True)
        t = self.measure()
        self.assertEqual(t["missing"], ["feature-rules"]); self.assertIn("undeclared", self.legs_text(t, "feature-rules"))

    def test_changed_policy_breaks_currentness(self):
        fixture(self.root, declare_boundaries=True, stale_policy=True)
        t = self.measure()
        self.assertEqual(t["missing"], ["currentness"]); self.assertIn("changed since the pin", self.legs_text(t, "currentness"))

    def test_oversize_declaration_refuses(self):
        case = fixture(self.root, declare_boundaries=True)
        planned = case / "planned-experiment.sexp"
        planned.write_text(planned.read_text() + '(comment "' + "x" * 65536 + '")\n')
        with self.assertRaises(self.M.Refused): self.measure()

    def test_unknown_case_refuses(self):
        fixture(self.root)
        with self.assertRaises(self.M.Refused): self.measure(case="absent")

    def test_cli_json_and_exit_codes(self):
        fixture(self.root)
        method = self.root / "method.json"; method.write_text(json.dumps(METHOD))
        from contextlib import redirect_stdout, redirect_stderr
        from io import StringIO
        out, err = StringIO(), StringIO()
        with redirect_stdout(out), redirect_stderr(err):
            code = self.M.main(["--root", str(self.root), "--case", "cx", "--method-json", str(method), "--json"])
        table = json.loads(out.getvalue())
        self.assertEqual((code, table["disposition"], table["credited"]), (0, "pending", False)); self.assertIn("DIV-POLICY: pending", err.getvalue())
        with redirect_stdout(out), redirect_stderr(err):
            self.assertEqual(self.M.main(["--root", str(self.root), "--case", "absent", "--method-json", str(method)]), 2)

    def test_output_is_deterministic_and_bounded(self):
        fixture(self.root, declare_boundaries=True)
        first, second = self.measure(), self.measure()
        self.assertEqual(first, second); self.assertLessEqual(len(json.dumps(first).encode()), 65536)

    def test_real_tree_measures_as_its_manifest_predicts(self):
        """Current pins: pending with two legs missing. A moved pin: invalidated, naming it, no finding."""
        import subprocess
        moved = moved_inputs(ROOT, self.M.CASE_ID)
        done = subprocess.run([sys.executable, "-B", str(ROOT / "scripts" / "review_div_method.py")],
                              capture_output=True, text=True, cwd=str(ROOT))
        self.assertEqual(done.returncode, 1 if moved else 0, done.stdout + done.stderr)
        table = self.M.measure_policy(ROOT, method=json.loads(done.stdout))
        if moved:
            self.assertEqual((table["disposition"], table["missing"], table["findings"], table["credited"]),
                             ("invalidated", ["boundary-fixtures", "matched-reference-comparison", "currentness", "form-coverage"], [], False))
            self.assertEqual(sum(1 for leg in table["legs"] if leg["disposition"] == "satisfied"), 6)
            self.assertEqual(table["method"]["disposition"], "stale"); self.assertEqual(self.M.summary(table)[0], 0)
            self.assertTrue(table["invalidated_by"], table["method"])
        else:
            self.assertEqual((table["disposition"], table["missing"], table["findings"], table["credited"]),
                             ("pending", ["boundary-fixtures", "form-coverage"], [], False))
            self.assertEqual(sum(1 for leg in table["legs"] if leg["disposition"] == "satisfied"), 8)
            self.assertIsNone(table["invalidated_by"])
        self.assertEqual(table["boundary"], dict(present=[10, 11, 12, 13, 17, 19], predeclared=[]))
        self.assertEqual((table["coverage"]["predeclared"], table["coverage"]["exercised"], len(table["coverage"]["required"])),
                         (["div"], ["div", "divu", "rem", "remu"], 13))
        self.assertEqual((table["requirement_id"], table["obligation_ids"], table["category"], table["risk"]),
                         ("REQ-GC-M", ["OB-GC-M"], "defined", "medium"))


def main():
    global MUTATION
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mutation", choices=sorted(SEAMS))
    MUTATION = parser.parse_args().mutation
    if MUTATION:
        suite = unittest.defaultTestLoader.loadTestsFromName(MUTATION_TESTS[MUTATION], PolicyTests)
    else:
        suite = unittest.defaultTestLoader.loadTestsFromTestCase(PolicyTests)
    result = unittest.TextTestRunner(stream=sys.stderr, verbosity=1).run(suite)
    print(f"DIV-POLICY-PROBE: {result.testsRun} tests / {len(result.failures)} failures / {len(result.errors)} errors; measurement only, no qualification credit")
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    sys.exit(main())
