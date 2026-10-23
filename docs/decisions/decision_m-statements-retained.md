# The other M statements and Table 1 are retained, so a credit can rest on retained text

- **Type:** `decision`
- **Date:** `2026-10-23`
- **Status:** `active`
- **Owner / source:** `P4-SYSTEM.14` a42bb, `SEMULITH-P4-0295`; answers the retention question raised in
  [`decision_ten-legs-satisfied-credit-separate.md`](decision_ten-legs-satisfied-credit-separate.md) and
  [`decision_credit-is-a-catalogue-record.md`](decision_credit-is-a-catalogue-record.md) (ruling (c) put to
  the director); extends the scoped redistribution recorded in `materials/RVI_M_RETENTION.md` (a42z).
answers: Which normative M text is retained for the m-forms case's 25 properties, and why did retaining it invalidate nothing?

## The fact / decision

1. `profiles/rv64gc-lab-v0/retained/m-statements.html` (identity `RVI-M-STATEMENTS`, 6,018 B, SHA256
   `bc777ebb97814f7361ececfa0dcfc16074374df2ddfeab71cf6684597681d518`) retains, unmodified, the eleven
   normative spans of RVI-M §11.1.1–§11.1.2 other than DIV/DIVU (multiply, high multiply, word multiply,
   remainder, remainder sign, word divide, word remainder, word remainder sign, division by zero,
   remainder by zero, signed overflow) and Table 1 with its caption, from the pinned page (35,588 B,
   `85e1db6c…`), with the same attribution and licence evidence as the DIV statement.
2. `scripts/retain_m_statements.py` emits it from the acquired pages (`--emit`, byte-identical on
   re-emission) and authenticates it offline (`--verify`); the gate runs `--verify` on every commit and
   its probe's 20 tests and ten seams in both interpreter modes. Only reviewed static markup passes.
3. Nothing pinned moved: `scripts/retain_div_statement.py` (the source and licence pins' one owner, a pinned
   input of the retained case) is imported, not edited, and neither the new file nor `sources.sexp` is
   among the 64 inputs the m-forms declaration pins. The method review stays `satisfied` and the policy
   `satisfied — 10 of 10`; no credit is recorded.

## Why

A credited disposition names the retained sources it rests on (`schema/credits.sexp`,
`retained_sources`). Before this record only `RVI-M-DIV-STATEMENT` existed, so a credit for `REQ-GC-M`
covering thirteen forms and twelve Table 1 cells would have rested mostly on cited, unretained text. The
licence finding of a42z (CC-BY 4.0 for the manual text, with the preface's statement covering future
versions) supports the same treatment for these spans; the decision stays scoped to them.

## How to apply

- A crediting record for `REQ-GC-M` cites `RVI-M-DIV-STATEMENT` and `RVI-M-STATEMENTS`.
- Never edit the retained bytes: a different selection is a new emission with a new pin and a reviewed
  reason; `--verify` failing is a finding, not a prompt to re-pin.
- The crediting act itself remains the director's (authority and sufficiency); this record settles only
  what text is retained.
