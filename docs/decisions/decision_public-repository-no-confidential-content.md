# This repository is public and carries no confidential content

- **Type:** `project`
- **Date:** `2026-09-13`
- **Status:** `active`
- **Owner / source:** director statement, 2026-09-13

## The fact / decision

The `semulith` GitHub repository is public, and nothing in it is confidential.

## Why

Stated directly by the director. It settles a question that otherwise gets re-litigated every
time evidence has to be recorded: whether a command, a URL, a hash, a tool version, or a
failing output may be written into a tracked file.

## Why it matters here

This project's evidence rules (`EVD-08`, `SRC-01`, `SRC-03`) require reports to carry input
fingerprints, commands, actual results, and honest limitations. That discipline is only
cheap when there is no redaction step. It also means the public surface — `README.md`, the
mdBook, `ROADMAP.md` — is read by people outside the project, so scope-honesty statements are
load-bearing rather than decorative.

## How to apply

- Record commands, versions, hashes, source URLs, and real tool output in task-trees, decision
  records, and the book without redaction.
- Keep third-party material governed by its own terms: public does not mean redistributable.
  `SRC-01` still requires recording the actual terms before shipping any acquired artifact.
- Do not commit credentials, tokens, or machine-local absolute paths — those are excluded for
  reasons unrelated to confidentiality, and the `DOCPATH` doctrine already gates the last one.

Related: [[decision_delivery-provenance-is-frozen]].
