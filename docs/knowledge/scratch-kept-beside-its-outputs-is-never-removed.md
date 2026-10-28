# The rule said each unit removes its disposable build directory — why were 268 of them still there two days later?

**Because the removal was a sentence, the scratch shared a directory with the evidence, and nothing ran at the
unit's close.** Rule 1 of `decision_orphan-incremental-sessions.md` (2026-10-26) says a build under altered
sources uses a disposable target directory "that the unit removes". Forty XTASK units built their draft crates
into `target/xtask/<unit>/draft-target` and none removed it; the clone helper (`red_clone.sh`) wrote each fixture's
full repository clone AND its compared outputs (`*.bash.out`, `*.rs.out`, `tally`, the `summary.txt` the acceptance
rows cite through a `red` link) into one `red-<epoch>` directory. Removing that directory whole would have
destroyed cited evidence, so nobody removed anything: 228 clones and 40 targets, 11.1 GB, until the recurring
cleanup's census (`ARTIFACT-CLEANUP.30`, AC0086) attributed 450 of its 784 unrecorded files to them.

## How to catch it, and what to do

- **Scratch and outputs never share a directory.** When they do, the safe removal is a per-entry judgement
  (a clone is a directory with `.git`; a cargo target carries `CACHEDIR.TAG`) — make that judgement in a tool,
  once, and keep the outputs where a whole-directory removal cannot reach them.
- **A removal promised in prose happens where a tool does it.** The same lesson in a card three days earlier
  (`a-name-one-tool-writes-is-a-path-another-tool-refuses.md`: "scratch a control writes under target/ is the
  control's to remove") did not stop the recurrence; a sweep run by the commit step after every landed unit does.
- **Census the population before acting, and validate each path by shape and content.** XTASK.9's removal
  listed 268 directories, checked each (`^target/xtask/xt[0-9]{4}/draft-target$` + `CACHEDIR.TAG` + only cargo's
  entries; `red-<epoch>/<state>` + `.git`), recorded each size, then removed — and confirmed the 1,408 output
  files beside the clones were all still present.

Evidence: target/xtask/xt0061 (targets.txt, clones.txt, remove_scratch.py, removed.tsv, kept-outputs.txt,
unrecorded-after.txt); target/artifact-cleanup/AC0086-census.txt; `docs/tasks/XTASK.md` `XTASK.9`.
