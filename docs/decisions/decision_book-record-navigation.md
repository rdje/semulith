# Resolve included record links in the generated book

- **Type:** `decision`
- **Date:** `2026-10-11`
- **Status:** `active` — project-book routes repaired; cross-unit routes and the full rendered gate are a24
- **Owner / source:** `P4-SYSTEM.14` a22–a23, `SEMULITH-P4-0213`–`0214`; actual mdBook0.5.4 renders
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
The print page also resolves. The six remaining cross-unit book paths are owned at
high priority by a24; the wider rendered-navigation gate is not registered yet.

## Contract and limits

The resolver uses mdBook's public `[context, book]` JSON protocol, supports HTML,
requires the project book root and safe chapter paths, and preserves book metadata.
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
