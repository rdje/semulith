#!/usr/bin/env python3
"""Do this profile's semantic citations RESOLVE in the artifact it pins?

`check_semantics.py` asks whether every rule carries a citation. This asks the next question,
which is a different one: does the citation point at a section that EXISTS in the document the
profile pins? A locator that points nowhere is still a locator — present, well-formed, and worth
nothing to the reviewer who is supposed to check the expression against the sentence.

⛔ WHY THIS TOOL EXISTS. An external investigation reported that no public build of
`riscv/riscv-isa-manual` produces the §1.1 / §3.1 numbering these citations use, and asked for the
exact source. The report was careful and its deduction was right: that numbering is what you get
when "Introduction" is unnumbered front matter rather than Chapter 1. Its conclusion was wrong
only because it searched the wrong publication — this profile pins the **RISC-V Ratified
Specifications Library** at docs.riscv.org, not the GitHub release PDFs, and the library renders
exactly that numbering. 52 of 52 resolved.

The claim held. The gap it exposed was real anyway: **nothing could have settled it mechanically**,
so the question could only be answered by a person going and looking. That is the gap this closes.

⛔ AND IT IS NOT A COMMIT GATE. The pinned artifacts are fetched into an untracked working area,
they need the network, and the rendering declares no redistribution licence (`OQ-4` in the
dossier), so a fresh clone cannot run this. When the evidence is absent this tool REFUSES AND SAYS
HOW TO GET IT. A check that reports success when its evidence is missing is the failure mode it
was built to prevent.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import sexp as _sexp                                                   # noqa: E402
import dossier_sexp as _D                                               # noqa: E402

REPO = Path(__file__).resolve().parent.parent
HEADING = re.compile(r"<h[1-6][^>]*>(.*?)</h[1-6]>", re.S)
NUMBER = re.compile(r"((?:\d+\.)+)\s")
LOCATOR = re.compile(r"([A-Z0-9-]+)\s+§([0-9.]+)")


class CitationError(Exception):
    """A refusal. An unresolvable citation is never reported as a resolved one."""


def headings(html: str) -> set[str]:
    """Every numbered section the document publishes, as bare dotted numbers."""
    out = set()
    for m in HEADING.finditer(html):
        text = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", m.group(1))).strip()
        n = NUMBER.match(text)
        if n:
            out.add(n.group(1).rstrip("."))
    return out


def _rel(p: Path) -> str:
    """Paths this tool PRINTS are repo-root-relative too (Policy 12) — an absolute path in a
    message is one a reader copies into a note, and it stops being true when the repo moves."""
    try:
        return p.resolve().relative_to(REPO).as_posix()
    except ValueError:
        return p.as_posix()


def published(sources_sexp: Path, work_dir: Path) -> dict[str, set[str]]:
    cfg = _D.load_sources(sources_sexp)   # SOT-FORMAT.4: the ledger behind the mapping
    if not work_dir.is_dir():
        raise CitationError(
            f"the pinned artifacts are not present at {_rel(work_dir)}. They are fetched, "
            f"untracked and need the network, so an absent working area is the normal state of a "
            f"fresh clone — not a pass. Fetch them:\n    scripts/fetch_sources.sh")
    out: dict[str, set[str]] = {}
    skipped: list[str] = []
    for s in cfg.get("source", []):
        # P4-SYSTEM.1: a row with http_status 0 is a DECLARED cache/corpus artifact (the
        # ledger's header comment) — a PDF pin for record-level citation, not an HTML
        # page of the snapshot; heading resolution does not apply. Skipped BY NAME,
        # never silently.
        if s.get("http_status") == 0:
            skipped.append(s["id"])
            continue
        p = work_dir / s["file"]
        if not p.exists():
            raise CitationError(f"{s['id']}: {_rel(p)} is missing; run scripts/fetch_sources.sh")
        out[s["id"]] = headings(p.read_text())
    if not out:
        raise CitationError(f"{_rel(sources_sexp)} declares no (source …) form")
    if skipped:
        print(f"           declared non-snapshot pins skipped (http_status 0): "
              f"{', '.join(skipped)}")
    return out


def citations(semantics: Path) -> dict[tuple[str, str], list[str]]:
    form = _sexp.read_file(semantics)[0]
    out: dict[tuple[str, str], list[str]] = {}
    for s in _sexp.children(form, "sem"):
        insn = str(_sexp.field(s, "insn", str(semantics)))
        src = str(_sexp.field(s, "source", str(semantics)))
        m = LOCATOR.match(src)
        if not m:
            raise CitationError(
                f"{semantics.name}: {insn}: the source {src[:60]!r} does not begin with a locator "
                f"of the form '<SOURCE-ID> §<number>'. A citation a tool cannot parse is a "
                f"citation a tool cannot check.")
        out.setdefault((m.group(1), m.group(2).rstrip(".")), []).append(insn)
    if not out:
        raise CitationError(f"{semantics.name}: declares no (sem …) form")
    return out


def check(sources_sexp: Path, work_dir: Path, semantics: Path) -> int:
    have = published(sources_sexp, work_dir)
    want = citations(semantics)
    bad, total = [], 0
    for (sid, num), insns in sorted(want.items()):
        total += len(insns)
        if sid not in have:
            bad.append(f"  §{num} ({len(insns)} instruction(s)) cites source {sid!r}, which "
                       f"{sources_sexp.name} does not pin")
        elif num not in have[sid]:
            near = sorted(n for n in have[sid] if n.startswith(num.split(".")[0]))
            bad.append(f"  {sid} §{num} ({len(insns)} instruction(s), e.g. {insns[0]}) does not "
                       f"exist in the pinned artifact. It publishes: {', '.join(near) or '(none)'}")
        else:
            print(f"  ok    {sid:10} §{num:<9} {len(insns):>3} instruction(s)")
    if bad:
        print("\nUNRESOLVED CITATIONS — each names a section the pinned document does not have:",
              file=sys.stderr)
        for b in bad:
            print(b, file=sys.stderr)
        print("\n⛔ A citation is the link between an expression and the sentence it came from. "
              "If it does not resolve, the evidence argument has a hole in it exactly here.",
              file=sys.stderr)
        return 1
    print(f"\n  {total} of {total} instruction citations resolve in the pinned artifact "
          f"({len(want)} distinct locator(s), {len(have)} pinned source(s))")
    return 0


def _work_dir(cfg: dict) -> tuple[Path, str]:
    """Where the pinned pages are RIGHT NOW, and which route found them.

    The fetched working area is the primary route. ⛔ But it is untracked and needs the network,
    which is what kept this check off the gate list. The materials cache is the second route: the
    same snapshot, verified against a manifest covering all 72 pages, reproducible OFFLINE. Which
    route was used is PRINTED, because a check whose evidence could come from two places and does
    not say which is a check whose result cannot be reproduced.
    """
    wd = REPO / cfg["work_dir"]
    if wd.is_dir():
        return wd, f"fetched working area {cfg['work_dir']}"
    try:
        import materials as _m
        cat = _m.load()
        rel = _m.resolve(cat, "RVI-PINNED-V20260120")
        # P4-SYSTEM.1 (rv64gc-lab-v0): a profile may pin pages from BOTH the unpriv/ and
        # priv/ subtrees — its `file` fields then carry the subdirectory, and the cache
        # root is the snapshot itself. Bare file fields (rv64i-lab-v0) keep the legacy
        # unpriv/ root. Derived from the declaration, and the route is PRINTED either way.
        if any("/" in s.get("file", "") for s in cfg.get("source", [])):
            return REPO / rel, f"materials cache {rel} (manifest-verified, offline)"
        return REPO / rel / "unpriv", f"materials cache {rel}/unpriv (manifest-verified, offline)"
    except Exception:                                   # noqa: BLE001 — fall back to the refusal
        return wd, f"fetched working area {cfg['work_dir']}"


def main(argv: list[str]) -> int:
    if len(argv) >= 2 and argv[1] == "--self-test":
        return _selftest()
    prof = REPO / "profiles" / (argv[1] if len(argv) > 1 else "rv64i-lab-v0")
    st = prof / "sources.sexp"
    try:
        cfg = _D.load_sources(st)
        wd, route = _work_dir(cfg)
        sem = REPO / "definitions" / "riscv" / "rv64i.sem.sexp"
        print(f"citations: {sem.relative_to(REPO)} against "
              f"{cfg.get('publication', '(publication not named)')}")
        print(f"           via {route}")
        return check(st, wd, sem)
    except (CitationError, _sexp.SexpError, KeyError, OSError) as exc:
        print(f"REFUSED: {exc}", file=sys.stderr)
        return 1


def _selftest() -> int:
    import tempfile, textwrap
    passed = failed = 0

    def arm(label, fn):
        nonlocal passed, failed
        try:
            fn()
        except AssertionError as exc:
            print(f"  FAIL  {label}: {exc}"); failed += 1
        except Exception as exc:                        # noqa: BLE001
            print(f"  FAIL  {label}: unexpected {type(exc).__name__}: {exc}"); failed += 1
        else:
            print(f"  ok    {label}"); passed += 1

    def fixture(html: str, sem: str) -> tuple[Path, Path, Path]:
        d = Path(tempfile.mkdtemp())
        (d / "w").mkdir()
        (d / "w" / "a.html").write_text(html)
        (d / "sources.sexp").write_text('(sources (work_dir "w") (source (id "S") (file "a.html")))\n')
        (d / "s.sexp").write_text(sem)
        return d / "sources.sexp", d / "w", d / "s.sexp"

    H = "<h2>3.1. Thing</h2><h3>3.1.2. Sub</h3><h4>3.1.2.1. Deep</h4>"
    def sem(loc): return f'(semantics (sem (insn add) (source "{loc} — why")))'

    arm("GREEN a locator that exists resolves",
        lambda: _eq(check(*fixture(H, sem("S §3.1.2.1"))), 0))
    arm("RED   a locator the document does not publish is refused",
        lambda: _eq(check(*fixture(H, sem("S §3.1.9"))), 1))
    arm("RED   a locator one level too deep is refused",
        lambda: _eq(check(*fixture(H, sem("S §3.1.2.1.1"))), 1))
    arm("RED   a citation naming an unpinned source is refused",
        lambda: _eq(check(*fixture(H, sem("OTHER §3.1"))), 1))
    arm("RED   a source line with no parseable locator is refused", lambda: _raises(
        lambda: check(*fixture(H, '(semantics (sem (insn add) (source "see the manual")))')),
        "does not begin with a locator"))
    arm("RED   an ABSENT working area refuses WITH the fetch command", lambda: _raises(
        lambda: (lambda t: check(t[0], t[1].parent / "gone", t[2]))(fixture(H, sem("S §3.1"))),
        "fetch_sources.sh"))
    arm("RED   a pinned file missing from a present working area is refused", lambda: _raises(
        lambda: (lambda t: (t[1] / "a.html").unlink() or check(*t))(fixture(H, sem("S §3.1"))),
        "is missing"))
    arm("RED   semantics declaring no rule is refused", lambda: _raises(
        lambda: check(*fixture(H, "(semantics (fragment \"x\"))")), "declares no (sem"))
    arm("GREEN an unnumbered heading is not mistaken for a section", lambda: _eq(
        headings("<h1>Introduction</h1><h2>1.1. Real</h2>"), {"1.1"}))
    arm("GREEN heading text is read through its inline markup", lambda: _eq(
        headings('<h3><a class="x" href="#y">3.1.2.</a> <span>Sub</span></h3>'), {"3.1.2"}))

    print(f"check_citations --self-test: {passed} pass / {failed} fail")
    return 1 if failed else 0


def _eq(got, want):
    assert got == want, f"got {got!r}, want {want!r}"


def _raises(fn, needle):
    try:
        fn()
    except CitationError as exc:
        assert needle in str(exc), f"raised, but for the wrong reason: {exc}"
    else:
        raise AssertionError(f"did not refuse ({needle})")


if __name__ == "__main__":
    sys.exit(main(sys.argv))
