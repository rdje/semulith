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
import struct
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
    "elf-flags": ("flags = struct.unpack(\"<H\", data[18:20])[0], struct.unpack(\"<I\", data[48:52])[0]\n", "flags = struct.unpack(\"<H\", data[18:20])[0], 5\n"),
    "comment-consumer": ("code = [line.split(\"//\", 1)[0] for line in", "code = [line for line in"),
    "other-enumeration": ("f\"{len(set(base) & set(reference))} shared, {len(set(base) ^ set(reference))} differ\"", "f\"{len(set(base) & set(reference))} shared, 0 differ\""),
    "unbound-slot": ("{len(S.children(part, 'slot'))} unbound slots", "0 unbound slots"),
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

    def test_a_trace_beside_the_record_reads_with_the_profile_s_own(self):
        self.take()
        (self.unit / "selections/statement-trace.sexp").write_text(TRACE)
        (self.unit / "statement-trace.sexp").unlink()
        self.assertEqual(self.reasons(), [])

    def test_a_requirement_traced_in_both_places_is_refused(self):
        self.take()
        (self.unit / "selections/statement-trace.sexp").write_text(TRACE)
        self.assertIn("is traced twice", self.reasons()[0])

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


def tiny_elf(flags=0x5, text=b"\x82\x80", elf_class=2):
    """A relocatable object with the three sections a fact reads, built here so no toolchain runs."""
    names = b"\0.text\0.shstrtab\0"
    text_off, names_off = 64, 64 + len(text)
    shoff = names_off + len(names)
    head = b"\x7fELF" + bytes([elf_class, 1, 1]) + bytes(9) + struct.pack("<HHIQQQIHHHHHH", 1, 243, 1, 0, 0, shoff, flags, 64, 0, 0, 64, 3, 2)
    empty = bytes(64)
    section = struct.pack("<IIQQQQIIQQ", 1, 1, 6, 0, text_off, len(text), 0, 0, 2, 0)
    strtab = struct.pack("<IIQQQQIIQQ", 7, 3, 0, 0, names_off, len(names), 0, 0, 1, 0)
    return head + text + names + empty + section + strtab


class FactTests(Tree):
    """What each of the four reads, on a small tree of the same paths: a fact must move when the thing it names moves."""

    def write(self, path, text):
        target = self.root / path
        target.parent.mkdir(parents=True, exist_ok=True)
        if isinstance(text, bytes):
            target.write_bytes(text)
        else:
            target.write_text(text)

    def abi_tree(self):
        for abi, flags, text in (("lp64d", 0x5, b"\x82\x80"), ("lp64", 0x1, b"\x2e\x85\x82\x80"), ("lp64f", 0x3, b"\x2e\x85\x82\x80")):
            self.write(f"{M.ABI_DIR}/abi-{abi}.o", tiny_elf(flags, text))
        self.write("scripts/run_workload_campaign.py", 'CFLAGS = ["--target=x", "-march=rv64gc", "-mabi=lp64d",\n          "-O2"]\n')
        self.write("scripts/riscv_toolchain.py", 'LLVM_VERSION = "21.1.8"\n')

    def test_an_object_reads_as_its_flags_and_instructions(self):
        self.abi_tree()
        facts = M.abi_facts(M.Reader(self.root))
        self.assertEqual(facts, {"object-lp64d": "ELFCLASS64 machine=243 flags=0x5 text=8280", "object-lp64": "ELFCLASS64 machine=243 flags=0x1 text=2e858280",
                                 "object-lp64f": "ELFCLASS64 machine=243 flags=0x3 text=2e858280", "workload-flags": "-march=rv64gc -mabi=lp64d", "toolchain-pin": "21.1.8"})

    def test_a_soft_float_object_named_lp64d_moves_its_fact(self):
        self.abi_tree()
        self.write(f"{M.ABI_DIR}/abi-lp64d.o", tiny_elf(0x1, b"\x2e\x85\x82\x80"))
        self.assertEqual(M.abi_facts(M.Reader(self.root))["object-lp64d"], "ELFCLASS64 machine=243 flags=0x1 text=2e858280")

    def test_a_32_bit_object_is_not_read_as_one(self):
        self.assertEqual(M._elf_fact(tiny_elf(elf_class=1)), "not a little-endian ELFCLASS64 file")

    def test_a_moved_compile_flag_moves_its_fact(self):
        self.abi_tree()
        self.write("scripts/run_workload_campaign.py", 'CFLAGS = ["-march=rv64gc", "-mabi=lp64"]\n')
        self.assertEqual(M.abi_facts(M.Reader(self.root))["workload-flags"], "-march=rv64gc -mabi=lp64")

    def fp_tree(self):
        self.write("crates/semulith-core/Cargo.toml", '[dependencies]\nrustc_apfloat = "=0.2.3"\n')
        self.write("Cargo.lock", '[[package]]\nname = "other"\nversion = "1"\n\n[[package]]\nname = "rustc_apfloat"\nversion = "0.2.3+x"\nchecksum = "abc"\n')
        self.write(M.FP_SOURCE, "use rustc_apfloat::Float;\n")
        self.write("crates/semulith-core/src/lib.rs", "// rustc_apfloat:: named in a comment\npub use rustc_apfloat;\n")
        self.write("crates/semulith-core/src/note.rs", 'const WHY: &str = "// rustc_apfloat 0.2.3";\n')
        self.write("xtask/src/none.rs", "fn main() {}\n")
        self.write(f"{M.UNIT}/profile.sexp", '(profile (extensions "F") (extensions "D") (extensions "M"))\n')
        self.write(f"{M.UNIT}/requirements.sexp", R.dump([dict(requirement(), id="REQ-D-FP-DEFER", dependencies=["REQ-D-ABI"])]))
        for name in ("decision_fp-backend-qualification.md", "reference_fp-model-layer-acceptance.md", "reference_softfloat-shared-ancestry.md"):
            self.write(f"docs/decisions/{name}", "- **Status:** `active`\nexact overflow/underflow judgment\n")

    def test_the_backend_reads_as_declared(self):
        self.fp_tree()
        facts = M.fp_facts(M.Reader(self.root))
        self.assertEqual(facts, {"backend-requirement": "=0.2.3", "backend-artifact": "0.2.3+x abc", "model-layer": M.FP_SOURCE,
                                 "backend-consumers": f"{M.FP_SOURCE} uses; crates/semulith-core/src/lib.rs re-exports",
                                 "f-and-d-selected": "D F", "needs-the-abi": "REQ-D-ABI", "qualification-status": "active active",
                                 "flag-corrections-recorded": "overflow/underflow", "shared-ancestry-status": "active"})

    def test_another_user_of_the_backend_moves_its_fact(self):
        self.fp_tree()
        self.write("crates/semulith-core/src/sneak.rs", "fn f() { rustc_apfloat::ieee::Double::ZERO; }\n")
        self.assertIn("crates/semulith-core/src/sneak.rs uses", M.fp_facts(M.Reader(self.root))["backend-consumers"])

    def test_another_package_moving_in_the_lock_does_not_move_the_fact(self):
        self.fp_tree()
        before = M.fp_facts(M.Reader(self.root))
        self.write("Cargo.lock", '[[package]]\nname = "other"\nversion = "2"\n\n[[package]]\nname = "rustc_apfloat"\nversion = "0.2.3+x"\nchecksum = "abc"\n')
        self.assertEqual(M.fp_facts(M.Reader(self.root)), before)

    def test_a_withdrawn_qualification_moves_its_fact(self):
        self.fp_tree()
        self.write("docs/decisions/decision_fp-backend-qualification.md", "- **Status:** `withdrawn`\n")
        self.assertEqual(M.fp_facts(M.Reader(self.root))["qualification-status"], "withdrawn active")

    def route_tree(self):
        self.write(f"{M.UNIT}/profile.sexp", '(profile (vehicle (route generated-definition)))\n')
        self.write(f"{M.UNIT}/encoding.sexp", '(encoding (compose (base "riscv/rv64i") (status complete)))\n')
        rows = "".join(f"x\to\t{path}\t{gate}\n" for path, gate in (("crates/semulith-core/src/state_rv64gc.rs", "STATE-GEN"), ("crates/semulith-core/src/definition_rv64gc.rs", "DEF-GEN"), ("crates/semulith-verify/src/guests_rv64gc.rs", "GUEST-GEN")))
        self.write("doctrine/fact_ownership.tsv", "# kind\n" + rows)
        for path, gen in (("crates/semulith-core/src/state_rv64gc.rs", "state"), ("crates/semulith-core/src/definition_rv64gc.rs", "definition"), ("crates/semulith-verify/src/guests_rv64gc.rs", "guests")):
            self.write(path, f"//! GENERATED — do not edit. Regenerate with `python3 scripts/gen_{gen}.py`\n")
        self.write("scripts/check_doctrines.project.sh", '  "STATE-GEN|x"\n  "DEF-GEN|x"\n  "GUEST-GEN|x"\n')

    def test_the_route_reads_as_declared(self):
        self.route_tree()
        self.assertEqual(M.definition_facts(M.Reader(self.root)), {"vehicle": "generated-definition", "composition": "complete, 0 unbound slots, base riscv/rv64i",
                         "mirror-state": "GENERATED, scripts/gen_state.py, STATE-GEN", "mirror-definition": "GENERATED, scripts/gen_definition.py, DEF-GEN",
                         "mirror-guests": "GENERATED, scripts/gen_guests.py, GUEST-GEN", "drift-gates": "DEF-GEN GUEST-GEN STATE-GEN"})

    def test_a_hand_owned_mirror_and_an_unbound_slot_move_their_facts(self):
        self.route_tree()
        self.write(f"{M.UNIT}/encoding.sexp", '(encoding (compose (base "riscv/rv64i") (status partial) (slot "x")))\n')
        self.write("crates/semulith-core/src/state_rv64gc.rs", "//! written by hand\n")
        facts = M.definition_facts(M.Reader(self.root))
        self.assertEqual(facts["composition"], "partial, 1 unbound slots, base riscv/rv64i")
        self.assertEqual(facts["mirror-state"], "not marked generated, no generator, STATE-GEN")

    def census_tree(self, base=("ADD", "SUB"), other=("ADD", "SUB"), total=3, source="RVI-RV32I §1; more"):
        family = lambda head, names: f"({head} " + " ".join(f'"{n}"' for n in names) + ")"
        self.write(f"{M.UNIT}/profile.sexp", f'(profile (scope (count_base {len(base)}) (count_rv64i_additions 0) (count_total {total}) (source "{source}") {family("base_op", base)} {family("m_muldiv", ("MUL",))}))\n')
        self.write("profiles/rv64i-lab-v0/profile.sexp", f'(profile (scope (source "RVI-RV32I §1") {family("base_op", other)}))\n')
        self.write(f"{M.UNIT}/encoding.sexp", "(encoding)\n")
        original = M.E._encoding_names
        M.E._encoding_names = lambda unit: {"add", "sub", "mul"}
        self.addCleanup(setattr, M.E, "_encoding_names", original)

    def test_the_census_reads_as_declared(self):
        self.census_tree()
        self.assertEqual(M.census_facts(M.Reader(self.root)), {"base-census": "2 forms, 2 base and 0 RV64I additions", "same-enumeration-as-rv64i": "2 shared, 0 differ",
                         "same-source-as-rv64i": "yes", "total": "3 stated, 3 enumerated", "grows-with-its-fragments": "3 resolved in the composition, 0 differ"})

    def test_a_census_apart_from_rv64i_moves_its_facts(self):
        self.census_tree(other=("ADD", "XOR"), source="RVI-OTHER §1")
        facts = M.census_facts(M.Reader(self.root))
        self.assertEqual((facts["same-enumeration-as-rv64i"], facts["same-source-as-rv64i"]), ("1 shared, 2 differ", "no"))

    def test_a_form_past_the_composition_moves_its_fact(self):
        self.census_tree(base=("ADD", "SUB", "NEW"), total=3)
        facts = M.census_facts(M.Reader(self.root))
        self.assertEqual(facts["total"], "3 stated, 4 enumerated")
        self.assertEqual(facts["grows-with-its-fragments"], "3 resolved in the composition, 1 differ")


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
    suite = unittest.TestSuite(unittest.defaultTestLoader.loadTestsFromTestCase(c) for c in (RecordTests, StatusTests, FactTests, TraceTests))
    result = unittest.TextTestRunner(verbosity=1).run(suite)
    print(f"SELECTIONS-PROBE: {result.testsRun} tests / {len(result.failures)} failures / {len(result.errors)} errors; a frozen fixture tree, no real credit")
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    sys.exit(main())
