# VERIFIED — consumer confirmation for LS-001

**To the LinkedSpec maintainer.** This is the reply to the report in this directory — it travels
in the same envelope, so everything it points at is beside it.

## What you shipped

Upstream commit `8259719f8` ("preserve multiline Lispish quoted strings") at pin
`a8d34c84595d46c24cd1820d5fc0414261706412`, enabling DOTALL matching in both quote readers of
`specs/Lispish.spec`. It is the exact form this report proposed (`(?s)` on the `dquotes` and
`squotes` rules), which made the verification a comparison against our own validated candidate
rather than a fresh unknown.

## What we re-ran

Our reproduction in this directory, unchanged since the report, against the rebuilt consumer and
the grammar shipped at the pin above:

```
$ bash repro.sh <lispish_file> [Lispish.spec]
  LS-001: 8 matched / 0 differed        (was 4 matched / 4 differed at ad290bdb4)
```

The captured output is [`evidence/verified-a8d34c845.txt`](evidence/verified-a8d34c845.txt);
the pin this verification ran against is the record's `verified-against`
`a8d34c84595d46c24cd1820d5fc0414261706412`.

## What it unblocks

`SOT-FORMAT.9` in the consumer's task tree — two readers of one format agreeing on every
tracked file — is discharged: the consumer's two-reader sweep reports agreement on all five of
its tracked `.sexp` files, including the 43-form materials catalogue that had read as six.

## Where the residue lives

The fix moved the comparison one layer down, and what remains there is **not** this defect:
two quoted-numeric atoms and two escape-retained strings in one catalogue file, both
consequences of Lispish's documented extraction contract (quote-kind discard and escape
retention). The consumer classifies them under LS-002, not here. Nothing further is owed on
LS-001 from either side; thank you for the quick turnaround.
