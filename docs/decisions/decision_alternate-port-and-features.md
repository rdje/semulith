# Alternate the Rust tooling port with project feature work

- **Type:** `decision`
- **Date:** `2026-10-26`
- **Status:** `active`
- **Owner / source:** the director, in session on 2026-10-26, after four consecutive `XTASK.6` port slices
  (6f–6i) had landed in one day: "Please alternate Rust tooling port and project feature implementation. Do
  not get stuck on Rust's tooling because the project work needs to progress."
answers: In what order do XTASK slices and project feature leaves run?

## The fact / decision

Units alternate: one `XTASK` slice (a Rust tooling port, `decision_rust-native-tooling.md`), then one project
feature leaf from the active P-tree frontiers in `docs/TASK_TREE.md` (`P4-SYSTEM`, `P5-BOARD`, …), then the next
`XTASK` slice. Two tooling units never land back to back while a project feature frontier is open. The
recurring cleanups (`ARTIFACT-CLEANUP`) run when due and count for neither side.

## Why

The port is support work: it moves what the gate already does into Rust without changing what the project
proves. The project's value is the modelling and verification work the P-trees carry (the CPU-SYSTEM gate's
open axes, the board's firmware probes). A run of tooling slices starves them, and the port's own measure
("nothing breaks, incrementally") does not need consecutive slices to hold.

## How to apply

- `MEMORY.md`'s `next_action` names the next unit's side explicitly; the `XTASK` tree's frontier row says
  "after the next project feature leaf".
- A tooling slice drafted ahead (as `XTASK.6` slice 6j is, in target/xtask/xt0016) waits its turn; drafting
  under `target/` while a feature chain runs is fine, landing it is not.
- The first application: after `SEMULITH-XTASK-0015` (slice 6i), the next unit is `P4-SYSTEM.14` a42bc (the
  first qualified experiment record in the dossier — G-TRACE evidenced), then slice 6j.
