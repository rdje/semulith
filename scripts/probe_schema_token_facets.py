#!/usr/bin/env python3
"""Exact-token regressions through the public schema kernel, without changing search semantics."""
from __future__ import annotations

import argparse
import copy
from pathlib import Path
import sys
import types
import unittest

import check_sexp_schema as K
import records_sexp as R
import sexp as S

ROOT = Path(__file__).resolve().parent.parent
# Named valid tokens, independent of anchor implementation. A new token language
# needs a reviewed example here; silently skipping an unknown pattern is forbidden.
TOKENS = {
    r'^I-[a-z0-9]+-[0-9]+\.S': 'I-add-01.S',
    r'^[0-9a-f]{64}': 'a' * 64,
    r'^0x[0-9a-f]{1,4}(_[0-9a-f]{4})*': '0x8000_0000',
    r'^OB-[A-Z0-9-]+': 'OB-EXAMPLE',
    r'^D-[A-Z0-9-]+': 'D-EXAMPLE',
    r'^(C|D)[0-9]{2}': 'C01',
    r'^[A-Za-z][A-Za-z0-9._:/-]*': 'REQ-example/v1:part',
    r'^[a-z0-9-]+-v[0-9]+': 'rv64gc-lab-v0',
    r'^[0-9]+': '0',
    r'^crates/[A-Za-z0-9_/-]+\.rs': 'crates/example/src/lib.rs',
    r'^[A-Z][A-Z0-9-]*': 'CPU-SYSTEM',
    r'^[A-Za-z0-9_./-]+': 'profiles/example/record.sexp',
    r'^[a-z_][a-z0-9_]*': 'example_check',
    r'^[A-Z][A-Z0-9-]*\.[0-9]+': 'P4-SYSTEM.14',
    r'^matched-gpr-dependencies-v1': 'matched-gpr-dependencies-v1',
    r'^[a-z0-9_]+': 'rv64gc',
    r'^matched-gpr-v1': 'matched-gpr-v1',
    r'^(gpr-change|witnessed-delivery)': 'gpr-change',
    r'^x([1-9]|[12][0-9]|3[01])': 'x31',
    r'^(reference|expected)': 'expected',
    r'^(baseline|repeat|control)': 'baseline',
    r'^(AGREE|DIVERGE|REFUSED)': 'AGREE',
    r'^(DIVERGE|REFUSED)': 'DIVERGE',
    r'^(shared|not-shared|no-evidence-of-sharing|not-examined)': 'not-examined',
    r'^[a-z0-9._]+': 'c.addi',
    r'^sail-gpr-capture-v1': 'sail-gpr-capture-v1',
    r'^(raw-gpr|process-stdout|process-stderr)': 'raw-gpr',
}
REAL_DOCUMENTS = (
    ('profiles/rv64gc-lab-v0/references.sexp', 'references', 'binary_sha256'),
    ('profiles/rv64gc-lab-v0/sources.sexp', 'sources', 'sha256'),
    ('profiles/rv64gc-lab-v0/requirements.sexp', 'requirements', 'id'),
    ('materials/units.sexp', 'units', 'id'),
    ('profiles/netboard-lab-v0/board.sexp', 'board', 'dossier-sha256'),
)


def cases():
    found = []
    for path in sorted((ROOT / 'schema').glob('*.sexp')):
        constructs, _ = K.load_schema(path)
        for head, construct in constructs.items():
            for name, field in construct.fields.items():
                if field.pattern is None:
                    continue
                pattern = field.pattern
                if pattern.endswith(r'\Z'):
                    body = pattern[:-2]
                elif pattern.endswith('$'):
                    body = pattern[:-1]
                else:
                    raise ValueError(f'no reviewed token boundary: {path.name}/{head}/{name}')
                if body not in TOKENS:
                    raise ValueError(f'no reviewed token example: {path.name}/{head}/{name}: {body}')
                found.append((f'{path.name}/{head}/{name}', field, TOKENS[body]))
    return found


def judge(field, value):
    # Isolate the real facet from unrelated required sibling/collection fields;
    # validate_text remains the same public kernel used by production callers.
    field = copy.deepcopy(field)
    field.name = 'value'
    field.repeat = field.optional = field.unique = False
    field.min = None
    construct = K.Construct('facet control', S.Symbol('fixture'), [])
    construct.fields['value'] = field
    return K.validate_text(R.render_forms([[S.Symbol('fixture'), [S.Symbol('value'), value]]]),
                           {'fixture': construct}, {}, 'facet control')


def changed_document(name, field):
    forms = S.parse((ROOT / name).read_text(), name)
    stack = list(forms)
    while stack:
        node = stack.pop(0)
        if not isinstance(node, list):
            continue
        if len(node) == 2 and node[0] == field and type(node[1]) is str:
            node[1] += '\n'
            return R.render_forms(forms)
        stack[0:0] = node[1:]
    raise ValueError(f'{name}: no {field} regression target')


class TokenFacetTests(unittest.TestCase):
    def test_closed_inventory_and_examples(self):
        current = cases()
        self.assertEqual(len(list((ROOT / 'schema').glob('*.sexp'))), 24)
        self.assertEqual(len(current), 91)
        self.assertEqual({field.pattern.removesuffix(r'\Z').removesuffix('$') for _, field, _ in current}, set(TOKENS))

    def test_named_positive_tokens(self):
        for tag, field, value in cases():
            with self.subTest(facet=tag):
                self.assertEqual(judge(field, value), [])

    def test_terminal_newline_refuses_every_token_facet(self):
        for tag, field, value in cases():
            with self.subTest(facet=tag):
                self.assertTrue(any('does not match' in error for error in judge(field, value + '\n')))

    def test_other_boundary_characters_refuse(self):
        for tag, field, value in cases():
            for bad in ('\n' + value, value + '\r\n', value + '\n\n', value + '\x00', value + '\t'):
                with self.subTest(facet=tag, bad=bad):
                    self.assertTrue(any('does not match' in error for error in judge(field, bad)))

    def test_real_complete_documents_stay_valid(self):
        for name, schema, _ in REAL_DOCUMENTS:
            with self.subTest(document=name):
                constructs, operators = K.load_schema(ROOT / f'schema/{schema}.sexp')
                self.assertEqual(K.validate_text((ROOT / name).read_text(), constructs, operators, name), [])

    def test_real_complete_document_newlines_refuse(self):
        for name, schema, field in REAL_DOCUMENTS:
            with self.subTest(document=name):
                constructs, operators = K.load_schema(ROOT / f'schema/{schema}.sexp')
                errors = K.validate_text(changed_document(name, field), constructs, operators, name)
                self.assertTrue(any('does not match' in error for error in errors))

    def test_generic_unanchored_pattern_remains_a_search(self):
        form = S.parse('(field (name value) (type string) (pattern "needle"))')[0]
        field = K.Field('generic search control', form)
        self.assertEqual(judge(field, 'λ hayneedlehay\n'), [])
        self.assertTrue(any('does not match' in error for error in judge(field, 'unmatched')))


MODES = ('loose-end', 'ignore-pattern', 'fullmatch')


def main():
    global K
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument('--mutation', choices=MODES)
    args = cli.parse_args()
    if args.mutation == 'loose-end':
        original = K.load_schema

        def loose_schema(path):
            constructs, operators = original(path)
            for construct in constructs.values():
                for field in construct.fields.values():
                    if field.pattern and field.pattern.endswith(r'\Z'):
                        field.pattern = field.pattern[:-2] + '$'
            return constructs, operators

        K.load_schema = loose_schema
    elif args.mutation:
        source = Path(K.__file__).read_text()
        old, new = (('if fld.pattern is not None and not re.search(', 'if False and not re.search(')
                    if args.mutation == 'ignore-pattern'
                    else ('not re.search(fld.pattern, value)', 'not re.fullmatch(fld.pattern, value)'))
        if source.count(old) != 1:
            raise SystemExit('mutation seam drift')
        module = types.ModuleType('schema_token_kernel_mutant')
        module.__file__ = K.__file__
        exec(compile(source.replace(old, new), K.__file__, 'exec'), module.__dict__)
        K = module
    result = unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(TokenFacetTests))
    return 0 if result.wasSuccessful() else 1


if __name__ == '__main__':
    raise SystemExit(main())
