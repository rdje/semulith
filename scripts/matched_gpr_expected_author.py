"""Pure binding of expected-producer declarations to separately reviewed metadata.

The caller supplies the public manifest/relation and snapshot-author owners' facts.
No file is authenticated or opened here. A match neither attests loaded code nor
establishes review completeness, property meaning, independence or qualification.
"""
from __future__ import annotations

from dataclasses import dataclass

import derive_rv64gc_expectations as Author
import matched_gpr_execution as E
import matched_gpr_input_review as T
import matched_gpr_manifest as M
import matched_gpr_relations as R


SNAPSHOT_ROUTE = "snapshot-parcels-v1"


@dataclass(frozen=True)
class ExpectedAuthorReview:
    inventory: T.InputReview
    author_input_id: str
    route: str


@dataclass(frozen=True)
class ExpectedAuthorFacts:
    author: E.InputBinding
    source: E.InputBinding
    manifest: E.InputBinding
    version: str
    route: str
    instructions: int


@dataclass(frozen=True)
class ExpectedAuthorCheck:
    disposition: str  # matched / refused; metadata only, never authentication
    reason: str
    facts: ExpectedAuthorFacts | None = None


class AuthorReviewError(ValueError):
    """The caller authority or supplied metadata cannot establish this binding."""


def _require(condition: bool, reason: str):
    if not condition:
        raise AuthorReviewError(reason)


def freeze_review(review: ExpectedAuthorReview, *, profile_id: str,
                  experiment_id: str) -> ExpectedAuthorReview:
    """Validate and copy caller authority before any future artifact reads."""
    _require(type(review) is ExpectedAuthorReview, "expected a plain ExpectedAuthorReview")
    try:
        inventory = T.freeze_review(getattr(review, "inventory", None),
                                    profile_id=profile_id, experiment_id=experiment_id)
    except T.ReviewError as exc:
        raise AuthorReviewError(str(exc)) from None
    selected = getattr(review, "author_input_id", None)
    route = getattr(review, "route", None)
    _require(type(selected) is str and 1 <= len(selected) <= T.TEXT_CHARS,
             "invalid selected author ID")
    authors = tuple(item for item in inventory.inputs if item.role == "expected-author")
    _require(len(authors) == 1 and authors[0].input_id == selected,
             "selected author must name the sole reviewed expected-author")
    _require(type(route) is str and route == SNAPSHOT_ROUTE, "unsupported expected-author route")
    return ExpectedAuthorReview(inventory, selected, route)


def bind_expected_author(review: ExpectedAuthorReview, *, profile_id: str,
                         experiment_id: str, manifest: M.ManifestPlan,
                         derivation: Author.SnapshotDerivation) -> ExpectedAuthorCheck:
    """Bind validated public-owner facts without I/O or execution attestation.

    Re-freeze the authority for direct calls. The existing input-review owner
    bounds and copies both inventories. Public plan owners retain responsibility
    for their complete raw schema, graph and snapshot semantics.
    """
    try:
        frozen = freeze_review(review, profile_id=profile_id, experiment_id=experiment_id)
        _require(type(manifest) is M.ManifestPlan, "expected a plain ManifestPlan")
        relations = manifest.relations
        _require(type(relations) is R.RelationPlan, "expected a plain RelationPlan")
        execution = relations.execution
        _require(type(execution) is E.ExecutionPlan, "expected a plain ExecutionPlan")
        coverage = T.compare_inputs(frozen.inventory, manifest.inputs)
        _require(coverage.disposition == "matched", "manifest inventory differs from author review")
        author = next(item for item in frozen.inventory.inputs
                      if item.input_id == frozen.author_input_id)
        _require(type(manifest.child_input_ids) is tuple
                 and 1 <= len(manifest.child_input_ids) <= T.MANIFEST_INPUTS
                 and author.input_id in manifest.child_input_ids,
                 "reviewed author is not a flat manifest child")
        _require(type(execution.common_inputs) is tuple and len(execution.common_inputs) == len(E.COMMON_ROLES),
                 "invalid common principal set")
        principals = {item.role: item for item in execution.common_inputs}
        source = principals["guest-source"]
        dependency = principals["dependency-manifest"]
        _require(source in frozen.inventory.inputs and dependency in frozen.inventory.inputs
                 and author not in execution.common_inputs
                 and manifest.manifest_input_id == dependency.input_id,
                 "source/manifest/author principal identities differ")
        # Return only bindings copied by the review owner, including principals.
        reviewed = {item.input_id: item for item in frozen.inventory.inputs}
        source, dependency = reviewed[source.input_id], reviewed[dependency.input_id]
        _require(relations.expected_version == "sha256:" + author.sha256,
                 "expected producer version differs from reviewed author digest")
        consumed = relations.derivation_common_input_ids
        _require(type(consumed) is tuple and len(consumed) <= len(E.COMMON_ROLES)
                 and source.input_id in consumed and dependency.input_id in consumed,
                 "expected producers must consume source and dependency manifest")
        _require(type(derivation) is Author.SnapshotDerivation,
                 "expected a plain SnapshotDerivation")
        _require(derivation.author_path == author.path and derivation.route == frozen.route,
                 "snapshot author path/route differs from caller review")
        _require(derivation.source_sha256 == source.sha256,
                 "snapshot source differs from selected guest-source pin")
        _require(type(execution.instructions) is int and 1 <= execution.instructions <= 4096
                 and type(derivation.instructions) is int
                 and derivation.instructions == execution.instructions,
                 "snapshot budget differs from frozen execution")
        facts = ExpectedAuthorFacts(author, source, dependency, relations.expected_version,
                                    frozen.route, execution.instructions)
    except (T.ReviewError, AuthorReviewError, AttributeError, KeyError, TypeError,
            ValueError, StopIteration) as exc:
        return ExpectedAuthorCheck("refused", "expected author: " + str(exc))
    return ExpectedAuthorCheck("matched", "expected author metadata binds; authentication/attestation pending", facts)
