#!/usr/bin/env python3
"""Synthetic change-impact controls, never evidence for a real CPU capture."""
from __future__ import annotations

import argparse
from dataclasses import FrozenInstanceError, replace
from itertools import product
from pathlib import Path
import sys
import types
import unittest

import change_impact as I


def node(key, *, kind="case-input", profiles=("p",), pin="a" * 64, path=None):
    return I.DependencyNode(key, kind, profiles, pin, path)


def graph(*nodes, edges=(), profiles=("p",)):
    return I.DependencyGraph(profiles, tuple(nodes), edges)


def chain():
    return graph(node("input", path="cases/input.sexp"), node("req", kind="requirement"),
                 node("obl", kind="obligation"), node("ev", kind="evidence"), node("other"),
                 edges=(("req", "input"), ("obl", "req"), ("ev", "obl")))


class String(str):
    pass


class ImpactTests(unittest.TestCase):
    def check(self, old, new=None, **kwargs):
        return I.analyze_impact(old, old if new is None else new, **kwargs)

    def refuses(self, old, reason, *, new=None, **kwargs):
        with self.assertRaises(I.ImpactError) as caught:
            self.check(old, new, **kwargs)
        self.assertIn(reason, str(caught.exception))

    def test_unchanged_known_graph_has_no_invalidation(self):
        result = self.check(chain())
        self.assertEqual(result, I.ChangeImpact((), (), (), (), (), (), ()))

    def test_content_change_reaches_requirements_obligations_and_evidence(self):
        old = chain()
        new = replace(old, nodes=(replace(old.nodes[0], fingerprint="b" * 64), *old.nodes[1:]))
        result = self.check(old, new)
        self.assertEqual(result.seed_ids, ("input",))
        self.assertEqual(result.affected_ids, ("ev", "input", "obl", "req"))
        self.assertEqual(result.stale_evidence_ids, ("ev",))
        self.assertEqual(result.affected_profile_ids, ("p",))
        self.assertEqual(result.broadened_profile_ids, ())

    def test_new_node_is_seeded(self):
        result = self.check(graph(), graph(node("new", kind="requirement")))
        self.assertEqual(result.seed_ids, ("new",))
        self.assertEqual(result.affected_ids, ("new",))

    def test_deleted_node_and_old_dependents_remain_visible(self):
        old = chain()
        new = graph(*old.nodes[1:], edges=old.edges[1:])
        result = self.check(old, new)
        self.assertEqual(result.seed_ids, ("input", "req"))
        self.assertEqual(result.affected_ids, ("ev", "input", "obl", "req"))
        self.assertEqual(result.stale_evidence_ids, ("ev",))

    def test_deleted_evidence_is_retained_in_report(self):
        old = graph(node("gone", kind="evidence"))
        self.assertEqual(self.check(old, graph()).stale_evidence_ids, ("gone",))

    def test_removed_edge_seeds_its_dependent_with_unchanged_nodes(self):
        old = chain()
        new = replace(old, edges=old.edges[1:])
        result = self.check(old, new)
        self.assertEqual(result.seed_ids, ("req",))
        self.assertEqual(result.affected_ids, ("ev", "obl", "req"))

    def test_added_edge_seeds_its_dependent_with_unchanged_nodes(self):
        new = chain()
        old = replace(new, edges=new.edges[1:])
        self.assertEqual(self.check(old, new).affected_ids, ("ev", "obl", "req"))

    def test_reverse_union_keeps_old_edge_and_new_edge(self):
        nodes = (node("input", path="case.s"), node("old"), node("new"), node("ev", kind="evidence"))
        old = graph(*nodes, edges=(("old", "input"), ("ev", "old")))
        new = graph(*nodes, edges=(("new", "input"), ("ev", "new")))
        result = self.check(old, new, changed_paths=("case.s",))
        self.assertEqual(result.affected_ids, ("ev", "input", "new", "old"))

    def test_path_change_is_metadata_change(self):
        old = graph(node("x", path="old.s"))
        new = graph(replace(old.nodes[0], path="new.s"))
        self.assertEqual(self.check(old, new).seed_ids, ("x",))

    def test_node_scope_change_is_metadata_change(self):
        old = graph(node("x"), profiles=("p", "q"))
        new = graph(replace(old.nodes[0], profile_ids=("q",)), profiles=("p", "q"))
        result = self.check(old, new)
        self.assertEqual(result.seed_ids, ("x",))
        self.assertEqual(result.affected_profile_ids, ("p", "q"))

    def test_every_node_for_a_changed_path_is_seeded(self):
        old = graph(node("a", path="shared.sexp"), node("b", path="shared.sexp"), node("c"))
        result = self.check(old, changed_paths=("shared.sexp",))
        self.assertEqual(result.seed_ids, ("a", "b"))
        self.assertEqual(result.affected_ids, ("a", "b"))

    def test_unmapped_path_broadens_all_scopes_including_empty_profile(self):
        old = graph(node("x"), profiles=("p", "empty"))
        result = self.check(old, changed_paths=("missing.s",))
        self.assertEqual(result.broadened_profile_ids, ("empty", "p"))
        self.assertEqual(result.affected_ids, ("x",))
        self.assertEqual(result.unmapped_paths, ("missing.s",))
        self.assertIn("unmapped-change", result.broadening_reasons)

    def test_explicit_uncertainty_broadens_every_old_and_new_profile(self):
        old = graph(node("old"), profiles=("p", "old-empty"))
        new = graph(node("new", profiles=("q",)), profiles=("q", "new-empty"))
        result = self.check(old, new, uncertain=True)
        self.assertEqual(result.broadened_profile_ids, ("new-empty", "old-empty", "p", "q"))
        self.assertIn("uncertain-influence", result.broadening_reasons)

    def test_scope_change_alone_broadens_without_nodes(self):
        result = self.check(graph(), graph(profiles=("q",)))
        self.assertEqual(result.broadened_profile_ids, ("p", "q"))
        self.assertEqual(result.affected_profile_ids, ("p", "q"))
        self.assertIn("profile-scope-change", result.broadening_reasons)

    def test_unknown_unchanged_fingerprint_broadens_its_scope(self):
        old = graph(node("unknown", pin=None), node("ev", kind="evidence"),
                    node("untouched", profiles=("q",)), profiles=("p", "q"))
        result = self.check(old)
        self.assertEqual(result.seed_ids, ())
        self.assertEqual(result.affected_ids, ("ev", "unknown"))
        self.assertEqual(result.broadened_profile_ids, ("p",))
        self.assertEqual(result.stale_evidence_ids, ("ev",))
        self.assertIn("unknown-fingerprint", result.broadening_reasons)

    def test_every_shared_kind_defaults_to_broad_scope(self):
        shared = {"semantic", "configuration", "implementation", "primitive", "generator",
                  "comparator", "source", "reference-build", "policy", "schema", "build", "artifact", "test"}
        for kind in sorted(shared):
            with self.subTest(kind=kind):
                old = graph(node("shared", kind=kind), node("ev", kind="evidence"))
                new = replace(old, nodes=(replace(old.nodes[0], fingerprint="b" * 64), old.nodes[1]))
                result = self.check(old, new)
                self.assertEqual(result.broadened_profile_ids, ("p",))
                self.assertEqual(result.stale_evidence_ids, ("ev",))
                self.assertIn("shared-kind-influence", result.broadening_reasons)

    def test_old_kind_and_scope_cannot_be_erased_by_new_kind(self):
        old = graph(node("x", kind="source"), node("ev", kind="evidence"))
        new = replace(old, nodes=(replace(old.nodes[0], kind="case-input"), old.nodes[1]))
        self.assertEqual(self.check(old, new).broadened_profile_ids, ("p",))

    def test_transitively_affected_shared_node_broadens(self):
        old = graph(node("x", path="input.s"), node("adapter", kind="comparator"), node("ev", kind="evidence"),
                    edges=(("adapter", "x"),))
        result = self.check(old, changed_paths=("input.s",))
        self.assertEqual(result.stale_evidence_ids, ("ev",))
        self.assertEqual(result.broadened_profile_ids, ("p",))

    def test_broad_profile_exposes_shared_node_and_second_profile(self):
        old = graph(node("x", pin=None), node("shared", kind="primitive", profiles=("p", "q")),
                    node("ev-q", kind="evidence", profiles=("q",)),
                    node("isolated", profiles=("r",)), profiles=("p", "q", "r"))
        result = self.check(old)
        self.assertEqual(result.broadened_profile_ids, ("p", "q"))
        self.assertEqual(result.affected_ids, ("ev-q", "shared", "x"))
        self.assertEqual(result.stale_evidence_ids, ("ev-q",))

    def test_cycles_terminate_and_reverse_orientation_does_not_select_dependencies(self):
        old = graph(node("a", path="a.s"), node("b"), node("dependency"),
                    edges=(("a", "b"), ("b", "a"), ("a", "dependency")))
        self.assertEqual(self.check(old, changed_paths=("a.s",)).affected_ids, ("a", "b"))

    def test_order_is_immaterial_for_nodes_edges_and_profiles(self):
        old = graph(node("x", kind="source", profiles=("p", "q")), node("ev", kind="evidence"),
                    profiles=("p", "q"), edges=(("ev", "x"),))
        new = replace(old, profile_ids=("q", "p"),
                      nodes=tuple(replace(n, profile_ids=tuple(reversed(n.profile_ids))) for n in reversed(old.nodes)),
                      edges=tuple(reversed(old.edges)))
        self.assertEqual(self.check(old, new), I.ChangeImpact((), (), (), (), (), (), ()))

    def test_result_is_frozen_sorted_and_contains_no_qualification_field(self):
        result = self.check(graph(node("z"), node("a", kind="evidence")), uncertain=True)
        self.assertEqual(result.affected_ids, ("a", "z"))
        with self.assertRaises(FrozenInstanceError):
            result.affected_ids = ()
        self.assertFalse(hasattr(result, "qualified"))
        self.assertTrue(all(type(value) is tuple for value in vars(result).values()))

    def test_graph_and_node_are_frozen(self):
        old = graph(node("x"))
        with self.assertRaises(FrozenInstanceError):
            old.nodes = ()
        with self.assertRaises(FrozenInstanceError):
            old.nodes[0].key = "different"

    def test_plain_input_types_are_required(self):
        old = graph(node("x"))
        class Graph(I.DependencyGraph):
            pass
        class Node(I.DependencyNode):
            pass
        for value, reason in (({}, "DependencyGraph"), (Graph(old.profile_ids, old.nodes, ()), "DependencyGraph"),
                              (replace(old, nodes=[old.nodes[0]]), "nodes"), (replace(old, edges=[]), "edges"),
                              (graph(Node("x", "case-input", ("p",), "a" * 64)), "DependencyNode"),
                              (graph(node(String("x"))), "node ID"),
                              (graph(node("x", profiles=["p"])), "profile IDs")):
            with self.subTest(value=value):
                self.refuses(value, reason)
        for value in (1, None, "yes"):
            self.refuses(old, "Boolean", uncertain=value)
        for value in (["a.s"], "a.s", None):
            self.refuses(old, "changed paths", changed_paths=value)

    def test_duplicate_ids_profiles_and_edges_refuse(self):
        self.refuses(graph(node("x"), node("x")), "duplicate node")
        self.refuses(graph(profiles=("p", "p")), "duplicate profile")
        self.refuses(graph(node("x", profiles=("p", "p"))), "duplicate profile")
        self.refuses(graph(node("x"), edges=(("x", "x"), ("x", "x"))), "duplicate edge")
        self.refuses(graph(), "duplicate changed path", changed_paths=("a.s", "a.s"))

    def test_unresolved_or_disjoint_edges_refuse(self):
        self.refuses(graph(node("x"), edges=(("x", "missing"),)), "unresolved")
        self.refuses(graph(node("x"), node("y", profiles=("q",)), profiles=("p", "q"),
                           edges=(("x", "y"),)), "disjoint")

    def test_malformed_edges_refuse(self):
        for edge in (["x", "x"], ("x",), ("x", "x", "x"), (True, "x"), (String("x"), "x")):
            with self.subTest(edge=edge):
                self.refuses(graph(node("x"), edges=(edge,)), "invalid edge")

    def test_node_identity_kind_fingerprint_and_scope_refuse(self):
        for value, reason in ((node(""), "node ID"), (node("x", kind="unknown"), "kind"),
                              (node("x", kind=String("source")), "kind"),
                              (node("x", profiles=("q",)), "outside"),
                              (node("x", pin="A" * 64), "fingerprint"),
                              (node("x", pin="a" * 63), "fingerprint"),
                              (node("x", pin=String("a" * 64)), "fingerprint")):
            with self.subTest(value=value):
                self.refuses(graph(value), reason)

    def test_paths_are_canonical_relative_plain_strings(self):
        for path in ("", "/absolute", "../up", "a/../b", "a//b", "./a", "a\\b", "a:b", "a\x00b", String("a.s")):
            with self.subTest(path=repr(path)):
                self.refuses(graph(node("x", path=path)), "node path")
                self.refuses(graph(), "changed path", changed_paths=(path,))

    def test_envelope_limits_refuse_before_invalid_members(self):
        self.refuses(I.DependencyGraph(("p",), (object(),) * 513, ()), "512")
        self.refuses(I.DependencyGraph(("p",), (object(),), (object(),) * 4097), "4096")
        self.refuses(graph(profiles=tuple(str(i) for i in range(65))), "1..64")
        self.refuses(graph(), "1024", changed_paths=(object(),) * 1025)

    def test_inclusive_envelope_limits_are_accepted(self):
        profiles = tuple(f"p{i}" for i in range(64))
        nodes = tuple(node(f"n{i}", profiles=profiles) for i in range(512))
        edges = tuple((f"n{i}", f"n{j}") for i in range(64) for j in range(64))
        old = graph(*nodes, profiles=profiles, edges=edges)
        self.assertEqual(self.check(old).affected_ids, ())
        paths = tuple(f"cases/{i}.s" for i in range(1024))
        result = self.check(graph(), changed_paths=paths)
        self.assertEqual(len(result.unmapped_paths), 1024)
        self.assertEqual(result.broadened_profile_ids, ("p",))

    def test_inclusive_text_limits_and_one_over(self):
        old = graph(node("x" * 1024, profiles=("p" * 128,), path="x" * 4096), profiles=("p" * 128,))
        self.assertEqual(self.check(old, changed_paths=("x" * 4096,)).seed_ids, ("x" * 1024,))
        self.refuses(graph(node("x" * 1025)), "node ID")
        self.refuses(graph(profiles=("p" * 129,)), "profile ID")
        self.refuses(graph(node("x", path="x" * 4097)), "node path")
        self.refuses(graph(), "changed path", changed_paths=("x" * 4097,))

    def test_both_old_and_new_graphs_are_validated(self):
        valid = graph(node("x"))
        bad = graph(node("x"), node("x"))
        self.refuses(bad, "duplicate node", new=valid)
        self.refuses(valid, "duplicate node", new=bad)

    def test_bounded_graph_pairs_match_independent_reachability(self):
        nodes = (node("a", path="seed.s"), node("b"), node("c", kind="evidence"))
        edges = tuple((a, b) for a in ("a", "b", "c") for b in ("a", "b", "c") if a != b)
        graphs = tuple(tuple(edge for bit, edge in enumerate(edges) if mask & (1 << bit))
                       for mask in range(64))
        for old_edges in graphs:
            for new_edges in graphs:
                seeds = {"a"} | {a for a, b in set(old_edges) ^ set(new_edges)}
                expected = set(seeds)
                while True:
                    reached = expected | {a for a, b in set(old_edges) | set(new_edges) if b in expected}
                    if reached == expected:
                        break
                    expected = reached
                actual = self.check(graph(*nodes, edges=old_edges), graph(*nodes, edges=new_edges),
                                    changed_paths=("seed.s",))
                self.assertEqual(actual.seed_ids, tuple(sorted(seeds)))
                self.assertEqual(actual.affected_ids, tuple(sorted(expected)))
                self.assertEqual(actual.stale_evidence_ids, ("c",) if "c" in expected else ())


MUTATIONS = {
    "content-seeds": ('_identity(old_nodes[key]) != _identity(new_nodes[key])', 'False'),
    "edge-seeds": ('seeds.update(dependent for dependent, _ in old_edges ^ new_edges)', 'seeds.update(())'),
    "path-seeds": ('seeds.update(by_path.get(path, ()))', 'seeds.update(())'),
    "unmapped-insertion": ('seeds.update(by_path.get(path, ()))', 'seeds.update(by_path[path])'),
    "unmapped-broad": ('if unmapped:', 'if False:'),
    "uncertain-broad": ('if uncertain:', 'if False:'),
    "scope-broad": ('if old_profiles != new_profiles:', 'if False:'),
    "unknown-broad": ('if node.fingerprint is None:', 'if False:'),
    "shared-broad": ('if node.kind not in NARROW_KINDS:', 'if False:'),
    "broad-expansion": ('if any(fresh.intersection(node.profile_ids) for node in items))', 'if False)'),
    "reverse-closure": ('pending.extend(reverse[key] - affected)', 'pending.extend(())'),
    "node-bound": ('len(graph.nodes) <= MAX_NODES', 'True'),
    "edge-bound": ('len(graph.edges) <= MAX_EDGES', 'True'),
    "plain-bool": ('type(uncertain) is bool', 'True'),
    "node-unique": ('node.key not in nodes', 'True'),
    "edge-unique": ('edge not in edges', 'True'),
    "edge-scope": ('bool(set(nodes[dependent].profile_ids) & set(nodes[dependency].profile_ids))', 'True'),
    "result-frozen": ('@dataclass(frozen=True)\nclass ChangeImpact:', '@dataclass\nclass ChangeImpact:'),
}


def check_edge_redundancy():
    """Bounded diagnostic of changed-edge seeding, separate from CPU evidence."""
    vertices = set(range(3))
    edges = tuple((a, b) for a in vertices for b in vertices if a != b)
    graphs = tuple({edge for bit, edge in enumerate(edges) if mask & (1 << bit)}
                   for mask in range(64))

    def closure(selected, seeds):
        reached = set(seeds)
        while True:
            updated = reached | {a for a, b in selected if b in reached}
            if updated == reached:
                return reached
            reached = updated

    count = 0
    for old, new, mask in product(graphs, graphs, range(8)):
        seeds = {v for v in vertices if mask & (1 << v)} | {a for a, b in old ^ new}
        expected = closure(old | new, seeds)
        if any(closure(selected, seeds) != expected for selected in (old, new)):
            raise SystemExit("changed-edge seed redundancy counterexample")
        count += 1
    print(f"CHANGE-IMPACT-REDUNDANCY: {count} bounded old/new/seed combinations; "
          "one-sided closures equal union with changed-edge dependents seeded; no universal claim")
    return 0


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--mutation", choices=MUTATIONS)
    mode.add_argument("--redundancy", action="store_true")
    args = parser.parse_args()
    if args.redundancy:
        return check_edge_redundancy()
    if args.mutation:
        before, after = MUTATIONS[args.mutation]
        source = Path(I.__file__).read_text()
        if source.count(before) != 1:
            raise SystemExit("mutation seam is not singular")
        # Reuse public value types when omitting only algorithm/validation seams.
        # The frozen-result omission intentionally substitutes its value type.
        global_module = types.ModuleType("mutated_change_impact")
        global_module.__file__ = I.__file__
        sys.modules[global_module.__name__] = global_module
        exec(compile(source.replace(before, after), I.__file__, "exec"), global_module.__dict__)
        for name in ("DependencyNode", "DependencyGraph", "ImpactError"):
            setattr(global_module, name, getattr(I, name))
        if args.mutation != "result-frozen":
            global_module.ChangeImpact = I.ChangeImpact
        globals()["I"] = global_module
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(ImpactTests)
    result = unittest.TextTestRunner(verbosity=1).run(suite)
    print(f"CHANGE-IMPACT: {result.testsRun} tests / {len(result.failures)} failures / "
          f"{len(result.errors)} errors; synthetic only")
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    raise SystemExit(main())
