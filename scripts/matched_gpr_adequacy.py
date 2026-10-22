"""Bind a finite measured DIV record to independently selected method review.

This module opens no artifact, executes no process and grants no policy credit.
The public schema tools retain their own I/O. Caller authority must come from
the reviewed producer/authority owners, never the measured record's own inputs.
"""

from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass
import hashlib

import dossier_sexp as D
import experiment_verification as V
import matched_gpr_artifacts as F
import matched_gpr_comparison as C
import matched_gpr_evaluation as E
import matched_gpr_execution as X
import matched_gpr_expected_author as U
import matched_gpr_files as Q
import matched_gpr_identity as I
import matched_gpr_impact as H
import matched_gpr_input_review as T
import matched_gpr_manifest as M
import matched_gpr_property as P
import matched_gpr_receipt as Receipt
import matched_gpr_relations as R
import matched_gpr_source_image as Image
import sexp as S


@dataclass(frozen=True)
class MethodReview:
    scope: V.Scope
    reference_identity: I.ReferenceIdentity
    planned_experiment: bytes
    manifest: M.ManifestPlan
    inventory: T.InputReview
    impact: H.InputImpactCheck
    evidence_key: str
    planned_sha256: str


@dataclass(frozen=True)
class ObservationIdentity:
    record_id: str
    role: str
    path: str
    sha256: str
    byte_size: int


@dataclass(frozen=True)
class CaptureBinding:
    disposition: str  # matched / stale / unavailable / refused; no artifact authentication
    reason: str
    record_sha256: str | None = None
    planned_sha256: str | None = None
    evidence_key: str | None = None
    observations: tuple[ObservationIdentity, ...] = ()


@dataclass(frozen=True)
class MethodFinding:
    disposition: str  # satisfied / pending / failed / stale / unavailable / refused / unsupported
    reason: str
    missing: tuple[str, ...] = ()


class AdequacyError(ValueError):
    """The supplied review cannot bind this finite method."""


def _need(condition: bool, reason: str):
    if not condition:
        raise AdequacyError(reason)


def _digest(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def _document(payload: bytes, scope: V.Scope):
    _need(type(payload) is bytes and 0 < len(payload) <= F.DOCUMENT_BYTES,
          "native record must be immutable bytes within 1..65536")
    forms = S.parse(payload.decode("utf-8"))
    _need(all(type(form) is list and form and form[0] in {"comment", "experiment"} for form in forms),
          "native record contains an unexpected document")
    records = [form for form in forms if form[0] == "experiment"]
    _need(len(records) == 1, "native record requires exactly one experiment")
    issues = V.check_experiment(records[0], scope)
    _need(not issues, "native record shape/scoped graph refuses: " + str(issues[:1]))
    return forms, records[0]


def freeze_review(*, planned_experiment: bytes, dependencies: bytes, scope: V.Scope,
                  current_candidate: dict, inventory: T.InputReview,
                  impact_review: H.ImpactReview) -> MethodReview:
    """Copy caller review and bind the actual selected evidence before artifact I/O.

    The supported review is the existing fixed DIV producer closure. Schema,
    relation, manifest and influence interpretation stay with their public owners.
    The evidence fingerprint denotes the predeclaration; measured output metadata
    is bound to it separately by bind_measured_capture.
    """
    _need(type(scope) is V.Scope, "expected a plain scoped authority")
    _need(type(scope.profile_id) is str and 1 <= len(scope.profile_id) <= 128,
          "invalid scoped profile")
    for values, limit in ((scope.candidate_ids, 64), (scope.requirement_ids, 4096),
                          (scope.obligation_ids, 4096)):
        _need(type(values) is frozenset and 0 < len(values) <= limit
              and all(type(value) is str and 0 < len(value) <= T.TEXT_CHARS for value in values),
              "invalid bounded scoped identity set")
    selected_scope = V.Scope(scope.profile_id, frozenset(scope.candidate_ids),
                             frozenset(scope.requirement_ids), frozenset(scope.obligation_ids))
    _, raw = _document(planned_experiment, selected_scope)
    planned = D.references_to_doc([S.Symbol("references"), raw])["experiment"][0]
    case = P.reviewed_case(P.CASE_ID)
    _need((selected_scope.profile_id, planned["id"], planned["program"], planned["instructions"])
          == (case.profile_id, case.case_id, case.program, case.instructions),
          "review differs from the supported finite DIV case")
    frozen = T.freeze_review(inventory, profile_id=case.profile_id, experiment_id=case.case_id)
    candidate = I.bind_reference_identity(current_candidate)
    relations = R.bind_relations(planned, dict(candidate.fields))
    _need(relations.disposition == "matched", "planned method relations refuse: " + relations.reason)
    dependency = next(item for item in relations.plan.execution.common_inputs
                      if item.role == "dependency-manifest")
    document = F.parse_dependencies(dependencies, path=dependency.path)
    _need(_digest(dependencies) == dependency.sha256, "manifest differs from planned principal")
    principals = planned["verification"]["input"]
    children = document["input"]
    _need(len(principals) == T.MIN_INPUTS and len(children) == F.MANIFEST_INPUTS,
          "review requires the declared nine principals and64 distinct children")
    declared = tuple(X.InputBinding(row["role"], row["id"], row["path"], row["sha256"])
                     for row in (*principals, *children))
    coverage = T.compare_inputs(frozen, declared)
    _need(coverage.disposition == "matched", "declared closure differs from independent input review")
    manifest = M.ManifestPlan(relations.plan, dependency.input_id, frozen.inputs,
                              tuple(sorted(row["id"] for row in children)))
    context = H.freeze_review(impact_review, profile_id=case.profile_id, experiment_id=case.case_id)
    impact = H.check_inputs(context, frozen.inputs, frozen.inputs)
    _need(impact.disposition != "refused", "reviewed influence refuses: " + impact.reason)
    projection = H.project_inputs(frozen)
    digest = _digest(planned_experiment)
    if impact.disposition == "matched":
        for graph in (context.previous, context.current):
            selected = [node for node in graph.nodes if node.key == projection.evidence_key]
            _need(len(selected) == 1
                  and (selected[0].kind, selected[0].profile_ids, selected[0].fingerprint, selected[0].path)
                  == ("evidence", (frozen.profile_id,), digest, None),
                  "reviewed evidence fingerprint differs from actual predeclaration")
    return MethodReview(selected_scope, candidate, bytes(planned_experiment), manifest, frozen,
                        impact, projection.evidence_key, digest)


def bind_measured_capture(review: MethodReview, measured_experiment: bytes) -> CaptureBinding:
    """Allow only observation hashes/sizes and actual exits to replace targets.

    All other fields, ordering and structured comments must preserve the reviewed
    predeclaration. A match binds supplied bytes only; authentication, successful
    execution/comparison and provenance remain separate requirements.
    """
    try:
        _need(type(review) is MethodReview, "expected the frozen method review")
        if review.impact.disposition != "matched":
            return CaptureBinding(review.impact.disposition, review.impact.reason)
        planned_forms, planned = _document(review.planned_experiment, review.scope)
        measured_forms, measured = _document(measured_experiment, review.scope)
        normalized = deepcopy(measured_forms)
        restored = next(form for form in normalized if form[0] == "experiment")
        planned_graph = S.children(planned, "verification")[0]
        measured_graph = S.children(restored, "verification")[0]
        for family, names, count in (("observation", ("byte_size", "sha256"), 12),
                                      ("run", ("process_exit",), 3)):
            old = S.children(planned_graph, family)
            new = S.children(measured_graph, family)
            _need(len(old) == len(new) == count, "measured method record population differs")
            originals = {S.field(row, "id"): row for row in old}
            _need(set(originals) == {S.field(row, "id") for row in new},
                  "measured identities differ from predeclaration")
            for row in new:
                original = originals[S.field(row, "id")]
                for name in names:
                    S.children(row, name)[0][1] = S.field(original, name)
        _need(normalized == planned_forms, "measured record changes non-observation predeclaration data")
        _need(_digest(review.planned_experiment) == review.planned_sha256,
              "frozen predeclaration identity differs")
        mapped = D.references_to_doc([S.Symbol("references"), measured])["experiment"][0]
        observations = tuple(ObservationIdentity(row["id"], row["role"], row["path"],
                                                 row["sha256"], row["byte_size"])
                             for row in mapped["verification"]["observation"])
        return CaptureBinding("matched", "measured metadata preserves the reviewed predeclaration",
                              _digest(measured_experiment), review.planned_sha256,
                              review.evidence_key, observations)
    except OSError as error:
        return CaptureBinding("unavailable", "capture schema unavailable: " + str(error))
    except (AdequacyError, UnicodeError, S.SexpError, D.DossierError, V.K.SchemaError,
            AttributeError, KeyError, IndexError, TypeError, ValueError, RecursionError) as error:
        return CaptureBinding("refused", "capture binding: " + str(error))


def assess_findings(review: MethodReview, binding: CaptureBinding,
                    evaluation: E.EvaluationCheck) -> MethodFinding:
    """Compose trusted public-owner findings; never close full policy or a requirement.

    Callers must supply the evaluator result for these actual bytes and current
    review. The read-only command owns that orchestration. A partial evaluation
    remains pending; coherent failed/stale/unavailable findings retain their kind.
    """
    try:
        _need(type(review) is MethodReview and type(binding) is CaptureBinding,
              "expected plain method review and capture binding")
        if binding.disposition != "matched":
            return MethodFinding(binding.disposition, binding.reason)
        _need(binding.planned_sha256 == review.planned_sha256
              and binding.evidence_key == review.evidence_key
              and type(binding.record_sha256) is str and len(binding.record_sha256) == 64
              and not (set(binding.record_sha256) - set("0123456789abcdef"))
              and type(binding.observations) is tuple and len(binding.observations) == 12
              and all(type(item) is ObservationIdentity for item in binding.observations),
              "capture binding differs from selected method review")
        _need(type(evaluation) is E.EvaluationCheck, "expected the public retained evaluation")
        _need(evaluation.disposition in {"pending", "failed", "stale", "unavailable", "refused", "unsupported"},
              "invalid retained evaluation disposition")
        if evaluation.disposition != "pending":
            return MethodFinding(evaluation.disposition, evaluation.reason)
        positive = {"record": "valid", "manifest": "matched", "authentication": "matched",
                    "identity": "matched", "input_review": "matched", "impact": "matched",
                    "comparison": "satisfied", "source_image": "matched", "source_values": "matched",
                    "expected_author": "matched", "source_property": "matched"}
        missing = tuple(name for name in positive if getattr(evaluation, name) is None)
        expected_types = {"record": E.RecordCheck, "manifest": M.ManifestCheck,
                          "authentication": E.AuthenticationSummary, "identity": I.IdentityCheck,
                          "input_review": T.InputReviewCheck, "impact": H.InputImpactCheck,
                          "comparison": C.ComparisonUnit, "source_image": Image.SourceImageCheck,
                          "source_values": C.SourceExpectationCheck, "expected_author": U.ExpectedAuthorCheck,
                          "source_property": P.SourcePropertyCheck}
        for name, expected in positive.items():
            value = getattr(evaluation, name)
            if value is None:
                continue
            _need(type(value) is expected_types[name], "invalid required finding type: " + name)
            if value.disposition != expected:
                _need(value.disposition in {"failed", "stale", "unavailable", "refused", "unsupported"},
                      "invalid required finding disposition: " + name)
                return MethodFinding(value.disposition, name + ": " + getattr(value, "reason", "record is not valid"))
        if missing:
            return MethodFinding("pending", "required method findings have not been computed", missing)
        _need(type(evaluation.manifest.plan) is M.ManifestPlan
              and evaluation.manifest.plan == review.manifest,
              "evaluated manifest/relations differ from independently reviewed selection")
        _need(type(evaluation.record.issues) is tuple and not evaluation.record.issues,
              "valid record carries unresolved issues")
        _need(evaluation.identity.execution_identity == review.reference_identity.fields,
              "evaluated execution identity differs from current reviewed candidate")
        authentication = evaluation.authentication
        _need(type(authentication.files) is tuple
              and len(authentication.files) == len(review.inventory.inputs) + 12,
              "authentication lacks the complete reviewed distinct file set")
        expected_files = {("input", item.input_id): (item.role, item.path, item.sha256, None)
                          for item in review.inventory.inputs}
        expected_files.update({("observation", item.record_id):
                               (item.role, item.path, item.sha256, item.byte_size)
                               for item in binding.observations})
        actual = set()
        authenticated_bytes = 0
        for item in authentication.files:
            _need(type(item) is Q.FileFact and type(item.pin) is E.A.PinResult,
                  "invalid authenticated file fact type")
            key = (item.record_kind, item.record_id)
            _need(key in expected_files and key not in actual, "unreviewed or repeated authenticated file")
            role, path, digest, size = expected_files[key]
            _need((item.role, item.path, item.pin.disposition, item.pin.sha256)
                  == (role, path, "matched", digest) and item.data is None
                  and (size is None or item.pin.byte_size == size),
                  "authenticated file differs from bound record or retains payload")
            _need((item.pin.record_kind, item.pin.record_id, item.pin.path) == (key[0], key[1], path)
                  and type(item.pin.byte_size) is int and 0 <= item.pin.byte_size <= Q.MAX_READ_BYTES,
                  "file pin identity or byte accounting differs")
            authenticated_bytes += item.pin.byte_size
            actual.add(key)
        _need(actual == set(expected_files), "authenticated set omits selected artifacts")
        _need(type(authentication.snapshot_bytes) is int
              and 0 <= authentication.snapshot_bytes <= E.Q.MAX_SNAPSHOT_BYTES,
              "evaluation snapshot bound differs")
        _need(type(authentication.authenticated_bytes) is int
              and authentication.authenticated_bytes == authenticated_bytes
              and type(authentication.charged_read_bytes) is int
              and authenticated_bytes <= authentication.charged_read_bytes <= Q.MAX_READ_BYTES,
              "evaluation read accounting differs from authenticated file facts")
        runs = review.manifest.relations.execution.runs
        _need(type(evaluation.receipts) is tuple and len(evaluation.receipts) == 3,
              "method requires three bound process receipts")
        for expected, receipt in zip(runs, evaluation.receipts):
            _need(type(receipt) is E.ReceiptBinding and type(receipt.check) is Receipt.ReceiptCheck
                  and receipt.check.disposition == "matched"
                  and type(receipt.check.facts) is Receipt.ReceiptFacts
                  and type(receipt.check.facts.process_exit) is int
                  and (receipt.run_id, receipt.run_kind, receipt.check.facts.process_exit)
                  == (expected.run_id, expected.kind, 0)
                  and (receipt.check.facts.run_id, receipt.check.facts.run_kind, receipt.check.facts.argv)
                  == (expected.run_id, expected.kind, expected.argv),
                  "receipt lacks the selected successful run")
        comparison = evaluation.comparison
        _need(type(comparison.runs) is tuple and len(comparison.runs) == 3
              and tuple(row.run_kind for row in comparison.runs) == ("baseline", "repeat", "control")
              and all(row.comparison is not None and row.refusal is None for row in comparison.runs)
              and tuple(row.comparison.verdict for row in comparison.runs) == ("AGREE", "AGREE", "DIVERGE"),
              "comparison lacks the complete expected baseline/repeat/control results")
        _need(all(getattr(evaluation, name).facts is not None
                  for name in ("source_image", "source_values", "expected_author", "source_property")),
              "matched source findings lack their binding facts")
        _need(evaluation.source_property.facts.case == P.reviewed_case(P.CASE_ID),
              "source property differs from the reviewed finite DIV case")
        return MethodFinding("satisfied", "reviewed finite DIV method satisfied; full policy and requirement closure pending")
    except (AdequacyError, AttributeError, KeyError, TypeError, ValueError) as error:
        return MethodFinding("refused", "method findings: " + str(error))
