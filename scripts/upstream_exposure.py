#!/usr/bin/env python3
"""upstream_exposure.py — age and exposure of the tracked upstream issues, DERIVED
(`UPSTREAM-TRACK.3`).

From each issue record's dated history (`docs/upstream/*/*/issue.sexp` — the one owner of
each issue's state, per `UPSTREAM-TRACK.1`), derive: how long the issue has been reported
(the earliest dated event → TODAY, computed at run time — a tracked document carrying the
figure would be a hand-kept date, which LIVE-DOC-CURRENCY refuses) and which of our leaves
it blocks (the record's `blocks` field, whose entries the `UPSTREAM-INDEX` gate requires
to name real leaves).

"Open" is the declared state vocabulary's unresolved half: draft, reported, acknowledged,
disputed, fixed-upstream. `verified` / `closed` / `wontfix` are resolved — a fix we
re-ran, or a question settled. An issue whose exposure matters is an OPEN one: a verified
fix's residue is classified in its subtree, not counted here.

The figure is printed, never stored: this command IS the deliverable. The one number a
tracked document may state (the open-issue count in MEMORY.md) is re-derived at gate time
by DERIVED-COUNTS through `--open-count`.

usage: upstream_exposure.py [--open-count] [--self-test] [root]
"""

from __future__ import annotations

import subprocess
import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import sexp as S                                # noqa: E402

REPO = Path(subprocess.run(["git", "rev-parse", "--show-toplevel"],
                           capture_output=True, text=True, check=True).stdout.strip())
OPEN_STATES = ("draft", "reported", "acknowledged", "disputed", "fixed-upstream")


def scan(root: Path) -> list[dict]:
    """Every issue record as derived facts: id, project, state, age, blocks."""
    out = []
    up = root / "docs" / "upstream"
    for d in sorted(p for p in up.glob("*/*") if p.is_dir()) if up.is_dir() else []:
        rec = d / "issue.sexp"
        if not rec.is_file():
            continue
        form = S.read_file(rec)[0]
        if S.head(form, str(rec)) != "issue":
            continue
        events = [e for c in S.children(form, "history") for e in S.children(c, "event")]
        dates = [str(S.field(e, "date", str(rec))) for e in events]
        earliest = min(dates) if dates else None
        age = (date.today() - date.fromisoformat(earliest)).days if earliest else None
        out.append({
            "id": str(S.field(form, "id", str(rec))),
            "project": str(S.field(form, "project", str(rec))),
            "state": str(S.field(form, "state", str(rec))),
            "blocks": str(S.field(form, "blocks", str(rec))).strip(),
            "age_days": age,
            "since": earliest,
        })
    return out


def render(issues: list[dict]) -> str:
    lines = []
    open_issues = [i for i in issues if i["state"] in OPEN_STATES]
    resolved = [i for i in issues if i["state"] not in OPEN_STATES]
    lines.append("upstream exposure — derived from the dated issue records, never typed")
    if open_issues:
        for i in open_issues:
            blocks = i["blocks"] or "(blocks nothing recorded)"
            lines.append(f"  OPEN     {i['id']:8} {i['project']:12} state {i['state']:14} "
                         f"reported {i['since']} ({i['age_days']}d ago)  blocks: {blocks}")
    else:
        lines.append("  no open issues — nothing upstream blocks any leaf today")
    for i in resolved:
        lines.append(f"  resolved {i['id']:8} {i['project']:12} state {i['state']:14} "
                     f"reported {i['since']} ({i['age_days']}d ago)")
    lines.append(f"upstream exposure: {len(open_issues)} open / {len(resolved)} resolved "
                 f"/ {len(issues)} tracked")
    return "\n".join(lines)


def _selftest() -> int:
    import tempfile
    passed = failed = 0

    def arm(label: str, fn) -> None:
        nonlocal passed, failed
        try:
            fn()
        except AssertionError as exc:
            print(f"  FAIL  {label}: {exc}"); failed += 1
        else:
            print(f"  ok    {label}"); passed += 1

    REC = ('(issue (id "{id}") (project "p") (title "t") (component "c") '
           '(severity medium) (state {state}) (blocks "{blocks}") '
           '(history (event (date "{date}") (state draft))))')

    def write(root: Path, id_: str, state: str, blocks: str, date_: str) -> None:
        d = root / "docs" / "upstream" / "p" / f"{id_}-x"
        d.mkdir(parents=True)
        (d / "issue.sexp").write_text(REC.format(id=id_, state=state, blocks=blocks,
                                                 date=date_))

    def eq(x, y):
        assert x == y, f"got {x!r}, want {y!r}"

    with tempfile.TemporaryDirectory(dir=REPO / "target") as t:
        root = Path(t)
        write(root, "LS-001", "reported", "SOT-FORMAT.9", "2026-09-20")
        write(root, "LS-002", "verified", "", "2026-09-21")
        issues = scan(root)
        arm("GREEN the dated history derives the age, never a stored figure",
            lambda: eq(issues[0]["age_days"],
                       (date.today() - date(2026, 9, 20)).days))
        arm("GREEN open states classify: reported is open, verified is resolved",
            lambda: eq([i["id"] for i in issues if i["state"] in OPEN_STATES],
                       ["LS-001"]))
        arm("GREEN the exposure is the record's blocks field, verbatim",
            lambda: eq((issues[0]["blocks"], issues[1]["blocks"]),
                       ("SOT-FORMAT.9", "")))
        rendered = render(issues)
        arm("GREEN the report counts open vs resolved and names the blocker",
            lambda: (eq("1 open / 1 resolved / 2 tracked" in rendered, True),
                     eq("SOT-FORMAT.9" in rendered, True))[0])
        (root / "docs/upstream/p/LS-001-x/issue.sexp").write_text(
            REC.format(id="LS-001", state="verified", blocks="", date="2026-09-20"))
        arm("GREEN a fully resolved tracker reports an honest zero",
            lambda: eq("no open issues" in render(scan(root)), True))

    print(f"upstream_exposure --self-test: {passed} pass / {failed} fail")
    return 1 if failed else 0


def main(argv: list[str]) -> int:
    args = argv[1:]
    if "--self-test" in args:
        return _selftest()
    root = REPO
    if args and not args[-1].startswith("--"):
        root = Path(args[-1])
    issues = scan(root)
    if "--open-count" in args:
        print(sum(1 for i in issues if i["state"] in OPEN_STATES))
        return 0
    if not issues:
        print("upstream_exposure: no issue records found under docs/upstream/ — "
              "nothing to derive from", file=sys.stderr)
        return 2
    print(render(issues))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
