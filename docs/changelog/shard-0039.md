# CHANGELOG shard — SEMULITH-SF-0054 … SEMULITH-SF-0053

> Sharded from `CHANGELOG.md` when it crossed its 64 KiB ceiling (`doctrine/readme_routes.tsv`).
> Entries in a shard are **never edited after the shard** — git history is canonical.

## SEMULITH-SF-0054 (leaf SOT-FORMAT.1) — the schema language, written in itself

The gap was "it parses": an S-expression reader accepts anything syntactically, so a mistyped
head or field was invisible. `schema/schema.sexp` now declares the language in itself —
`(construct (name …) (field …)…)`, atom fields, form fields in the corpus's two house shapes
(`(source (file …) …)` whole-list and `(effect (set …))` value-held), `(empty yes)` markers
for the corpus's `(requires)`/`(extensions)` idiom, `(values …)` spellings, sibling repetition —
and `scripts/check_sexp_schema.py` (16 arms, 13 RED, each naming its construct, field and
reason) validates any file against any schema. The fixpoint is the proof, not a slogan:
`schema.sexp` conforms to `schema.sexp`.

⭐ The first design assumed a tidy uniform `(name value)` pair grammar — and the real corpus
refuted it before it shipped. Reading `rv64i.sexp`/`rv64i.sem.sexp` first is what made the
language fit the files `.2` must declare; an invented grammar would have met the corpus as an
argument. `schema/` is registered in `doctrine/readme_routes.tsv` in its creating commit, and
`TOOLBOX.md` gains the row.

## SEMULITH-SF-0053 (leaf SOT-FORMAT.8) — the contract names its format at last

The mdBook chapter *"Architecture and canonical definitions"* includes `docs/ARCHITECTURE.md`
verbatim, and that document named no format, no `definitions/` directory and no composition —
four commits had introduced all three, and the director's only window showed none of it
(`grep -c 'S-expression'` → 0). The drift is closed at the source document: §1.1 records the
one-format decision and what exists in it today (fragments, cited semantics at 52 of 52, the
two-reader agreement check), §1.2 defines the fragment and the composition operator that is
*decided, not hoped* (`check_encoding_disjoint.py`), §1.3 states the schema layer's contract and
labels it specified-not-built. Built claims name their instruments; pending layers say pending;
the one count that moves (`5 of 5`) was rephrased to "agreement file by file" so the prose
cannot drift. `make book` builds; the chapter preface needed no edit — that was the point.

Also: a knowledge card for the session's other lesson — a director-named action runs first,
right after context recovery; standing cadences queue behind it.

