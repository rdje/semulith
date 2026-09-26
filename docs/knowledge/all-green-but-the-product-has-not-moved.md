# Every check is green and the infrastructure is beautiful — why hasn't the product moved?

**Answer: measure when each milestone was last touched; if the plan cannot *derive* when the
first milestone starts, velocity will flow forever to whatever lane is open.** Green gates
prove the work done is sound; they say nothing about whether the work done is the work that
matters. A plan with a correct dependency graph and no start condition for any milestone has
left the sequencing decision unmade — and an unmade sequencing decision gets made anyway, by
default, in favour of the lane that is already open.

## Evidence

Measured on this repository at adoption of `ROADMAP.md` v0.3:

```
$ git log --format='%H %s' -1 -- docs/tasks/P0-PROFILE.md docs/tasks/P1-LAB.md docs/tasks/P2-SCALAR.md docs/tasks/P3-BREADTH.md docs/tasks/P4-SYSTEM.md docs/tasks/P5-BOARD.md docs/tasks/P6-LINUX.md docs/tasks/P7-COMPUTER.md docs/tasks/AG-OS.md docs/tasks/MC-MULTICORE.md docs/tasks/DSP-REVIEW.md
74b081097ef0b3e04786f049006571d8cceed9a6 SEMILITH-P0-0031 (leaf P0-PROFILE.10): the profile was matched on its ISA and not its platform
$ git log --oneline 74b0810..HEAD | wc -l
27
```

27 commits since any milestone tree was last touched — and that touch was P0 *closure*, not
P1 progress. Every one of those commits was sound, gated work. The star did not move.

## The rule that closes it

- **Start conditions, not vibes:** each milestone's tree names the facts that must exist
  before its first leaf starts, in checkable form (`ROADMAP.md` v0.3 §6: P1 starts on
  `SOT-FORMAT.2` + `MODEL-METHOD.10`).
- **Every lane names its consumer** (`decision_lane-consumption`): a cross-cutting lane
  without a named consuming milestone is descoped at the next revision — an investment that
  cannot name what it unblocks is indistinguishable from an end in itself.
- **Re-verify cheaply and often:**

  ```
  $ last=$(git log --format='%H' -1 -- docs/tasks/P*.md); git log --oneline "$last"..HEAD | wc -l
  ```

  A number that only grows while the milestone rows stay `proposed` is the vacuum re-forming.
