#!/usr/bin/env python3
"""Read-only finite DIV method review; complete policy qualification stays pending.

The selected capture origin is a reviewed historical fact, not independent
execution attestation. Current producer/declaration/byte owners and the supplied
native record establish the computed findings. No reference is launched.
"""

from __future__ import annotations

import argparse
from dataclasses import asdict, dataclass
import hashlib
import json
from pathlib import Path
import sys

sys.dont_write_bytecode = True

import capture_div as A
import matched_gpr_adequacy as Adequacy


ROOT = Path(__file__).resolve().parent.parent
SOURCE_MODULES = frozenset((*A.Review.REVIEWED_MODULES,
                            "matched_gpr_adequacy", "review_div_method"))
SOURCE_DECLARATION_COMMIT = "b160c66e183dee267ebf12edf25066412fe96ff6"
RETAINED_CAPTURE_COMMIT = "c91d08f52a2c8027092f2014e93f0e47ca4df557"
MEASURED_SHA256 = "2cb6c7041be5a6e52213c57fe7b1507ad096e76aebcc8323884679526fc6b29e"
MEASURED_BYTES = 9928
TOTAL_BYTES = A.Unit.Evaluation.Q.MAX_READ_BYTES


@dataclass(frozen=True)
class SourceIdentity:
    object: str
    byte_size: int
    sha256: str


@dataclass(frozen=True)
class MethodCheck:
    disposition: str
    reason: str
    policy_disposition: str = "pending"
    replay_disposition: str = "not-checked"
    case_id: str = A.P.CASE_ID
    record_disposition: str | None = None
    capture_binding: str | None = None
    evaluation_disposition: str | None = None
    read_limit: int = TOTAL_BYTES
    charged_read_bytes: int = 0
    authenticated_files: int | None = None
    authenticated_bytes: int | None = None
    snapshot_bytes: int | None = None
    record_sha256: str | None = None
    planned_sha256: str | None = None
    evidence_key: str | None = None
    missing_findings: tuple[str, ...] = ()
    checker_disposition: str | None = None
    checker_sources: tuple[SourceIdentity, ...] = ()
    origin: tuple[tuple[str, str], ...] = ()
    supported_claims: tuple[str, ...] = ()


class _Stopped(Exception):
    def __init__(self, disposition, reason):
        self.disposition = disposition
        self.reason = reason
        super().__init__(reason)


class _ReadBudget:
    """Reserve before each public reader; failed calls retain their full allowance."""

    def __init__(self, limit):
        self.limit = limit
        self.charged = 0

    @property
    def remaining(self):
        return self.limit - self.charged

    def snapshot(self, kind, record, expected=None):
        allowance = min(A.SMALL_BYTES, self.remaining)
        self.charged += allowance
        snapshot = A.Artifacts.read_snapshot(ROOT, kind, record, max_bytes=allowance)
        if type(snapshot) is not A.Artifacts.Snapshot or type(snapshot.pin) is not A.Artifacts.PinResult:
            raise _Stopped("refused", "native reader returned an invalid result")
        pin = snapshot.pin
        if pin.disposition != "matched":
            disposition = {"mismatch": "stale", "unavailable": "unavailable", "refused": "refused"}.get(pin.disposition)
            if disposition is None:
                raise _Stopped("refused", "native reader returned an unknown disposition")
            raise _Stopped(disposition, record["path"] + ": " + pin.reason)
        if (type(snapshot.data) is not bytes or type(pin.byte_size) is not int
                or pin.byte_size != len(snapshot.data) or not 0 <= pin.byte_size <= allowance
                or (pin.record_kind, pin.record_id, pin.path, pin.sha256)
                != (kind, record["id"], record["path"], record["sha256"])):
            raise _Stopped("refused", "native snapshot differs from selected bounded pin")
        if expected is not None and snapshot.data != expected:
            raise _Stopped("refused", "native predeclaration differs from reviewed generator")
        self.charged -= allowance - pin.byte_size
        return snapshot.data

    def evaluate(self, raw, declaration):
        allowance = self.remaining
        self.charged += allowance
        result = A.Unit.Evaluation.evaluate_retained_unit(
            ROOT, raw_experiment=raw, scope=declaration.authorities.scope,
            current_candidate=dict(declaration.authorities.reference.fields),
            reviewed_inputs=declaration.inventory, author_review=declaration.author,
            impact_review=declaration.impact,
            property_authority=declaration.authorities.property_authority,
            max_read_bytes=allowance)
        if type(result) is not A.Unit.Evaluation.EvaluationCheck:
            raise _Stopped("refused", "retained evaluator returned an invalid result")
        authentication = result.authentication
        if authentication is not None:
            if (type(authentication) is not A.Unit.Evaluation.AuthenticationSummary
                    or type(authentication.charged_read_bytes) is not int
                    or not 0 <= authentication.charged_read_bytes <= allowance
                    or type(authentication.authenticated_bytes) is not int
                    or not 0 <= authentication.authenticated_bytes <= authentication.charged_read_bytes):
                raise _Stopped("refused", "evaluator read receipt exceeds delegated allowance")
            self.charged -= allowance - authentication.charged_read_bytes
        # Before authentication, partial manifest reads have no complete receipt.
        # Keep the reservation rather than inventing a smaller failed-read charge.
        return result


def review_method(*, case_id=A.P.CASE_ID, max_read_bytes=TOTAL_BYTES) -> MethodCheck:
    """Check the one reviewed retained case without Git, acquired caches or a binary.

    One inclusive128MiB native/evaluation allowance and the existing16MiB evaluator
    snapshot ceiling apply. Producer/authority preparation retains its published
    separate limits; the checker import census uses one8MiB pass and a recheck.
    These bounds do not describe peak RAM, loaded-code attestation or an atomic set.
    """
    if type(case_id) is not str or not 0 < len(case_id) <= 256:
        return MethodCheck("refused", "invalid bounded case selector")
    if case_id != A.P.CASE_ID:
        return MethodCheck("unsupported", "no reviewed capture for selected case", case_id=case_id)
    if type(max_read_bytes) is not int or not 0 <= max_read_bytes <= TOTAL_BYTES:
        return MethodCheck("refused", "invalid method read allowance")
    if max_read_bytes == 0:
        return MethodCheck("refused", "method artifact allowance is zero", read_limit=0)
    budget = _ReadBudget(max_read_bytes)
    sources = None
    source_review_complete = False
    binding = evaluation = None

    def finish(disposition, reason, missing=()):
        identities = ()
        checker_disposition = None
        if sources is not None and not source_review_complete:
            checker_disposition = "unavailable" if disposition == "unavailable" else "refused"
        elif sources is not None:
            try:
                sources.recheck()
            except OSError as error:
                checker_disposition = disposition = "unavailable"
                reason = "checker source recheck: " + type(error).__name__
            except A.Review.ReviewError as error:
                checker_disposition = disposition = "refused"
                reason = "checker source recheck: " + str(error)
            else:
                checker_disposition = "matched"
                identities = tuple(SourceIdentity(path, len(data), hashlib.sha256(data).hexdigest())
                                   for path, data in sorted(sources.data.items()))
        authentication = None if evaluation is None else evaluation.authentication
        case = A.P.reviewed_case(A.P.CASE_ID)
        return MethodCheck(
            disposition, reason, case_id=case_id,
            record_disposition=None if evaluation is None else evaluation.record.disposition,
            capture_binding=None if binding is None else binding.disposition,
            evaluation_disposition=None if evaluation is None else evaluation.disposition,
            read_limit=max_read_bytes, charged_read_bytes=budget.charged,
            authenticated_files=None if authentication is None else len(authentication.files),
            authenticated_bytes=None if authentication is None else authentication.authenticated_bytes,
            snapshot_bytes=None if authentication is None else authentication.snapshot_bytes,
            record_sha256=None if binding is None else binding.record_sha256,
            planned_sha256=None if binding is None else binding.planned_sha256,
            evidence_key=None if binding is None else binding.evidence_key,
            missing_findings=missing, checker_disposition=checker_disposition, checker_sources=identities,
            origin=(("reviewed_source_declaration", SOURCE_DECLARATION_COMMIT),
                    ("reviewed_retained_capture", RETAINED_CAPTURE_COMMIT),
                    ("trust", "reviewed tracked collector and capture procedure; no independent execution attestation")),
            supported_claims=tuple(item.statement for item in case.properties))

    try:
        if ROOT != A.ROOT or ROOT != A.Review.ROOT or ROOT != A.V.ROOT:
            raise _Stopped("refused", "method owners do not share the selected runtime root")
        sources = A.Review.Snapshots(ROOT)
        A.Review.import_census(sources, roots=frozenset({"review_div_method"}), reviewed=SOURCE_MODULES)
        source_review_complete = True
        declaration = A.prepare_capture()
        context = Adequacy.freeze_review(
            planned_experiment=declaration.planned_experiment, dependencies=declaration.dependencies,
            scope=declaration.authorities.scope,
            current_candidate=dict(declaration.authorities.reference.fields),
            inventory=declaration.inventory, impact_review=declaration.impact)
        for name, payload in A.declaration_files(declaration):
            budget.snapshot("input", dict(id=name, path=A.PREFIX + "/" + name,
                                          sha256=hashlib.sha256(payload).hexdigest()), expected=payload)
        measured = budget.snapshot("observation", dict(
            id="measured-experiment", path=A.PREFIX + "/measured-experiment.sexp",
            sha256=MEASURED_SHA256, byte_size=MEASURED_BYTES))
        binding = Adequacy.bind_measured_capture(context, measured)
        if binding.disposition != "matched":
            return finish(binding.disposition, binding.reason)
        raw = next(form for form in A.S.parse(measured.decode()) if form[0] == "experiment")
        del measured
        evaluation = budget.evaluate(raw, declaration)
        finding = Adequacy.assess_findings(context, binding, evaluation)
        return finish(finding.disposition, finding.reason, finding.missing)
    except _Stopped as error:
        return finish(error.disposition, error.reason)
    except OSError as error:
        return finish("unavailable", type(error).__name__)
    except (Adequacy.AdequacyError, A.AuthorityError, A.Review.ReviewError,
            A.F.ArtifactError, A.R.RecordRefused, A.Inputs.ReviewError,
            A.Author.AuthorReviewError, A.Impact.ImpactReviewError, A.Change.ImpactError,
            A.K.SchemaError, A.S.SexpError, A.C.CatalogRefused, A.D.DossierError,
            A.I.IdentityError, A.P.PropertyError, UnicodeError, KeyError, IndexError,
            TypeError, ValueError, RecursionError) as error:
        return finish("refused", str(error))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--case", default=A.P.CASE_ID)
    parser.add_argument("--max-read-bytes", type=int, default=TOTAL_BYTES)
    args = parser.parse_args()
    result = review_method(case_id=args.case, max_read_bytes=args.max_read_bytes)
    payload = json.dumps(asdict(result), indent=2)
    if len(payload.encode("utf-8")) > A.SMALL_BYTES:
        print(json.dumps(dict(disposition="refused", reason="method diagnostic exceeds65536 bytes")))
        return 1
    print(payload)
    if result.disposition == "satisfied":
        return 0
    return 2 if result.disposition in {"unavailable", "unsupported"} else 1


if __name__ == "__main__":
    sys.exit(main())
