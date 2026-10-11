#!/usr/bin/env python3
"""Conservative influence over reviewed old/new in-memory dependency projections.

Edges point from a dependent to its dependency. The caller owns projection
completeness, fingerprints and change inventory; this pure helper cannot discover
undeclared influences, authenticate files or establish current/qualified evidence.
See docs/EVIDENCE_AND_GATES.md sections 3–4 and the GC book's impact chapter.
"""
from __future__ import annotations

from collections import defaultdict, deque
from dataclasses import dataclass
import re

from experiment_verification import is_canonical_path

MAX_PROFILES = 64
MAX_NODES = 512
MAX_EDGES = 4096
MAX_CHANGED_PATHS = 1024
KINDS = frozenset({"requirement", "obligation", "evidence", "case-input",
                   "semantic", "configuration", "implementation", "primitive",
                   "generator", "comparator", "source", "reference-build",
                   "policy", "schema", "build", "artifact", "test"})
NARROW_KINDS = frozenset({"requirement", "obligation", "evidence", "case-input"})


@dataclass(frozen=True)
class DependencyNode:
    key: str
    kind: str
    profile_ids: tuple[str, ...]
    fingerprint: str | None
    path: str | None = None


@dataclass(frozen=True)
class DependencyGraph:
    profile_ids: tuple[str, ...]
    nodes: tuple[DependencyNode, ...]
    edges: tuple[tuple[str, str], ...]  # dependent -> dependency


@dataclass(frozen=True)
class ChangeImpact:
    seed_ids: tuple[str, ...]
    affected_ids: tuple[str, ...]
    affected_profile_ids: tuple[str, ...]
    broadened_profile_ids: tuple[str, ...]
    stale_evidence_ids: tuple[str, ...]
    unmapped_paths: tuple[str, ...]
    broadening_reasons: tuple[str, ...]


class ImpactError(ValueError):
    """An ambiguous, invalid or oversized dependency projection was supplied."""


def _require(condition: bool, reason: str):
    if not condition:
        raise ImpactError(reason)


def _text(value, limit: int) -> bool:
    return type(value) is str and 1 <= len(value) <= limit


def _path(value) -> bool:
    return _text(value, 4096) and is_canonical_path(value)


def _profiles(value) -> frozenset[str]:
    _require(type(value) is tuple and 1 <= len(value) <= MAX_PROFILES,
             "profile IDs must be a plain tuple of 1..64 entries")
    _require(all(_text(item, 128) for item in value), "invalid profile ID")
    result = frozenset(value)
    _require(len(result) == len(value), "duplicate profile ID")
    return result


def _graph(graph: DependencyGraph):
    _require(type(graph) is DependencyGraph, "expected a plain DependencyGraph")
    profiles = _profiles(graph.profile_ids)
    # Refuse the envelope before constructing an index or traversing its members.
    _require(type(graph.nodes) is tuple and len(graph.nodes) <= MAX_NODES,
             "nodes must be a plain tuple of at most 512 entries")
    _require(type(graph.edges) is tuple and len(graph.edges) <= MAX_EDGES,
             "edges must be a plain tuple of at most 4096 entries")
    nodes = {}
    for node in graph.nodes:
        _require(type(node) is DependencyNode, "expected a plain DependencyNode")
        _require(_text(node.key, 1024), "invalid node ID")
        _require(type(node.kind) is str and node.kind in KINDS, "unknown node kind")
        scope = _profiles(node.profile_ids)
        _require(scope <= profiles, "node profile outside graph scope")
        _require(node.fingerprint is None or
                 (type(node.fingerprint) is str and
                  re.fullmatch(r"[0-9a-f]{64}", node.fingerprint) is not None),
                 "fingerprint must be lowercase SHA256 or None")
        _require(node.path is None or _path(node.path), "invalid node path")
        _require(node.key not in nodes, "duplicate node ID")
        nodes[node.key] = node
    edges = set()
    for edge in graph.edges:
        _require(type(edge) is tuple and len(edge) == 2 and
                 all(_text(item, 1024) for item in edge), "invalid edge")
        dependent, dependency = edge
        _require(dependent in nodes and dependency in nodes, "unresolved edge")
        _require(bool(set(nodes[dependent].profile_ids) & set(nodes[dependency].profile_ids)),
                 "edge endpoints have disjoint profile scopes")
        _require(edge not in edges, "duplicate edge")
        edges.add(edge)
    return profiles, nodes, edges


def _identity(node: DependencyNode):
    return node.kind, frozenset(node.profile_ids), node.fingerprint, node.path


def analyze_impact(old: DependencyGraph, new: DependencyGraph, *,
                   changed_paths: tuple[str, ...] = (), uncertain: bool = False) -> ChangeImpact:
    """Return deterministic invalidation recommendations over both projections.

    Unknown fingerprints, shared-kind influence, unmapped changes or uncertain
    influence broaden validation. Removed nodes/edges remain visible. Invalid
    input raises ImpactError; no return value grants currentness or qualification.
    """
    _require(type(uncertain) is bool, "uncertain must be a plain Boolean")
    _require(type(changed_paths) is tuple and len(changed_paths) <= MAX_CHANGED_PATHS,
             "changed paths must be a plain tuple of at most 1024 entries")
    _require(all(_path(path) for path in changed_paths), "invalid changed path")
    paths = set(changed_paths)
    _require(len(paths) == len(changed_paths), "duplicate changed path")
    old_profiles, old_nodes, old_edges = _graph(old)
    new_profiles, new_nodes, new_edges = _graph(new)
    profiles = old_profiles | new_profiles
    keys = old_nodes.keys() | new_nodes.keys()
    versions = {key: tuple(nodes[key] for nodes in (old_nodes, new_nodes) if key in nodes)
                for key in keys}
    seeds = {key for key in keys if key not in old_nodes or key not in new_nodes or
             _identity(old_nodes[key]) != _identity(new_nodes[key])}
    seeds.update(dependent for dependent, _ in old_edges ^ new_edges)
    by_path = defaultdict(set)
    reverse = defaultdict(set)
    for key, items in versions.items():
        for node in items:
            if node.path is not None:
                by_path[node.path].add(key)
    for dependent, dependency in old_edges | new_edges:
        reverse[dependency].add(dependent)
    for path in paths:
        seeds.update(by_path.get(path, ()))
    unmapped = paths - by_path.keys()
    broad = set()
    reasons = set()
    if uncertain:
        broad.update(profiles)
        reasons.add("uncertain-influence")
    if unmapped:
        broad.update(profiles)
        reasons.add("unmapped-change")
    if old_profiles != new_profiles:
        broad.update(profiles)
        reasons.add("profile-scope-change")
    for items in versions.values():
        for node in items:
            if node.fingerprint is None:
                broad.update(node.profile_ids)
                reasons.add("unknown-fingerprint")

    affected = set()
    expanded_profiles = set()
    pending = deque(sorted(seeds))
    # Broad expansion and reverse reachability share one fixed point. An expanded
    # profile may expose a shared node that broadens a second profile in turn.
    while pending or broad - expanded_profiles:
        fresh = broad - expanded_profiles
        expanded_profiles.update(fresh)
        if fresh:
            pending.extend(key for key, items in versions.items()
                           if any(fresh.intersection(node.profile_ids) for node in items))
        if not pending:
            continue
        key = pending.popleft()
        if key in affected:
            continue
        affected.add(key)
        pending.extend(reverse[key] - affected)
        for node in versions[key]:
            if node.kind not in NARROW_KINDS:
                broad.update(node.profile_ids)
                reasons.add("shared-kind-influence")
    affected_profiles = {profile for key in affected for node in versions[key]
                         for profile in node.profile_ids} | broad
    evidence = {key for key in affected if any(node.kind == "evidence" for node in versions[key])}
    return ChangeImpact(tuple(sorted(seeds)), tuple(sorted(affected)),
                        tuple(sorted(affected_profiles)), tuple(sorted(broad)),
                        tuple(sorted(evidence)), tuple(sorted(unmapped)), tuple(sorted(reasons)))
