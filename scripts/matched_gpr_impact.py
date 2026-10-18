"""Bind retained/current input metadata to caller-reviewed old/new influence.

The graph owner remains change_impact. This layer copies caller context before
artifact I/O and checks its selected input projection; it discovers no dependencies,
authenticates no files and grants no qualification or complete-currentness claim.
"""
from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json

import change_impact as I
import matched_gpr_input_review as T


@dataclass(frozen=True)
class ImpactReview:
    profile_id: str
    experiment_id: str
    previous: I.DependencyGraph
    current: I.DependencyGraph
    changed_paths: tuple[str, ...] = ()
    uncertain: bool = False


@dataclass(frozen=True)
class InputProjection:
    evidence_key: str
    nodes: tuple[I.DependencyNode, ...]


@dataclass(frozen=True)
class InputImpactCheck:
    disposition: str  # matched / stale / refused; supplied metadata only
    reason: str
    profile_id: str
    experiment_id: str
    analysis: I.ChangeImpact | None = None


@dataclass(frozen=True)
class _Context:
    profile_id: str
    experiment_id: str
    previous: I.DependencyGraph
    current: I.DependencyGraph
    analysis: I.ChangeImpact


class ImpactReviewError(ValueError):
    """The selected review context or its input projection cannot be bound."""


def _require(condition: bool, reason: str):
    if not condition:
        raise ImpactReviewError(reason)


def _json(value) -> str:
    return json.dumps(value, ensure_ascii=True, separators=(',', ':'))


def _key(kind: str, *parts: str) -> str:
    key = kind + ':' + _json(parts)
    # The published graph contract bounds a node ID to 1,024 characters.
    _require(len(key) <= 1024, 'selected identity exceeds graph key bound')
    return key


def project_inputs(review: T.InputReview) -> InputProjection:
    """Return bounded namespaced leaves, including the full metadata fingerprint.

    These are input leaves, not an evidence node or a complete dependency graph.
    The caller supplies actual evidence/other metadata and reviewed influence edges.
    """
    _require(type(review) is T.InputReview, 'expected a plain InputReview')
    try:
        frozen = T.freeze_review(review, profile_id=getattr(review, 'profile_id', None),
                                 experiment_id=getattr(review, 'experiment_id', None))
        nodes = tuple(I.DependencyNode(
            _key('input', frozen.profile_id, frozen.experiment_id, item.input_id),
            'implementation', (frozen.profile_id,),
            hashlib.sha256(_json(['matched-gpr-input-v1', item.role, item.input_id,
                                 item.path, item.sha256]).encode('ascii')).hexdigest(),
            item.path) for item in frozen.inputs)
        shape = I.DependencyGraph((frozen.profile_id,), nodes, ())
        I.analyze_impact(shape, shape)  # Public owner validates inherited graph limits.
        return InputProjection(_key('experiment', frozen.profile_id, frozen.experiment_id), nodes)
    except (T.ReviewError, I.ImpactError) as exc:
        raise ImpactReviewError(str(exc)) from exc


def _copy_graph(graph: I.DependencyGraph) -> I.DependencyGraph:
    _require(type(graph) is I.DependencyGraph, 'expected a plain DependencyGraph')
    profiles, nodes, edges = (getattr(graph, key, None)
                               for key in ('profile_ids', 'nodes', 'edges'))
    # Bound containers before copying members; the public analyzer owns full validity.
    _require(type(profiles) is tuple and 1 <= len(profiles) <= I.MAX_PROFILES,
             'invalid graph profile envelope')
    _require(type(nodes) is tuple and len(nodes) <= I.MAX_NODES, 'invalid graph node envelope')
    _require(type(edges) is tuple and len(edges) <= I.MAX_EDGES, 'invalid graph edge envelope')
    copied = []
    for node in nodes:
        _require(type(node) is I.DependencyNode, 'expected a plain DependencyNode')
        values = tuple(getattr(node, key, None)
                       for key in ('key', 'kind', 'profile_ids', 'fingerprint', 'path'))
        copied.append(I.DependencyNode(*values))
    return I.DependencyGraph(profiles, tuple(copied), edges)


def freeze_review(review: ImpactReview, *, profile_id: str, experiment_id: str) -> _Context:
    """Copy bounded graph values and analyze before the evaluator opens artifacts."""
    _require(type(review) is ImpactReview, 'expected a plain ImpactReview')
    selected_profile, selected_experiment, previous, current, paths, uncertain = (
        getattr(review, key, None) for key in
        ('profile_id', 'experiment_id', 'previous', 'current', 'changed_paths', 'uncertain'))
    _require(type(profile_id) is str and 1 <= len(profile_id) <= 128
             and type(selected_profile) is str and selected_profile == profile_id,
             'impact profile differs from selected scope or graph bound')
    _require(type(experiment_id) is str and 1 <= len(experiment_id) <= T.TEXT_CHARS
             and type(selected_experiment) is str and selected_experiment == experiment_id,
             'impact experiment differs from selected parent')
    _key('experiment', profile_id, experiment_id)
    previous, current = _copy_graph(previous), _copy_graph(current)
    try:
        analysis = I.analyze_impact(previous, current, changed_paths=paths, uncertain=uncertain)
    except I.ImpactError as exc:
        raise ImpactReviewError(str(exc)) from exc
    _require(profile_id in previous.profile_ids and profile_id in current.profile_ids,
             'selected profile absent from reviewed graph scope')
    return _Context(profile_id, experiment_id, previous, current, analysis)


def _bind_projection(graph: I.DependencyGraph, projection: InputProjection, *,
                     profile_id: str, previous: bool):
    nodes = {node.key: node for node in graph.nodes}
    evidence = nodes.get(projection.evidence_key)
    _require(evidence is not None or not previous, 'old graph lacks selected evidence')
    if evidence is not None:
        _require(evidence.kind == 'evidence' and profile_id in evidence.profile_ids,
                 'selected evidence kind or profile differs')
    for expected in projection.nodes:
        actual = nodes.get(expected.key)
        _require(actual is not None and actual.kind == expected.kind
                 and actual.path == expected.path and actual.fingerprint == expected.fingerprint
                 and profile_id in actual.profile_ids, 'graph input metadata differs from selected inventory')
    if evidence is None:
        return  # The analyzer retains the old evidence key as stale after removal.
    outgoing = {}
    for dependent, dependency in graph.edges:
        outgoing.setdefault(dependent, set()).add(dependency)
    reachable, pending = set(), [projection.evidence_key]
    while pending:
        key = pending.pop()
        if key in reachable:
            continue
        reachable.add(key)
        pending.extend(outgoing.get(key, set()) - reachable)
    _require(all(node.key in reachable for node in projection.nodes),
             'selected evidence does not reach every projected input')


def check_inputs(context: _Context, previous_inputs: tuple[T.InputBinding, ...],
                 current_inputs: tuple[T.InputBinding, ...]) -> InputImpactCheck:
    """Bind both projections; recommendations remain conditional on caller review.

    Use the context returned by freeze_review, before artifact I/O. Invalid input
    metadata/relationships refuses with no analysis, rather than a false clean set.
    """
    _require(type(context) is _Context, 'expected frozen impact context')
    profile, experiment = context.profile_id, context.experiment_id
    try:
        previous = project_inputs(T.InputReview(profile, experiment, previous_inputs))
        current = project_inputs(T.InputReview(profile, experiment, current_inputs))
        _bind_projection(context.previous, previous, profile_id=profile, previous=True)
        _bind_projection(context.current, current, profile_id=profile, previous=False)
    except ImpactReviewError as exc:
        return InputImpactCheck('refused', str(exc), profile, experiment)
    stale = previous.evidence_key in context.analysis.stale_evidence_ids
    return InputImpactCheck('stale' if stale else 'matched',
                            'selected evidence affected by reviewed old/new graph' if stale else
                            'input projections bind; supplied graph does not select evidence; adequacy pending',
                            profile, experiment, context.analysis)
