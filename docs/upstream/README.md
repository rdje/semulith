# Upstream issue tracker

Defects and feedback this project raises against **other** projects it depends on. One directory
per upstream project; one directory per issue, carrying everything that project needs to reproduce
and validate the finding without access to this repository.

⛔ **This is not a place to log complaints.** An issue lands here only when it is reproducible from
the files beside it, and it carries the reproduction, not a description of one. An upstream
maintainer should be able to copy the issue directory, run one command against their own build,
and see the same result — or fail to, which is equally useful and is why the cases are files
rather than prose.

## Issue identity

`<PROJECT>-<NNN>` — stable for the life of the issue, never reused, never renumbered. The
directory name carries the id and a slug: `LS-001-multiline-string`.

## States

| State | Meaning |
| --- | --- |
| `draft` | reproducible here, not yet sent upstream |
| `reported` | sent upstream; no response yet |
| `acknowledged` | upstream has confirmed it reproduces |
| `disputed` | upstream disagrees it is a defect — their reasoning recorded in the issue |
| `fixed-upstream` | upstream has shipped a change claiming to fix it |
| `verified` | **we re-ran the reproduction against the new pin and it passes** |
| `closed` | verified, and the consumer-side workaround (if any) has been removed |
| `wontfix` | upstream declines; the issue records what we do instead |

⛔ `fixed-upstream` and `verified` are deliberately separate. A fix we have not re-run is a claim,
and adopting a new pin on the strength of a changelog entry is how a consumer inherits a
regression. **Only our own re-run moves an issue to `verified`.**

## Severity

| Severity | Test |
| --- | --- |
| `high` | wrong results with **no error** — the consumer cannot detect it |
| `medium` | wrong or missing results, but the consumer is told |
| `low` | correct results; cost is time, size or clarity |

Silence is what makes something `high`. A crash is recoverable; a plausible wrong answer is not.

## Index

| ID | Project | Title | Severity | State | Blocks |
| --- | --- | --- | --- | --- | --- |
| [`LS-001`](linkedspec/LS-001-multiline-string/REPORT.md) | LinkedSpec | a double-quoted string containing LF is not one string | `high` | `verified` | `SOT-FORMAT.9` |
| [`LS-002`](linkedspec/LS-002-atom-typing/REPORT.md) | LinkedSpec | quoted and bare atoms are indistinguishable | `medium` | `acknowledged` | — |
| [`LS-003`](linkedspec/LS-003-guide-papercuts/REPORT.md) | LinkedSpec | three first-consumer papercuts in the integration guide | `low` | `verified` | — |
