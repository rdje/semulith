# LS-002 — quoted and bare atoms are indistinguishable

| | |
| --- | --- |
| **ID** | `LS-002` |
| **Project** | LinkedSpec (`rdje/linkedspec`) |
| **Component** | `specs/Lispish.spec` — the parent rules, as documented |
| **Severity** | `medium` — correct per the documented contract; blocks a use the contract does not claim |
| **State** | `acknowledged` `2026-09-26` — upstream took ownership (`.83.1 owned`, commit `8259719f8`) |
| **Raised** | `2026-09-20` |
| **Affects** | `ad290bdb4`; see `../README.md` |
| **Blocks** | nothing today; would block using Lispish for a format that is **written** as well as read |
| **Fix** | none proposed — this is a design question for you, not a patch |
| **Reproduce** | `bash repro.sh <lispish_file> [Lispish.spec]` |
| **Validate** | [`VALIDATE.md`](VALIDATE.md) — what is in this sub-tree and how to reproduce |

## This is documented behaviour, not a defect

The guide says it plainly: *"Lispish's parent rules discard distinctions between symbols, quoted
strings and numeric tokens."* We raise it only because its consequence for a **source-of-truth
format** may not be obvious from that sentence, and we are the first consumer to hit it.

## What it looks like

```
(v 20260911)      ->  ["r",["v","20260911"]]
(v "20260911")    ->  ["r",["v","20260911"]]      same value, different source text
(v 1.0)           ->  ["r",["v","1.0"]]
(v "1.0")         ->  ["r",["v","1.0"]]
```

## Why a consumer may care

A consumer **cannot round-trip**: having read a file, it cannot write one back that re-reads
identically, because the quoting is not recoverable. For semulith that means Lispish alone cannot
be the basis of a format that is both generated and consumed, and the type of every atom must come
from a schema rather than from the file. That is a workable answer, and it is the one we will take
— but it is an architectural consequence rather than a detail, so it belongs on the record.

If `SESSION-STARTUP-READING.83.1-.83.3` is already the home for strict-document work, a token-kind
channel may belong beside it. Two shapes would both solve our case, and we have no preference:
a grammar variant that preserves token kind, or an optional side-channel reporting the kind and
source span of each atom.

## What we are NOT asking for

Not a change to the shipped Lispish grammar's behaviour. It does what it documents, and other
consumers may depend on exactly this collapse.
