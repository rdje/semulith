#!/usr/bin/env python3
"""Behavioral probe of scripts/statement_trace.py: each way a trace can leave a clause out, or lie about a witness, refuses.

Run from the repository root; every fixture is synthetic, in a temporary directory on this repository's volume. `--mutation <seam>`
replaces one load-bearing predicate in a copy of the module, and that seam's test must then fail. P4-SYSTEM.14 a49-1.
"""
from __future__ import annotations

import argparse
import importlib.util
from pathlib import Path
import shutil
import sys
import tempfile
import unittest

import dispositions as DS

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
MUTATION = None
SEAMS = {
    "words-optional": ('    if have != want:\n', '    if False:\n'),
    "unknown-ok": ('    if unknown:\n', '    if False:\n'),
    "unread-ok": ('    if unread:\n', '    if False:\n'),
    "limit-anywhere": ('if limit not in limitation})', 'if False})'),
    "bare-ok": ('    if bare:\n', '    if False:\n'),
    "twice-ok": ('        _require(ids[0] not in trace, f"{path}: {ids[0]} is traced twice")\n', ''),
    "any-size": ('path.stat().st_size <= DOCUMENT_BYTES', 'True'),
}
MUTATION_TESTS = {
    "words-optional": "test_a_skipped_clause_refuses",
    "unknown-ok": "test_a_property_the_case_does_not_declare_refuses",
    "unread-ok": "test_a_property_standing_for_no_clause_refuses",
    "limit-anywhere": "test_a_limit_the_case_does_not_name_refuses",
    "bare-ok": "test_a_clause_with_neither_witness_nor_limit_refuses",
    "twice-ok": "test_a_requirement_traced_twice_refuses",
    "any-size": "test_an_oversized_catalogue_refuses",
}
STATEMENT = "First the one rule. Then the other rule, in two   parts."
ONE = dict(text="First the one rule.", properties=["p0"], limits=[])
TWO = dict(text="Then the other rule, in two parts.", properties=["p1"], limits=[])


def load_module(workdir: Path):
    src = (HERE / "statement_trace.py").read_text()
    if MUTATION:
        old, new = SEAMS[MUTATION]
        assert src.count(old) == 1, MUTATION
        src = src.replace(old, new, 1)
    target = workdir / "scripts"; target.mkdir(exist_ok=True)
    for name in ("sexp.py", "check_sexp_schema.py"):
        shutil.copy(HERE / name, target / name)
    (workdir / "schema").mkdir(exist_ok=True)
    shutil.copy(ROOT / "schema" / "statement-trace.sexp", workdir / "schema" / "statement-trace.sexp")
    (target / "statement_trace.py").write_text(src)
    spec = importlib.util.spec_from_file_location("statement_trace_under_test", target / "statement_trace.py")
    module = importlib.util.module_from_spec(spec); spec.loader.exec_module(module)
    return module


class Trace(unittest.TestCase):
    def setUp(self):
        (ROOT / "target" / "tmp").mkdir(parents=True, exist_ok=True)
        self.dir = tempfile.TemporaryDirectory(dir=ROOT / "target" / "tmp")
        self.root = Path(self.dir.name)
        self.M = load_module(self.root)
        self.profile = self.root / "profiles" / "fx"; self.profile.mkdir(parents=True)

    def tearDown(self):
        self.dir.cleanup()

    def holds(self, clauses, properties=("p0", "p1"), limitation="l"):
        return self.M.measure(STATEMENT, clauses, list(properties), limitation)

    def test_clauses_that_are_the_statement_hold_whatever_the_spacing(self):
        holds, measured = self.holds([ONE, TWO])
        self.assertTrue(holds, measured)
        self.assertIn("2 clauses are the statement's 11 words", measured)
        self.assertIn("all 2 properties stand for a clause", measured)

    def test_a_skipped_clause_refuses(self):
        holds, measured = self.holds([ONE], properties=("p0",))
        self.assertFalse(holds)
        self.assertIn("the clauses are not the statement", measured)

    def test_reordered_clauses_refuse(self):
        self.assertFalse(self.holds([TWO, ONE])[0])

    def test_a_word_added_refuses(self):
        holds, measured = self.holds([ONE, dict(TWO, text=TWO["text"] + " Mostly.")])
        self.assertFalse(holds)
        self.assertIn("the clauses are not the statement", measured)

    def test_a_property_the_case_does_not_declare_refuses(self):
        holds, measured = self.holds([ONE, dict(TWO, properties=["p1", "ghost"])])
        self.assertFalse(holds)
        self.assertIn("does not declare: ['ghost']", measured)

    def test_a_property_standing_for_no_clause_refuses(self):
        holds, measured = self.holds([ONE, TWO], properties=("p0", "p1", "p2"))
        self.assertFalse(holds)
        self.assertIn("stand for no clause: ['p2']", measured)

    def test_a_limit_the_case_does_not_name_refuses(self):
        holds, measured = self.holds([ONE, dict(TWO, properties=["p1"], limits=["not witnessed here"])], limitation="something else")
        self.assertFalse(holds)
        self.assertIn("not in the case's limitation", measured)

    def test_a_limit_the_case_names_stands_for_a_clause(self):
        holds, measured = self.holds([ONE, dict(TWO, properties=[], limits=["not witnessed here"])], properties=("p0",), limitation="this is not witnessed here; the rest is")
        self.assertTrue(holds, measured)
        self.assertIn("(1 name a limit)", measured)

    def test_a_clause_with_neither_witness_nor_limit_refuses(self):
        holds, measured = self.holds([ONE, dict(TWO, properties=[])], properties=("p0",))
        self.assertFalse(holds)
        self.assertIn("neither a witness nor a limit", measured)

    def write(self, text):
        (self.profile / "statement-trace.sexp").write_text(text)
        return self.M.load_trace(self.root, self.profile)

    def test_an_absent_catalogue_traces_nothing(self):
        self.assertEqual(self.M.load_trace(self.root, self.profile), {})

    def test_a_catalogue_reads_back_clause_by_clause(self):
        trace = self.write('(trace (requirement_id "R") (clause (text "a") (properties "p0") (properties "p1")) (clause (text "b") (limits "l")))\n')
        self.assertEqual(trace, {"R": [dict(text="a", properties=["p0", "p1"], limits=[]), dict(text="b", properties=[], limits=["l"])]})

    def test_a_requirement_traced_twice_refuses(self):
        with self.assertRaisesRegex(self.M.TraceRefused, "traced twice"):
            self.write('(trace (requirement_id "R") (clause (text "a") (limits "l")))\n(trace (requirement_id "R") (clause (text "b") (limits "l")))\n')

    def test_a_trace_with_no_clause_refuses(self):
        with self.assertRaises(self.M.TraceRefused):
            self.write('(trace (requirement_id "R"))\n')

    def test_an_oversized_catalogue_refuses(self):
        with self.assertRaisesRegex(self.M.TraceRefused, "bounded regular file"):
            self.write(";" + "x" * self.M.DOCUMENT_BYTES + "\n")

    def test_the_real_tree_traces_every_declared_case(self):
        real = load_real()
        profile = ROOT / "profiles" / "rv64gc-lab-v0"
        self.assertEqual(real.main(["--profile", "rv64gc-lab-v0"]), 0)
        # A requirement with nothing to run is traced from its disposition's declaration, as a case's is from its own (a51-12).
        declared = {requirement for requirement, row in DS.load(ROOT, profile).items() if row["kind"] == "record"}
        self.assertEqual(sorted(real.load_trace(ROOT, profile)), sorted(set(real._declared_cases(ROOT, "rv64gc-lab-v0")) | declared))


def load_real():
    spec = importlib.util.spec_from_file_location("statement_trace_real", HERE / "statement_trace.py")
    module = importlib.util.module_from_spec(spec); spec.loader.exec_module(module)
    return module


def main():
    global MUTATION
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mutation", choices=sorted(SEAMS))
    MUTATION = parser.parse_args().mutation
    suite = (unittest.defaultTestLoader.loadTestsFromName(MUTATION_TESTS[MUTATION], Trace) if MUTATION
             else unittest.defaultTestLoader.loadTestsFromTestCase(Trace))
    result = unittest.TextTestRunner(stream=sys.stderr, verbosity=1).run(suite)
    print(f"STATEMENT-TRACE-PROBE: {result.testsRun} tests / {len(result.failures)} failures / {len(result.errors)} errors; synthetic traces, no capture credit")
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    sys.exit(main())
