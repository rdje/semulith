# Engineering rules

`RULES.md` is the short normative layer: stable IDs, one sentence each, no rationale. Rationale
lives in the design documents; the rules themselves are meant to be citable from a task leaf or
an evidence record without quoting a paragraph.

The prefixes are the project's vocabulary, and they appear throughout this book:

| Prefix | Governs |
| --- | --- |
| `SCP-` | scope and authority — what a support claim must identify |
| `OWN-` | canonical definitions, generation, and single ownership |
| `SEM-` | target semantics — outcomes, numerics, sequencing, addressing, undefined cases |
| `ENV-` | the environment and execution contract |
| `EVD-` | evidence and what a claim is allowed to say |
| `RUST-` | implementation language, tracing, performance, portability |
| `AI-` | the AI-assisted workflow and its limits as evidence |
| `SRC-` | source handling, artifact terms, and fabrication |

Included verbatim below — the book does not paraphrase a rule, because a paraphrase is a second
owner and `OWN-01` is the rule that there is only one.

{{#include ../../../../RULES.md}}
