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
# The checker's own code, reached from review_div_method. The excerpt extractor is a producer root (the capture's
# manifest pins it) but no checker code imports it since a44-2c bound excerpts to the case's own authority.
SOURCE_MODULES = frozenset((*(A.Review.REVIEWED_MODULES - {"retain_div_statement"}),
                            "matched_gpr_adequacy", "review_div_method"))
# The retained, captured cases this review reads. They live here, in a consumer no case pins, so
# adding the next captured case does not invalidate any declaration (a42av).
# a42ax: the m-forms capture (a42aw) retained in e775705; P4-SYSTEM.14 a44-5: the M case re-captured as v4 under the
# declaration-as-data manifest (declared 177b43a1, captured 3c464095); P4-SYSTEM.14 a43b-2e: the M case re-captured once
# more as v5, its control declared (declared 7b1a8f44, captured 2988d6a2; traces byte-identical to v4's); P4-SYSTEM.14 a43e-5: as v6
# in the window that opens SSTC (declared 18a09566, captured 178f9c6c; traces byte-identical to v5's). P4-SYSTEM.14 a49-3: as v7, in the window that carries fetch faults
# (declared 3b24bd52, captured 57544407; traces byte-identical to v6's). Earlier versions are retained history, reviewed by nothing. The default case keeps its named pins (the method probe's synthetic copy re-pins them).
RETAINED_CASE_ID = "rv64gc-m-forms-v7"
SOURCE_DECLARATION_COMMIT = "3b24bd526765c389db476ba8d4bdda918ec6557d"
RETAINED_CAPTURE_COMMIT = "57544407914f8374faaadc1a756ff9fef8e7f40b"
MEASURED_SHA256 = "7527a85c33acaae90d929a70f008adaa892dd3af7a67664d1db51e275176748e"
MEASURED_BYTES = 16943
TOTAL_BYTES = A.Unit.Evaluation.Q.MAX_READ_BYTES


@dataclass(frozen=True)
class RetainedCapture:
    """Where one retained case was declared and captured, and its measured record: reviewed historical facts."""
    declaration_commit: str
    capture_commit: str
    measured_sha256: str
    measured_bytes: int


# P4-SYSTEM.14 a43a-2f: one row per reviewed capture, each case's own pins; a case without a row is unsupported.
RETAINED_CAPTURES = {
    RETAINED_CASE_ID: RetainedCapture(SOURCE_DECLARATION_COMMIT, RETAINED_CAPTURE_COMMIT, MEASURED_SHA256, MEASURED_BYTES),
    # The window that carries fetch faults (P4-SYSTEM.14 a49-1, a49-2): all 23 declared in 3b24bd52 and captured once in 57544407, the 17 unchanged cases' traces byte-identical to their predecessors', which are history since a49-1.
    "rv64gc-xlen-forms-v4": RetainedCapture(
        "3b24bd526765c389db476ba8d4bdda918ec6557d", "57544407914f8374faaadc1a756ff9fef8e7f40b",
        "0b87cbce6ce388e25523a05262ab432d77625a3242c201b51a72504a98cd5342", 14980),
    "rv64gc-csr-set-v3": RetainedCapture(
        "3b24bd526765c389db476ba8d4bdda918ec6557d", "57544407914f8374faaadc1a756ff9fef8e7f40b",
        "bf24e2583a868fc5d1f90aabf3989830afeaf4c1b9e3c6c314ef35905d2d5cde", 27347),
    "rv64gc-zicntr-v3": RetainedCapture(
        "3b24bd526765c389db476ba8d4bdda918ec6557d", "57544407914f8374faaadc1a756ff9fef8e7f40b",
        "88b6adfb8b78c0bbba0ffafc8709784242fd24415bb36e411434733501f90a6a", 24163),
    "rv64gc-sstc-v2": RetainedCapture(
        "3b24bd526765c389db476ba8d4bdda918ec6557d", "57544407914f8374faaadc1a756ff9fef8e7f40b",
        "0c84e833b2862001263d74210105dabb36219483f5d6e7bf65fb69477a2ed1a8", 22241),
    "rv64gc-alu-imm-v2": RetainedCapture(
        "3b24bd526765c389db476ba8d4bdda918ec6557d", "57544407914f8374faaadc1a756ff9fef8e7f40b",
        "d8159cefb9e8ddd209d8aa9205be6499a69b99c00ee9600b6547bf4bd91c7624", 13251),
    "rv64gc-alu-reg-v2": RetainedCapture(
        "3b24bd526765c389db476ba8d4bdda918ec6557d", "57544407914f8374faaadc1a756ff9fef8e7f40b",
        "fc17ca34d3ca147cff3bd1812f184b16a398555a02e244385a5e02086001f1de", 12154),
    "rv64gc-lui-auipc-v2": RetainedCapture(
        "3b24bd526765c389db476ba8d4bdda918ec6557d", "57544407914f8374faaadc1a756ff9fef8e7f40b",
        "3bd11dba2f5b9e7bad63cc4e30af7bba7a8751c5b83ee138aa35679a9f17e520", 12201),
    "rv64gc-jalr-lsb-v2": RetainedCapture(
        "3b24bd526765c389db476ba8d4bdda918ec6557d", "57544407914f8374faaadc1a756ff9fef8e7f40b",
        "c4856561e770ab01887f80e227d08fb3158c2e790782c6747e5cc57a5680dbc0", 12476),
    "rv64gc-no-delay-slots-v2": RetainedCapture(
        "3b24bd526765c389db476ba8d4bdda918ec6557d", "57544407914f8374faaadc1a756ff9fef8e7f40b",
        "6c12cb8b6adff8049d57518bd08eac50bf79d680ff9257d40acc60ade530397e", 13753),
    "rv64gc-shamt-v2": RetainedCapture(
        "3b24bd526765c389db476ba8d4bdda918ec6557d", "57544407914f8374faaadc1a756ff9fef8e7f40b",
        "84c147cd2a7aeac6cfcba8fb99530ecdfa0fd8a00afe03bfa1fab855136e26e8", 13497),
    "rv64gc-wsuffix-v2": RetainedCapture(
        "3b24bd526765c389db476ba8d4bdda918ec6557d", "57544407914f8374faaadc1a756ff9fef8e7f40b",
        "e036103d04a959701f571058d2a566da09db0123d75218cdf34cd8eb488a9475", 12951),
    "rv64gc-load-ext-v2": RetainedCapture(
        "3b24bd526765c389db476ba8d4bdda918ec6557d", "57544407914f8374faaadc1a756ff9fef8e7f40b",
        "c93bdd565a20a629e7e311b2a083833a2973b7ddcfb371904ee50d9fda6c80ba", 12832),
    "rv64gc-load-x0-v2": RetainedCapture(
        "3b24bd526765c389db476ba8d4bdda918ec6557d", "57544407914f8374faaadc1a756ff9fef8e7f40b",
        "de9b732a58b0f1f69690fa4ee6b892796db1fb881d1845dcf29408622d4f184b", 14719),
    "rv64gc-ecall-ebreak-v2": RetainedCapture(
        "3b24bd526765c389db476ba8d4bdda918ec6557d", "57544407914f8374faaadc1a756ff9fef8e7f40b",
        "ed55336b939390102d1b8956e67f7b8a4cd3e56c924dbc1326e2096a735e0134", 17655),
    "rv64gc-csr-access-v2": RetainedCapture(
        "3b24bd526765c389db476ba8d4bdda918ec6557d", "57544407914f8374faaadc1a756ff9fef8e7f40b",
        "20f7d58dabe54d5636d6abbfeec581a6c0a2c50eb91b660232d81773383b2b9c", 17178),
    "rv64gc-counters-v2": RetainedCapture(
        "3b24bd526765c389db476ba8d4bdda918ec6557d", "57544407914f8374faaadc1a756ff9fef8e7f40b",
        "3aa72b511c401a619fb37085218c754629020a156b5e90fa459ecec9bec7e364", 12150),
    "rv64gc-fencei-v2": RetainedCapture(
        "3b24bd526765c389db476ba8d4bdda918ec6557d", "57544407914f8374faaadc1a756ff9fef8e7f40b",
        "bf596e7c7944ed142d09c4201b0e60622f920a2f82befacecc1b676c37bbf963", 11052),
    "rv64gc-ialign-16-v2": RetainedCapture(
        "3b24bd526765c389db476ba8d4bdda918ec6557d", "57544407914f8374faaadc1a756ff9fef8e7f40b",
        "3a6a0f30be5173c6f7b9b99c59d7f843098bb25264e5404f654edbc86a29d387", 11405),
    "rv64gc-atomics-v1": RetainedCapture(
        "3b24bd526765c389db476ba8d4bdda918ec6557d", "57544407914f8374faaadc1a756ff9fef8e7f40b",
        "a9c6a2f0256b40fa38c8c42661b7840cc0abc75b727d6469bbaa7331e24f2896", 27721),
    "rv64gc-c-forms-v1": RetainedCapture(
        "3b24bd526765c389db476ba8d4bdda918ec6557d", "57544407914f8374faaadc1a756ff9fef8e7f40b",
        "a8795ba63d55ec942cb8786f99651b90bb09addc0a0633be6d8a16e20f6362c5", 23555),
    "rv64gc-f-forms-v1": RetainedCapture(
        "3b24bd526765c389db476ba8d4bdda918ec6557d", "57544407914f8374faaadc1a756ff9fef8e7f40b",
        "098f2565f8045da5eaf1f5f75b6a2fd2b942c275175cabfa7fdf378894da9f99", 33297),
    "rv64gc-d-forms-v1": RetainedCapture(
        "3b24bd526765c389db476ba8d4bdda918ec6557d", "57544407914f8374faaadc1a756ff9fef8e7f40b",
        "ab0630356bad8822b6d18a0bda62619680fff9091f32a6a1e1e9aeb7c57acb9b", 34607),
    # The seven with a switch (P4-SYSTEM.14 a50-2, a50-3): declared in 40488d5b, captured once in 633fe0cb, every compared file byte-identical to the rehearsal.
    "rv64gc-svade-v1": RetainedCapture(
        "40488d5b5ef2c24049a1f7a1b9760cc6d24d6bcf", "633fe0cb0c00d689fdfa3da785b531b49864d8f5",
        "d0ad7094446b2caaf54b471d5ce55aaf115c2a9bc59349e5e91bc622c41e8116", 13822),
    "rv64gc-atomic-misalign-v1": RetainedCapture(
        "40488d5b5ef2c24049a1f7a1b9760cc6d24d6bcf", "633fe0cb0c00d689fdfa3da785b531b49864d8f5",
        "a78b331867bc0ca445acee6039303d7f2fe1eccf01f167a9fd44a29a8449c5e1", 17750),
    "rv64gc-fault-priority-v1": RetainedCapture(
        "40488d5b5ef2c24049a1f7a1b9760cc6d24d6bcf", "633fe0cb0c00d689fdfa3da785b531b49864d8f5",
        "884f71918f6fecca4042341d0973668244b0b3ee4990f89847769520f62cc440", 21562),
    "rv64gc-priv-modes-v1": RetainedCapture(
        "40488d5b5ef2c24049a1f7a1b9760cc6d24d6bcf", "633fe0cb0c00d689fdfa3da785b531b49864d8f5",
        "c25f84eab25b567be5174fe56ea5b7ae857fcc9f5d6600a307a7d84a6594159a", 13782),
    "rv64gc-sv39-v1": RetainedCapture(
        "40488d5b5ef2c24049a1f7a1b9760cc6d24d6bcf", "633fe0cb0c00d689fdfa3da785b531b49864d8f5",
        "62ea14c63686b70c5761ba046967ecca485b70eafb8ed3bb0994014828ed79f7", 12765),
    "rv64gc-reservation-v1": RetainedCapture(
        "40488d5b5ef2c24049a1f7a1b9760cc6d24d6bcf", "633fe0cb0c00d689fdfa3da785b531b49864d8f5",
        "9704f8d4b35857ea7006fcb0f863ca055f18cb12b67f9c4e997776e36d3da5b3", 17095),
    "rv64gc-sc-deterministic-v1": RetainedCapture(
        "40488d5b5ef2c24049a1f7a1b9760cc6d24d6bcf", "633fe0cb0c00d689fdfa3da785b531b49864d8f5",
        "d956f455bbaff00e22184e4c1fc884f5f7dbcf5915b3fcfad1fdc63f2ce224dd", 16274),
    # The six `defined` of the last 17 (P4-SYSTEM.14 a51-1, a51-2): declared in 83f9ca4d, captured once in b3d1f8e8, every compared file byte-identical to the rehearsal.
    "rv64gc-composition-v1": RetainedCapture(
        "83f9ca4dc4ff4d3e299a6d1a47261f0f48623a24", "b3d1f8e8f19114b25810b4144b730337cf934457",
        "d6a4446a9d07fc5933a2cc276973b6d89e56193370ae0b3e032c42773111395c", 12769),
    "rv64gc-ext-closure-v1": RetainedCapture(
        "83f9ca4dc4ff4d3e299a6d1a47261f0f48623a24", "b3d1f8e8f19114b25810b4144b730337cf934457",
        "c74bf7c641c3dffa13fb8070b06f3fdf5c8e97c92385bd53ff1e42666fd6cd82", 12981),
    "rv64gc-priv-revision-v1": RetainedCapture(
        "83f9ca4dc4ff4d3e299a6d1a47261f0f48623a24", "b3d1f8e8f19114b25810b4144b730337cf934457",
        "224522d8f20effca248ba8233c1060589241977f5ec9b641fbb8a87783776ea2", 11259),
    "rv64gc-rvwmo-v1": RetainedCapture(
        "83f9ca4dc4ff4d3e299a6d1a47261f0f48623a24", "b3d1f8e8f19114b25810b4144b730337cf934457",
        "889d11ea2aa3912049e976970792410f68f0b8e9f98c0c9ecbcf9e6c26ad33e4", 12483),
    "rv64gc-priv-insns-v1": RetainedCapture(
        "83f9ca4dc4ff4d3e299a6d1a47261f0f48623a24", "b3d1f8e8f19114b25810b4144b730337cf934457",
        "5aaf71559610c6d61b04a883d969a51b29fb44ffd943aed0e7fd31dd043c2192", 10682),
    "rv64gc-priv-forms-v1": RetainedCapture(
        "83f9ca4dc4ff4d3e299a6d1a47261f0f48623a24", "b3d1f8e8f19114b25810b4144b730337cf934457",
        "79e752e4f8976dd39bf5bacc92012e85b783bbfde3c8aedfe297d6c2055193f5", 16584),
    # The two with a switch of the last 17 (P4-SYSTEM.14 a51-4, a51-5): declared in daadeb52, captured once in 45a334a2, every compared file byte-identical to the rehearsal.
    "rv64gc-no-h-v1": RetainedCapture(
        "daadeb524e789d01dbfa187e9ab3446083b70edc", "45a334a27e2e0b45855da920648abf9559b33a09",
        "0f6a17552aedb68de0aeb09af4d2f8d11d8815e0baa0da08957678738e00c158", 10785),
    "rv64gc-no-pmp-v1": RetainedCapture(
        "daadeb524e789d01dbfa187e9ab3446083b70edc", "45a334a27e2e0b45855da920648abf9559b33a09",
        "8e6da2e5d1cf7f598704b0c019cb48b57d9812e4f114ec5b11bf03270c334f5e", 10960),
}


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
    case_id: str = RETAINED_CASE_ID
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
            case_id=declaration.authorities.case_id, max_read_bytes=allowance)
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


def _measured_record(case_id, retained):
    """The reviewed capture's measured record, pinned by its row: the capture origin both review paths read."""
    return dict(id="measured-experiment", path=A.prefix(case_id) + "/measured-experiment.sexp",
                sha256=retained.measured_sha256, byte_size=retained.measured_bytes)


def _stale_declaration_route(budget, case_id, retained):
    """Ask whether a capture the producer refuses to prepare is stale (P4-SYSTEM.14 a43b-2b); return if it is not.

    A declaration retained before a43b-2b names no control id/statement, so the producer refuses to prepare it and
    the regenerated declarations cannot name the first moved one. Staleness is a moved pin (a42as), so it is measured
    on the capture's own manifest instead, read through the measured record's dependency-manifest pin: the pins of the
    declaration's route (the case file and its schema, the inputs a preparation reads first) are re-checked in order
    and the first that moved stops the review `stale`, naming it. When none moved, the refusal stands.
    """
    measured = budget.snapshot("observation", _measured_record(case_id, retained))
    experiments = [form for form in A.S.parse(measured.decode()) if form[0] == "experiment"]
    graphs = A.S.children(experiments[0], "verification") if len(experiments) == 1 else []
    pins = [item for item in (A.S.children(graphs[0], "input") if len(graphs) == 1 else [])
            if A.S.field(item, "role") == "dependency-manifest"]
    if len(pins) != 1:
        raise _Stopped("refused", "measured record names no single dependency manifest")
    manifest = budget.snapshot("input", dict(id="dependency-manifest", path=str(A.S.field(pins[0], "path")),
                                             sha256=str(A.S.field(pins[0], "sha256"))))
    documents = [form for form in A.S.parse(manifest.decode()) if form[0] == "dependencies"]
    if len(documents) != 1:
        raise _Stopped("refused", "dependency manifest is not one dependencies form")
    rows = {str(A.S.field(item, "path")): (str(A.S.field(item, "id")), str(A.S.field(item, "sha256")))
            for item in A.S.children(documents[0], "input")}
    for path in A.Review.declaration_paths(A.P.reviewed_case(case_id)):
        if path in rows:
            budget.snapshot("input", dict(id=rows[path][0], path=path, sha256=rows[path][1]))


def review_method(*, case_id=RETAINED_CASE_ID, max_read_bytes=TOTAL_BYTES) -> MethodCheck:
    """Check one reviewed retained case without Git, acquired caches or a binary.

    One inclusive128MiB native/evaluation allowance and the existing16MiB evaluator
    snapshot ceiling apply. Producer/authority preparation retains its published
    separate limits; the checker import census uses one8MiB pass and a recheck.
    These bounds do not describe peak RAM, loaded-code attestation or an atomic set.
    """
    if type(case_id) is not str or not 0 < len(case_id) <= 256:
        return MethodCheck("refused", "invalid bounded case selector")
    if case_id not in RETAINED_CAPTURES:
        return MethodCheck("unsupported", "no reviewed capture for selected case", case_id=case_id)
    retained = RETAINED_CAPTURES[case_id]
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
        case = A.P.reviewed_case(case_id)
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
            origin=(("reviewed_source_declaration", retained.declaration_commit),
                    ("reviewed_retained_capture", retained.capture_commit),
                    ("trust", "reviewed tracked collector and capture procedure; no independent execution attestation")),
            supported_claims=tuple(item.statement for item in case.properties))

    try:
        if ROOT != A.ROOT or ROOT != A.Review.ROOT or ROOT != A.V.ROOT:
            raise _Stopped("refused", "method owners do not share the selected runtime root")
        sources = A.Review.Snapshots(ROOT)
        A.Review.import_census(sources, roots=frozenset({"review_div_method"}), reviewed=SOURCE_MODULES)
        source_review_complete = True
        try:
            declaration = A.prepare_capture(case_id)
        except A.AuthorityError:
            _stale_declaration_route(budget, case_id, retained)  # stops `stale` on a moved pin of the route
            raise
        context = Adequacy.freeze_review(
            planned_experiment=declaration.planned_experiment, dependencies=declaration.dependencies,
            scope=declaration.authorities.scope,
            current_candidate=dict(declaration.authorities.reference.fields),
            inventory=declaration.inventory, impact_review=declaration.impact, case_id=case_id)
        for name, payload in A.declaration_files(declaration):
            budget.snapshot("input", dict(id=name, path=A.prefix(case_id) + "/" + name,
                                          sha256=hashlib.sha256(payload).hexdigest()), expected=payload)
        measured = budget.snapshot("observation", _measured_record(case_id, retained))
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
    parser.add_argument("--case", default=RETAINED_CASE_ID)
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
