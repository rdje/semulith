#!/usr/bin/env python3
"""Guarded deletion core: unlink only what plan, strict selection and journal agree on.

This module is the deletion core for the host-bound operator workflow. Its command
line performs no deletion; `remove` is exercised in owned fixtures until .14 binds
the host census around it.
"""
from __future__ import annotations

import argparse
from dataclasses import asdict, dataclass, replace
import hashlib
import json
import os
from pathlib import Path
import sys

import artifact_cleanup as A
import artifact_cleanup_journal as J
import artifact_cleanup_selection as S
import artifact_output_provenance as O

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parent.parent
OBJECT = "scripts/artifact_cleanup_guarded.py"

USAGE = """# ANCHOR: usage
### Guarded deletion core

`remove(root, workdir)` is the only cache-unlink path in the repository. It
binds three published records and refuses when any of them disagrees with the
tree it is about to change:

1. **Whole-cohort preflight.** The strict selection is re-decided now (fresh
   census, current tracked inventory, current ledger and source pins) and must
   equal the saved `selection.json` exactly; a stale plan names its first
   differing member. Nothing approved means nothing is attempted.
2. **Durable attempt.** A version-2 journal begins with the selection digest
   and the approved plan indices; an intent is flushed before every unlink and
   its return recorded after it, so a torn attempt is readable later.
3. **Per-file revalidation immediately before each unlink.** The parent is
   reopened through descriptor traversal (no symlink, foreign-volume or nested
   Git ancestor), the candidate must still be untracked, and its device, inode,
   mode, single link, size, mtime, ctime and digest must equal the plan's
   fact. The unlink uses that directory descriptor, and the file must then be
   absent. Any refusal finishes the journal as `failed` at its stage with the
   count already removed; an interruption finishes it as `interrupted` and
   propagates.
4. **Post-check.** A fresh census must equal the plan minus the approved files:
   unrecorded candidates, retained files and exclusions byte-exact, tracked
   inventory and instrument unchanged. Only then is the attempt `verified`.

```sh
python3 -B scripts/artifact_cleanup_guarded.py --dry-run --workdir target/artifact-cleanup/review
```

`--dry-run` runs the preflight and reports what the saved selection approves,
without opening a journal or touching a file. There is no delete option here:
the supported operator path (`.14`) adds the fresh host census and the explicit
act. Owned on-volume fixtures exercise every stage:

```sh
python3 -B scripts/probe_artifact_cleanup_guarded.py
```
# ANCHOR_END: usage
"""


def need(condition, reason, disposition="refused"):
    A.need(condition, "guarded: " + reason, disposition)


def bound_root(root: Path) -> Path:
    need(ROOT == A.ROOT == O.ROOT == S.ROOT == J.ROOT, "guarded/planner/reader/selector/journal roots differ")
    return A.runtime_root(root)


@dataclass(frozen=True)
class Outcome:
    disposition: str
    stage: str
    approved: int
    approved_bytes: int
    removed: int
    removed_bytes: int
    residue: int
    failure: J.Failure | None
    journal: str | None


def preflight(root: Path, workdir: str):
    """Re-decide the strict partition now and require the saved selection to match it."""
    root = bound_root(root)
    plan, selection, current = S.inspect(root, workdir)
    need(current, "selection sources are no longer current", "stale")
    fresh = S.decide(root, plan)
    need((fresh.approved, fresh.unrecorded, fresh.ledger_sha256)
         == (selection.approved, selection.unrecorded, selection.ledger_sha256),
         "current authority differs from the saved selection", "stale")
    approved = set(selection.approved)
    indices = tuple(index for index, item in enumerate(plan.candidates) if item.path in approved)
    return plan, selection, A.tracked_paths(root), indices


def _identity(fact: A.FileFact):
    return (fact.device, fact.inode, fact.mode, fact.links, fact.byte_size, fact.mtime_ns, fact.ctime_ns)


def postcheck(root: Path, plan: A.Plan, selection: S.Selection) -> str:
    """Name the first way the tree differs from the plan minus the approved files; empty when exact."""
    approved = set(selection.approved)
    expected = replace(plan, candidates=tuple(item for item in plan.candidates if item.path not in approved))
    fresh = A.make_plan(root, workdir=plan.workdir, scopes=plan.scopes, limits=plan.limits)
    return A.difference(expected, fresh)


def remove(root: Path, workdir: str, *, actor_object: str = OBJECT) -> Outcome:
    """Unlink exactly the approved candidates, each revalidated immediately before its unlink."""
    plan, selection, tracked, indices = preflight(root, workdir)
    approved_bytes = selection.approved_bytes
    if not indices:
        return Outcome("nothing", "preflight", 0, 0, 0, 0, 0, None, None)
    tracked_keys = frozenset(A._ownership_key(path) for path in tracked)
    binding = (hashlib.sha256(S.encode(selection)).hexdigest(), indices)
    journal = workdir + "/" + J.NAME
    removed = removed_bytes = 0
    stage = "preflight"

    def outcome(disposition, problem=None, residue=0):
        return Outcome(disposition, stage, len(indices), approved_bytes, removed, removed_bytes, residue, problem, journal)

    with J.start(root, workdir, actor_object=actor_object, selection=binding) as writer:
        try:
            with A.OwnedRoot(root) as owned:
                for index in indices:
                    fact = plan.candidates[index]
                    parent, leaf = fact.path.rsplit("/", 1)
                    stage = "revalidate"
                    try:
                        with owned.directory(parent) as directory:
                            need(A._ownership_key(fact.path) not in tracked_keys, "candidate became tracked")
                            current, _ = owned.snapshot(directory, leaf, fact.path, fact.byte_size, expected=_identity(fact))
                            need(current == fact and fact.links == 1, "file identity or digest differs before unlink")
                            writer.intent(index)
                            stage = "unlink"
                            try:
                                os.unlink(leaf, dir_fd=directory)
                            except OSError as error:
                                problem = J.Failure(type(error).__name__, error.errno, str(error)[:2000])
                                writer.finish("failed", stage, problem)
                                return outcome("failed", problem)
                            writer.removed(index)
                            try:
                                os.stat(leaf, dir_fd=directory, follow_symlinks=False)
                            except FileNotFoundError:
                                pass
                            else:
                                problem = J.Failure("residue", None, fact.path)
                                writer.finish("failed", stage, problem)
                                return outcome("failed", problem, residue=1)
                            removed += 1
                            removed_bytes += fact.byte_size
                    except (A.CleanupError, A.Boundary) as error:
                        if stage != "revalidate":
                            raise
                        problem = J.Failure(type(error).__name__, None, getattr(error, "reason", str(error))[:2000])
                        writer.finish("failed", stage, problem)
                        return outcome("failed", problem)
            stage = "postcheck"
            detail = postcheck(root, plan, selection)
            if detail:
                problem = J.Failure("postcheck", None, detail[:2000])
                writer.finish("failed", stage, problem)
                return outcome("failed", problem)
            stage = "verified"
            writer.finish("complete", stage)
            return outcome("complete")
        except BaseException as error:
            try:
                writer.finish("interrupted", stage if stage in J.STAGES else "interrupt",
                              J.Failure(type(error).__name__, getattr(error, "errno", None), str(error)[:2000]))
            except Exception:
                pass  # a poisoned writer keeps its bytes; the interruption itself propagates
            raise


def main():
    parser = argparse.ArgumentParser(description="\n".join(USAGE.splitlines()[1:-1]),
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--dry-run", action="store_true", required=True)
    parser.add_argument("--workdir", required=True)
    args = parser.parse_args()
    try:
        plan, selection, _, indices = preflight(ROOT, args.workdir)
        report = dict(disposition="ready", approved=len(indices), approved_bytes=selection.approved_bytes,
                      unrecorded=len(selection.unrecorded), candidates=len(plan.candidates),
                      reason="preflight matched the saved selection; no journal opened, no cache deleted")
    except A.CleanupError as error:
        report = dict(disposition=error.disposition, reason=error.reason)
    except A.Boundary as error:
        report = dict(disposition="refused", reason="unsafe source boundary: " + error.reason)
    except (O.ProvenanceError, UnicodeError, ValueError, RecursionError) as error:
        report = dict(disposition="refused", reason="invalid input: " + str(error))
    except OSError as error:
        report = dict(disposition="unavailable", reason="filesystem/Git operation: " + type(error).__name__)
    print(json.dumps(report, sort_keys=True))
    return 0 if report["disposition"] == "ready" else 1 if report["disposition"] == "stale" else 2


if __name__ == "__main__":
    sys.exit(main())
