#!/usr/bin/env python3
"""The supported cleanup act: a fresh host census, then the guarded core, then the receipt.

This is the only command line that deletes caches. It adds nothing to the core's
guards; it binds the public handoff census immediately before them.
"""
from __future__ import annotations

import argparse
from dataclasses import asdict, dataclass
import json
import os
from pathlib import Path
import signal
import subprocess
import sys

import artifact_cleanup as A
import artifact_cleanup_guarded as G
import artifact_cleanup_journal as J
import artifact_cleanup_selection as S

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parent.parent
OBJECT = "scripts/artifact_cleanup_operator.py"
CENSUS = "scripts/check_no_background_jobs.sh"
CENSUS_TIMEOUT = 60
CENSUS_BYTES = 1024 * 1024
VERDICT = "handoff: OK"

USAGE = """# ANCHOR: usage
### The supported cleanup act

Cleanup is four explicit acts in one fresh work directory, each leaving a
record the next can be judged against:

```sh
python3 -B scripts/artifact_cleanup.py --plan --workdir target/artifact-cleanup/NEW
python3 -B scripts/artifact_cleanup_selection.py --select --workdir target/artifact-cleanup/NEW
python3 -B scripts/artifact_cleanup_operator.py --delete --workdir target/artifact-cleanup/NEW
python3 -B scripts/artifact_cleanup_operator.py --inspect --workdir target/artifact-cleanup/NEW
```

`--delete` first runs the public handoff census (`scripts/check_no_background_jobs.sh`)
as a bounded child of this repository: same user, same sanctioned exemptions,
same observation limits, a one-minute deadline and a1MiB output bound. It
proceeds only on exit0 with the `handoff: OK` verdict line; exit1 (project
work running) refuses, and exit2, a timeout, empty or oversized output or a
missing verdict refuse as unavailable, because an absent snapshot is not an
empty process set. The caller must be quiescent: the census excludes only its
own ancestry, so a plan, selection or build still running elsewhere refuses.
Then the guarded core re-decides the selection, journals every intent and
return, revalidates each file immediately before its unlink and verifies the
after-state. The receipt is one JSON line: disposition, stage, approved and
removed counts/bytes, residue, failure and the journal path. Exit0 means
complete or nothing approved; 1 a stale plan or a failed/partial attempt; 2 a
refusal; 130 an interruption that was journaled.

`--inspect` reads the plan, the selection and any attempt journal in the work
directory and reports them without a census or any mutation.

Recovery: a `failed` or `interrupted` receipt names its stage; the files whose
returns the journal recorded are gone, every other file kept its bytes, and the
work directory keeps plan, selection and journal as evidence. Do not reuse it:
plan and select into a new directory and run the act again. A refusal before
the journal opened changed nothing. Keep run logs inside the work directory;
a growing log elsewhere under `target/` makes the next plan stale.

The host census stays outside the doctrine gates; only this act binds it.
Owned fixtures exercise green, running, unavailable, malformed and interrupted
censuses and partial attempts without any real cleanup event:

```sh
python3 -B scripts/probe_artifact_cleanup_operator.py
```
# ANCHOR_END: usage
"""


def need(condition, reason, disposition="refused"):
    A.need(condition, "operator: " + reason, disposition)


def bound_root(root: Path) -> Path:
    need(ROOT == A.ROOT == G.ROOT == S.ROOT == J.ROOT, "operator/core roots differ")
    return A.runtime_root(root)


@dataclass(frozen=True)
class Census:
    returncode: int
    verdict: str


def census(root: Path) -> Census:
    """Run the public handoff census as a bounded child; refuse anything but a green verdict."""
    root = bound_root(root)
    script = root / CENSUS
    need(script.is_file() and not script.is_symlink(), "host census script unavailable")
    env = {name: value for name, value in os.environ.items() if not name.startswith("GIT_")}
    env.update(PYTHONDONTWRITEBYTECODE="1", TMPDIR=str(root / "target/tmp"))
    try:
        child = subprocess.Popen(["bash", str(script)], cwd=root, env=env, stdin=subprocess.DEVNULL,
                                 stdout=subprocess.PIPE, stderr=subprocess.PIPE, start_new_session=True)
    except OSError as error:
        raise A.CleanupError("unavailable", "operator: host census could not start: " + type(error).__name__) from error
    with child:
        try:
            out, err = child.communicate(timeout=CENSUS_TIMEOUT)
        except subprocess.TimeoutExpired as error:
            try:
                os.killpg(child.pid, signal.SIGKILL)
            except ProcessLookupError:
                pass
            child.wait()
            raise A.CleanupError("unavailable", "operator: host census timed out") from error
    need(len(out) <= CENSUS_BYTES and len(err) <= CENSUS_BYTES, "host census output exceeds bound", "unavailable")
    text = out.decode("utf-8", errors="replace")
    first = text.splitlines()[0].strip() if text.strip() else ""
    need(child.returncode in {0, 1}, "host census unavailable: exit " + str(child.returncode)
         + (" " + err.decode("utf-8", errors="replace").strip()[:200] if err.strip() else ""), "unavailable")
    need(child.returncode == 0, "project work is running: " + first[:200])
    need(first.startswith(VERDICT), "host census gave no green verdict: " + first[:200], "unavailable")
    return Census(child.returncode, first)


def delete(root: Path, workdir: str) -> tuple[Census, G.Outcome]:
    """The act: a fresh green census immediately before the guarded core."""
    root = bound_root(root)
    A._selection(workdir, A.DEFAULT_SCOPES)
    verdict = census(root)
    outcome = G.remove(root, workdir, actor_object=OBJECT)
    return verdict, outcome


def inspect(root: Path, workdir: str) -> dict:
    root = bound_root(root)
    plan, selection, current = S.inspect(root, workdir)
    report = dict(plan=dict(created_utc=plan.created_utc, candidates=len(plan.candidates),
                            candidate_bytes=sum(item.byte_size for item in plan.candidates),
                            retained=len(plan.retained), excluded=len(plan.excluded)),
                  selection=S.summary(selection, sources_current=current), journal=None)
    try:
        attempt, finding = J.inspect(root, workdir)
    except FileNotFoundError:
        pass  # no attempt was ever opened in this work directory
    else:
        report["journal"] = J.report(attempt, finding)
    return report


def receipt(verdict: Census, outcome: G.Outcome) -> dict:
    row = asdict(outcome)
    row["failure"] = None if outcome.failure is None else asdict(outcome.failure)
    return dict(disposition=outcome.disposition, census=verdict.verdict, **{k: v for k, v in row.items() if k != "disposition"},
                claim_scope="immediate measured act under a fresh census; later builds may regenerate caches")


def main():
    parser = argparse.ArgumentParser(description="\n".join(USAGE.splitlines()[1:-1]),
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--delete", action="store_true")
    mode.add_argument("--inspect", action="store_true")
    parser.add_argument("--workdir", required=True)
    args = parser.parse_args()
    try:
        if args.delete:
            verdict, outcome = delete(ROOT, args.workdir)
            report = receipt(verdict, outcome)
            code = 0 if outcome.disposition in {"complete", "nothing"} else 1
        else:
            report = dict(disposition="inspected", **inspect(ROOT, args.workdir),
                          claim_scope="recorded plan/selection/journal only; no census, no mutation")
            code = 0
    except KeyboardInterrupt:
        report = dict(disposition="interrupted", reason="the attempt was interrupted; its journal records the stage",
                      journal=args.workdir + "/" + J.NAME)
        code = 130
    except A.CleanupError as error:
        report = dict(disposition=error.disposition, reason=error.reason)
        code = 1 if error.disposition == "stale" else 2
    except A.Boundary as error:
        report, code = dict(disposition="refused", reason="unsafe source boundary: " + error.reason), 2
    except (UnicodeError, ValueError, RecursionError) as error:
        report, code = dict(disposition="refused", reason="invalid input: " + str(error)), 2
    except OSError as error:
        report, code = dict(disposition="unavailable", reason="filesystem/Git operation: " + type(error).__name__), 2
    print(json.dumps(report, sort_keys=True))
    return code


if __name__ == "__main__":
    sys.exit(main())
