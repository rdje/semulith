# DEV_NOTES shard — _(2026-10-02)_ … _(2026-10-02)_

> Sharded from `DEV_NOTES.md` when it crossed its 48 KiB ceiling (`doctrine/readme_routes.tsv`).
> Entries in a shard are **never edited after the shard** — git history is canonical.

## _(2026-10-02)_ — the channel answered in hours; the survey's excluded layer was our own catalog (MCU-DOCS.2)

The twelve MCU requests came back 12/12 fulfilled the same day — the channel's report
(`build_responses.py --report`, rc 0) is the verification entry point, and the adoption
pattern from P5-BOARD.9 (adopt → fetch with digest re-verification → mark our own file)
carried unchanged. The routes the channel measured are worth reading in the answers:
Arm's documentation-service API works; NXP/Microchip/ST's live URLs 404/403/reset to
automated clients and the Wayback captures of the same official URLs carried the bytes.

The execution's real event: the RP2040 datasheet answer read "already held before this
request" — and it was held **twice**: corpus-side, and in our own tracked catalog as
`RP2040-DS` since 2026-09-14 (digest-identical, cached). The `.1` survey had measured
the corpus's proposals feed, not the corpus tree, and not our catalog — the
survey-sampling failure class from MODEL-METHOD.13 recurring at a second layer. Fixed
at root: no duplicate record adopted, the request's answer records the redundancy, and
the knowledge card gained the three-layer "already held" rule with the cheap
complement-check commands.

Lesson: **promoted** — `docs/knowledge/a-survey-that-found-things-can-still-have-missed-things.md`
(the recurrence + the three-layer rule).

## _(2026-10-02)_ — the reading-experience audit's yield was drift, not style (BOOK-APPARATUS.2)

The first audit pass against `decision_mdbook-incremental-engaging` ran as six parallel
read-only chapter-group reviews with the decision's four criteria operationalized
(incremental build-up; motivation before mechanism; layered density; both-audiences
engagement), each returning per-chapter verdicts with line-level evidence. The signing
discipline: **every flagged item was re-verified against the repository before any edit**
— and that verification caught one audit false-positive class (a `grep -c` miscount of
the rv64i profile's inline decision forms; the real count is 28, verified by enumerating
the ids) and one of my own typos (a search string that silently didn't match —
`grep`-verified after the edit, not assumed).

The measured surprise: the audit's yield was **factual drift**, twelve places where
hand-carried repository facts in the book had gone stale — the class DERIVED-COUNTS was
founded on, living in chapters no enumerator covers. Three genuine style violations
(a duplicated sentence, a cold open, a 68-line accreted list item) were the minority.
Two mermaid blocks rendered as raw source in the book; replaced by text flows rather
than adding `mdbook-mermaid` (a dependency the project hasn't sanctioned).

Lesson: `promotion: declined` — the audit method is the decision record's own
consequence clause (`.2` owns the pass; the pass is recorded); the drift fixes are
per-slice history.

