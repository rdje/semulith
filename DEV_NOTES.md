# DEV_NOTES.md

Detailed technical notes — root cause, implementation, validation — per slice. The
engineering-continuity surface (not the public docs; that's `docs/book/`). Newest first.

Every dated entry here must reach the retrievable layer: a card under
[`docs/knowledge/`](docs/knowledge/INDEX.md), or a decision record, or an explicit decline in
the owning task leaf. That is the `LESSON-PROMOTION` doctrine, and the reason for it is that a
lesson nobody can retrieve by question is a lesson nobody has.

## _(2026-09-14)_ — a self-test reports the arms it ran, not the arms you wrote

- `docs/TASK_TREE.md` and the tree it indexes disagreed about which leaf was next: the index
  said `P0-PROFILE.2`, the tree said `.5`, and `.2` was `done`. `COMMIT.md` updates that index
  "only if the frontier changes" — a CONDITIONAL manual step, which is the shape that rots. One
  row of fourteen had drifted, and it was the only `active` tree: the single row the documented
  resume path (`MEMORY.md` → index → frontier) actually reads. A 1-in-14 drift rate is not the
  number that matters; a 1-in-1 rate on the followed row is. Gated by `FRONTIER-SYNC`.
- ⛔ **The new gate's own self-test printed `4 pass / 0 fail` while running four of fourteen
  arms.** Ten `arm` calls sat on the same physical line as the fixture call before them with no
  `;`, so bash passed `arm` and its three arguments as extra positional parameters to a function
  reading only `$1` and `$2` — discarded in silence, no error of any kind. Adding the separator
  gave `13 pass / 1 fail`, and that one failure was a real defect: two opposite drift directions
  shared a single message. Caught by counting the arms written against the arms reported, not by
  reading the code. Promoted:
  [`docs/knowledge/self-test-arms-that-never-ran.md`](docs/knowledge/self-test-arms-that-never-ran.md).
- Two blank lines inside `DOCTRINE_ENFORCEMENT.md`'s project-doctrine table split it into three
  GFM fragments, so two registered doctrines rendered as literal `| … |` text instead of rows.
  Right in the file, wrong on the page — one column over from what `TABLE-ARITY-RATCHET`
  catches, and no gate sees a blank line.

- The same mechanism, one document over: `docs/book/src/working/doctrines.md` listed 3 project
  doctrines while 5 were registered. A mirror that falls behind never **invents** a guarantee —
  it **withholds** one, on the surface a reviewer reads instead of the code. Gated by
  `REGISTRY-MIRROR`, which also caught the opposite direction unprompted (`PHANTOM`: a row added
  one step before its registration).
- The durable fix for the swallowed arms is a strict-arity guard on every self-test fixture
  helper, fired RED by deleting one `;`. A helper that ignores surplus arguments is what made the
  swallow silent; refusing them is what makes it loud.

- The third mirror had **not** drifted, and the leaf says so instead of manufacturing a defect.
  For a prevention leaf the falsification is the load-bearing box: four controls, each breaking a
  real claim in `MEMORY.md`/`LIVE_STATUS.md` and restored with `git checkout --`.
- A gate's scope can be data someone already wrote down. `TREE-CLAIMS` reads the `hot_live` rows
  of `doctrine/readme_routes.tsv` rather than carrying a file list — which also gets the
  `append_history` exclusion right for free: history must never be rewritten to match today.
- ⭐ The gates now catch each other. Registering a doctrine without mirroring it failed inside the
  same commit; the same omission had survived two prior registrations unnoticed.
- A rule keyed on words fires on prose about the rule. The frontier check matched any line
  mentioning "frontier leaf" and double-reported; anchoring it on the label fixed it, and the
  narrowing was re-fired RED — narrowing a gate is precisely the edit that can silently disable it.

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
