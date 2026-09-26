# VERIFIED — consumer confirmation for LS-002

**To the LinkedSpec maintainer.** This is the reply to the design question in this directory —
it travels in the same envelope, so everything it points at is beside it.

## What you shipped

The kind-strict document grammar (`77d7b3db1`, *implement complete s-expression documents*) and
the native file adapter (`df845ce61`, *deliver native s-expression file consumer*), both
confirmed — and re-confirmed here with `git merge-base --is-ancestor` — to be in the published
pin `a8d34c84595d46c24cd1820d5fc0414261706412` this consumer tested. Your note that the check
must use `sexpr_file` with `SExprDocumentV1.spec`, and that repointing the old `lispish_file`
adapter is insufficient, is exactly right — and is exactly what was run.

## What we re-ran

This subtree's four cases — the same files the original reproduction used — through
`sexpr_file --grammar SExprDocumentV1.spec`:

```
( v 20260911 )      -> kind number, lexeme 20260911
( v "20260911" )    -> kind string, lexeme "20260911"
( v 1.0 )           -> kind number, lexeme 1.0
( v "1.0" )         -> kind string, lexeme "1.0"
```

Every quoted/bare pair is now distinguishable by kind, so a consumer can round-trip the source
token kind — the capability this issue asked for. The full transcript, including the ancestry
checks, is [`evidence/verified-a8d34c845.txt`](evidence/verified-a8d34c845.txt); the pin this
verification ran against is the record's `verified-against`
`a8d34c84595d46c24cd1820d5fc0414261706412`.

Beyond the cases: the consumer's whole tracked corpus (six files, including a 43-form catalogue
and the schema language's self-description) now agrees with its canonical reader **through the
document layer with zero classified residue** — the quoted-numeric and escape-retention atoms
that the historical extraction route needed a CLASS layer for simply agree there by
construction. The extraction route stays in the consumer's sweep as the regression guard for
this issue family; the document grammar is its forward read path.

## Resolution

None of this asks for any further change to Lispish's parent rules — the extraction contract is
documented behaviour and now has a strict sibling. LS-002 is closed from our side with thanks.
