# DEV_NOTES shard — _(2026-10-01)_ … _(2026-10-01)_

> Sharded from `DEV_NOTES.md` when it crossed its 48 KiB ceiling (`doctrine/readme_routes.tsv`).
> Entries in a shard are **never edited after the shard** — git history is canonical.

## _(2026-10-01)_ — measure the attachment before landing the document (P3-BREADTH.5 slice 2)

The slice's real content was a measurement discipline: the DSP's `profile.sexp` and
`state.sexp` were drafted, then placed untracked — and intent-to-added, because three of
the four attaching gates enumerate units through `git ls-files` while PROFILE-CONSISTENCY
globs the filesystem; the difference mattered, and the first measurement saw only one
gate's verdict — and every attaching gate was run before anything landed. The haul:
PROFILE-CONSISTENCY's EVD-04 and SRC-03 arms had seven latent defects to catch in a
dossier that had sat tracked-but-unchecked since `.4` — an "obtained" candidate with no
binary/digest/injection, and independence pairs naming labels instead of candidates. The
fix made the dossier better, not just greener: the asm/emu legs and gearmulator are now
first-class candidates, so the independence rows name things the dossier describes. Two
more defects fell out of the re-validation sweep: rv64's own `profile.sexp` had drifted
from its schema (two notes on D-FENCE — ungated, because no gate schema-validates the
dossier documents as a class; the landing slice now owns that leg), and the coverage
denominator counted a comment's prose as mnemonics. Design note: the taxonomy's scalar
shape lived in exactly two closed places (the schema's scope construct and
`_SCOPE_LISTS`), and the gate readers were already generic over group names — the whole
extension was schema fields plus one tuple, no reader edits. That is what generic readers
buy: the schema is where per-target shape lives, and adding a target is naming it there.

## _(2026-10-01)_ — moving a refusal one layer down, on purpose (P3-BREADTH.5 slice 1)

The interesting engineering was not the schema constructs but the boundary mechanics. The
synth fixture exists to measure the pipeline's refusal boundary; when the schema learned
`memory_spaces`, probe 2's pin went stale and the suite turned RED on the first run —
that RED is the fixture working, and the re-pin (schema accepts rc 0, generator refuses
`memory_spaces declared` rc 2) is the boundary's new position measured rather than
asserted. Two silent-path hazards had to be closed for the move to be honest: the mapping
owner built the state document from named fields only, so a schema-legal `memory_spaces`
would have vanished before the generator could refuse it (the same class `.2` fixed for
operands — the promoted lesson's second instance); and `gen_state.py` subscripted
`doc["xlen"]`, so the schema's newly-optional xlen would have crashed with a KeyError
traceback instead of a named Refusal. Both are now refusals by name with RED self-test
arms. A design rule the slice surfaced and recorded: a profile document that no gate reads
is an ungoverned claim — PROFILE-CONSISTENCY attaches at `profile.sexp`, so the DSP's
`state.sexp` waits for the scope-taxonomy slice rather than landing unread.

