# CHANGELOG shard — _(2026-09-13)_ … _(2026-09-13)_

> Sharded from `CHANGELOG.md` when it crossed its 64 KiB ceiling (`doctrine/readme_routes.tsv`).
> Entries in a shard are **never edited after the shard** — git history is canonical.

## _(2026-09-13)_ — a delivered package is not ingested until its rot sources are removed

- Planning package v0.2 arrived in the worktree as 15 untracked files plus two modified
  tracked ones, and every problem it carried was invisible to a reader: `shasum -a 256 -c
  MANIFEST.sha256` printed 25 × `OK` and `rc=0`. The manifest was *correct and already
  doomed* — two of its rows (`README.md`, `ROADMAP.md`) name files this repository exists to
  change. A control whose failure is scheduled is not a control.
- The enforcer found the one defect a human review had not: `scripts/check_doctrines.sh` →
  `README-STABILITY: README.md no longer links README_POLICY.md`. The delivered README was a
  perfectly good package front page and a policy breach, because replacing a landing page
  silently drops whatever contract the landing page carried. Promoted:
  [`docs/knowledge/re-derivable-vs-cited-evidence.md`](docs/knowledge/re-derivable-vs-cited-evidence.md).
- Two byte-identical copies of the archogen integration contract shipped together. Both
  passed every gate. Promoted:
  [`docs/knowledge/duplicate-document-ownership.md`](docs/knowledge/duplicate-document-ownership.md).
- ⛔ **Two sibling doctrines disagreed about what an instrument is.** `GAP-CLAIM-CENSUS` prints
  `git grep -n '<symbol>' -- src scripts | wc -l` in its own failure hint and accepts it as a
  census; `TASK-ACCEPTANCE`'s default signature family recognises `git ls-files|log -S|…` and
  **not** `git grep` or `wc -l`. Obeying one gate produced evidence the other refused. Fixed
  through the sanctioned `.doctrine/evidence_tokens.txt` seam, never by weakening the evidence
  — and the widened gate was then fired RED (a prose-only box → `rc=1`) to prove it still
  discriminates. Promoted:
  [`docs/knowledge/census-instrument-signature-gap.md`](docs/knowledge/census-instrument-signature-gap.md).
  Upstream owner: this is a `bedrock` template defect, not a Semulith one.

