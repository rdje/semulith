#!/usr/bin/env python3
"""Source-derived GPR controls; synthetic bytes, no execution or qualification."""
from __future__ import annotations

from copy import deepcopy
import argparse
from dataclasses import FrozenInstanceError, fields, is_dataclass, replace
import hashlib
from pathlib import Path
import sys
import tempfile
import types
import unittest
from unittest import mock

import dossier_sexp as D
import matched_gpr_comparison as C
import records_sexp as R


def expectation(writes, *, program="example.s", entry="0x80000000"):
    return dict(
        program=program,
        entry=entry,
        instructions=len(writes),
        step=[
            dict(
                n=n,
                insn="synthetic instruction",
                writes=row,
                derivation="synthetic expectation; no capture",
                source="synthetic",
            )
            for n, row in enumerate(writes)
        ],
    )


def encode(doc):
    return R.render_forms([D.expectations_to_form(doc)]).encode()


class DerivationTests(unittest.TestCase):
    def compare(self, source, expected, witness, **changes):
        function = getattr(C, "compare_source_expectation", None)
        self.assertTrue(callable(function), "source-derived expectation binding API is missing")
        args = dict(
            source=source,
            baseline_expectation=encode(expected),
            instructions=expected["instructions"],
            program=expected["program"],
            witness=witness,
        )
        args.update(changes)
        try:
            return function(**args)
        except (
            ValueError,
            TypeError,
            AttributeError,
            KeyError,
            IndexError,
            OSError,
            AssertionError,
        ) as exc:
            self.fail(f"derivation boundary escaped as {type(exc).__name__}: {exc}")

    def outcome(
        self,
        disposition="matched",
        *,
        source=b"addi x1, x0, 1\n",
        expected=None,
        witness=None,
        reason=None,
        **changes,
    ):
        if expected is None:
            expected = expectation([{"x1": "0x1"}])
        if witness is None:
            witness = C.GprWitness(0, "x1")
        checked = self.compare(source, expected, witness, **changes)
        self.assertEqual(checked.disposition, disposition, checked.reason)
        if reason:
            self.assertIn(reason, checked.reason)
        self.assertFalse(hasattr(checked, "qualified"))
        return checked

    def test_colluding_wrong_value_fails_despite_satisfied_byte_unit(self):
        source = b"addi x1, x0, 1\n"
        expected = expectation([{"x1": "0x9"}])
        control = deepcopy(expected)
        control["step"][0]["writes"]["x1"] = "0xa"
        witness = C.GprWitness(0, "x1")
        trace = (
            b"[0] [M]: 0x0000000080000000 (0x00100093) addi x1, x0, 1\n"
            b"x1 <- 0x0000000000000009\n"
        )
        run = C.RunBytes(trace, 0)
        old = C.compare_unit(
            instructions=1,
            program="example.s",
            witness=witness,
            baseline_expectation=encode(expected),
            control_expectation=encode(control),
            baseline=run,
            repeat=run,
            control=run,
        )
        self.assertEqual(old.disposition, "satisfied")
        checked = self.compare(source, expected, witness)
        self.assertEqual(checked.disposition, "failed")
        self.assertEqual(checked.difference.step_n, 0)
        self.assertEqual(checked.difference.observed, (("x1", 1),))
        self.assertEqual(checked.difference.expected, (("x1", 9),))

    def test_mixed_width_complete_changes_match(self):
        source = b"addi x1, x0, 5\nc.addi x1, 1\n"
        expected = expectation([{"x1": "0x5"}, {"x1": "0x6"}])
        checked = self.compare(source, expected, C.GprWitness(1, "x1"))
        self.assertEqual(checked.disposition, "matched")
        self.assertEqual(checked.facts.witness_value, 6)
        self.assertEqual(checked.facts.derivation.steps[1].instruction_bits, 0x0085)
        self.assertIsNone(checked.difference)

    def test_wrong_changes_before_and_after_witness_are_not_ignored(self):
        source = b"addi x1, x0, 1\naddi x2, x0, 2\naddi x3, x0, 3\n"
        for n in (0, 2):
            doc = expectation([{"x1": "0x1"}, {"x2": "0x2"}, {"x3": "0x3"}])
            doc["step"][n]["writes"][f"x{n+1}"] = "0x9"
            with self.subTest(n=n):
                checked = self.outcome(
                    "failed", source=source, expected=doc, witness=C.GprWitness(1, "x2")
                )
                self.assertEqual(checked.difference.step_n, n)
                self.assertEqual(checked.facts.witness_value, 2)

    def test_missing_extra_and_first_difference_are_structured(self):
        source = b"addi x1, x0, 1\naddi x2, x0, 2\n"
        for writes in [
            [{}, {"x2": "0x2"}],
            [{"x1": "0x1", "x3": "0x3"}, {"x2": "0x2"}],
            [{"x1": "0x9"}, {"x2": "0x9"}],
        ]:
            with self.subTest(writes=writes):
                checked = self.outcome("failed", source=source, expected=expectation(writes))
                self.assertEqual(checked.difference.step_n, 0)
                self.assertEqual(checked.difference.observed, (("x1", 1),))

    def test_rv64_spelling_and_zero_change_value(self):
        self.outcome(expected=expectation([{"x1": "0X00000000000000000001"}]))
        checked = self.outcome(
            source=b"addi x1, x0, 1\naddi x1, x0, 0\n",
            expected=expectation([{"x1": "0x1"}, {"x1": "0x0"}]),
            witness=C.GprWitness(1, "x1"),
        )
        self.assertEqual(checked.facts.witness_value, 0)

    def test_unchanged_register_is_a_failed_witness(self):
        checked = self.outcome(
            "failed",
            source=b"addi x0, x0, 0\n",
            expected=expectation([{}]),
            reason="not an actual derived register change",
        )
        self.assertIsNone(checked.facts.witness_value)
        self.assertIsNone(checked.difference)

    def test_metadata_and_stock_derivation_are_retained_without_payload(self):
        expected = expectation([{"x1": "0x1"}])
        payload = encode(expected)
        source = b"addi x1, x0, 1 #: fabricated capture | fabricated source\n"
        checked = self.outcome(source=source, expected=expected)
        facts = checked.facts
        self.assertEqual(
            (facts.expectation_size, facts.expectation_sha256),
            (len(payload), hashlib.sha256(payload).hexdigest()),
        )
        self.assertEqual(facts.derivation.source_sha256, hashlib.sha256(source).hexdigest())
        self.assertEqual(
            (facts.derivation.author_path, facts.derivation.route),
            ("scripts/derive_rv64gc_expectations.py", "snapshot-parcels-v1"),
        )
        self.assertNotIn("fabricated", facts.derivation.steps[0].source)
        self.assertNotIn("fabricated", facts.derivation.steps[0].derivation)

        def payload_present(value):
            if isinstance(value, (bytes, bytearray, memoryview)):
                return True
            if is_dataclass(value):
                return any(payload_present(getattr(value, f.name)) for f in fields(value))
            if isinstance(value, tuple):
                return any(payload_present(v) for v in value)
            return False

        self.assertFalse(payload_present(checked))

    def test_check_facts_and_selected_witness_are_frozen(self):
        checked = self.outcome()
        for value, field in [
            (checked, "reason"),
            (checked.facts, "witness_value"),
            (checked.facts.witness, "register"),
        ]:
            with self.subTest(field=field), self.assertRaises(FrozenInstanceError):
                setattr(value, field, None)

    def test_witness_is_copied_before_tool_callbacks(self):
        witness = C.GprWitness(0, "x1")
        deriving = C.Author.derive_snapshot

        def derive(*args, **kwargs):
            object.__setattr__(witness, "register", "x31")
            return deriving(*args, **kwargs)

        with mock.patch.object(C.Author, "derive_snapshot", side_effect=derive):
            checked = self.outcome(witness=witness)
        self.assertEqual(checked.facts.witness, C.GprWitness(0, "x1"))
        self.assertIsNot(checked.facts.witness, witness)

    def test_preflight_shapes_and_bounds_precede_schema_and_author(self):
        class Text(str):
            pass

        cases = [
            dict(source=s)
            for s in (
                None,
                bytearray(b"x"),
                memoryview(b"x"),
                b"",
                b"\xff",
                b"x" * 1048577,
                b"#\n" * 8193,
            )
        ]
        cases += [
            dict(baseline_expectation=s) for s in (None, bytearray(b"x"), b"", b"x" * 1048577)
        ]
        cases += [dict(program=p) for p in (None, "", False, Text("example.s"), "x" * 65537)]
        cases += [dict(instructions=n) for n in (False, 0, -1, 4097, 1.0)]
        cases += [
            dict(witness=w)
            for w in (
                {},
                C.GprWitness(False, "x1"),
                C.GprWitness(-1, "x1"),
                C.GprWitness(1, "x1"),
                C.GprWitness(0, "x0"),
                C.GprWitness(0, "x32"),
                C.GprWitness(0, "x01"),
                C.GprWitness(0, Text("x1")),
            )
        ]
        for changes in cases:
            with (
                self.subTest(changes=list(changes)),
                mock.patch.object(C, "_schema", side_effect=AssertionError("schema I/O")),
                mock.patch.object(
                    C.Author, "derive_snapshot", side_effect=AssertionError("author I/O")
                ),
            ):
                self.outcome("refused", **changes)

    def test_inclusive_source_program_and_budget_limits(self):
        code = b"addi x1, x0, 1\n"
        source = b"#" + b"x" * (1048576 - len(code) - 2) + b"\n" + code
        self.outcome(source=source, expected=expectation([{"x1": "0x1"}], program="x" * 65536))
        doc = expectation([{"x1": "0x1"}] + [{} for _ in range(4095)])
        checked = self.outcome(source=code + b"jal x0, 0\n", expected=doc)
        self.assertEqual(
            (checked.facts.derivation.instructions, len(checked.facts.derivation.steps)),
            (4096, 4096),
        )

    def test_program_budget_entry_and_malformed_expectation_refuse(self):
        for fields in (
            dict(program="wrong.s"),
            dict(instructions=2),
            dict(entry="0xno"),
            dict(entry="0x10000000000000000"),
        ):
            doc = expectation([{"x1": "0x1"}])
            doc.update(fields)
            with self.subTest(fields=fields):
                self.outcome("refused", baseline_expectation=encode(doc))
        doc = expectation([{"x1": "0x1"}])
        doc.pop("entry")
        self.outcome("refused", baseline_expectation=encode(doc), reason="explicit string entry")
        for payload in (b"(expectations (unknown 1))", b"\xff"):
            with self.subTest(payload=payload):
                self.outcome("refused", baseline_expectation=payload)

    def test_duplicate_write_keys_and_invalid_rv64_values_refuse(self):
        for register, value in [
            ("x0", "0x1"),
            ("x32", "0x1"),
            ("x01", "0x1"),
            ("x1", "1"),
            ("x1", "0x10000000000000000"),
        ]:
            with self.subTest(register=register, value=value):
                self.outcome("refused", expected=expectation([{register: value}]))
        payload = (
            b'(expectations (program "example.s") (entry "0x80000000") (instructions 1) '
            b'(step (n 0) (insn "addi") (writes (write (reg "x1") (value "0x1")) '
            b'(write (reg "x1") (value "0x1"))) (derivation "d") (source "s")))'
        )
        self.outcome("refused", baseline_expectation=payload, reason="duplicate write")

    def test_exclusions_and_fixed_context_are_unsupported_before_author(self):
        for fields in [
            dict(entry="0x80000002"),
            dict(cross_model=False),
            dict(expect_divergence=dict(difference="d", at_step=0)),
            dict(refuse=[dict(kind="load", base="0x80000000", size="0x4")]),
        ]:
            doc = expectation([{"x1": "0x1"}])
            doc.update(fields)
            with (
                self.subTest(fields=fields),
                mock.patch.object(
                    C.Author, "derive_snapshot", side_effect=AssertionError("author I/O")
                ),
            ):
                self.outcome("unsupported", expected=doc)

    def test_declared_event_markers_are_unsupported_before_author(self):
        for field, text in [
            ("insn", "<fetch fault>"),
            ("insn", "<halted>"),
            (
                "derivation",
                "pending interrupt 7 delivers in M before instruction fetch; no retirement.",
            ),
        ]:
            doc = expectation([{"x1": "0x1"}])
            doc["step"][0][field] = text
            with (
                self.subTest(field=field, text=text),
                mock.patch.object(
                    C.Author, "derive_snapshot", side_effect=AssertionError("author I/O")
                ),
            ):
                self.outcome("unsupported", expected=doc, reason="event boundaries")

    def test_unfetched_source_boundaries_need_typed_event_binding(self):
        for source in (b"wfi\n", b"jal x0, -4\n"):
            with self.subTest(source=source):
                self.outcome(
                    "unsupported",
                    source=source,
                    expected=expectation([{}, {}]),
                    reason="unfetched boundaries",
                )

    def test_source_refusals_and_unavailable_tools_stay_distinct(self):
        self.outcome("refused", source=b"not_an_instruction\n", reason="source derivation")
        for source in (b"#|never: x31\naddi x1, x0, 1\n", b"csrrw x1, mcycle, x0\n"):
            with self.subTest(source=source):
                self.outcome("unsupported", source=source, reason="supported semantics")
        with mock.patch.object(
            C.G, "canonical_guest_assembler", side_effect=C.G.ImageUnavailable("unavailable")
        ):
            self.outcome("unavailable", reason="canonical snapshot author")
        with mock.patch.object(C, "_schema", side_effect=OSError("schema unavailable")):
            self.outcome("refused", reason="cannot decode/validate")

    def test_exact_source_program_and_budget_reach_author_once(self):
        source = b"addi x1, x0, 1\n"
        program = "dir / 雪.s"
        with mock.patch.object(
            C.Author, "derive_snapshot", wraps=C.Author.derive_snapshot
        ) as deriving:
            self.outcome(source=source, expected=expectation([{"x1": "0x1"}], program=program))
        deriving.assert_called_once_with(source, program=program, instructions=1)

    def test_source_file_is_not_reopened(self):
        root = Path(__file__).resolve().parent.parent
        base = root / "target/p4-system-14/a42p/fixtures"
        base.mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryDirectory(dir=base) as directory:
            path = Path(directory) / "example.s"
            path.write_bytes(b"addi x1, x0, 9\n")
            program = path.relative_to(root).as_posix()
            self.outcome(expected=expectation([{"x1": "0x1"}], program=program))

    def test_contradictory_author_context_refuses(self):
        derived = C.Author.derive_snapshot(b"addi x1, x0, 1\n", program="example.s", instructions=1)
        corrupt = [
            None,
            replace(derived, program="wrong.s"),
            replace(derived, instructions=2),
            replace(derived, entry=0),
            replace(derived, source_size=0),
            replace(derived, source_sha256="0" * 64),
            replace(derived, steps=()),
            replace(derived, steps=(replace(derived.steps[0], n=1),)),
        ]
        for result in corrupt:
            with (
                self.subTest(result=type(result)),
                mock.patch.object(C.Author, "derive_snapshot", return_value=result),
            ):
                self.outcome("refused", reason="requested context")

    def test_signed_division_retains_stock_witness_provenance(self):
        checked = self.outcome(
            source=b"addi x1, x0, -7\naddi x2, x0, 2\ndiv x3, x1, x2\n",
            expected=expectation(
                [{"x1": "0xfffffffffffffff9"}, {"x2": "0x2"}, {"x3": "0xfffffffffffffffd"}]
            ),
            witness=C.GprWitness(2, "x3"),
        )
        step = checked.facts.derivation.steps[2]
        self.assertEqual(
            (step.pc, step.instruction_bits, step.instruction_length), (0x80000008, 0x0220C1B3, 4)
        )
        self.assertIn("RVI-M", step.source)
        self.assertEqual(checked.facts.witness_value, 0xFFFFFFFFFFFFFFFD)

    def test_actual_modified_instruction_is_used(self):
        source = (
            b"auipc x1, 0\naddi x1, x1, 24\nlui x2, 0x700\naddi x2, x2, 0x293\n"
            b"sw x2, 0, x1\naddi x0, x0, 0\naddi x5, x0, 1\n"
        )
        expected = expectation(
            [
                {"x1": "0x80000000"},
                {"x1": "0x80000018"},
                {"x2": "0x700000"},
                {"x2": "0x700293"},
                {},
                {},
                {"x5": "0x7"},
            ]
        )
        checked = self.outcome(source=source, expected=expected, witness=C.GprWitness(6, "x5"))
        self.assertEqual(checked.facts.derivation.steps[6].instruction_bits, 0x00700293)

    def test_no_outputs_or_reference_processes_and_unexpected_failure_propagates(self):
        with (
            mock.patch.object(Path, "write_bytes", side_effect=AssertionError("file output")),
            mock.patch.object(Path, "write_text", side_effect=AssertionError("file output")),
            mock.patch("subprocess.run", side_effect=AssertionError("process")),
            mock.patch("subprocess.Popen", side_effect=AssertionError("process")),
        ):
            self.outcome()
        with (
            mock.patch.object(
                C.Author,
                "derive_snapshot",
                side_effect=RuntimeError("unexpected programming failure"),
            ),
            self.assertRaisesRegex(RuntimeError, "unexpected programming failure"),
        ):
            C.compare_source_expectation(
                source=b"addi x1, x0, 1\n",
                baseline_expectation=encode(expectation([{"x1": "0x1"}])),
                instructions=1,
                program="example.s",
                witness=C.GprWitness(0, "x1"),
            )


MUTATIONS = {
    "source-preflight": (
        "G.prepare_guest_source(source, program=program, entry=Author.ENTRY)",
        "pass",
    ),
    "expectation-bounds": (
        '_bounded(baseline_expectation, EXPECTATION_BYTES, "baseline expectation", empty=False)\n        if (type(witness)',
        "pass\n        if (type(witness)",
    ),
    "witness-copy": (
        "selected = GprWitness(witness.step_n, witness.register)",
        "selected = witness",
    ),
    "program": ('        if doc["program"] != program:', "        if False:"),
    "fixed-entry": ("if entry != Author.ENTRY:", "if False:"),
    "exclusions": ("if excluded:", "if False:"),
    "declared-events": (
        'if any(step["insn"].startswith("<") or Sail.LEGACY_FETCH.fullmatch(step["insn"])\n           or Sail.DECLARED_INTERRUPT.match(step["derivation"]) for step in doc["step"]):',
        "if False:",
    ),
    "source-forward": (
        "derived = Author.derive_snapshot(source, program=program, instructions=instructions)",
        'derived = Author.derive_snapshot(b"addi x1, x0, 9\\n", program=program, instructions=instructions)',
    ),
    "budget-forward": (
        "derived = Author.derive_snapshot(source, program=program, instructions=instructions)",
        "derived = Author.derive_snapshot(source, program=program, instructions=1)",
    ),
    "source-reopen": (
        "derived = Author.derive_snapshot(source, program=program, instructions=instructions)",
        "derived = Author.derive_snapshot(Path(program).read_bytes(), program=program, instructions=instructions)",
    ),
    "context-program": ("or derived.program != program", "or False"),
    "unfetched": (
        "if any(step.instruction_bits is None or step.instruction_length is None for step in derived.steps):",
        "if False:",
    ),
    "whole-budget": (
        'for step, expected in zip(derived.steps, doc["step"]):',
        'for step, expected in [(derived.steps[selected.step_n], doc["step"][selected.step_n])]:',
    ),
    "value-comparison": ("if observed != wanted:", "if False:"),
    "witness-change": ("if value is None:", "if False:"),
    "zero-value": ("if value is None:", "if not value:"),
    "baseline-fingerprint": (
        "hashlib.sha256(baseline_expectation).hexdigest()",
        "hashlib.sha256(source).hexdigest()",
    ),
    "facts-frozen": (
        "@dataclass(frozen=True)\nclass SourceExpectationFacts:",
        "@dataclass\nclass SourceExpectationFacts:",
    ),
    "check-frozen": (
        "@dataclass(frozen=True)\nclass SourceExpectationCheck:",
        "@dataclass\nclass SourceExpectationCheck:",
    ),
}


def main():
    global C
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mutation", choices=MUTATIONS)
    args = parser.parse_args()
    if args.mutation:
        source = Path(C.__file__).read_text()
        before, after = MUTATIONS[args.mutation]
        if source.count(before) != 1:
            raise RuntimeError("mutation seam is not singular")
        module = types.ModuleType("mutated_gpr_derivation")
        module.__file__ = C.__file__
        sys.modules[module.__name__] = module
        exec(compile(source.replace(before, after), C.__file__, "exec"), module.__dict__)
        C = module
    result = unittest.TextTestRunner(verbosity=1).run(
        unittest.defaultTestLoader.loadTestsFromTestCase(DerivationTests)
    )
    print(
        f"MATCHED-GPR-DERIVATION: {result.testsRun} tests / {len(result.failures)} failures / "
        f"{len(result.errors)} errors; no qualification"
    )
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    raise SystemExit(main())
