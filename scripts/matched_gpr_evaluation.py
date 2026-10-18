#!/usr/bin/env python3
"""Read-only composition of retained first-method bindings and byte comparisons.

This boundary computes record validity and authenticated byte findings, not full
method/policy adequacy or qualification. The caller owns the current parent and
candidate selection, scoped authority and trusted runtime root. Parent in-memory
allocation and schema-tool I/O are outside the authenticated artifact budgets.
"""
from __future__ import annotations

from dataclasses import dataclass, replace
from pathlib import Path

import check_sexp_schema as K
import dossier_sexp as D
import experiment_artifacts as A
import experiment_verification as V
import matched_gpr_comparison as C
import matched_gpr_files as Q
import matched_gpr_identity as I
import matched_gpr_manifest as M
import matched_gpr_receipt as R
import matched_gpr_relations as B
import matched_gpr_source_image as F
import matched_gpr_input_review as T
import matched_gpr_impact as H
import sexp as S


@dataclass(frozen=True)
class RecordCheck:
    disposition: str  # valid / refused / unchecked; separate from method support
    issues: tuple[str, ...] = ()


@dataclass(frozen=True)
class AuthenticationSummary:
    disposition: str
    reason: str
    manifest_pin: A.PinResult | None
    files: tuple[Q.FileFact, ...]  # Metadata only: every data field is None.
    authenticated_bytes: int
    charged_read_bytes: int
    snapshot_bytes: int  # Payload returned by Q before release; not peak/process RAM.


@dataclass(frozen=True)
class ReceiptBinding:
    run_id: str
    run_kind: str
    declared_verdict: str
    check: R.ReceiptCheck


@dataclass(frozen=True)
class EvaluationCheck:
    disposition: str  # pending / failed / stale / unavailable / refused / unsupported
    reason: str
    record: RecordCheck
    manifest: M.ManifestCheck | None = None
    authentication: AuthenticationSummary | None = None
    identity: I.IdentityCheck | None = None
    receipts: tuple[ReceiptBinding, ...] = ()
    comparison: C.ComparisonUnit | None = None
    source_image: F.SourceImageCheck | None = None
    input_review: T.InputReviewCheck | None = None
    impact: H.InputImpactCheck | None = None
    source_values: C.SourceExpectationCheck | None = None


@dataclass(frozen=True)
class _RunContext:
    run_id: str
    kind: str
    verdict: str
    receipt: R.ReceiptContext


def _summary(files: Q.FileSetCheck | None) -> AuthenticationSummary | None:
    if files is None:
        return None
    return AuthenticationSummary(files.disposition, files.reason, files.manifest_pin,
                                 tuple(replace(fact, data=None) for fact in files.files),
                                 files.authenticated_bytes, files.charged_read_bytes,
                                 files.retained_bytes)


def _payload(files: Q.FileSetCheck, kind: str, rid: str) -> bytes | None:
    # Q owns the bounded distinct set and selected pin identities. Missing data
    # still reaches the public byte consumers as an explicit immutable-byte refusal.
    return next((fact.data for fact in files.files
                 if fact.record_kind == kind and fact.record_id == rid), None)


def evaluate_retained_unit(root: Path, *, raw_experiment: list, scope: V.Scope,
                           current_candidate: dict,
                           reviewed_inputs: T.InputReview | None = None,
                           impact_review: H.ImpactReview | None = None) -> EvaluationCheck:
    """Validate the scoped record, authenticate once and compute byte comparisons.

    Fixed 128 MiB total artifact reads/16 MiB live snapshot payload are owned by
    M's bounded manifest seed and Q's shared ledger. All used canonical context
    freezes before either reads. No artifact is reopened, no binary/process is
    accessed, and returned summaries release raw payloads. A fully bound positive
    comparison remains pending source-grounded property/closure/impact/provenance and
    full policy adequacy. Optional reviewed_inputs is separate caller authority;
    matching it checks declared coverage, not the completeness of that review.
    Optional impact_review binds supplied old/current graphs to those inventories;
    the caller still owns graph completeness, metadata and change review.
    It never grants qualification or CPU acceptance.
    """
    if type(scope) is not V.Scope:
        return EvaluationCheck("refused", "expected scoped record context", RecordCheck("unchecked"))
    try:
        issues = tuple(V.check_experiment(raw_experiment, scope))
    except OSError as exc:
        return EvaluationCheck("unavailable", f"record schema unavailable: {exc}", RecordCheck("unchecked"))
    except (K.SchemaError, D.DossierError, S.SexpError, UnicodeError,
            RecursionError, ValueError, TypeError) as exc:
        return EvaluationCheck("refused", f"record cannot be validated: {exc}", RecordCheck("refused"))
    if issues:
        return EvaluationCheck("refused", "record shape/identities/edges refuse", RecordCheck("refused", issues))
    record = RecordCheck("valid")
    try:
        experiment = D.references_to_doc([S.Symbol("references"), raw_experiment])["experiment"][0]
        identity_context = I.bind_reference_identity(current_candidate)
        candidate = dict(identity_context.fields)
        relations = B.bind_relations(experiment, candidate)
        if relations.disposition != "matched":
            return EvaluationCheck(relations.disposition, "relations: " + relations.reason, record)
        program = str(experiment["program"])
        if not 1 <= len(program) <= 65536:
            raise ValueError("parent program outside 1..65536 characters")
        execution = relations.plan.execution
        principals = {item.role: item for item in execution.common_inputs}
        source_input, image_input = principals["guest-source"], principals["guest-image"]
        graph = experiment["verification"]
        # The public relation/execution owners counted 9 inputs/12 outputs/3 runs
        # before these indexes. Copy selected observations before manifest I/O.
        inputs = {item["id"]: item for item in graph["input"]}
        observations = tuple(dict(item) for item in graph["observation"])
        outputs = {item["id"]: item for item in observations}
        runs = {item["id"]: item for item in graph["run"]}
        selected = []
        for binding in execution.runs:
            run = runs[binding.run_id]
            receipt_context = R.bind_receipt_context(
                run=run, inputs=[inputs[rid] for rid in run["input_ids"]],
                observations=[outputs[rid] for rid in run["observation_ids"]],
                current_candidate=candidate)
            selected.append(_RunContext(binding.run_id, binding.kind, run["verdict"], receipt_context))
        contexts = tuple(selected)
        review_context = (None if reviewed_inputs is None else
                          T.freeze_review(reviewed_inputs, profile_id=scope.profile_id,
                                          experiment_id=experiment["id"]))
        if impact_review is not None and review_context is None:
            raise ValueError("impact review requires current input review")
        impact_context = (None if impact_review is None else
                          H.freeze_review(impact_review, profile_id=scope.profile_id,
                                          experiment_id=experiment["id"]))
    except (I.IdentityError, R.BindingError, D.DossierError, KeyError, IndexError,
            TypeError, ValueError, RecursionError) as exc:
        return EvaluationCheck("refused", f"cannot bind selected context: {exc}", record)

    manifest = M.read_dependency_manifest(root, experiment=experiment, current_candidate=candidate)
    if manifest.disposition != "matched":
        return EvaluationCheck(manifest.disposition, "manifest: " + manifest.reason, record, manifest)
    if manifest.plan.relations != relations.plan:
        return EvaluationCheck("refused", "manifest differs from frozen relations", record, manifest)
    input_review = None
    impact = None
    if review_context is not None:
        try:
            input_review = T.compare_inputs(review_context, manifest.plan.inputs)
        except T.ReviewError as exc:
            return EvaluationCheck("refused", f"input review: {exc}", record, manifest)
        if impact_context is not None:
            impact = H.check_inputs(impact_context, manifest.plan.inputs, review_context.inputs)
            if impact.disposition == "refused":
                return EvaluationCheck("refused", "impact: " + impact.reason, record, manifest,
                                       input_review=input_review, impact=impact)
        if input_review.disposition != "matched":
            return EvaluationCheck("refused", "input review: " + input_review.reason,
                                   record, manifest, input_review=input_review, impact=impact)
        if impact is not None and impact.disposition == "stale":
            return EvaluationCheck("stale", "impact: " + impact.reason, record, manifest,
                                   input_review=input_review, impact=impact)
    files = Q.read_declared_files(root, manifest=manifest, observations=observations,
                                  retain_source_image=True)
    authentication = _summary(files)

    def finish(disposition: str, reason: str, *, identity: I.IdentityCheck | None = None,
               receipts: tuple[ReceiptBinding, ...] = (),
               comparison: C.ComparisonUnit | None = None,
               source_image: F.SourceImageCheck | None = None,
               source_values: C.SourceExpectationCheck | None = None) -> EvaluationCheck:
        result = EvaluationCheck(disposition, reason, record, manifest, authentication,
                               identity, receipts, comparison, source_image, input_review, impact)
        return replace(result, source_values=source_values)

    if files.disposition != "matched":
        return finish(files.disposition, "files: " + files.reason)
    identity_input = next(item for item in execution.common_inputs if item.role == "reference-identity")
    identity = I.check_reference_identity_bytes(_payload(files, "input", identity_input.input_id),
                                               path=identity_input.path, context=identity_context)
    if identity.disposition != "matched":
        return finish(identity.disposition, "identity: " + identity.reason, identity=identity)
    receipts = []
    for context in contexts:
        receipt_id = dict(context.receipt.receipt)["id"]
        checked = R.check_receipt_bytes(_payload(files, "observation", receipt_id), context=context.receipt)
        receipts.append(ReceiptBinding(context.run_id, context.kind, context.verdict, checked))
        if checked.disposition != "matched":
            return finish(checked.disposition, "receipt: " + checked.reason,
                          identity=identity, receipts=tuple(receipts))
    run_bytes = tuple(C.RunBytes(_payload(files, "observation", dict(binding.observations)["raw-gpr"]),
                                receipt.check.facts.process_exit)
                      for binding, receipt in zip(execution.runs, receipts))
    try:
        comparison = C.compare_unit(instructions=execution.instructions, witness=relations.plan.witness,
            program=program,
            baseline_expectation=_payload(files, "input", execution.baseline_expectation.input_id),
            control_expectation=_payload(files, "input", execution.control_expectation.input_id),
            baseline=run_bytes[0], repeat=run_bytes[1], control=run_bytes[2])
    except C.UnitError as exc:
        return finish("refused", "comparison: " + str(exc), identity=identity, receipts=tuple(receipts))
    if (comparison.disposition not in ("satisfied", "failed", "unsupported") or
            (comparison.disposition != "unsupported" and
             tuple(run.run_kind for run in comparison.runs) != tuple(run.kind for run in contexts))):
        return finish("refused", "comparison result lacks the complete ordered run set",
                      identity=identity, receipts=tuple(receipts), comparison=comparison)
    for declaration, observed in zip(contexts, comparison.runs):
        verdict = observed.comparison.verdict if observed.comparison is not None else "REFUSED"
        if declaration.verdict != verdict:
            return finish("refused", "recorded verdict differs from observed " + declaration.kind,
                          identity=identity, receipts=tuple(receipts), comparison=comparison)
    if comparison.disposition != "satisfied":
        return finish(comparison.disposition, "comparison: " + comparison.reason,
                      identity=identity, receipts=tuple(receipts), comparison=comparison)
    try:
        image_context = C.expectation_image_context(
            _payload(files, "input", execution.baseline_expectation.input_id),
            instructions=execution.instructions, program=program)
    except C.UnitError as exc:
        return finish("refused", "image context: " + str(exc), identity=identity,
                      receipts=tuple(receipts), comparison=comparison)
    source_bytes = _payload(files, "input", source_input.input_id)
    source_image = F.check_source_image(
        source_bytes,
        _payload(files, "input", image_input.input_id),
        program=image_context.program, entry=image_context.entry)
    if source_image.disposition != "matched":
        return finish(source_image.disposition, "source/image: " + source_image.reason,
                      identity=identity, receipts=tuple(receipts), comparison=comparison,
                      source_image=source_image)
    source_values = C.compare_source_expectation(
        source=source_bytes,
        baseline_expectation=_payload(files, "input", execution.baseline_expectation.input_id),
        instructions=execution.instructions, program=image_context.program,
        witness=relations.plan.witness)
    if (type(source_values) is not C.SourceExpectationCheck
            or source_values.disposition not in ("matched", "failed", "refused", "unavailable", "unsupported")
            or (source_values.disposition not in ("matched", "failed") and source_values.facts is not None)):
        return finish("refused", "source values: invalid result shape or disposition",
                      identity=identity, receipts=tuple(receipts), comparison=comparison,
                      source_image=source_image)
    if source_values.disposition in ("matched", "failed"):
        if (type(source_values.facts) is not C.SourceExpectationFacts
                or type(source_values.facts.derivation) is not C.Author.SnapshotDerivation
                or type(source_image.facts) is not F.SourceImageFacts):
            return finish("refused", "source values: incomplete source/image binding facts",
                          identity=identity, receipts=tuple(receipts), comparison=comparison,
                          source_image=source_image)
        derived = source_values.facts.derivation
        image_facts = source_image.facts
        if ((derived.program, derived.entry, derived.encoding_path, derived.source_size,
             derived.source_sha256, derived.payload_size, derived.payload_sha256) !=
                (image_facts.program, image_facts.entry, image_facts.encoding_path, image_facts.source_size,
                 image_facts.source_sha256, image_facts.payload_size, image_facts.payload_sha256)):
            return finish("refused", "source values: derivation differs from source/image context",
                          identity=identity, receipts=tuple(receipts), comparison=comparison,
                          source_image=source_image)
    if source_values.disposition in ("failed", "refused", "unavailable"):
        return finish(source_values.disposition, "source values: " + source_values.reason,
                      identity=identity, receipts=tuple(receipts), comparison=comparison,
                      source_image=source_image, source_values=source_values)
    value_scope = ("source values match" if source_values.disposition == "matched"
                   else "source values unsupported by current author, no credit")
    return finish("pending", "authenticated byte comparison binds; source/image match; " + value_scope
                  + "; complete method/policy adequacy pending",
                  identity=identity, receipts=tuple(receipts), comparison=comparison,
                  source_image=source_image, source_values=source_values)
