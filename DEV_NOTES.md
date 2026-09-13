# DEV_NOTES.md

Detailed technical notes — root cause, implementation, validation — per slice. The
engineering-continuity surface (not the public docs; that's `docs/book/`). Newest first.

Every dated entry here must reach the retrievable layer: a card under
[`docs/knowledge/`](docs/knowledge/INDEX.md), or a decision record, or an explicit decline in
the owning task leaf. That is the `LESSON-PROMOTION` doctrine, and the reason for it is that a
lesson nobody can retrieve by question is a lesson nobody has.

## _(2026-09-14)_ — a partial validator must refuse, not skip

- No JSON Schema library exists on this host and installing one would put a dependency store off
  the repository volume, so the validator is 180 tracked lines covering exactly the 17 keywords a
  census of `schemas/*.json` found. ⛔ **The soundness property is the REFUSAL.** A partial
  validator that silently ignores an unimplemented keyword reports `valid` for a document it never
  fully checked — so this one raises `UnsupportedSchema`, and a schema gaining a keyword breaks
  the gate loudly instead of widening what passes.
- ⭐ `source_semantics.category` is **not** a function of the profile's `authority`. `laboratory`
  covers both "the spec says UNSPECIFIED and we chose" and "the spec delegates to the EEI and we
  chose"; collapsing them records a laboratory policy as an architectural rule.
- The sharpest gate rule this leaf adds: `research_status: resolved` may not coexist with an
  `OPEN:` note. Both halves are true separately, which is what makes the pair convenient.
- ⛔ Two defects in the new gate were found by its own arms, not by review. It excluded `target/`
  by ABSOLUTE path — and its own fixtures live under `target/doctrine-selftest/`, so all ten arms
  failed with "no .jsonl record file found". And the cross-checks re-parsed a file that had
  already failed to parse, crashing the gate rather than failing it: a traceback is not a verdict.
- Promotion is explicitly declined in the owning leaf, with the reason.

## _(2026-09-14)_ — a running total is a memory of a measurement, not a measurement

- ⛔ Two derived counts were committed WRONG in a single session, both as running totals:
  `24 destinations governed` against a 25-row registry, and `107 self-test arms` against 112. The
  method was identical each time — take the written number, add your delta, write the sum back —
  and nothing recomputed either. Gated by `DERIVED-COUNTS`, which re-derives each from the
  population it summarises and prints the enumerator alongside the value.
- ⭐ The new gate caught its own registration: adding it made the project hold 9 doctrines where
  the page said 8, and the commit was blocked until the number was re-derived rather than bumped.
- ⛔ Its first cut was wrong in the *dangerous* direction. `sed -nE "s/.*([0-9]+) widgets.*/\1/p"`
  is greedy: on `12 widgets` the leading `.*` eats the `1` and the capture is `2`. A stale count
  could have matched a wrong extraction and read as correct. Found by a GREEN arm going red.
  Extraction is now off the front of a `grep -o` match, and a pattern not beginning with its
  number group is refused.
- The `TASK-ACCEPTANCE` recipient-tree boundary is **documented, not relaxed**. Requiring only one
  staged leaf to pass would reopen the co-staged-leaf hole that box-scoping exists to close, so a
  routed annotation lands as its own doc-only commit instead. The lesson's promotion is
  explicitly declined in the owning leaf, with the reason.

## _(2026-09-14)_ — 184 of 199 files are the same file, and an instrument that answered blind

- ⛔ **The two reference models run the SAME floating-point source.** Both vendor Berkeley
  SoftFloat; 199 `.c` files exist in both copies and **184 are byte-identical** once the release
  comment is normalized (sail 3e, spike 3d; `f64_add.c` differs by one line). A Sail-vs-Spike FP
  comparison executes one implementation twice. No current evidence is affected — this profile
  has no floating point — so it is routed to `P4-SYSTEM.7` with its measurement. Recorded:
  [`reference_softfloat-shared-ancestry`](docs/decisions/reference_softfloat-shared-ancestry.md).
- ⛔ **`strings | grep -c softfloat` returned 0 for both binaries and that was BLINDNESS, not
  absence.** `nm -a` showed why: spike carries 649,743 symbols, the Sail release binary 400. A
  stripped binary cannot answer the question. The `0` was one step away from being written down
  as a finding; the source was cloned instead, at the exact commit the binary's `--build-info`
  reports. Pick the instrument that can see, then read it.
- ⭐ Independence cuts in unexpected directions. Encoding is **not** shared — spike generates
  `encoding.h` from `riscv-opcodes` while the Sail model hand-writes 59 `encdec` files and never
  mentions it — so *our* assembler shares an ancestor with spike and not with sail, which makes
  sail decoding our bytes an independent confirmation and spike doing so not one.
- `docs/tasks/P0-PROFILE.md` hit the per-part **ceiling** (73,317 B > 65,536) and the completed-leaf
  evidence was split to `docs/tasks/archive/`, unedited. The ceiling was obeyed, not raised, which
  is what the registry's own header prescribes. Checked that the split did not move pressure
  somewhere ungoverned: `git ls-files -- docs/tasks` is recursive, so the archive still counts
  toward the family aggregate (240,293 B against a 393,216 ceiling).
- 🔎 **A new mirror-drift instance, outside what `MIRROR-DRIFT` gated.** `LIVE_STATUS.md` claimed
  "24 destinations governed" while `doctrine/readme_routes.tsv` holds 25 rows and the gate prints
  25 — stale since `SEMULITH-P0-0013` added the `profiles/` row. Corrected here; the *class*
  (a live document restating a count that a registry owns) is not yet mechanized, and `TREE-CLAIMS`
  only covers task-tree facts. Owner: `MIRROR-DRIFT.4`, opened next.
- 🔎 `TASK-ACCEPTANCE` requires every staged `docs/tasks/*.md` to carry a ticked checklist. It
  cannot tell the leaf that OWNS a change from a tree that RECEIVES a routed finding, so
  annotating `P4-SYSTEM.7` had to be split into its own commit — P4 has not started and ticking
  its template would be a lie. Splitting is the right answer; the gate not distinguishing the two
  roles is the defect. Owner: `MIRROR-DRIFT.4` alongside the registry-count class.
- Promoted: [`docs/knowledge/zero-hits-absence-or-blindness.md`](docs/knowledge/zero-hits-absence-or-blindness.md).

## _(2026-09-14)_ — the pinned spec has no encodings, and a shorter trace is not agreement

- ⛔ **The specification we pinned does not contain instruction encodings.** Census over all six
  artifacts: `grep -cE '[01]{7}'` -> 0 every time; the format diagrams are images (31 in the
  RV32I chapter). The SEMANTICS are all present in prose, which is the half expected values need,
  so encodings were pinned separately from `riscv-opcodes` and recorded as a *different*
  provenance. That source is upstream of both models, so encoding agreement is not independent
  evidence — only semantic agreement is, and that is what the experiment tests.
- ⭐ Unplanned corroboration: the encoding table holds exactly 52 instructions for this extension
  set, and `P0-PROFILE.1` enumerated exactly 52 by hand from the prose without it. Symmetric
  difference: none. Two independent routes to the same closed set.
- ⛔ **The comparator reported a false pass and running it is what found that.** Walking only the
  overlapping prefix, it printed `AGREE over 2 aligned step(s)` for a run where one model trapped
  and the other stopped. The prefixes agreed; the observation did not. Promoted:
  [`docs/knowledge/a-shorter-trace-is-not-agreement.md`](docs/knowledge/a-shorter-trace-is-not-agreement.md).
- ⭐ **Two models agreeing means nothing until the agreement is shown to be doing work.** Flipping
  one configuration key — the misaligned policy — with the same binary produced a real first
  divergence. That control is why "matched profile" is now a measurement. The project gate now
  refuses an experiment record that claims agreement without naming such a control.
- 🔎 `docs/tasks/` crossed its advisory health target (214,002 B against 196,608). Not a ceiling
  (393,216 aggregate, 65,536 per part) and nothing is breached, but `P0-PROFILE.md` is at 49,521 B
  — 76% of the per-part ceiling — because completed-leaf evidence accumulates in-tree by design.
  The mechanism intended for this is archive compaction, and no tree has needed it yet.

## _(2026-09-14)_ — availability is not identity, and a budget can be wrong in your favour

- ⛔ **The package manager had a formula called `sail`. It deploys WordPress sites to
  DigitalOcean.** An exact name collision with the Sail ISA specification language: the lookup
  succeeded, the version was current, the licence was real, and the referent was wrong. Had the
  check been `brew info sail >/dev/null && echo available`, the dossier would carry a sentence
  that is false, sourced and reproducible. Identity needs a field only the real thing can
  produce — here `--build-info`, which prints an upstream release, a git sha and the compiler.
  Promoted: [`docs/knowledge/availability-is-not-identity.md`](docs/knowledge/availability-is-not-identity.md).
- The roadmap priced reference acquisition as the first activity whose cost was *not obviously
  bounded*, assuming an OCaml/opam build of Sail. Release 0.14 ships a native binary for this
  host's architecture, so Sail was the **cheapest** candidate, not the dearest. Three models
  obtained in one leaf. The estimate was wrong; the reasoning behind it ("acquisition is work
  with observable outcomes") was right and is untouched.
- ⛔ **The Sail model will not tell you what configuration it ran with.**
  `--print-default-config` ignores `--config-override` — byte-identical dumps. `EVIDENCE_AND_GATES`
  §5 wants the *effective* configuration, so it is recorded as (default) + (tracked override)
  with the merge explicitly labelled **ours**. The model's one self-description is
  `--print-isa-string`, which is why `rv64i_zvl32b` is pinned and re-derived.
- Having three binaries is not having three opinions. The gate now refuses a candidate whose
  `lineage` field is missing, because an unasked independence question reads exactly like an
  answered one.

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
