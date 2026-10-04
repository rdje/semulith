# DEV_NOTES shard — _(2026-10-02)_ … _(2026-10-02)_

> Sharded from `DEV_NOTES.md` when it crossed its 48 KiB ceiling (`doctrine/readme_routes.tsv`).
> Entries in a shard are **never edited after the shard** — git history is canonical.

## _(2026-10-02)_ — the ceiling taxed a property the file could not have: the instrument must match the failure mode (P5-BOARD.12)

The day after the composed-unit bound raise, the director delegated the policy question
it stood on ("yours to decision and act upon … SOTA, SIGNOFF and PRODUCTION-GRADE").
The ruling: a per-part byte ceiling exists to catch silent accretion in
hand-maintained files, and a regeneration-gated derived file cannot accrete silently —
every byte is re-derived on every commit, and its size is a pure function of
already-bounded inputs. So the interim 128 KiB raise (one day old) was the right
stopgap and the wrong instrument, and the gate went two-tier: authored members keep
the 64 KiB ceiling, derived members are exempt **as a checked property** — a
fact_ownership.tsv mirror row with a regeneration-doctrine governor (closed set), never
a declaration. The exemption consuming the FACT-OWNERSHIP registry is the part that
makes it signoff-grade: the registry is already completeness-checked (every governor
registered, every corpus pair named), so no second declaration surface exists to drift,
and an authored file cannot smuggle under the exemption because nothing regenerates it.

Two implementation details worth remembering. The per-part loop previously inspected
only the single biggest member (`sort -rn | head -1`) — a second over-ceiling file was
never even reported; the two-tier rule forced judging EVERY member, which is strictly
stronger for authored content too. And the self-test harness gained the arms in the
real corpus's shape: the RED for an authored file over the ceiling fires on fixtures
because the real corpus's authored members are all (correctly) under the ceiling — a
control that only ever sees GREEN in production is exactly the kind that must be seen
RED in the harness. And a third, caught by DERIVED-COUNTS itself: the regen-set arms
were first written under a new `armregen` helper the enumerator does not count, so 2
of 17 arms were invisible to the arm total (357 ≠ 359) — fixed by folding the probe
into `arm`'s optional `[cmd...]` form rather than teaching the enumerator a third
idiom. New self-test idioms are not free: the arm total is a census, and a census
only counts the shapes it knows.

Lesson: **promoted** — `docs/knowledge/a-byte-ceiling-applies-to-authored-content.md`
(the question form + the checked-exemption pattern; the ruling itself is
`decision_derived-members-of-bounded-families`).

