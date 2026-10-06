# P4.10 — The CPU-SYSTEM gate report

**Status:** Underway (slice a, 2026-10-06)

The processor gate has ten parts, called *axes*. Each one asks a different question: is the
profile exactly defined, is its state fully accounted for, is its contract with the
environment complete and tested, are the experiments real and reproducible, does every
requirement have its evidence, are the tricky combinations exercised, do the regression
suites pass, does it behave identically on both kinds of host, can every result be replayed,
and has a release decision been recorded? The gate report answers each question separately
— there is no single "it works" — and it is *generated* from the repository's files, so it
cannot say more than the files show.

This leaf builds that report for the Linux-capable profile. The measurement taken before
building it found that several axes have no evidence yet for this profile (see the P4 page:
"What the gate still needs"). So the report is built first, as an instrument that reads
`incomplete` honestly, and eight later leaves close the axes it finds open.

Slice (a) fixed how the contract axis counts. Every obligation in the contract names two
checks — one showing the promise holding, one showing what breaking it looks like. A check
used to count as "implemented" if any program in the repository mentioned its name. That was
safe while there was only one profile. But the Linux-capable profile reuses thirteen of the
scalar profile's obligations word for word, so the moment it ran one of those checks, the
scalar profile would have been credited with a check it never ran. This was shown directly:
in a scratch copy, the old count rose from 0 to 1 for the scalar profile. Now each profile
names its own *registry* of checks, and only the checks its registry runs are counted. Checks
replaced by a newer contract version no longer count either. The Linux-capable profile reads
**14 of 100** checks realized; the scalar profile still reads 0 of 72, and its existing reports
did not change.
