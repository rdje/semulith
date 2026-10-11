#!/usr/bin/env python3
"""Synthetic byte-unit controls; these never constitute execution evidence."""
from __future__ import annotations

import argparse
from copy import deepcopy
from dataclasses import FrozenInstanceError, replace
from pathlib import Path
import sys
import types
import unittest
from unittest import mock

import dossier_sexp as D
import matched_gpr_comparison as M
import probe_sail_comparison as P
import records_sexp as R
import run_rv64gc_sail as Sail


def encode(doc):
    return R.render_forms([D.expectations_to_form(doc)]).encode()


def fixture():
    base = P.expected([{'x1': '0x1'}, {'x2': '0x2', 'x3': '0x3'}])
    changed = deepcopy(base); changed['step'][1]['writes']['x2'] = '0x9'
    raw = P.trace([{'x1': 1}, {'x2': 2, 'x3': 3}]).encode()
    run = M.RunBytes(raw, 0)
    return dict(instructions=2, witness=M.GprWitness(1, 'x2'),
                baseline_expectation=encode(base), control_expectation=encode(changed),
                baseline=run, repeat=run, control=run)


class UnitTests(unittest.TestCase):
    def setUp(self):
        self.args = fixture()

    def outcome(self, disposition, reason=None):
        result = M.compare_unit(**self.args)
        self.assertEqual(result.disposition, disposition)
        if reason: self.assertIn(reason, result.reason)
        return result

    def refusal(self, reason):
        with self.assertRaisesRegex(M.UnitError, reason): M.compare_unit(**self.args)

    def change_doc(self, key, mutate):
        # Only fixtures map here; production mapping still belongs to dossier_sexp.
        forms = M.S.parse(self.args[key].decode())
        doc = D.expectations_to_doc(forms[0]); mutate(doc)
        self.args[key] = encode(doc)

    def test_positive_has_three_computed_results(self):
        result = self.outcome('satisfied', 'authentication and qualification pending')
        self.assertEqual(tuple(r.run_kind for r in result.runs), ('baseline', 'repeat', 'control'))
        self.assertEqual(tuple(r.comparison.verdict for r in result.runs), ('AGREE', 'AGREE', 'DIVERGE'))
        self.assertTrue(all(r.refusal is None for r in result.runs))
        self.assertEqual(result.runs[2].comparison.gpr_difference,
                         Sail.GprDifference(1, (('x2', 2), ('x3', 3)), (('x2', 9), ('x3', 3))))

    def test_first_boundary_and_maximum_register_value(self):
        base=P.expected([{'x31':'0xffffffffffffffff'}]); changed=deepcopy(base)
        changed['step'][0]['writes']['x31']='0x0'; run=M.RunBytes(P.trace([{'x31':2**64-1}]).encode(),0)
        self.args.update(instructions=1,witness=M.GprWitness(0,'x31'),baseline_expectation=encode(base),
                         control_expectation=encode(changed),baseline=run,repeat=run,control=run)
        self.outcome('satisfied')

    def test_later_change_to_zero_is_observed(self):
        base=P.expected([{'x1':'0x1'},{'x1':'0x0'}]);changed=deepcopy(base)
        changed['step'][1]['writes']['x1']='0x2';run=M.RunBytes(P.trace([{'x1':1},{'x1':0}]).encode(),0)
        self.args.update(witness=M.GprWitness(1,'x1'),baseline_expectation=encode(base),
                         control_expectation=encode(changed),baseline=run,repeat=run,control=run)
        self.outcome('satisfied')

    def test_numeric_alias_is_not_a_changed_control(self):
        self.change_doc('control_expectation',lambda d:d['step'][1]['writes'].update(x2='0X0002'))
        self.outcome('failed','change the witnessed RV64 value')

    def test_leading_zero_hex_values_are_valid(self):
        self.change_doc('baseline_expectation',lambda d:d['step'][1]['writes'].update(x2='0x'+'0'*30+'2'))
        self.outcome('satisfied')

    def test_formatting_and_comments_are_not_expectation_data(self):
        self.args['control_expectation']=b'; diagnostic annotation\n'+self.args['control_expectation']+b'\n(comment "note")\n'
        self.outcome('satisfied')

    def test_other_metadata_is_retained_without_extra_observation_credit(self):
        for key in ('baseline_expectation','control_expectation'):
            self.change_doc(key,lambda d:d.update(entry='0x80000000',fetches=2,
                                                  never_written=['x4'],cross_model=True))
        self.outcome('satisfied')

    def test_outcomes_and_runs_are_immutable(self):
        result=self.outcome('satisfied')
        with self.assertRaises(FrozenInstanceError):result.disposition='failed'
        with self.assertRaises(FrozenInstanceError):result.runs[0].refusal='forged'
        with self.assertRaises(FrozenInstanceError):self.args['baseline'].process_exit=1
        with self.assertRaises(FrozenInstanceError):self.args['witness'].step_n=0

    def test_no_artifact_loader_or_reference_execution(self):
        with mock.patch.object(D,'load') as load, mock.patch.object(Sail,'run_guest') as run:
            self.outcome('satisfied')
            load.assert_not_called();run.assert_not_called()

    def test_each_failed_process_remains_a_failed_unit(self):
        for kind in ('baseline','repeat','control'):
            for code in (-9,1,127):
                with self.subTest(kind=kind,code=code):
                    self.args=fixture();self.args[kind]=replace(self.args[kind],process_exit=code)
                    result=self.outcome('failed',kind+' comparison refused')
                    record=next(r for r in result.runs if r.run_kind==kind)
                    self.assertIsNone(record.comparison);self.assertIn(f'rc={code}',record.refusal)

    def test_failed_baseline_still_records_all_three_comparisons(self):
        self.args['baseline']=replace(self.args['baseline'],process_exit=1)
        result=self.outcome('failed');self.assertEqual(len(result.runs),3)
        self.assertEqual(result.runs[2].comparison.verdict,'DIVERGE')

    def test_baseline_difference_fails(self):
        self.args['baseline']=M.RunBytes(P.trace([{'x1':4},{'x2':2,'x3':3}]).encode(),0)
        self.outcome('failed','baseline and repeat must both agree')

    def test_repeat_difference_fails(self):
        self.args['repeat']=M.RunBytes(P.trace([{'x1':1},{'x2':4,'x3':3}]).encode(),0)
        self.outcome('failed','baseline and repeat must both agree')

    def test_raw_repeat_alias_cannot_pass(self):
        self.args['repeat']=replace(self.args['repeat'],trace=b'banner\n'+self.args['repeat'].trace)
        self.outcome('failed','repeat raw bytes differ')

    def test_raw_control_alias_cannot_pass(self):
        self.args['control']=replace(self.args['control'],trace=self.args['control'].trace+b'\n')
        self.outcome('failed','control raw bytes differ')

    def test_missing_rows_fail_for_each_run(self):
        for kind in ('baseline','repeat','control'):
            with self.subTest(kind=kind):
                self.args=fixture();self.args[kind]=M.RunBytes(P.trace([{'x1':1}]).encode(),0)
                result=self.outcome('failed',kind+' comparison refused')
                self.assertIn('missing expected step 1',next(r.refusal for r in result.runs if r.run_kind==kind))

    def test_empty_raw_trace_is_representable_but_fails(self):
        self.args['control']=M.RunBytes(b'',0)
        self.outcome('failed','control comparison refused')

    def test_surplus_rows_fail(self):
        self.args['control']=replace(self.args['control'],trace=self.args['control'].trace+P.trace([{}]).replace('[0]','[2]').encode())
        self.outcome('failed','outside declared budget')

    def test_late_invalid_x0_cannot_make_a_negative_control(self):
        self.change_doc('control_expectation',lambda d:d['step'][0]['writes'].update(x1='0x9'))
        self.args['control']=M.RunBytes(P.trace([{'x1':1},{'x0':1}]).encode(),0)
        self.outcome('failed','x0 trace write is nonzero')

    def test_malformed_raw_trace_fails(self):
        self.args['control']=replace(self.args['control'],trace=self.args['control'].trace+b'[broken]\n')
        self.outcome('failed','malformed trace record')

    def test_non_utf8_raw_trace_fails(self):
        self.args['control']=M.RunBytes(b'\xff',0)
        self.outcome('failed','control comparison refused')

    def decimal_trace(self, kind):
        raw=self.args['control'].trace
        if kind=='step':return raw.replace(b'[1]',b'['+b'9'*5000+b']',1)
        return raw.replace(b'x2 <-',b'x'+b'9'*5000+b' <-',1)

    def decimal_refusal(self, raw):
        self.args['control']=M.RunBytes(raw,0)
        try:
            result=M.compare_unit(**self.args)
        except Exception as exc:
            self.fail('decimal conversion escaped comparison refusal: '+type(exc).__name__)
        self.assertEqual(result.disposition,'failed')
        self.assertIn('decimal trace index cannot be converted',result.reason)
        want=D.expectations_to_doc(M.S.parse(self.args['baseline_expectation'].decode())[0])
        try:
            Sail.compare_trace(want,raw.decode(),0)
        except Sail.SailError as exc:
            self.assertIn('decimal trace index cannot be converted',str(exc))
        except Exception as exc:
            self.fail('decimal conversion escaped legacy refusal: '+type(exc).__name__)
        else:self.fail('unconvertible decimal accepted by legacy API')

    def injected_decimal_refusal(self, kind):
        original=int
        def converting(value, base=10):
            if base==10 and value=='9'*5000:raise ValueError('injected native conversion refusal')
            return original(value,base)
        # Isolate conversion injection from the adapter's isinstance(..., int).
        helper=Sail._decimal_trace_index
        isolated=types.FunctionType(helper.__code__,{**helper.__globals__,'int':converting},
                                    helper.__name__,helper.__defaults__,helper.__closure__)
        with mock.patch.object(Sail,'_decimal_trace_index',isolated):
            self.decimal_refusal(self.decimal_trace(kind))

    def test_step_decimal_conversion_failure_refuses(self):
        self.injected_decimal_refusal('step')

    def test_register_decimal_conversion_failure_refuses(self):
        self.injected_decimal_refusal('register')

    def test_native_configured_decimal_limit_refuses(self):
        if not hasattr(sys,'set_int_max_str_digits'):self.skipTest('interpreter has no configured decimal conversion limit')
        previous=sys.get_int_max_str_digits()
        try:
            sys.set_int_max_str_digits(640)
            for kind in ('step','register'):
                with self.subTest(kind=kind):
                    self.args=fixture();self.decimal_refusal(self.decimal_trace(kind))
        finally:sys.set_int_max_str_digits(previous)

    def test_wrong_witness_target_fails(self):
        self.args['witness']=M.GprWitness(1,'x3')
        self.outcome('failed','change the witnessed RV64 value')

    def test_missing_witness_change_fails(self):
        self.args['witness']=M.GprWitness(0,'x2')
        self.outcome('failed','declare the register change')

    def test_changed_program_fails(self):
        self.change_doc('control_expectation',lambda d:d.update(program='other.s'))
        self.outcome('failed','outside the sole witnessed value')

    def test_changed_other_expectation_metadata_fails(self):
        for field in ('insn','derivation','source','limit'):
            with self.subTest(field=field):
                self.args=fixture();self.change_doc('control_expectation',lambda d:d['step'][1].update({field:'changed'}))
                self.outcome('failed','outside the sole witnessed value')

    def test_extra_control_change_fails(self):
        self.change_doc('control_expectation',lambda d:d['step'][1]['writes'].update(x4='0x4'))
        self.outcome('failed','outside the sole witnessed value')

    def test_wrong_earlier_change_fails(self):
        self.change_doc('control_expectation',lambda d:d['step'][0]['writes'].update(x1='0x4'))
        self.outcome('failed','outside the sole witnessed value')

    def test_exact_structured_difference_required(self):
        good=Sail.GprDifference(1,(('x2',2),('x3',3)),(('x2',9),('x3',3)))
        cases=[Sail.Comparison('AGREE','no difference'),Sail.Comparison('DIVERGE','delivery'),
               Sail.Comparison('DIVERGE','wrong step',replace(good,step_n=0)),
               Sail.Comparison('DIVERGE','missing observed',replace(good,observed=(('x2',2),))),
               Sail.Comparison('DIVERGE','wrong expected',replace(good,expected=(('x2',8),('x3',3)))),
               Sail.Comparison('DIVERGE','extra observed',replace(good,observed=good.observed+(('x4',4),)))]
        for result in cases:
            with self.subTest(result=result),mock.patch.object(Sail,'compare_observations',side_effect=[Sail.Comparison('AGREE','base'),Sail.Comparison('AGREE','repeat'),result]):
                self.outcome('failed','exactly the witnessed complete GPR change sets')

    def test_unsupported_expectations_earn_no_comparison_credit(self):
        mutations=[lambda d:d.update(cross_model=False),
                   lambda d:d.update(expect_divergence={'difference':'known','at_step':1}),
                   lambda d:d.update(refuse=[{'kind':'fetch','base':'0x80000000','size':'0x4'}])]
        for key in ('baseline_expectation','control_expectation'):
            for mutate in mutations:
                with self.subTest(key=key,mutate=mutate):
                    self.args=fixture();self.change_doc(key,mutate)
                    result=self.outcome('unsupported');self.assertEqual(result.runs,())

    def test_invalid_parent_budget_refuses_before_parse(self):
        for value in (0,-1,True,1.5,'2',4097):
            with self.subTest(value=value),mock.patch.object(M,'_expectation',side_effect=M.UnitError('unexpected parser entry')):
                self.args['instructions']=value;self.refusal('parent budget')

    def test_invalid_witness_refuses(self):
        values=[None,{'step_n':1,'register':'x2'},M.GprWitness(-1,'x2'),M.GprWitness(2,'x2'),
                M.GprWitness(True,'x2'),M.GprWitness(1,'x0'),M.GprWitness(1,'x01'),
                M.GprWitness(1,'x32'),M.GprWitness(1,'f2'),M.GprWitness(1,'x2\n')]
        for value in values:
            with self.subTest(value=value):self.args['witness']=value;self.refusal('witness must name')

    def test_typed_runs_and_integer_exits_required(self):
        for value in (None,{'trace':b'','process_exit':0},M.RunBytes(b'',True),M.RunBytes(b'','0')):
            with self.subTest(value=value):self.args['baseline']=value;self.refusal('typed run and actual integer')

    def test_mutable_or_text_payloads_refuse(self):
        for key in ('baseline_expectation','control_expectation','baseline','repeat','control'):
            for value in (bytearray(b'x'),memoryview(b'x'),'x'):
                with self.subTest(key=key,kind=type(value)):
                    self.args=fixture();self.args[key]=M.RunBytes(value,0) if key in ('baseline','repeat','control') else value
                    self.refusal('immutable snapshot bytes')

    def test_all_payload_bounds_precede_any_parser(self):
        for key in ('baseline_expectation','control_expectation','baseline','repeat','control'):
            with self.subTest(key=key),mock.patch.object(M,'_expectation',side_effect=M.UnitError('unexpected parser entry')):
                self.args=fixture();is_run=key in ('baseline','repeat','control');limit=M.TRACE_BYTES if is_run else M.EXPECTATION_BYTES
                value=b' '*(limit+1);self.args[key]=M.RunBytes(value,0) if is_run else value
                self.refusal('payload outside')

    def test_empty_expectation_refuses(self):
        self.args['baseline_expectation']=b'';self.refusal('payload outside')

    def test_exact_payload_limits_are_inclusive(self):
        for key in ('baseline_expectation','control_expectation'):
            raw=self.args[key];self.args[key]=raw+b' '*(M.EXPECTATION_BYTES-len(raw))
        raw=self.args['baseline'].trace;run=M.RunBytes(raw+b' '*(M.TRACE_BYTES-len(raw)),0)
        self.args.update(baseline=run,repeat=run,control=run);self.outcome('satisfied')

    def test_maximum_complete_budget_is_inclusive(self):
        base=P.expected([{'x1':'0x1'}]+[{}]*4095);changed=deepcopy(base);changed['step'][0]['writes']['x1']='0x2'
        run=M.RunBytes(P.trace([{'x1':1}]+[{}]*4095).encode(),0)
        self.args.update(instructions=4096,witness=M.GprWitness(0,'x1'),baseline_expectation=encode(base),control_expectation=encode(changed),baseline=run,repeat=run,control=run)
        self.outcome('satisfied')

    def test_schema_precedes_mapping(self):
        self.args['baseline_expectation']=self.args['baseline_expectation'].replace(b'(program',b'(unknown',1)
        with mock.patch.object(D,'expectations_to_doc',side_effect=M.UnitError('unexpected mapping')):
            self.refusal('shape')

    def test_duplicate_singular_fields_refuse(self):
        self.args['baseline_expectation']=self.args['baseline_expectation'].replace(b'(expectations',b'(expectations (instructions 2)',1)
        self.refusal('shape')

    def test_unknown_fields_cannot_be_silently_mapped_away(self):
        self.args['baseline_expectation']=self.args['baseline_expectation'].replace(b'(expectations',b'(expectations (unknown "hidden")',1)
        self.refusal('shape')

    def test_field_types_are_validated_before_mapping(self):
        changes=[(b'(instructions 2)',b'(instructions "2")'),
                 (b'(n 0)',b'(n "0")'),(b'(program "fixture.s")',b'(program 1)'),
                 (b'(reg "x1")',b'(reg 1)'),(b'(value "0x1")',b'(value 1)')]
        for old,new in changes:
            with self.subTest(field=old):
                self.args=fixture();self.assertIn(old,self.args['baseline_expectation'])
                self.args['baseline_expectation']=self.args['baseline_expectation'].replace(old,new,1)
                with mock.patch.object(D,'expectations_to_doc',side_effect=M.UnitError('unexpected mapping')):
                    self.refusal('shape')

    def test_extra_complete_root_refuses(self):
        self.args['baseline_expectation']*=2;self.refusal('exactly one expectations')

    def test_comments_only_refuse(self):
        self.args['baseline_expectation']=b'(comment "only")';self.refusal('exactly one expectations')

    def test_non_utf8_expectation_refuses(self):
        self.args['baseline_expectation']=b'\xff';self.refusal('cannot decode/validate')

    def test_duplicate_write_keys_refuse_before_collapse(self):
        self.args['baseline_expectation']=self.args['baseline_expectation'].replace(b'(writes',b'(writes (write (reg "x1") (value "0x1"))',1)
        self.refusal('duplicate write register')

    def test_missing_or_mismatched_declared_budget_refuses(self):
        for mutate in (lambda d:d.pop('instructions'),lambda d:d.update(instructions=1)):
            with self.subTest(mutate=mutate):
                self.args=fixture();self.change_doc('baseline_expectation',mutate);self.refusal('instruction budget differs')

    def test_noncomplete_or_unordered_steps_refuse(self):
        for numbers in ([0],[0,0],[1,0],[0,2]):
            with self.subTest(numbers=numbers):
                self.args=fixture()
                def mutate(d):
                    d['step']=d['step'][:len(numbers)]
                    for step,n in zip(d['step'],numbers):step['n']=n
                self.change_doc('baseline_expectation',mutate);self.refusal('complete ordered budget')

    def test_invalid_change_registers_refuse(self):
        for register in ('x0','x01','x32','f1','x1\n'):
            with self.subTest(register=register):
                self.args=fixture();self.change_doc('baseline_expectation',lambda d:d['step'][0]['writes'].update({register:'0x1'}))
                self.refusal('canonical x1..x31')

    def test_invalid_rv64_values_refuse(self):
        for value in ('','1','-0x1','+0x1','0x','0xg','0x1\n','0x10000000000000000'):
            with self.subTest(value=value):
                self.args=fixture();self.change_doc('baseline_expectation',lambda d:d['step'][0]['writes'].update(x1=value))
                self.refusal('shape|hexadecimal RV64')


MUTATIONS = {
    'byte-bounds': ('if len(payload) > limit or (not empty and not payload):','if False:'),
    'budget-cap': ('not 1 <= instructions <= MAX_BOUNDARIES','not 1 <= instructions'),
    'raw-schema': ('if errors:','if False:'),
    'root-count': ('len(forms) != 1','not forms'),
    'step-sequence': ('[s["n"] for s in doc["step"]] != list(range(instructions))','False'),
    'rv64-range': ('len(value[2:].lstrip("0")) > 16','False'),
    'process-exit': ('run.trace.decode("utf-8"), run.process_exit','run.trace.decode("utf-8"), 0'),
    'unsupported': ('if doc.get("cross_model") is False or "expect_divergence" in doc or "refuse" in doc:','if False:'),
    'repeat-bytes': ('if repeat.trace != baseline.trace:','if False:'),
    'control-bytes': ('if control.trace != baseline.trace:','if False:'),
    'sole-value': ('if restored != base:','if False:'),
    'structured-difference': ('if (result.verdict != "DIVERGE" or difference is None or difference.step_n != n\n            or difference.observed != observed or difference.expected != expected):','if False:'),
    'witness-register': ('not _REGISTER.fullmatch(witness.register)','False'),
    'decimal-conversion': ("except ValueError as exc:\n        raise SailError", "except TypeError as exc:\n        raise SailError"),
}


def main():
    global M, Sail
    cli=argparse.ArgumentParser(description=__doc__);cli.add_argument('--mutation',choices=tuple(MUTATIONS));args=cli.parse_args()
    if args.mutation:
        owner=Sail if args.mutation=='decimal-conversion' else M
        source=Path(owner.__file__).read_text();old,new=MUTATIONS[args.mutation]
        if source.count(old)!=1:raise SystemExit('mutation seam drift')
        module=types.ModuleType('comparison_unit_mutant');module.__file__=owner.__file__;sys.modules[module.__name__]=module
        exec(compile(source.replace(old,new),owner.__file__,'exec'),module.__dict__)
        if args.mutation=='decimal-conversion':Sail=module;M.Sail=module
        else:M=module
    result=unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(UnitTests))
    return 0 if result.wasSuccessful() else 1


if __name__=='__main__':raise SystemExit(main())
