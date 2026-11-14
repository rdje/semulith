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
# (declared 3b24bd52, captured 57544407; traces byte-identical to v6's). P4-SYSTEM.20 f2: as v8, in version 1's window
# (declared 8a50b9c5, captured 5c3d6737; traces byte-identical to v7's). Earlier versions are retained history, reviewed by nothing. The default case keeps its named pins (the method probe's synthetic copy re-pins them).
RETAINED_CASE_ID = "rv64gc-m-forms-v8"
SOURCE_DECLARATION_COMMIT = "8a50b9c566be47bd697e1969fa53ebf76d2d981b"
RETAINED_CAPTURE_COMMIT = "5c3d6737c7a73e0d90eac498c6b9e46cf6b0c990"
MEASURED_SHA256 = "beb996a107d1181011dd34676403da0c299d3280529394cc499a2fb4c452f4ae"
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
    # Version 1's window (P4-SYSTEM.20 f1, f2): the 42 successors declared in 8a50b9c5 and captured once in 5c3d6737, every
    # trace byte-identical to its predecessor's; the predecessors are listed on retired-cases.md. In the order their predecessors stood.
    "rv64gc-xlen-forms-v5": RetainedCapture(
        "8a50b9c566be47bd697e1969fa53ebf76d2d981b", "5c3d6737c7a73e0d90eac498c6b9e46cf6b0c990",
        "440c4d698f53597e2ca5220254841043767a497a2a5a6747ce21c10bc017dac9", 14980),
    "rv64gc-csr-set-v4": RetainedCapture(
        "8a50b9c566be47bd697e1969fa53ebf76d2d981b", "5c3d6737c7a73e0d90eac498c6b9e46cf6b0c990",
        "dc628b5fa0c8db6a7833c6cf39fba1f1b6633f01c5554b3c3129251a5541d71d", 27347),
    "rv64gc-zicntr-v4": RetainedCapture(
        "8a50b9c566be47bd697e1969fa53ebf76d2d981b", "5c3d6737c7a73e0d90eac498c6b9e46cf6b0c990",
        "b9cc6cfed9391c71bdb5939a18f7482eef90a789cc7493abbd9ee454e28bfe55", 24163),
    "rv64gc-sstc-v3": RetainedCapture(
        "8a50b9c566be47bd697e1969fa53ebf76d2d981b", "5c3d6737c7a73e0d90eac498c6b9e46cf6b0c990",
        "612ffa26942c1748a95b56d18b2e28db9bc98a93fea9300b3d51e133ccecd985", 22241),
    "rv64gc-alu-imm-v3": RetainedCapture(
        "8a50b9c566be47bd697e1969fa53ebf76d2d981b", "5c3d6737c7a73e0d90eac498c6b9e46cf6b0c990",
        "559028769f6499a6d519791f7857042962f05ae33036be11966064d828185298", 13251),
    "rv64gc-alu-reg-v3": RetainedCapture(
        "8a50b9c566be47bd697e1969fa53ebf76d2d981b", "5c3d6737c7a73e0d90eac498c6b9e46cf6b0c990",
        "2f301777c0ce27a5d565a7f38213d0bc625cfdeb219b0aeece9cc3b5f3d12f9f", 12154),
    "rv64gc-lui-auipc-v3": RetainedCapture(
        "8a50b9c566be47bd697e1969fa53ebf76d2d981b", "5c3d6737c7a73e0d90eac498c6b9e46cf6b0c990",
        "fa260ba372179bd1d9cf0c6b8c934b07eef445eba163bd1953be64d960a7800f", 12201),
    "rv64gc-jalr-lsb-v3": RetainedCapture(
        "8a50b9c566be47bd697e1969fa53ebf76d2d981b", "5c3d6737c7a73e0d90eac498c6b9e46cf6b0c990",
        "148d046cf5169146c3295c53bb10d1665b2bfb34607d74cf218e142ff4c5decb", 12476),
    "rv64gc-no-delay-slots-v3": RetainedCapture(
        "8a50b9c566be47bd697e1969fa53ebf76d2d981b", "5c3d6737c7a73e0d90eac498c6b9e46cf6b0c990",
        "78d9bad17dbe2c1002c2c051d463601fcbe1f2d699d921a946e89b8c0be8b597", 13753),
    "rv64gc-shamt-v3": RetainedCapture(
        "8a50b9c566be47bd697e1969fa53ebf76d2d981b", "5c3d6737c7a73e0d90eac498c6b9e46cf6b0c990",
        "709d9237e30e61c6e94cbb711917c83a9c201db31ea3d9c9512ccea0aa0d05cd", 13497),
    "rv64gc-wsuffix-v3": RetainedCapture(
        "8a50b9c566be47bd697e1969fa53ebf76d2d981b", "5c3d6737c7a73e0d90eac498c6b9e46cf6b0c990",
        "ccaec0dd2a27ed8226eb0cafa5468d3d82f4c933e55f9d8fcecbdba63094ef5a", 12951),
    "rv64gc-load-ext-v3": RetainedCapture(
        "8a50b9c566be47bd697e1969fa53ebf76d2d981b", "5c3d6737c7a73e0d90eac498c6b9e46cf6b0c990",
        "ffe3412c681ee2f9254ce25955300877ba2ebb7b38a5a0d0a6143102027091ac", 12832),
    "rv64gc-load-x0-v3": RetainedCapture(
        "8a50b9c566be47bd697e1969fa53ebf76d2d981b", "5c3d6737c7a73e0d90eac498c6b9e46cf6b0c990",
        "8b822ef6d4af41c53708c0557c7f50de6741ccd0f8afcb4b6f7ddaf96a48867f", 14719),
    "rv64gc-ecall-ebreak-v3": RetainedCapture(
        "8a50b9c566be47bd697e1969fa53ebf76d2d981b", "5c3d6737c7a73e0d90eac498c6b9e46cf6b0c990",
        "22c4e1d94aa3212e61818636a4f2a1b5a27fa8042e915f64f1bad459aa810b16", 17655),
    "rv64gc-csr-access-v3": RetainedCapture(
        "8a50b9c566be47bd697e1969fa53ebf76d2d981b", "5c3d6737c7a73e0d90eac498c6b9e46cf6b0c990",
        "7c1b02bf39e24647ead6029bb4e8567349c0165e157dbd2eaf05129b3aed03a1", 17178),
    "rv64gc-counters-v3": RetainedCapture(
        "8a50b9c566be47bd697e1969fa53ebf76d2d981b", "5c3d6737c7a73e0d90eac498c6b9e46cf6b0c990",
        "7c6e1a082c93049d7908b3f05275da10ffb063b8b2be7d6bec49bd9c7e468707", 12150),
    "rv64gc-fencei-v3": RetainedCapture(
        "8a50b9c566be47bd697e1969fa53ebf76d2d981b", "5c3d6737c7a73e0d90eac498c6b9e46cf6b0c990",
        "cbbd3362fa2fbd390e27839024efc24b3fe4ed178f8577ccfde759394f8b99da", 11052),
    "rv64gc-ialign-16-v3": RetainedCapture(
        "8a50b9c566be47bd697e1969fa53ebf76d2d981b", "5c3d6737c7a73e0d90eac498c6b9e46cf6b0c990",
        "bd76325485f7e8e01c61cacb44ff92d86a970140e74b4dac313b8a0a78ad0d37", 11405),
    "rv64gc-atomics-v2": RetainedCapture(
        "8a50b9c566be47bd697e1969fa53ebf76d2d981b", "5c3d6737c7a73e0d90eac498c6b9e46cf6b0c990",
        "92cef4788bf48939b3e86f924d338750f043ccf7ccc28e86371d07cecc51cec5", 27721),
    "rv64gc-c-forms-v2": RetainedCapture(
        "8a50b9c566be47bd697e1969fa53ebf76d2d981b", "5c3d6737c7a73e0d90eac498c6b9e46cf6b0c990",
        "76f8ecf4ff10c60007f4e7a153fabecfc5d958969a96a58d344a03b8b7061392", 23555),
    "rv64gc-f-forms-v2": RetainedCapture(
        "8a50b9c566be47bd697e1969fa53ebf76d2d981b", "5c3d6737c7a73e0d90eac498c6b9e46cf6b0c990",
        "1c87177f6a0697b4193aab5e04b007113bad87757c882fd578dc996d7ec8bdd0", 33297),
    "rv64gc-d-forms-v2": RetainedCapture(
        "8a50b9c566be47bd697e1969fa53ebf76d2d981b", "5c3d6737c7a73e0d90eac498c6b9e46cf6b0c990",
        "9f880c547427746e7fe564ea4427e96471a791bae28bec9b1d20e9f67087b8f8", 34607),
    "rv64gc-svade-v2": RetainedCapture(
        "8a50b9c566be47bd697e1969fa53ebf76d2d981b", "5c3d6737c7a73e0d90eac498c6b9e46cf6b0c990",
        "f91c76535ab8c4b8e0549ca629a2ef3821f3472f503b6ffdf8bdd90dfc23fbe5", 13822),
    "rv64gc-atomic-misalign-v2": RetainedCapture(
        "8a50b9c566be47bd697e1969fa53ebf76d2d981b", "5c3d6737c7a73e0d90eac498c6b9e46cf6b0c990",
        "e4c36de6c95e6a4dcc785afb47a3f2d2da7f0250015e7699a2f203f9323dbc90", 17750),
    "rv64gc-fault-priority-v2": RetainedCapture(
        "8a50b9c566be47bd697e1969fa53ebf76d2d981b", "5c3d6737c7a73e0d90eac498c6b9e46cf6b0c990",
        "aecae108408040ed3195d4d750b580d510153de4c8d607c3ca99377636e5e4de", 21562),
    "rv64gc-priv-modes-v2": RetainedCapture(
        "8a50b9c566be47bd697e1969fa53ebf76d2d981b", "5c3d6737c7a73e0d90eac498c6b9e46cf6b0c990",
        "15124b424ed49fdacfc748629e7665ca7ba0a90fb608a99f9a7f71fcd52816ef", 13782),
    "rv64gc-sv39-v2": RetainedCapture(
        "8a50b9c566be47bd697e1969fa53ebf76d2d981b", "5c3d6737c7a73e0d90eac498c6b9e46cf6b0c990",
        "3c5af9c7342009982281ba14d390d869d0958f3d4d234c4bbb8a01e9519deec5", 12765),
    "rv64gc-reservation-v2": RetainedCapture(
        "8a50b9c566be47bd697e1969fa53ebf76d2d981b", "5c3d6737c7a73e0d90eac498c6b9e46cf6b0c990",
        "c9dbddc6124655f8927e02401cc3566b190be2c3c282a273217986ed26a0231a", 17095),
    "rv64gc-sc-deterministic-v2": RetainedCapture(
        "8a50b9c566be47bd697e1969fa53ebf76d2d981b", "5c3d6737c7a73e0d90eac498c6b9e46cf6b0c990",
        "d6c766154741e1d3e8554cd6fe97a41266592febd38f39b540bc50a069cb04ad", 16274),
    "rv64gc-composition-v2": RetainedCapture(
        "8a50b9c566be47bd697e1969fa53ebf76d2d981b", "5c3d6737c7a73e0d90eac498c6b9e46cf6b0c990",
        "233bc67654d05ef146e9e89a5642bffda939097878d141876783919852c526db", 12769),
    "rv64gc-ext-closure-v2": RetainedCapture(
        "8a50b9c566be47bd697e1969fa53ebf76d2d981b", "5c3d6737c7a73e0d90eac498c6b9e46cf6b0c990",
        "9f71e6d66da8a42bedeadc45c402bc77ebe89a028baca4b136ed18b28c943581", 12981),
    "rv64gc-priv-revision-v2": RetainedCapture(
        "8a50b9c566be47bd697e1969fa53ebf76d2d981b", "5c3d6737c7a73e0d90eac498c6b9e46cf6b0c990",
        "5f570088a6c09d9eded006cff9a0367dfa4d666753ad4ee5ef4d1abcc670c6af", 11259),
    "rv64gc-rvwmo-v2": RetainedCapture(
        "8a50b9c566be47bd697e1969fa53ebf76d2d981b", "5c3d6737c7a73e0d90eac498c6b9e46cf6b0c990",
        "378f005f10b3827eb3128412bf121146d7d818199ff822408422f4f3b5618b7b", 12483),
    "rv64gc-priv-insns-v2": RetainedCapture(
        "8a50b9c566be47bd697e1969fa53ebf76d2d981b", "5c3d6737c7a73e0d90eac498c6b9e46cf6b0c990",
        "bc087b47c470b7fde6d036c35a227e7702646e5c97007a2e1b07aa115377a1ed", 10682),
    "rv64gc-priv-forms-v2": RetainedCapture(
        "8a50b9c566be47bd697e1969fa53ebf76d2d981b", "5c3d6737c7a73e0d90eac498c6b9e46cf6b0c990",
        "608138ee4f98bbddc81c74cb93482df6d85940b897f0bc3103ca595e417a85f0", 16584),
    "rv64gc-no-h-v2": RetainedCapture(
        "8a50b9c566be47bd697e1969fa53ebf76d2d981b", "5c3d6737c7a73e0d90eac498c6b9e46cf6b0c990",
        "7202b4c37608c2cbcf5e1af7e39bfd78c45c9daecffdbac47953ea75a321af75", 10785),
    "rv64gc-no-pmp-v2": RetainedCapture(
        "8a50b9c566be47bd697e1969fa53ebf76d2d981b", "5c3d6737c7a73e0d90eac498c6b9e46cf6b0c990",
        "8dd1e14aaddeeba54094865364c95ac0e5f709e92b701907f13fdab0e0becc7e", 10960),
    "rv64gc-endian-v2": RetainedCapture(
        "8a50b9c566be47bd697e1969fa53ebf76d2d981b", "5c3d6737c7a73e0d90eac498c6b9e46cf6b0c990",
        "51303f300c828641c98141034ad988f1ee733bb36ec1f8d7cfb8ea204abd266b", 11568),
    "rv64gc-fence-v2": RetainedCapture(
        "8a50b9c566be47bd697e1969fa53ebf76d2d981b", "5c3d6737c7a73e0d90eac498c6b9e46cf6b0c990",
        "c939dd61df925be149005aaef221d56f6367c2e7e219ebf4a9e76a4266ac9f44", 12448),
    "rv64gc-walk-implicit-v2": RetainedCapture(
        "8a50b9c566be47bd697e1969fa53ebf76d2d981b", "5c3d6737c7a73e0d90eac498c6b9e46cf6b0c990",
        "329500f52b140f48f1fb325c5d7e237ad915714e01cc65050bc85c9ea66f80ca", 11507),
    "rv64gc-partial-progress-v2": RetainedCapture(
        "8a50b9c566be47bd697e1969fa53ebf76d2d981b", "5c3d6737c7a73e0d90eac498c6b9e46cf6b0c990",
        "5feed26872e23f5c0ca61f9581eb8c27ce5b586fa67c414bd8315307f90f352c", 15978),
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
