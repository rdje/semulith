#!/usr/bin/env python3
"""Capture a declared finite case once and retain its measured record and derived receipt.

The first canonical capture (P4-SYSTEM.14 a42am) was invoked by a scratch script and its two
result files were written by hand. This tool is that procedure, tracked:

  preflight   no process: the case is reviewed and its prepared inputs are pinned; every one of
              its twelve observation names and two result names is absent; the three native
              declarations on disk equal their regeneration from the current tree; the selected
              reference binary's bytes carry the retained identity's digest (public anchored
              reader, 8 MiB member bound); the declaration commit the operator names is a 40-hex
              object id. It is recorded in the receipt, never verified: this tool uses no Git.
  capture     one invocation of capture_div.capture(case_id). It is never retried, and every
              observation the collector reached stays on disk whatever the outcome.
  retain      exclusive publication of measured-experiment.sexp (the native record with measured
              output sizes, hashes and exits) when the collection recorded, and of
              verification.json (`div-capture-verification-v1`, qualification false) always. The
              receipt names repository-root identities under `object`, never `path`+`sha256`.

Exit 0 when the capture is pending and complete (three fresh zero-exit processes, every finding
reached); 1 when the preflight refuses or the capture refuses, fails or stays partial (outputs
preserved, receipt published if the invocation returned); 2 unavailable. Nothing here grants
method, policy, qualification or CPU credit; the receipt says so in its own words.
"""
from __future__ import annotations

import argparse
from dataclasses import asdict
import hashlib
import json
import os
from pathlib import Path
import re
import sys
import traceback

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))
import capture_div as A  # noqa: E402
import experiment_artifacts as Artifacts  # noqa: E402
import matched_gpr_collector as Collector  # noqa: E402
import matched_gpr_execution as E  # noqa: E402
import matched_gpr_property as P  # noqa: E402

ROOT = HERE.parent
FORMAT = "div-capture-verification-v1"
RESULT_BYTES = 65536
COMBINED_LIMIT = 128 * 1024 * 1024
SNAPSHOT_LIMIT = 16 * 1024 * 1024
OBJECT_ID = re.compile(r"[0-9a-f]{40}\Z")
RESULT_NAMES = ("measured-experiment.sexp", "verification.json")
FINDINGS = ("manifest", "identity", "comparison", "source_image", "input_review", "impact",
            "source_values", "expected_author", "source_property")
GENERIC_LIMITATIONS = (
    "before/after byte checks under a trusted quiescent runtime, not an atomic input set",
    "preparation/schema/runtime I/O and process RAM are outside the combined artifact-read allowance",
)


class RetentionRefused(ValueError):
    """The preflight found the case not ready, or a result could not be published exactly."""


def _require(condition, reason: str) -> None:
    if not condition:
        raise RetentionRefused(reason)


def observation_names() -> tuple[str, ...]:
    return tuple(f"{kind}.{suffix}" for kind in E.RUN_KINDS
                 for suffix in ("trace", "stdout", "stderr", "receipt.sexp"))


def preflight(root: Path, case_id: str, declaration_commit: str) -> dict:
    """Everything that must hold before a process starts; it starts none."""
    _require(type(declaration_commit) is str and OBJECT_ID.fullmatch(declaration_commit) is not None,
             "declaration commit must be a 40-hex object id")
    case = P.reviewed_case(case_id)
    pinned = A.prepared_inputs(case.case_id)
    directory = root / A.prefix(case.case_id)
    _require(directory.is_dir(), "case directory is missing: " + A.prefix(case.case_id))
    present = [name for name in (*observation_names(), *RESULT_NAMES) if (directory / name).exists()]
    _require(not present, "outputs already exist; a capture is never rerun: " + ", ".join(present))
    declaration = A.prepare_capture(case.case_id)
    for name, payload in A.declaration_files(declaration):
        record = dict(id=name, role="declaration", path=A.prefix(case.case_id) + "/" + name,
                      sha256=hashlib.sha256(payload).hexdigest())
        snapshot = Artifacts.read_snapshot(root, "input", record, max_bytes=RESULT_BYTES)
        _require(snapshot.pin.disposition == "matched" and snapshot.data == payload,
                 "retained declaration differs from its regeneration: " + name + " (" + snapshot.pin.reason + ")")
    fields = dict(declaration.authorities.reference.fields)
    binary = dict(id="sail-riscv", role="reference-binary", path=fields["binary"], sha256=fields["binary_sha256"])
    snapshot = Artifacts.read_snapshot(root, "input", binary, max_bytes=Collector.FILE_BYTES)
    _require(snapshot.pin.disposition == "matched",
             "reference binary differs from the retained identity: " + snapshot.pin.reason)
    return dict(case_id=case.case_id, program=case.program, instructions=case.instructions,
                properties=len(case.properties), declaration_commit=declaration_commit,
                binary=dict(path=binary["path"], sha256=binary["sha256"], byte_size=snapshot.pin.byte_size),
                prepared_inputs=[dict(role=role, id=identity, path=path, byte_size=size, sha256=digest)
                                 for role, identity, path, size, digest in pinned],
                declarations=[dict(name=name, byte_size=len(payload), sha256=hashlib.sha256(payload).hexdigest())
                              for name, payload in A.declaration_files(declaration)],
                absent=list((*observation_names(), *RESULT_NAMES)))


def _serial(value):
    if isinstance(value, bytes):
        return dict(encoding="hex", bytes=len(value), data=value.hex())
    raise TypeError(type(value).__name__)


def receipt(case: P.ReviewedPropertyCase, declaration_commit: str, result) -> dict:
    """The derived receipt: what the one invocation returned, with qualification false."""
    evaluation, collection = result.evaluation, result.collection
    authentication = None if evaluation is None else evaluation.authentication
    findings = {name: None if evaluation is None or getattr(evaluation, name) is None
                else getattr(evaluation, name).disposition for name in FINDINGS}
    runs = []
    if collection is not None:
        for kind, run in zip(E.RUN_KINDS, collection.runs):
            process = run.process
            outputs = () if process is None else (*process.outputs, *(() if run.receipt is None else (run.receipt,)))
            # Repository-root identities are pinned under `object`, as the first receipt does: a JSON
            # object carrying both `path` and `sha256` is a fixture pin resolved relative to the record's
            # own directory (FIXTURE-FINGERPRINT), which these are not. Readers map `object` to the
            # native `path` contract.
            runs.append(dict(kind=kind, process=run.disposition,
                             pid=None if process is None else process.pid,
                             exit=None if process is None else process.process_exit,
                             charge=run.charged_read_bytes,
                             outputs=[dict(role=item.role, observation_id=item.observation_id, object=item.path,
                                           byte_size=item.byte_size, sha256=item.sha256) for item in outputs]))
    complete = (collection is not None and collection.disposition == "recorded" and len(runs) == 3
                and len({run["pid"] for run in runs}) == 3 and all(run["exit"] == 0 for run in runs)
                and evaluation is not None and evaluation.disposition == "pending"
                and all(findings[name] is not None for name in FINDINGS))
    return dict(
        format_version=FORMAT, case_id=case.case_id, profile_id=A.PROFILE,
        source_declaration_commit=declaration_commit,
        disposition=result.disposition, reason=result.reason,
        canonical_capture_attempted=True, complete_canonical_capture=complete, qualification=False,
        policy_disposition="pending complete source/risk/feature policy",
        charged_read_bytes=result.charged_read_bytes, combined_limit=COMBINED_LIMIT,
        collection=None if collection is None else collection.disposition,
        evaluation=None if evaluation is None else evaluation.disposition,
        record=None if evaluation is None else asdict(evaluation.record),
        findings=findings,
        comparison=None if evaluation is None or evaluation.comparison is None else asdict(evaluation.comparison),
        runs=runs,
        authentication=None if authentication is None else dict(
            disposition=authentication.disposition, files=len(authentication.files),
            authenticated_bytes=authentication.authenticated_bytes,
            charged_read_bytes=authentication.charged_read_bytes,
            snapshot_bytes=authentication.snapshot_bytes, snapshot_limit=SNAPSHOT_LIMIT),
        limitations=[case.coverage + ", not all M or CPU acceptance", *GENERIC_LIMITATIONS],
    )


def publish(root: Path, case_id: str, name: str, payload: bytes) -> dict:
    """Write one result exclusively and read it back; an existing file refuses untouched."""
    _require(type(payload) is bytes and 0 < len(payload) <= RESULT_BYTES, "result payload outside 1..65536 bytes: " + name)
    path = root / A.prefix(case_id) / name
    try:
        fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o644)
    except FileExistsError:
        raise RetentionRefused("result already exists; never replaced: " + name) from None
    with os.fdopen(fd, "wb") as stream:
        _require(stream.write(payload) == len(payload), "incomplete result publication: " + name)
        stream.flush()
        os.fsync(stream.fileno())
    _require(path.read_bytes() == payload, "published result differs from its payload: " + name)
    return dict(path=A.prefix(case_id) + "/" + name, byte_size=len(payload), sha256=hashlib.sha256(payload).hexdigest())


def retain(root: Path, case_id: str, declaration_commit: str, *, preflight_only: bool = False) -> tuple[int, dict]:
    ready = preflight(root, case_id, declaration_commit)
    if preflight_only:
        return 0, dict(disposition="ready", qualification=False, canonical_capture=False, preflight=ready)
    case = P.reviewed_case(case_id)
    # One invocation. Whatever it returns or raises, nothing below removes or rewrites an output.
    try:
        result = A.capture(case.case_id)
    except BaseException:
        return 1, dict(disposition="escaped", qualification=False, canonical_capture=True, preflight=ready,
                       traceback=traceback.format_exc(), rule="outputs preserved; investigate; never retry")
    report = receipt(case, declaration_commit, result)
    publications = []
    if result.experiment is not None:
        publications.append(publish(root, case.case_id, "measured-experiment.sexp", result.experiment))
        report["measured_experiment"] = dict(id="measured-experiment", role="measured-record",
                                             object=publications[-1]["path"],
                                             byte_size=publications[-1]["byte_size"], sha256=publications[-1]["sha256"])
    payload = (json.dumps(report, indent=2, default=_serial) + "\n").encode("utf-8")
    publications.append(publish(root, case.case_id, "verification.json", payload))
    complete = report["complete_canonical_capture"] and result.disposition == "pending"
    return (0 if complete else 1), dict(disposition=result.disposition, complete_canonical_capture=complete,
                                        qualification=False, canonical_capture=True, preflight=ready,
                                        publications=publications, receipt=report)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--case", required=True, help="a reviewed case with pinned prepared inputs and retained declarations")
    parser.add_argument("--declaration-commit", required=True, help="the 40-hex commit that retained the declarations (recorded, not verified)")
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--preflight-only", action="store_true", help="check readiness; start no process, write nothing")
    args = parser.parse_args(argv)
    try:
        code, report = retain(args.root.resolve(), args.case, args.declaration_commit, preflight_only=args.preflight_only)
    except OSError as error:
        print(json.dumps(dict(disposition="unavailable", case_id=args.case, reason=type(error).__name__)))
        return 2
    except (RetentionRefused, P.PropertyError, A.AuthorityError, A.Review.ReviewError, A.F.ArtifactError,
            A.R.RecordRefused, A.Inputs.ReviewError, A.Author.AuthorReviewError, A.Impact.ImpactReviewError,
            A.Change.ImpactError, A.K.SchemaError, A.S.SexpError, A.C.CatalogRefused, A.D.DossierError,
            A.I.IdentityError, UnicodeError) as error:
        print(json.dumps(dict(disposition="refused", case_id=args.case, reason=str(error))))
        return 1
    text = json.dumps(report, indent=2, default=_serial)
    print(text if len(text) <= 4 * RESULT_BYTES else json.dumps(dict(disposition=report["disposition"], note="report truncated")))
    return code


if __name__ == "__main__":
    sys.exit(main())
