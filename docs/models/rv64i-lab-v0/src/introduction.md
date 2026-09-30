# Introduction

This is the **model book** for `rv64i-lab-v0` — the project's first processor unit. It
answers one question end to end: *what documents define this processor, and how did the
project get from them to a running model?*

The project book (`docs/book/`) narrates the plan and the working practices. This book is
about **one model**. The two never restate each other: where this book needs a fact the
project already owns — a pinned digest, a record count, a gate verdict — that content is
**generated or gated**, never retyped. The tables in the materials bill are produced by
`scripts/gen_model_book.py` from the pinned dossier (`profiles/rv64i-lab-v0/`), and the
`MATERIALS-BILL` doctrine fails the commit if they drift.

## The shape contract

One canonical definition, one book (`decision_one-definition-one-book`). Every modelled
unit — CPU, MCU, DSP, device, board, SoC — gets a book of this **same shape**; a board's
book and this CPU's book differ in content, not in shape. The arc is five parts, and each
part here names the leaf that owns it:

1. **The materials** — every document that specifies the unit, pinned by exact identity,
   with what it supplies and what it does *not*. (This leaf, `MODEL-BOOKS.1`.)
2. **The gaps** — what the materials do not contain, and where the missing information
   came from instead. (`MODEL-BOOKS.2`, including the PDF investigation.)
3. **The method** — document → decision → requirement → obligation → check, with the
   judgement calls named. (`MODEL-BOOKS.3`.)
4. **The references** — how each reference model was obtained, matched and cross-checked,
   and what agreement is worth. (`MODEL-BOOKS.4`.)
5. **The evidence and the gate** — what has been demonstrated, and the honest verdict.
   (`MODEL-BOOKS.5`.)

⚠️ This book is written for a model that is **not yet finished** — the laboratory gate `G1`
reads `passed`, but the full processor gate `CPU-LAB` has not run — and it says so. A book
that waited for completion would be a retrospective; the method is the transferable part.

## The teaching mandate

This book is also a teaching text (`decision_dual-mandate-production-and-teaching`): the
reasoning is recoverable, not just the result, and **the mistakes stay in** — the encoding
provenance that shares an ancestor with one comparator, the matched profile that matched
only an instruction set. Each chapter is written so a reader could *build* from it, not
only agree with it.
