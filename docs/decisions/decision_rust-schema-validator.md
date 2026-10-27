# The harness validates source-of-truth files with its own schema validator, measured equal to the pinned `scripts/check_sexp_schema.py`; the pinned validator stays

- **Type:** `decision`
- **Date:** `2026-10-27`
- **Status:** `active`
- **Owner / source:** `XTASK.6` slice 6l, `SEMULITH-XTASK-0020` (a tooling slice taken while every feature leaf waits on a
  ruling — the alternation of [`decision_alternate-port-and-features.md`](decision_alternate-port-and-features.md) resumes
  with features the day one lands); continues [`decision_rust-sexp-reader.md`](decision_rust-sexp-reader.md).
answers: How does the harness judge a document against its schema without a second definition of the schema language, and what does the Rust validator refuse that the pinned one accepts?

## The fact / decision

1. **One validator in Rust, `xtask/src/schema.rs`**, equal to the pinned `scripts/check_sexp_schema.py` by measurement: the
   same kernel (constructs, fields with their types, repetition, optionality, markers and facets; operators with fixed or
   variadic arity and argument specs), the same validation walk, and every refusal the pinned validator's text byte for
   byte — Python's `repr` of the offending value through the 6j reader's `py_repr`. Its 51 self-test arms are re-asserted
   as the port's own, with the same labels, fixtures and needles; `cargo xtask check-sexp-schema --self-test` prints the
   same 52 lines as `python3 scripts/check_sexp_schema.py --self-test`.
2. **The equality is held by a test, permanently.** `the_corpus_validates_as_the_pinned_validator_validates_it` lists every
   tracked `.sexp` the project validates — schemas under `schema/` against `schema.sexp`, fragments against `fragment.sexp`,
   guests' expectations, the profile catalogues against their same-named schemas, the obligation parts, the encodings (315
   pairs today) — and requires both validators' refusal lists identical; an absent comparator fails, never skips. The
   command line `cargo xtask check-sexp-schema <file> <schema>` mirrors the pinned tool's verdict lines and exit statuses
   (0 conforms, 1 refused, 2 an input missing).
3. **The one documented limit is the regex facet.** The pinned validator takes any Python regular expression; the Rust one
   implements the anchored subset the corpus declares — `^` and `\Z`/`$`, literals, character classes with ranges, groups
   with alternation, the quantifiers `* + ? {n} {n,m}` (31 distinct patterns today, all inside it) — and refuses a pattern
   outside the subset BY NAME at schema load (`is not a valid regex: …`), where Python would accept it. A new facet shape in
   `schema/` is therefore a loud question at the harness's gate, never a silent mismatch; widening the subset is a decision
   recorded here. The one `(pattern "regex")` placeholder in the corpus is a literal and compiles.
4. **Nothing is ported and nothing is shimmed by this slice.** `scripts/check_sexp_schema.py` is untouched — it is a pinned
   input of the retained M case's manifest — and every caller still runs it. The validator exists so that slices 6m (the
   encoding-disjointness judge, which validates every document before judging) and 6n (`check_unit_composition.sh` behind a
   held shim) can be ported without a second definition of the schema language.

## Why

- A port that re-derives the schema language from its description would be a second definition; one measured identical to
  the pinned validator on every (file, schema) pair the project owns inherits the pinned meaning — and the measurement reruns
  on every `cargo test`.
- A hand-written regex subset is the honest alternative to a dependency: the corpus's patterns are small and anchored, the
  subset is enumerated, and the refusal names what it does not understand.

## How to apply

- xtask doctrine modules validate through `schema::load_schema` and `schema::validate_file`; the pinned Python validator is
  never edited for the port's sake.
- A corpus pattern the subset refuses stops the harness's gate by name: widen the subset here, with the new shape named and
  measured, or rewrite the pattern inside the subset.
- A new (file, schema) route the project adopts joins the corpus-equality test's pair list.
