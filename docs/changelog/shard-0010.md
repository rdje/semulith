# CHANGELOG shard — _(2026-09-14)_ … _(2026-09-14)_

> Sharded from `CHANGELOG.md` when it crossed its 64 KiB ceiling (`doctrine/readme_routes.tsv`).
> Entries in a shard are **never edited after the shard** — git history is canonical.

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

