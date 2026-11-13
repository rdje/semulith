#!/usr/bin/env python3
"""Exact-token regressions through the public schema kernel, without changing search semantics.

The controls and their mutations judge a frozen copy, `scripts/fixtures/record-schema/`, so a damaged real schema
cannot read as a check that does not discriminate. `--live` is RECORD-SCHEMA's real-run step: every real facet and the
five complete documents, each finding by its own name (XTASK.13 slice i).
"""
from __future__ import annotations

import argparse
import copy
from pathlib import Path
import sys
import tempfile
import types
import unittest

import check_sexp_schema as K
import records_sexp as R
import sexp as S

ROOT = Path(__file__).resolve().parent.parent
FROZEN = ROOT / 'scripts/fixtures/record-schema'
FROZEN_FACETS = 38  # one per token language at the freeze; a later language joins TOKENS and the real inventory only
# What the real tree states. A new or lost facet moves these two and nothing else.
LIVE_SCHEMAS = 33  # schema/identity.sexp (P4-SYSTEM.20 slice a); schema/alternative.sexp (P4-SYSTEM.14 a50-1); schema/credits.sexp (a42ay); schema/workload.sexp (P4-SYSTEM.15 slice f); schema/matched-case.sexp (P4-SYSTEM.14 a44-2a); schema/overlay.sexp (a43b-3c, no anchored pattern); schema/config-effect.sexp (a43b-3f); schema/dispositions.sexp (a51-7)
LIVE_FACETS = 157  # +2: an identity's unit and version (P4-SYSTEM.20 slice a); +2: a recorded row's covers (P4-SYSTEM.18 slice a); +10: a selection's record and its credit (a51-11); +21: matched-case.sexp's facets (a44-2a); +5: its control id and second-method forms (a43b-2b); +6: config-effect.sexp's case id and five digests (a43b-3f); +8: dispositions.sexp's two and config-effect.sexp's walk_trace's six (a51-7)
BOUNDARY_BREAKERS = (lambda v: v + '\n', lambda v: '\n' + v, lambda v: v + '\r\n', lambda v: v + '\n\n', lambda v: v + '\x00', lambda v: v + '\t')
# Named valid tokens, independent of anchor implementation. A new token language
# needs a reviewed example here; silently skipping an unknown pattern is forbidden.
TOKENS = {
    r'^DS-[A-Z0-9-]+': 'DS-A',
    r'^SEL-[A-Z0-9-]+': 'SEL-A',  # credits.sexp and dispositions.sexp: a selection's record (P4-SYSTEM.14 a51-11)
    r'^[A-Z][A-Za-z]*-[a-z0-9.]+-[0-9]+\.S': 'Zaamo-amoadd.d-00.S',  # act4.sexp: <Suite>-<mnemonic>-<nn>.S since P4-SYSTEM.15 slice b
    r'^wl-[a-z]+\.c': 'wl-integer.c',  # workload.sexp: a tracked workload source, P4-SYSTEM.15 slice f
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
    r'^20[0-9]{2}-[0-9]{2}-[0-9]{2}': '2026-10-23',  # credits.sexp: the crediting date (a42ay)
    r'^decision_[a-z0-9-]+\.md': 'decision_example-record.md',  # credits.sexp: the decision record a credit cites
    r'^[a-z0-9][a-z0-9-]*-v[0-9]+': 'rv64gc-m-forms-v3',  # matched-case.sexp: a case id, its directory's name (a44-2a)
    r'^[a-z0-9][a-z0-9-]*\.s': 'm-forms.s',  # matched-case.sexp: the guest program
    r'^(guest-image|reference-config|expectation)': 'guest-image',  # matched-case.sexp: a prepared input's role
    r'^[A-Za-z0-9][A-Za-z0-9._-]*': 'guest.elf',  # matched-case.sexp: a prepared input's file name
    r'^(form|table1):[A-Za-z0-9._-]+': 'form:div',  # matched-case.sexp: the policy cell a property serves
    r'^[a-z0-9][a-z0-9-]*': 'truncated-address',  # matched-case.sexp: a control run's declared id (a43b-2b)
    r'^(independent-exact-expectation|bounded-exhaustive-check|source-grounded-invariant-check|qualified-hardware-observation)':
        'independent-exact-expectation',  # matched-case.sexp: a second method's kind, the policy's four (a43b-2b)
}
REAL_DOCUMENTS = (
    ('profiles/rv64gc-lab-v0/references.sexp', 'references', 'binary_sha256'),
    ('profiles/rv64gc-lab-v0/sources.sexp', 'sources', 'sha256'),
    ('profiles/rv64gc-lab-v0/requirements.sexp', 'requirements', 'id'),
    ('materials/units.sexp', 'units', 'id'),
    ('profiles/netboard-lab-v0/board.sexp', 'board', 'dossier-sha256'),
)


def language(pattern):
    """A facet's token language, or None when no reviewed boundary ends it."""
    if pattern.endswith(r'\Z'):
        return pattern[:-2]
    return pattern[:-1] if pattern.endswith('$') else None


def cases():
    """The controls' facets: the frozen copy's, one per token language."""
    path = FROZEN / 'schema-tokens.sexp'
    constructs, _ = K.load_schema(path)
    return [(f'{path.name}/{head}/{name}', field, TOKENS[language(field.pattern)])
            for head, construct in constructs.items()
            for name, field in construct.fields.items()]


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


def changed_document(path, field):
    name = path.name
    forms = S.parse(path.read_text(), name)
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


def live_findings(root, documents=REAL_DOCUMENTS, stated=(LIVE_SCHEMAS, LIVE_FACETS)):
    """Every real facet and complete document, each finding by its own name; the real run's step."""
    findings, used, facets = [], set(), 0
    paths = sorted((root / 'schema').glob('*.sexp'))
    for path in paths:
        try:
            constructs, _ = K.load_schema(path)
        except Exception as error:  # A schema that cannot load is a finding about that schema.
            findings.append(f"schema/{path.name}: cannot load: {str(error).replace(f'{root}/', '')}")
            continue
        for head, construct in constructs.items():
            for name, field in construct.fields.items():
                if field.pattern is None:
                    continue
                facets += 1
                tag = f'schema/{path.name}/{head}/{name}'
                body = language(field.pattern)
                if body is None:
                    findings.append(f'{tag}: no reviewed token boundary: {field.pattern}')
                elif body not in TOKENS:
                    findings.append(f'{tag}: no reviewed token example: {body}')
                else:
                    used.add(body)
                    if judge(field, TOKENS[body]):
                        findings.append(f'{tag}: refuses its reviewed example {TOKENS[body]!r}')
                    for breaker in BOUNDARY_BREAKERS:
                        bad = breaker(TOKENS[body])
                        if not any('does not match' in error for error in judge(field, bad)):
                            findings.append(f'{tag}: admits {bad!r}')
    if len(paths) != stated[0]:
        findings.append(f'schema/: {len(paths)} schema file(s), the inventory states {stated[0]}')
    if facets != stated[1]:
        findings.append(f'schema/: {facets} anchored facet(s), the inventory states {stated[1]}')
    findings.extend(f'TOKENS: a reviewed example no facet uses: {body}' for body in sorted(set(TOKENS) - used))
    for name, schema, field in documents:
        try:
            constructs, operators = K.load_schema(root / f'schema/{schema}.sexp')
            errors = K.validate_text((root / name).read_text(), constructs, operators, name)
            findings.extend(errors)  # Each already names the document.
            if not errors and not any('does not match' in error for error in K.validate_text(
                    changed_document(root / name, field), constructs, operators, name)):
                findings.append(f'{name}: admits a terminal newline in its {field}')
        except Exception as error:  # A document that cannot be read is a finding about that document.
            findings.append(f"{name}: cannot judge: {str(error).replace(f'{root}/', '')}")
    return findings


class TokenFacetTests(unittest.TestCase):
    def test_closed_inventory_and_examples(self):
        current = cases()
        self.assertEqual(len(current), FROZEN_FACETS)
        self.assertLessEqual({language(field.pattern) for _, field, _ in current}, set(TOKENS))

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

    def test_complete_documents_stay_valid(self):
        for name, schema, _ in REAL_DOCUMENTS:
            with self.subTest(document=name):
                constructs, operators = K.load_schema(FROZEN / f'schema-{schema}.sexp')
                path = FROZEN / f'document-{Path(name).name}'
                self.assertEqual(K.validate_text(path.read_text(), constructs, operators, path.name), [])

    def test_complete_document_newlines_refuse(self):
        for name, schema, field in REAL_DOCUMENTS:
            with self.subTest(document=name):
                constructs, operators = K.load_schema(FROZEN / f'schema-{schema}.sexp')
                path = FROZEN / f'document-{Path(name).name}'
                errors = K.validate_text(changed_document(path, field), constructs, operators, path.name)
                self.assertTrue(any('does not match' in error for error in errors))

    def test_the_real_run_step_names_what_it_finds(self):
        base = ROOT / 'target/record-catalog-probe'
        base.mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryDirectory(dir=base) as scratch:
            root = Path(scratch)
            (root / 'schema').mkdir()
            (root / 'schema/a.sexp').write_text('(schema (id "a"))\n(construct (name a)\n'
                                                '  (field (name kept) (type string) (pattern "^[0-9]+\\\\Z"))\n'
                                                '  (field (name loose) (type string) (pattern "^[0-9]+$"))\n'
                                                '  (field (name open) (type string) (pattern "needle"))\n'
                                                '  (field (name unknown) (type string) (pattern "^unreviewed\\\\Z")))\n')
            (root / 'schema/b.sexp').write_text('(schema (id "b"))\n(construct')
            found = live_findings(root, documents=(('absent.sexp', 'a', 'kept'),), stated=(3, 5))
        for want in ('schema/a.sexp/a/loose: admits', 'schema/a.sexp/a/open: no reviewed token boundary',
                     'schema/a.sexp/a/unknown: no reviewed token example', 'schema/b.sexp: cannot load',
                     'schema/: 2 schema file(s), the inventory states 3',
                     'schema/: 4 anchored facet(s), the inventory states 5',
                     'TOKENS: a reviewed example no facet uses', 'absent.sexp: cannot judge'):
            self.assertTrue(any(line.startswith(want) for line in found), (want, found))

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
    cli.add_argument('--live', action='store_true', help="judge the real schemas and documents, RECORD-SCHEMA's real-run step")
    args = cli.parse_args()
    if args.live:
        if args.mutation:
            cli.error('--live judges the real tree; the mutations belong to the controls')
        found = live_findings(ROOT)
        for finding in found:
            print(finding)
        if not found:
            print(f'TOKEN-FACETS: ok ({LIVE_FACETS} anchored facet(s) in {LIVE_SCHEMAS} schema(s) and {len(REAL_DOCUMENTS)} complete document(s) hold their boundaries)')
        return int(bool(found))
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
