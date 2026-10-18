#!/usr/bin/env python3
"""Synthetic graph/input integration controls; no reference execution or qualification."""
from __future__ import annotations

import argparse
from dataclasses import FrozenInstanceError, replace
import hashlib
from pathlib import Path
import sys
import tempfile
import types
import unittest
from unittest import mock

import change_impact as I
import matched_gpr_impact as H
import matched_gpr_input_review as T
import matched_gpr_evaluation as E
import probe_matched_gpr_evaluation as P

ROOT = Path(__file__).resolve().parent.parent


def pins():
    return tuple(T.InputBinding('implementation', f'pin-{n}', f'inputs/{n}.dat', 'a' * 64)
                 for n in range(10))


def inventory():
    return T.InputReview('synthetic', 'unit', pins())


def graph_for(review, extra=()):
    projection = H.project_inputs(review)
    evidence = I.DependencyNode(projection.evidence_key, 'evidence', (review.profile_id,), 'd' * 64)
    nodes = (*projection.nodes, evidence, *extra)
    edges = tuple((evidence.key, node.key) for node in (*projection.nodes, *extra))
    return I.DependencyGraph((review.profile_id,), nodes, edges)


def authority(review, previous=None, current=None, **changes):
    previous = graph_for(review) if previous is None else previous
    current = previous if current is None else current
    return H.ImpactReview(review.profile_id, review.experiment_id, previous, current, **changes)


def context(value):
    return H.freeze_review(value, profile_id='synthetic', experiment_id='unit')


class ImpactTests(unittest.TestCase):
    def check(self, value, old=None, new=None):
        return H.check_inputs(context(value), pins() if old is None else old,
                              pins() if new is None else new)

    def test_full_metadata_fingerprint_and_unambiguous_namespaces(self):
        review = inventory(); projected = H.project_inputs(review)
        expected = b'["matched-gpr-input-v1","implementation","pin-0","inputs/0.dat","' + b'a' * 64 + b'"]'
        self.assertEqual(projected.nodes[0].fingerprint, hashlib.sha256(expected).hexdigest())
        self.assertEqual(projected.evidence_key, 'experiment:["synthetic","unit"]')
        self.assertEqual(projected.nodes[0].key, 'input:["synthetic","unit","pin-0"]')
        for change in [dict(role='source'), dict(input_id='other'), dict(path='inputs/other.dat'),
                       dict(sha256='b' * 64)]:
            with self.subTest(change=change):
                changed = H.project_inputs(replace(review, inputs=(replace(pins()[0], **change), *pins()[1:])))
                self.assertNotEqual({n.fingerprint for n in projected.nodes}, {n.fingerprint for n in changed.nodes})
        left = H.project_inputs(replace(review, experiment_id='a/b'))
        right = H.project_inputs(replace(review, experiment_id='a', inputs=(replace(pins()[0], input_id='b/pin-0'), *pins()[1:])))
        self.assertNotEqual(left.nodes[0].key, right.nodes[0].key)
        quoted = H.project_inputs(replace(review, inputs=(replace(pins()[0], input_id='a",/☃'), *pins()[1:])))
        self.assertTrue(all(node.key.isascii() for node in quoted.nodes))

    def test_unchanged_projection_is_only_a_conditional_metadata_match(self):
        checked = self.check(authority(inventory()))
        self.assertEqual(checked.disposition, 'matched')
        self.assertIsNotNone(checked.analysis)
        self.assertEqual(checked.analysis.affected_ids, ())
        self.assertEqual((checked.profile_id, checked.experiment_id), ('synthetic', 'unit'))
        self.assertFalse(hasattr(checked, 'qualified'))

    def test_nonfile_context_change_stales_selected_evidence_with_unchanged_inputs(self):
        review = inventory(); node = I.DependencyNode('parent-context', 'configuration', ('synthetic',), 'a' * 64)
        old = graph_for(review, (node,)); new = replace(old, nodes=tuple(replace(n, fingerprint='b' * 64) if n.key == node.key else n for n in old.nodes))
        checked = self.check(authority(review, old, new))
        self.assertEqual(checked.disposition, 'stale')
        self.assertIn(H.project_inputs(review).evidence_key, checked.analysis.stale_evidence_ids)
        self.assertIsNotNone(checked.analysis)
        self.assertEqual(checked.analysis.broadened_profile_ids, ('synthetic',))

    def test_changed_path_uncertainty_and_unknown_fingerprint_are_forwarded(self):
        review = inventory()
        for options in [dict(changed_paths=('unmapped/change.py',)), dict(uncertain=True)]:
            with self.subTest(options=options):
                checked = self.check(authority(review, **options))
                self.assertEqual(checked.disposition, 'stale')
                self.assertIsNotNone(checked.analysis)
        self.assertEqual(checked.analysis.broadened_profile_ids, ('synthetic',))
        unknown = I.DependencyNode('unknown', 'semantic', ('synthetic',), None)
        checked = self.check(authority(review, graph_for(review, (unknown,))))
        self.assertEqual(checked.disposition, 'stale')
        self.assertIn('unknown-fingerprint', checked.analysis.broadening_reasons)

    def test_deleted_current_evidence_stays_stale_and_old_evidence_is_required(self):
        review = inventory(); old = graph_for(review); key = H.project_inputs(review).evidence_key
        removed = replace(old, nodes=tuple(n for n in old.nodes if n.key != key), edges=())
        self.assertEqual(self.check(authority(review, old, removed)).disposition, 'stale')
        refused = self.check(authority(review, removed, old))
        self.assertEqual(refused.disposition, 'refused'); self.assertIsNone(refused.analysis)

    def test_both_versions_bind_complete_input_metadata(self):
        review = inventory(); old = graph_for(review); leaf = old.nodes[0]
        for version in ['previous', 'current']:
            for changes in [dict(path='inputs/other.dat'), dict(fingerprint='e' * 64), dict(kind='case-input')]:
                with self.subTest(version=version, changes=changes):
                    damaged = replace(old, nodes=(replace(leaf, **changes), *old.nodes[1:]))
                    value = replace(authority(review, old), **{version: damaged})
                    checked = self.check(value)
                    self.assertEqual(checked.disposition, 'refused'); self.assertIsNone(checked.analysis)
            damaged_root = replace(old, nodes=(*old.nodes[:-1], replace(old.nodes[-1], kind='implementation')))
            checked = self.check(replace(authority(review, old), **{version: damaged_root}))
            self.assertEqual(checked.disposition, 'refused'); self.assertIsNone(checked.analysis)

    def test_every_input_identity_change_invalidates_evidence(self):
        review = inventory(); old = graph_for(review)
        for changes in [dict(role='source'), dict(path='inputs/other.dat'),
                        dict(sha256='b' * 64), dict(input_id='renamed')]:
            with self.subTest(changes=changes):
                current = replace(review, inputs=(replace(pins()[0], **changes), *pins()[1:]))
                checked = self.check(authority(review, old, graph_for(current)), new=current.inputs)
                self.assertEqual(checked.disposition, 'stale')

    def test_missing_input_and_wrong_shared_scope_refuse(self):
        review = inventory(); old = graph_for(review); leaf = old.nodes[0]
        missing = replace(old, nodes=old.nodes[1:], edges=tuple(e for e in old.edges if leaf.key not in e))
        self.assertEqual(self.check(authority(review, missing, old)).disposition, 'refused')
        nodes = tuple(replace(n, profile_ids=('other',)) if n.key == leaf.key else
                      replace(n, profile_ids=('synthetic', 'other')) for n in old.nodes)
        wrong_scope = replace(old, profile_ids=('synthetic', 'other'), nodes=nodes)
        self.assertEqual(self.check(authority(review, wrong_scope, old)).disposition, 'refused')

    def test_both_evidence_to_input_closures_are_required(self):
        review = inventory(); old = graph_for(review); missing = replace(old, edges=old.edges[1:])
        for value in [authority(review, missing, old), authority(review, old, missing)]:
            checked = self.check(value)
            self.assertEqual(checked.disposition, 'refused'); self.assertIsNone(checked.analysis)

    def test_transitive_and_cyclic_edges_terminate_and_bind(self):
        review = inventory(); graph = graph_for(review); key = H.project_inputs(review).evidence_key
        bridge = I.DependencyNode('bridge', 'configuration', ('synthetic',), 'b' * 64)
        edges = ((key, bridge.key), (bridge.key, key), *((bridge.key, n.key) for n in graph.nodes if n.key != key))
        graph = replace(graph, nodes=(*graph.nodes, bridge), edges=edges)
        self.assertEqual(self.check(authority(review, graph)).disposition, 'matched')

    def test_labels_types_incomplete_objects_and_graph_envelopes_refuse(self):
        review = inventory(); value = authority(review)
        bad = [False, object.__new__(H.ImpactReview), replace(value, profile_id='other'),
               replace(value, experiment_id='other'), replace(value, previous=False),
               replace(value, previous=object.__new__(I.DependencyGraph)),
               replace(value, changed_paths=[]), replace(value, uncertain=1)]
        for field, content in [('nodes', (object(),) * (I.MAX_NODES + 1)),
                               ('edges', (object(),) * (I.MAX_EDGES + 1)),
                               ('profile_ids', ('synthetic',) * (I.MAX_PROFILES + 1))]:
            bad.append(replace(value, previous=replace(value.previous, **{field: content})))
        for item in bad:
            with self.subTest(kind=type(item)), self.assertRaises(H.ImpactReviewError): context(item)
        with self.assertRaises(H.ImpactReviewError): H.project_inputs(replace(review, profile_id='p' * 129))
        with self.assertRaises(H.ImpactReviewError): H.project_inputs(replace(review, experiment_id='x' * 1024))

    def test_count_envelopes_precede_node_field_access(self):
        value = authority(inventory()); accesses = []
        builtin_getattr = getattr
        def tracking(obj, key, default=None):
            if type(obj) is I.DependencyNode: accesses.append(key)
            return builtin_getattr(obj, key, default)
        base = value.previous
        cases = [replace(base, nodes=(base.nodes[0],) * (I.MAX_NODES + 1)),
                 replace(base, edges=(('unused', 'unused'),) * (I.MAX_EDGES + 1)),
                 replace(base, profile_ids=('synthetic',) * (I.MAX_PROFILES + 1))]
        for graph in cases:
            with self.subTest(field_counts=(len(graph.nodes), len(graph.edges), len(graph.profile_ids))):
                accesses.clear()
                with mock.patch.object(H, 'getattr', tracking, create=True):
                    with self.assertRaises(H.ImpactReviewError): context(replace(value, previous=graph))
                self.assertEqual(accesses, [])

    def test_maximum_graph_envelopes_are_inclusive(self):
        review = inventory(); graph = graph_for(review)
        extra = tuple(I.DependencyNode(f'extra-{n}', 'requirement', ('synthetic',), 'f' * 64)
                      for n in range(I.MAX_NODES - len(graph.nodes)))
        nodes = (*graph.nodes, *extra); edges = list(graph.edges); known = set(edges)
        for left in nodes:
            for right in nodes:
                edge = (left.key, right.key)
                if edge not in known and len(edges) < I.MAX_EDGES: edges.append(edge); known.add(edge)
            if len(edges) == I.MAX_EDGES: break
        graph = replace(graph, nodes=nodes, edges=tuple(edges))
        self.assertEqual(self.check(authority(review, graph)).disposition, 'matched')

    def test_frozen_results_and_context_copy_caller_nodes(self):
        value = authority(inventory()); frozen = context(value); checked = H.check_inputs(frozen, pins(), pins())
        with self.assertRaises(FrozenInstanceError): checked.reason = 'changed'
        with self.assertRaises(FrozenInstanceError): frozen.profile_id = 'changed'
        projection = H.project_inputs(inventory())
        with self.assertRaises(FrozenInstanceError): projection.evidence_key = 'changed'
        self.assertIsNot(frozen.previous.nodes[0], value.previous.nodes[0])
        object.__setattr__(value.previous.nodes[0], 'fingerprint', 'e' * 64)
        object.__setattr__(value, 'experiment_id', 'changed')
        self.assertEqual(frozen.previous.nodes[0].fingerprint, H.project_inputs(inventory()).nodes[0].fingerprint)
        self.assertEqual(H.check_inputs(frozen, pins(), pins()).disposition, 'matched')

    def test_pure_helpers_perform_no_file_or_process_operations(self):
        value = authority(inventory())
        with mock.patch('builtins.open', side_effect=AssertionError('file I/O')), \
             mock.patch.object(Path, 'open', side_effect=AssertionError('path I/O')), \
             mock.patch('subprocess.run', side_effect=AssertionError('process')):
            self.assertEqual(self.check(value).disposition, 'matched')


class EvaluationImpactTests(unittest.TestCase):
    def setUp(self):
        base = ROOT / 'target/p4-system-14/a42n/fixtures'; base.mkdir(parents=True, exist_ok=True)
        temporary = tempfile.TemporaryDirectory(dir=base); self.addCleanup(temporary.cleanup)
        self.f = P.Fixture(Path(temporary.name))
        self.review = T.InputReview('synthetic', self.f.experiment['id'], tuple(
            T.InputBinding(row['role'], row['id'], row['path'], row['sha256'])
            for row in [*self.f.inputs.values(), self.f.child]))
        self.impact = authority(self.review)

    def outcome(self, disposition, **changes):
        arguments = self.f.arguments(); arguments.update(reviewed_inputs=self.review, impact_review=self.impact)
        arguments.update(changes)
        try: checked = E.evaluate_retained_unit(self.f.root, **arguments)
        except (AttributeError, KeyError, IndexError, TypeError, ValueError, OSError, AssertionError) as exc:
            self.fail(f'evaluation escaped as {type(exc).__name__}: {exc}')
        self.assertEqual(checked.disposition, disposition, checked.reason)
        return checked

    def test_complete_positive_legacy_and_explicit_none_remain_pending(self):
        checked = self.outcome('pending')
        self.assertIsNotNone(checked.impact)
        self.assertEqual(checked.impact.disposition, 'matched')
        self.assertEqual(checked.input_review.disposition, 'matched')
        self.assertEqual(checked.authentication.disposition, 'matched')
        self.assertTrue(all(item.data is None for item in checked.authentication.files))
        self.assertIsNone(self.outcome('pending', impact_review=None).impact)
        self.assertIsNone(self.outcome('pending', impact_review=None, reviewed_inputs=None).impact)

    def test_changed_parent_context_stales_before_file_set_reads(self):
        old = graph_for(self.review, (I.DependencyNode('parent-context', 'configuration', ('synthetic',), 'a' * 64),))
        current = replace(old, nodes=tuple(replace(n, fingerprint='b' * 64) if n.key == 'parent-context' else n for n in old.nodes))
        self.impact = authority(self.review, old, current)
        with mock.patch.object(E.Q, 'read_declared_files', side_effect=AssertionError('file-set read')):
            checked = self.outcome('stale')
        self.assertIsNotNone(checked.impact)
        self.assertEqual(checked.impact.disposition, 'stale')
        self.assertEqual(checked.input_review.disposition, 'matched')
        self.assertIsNone(checked.authentication)

    def test_invalid_context_and_missing_current_review_refuse_before_artifact_io(self):
        for options in [dict(impact_review=False), dict(reviewed_inputs=None),
                        dict(impact_review=replace(self.impact, experiment_id='other'))]:
            with self.subTest(options=list(options)), mock.patch.object(E.A, 'read_snapshot', side_effect=AssertionError('artifact read')):
                checked = self.outcome('refused', **options)
                self.assertEqual(checked.record.disposition, 'valid'); self.assertIsNone(checked.manifest)

    def test_graph_input_mismatch_refuses_with_independent_review_finding(self):
        old = self.impact.previous
        wrong = replace(old, nodes=(replace(old.nodes[0], path='wrong/path.dat'), *old.nodes[1:]))
        self.impact = replace(self.impact, previous=wrong)
        with mock.patch.object(E.Q, 'read_declared_files', side_effect=AssertionError('file-set read')):
            checked = self.outcome('refused')
        self.assertEqual(checked.input_review.disposition, 'matched')
        self.assertIsNotNone(checked.impact)
        self.assertEqual(checked.impact.disposition, 'refused'); self.assertIsNone(checked.impact.analysis)

    def test_input_review_refusal_retains_separate_stale_analysis(self):
        old = self.impact.previous
        self.review = replace(self.review, inputs=tuple(n for n in self.review.inputs if n.input_id != self.f.child['id']))
        self.impact = authority(self.review, old, graph_for(self.review))
        checked = self.outcome('refused')
        self.assertEqual(checked.input_review.disposition, 'refused')
        self.assertIsNotNone(checked.impact)
        self.assertEqual(checked.impact.disposition, 'stale')
        self.assertIsNone(checked.authentication)

    def test_graph_values_freeze_before_first_artifact_read(self):
        reading = E.A.read_snapshot; changed = False; original = self.impact
        def read(*args, **kwargs):
            nonlocal changed
            result = reading(*args, **kwargs)
            if not changed:
                changed = True
                object.__setattr__(original.current.nodes[0], 'fingerprint', 'e' * 64)
            return result
        with mock.patch.object(E.A, 'read_snapshot', side_effect=read): checked = self.outcome('pending')
        self.assertTrue(changed)
        self.assertIsNotNone(checked.impact)
        self.assertEqual(checked.impact.disposition, 'matched')

    def test_later_actual_file_staleness_is_not_hidden_by_metadata_match(self):
        (self.f.root / self.f.child['path']).write_bytes(b'# stale file\n')
        checked = self.outcome('stale')
        self.assertIsNotNone(checked.impact)
        self.assertEqual(checked.impact.disposition, 'matched')
        self.assertIsNotNone(checked.authentication)

    def test_coherent_failed_process_is_not_hidden_by_metadata_match(self):
        self.f.runs['repeat'].update(process_exit=1, verdict='REFUSED'); self.f.publish_receipts()
        checked = self.outcome('failed')
        self.assertIsNotNone(checked.impact)
        self.assertEqual(checked.impact.disposition, 'matched')

    def test_manifest_failure_keeps_impact_finding_absent(self):
        (self.f.root / self.f.inputs['dependency-manifest']['path']).unlink()
        self.assertIsNone(self.outcome('unavailable').impact)


MUTATIONS = {'role-fingerprint': ('helper',
                      "'matched-gpr-input-v1', item.role, item.input_id",
                      "'matched-gpr-input-v1', 'implementation', item.input_id"),
 'digest-fingerprint': ('helper',
                        "item.path, item.sha256]).encode('ascii')",
                        "item.path, '0' * 64]).encode('ascii')"),
 'profile': ('helper', 'selected_profile == profile_id', 'True'),
 'experiment': ('helper', 'selected_experiment == experiment_id', 'True'),
 'input-path': ('helper', 'actual.path == expected.path', 'True'),
 'input-fingerprint': ('helper', 'actual.fingerprint == expected.fingerprint', 'True'),
 'input-kind': ('helper', 'actual.kind == expected.kind', 'True'),
 'input-profile': ('helper',
                   "and profile_id in actual.profile_ids, 'graph input metadata",
                   "and True, 'graph input metadata"),
 'old-evidence': ('helper', '_require(evidence is not None or not previous,', '_require(True,'),
 'evidence-kind': ('helper', "evidence.kind == 'evidence'", 'True'),
 'reachability': ('helper', 'all(node.key in reachable for node in projection.nodes),', 'True,'),
 'graph-copy': ('helper', 'copied.append(I.DependencyNode(*values))', 'copied.append(node)'),
 'node-envelope': ('helper', 'len(nodes) <= I.MAX_NODES', 'True'),
 'edge-envelope': ('helper', 'len(edges) <= I.MAX_EDGES', 'True'),
 'profile-envelope': ('helper', '1 <= len(profiles) <= I.MAX_PROFILES', 'True'),
 'result-frozen': ('helper',
                   '@dataclass(frozen=True)\nclass InputImpactCheck:',
                   '@dataclass\nclass InputImpactCheck:'),
 'context-frozen': ('helper',
                    '@dataclass(frozen=True)\nclass _Context:',
                    '@dataclass\nclass _Context:'),
 'binding-status': ('evaluator', 'if impact.disposition == "refused":', 'if False:'),
 'stale-status': ('evaluator',
                  'if impact is not None and impact.disposition == "stale":',
                  'if False:'),
 'current-review': ('evaluator',
                    'if impact_review is not None and review_context is None:',
                    'if False:'),
 'finding': ('evaluator',
             'identity, receipts, comparison, source_image, input_review, impact)',
             'identity, receipts, comparison, source_image, input_review, None)'),
 'frozen-context': ('evaluator',
                    'H.check_inputs(impact_context, manifest.plan.inputs, review_context.inputs)',
                    'H.check_inputs(H.freeze_review(impact_review, profile_id=scope.profile_id, '
                    'experiment_id=experiment["id"]), manifest.plan.inputs, '
                    'review_context.inputs)')}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--mutation', choices=MUTATIONS)
    args = parser.parse_args()
    if args.mutation:
        global H, E
        target_name, before, after = MUTATIONS[args.mutation]
        target = H if target_name == 'helper' else E
        source = Path(target.__file__).read_text()
        if source.count(before) != 1: raise SystemExit('mutation seam is not singular')
        module = types.ModuleType('mutated_impact_' + target.__name__); module.__file__ = target.__file__
        sys.modules[module.__name__] = module
        exec(compile(source.replace(before, after), target.__file__, 'exec'), module.__dict__)
        if target_name == 'helper': H = module; E.H = module
        else: E = module
    suite = unittest.TestSuite([unittest.defaultTestLoader.loadTestsFromTestCase(ImpactTests),
                               unittest.defaultTestLoader.loadTestsFromTestCase(EvaluationImpactTests)])
    result = unittest.TextTestRunner(verbosity=1).run(suite)
    print(f'MATCHED-GPR-IMPACT: {result.testsRun} tests / {len(result.failures)} failures / {len(result.errors)} errors; synthetic only')
    return 0 if result.wasSuccessful() else 1


if __name__ == '__main__': raise SystemExit(main())
