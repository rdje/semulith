#!/usr/bin/env python3
"""Credited dispositions: the catalogue `profiles/<profile>/credits.sexp`, read and authenticated.

EVIDENCE_POLICY.md ("Records, controls and currentness") makes a credited disposition a structured
record linking the requirement, the effective obligation, the owner, the tracked runner and the
evidence record. This module reads those records and says, for each, whether it is `current` — every
pin it carries (the measured record, the receipt, the policy document, every input of the case's
dependency manifest) still describes the tree and the receipt is a complete, uncredited capture — or
`lapsed`, naming the first reason. It grants nothing: `scripts/requirement_status.py` credits a case
only through a current record here, and `scripts/review_div_policy.py` reports `credited` from it.

P4-SYSTEM.14 a42ay. Read-only; no Git; no process.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
import check_sexp_schema as K  # noqa: E402  (pinned by the finite cases; read, never changed)
import record_catalog as C  # noqa: E402
import sexp as S  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
CATALOGUE = "credits.sexp"
SCHEMA = "schema/credits.sexp"
MAX_CREDITS = 64
DOCUMENT_BYTES = 65536
PIN_BYTES = 16 * 1024 * 1024
PINS = ("measured", "receipt", "policy")


class CreditRefused(Exception):
    """Unreadable, oversized or malformed credit input — a refusal, never a disposition."""


def _require(condition, reason: str) -> None:
    if not condition:
        raise CreditRefused(reason)


def _one(form, name):
    found = S.children(form, name)
    _require(len(found) <= 1, f"duplicate field {name}")
    return found[0][1] if found and len(found[0]) == 2 else None


def _strings(form, name) -> list[str]:
    return [str(c[1]) for c in S.children(form, name) if len(c) == 2]


def _pin(form, name) -> dict:
    pins = S.children(form, name)
    _require(len(pins) == 1 and len(pins[0]) == 2, f"credit needs exactly one {name} pin")
    pin = pins[0][1]
    return dict(path=str(_one(pin, "path")), sha256=str(_one(pin, "sha256")), byte_size=int(_one(pin, "byte_size")))


def credit_to_dict(form) -> dict:
    return dict(id=str(_one(form, "id")), profile_ids=_strings(form, "profile_ids"),
                requirement_id=str(_one(form, "requirement_id")), obligation_ids=_strings(form, "obligation_ids"),
                case_id=str(_one(form, "case_id")), **{name: _pin(form, name) for name in PINS},
                retained_sources=_strings(form, "retained_sources"), authority=str(_one(form, "authority")),
                date=str(_one(form, "date")), decision=str(_one(form, "decision")), legs=int(_one(form, "legs")),
                limitations=_strings(form, "limitations"))


def load_credits(root: Path, profile_dir: Path) -> list[dict]:
    """The profile's credit records, schema-validated; an absent catalogue is no credits."""
    path = Path(profile_dir) / CATALOGUE
    if not path.exists():
        return []
    _require(path.is_file() and path.stat().st_size <= DOCUMENT_BYTES, f"{path}: not a bounded regular file")
    schema = Path(root) / SCHEMA
    _require(schema.is_file(), f"{SCHEMA} is missing")
    try:
        constructs, operators = K.load_schema(schema)
        text = path.read_text("utf-8")
        errors = K.validate_text(text, constructs, operators, path.as_posix(), parse_where=str(path))
    except (K.SchemaError, S.SexpError, UnicodeError, OSError) as error:
        raise CreditRefused(f"{path}: {error}") from error
    _require(not errors, f"{path}: " + "; ".join(str(e) for e in errors[:3]))
    forms = [f for f in S.parse(text, str(path)) if isinstance(f, list) and f and str(f[0]) == "credit"]
    _require(len(forms) <= MAX_CREDITS, f"{path}: more than {MAX_CREDITS} credits")
    credits = [credit_to_dict(f) for f in forms]
    _require(len({c["id"] for c in credits}) == len(credits), f"{path}: duplicate credit id")
    return credits


def _digest_file(path: Path) -> tuple[str, int]:
    _require(path.is_file() and not path.is_symlink(), f"{path}: not a regular file")
    size = path.stat().st_size
    _require(size <= PIN_BYTES, f"{path}: exceeds the {PIN_BYTES}-byte pin read limit")
    return hashlib.sha256(path.read_bytes()).hexdigest(), size


def authenticate(root: Path, credit: dict) -> dict:
    """`current` when every pin still describes the tree and the receipt is a complete, uncredited
    capture whose declaration binds the credited requirement; otherwise `lapsed`, every reason named."""
    root = Path(root)
    reasons: list[str] = []
    for name in PINS:
        pin = credit[name]
        target = root / pin["path"]
        if not target.is_file():
            reasons.append(f"{name} pin {pin['path']}: missing"); continue
        digest, size = _digest_file(target)
        if (digest, size) != (pin["sha256"], pin["byte_size"]):
            reasons.append(f"{name} pin {pin['path']}: SHA256 or size differs")
    case_dir = root / "evidence" / credit["case_id"]
    receipt_path, planned_path, manifest_path = (case_dir / "verification.json", case_dir / "planned-experiment.sexp",
                                                 case_dir / "dependencies.sexp")
    if credit["receipt"]["path"] != receipt_path.relative_to(root).as_posix():
        reasons.append("receipt pin does not name the case's verification.json")
    if credit["measured"]["path"] != (case_dir / "measured-experiment.sexp").relative_to(root).as_posix():
        reasons.append("measured pin does not name the case's measured-experiment.sexp")
    if receipt_path.is_file():
        try:
            receipt = json.loads(receipt_path.read_bytes()[:DOCUMENT_BYTES].decode("utf-8"))
        except (ValueError, UnicodeError):
            receipt = None
        if not isinstance(receipt, dict):
            reasons.append("receipt is unreadable")
        else:
            if receipt.get("case_id") != credit["case_id"]:
                reasons.append("receipt names another case")
            if receipt.get("complete_canonical_capture") is not True:
                reasons.append("receipt is not a complete canonical capture")
            if receipt.get("qualification") is not False:
                reasons.append("receipt carries a qualification verdict of its own (a typed success word)")
            if receipt.get("profile_id") not in credit["profile_ids"]:
                reasons.append("receipt's profile is not one the credit names")
    else:
        reasons.append("receipt missing")
    if planned_path.is_file():
        forms = S.parse(planned_path.read_bytes()[:DOCUMENT_BYTES].decode("utf-8"), str(planned_path))
        experiments = [f for f in forms if isinstance(f, list) and f and str(f[0]) == "experiment"]
        if len(experiments) != 1:
            reasons.append("planned experiment is not one record")
        else:
            verification = S.children(experiments[0], "verification")
            holder = verification[0] if len(verification) == 1 else experiments[0]
            properties = S.children(holder, "property")
            bound = {str(_one(p, "requirement_id")) for p in properties}
            obligations = {o for p in properties for o in _strings(p, "obligation_ids")}
            if bound != {credit["requirement_id"]}:
                reasons.append(f"declaration binds {sorted(bound)}, not the credited requirement alone")
            if not set(credit["obligation_ids"]) <= obligations:
                reasons.append("declaration does not bind every credited obligation")
    else:
        reasons.append("planned experiment missing")
    if manifest_path.is_file():
        forms = S.parse(manifest_path.read_bytes()[:DOCUMENT_BYTES].decode("utf-8"), str(manifest_path))
        rows = [i for f in forms if isinstance(f, list) and f and str(f[0]) == "dependencies" for i in S.children(f, "input")]
        if not rows:
            reasons.append("dependency manifest pins no input")
        for row in rows:
            path, sha = str(_one(row, "path")), str(_one(row, "sha256"))
            target = root / path
            if not target.is_file():
                reasons.append(f"manifest input {path}: missing"); break
            if _digest_file(target)[0] != sha:
                reasons.append(f"manifest input {path}: SHA256 differs"); break
    else:
        reasons.append("dependency manifest missing")
    return dict(id=credit["id"], case_id=credit["case_id"], requirement_id=credit["requirement_id"],
                obligation_ids=list(credit["obligation_ids"]), disposition="lapsed" if reasons else "current",
                reasons=reasons)


def current_credits(root: Path, profile_dir: Path) -> list[dict]:
    return [dict(credit, **authenticate(root, credit)) for credit in load_credits(root, profile_dir)]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--profile", required=True)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    try:
        table = current_credits(args.root, args.root / "profiles" / args.profile)
    except CreditRefused as error:
        print(f"CREDIT-RECORDS: refused — {error}", file=sys.stderr); return 2
    current = sum(1 for c in table if c["disposition"] == "current")
    if args.json:
        json.dump(table, sys.stdout, indent=1); print()
    print(f"CREDIT-RECORDS: {args.profile}: {len(table)} credit(s), {current} current, {len(table) - current} lapsed; "
          "records read and authenticated, nothing granted")
    return 0 if current == len(table) else 1


if __name__ == "__main__":
    sys.exit(main())
