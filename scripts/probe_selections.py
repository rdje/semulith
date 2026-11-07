#!/usr/bin/env python3
"""Controls for a selection's record and a credit with no case (`selections.py`, P4-SYSTEM.14 a51-11).

A small frozen tree in scratch, with grammars from `scripts/fixtures/selections/`, so a damaged real catalogue is that catalogue's
finding and no control here misses for it. No real requirement is credited, and nothing here runs a real check.
"""
from __future__ import annotations

import argparse
import hashlib
from pathlib import Path
import shutil
import sys
import tempfile
import types
import unittest

import credit_records as CR
import records_sexp as R
import requirement_status as RS
import selections as M
import statement_trace as ST

ROOT = Path(__file__).resolve().parent.parent
FROZEN = ROOT / "scripts/fixtures/selections"
MUTATIONS = {
    "live-fact": ("                if record[\"facts\"].get(name) != live.get(name):\n", "                if False:\n"),
    "expected": ("        if record[\"facts\"][name] != expected[name]:\n", "        if False:\n"),
    "declared-set": ("    if set(expected) != set(record[\"facts\"]):\n", "    if False:\n"),
    "kind": ("    if declared is None or declared[\"kind\"] != \"record\":\n        reasons.append", "    if declared is None:\n        reasons.append"),
    "required-check": ("        if check not in served:\n", "        if False:\n"),
    "run-rc": ("        if run[\"rc\"] != 0:\n", "        if False:\n"),
    "repeat": ("        if run[\"repeated\"] != \"identical\":\n", "        if False:\n"),
    "trace": ("        if not held:\n            reasons.append(f\"statement trace", "        if False:\n            reasons.append(f\"statement trace"),
    "reuse": ("    if record_path(profile_dir, selection.id).exists():\n", "    if False:\n"),
    "undeclared-run": ("    if declared is None or declared[\"kind\"] != \"record\":\n        raise", "    if False:\n        raise"),
    "unremembered-read": ("        self.read_paths.add(path)\n        return target.read_bytes()\n", "        return target.read_bytes()\n"),
}
STATEMENT = "The fixture selects one thing. It stays selected."
SEL = "SEL-FIXTURE"
REQ = "REQ-FIXTURE"
OB = "OB-FIXTURE"


def requirement(status="planned"):
    return {"id": REQ, "profile_ids": ["fixture"], "kind": "configuration", "statement": STATEMENT,
            "source_refs": [{"source_id": "SRC-FIXTURE", "locator": "§1"}], "applicability": "included", "research_status": "resolved",
            "implementation_status": status, "source_semantics": {"category": "implementation-defined", "detail": "A selection."},
            "risk": "low", "obligation_ids": [OB], "dependencies": [], "implementation_refs": [], "evidence_ids": []}


def obligation():
    return {"id": OB, "contract_id": "fixture", "contract_version": "0", "profile_ids": ["fixture"], "direction": "cpu-guarantee",
            "statement": STATEMENT, "authority": "laboratory", "source_refs": [{"source_id": "SRC-FIXTURE", "locator": "§1"}],
            "parameters": {"requirement_id": REQ}, "dependencies": [], "required_checks": ["CHK-FIXTURE-POS", "CHK-FIXTURE-NEG"]}


DISPOSITION = ('(disposition (id "DS-FIXTURE") (requirement_id "REQ-FIXTURE") (kind record) (source_id "SRC-FIXTURE") (source_locator "§1")\n'
               '  (argument "A selection, with nothing to run.") (controls "the named negative check")\n'
               '  (expect (fact "chosen") (value "one")) (expect (fact "held") (value "yes")))\n')
TRACE = ('(trace (requirement_id "REQ-FIXTURE")\n  (clause (text "The fixture selects one thing.") (properties "chosen"))\n'
         '  (clause (text "It stays selected.") (properties "held") (limits "a limit")))\n')


def fixture_facts(reader: M.Reader) -> dict[str, str]:
    chosen = reader.text("fact.txt").strip()
    return {"chosen": chosen, "held": "yes" if reader.bytes("held.txt") else "no"}


def table(root: Path) -> dict:
    ok = (sys.executable, "-c", "print('the check holds')")
    return {REQ: M.Selection(SEL, REQ, fixture_facts, (M.Run(ok, ("CHK-FIXTURE-POS",)), M.Run(ok, ("CHK-FIXTURE-NEG",))), ("a limit",))}


class Tree(unittest.TestCase):
    def setUp(self):
        base = ROOT / "target/selections-probe"
        base.mkdir(parents=True, exist_ok=True)
        self.scratch = tempfile.TemporaryDirectory(dir=base)
        self.root = Path(self.scratch.name)
        (self.root / "schema").mkdir()
        for name in ("dispositions", "statement-trace", "credits"):
            shutil.copy(FROZEN / f"schema-{name}.sexp", self.root / f"schema/{name}.sexp")
        self.unit = self.root / "profiles/fixture"
        self.unit.mkdir(parents=True)
        (self.unit / "requirements.sexp").write_text(R.dump([requirement()]))
        (self.unit / "contract-obligations.sexp").write_text(R.dump([obligation()]))
        (self.unit / "dispositions.sexp").write_text(DISPOSITION)
        (self.unit / "statement-trace.sexp").write_text(TRACE)
        (self.root / "fact.txt").write_text("one\n")
        (self.root / "held.txt").write_text("held\n")
        self.table = table(self.root)

    def tearDown(self):
        self.scratch.cleanup()

    def take(self):
        text = M.build_record(self.root, self.unit, self.table[REQ], "2026-11-07")
        path = M.record_path(self.unit, SEL)
        path.parent.mkdir(exist_ok=True)
        path.write_text(text)
        return path

    def reasons(self):
        return M.review(self.root, self.unit, SEL, REQ, [OB], selections=self.table)

    def edit(self, path: Path, old: str, new: str):
        text = path.read_text()
        self.assertIn(old, text)
        path.write_text(text.replace(old, new))


class RecordTests(Tree):
    def test_a_taken_record_stands(self):
        self.take()
        self.assertEqual(self.reasons(), [])

    def test_a_record_names_what_it_read_and_ran(self):
        text = self.take().read_text()
        for word in ('(path "fact.txt")', '(path "held.txt")', hashlib.sha256(b"one\n").hexdigest(), '(serves "CHK-FIXTURE-NEG")',
                     '(output "the check holds")', "(repeated identical)", '(fact (id "chosen") (observed "one"))', '(limitation "a limit")'):
            self.assertIn(word, text)
        self.assertNotIn(str(self.root), text)
        self.assertNotIn(sys.executable, text)

    def test_a_second_record_is_refused(self):
        self.take()
        with self.assertRaisesRegex(M.SelectionRefused, "already holds a record"):
            M.build_record(self.root, self.unit, self.table[REQ], "2026-11-07")

    def test_nothing_runs_before_a_disposition_is_declared(self):
        (self.unit / "dispositions.sexp").unlink()
        with self.assertRaisesRegex(M.SelectionRefused, "no kind record disposition is declared"):
            M.build_record(self.root, self.unit, self.table[REQ], "2026-11-07")

    def test_a_reader_reading_other_facts_is_refused(self):
        (self.unit / "dispositions.sexp").write_text(DISPOSITION.replace('"held"', '"other"'))
        with self.assertRaisesRegex(M.SelectionRefused, "the disposition declares"):
            M.build_record(self.root, self.unit, self.table[REQ], "2026-11-07")

    def test_a_moved_fact_lapses_it_by_name(self):
        self.take()
        (self.root / "fact.txt").write_text("two\n")
        self.assertEqual(self.reasons(), ["fact chosen: the tree reads 'two', the record 'one'"])

    def test_bytes_that_keep_the_fact_do_not_lapse_it(self):
        self.take()
        (self.root / "fact.txt").write_text("one\n\n")
        self.assertEqual(self.reasons(), [])

    def test_an_observation_the_disposition_did_not_expect_lapses_it(self):
        self.take()
        (self.unit / "dispositions.sexp").write_text(DISPOSITION.replace('(value "one")', '(value "uno")'))
        self.assertEqual(self.reasons(), ["fact chosen: observed 'one', the disposition expects 'uno'"])

    def test_a_declared_fact_the_record_lacks_lapses_it(self):
        self.take()
        (self.unit / "dispositions.sexp").write_text(DISPOSITION.replace('(expect (fact "held") (value "yes"))', '(expect (fact "held") (value "yes")) (expect (fact "new") (value "x"))'))
        self.assertTrue(any("differ from the record's" in r for r in self.reasons()), self.reasons())

    def test_a_requirement_answered_by_a_case_has_no_record(self):
        self.take()
        as_case = DISPOSITION.replace("(kind record)", '(kind case) (control_property "p")').replace('\n  (expect (fact "chosen") (value "one")) (expect (fact "held") (value "yes"))', "")
        (self.unit / "dispositions.sexp").write_text(as_case)
        self.assertEqual(self.reasons(), [f"no kind record disposition answers {REQ}"])

    def test_a_required_check_nothing_served_lapses_it(self):
        path = self.take()
        self.edit(path, '(serves "CHK-FIXTURE-NEG") ', "")
        self.assertEqual(self.reasons(), ["required check CHK-FIXTURE-NEG: no retained run serves it"])

    def test_a_failed_run_lapses_it(self):
        path = self.take()
        self.edit(path, "(rc 0)", "(rc 1)")
        self.assertEqual(len(self.reasons()), 2, self.reasons())
        self.assertIn("exit 1", self.reasons()[0])

    def test_a_repeat_that_differs_lapses_it(self):
        path = self.take()
        self.edit(path, "(repeated identical)", "(repeated different)")
        self.assertIn("its repeat differs", self.reasons()[0])

    def test_a_run_that_differs_when_repeated_is_retained_as_different(self):
        counter = self.root / "count.txt"
        code = ("from pathlib import Path; p = Path('count.txt'); n = int(p.read_text()) if p.exists() else 0; p.write_text(str(n + 1)); print(n)")
        ok = (sys.executable, "-c", "print('held')")
        selection = M.Selection(SEL, REQ, fixture_facts, (M.Run((sys.executable, "-c", code), ("CHK-FIXTURE-POS",)), M.Run(ok, ("CHK-FIXTURE-NEG",))), ("a limit",))
        self.assertIn("(repeated different)", M.build_record(self.root, self.unit, selection, "2026-11-07"))
        self.assertEqual(counter.read_text(), "2")

    def test_a_record_that_does_not_read_is_a_reason(self):
        self.take().write_text("(selection (id")
        self.assertIn("record unreadable", self.reasons()[0])

    def test_a_record_outside_the_grammar_is_a_reason(self):
        path = self.take()
        self.edit(path, "(limitation", "(limit")
        self.assertIn("record unreadable", self.reasons()[0])

    def test_a_clause_outside_the_statement_lapses_it(self):
        self.take()
        (self.unit / "statement-trace.sexp").write_text(TRACE.replace("It stays selected.", "It stays."))
        self.assertIn("statement trace: the clauses are not the statement", self.reasons()[0])

    def test_no_trace_lapses_it(self):
        self.take()
        (self.unit / "statement-trace.sexp").unlink()
        self.assertEqual(self.reasons(), [f"{REQ} has no statement trace"])

    def test_a_symlink_is_not_a_fact(self):
        self.take()
        (self.root / "fact.txt").unlink()
        (self.root / "fact.txt").symlink_to("held.txt")
        self.assertIn("facts cannot be read", self.reasons()[0])


class CreditTests(Tree):
    def pin(self, path: Path) -> str:
        data = path.read_bytes()
        return f'(pin (path "{path.relative_to(self.root).as_posix()}") (sha256 "{hashlib.sha256(data).hexdigest()}") (byte_size {len(data)}))'

    def write_credit(self, extra=""):
        record = self.take() if not M.record_path(self.unit, SEL).exists() else M.record_path(self.unit, SEL)
        policy = self.unit / "EVIDENCE_POLICY.md"
        policy.write_text("policy\n")
        (self.unit / "credits.sexp").write_text(
            f'(credit (id "CR-FIXTURE-1") (profile_ids "fixture") (requirement_id "{REQ}") (obligation_ids "{OB}")\n'
            f'  (selection "{SEL}") {extra}\n  (measured {self.pin(record)})\n  (policy {self.pin(policy)})\n  (retained_sources "SRC-FIXTURE")\n'
            '  (authority review) (date "2026-11-07") (decision "decision_fixture.md") (legs 2)\n  (limitations "a limit"))\n')

    def credits(self):
        M.SELECTIONS[REQ] = self.table[REQ]
        self.addCleanup(M.SELECTIONS.pop, REQ, None)
        return CR.current_credits(self.root, self.unit)

    def test_a_credit_with_no_case_is_current(self):
        self.write_credit()
        credit = self.credits()[0]
        self.assertEqual((credit["disposition"], credit["reasons"], credit["case_id"], credit["selection"]), ("current", [], None, SEL))

    def test_it_lapses_with_its_record(self):
        self.write_credit()
        record = M.record_path(self.unit, SEL)
        record.write_text(record.read_text() + "\n")
        self.assertEqual(self.credits()[0]["reasons"], [f"measured pin {record.relative_to(self.root).as_posix()}: SHA256 or size differs"])

    def test_it_lapses_with_its_fact(self):
        self.write_credit()
        (self.root / "fact.txt").write_text("two\n")
        self.assertEqual(self.credits()[0]["reasons"], ["fact chosen: the tree reads 'two', the record 'one'"])

    def test_it_pins_its_own_record(self):
        self.write_credit()
        other = M.record_path(self.unit, SEL).with_name("other.selection.sexp")
        other.write_text("x")
        text = (self.unit / "credits.sexp").read_text()
        (self.unit / "credits.sexp").write_text(text.replace(f"selections/{SEL}.selection.sexp", "selections/other.selection.sexp").replace(
            hashlib.sha256(M.record_path(self.unit, SEL).read_bytes()).hexdigest(), hashlib.sha256(b"x").hexdigest()).replace(
            f"(byte_size {M.record_path(self.unit, SEL).stat().st_size})", "(byte_size 1)"))
        self.assertIn("measured pin does not name the selection's record", self.credits()[0]["reasons"])

    def test_a_credit_names_a_case_or_a_selection_and_not_both(self):
        self.write_credit('(case_id "fixture-case")')
        with self.assertRaisesRegex(CR.CreditRefused, "names exactly one of"):
            CR.load_credits(self.root, self.unit)

    def test_a_credit_naming_neither_is_refused(self):
        self.write_credit()
        text = (self.unit / "credits.sexp").read_text()
        (self.unit / "credits.sexp").write_text(text.replace(f'(selection "{SEL}") ', ""))
        with self.assertRaisesRegex(CR.CreditRefused, "names exactly one of"):
            CR.load_credits(self.root, self.unit)

    def test_a_selection_has_no_receipt(self):
        self.write_credit()
        text = (self.unit / "credits.sexp").read_text()
        pin = text[text.index("(policy ") + len("(policy "):text.index("\n  (retained_sources") - 1]
        (self.unit / "credits.sexp").write_text(text.replace("  (retained_sources", f"  (receipt {pin})\n  (retained_sources"))
        with self.assertRaisesRegex(CR.CreditRefused, "a receipt belongs to a case"):
            CR.load_credits(self.root, self.unit)


class StatusTests(CreditTests):
    def derive(self):
        M.SELECTIONS[REQ] = self.table[REQ]
        self.addCleanup(M.SELECTIONS.pop, REQ, None)
        return RS.derive_profile(self.root, self.unit, [])

    def test_a_current_credit_implements_its_requirement(self):
        self.write_credit()
        table = self.derive()
        self.assertEqual((table["rows"][0]["derived"], table["findings"], table["cases"], table["current_credits"]), ("implemented", [], 0, 1))

    def test_a_lapsed_credit_is_a_finding_and_implements_nothing(self):
        self.write_credit()
        (self.root / "fact.txt").write_text("two\n")
        table = self.derive()
        self.assertEqual(table["rows"][0]["derived"], "planned")
        self.assertEqual(table["findings"], ["credit CR-FIXTURE-1 lapsed: fact chosen: the tree reads 'two', the record 'one'"])

    def test_an_obligation_the_requirement_does_not_name_implements_nothing(self):
        self.write_credit()
        (self.unit / "requirements.sexp").write_text(R.dump([dict(requirement(), obligation_ids=["OB-OTHER"])]))
        table = self.derive()
        self.assertEqual(table["rows"][0]["derived"], "planned")
        self.assertEqual(table["findings"], [f"credit CR-FIXTURE-1 binds {OB} to {REQ}, which does not name it"])

    def test_an_obligation_outside_the_contract_implements_nothing(self):
        self.write_credit()
        (self.unit / "contract-obligations.sexp").write_text(R.dump([dict(obligation(), id="OB-OTHER")]))
        table = self.derive()
        self.assertEqual(table["rows"][0]["derived"], "planned")
        self.assertIn(f"credit CR-FIXTURE-1 names obligation {OB} outside the effective contract (superseded or unknown)", table["findings"])


class TraceTests(Tree):
    def test_the_trace_tool_reads_a_selection_as_it_reads_a_case(self):
        self.take()
        found = ST._declared_selections(self.root, self.unit)
        self.assertEqual(found, {REQ: [(SEL, ["chosen", "held"], "a limit")]})


def main() -> int:
    global M
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--mutation", choices=sorted(MUTATIONS))
    args = parser.parse_args()
    if args.mutation:
        old, new = MUTATIONS[args.mutation]
        source = Path(M.__file__).read_text()
        if source.count(old) != 1:
            print(f"SELECTIONS-PROBE: mutation {args.mutation} no longer applies", file=sys.stderr)
            return 2
        mutant = types.ModuleType("selections")
        mutant.__file__ = M.__file__
        sys.modules["selections"] = mutant
        exec(compile(source.replace(old, new), M.__file__, "exec"), mutant.__dict__)
        M = mutant
    suite = unittest.TestSuite(unittest.defaultTestLoader.loadTestsFromTestCase(c) for c in (RecordTests, StatusTests, TraceTests))
    result = unittest.TextTestRunner(verbosity=1).run(suite)
    print(f"SELECTIONS-PROBE: {result.testsRun} tests / {len(result.failures)} failures / {len(result.errors)} errors; a frozen fixture tree, no real credit")
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    sys.exit(main())
