"""Pure binding against a caller-selected, separately reviewed input inventory.

This checks metadata coverage, not the quality/completeness of the caller's review.
It opens no artifact files, discovers no dependencies and grants no qualification. The
current review is trusted caller authority, like the evaluator's scoped IDs;
copying a record's own inputs into it supplies no independent coverage review.
"""
from __future__ import annotations

from dataclasses import dataclass
import re

from experiment_verification import is_canonical_path
from matched_gpr_artifacts import MANIFEST_INPUTS
from matched_gpr_execution import COMMON_ROLES, InputBinding

MIN_INPUTS = len(COMMON_ROLES) + 2  # common principals plus both expectations
MAX_INPUTS = MIN_INPUTS + MANIFEST_INPUTS
TEXT_CHARS = 65536


@dataclass(frozen=True)
class InputReview:
    profile_id: str
    experiment_id: str
    inputs: tuple[InputBinding, ...]


@dataclass(frozen=True)
class InputReviewCheck:
    disposition: str  # matched / refused: metadata equality only
    reason: str
    profile_id: str
    experiment_id: str
    reviewed_count: int
    declared_count: int
    missing_ids: tuple[str, ...] = ()
    unreviewed_ids: tuple[str, ...] = ()
    changed_ids: tuple[str, ...] = ()


class ReviewError(ValueError):
    """Malformed authority or supplied inventory, not a failed dependency review."""


def _require(condition: bool, reason: str):
    if not condition:
        raise ReviewError(reason)


def _text(value) -> bool:
    return type(value) is str and 1 <= len(value) <= TEXT_CHARS


def _inputs(value) -> tuple[InputBinding, ...]:
    # Bound the plain container before indexing or copying any member.
    _require(type(value) is tuple and MIN_INPUTS <= len(value) <= MAX_INPUTS,
             f"inputs must be a plain tuple of {MIN_INPUTS}..{MAX_INPUTS} bindings")
    result = []
    ids, paths = set(), set()
    for item in value:
        _require(type(item) is InputBinding, "expected a plain InputBinding")
        role, rid, path, digest = (getattr(item, key, None)
                                  for key in ("role", "input_id", "path", "sha256"))
        _require(_text(role) and _text(rid), "invalid input role/ID")
        _require(type(path) is str and 1 <= len(path) <= 4096
                 and is_canonical_path(path), "noncanonical input path")
        _require(type(digest) is str and re.fullmatch(r"[0-9a-f]{64}", digest) is not None,
                 "input digest must be lowercase SHA256")
        _require(rid not in ids, "duplicate input ID")
        _require(path not in paths, "duplicate input path")
        ids.add(rid)
        paths.add(path)
        # Do not retain caller-owned dataclass objects, even though normally frozen.
        result.append(InputBinding(role, rid, path, digest))
    return tuple(sorted(result, key=lambda item: item.input_id))


def freeze_review(review: InputReview, *, profile_id: str, experiment_id: str) -> InputReview:
    """Validate and copy the selected authority before any artifact I/O.

    IDs/roles follow the existing bounded text vocabulary; manifest child IDs can
    contain spaces. This is not another S-expression loader or review producer.
    """
    _require(type(review) is InputReview, "expected a plain InputReview")
    selected_profile = getattr(review, "profile_id", None)
    selected_experiment = getattr(review, "experiment_id", None)
    selected_inputs = getattr(review, "inputs", None)
    _require(_text(profile_id) and _text(experiment_id), "invalid selected profile/experiment")
    _require(_text(selected_profile) and selected_profile == profile_id,
             "review profile differs from selected scope")
    _require(_text(selected_experiment) and selected_experiment == experiment_id,
             "review experiment differs from selected parent")
    return InputReview(selected_profile, selected_experiment, _inputs(selected_inputs))


def compare_inputs(review: InputReview, declared: tuple[InputBinding, ...]) -> InputReviewCheck:
    """Compare exact ID/role/path/digest coverage; this does not authenticate files.

    Order is irrelevant. Missing, unreviewed and changed identities are separate,
    deterministic tuples. A matched result does not attest execution or adequacy.
    """
    _require(type(review) is InputReview, "expected a plain InputReview")
    frozen = freeze_review(review, profile_id=getattr(review, "profile_id", None),
                           experiment_id=getattr(review, "experiment_id", None))
    supplied = _inputs(declared)
    expected = {item.input_id: item for item in frozen.inputs}
    actual = {item.input_id: item for item in supplied}
    missing = tuple(sorted(expected.keys() - actual.keys()))
    unreviewed = tuple(sorted(actual.keys() - expected.keys()))
    changed = tuple(sorted(key for key in expected.keys() & actual.keys() if expected[key] != actual[key]))
    agrees = not (missing or unreviewed or changed)
    return InputReviewCheck(
        disposition="matched" if agrees else "refused",
        reason=("declared inventory matches caller review; adequacy pending" if agrees else
                "declared inventory differs from caller review"),
        profile_id=frozen.profile_id,
        experiment_id=frozen.experiment_id,
        reviewed_count=len(expected),
        declared_count=len(actual),
        missing_ids=missing,
        unreviewed_ids=unreviewed,
        changed_ids=changed,
    )
