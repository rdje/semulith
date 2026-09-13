# DEV_NOTES.md

Detailed technical notes — root cause, implementation, validation — per slice. The
engineering-continuity surface (not the public docs; that's `docs/book/`). Newest first.

Every dated entry here must reach the retrievable layer: a card under
[`docs/knowledge/`](docs/knowledge/INDEX.md), or a decision record, or an explicit decline in
the owning task leaf. That is the `LESSON-PROMOTION` doctrine, and the reason for it is that a
lesson nobody can retrieve by question is a lesson nobody has.

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

## _(2026-09-04)_ — a template's trial must include the first commit

- Every gate was green on the generated project and the first commit still failed: the doctrines judge STAGED
  code, and nothing had been staged until the user tried. Trial the path a user walks, to its end.
- `grep -c` prints `0` and exits 1. `$(grep -c … || echo 0)` therefore yields `0⏎0` — a second line — which
  here started a flush-left line inside a checklist bullet and hid its evidence from the box-scoped extractor.
  Capture the count, then default the empty case; never append a fallback to grep's own output.

## _(2026-09-04)_ — a green gate that judges nothing is the class a template must not ship

- Two of the four doctrine ports in `.2.6` were wrong on first run and their own RED self-test arms said so:
  a `python3 - <<'PY'` detector whose stdin was the heredoc (every arm read 0 rows), and a `grep -c … | grep -qx 0`
  control under `pipefail` (`grep -c` prints 0 and exits 1). A self-test with only GREEN arms would have passed both.
- The neutrality bar is measured, not felt: `grep -ciE 'grammar|parser|…'` over each ported script → 0, after the
  generic uses of "corpus" and "grammar" were re-worded ("tree", "syntax") so the count means what it says.
