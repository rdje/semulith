# CHANGELOG shard — _(2026-09-14)_ … _(2026-09-14)_

> Sharded from `CHANGELOG.md` when it crossed its 64 KiB ceiling (`doctrine/readme_routes.tsv`).
> Entries in a shard are **never edited after the shard** — git history is canonical.

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

