#!/usr/bin/env python3
"""Structured adapter controls using synthetic text, never execution evidence."""
from __future__ import annotations

import argparse
from dataclasses import FrozenInstanceError
from pathlib import Path
import sys
import types
import unittest
from unittest import mock

import probe_gc_sail as P
import run_rv64gc_sail as S


def expected(writes):
    return {'program': 'fixture.s', 'instructions': len(writes),
            'step': [{'n': n, 'insn': 'fixture', 'writes': values,
                      'derivation': 'synthetic adapter observation', 'source': 'fixture'}
                     for n, values in enumerate(writes)]}


def trace(writes):
    lines = []
    for n, values in enumerate(writes):
        lines.append(f'[{n}] [M]: 0x{0x80000000 + 4*n:016x} (0x00000013) fixture')
        lines.extend(f'{reg} <- 0x{value:016x}' for reg, value in values.items())
    return '\n'.join(lines) + '\n'


class ComparisonTests(unittest.TestCase):
    def refusal(self, want, text, reason, status=0):
        for compare in (S.compare_observations, S.compare_trace):
            with self.assertRaisesRegex(S.SailError, reason):
                compare(want, text, status)

    def test_agreement_has_no_difference(self):
        result = S.compare_observations(expected([{'x1': '0x1'}]), trace([{'x1': 1}]))
        self.assertEqual(result.verdict, 'AGREE')
        self.assertIsNone(result.gpr_difference)
        self.assertEqual(result.detail, '1 declared steps; every change-observation and required row present')

    def test_exact_first_gpr_difference(self):
        result = S.compare_observations(expected([{'x1': '0x2'}]), trace([{'x1': 1}]))
        self.assertEqual(result.verdict, 'DIVERGE')
        self.assertEqual(result.gpr_difference, S.GprDifference(0, (('x1', 1),), (('x1', 2),)))
        self.assertEqual(result.detail, "step 0 (fixture): Sail {'x1': 1}, expectations {'x1': 2}")

    def test_first_boundary_not_later_difference(self):
        want = expected([{'x1': '0x1'}, {'x2': '0x3'}, {'x3': '0x5'}])
        result = S.compare_observations(want, trace([{'x1': 1}, {'x2': 2}, {'x3': 4}]))
        self.assertEqual(result.gpr_difference, S.GprDifference(1, (('x2', 2),), (('x2', 3),)))

    def test_last_boundary_difference(self):
        result = S.compare_observations(expected([{}, {'x31': '0x2'}]), trace([{}, {'x31': 1}]))
        self.assertEqual(result.gpr_difference, S.GprDifference(1, (('x31', 1),), (('x31', 2),)))

    def test_complete_canonical_change_sets(self):
        want = expected([{'x2': '0x9', 'x1': '0x8'}])
        result = S.compare_observations(want, trace([{'x2': 2, 'x10': 10, 'x1': 1}]))
        self.assertEqual(result.gpr_difference, S.GprDifference(
            0, (('x1', 1), ('x10', 10), ('x2', 2)), (('x1', 8), ('x2', 9))))

    def test_extra_observed_change_retained(self):
        result = S.compare_observations(expected([{}]), trace([{'x4': 4}]))
        self.assertEqual(result.gpr_difference, S.GprDifference(0, (('x4', 4),), ()))

    def test_missing_observed_change_retained(self):
        result = S.compare_observations(expected([{'x4': '0x4'}]), trace([{}]))
        self.assertEqual(result.gpr_difference, S.GprDifference(0, (), (('x4', 4),)))

    def test_unchanged_writes_are_not_changes(self):
        want = expected([{'x1': '0x1'}, {'x2': '0x2'}])
        text = trace([{'x1': 1}, {'x1': 1, 'x2': 2}])
        self.assertEqual(S.compare_observations(want, text).verdict, 'AGREE')
        want['step'][1]['writes']['x1'] = '0x1'
        self.assertEqual(S.compare_observations(want, text).gpr_difference,
                         S.GprDifference(1, (('x2', 2),), (('x1', 1), ('x2', 2))))

    def test_numerically_equal_hex_spellings_agree(self):
        result = S.compare_observations(expected([{'x1': '0X0001'}]), trace([{'x1': 1}]))
        self.assertEqual(result.verdict, 'AGREE')
        self.assertIsNone(result.gpr_difference)

    def test_maximum_rv64_value_retained(self):
        result = S.compare_observations(expected([{'x31': '0x1'}]), trace([{'x31': 2**64-1}]))
        self.assertEqual(result.gpr_difference, S.GprDifference(0, (('x31', 2**64-1),), (('x31', 1),)))

    def test_result_and_nested_difference_are_immutable(self):
        result = S.compare_observations(expected([{'x1': '0x2'}]), trace([{'x1': 1}]))
        self.assertIsInstance(result.gpr_difference, S.GprDifference)
        with self.assertRaises(FrozenInstanceError): result.verdict = 'AGREE'
        with self.assertRaises(FrozenInstanceError): result.gpr_difference.step_n = 9
        with self.assertRaises(TypeError): result.gpr_difference.observed[0] = ('x1', 9)

    def test_result_does_not_alias_caller_dictionary(self):
        want = expected([{'x1': '0x2'}])
        result = S.compare_observations(want, trace([{'x1': 1}]))
        want['step'][0]['writes']['x1'] = '0x9'
        self.assertEqual(result.gpr_difference, S.GprDifference(0, (('x1', 1),), (('x1', 2),)))

    def test_delivery_mismatch_has_no_gpr_difference(self):
        want = P.expected('<fetch page fault at 0x403000>', 'The fetch walk denies execute permission.')
        result = S.compare_observations(want, P.NOP)
        self.assertEqual(result.verdict, 'DIVERGE')
        self.assertIsNone(result.gpr_difference)
        self.assertEqual(result.detail, 'step 0: Sail printed an instruction row for declared delivery/wait')

    def test_witnessed_delivery_agrees(self):
        want = P.expected('<fetch page fault at 0x403000>', 'The fetch walk denies execute permission.')
        text = 'handling exc#fetch-page-fault at priv M | tval=0x0000000000403000\n'
        result = S.compare_observations(want, text)
        self.assertEqual(result.verdict, 'AGREE')
        self.assertIsNone(result.gpr_difference)

    def test_delivery_difference_precedes_later_gpr_difference(self):
        want = expected([{}, {'x1': '0x2'}])
        want['step'][0]['insn'] = '<fetch fault>'
        result = S.compare_observations(want, trace([{}, {'x1': 1}]))
        self.assertEqual(result.detail, 'step 0: Sail printed an instruction row for declared delivery/wait')
        self.assertIsNone(result.gpr_difference)

    def test_gpr_difference_precedes_later_delivery_difference(self):
        want = expected([{'x1': '0x2'}, {}])
        want['step'][1]['insn'] = '<fetch fault>'
        result = S.compare_observations(want, trace([{'x1': 1}, {}]))
        self.assertEqual(result.gpr_difference, S.GprDifference(0, (('x1', 1),), (('x1', 2),)))

    def test_delivery_difference_cannot_hide_nonzero_x0_in_same_row(self):
        want = P.expected('<fetch fault>')
        self.refusal(want, trace([{'x0': 1}]), 'x0 trace write is nonzero')

    def test_failed_process_refuses(self):
        for status in (-9, 1, 127):
            with self.subTest(status=status):
                self.refusal(expected([{}]), P.NOP, f'rc={status}', status)

    def test_empty_and_zero_budget_refuse(self):
        self.refusal(expected([{}]), '', 'missing expected step 0')
        self.refusal(expected([]), '', 'no positive program step budget')

    def test_incomplete_expectation_steps_refuse(self):
        want = expected([{}, {}]); want['step'][1]['n'] = 0
        self.refusal(want, trace([{}, {}]), 'incomplete, duplicated or out of order')

    def test_truncated_trace_refuses(self):
        self.refusal(expected([{}, {}]), trace([{}]), 'missing expected step 1')

    def test_early_gpr_difference_cannot_hide_missing_tail(self):
        self.refusal(expected([{'x1': '0x2'}, {}]), trace([{'x1': 1}]), 'missing expected step 1')

    def test_early_gpr_difference_cannot_hide_invalid_x0_tail(self):
        self.refusal(expected([{'x1': '0x2'}, {}]), trace([{'x1': 1}, {'x0': 1}]),
                     'x0 trace write is nonzero')

    def test_early_delivery_difference_cannot_hide_missing_tail(self):
        want = expected([{}, {}])
        want['step'][0]['insn'] = '<fetch page fault at 0x403000>'
        self.refusal(want, trace([{}]), 'missing expected step 1')

    def test_early_delivery_difference_cannot_hide_invalid_x0_tail(self):
        want = expected([{}, {}])
        want['step'][0]['insn'] = '<fetch page fault at 0x403000>'
        self.refusal(want, trace([{}, {'x0': 1}]), 'x0 trace write is nonzero')

    def test_surplus_instruction_before_earlier_difference_refuses(self):
        self.refusal(expected([{}]), trace([{'x1': 1}, {}]), 'instruction steps')

    def test_surplus_delivery_before_earlier_difference_refuses(self):
        event = 'handling int#supervisor-software-interrupt at priv M | tval=0x0000000000000000\n'
        self.refusal(expected([{}]), trace([{'x1': 1}]) + event, 'delivery steps')

    def test_malformed_late_record_before_earlier_difference_refuses(self):
        self.refusal(expected([{}]), trace([{'x1': 1}]) + '[broken]\n', 'malformed trace record')

    def test_duplicate_write_refuses(self):
        text = trace([{'x1': 1}]) + 'x1 <- 0x0000000000000002\n'
        self.refusal(expected([{'x1': '0x1'}]), text, 'duplicate GPR write')

    def test_invalid_or_orphan_write_refuses(self):
        self.refusal(expected([{}]), 'x1 <- 0x0000000000000001\n', 'invalid or orphan')
        self.refusal(expected([{}]), trace([{'x32': 1}]), 'invalid or orphan')

    def test_nonzero_x0_refuses(self):
        self.refusal(expected([{}]), trace([{'x0': 1}]), 'x0 trace write is nonzero')

    def test_zero_x0_is_not_a_change(self):
        result = S.compare_observations(expected([{}]), trace([{'x0': 0}]))
        self.assertEqual(result.verdict, 'AGREE')
        self.assertIsNone(result.gpr_difference)

    def test_legacy_wrapper_delegates_to_one_owner(self):
        want, text = expected([{}]), P.NOP
        result = S.Comparison('DIVERGE', 'opaque detail', S.GprDifference(0, (), (('x1', 1),)))
        with mock.patch.object(S, 'compare_observations', return_value=result) as compare:
            self.assertEqual(S.compare_trace(want, text, 7), ('DIVERGE', 'opaque detail'))
            compare.assert_called_once_with(want, text, 7)

    def test_legacy_tuple_values_match_structured_result(self):
        for want, text in ((expected([{}]), P.NOP),
                           (expected([{'x1': '0x2'}]), trace([{'x1': 1}])),
                           (P.expected('<fetch fault>'), P.NOP)):
            result = S.compare_observations(want, text)
            self.assertEqual(S.compare_trace(want, text), (result.verdict, result.detail))


MUTATIONS = {
    'lose-difference': ('GprDifference(n, tuple(sorted(changes.items())), tuple(sorted(want.items())))', 'None'),
    'wrong-boundary': ('GprDifference(n,', 'GprDifference(n + 1,'),
    'reverse-change-sets': ('GprDifference(n, tuple(sorted(changes.items())), tuple(sorted(want.items())))',
                            'GprDifference(n, tuple(sorted(want.items())), tuple(sorted(changes.items())))'),
    'lose-extra-changes': ('tuple(sorted(changes.items()))', 'tuple(sorted(changes.items()))[:1]'),
    'ignore-status': ('if returncode != 0:', 'if False:'),
    'ignore-extra-rows': ('if extra_rows := sorted(n for n in rows if n >= count):', 'if False:'),
    'ignore-extra-deliveries': ('if extra_deliveries := sorted(n for n in deliveries if n >= count):', 'if False:'),
    'bypass-wrapper': ('return result.verdict, result.detail', "return 'AGREE', 'bypassed'"),
    'early-gpr-return': ("first_difference = Comparison(\n                'DIVERGE', f'step {n} ({e[\"insn\"]})",
                         "return Comparison(\n                'DIVERGE', f'step {n} ({e[\"insn\"]})"),
    'early-delivery-return': ("first_difference = Comparison(\n                    'DIVERGE', f'step {n}: Sail printed",
                              "return Comparison(\n                    'DIVERGE', f'step {n}: Sail printed"),
}


def main():
    global S
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument('--mutation', choices=tuple(MUTATIONS))
    args = cli.parse_args()
    if args.mutation:
        source = Path(S.__file__).read_text()
        old, new = MUTATIONS[args.mutation]
        if source.count(old) != 1: raise SystemExit('mutation seam drift')
        module = types.ModuleType('sail_comparison_mutant')
        module.__file__ = S.__file__
        sys.modules[module.__name__] = module
        exec(compile(source.replace(old, new), S.__file__, 'exec'), module.__dict__)
        S = module
    result = unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(ComparisonTests))
    return 0 if result.wasSuccessful() else 1


if __name__ == '__main__':
    raise SystemExit(main())
