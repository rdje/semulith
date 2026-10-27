#!/usr/bin/env python3
"""Bounded controls for real contract owners; no reference process or CPU credit."""

from __future__ import annotations

import argparse
from copy import deepcopy
import os
from pathlib import Path
import signal
import subprocess
import sys
from tempfile import TemporaryDirectory
import unittest

import check_sexp_schema as K
import record_catalog as C
import records_sexp as R
import sexp as S

ROOT = Path(__file__).resolve().parent.parent
PROFILE = ROOT / "profiles/rv64gc-lab-v0"
DEADLINE_SECONDS = 3
MUTATION = None
FREEZE_GUARD = '''            if p in ancestry:
                findings.append(f"EXTENDS CYCLE {unit} [{vid}]: revisits {p}")
                break
'''
SCOPE_GUARD = '''            if v["version"] in ancestry:
                raise SystemExit(f"gate_report: {cdoc.relative_to(ROOT)}: CONTRACT CYCLE: "
                                 f"revisits version {v['version']}")
'''


def without_guard(source, guard):
    if source.count(guard) != 1:
        raise RuntimeError("ancestry mutation target must be singular")
    return source.replace(guard, "", 1)


def run_owner(owner, directory):
    """Run the real shell judge/public measure; join even a hanging omission.

    The deadline protects this diagnostic, not production runtime. Omitted guards
    must fail assertions rather than hanging a gate or leaving child processes.
    """
    if owner == "freeze":
        source = (ROOT / "scripts/check_contract_freeze.sh").read_text()
        if "judge() {" not in source:
            # XTASK.6 slice 6aj: the shell driver is a shim of `cargo xtask check-contract-freeze`; the judge is the
            # Rust module's verbatim constant — the same bytes the heredoc carried, rebuilt into the same shell function.
            module = (ROOT / "xtask/src/check_contract_freeze.rs").read_text()
            head, tail = 'const JUDGE: &str = r#"', '"#;'
            a = module.index(head) + len(head)
            source = "judge() {\npython3 - \"$1\" <<'PY'\n" + module[a:module.index(tail, a)] + "PY\n}\n# ── self-test"
        if MUTATION == "freeze-cycle":
            source = without_guard(source, FREEZE_GUARD)
        start, end = "judge() {", "# ── self-test"
        if source.count(start) != 1 or source.count(end) != 1:
            raise RuntimeError("real shell judge boundary changed")
        judge = source[source.index(start):source.index(end)]
        command = ["bash", "-c", judge + '\njudge "$1"', "ancestry-control",
                   str(directory.parent.parent)]
    else:
        source = (ROOT / "scripts/gate_report.py").read_text()
        if MUTATION == "scope-cycle":
            source = without_guard(source, SCOPE_GUARD)
        # Compile the complete owner with its original __file__, ordinary imports
        # and public function. Only the selected deliberate omission can differ.
        program = (
            "import sys;from pathlib import Path;sys.path.insert(0,'scripts');"
            "import records_sexp as R;"
            "ns={'__name__':'ancestry_owner','__file__':sys.argv[2]};"
            "exec(compile(sys.stdin.read(),sys.argv[2],'exec'),ns);"
            "d=Path(sys.argv[1]);"
            "print(ns['contract_measure'](d,R.load(d/'contract-obligations.sexp',"
            "root=d.parent.parent)))"
        )
        command = [sys.executable, *(["-O"] if sys.flags.optimize else []),
                   "-c", program, str(directory), str(ROOT / "scripts/gate_report.py")]
    environment = dict(os.environ, PYTHONOPTIMIZE=str(sys.flags.optimize))
    process = subprocess.Popen(command, cwd=ROOT, env=environment,
                               stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                               stderr=subprocess.STDOUT, start_new_session=True)
    try:
        payload = source.encode() if owner == "scope" else None
        output, _ = process.communicate(input=payload, timeout=DEADLINE_SECONDS)
        return process.returncode, output.decode("utf-8", errors="replace")
    except subprocess.TimeoutExpired:
        try:
            os.killpg(process.pid, signal.SIGKILL)
        except ProcessLookupError:
            pass  # The group can exit between the deadline and termination.
        output, _ = process.communicate()
        return 124, "ANCESTRY DEADLINE: owner did not terminate\n" + output.decode(
            "utf-8", errors="replace")


class AncestryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.contract = S.parse((PROFILE / "contract.sexp").read_text())
        cls.obligations = C.text(PROFILE / "contract-obligations.sexp")
        cls.schema = K.load_schema(ROOT / "schema/contract.sexp")
        # Independent current-data recount: all declared pairs minus explicit
        # superseded records; this fixture's real chain inherits every version.
        records = [R.form_to_dict(form) for form in S.parse(cls.obligations)
                   if form[0] != "comment"]
        removed = {S.field(child, "record", "supersession")
                   for form in cls.contract if form[0] == "contract"
                   for child in S.children(form, "supersede")}
        cls.expected_pairs = sorted((record["id"], check) for record in records
                                    if record["id"] not in removed
                                    for check in record["required_checks"])

    def setUp(self):
        base = ROOT / "target/contract-ancestry-controls"
        base.mkdir(parents=True, exist_ok=True)
        self.temporary = TemporaryDirectory(dir=base)
        self.addCleanup(self.temporary.cleanup)
        self.directory = Path(self.temporary.name) / "profiles/u"
        self.directory.mkdir(parents=True)
        (self.directory / "contract-obligations.sexp").write_text(self.obligations)
        self.forms = deepcopy(self.contract)

    def publish(self):
        text = R.render_forms(self.forms)
        self.assertEqual(K.validate_text(text, *self.schema, "ancestry fixture"), [])
        (self.directory / "contract.sexp").write_text(text)

    def versions(self):
        return sorted((form for form in self.forms if form[0] == "contract"),
                      key=lambda form: int(S.field(form, "version", "version")))

    def refuses_cycle(self):
        self.publish()
        for owner, reason in (("freeze", "EXTENDS CYCLE"), ("scope", "CONTRACT CYCLE")):
            with self.subTest(owner=owner):
                code, output = run_owner(owner, self.directory)
                self.assertEqual(code, 1, output)
                self.assertIn(reason, output)

    def test_real_acyclic_contract_preserves_frozen_and_effective_results(self):
        self.publish()
        code, output = run_owner("freeze", self.directory)
        self.assertEqual(code, 0, output)
        self.assertIn("0 finding(s)", output)
        code, output = run_owner("scope", self.directory)
        self.assertEqual(code, 0, output)
        # Output is the public pair of lists, emitted with Python repr. Parse
        # it with the standard literal reader, never eval executable data.
        import ast
        declared, realized = ast.literal_eval(output.strip())
        self.assertEqual(sorted(declared), self.expected_pairs)
        self.assertTrue(set(realized) <= set(declared))

    def test_self_cycle_refuses(self):
        latest = self.versions()[-1]
        latest[:] = [child for child in latest
                     if not (isinstance(child, list) and child[0] == "extends")]
        latest.append([S.Symbol("extends"), S.field(latest, "id", "latest")])
        self.refuses_cycle()

    def test_two_version_cycle_reached_from_latest_refuses(self):
        first, second = self.versions()[:2]
        first.append([S.Symbol("extends"), S.field(second, "id", "second")])
        self.refuses_cycle()

    def test_cycle_through_complete_ancestry_refuses(self):
        first, latest = self.versions()[0], self.versions()[-1]
        first.append([S.Symbol("extends"), S.field(latest, "id", "latest")])
        self.refuses_cycle()


def main():
    global MUTATION
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mutation", choices=("freeze-cycle", "scope-cycle"))
    args = parser.parse_args()
    MUTATION = args.mutation
    result = unittest.TextTestRunner(verbosity=2).run(
        unittest.defaultTestLoader.loadTestsFromTestCase(AncestryTests))
    print(f"CONTRACT-ANCESTRY: {result.testsRun} tests / {len(result.failures)} failures / "
          f"{len(result.errors)} errors; finite contract owners, no capture credit")
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    sys.exit(main())
