#!/usr/bin/env python3
"""Snapshot-author controls; no engine/reference execution or qualification."""
from __future__ import annotations

import argparse
from dataclasses import FrozenInstanceError, fields
import hashlib
from pathlib import Path
import sys
import tempfile
import types
import unittest
from unittest import mock
import derive_rv64gc_expectations as Q

SOURCE = b'addi x1, x0, 5\nc.addi x1, 1\n'


class SnapshotTests(unittest.TestCase):
    def derive(self, source=SOURCE, program='example.s', instructions=2):
        function = getattr(Q, 'derive_snapshot', None)
        self.assertTrue(callable(function), 'bounded immutable-source author API is missing')
        try:
            return function(source, program=program, instructions=instructions)
        except (ValueError, RuntimeError, OSError, Q.Refusal, AssertionError, TypeError,
                KeyError, IndexError) as exc:
            self.fail(f'positive snapshot escaped as {type(exc).__name__}: {exc}')

    def test_exact_mixed_width_changes_and_actual_instruction_bytes(self):
        checked = self.derive()
        self.assertEqual((checked.program, checked.entry, checked.instructions),
                         ('example.s', 0x80000000, 2))
        self.assertEqual(checked.route, 'snapshot-parcels-v1')
        self.assertEqual([(step.n, step.pc, step.instruction_bits, step.instruction_length,
                           step.fetches, step.writes) for step in checked.steps],
                         [(0, 0x80000000, 0x00500093, 4, 2, ((1, 5),)),
                          (1, 0x80000004, 0x0085, 2, 1, ((1, 6),))])


    def test_assembly_refusal_has_the_declared_bounded_exception(self):
        try:
            Q.derive_snapshot(b'not_an_instruction secret\n', program='example.s', instructions=1)
        except Exception as exc:
            self.assertIsInstance(exc, Q.SnapshotError)
            self.assertLess(len(str(exc)), 128)
            self.assertNotIn('secret', str(exc))
        else:
            self.fail('unsupported assembly was accepted')


    def rejected(self, kind, reason=None, **changes):
        args = dict(source=SOURCE, program='example.s', instructions=2); args.update(changes)
        try:
            Q.derive_snapshot(**args)
        except Exception as exc:
            self.assertIsInstance(exc, kind)
            if reason is not None: self.assertIn(reason, str(exc))
            self.assertLess(len(str(exc)), 128)
        else:
            self.fail('invalid/unsupported snapshot accepted')

    def preflight(self, **changes):
        with mock.patch.object(Q.G, 'canonical_guest_assembler') as factory:
            self.rejected(Q.SnapshotError, **changes)
        factory.assert_not_called()

    def test_exact_metadata_and_no_mutable_execution_state(self):
        checked = self.derive()
        payload = bytes.fromhex('930050008500')
        self.assertEqual((checked.source_size, checked.source_sha256), (len(SOURCE), hashlib.sha256(SOURCE).hexdigest()))
        self.assertEqual((checked.payload_size, checked.payload_sha256), (6, hashlib.sha256(payload).hexdigest()))
        self.assertEqual((checked.author_path, checked.encoding_path, checked.region_bytes),
                         ('scripts/derive_rv64gc_expectations.py', 'profiles/rv64gc-lab-v0/encoding.sexp', 65536))
        self.assertIs(type(checked.steps), tuple)
        self.assertFalse({'hart', 'image', 'source'} & {f.name for f in fields(checked)})
        self.assertFalse(hasattr(checked, 'qualified'))
        self.assertTrue(all(step.derivation and step.source for step in checked.steps))

    def test_result_and_step_are_frozen(self):
        checked = self.derive()
        with self.assertRaises(FrozenInstanceError): checked.program = 'changed'
        checked = self.derive()
        with self.assertRaises(FrozenInstanceError): checked.steps[0].pc = 0

    def test_mutable_internal_records_cannot_change_snapshot(self):
        derived = Q._derive_parcel_lines; held = []
        def run(*args, **kwargs):
            result = derived(*args, **kwargs); held.append(result); return result
        with mock.patch.object(Q, '_derive_parcel_lines', side_effect=run): checked = self.derive()
        held[0].steps[0].writes[1] = 999
        held[0].steps[0].source = 'forged'
        held[0].steps[0].pc = 0
        held[0].hart.x[1] = 999
        held[0].image = b'changed'
        self.assertEqual(checked.steps[0].writes, ((1, 5),))
        self.assertNotEqual(checked.steps[0].source, 'forged')
        self.assertEqual(checked.steps[0].pc, 0x80000000)
        self.assertEqual(checked.payload_sha256, hashlib.sha256(bytes.fromhex('930050008500')).hexdigest())

    def test_source_shapes_utf8_and_size_refuse_before_tool_reads(self):
        for source in [None, SOURCE.decode(), bytearray(SOURCE), memoryview(SOURCE), b'', b'\xff', b'#' * (1048576 + 1)]:
            with self.subTest(kind=type(source)): self.preflight(source=source)

    def test_program_and_budget_shapes_refuse_before_tool_reads(self):
        class Text(str): pass
        for program in ['', None, False, Text('example.s'), 'x' * 65537]:
            with self.subTest(program=type(program)): self.preflight(program=program)
        for instructions in [False, 0, -1, 4097, 1.0, None]:
            with self.subTest(instructions=instructions): self.preflight(instructions=instructions)

    def test_inclusive_source_and_program_limits(self):
        checked = self.derive(source=b'#' * 1048576, program='x' * 65536, instructions=1)
        self.assertEqual((checked.source_size, len(checked.program), checked.payload_size, len(checked.steps)),
                         (1048576, 65536, 0, 1))

    def test_line_preflight_includes_final_and_unicode_boundaries(self):
        self.assertEqual(self.derive(source=b'#\n' * 8192, instructions=1).payload_size, 0)
        for source in [b'#\n' * 8193, b'#\n' * 8192 + b'#', ('#\u2028' * 8193).encode()]:
            with self.subTest(size=len(source)): self.preflight(source=source)

    def test_canonical_context_is_explicit_and_prebind_override_is_ignored(self):
        with mock.patch.object(Q, 'ENCODING', Path('missing/prebind.sexp')):
            checked = self.derive()
        self.assertEqual(checked.encoding_path, 'profiles/rv64gc-lab-v0/encoding.sexp')
        with mock.patch.object(Q.G, 'canonical_guest_assembler', side_effect=Q.G.ImageUnavailable('secret' * 500)):
            self.rejected(Q.SnapshotUnavailable, 'canonical GC author context')

    def test_program_label_is_exact_and_never_opened_as_source(self):
        reading = Path.read_text; source_reads = []
        def read(path, *args, **kwargs):
            if path.suffix == '.s':
                source_reads.append(str(path)); raise AssertionError('source path reopened')
            return reading(path, *args, **kwargs)
        with mock.patch.object(Path, 'read_text', read): checked = self.derive(program='dir/雪-example.s')
        self.assertEqual(source_reads, [])
        self.assertEqual(checked.program, 'dir/雪-example.s')
        self.assertEqual(checked.steps[0].writes, ((1, 5),))

    def test_existing_file_changes_do_not_replace_supplied_source(self):
        base = Path(__file__).resolve().parent.parent / 'target/p4-system-14/a42o/fixtures'
        base.mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryDirectory(dir=base) as allocated:
            path = Path(allocated) / 'example.s'; path.write_bytes(b'addi x1, x0, 5\n')
            saved = path.read_bytes(); path.write_bytes(b'addi x1, x0, 9\n')
            actual = self.derive(source=saved, program=path.relative_to(Path(__file__).resolve().parent.parent).as_posix(), instructions=1)
        self.assertEqual(actual.steps[0].writes, ((1, 5),))

    def test_snapshot_stock_notes_ignore_claims_in_annotations(self):
        normal = self.derive()
        source = b'addi x1, x0, 5 #: forged original capture | forged source\nc.addi x1, 1\n'
        annotated = self.derive(source=source)
        self.assertEqual([(s.writes, s.derivation, s.source) for s in normal.steps],
                         [(s.writes, s.derivation, s.source) for s in annotated.steps])
        self.assertNotEqual(normal.source_sha256, annotated.source_sha256)

    def test_source_controls_are_explicitly_unsupported(self):
        for prefix in [b'#|never: x31\n', b'#|refuse: load 0x80000000 0x4\n']:
            with self.subTest(prefix=prefix): self.rejected(Q.SnapshotUnsupported, source=prefix + SOURCE)

    def test_explicit_budget_not_end_marker_or_runoff_controls_execution(self):
        checked = self.derive(source=b'jal x0, 0 #|end\n', instructions=4096)
        self.assertEqual((checked.instructions, len(checked.steps)), (4096, 4096))
        self.assertTrue(all(step.pc == 0x80000000 and step.writes == () for step in checked.steps))
        self.assertEqual(self.derive(source=b'addi x1, x0, 5\n', instructions=3).instructions, 3)

    def test_gpr_changes_elide_same_value_and_x0_writes(self):
        checked = self.derive(source=b'addi x1, x0, 5\naddi x1, x0, 5\naddi x0, x0, 7\n', instructions=3)
        self.assertEqual([s.writes for s in checked.steps], [((1, 5),), (), ()])

    def test_actual_self_modified_instruction_is_recorded(self):
        source = b'auipc x1, 0\naddi x1, x1, 24\nlui x2, 0x700\naddi x2, x2, 0x293\nsw x2, 0, x1\naddi x0, x0, 0\naddi x5, x0, 1\n'
        checked = self.derive(source=source, instructions=7)
        self.assertEqual((checked.steps[-1].pc, checked.steps[-1].instruction_bits, checked.steps[-1].writes),
                         (0x80000018, 0x00700293, ((5, 7),)))
        original = b''.join(word.to_bytes(4, 'little') for word in
                            (0x00000097, 0x01808093, 0x00700137, 0x29310113,
                             0x0020A023, 0x00000013, 0x00100293))
        self.assertEqual((checked.payload_size, checked.payload_sha256),
                         (28, hashlib.sha256(original).hexdigest()))

    def test_halt_and_fetch_fault_have_no_complete_instruction(self):
        halted = self.derive(source=b'wfi\naddi x1, x0, 5\n', instructions=3)
        self.assertEqual([(s.instruction_bits, s.instruction_length, s.fetches) for s in halted.steps[1:]],
                         [(None, None, 0), (None, None, 0)])
        fault = self.derive(source=b'jal x0, -4\n', instructions=2)
        self.assertEqual((fault.steps[1].instruction_bits, fault.steps[1].instruction_length, fault.steps[1].fetches),
                         (None, None, 1))

    def test_semantic_shape_outside_existing_author_is_unsupported(self):
        self.rejected(Q.SnapshotUnsupported, source=b'csrrw x1, mcycle, x0\n', instructions=1)

    def test_incomplete_or_mutable_internal_result_refuses(self):
        core = Q._derive_parcel_lines
        for damage in ['steps', 'image']:
            def run(*args, **kwargs):
                result = core(*args, **kwargs)
                if damage == 'steps': result.steps.pop()
                else: result.image = bytearray(result.image)
                return result
            with self.subTest(damage=damage), mock.patch.object(Q, '_derive_parcel_lines', side_effect=run):
                self.rejected(Q.SnapshotError, 'invalid image or incomplete budget')

    def test_no_outputs_or_reference_processes(self):
        with mock.patch.object(Path, 'write_bytes', side_effect=AssertionError('file write')), \
             mock.patch.object(Path, 'write_text', side_effect=AssertionError('file write')), \
             mock.patch('subprocess.run', side_effect=AssertionError('process')), \
             mock.patch('subprocess.Popen', side_effect=AssertionError('process')):
            self.assertEqual(self.derive().steps[1].writes, ((1, 6),))


MUTATIONS = {
    'budget': ('if type(instructions) is not int or not 1 <= instructions <= 4096:', 'if False:'),
    'source-preflight': ('lines = G.prepare_guest_source(source, program=program, entry=ENTRY)', 'lines = source.decode("utf-8").splitlines()'),
    'canonical-context': ('assembler = G.canonical_guest_assembler()', 'assembler = Assembler(ENCODING)'),
    'budget-forward': ('_derive_parcel_lines(lines, assembler, instructions, program=program,', '_derive_parcel_lines(lines, assembler, 1, program=program,'),
    'stock-notes': ('annotations=False, controls=False,', 'annotations=True, controls=False,'),
    'source-controls': ('annotations=False, controls=False,', 'annotations=False, controls=True,'),
    'complete-result': ('if (type(run.image) is not bytes or len(run.image) > G.PAYLOAD_BYTES\n            or len(run.steps) != instructions):', 'if False:'),
    'raw-bits': ('step.instruction_bits = bits', 'step.instruction_bits = None'),
    'source-fingerprint': ('hashlib.sha256(source).hexdigest()', 'hashlib.sha256(run.image).hexdigest()'),
    'payload-fingerprint': ('hashlib.sha256(run.image).hexdigest()', 'hashlib.sha256(source).hexdigest()'),
    'writes-copy': ('tuple(sorted(step.writes.items()))', 'step.writes'),
    'result-frozen': ('@dataclass(frozen=True)\nclass SnapshotDerivation:', '@dataclass\nclass SnapshotDerivation:'),
    'step-frozen': ('@dataclass(frozen=True)\nclass SnapshotStep:', '@dataclass\nclass SnapshotStep:'),
    'program-label': ('SnapshotDerivation(program,', 'SnapshotDerivation("other.s",'),
    'source-reopen': ('lines = G.prepare_guest_source(source, program=program, entry=ENTRY)', 'lines = G.prepare_guest_source(Path(program).read_bytes(), program=program, entry=ENTRY)'),
}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--mutation', choices=MUTATIONS)
    args = parser.parse_args()
    if args.mutation:
        global Q
        before, after = MUTATIONS[args.mutation]
        source = Path(Q.__file__).read_text()
        if source.count(before) != 1: raise SystemExit('mutation seam is not singular')
        module = types.ModuleType('mutated_snapshot_author'); module.__file__ = Q.__file__
        sys.modules[module.__name__] = module
        exec(compile(source.replace(before, after), Q.__file__, 'exec'), module.__dict__)
        Q = module
    result = unittest.TextTestRunner(verbosity=1).run(unittest.defaultTestLoader.loadTestsFromTestCase(SnapshotTests))
    print(f'GC-SNAPSHOT-AUTHOR: {result.testsRun} tests / {len(result.failures)} failures / {len(result.errors)} errors; no reference execution')
    return 0 if result.wasSuccessful() else 1


if __name__ == '__main__': raise SystemExit(main())
