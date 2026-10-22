#!/usr/bin/env python3
"""Collect fresh three-run units and optionally evaluate them; no qualification."""
from __future__ import annotations

from contextlib import ExitStack
from dataclasses import dataclass
import errno
import os
from pathlib import Path

import dossier_sexp as D
import experiment_verification as V
import matched_gpr_collector as C
import matched_gpr_evaluation as Evaluation
import matched_gpr_expected_author as Author
import matched_gpr_identity as Identity
import matched_gpr_impact as Impact
import matched_gpr_input_review as Inventory
import matched_gpr_property as Property
import records_sexp as Records
import sexp as S


@dataclass(frozen=True)
class UnitRequest:
    runs: tuple[C.CaptureRequest, ...]


@dataclass(frozen=True)
class UnitCapture:
    disposition: str  # recorded / failed / stale / unavailable / refused
    reason: str
    runs: tuple[C.PublishedCapture, ...] = ()
    charged_read_bytes: int = 0


def _freeze(request):
    C._need(
        type(request) is UnitRequest
        and type(request.runs) is tuple
        and len(request.runs) == 3,
        "expected three frozen run requests",
    )
    runs = tuple(C._freeze(run) for run in request.runs)
    C._need(
        tuple(run.run_kind for run in runs) == C.E.RUN_KINDS,
        "expected baseline/repeat/control order",
    )
    C._need(len({run.run_id for run in runs}) == 3, "duplicate unit run ID")
    base, repeat, control = runs
    C._need(
        all(
            (r.instructions, r.binary_path, r.binary_sha256)
            == (base.instructions, base.binary_path, base.binary_sha256)
            for r in runs
        ),
        "unit execution identity differs",
    )
    common = [{i.role: i for i in r.inputs if i.role != "expectation"} for r in runs]
    C._need(
        common[0] == common[1] == common[2] and base.inputs == repeat.inputs,
        "unit common inputs differ",
    )
    expected = [next(i for i in r.inputs if i.role == "expectation") for r in runs]
    C._need(
        expected[2].input_id != expected[0].input_id
        and expected[2].path != expected[0].path,
        "control expectation is not distinct",
    )
    inputs = (*base.inputs, expected[2])
    outputs = tuple(o for r in runs for o in r.outputs)
    C._need(len({i.input_id for i in inputs}) == 9, "duplicate unit input ID")
    C._need(len({o.observation_id for o in outputs}) == 12, "duplicate unit output ID")
    C._need(
        not {i.input_id for i in inputs} & {o.observation_id for o in outputs},
        "unit input/output ID alias",
    )
    paths = [base.binary_path, *(i.path for i in inputs), *(o.path for o in outputs)]
    C._need(len(set(paths)) == len(paths), "unit input/output path alias")
    return UnitRequest(runs)


def _bind_unit(
    plan: C.E.ExecutionPlan, *, outputs: tuple[C.OutputTarget, ...]
) -> UnitRequest:
    """Freeze a validated public execution plan and its twelve owned output targets."""
    C._need(
        type(plan) is C.E.ExecutionPlan
        and type(outputs) is tuple
        and len(outputs) == 12,
        "expected public plan and twelve output targets",
    )
    C._need(
        all(type(o) is C.OutputTarget for o in outputs), "invalid unit output target"
    )
    C._need(
        type(plan.runs) is tuple
        and len(plan.runs) == 3
        and all(type(r) is C.E.RunBinding for r in plan.runs),
        "invalid public runs",
    )
    by_id = {C._id(o.observation_id): o for o in outputs}
    C._need(len(by_id) == 12, "duplicate unit output ID")
    runs = []
    for kind in C.E.RUN_KINDS:
        selected = [r for r in plan.runs if r.kind == kind]
        C._need(len(selected) == 1, "unit run selection is not singular")
        run = selected[0]
        C._need(
            type(run.observations) is tuple and len(run.observations) == 4,
            "invalid public output selection",
        )
        targets = []
        for pair in run.observations:
            C._need(
                type(pair) is tuple and len(pair) == 2 and pair[1] in by_id,
                "unknown public unit output",
            )
            targets.append(by_id[pair[1]])
        runs.append(C.freeze_request(plan, run_id=run.run_id, outputs=tuple(targets)))
    return _freeze(UnitRequest(tuple(runs)))


def freeze_unit(
    plan: C.E.ExecutionPlan, *, outputs: tuple[C.OutputTarget, ...]
) -> UnitRequest:
    """Freeze all used plan fields; malformed public plans raise CaptureError before I/O."""
    try:
        return _bind_unit(plan, outputs=outputs)
    except (AttributeError, IndexError, KeyError, TypeError) as exc:
        raise C.CaptureError("malformed public unit plan") from exc


def _reserve(root, request, resources):
    """Require fresh names and prove actual namespace separation before any child."""
    base = request.runs[0]
    inputs = (
        *base.inputs,
        next(i for i in request.runs[2].inputs if i.role == "expectation"),
    )
    protected_paths = [base.binary_path, *(i.path for i in inputs)]
    outputs = [o for r in request.runs for o in r.outputs]
    # The shared directory anchor indexes by role; use unique local keys because
    # all three runs intentionally reuse the four observation role names.
    records = tuple(
        C.OutputTarget(str(n), "anchor", path)
        for n, path in enumerate([*protected_paths, *(o.path for o in outputs)])
    )
    anchors, chain = C._parents(root, records, resources)
    C._check_parents(chain)
    selected = [anchors[str(n)] for n in range(len(protected_paths), len(records))]
    for parent, name in selected:
        try:
            os.stat(name, dir_fd=parent, follow_symlinks=False)
        except FileNotFoundError:
            continue
        raise C.CaptureError("unit output already exists; use a fresh capture set")
    reservations = []
    try:
        for parent, name in selected:
            fd = os.open(
                name,
                os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW,
                0o600,
                dir_fd=parent,
            )
            resources.callback(os.close, fd)
            info = os.fstat(fd)
            reservations.append((parent, name, info.st_dev, info.st_ino))
        C._check_parents(chain)
        for parent, name, device, inode in reservations:
            info = os.stat(name, dir_fd=parent, follow_symlinks=False)
            C._need(
                (info.st_dev, info.st_ino) == (device, inode),
                "unit reservation replaced",
            )
    finally:
        # A newly observed Git boundary revokes cleanup authority as well.
        C._check_parents(chain)
        for parent, name, device, inode in reservations:
            try:
                info = os.stat(name, dir_fd=parent, follow_symlinks=False)
                if (info.st_dev, info.st_ino) == (device, inode):
                    os.unlink(name, dir_fd=parent)
            except FileNotFoundError:
                pass
    return chain


def capture_unit(
    root: Path, *, request: UnitRequest, max_read_bytes: int = C.TOTAL_BYTES
) -> UnitCapture:
    """Collect the complete fresh unit within one conservative artifact-read bound."""
    runs = []
    allowance = remaining = 0

    def finish(disposition, reason):
        return UnitCapture(disposition, reason, tuple(runs), allowance - remaining)

    try:
        request = _freeze(request)
        C._need(
            type(max_read_bytes) is int and 0 <= max_read_bytes <= C.TOTAL_BYTES,
            "invalid unit read allowance",
        )
        allowance = remaining = max_read_bytes
        root = Path(root)
        with ExitStack() as resources:
            chain = _reserve(root, request, resources)
            pids = set()
            for run in request.runs:
                C._check_parents(chain)
                reserved = remaining
                remaining = 0
                result = C.capture_run_with_receipt(
                    root, request=run, max_read_bytes=reserved
                )
                C._need(
                    type(result) is C.PublishedCapture
                    and type(result.charged_read_bytes) is int
                    and 0 <= result.charged_read_bytes <= reserved,
                    "invalid unit delegated accounting",
                )
                C._need(
                    result.disposition
                    in ("recorded", "stale", "unavailable", "refused")
                    and type(result.reason) is str,
                    "invalid unit run disposition",
                )
                process = result.process
                if result.disposition == "recorded":
                    C._need(
                        type(process) is C.ProcessCapture
                        and process.disposition == "recorded"
                        and type(process.pid) is int
                        and process.pid > 0
                        and type(process.process_exit) is int
                        and type(process.charged_read_bytes) is int
                        and 0 <= process.charged_read_bytes <= result.charged_read_bytes
                        and type(process.outputs) is tuple
                        and len(process.outputs) == 3
                        and type(result.receipt) is C.CapturedOutput,
                        "incomplete collected unit run",
                    )
                    outputs = (*process.outputs, result.receipt)
                    for output, target in zip(outputs, run.outputs):
                        C._need(
                            type(output) is C.CapturedOutput
                            and (output.role, output.observation_id, output.path)
                            == (target.role, target.observation_id, target.path),
                            "unit output metadata differs",
                        )
                        limit = (
                            C.TRACE_BYTES
                            if output.role == "raw-gpr"
                            else C.STREAM_BYTES
                        )
                        C._need(
                            type(output.byte_size) is int
                            and 0 <= output.byte_size <= limit,
                            "invalid unit output size",
                        )
                        C._sha(output.sha256)
                    C._need(process.pid not in pids, "unit process identity repeated")
                    pids.add(process.pid)
                remaining = reserved - result.charged_read_bytes
                runs.append(result)
                C._check_parents(chain)
                if result.disposition != "recorded":
                    return finish(result.disposition, "unit run: " + result.reason)
                if process.process_exit != 0:
                    return finish("failed", "unit process did not exit zero")
            return finish(
                "recorded",
                "three fresh process/receipt pairs; comparison and qualification pending",
            )
    except (
        C.CaptureError,
        AttributeError,
        IndexError,
        KeyError,
        TypeError,
        ValueError,
    ) as exc:
        return finish("refused", str(exc))
    except OSError as exc:
        disposition = (
            "refused"
            if exc.errno in (errno.ELOOP, errno.ENOTDIR, errno.EEXIST)
            else "unavailable"
        )
        return finish(disposition, "unit I/O: " + (exc.strerror or type(exc).__name__))


@dataclass(frozen=True)
class UnitEvaluation:
    disposition: str  # pending / failed / stale / unavailable / refused / unsupported
    reason: str
    collection: UnitCapture | None = None
    evaluation: Evaluation.EvaluationCheck | None = None
    experiment: bytes | None = None  # Bounded measured record, not qualification.
    charged_read_bytes: int = 0


@dataclass(frozen=True)
class _EvaluationPlan:
    forms: list  # Private parsed copy; never caller-owned or returned directly.
    raw: list
    scope: V.Scope
    candidate: dict
    request: UnitRequest
    inventory: Inventory.InputReview | None
    impact: Impact.ImpactReview | None
    author: Author.ExpectedAuthorReview | None
    authority: Property.PropertyAuthority | None
    case_id: str  # the reviewed case the evaluation binds; the caller names it


EXPERIMENT_BYTES = 64 * 1024
SCOPE_IDS = 4096


class _PreparationFinding(C.CaptureError):
    def __init__(self, disposition, reason):
        super().__init__(reason)
        self.disposition = disposition


def _evaluation_scope(scope):
    C._need(type(scope) is V.Scope, "expected a plain scoped authority")
    C._text(scope.profile_id, "scope profile")
    groups = (scope.candidate_ids, scope.requirement_ids, scope.obligation_ids)
    for values in groups:
        C._need(type(values) is frozenset and len(values) <= SCOPE_IDS,
                "scope requires at most4096 immutable IDs per family")
        C._need(all(type(value) is str and 0 < len(value) <= 65536
                    for value in values), "invalid scope IDs")
    return V.Scope(scope.profile_id, *groups)


def _evaluation_plan(payload, scope, candidate, inventory, impact, author, authority, case_id):
    C._need(type(payload) is bytes and 0 < len(payload) <= EXPERIMENT_BYTES,
            "planned experiment requires1..65536 immutable bytes")
    # The case is the caller's selection, frozen before any artifact I/O; an unknown case
    # refuses here, not after a process ran.
    case_id = Property.reviewed_case(case_id).case_id
    scope = _evaluation_scope(scope)
    forms = S.parse(payload.decode("utf-8"), "planned experiment")
    documents = [form for form in forms
                 if not (isinstance(form, list) and form and form[0] == "comment")]
    C._need(len(documents) == 1 and isinstance(documents[0], list)
            and documents[0] and documents[0][0] == "experiment",
            "expected one planned experiment")
    raw = documents[0]
    issues = V.check_experiment(raw, scope)
    C._need(not issues, "planned record shape/identities/edges refuse")
    experiment = D.references_to_doc([S.Symbol("references"), raw])["experiment"][0]
    candidate = dict(Identity.bind_reference_identity(candidate).fields)
    relations = Evaluation.B.bind_relations(experiment, candidate)
    if relations.disposition != "matched":
        disposition = relations.disposition if relations.disposition in {"refused", "unsupported"} else "refused"
        raise _PreparationFinding(disposition, "planned relations: " + relations.reason)
    graph = experiment["verification"]
    targets = tuple(C.OutputTarget(item["role"], item["id"], item["path"])
                    for item in graph["observation"])
    request = freeze_unit(relations.plan.execution, outputs=targets)
    selected = dict(profile_id=scope.profile_id, experiment_id=experiment["id"])
    inventory = None if inventory is None else Inventory.freeze_review(inventory, **selected)
    author = None if author is None else Author.freeze_review(author, **selected)
    if author is not None:
        C._need(inventory is None or inventory == author.inventory,
                "author inventory differs from current review")
        inventory = author.inventory
    if authority is not None:
        C._need(author is not None, "source property requires author review")
        declared = graph["property"]
        C._need(type(declared) is list and 1 <= len(declared) <= Property.MAX_PROPERTIES,
                "source property requires 1..64 declared properties")
        witnesses = {item.property_id: item.witness for item in relations.plan.properties}
        claims = tuple(Property.PropertyClaim(
            prop["id"], prop["requirement_id"], tuple(prop["obligation_ids"]), prop["statement"],
            witnesses[prop["id"]]) for prop in declared)
        context = Property.freeze_context(Property.PropertyContext(
            scope.profile_id, experiment["id"], experiment["program"], claims,
            relations.plan.control_property_id, authority), **selected)
        authority = context.authority
    if impact is not None:
        C._need(inventory is not None, "impact requires current input review")
        paths, uncertain = impact.changed_paths, impact.uncertain
        frozen = Impact.freeze_review(impact, **selected)
        impact = Impact.ImpactReview(frozen.profile_id, frozen.experiment_id,
                                    frozen.previous, frozen.current, paths, uncertain)
    return _EvaluationPlan(forms, raw, scope, candidate, request, inventory,
                           impact, author, authority, case_id)


def _unit_observations(result, request, allowance):
    C._need(type(result) is UnitCapture and type(result.reason) is str
            and type(result.charged_read_bytes) is int
            and 0 <= result.charged_read_bytes <= allowance,
            "invalid combined collection accounting")
    C._need(result.disposition == "recorded" and type(result.runs) is tuple
            and len(result.runs) == 3, "collection is incomplete")
    observations, pids, charges = [], set(), 0
    for published, run in zip(result.runs, request.runs):
        C._need(type(published) is C.PublishedCapture and published.disposition == "recorded"
                and type(published.charged_read_bytes) is int
                and 0 <= published.charged_read_bytes <= result.charged_read_bytes,
                "invalid combined publication metadata")
        process = published.process
        C._need(type(process) is C.ProcessCapture and process.disposition == "recorded"
                and type(process.process_exit) is int and process.process_exit == 0
                and type(process.pid) is int and process.pid > 0 and process.pid not in pids
                and type(process.charged_read_bytes) is int
                and 0 <= process.charged_read_bytes <= published.charged_read_bytes
                and type(process.outputs) is tuple and len(process.outputs) == 3,
                "invalid combined process metadata")
        pids.add(process.pid)
        outputs = (*process.outputs, published.receipt)
        for item, target in zip(outputs, run.outputs):
            C._need(type(item) is C.CapturedOutput
                    and (item.role, item.observation_id, item.path)
                    == (target.role, target.observation_id, target.path),
                    "combined output differs from frozen target")
            limit = C.TRACE_BYTES if item.role == "raw-gpr" else C.STREAM_BYTES
            C._need(type(item.byte_size) is int and 0 <= item.byte_size <= limit,
                    "invalid combined output size")
            C._sha(item.sha256)
            observations.append(C.CapturedOutput(item.role, item.observation_id,
                                                item.path, item.byte_size, item.sha256))
        charges += published.charged_read_bytes
    C._need(charges == result.charged_read_bytes
            and sum(item.byte_size for item in observations) <= charges,
            "combined collection charge omits observed bytes")
    return tuple(observations)


def _measured_experiment(plan, observations):
    verification = S.children(plan.raw, "verification")[0]
    by_id = {item.observation_id: item for item in observations}
    for form in S.children(verification, "observation"):
        item = by_id[S.field(form, "id")]
        S.children(form, "byte_size")[0][1] = item.byte_size
        S.children(form, "sha256")[0][1] = item.sha256
    for form in S.children(verification, "run"):
        S.children(form, "process_exit")[0][1] = 0  # All measured exits checked above.
    payload = Records.render_forms(plan.forms).encode("utf-8")
    C._need(0 < len(payload) <= EXPERIMENT_BYTES, "measured experiment exceeds65536 bytes")
    return payload


def _evaluation_charge(result, plan, allowance):
    C._need(type(result) is Evaluation.EvaluationCheck and result.disposition == "pending",
            "evaluation is not pending")
    summary, manifest = result.authentication, result.manifest
    C._need(type(summary) is Evaluation.AuthenticationSummary
            and summary.disposition == "matched"
            and type(manifest) is Evaluation.M.ManifestCheck
            and manifest.disposition == "matched"
            and type(manifest.pin) is C.A.PinResult
            and manifest.pin.disposition == "matched"
            and summary.manifest_pin == manifest.pin,
            "pending evaluation lacks authenticated manifest accounting")
    selected = next(item for item in plan.request.runs[0].inputs
                    if item.role == "dependency-manifest")
    pin = manifest.pin
    C._need((pin.record_kind, pin.record_id, pin.path, pin.sha256)
            == ("input", selected.input_id, selected.path, selected.sha256)
            and type(pin.byte_size) is int and 1 <= pin.byte_size <= EXPERIMENT_BYTES,
            "evaluation seed differs from frozen manifest")
    C._need(type(summary.authenticated_bytes) is int
            and type(summary.charged_read_bytes) is int
            and pin.byte_size <= summary.authenticated_bytes
            <= summary.charged_read_bytes <= allowance
            and type(summary.snapshot_bytes) is int
            and 0 <= summary.snapshot_bytes <= Evaluation.Q.MAX_SNAPSHOT_BYTES,
            "invalid seed-inclusive evaluation accounting")
    return summary.charged_read_bytes


def capture_and_evaluate(
    root: Path, *, planned_experiment: bytes, scope: V.Scope, current_candidate: dict,
    reviewed_inputs: Inventory.InputReview | None = None,
    impact_review: Impact.ImpactReview | None = None,
    author_review: Author.ExpectedAuthorReview | None = None,
    property_authority: Property.PropertyAuthority | None = None,
    case_id: str = Property.CASE_ID,
    max_read_bytes: int = C.TOTAL_BYTES,
) -> UnitEvaluation:
    """Collect and evaluate one unit within one conservative artifact-read allowance.

    The case the evaluation binds is the caller's (case_id; the retained case by default): a
    capture of a declared case names it, so no pinned module constant has to move (a42av).

    Planned bytes/caller authorities are frozen before artifact I/O. Declared
    verdicts stay caller claims checked by evaluation; output hashes/sizes/exits
    come from collection. Structured comment forms survive canonical rendering.
    Failed/invalid delegated findings keep their whole reservation; no retry or
    qualification occurs. Runtime/schema I/O and caller RAM are separate costs.
    Unexpected programming exceptions propagate; the caller must keep reservations.
    """
    if type(max_read_bytes) is not int or not 0 <= max_read_bytes <= C.TOTAL_BYTES:
        return UnitEvaluation("refused", "invalid combined read allowance")
    allowance = remaining = max_read_bytes
    collection = evaluation = payload = None

    def finish(disposition, reason):
        return UnitEvaluation(disposition, reason, collection, evaluation, payload,
                              allowance - remaining)

    try:
        plan = _evaluation_plan(planned_experiment, scope, current_candidate,
                                reviewed_inputs, impact_review, author_review,
                                property_authority, case_id)
        reserved, remaining = remaining, 0
        captured = capture_unit(root, request=plan.request, max_read_bytes=reserved)
        C._need(type(captured) is UnitCapture and type(captured.reason) is str
                and type(captured.charged_read_bytes) is int
                and 0 <= captured.charged_read_bytes <= reserved
                and type(captured.runs) is tuple and len(captured.runs) <= 3
                and all(type(run) is C.PublishedCapture for run in captured.runs),
                "invalid combined collection finding")
        C._need(captured.disposition in {"recorded", "failed", "stale", "unavailable", "refused"},
                "unknown combined collection disposition")
        if captured.disposition != "recorded":
            collection = captured
            return finish(captured.disposition, "collection: " + captured.reason)
        observations = _unit_observations(captured, plan.request, reserved)
        collection = captured
        remaining = reserved - captured.charged_read_bytes
        payload = _measured_experiment(plan, observations)
        reserved, remaining = remaining, 0
        checked = Evaluation.evaluate_retained_unit(
            root, raw_experiment=plan.raw, scope=plan.scope,
            current_candidate=plan.candidate, reviewed_inputs=plan.inventory,
            impact_review=plan.impact, author_review=plan.author, case_id=plan.case_id,
            property_authority=plan.authority, max_read_bytes=reserved)
        C._need(type(checked) is Evaluation.EvaluationCheck
                and type(checked.reason) is str
                and type(checked.record) is Evaluation.RecordCheck
                and checked.disposition in {"pending", "failed", "stale", "unavailable", "refused", "unsupported"},
                "invalid combined evaluation finding")
        if checked.disposition != "pending":
            evaluation = checked
            return finish(checked.disposition, "evaluation: " + checked.reason)
        charged = _evaluation_charge(checked, plan, reserved)
        evaluation = checked
        remaining = reserved - charged
        return finish("pending", "fresh collection and retained findings; complete policy/qualification pending")
    except _PreparationFinding as exc:
        return finish(exc.disposition, str(exc))
    except (C.CaptureError, Identity.IdentityError, Inventory.ReviewError,
            Author.AuthorReviewError, Impact.ImpactReviewError, Property.PropertyError,
            D.DossierError, S.SexpError, Evaluation.K.SchemaError, UnicodeError,
            AttributeError, IndexError, KeyError, TypeError, ValueError, RecursionError) as exc:
        return finish("refused", "combined unit: " + str(exc))
    except OSError as exc:
        return finish("unavailable", "combined unit I/O: " + (exc.strerror or type(exc).__name__))
