# CHANGELOG shard — LS-002 … SEMULITH-UT-0055

> Sharded from `CHANGELOG.md` when it crossed its 64 KiB ceiling (`doctrine/readme_routes.tsv`).
> Entries in a shard are **never edited after the shard** — git history is canonical.

## LS-002 → `verified` — the design question closes with a re-run, not a changelog

Upstream confirmed the kind-strict grammar (`77d7b3db1`) and the native adapter (`df845ce61`)
are ancestors of the published pin `a8d34c845` — checked mechanically here with
`merge-base --is-ancestor`, not taken on their word — and prescribed the verification
instrument: `sexpr_file` with `SExprDocumentV1.spec` (the old `lispish_file` adapter is
insufficient). That instrument is exactly what `SOT-FORMAT.10` just added: LS-002's own four
cases re-run through the document layer return distinct kinds for every quoted/bare pair, and
the consumer's whole corpus agrees with its canonical reader there with zero classified
residue. The record gains the `verified-against` pin and the captured transcript; `VERIFIED.md`
carries the reply to upstream in the same envelope as the report. All three of this project's
LinkedSpec issues are now `verified`.

## SEMULITH-SF-0056 (leaf SOT-FORMAT.10) — the document grammar joins the agreement sweep

Director decision on the recorded candidate: adopt SExprDocumentV1 **additively** — a third
reader in `compare_readers.py`, never a replacement. The Lispish layer stays as what it is (the
LS-001/LS-002 regression guard, CLASS notes and all); the new document layer answers both CLASS
families by construction — tagged kinds keep `"20260911"` a `string` (quoted-numeric cannot
arise), raw lexemes decoded on OUR side with sexp.py's own escape table (escape-retention
cannot arise) — and it compares **every** form in every file, not the first. 28 self-test arms
(7 new), and the falsifiable acceptance was exceeded: **6 of 6** tracked files agree in the
document layer with ZERO class notes, because `schema/schema.sexp` itself joined the corpus and
passes both layers — the schema language's fixpoint now also verifies through the document
grammar. Upstream's instruction for LS-002 verification ("use `sexpr_file` with
`SExprDocumentV1.spec`; the lispish_file adapter is insufficient") describes exactly this
layer — which is what the next commit uses to close LS-002.

## SEMULITH-UT-0055 (leaf UPSTREAM-TRACK.4) — the reply travels in the same envelope

Director instruction `2026-09-26`: the verification acknowledgment to LinkedSpec is a
git-tracked note inside the bug's own directory. The subtree was already the envelope a
maintainer copies out — `VERIFIED.md` is now the reply inside that envelope, beside the report
it answers: what shipped, what we re-ran against which pin, the result, what it unblocks, and
where the residue lives (for LS-001: classified under LS-002, not this defect).

The note is gated, not just written: `UPSTREAM-INDEX` refuses a `verified` state whose subtree
carries no `VERIFIED.md`, and refuses a note that does not name the pin the record was verified
against — the note and the record must agree the way the indices and the record must agree.
Fired RED on the real tracker against both LS-001 and LS-003 before the notes existed; 17 arms
(16 → 17) with the wrong-pin refusal; green after, both notes self-contained and pin-consistent.

