# I measured a doctrine's binary "before" my change on the same tree as "after" — why did the before binary fail everything?

**`cargo xtask` fixes its repository root at build time.** `repository_root()` in `xtask/src/main.rs` is
`env!("CARGO_MANIFEST_DIR")`'s parent, by design: the front door behaves the same from any working directory. So a
binary built in one checkout judges *that* checkout, wherever it is run. `XTASK.13` slice b2 built its "before" binary
in a temporary worktree at HEAD, removed the worktree, and ran the binary on the real tree: every probe of GUEST-GEN's
self-test was launched in the deleted worktree (it even recreated `wt-before/target/guest-gen/self-test.log`), the
self-test failed throughout, and the in-sync state read `rc=2` — a result about the measurement, not the change. The
visible clue was a probe path naming the worktree (`can't open file '…/wt-before/scripts/probe_matched_gpr_derivation.py'`).

## How to measure a binary before and after

- Run each binary on the tree it was built in: keep a worktree at HEAD (link its untracked `.app-data`, `.materials`
  and `.semulith-data` read-only), build the before binary there, and apply the corpus states to the worktree; the
  after binary is built and run in the working tree. That is a true before — HEAD's checker over HEAD's scripts and
  corpus — and the states never touch the real tree.
- Check the binary's root before trusting a run: `strings <binary> | grep <checkout path>`.
- Never compare a before binary with after scripts: a doctrine's arms spawn the tree's scripts, so the mix measures
  neither state.

Evidence: `docs/tasks/XTASK.md` XTASK.13 slice b2 (target/xtask/xt0075: red-invalid-before.txt, red-before.txt).
