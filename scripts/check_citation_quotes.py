#!/usr/bin/env python3
"""Does every quoted phrase a tracked document attributes to a pinned section occur IN that
section? (CITATION-ACCURACY.1 — the CITATION-QUOTES doctrine.)

`check_citations.py` asks whether a locator RESOLVES — whether `RVI-F §20.1.1` exists in the
pinned page. This asks the next question, which a resolving locator can still fail: is the
sentence the document QUOTES under that locator actually in that section?

⛔ WHY THIS TOOL EXISTS, measured (P4-SYSTEM.7 slice (c3) part 1, SEMULITH-P4-0043): the rv64gc
state document cited fflags/frm/fcsr content as `RVI-F §20.1.1` — a section that exists (the F
register state) and is the wrong one (the fcsr is §20.1.2); a statement quoted the FSRM
sentence under it. Both guests that exercise the fcsr carried the same locator. Every gate
was green: the locators resolved, and nothing read the quotes.

WHAT IS JUDGED. Every string atom of every tracked `.sexp` (comments are not atoms). A
single-quoted phrase of six or more characters is JUDGED only when its attribution is
decidable by one of four rules, tried in order:

- R1 — the quote is immediately followed by a parenthesized locator: `'…' (RVI-F §20.1.2`;
- R2 — the quote sits in a `(source "ID §N …")` string — the source's leading locator;
- R3 — the quote sits in an expectation step's `(derivation …)` — the step's `(source …)`;
- R4 — the string names exactly ONE distinct locator.

A quote no rule attributes is COUNTED, never judged — a string naming two sections beside a
quote does not say which one it quotes, and a guess would be a second citation. An ellipsis
(`…`, `...`) or an editorial bracket (`[it]`) splits the phrase into pieces that must occur IN
ORDER. Matching folds case, whitespace, quote characters and typographic dashes, and drops
zero-width characters: the pinned HTML renders code literals in quotes (`('pc'+4)`) and puts
zero-width spaces inside dash ranges (`7—​5`) — both measured on the real pages.

A SECTION is a numbered heading's text through the next heading that is neither it nor its
descendant: `§12.1` includes `§12.1.2`. A miss NAMES THE CURE — the refusal says which section
of the cited artifact does hold the phrase, or that none does.

⚠️ HONEST LIMITS. It judges quotes, not paraphrase: an unquoted claim under a locator is still
a reviewer's question. A source pinned as a declared non-snapshot artifact (`http_status 0` —
a PDF) has no section structure here; quotes attributed to it are counted UNCHECKABLE by name.
Markdown documents are not in the corpus (the tree's open question).

Usage:
  check_citation_quotes.py                       judge every tracked .sexp (the corpus)
  check_citation_quotes.py --pages DIR FILE…     judge FILEs against synthetic pages DIR/<ID>.html
Exit: 0 every judged quote occurs in its cited section; 1 a miss or an unresolved section;
      2 refused (the pinned pages are absent — a check that cannot judge never reports green).
"""

from __future__ import annotations

import html
import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import sexp as _sexp                                                    # noqa: E402

REPO = Path(__file__).resolve().parent.parent

HEADING = re.compile(r"<h([1-6])[^>]*>(.*?)</h\1>", re.S)
NUMBER = re.compile(r"((?:\d+\.)+)\s")
LOCATOR = re.compile(r"([A-Z][A-Z0-9-]+)\s+§([0-9]+(?:\.[0-9]+)*)")
# An opening quote follows the start, whitespace or an opening bracket/separator; the body may
# hold apostrophes that are followed by a letter (possessives, contractions); a closing quote
# is NOT followed by a letter. Six characters is the floor below which a match is noise.
QUOTE = re.compile(r"(?:^|(?<=[\s(\[—:;,]))'((?:[^']|'(?=[A-Za-z]))+?)'(?![A-Za-z])")
R1_TAIL = re.compile(r"\s*[,;]?\s*\(\s*([A-Z][A-Z0-9-]+\s+§[0-9]+(?:\.[0-9]+)*)")
MIN_PHRASE = 6


class Refusal(Exception):
    """The check cannot judge — never reported as a pass."""


def normalize(text: str) -> str:
    text = html.unescape(text)
    text = re.sub("[​‌‍﻿]", "", text).replace(" ", " ")
    text = re.sub("[‘’`]", "'", text)
    text = re.sub("[“”]", '"', text)
    text = re.sub("[‐‑‒–—−]", "-", text)
    return re.sub(r"\s+", " ", text).strip().lower()


def key(text: str) -> str:
    """The matching key: normalized, then whitespace and quote characters dropped."""
    return re.sub(r"[\s'\"]+", "", normalize(text))


def sections(page: str) -> dict[str, str]:
    """Every numbered section of a page → the matching key of its text (descendants included)."""
    heads = []
    for m in HEADING.finditer(page):
        title = normalize(re.sub(r"<[^>]+>", "", m.group(2)))
        n = NUMBER.match(title + " ")
        if n:
            heads.append((n.group(1).rstrip("."), m.start(), m.end()))
    out: dict[str, str] = {}
    for i, (num, _, body_start) in enumerate(heads):
        end = len(page)
        for num2, start2, _ in heads[i + 1:]:
            if num2 != num and not num2.startswith(num + "."):
                end = start2
                break
        out.setdefault(num, key(re.sub(r"<[^>]+>", " ", page[body_start:end])))
    return out


def pieces(phrase: str) -> list[str]:
    split = re.sub(r"\[[^\]]*\]", "…", phrase).replace("...", "…")
    return [k for k in (key(p) for p in split.split("…")) if k]


def occurs(phrase: str, body: str) -> bool:
    at = 0
    for piece in pieces(phrase):
        i = body.find(piece, at)
        if i < 0:
            return False
        at = i + len(piece)
    return True


def where(phrase: str, secs: dict[str, str]) -> str:
    """The most specific section of the artifact that holds the phrase, for the refusal."""
    hits = [n for n, body in secs.items() if occurs(phrase, body)]
    if not hits:
        return "found nowhere in the cited artifact"
    best = max(hits, key=lambda n: (n.count("."), [int(x) for x in n.split(".")]))
    return f"found in §{best}"


def atoms(form, parent=None):
    """(string, head of the enclosing form, the enclosing form, its parent) per string atom."""
    if isinstance(form, list) and form:
        head = str(form[0]) if isinstance(form[0], _sexp.Symbol) else None
        for x in form[1:]:
            if isinstance(x, str) and not isinstance(x, _sexp.Symbol):
                yield x, head, form, parent
            elif isinstance(x, list):
                yield from atoms(x, form)


def attribute(s: str, end: int, head, form, parent):
    """(rule, source id, section number) for the quote ending at `end`, or None."""
    m = R1_TAIL.match(s, end)
    if m:
        loc = LOCATOR.match(m.group(1))
        return "R1", loc.group(1), loc.group(2).rstrip(".")
    if head == "source":
        loc = LOCATOR.match(s)
        if loc:
            return "R2", loc.group(1), loc.group(2).rstrip(".")
    if head == "derivation" and isinstance(parent, list):
        src = next((x for x in parent if isinstance(x, list) and x
                    and str(x[0]) == "source" and len(x) > 1), None)
        loc = LOCATOR.match(str(src[1])) if src else None
        if loc:
            return "R3", loc.group(1), loc.group(2).rstrip(".")
    locs = {(a, b.rstrip(".")) for a, b in LOCATOR.findall(s)}
    if len(locs) == 1:
        sid, num = next(iter(locs))
        return "R4", sid, num
    return None


def judge(files: list[Path], pages: dict[str, Path | None], label) -> int:
    """Judge every attributed quote in `files`; print the findings and the census."""
    secs: dict[str, dict[str, str]] = {}
    counts = {"R1": 0, "R2": 0, "R3": 0, "R4": 0}
    unattributed, uncheckable, findings = 0, {}, []
    for f in files:
        for top in _sexp.read_file(f):
            for s, head, form, parent in atoms(top):
                for q in QUOTE.finditer(s):
                    phrase = q.group(1)
                    if len(key(phrase)) < MIN_PHRASE:
                        continue
                    got = attribute(s, q.end(), head, form, parent)
                    if got is None:
                        unattributed += 1
                        continue
                    rule, sid, num = got
                    if sid not in pages or pages[sid] is None:
                        uncheckable[sid] = uncheckable.get(sid, 0) + 1
                        continue
                    if sid not in secs:
                        secs[sid] = sections(pages[sid].read_text(encoding="utf-8",
                                                                  errors="replace"))
                    counts[rule] += 1
                    body = secs[sid].get(num)
                    short = phrase if len(phrase) <= 90 else phrase[:87] + "…"
                    if body is None:
                        findings.append(f"  UNRESOLVED {label(f)} [{rule}]: {sid} §{num} does not "
                                        f"exist in the pinned artifact — '{short}'")
                    elif not occurs(phrase, body):
                        findings.append(f"  MISS {label(f)} [{rule}]: '{short}' is not in {sid} "
                                        f"§{num} — {where(phrase, secs[sid])}")
    judged = sum(counts.values())
    for line in findings:
        print(line)
    rules = ", ".join(f"{r} {n}" for r, n in counts.items())
    skip = (", ".join(f"{sid} ×{n}" for sid, n in sorted(uncheckable.items()))
            or "none")
    print(f"CITATION-QUOTES: {judged} attributed quote(s) judged ({rules}); "
          f"{len(findings)} finding(s); {unattributed} unattributed (counted, never judged); "
          f"uncheckable (no HTML pin): {skip}")
    return 1 if findings else 0


def corpus_pages() -> dict[str, Path | None]:
    """Every source id the profiles pin → its page on disk (None for a declared PDF pin),
    through check_citations' own route (the fetched area, else the materials cache)."""
    import check_citations as _C
    import dossier_sexp as _D
    pages: dict[str, Path | None] = {}
    for sp in sorted((REPO / "profiles").glob("*/sources.sexp")):
        cfg = _D.load_sources(sp)
        wd, _route = _C._work_dir(cfg)
        for s in cfg.get("source", []):
            if s.get("http_status") == 0:
                pages.setdefault(s["id"], None)
                continue
            p = wd / s["file"]
            if p.is_file():
                pages[s["id"]] = p
            elif s["id"] not in pages:
                raise Refusal(f"{s['id']}: the pinned page {p.relative_to(REPO)} is absent — "
                              f"fetch it (scripts/materials.py --fetch or scripts/fetch_sources.sh); "
                              f"a check that cannot judge never reports green")
    return pages


def main(argv: list[str]) -> int:
    try:
        if argv[:1] == ["--pages"]:
            if len(argv) < 3:
                print(__doc__, file=sys.stderr)
                return 2
            d = Path(argv[1])
            pages = {p.stem: p for p in d.glob("*.html")}
            pages.update({p.stem: None for p in d.glob("*.pdf")})
            return judge([Path(a) for a in argv[2:]], pages, lambda f: f.name)
        if argv:
            print(__doc__, file=sys.stderr)
            return 2
        tracked = subprocess.run(["git", "ls-files", "*.sexp"], cwd=REPO, check=True,
                                 capture_output=True, text=True).stdout.split()
        return judge([REPO / t for t in tracked], corpus_pages(),
                     lambda f: f.relative_to(REPO).as_posix())
    except Refusal as exc:
        print(f"CITATION-QUOTES: REFUSED — {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
