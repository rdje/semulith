# Can two checks `cargo run` the same binary at the same time?

**Not on this platform.** Cargo "uplifts" a built binary from `target/debug/deps/<name>-<hash>` to
`target/debug/<name>` on *every* `cargo run`, fresh build or not, and on macOS it does so by **copy**,
not hard link: the uplifted file gets a new inode each run (measured: `/usr/bin/stat -f %i` of
`target/debug/xtask` changed across two back-to-back runs of an unchanged crate, and never equalled the
`deps/` inode). Cargo holds its build lock through the uplift and releases it *before* it executes the
binary. So when two `cargo run`s of one binary overlap, the second's uplift removes the file the first
is about to execute — `error: could not execute process `target/debug/xtask …` (never executed) … No
such file or directory` — or rewrites what the first is already executing, and the first dies with
`Killed: 9`.

## What happened

On 2026-10-27 (`XTASK.8` slice b) the project doctrine slot started running its 41 checks through a
pool. Nine of them are shims that run `cargo xtask <check>`; all nine start within the pool's first
second. Two idle-machine measurements of the pooled gate passed; the chain's own gate then refused on
`PUSH-RECORD` with the `never executed` error above. Six parallel workers each running
`cargo xtask check-registry-mirror` six times reproduced it: 4 of 36 runs failed, three of them
`Killed: 9`. The slice-b safety census had said "the cargo-based checks serialize on cargo's lock" —
true of their *builds*, false of the exec that follows.

## How to catch it, and what to do

- **Measure the uplift before trusting the lock.** Two back-to-back runs and an inode comparison
  settle whether the binary's path is stable; a six-way loop of the same command settles whether
  concurrency is safe. Both take a minute.
- **Serialize the cargo-invoking checks in one lane beside the pool**, detected from each check
  script's own text (`grep -q cargo`), so a check that starts using cargo joins the lane without a
  list to keep in step. Everything else stays pooled; the lane's sum stays well under the longest
  pooled check.
- **A pool's safety argument must cover every shared PATH, not only shared scratch.** The census
  looked at mktemp directories and the index; the uplifted binary is a shared path too.

Evidence: `docs/tasks/XTASK.md` `XTASK.8` slice b; target/xtask/xt0017 (chain.log 03:15Z, race/ 36 runs,
red_pool.sh `LANE-SERIAL`).
