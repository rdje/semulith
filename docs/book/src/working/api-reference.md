# The API reference

SEMULITH's Rust API is documented by rustdoc, from the code itself: the reference is never written by
hand beside the code, and nothing of it is committed. `make book` builds it into the book's output
next to these pages (`decision_rust-native-tooling.md`, tree `RUSTDOC`):

- [`semulith_core`](../api/semulith_core/index.html) — the engine: the canonical definition's generated
  tables, the architectural state, execution, the floating-point and environment layers.
- [`semulith_verify`](../api/semulith_verify/index.html) — evidence: fixtures, the comparison and replay
  paths, reduction, the bench.
- [`semulith_dsp56300`](../api/semulith_dsp56300/index.html) — the DSP56300 slice.
- [`semulith`](../api/semulith/index.html) — the command-line front end.

## What holds it

The `API-DOCS` doctrine builds the reference on every commit and refuses a broken intra-doc link, a
public doc linking a private item, or an unclosed HTML tag, naming file, line and lint. A defect is
fixed in the doc comment, or in the generator that writes it, never by allowing the lint; it fired on
20 such defects before it was registered. The book's own link check builds the reference fresh with
the books and verifies that every link from these pages into it lands on a real page; the reference's
internal links are rustdoc's, held by `API-DOCS`.

## How complete it is

Measured on 2026-10-23 with rustdoc's coverage report:

| Crate | Items documented | Coverage |
| --- | --- | --- |
| `semulith_core` | 553 | 90.1% |
| `semulith_verify` | 404 | 82.4% |
| `semulith_dsp56300` | 66 | 35.5% |

The undocumented public items are counted per crate on every commit and may only fall (`RUSTDOC.3`):
the record is `doctrine/undocumented_items.tsv`, and a rise is refused with the crate's items listed.
The DSP crate is brought to parity (`RUSTDOC.5`) and runnable examples follow (`RUSTDOC.6`).
