# Resolve included record links in the generated book

- **Type:** `decision`
- **Date:** `2026-10-11`
- **Status:** `active` — seven-book catalogue and rendered navigation enforced
- **Owner / source:** `P4-SYSTEM.14` a22–a24, `SEMULITH-P4-0213`–`0215`; actual mdBook0.5.4 renders
answers: Why do canonical task links need a book resolver, and how are their records read?

## The fact / decision

Canonical live status and task tables keep their repository links. The HTML-only
`book_navigation.py` preprocessor runs after mdBook's include expansion and resolves
their simple inline task destinations to the project book's record-reading section.
The linked tree ID selects `docs/tasks/<TREE>.md`. The two declared external history
surfaces also lead there, with their exact reading commands displayed in the book.
This supplies navigation to the source records; it does not render their full bodies.

mdBook expands includes without rebasing their links, then rewrites `.md` targets to
`.html`. The public before/after build measures50 missing main-book paths becoming0,
with exactly50 href changes and every other byte of50 normal HTML pages unchanged.
The print page also resolves. A24 completes the six ordinary cross-unit paths and their four print copies,
then extends UNIT-BOOKS to check fresh builds of the complete collection.

## Contract and limits

The resolver uses mdBook's public `[context, book]` JSON protocol, supports HTML,
requires the project or a registered unit book root and safe chapter paths, and preserves book metadata.
A missing or symlinked declared source refuses before JSON output. It handles only
simple inline links, leaving other destinations/syntax intact. Fences, closed inline
code spans, explicit HTML literal containers/comments, escaped links and images stay
unchanged. An unsupported form is not evidence that its rendered route is valid.
Future verification must inspect actual built paths and fragments.

Nineteen API/CLI tests pass normally and optimized. Independent route, code-mask,
relative-context and source-guard omissions cause16/10/13/2 assertion failures in
both modes. Fixtures stay under `target/book-navigation-probe` and are removed.
Five literal book retrieval commands return the exact retained bytes. Earlier seals,
archives, LIVE_STATUS and task indexes are unchanged. No CPU or evidence credit.

The public integration follows [mdBook's preprocessor protocol](https://rust-lang.github.io/mdBook/for_developers/preprocessors.html)
and [ordering/configuration contract](https://rust-lang.github.io/mdBook/format/configuration/preprocessors.html).
Only this repository's script and relative configuration are build dependencies.

answers: How are sibling books browsed and how does UNIT-BOOKS detect stale catalogue/navigation or unsafe source paths?

## Collection contract (a24)

Use the shared `docs` serving root after `make book`; per-unit serving cannot
reach sibling books. The resolver maps simple declared sibling source chapters
to relative built HTML destinations and retains query/fragment suffixes. Missing
or symlinked declared chapters refuse. Unregistered destinations remain unchanged
and the rendered gate decides whether they resolve. Six normal/four print href
changes reconstruct all62 model HTML pages byte-exactly;12 loopback HTTP reads
pass and the temporary server closes. Authored model chapters remain unchanged.

UNIT-BOOKS reuses records_sexp's unit mapping, refuses absolute/traversing,
symlinked, cross-volume or nested-Git book paths before builds, and compares the
main catalogue's IDs/kinds to registration. It builds the project and registered
books into a fresh disposable bundle under target/, preserving the normal docs
layout. Local hyperlink paths and HTML fragments, including print pages, must
resolve within that bundle. Old output cannot qualify. The corrected RV64GC entry
means registered, not accepted; CPU-SYSTEM is still incomplete. Remote availability,
unsupported source syntax and semantic/chapter completeness are separate claims.

The original19 resolver controls remain among26; gate controls cover23 cases.
Both suites pass normally/optimized; independent omissions discriminate. Twelve
shell arms plus four nested-suite runs pass, and derived outer arms total773.
Part14 preserves the whole stale overview and two whole completed book receipts
with complete source inverses and six damaged refusals; it is ordinary Markdown
outside the closed12-file seal. Published DEV sharding preserves30==26+4 entries.
The actual build comparison caught a wrong relative -d assumption before signoff:
public CLI help identifies cwd-relative destinations. Restore the established
Makefile and reproduce/remove exactly41 misdirected generated files; all corrected
builds use their expected directories. Absolute scratch destinations are unaffected.
