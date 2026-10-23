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

The SEMANTICS doctrine runs this reader and its controls on every commit. Fetched
pages are preferred; otherwise the authenticated materials snapshot supplies them.
Both routes require exact source hashes and byte lengths before section resolution.
A standalone invocation refuses absent evidence; doctrine wrappers print a named
skip only when neither artifact route is present. Partial or altered evidence
refuses. No network access or repinning happens in this reader.
"""

from __future__ import annotations

import hashlib
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


def verified_source(source: dict, work_dir: Path) -> Path:
    """Refuse unpinned bytes before either citation reader uses a source page."""
    path = work_dir / source["file"]
    if not path.is_file():
        raise CitationError(f"{source['id']}: {_rel(path)} is missing; run scripts/fetch_sources.sh")
    digest, size = source.get("sha256"), source.get("bytes")
    if (not isinstance(digest, str) or not re.fullmatch(r"[0-9a-f]{64}", digest)
            or type(size) is not int or size < 0):
        raise CitationError(f"{source['id']}: missing or invalid source identity (sha256/bytes)")
    data = path.read_bytes()
    if len(data) != size:
        raise CitationError(f"{source['id']}: {_rel(path)} byte length {len(data)} differs "
                            f"from pinned {size}; restore the exact pinned artifact")
    actual = hashlib.sha256(data).hexdigest()
    if actual != digest:
        raise CitationError(f"{source['id']}: {_rel(path)} sha256 {actual} differs from pinned "
                            f"{digest}; restore the exact pinned artifact, never repin to pass")
    return path


def artifacts_available(repo: Path | None = None) -> bool:
    """Presence for named-skip dispatch, never an identity verdict.

    A partial or corrupt directory is present and must reach the refusing reader.
    A fetched-only installation must be judged even without a materials cache.
    """
    repo = repo or REPO
    for sp in sorted((repo / "profiles").glob("*/sources.sexp")):
        cfg = _D.load_sources(sp)
        if (any(s.get("http_status") != 0 for s in cfg.get("source", []))
                and (repo / cfg["work_dir"]).is_dir()):
            return True
    import materials as _m
    catalog = repo / "materials/catalog.sexp"
    if not catalog.is_file():
        return False
    try:
        cat = _m.load(catalog)
        rec = cat["materials"]["RVI-PINNED-V20260120"]
    except (_m.MaterialError, _sexp.SexpError, KeyError, OSError) as exc:
        raise CitationError(f"source availability cannot be judged: {exc}") from exc
    return (repo / cat["cache_root"] / rec["cache_path"]).exists()


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
        p = verified_source(s, work_dir)
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
    for s in _sexp.children(form, "sem") + _sexp.children(form, "expand"):
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
        raise CitationError(f"{semantics.name}: declares no (sem …) or (expand …) form")
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


def _work_dir(cfg: dict, repo: Path | None = None) -> tuple[Path, str]:
    """Where the pinned pages are RIGHT NOW, and which route found them.

    The fetched working area is the primary route. ⛔ But it is untracked and needs the network,
    which is what kept this check off the gate list. The materials cache is the second route: the
    same snapshot, verified against a manifest covering all 72 pages, reproducible OFFLINE. Which
    route was used is PRINTED, because a check whose evidence could come from two places and does
    not say which is a check whose result cannot be reproduced.
    """
    repo = repo or REPO
    wd = repo / cfg["work_dir"]
    if wd.is_dir():
        return wd, f"fetched working area {cfg['work_dir']}"
    try:
        import materials as _m
        cat = _m.load(repo / "materials/catalog.sexp")
        rel = _m.resolve(cat, "RVI-PINNED-V20260120", repo=repo)
        # P4-SYSTEM.1 (rv64gc-lab-v0): a profile may pin pages from BOTH the unpriv/ and
        # priv/ subtrees — its `file` fields then carry the subdirectory, and the cache
        # root is the snapshot itself. Bare file fields (rv64i-lab-v0) keep the legacy
        # unpriv/ root. Derived from the declaration, and the route is PRINTED either way.
        if any("/" in s.get("file", "") for s in cfg.get("source", [])):
            return repo / rel, f"materials cache {rel} (manifest-verified, offline)"
        return repo / rel / "unpriv", f"materials cache {rel}/unpriv (manifest-verified, offline)"
    except (_m.MaterialError, _sexp.SexpError, KeyError, OSError) as exc:
        raise CitationError(f"the pinned source route is unavailable: {exc}") from exc


def corpus(repo: Path) -> int:
    """Every tracked sem file's citations, against the profile(s) that pin what it cites.

    ⭐ THE BINDING IS DERIVED, NEVER HAR-CODED: a sem file checks against every profile whose
    sources.sexp pins ALL the source-ids its rules cite (rv64i.sem.sexp resolves under both
    RISC-V units; the Zicsr/Zicntr/privileged-system files cite RVP-* pages only rv64gc
    pins). A sem file NO profile fully pins is a finding BY NAME — its locators are
    unverifiable in this repository, which is exactly the hole the single-file mode was
    built to close for one file (P4-SYSTEM.2 slice b: the new corpus needed it for four).
    """
    sems = sorted((repo / "definitions").glob("**/*.sem.sexp"))
    if not sems:
        raise CitationError(f"{_rel(repo / 'definitions')}: no sem files — an empty corpus "
                            f"is not a checkable one")
    wants = {sem: citations(sem) for sem in sems}
    cited_ids = {sid for want in wants.values() for sid, _ in want}
    # A profile enters the binding only if it DECLARES a cited source-id — loading every
    # profile's pins would read artifacts (binary manuals, other architectures) the
    # sem corpus never cites.
    pins: dict[str, tuple[Path, dict[str, set[str]]]] = {}
    for sp in sorted((repo / "profiles").glob("*/sources.sexp")):
        cfg = _D.load_sources(sp)
        if not cited_ids & {s["id"] for s in cfg.get("source", [])}:
            continue
        wd, _route = _work_dir(cfg, repo)
        pins[sp.parent.name] = (sp, published(sp, wd))
    rc, checked = 0, 0
    for sem in sems:
        want = wants[sem]
        cited = {sid for sid, _ in want}
        full = sorted(name for name, (_, have) in pins.items() if cited <= set(have))
        if not full:
            print(f"  UNCHECKABLE {sem.name}: cites {sorted(cited)} — no profile pins them all",
                  file=sys.stderr)
            rc = 1
            continue
        for name in full:
            sp, _have = pins[name]
            cfg = _D.load_sources(sp)
            wd, route = _work_dir(cfg, repo)
            print(f"{sem.name} against {name} (via {route}):")
            rc |= check(sp, wd, sem)
            checked += 1
    print(f"corpus: {len(sems)} sem file(s), {checked} resolution(s)")
    return rc


def main(argv: list[str]) -> int:
    if len(argv) >= 2 and argv[1] == "--self-test":
        return _selftest()
    if len(argv) >= 2 and argv[1] == "--corpus":
        try:
            return corpus(REPO)
        except (CitationError, _sexp.SexpError, KeyError, OSError) as exc:
            print(f"REFUSED: {exc}", file=sys.stderr)
            return 1
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
    import shutil
    import tempfile
    passed = failed = 0
    temporary_root = REPO / "target/doctrine-selftest"
    temporary_root.mkdir(parents=True, exist_ok=True)
    # Every fixture directory this self-test creates is removed when it ends (a42ax, 2026-10-23):
    # before that, each run left its 19 directories behind — 5,494 of them, 87 MB, by the gate run
    # of 2026-10-23 — a leak no cleanup act governs because the fixtures are not recorded outputs.
    created: list[Path] = []

    def scratch() -> Path:
        d = Path(tempfile.mkdtemp(dir=temporary_root))
        created.append(d)
        return d

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
        d = scratch()
        (d / "w").mkdir()
        (d / "w" / "a.html").write_text(html)
        digest = hashlib.sha256(html.encode()).hexdigest()
        (d / "sources.sexp").write_text(
            f'(sources (work_dir "w") (source (id "S") (file "a.html") '
            f'(sha256 "{digest}") (bytes {len(html.encode())})))\n')
        (d / "s.sexp").write_text(sem)
        return d / "sources.sexp", d / "w", d / "s.sexp"

    H = "<h2>3.1. Thing</h2><h3>3.1.2. Sub</h3><h4>3.1.2.1. Deep</h4>"
    def sem(loc): return f'(semantics (sem (insn add) (source "{loc} — why")))'

    arm("GREEN a locator that exists resolves",
        lambda: _eq(check(*fixture(H, sem("S §3.1.2.1"))), 0))
    arm("GREEN an expansion-only document's locator resolves",
        lambda: _eq(check(*fixture(H, sem("S §3.1.2.1").replace('(sem (insn', '(expand (insn'))), 0))
    arm("RED   an expansion-only document's missing section is refused",
        lambda: _eq(check(*fixture(H, sem("S §3.1.9").replace('(sem (insn', '(expand (insn'))), 1))
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
    arm("RED   same-size altered bytes refuse even with unchanged headings", lambda: _raises(
        lambda: (lambda t: ((t[1] / "a.html").write_text(H.replace("Thing", "Other")),
                            check(*t))[1])(fixture(H, sem("S §3.1"))), "sha256"))
    arm("RED   a wrong byte-length pin refuses even when the digest matches", lambda: _raises(
        lambda: (lambda t: (t[0].write_text(t[0].read_text().replace(
            f'(bytes {len(H.encode())})', '(bytes 1)')), check(*t))[1])(
                fixture(H, sem("S §3.1"))), "byte length"))
    arm("RED   absent source identity refuses rather than trusting the filename", lambda: _raises(
        lambda: (lambda t: (t[0].write_text(re.sub(r'\(sha256 "[0-9a-f]+"\)', '',
            t[0].read_text())), check(*t))[1])(fixture(H, sem("S §3.1"))), "source identity"))
    arm("RED   semantics declaring no rule is refused", lambda: _raises(
        lambda: check(*fixture(H, "(semantics (fragment \"x\"))")), "declares no (sem"))
    arm("GREEN an unnumbered heading is not mistaken for a section", lambda: _eq(
        headings("<h1>Introduction</h1><h2>1.1. Real</h2>"), {"1.1"}))
    arm("GREEN heading text is read through its inline markup", lambda: _eq(
        headings('<h3><a class="x" href="#y">3.1.2.</a> <span>Sub</span></h3>'), {"3.1.2"}))

    def corpus_fixture():
        d = scratch()
        (d / "definitions" / "riscv").mkdir(parents=True)
        for prof, sid, html_text in (("p1", "S", H), ("p2", "T", "<h2>7.1. Other</h2>")):
            w = d / "profiles" / prof / "w"
            w.mkdir(parents=True)
            (w / "a.html").write_text(html_text)
            digest = hashlib.sha256(html_text.encode()).hexdigest()
            (d / "profiles" / prof / "sources.sexp").write_text(
                f'(sources (work_dir "profiles/{prof}/w") (source (id "{sid}") (file "a.html") '
                f'(sha256 "{digest}") (bytes {len(html_text.encode())})))\n')
        return d

    def corpus_sem(d, name, loc):
        (d / "definitions" / "riscv" / name).write_text(
            f'(semantics (sem (insn add) (source "{loc} — why")))')

    arm("GREEN --corpus binds each sem file to the profile that pins its sources",
        lambda: _eq((lambda d: (corpus_sem(d, "x.sem.sexp", "S §3.1.2.1"), corpus(d))[1])(
            corpus_fixture()), 0))
    arm("RED   --corpus: a sem file whose sources no profile pins is named",
        lambda: _eq((lambda d: (corpus_sem(d, "y.sem.sexp", "NOPE §1.1"), corpus(d))[1])(
            corpus_fixture()), 1))
    arm("RED   --corpus: a locator the pinning profile does not publish fails resolution",
        lambda: _eq((lambda d: (corpus_sem(d, "z.sem.sexp", "T §7.1.9"), corpus(d))[1])(
            corpus_fixture()), 1))
    arm("GREEN fetched-only artifacts are available without a materials cache",
        lambda: _eq(artifacts_available(corpus_fixture()), True))
    arm("GREEN an absent artifact set permits named-skip dispatch",
        lambda: _eq(artifacts_available(scratch()), False))
    arm("GREEN a partial fetched directory reaches refusal rather than named skip",
        lambda: _eq((lambda d: ((d / 'profiles/p1/w/a.html').unlink(),
                               (d / 'profiles/p2/w/a.html').unlink(),
                               artifacts_available(d))[-1])(corpus_fixture()), True))

    for d in created:
        shutil.rmtree(d, ignore_errors=True)
    leaked = [d for d in created if d.exists()]
    print(f"check_citations --self-test: {passed} pass / {failed} fail; "
          f"{len(created)} fixture directories removed, {len(leaked)} left behind")
    return 1 if failed or leaked else 0


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
