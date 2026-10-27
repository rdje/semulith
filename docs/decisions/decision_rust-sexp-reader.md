# The harness reads S-expressions with its own reader, measured equal to the pinned `scripts/sexp.py` over the whole corpus; the pinned reader stays

- **Type:** `decision`
- **Date:** `2026-10-27`
- **Status:** `active`
- **Owner / source:** `XTASK.6` slice 6j, `SEMULITH-XTASK-0018` (the one tooling slice after features 6–10 under
  [`decision_alternate-port-and-features.md`](decision_alternate-port-and-features.md)); continues
  [`rust-native-tooling-direction`](../../MEMORY.md) and the XTASK.6 port record in `docs/tasks/XTASK.md`.
answers: How do the six uncoupled bash drivers that read the corpus through Python ever move to the harness without a second definition of the S-expression format?

## The fact / decision

1. **One reader in Rust, `xtask/src/sexp.rs`**, equal to the pinned `scripts/sexp.py` by measurement, not by claim: the
   same grammar (lists, symbols, integers in decimal/hex/binary with `_` and signs, strings with the five escapes,
   `;` comments, universal newlines), the same refusal messages with the same line numbers and the same Python-shaped
   `[Errno …]` I/O errors, and the pinned reader's twenty self-test arms re-asserted as a unit test.
2. **The equality is held by a test, permanently.** `the_corpus_reads_as_the_pinned_reader_reads_it` lists every tracked
   `.sexp` file (367 today), dumps each through both readers (the Python side in one `python3 -I` process over the
   list) and requires the two dumps byte-identical; an absent comparator fails the test, it never skips. The command line
   `cargo xtask sexp <file>` mirrors `scripts/sexp.py <file>` (stdout, stderr, exit code): 390 cases measured (the
   corpus, 21 fixtures covering every refusal shape, encodings, CRLF, deep nesting, big integers, a missing file, a
   directory, the usage path), 389 identical.
3. **The one documented limit** is the 390th case: an integer of 41 digits. Python's integers are unbounded; the Rust
   reader holds `i128` and refuses such an atom as unreadable (exit 1 where Python prints it). No corpus file carries one
   — the unit test is what says so, and the day one does the test fails naming the file, and this record is the place
   to decide (widen the integer, or refuse by rule on both sides).
4. **Nothing is ported and nothing is shimmed by this slice.** `scripts/sexp.py` is untouched — it is a pinned input of the
   retained M case's manifest — and every bash driver still runs as before. The reader exists so that slices 6k onward
   can port the six drivers (`check_exercise_coverage.sh` first: it uses `children`/`read_file`/`field` directly;
   `check_scope_coverage.sh` and `check_extraction.sh` also need `records_sexp`'s form-to-dict and dump).

## Why

- A port that re-derives the format from the grammar's description would be a second definition; a port whose reader is
  measured byte-identical to the pinned one on every file the project owns inherits the pinned reader's meaning.
- Holding the equality in a test, not in a one-time measurement, is what keeps the two readers one as the corpus grows:
  the measurement reruns on every `cargo test`.

## How to apply

- xtask doctrine modules read `.sexp` through `sexp::read_file`, `children`, `field`, `head`; the pinned Python
  reader is never edited for the port's sake.
- A new corpus shape the Rust reader refuses or reads differently is a failing unit test: fix the Rust side to the
  pinned behaviour, or record a new limit here with the rule applied to both readers.
