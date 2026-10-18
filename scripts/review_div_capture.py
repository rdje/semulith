#!/usr/bin/env python3
"""Review the proposed first DIV capture's producers and exercised data loaders.

This read-only diagnostic has an explicit source-reviewed population. It does not
produce a manifest, run Sail, prove arbitrary Python dependency completeness or
qualify evidence. A source edit still needs review even with identical imports.
"""

from __future__ import annotations

import argparse
import ast
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import platform
import stat
import sys
from unittest.mock import patch

ROOT = Path(__file__).resolve().parent.parent
FILE_BYTES = 1024 * 1024
TOTAL_BYTES = 8 * 1024 * 1024
MODULE_LIMIT = 64
ROOT_MODULES = frozenset(
    {
        "matched_gpr_unit_collector",
        "matched_gpr_evaluation",
        "derive_rv64gc_expectations",
        "retain_div_statement",
    }
)
REVIEWED_MODULES = frozenset(
    """change_impact check_sexp_schema compare_traces derive_rv64gc_expectations
    dossier_sexp expectations_text experiment_artifacts experiment_verification
    gate_report matched_gpr_artifacts matched_gpr_collector matched_gpr_comparison
    matched_gpr_evaluation matched_gpr_execution matched_gpr_expected_author
    matched_gpr_files matched_gpr_identity matched_gpr_image matched_gpr_impact
    matched_gpr_input_review matched_gpr_leaf matched_gpr_manifest
    matched_gpr_property matched_gpr_receipt matched_gpr_relations
    matched_gpr_source_image matched_gpr_unit_collector record_catalog records_sexp
    retain_div_statement riscv_asm run_rv64gc_sail sexp spec_c specfp""".split()
)
REVIEWED_EXTERNALS = frozenset(
    """__future__ argparse collections contextlib copy csv dataclasses decimal errno
    fractions functools hashlib itertools json math os pathlib platform re shutil
    signal stat struct subprocess sys tempfile tomllib""".split()
)
FRAGMENTS = ("a", "c", "d", "f", "m", "rv64i", "system", "zicntr", "zicsr", "zifencei")
DATA_PATHS = frozenset(
    [
        f"definitions/riscv/{name}{suffix}.sexp"
        for name in FRAGMENTS
        for suffix in ("", ".sem")
    ]
    + [
        f"profiles/rv64gc-lab-v0/{name}.sexp"
        for name in ("encoding", "profile", "state")
    ]
    + [
        f"schema/{name}.sexp"
        for name in (
            "expectations",
            "matched-gpr-dependencies",
            "references",
            "sail-gpr-capture",
        )
    ]
)
GUEST = "profiles/rv64gc-lab-v0/guests/m-div.s"
PRIMARY = "profiles/rv64gc-lab-v0/retained/div-statement.html"
POLICY = "profiles/rv64gc-lab-v0/EVIDENCE_POLICY.md"
SELF = "scripts/review_div_capture.py"
PRINCIPAL_CODE = frozenset(
    {"scripts/matched_gpr_unit_collector.py", "scripts/run_rv64gc_sail.py"}
)


class ReviewError(ValueError):
    """The proposed population or exercised context cannot be confirmed."""


def require(condition, reason):
    if not condition:
        raise ReviewError(reason)


def canonical(path):
    require(type(path) is str and 1 <= len(path) <= 4096, "invalid relative path")
    parts = PurePosixPath(path)
    require(
        not parts.is_absolute()
        and parts.as_posix() == path
        and path != "."
        and ".." not in parts.parts
        and "\\" not in path
        and ":" not in path
        and not any(ord(c) < 32 or 127 <= ord(c) <= 159 for c in path),
        "noncanonical relative path",
    )
    return parts.parts


class Snapshots:
    """Bounded trusted-repository reads; no cross-repository/volume traversal.

    Runtime imports and the exercised schema tools have their own I/O. These
    snapshots bound this diagnostic's direct reads, not Python process memory.
    """

    def __init__(self, root):
        self.root = root.resolve(strict=True)
        self.device = self.root.stat().st_dev
        self.data = {}
        self.total = 0

    def read(self, relative):
        parts = canonical(relative)
        path = self.root
        for index, part in enumerate(parts):
            path /= part
            info = path.lstat()
            require(not stat.S_ISLNK(info.st_mode), "symlink in reviewed path")
            require(info.st_dev == self.device, "reviewed path crosses a volume")
            if index < len(parts) - 1:
                require(
                    stat.S_ISDIR(info.st_mode), "reviewed parent is not a directory"
                )
                require(
                    not os.path.lexists(path / ".git"),
                    "reviewed path crosses a Git boundary",
                )
        require(stat.S_ISREG(info.st_mode), "reviewed input is not a regular file")
        require(
            0 <= info.st_size <= FILE_BYTES, "reviewed input exceeds per-file bound"
        )
        require(
            self.total + info.st_size <= TOTAL_BYTES, "review exceeds aggregate bound"
        )
        with path.open("rb") as stream:
            opened = os.fstat(stream.fileno())
            require(
                (opened.st_dev, opened.st_ino) == (info.st_dev, info.st_ino),
                "input replaced",
            )
            payload = stream.read(info.st_size)
            after = os.fstat(stream.fileno())
        end = path.lstat()

        def signature(item):
            return (
                item.st_dev,
                item.st_ino,
                item.st_size,
                item.st_mtime_ns,
                item.st_ctime_ns,
            )

        require(
            signature(info) == signature(after) == signature(end),
            "input changed during review",
        )
        require(len(payload) == info.st_size, "reviewed input size changed")
        self.total += len(payload)
        return payload

    def pin(self, relative):
        if relative not in self.data:
            self.data[relative] = self.read(relative)
        return self.data[relative]

    def recheck(self):
        # A second independent allowance; total direct reads are at most16 MiB.
        self.total = 0
        for path, data in sorted(self.data.items()):
            require(self.read(path) == data, "reviewed bytes changed: " + path)


def import_census(snapshots, *, roots=ROOT_MODULES, reviewed=REVIEWED_MODULES):
    pending = list(sorted(roots))
    seen, edges, external = set(), set(), set()
    while pending:
        name = pending.pop()
        if name in seen:
            continue
        require(len(seen) < MODULE_LIMIT, "module population exceeds bound")
        require(name.isidentifier(), "invalid project module name")
        seen.add(name)
        path = f"scripts/{name}.py"
        tree = ast.parse(snapshots.pin(path), filename=path)
        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom):
                require(
                    node.level == 0 and node.module is not None,
                    "relative import needs review",
                )
                imports = [node.module]
            elif isinstance(node, ast.Import):
                imports = [alias.name for alias in node.names]
            else:
                imports = []
            if isinstance(node, ast.Call):
                called = (
                    node.func.id
                    if isinstance(node.func, ast.Name)
                    else getattr(node.func, "attr", "")
                )
                require(
                    called
                    not in {"__import__", "import_module", "spec_from_file_location"},
                    "dynamic import needs review",
                )
            for imported in imports:
                base = imported.split(".")[0]
                if (snapshots.root / "scripts" / (base + ".py")).exists():
                    require(imported == base, "project package import needs review")
                    edges.add((name, base))
                    pending.append(base)
                else:
                    require(
                        not os.path.lexists(snapshots.root / "scripts" / base),
                        "project package import needs review",
                    )
                    require(
                        base in REVIEWED_EXTERNALS,
                        "unreviewed external import: " + base,
                    )
                    external.add(base)
    require(
        seen == set(reviewed), "project module population differs from reviewed set"
    )
    return tuple(sorted(seen)), tuple(sorted(edges)), tuple(sorted(external))


def check_data_population(observed):
    require(
        set(observed) == DATA_PATHS,
        "exercised data population differs from reviewed set",
    )


def child_paths(modules):
    paths = (
        ({f"scripts/{name}.py" for name in modules} - PRINCIPAL_CODE)
        | DATA_PATHS
        | {PRIMARY, POLICY, SELF}
    )
    require(len(paths) <= 64, "proposed manifest exceeds64 children")
    return tuple(sorted(paths))


def exercise_loaders(source, snapshots):
    # Imports are ordinary, explicit and already covered by the producer census.
    import sexp as S
    import matched_gpr_image as G
    import derive_rv64gc_expectations as Author
    import matched_gpr_artifacts as F
    import matched_gpr_comparison as C
    import matched_gpr_identity as I
    import experiment_verification as V

    observed = []
    original = S.read_file

    def read(path):
        relative = Path(path).relative_to(snapshots.root).as_posix()
        # Reject an unreviewed read BEFORE delegating to the real loader.
        require(relative in DATA_PATHS, "unreviewed data read: " + relative)
        snapshots.pin(relative)
        observed.append(relative)
        return original(path)

    for loader in (F._schema, C._schema, I._schema, V._schema):
        loader.cache_clear()
    with patch.object(S, "read_file", read):
        image = G.build_guest_image(source, program="m-div.s", entry=0x80000000)
        derived = Author.derive_snapshot(source, program="m-div.s", instructions=27)
        F._schema("capture")
        F._schema("dependencies")
        C._schema()
        I._schema()
        V._schema()
    check_data_population(observed)
    require(
        image.payload_sha256 == derived.payload_sha256, "image/author payload differs"
    )
    require(
        image.payload_size == derived.payload_size, "image/author payload size differs"
    )
    require(len(derived.steps) == 27, "author boundary budget differs")
    require(
        derived.steps[2].writes == ((7, (1 << 64) - 3),), "signed DIV witness differs"
    )
    return {
        "data_paths": sorted(set(observed)),
        "read_calls": len(observed),
        "image_bytes": image.image_size,
        "image_sha256": image.image_sha256,
        "payload_bytes": image.payload_size,
        "payload_sha256": image.payload_sha256,
        "boundaries": len(derived.steps),
    }


def check_retained_input(case, data):
    """Bind the curated bytes and their distinct original publication identity."""
    import retain_div_statement as Retain

    require(len(case.required_inputs) == 1, "normative source population changed")
    primary = case.required_inputs[0]
    require(
        (primary.role, primary.input_id, primary.path, primary.sha256)
        == ("normative-source", "RVI-M-DIV-STATEMENT", PRIMARY, Retain.RETAINED_SHA),
        "retained source identity changed",
    )
    require(
        case.authority.source_id == "RVI-M"
        and case.authority.source_sha256 == Retain.SOURCE_SHA,
        "original publication authority changed",
    )
    require(
        hashlib.sha256(data).hexdigest() == primary.sha256,
        "retained source pin differs",
    )


def review():
    snapshots = Snapshots(ROOT)
    modules, edges, external = import_census(snapshots)
    children = child_paths(modules)
    for path in (*children, GUEST):
        snapshots.pin(path)
    import matched_gpr_property as P

    case = P.signed_division_case()
    require(
        hashlib.sha256(snapshots.data[GUEST]).hexdigest() == P._SOURCE_SHA,
        "guest differs from reviewed case",
    )
    check_retained_input(case, snapshots.data[PRIMARY])
    exercised = exercise_loaders(snapshots.data[GUEST], snapshots)
    snapshots.recheck()
    files = [
        {"path": path, "bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()}
        for path, data in sorted(snapshots.data.items())
    ]
    return {
        "disposition": "pending",
        "canonical_capture": False,
        "qualification": False,
        "case_id": case.case_id,
        "module_roots": sorted(ROOT_MODULES),
        "modules": list(modules),
        "import_edges": edges,
        "external_imports": external,
        "exercised": exercised,
        "proposed_children": children,
        "counts": {
            "modules": len(modules),
            "data_files": len(DATA_PATHS),
            "children": len(children),
            "child_limit": 64,
            "reviewed_files": len(files),
            "reviewed_bytes": sum(row["bytes"] for row in files),
        },
        "files": files,
        "runtime": {
            "python": platform.python_version(),
            "implementation": platform.python_implementation(),
            "os": platform.system(),
            "kernel": platform.release(),
            "arch": platform.machine(),
        },
        "limits": {
            "file_bytes": FILE_BYTES,
            "per_pass_bytes": TOTAL_BYTES,
            "passes": 2,
        },
        "limitations": [
            "source review still required after code edits",
            "loader trace covers only declared route",
            "current semantic authorities selected separately",
            "retention and canonical entrypoint pending",
        ],
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--review", action="store_true", required=True)
    parser.parse_args()
    try:
        result = review()
    except OSError as exc:
        reason = str(exc).replace(str(ROOT) + os.sep, "")
        print(json.dumps({"disposition": "unavailable", "reason": reason}))
        return 2
    except (ReviewError, ValueError, SyntaxError, RuntimeError) as exc:
        print(json.dumps({"disposition": "refused", "reason": str(exc)}))
        return 1
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
