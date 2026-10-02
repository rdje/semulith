# What the materials do not contain

A materials bill that lists only what things provide is how a project comes to believe
it has information it never acquired. This chapter is the bill's other half.

## The absences that are the design

Timers and interrupt controllers are **absent by contract**, declared as data in
`board.sexp` with the obligations the absences satisfy — they are not missing features,
and adding them would be a composition *rejection* (`D-BOARD-NO-TIMER-IRQ`): the CPU
contract excludes every guest-reachable time source and admits no deliverable
asynchronous interrupt. Both devices' interrupt lines are unconnected *and declared so*;
drivers poll. The same discipline reaches inside the NIC: its MMIO-readable counters
(FREE_RUN, GPT_CNT) are guest-readable time sources, frozen or guest-deterministic by
the composition (`REQ-D-NIC-TIME-SOURCES`), never wired to wall-clock.

## The pending verdicts, with their owners

- ~~**The composition verdict** — `P5-BOARD.4`~~ **landed** (`2026-10-02`): **ACCEPTED** —
  every CPU assumption matched to a named board/device guarantee, re-decided on every
  commit by the BOARD-VERDICT doctrine ([The composition verdict](the-verdict.md)). The
  board is now a *checked* platform, conditional on the CPU's acceptance trajectory.
- ~~**The strap values**~~ **landed** with the verdict: D32 tied high (32-bit native
  mode), SPEED_SEL at its internal pull-up (`D-BOARD-NIC-STRAPS`).
- **The firmware probes** — `P5-BOARD.5`, gated on the CPU's acceptance trajectory: small
  firmware that finds and interacts with the devices it expects, with failures
  classified to an explicit owner — never an unattributed "emulator bug".
- **The capability manifest** — `P5-BOARD.6`: the derived, never handwritten export for
  archogen's compatibility checker.

## What the board never owed

Its own specification (a board composes pinned units), an encoding space (the
processor's encodings, pinned by digest), reference models of its own, and — by
contract, again — any live network surface inside an evidence claim.
